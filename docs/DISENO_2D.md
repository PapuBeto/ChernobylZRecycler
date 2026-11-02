# Dirección de arte 2D — ChernobylZ Recycler

Fecha de cierre: 2026-10-26.

## Resumen

Toda la colección de items (97) se ha rediseñado como **pixel art auténtico
dibujado directamente en la cuadrícula 32×32**. Ninguna textura proviene ya
de renderizados 3D ni de imágenes escaladas: cada sprite está construido
píxel a píxel por el motor propio `tools/pixelart/` y compilado al jar.

## Reglas del estilo (obligatorias para futuros sprites)

- **Resolución única 32×32** para toda la colección.
- **Luz global top-left**: la cara superior e izquierda siempre más clara;
  nunca mezclar direcciones de sombreado entre sprites.
- **Paleta compartida**: las 13 rampas desaturadas de `tools/pixelart/pal.py`
  (STEEL, HIERRO, OLIVA, MADERA, OXIDO, BEIGE, CARBON, LATON, AMARILLO,
  CRISTAL, CAUCHO, SULFATO, ROJO). No introducir colores por fuera.
- **Transiciones por escalones** de tono con dither en dama, nunca por
  degradado continuo; bordes duros, sin antialiasing ni blur.
- **Ruido cero**: el óxido, la suciedad y el daño se colocan a mano y con
  función visual (borde de uso, goteo, mancha localizada).
- Item individual en inventario: fondo transparente, sin marcos, textos,
  escenarios ni sombras externas.

## Pipeline

1. **Diseño**: cada sprite es una función en un módulo temático
   (`pilotos.py`, `componentes.py`, `industrial.py`, `militar.py`,
   `medico.py`, `hogar.py`, `electrico.py`, `construccion.py`) que usa las
   primitivas de `px.py` (clase `P`) y las formas reutilizables de
   `formas.py`. Todo se registra en el dict `DIBUJOS` del módulo.
2. **Render maestro**: `python -m tools.pixelart.render --hoja id1,id2,...`
   escribe PNG nativos 32×32 en `docs/pixelart/` y una hoja de contacto
   (`hoja_contacto.png`, ×6 NEAREST sobre fondo gris 58,61,64) para control
   de calidad por lotes.
3. **Publicación al juego**: `--todos --juego` escribe las 97 texturas en
   `src/main/resources/assets/chernobylz_recycler/textures/item/`.
4. **Compilación**: `.\gradlew.bat build` reempaqueta
   `build/libs/chernobylz_recycler-1.0.0.jar` (recuerda copiar el jar al
   mods de tu instalación si pruebas fuera del runClient).

Los 5 sprites piloto (motor de grúa, Geiger Pripyat-M, máscara GP-5,
batería T-72, televisor Rubin) fueron la hoja de estilo aprobada y todo el
resto de la colección se diseñó sobre esas mismas convenciones.

## Deprecación de `tools/sprites2d/`

La carpeta `tools/sprites2d/` queda **deprecada**: era el pipeline anterior
(borrosos/redimensionados) y ya no alimenta ninguna textura del juego. Se
conserva únicamente como referencia histórica, incluido el respaldo de los
4 modelos 3D que fueron convertidos (en `tools/sprites2d/backup_models3d/`).

## Modelos de item

Los 4 JSON que aún eran modelos cúbicos 3D
(`bateria_tanque_t72`, `contador_geiger_pripyat`, `radio_campana_r159`,
`traje_hazmat_liquidador`) usan ahora la plantilla estándar
`minecraft:item/generated` + `layer0`, igual que el resto. Sus originales
están respaldados en `tools/sprites2d/backup_models3d/`.

## Bloque y GUI del reciclador

Las tres caras del bloque (`recycler_front/side/top.png`, 16×16) y la textura
GUI (`textures/gui/recycler.png`, 176×166) también viven en el motor:

- `tools/pixelart/bloque.py` (`python -m tools.pixelart.bloque [--juego]`):
  tres funciones de cara que comparten la **cornisa** (`carroceria`, los
  cuatro cantos de 1 px idénticos en las caras) para que las esquinas del
  cubo y los bloques vecinos casen sin costura. El render valida opacidad
  total y cornisa común antes de escribir nada.
- `tools/pixelart/gui.py` (`python -m tools.pixelart.gui [--juego]`): compone
  el panel oscuro 176x166 (estilo generador HEPA) para el layout Rust de
  5 slots de entrada + 5 de salida. Las coordenadas son las del Java:
  entrada x=15+18k/y=24, medidor x=48..127/y=45..55, salida x=15+18k/y=60,
  inventario x=8+18k/y=89,107,125, hotbar x=8+18k/y=147 (ver
  `docs/TEXTURAS.md`). El relleno verde del medidor lo dibuja
  `RecyclerScreen` con separadores de 5 segmentos.

Los slots de la maquina viven en `RecyclerMenu`/`RecyclerBlockEntity`
(5 entradas procesadas como cola estilo Rust, 5 salidas); el titulo blanco y
el relleno del medidor se dibujan en `RecyclerScreen`.

`models/blockstates`, las recetas y los valores de reciclaje siguen intocables;
el unico Java que cambia con la GUI es `RecyclerMenu`/`RecyclerScreen`
(posiciones de slots y dibujo de textos/medidor).

## Cómo añadir un item nuevo

1. Añadir la entrada a `tools/items.json` (id, nombre, categoría).
2. Escribir la función sprite en el módulo temático que corresponda y
   registrarla en su `DIBUJOS`.
3. Validar en hoja de contacto y corregir hasta lectura correcta.
4. `python -m tools.pixelart.render --todos --juego` + `.\gradlew.bat build`.
