# -*- coding: utf-8 -*-
"""Paleta pixel art de ChernobylZ.

Rampas de tonos ordenadas del oscuro (0) al claro (ultimo), coherentes con
el enfoque desaturado de un mundo postapocaliptico soviético y con la
estetica de las texturas vanilla de Minecraft. Todos los sprites comparten
estas rampas: las zonas se distinguen por MATERIAL (acero, oliva, oxido...),
nunca por colores sueltos.

La luz global es top-left (como los items vanilla): el borde superior e
izquierdo de cada pieza toma el indice alto de la rampa, el derecho e
inferior el bajo, y las transiciones entre bandas usan dama (dithering).
"""

STEEL = (       # acero mecanizado / gris metalico
    (26, 29, 32), (43, 47, 52), (64, 70, 76), (88, 95, 102),
    (120, 128, 136), (160, 168, 176))

HIERRO = (      # fundicion oscura / estructura sin pintar
    (22, 23, 25), (35, 37, 40), (52, 56, 60), (72, 77, 82),
    (96, 102, 108))

OLIVA = (       # pintura militar/electronica sovietica
    (38, 41, 22), (58, 62, 33), (80, 85, 45), (104, 109, 62),
    (132, 136, 84), (158, 162, 110))

MADERA = (      # chapa/madera teñida (muebles turcos)
    (46, 32, 20), (66, 47, 29), (92, 66, 40), (121, 88, 55),
    (148, 112, 74))

OXIDO = (       # corrosión marron (degradado puro)
    (48, 26, 15), (74, 42, 23), (102, 60, 32), (133, 81, 44),
    (162, 109, 63), (190, 141, 89))

BEIGE = (       # lino/envejecido (hueso, papel, plastico viejo)
    (92, 86, 68), (122, 114, 91), (152, 143, 117), (183, 174, 148),
    (210, 203, 182))

CARBON = (      # negro carbón (goma, sombras, botones)
    (14, 15, 18), (30, 32, 37), (52, 55, 62), (78, 82, 90))

LATON = (       # laton/cobre brillo (placas, contactos)
    (64, 48, 20), (105, 81, 32), (146, 114, 44), (189, 155, 70),
    (227, 201, 110))

AMARILLO = (    # industrial marca y seguridad
    (96, 74, 20), (140, 109, 24), (184, 144, 30), (224, 182, 42))

CRISTAL = (     # pantallas/piezas de vidrio turbio
    (16, 26, 29), (28, 42, 46), (46, 66, 71), (70, 96, 101),
    (104, 133, 137), (141, 171, 173))

CAUCHO = (      # goma (mascarilla, cable)
    (15, 15, 18), (30, 30, 35), (48, 48, 55), (70, 70, 78))

SULFATO = (     # cristalizacion blanco-verdosa de baterias
    (94, 102, 80), (124, 134, 105), (157, 168, 134), (190, 199, 166))

ROJO = (        # lampara/liquido (poco uso, marca elect)
    (70, 18, 16), (126, 32, 24), (176, 56, 38), (214, 102, 66))

#--------

def t(rampa, i):
    """Tono escalonado de una rampa, con indice recortado a su rango."""
    return rampa[max(0, min(len(rampa) - 1, int(i)))]
