# -*- coding: utf-8 -*-
"""Formas reutilizables de pixel art para la coleccion ChernobylZ.

Todas usan la misma convencion: luz global top-left, bandas solidas con
transicion en dama, contorno por contraste (nunca antialiasing).
"""
from __future__ import annotations

from tools.pixelart import pal
from tools.pixelart.px import P, tono

# ----------------------------------------------------------------- caras
def cara(p, x0, y0, x1, y1, rampa, brillo=3, base=2, prof=1, esquinas=None):
    """Cara frontal: relleno por escalones verticales + contorno inferior."""
    p.rect(x0, y0, x1, y1, tono(rampa, base))
    p.pasos_v(x0, y0, x1, y1,
              [tono(rampa, brillo), tono(rampa, base), tono(rampa, prof)])
    p.hlinea(x0, x1, y1, tono(rampa, 0))
    p.vlinea(x1 - 1, y0, y1, tono(rampa, max(0, prof - 1)))
    if esquinas:                      # recorte de esquinas (silueta redondeada)
        for x, y in esquinas:
            p.pset(x, y, (0, 0, 0, 0))


def pernos_esquinas(p, x0, y0, x1, y1, rampa, gap=2):
    """Pernos de tapa en las cuatro esquinas de una caja."""
    luz = tono(rampa, len(rampa) - 1)
    for x, y in ((x0 + gap, y0 + gap), (x1 - gap, y0 + gap),
                 (x0 + gap, y1 - gap), (x1 - gap, y1 - gap)):
        p.pset(x, y, luz)
        p.pset(x + 1, y + 1, tono(rampa, 0))


def rejilla_puntos(p, x0, y0, cols, filas, paso, c, desfase=False):
    """Malla perforada (altavoces, rejillas, filtros)."""
    for f in range(filas):
        d = paso // 2 if desfase and f % 2 else 0
        for k in range(cols):
            p.pset(x0 + k * paso + d, y0 + f * paso, c)


def rejilla_lineas(p, x0, y0, x1, y1, c_luz, c_sombra, paso=2):
    """Rejilla de ranuras horizontales (parlantes, calefaccion)."""
    for y in range(y0, y1 + 1, paso):
        p.hlinea(x0, x1, y, c_luz)
        p.hlinea(x0, x1, y + 1, c_sombra)


# ----------------------------------------------------------------- piezas
def perilla(p, cx, cy, r, rampa, indice_selector=None):
    """Chapa de mandos: disco con borde oscuro, brillo y muesca."""
    p.elipse(cx, cy, r, r, tono(rampa, 2), contorno=tono(rampa, 0))
    p.pset(cx - r // 2 if r > 1 else cx, cy - r // 2 if r > 1 else cy,
           tono(rampa, 3))
    if indice_selector is None:
        p.pset(cx + r, cy - 1, tono(pal.BEIGE, 3))
    else:
        p.pset(*indice_selector, tono(pal.BEIGE, 3))


def lampara(p, x, y, color_rampa):
    """Piloto luminoso 2x2 con nucleo claro."""
    p.pset(x, y, tono(color_rampa, len(color_rampa) - 1))
    p.pset(x + 1, y, tono(color_rampa, len(color_rampa) - 2))
    p.pset(x, y + 1, tono(color_rampa, 1))
    p.pset(x + 1, y + 1, tono(color_rampa, 0))


def cilindro(p, x0, ytop, ancho, alto, rampa, cuerpo=2, tapa=True):
    """Cilindro vertical de frente (bidones, ollas, condensadores, celulas)."""
    x1, ybot = x0 + ancho - 1, ytop + alto - 1
    p.rect(x0, ytop, x1, ybot, tono(rampa, cuerpo))
    p.vlinea(x0 + 1, ytop + 1, ybot, tono(rampa, min(4, cuerpo + 1)))  # brillo
    p.banda_der(x0, ytop, x1, ybot, tono(rampa, max(0, cuerpo - 1)))
    p.hlinea(x0, x1, ybot, tono(rampa, 0))
    if tapa:
        p.hlinea(x0, x1, ytop, tono(rampa, 4))
    return x1, ybot


def terminal(p, x0, y0, rampa):
    """Poste/borne metalico 2x3 con luz arriba."""
    p.rect(x0, y0, x0 + 1, y0 + 2, tono(rampa, 3))
    p.hlinea(x0, x0 + 1, y0, tono(rampa, 4))
    p.pset(x0, y0 + 2, tono(rampa, 1))


def corroer(p, pixeles, oxido, mezcla_beige=False):
    """Manchas de oxido deliberadas: [(x, y, indice), ...]."""
    for x, y, i in pixeles:
        p.pset(x, y, tono(oxido, i))
    if mezcla_beige:
        for x, y, i in pixeles[::2]:
            p.pset(x, y + 1, tono(pal.BEIGE, min(2, i)))


def costuras(p, puntos, hilo):
    """Costura punteada (textiles): puntos alternos de 1 px."""
    for k, (x, y) in enumerate(puntos):
        if k % 2 == 0:
            p.pset(x, y, hilo)


def manta(p, x0, y0, x1, y1, rampa, pliegues=2):
    """Tela plegada: cuerpo + pliegues en escalon diagonal."""
    p.rect(x0, y0, x1, y1, tono(rampa, 2))
    p.banda_top(x0, y0, x1, y1, tono(rampa, 3))
    p.banda_izq(x0, y0, x1, y1, tono(rampa, 3))
    p.banda_der(x0, y0, x1, y1, tono(rampa, 1))
    p.banda_bot(x0, y0, x1, y1, tono(rampa, 0))
    for k in range(pliegues):
        x = x0 + 3 + k * max(3, (x1 - x0) // (pliegues + 1))
        y = y0 + 2 + k
        for paso in range(min(5, y1 - y0 - 3)):
            p.pset(min(x + paso, x1 - 1), min(y + paso, y1 - 1),
                   tono(rampa, 0 if paso % 2 else 1))
    return (x0, y0, x1, y1)
