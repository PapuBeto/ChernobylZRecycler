"""Fase Blockbench — genera el proyecto fuente .bbmodel por item.

El .bbmodel es ahora la fuente editable del modelado 3D (el usuario puede
abrirlo en Blockbench, formato Java Block/Item, y seguir editando geometria,
grupos y UV). Este modulo lo construye desde las specs validadas:

- meta: format_version 4.10 (los 4.x y 5.x lo abren), java_block, box_uv false
- resolution: {32, 32} = espacio UV (2 px UV por unidad de Minecraft)
- elements: cubos de la spec con faces {north..down} apuntando al indice de
  la textura, rota ciones como array [x,y,z] + origin (formato de proyecto)
- groups + outliner: grupos logicos por componente con hijos por uuid
- textures: UNA textura por item (painter de bbpaint) incrustada como
  data:image/png;base64
- display: copia de palette.display_estandar (mismo formato que el JSON MC)

Uso:  python -m tools.models3d.bbsrc [ids...]
Salida: tools/models3d/blockbench/<id>.bbmodel
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import sys
from pathlib import Path

from tools.models3d.bbpaint import (
    ESCALA_PNG,
    dims_cara,
    firmas_de_spec,
    pintar_textura,
    planificar,
)
from tools.models3d.palette import display_estandar, resolver
from tools.models3d.render import cargar_specs
from tools.models3d.spec import Spec

CARAS_MC_ES = ("norte", "sur", "este", "oeste", "arriba", "abajo")
CARA_A_MC = {
    "norte": "north", "sur": "south", "este": "east",
    "oeste": "west", "arriba": "up", "abajo": "down",
}

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "tools" / "models3d" / "blockbench"

GRUPOS = {
    "motor_grua_sovietica": [
        ("Bancada", ("zapata", "rem_base")),
        ("Pies", ("pie_",)),
        ("Carcasa", ("carcaza", "aleta")),
        ("Acople", ("tapa_delantera", "eje", "collar")),
        ("Volante", ("volante", "diente", "centro")),
        ("Bornes y escape", ("caja_bornes", "escape", "tapa_escape")),
        ("Hidraulica", ("bota", "vastago", "copa")),
        ("Accesorios", ("caja_cobre", "tornillo_cobre", "placa_marca", "puerto")),
        ("Desgaste", ("hollin", "mugre")),
    ],
    "bateria_tanque_t72": [
        ("Peana y caja", ("peana", "caja")),
        ("Tapa y tapones", ("tapa", "tapon")),
        ("Bornes", ("torre", "bozal", "tornillo")),
        ("Sulfato", ("costra",)),
        ("Herrajes", ("corchete", "hebilla", "manija", "oxido_correa")),
        ("Placa", ("placa_datos",)),
        ("Desgaste", ("mugre_pie",)),
    ],
    "radio_campana_r159": [
        ("Caja y pies", ("caja", "pie_")),
        ("Rejilla", ("reja", "barra_reja")),
        ("Botonera", ("teclado", "tecla", "selector", "marcador", "led_")),
        ("Antena", ("prolongador", "varilla", "seguro")),
        ("Cifrado", ("modulo_cifrado", "borne_mod")),
        ("Asa y prensas", ("asa", "prensa")),
        ("Desgaste", ("patina", "mugre_pie")),
    ],
    "contador_geiger_pripyat": [
        ("Cuerpo", ("cuerpo", "faldon")),
        ("Visor", ("arco_visor", "vidrio", "remache")),
        ("Botonera", ("boton",)),
        ("Dial lateral", ("dial_lateral", "volante_dial")),
        ("Asa y correa", ("post_izq", "asa_barra", "grip", "stub_der", "correa")),
        ("Sonda", ("tuerca_sonda", "flange_sonda", "aro_sonda", "tapa_sonda", "ventana", "cable")),
        ("Desgaste", ("imprimacion", "oxido")),
    ],
    "traje_hazmat_liquidador": [
        ("Piernas", ("pierna", "bota_")),
        ("Torso", ("torso", "cinturon", "hebilla")),
        ("Respirador", ("respirador", "filtro", "valvula")),
        ("Capucha", ("capucha_baja", "corona", "visor")),
        ("Brazos", ("brazo", "guante", "rasgadura")),
        ("Desgaste", ("patina", "moho", "goteo")),
    ],
}


def _uuid(semilla):
    """UUID v4-compat determinista a partir de la semilla (estable por regeneracion)."""
    h = hashlib.md5(("chernobylz:" + semilla).encode("utf-8")).hexdigest()
    h = h[:12] + "4" + h[13:16] + "a" + h[17:32]
    return "-".join((h[0:8], h[8:12], h[12:16], h[16:20], h[20:32]))


def materiales_de_spec(spec):
    """[(clave_material, dims), ...] UNA ENTRADA POR CARA (sin duplicar)."""
    usos = []
    for pieza in spec.piezas:
        for cara_es in CARAS_MC_ES:
            clave = pieza.caras.get(cara_es, pieza.material)
            resolver(clave)
            usos.append((clave, dims_cara(pieza.desde, pieza.hasta, cara_es)))
    return usos


def _grupo_de(nombre_expandido, id_item):
    if id_item not in GRUPOS:
        return "Sin grupo"
    for grupo, prefijos in GRUPOS[id_item]:
        for prefijo in prefijos:
            if nombre_expandido.startswith(prefijo):
                return grupo
    return "Sin grupo"


def _elemento(pieza, id_item, rects_material, rects_firmas):
    """Dict de elemento bbmodel (cubo) desde una Pieza."""
    caras = {}
    for cara_es in CARAS_MC_ES:
        clave_material = pieza.caras.get(cara_es, pieza.material)
        clave_firma = (pieza.nombre, cara_es)
        dims = dims_cara(pieza.desde, pieza.hasta, cara_es)
        rect = rects_firmas.get(clave_firma) or rects_material.get((clave_material, dims))
        if rect is None:
            raise ValueError(
                f"{id_item}: sin recorte para {clave_material} {dims} / firma {clave_firma}"
            )
        caras[CARA_A_MC[cara_es]] = {
            "uv": [rect[0], rect[1], rect[2], rect[3]],
            "texture": 0,
        }
    el = {
        "name": pieza.nombre,
        "box_uv": False,
        "rescale": False,
        "locked": False,
        "render_order": "default",
        "allow_mirror_modeling": True,
        "from": [float(v) for v in pieza.desde],
        "to": [float(v) for v in pieza.hasta],
        "autouv": 0,
        "color": 0,
        "origin": ([float(v) for v in pieza.rotacion.origen] if pieza.rotacion else [8.0, 8.0, 8.0]),
        "faces": caras,
        "type": "cube",
        "uuid": _uuid(f"{id_item}:el:{pieza.nombre}"),
    }
    if pieza.rotacion is not None:
        rot = [0.0, 0.0, 0.0]
        i = ("x", "y", "z").index(pieza.rotacion.eje)
        rot[i] = float(pieza.rotacion.angulo)
        el["rotation"] = rot
        el["rotation_axis"] = pieza.rotacion.eje
    return el


def _construir_grupos(spec):
    """outliner: lista de grupos (dicts con children, uuid incluidos)."""
    por_grupo = {}
    orden = []
    for pieza in spec.piezas:
        g = _grupo_de(pieza.nombre, spec.id)
        if g not in por_grupo:
            por_grupo[g] = []
            orden.append(g)
        por_grupo[g].append(pieza)
    out = []
    for g in orden:
        uuid_g = _uuid(f"{spec.id}:grupo:{g}")
        origin = [8.0, 8.0, 8.0]
        out.append({
            "name": g,
            "origin": origin,
            "color": 0,
            "uuid": uuid_g,
            "export": True,
            "isOpen": True,
            "locked": False,
            "visibility": True,
            "autouv": 0,
            "children": [_uuid(f"{spec.id}:el:{p.nombre}") for p in por_grupo[g]],
        })
    sueltos = [p for p in spec.piezas if _grupo_de(p.nombre, spec.id) == "Sin grupo"]
    for p in sueltos:
        out.append(_uuid(f"{spec.id}:el:{p.nombre}"))
    return out


def construir_bbmodel(spec, datos_retorno=None):
    """Devuelve el dict completo del proyecto .bbmodel."""
    errores, avisos = spec.validar()
    for a in avisos:
        print("aviso [%s] %s" % (spec.id, a))
    if errores:
        for e in errores:
            print("ERROR [%s] %s" % (spec.id, e))
        return None

    claves = materiales_de_spec(spec)
    firmas = firmas_de_spec(spec)
    (rects_material, rects_firmas), lado_uv = planificar(claves, firmas)

    imagen = pintar_textura(spec, rects_material, rects_firmas, lado_uv=lado_uv)
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

    texture = {
        "path": "",
        "name": spec.id + ".png",
        "folder": "item",
        "namespace": "chernobylz_recycler",
        "id": "tex",
        "particle": False,
        "width": imagen.size[0],
        "height": imagen.size[1],
        "uv_width": lado_uv,
        "uv_height": lado_uv,
        "visible": True,
        "render_mode": "default",
        "render_sides": "auto",
        "frame_time": 1,
        "frame_order_type": "loop",
        "frame_order": "",
        "frame_interpolate": False,
        "layered": False,
        "layers_identical": True,
        "sync_to_project": "",
        "saved": False,
        "internal": True,
        "uuid": _uuid(f"{spec.id}:texture:0"),
        "source": data_uri,
        "relative_path": "",
    }

    elementos = [_elemento(p, spec.id, rects_material, rects_firmas) for p in spec.piezas]

    modelo = {
        "meta": {
            "format_version": "4.10",
            "model_format": "java_block",
            "box_uv": False,
        },
        "name": spec.nombre or spec.id,
        "model_identifier": spec.id,
        "visible_box": [1.0, 1.0, 0.0],
        "unhandled_root_fields": {
            "credit": "chernobylz_recycler 3D — fuente editable Blockbench",
        },
        "ambientocclusion": False,
        "front_gui_light": False,
        "resolution": {"width": lado_uv, "height": lado_uv},
        "elements": elementos,
        "outliner": _construir_grupos(spec),
        "groups": [],
        "textures": [texture],
        "display": display_estandar(spec.clase),
    }
    datos_retorno = datos_retorno or {}
    datos_retorno["rects_material"] = rects_material
    datos_retorno["rects_firmas"] = rects_firmas
    datos_retorno["lado_uv"] = lado_uv
    return modelo


def construir(spec):
    modelo = construir_bbmodel(spec)
    if modelo is None:
        return False
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = SALIDA / (spec.id + ".bbmodel")
    ruta.write_text(
        json.dumps(modelo, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("ok  %s (%d elementos, %d firmas) -> %s"
          % (spec.id, len(modelo["elements"]),
             len(firmas_de_spec(spec)), ruta.relative_to(RAIZ)))
    return True


def main(argv):
    ids = set(argv)
    specs = cargar_specs()
    if ids:
        specs = [s for s in specs if s.id in ids]
        faltan = ids - {s.id for s in specs}
        if faltan:
            print("sin spec para: " + ", ".join(sorted(faltan)))
            return 1
    bien = all(construir(s) for s in specs)
    return 0 if bien else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
