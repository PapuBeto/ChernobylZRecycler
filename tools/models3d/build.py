"""Fase Blockbench consolidada — delega en bbsrc (proyecto .bbmodel) y bbexport.

Uso:  python -m tools.models3d.build [ids...]

El generador del atlas plano de la Fase 1 quedo obsoleto: sobrescribia la
textura pintada con color plano y no lleva proyectos editables. El flujo
vigente es:

1. specs validadas  ->  bbsrc  ->  tools/models3d/blockbench/<id>.bbmodel
   (proyecto Blockbench FUENTE: geometria + grupos + UV + textura pintada
   incrustada + display; editable en Blockbench)
2. bbmodel          ->  bbexport ->  assets: models/item/<id>.json +
   textures/item/<id>.png (uv escalada a 0..16; PNG decodificado del
   data URI incrustado; caras/rotaciones/display passthrough)

Los previews texturizados salen de bbpreview (documentacion en
docs/DISENO_3D.md, seccion flujo Blockbench).
"""

from __future__ import annotations

import sys

from tools.models3d.bbexport import exportar
from tools.models3d.bbsrc import construir
from tools.models3d.render import cargar_specs


def main(argv):
    from pathlib import Path

    ids = set(argv)
    specs = cargar_specs()
    if ids:
        specs = [s for s in specs if s.id in ids]
        faltan = ids - {s.id for s in specs}
        if faltan:
            print("sin spec para: " + ", ".join(sorted(faltan)))
            return 1
    pedidos = {s.id for s in specs}
    bien = all(construir(s) for s in specs)
    carpeta_bb = Path(__file__).resolve().parent / "blockbench"
    desde_bb = sorted(p.stem for p in carpeta_bb.glob("*.bbmodel") if p.stem in pedidos)
    return 0 if bien and all(exportar(i) for i in desde_bb) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
