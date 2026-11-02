"""Fase Blockbench — exporta .bbmodel -> JSON de Minecraft 1.20.1 + PNG.

Lee cada proyecto tools/models3d/blockbench/<id>.bbmodel (la fuente editable
de Blockbench) y produce:

- src/main/resources/assets/chernobylz_recycler/models/item/<id>.json
  elements con uv escalada a espacio 0..16 (2 px UV por unidad MC) desde los
  recortes del proyecto; rotation desde el array [x,y,z] del cubo (+ origin);
  display y gui_light tal y como estan guardados en el proyecto.
- src/main/resources/assets/chernobylz_recycler/textures/item/<id>.png
  La textura incrustada del proyecto (data:image/png;base64) decodificada.
  Va en textures/item/ porque es el directorio que vanilla cose al atlas de
  bloques en 1.20.1 (ver docs/DISENO_3D.md); no se usan carpetas nuevas.

El id y las rutas son las mismas que usa el registro de items: solo cambian
los assets.

Uso:  python -m tools.models3d.bbexport [ids...]   (sin ids = todos)
"""

from __future__ import annotations

import base64
import json
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
FUENTE = RAIZ / "tools" / "models3d" / "blockbench"
ASSETS = RAIZ / "src" / "main" / "resources" / "assets" / "chernobylz_recycler"
CARPETA_MODELOS = ASSETS / "models" / "item"
CARPETA_TEXTURAS = ASSETS / "textures" / "item"

CARAS_MC = ("north", "east", "south", "west", "up", "down")


def _link_textura(tex, id_item):
    namespace = tex.get("namespace") or "minecraft"
    carpeta = tex.get("folder") or "item"
    nombre = Path(tex.get("name") or (id_item + ".png")).stem
    return f"{namespace}:{carpeta}/{nombre}"


def _cara_mc(cara_bb, escala):
    """uv del proyecto (px del espacio de resolucion) -> espacio 0..16 de MC."""
    u1, v1, u2, v2 = cara_bb["uv"]
    mc = {
        "uv": [round(u * 16.0 / escala, 4) for u in (u1, v1, u2, v2)],
        "texture": "#tex",
    }
    if cara_bb.get("rotation"):
        mc["rotation"] = int(cara_bb["rotation"])
    return mc


def _elemento_mc(el_bb, escala):
    mc = {
        "name": el_bb.get("name", "cubo"),
        "from": [round(float(v), 6) for v in el_bb["from"]],
        "to": [round(float(v), 6) for v in el_bb["to"]],
        "faces": {},
    }
    rot = el_bb.get("rotation")
    if isinstance(rot, dict):
        mc["rotation"] = {
            "axis": rot.get("axis", "y"),
            "angle": float(rot.get("angle", 0)),
            "origin": [round(float(v), 6) for v in rot.get("origin", [8, 8, 8])],
        }
    elif isinstance(rot, (list, tuple)) and any(abs(v) > 0 for v in rot):
        i = next(i for i, v in enumerate(rot) if abs(v) > 0)
        mc["rotation"] = {
            "axis": ("x", "y", "z")[i],
            "angle": float(rot[i]),
            "origin": [round(float(v), 6) for v in el_bb.get("origin", [8, 8, 8])],
        }
    caras = el_bb.get("faces") or {}
    for cara in CARAS_MC:
        f = caras.get(cara)
        if f is None or f.get("texture") is None:
            continue
        mc["faces"][cara] = _cara_mc(f, escala)
    return mc


def exportar(id_item):
    ruta = FUENTE / (id_item + ".bbmodel")
    if not ruta.exists():
        print("falta %s" % ruta.relative_to(RAIZ))
        return False
    proyecto = json.loads(ruta.read_text(encoding="utf-8"))

    res = proyecto.get("resolution", {})
    escala = float(res.get("width", 16) or 16)

    texturas_bb = proyecto.get("textures") or []
    if not texturas_bb:
        print(f"[{id_item}] el proyecto no tiene texturas incrustadas")
        return False
    tex = texturas_bb[0]
    source = tex.get("source") or ""
    if not source.startswith("data:image/png;base64,"):
        print(f"[{id_item}] la textura 0 no es PNG incrustado")
        return False
    png = base64.b64decode(source.split(",", 1)[1])

    # validacion: los indices de textura de las caras deben existir
    n_tex = len(texturas_bb)
    for el_bb in proyecto.get("elements", []):
        for f in (el_bb.get("faces") or {}).values():
            t = f.get("texture")
            if isinstance(t, int) and not (0 <= t < n_tex):
                print(f"[{id_item}] cara con indice de textura {t} fuera de rango")
                return False

    modelo_mc = {
        "gui_light": "front" if proyecto.get("front_gui_light") else "side",
        "display": proyecto.get("display", {}),
        "textures": {"tex": _link_textura(tex, id_item)},
        "elements": [_elemento_mc(el_bb, escala) for el_bb in proyecto.get("elements", [])],
    }

    CARPETA_TEXTURAS.mkdir(parents=True, exist_ok=True)
    ruta_png = CARPETA_TEXTURAS / (id_item + ".png")
    ruta_png.write_bytes(png)
    Image.open(BytesIO(png)).verify()  # sanity: el PNG decodifica

    CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)
    ruta_json = CARPETA_MODELOS / (id_item + ".json")
    ruta_json.write_text(
        json.dumps(modelo_mc, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("ok  %s -> %s + %s (%d elementos)"
          % (id_item, ruta_json.relative_to(RAIZ), ruta_png.relative_to(RAIZ),
             len(modelo_mc["elements"])))
    return True


def main(argv):
    ids = list(dict.fromkeys(argv)) or sorted(p.stem for p in FUENTE.glob("*.bbmodel"))
    if not ids:
        print("no hay .bbmodel en %s" % FUENTE.relative_to(RAIZ))
        return 1
    bien = all(exportar(i) for i in ids)
    return 0 if bien else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
