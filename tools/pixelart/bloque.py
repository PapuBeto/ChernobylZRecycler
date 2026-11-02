# -*- coding: utf-8 -*-
"""Caras pixel art del bloque reciclador (front, side, top; 16x16 opacas).

Reglas heredadas del motor: luz top-left, bandas escalonadas, dama en las
transiciones, contorno por contraste, sin antialiasing. Las tres caras
comparten cornisa (los cuatro cantos de 1 px) para que las esquinas del cubo
casen sin costura y los bloques vecinos se apoyen en el mismo canto.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from tools.pixelart import pal
from tools.pixelart.formas import (lampara, rejilla_lineas, rejilla_puntos)
from tools.pixelart.px import P, tono

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs" / "pixelart"
JUEGO = RAIZ / "src" / "main" / "resources" / "assets" / \
    "chernobylz_recycler" / "textures" / "block"
LADO = 16


# ------------------------------------------------------------ utilidades
def celda_peligro(x, y):
    """Color de un bloque 2x2 de la franja diagonal amarilla/negra."""
    if ((x - y) // 2) % 2 == 0:
        return tono(pal.AMARILLO, 2)
    return tono(pal.CARBON, 1)


def perno(p, x, y):
    """Tornillo de tapa: pixel de luz con sombra al sur-este."""
    p.pset(x, y, tono(pal.STEEL, 5))
    p.pset(x + 1, y + 1, tono(pal.STEEL, 0))


# ------------------------------------------------------------ cornisa
def carroceria(p):
    """Casco comun a las tres caras: opaco y cantos planos repetibles."""
    acero, hierro = pal.STEEL, pal.HIERRO
    p.rect(0, 0, 15, 15, tono(acero, 2))     # columnas laterales
    p.hlinea(0, 15, 0, tono(acero, 4))       # canto superior iluminado
    p.hlinea(1, 14, 1, tono(acero, 3))       # segunda fila de luz
    p.rect(1, 2, 14, 13, tono(acero, 2))     # cuerpo de chapa
    p.hlinea(1, 14, 14, tono(hierro, 1))     # banda inferior
    p.hlinea(0, 15, 15, tono(hierro, 0))     # canto bajo en sombra


# ------------------------------------------------------------ caras
def cara_front(p):
    """Cara de trabajo: boca de carga con rejilla, panel de control y escape."""
    carroceria(p)
    acero, hierro, carbon = pal.STEEL, pal.HIERRO, pal.CARBON
    # franja de peligro diagonal sobre la cornisa
    for x in range(1, 15):
        p.vlinea(x, 2, 3, celda_peligro(x, 2))
    # canto superior de la maquina
    p.hlinea(1, 14, 4, tono(hierro, 2))
    # panel de control: piloto, palanca y visor de lectura
    p.rect(1, 5, 4, 12, tono(acero, 1))
    p.hlinea(1, 4, 5, tono(acero, 3))
    lampara(p, 2, 7, pal.ROJO)
    p.pset(1, 10, tono(pal.LATON, 2))
    p.pset(1, 11, tono(pal.LATON, 0))
    p.rect(2, 10, 4, 12, tono(pal.CRISTAL, 1))
    p.pset(3, 11, tono(pal.CRISTAL, 4))
    p.pset(2, 12, tono(pal.CRISTAL, 2))
    # boca de carga: receso oscuro con rejilla de barras verticales
    p.rect(5, 5, 10, 12, tono(carbon, 1))
    p.hlinea(5, 10, 5, tono(carbon, 0))
    p.vlinea(5, 5, 12, tono(carbon, 0))
    p.rect(6, 6, 10, 12, tono(carbon, 0))
    p.vlinea(7, 6, 12, tono(acero, 3))
    p.vlinea(9, 6, 12, tono(acero, 3))
    # rejilla de escape mecanica
    rejilla_lineas(p, 11, 5, 14, 12, tono(acero, 4), tono(acero, 1), paso=3)
    # canto inferior de la maquina
    p.hlinea(1, 14, 13, tono(hierro, 1))
    # oxido en la base
    p.pset(3, 14, tono(pal.OXIDO, 1))
    p.pset(12, 13, tono(pal.OXIDO, 2))


def cara_side(p):
    """Lateral: chapa vertical con junta remachada y rejilla de escape."""
    carroceria(p)
    acero, hierro = pal.STEEL, pal.HIERRO
    # cuerpo de chapa con luz de canto arriba e izquierda
    p.rect(1, 2, 14, 13, tono(acero, 2))
    p.hlinea(1, 14, 2, tono(acero, 3))
    p.vlinea(1, 2, 13, tono(acero, 3))
    # junta horizontal de la chapa
    p.hlinea(1, 14, 7, tono(hierro, 0))
    p.hlinea(1, 14, 8, tono(acero, 3))
    for x, y in ((2, 3), (13, 3), (2, 8), (13, 8), (2, 12), (13, 12)):
        perno(p, x, y)
    # rejilla de escape inferior
    rejilla_lineas(p, 1, 10, 14, 13, tono(acero, 3), tono(hierro, 1), paso=3)
    # goteo de oxido bajo la junta
    p.pset(4, 12, tono(pal.OXIDO, 2))
    p.pset(4, 13, tono(pal.OXIDO, 1))
    p.pset(11, 13, tono(pal.OXIDO, 1))


def cara_top(p):
    """Tapa: placa con caja de ventilacion en receso y remaches de esquina."""
    carroceria(p)
    acero, hierro, carbono = pal.STEEL, pal.HIERRO, pal.CARBON
    # placa superior con luz de canto arriba e izquierda
    p.rect(1, 2, 14, 13, tono(acero, 2))
    p.hlinea(1, 14, 2, tono(acero, 3))
    p.vlinea(1, 2, 13, tono(acero, 3))
    p.vlinea(14, 2, 13, tono(hierro, 1))
    p.hlinea(1, 14, 13, tono(hierro, 1))
    # caja de venta en receso con rejilla de puntos
    p.rect(4, 4, 12, 12, tono(carbono, 1))
    p.hlinea(4, 12, 4, tono(carbono, 0))
    p.vlinea(4, 4, 12, tono(carbono, 0))
    p.rect(5, 5, 11, 11, tono(carbono, 0))
    rejilla_puntos(p, 5, 5, cols=3, filas=3, paso=3, c=tono(acero, 3))
    # remaches de esquina de la placa
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)):
        perno(p, x, y)
    # oxido en la base
    p.pset(6, 13, tono(pal.OXIDO, 2))
    p.pset(3, 5, tono(pal.OXIDO, 1))


# ------------------------------------------------------------ salida
CARAS = {"front": cara_front, "side": cara_side, "top": cara_top}
NOMBRES_JUEGO = {"front": "recycler_front.png",
                 "side": "recycler_side.png",
                 "top": "recycler_top.png"}


def _pixel(im, x, y):
    return im.getpixel((x, y))


def _validar(imagenes):
    """Cornisas casadas entre caras y PNGs completamente opacos."""
    fre, lat, tapa = imagenes["front"], imagenes["side"], imagenes["top"]
    for nombre, im in imagenes.items():
        for yy in range(LADO):
            for xx in range(LADO):
                if _pixel(im, xx, yy)[3] != 255:
                    raise AssertionError(
                        f"{nombre}: pixel transparente en {xx},{yy}")
    for yy in (0, LADO - 1):
        fila = [_pixel(fre, xx, yy) for xx in range(LADO)]
        for otra in (lat, tapa):
            if [_pixel(otra, xx, yy) for xx in range(LADO)] != fila:
                raise AssertionError("cornisa superior/inferior inconsistente")
    for xx in (0, LADO - 1):
        col = [_pixel(fre, xx, yy) for yy in range(LADO)]
        for otra in (lat, tapa):
            if [_pixel(otra, xx, yy) for yy in range(LADO)] != col:
                raise AssertionError("cornisa lateral inconsistente")


def hoja(imagenes, destino, zoom=8):
    """Hoja de revision: las tres caras ampliadas sobre fondo neutro."""
    sep = 12
    esc = [im.resize((LADO * zoom, LADO * zoom), Image.NEAREST)
           for im in imagenes.values()]
    ancho = sum(im.width for im in esc) + sep * 4
    alto = esc[0].height + sep * 2
    lienzo = Image.new("RGBA", (ancho, alto), (58, 61, 64, 255))
    x = sep
    for im in esc:
        lienzo.alpha_composite(im, (x, sep))
        x += im.width + sep
    lienzo.save(destino)


def render_caras():
    """Dibuja las tres caras y valida opacidad y cornisa comun."""
    imagenes = {}
    for nombre, dibujo in CARAS.items():
        p = P(LADO)
        dibujo(p)
        imagenes[nombre] = p.img
    _validar(imagenes)
    return imagenes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--juego", action="store_true")
    args = parser.parse_args()
    imagenes = render_caras()
    DOCS.mkdir(parents=True, exist_ok=True)
    for nombre, im in imagenes.items():
        im.save(DOCS / f"bloque_{nombre}.png")
    hoja(imagenes, DOCS / "hoja_bloque.png")
    if args.juego:
        JUEGO.mkdir(parents=True, exist_ok=True)
        for nombre, im in imagenes.items():
            im.save(JUEGO / NOMBRES_JUEGO[nombre])
    sufijo = " (juego)" if args.juego else ""
    print(f"[ok] bloque reciclador: front, side, top{sufijo}")


if __name__ == "__main__":
    main()
