#!/usr/bin/env python3
"""
Generador de contenido de Chernobyl Z: Reciclaje.

Lee tools/items.json y produce:
  - src/main/java/com/chernobylz/recycler/registry/ModItems.java
  - modelos de item, lang en_us/es_es/es_mx
  - recetas de reciclaje (Fase 1 y Fase 2)
  - tags de items (zonas, componentes, basura, compuestos)
  - loot modifiers (zombis + cofres de ejemplo)
  - texturas placeholder (no sobreescribe arte existente)
  - texturas del bloque y del GUI, blockstate y modelo de bloque
  - docs/ITEMS.md

Uso:
  python tools/generate.py                # genera todo, respeta texturas existentes
  python tools/generate.py --force-textures   # regenera los placeholders
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
MODID = "chernobylz_recycler"
JAVA_DIR = ROOT / "src/main/java/com/chernobylz/recycler"
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets" / MODID
DATA = RES / "data" / MODID
FORGE_DATA = RES / "data/forge"
DOCS = ROOT / "docs"

FORCE_TEXTURES = "--force-textures" in sys.argv

ZONES = ["industrial", "chemical", "military", "hospital", "residential", "electrical"]

ZONE_ES = {
    "industrial": "Zona Industrial",
    "chemical": "Zona Química",
    "military": "Zona Militar",
    "hospital": "Zona Hospital",
    "residential": "Zona Residencial",
    "electrical": "Componentes Eléctricos",
}

ZONE_COLOR = {
    "industrial": (124, 136, 148),
    "chemical": (143, 163, 74),
    "military": (122, 120, 80),
    "hospital": (159, 184, 188),
    "residential": (176, 154, 122),
    "electrical": (176, 128, 80),
}

RESOURCE_COLOR = {
    "tela": (207, 198, 174),
    "scrap": (150, 150, 150),
    "lingote_pesado": (110, 118, 129),
}

COMPONENT_COLOR = (154, 143, 128)

# Tintes para que cada componente tenga su propio tono (los placeholders se
# distinguen mejor en el inventario).
COMPONENT_TINTS = [
    (196, 200, 206),
    (168, 186, 176),
    (196, 172, 132),
    (152, 160, 190),
    (188, 158, 150),
    (170, 178, 150),
]

TIER_MULT = {1: 1.0, 2: 1.4, 3: 2.0}

# Prefijo de las claves de idioma
LANG_PREFIX = "item." + MODID + "."


def load_data():
    with open(ROOT / "tools/items.json", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def all_items(data):
    """Devuelve (id, kind, zone, tier, es, en) en orden de registro."""
    out = []
    for res in data["resources"]:
        out.append(
            {
                "id": res["id"],
                "kind": "resource",
                "zone": None,
                "tier": 0,
                "es": res["es"],
                "en": res["en"],
            }
        )
    for comp in data["components"]:
        out.append(
            {
                "id": comp["id"],
                "kind": "component",
                "zone": None,
                "tier": 0,
                "es": comp["es"],
                "en": comp["en"],
                "use_es": comp.get("use_es", ""),
                "use_en": comp.get("use_en", ""),
            }
        )
    for obj in data["objects"]:
        out.append(
            {
                "id": obj["id"],
                "kind": obj["kind"],
                "zone": obj["zone"],
                "tier": obj["tier"],
                "es": obj["es"],
                "en": obj["en"],
            }
        )
    return out


# --------------------------------------------------------------------------
# Java
# --------------------------------------------------------------------------

def generate_java(items) -> None:
    lines = [
        "package com.chernobylz.recycler.registry;",
        "",
        "import com.chernobylz.recycler.ChernobylZRecycler;",
        "import com.chernobylz.recycler.item.RecyclerItem;",
        "import java.util.List;",
        "import net.minecraft.world.item.Item;",
        "import net.minecraft.world.item.Rarity;",
        "import net.minecraftforge.eventbus.api.IEventBus;",
        "import net.minecraftforge.registries.DeferredRegister;",
        "import net.minecraftforge.registries.ForgeRegistries;",
        "import net.minecraftforge.registries.RegistryObject;",
        "",
        "/**",
        " * Registro de items. ARCHIVO GENERADO por tools/generate.py.",
        " * Edita tools/items.json y vuelve a ejecutar el generador.",
        " */",
        "public final class ModItems {",
        '    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ChernobylZRecycler.MODID);',
        "",
    ]

    const_names = []
    for item in items:
        const = item["id"].upper()
        const_names.append(const)
        if item["kind"] == "resource":
            max_stack, rarity, keys = 64, "Rarity.COMMON", '"tooltip.resource"'
        elif item["kind"] == "component":
            max_stack, rarity = 64, "Rarity.COMMON"
            keys = f'"tooltip.component", "use.{item["id"]}"'
        elif item["kind"] == "compound":
            max_stack = 16
            rarity = {1: "Rarity.COMMON", 2: "Rarity.UNCOMMON", 3: "Rarity.RARE"}[item["tier"]]
            keys = '"tooltip.compound"'
        else:
            max_stack, rarity, keys = 64, "Rarity.COMMON", '"tooltip.simple"'
        lines.append(
            f'    public static final RegistryObject<Item> {const} = register('
            f'"{item["id"]}", {max_stack}, {rarity}, {keys});'
        )

    lines += [
        "",
        "    private static RegistryObject<Item> register(String id, int maxStack, Rarity rarity, String... tooltipKeys) {",
        "        return ITEMS.register(id, () -> new RecyclerItem(new Item.Properties().stacksTo(maxStack).rarity(rarity), tooltipKeys));",
        "    }",
        "",
        "    /** Todos los items, en el orden del documento de diseno. */",
        "    public static final List<RegistryObject<Item>> ALL = List.of(",
    ]
    for i, const in enumerate(const_names):
        suffix = "," if i < len(const_names) - 1 else ""
        lines.append(f"            {const}{suffix}")
    lines += [
        "    );",
        "",
        "    public static void register(IEventBus modBus) {",
        "        ITEMS.register(modBus);",
        "    }",
        "",
        "    private ModItems() {",
        "    }",
        "}",
        "",
    ]

    target = JAVA_DIR / "registry/ModItems.java"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
# Assets: modelos + idioma
# --------------------------------------------------------------------------

def generate_item_models(items) -> None:
    for item in items:
        write_json(
            ASSETS / "models/item" / f'{item["id"]}.json',
            {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{item['id']}"}},
        )


def generate_lang(items) -> None:
    common_es = {
        "itemGroup.chernobylz_recycler": "Chernobyl Z: Reciclaje",
        "block.chernobylz_recycler.recycler": "Recicladora",
        "item.chernobylz_recycler.tooltip.resource": "Recurso base",
        "item.chernobylz_recycler.tooltip.component": "Componente util - Fase 2",
        "item.chernobylz_recycler.tooltip.compound": "Objeto compuesto - Fase 1 + Fase 2",
        "item.chernobylz_recycler.tooltip.simple": "Objeto simple - Fase 1",
        "item.chernobylz_recycler.tooltip.phase1": "Fase 1: %s",
        "item.chernobylz_recycler.tooltip.phase2": "Fase 2: %s",
        "item.chernobylz_recycler.tooltip.components": "Componentes: %s",
        "item.chernobylz_recycler.tooltip.entry": "%sx %s",
        "item.chernobylz_recycler.tooltip.none": "No reciclable",
        "commands.chernobylz_recycler.loot.success": "Entregados %s objeto(s) de %s a %s jugador(es).",
        "commands.chernobylz_recycler.loot.empty": "El tag %s esta vacio. Revisa los datos del datapack.",
        "commands.chernobylz_recycler.unknown_zone": "Zona desconocida: %s",
        "commands.chernobylz_recycler.zones.header": "Zonas disponibles (%s):",
        "commands.chernobylz_recycler.zones.entry": "%s (%s objetos)",
        "zone.chernobylz_recycler.industrial": "Zona Industrial",
        "zone.chernobylz_recycler.chemical": "Zona Quimica",
        "zone.chernobylz_recycler.military": "Zona Militar",
        "zone.chernobylz_recycler.hospital": "Zona Hospital",
        "zone.chernobylz_recycler.residential": "Zona Residencial",
        "zone.chernobylz_recycler.electrical": "Componentes Electricos",
    }
    common_en = {
        "itemGroup.chernobylz_recycler": "Chernobyl Z: Recycling",
        "block.chernobylz_recycler.recycler": "Recycler",
        "item.chernobylz_recycler.tooltip.resource": "Base resource",
        "item.chernobylz_recycler.tooltip.component": "Useful component - Phase 2",
        "item.chernobylz_recycler.tooltip.compound": "Compound item - Phase 1 + Phase 2",
        "item.chernobylz_recycler.tooltip.simple": "Simple item - Phase 1",
        "item.chernobylz_recycler.tooltip.phase1": "Phase 1: %s",
        "item.chernobylz_recycler.tooltip.phase2": "Phase 2: %s",
        "item.chernobylz_recycler.tooltip.components": "Components: %s",
        "item.chernobylz_recycler.tooltip.entry": "%sx %s",
        "item.chernobylz_recycler.tooltip.none": "Not recyclable",
        "commands.chernobylz_recycler.loot.success": "Gave %s item(s) from %s to %s player(s).",
        "commands.chernobylz_recycler.loot.empty": "Tag %s is empty. Check the datapack data.",
        "commands.chernobylz_recycler.unknown_zone": "Unknown zone: %s",
        "commands.chernobylz_recycler.zones.header": "Available zones (%s):",
        "commands.chernobylz_recycler.zones.entry": "%s (%s items)",
        "zone.chernobylz_recycler.industrial": "Industrial Zone",
        "zone.chernobylz_recycler.chemical": "Chemical Zone",
        "zone.chernobylz_recycler.military": "Military Zone",
        "zone.chernobylz_recycler.hospital": "Hospital Zone",
        "zone.chernobylz_recycler.residential": "Residential Zone",
        "zone.chernobylz_recycler.electrical": "Electrical Components",
    }

    es = dict(common_es)
    en = dict(common_en)
    for item in items:
        es[LANG_PREFIX + item["id"]] = item["es"]
        en[LANG_PREFIX + item["id"]] = item["en"]
        if item["kind"] == "component" and item.get("use_es"):
            es[LANG_PREFIX + "use." + item["id"]] = item["use_es"]
            en[LANG_PREFIX + "use." + item["id"]] = item["use_en"]

    write_json(ASSETS / "lang/es_es.json", es)
    write_json(ASSETS / "lang/es_mx.json", es)
    write_json(ASSETS / "lang/en_us.json", en)


# --------------------------------------------------------------------------
# Datapack: recetas, tags, loot
# --------------------------------------------------------------------------

def stack_json(entry) -> dict:
    item_id, count = entry
    return {"item": f"{MODID}:{item_id}", "count": count}


def processing_time(kind: str, tier: int) -> int:
    if kind == "simple":
        base = 70
    elif kind == "compound":
        base = 120
    else:
        base = 80
    mult = TIER_MULT.get(tier, 1.0)
    return int(round(base * mult / 5.0) * 5)


def generate_recipes(data) -> None:
    recipe_dir = DATA / "recipes/recycling"

    for obj in data["objects"]:
        payload = {
            "type": f"{MODID}:recycling",
            "phase": 1,
            "processing_time": processing_time(obj["kind"], obj["tier"]),
            "ingredient": {"item": f"{MODID}:{obj['id']}"},
            "base": [stack_json(e) for e in obj["base"]],
            "components": [stack_json(e) for e in obj.get("components", [])],
        }
        write_json(recipe_dir / f'{obj["id"]}.json', payload)

    for comp in data["components"]:
        payload = {
            "type": f"{MODID}:recycling",
            "phase": 2,
            "processing_time": 80,
            "ingredient": {"item": f"{MODID}:{comp['id']}"},
            "base": [stack_json(e) for e in comp["recycle"]],
            "components": [],
        }
        write_json(recipe_dir / f'{comp["id"]}.json', payload)


def generate_tags(data) -> None:
    tag_dir = DATA / "tags/items"

    by_zone = {zone: [] for zone in ZONES}
    compounds = []
    junk = []
    for obj in data["objects"]:
        full = f"{MODID}:{obj['id']}"
        by_zone[obj["zone"]].append(full)
        if obj["kind"] == "compound":
            compounds.append(full)
        else:
            junk.append(full)

    for zone, values in by_zone.items():
        write_json(tag_dir / "zone" / f"{zone}.json", {"replace": False, "values": values})

    write_json(tag_dir / "compound.json", {"replace": False, "values": compounds})
    write_json(tag_dir / "junk.json", {"replace": False, "values": junk})
    write_json(
        tag_dir / "components.json",
        {"replace": False, "values": [f'{MODID}:{c["id"]}' for c in data["components"]]},
    )
    write_json(
        tag_dir / "resources.json",
        {"replace": False, "values": [f'{MODID}:{r["id"]}' for r in data["resources"]]},
    )
    write_json(
        tag_dir / "recyclable.json",
        {
            "replace": False,
            "values": [
                f'{MODID}:{o["id"]}' for o in data["objects"]
            ]
            + [f'{MODID}:{c["id"]}' for c in data["components"]],
        },
    )


def loot_condition(loot_table: str) -> dict:
    return {"condition": "forge:loot_table_id", "loot_table_id": loot_table}


def any_of(loot_tables) -> dict:
    return {
        "condition": "minecraft:any_of",
        "terms": [loot_condition(t) for t in loot_tables],
    }


def modifier(tag: str, chance: float, minimum: int, maximum: int, conditions) -> dict:
    return {
        "type": f"{MODID}:inject_tag_items",
        "conditions": conditions,
        "tag": f"{MODID}:{tag}",
        "chance": chance,
        "min": minimum,
        "max": maximum,
    }


ZOMBIE_TABLES = [
    "minecraft:entities/zombie",
    "minecraft:entities/husk",
    "minecraft:entities/drowned",
    "minecraft:entities/zombie_villager",
    "minecraft:entities/zombified_piglin",
]

# Loot tables reales del pack Chernobyl Z (ChernobylLauncher):
# - doomsday_functionality: cofres de props (restos, taquillas, cars, laboratorio...).
# - zombiekit: tablas de los airdrops (referenciadas por el codigo de dyairdrop).
# Zombis: The Hordes / LootStock generan loot por codigo; los zombis comunes
# siguen usando la tabla vanilla, asi que ZOMBIE_TABLES no cambia.
CHEST_TABLES = {
    "industrial": [
        "doomsday_functionality:chests/toolbox",
        "doomsday_functionality:chests/metaldrawer",
        "doomsday_functionality:chests/metalcabinet",
        "doomsday_functionality:chests/draw",
        "doomsday_functionality:chests/draw_2",
        "doomsday_functionality:chests/draw_3",
        "doomsday_functionality:chests/carton",
        "doomsday_functionality:chests/carton_2",
        "doomsday_functionality:chests/oildrum",
        "doomsday_functionality:chests/gastank",
        "doomsday_functionality:chests/generator",
        "doomsday_functionality:chests/fixedgenerator",
        "doomsday_functionality:chests/trailergenerator",
        "doomsday_functionality:chests/forklifttruck",
    ],
    "chemical": [
        "doomsday_functionality:chests/oildrum",
        "doomsday_functionality:chests/oiltank",
        "doomsday_functionality:chests/oiltank_2",
        "doomsday_functionality:chests/gastank",
        "doomsday_functionality:chests/gasstation",
        "doomsday_functionality:chests/chemicalprotectiveclothing",
        "doomsday_functionality:chests/chemicalprotectiveclothing_2",
        "doomsday_functionality:chests/drug",
        "doomsday_functionality:chests/insulationcabinet",
        "doomsday_functionality:chests/waterdispenser",
    ],
    "military": [
        "doomsday_functionality:chests/weaponbox",
        "doomsday_functionality:chests/weapon_rack",
        "doomsday_functionality:chests/weapon_rack_2",
        "doomsday_functionality:chests/weapon_rack_3",
        "doomsday_functionality:chests/ammunitionbox",
        "zombiekit:chests/weaponairdrop1",
        "zombiekit:chests/weaponairdrop2",
        "zombiekit:chests/weaponairdrop3",
        "zombiekit:chests/weaponairdrop4",
        "zombiekit:chests/weaponairdrop5",
        "zombiekit:chests/largeairdrop1",
        "zombiekit:chests/largeairdrop2",
        "zombiekit:chests/largeairdrop3",
        "zombiekit:chests/largeairdrop4",
        "zombiekit:chests/largeairdrop5",
    ],
    "hospital": [
        "doomsday_functionality:chests/firstaidkit",
        "doomsday_functionality:chests/medicalbox",
        "doomsday_functionality:chests/ambulance_1",
        "doomsday_functionality:chests/ambulance_2",
        "doomsday_functionality:chests/ambulance_3",
        "doomsday_functionality:chests/chemicalprotectiveclothing",
        "doomsday_functionality:chests/chemicalprotectiveclothing_2",
        "doomsday_functionality:chests/beaker",
        "doomsday_functionality:chests/glassware",
        "zombiekit:chests/medicalairdrop1",
        "zombiekit:chests/medicalairdrop2",
        "zombiekit:chests/medicalairdrop3",
        "zombiekit:chests/medicalairdrop4",
        "zombiekit:chests/medicalairdrop5",
    ],
    "residential": [
        "doomsday_functionality:chests/remains_1",
        "doomsday_functionality:chests/remains_2",
        "doomsday_functionality:chests/remains_3",
        "doomsday_functionality:chests/remains_4",
        "doomsday_functionality:chests/remains_5",
        "doomsday_functionality:chests/remains_6",
        "doomsday_functionality:chests/remains_7",
        "doomsday_functionality:chests/remains_8",
        "doomsday_functionality:chests/remains_9",
        "doomsday_functionality:chests/remains_10",
        "doomsday_functionality:chests/remains_11",
        "doomsday_functionality:chests/knapsack",
        "doomsday_functionality:chests/blueluggage",
        "doomsday_functionality:chests/blackluggage",
        "doomsday_functionality:chests/redluggage",
        "doomsday_functionality:chests/greyluggage",
        "doomsday_functionality:chests/trashbag",
        "doomsday_functionality:chests/trashbag_2",
        "doomsday_functionality:chests/trashbag_3",
    ],
    "electrical": [
        "doomsday_functionality:chests/atm",
        "doomsday_functionality:chests/atm_2",
        "doomsday_functionality:chests/cashregister",
        "doomsday_functionality:chests/printer",
        "doomsday_functionality:chests/microwave",
        "doomsday_functionality:chests/electricoven",
        "doomsday_functionality:chests/coffee_machine",
        "doomsday_functionality:chests/waterdispenser",
        "doomsday_functionality:chests/vendingmachine",
        "doomsday_functionality:chests/vendingmachine_2",
    ],
}


def generate_loot() -> None:
    entries = []

    for i, table in enumerate(ZOMBIE_TABLES):
        name = f"zombie_junk_{i}"
        write_json(
            DATA / "loot_modifiers" / f"{name}.json",
            modifier("junk", 0.35, 1, 2, [loot_condition(table)]),
        )
        entries.append(f"{MODID}:{name}")

        name = f"zombie_compound_{i}"
        write_json(
            DATA / "loot_modifiers" / f"{name}.json",
            modifier("compound", 0.04, 1, 1, [loot_condition(table)]),
        )
        entries.append(f"{MODID}:{name}")

    for zone, tables in CHEST_TABLES.items():
        name = f"chest_{zone}"
        write_json(
            DATA / "loot_modifiers" / f"{name}.json",
            modifier(f"zone/{zone}", 0.4, 1, 2, [any_of(tables)]),
        )
        entries.append(f"{MODID}:{name}")

    write_json(
        FORGE_DATA / "loot_modifiers/global_loot_modifiers.json",
        {"replace": False, "entries": entries},
    )


# --------------------------------------------------------------------------
# Texturas
# --------------------------------------------------------------------------

def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def canvas():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def bevel_box(d, x0, y0, x1, y1, base, strength=0.45):
    light = shade(base, 1 + strength)
    dark = shade(base, 1 - strength)
    d.rectangle([x0, y0, x1, y1], fill=dark)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=base)
    d.line([x0 + 1, y0 + 1, x1 - 1, y0 + 1], fill=light)
    d.line([x0 + 1, y0 + 1, x0 + 1, y1 - 1], fill=light)
    d.line([x0 + 1, y1 - 1, x1 - 1, y1 - 1], fill=dark)
    d.line([x1 - 1, y0 + 1, x1 - 1, y1 - 1], fill=dark)


def draw_bar(d, base):
    bevel_box(d, 3, 8, 12, 12, base)
    bevel_box(d, 5, 4, 13, 8, shade(base, 1.12))


def draw_cloth(d, base):
    bevel_box(d, 3, 5, 12, 12, base, 0.3)
    for y in (7, 9, 11):
        d.line([4, y, 11, y], fill=shade(base, 0.75))
    d.line([7, 5, 7, 11], fill=shade(base, 1.2))


def draw_scrap(d, base, rnd):
    for _ in range(4):
        x = rnd.randint(2, 9)
        y = rnd.randint(3, 10)
        w = rnd.randint(3, 5)
        h = rnd.randint(2, 4)
        bevel_box(d, x, y, x + w, y + h, base, 0.35)
    d.line([4, 12, 11, 12], fill=shade(base, 0.5))


def draw_gear(d, base, offset=0):
    light = shade(base, 1.35)
    dark = shade(base, 0.55)
    d.ellipse([3, 3, 12, 12], fill=dark)
    d.ellipse([4, 4, 11, 11], fill=base)
    d.ellipse([7, 7, 8, 8], fill=dark)
    for x, y in ((6, 1), (6, 12), (1, 6), (12, 6)):
        d.rectangle([x, y, x + 2, y + 2], fill=base)
        d.point((x, y), fill=light)
    d.arc([4, 4, 11, 11], 200, 260, fill=light)


def draw_pipe(d, base):
    bevel_box(d, 2, 6, 13, 9, base, 0.4)
    bevel_box(d, 2, 4, 4, 11, shade(base, 0.85))
    bevel_box(d, 11, 4, 13, 11, shade(base, 0.85))
    d.line([5, 8, 10, 8], fill=shade(base, 1.3))


def draw_coil(d, base):
    for r in (2, 4, 6):
        d.ellipse([7 - r, 7 - r, 8 + r, 8 + r], outline=shade(base, 1.25 if r % 2 else 0.7), width=1)
    d.ellipse([7, 7, 8, 8], fill=shade(base, 1.4))


def draw_board(d, base, rnd):
    bevel_box(d, 2, 3, 13, 12, base, 0.25)
    for _ in range(5):
        x = rnd.randint(4, 9)
        y = rnd.randint(5, 9)
        d.rectangle([x, y, x + 1, y + 1], fill=shade(base, 0.55))
    d.line([3, 10, 12, 10], fill=shade(base, 0.6))
    d.line([3, 11, 12, 11], fill=shade(base, 0.6))


def draw_cell(d, base):
    bevel_box(d, 5, 2, 10, 13, base, 0.35)
    d.rectangle([6, 3, 9, 5], fill=shade(base, 1.5))
    d.rectangle([6, 10, 9, 12], fill=shade(base, 0.5))


def draw_lens(d, base):
    d.ellipse([2, 2, 13, 13], fill=shade(base, 0.55))
    d.ellipse([3, 3, 12, 12], fill=shade(base, 1.15))
    d.ellipse([5, 5, 10, 10], fill=shade(base, 1.4))
    d.point((6, 6), fill=(255, 255, 255, 220))


def draw_filter(d, base):
    bevel_box(d, 3, 2, 12, 13, base, 0.3)
    for x in range(4, 12, 2):
        d.line([x, 4, x, 11], fill=shade(base, 0.55))


def draw_flask(d, base):
    d.rectangle([6, 2, 9, 5], fill=shade(base, 1.15))
    d.polygon([(5, 6), (10, 6), (13, 13), (2, 13)], fill=shade(base, 0.95))
    d.polygon([(5, 7), (10, 7), (12, 12), (3, 12)], fill=shade(base, 1.15))
    d.rectangle([5, 10, 11, 12], fill=shade(base, 0.75))


def draw_compound(d, base, rnd, variant):
    if variant % 3 == 0:
        # Caja reforzada
        bevel_box(d, 2, 4, 13, 12, base, 0.35)
        d.rectangle([4, 6, 11, 7], fill=shade(base, 0.5))
        d.rectangle([4, 9, 8, 10], fill=shade(base, 1.3))
        d.point((12, 5), fill=shade(base, 1.5))
    elif variant % 3 == 1:
        # Bloque de maquina con rejillas
        bevel_box(d, 3, 2, 12, 13, base, 0.4)
        d.rectangle([5, 4, 10, 7], fill=shade(base, 0.45))
        for y in (9, 11):
            d.line([5, y, 10, y], fill=shade(base, 1.2))
        d.line([8, 2, 8, 13], fill=shade(base, 0.6))
    else:
        # Bidon con asa y banda
        bevel_box(d, 4, 3, 11, 13, base, 0.35)
        d.rectangle([6, 1, 9, 3], fill=shade(base, 1.2))
        d.rectangle([5, 8, 10, 9], fill=shade(base, 0.5))
        d.point((7, 6), fill=shade(base, 1.4))
    for _ in range(2):
        d.point((rnd.randint(3, 12), rnd.randint(3, 12)), fill=shade(base, 0.4))


def draw_junk(d, base, rnd, variant):
    if variant % 3 == 0:
        # Chatarra irregular
        pts = [(3, 6), (5, 3), (9, 4), (12, 7), (11, 12), (6, 13), (3, 10)]
        d.polygon(pts, fill=shade(base, 0.9))
        d.line(pts + [pts[0]], fill=shade(base, 0.5))
        d.line([5, 8, 10, 8], fill=shade(base, 1.25))
    elif variant % 3 == 1:
        # Chapa doblada
        pts = [(2, 4), (12, 3), (13, 10), (9, 12), (3, 11)]
        d.polygon(pts, fill=shade(base, 0.95))
        d.line(pts + [pts[0]], fill=shade(base, 0.5))
        d.line([4, 7, 9, 6], fill=shade(base, 1.25))
        d.line([6, 9, 11, 8], fill=shade(base, 0.65))
    else:
        # Lata aplastada
        bevel_box(d, 4, 4, 11, 13, base, 0.35)
        d.ellipse([4, 2, 11, 6], fill=shade(base, 1.15))
        d.ellipse([5, 3, 10, 5], fill=shade(base, 0.7))
        d.line([4, 9, 11, 9], fill=shade(base, 0.55))
    for _ in range(2):
        d.point((rnd.randint(3, 12), rnd.randint(4, 12)), fill=shade(base, 0.4))


def make_item_texture(path: Path, item, force: bool) -> None:
    if path.exists() and not force:
        return

    # Si hay un diseno definitivo (tools/textures.py o tools/objects.py), usarlo.
    try:
        from textures import DESIGNS as BASE_DESIGNS
        from objects import DESIGNS as OBJECT_DESIGNS
    except ImportError:
        BASE_DESIGNS, OBJECT_DESIGNS = {}, {}

    render = BASE_DESIGNS.get(item["id"]) or OBJECT_DESIGNS.get(item["id"])
    if render is not None:
        img = render()
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path)
        return

    rnd = random.Random(item["id"])
    if item["kind"] == "resource":
        base = RESOURCE_COLOR.get(item["id"], (160, 160, 160))
    elif item["kind"] == "component":
        base = mix(COMPONENT_COLOR, COMPONENT_TINTS[rnd.randrange(len(COMPONENT_TINTS))], 0.35)
    elif item["kind"] == "compound":
        base = ZONE_COLOR[item["zone"]]
    else:
        base = mix(ZONE_COLOR[item["zone"]], (90, 90, 90), 0.35)

    # Variacion de brillo por item: los placeholders de una misma zona no se ven iguales.
    base = shade(base, 0.82 + rnd.random() * 0.36)

    img, d = canvas()
    variant = rnd.randrange(6)

    if item["id"] == "tela":
        draw_cloth(d, base)
    elif item["id"] == "scrap":
        draw_scrap(d, base, rnd)
    elif item["id"] == "lingote_pesado":
        draw_bar(d, base)
    elif item["kind"] == "component":
        draw = [draw_gear, draw_pipe, draw_coil, draw_board, draw_cell, draw_lens][variant]
        if draw in (draw_board,):
            draw(d, base, rnd)
        else:
            draw(d, base)
        if item["id"] in ("filtro_carbon_activado",):
            draw_filter(d, base)
        elif item["id"] in ("nucleo_plomo_sellado",):
            bevel_box(d, 4, 4, 11, 11, base, 0.3)
            d.rectangle([6, 6, 9, 9], fill=shade(base, 0.45))
    elif item["kind"] == "compound":
        draw_compound(d, base, rnd, variant)
    else:
        if item["zone"] == "chemical" and variant % 3 == 0:
            draw_flask(d, base)
        else:
            draw_junk(d, base, rnd, variant)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def make_block_textures() -> None:
    def panel(base, rnd, front=False):
        img = Image.new("RGBA", (16, 16), base)
        d = ImageDraw.Draw(img)
        light = shade(base, 1.25)
        dark = shade(base, 0.55)
        mid = shade(base, 0.8)
        d.rectangle([0, 0, 15, 15], outline=dark)
        d.line([1, 1, 14, 1], fill=light)
        d.line([1, 1, 1, 14], fill=light)
        # remaches
        for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)):
            d.rectangle([x, y, x + 1, y + 1], fill=dark)
            d.point((x, y), fill=light)
        # paneles y oxido
        d.line([1, 8, 14, 8], fill=mid)
        for _ in range(10):
            x = rnd.randint(2, 13)
            y = rnd.randint(2, 13)
            if rnd.random() < 0.5:
                d.point((x, y), fill=(120, 74, 40, 255))
        if front:
            d.rectangle([4, 4, 11, 7], fill=(28, 34, 30))
            d.rectangle([5, 5, 10, 6], fill=(90, 200, 110))
            d.rectangle([4, 9, 11, 12], fill=(40, 40, 40))
            for x in range(5, 11, 2):
                d.line([x, 9, x, 12], fill=(70, 70, 70))
        return img

    rnd = random.Random(1234)
    tex = ASSETS / "textures/block"
    tex.mkdir(parents=True, exist_ok=True)
    panel((86, 92, 98), rnd).save(tex / "recycler_side.png")
    panel((96, 90, 82), rnd).save(tex / "recycler_top.png")
    panel((80, 88, 96), rnd, front=True).save(tex / "recycler_front.png")


def slot(d, x, y):
    dark = (55, 55, 55)
    mid = (139, 139, 139)
    light = (255, 255, 255)
    d.rectangle([x, y, x + 17, y + 17], fill=dark)
    d.rectangle([x + 1, y + 1, x + 16, y + 16], fill=mid)
    d.line([x + 1, y + 1, x + 16, y + 1], fill=dark)
    d.line([x + 1, y + 1, x + 1, y + 16], fill=dark)
    d.line([x + 1, y + 16, x + 16, y + 16], fill=light)
    d.line([x + 16, y + 1, x + 16, y + 16], fill=light)


def make_gui_texture() -> None:
    img = Image.new("RGBA", (176, 166), (198, 198, 198, 255))
    d = ImageDraw.Draw(img)

    # Marco con bisel vanila
    d.rectangle([0, 0, 175, 165], fill=(198, 198, 198))
    d.line([0, 0, 175, 0], fill=(255, 255, 255))
    d.line([0, 0, 0, 165], fill=(255, 255, 255))
    d.line([0, 165, 175, 165], fill=(85, 85, 85))
    d.line([175, 0, 175, 165], fill=(85, 85, 85))
    d.rectangle([1, 1, 174, 164], outline=(139, 139, 139))
    d.rectangle([2, 2, 173, 163], outline=(198, 198, 198))

    # Franja superior con rayas de peligro
    for x in range(3, 174, 8):
        d.polygon([(x, 3), (x + 4, 3), (x, 12), (x - 4, 12)], fill=(160, 142, 64))
    d.rectangle([2, 2, 173, 14], outline=(139, 139, 139))

    # Remaches
    for x, y in ((4, 4), (171, 4), (4, 161), (171, 161)):
        d.rectangle([x, y, x + 1, y + 1], fill=(85, 85, 85))
        d.point((x, y), fill=(255, 255, 255))

    # Slot de entrada y parrilla de salida
    slot(d, 25, 34)
    for row in range(3):
        for col in range(3):
            slot(d, 97 + col * 18, 16 + row * 18)

    # Barra de progreso
    d.rectangle([55, 36, 81, 54], fill=(55, 55, 55))
    d.rectangle([56, 37, 80, 53], fill=(35, 35, 35))
    d.line([56, 37, 80, 37], fill=(85, 85, 85))
    d.line([56, 37, 56, 53], fill=(85, 85, 85))

    # Inventario del jugador
    for row in range(3):
        for col in range(9):
            slot(d, 7 + col * 18, 83 + row * 18)
    for col in range(9):
        slot(d, 7 + col * 18, 141)

    # Placa del titulo: cubre la franja de peligro para que el texto no se corte
    d.rectangle([7, 4, 72, 14], fill=(198, 198, 198))
    d.line([7, 14, 72, 14], fill=(139, 139, 139))

    out = ASSETS / "textures/gui/recycler.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


# --------------------------------------------------------------------------
# Block assets + receta de crafteo
# --------------------------------------------------------------------------

def generate_block_assets() -> None:
    write_json(
        ASSETS / "blockstates/recycler.json",
        {"variants": {"": {"model": f"{MODID}:block/recycler"}}},
    )
    write_json(
        ASSETS / "models/block/recycler.json",
        {
            "parent": "minecraft:block/cube",
            "textures": {
                "particle": f"{MODID}:block/recycler_side",
                "down": f"{MODID}:block/recycler_top",
                "up": f"{MODID}:block/recycler_top",
                "north": f"{MODID}:block/recycler_front",
                "south": f"{MODID}:block/recycler_side",
                "east": f"{MODID}:block/recycler_side",
                "west": f"{MODID}:block/recycler_side",
            },
        },
    )
    write_json(
        ASSETS / "models/item/recycler.json",
        {"parent": f"{MODID}:block/recycler"},
    )

    write_json(
        DATA / "recipes/recycler.json",
        {
            "type": "minecraft:crafting_shaped",
            "pattern": ["III", "IBI", "IRI"],
            "key": {
                "I": {"item": "minecraft:iron_ingot"},
                "B": {"item": "minecraft:blast_furnace"},
                "R": {"item": "minecraft:redstone_block"},
            },
            "result": {"item": f"{MODID}:recycler"},
        },
    )

    write_json(
        DATA / "loot_tables/blocks/recycler.json",
        {
            "type": "minecraft:block",
            "pools": [
                {
                    "rolls": 1,
                    "entries": [{"type": "minecraft:item", "name": f"{MODID}:recycler"}],
                    "conditions": [{"condition": "minecraft:survives_explosion"}],
                }
            ],
        },
    )

    write_json(
        RES / "data/minecraft/tags/blocks/mineable/pickaxe.json",
        {"replace": False, "values": [f"{MODID}:recycler"]},
    )
    write_json(
        RES / "data/minecraft/tags/blocks/needs_stone_tool.json",
        {"replace": False, "values": [f"{MODID}:recycler"]},
    )


# --------------------------------------------------------------------------
# Docs
# --------------------------------------------------------------------------

def generate_docs(data) -> None:
    lines = [
        "# Listado de objetos y recetas",
        "",
        "Generado por `tools/generate.py` a partir de `tools/items.json`.",
        "",
        "## Recursos base",
        "",
        "| Item | Nombre (ES) | Nombre (EN) |",
        "| :--- | :--- | :--- |",
    ]
    for res in data["resources"]:
        lines.append(f"| `{MODID}:{res['id']}` | {res['es']} | {res['en']} |")

    lines += ["", "## Componentes (Fase 2)", "", "| Item | Nombre (ES) | Al reciclar | Uso |", "| :--- | :--- | :--- | :--- |"]
    for comp in data["components"]:
        recycle = ", ".join(f"{c}x {i}" for i, c in comp["recycle"])
        lines.append(f"| `{MODID}:{comp['id']}` | {comp['es']} | {recycle} | {comp.get('use_es', '')} |")

    for zone in ZONES:
        objs = [o for o in data["objects"] if o["zone"] == zone]
        lines += ["", f"## {ZONE_ES[zone]}", "", "| Objeto | Fase 1 | Componentes | Tiempo (ticks) |", "| :--- | :--- | :--- | :--- |"]
        for obj in objs:
            base = ", ".join(f"{c}x {i}" for i, c in obj["base"])
            comps = ", ".join(f"{c}x {i}" for i, c in obj.get("components", [])) or "-"
            lines.append(
                f"| `{MODID}:{obj['id']}` ({obj['kind']}) | {base} | {comps} | {processing_time(obj['kind'], obj['tier'])} |"
            )

    lines += [
        "",
        "## Texturas",
        "",
        "Las 97 texturas estan en `src/main/resources/assets/chernobylz_recycler/textures/item/`.",
        "Se generan con `tools/textures.py` (recursos y componentes) y `tools/objects.py`",
        "(objetos por zona). Reemplaza cada PNG por tu arte de Blockbench manteniendo el mismo",
        "nombre; `tools/generate.py` no sobreescribe texturas existentes.",
        "",
    ]
    (DOCS).mkdir(parents=True, exist_ok=True)
    (DOCS / "ITEMS.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------

def main() -> None:
    data = load_data()
    items = all_items(data)

    generate_java(items)
    generate_item_models(items)
    generate_lang(items)
    generate_recipes(data)
    generate_tags(data)
    generate_loot()
    generate_block_assets()

    for item in items:
        make_item_texture(ASSETS / "textures/item" / f'{item["id"]}.png', item, FORCE_TEXTURES)
    make_block_textures()
    make_gui_texture()

    generate_docs(data)
    print(f"OK: {len(items)} items, {len(data['objects'])} objetos, {len(data['components'])} componentes.")


if __name__ == "__main__":
    main()
