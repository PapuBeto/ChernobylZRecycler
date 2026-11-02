# Loot: cómo conectarlo al servidor

El mod no reemplaza las loot tables del servidor: **inyecta objetos** en las tablas que ya
existen mediante un loot modifier global de Forge. Así se puede activar el reciclaje sin tocar
los cofres, zombis o estructuras de Chernobyl Z.

## Cómo funciona

```
data/
  chernobylz_recycler/
    loot_modifiers/          <- definición de cada inyección
      zombie_junk_0.json
      zombie_compound_0.json
      chest_industrial.json
      ...
    tags/items/
      junk.json              <- qué objetos puede soltar un zombi
      compound.json          <- objetos compuestos raros
      zone/industrial.json   <- objetos de la zona industrial
      zone/chemical.json
      zone/military.json
      zone/hospital.json
      zone/residential.json
      zone/electrical.json
  forge/
    loot_modifiers/
      global_loot_modifiers.json   <- lista de modifiers activos
```

Un modifier tiene esta forma:

```json
{
  "type": "chernobylz_recycler:inject_tag_items",
  "conditions": [
    {
      "condition": "forge:loot_table_id",
      "loot_table_id": "minecraft:entities/zombie"
    }
  ],
  "tag": "chernobylz_recycler:junk",
  "chance": 0.35,
  "min": 1,
  "max": 2
}
```

| Campo | Descripción |
| :--- | :--- |
| `type` | Siempre `chernobylz_recycler:inject_tag_items`. |
| `conditions` | Condiciones de Forge. Todas deben cumplirse (AND). |
| `tag` | Tag de items del que se elige al azar. |
| `chance` | Probabilidad por tirada, de `0.0` a `1.0`. |
| `min` / `max` | Cantidad de objetos añadidos, ambos inclusive. |

Si `chance` falla, no se añade nada. Si el tag está vacío, tampoco (y no se rompe nada).

## Lo que se genera por defecto

Los cofres ya apuntan a las **loot tables reales del pack Chernobyl Z**
(`ChernobylLauncher\modpacks\completa`), no a tablas vanilla:

| Modifier | Tablas | Tag | Prob | Cant |
| :--- | :--- | :--- | :--- | :--- |
| `zombie_junk_0..4` | zombi, husk, ahogado, aldeano zombi, piglin zombificado | `junk` | 35% | 1-2 |
| `zombie_compound_0..4` | las mismas | `compound` | 4% | 1 |
| `chest_industrial` | taquillas/alcachas de taller, maletines, barriles, tanques, generadores | `zone/industrial` | 40% | 1-2 |
| `chest_chemical` | barriles, depositos, gasolinera, equipo quimico/laboratorio | `zone/chemical` | 40% | 1-2 |
| `chest_military` | racks de armas, caja de municion + airdrops `zombiekit:` (weapon/large) | `zone/military` | 40% | 1-2 |
| `chest_hospital` | botiquines, ambulancias, material de laboratorio + airdrops medicos | `zone/hospital` | 40% | 1-2 |
| `chest_residential` | restos humanos (`remains_*`), mochilas, maletas, bolsas de basura | `zone/residential` | 40% | 1-2 |
| `chest_electrical` | ATMs, registradoras, impresoras, microondas, vending | `zone/electrical` | 40% | 1-2 |

Los IDs completos estan en `tools/generate.py` (`CHEST_TABLES`), que es la fuente:
si se cambian ahi, regenera los JSON con `python tools/generate.py`.

### Como se genera el loot en el pack (contexto)

- **`doomsday_functionality`** (con `doomsday_decoration`): casi todos los props que
  contienen loot (coches, taquillas, remains, vending, laboratorio...) se llenan con
  `data/doomsday_functionality/loot_tables/chests/*.json`. Es la fuente principal.
- **`dyairdrop` / `zombiekit`**: los 20 airdrops (small/large/weapon/medical 1..5).
  El codigo de dyairdrop llama a las tablas del namespace `zombiekit:`, no `dyairdrop:`.
- **LootStock** (cajas crate/locker/metal_chest/military_box/ammo_box/dufflebag/suitcase):
  genera loot **por codigo** con la config de la instancia `config/lootstock.toml`
  (campos `item1..5` y `itemNtag`). No tiene loot tables, asi que no se puede inyectar
  con modifiers; para meter objetos reciclables alli, edita ese TOML con
  `item1tag = "chernobylz_recycler:junk"` (integracion opcional, fuera del mod).
- **Zombis de The Hordes / zombies_plus**: tambien loot por codigo; los zombis comunes
  siguen tirando `minecraft:entities/zombie`, que es donde apuntan los modifiers
  `zombie_*`. Enemy units PMC/RU/US de `simpleenemymod` no exponen tabla de entidad.
- **`sa_decor` (Survivor's Arsenal)**: sus cofres existen en tu carpeta de desarrollo
  (`forge-1.20.1-47.4.28-mdk/libs`) pero NO estan en el pack `completa`, asi que no se
  apunta a sus tablas. Si un dia se añaden, sus ids van bajo `sa_decor:loot_tables/blocks/`.

## Apuntar a las loot tables reales de Chernobyl Z

Hay dos formas.

### Opción A: editar `tools/generate.py` y regenerar (recomendado)

En `generate.py`:

```python
ZOMBIE_TABLES = [
    "minecraft:entities/zombie",
    ...
]

CHEST_TABLES = {
    "industrial": [
        "minecraft:chests/abandoned_mineshaft",
        ...
    ],
    ...
}
```

Cambia los IDs por los del datapack de Chernobyl Z, por ejemplo:

```python
CHEST_TABLES = {
    "industrial": [
        "chernobylz:chests/factory_office",
        "chernobylz:chests/industrial_yard",
    ],
    ...
}
```

Después:

```bash
python tools/generate.py
```

Esto reescribe los JSON de `loot_modifiers/` y `global_loot_modifiers.json` sin tocar recetas
ni texturas.

### Opción B: editar los JSON a mano

En cada archivo de `data/chernobylz_recycler/loot_modifiers/`, cambia el valor de
`loot_table_id`. Para varias tablas, usa `minecraft:any_of`:

```json
{
  "type": "chernobylz_recycler:inject_tag_items",
  "conditions": [
    {
      "condition": "minecraft:any_of",
      "terms": [
        { "condition": "forge:loot_table_id", "loot_table_id": "chernobylz:chests/factory_office" },
        { "condition": "forge:loot_table_id", "loot_table_id": "chernobylz:chests/industrial_yard" }
      ]
    }
  ],
  "tag": "chernobylz_recycler:zone/industrial",
  "chance": 0.4,
  "min": 1,
  "max": 2
}
```

La condición `forge:loot_table_id` compara con la tabla que se está tirando en ese momento.
No sirve para tablas anidadas: si un cofre usa una tabla puente que a su vez llama a otra, hay
que apuntar a la que realmente se ejecuta.

## Activar o desactivar

- Todos los modifiers deben estar listados en
  `data/forge/loot_modifiers/global_loot_modifiers.json`. Si añades un archivo nuevo y no lo
  listas, no se aplica.
- `"replace": false` conserva los modifiers de otros mods. No lo cambies a `true` salvo que
  quieras borrar los ajenos.
- Para desactivar todo sin tocar datos: `enableLootModifiers = false` en
  `config/chernobylz_recycler-common.toml`.
- Para desactivar solo una tabla: pon `"chance": 0.0` en su modifier o quita su entrada de
  `global_loot_modifiers.json`.

## Añadir un modifier nuevo

1. Crea el tag (o reutiliza uno):

   `data/chernobylz_recycler/tags/items/zone/military.json`

   ```json
   {
     "replace": false,
     "values": [
       "chernobylz_recycler:casco_ssh68",
       "chernobylz_recycler:chaleco_balistico_6b3"
     ]
   }
   ```

2. Crea `data/chernobylz_recycler/loot_modifiers/chest_bunker.json`:

   ```json
   {
     "type": "chernobylz_recycler:inject_tag_items",
     "conditions": [
       { "condition": "forge:loot_table_id", "loot_table_id": "chernobylz:chests/bunker" }
     ],
     "tag": "chernobylz_recycler:zone/military",
     "chance": 0.5,
     "min": 1,
     "max": 3
   }
   ```

3. Añade `"chernobylz_recycler:chest_bunker"` a `global_loot_modifiers.json`.
4. `/reload` en el servidor.

## Probar

```
/reload
/loot spawn ~ ~ ~ loot minecraft:entities/zombie
/loot spawn ~ ~ ~ loot doomsday_functionality:chests/toolbox
```

Los objetos aparecen en el suelo. Repite varias veces: las probabilidades son bajas a
propósito. También puedes matar zombis en creativo o abrir cofres con una palanca.

Para ver qué objeto salió:

```
/data get entity @e[type=item,limit=1,sort=nearest]
```

## Problemas comunes

| Síntoma | Causa probable |
| :--- | :--- |
| No cae nada nunca | El modifier no está en `global_loot_modifiers.json`, o el `loot_table_id` no coincide. |
| Error al cargar el datapack | JSON inválido, tag inexistente o `chance` fuera de `0..1`. |
| Cae el objeto equivocado | El tag de la zona tiene items que no esperabas; revisa `tags/items/zone/*.json`. |
| Funciona en cofres pero no en zombis | La tabla del zombi custom no es `minecraft:entities/zombie`; apunta a la real. |
| Cae en todos los cofres | La condición está mal escrita o se usa `minecraft:any_of` con una tabla comodín. |

Los errores de carga aparecen en `logs/latest.log` con `Failed to parse global loot modifier`
o `Couldn't parse loot table`.
