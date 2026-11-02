# Chernobyl Z: Reciclaje

Mod de **Forge 1.20.1** que implementa el sistema de reciclaje del GDD de Chernobyl Z:
una recicladora colocable, tres recursos base, dieciséis componentes útiles y setenta y ocho
objetos repartidos en seis zonas de riesgo.

El objetivo es el de Rust: convertir basura en materiales, pero obligando a elegir entre
**reciclar** un componente o **guardarlo para craftear**.

---

## Requisitos

| Elemento | Versión |
| :--- | :--- |
| Minecraft | 1.20.1 |
| Forge | 47.4.x (probado con 47.4.28) |
| Java | 17 |

El mod debe instalarse en **cliente y servidor**.

## Instalación

1. Compila el proyecto o usa el jar ya generado: `build/libs/chernobylz_recycler-1.0.0.jar`.
2. Copia el jar en la carpeta `mods/` del servidor y de los clientes.
3. Arranca el servidor una vez. Se creará `config/chernobylz_recycler-common.toml`.

## Contenido

- **Recicladora**: bloque con GUI de 1 slot de entrada y 3x3 de salida.
- **3 recursos base**: Tela, Scrap y Lingote Pesado.
- **16 componentes útiles**: engranajes, hidráulica, electrónica, filtros, kevlar plomado, etc.
- **78 objetos reciclables** repartidos en Industrial, Química, Militar, Hospital, Residencial y
  Eléctrica (26 de cada tier, 13-14 por zona).
- **94 recetas** de reciclaje data-driven (78 de Fase 1 + 16 de Fase 2).
- **Loot integrado**: basura en zombis y objetos por zona en cofres mediante loot modifiers.
- **Tooltips dinámicos**: al pasar el ratón por un objeto se muestran los rendimientos reales
  leídos de las recetas sincronizadas, no texto fijo.

El listado completo con nombres, rendimientos y tiempos está en [`docs/ITEMS.md`](docs/ITEMS.md).

## Cómo se consigue

### Crafteo

```
L L L
L A L
L R L
```

`L` = lingote de hierro, `A` = alto horno, `R` = bloque de redstone.

### Comando de administración

```
/czrecycler loot <jugadores> <zona> [cantidad]
/czrecycler zones
```

Requiere nivel de permiso 2 (operador). `cantidad` va de 1 a 64 por jugador.
Las zonas válidas son `industrial`, `chemical`, `military`, `hospital`, `residential` y
`electrical`.

## Uso

1. Coloca la recicladora y haz clic derecho para abrirla.
2. Pon **un** objeto en el slot de entrada.
3. La barra central muestra el progreso. Al terminar, los recursos van a la parrilla 3x3.
4. Saca el resultado. Si la salida está llena, el objeto no se procesa (no se pierde nada).

### Fase 1: objeto → recursos + componentes

Los objetos simples entregan recursos base. Los objetos compuestos entregan recursos base
**y** componentes útiles. Los objetos de tier alto tardan más y rinden más.

| Tipo | Tiempo base | Multiplicador por tier |
| :--- | :--- | :--- |
| Simple | 70 ticks | x1.0 / x1.4 / x2.0 |
| Compuesto | 120 ticks | x1.0 / x1.4 / x2.0 |

### Fase 2: componente → recursos base

Los 16 componentes también se pueden reciclar (80 ticks) para recuperar parte de su valor en
Tela, Scrap o Lingote Pesado. Es la decisión de costo de oportunidad del sistema: ese
engranaje de titanio puede volver a ser metal… o convertirse en una torreta.

La Fase 2 se puede desactivar en la configuración del servidor.

### Automatización

Las tolvas solo pueden **insertar en el slot de entrada** y **extraer de la parrilla de salida**.
No se puede vaciar la entrada por debajo ni empujar objetos a la salida.

## Configuración

Archivo: `config/chernobylz_recycler-common.toml`

| Clave | Por defecto | Descripción |
| :--- | :--- | :--- |
| `allowPhaseTwo` | `true` | Permite reciclar componentes útiles. |
| `processingSpeedMultiplier` | `1.0` | Velocidad global; `2.0` tarda la mitad. |
| `enableLootModifiers` | `true` | Activa la inyección de basura/objetos en el loot. |

## Datos y balance

Todo el contenido sale de `items.json` y de los generadores:

- `tools/items.json`: recursos, componentes, objetos, zonas, tiers, rendimientos y usos.
- `tools/generate.py`: genera items Java, modelos, lang, recetas, tags, loot, texturas
  y `docs/ITEMS.md`.
- `tools/textures.py`: diseños de los 3 recursos y 16 componentes.
- `tools/objects.py`: diseños de los 78 objetos, agrupados por zona.

Para cambiar el balance, edita `items.json` y ejecuta:

```bash
python tools/generate.py
```

Esto **no sobrescribe** las texturas existentes. Para regenerar también las 97 texturas con
los diseños de `tools/textures.py` y `tools/objects.py`:

```bash
python tools/generate.py --force-textures
```

### Formato de una receta

`src/main/resources/data/chernobylz_recycler/recipes/recycling/<item>.json`

```json
{
  "type": "chernobylz_recycler:recycling",
  "phase": 1,
  "processing_time": 120,
  "ingredient": { "item": "chernobylz_recycler:abrigo_afghanka" },
  "base": [
    { "item": "chernobylz_recycler:tela", "count": 18 },
    { "item": "chernobylz_recycler:scrap", "count": 2 }
  ],
  "components": [
    { "item": "chernobylz_recycler:tejido_kevlar_plomado", "count": 1 }
  ]
}
```

- `phase`: `1` para objetos, `2` para componentes.
- `processing_time`: ticks a velocidad x1.
- `base` / `components`: listas de `{item, count}`. Una receta puede no tener componentes.

## Loot

El mod inyecta objetos en loot tables existentes con un loot modifier global propio
(`chernobylz_recycler:inject_tag_items`). Por defecto:

- Zombis, husks, ahogados, aldeanos zombi y piglins zombificados: 35% de 1-2 objetos de
  basura y 4% de 1 objeto compuesto.
- Cofres de ejemplo por zona: 40% de 1-2 objetos de la zona.

Los IDs de cofres son de ejemplo (vanilla). Para el mapa de Chernobyl Z hay que apuntarlos a
las loot tables reales. Instrucciones en [`docs/LOOT.md`](docs/LOOT.md).

## Compilar

```bash
./gradlew build
```

El jar queda en `build/libs/`. Para probar en desarrollo:

```bash
./gradlew runClient
./gradlew runServer
```

## Estructura

```
src/main/java/com/chernobylz/recycler/
  block/        Recicladora y block entity (tick, inventario, tolvas)
  client/       GUI, tooltips dinámicos y registro de pantallas
  command/      /czrecycler
  item/         Item base con tooltips
  loot/         Loot modifier inject_tag_items
  menu/         Menú y slots
  recipe/       Receta de reciclaje y serializer
  registry/     Items, bloques, block entities, menús, recetas, tabs
  util/         Zonas de riesgo
src/main/resources/
  assets/       Modelos, lang, texturas
  data/         Recetas, tags, loot modifiers, loot tables
tools/          Generador y utilidades de previsualización
docs/           Documentación y previews
```

## Documentación

- [`docs/ITEMS.md`](docs/ITEMS.md): catálogo completo y rendimientos.
- [`docs/TEXTURAS.md`](docs/TEXTURAS.md): cómo reemplazar las texturas en Blockbench.
- [`docs/DISENO_3D.md`](docs/DISENO_3D.md): sistema de diseño del arte 3D de items
  (paleta, reglas de forma, presupuesto por tier, pipeline) — specs en
  `tools/models3d/specs/` y previews calibradas en `docs/models3d/`.
- [`docs/LOOT.md`](docs/LOOT.md): cómo conectar el loot a las loot tables del servidor.
- `docs/preview_items.png`, `docs/preview_gui.png`, `docs/preview_block.png`: previews generadas.

## Notas

- Las 97 texturas de item están generadas por código con un estilo común. Están pensadas para
  ser reemplazadas por arte propio sin tocar Java ni JSON.
- El proyecto no incluye un repositorio git; los cambios viven en disco.
- `LICENSE.txt` y `CREDITS.txt` pertenecen al MDK de Forge.
