# Sistema de diseño 3D (Fase 0)

Documento de trabajo del arte 3D de items de ChernobylZ. Define **cómo se
diseñan, escalan, texturizan y validan** los modelos low-poly de los 97 items
del mod, con una tubería que valida y previsualiza todo por código antes de
construir el JSON y los atlas definitivos.

- Paleta y reglas vivas: `tools/models3d/palette.py`
- Esquema de specs y validador: `tools/models3d/spec.py`
- Renderizador de previews: `tools/models3d/render.py`
- Generador de salida (JSON + atlas): `tools/models3d/build.py`
  (usa `python -m tools.models3d.build [ids...]`; hero 64×64 definido
  en `HEROES`)
- Specs por zona: `tools/models3d/specs/<zona>.py`
- Previews calibradas: `docs/models3d/`

Objetivo de estilo: props de supervivencia postapocalíptica (referencias
S.T.A.L.K.E.R. / DayZ / Tarkov) con geometría soviética de los 70-90:
funcional, macizo, sin ornamento gratuito, desgaste que cuenta la historia
del objeto. **Geometría real (volúmenes compuestos), no cubos con textura.**

## 1. Alcance técnico

- Minecraft 1.20.1 + Forge. Los items usan modelos JSON con `elements`
  (cubos): `assets/chernobylz_recycler/models/item/<id>.json`.
- Cada modelo lleva **una textura propia**: `textures/item/<id>.png`
  (atlas de color plano, una casilla por material), 32×32 por defecto y
  64×64 solo para hero items con visores/diales. Va en `textures/item/`
  porque vanilla ya cose ese directorio a su atlas: las carpetas nuevas
  (p. ej. `textures/model/`) no se cosen de forma fiable en 1.20.1 y los
  items salen violeta/negro aun con `atlases/blocks.json`.
- Los iconos planos actuales de `textures/item/` **se conservan** como
  referencia/documentación; el modelo 3D los sustituye en inventario y mano.
- Bloques de elemento: coordenadas enteras en rejilla **0..16** (`from` <
  `to` en cada eje); rotaciones de elemento solo **±22.5° / ±45°**.
- **Regla de detalle anti z-fighting**: toda pieza de detalle sobresale
  1 px del cuerpo y penetra **≥ 1 px** dentro de él (`from` entierrado).
  Nunca dos caras de distinto material coplanares con área en común.
- Solo se solapan caras coplanares del mismo material (fusión visual),
  nunca de materiales distintos.
- Nomenclatura de caras: `norte (−z) / sur (+z) / este (+x) / oeste
  (−x) / arriba / abajo`. La cámara estándar ve **arriba, sur (izquierda)
  y este (derecha)**.

## 2. Unidades y clases de tamaño

La unidad es el **píxel de modelo**: 1 unidad del espacio 0..16 (igual a 1
píxel de textura). Todo modelo apoya en el plano **y = 0**.

| Clase | Altura | Huella @ (x/z) | Uso típico |
| :--- | :--- | :--- | :--- |
| `pequena` | 6-10 | ≤ 10 | tazas, cubiertos, muñecas, fusibles, válvulas |
| `media`   | 10-15 | ≤ 16 | radios, contadores, casco, botas, filtros, traje |
| `grande`  | 14-16 | ≤ 16 | transformador, contrapeso, osciloscopio, viga |

- La huella y la altura cuentan desde el plano de apoyo (y=0).
- El modelo nunca flota: toda pieza apoya en y=0 o está unida a una pieza
  que apoya. `permitir_flotantes` solo con nota justificada (correas de
  transporte, cableado en tensión).

## 3. Presupuesto de piezas por tier

El tier de `tools/items.json` define el detalle máximo por modelo. Tras el
rediseño radical de la Fase 1 (calidad S.T.A.L.K.E.R.: cantidad de
componentes reales, no cajas) los topes subieron:

| Tier | Elementos máx. | Acentos máx. | Altura | Idioma visual |
| :--- | :-- | :-- | :-- | :-- |
| 1 (residential/electrical) | 24 | 2 | 6-12 | silueta simple, desgaste alto, 0-1 acento |
| 2 (industrial/hospital)    | 48 | 4 | 8-15 | máquina con cluster de control, 1-2 acentos |
| 3 (chemical/military)      | 64 | 5 | 10-16 | rasgo firma (visor/dial/franja), 2-3 acentos |

- Los acentos cuentan las piezas con material de desgaste (`WEAR`), no las
  de material pleno.
- Piezas 1×1×1 reservadas a remaches y conectores (el validador avisa si se
  abusa).
- El detalle no es obligatorio: menos piezas bien compuestas > muchas
  piezas amontonadas.

## 4. Gramática de forma

Todo modelo del catálogo se construye con la misma gramática:

1. **Masa principal** (60-70 % del volumen): la carcasa/silueta.
2. **Rasgo firma** (el item se reconoce por esto): visor, dial, espiral,
   boquilla, cuchara, pantalla, asa…
3. **Cluster de control** (opcional, si lo tenía el objeto real): botones,
   válvulas, interruptores; 2-3 piezas máx.
4. **Anclas de desgaste**: donde el objeto real se desgasta (bordes bajos,
   juntas, asas): parches salientes 1 px con materiales de `WEAR`.

Rasgo firma por categoría:

| Categoría | Masa principal | Rasgo firma | Detalles habituales |
| :--- | :--- | :--- | :--- |
| `maquinaria` | carcasa maciza apoyada | motor/compresor que sobresale | remaches, franja de peligro, ganchos de grúa |
| `electronica` | caja rectangular | visor/panel frontal | botones, antena, dial de mano, rejilla |
| `recipiente` | volumen rotacional (frasco/taza/tambor) | pico/tapa/boquilla | asa lateral, etiqueta grabada |
| `medico` | cuerpo blanco/vidrio | indicador o escala | boquilla, jeringa, varilla, pinza |
| `textil` | paneles colgantes o doblados | cuello/estampado | tirantes, bolsillos, cremallera |
| `metal` | pieza en L o barra | perforaciones en fila | rebajes, remaches en hilera |
| `prop` | silueta doméstica simple | su contorno característico | 1-2 anclas de desgaste |

## 5. Silueta y legibilidad

- La silueta debe leerse a 256×256 y a tamaño de slot de GUI: la masa
  principal y el rasgo firma se separan 2-3 tonos del contorno.
- Nunca > 3 masas grandes exteriormente compuestas; los detalles pequeños
  viven ADOSADOS a una masa (sobresalen 1 px), nunca sueltos.
- Una cara "hero": el frente (sur) lleva el rasgo firma; lateral para
  accesorios (dials, rejillas de ventilación, enchufe).
- Proporción: las clases varían su altura al menos 2 px entre sí; nunca
  caras coplanares: relieve de 1 px y penetración ≥ 1 px (sección 1).
- Volumen mínimo legible: rasgos ≥ 2 px en su eje mayor; piezas 1×1×1 solo
  remaches/conectores.

## 6. Materiales

La paleta vive en `tools/models3d/palette.py` (`MATERIALES`, con variantes
`base`/`claro`/`oscuro`) y es espejo de la paleta 2D (estilo D). Resumen
con usos:

| Material | Base | Uso canónico |
| :--- | :--- | :--- |
| `acero` | #8A8E92 | chapa general, carcasa industrial |
| `hierro` | #606468 | chapa envejecida, soportes |
| `metal_oscuro` | #525658 | interior de máquinas, herrajes oscuros |
| `aluminio` | #A8AEB4 | paneles de instrumentos, remaches, marcos |
| `plomo` | #6A7078 | blindaje radiactivo |
| `cobre` | #B87040 | cableado, trajes térmicos |
| `laton` | #BC9E52 | diales, conectores, remates de valor |
| `vidrio` | #5498C0 | ampollas, lámparas, pantallas |
| `vidrio_oscuro` | #283034 | visores y diales apagados |
| `porcelana` | #DEDCD4 | aisladores eléctricos, sanitarios, enchufes |
| `pantalla` | #405434 | pantallas CRT/LCD apagadas |
| `verde_oliva` | #62704A | laca militar clásica |
| `verde_militar` | #467444 | laca verde saturada |
| `baquelita` | #6E543A | carcasas de radios, teléfonos e instrumentos |
| `baquelita_negra` | #343230 | carcasas negras (teléfono, interruptor) |
| `plastico_amarillento` | #CCC49C | plásticos de los años 70-80, amarillentos |
| `beige_aparato` | #BEB8A6 | cocinas, decoración doméstica |
| `goma` | #4E524E | mangos, juntas, sondas |
| `amarillo_peligro` | #CCAC46 | franjas de maquinaria |
| `rojo_desgastado` | #96463C | botones, señales de emergencia |
| `verde_acido` | #80BA4C | líquidos ácidos, etiquetas |
| `blanco_lab` | #C6CCCC | equipo de laboratorio |
| `azul_quirurgico` | #588494 | vestimenta médica |
| `hazmat` | #B0B45C | laca antirradiación pálida |
| `caqui` | #8C8460 | uniformes |
| `kevlar` | #80886E | chalecos reforzados |
| `tela_crema` | #BEB296 | tapicería, correas de transporte |
| `pelaje` | #6E5C48 | ushanka, forro |
| `madera` | #7A5838 | mangos de herramientas, cajas, mobiliario |

## 7. Desgaste (lenguaje y presupuesto)

Paleta de desgaste (`WEAR`) con colocación canónica:

| Desgaste | Valor | Dónde | Máximo en superficie |
| :--- | :--- | :--- | :--- |
| `oxido` | #94542A | juntas y bordes bajos del metal | 30 % |
| `oxido_oscuro` | #683A1C | óxido seco, metal quemado | 25 % |
| `mugre` | #5E584A | tercio inferior, asas, cantos | 25 % |
| `hollin` | #242220 | chimeneas, motores, fogatas | 20 % |
| `imprimacion` | #807A72 | puntas de pintura saltada | 10 % |
| `sulfato` | #B0BAC0 | baterías: bornes y cantos | 15 % |
| `sulfato_azul` | #7A98B4 | pilas alcalinas: fugas | 12 % |
| `goteo_acido` | #80BA4C | canales verticales desde la tapa | 15 % |
| `patina_rad` | #968E56 | juntas de zona radiactiva (chemical) | 15 % |
| `moho` | #606E54 | textiles húmedos, madera | 20 % |
| `yodo` | #965C36 | hospital: recipientes de antiséptico | 10 % |
| `quemado` | #4A4038 | plástico/madera chamuscada | 20 % |

Reglas:

- El desgaste **geográfico** sigue la historia del objeto:
  - bordes/cantos → pintura saltada (`imprimacion`) y óxido;
  - base → mugre + suciedad;
  - juntas → oxidación;
  - boca/pico de recipiente → goteo/residuos;
  - asas/manijas → mugre de uso.
- Cada estado del nombre del item (`roto`, `perforado`, `quemado`, `abollado`,
  `fundido`, `irradiado`) tiene su lenguaje geométrico:

| Estado | Lenguaje geométrico en el modelo |
| :--- | :--- |
| roto | parte faltante limpia; o pieza desplazada dentro del plano |
| perforado | hueco construido entre cajos, con borde en muescas |
| quemado | esquinas quemadas (hollín) y volumen achaparrado |
| abollado | cantos rebajados (esquina hundida 1 px) |
| fundido | silueta colapsada y gotas colgando |
| irradiado | pátina `patina_rad` en juntas sin deformar volumen |

- Material correcto: nunca moho sobre goma; nunca hollín directo sobre
  `blanco_lab` salvo quema explicada por el nombre del item.
- Presupuesto global: el desgaste es ≤ 30 % de la superficie visible del
  modelo, colocado una vez fijada la zona (sección 9).

## 8. Lenguaje de valor (tier)

El valor del item no se telegrafia con tamaño ni con limpieza, sino con
**complejidad + material hero + rasgo firma**:

- **tier 1**: doméstico/electrodoméstico simple; 1 material dominante, 1
  acento máx; el daño es normal y no oculta el rasgo firma.
- **tier 2**: piezas de máquina/instrumento; 2 acentos; cluster de control;
  material secundario estructural (aluminio con acero).
- **tier 3**: hero items químicos/militares; 3 acentos; rasgo firma fuerte
  (visor con marco, dial de latón, lente, franja de peligro) y 1 material
  hero (latón, vidrio, hazmat).
- Un item "roto" sigue leyéndose valioso si conserva su rasgo firma
  (los componentes que se reciclan son el valor).
- Los 16 `components` de items.json (piezas que fabrica el reciclador)
  se diseñan más limpios que los objetos: llegan "nuevos" de fábrica,
  con menos desgaste geométrico y más definición.

## 9. Código de zona (tabla en `palette.py` → `ZONA_INFO`)

| Zona | Materiales dominantes | Acento | Nota |
| :--- | :--- | :--- | :--- |
| `industrial` | acero, hierro, metal_oscuro, aluminio | amarillo_peligro | franjas de peligro en bandas, óxido en juntas |
| `chemical` | hazmat, verde_oliva, goma, vidrio, blanco_lab, baquelita | verde_acido | manchas ácidas y pátina radiactiva en juntas |
| `military` | verde_oliva, verde_militar, caqui, metal_oscuro, baquelita | rojo_desgastado | marcas de peligro pequeñas, piezas mayormente intactas |
| `hospital` | blanco_lab, azul_quirurgico, acero, aluminio | rojo_desgastado | porcelana y plásticos limpios con señales de emergencia |
| `residential` | tela_crema, madera, beige_aparato, pelaje, porcelana | rojo_desgastado | objeto doméstico evacuado: mugre, hollín y moho |
| `electrical` | cobre, laton, porcelana, goma, plastico_amarillento, vidrio | amarillo_peligro | herrajes con cableado saliente y hollín de chispa |

El acento de zona aparece como máximo en 2 piezas del modelo (banda,
botón o placa); es **marca del mundo**, no decoración.

## 10. Convenciones de archivo y specs

```
tools/models3d/
  palette.py          paleta, zonas, clases, displays (fuente de verdad)
  spec.py             esquema + validador
  render.py           previews isométricas (CLI)
  specs/<zona>.py     SPECS: una entrada dict por item
docs/models3d/
  <id>.png            render individual (256×256, fondo gris neutro)
  hoja_<zona>.png     hoja de contacto de revisión
```

Dentro del mod (Fase 1+):

```
assets/chernobylz_recycler/models/item/<id>.json     modelo 3D
assets/chernobylz_recycler/textures/model/<id>.png   atlas del modelo
```

Plantilla de spec (claves en español, ASCII):

```python
{
    "id": "contador_geiger_pripyat",
    "nombre": "Contador Geiger \"Pripyat-M\" Roto",
    "zona": "chemical",
    "tier": 3,
    "categoria": "electronica",   # maquinaria|electronica|recipiente|medico|textil|metal|prop
    "clase": "media",             # pequena|media|grande
    "silueta": "…una frase…",
    "notas": ["historia visual", "decisiones"],
    "permitir_flotantes": False,
    "piezas": [
        {"nombre": "cuerpo", "desde": [0, 0, 4], "hasta": [10, 11, 9], "material": "baquelita"},
        {"nombre": "visor", "desde": [3, 5, 9], "hasta": [6, 8, 11], "material": "vidrio_oscuro"},
        {"nombre": "dial", "desde": [8, 5, 5], "hasta": [12, 9, 8], "material": "laton.base",
         "caras": {"este": "vidrio_oscuro"}},
    ],
}
```

`caras` permite pintar una cara concreta con otra referencia de paleta
(el visor de vidrio sobre el marco de aluminio). Las rotaciones de pieza
se declaran con `rotacion: {eje, angulo, origen}` (±22.5/±45).

## 11. Displays estándar

`palette.display_estandar(clase)` genera el bloque `display` JSON a usar en
todos los modelos (coherencia visual):

| Escala | gui | ground/fixed/manos |
| :--- | :-- | :-- |
| pequena | 0.85 | 0.55 |
| media | 0.70 | 0.45 |
| grande | 0.60 | 0.35 |

Con rotación gui estándar `[30, 225, 0]` y manos `[0, ±135/225, 0]`.
Los ajustes de la Fase 3 pueden tocar `translation`; la rotación gui
no cambia.

## 12. Tubería (pipeline — flujo Blockbench)

La herramienta principal es **Blockbench**: cada modelo nace como proyecto
`.bbmodel` FUENTE (editable en Blockbench) con geometría, grupos, UV y
textura pintada incrustada; el JSON de Minecraft (`models/item/<id>.json`)
y el PNG (`textures/item/<id>.png`) son EXPORTACIÓN de ese proyecto.

```text
1. specs fuente             tools/models3d/specs/<zona>.py
2. python -m tools.models3d.bbsrc      → tools/models3d/blockbench/<id>.bbmodel
                                       (proyecto fuente; internamente usa
                                        planificar + pintar_textura de bbpaint)
3. python -m tools.models3d.bbexport   → src/main/resources/assets/chernobylz_recycler/
                                        models/item/<id>.json + textures/item/<id>.png
4. python -m tools.models3d.bbpreview  → docs/models3d/<id>.png + hoja_<zona>.png
                                        (previews texturizadas)
   (los pasos 2+3 juntos: python -m tools.models3d.build [ids...])
5. revisar la preview; retoques de textura → FIRMAS/familias en
   tools/models3d/bbpaint.py y regenerar; retocar geometría a mano →
   abrir el .bbmodel en Blockbench (convenciones en 12.5)
```

El render de color plano (`python -m tools.models3d.render <id>`) sigue
disponible como *ghost* de comparación, pero la preview definitiva es la
texturizada de `bbpreview` (warp afín por tesela + máscara de
paralelogramo, misma proyección y sombra que `render.py`).

### 12.1 Formato `.bbmodel` (validado contra Blockbench 4.10)

- `meta: {format_version: "4.10", model_format: "java_block", box_uv: false}`.
- `resolution: {width, height}` = espacio UV del proyecto (lados
  escalables, ver 12.4); la textura incrustada mide UV×8 px.
- `textures[]`: una entrada; `source` = data URI PNG, `internal: true`.
- Las caras referencian la textura por **índice entero** (`"texture": 0`).
- Cubos: `from/to` en unidades MC; la **rotación del proyecto** es
  `[x,y,z]` en grados, un solo eje, ±22.5/±45, con `origin` aparte.
- Grupos en `outliner` (uno por pieza, hijos = uuids; estilo legacy 4.10
  con `groups: []`).
- `display` = mismo formato del JSON de MC; `gui_light: "front"` solo si
  `front_gui_light: true`.

### 12.2 Mapeo UV natural por cara (idéntico al de Minecraft)

Fuente `UVToLocal` (cube.js, igual que el juego): en caras laterales
**sur** u→+x, **norte** u→−x, **este** u→−z, **oeste** u→+z, con v→−y;
en **arriba** u→+x y v→+z; en **abajo** u→+x y v→−z. Por eso las firmas
se pintan en vista externa directa: lo que se ve en el PNG es lo que se
ve en el juego mirando esa cara de frente.

### 12.3 Política de regiones UV y firmas

- Cada cara recibe una región UV del **tamaño exacto de la cara**
  (2 px UV por unidad MC): cero estiramientos y densidad uniforme
  (16 px PNG por unidad, la misma de los iconos de item).
- Caras con la misma `(clave_material, dims)` **comparten** región; se
  pinta baldosa a baldosa (1 unidad = 1 casilla con semilla por
  posición) para que la repetición no se note.
- **Firmas**: rect dedicado por `(pieza, cara)` — aguja del geiger,
  placa 48ТН-125, reja del radio, visor del casco, deck de la batería…
  (`LienzoFirma` recorta, dibuja con rng determinista y pega de vuelta).
- `_sangrado_bordes` copia el borde exterior 1 px hacia los huecos
  vecinos (evita que el mipmap promedie el color equivocado).

### 12.4 Espacios UV escalables

El planificador prueba lados 32 → 48 → 64 → 96 → 128 px UV y toma el
primero donde caben todas las regiones (PNG = UV×8). Pilotos: geiger,
traje y radio 64; batería y motor 96 (PNG 512/768, dentro del atlas).
Al exportar, el UV se reescala a 0..16 dividiendo por `resolution/16`.

### 12.5 Edición en Blockbench y regeneración

- El `.bbmodel` abre directo en Blockbench (formato java_block): se
  puede seguir modelando y pintando ahí.
- OJO: regenerar con `bbsrc` REEMPLAZA el proyecto; si se editó a mano,
  guardar la copia editada fuera de `tools/models3d/blockbench/` (o
  copiarla) antes de regenerar.
- Reexportar desde Blockbench (File ▸ Export ▸ Java Item/Block Model) es
  compatible: mismas convenciones de UV y caras. El PNG sale del data
  URI incrustado (o se guarda aparte en `textures/item/<id>.png`).
- Cambiar `resolution` a mano desalinea las uv de las caras (referencian
  px absolutos del espacio); si se redimensiona, regenerar el pintado.

## 13. Calibración: `contador_geiger_pripyat`

La spec calibrada (zona `chemical`, tier 3, 24 piezas, clase media)
documenta el sistema completo — caja de baquelita, marco con visor de
vidrio (aguja pintada en la firma sur), botonera, correa de lona rota,
dial lateral de latón (firma este: reloj), parches de desgaste, sonda
vertical y cable. La geometría exacta está en
`tools/models3d/bbsrc.py` y las firmas en `bbpaint.py`.

Imagen: `docs/models3d/contador_geiger_pripyat.png` (preview
texturizada; `render.py` da el ghost plano para comparar). Ajustes que
salieron de la calibración: proyección isométrica (cámara
arriba-sur-este), sombra por huella convexa difuminada, teselas de
z-buffer en rejilla para caras grandes superpuestas a distintos niveles.

## 14. Checklist QA por modelo

- [ ] `desde`/`hasta` enteros en 0..16, `desde < hasta`
- [ ] apoya en y=0 (o `permitir_flotantes` documentado)
- [ ] altura y huella dentro de la clase y del tier
- [ ] piezas ≤ tope del tier; remaches 1×1×1 solo conectores
- [ ] detalles salientes 1 px, penetración ≥ 1 px, sin coplanaridad
- [ ] silueta legible a slot; rasgo firma presente y visible
- [ ] materiales de la paleta, variantes correctas
- [ ] desgaste ≤ 30 %, colocado con geografía, ACENTO de zona ≤ 2 piezas
- [ ] la cara sur (izquierda) lleva el mejor detalle; ventana lectora entre
      clases (pequena ≠ media ≠ grande)
- [ ] ids/nombres EXACTOS contra tools/items.json

## 15. Fases siguientes

- **Fase 1 — lote piloto (5 items) ✓**: specs rediseñadas (motor 38,
  batería 24, radio 28, geiger 24, traje 22 piezas), proyectos
  `.bbmodel` fuente + texturas pintadas + modelos exportados e
  integrados in-game (`models/item/<id>.json` + `textures/item/<id>.png`;
  ver 12). Previews texturizadas en `docs/models3d/`.
- **Fase 2 — despliegue por zonas** (los 92 restantes: 3 recursos
  + 16 componentes + 73 objetos, en tandas de 6-8 specs): chemical →
  military → industrial → hospital → electrical → residential.
- **Fase 3 — pulido**: revisión in-game (gui/ground/hands), ajustes de
  `display` desde Blockbench, retoque de firmas/familias del pintor,
  hojas de contacto finales.
