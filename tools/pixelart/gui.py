# -*- coding: utf-8 -*-
"""Textura GUI del reciclador (176x166, panel oscuro estilo generador).

Tema: panel casi negro con bordes grises finos, franja de cabecera para el
titulo blanco (el texto lo dibuja RecyclerScreen) y acentos verdes en la
barra de progreso de 5 segmentos. Layout tipo Rust: fila de 5 slots de
entrada, medidor, fila de 5 slots de salida, inventario del jugador.

Las posiciones son las del Java (constructor de RecyclerMenu y BARRA_* de
RecyclerScreen); el marco 18x18 de cada slot rodea al item de 16x16.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from tools.pixelart import pal
from tools.pixelart.px import P, tono

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs" / "pixelart"
JUEGO = RAIZ / "src" / "main" / "resources" / "assets" / \
    "chernobylz_recycler" / "textures" / "gui"

ANCHO = 176
ALTO = 166

# ---------------------------- paleta del panel oscuro
CUERPO = tono(pal.CARBON, 1)        # fondo del panel
_LINEA = (8, 9, 11)                 # borde exterior casi negro
CANTO = tono(pal.STEEL, 1)          # filete interior del marco
CABECERA = tono(pal.CARBON, 2)      # franja del titulo
RIM = tono(pal.STEEL, 2)            # marco de los slots
HUECO = tono(pal.CARBON, 0)         # interior oscuro de slots y barra

# ---------------------------- coords fijas (no mover sin tocar el Java)
ENTRADA_X = 44          # fila de 5 slots de entrada centrada, paso 18
ENTRADA_Y = 24
SALIDA_Y = 60           # fila de 5 slots de salida, mismas columnas
INV_X = 8               # inventario del jugador 3x9, paso 18
INV_Y = (89, 107, 125)
HOTBAR_Y = 147
BARRA_MARCO = (47, 44, 128, 56)     # marco del medidor


def _celda_peligro(x, y):
    """Color de un bloque 2x2 de la franja diagonal amarilla/negra."""
    if ((x - y) // 2) % 2 == 0:
        return tono(pal.AMARILLO, 2)
    return tono(pal.CARBON, 1)


def franja_peligro(p, x0, y0, x1, y1):
    """Franja diagonal de advertencia entre dos puntos."""
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            p.pset(x, y, _celda_peligro(x, y))


def panel(p):
    """Cuerpo oscuro del dialogo con borde exterior y cabecera del titulo."""
    p.rect(0, 0, ANCHO - 1, ALTO - 1, CUERPO)
    p.marco(0, 0, ANCHO - 1, ALTO - 1, _LINEA)
    p.marco(1, 1, ANCHO - 2, ALTO - 2, CANTO)
    # franja de cabecera donde el Java dibuja el titulo blanco
    p.rect(2, 2, ANCHO - 3, 17, CABECERA)
    p.hlinea(2, ANCHO - 3, 17, CANTO)
    # marca de zona: mini franja de peligro al final de la cabecera
    franja_peligro(p, 158, 6, 170, 7)


def hueco_slot(p, x_item, y_item):
    """Slot 18x18 alrededor del item: marco gris e interior casi negro."""
    p.rect(x_item - 1, y_item - 1, x_item + 16, y_item + 16, RIM)
    p.rect(x_item, y_item, x_item + 15, y_item + 15, HUECO)


def fila_slots(p, x0, y, n=5):
    """Fila horizontal de n slots con paso 18."""
    for c in range(n):
        hueco_slot(p, x0 + c * 18, y)


def medidor_barra(p):
    """Marco del medidor de progreso: igual que los slots pero en pieza."""
    x0, y0, x1, y1 = BARRA_MARCO
    p.rect(x0, y0, x1, y1, RIM)
    p.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, HUECO)


def dibujar_gui(p):
    """Compone la GUI completa en el orden correcto."""
    panel(p)
    fila_slots(p, ENTRADA_X, ENTRADA_Y)
    medidor_barra(p)
    fila_slots(p, ENTRADA_X, SALIDA_Y)
    for y in INV_Y:
        fila_slots(p, INV_X, y, n=9)
    fila_slots(p, INV_X, HOTBAR_Y, n=9)


def _validar(img):
    """El PNG debe medir exactamente 176x166 y ser opaco."""
    if img.size != (ANCHO, ALTO):
        raise AssertionError(f"tamano {img.size} != ({ANCHO},{ALTO})")
    for px in img.getdata():
        if px[3] != 255:
            raise AssertionError("pixel transparente en la gui")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--juego", action="store_true")
    args = parser.parse_args()
    p = P(ANCHO)
    dibujar_gui(p)
    img = p.img.crop((0, 0, ANCHO, ALTO))
    _validar(img)
    DOCS.mkdir(parents=True, exist_ok=True)
    img.save(DOCS / "gui_recycler.png")
    img.resize((ANCHO * 2, ALTO * 2), Image.NEAREST).save(
        DOCS / "hoja_gui.png")
    if args.juego:
        JUEGO.mkdir(parents=True, exist_ok=True)
        img.save(JUEGO / "recycler.png")
    sufijo = " (juego)" if args.juego else ""
    print(f"[ok] gui reciclador panel oscuro 176x166{sufijo}")


if __name__ == "__main__":
    main()
