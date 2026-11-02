Chernobyl Z: Reciclaje
======================

Mod de Forge 1.20.1 (Java 17) que implementa el sistema de reciclaje del GDD de
Chernobyl Z: recicladora colocable, 3 recursos base, 16 componentes utiles y 78
objetos repartidos en 6 zonas de riesgo.

Documentacion completa: README.md

Resumen rapido
--------------

- Instalar el jar en mods/ del servidor y de los clientes.
- Craftear la recicladora:
      L L L
      L A L      L = lingote de hierro
      L R L      A = alto horno, R = bloque de redstone
- Usar: clic derecho en la recicladora, poner un objeto en la entrada y sacar
  el resultado de la parrilla 3x3.
- Comandos de operador:
      /czrecycler loot <jugadores> <zona> [cantidad]
      /czrecycler zones
- Configuracion: config/chernobylz_recycler-common.toml
      allowPhaseTwo, processingSpeedMultiplier, enableLootModifiers

Documentos
----------

- README.md          Guia de instalacion, uso, balance y estructura.
- docs/ITEMS.md      Catalogo completo con rendimientos y tiempos.
- docs/TEXTURAS.md   Como reemplazar los placeholders en Blockbench.
- docs/LOOT.md       Como conectar el loot a las loot tables del servidor.
- docs/preview_*.png Previews de items, GUI y bloque.

Compilar
--------

    ./gradlew build

El jar se genera en build/libs/.

Notas
-----

Las texturas incluidas son placeholders generados con tools/generate.py. Se pueden
sobrescribir con arte propio manteniendo el mismo nombre y tamano.

LICENSE.txt y CREDITS.txt pertenecen al MDK de Forge.
