"""Fase 0 — renderizador de previews isométricas.

Pinta una Spec (cubos en rejilla 0..16) como imagen isométrica sobre fondo
gris neutro, con sombra de apoyo e iluminación por cara. Sirve para calibrar
silueta, escala, paleta y desgaste antes de construir modelos y atlas reales.
Las previews son mockups de color plano: el acabado final llega con las
texturas del atlas (Fase 1+).

Uso (desde la raíz del repo):
    python -m tools.models3d.render                       # todas las specs
    python -m tools.models3d.render contador_geiger_pripyat

Salida:
    docs/models3d/<id>.png        render individual (256x256)
    docs/models3d/hoja_<zona>.png hoja de contacto por zona
"""

from __future__ import annotations

import argparse
import importlib
import math
import pkgutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from tools.models3d.palette import resolver
from tools.models3d.spec import Spec

ROOT = Path(__file__).resolve().parents[2]
SALIDA = ROOT / "docs" / "models3d"

C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))

# Luz desde arriba-entre-norte y oeste: cara superior blanc, frente medio,
# lateral más oscuro. Claves igual que CARAS en spec.py.
SOMBRA_CARA = {
    "arriba": 1.00,
    "sur": 0.80,    # cara frontal (visible, a la izquierda del render)
    "este": 0.62,   # cara lateral (visible, a la derecha)
    "norte": 0.52,
    "oeste": 0.46,
    "abajo": 0.36,
}

FONDO = (198, 198, 198)
SOMBRA_ALFA = 70

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # Pillow antiguo
    RESAMPLE = Image.LANCZOS

# Normales de cara por nombre (el eje fijo queda determinado por _def_caras).
NORMAL_DE = {
    "arriba": (0, 1, 0),
    "abajo": (0, -1, 0),
    "sur": (0, 0, 1),
    "norte": (0, 0, -1),
    "este": (1, 0, 0),
    "oeste": (-1, 0, 0),
}


# ---------------------------------------------------------------------------
# Geometría
# ---------------------------------------------------------------------------

def proyectar(x, y, z):
    """Proyección isométrica; Y de pantalla crece hacia abajo (PIL).

    +x va hacia abajo-derecha, +z hacia abajo-izquierda, +y hacia arriba.
    Cámara en el octante (+x,+y,+z): caras visibles = sur (izquierda),
    este (derecha) y arriba.
    """
    return (x - z) * C30, (x + z) * S30 - y


def matriz_rot(eje, angulo):
    a = math.radians(angulo)
    c, s = math.cos(a), math.sin(a)
    if eje == "x":
        return ((1, 0, 0), (0, c, -s), (0, s, c))
    if eje == "y":
        return ((c, 0, s), (0, 1, 0), (-s, 0, c))
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))


def aplicar(m, p):
    return (
        m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2],
        m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2],
        m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2],
    )


def rotar_punto(m, p, origen):
    q = (p[0] - origen[0], p[1] - origen[1], p[2] - origen[2])
    r = aplicar(m, q)
    return (r[0] + origen[0], r[1] + origen[1], r[2] + origen[2])


def esquinas(desde, hasta):
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    return (
        (x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1),
        (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1),
    )


def clave_sombra(n):
    ax, ay, az = abs(n[0]), abs(n[1]), abs(n[2])
    if ay >= ax and ay >= az:
        return "arriba" if n[1] > 0 else "abajo"
    if az >= ax:
        return "sur" if n[2] > 0 else "norte"
    return "este" if n[0] > 0 else "oeste"


def tono(color, f):
    return tuple(max(0, min(255, int(round(c * f)))) for c in color)


def casco_hull(puntos):
    """Casco convexo 2D (monotone chain) de la huella de sombra."""
    pts = sorted(set(puntos))

    def cruce(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def mitad(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and cruce(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h

    baja = mitad(pts)
    alta = mitad(reversed(pts))
    return baja[:-1] + alta[:-1]


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def _def_caras(desde, hasta):
    """Six faces del cubo: (nombre, generador de puntos, rango A, rango B).

    El generador construye el punto del modelo (sin rotar) para una tesela;
    los rangos barren los dos ejes libres de la cara.
    """
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    return (
        ("arriba", lambda a, b: (a, y1, b), (x0, x1), (z0, z1)),
        ("abajo",  lambda a, b: (a, y0, b), (x0, x1), (z0, z1)),
        ("sur",    lambda a, b: (a, b, z1), (x0, x1), (y0, y1)),
        ("norte",  lambda a, b: (a, b, z0), (x0, x1), (y0, y1)),
        ("este",   lambda a, b: (x1, a, b), (y0, y1), (z0, z1)),
        ("oeste",  lambda a, b: (x0, a, b), (y0, y1), (z0, z1)),
    )


def _preparar_piezas(spec):
    """Devuelve [(pieza, esquinas_rotadas, matriz|None)] para encuadre."""
    preparadas = []
    for pieza in spec.piezas:
        m = None
        if pieza.rotacion is not None:
            r = pieza.rotacion
            m = matriz_rot(r.eje, r.angulo)
        cs = esquinas(pieza.desde, pieza.hasta)
        if m is not None:
            cs = [rotar_punto(m, c, pieza.rotacion.origen) for c in cs]
        preparadas.append((pieza, cs, m))
    return preparadas


def _fit(puntos_proyectados, canvas, margen=0.14):
    """Devuelve (escala, offset_x, offset_y) para encajar el modelo en el lienzo."""
    us = [p[0] for p in puntos_proyectados]
    vs = [p[1] for p in puntos_proyectados]
    umin, umax = min(us), max(us)
    vmin, vmax = min(vs), max(vs)
    w = max(umax - umin, 1e-6)
    h = max(vmax - vmin, 1e-6)
    interno = canvas * (1 - 2 * margen)
    escala = interno / max(w, h)
    ox = canvas / 2 - (umin + umax) / 2 * escala
    oy = canvas / 2 - (vmin + vmax) / 2 * escala
    return escala, umin, vmin, ox, oy


def render_spec(spec, canvas=256, ss=3):
    """Renderiza una Spec a un PNG RGB de `canvas` px (con supersample)."""
    piezas = _preparar_piezas(spec)

    # puntos para encuadre: esquinas del modelo + huella de sombra
    proys = [proyectar(*c) for _, cs, _ in piezas for c in cs]
    huella = []
    for _, cs, _ in piezas:
        huella += [(c[0], c[2]) for c in cs]
    if huella:
        proys += [proyectar(x, 0, z) for x, z in casco_hull(huella)]
    escala, umin, vmin, ox, oy = _fit(proys, canvas)

    total = canvas * ss

    def a_pixel(p):
        u, v = p
        return (ox + u * escala) * ss, (oy + v * escala) * ss

    # 1) lienzo + sombra de apoyo difuminada
    imagen = Image.new("RGBA", (total, total), FONDO + (255,))
    if huella:
        capa = Image.new("RGBA", (total, total), (0, 0, 0, 0))
        capadraw = ImageDraw.Draw(capa)
        marco = casco_hull(huella)
        capadraw.polygon(
            [a_pixel(proyectar(x, 0, z)) for x, z in marco], fill=(20, 18, 16, SOMBRA_ALFA)
        )
        capa = capa.filter(ImageFilter.GaussianBlur(radius=2.5 * ss))
        imagen = Image.alpha_composite(imagen, capa)
    imagen = imagen.convert("RGB")

    # 2) teselas: cada cara se corta en mosaicos de 1 unidad; la profundidad se
    #    calcula en el centro de la tesela (z-buffer exacto sobre la rejilla).
    #    Solo se pintan caras hacia la cámara (backface culling con vista (1,1,1)).
    teselas = []
    for pieza in spec.piezas:
        m = None
        origen = None
        if pieza.rotacion is not None:
            m = matriz_rot(pieza.rotacion.eje, pieza.rotacion.angulo)
            origen = pieza.rotacion.origen
        for nombre, gen, rango_a, rango_b in _def_caras(pieza.desde, pieza.hasta):
            n = aplicar(m, NORMAL_DE[nombre]) if m is not None else NORMAL_DE[nombre]
            if n[0] + n[1] + n[2] <= 0:
                continue
            clave = clave_sombra(n)
            ref = pieza.caras.get(nombre, pieza.material)
            color = tono(resolver(ref), SOMBRA_CARA[clave])
            a0, a1 = rango_a
            b0, b1 = rango_b
            for a in range(a0, a1):
                for b in range(b0, b1):
                    pts_m = [gen(a, b), gen(a + 1, b), gen(a + 1, b + 1), gen(a, b + 1)]
                    if m is not None:
                        pts_t = [rotar_punto(m, p, origen) for p in pts_m]
                    else:
                        pts_t = list(pts_m)
                    profundidad = sum(c[0] + c[1] + c[2] for c in pts_t) / 4
                    pix = [a_pixel(proyectar(*p)) for p in pts_t]
                    teselas.append((profundidad, pix, color))
    teselas.sort(key=lambda t: t[0])
    dibujo = ImageDraw.Draw(imagen)
    for profundidad, pix, color in teselas:
        dibujo.polygon(pix, fill=color)

    return imagen.resize((canvas, canvas), RESAMPLE)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cargar_specs():
    from tools.models3d import specs as paquete

    specs = []
    for info in pkgutil.iter_modules(paquete.__path__):
        if info.name.startswith("_"):
            continue
        modulo = importlib.import_module(f"tools.models3d.specs.{info.name}")
        for d in getattr(modulo, "SPECS", []):
            specs.append(Spec.de_dict(d))
    return specs


def hoja_zona(specs, zona, camino, celda=256, hueco=8):
    """Hoja de contacto: renders de una zona en grid, sin textos."""
    n = len(specs)
    columnas = min(4, max(1, n))
    filas = math.ceil(n / columnas)
    ancho = columnas * celda + hueco * (columnas + 1)
    alto = filas * celda + hueco * (filas + 1)
    pagina = Image.new("RGB", (ancho, alto), (222, 222, 220))
    for i, spec in enumerate(specs):
        img = render_spec(spec, canvas=celda)
        col = i % columnas
        fila = i // columnas
        x = hueco + col * (celda + hueco)
        y = hueco + fila * (celda + hueco)
        pagina.paste(img, (x, y))
    pagina.save(camino)
    return camino


def main(argv=None):
    parser = argparse.ArgumentParser(description="Previews isométricas de las specs 3D.")
    parser.add_argument("ids", nargs="*", help="ids concretos; vacío = todas")
    args = parser.parse_args(argv)

    todas = cargar_specs()
    if args.ids:
        pedidas = set(args.ids)
        specs = [s for s in todas if s.id in pedidas]
        faltantes = pedidas - {s.id for s in specs}
        if faltantes:
            print(f"avs: ids no encontrados: {', '.join(sorted(faltantes))}")
    else:
        specs = todas

    if not specs:
        print("No hay specs que renderizar.")
        return 1

    fallo = False
    for spec in specs:
        errores, avisos = spec.validar()
        for e in errores:
            print(f"ERROR [{spec.id}] {e}")
        for a in avisos:
            print(f"aviso [{spec.id}] {a}")
        if errores:
            fallo = True
    if fallo:
        print("Corrige los errores antes de renderizar.")
        return 1

    SALIDA.mkdir(parents=True, exist_ok=True)
    por_zona = {}
    for spec in specs:
        img = render_spec(spec)
        camino = SALIDA / f"{spec.id}.png"
        img.save(camino)
        por_zona.setdefault(spec.zona, []).append(spec)
        print(f"ok  {spec.id} ({spec.zona}, {len(spec.piezas)} piezas) -> {camino.relative_to(ROOT)}")

    for zona, lista in sorted(por_zona.items()):
        camino = hoja_zona(lista, zona, SALIDA / f"hoja_{zona}.png")
        print(f"ok  hoja {zona} ({len(lista)} items) -> {camino.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
