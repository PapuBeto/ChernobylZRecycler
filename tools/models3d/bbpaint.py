"""Fase Blockbench — pintor de texturas por item y planificador de recortes UV.

Flujo nuevo: el .bbmodel es la fuente editable y lleva su textura incrustada
(base64). Este modulo la pinta (PIL, pixel-art de 256x256 con detalle
pintado: agujas, rejillas, etiquetas, mugre) y planifica los recortes UV
que cada cara del .bbmodel usa.

Espacios:
- espacio UV del proyecto: 32x32 px  (el que Blockbench enseña en el editor)
- textura PNG: 256x256 px (ESCALA_PNG = 8 px de PNG por px de espacio UV)
  -> 16 px de PNG por unidad de Minecraft: mucho margen para arte firmado.
Casillas de material: 2x2 px UV (16x16 px PNG). Firmas: cara completa.
"""

from __future__ import annotations

import random
import zlib
from PIL import Image, ImageDraw

from tools.models3d.palette import WEAR, resolver

UV_LADO = 32        # px del espacio UV del proyecto Blockbench (escalable)
ESCALA_PNG = 8      # px de PNG por px UV (32 uv -> 256 png)
CASILLA = 2         # casilla de material en px UV (1 unidad MC = 2 px UV)
SEPARACION = 1      # hueco entre recortes (evita sangrado en mipmaps)
UV_NIVELES = (32, 48, 64, 96, 128)   # escalado si no cabe (PNG = UV * 8)

# ---------------------------------------------------------------------------
# Planificador de recortes
#
# Cada cara recibe una region del tamano EXACTO de la cara (2 px UV por
# unidad MC): la textura se pinta a densidad uniforme (16 px PNG por unidad)
# sin estiramientos. Caras con la misma (clave, dimensiones) comparten
# region. Firmas: rect a medida por (pieza, cara).
# ---------------------------------------------------------------------------

def planificar(usos, firmas, lado=UV_LADO):
    """Asigna un rect UV a cada (clave, dims) de material y a cada firma.

    usos:  [(clave, (w, h)), ...] con w,h = dimensiones de cara en unidades MC
           (horizontal, vertical segun la convencion por cara de _dims_caras).
    firmas: [((pieza, cara), (w, h)), ...] iguales.
    Devuelve ({(clave, dims): rect}, {(pieza, cara): rect, lado_uv}) con
    rect = [u1, v1, u2, v2] en px UV.

    Si no cabe, reintenta con el siguiente nivel de UV_NIVELES.
    """
    niveles = [lado] + [n for n in UV_NIVELES if n > lado]
    for nivel in niveles:
        try:
            return _estanteria(usos, firmas, nivel), nivel
        except ValueError:
            continue
    raise ValueError(
        f"las firmas/regiones no caben ni en {niveles[-1]}x{niveles[-1]}; "
        "reduce firmas o amplifica UV_NIVELES"
    )


def _estanteria(usos, firmas, uv_lado):
    # deduplicar: mismas (clave, dims) -> mismo rect
    unicos = []
    vistos = set()
    for clave, dims in usos:
        if (clave, dims) in vistos:
            continue
        vistos.add((clave, dims))
        unicos.append(("m", (clave, dims), (dims[0] * 2, dims[1] * 2)))
    for (k, (w, h)) in firmas:
        unicos.append(("f", k, (min(w * 2, uv_lado), min(h * 2, uv_lado))))

    # estanteria: apila por filas de altura descendente
    recortes = sorted(unicos, key=lambda r: (-r[2][1], -r[2][0], r[0]))
    rects_m, rects_f = {}, {}
    x, y, alto_fila = 0, 0, 0
    for tipo, clave, (w, h) in recortes:
        if x + w > uv_lado:
            x, y, alto_fila = 0, y + alto_fila + SEPARACION, 0
        if y + h > uv_lado:
            raise ValueError(
                f"no cabe el recorte {clave} ({w}x{h}) en {uv_lado}x{uv_lado}"
            )
        rect = [x, y, x + w, y + h]
        if tipo == "f":
            rects_f[clave] = rect
        else:
            rects_m[clave] = rect
        x += w + SEPARACION
        alto_fila = max(alto_fila, h)
    return rects_m, rects_f


# ---------------------------------------------------------------------------
# Pintado de casillas de material
# ---------------------------------------------------------------------------

def _tono(c, f):
    return tuple(max(0, min(255, round(v * f))) for v in c)


def _mezcla(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _semilla(texto):
    return zlib.crc32(texto.encode("utf-8")) & 0xFFFFFFFF


FAMILIA = {
    "acero": "metal", "hierro": "metal", "metal_oscuro": "metal",
    "aluminio": "metal", "plomo": "metal",
    "cobre": "cobre", "laton": "cobre",
    "vidrio": "vidrio", "vidrio_oscuro": "vidrio", "pantalla": "pantalla",
    "baquelita": "lacado", "baquelita_negra": "lacado",
    "plastico_amarillento": "lacado", "beige_aparato": "lacado",
    "verde_oliva": "lacado", "verde_militar": "lacado", "hazmat": "telalacada",
    "goma": "goma",
    "caqui": "tela", "kevlar": "tela", "tela_crema": "tela", "pelaje": "tela",
    "amarillo_peligro": "liso", "rojo_desgastado": "liso",
    "verde_acido": "liso", "blanco_lab": "pintura", "azul_quirurgico": "pintura",
    "porcelana": "pintura", "madera": "madera",
}


def pintar_tile(clave, semilla=None):
    """Casilla de material 16x16 px PNG con textura pintada del material."""
    base = resolver(clave)
    material, _, variante = clave.partition(".")
    wear = clave in WEAR
    if wear:
        familia = "wear_" + clave
    else:
        familia = FAMILIA.get(material, "liso")
        fvar = {"base": 1.0, "claro": 1.16, "oscuro": 0.82}.get(variante or "base", 1.0)
        base = _tono(base, fvar) if fvar != 1.0 else base

    lado = CASILLA * ESCALA_PNG  # 16
    img = Image.new("RGBA", (lado, lado), base + (255,))
    d = ImageDraw.Draw(img)
    rng = random.Random(_semilla(clave) if semilla is None else semilla)
    N = lado  # 16

    if familia == "metal":
        for x in range(N):
            for y in range(N):
                f = 1.0
                if x % 4 == 1:
                    f *= 0.95
                if x % 4 == 3:
                    f *= 1.04
                f += rng.uniform(-0.045, 0.045)
                if y == 0:
                    f *= 1.10
                if y == N - 1:
                    f *= 0.86
                img.putpixel((x, y), _tono(base, f) + (255,))
        # raspones finos
        for _ in range(3):
            y = rng.randrange(1, N - 1)
            x0 = rng.randrange(0, N - 4)
            d.line((x0, y, x0 + rng.randint(2, 4), y),
                   fill=_tono(base, 1.22) + (255,), width=1)

    elif familia == "cobre":
        for x in range(N):
            for y in range(N):
                f = 1.0
                if x % 3 == 0:
                    f *= 0.92
                f += rng.uniform(-0.04, 0.04)
                img.putpixel((x, y), _tono(base, f) + (255,))
        for _ in range(4):  # motas de pátina
            x, y = rng.randrange(N), rng.randrange(N)
            d.point((x, y), fill=_tono(base, 0.55) + (255,))

    elif familia in ("vidrio",):
        for x in range(N):
            for y in range(N):
                f = 0.92 + 0.13 * (N - y) / N
                f += rng.uniform(-0.02, 0.02)
                img.putpixel((x, y), _tono(base, f) + (255,))
        d.line((3, 0, 0, 3), fill=_tono(base, 1.55) + (255,), width=1)
        d.line((8, 0, 0, 8), fill=_tono(base, 1.35) + (255,), width=1)

    elif familia == "pantalla":
        for x in range(N):
            for y in range(N):
                f = 0.85
                if y % 2 == 0:
                    f *= 1.18
                d_ing = max(abs(x - N / 2), abs(y - N / 2)) / (N / 2)
                f *= 1.0 - 0.30 * d_ing
                img.putpixel((x, y), _tono(base, f) + (255,))

    elif familia in ("lacado", "telalacada"):
        for x in range(N):
            for y in range(N):
                f = 1.0 + rng.uniform(-0.03, 0.03)
                if y < 2:
                    f *= 1.10
                if y == N - 1 or x == N - 1:
                    f *= 0.85
                img.putpixel((x, y), _tono(base, f) + (255,))
        for _ in range(3):  # pícnicos de uso
            x, y = rng.randrange(N - 1), rng.randrange(2, N - 1)
            d.point((x, y), fill=_tono(base, 0.7) + (255,))
        if familia == "telalacada":
            d.line((2, 6, 6, 6), fill=_tono(base, 1.08) + (255,))
            d.line((9, 11, 13, 11), fill=_tono(base, 0.92) + (255,))

    elif familia == "goma":
        for x in range(N):
            for y in range(N):
                f = 1.0 + rng.uniform(-0.05, 0.05)
                img.putpixel((x, y), _tono(base, f) + (255,))
        for _ in range(3):  # bultos
            x, y = rng.randrange(2, N - 2), rng.randrange(2, N - 2)
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=_tono(base, 0.86) + (255,))
        for _ in range(2):  # grietas claras
            x, y = rng.randrange(1, N - 4), rng.randrange(1, N - 4)
            d.line((x, y, x + 2, y + 2), fill=_tono(base, 1.25) + (255,))

    elif familia in ("tela",):
        for x in range(N):
            for y in range(N):
                f = 1.0 if (y % 2 == 0) else 0.92
                if x % 4 == 0:
                    f *= 0.95
                f += rng.uniform(-0.03, 0.03)
                img.putpixel((x, y), _tono(base, f) + (255,))

    elif familia == "pintura":
        for x in range(N):
            for y in range(N):
                f = 1.0 + rng.uniform(-0.02, 0.02)
                if y == 0:
                    f *= 0.94
                img.putpixel((x, y), _tono(base, f) + (255,))
        for _ in range(2):
            x = rng.randrange(1, N)
            d.line((x, rng.randrange(4, 10), x, N - 1), fill=_tono(base, 0.93) + (255,))

    elif familia == "madera":
        for x in range(N):
            for y in range(N):
                f = 1.0 + math_sin(x * 1.4 + y) * 0.06 + rng.uniform(-0.03, 0.03)
                img.putpixel((x, y), _tono(base, f) + (255,))
        d.line((0, rng.randrange(5, 12), N - 1, rng.randrange(3, 9)),
               fill=_tono(base, 0.8) + (255,))

    elif familia.startswith("wear_"):
        nombre = clave
        if nombre == "oxido":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.1, 0.1)
                    img.putpixel((x, y), _tono(base, f) + (255,))
            for _ in range(5):
                x, y = rng.randrange(N), rng.randrange(N)
                d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=_tono(base, 0.68) + (255,))
        elif nombre == "oxido_oscuro":
            for x in range(N):
                for y in range(N):
                    img.putpixel((x, y), _tono(base, 1 + rng.uniform(-0.08, 0.08)) + (255,))
            for _ in range(6):
                x, y = rng.randrange(N), rng.randrange(N)
                d.point((x, y), fill=_tono(base, 0.7) + (255,))
        elif nombre in ("mugre", "hollin"):
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.14, 0.07)
                    img.putpixel((x, y), _tono(base, f) + (255,))
            for _ in range(4):
                x, y = rng.randrange(N), rng.randrange(N)
                d.point((x, y), fill=_tono(base, 0.75) + (255,))
        elif nombre == "imprimacion":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.05, 0.06)
                    img.putpixel((x, y), _tono(base, f) + (255,))
            d.line((0, N - 1, N - 1, N - 1), fill=_tono(base, 0.72) + (255,))
        elif nombre in ("sulfato", "sulfato_azul"):
            for x in range(N):
                for y in range(N):
                    img.putpixel((x, y), _tono(base, 1 + rng.uniform(-0.06, 0.09)) + (255,))
            for _ in range(6):  # cristales que sobresalen
                x, y = rng.randrange(1, N - 1), rng.randrange(1, N - 1)
                d.point((x, y), fill=_tono(base, 1.3) + (255,))
                d.point((x, y + 1), fill=_tono(base, 0.72) + (255,))
        elif nombre == "goteo_acido":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + (0.22 if x % 3 == 0 else 0) + rng.uniform(-0.04, 0.04)
                    img.putpixel((x, y), _tono(base, f) + (255,))
        elif nombre == "patina_rad":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.06, 0.12)
                    img.putpixel((x, y), _tono(base, f) + (255,))
        elif nombre == "moho":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.12, 0.05)
                    img.putpixel((x, y), _tono(base, f) + (255,))
            for _ in range(4):
                x, y = rng.randrange(N - 1), rng.randrange(N - 1)
                d.point((x, y), fill=_tono(base, 0.62) + (255,))
        elif nombre == "yodo":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.1, 0.1)
                    img.putpixel((x, y), _tono(base, f) + (255,))
            for _ in range(3):
                x, y = rng.randrange(N), rng.randrange(N)
                d.ellipse((x - 1, y, x + 1, y + 1), fill=_tono(base, 0.78) + (255,))
        elif nombre == "quemado":
            for x in range(N):
                for y in range(N):
                    f = 1.0 + rng.uniform(-0.12, 0.05)
                    img.putpixel((x, y), _tono(base, f) + (255,))
        else:
            for x in range(N):
                for y in range(N):
                    img.putpixel((x, y), _tono(base, 1 + rng.uniform(-0.05, 0.05)) + (255,))

    else:  # liso
        for x in range(N):
            for y in range(N):
                f = 1.0 + rng.uniform(-0.03, 0.03)
                img.putpixel((x, y), _tono(base, f) + (255,))
    return img


def math_sin(v):
    import math as _m
    return _m.sin(v)


# ---------------------------------------------------------------------------
# Firmas — funciones de cara pintada
# ---------------------------------------------------------------------------


class LienzoFirma:
    """Pinta un recorte (px UV) y lo pega en el canvas de textura."""

    def __init__(self, canvas, rect, rng):
        self.canvas = canvas
        self.rect = rect
        self.rng = rng
        caja = self._caja()
        self.sub = canvas.crop(caja)
        self.d = ImageDraw.Draw(self.sub)

    def _caja(self):
        u1, v1, u2, v2 = self.rect
        return (u1 * ESCALA_PNG, v1 * ESCALA_PNG, u2 * ESCALA_PNG, v2 * ESCALA_PNG)

    def w(self):
        return self.sub.size[0]

    def h(self):
        return self.sub.size[1]

    def tono(self, c, f=1.0):
        return _tono(c, f) + (255,)

    def todo(self, color):
        self.d.rectangle((0, 0, self.w() - 1, self.h() - 1), fill=self.tono(color))

    def marco(self, color, f=1.0, grosor=1):
        w, h = self.w(), self.h()
        self.d.rectangle((0, 0, w - 1, h - 1), outline=self.tono(color, f), width=grosor)

    def pegar(self):
        self.canvas.paste(self.sub, (self._caja()[0], self._caja()[1]))


# Accesos a la paleta sin importarlo 10 veces dentro de cada firma:
from tools.models3d.palette import resolver as _res


def _p_dial_vidrio(cuadro, rng):
    """Visor del Geiger: vidrio oscuro con aguja roja, escala y destello."""
    vidrio = _res("vidrio_oscuro")
    alu = _res("aluminio.claro")
    laton = _res("laton.claro")
    rojo = _res("rojo_desgastado.claro")
    cuadro.todo(vidrio)
    w, h = cuadro.w(), cuadro.h()
    # vidrio con gradiente vertical sutil (oscuro arriba, algo mas claro abajo)
    for y in range(h):
        t = 0.16 * (y / h)
        for x in range(w):
            cuadro.d.point((x, y), fill=_mezcla_ex(vidrio, _tono(vidrio, 1.45), t))
    # destello diagonal
    for i in range(min(w, h) // 3):
        cuadro.d.line((0, h - 1 - i, min(w - 1, h - 1 - i + w // 4), h - 1),
                      fill=cuadro.tono(vidrio, 1.9), width=1)
    # escala superior: ticks de latón
    y_t = h // 4
    for x in range(2, w - 2, 3):
        cuadro.d.line((x, y_t, x, y_t + 2), fill=cuadro.tono(laton, 1.1), width=1)
    cuadro.d.line((1, y_t + 3, w - 2, y_t + 3), fill=cuadro.tono(laton, 0.62), width=1)
    # aguja roja diagonal (de abajo-centro hacia arriba-derecha)
    piv = (w // 2, h - 3)
    punta = (int(w * 0.82), int(h * 0.28))
    cuadro.d.line((piv, punta), fill=cuadro.tono(rojo, 1.25), width=1)
    for dx in (-1, 1):
        cuadro.d.point((punta[0] + dx, punta[1]), fill=cuadro.tono(rojo, 1.0))
    # soporte de la aguja
    cuadro.d.ellipse((piv[0] - 2, piv[1] - 2, piv[0] + 2, piv[1] + 2),
                     fill=cuadro.tono(alu, 0.9))


def _mezcla_ex(a, b, t):
    return _mezcla(a, b, t) + (255,)


def _p_dial_lateral(cuadro, rng):
    """Dial lateral del Geiger: placa de latón con escudo grabado."""
    laton = _res("laton")
    laton_osc = _res("laton.oscuro")
    vidrio = _res("vidrio_oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(laton)
    # gran cicatriz de uso (franjas horizontales suaves)
    for y in range(h):
        f = 1.0 + (0.05 if (y // max(1, h // 8)) % 2 == 0 else -0.05)
        for x in range(w):
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), f) + (255,))
    cuadro.marco(laton_osc, 1.0)
    # círculo central oscuro (cristal) con escala
    cx, cy = w // 2, h // 2
    r = min(w, h) // 2 - 2
    cuadro.d.ellipse((cx - r, cy - r + 1, cx + r, cy + r + 1), fill=cuadro.tono(vidrio, 1.28))
    cuadro.d.ellipse((cx - r, cy - r + 1, cx + r, cy + r + 1),
                     outline=cuadro.tono(laton_osc, 1.1), width=1)
    # ticks alrededor
    for ang in range(0, 360, 30):
        import math as _m
        x0 = cx + int((r - 1) * _m.cos(_m.radians(ang)))
        y0 = cy + 1 + int((r - 1) * _m.sin(_m.radians(ang)))
        x1 = cx + int((r - 3) * _m.cos(_m.radians(ang)))
        y1 = cy + 1 + int((r - 3) * _m.sin(_m.radians(ang)))
        cuadro.d.line((x0, y0, x1, y1), fill=cuadro.tono(laton, 1.25), width=1)
    # aguja
    cuadro.d.line((cx + 1, cy + 1, cx + r - 3, cy - 3),
                  fill=cuadro.tono(rojo := _res("rojo_desgastado"), 1.1), width=1)
    # reflejo de cristal
    for i in range(3):
        cuadro.d.line((cx - r + 2 + i, cy - r + 4 + i, cx - 1, cy),
                      fill=cuadro.tono(vidrio, 1.8), width=1)


def _p_placa_marca(cuadro, rng):
    """Placa de marca del motor: latón con pseudo-texto КРАН-14."""
    laton = _res("laton")
    oscuro = _res("laton.oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(laton)
    for x in range(w):
        for y in range(h):
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), 1 + rng.uniform(-0.03, 0.03)) + (255,))
    cuadro.marco(oscuro, 1.0)
    # pseudo texto cirílico: celdas de glifos con trazos verticales y puente
    alto_tx = h // 2
    y0 = (h - alto_tx) // 2
    celda = 3
    for cx0 in range(2, w - 3, celda):
        trazos = sorted(rng.sample(
            range(cx0, min(cx0 + celda, w - 3)), max(1, celda - 2)
        ))
        top = y0
        bottom = y0 + alto_tx - 1
        for x_trazo in trazos:
            cuadro.d.line((x_trazo, top, x_trazo, bottom), fill=cuadro.tono(oscuro, 1.0), width=1)
        if rng.random() < 0.75:  # puente horizontal tipo visa/ia
            medio = top + alto_tx // 2
            cuadro.d.line((trazos[0], medio, trazos[-1], medio),
                          fill=cuadro.tono(oscuro, 1.0), width=1)
        if rng.random() < 0.35:  # descendente como la 'р'
            cuadro.d.line((trazos[-1], bottom, trazos[-1], min(h - 2, bottom + 1)),
                          fill=cuadro.tono(oscuro, 1.0), width=1)
    # remaches
    cuadro.d.point((0, 0), fill=cuadro.tono(oscuro, 1.3))
    cuadro.d.point((w - 1, h - 1), fill=cuadro.tono(oscuro, 1.3))


def _p_reja_radio(cuadro, rng):
    """Rejilla de altavoz del radio: tela con ranuras horizontales."""
    fondo = _res("metal_oscuro.oscuro")
    tela_clara = _res("aluminio.base")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(fondo)
    # tela: malla de pequeños puntos (celdas 3x3)
    for y in range(2, h - 1, 3):
        for x in range(2, w - 1, 3):
            brillo = 1.0 + rng.uniform(-0.15, 0.12)
            cuadro.d.point((x, y), fill=cuadro.tono(tela_clara, 0.42 * brillo))
    # ranuras horizontales (dos bandas oscuras alineadas con las barras)
    for yb in (h // 4, h * 3 // 4):
        cuadro.d.rectangle((1, yb - 1, w - 2, yb), fill=cuadro.tono(fondo, 0.6))
    # reflejo tenue diagonal
    for i in range(w // 6):
        cuadro.d.line((i, 0, i + 2, min(h - 1, 2 + i)), fill=cuadro.tono(fondo, 1.5), width=1)


def _p_selector_radio(cuadro, rng):
    """Mando del selector: baquelita negra con marcas y aguja clara."""
    neg = _res("baquelita_negra")
    claro = _res("plastico_amarillento.claro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(neg)
    for x in range(w):
        for y in range(h):
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), 1 + rng.uniform(-0.05, 0.05)) + (255,))
    cuadro.marco(neg, 1.35)
    # marcas alrededor (puntos claros)
    for i in range(5):
        y = 2 + i * (h - 4) // 4
        cuadro.d.line((2, y, 3, y), fill=cuadro.tono(claro, 0.95), width=1)
    # aguja hacia arriba-derecha
    cx, cy = w // 2, h // 2
    cuadro.d.line((cx, cy + 2, cx + 2, 2), fill=cuadro.tono(claro, 1.1), width=1)


def _p_placa_bateria(cuadro, rng):
    """Etiqueta 48ТН-125 de la batería: latón con texto grabado."""
    laton = _res("laton")
    oscuro = _res("laton.oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(laton)
    cuadro.marco(oscuro, 1.0)
    # banda oscura superior (título) y lineas de datos
    cuadro.d.rectangle((2, 2, w - 3, 2 + max(2, h // 5)), fill=cuadro.tono(oscuro, 0.92))
    for fy in range(2 + max(2, h // 5) + 2, h - 2, 3):
        x = 3
        while x < w - 4:
            ancho = rng.randint(2, 4)
            if rng.random() < 0.7:
                cuadro.d.line((x, fy, min(x + ancho, w - 4), fy), fill=cuadro.tono(oscuro, 1.05), width=1)
            x += ancho + rng.randint(1, 3)
    # marca de tensión: cuadrado rojo desgastado abajo-derecha
    rojo = _res("rojo_desgastado")
    cuadro.d.rectangle((w - 5, h - 5, w - 2, h - 2), fill=cuadro.tono(rojo, 1.0))
    cuadro.d.point((w - 4, h - 4), fill=cuadro.tono(rojo, 0.8))


def _p_deck_bateria(cuadro, rng):
    """Deck de goma de la batería (cara superior de la tapa)."""
    goma = _res("goma.base")
    oscuro = _res("goma.oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(goma)
    for x in range(w):
        for y in range(h):
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), 1 + rng.uniform(-0.04, 0.04)) + (255,))
    # bandejas hundidas de las 6 casillas de tapón (2x3) con franjas de uso
    for col in range(3):
        for fil in range(2):
            x0 = 2 + col * (w - 4) // 3
            y0 = 2 + fil * (h - 4) // 2
            x1 = x0 + max(3, (w - 4) // 3) - 2
            y1 = y0 + max(3, (h - 4) // 2) - 2
            cuadro.d.rectangle((x0, y0, x1, y1), outline=cuadro.tono(oscuro, 0.9), width=1)
            cuadro.d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=cuadro.tono(goma, 0.93))
    cuadro.marco(goma, 0.7)


def _p_visor_casco(cuadro, rng):
    """Visor del casco de liquidador: vidrio oscuro con doble destello."""
    vidrio = _res("vidrio_oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(vidrio)
    for y in range(h):
        f = 0.78 + 0.4 * (1 - y / h) ** 1.4
        for x in range(w):
            cuadro.d.point((x, y), fill=_mezcla_ex(vidrio, (20, 26, 30), min(1.0, f - 0.7)))
    # doble banda de reflejo horizontal (luz de sisio sobre el yelmo)
    for y in (h // 4, h // 4 + 1):
        cuadro.d.line((w // 5, y, w * 4 // 5, y), fill=cuadro.tono(vidrio, 2.1), width=1)
    # bordes de goma (sellado del visor)
    for x in range(w):
        cuadro.d.point((x, 0), fill=cuadro.tono(vidrio, 0.72))
        cuadro.d.point((x, h - 1), fill=cuadro.tono(vidrio, 0.72))


def _p_forro_rasgadura(cuadro, rng):
    """Forro de goma bajo la rasgadura del brazo: tela oscura."""
    goma = _res("goma.oscuro")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(goma)
    for x in range(w):
        for y in range(h):
            f = 1.0 if (x + y) % 3 else 1.16
            f += rng.uniform(-0.05, 0.05)
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), f) + (255,))


def _p_escape_arriba(cuadro, rng):
    """Boca del escape del motor: hollin con aro de óxido."""
    hollin = _res("hollin")
    ox = _res("oxido")
    w, h = cuadro.w(), cuadro.h()
    cuadro.todo(hollin)
    for x in range(w):
        for y in range(h):
            r, g, b, _ = cuadro.sub.getpixel((x, y))
            cuadro.d.point((x, y), fill=_tono((r, g, b), 1 + rng.uniform(-0.12, 0.12)) + (255,))
    cuadro.d.ellipse((w // 4, h // 4, w * 3 // 4, h * 3 // 4), fill=cuadro.tono(hollin, 0.55))
    cuadro.d.ellipse((w // 4, h // 4, w * 3 // 4, h * 3 // 4), outline=cuadro.tono(ox, 0.95), width=1)


# Firmas por item: (id) -> {(pieza, cara): funcion}
FIRMAS = {
    "contador_geiger_pripyat": {
        ("vidrio", "sur"): _p_dial_vidrio,
        ("dial_lateral", "este"): _p_dial_lateral,
    },
    "bateria_tanque_t72": {
        ("placa_datos", "oeste"): _p_placa_bateria,
        ("tapa", "arriba"): _p_deck_bateria,
    },
    "radio_campana_r159": {
        ("reja", "sur"): _p_reja_radio,
        ("selector", "sur"): _p_selector_radio,
    },
    "motor_grua_sovietica": {
        ("placa_marca", "sur"): _p_placa_marca,
        ("tapa_escape", "arriba"): _p_escape_arriba,
    },
    "traje_hazmat_liquidador": {
        ("visor", "sur"): _p_visor_casco,
        ("rasgadura", "sur"): _p_forro_rasgadura,
        ("respirador", "sur"): _p_deck_bateria,  # rejilla de respiración
    },
}


# ---------------------------------------------------------------------------
# Pintado completo de la textura por item
# ---------------------------------------------------------------------------

def pintar_textura(spec, rects_material, rects_firmas, lado_uv=UV_LADO):
    """Pinta la textura PNG del item y devuelve (Image RGBA, lado px)."""
    lado = lado_uv * ESCALA_PNG
    fondo = (198, 198, 198, 255)  # el resto de la hoja: neutro (no referenciado)
    img = Image.new("RGBA", (lado, lado), fondo)

    # 1) regiones de material: baldosas pintar_tile a densidad 1 unidad/celda
    for (clave, dims), rect in rects_material.items():
        w, h = dims
        for cx in range(w):
            for cy in range(h):
                tile = pintar_tile(clave, _semilla(f"{spec.id}:{clave}:{cx}:{cy}"))
                px = (rect[0] + cx * CASILLA) * ESCALA_PNG
                py = (rect[1] + cy * CASILLA) * ESCALA_PNG
                img.paste(tile, (px, py))
        # goteo de bordes hacia el hueco contiguo (aviso antialias/mipmap)
        _sangrado_bordes(img, rect, w, h)

    # 2) firmas
    for clave, func in FIRMAS.get(spec.id, {}).items():
        rect = rects_firmas.get((clave[0], clave[1]))
        if rect is None:
            continue
        rng = random.Random(_semilla("%s:%s:%s" % (spec.id, clave[0], clave[1])))
        cuadro = LienzoFirma(img, rect, rng)
        func(cuadro, rng)
        cuadro.pegar()

    return img


def _sangrado_bordes(img, rect, w, h):
    """Copia el borde exterior 1 px hacia los huecos limitrofes del recorte
    (evita que el mipmap promedie color vecino dentro de la region)."""
    x0, y0 = rect[0] * ESCALA_PNG, rect[1] * ESCALA_PNG
    ancho, alto = w * CASILLA * ESCALA_PNG, h * CASILLA * ESCALA_PNG
    if x0 > 0:
        franja = img.crop((x0, y0, x0 + 1, y0 + alto))
        img.paste(franja, (x0 - 1, y0))
    if y0 > 0:
        franja = img.crop((x0, y0, x0 + ancho, y0 + 1))
        img.paste(franja, (x0, y0 - 1))


# ---------------------------------------------------------------------------
# Definición de firmas por spec (dimensiones de cara en unidades MC)
# ---------------------------------------------------------------------------

def dims_cara(desde, hasta, cara):
    """(w, h) de la cara en unidades MC: horizontal, vertical (convencion de
    pintado por cara: norte/sur horizontal=x; este/oeste horizontal=z;
    arriba/abajo horizontal=x, vertical=z)."""
    x0, y0, z0 = desde
    x1, y1, z1 = hasta
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    if cara in ("norte", "sur"):
        return (dx, dy)
    if cara in ("este", "oeste"):
        return (dz, dy)
    return (dx, dz)


def firmas_de_spec(spec):
    """[( (pieza, cara), (w,h) )] para planificar; ignora lo que no esté en la spec."""
    marcadas = FIRMAS.get(spec.id, {})
    dims = {}
    for pieza in spec.piezas:
        for cara_es in ("norte", "sur", "este", "oeste", "arriba", "abajo"):
            dims[(pieza.nombre, cara_es)] = dims_cara(pieza.desde, pieza.hasta, cara_es)
    salida = []
    for (pieza, cara) in marcadas:
        dim = dims.get((pieza, cara))
        if dim is None:
            continue
        salida.append(((pieza, cara), dim))
    return salida
