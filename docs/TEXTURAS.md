# Guía de texturas

Todas las texturas de item se generan por código con un estilo común (contorno legible y desgaste
moderado). Son un punto de partida: se pueden reemplazar sin tocar Java, modelos ni recetas,
sobrescribiendo el PNG con el mismo nombre y tamaño.

## Dónde están

```
src/main/resources/assets/chernobylz_recycler/
  textures/
    item/     <id>.png            (97 texturas, una por item)
    block/    recycler_front.png
              recycler_side.png
              recycler_top.png
    gui/      recycler.png        (176x166)
```

Los nombres de `textures/item/` coinciden exactamente con el `id` de `tools/items.json`.
Por ejemplo, el item `chernobylz_recycler:abrigo_afghanka` usa
`textures/item/abrigo_afghanka.png`.

## Items (32x32 pixel art)

- Tamaño: **32x32 píxeles**, PNG con canal alfa.
- Fondo transparente; el objeto debe ocupar el centro del lienzo.
- No hace falta animación.
- El modelo ya es `item/generated` con `layer0`, así que no hay que crear modelos.
- Se diseñan con el motor `tools/pixelart/` (ver `docs/DISENO_2D.md`); `tools/textures.py`
  y `tools/objects.py` son el pipeline viejo, deprecado.

### Flujo con Blockbench

1. `File > New Project > Java Block/Item` (o abre un proyecto vacío).
2. En el panel **Textures**, crea una textura de **16x16**.
3. Pinta el icono en el modo **Paint**. Activa la cuadrícula y usa lápiz de 1 píxel.
4. Exporta la textura: clic derecho en la textura del panel → **Export Texture**
   (o `File > Export > Export Textures`).
5. Guarda como PNG con el nombre exacto del item, por ejemplo `abrigo_afghanka.png`,
   dentro de `textures/item/`.

Consejos:

- Blockbench suele exportar con el nombre de la textura interna. Renómbralo al del item.
- Si el PNG sale en 32x32 o 64x64, vuelve a exportar a 16x16. Minecraft no lo escalará.
- Para ver el resultado sin reiniciar el cliente: `F3 + T` recarga recursos.
- En el juego, el tooltip muestra los rendimientos reales de la receta.

### Estilo por zona

| Zona | Paleta sugerida |
| :--- | :--- |
| Industrial | grises, óxido, amarillo de advertencia |
| Química | verdes ácidos, amarillos, bidones con etiquetas |
| Militar | verde oliva, caqui, negro, metal gastado |
| Hospital | blanco sucio, rojo médico, azul claro |
| Residencial | maderas, telas descoloridas, rojo ladrillo |
| Eléctrica | cobre, cian, negro de plástico, dorado de contactos |

Los recursos base (`tela`, `scrap`, `lingote_pesado`) conviene que sean muy legibles: se usan
en todos los tooltips y en el crafteo.

## Bloque (16x16 por cara)

El modelo es un cubo con tres texturas:

| Archivo | Caras |
| :--- | :--- |
| `recycler_front.png` | norte (la cara que se ve al colocar mirando al sur) |
| `recycler_side.png` | este, oeste y sur |
| `recycler_top.png` | arriba y abajo |

Requisitos:

- **16x16**, opacas (sin transparencia).
- Deben ser repetibles en los bordes para que no se note la costura entre bloques.
- La cara frontal debería leerse como una máquina: tolva, rejilla, panel de control o
  advertencia radiactiva. Es la que el jugador verá al usar el bloque.

Para reemplazarlas: sobrescribe los tres PNG y ejecuta `F3 + T`. No hay que tocar
`models/block/recycler.json` ni `blockstates/recycler.json`.

## GUI (176x166)

`textures/gui/recycler.png` es una interfaz de panel oscuro estilo generador:
fondo carbone, bordes grises finos, cabecera para el titulo blanco y la barra
de progreso verde de 5 segmentos. Layout de slots estilo Rust: 5 de entrada
arriba, medidor, 5 de salida abajo, y el inventario del jugador al pie.

Mantén **exactamente 176x166**: el blit de `RecyclerScreen` usa
(`TEXTURE_WIDTH=176`, `TEXTURE_HEIGHT=166`), nunca el de 7 argumentos (que
asume 256x256 y deforma).

| Elemento | Coordenadas (px) |
| :--- | :--- |
| Titulo (texto dibujado por Java, blanco) | x=8, y=6 sobre franja y=2..17 |
| Slots de entrada (5, centrados) | items x=44+18k, y=24 (marcos x=43..132, y=23..40) |
| Medidor de progreso | hueco x=48..127, y=45..55 (80x11, 5 segmentos) |
| Relleno del medidor | lo dibuja Java (verde `0xFF4E9A57`) + separadores |
| Slots de salida (5, centrados) | items x=44+18k, y=60 |
| Etiquetas ENTRADA/SALIDA | texto Java en escala 0.75, x=138 / y=28 y 64 |
| Etiqueta "Inventario" | texto dibujado por Java en x=8, y=78 |
| Inventario del jugador (3x9) | items x=8+18k, y=89 / 107 / 125 |
| Hotbar | items x=8+18k, y=147 |

Nota: los items de slot se colocan en la posicion de 16x16 (coincide con el
constructor de `RecyclerMenu`); el marco de 18x18 en la textura rodea ese
punto (item-1). Además, Minecraft dibuja su sprite vanilla de slot encima del
interior de cada marco: es lo esperado en GUIs custom.

## Regenerar texturas

El pipeline vigente es el motor pixel art `tools/pixelart/` (ver
`docs/DISENO_2D.md`):

```bash
python -m tools.pixelart.render --todos          # hoja de contacto de items
python -m tools.pixelart.render --todos --juego  # escribe las 97 texturas de item
python -m tools.pixelart.bloque --juego          # caras del bloque reciclador
python -m tools.pixelart.gui --juego             # GUI del reciclador (176x166)
```

Cada lote genera PNG nativos en `docs/pixelart/` y hojas de control
(`hoja_contacto.png`, `hoja_bloque.png`, `hoja_gui.png`). Las hojas viejas de
`docs/style_test/final/` corresponden al pipeline antiguo y ya no se usan.

## Previsualizar

```bash
python tools/preview.py
```

Genera:

- `docs/preview_items.png`: hoja con los 97 iconos.
- `docs/preview_gui.png`: la GUI al doble de tamaño.
- `docs/preview_block.png`: las tres caras del bloque.

## Checklist antes de publicar

- [ ] Los 97 PNG de `textures/item/` existen y pesan más de unos pocos bytes.
- [ ] Ningún icono tiene fondo blanco o negro opaco.
- [ ] Las tres caras del bloque son opacas y repetibles.
- [ ] La GUI mide 176x166 y los slots siguen alineados.
- [ ] `F3 + T` en el cliente no muestra texturas rosa/negras.
- [ ] `docs/preview_items.png` se ve legible a tamaño 16x16.
