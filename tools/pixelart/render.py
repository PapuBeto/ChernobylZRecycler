# -*- coding: utf-8 -*-
"""Renderiza los sprites pixel art del mod.

Uso (desde la raiz del proyecto):
    python -m tools.pixelart.render <id_item> [<id_item2> ...] [--juego]
    python -m tools.pixelart.render --todos [--juego]
    python -m tools.pixelart.render --hoja <id1,id2,...>

Genera por cada item:
- docs/pixelart/<id>.png            : sprite nativo (32x32).
- textures/item/<id>.png            : mismo PNG, in-game (solo con --juego).
- docs/pixelart/hoja_contacto.png   : conjunto ampliada x6 en fondo neutro.
"""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

from PIL import Image

from tools.pixelart.px import P

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs" / "pixelart"
JUEGO = RAIZ / "src" / "main" / "resources" / "assets" / \
    "chernobylz_recycler" / "textures" / "item"
MODULOS = ("pilotos", "componentes", "industrial", "militar",
           "medico", "hogar", "electrico", "construccion")


def registro():
    reg = {}
    for nombre in MODULOS:
        try:
            mod = importlib.import_module(f"tools.pixelart.{nombre}")
        except ModuleNotFoundError:
            continue
        reg.update(getattr(mod, "DIBUJOS", {}))
    return reg


def renderizar(id_item, juego=False):
    dibujos = registro()
    if id_item not in dibujos:
        raise KeyError(f"sin sprite pixel para '{id_item}'")
    p = P()
    dibujos[id_item](p)
    DOCS.mkdir(parents=True, exist_ok=True)
    ruta_docs = DOCS / f"{id_item}.png"
    p.img.save(ruta_docs)
    ruta_juego = None
    if juego:
        JUEGO.mkdir(parents=True, exist_ok=True)
        ruta_juego = JUEGO / f"{id_item}.png"
        p.img.save(ruta_juego)      # nativo, sin reescalar
    return ruta_docs, ruta_juego


def hoja_contacto(rutas, archivo="hoja_contacto.png", zoom=6):
    """Conjunto de sprites ampliados x6 (vecino mas cercano) sobre neutro."""
    escalados = [Image.open(ruta).resize((32 * zoom, 32 * zoom), Image.NEAREST)
                 for ruta in rutas]
    sep = 12
    w = sum(im.width for im in escalados) + sep * (len(escalados) + 1)
    h = escalados[0].height + sep * 2
    hoja = Image.new("RGBA", (w, h), (58, 61, 64, 255))
    x = sep
    for im in escalados:
        hoja.alpha_composite(im, (x, sep))
        x += im.width + sep
    destino = DOCS / archivo
    hoja.save(destino)
    return destino


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--todos", action="store_true")
    parser.add_argument("--juego", action="store_true")
    parser.add_argument("--hoja", default=None,
                        help="ids separados por coma -> hoja de contacto")
    args = parser.parse_args()

    dibujos = registro()
    if args.hoja:
        ids = [s.strip() for s in args.hoja.split(",") if s.strip()]
        rutas = []
        for id_item in ids:
            ruta_docs, _ = renderizar(id_item)
            rutas.append(ruta_docs)
        print(f"[ok] hoja -> {hoja_contacto(rutas)}")
        return

    if args.todos:
        datos = json.loads((RAIZ / "tools" / "items.json").read_text(
            encoding="utf-8"))
        ids = [fila["id"] for grupo in datos.values() for fila in grupo]
    else:
        ids = args.ids
    if not ids:
        parser.error("indica ids, --todos o --hoja")

    faltan = []
    for id_item in ids:
        if id_item not in dibujos:
            faltan.append(id_item)
            continue
        ruta_docs, ruta_juego = renderizar(id_item, juego=args.juego)
        if ruta_juego:
            print(f"[ok] {id_item} -> {ruta_docs.name} + juego")
        else:
            print(f"[ok] {id_item} -> {ruta_docs.name}")
    if faltan:
        print(f"[!] sin sprite ({len(faltan)}): {', '.join(faltan)}")


if __name__ == "__main__":
    main()
