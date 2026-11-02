# -*- coding: utf-8 -*-
"""Motor de sprites 2D para ChernobylZ.

Ilustracion semirrealista dibujada por codigo con PIL: cada forma se pinta
como una mascara con gradiente direccional multifase + material + bisel de
luz/sombra + ruido de superficie + retokes del item; el conjunto se
reescala con LANCZOS para antialiasing de ilustracion (nada de pixel art).

Convenciones de la coleccion:
- Maestro de 512 px de lado (LADO); salida de juego 256 px (SALIDA).
- Luz global desde arriba-izquierda (LUZ).
- Coordenadas en unidades del maestro 512 (se supersamplean xSS).
- Fondo transparente; sombra de contacto sutil integrada.
"""
from __future__ import annotations

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from tools.sprites2d.paleta import OXIDO, OXIDO_CLARO, PRIMER

SS = 2                   # supersample del maestro
LADO = 512               # lado del maestro
SALIDA = 256             # lado del PNG de juego
LUZ = (-0.42, -1.0)      # direccion de la luz (global de coleccion)
_NEGRO = (18, 16, 20)
_ACENTO = (255, 253, 246)


# ------------------------------------------------------------------ basicos
def _lerp(a, b, t):
    return a + (b - a) * t


def _mezcla(c1, c2, t):
    return tuple(int(round(_lerp(a, b, t))) for a, b in zip(c1, c2))


def _tono(rgb, f):
    return tuple(max(0, min(255, int(round(c * f)))) for c in rgb[:3])


def _desplaza(im, dx, dy):
    return ImageChops.offset(im, int(dx), int(dy))


def curva_suave(puntos, n=28):
    """Catmull-Rom simple: centrolinea suave desde puntos de control."""
    pts = list(puntos)
    if len(pts) < 3:
        return pts
    sal = []
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            sal.append((x, y))
    sal.append(pts[-1])
    return sal


def arco_bandas(centro, r_in, r_out, a0, a1, pasos=14):
    """Poligono cerrado de una banda angular (para desgastes en arcos)."""
    pts = []
    for i in range(pasos + 1):
        a = math.radians(a0 + (a1 - a0) * i / pasos)
        pts.append((centro[0] + r_out * math.cos(a), centro[1] + r_out * math.sin(a)))
    for i in range(pasos, -1, -1):
        a = math.radians(a0 + (a1 - a0) * i / pasos)
        pts.append((centro[0] + r_in * math.cos(a), centro[1] + r_in * math.sin(a)))
    return pts


def faja_puntos(pts, grosor, taper=1.0):
    """Cinta cerrada en torno a una centrolinea (grosor variable)."""
    izq, der = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        d = math.hypot(dx, dy) or 1.0
        px, py = -dy / d, dx / d
        t = i / max(1, n - 1)
        g = grosor * (1.0 - taper * abs(t - 0.5) * 2 * 0.3) * 0.5
        izq.append((x + px * g, y + py * g))
        der.append((x - px * g, y - py * g))
    return izq + der[::-1]


# ================================================================== lienzo
class Lienzo:
    """Lamina RGBA transparente donde los items pintan sus formas."""

    def __init__(self, semilla=0, lado=LADO):
        self.rng = random.Random(semilla)
        self.lado = lado
        self._lam = lado * SS
        self.img = Image.new("RGBA", (self._lam, self._lam), (0, 0, 0, 0))

    # ------------------------------------------------------------ helpers
    def _es(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def _caja_es(self, caja):
        x0, y0, x1, y1 = caja
        return (x0 * SS, y0 * SS, x1 * SS, y1 * SS)

    def _mascara(self, dibujar):
        m = Image.new("L", (self._lam, self._lam), 0)
        dibujar(ImageDraw.Draw(m))
        return m

    def _pegar(self, capa):
        self.img = Image.alpha_composite(self.img, capa)

    # ------------------------------------------------------------- pintura
    def pintar(self, mask, material, color, luz=LUZ, fases=None, bisel=None,
               contorno=None, retocar=None):
        """Pinta una forma (mask L en supersample) sobre el lienzo.

        material : 'acero','aluminio','hierro','cobre','tela','caucho',
                   'porcelana','oscuro' o None (plastico/pintura lisa)
        fases    : [(t, factor), ...] luz->sombra sobre el color base
        bisel    : (grosor px, luz, sombra) en las bandas alineadas a la luz
        contorno : grosor px del contorno por contraste (0 = sin contorno)
        retocar  : callable(rgb_recorte, caja, rng) -> rgb; detalle del item
        """
        caja = mask.getbbox()
        if caja is None:
            return
        rg = random.Random(self.rng.randrange(1 << 30))
        if fases is None:
            fases = [(0.0, 1.16), (0.5, 1.0), (1.0, 0.58)]
        rgb = gradiente(caja, color, luz, fases)
        if material:
            rgb = aplicar_material(rgb, caja, material, rg)
        if retocar is not None:
            rgb = retocar(rgb, caja, rg)

        capa = Image.new("RGBA", (self._lam, self._lam), (0, 0, 0, 0))
        capa.paste(rgb, caja[:2])

        if bisel:
            g, luz_f, sombra_f = bisel
            g = max(1, int(g * SS))
            ux, uy = LUZ
            banda_l = ImageChops.subtract(mask, _desplaza(mask, -ux * g * 0.8, -uy * g * 0.8))
            banda_l = banda_l.filter(ImageFilter.GaussianBlur(g * 0.8))
            banda_s = ImageChops.subtract(mask, _desplaza(mask, ux * g * 0.8, uy * g * 0.8))
            banda_s = banda_s.filter(ImageFilter.GaussianBlur(g))
            capa = _mezclar_rgb(capa, banda_l, int(255 * luz_f), True)
            capa = _mezclar_rgb(capa, banda_s, int(150 * sombra_f), False)

        capa.putalpha(ImageChops.multiply(capa.getchannel("A"), mask))
        self._pegar(capa)

        if contorno is None:
            contorno = 1.3
        if contorno:
            self.contorno(mask, grosor=contorno)

    def contorno(self, mask, grosor=1.3, color=_NEGRO, alpha=110):
        """Contorno oscuro por contraste (silueta + separacion entre piezas)."""
        kg = max(1, int(round(grosor * SS)))
        if kg < 1:
            return
        borde = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(2 * kg + 1)), mask)
        borde = borde.point(lambda v: int(v * alpha / 255))
        capa = Image.new("RGBA", mask.size, color + (0,))
        capa.putalpha(borde)
        self._pegar(capa)

    # -------------------------------------------------------- primitivas
    def poligono(self, puntos, material, color, luz=LUZ, fases=None, bisel=None,
                 contorno=None, retocar=None):
        pts = self._es(puntos)
        mask = self._mascara(lambda d: d.polygon(pts, fill=255))
        self.pintar(mask, material, color, luz=luz, fases=fases, bisel=bisel,
                    contorno=contorno, retocar=retocar)
        return mask

    def circulo(self, centro, radio, material, color, **kw):
        cx, cy = centro
        return self.elipse((cx - radio, cy - radio, cx + radio, cy + radio),
                           material, color, **kw)

    def elipse(self, caja, material, color, luz=LUZ, fases=None, bisel=None,
               contorno=None, retocar=None):
        mask = self._mascara(lambda d: d.ellipse(self._caja_es(caja), fill=255))
        self.pintar(mask, material, color, luz=luz, fases=fases, bisel=bisel,
                    contorno=contorno, retocar=retocar)
        return mask

    def anillo(self, caja, grosor, material, color, luz=LUZ, fases=None, bisel=None,
               contorno=None, retocar=None):
        def dib(d):
            d.ellipse(self._caja_es(caja), fill=255)
            g = grosor * SS
            d.ellipse((caja[0] * SS + g, caja[1] * SS + g,
                       caja[2] * SS - g, caja[3] * SS - g), fill=0)
        mask = self._mascara(dib)
        self.pintar(mask, material, color, luz=luz, fases=fases, bisel=bisel,
                    contorno=contorno, retocar=retocar)
        return mask

    def curva(self, puntos, grosor, material, color, taper=1.0, **kw):
        pol = faja_puntos(curva_suave(puntos), grosor, taper)
        return self.poligono(pol, material, color, **kw)

    # --------------------------------------------------------------- luz
    def sombra_contacto(self, caja, alpha=64, difum=9, color=(16, 14, 18)):
        """Sombra sutil de contacto bajo el objeto (fondo se mantiene limpio)."""
        m = self._mascara(lambda d: d.ellipse(self._caja_es(caja), fill=255))
        m = m.filter(ImageFilter.GaussianBlur(difum * SS))
        capa = Image.new("RGBA", m.size, color + (0,))
        capa.putalpha(m.point(lambda v: int(v * alpha / 255)))
        self._pegar(capa)

    def oclusion(self, puntos, desplaz=(0, 6), alpha=60, difum=5):
        """AO proyectada de una pieza sobre la pieza de abajo."""
        dx, dy = desplaz
        m = self._mascara(lambda d: d.polygon(
            self._es([(x + dx, y + dy) for x, y in puntos]), fill=255))
        m = m.filter(ImageFilter.GaussianBlur(difum * SS))
        capa = Image.new("RGBA", m.size, (10, 8, 12, 0))
        capa.putalpha(m.point(lambda v: int(v * alpha / 255)))
        self._pegar(capa)

    def brillito(self, centro, radio, alpha=60, difum=None):
        """Destello especular difuso compuesto (metales/plastico)."""
        cx, cy = centro
        caja = (cx - radio, cy - radio, cx + radio, cy + radio)
        m = self._mascara(lambda d: d.ellipse(self._caja_es(caja), fill=255))
        m = m.filter(ImageFilter.GaussianBlur((difum or radio * 0.8) * SS))
        capa = Image.new("RGBA", m.size, _ACENTO + (0,))
        capa.putalpha(m.point(lambda v: int(v * alpha / 255)))
        self._pegar(capa)

    def velo(self, mask, color, alpha, difum=0):
        """Masa translucida de color uniforme (oxido, imprimacion, hollin)."""
        capa = Image.new("RGBA", mask.size, color + (alpha,))
        a = mask if not difum else mask.filter(ImageFilter.GaussianBlur(difum * SS))
        capa.putalpha(ImageChops.multiply(capa.getchannel("A"), a))
        self._pegar(capa)

    # ------------------------------------------------------------ ferreteria
    def remache(self, cx, cy, r, color, fuerza_luz=120):
        self.circulo((cx, cy), r, "acero", color, fases=[(0.0, 1.32), (0.42, 1.06), (1.0, 0.55)],
                     bisel=(max(1.0, r * 0.5), 0.25, 0.3), contorno=0.8)
        self.brillito((cx - r * 0.30, cy - r * 0.34), r * 0.42, alpha=int(fuerza_luz * 0.5), difum=r * 0.45)

    def tuerca(self, cx, cy, r, color, rot=None, hueco=True):
        ang = rot if rot is not None else self.rng.uniform(0, math.pi)
        pts = [(cx + r * math.cos(ang + i * math.pi / 3),
                cy + r * math.sin(ang + i * math.pi / 3)) for i in range(6)]
        self.poligono(pts, "acero", color, fases=[(0.0, 1.30), (0.5, 1.02), (1.0, 0.58)],
                      bisel=(max(1.0, r * 0.4), 0.3, 0.3), contorno=0.9)
        if hueco:
            self.circulo((cx, cy), r * 0.40, "oscuro", _tono(color, 0.55),
                         fases=[(0.0, 1.15), (1.0, 0.7)], contorno=0.6)

    # ------------------------------------------------------------------ fin
    def maestro(self):
        return self.img.resize((self.lado, self.lado), Image.LANCZOS)


# ==================================================== gradientes/materiales
def gradiente(caja, color, luz, fases):
    """RGB: color base x fases(t) proyectadas a lo largo de la luz."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    t = _mapa_t(caja, luz)
    lut = _lut_fases(fases)
    ill = t.point(lut)
    canales = []
    for c in color[:3]:
        tabla = [max(0, min(255, int(round(v * (c / 255.0))))) for v in range(256)]
        canales.append(ill.point(tabla))
    return Image.merge("RGB", tuple(canales))


def _mapa_t(caja, luz):
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    lx, ly = luz
    n = math.hypot(lx, ly) or 1.0
    ux, uy = lx / n, ly / n
    # el gradiente debe cubrir toda la proyeccion de la caja sobre el eje de luz
    proy = int(abs(w * ux) + abs(h * uy)) + 8
    grad = Image.linear_gradient("L").resize((proy, proy), Image.BILINEAR)
    grados = math.degrees(math.atan2(uy, ux))
    rot = grad.rotate(-grados - 90, expand=True, resample=Image.BILINEAR)
    cw, ch = rot.size
    rec = rot.crop((cw // 2 - w // 2, ch // 2 - h // 2,
                    cw // 2 - w // 2 + w, ch // 2 - h // 2 + h))
    return rec.resize((w, h), Image.BILINEAR)


def _lut_fases(fases):
    lut = []
    for i in range(256):
        t = i / 255.0
        f = fases[0][1]
        for (t0, f0), (t1, f1) in zip(fases, fases[1:]):
            if t0 <= t <= t1:
                f = _lerp(f0, f1, (t - t0) / max(1e-6, t1 - t0))
                break
        else:
            if t >= fases[-1][0]:
                f = fases[-1][1]
        lut.append(max(0, min(255, int(round(f * 255)))))
    return lut


def aplicar_material(rgb, caja, mat, rg):
    """Textura de material sobre el gradiente (rgb es un crop de caja)."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    if mat in ("acero", "aluminio"):
        banda = Image.new("L", (w, h), 0)
        bd = ImageDraw.Draw(banda)
        for _ in range(6):
            yy = rg.uniform(-h * 0.15, h * 1.05)
            incl = rg.uniform(-0.25, 0.25)
            bd.line([(0, yy), (w, yy + w * incl)], fill=rg.randint(40, 80), width=rg.randint(2, 4))
        banda = banda.filter(ImageFilter.GaussianBlur(2.2 * SS))
        rgb = _aclarar(rgb, banda, 0.30)
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 9), 0.07)
    elif mat == "hierro":
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 22), 0.22)
    elif mat == "cobre":
        bandas = Image.new("L", (w, h), 0)
        bd = ImageDraw.Draw(bandas)
        for _ in range(9):
            xx = rg.uniform(0, w)
            bd.line([(xx, 0), (xx + rg.uniform(-7, 7), h)], fill=rg.randint(16, 40), width=1)
        bandas = bandas.filter(ImageFilter.GaussianBlur(1.1 * SS))
        rgb = _aclarar(rgb, bandas, 0.24)
    elif mat == "tela":
        trama = Image.new("L", (w, h), 0)
        td = ImageDraw.Draw(trama)
        paso = max(3, int(h * 0.035)) | 1
        for yy in range(0, h, paso):
            td.line([(0, yy), (w, yy)], fill=30, width=1)
        for xx in range(0, w, paso):
            td.line([(xx, 0), (xx, h)], fill=22, width=1)
        rgb = _oscurecer(rgb, trama, 0.14)
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 10), 0.10)
    elif mat == "caucho":
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 15), 0.15)
    elif mat == "porcelana":
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 7), 0.05)
    elif mat == "oscuro":
        rgb = _ruido_mult(rgb, Image.effect_noise((w, h), 12), 0.12)
    return rgb  # None => liso (plastico/pintura/vidrio mate)


def _aclarar(rgb, banda, k):
    """Aclara hacia blanco donde banda marca (k: 0..1)."""
    delta = banda.point(lambda v: int(v * k))
    delta = Image.merge("RGB", (delta,) * 3)
    delta = ImageChops.multiply(delta, ImageChops.invert(rgb))
    delta = delta.point(lambda v: v // 2)
    return ImageChops.add(rgb, delta)


def _oscurecer(rgb, banda, k):
    delta = banda.point(lambda v: int(v * k * 255))
    delta = Image.merge("RGB", (delta,) * 3)
    delta = ImageChops.multiply(delta, rgb)
    delta = delta.point(lambda v: v // 2)
    return ImageChops.subtract(rgb, delta)


def _ruido_mult(rgb, ruido, k):
    sube = ruido.point(lambda v: max(0, int((v - 128) * k)))
    baja = ruido.point(lambda v: max(0, int((128 - v) * k)))
    clr = ImageChops.add(rgb, Image.merge("RGB", (sube,) * 3))
    return ImageChops.subtract(clr, Image.merge("RGB", (baja,) * 3))


def _mezclar_rgb(capa_rgba, banda, cantidad, aclarar):
    """Suma/resta un delta RGB donde banda marca (compone con la banda)."""
    if cantidad <= 0:
        return capa_rgba
    r, g, b, a = capa_rgba.split()
    delta = banda.point(lambda v: int(v * cantidad / 255))
    if aclarar:
        r = ImageChops.add(r, delta)
        g = ImageChops.add(g, delta)
        b = ImageChops.add(b, delta)
    else:
        r = ImageChops.subtract(r, delta)
        g = ImageChops.subtract(g, delta)
        b = ImageChops.subtract(b, delta)
    sal = Image.merge("RGBA", (r, g, b, a))
    return Image.composite(sal, capa_rgba, banda.point(lambda v: min(255, v * 2)))


# ================================================================== desgaste
def manchas_oxido(rgb, caja, rng, densidad=6, escala=1.0, chorreos=0.5):
    """Manchas de oxido con chorreado vertical (retocar de una pieza)."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for _ in range(int(densidad)):
        cx = rng.uniform(0, w)
        cy = rng.uniform(0, h)
        rr = rng.uniform(2.5, 8) * escala
        col = _mezcla(OXIDO, OXIDO_CLARO, rng.random())
        al = rng.randint(85, 140)
        d.ellipse((cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8), fill=col + (al,))
        if rng.random() < chorreos:
            largo = rng.uniform(8, 42) * escala
            pasos = max(3, int(largo / 7))
            for k in range(pasos):
                tt = k / pasos
                gorro = (1 - tt) * rr * 0.5 + 0.8
                yy = cy + k * (largo / pasos)
                d.ellipse((cx - gorro, yy, cx + gorro, yy + (largo / pasos) * 1.1),
                          fill=col + (int(al * (1 - tt * 0.9)),))
    capa = capa.filter(ImageFilter.GaussianBlur(1.5 * SS))
    return Image.alpha_composite(rgb.convert("RGBA"), capa).convert("RGB")


def rayitas(rgb, caja, rng, n=5, color=(226, 222, 214), alpha=80):
    """Aranazos finos de luz."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for _ in range(n):
        px = rng.uniform(0.08, 0.9) * w
        py = rng.uniform(0.12, 0.85) * h
        largo = rng.uniform(8, 36)
        ang = rng.uniform(-0.45, 0.45)
        d.line([(px, py), (px + largo, py + largo * ang)],
               fill=color[:3] + (rng.randint(alpha // 3, alpha),),
               width=max(1, int(1.1 * SS)))
    capa = capa.filter(ImageFilter.GaussianBlur(0.5 * SS))
    return Image.alpha_composite(rgb.convert("RGBA"), capa).convert("RGB")


def mugre(rgb, caja, rng, fuerza=0.12, en_bordes=0.6):
    """Motas de grasa; algo mas densas hacia los bordes (en_bordes 0..1)."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    motas = Image.effect_noise((w, h), 20)
    capa = motas.point(lambda v: max(0, int((v - 130) * fuerza * 2)))
    if en_bordes > 0:
        borde = _banda_borde(w, h, int(min(w, h) * 0.12))
        capa2 = ImageChops.multiply(capa, borde.point(lambda v: int(v * en_bordes)))
        capa = ImageChops.add(capa, capa2)
    delta = Image.merge("RGB", (capa,) * 3)
    return ImageChops.subtract(rgb, delta)


def _banda_borde(w, h, g):
    m = Image.new("L", (w, h), 255)
    md = ImageDraw.Draw(m)
    md.rectangle((g, g, w - g, h - g), fill=0)
    return m.filter(ImageFilter.GaussianBlur(g * 0.7))


def descascarillado(rgb, caja, rng, n=4, fuerzab=130):
    """Parches de imprimacion (pintura caida)."""
    x0, y0, x1, y1 = caja
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    parches = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(parches)
    for _ in range(n):
        cx = rng.uniform(0, w)
        cy = rng.uniform(0, h)
        rx, ry = rng.uniform(5, 18), rng.uniform(4, 11)
        npts = 9
        poly = [(cx + math.cos(2 * math.pi * i / npts) * rx * rng.uniform(0.55, 1.2),
                 cy + math.sin(2 * math.pi * i / npts) * ry * rng.uniform(0.55, 1.2))
                for i in range(npts)]
        col = _mezcla(PRIMER, (150, 146, 134), rng.random())
        d.polygon(poly, fill=col + (rng.randint(fuerzab // 2, fuerzab),))
    parches = parches.filter(ImageFilter.GaussianBlur(0.9 * SS))
    return Image.alpha_composite(rgb.convert("RGBA"), parches).convert("RGB")
