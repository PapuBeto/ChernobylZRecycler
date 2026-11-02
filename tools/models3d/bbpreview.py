"""Fase Blockbench — previews isometricas TEXTURIZADAS desde .bbmodel.

Carga cada proyecto .bbmodel (elementos + textura incrustada), decodifica el
PNG y renderiza una vista isometrica muestreando la textura por tesela
(mismo encuadre, luz y sombra de apoyo que render.py). Sirve para verificar
visualmente agujas, rejillas, etiquetas y desgaste pintado antes de construir
el jar; los renders son la 'captura del modelo terminado'.

Uso:  python -m tools.models3d.bbpreview [ids...]
Salida:  docs/models3d/<id>.png  +  hoja_<zona>.png (regeneradas)
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from tools.models3d.render import (
    FONDO,
    RESAMPLE,
    SOMBRA_ALFA,
    SOMBRA_CARA,
    aplicar,
    casco_hull,
    clave_sombra,
    cargar_specs,
    matriz_rot,
    proyectar,
)

RAIZ = Path(__file__).resolve().parents[2]
FUENTE = RAIZ / "tools" / "models3d" / "blockbench"
SALIDA = RAIZ / "docs" / "models3d"

CARAS_MC = ("north", "south", "east", "west", "up", "down")
NORMAL = {
    "north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0),
    "up": (0, 1, 0), "down": (0, -1, 0),
}


def _rango_cara(nombre, desde, hasta):
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    if nombre in ("up", "down"):
        return (x0, x1), (z0, z1)
    if nombre in ("north", "south"):
        return (x0, x1), (y0, y1)
    return (y0, y1), (z0, z1)  # east / west


def _punto_cara(nombre, desde, hasta, a, b):
    """Punto NO rotado en el mundo para el vertice (a, b) de la cara."""
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    if nombre == "up":
        return (a, y1, b)
    if nombre == "down":
        return (a, y0, b)
    if nombre == "south":
        return (a, b, z1)
    if nombre == "north":
        return (a, b, z0)
    if nombre == "east":
        return (x1, a, b)
    return (x0, a, b)


def _uv_cara(nombre, desde, hasta, rect, a, b):
    """Coordenadas uv de un punto (a,b) de la cara — convención MC/Blockbench.

    sur:  u->+x, v->-y | norte: u->-x, v->-y | este: u->-z, v->-y
    oeste: u->+z, v->-y | arriba: u->+x, v->+z | abajo: u->+x, v->-z
    """
    u1, v1, u2, v2 = rect
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    dx = max(x1 - x0, 1e-9)
    dy = max(y1 - y0, 1e-9)
    dz = max(z1 - z0, 1e-9)
    sx = (u2 - u1) / dx
    sy = (v2 - v1) / dy
    su = (u2 - u1) / dz
    sz = (v2 - v1) / dz
    if nombre == "south":
        u = u1 + (a - x0) * sx
        v = v2 - (b - y0) * sy
    elif nombre == "north":
        u = u2 - (a - x0) * sx
        v = v2 - (b - y0) * sy
    elif nombre == "east":
        u = u2 - (b - z0) * su
        v = v2 - (a - y0) * sy
    elif nombre == "west":
        u = u1 + (b - z0) * su
        v = v2 - (a - y0) * sy
    elif nombre == "up":
        u = u1 + (a - x0) * sx
        v = v1 + (b - z0) * sz
    else:  # down
        u = u1 + (a - x0) * sx
        v = v2 - (b - z0) * sz
    return u, v


def _cargar(id_item):
    ruta = FUENTE / (id_item + ".bbmodel")
    proyecto = json.loads(ruta.read_text(encoding="utf-8"))
    texturas = proyecto.get("textures") or []
    if not texturas or not (texturas[0].get("source") or "").startswith("data:image/png;base64,"):
        raise ValueError(f"{id_item}: sin textura incrustada")
    png = base64.b64decode(texturas[0]["source"].split(",", 1)[1])
    textura = Image.open(io.BytesIO(png)).convert("RGBA")
    res = proyecto.get("resolution", {"width": 32, "height": 32})
    lado_uv = float(res.get("width", 32))
    factor = textura.size[0] / lado_uv

    elementos = []
    for el in proyecto.get("elements", []):
        desde = tuple(float(v) for v in el["from"])
        hasta = tuple(float(v) for v in el["to"])
        matriz, origen = None, (8.0, 8.0, 8.0)
        rot = el.get("rotation")
        if isinstance(rot, (list, tuple)) and any(abs(v) > 0 for v in rot):
            i = next(i for i, v in enumerate(rot) if abs(v) > 0)
            matriz = matriz_rot(("x", "y", "z")[i], float(rot[i]))
            origen = tuple(float(v) for v in el.get("origin", (8.0, 8.0, 8.0)))
        caras = {}
        for nombre, f in (el.get("faces") or {}).items():
            t = f.get("texture")
            caras[nombre] = {
                "uv": tuple(float(v) for v in f["uv"]),
                "visible": t is not None and (not isinstance(t, int) or 0 <= t < len(texturas)),
            }
        elementos.append({
            "desde": desde, "hasta": hasta, "matriz": matriz, "origen": origen,
            "caras": caras, "nombre": el.get("name", ""),
        })
    return {"textura": textura, "factor": factor, "elementos": elementos}


def _rotar_puntos(m, origen, pts):
    out = []
    for p in pts:
        q = (p[0] - origen[0], p[1] - origen[1], p[2] - origen[2])
        r = aplicar(m, q)
        out.append((r[0] + origen[0], r[1] + origen[1], r[2] + origen[2]))
    return out


def _teselas_datos(elementos):
    """[(elemento, nombre cara, pts derotados 4 x (a..) , uvs 4, sombra_clave, prof)]"""
    salida = []
    for el in elementos:
        m, origen = el["matriz"], el["origen"]
        for nombre, datos in el["caras"].items():
            if nombre not in CARAS_MC or not datos["visible"]:
                continue
            n = aplicar(m, NORMAL[nombre]) if m is not None else NORMAL[nombre]
            if n[0] + n[1] + n[2] <= 0:
                continue
            (r0, r1), (s0, s1) = _rango_cara(nombre, el["desde"], el["hasta"])
            for a in range(int(math.floor(r0)), int(math.ceil(r1))):
                for b in range(int(math.floor(s0)), int(math.ceil(s1))):
                    a_hi, b_hi = min(a + 1, r1), min(b + 1, s1)
                    pts_m = [
                        _punto_cara(nombre, el["desde"], el["hasta"], a, b),
                        _punto_cara(nombre, el["desde"], el["hasta"], a_hi, b),
                        _punto_cara(nombre, el["desde"], el["hasta"], a_hi, b_hi),
                        _punto_cara(nombre, el["desde"], el["hasta"], a, b_hi),
                    ]
                    uvs = [
                        _uv_cara(nombre, el["desde"], el["hasta"], datos["uv"], ca, cb)
                        for ca, cb in ((a, b), (a_hi, b), (a_hi, b_hi), (a, b_hi))
                    ]
                    if m is not None:
                        pts = _rotar_puntos(m, origen, pts_m)
                    else:
                        pts = pts_m
                    prof = sum(c[0] + c[1] + c[2] for c in pts) / 4
                    salida.append((pts, uvs, clave_sombra(n), prof))
    return salida


def _tesela_warp(textura, uvs, factor, pix, sombra):
    """Warp afin de la textura al paralelogramo de la tesela + sombreado.

    Devuelve (imagen RGBA, offset_x, offset_y) o None si es degenerada; la
    esquina (0,0) del fragmento queda en el offset devuelto.
    """
    p00, p10, p01 = pix[0], pix[1], pix[3]
    (u00, v00), (u10, v10), (u01, v01) = uvs[0], uvs[1], uvs[3]
    s00 = (u00 * factor, v00 * factor)
    s10 = (u10 * factor, v10 * factor)
    s01 = (u01 * factor, v01 * factor)
    U = (p10[0] - p00[0], p10[1] - p00[1])
    V = (p01[0] - p00[0], p01[1] - p00[1])
    Su = (s10[0] - s00[0], s10[1] - s00[1])
    Sv = (s01[0] - s00[0], s01[1] - s00[1])
    det = U[0] * V[1] - U[1] * V[0]
    if abs(det) < 1e-9:
        return None
    pxs = [p00[0], p10[0], p01[0], p00[0] + U[0] + V[0]]
    pys = [p00[1], p10[1], p01[1], p00[1] + U[1] + V[1]]
    bx, by = math.floor(min(pxs)), math.floor(min(pys))
    w = int(math.ceil(max(pxs))) - bx
    h = int(math.ceil(max(pys))) - by
    w, h = max(w, 1), max(h, 1)

    a = (Su[0] * V[1] - Sv[0] * U[1]) / det
    b = (Sv[0] * U[0] - Su[0] * V[0]) / det
    d = (Su[1] * V[1] - Sv[1] * U[1]) / det
    e = (Sv[1] * U[0] - Su[1] * V[0]) / det
    # el pixel (i,j) del fragmento cae en el lienzo en (bx+i, by+j): la
    # constante lleva el origen del recorte a la esquina p00 (con subpixel).
    c = s00[0] + a * (bx - p00[0]) + b * (by - p00[1])
    f = s00[1] + d * (bx - p00[0]) + e * (by - p00[1])

    warp = textura.transform((w, h), Image.AFFINE, (a, b, c, d, e, f))
    gris = SOMBRA_CARA[sombra]
    sensor = Image.new("RGBA", (w, h), tuple(int(round(255 * gris)) for _ in range(3)) + (255,))
    fragmento = ImageChops.multiply(warp, sensor)
    # recorta al paralelogramo de la tesela (el bbox sobra y pintaria textura vecina)
    poligono = Image.new("L", (w, h), 0)
    ImageDraw.Draw(poligono).polygon(
        [(qx - bx, qy - by) for qx, qy in pix], fill=255
    )
    fragmento.putalpha(ImageChops.multiply(fragmento.getchannel("A"), poligono))
    return fragmento, bx, by


def render_bb(datos, canvas=256, ss=2):
    """Renderiza un proyecto bbmodel a PNG RGB de `canvas` px."""
    textura, factor, elementos = datos["textura"], datos["factor"], datos["elementos"]

    esquinas_todas = []
    for el in elementos:
        x0, y0, z0 = el["desde"]
        x1, y1, z1 = el["hasta"]
        cs = [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1),
              (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]
        if el["matriz"] is not None:
            cs = _rotar_puntos(el["matriz"], el["origen"], cs)
        esquinas_todas += cs
    proys = [proyectar(*c) for c in esquinas_todas]
    huella = [(c[0], c[2]) for c in esquinas_todas]
    proys += [proyectar(x, 0.0, z) for x, z in casco_hull(huella)]

    us = [p[0] for p in proys]
    vs = [p[1] for p in proys]
    umin, umax, vmin, vmax = min(us), max(us), min(vs), max(vs)
    margen = 0.14
    interno = canvas * (1 - 2 * margen)
    escala_px = interno / max(max(umax - umin, 1e-6), max(vmax - vmin, 1e-6))
    ox = canvas / 2 - (umin + umax) / 2 * escala_px
    oy = canvas / 2 - (vmin + vmax) / 2 * escala_px
    total = canvas * ss

    def a_pixel(p):
        return (ox + p[0] * escala_px) * ss, (oy + p[1] * escala_px) * ss

    # 1) lienzo + sombra de apoyo
    imagen = Image.new("RGBA", (total, total), FONDO + (255,))
    capa = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    dibujo = ImageDraw.Draw(capa)
    dibujo.polygon(
        [a_pixel(proyectar(x, 0.0, z)) for x, z in casco_hull(huella)],
        fill=(20, 18, 16, SOMBRA_ALFA),
    )
    capa = capa.filter(ImageFilter.GaussianBlur(radius=2.5 * ss))
    imagen = Image.alpha_composite(imagen, capa).convert("RGB")

    # 2) teselas ordenadas por profundidad, con muestreo afin
    teselas = []
    for pts, uvs, sombra, prof in _teselas_datos(elementos):
        pix = [a_pixel(proyectar(*c)) for c in pts]
        teselas.append((prof, pix, uvs, sombra))
    teselas.sort(key=lambda t: t[0])

    for prof, pix, uvs, sombra in teselas:
        resultado = _tesela_warp(textura, uvs, factor, pix, sombra)
        if resultado is None:
            continue
        fragmento, fx, fy = resultado
        if fragmento.size[0] <= 0 or fragmento.size[1] <= 0:
            continue
        imagen.paste(fragmento, (fx, fy), fragmento)
    return imagen.resize((canvas, canvas), RESAMPLE)


def hoja_zona(imagenes, camino, celda=256, hueco=8):
    n = len(imagenes)
    columnas = min(4, max(1, n))
    filas = math.ceil(n / columnas)
    ancho = columnas * celda + hueco * (columnas + 1)
    alto = filas * celda + hueco * (filas + 1)
    pagina = Image.new("RGB", (ancho, alto), (222, 222, 220))
    for i, img in enumerate(imagenes):
        col, fila = i % columnas, i // columnas
        pagina.paste(img, (hueco + col * (celda + hueco), hueco + fila * (celda + hueco)))
    pagina.save(camino)
    return camino


def render_item(id_item, canvas=256):
    datos = _cargar(id_item)
    return render_bb(datos, canvas=canvas)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Previews isometricas texturizadas (.bbmodel).")
    parser.add_argument("ids", nargs="*", help="ids concretos; vacio = todos los .bbmodel")
    parser.add_argument("--canvas", type=int, default=256)
    args = parser.parse_args(argv)

    ids = args.ids or sorted(p.stem for p in FUENTE.glob("*.bbmodel"))
    if not ids:
        print("no hay .bbmodel en %s" % FUENTE.relative_to(RAIZ))
        return 1

    SALIDA.mkdir(parents=True, exist_ok=True)
    por_zona = {}
    for id_item in ids:
        try:
            img = render_item(id_item, canvas=args.canvas)
        except Exception as e:
            print(f"ERROR [{id_item}] {e}")
            return 1
        zona = _zona_de(id_item)
        por_zona.setdefault(zona, []).append((id_item, img))
        camino = SALIDA / f"{id_item}.png"
        img.save(camino)
        print(f"ok  {id_item} ({zona}) -> {camino.relative_to(RAIZ)}")

    for zona, lista in sorted(por_zona.items()):
        camino = hoja_zona([img for _, img in lista], SALIDA / f"hoja_{zona}.png")
        print(f"ok  hoja {zona} ({len(lista)} items) -> {camino.relative_to(RAIZ)}")
    return 0


def _zona_de(id_item):
    for spec in cargar_specs():
        if spec.id == id_item:
            return spec.zona
    return "varios"


if __name__ == "__main__":
    sys.exit(main())
