# -*- coding: utf-8 -*-
"""Renderiza los sprites 2D del mod.

Uso (desde la raiz del proyecto):
    python -m tools.sprites2d.render <id_item> [<id_item2> ...] [--juego]
    python -m tools.sprites2d.render --todos [--juego]

Genera por cada item:
- docs/sprites2d/<id>.png  : maestro 512 px (con sombra y acabado final).
- textures/item/<id>.png   : 256 px in-game (solo con --juego).
"""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

from PIL import Image

from tools.sprites2d.base import LADO, SALIDA, Lienzo

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs" / "sprites2d"
JUEGO = RAIZ / "src" / "main" / "resources" / "assets" / \
    "chernobylz_recycler" / "textures" / "item"
MODULOS = ("industrial", "chemical", "military", "hospital",
           "residential", "electrical", "componentes", "recursos")


def registro():
    """Une los DIBUJOS de todos los modulos de zona existentes."""
    reg = {}
    for nombre in MODULOS:
        try:
            mod = importlib.import_module(f"tools.sprites2d.{nombre}")
        except ModuleNotFoundError:
            continue
        reg.update(getattr(mod, "DIBUJOS", {}))
    return reg


def renderizar(id_item, juego=False):
    dibujos = registro()
    if id_item not in dibujos:
        raise KeyError(f"sin dibujo para '{id_item}'")
    semilla = sum(ord(c) for c in id_item) * 31 % (1 << 30)
    lienzo = Lienzo(semilla)
    dibujos[id_item](lienzo)
    maestro = lienzo.maestro()
    DOCS.mkdir(parents=True, exist_ok=True)
    ruta_docs = DOCS / f"{id_item}.png"
    maestro.save(ruta_docs)
    ruta_juego = None
    if juego:
        JUEGO.mkdir(parents=True, exist_ok=True)
        ruta_juego = JUEGO / f"{id_item}.png"
        maestro.resize((SALIDA, SALIDA), Image.LANCZOS).save(ruta_juego)
    return ruta_docs, ruta_juego


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="*", help="ids de item a renderizar")
    parser.add_argument("--todos", action="store_true",
                        help="renderizar los 91 ids de tools/items.json")
    parser.add_argument("--juego", action="store_true",
                        help="escribir tambien la textura 256 in-game")
    args = parser.parse_args()

    if args.todos:
        datos = json.loads((RAIZ / "tools" / "items.json").read_text(
            encoding="utf-8"))
        ids = []
        for grupo in datos.values():
            for fila in grupo:
                ids.append(fila["id"])
    else:
        ids = args.ids
    if not ids:
        parser.error("indica ids o --todos")

    dibujos = registro()
    faltan = [i for i in ids if i not in dibujos]
    for id_item in ids:
        if id_item not in dibujos:
            continue
        ruta_docs, ruta_juego = renderizar(id_item, juego=args.juego)
        if ruta_juego:
            print(f"[ok] {id_item} -> {ruta_docs.name} + juego")
        else:
            print(f"[ok] {id_item} -> {ruta_docs.name}")
    if faltan:
        print(f"[!] sin dibujo ({len(faltan)}): {', '.join(faltan)}")


if __name__ == "__main__":
    main()
