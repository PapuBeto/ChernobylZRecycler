# -*- coding: utf-8 -*-
"""Los cinco sprites de prueba obligatorios: pixel art 32x32 disenado
directamente en la cuadricula. Luz global top-left de la coleccion;
transiciones por escalones de tono con dama; sin antialiasing ni ruido.

Cada sprite comparte la misma paleta (tools/pixelart/pal.py) y la misma
densidad: una sola resolucion (32x32) para TODA la coleccion.
"""
from __future__ import annotations

import math

from tools.pixelart import pal
from tools.pixelart.px import P, tono


# ---------------------------------------------------------------- motors
def motor_grua_sovietica(p: P):
    """Motor de grua: campana con rejilla de ventilador a la izquierda,
    caramel repujado con aletas, caja de bornes, gato de izado y pies."""
    hierro, oliva, carbon = pal.HIERRO, pal.OLIVA, pal.CARBON
    oxido, beige, laton = pal.OXIDO, pal.BEIGE, pal.LATON

    # --- carcaza (cuerpo ribeteado recidiendo a la derecha) -------------------
    p.rect(21, 7, 27, 27, tono(oliva, 2))
    p.pasos_v(21, 7, 27, 27, [tono(oliva, 3), tono(oliva, 2), tono(oliva, 1)])
    p.hlinea(21, 27, 27, tono(oliva, 0))
    p.pset(21, 7, tono(oliva, 4))
    # repujado: dos nervaduras verticales con luz en iabetes
    for xv in (23, 25):
        p.vlinea(xv, 8, 26, tono(oliva, 1))
        p.vlinea(xv + 1, 8, 26, tono(oliva, 3))
    p.hlinea(21, 27, 6, tono(hierro, 3))          # brida superior

    # --- tapa trasera del elemento --------------------------------------------
    p.rect(28, 9, 30, 26, tono(hierro, 1))
    p.banda_der(28, 9, 30, 26, tono(hierro, 0))
    p.banda_top(28, 9, 30, 26, tono(hierro, 2))
    p.pset(29, 12, tono(hierro, 4))
    p.pset(29, 23, tono(hierro, 4))

    # --- pie lejano / pie cercano ---------------------------------------------
    p.rect(22, 28, 26, 30, tono(hierro, 2))
    p.rect(21, 30, 27, 31, tono(hierro, 1))
    p.hlinea(21, 27, 31, tono(hierro, 0))
    p.pset(23, 29, tono(hierro, 4))
    p.pset(25, 29, tono(hierro, 4))
    p.rect(7, 28, 13, 30, tono(hierro, 2))
    p.rect(6, 30, 14, 31, tono(hierro, 1))
    p.hlinea(6, 14, 31, tono(hierro, 0))
    p.pset(9, 29, tono(hierro, 4))
    p.pset(11, 29, tono(hierro, 4))

    # --- caja de bornes ---------------------------------------------------------
    p.rect(22, 2, 26, 5, tono(hierro, 2))
    p.banda_top(22, 2, 26, 5, tono(hierro, 3))
    p.banda_bot(22, 2, 26, 5, tono(hierro, 1))
    p.hlinea(22, 26, 4, tono(hierro, 0))
    p.pset(23, 3, tono(hierro, 4))
    p.pset(25, 3, tono(hierro, 4))

    # --- gato de izado ------------------------------------------------------------
    for px, py in ((14, 2), (15, 2), (16, 3), (16, 4), (15, 5), (14, 5),
                   (13, 4), (13, 3)):
        p.pset(px, py, tono(hierro, 3))
    p.pset(14, 3, (0, 0, 0, 0))
    p.pset(15, 4, (0, 0, 0, 0))
    p.pset(14, 2, tono(hierro, 5))
    p.vlinea(14, 6, 6, tono(hierro, 2))

    # --- campana frontal (ventilador) -------------------------------------------
    C, CY = 11, 17
    p.elipse(C, CY, 11, 11, tono(hierro, 2), contorno=tono(hierro, 0))
    p.elipse(C, CY, 9, 9, tono(hierro, 3))       # anillo exterior brillante
    p.elipse(C, CY, 7, 7, tono(hierro, 2))       # escalon de vuelta
    p.elipse(C, CY, 5.4, 5.4, tono(hierro, 1))   # placa interior
    # rejilla oscura con anillos concéntricos y radios
    p.elipse(C, CY, 4, 4, tono(carbon, 2), contorno=tono(hierro, 2))
    p.elipse(C, CY, 1.6, 1.6, tono(hierro, 3))
    p.pset(C, CY, tono(hierro, 5))
    for grados in (45, 135, 225, 315):
        a = math.radians(grados)
        p.linea(int(C + 2.2 * math.cos(a)), int(CY + 2.2 * math.sin(a)),
                int(C + 3.8 * math.cos(a)), int(CY + 3.8 * math.sin(a)),
                tono(hierro, 2))
    # pernos del aro (2x2: luz arriba-izq + sombra abajo-der)
    for grados in (0, 60, 120, 180, 240, 300):
        a = math.radians(grados)
        bx = int(round(C + 9.4 * math.cos(a)))
        by = int(round(CY + 9.4 * math.sin(a)))
        p.pset(bx, by, tono(hierro, 5))
        p.pset(bx + 1, by + 1, tono(hierro, 1))
    # brillo de borde superior-izquierdo del aro
    for px, py in ((3, 9), (4, 8), (6, 7), (8, 6), (11, 6)):
        p.pset(px, py, tono(hierro, 4))

    # --- prensaestopas + latiguillo ---------------------------------------------
    p.pset(21, 5, tono(hierro, 3))
    for px, py in ((20, 6), (19, 7), (19, 8), (18, 9), (17, 10), (16, 11),
                   (16, 12)):
        p.pset(px, py, tono(carbon, 2))
        p.pset(px + 1, py, tono(carbon, 0))
    p.rect(15, 13, 16, 14, tono(carbon, 3))
    p.pset(15, 13, tono(carbon, 2))

    # --- oxido y desgaste deliberado --------------------------------------------
    p.pset(4, 25, tono(oxido, 2))
    p.pset(3, 24, tono(oxido, 1))
    p.pset(4, 26, tono(oxido, 1))
    p.pset(18, 26, tono(oxido, 2))
    p.pset(19, 26, tono(oxido, 1))
    p.pset(21, 26, tono(oxido, 2))
    p.pset(27, 25, tono(oxido, 2))
    p.pset(26, 6, tono(oxido, 1))
    p.pset(24, 25, tono(beige, 1))
    p.pset(7, 27, tono(oxido, 2))
    p.pset(25, 30, tono(oxido, 1))


# --------------------------------------------------------------- contador Geiger
def contador_geiger_pripyat(p: P):
    """Contador Geiger Pripyat-M roto: caja sovietica con pantalla craqueada,
    perilla de atenuacion, rejilla de altavoz y lampara de alerta."""
    oliva, hierro, cristal, carbon = pal.OLIVA, pal.HIERRO, pal.CRISTAL, pal.CARBON
    laton, beige, oxido, rojo = pal.LATON, pal.BEIGE, pal.OXIDO, pal.ROJO

    # caja con esquinas recortadas
    p.rect(3, 7, 28, 27, tono(oliva, 2))
    p.pasos_v(3, 7, 28, 27, [tono(oliva, 3), tono(oliva, 2), tono(oliva, 1)])
    p.hlinea(3, 28, 27, tono(oliva, 0))
    for x, y in ((3, 7), (28, 7), (3, 27), (28, 27)):
        p.pset(x, y, (0, 0, 0, 0))
    # pernos de tapa
    p.pset(4, 8, tono(hierro, 4))
    p.pset(27, 8, tono(hierro, 4))
    p.pset(4, 26, tono(hierro, 4))
    p.pset(27, 26, tono(hierro, 4))

    # pantalla con marco oscuro (cristal craqueado)
    p.rect(7, 10, 18, 17, tono(hierro, 0))
    p.rect(8, 11, 17, 16, tono(cristal, 1))
    p.banda_izq(8, 11, 17, 16, tono(cristal, 2))
    p.banda_top(8, 11, 17, 16, tono(cristal, 2))
    p.hlinea(8, 17, 15, tono(cristal, 0))
    p.hlinea(8, 17, 16, tono(cristal, 0))
    p.banda_der(8, 11, 17, 16, tono(cristal, 0))
    # aguja desviada
    p.pset(12, 15, tono(laton, 3))
    p.pset(11, 14, tono(laton, 3))
    p.pset(10, 13, tono(laton, 2))
    p.pset(9, 12, tono(laton, 2))
    p.pset(13, 15, tono(carbon, 0))
    # cristal roto: esquirla perdida y grietas
    p.pset(17, 11, tono(beige, 3))
    p.pset(17, 12, tono(beige, 2))
    p.pset(16, 11, tono(beige, 2))
    p.pset(15, 12, tono(cristal, 4))
    p.pset(14, 13, tono(cristal, 4))

    # perilla de goma
    p.elipse(23, 13, 2, 2, tono(carbon, 2), contorno=tono(carbon, 0))
    p.pset(22, 12, tono(carbon, 3))
    p.pset(25, 12, tono(beige, 3))
    # boton de sondeo
    p.rect(21, 17, 23, 19, tono(carbon, 1))
    p.hlinea(21, 23, 17, tono(carbon, 2))
    p.hlinea(21, 23, 19, tono(carbon, 0))
    # lampara de radiacion
    p.pset(26, 9, tono(rojo, 3))
    p.pset(27, 9, tono(rojo, 1))
    p.pset(26, 10, tono(rojo, 1))
    p.pset(27, 10, tono(rojo, 0))

    # rejilla de altavoz (puntos perforados)
    for yy in range(20, 25, 2):
        for xx in range(7, 15, 2):
            p.pset(xx, yy, tono(carbon, 0))
    # variaciones de desgaste
    p.pset(6, 25, tono(oxido, 1))
    p.pset(7, 25, tono(oxido, 2))
    p.pset(25, 21, tono(oxido, 2))
    p.pset(10, 7, tono(beige, 1))


# ------------------------------------------------------------------ mascarilla GP-5
def mascarilla_gp5(p: P):
    """Mascara antigas GP-5: visor de goma con dos lentes, filtro metálico
    central y correas laterales con perforaciones."""
    cauch, carbon, hierro = pal.CAUCHO, pal.CARBON, pal.HIERRO
    cristal, oxido = pal.CRISTAL, pal.OXIDO

    # correas (detras del visor, asoman por los lados)
    p.rect(3, 3, 5, 13, tono(cauch, 1))
    p.rect(26, 3, 28, 13, tono(cauch, 1))
    p.vlinea(4, 3, 13, tono(cauch, 2))
    p.vlinea(27, 3, 13, tono(cauch, 2))
    for yy in (5, 8, 11):
        p.pset(4, yy, tono(carbon, 0))
        p.pset(27, yy, tono(carbon, 0))

    # visor de goma: domo con sombreado escalonado
    p.elipse(16, 14, 10, 11, tono(cauch, 1), contorno=tono(cauch, 0))
    p.elipse(15, 13, 8, 9, tono(cauch, 2))          # media luna superior-izq
    for px, py in ((10, 7), (12, 6), (14, 5), (16, 5), (18, 5)):
        p.pset(px, py, tono(cauch, 3))              # brillo del domo

    # lentes
    p.elipse(11, 13, 2.4, 2.4, tono(carbon, 0), contorno=tono(cauch, 3))
    p.elipse(21, 13, 2.4, 2.4, tono(carbon, 0), contorno=tono(cauch, 3))
    p.pset(10, 12, tono(cristal, 4))
    p.pset(20, 12, tono(cristal, 4))
    p.pset(10, 13, tono(cristal, 2))
    p.pset(20, 13, tono(cristal, 2))

    # filtro metálico central
    p.elipse(16, 20, 4.5, 4.5, tono(hierro, 2), contorno=tono(hierro, 0))
    p.elipse(16, 20, 3, 3, tono(hierro, 1))
    p.elipse(16, 20, 1.3, 1.3, tono(carbon, 0))
    p.pset(13, 17, tono(hierro, 4))
    p.pset(12, 18, tono(hierro, 3))
    p.pset(19, 23, tono(hierro, 0))
    p.pset(13, 23, tono(hierro, 0))
    # valvula inferior
    p.rect(15, 25, 16, 26, tono(hierro, 1))
    p.hlinea(15, 16, 26, tono(hierro, 0))
    # oxido del filtro
    p.pset(19, 18, tono(oxido, 1))
    p.pset(18, 17, tono(oxido, 2))


# ------------------------------------------------------------------ bateria T-72
def bateria_tanque_t72(p: P):
    """Bateria de tanque sulfatada: bloque pesado de tres vistas, con hilos
    de celdas, bornes de acero y cristalizacion verde-blanca."""
    oliva, hierro, acero, oxido = pal.OLIVA, pal.HIERRO, pal.STEEL, pal.OXIDO
    sulfato, carbon = pal.SULFATO, pal.CARBON

    # cara superior (paralelogramo inclinado hacia arriba-izquierda)
    p.poligono([(4, 10), (26, 10), (29, 5), (7, 5)], tono(oliva, 4))
    # cara lateral derecha (alejada de la luz)
    p.poligono([(26, 10), (29, 5), (29, 24), (26, 27)], tono(oliva, 1))
    p.vlinea(29, 6, 25, tono(oliva, 0))
    p.pset(29, 24, tono(oliva, 0))
    p.pset(28, 24, tono(oliva, 0))
    # cara frontal
    p.rect(4, 10, 26, 27, tono(oliva, 2))
    p.pasos_v(4, 10, 26, 27, [tono(oliva, 3), tono(oliva, 2), tono(oliva, 1)])
    p.hlinea(4, 26, 27, tono(oliva, 0))
    p.hlinea(4, 29, 10, tono(oliva, 1))
    # separadores de celdas
    for xv in (9, 14, 19, 24):
        p.vlinea(xv, 12, 26, tono(oliva, 0))

    # tapones de bateria sobre la cara superior (metal oscuro)
    for x0 in (11, 20):
        p.rect(x0, 5, x0 + 3, 9, tono(hierro, 2))
        p.hlinea(x0, x0 + 3, 9, tono(hierro, 0))
        p.elipse(x0 + 1, 5, 1.6, 0.8, tono(hierro, 3))
        p.pset(x0 + 1, 6, tono(hierro, 1))

    # bornes de acero
    p.rect(6, 3, 7, 6, tono(acero, 4))
    p.hlinea(6, 7, 3, tono(acero, 5))
    p.rect(24, 3, 25, 6, tono(acero, 4))
    p.hlinea(24, 25, 3, tono(acero, 5))

    # cristalizacion de sulfato en bornes y esquinas
    p.pset(5, 7, tono(sulfato, 2))
    p.pset(5, 8, tono(sulfato, 1))
    p.pset(6, 8, tono(sulfato, 1))
    p.pset(25, 7, tono(sulfato, 2))
    p.pset(26, 8, tono(sulfato, 1))
    p.pset(25, 24, tono(sulfato, 1))
    p.pset(26, 25, tono(sulfato, 0))
    p.pset(24, 25, tono(sulfato, 1))

    # oxido y astillado
    p.pset(5, 24, tono(oxido, 2))
    p.pset(6, 25, tono(oxido, 1))
    p.pset(9, 26, tono(oxido, 1))
    p.pset(11, 23, tono(pal.BEIGE, 1))
    p.pset(19, 22, tono(pal.BEIGE, 1))

    # pernos de fijacion frontal
    p.pset(5, 12, tono(acero, 4))
    p.pset(25, 12, tono(acero, 4))


# ------------------------------------------------------------------ televisor Rubin
def televisor_rubin(p: P):
    """Televisor de tubo sovietico: chasis de madera tecida, CRT con curvatura
    brillosa, panel de perillas, rejilla parlante y antenas ofrmadas."""
    madera, carbon, cristal, acero = pal.MADERA, pal.CARBON, pal.CRISTAL, pal.STEEL
    oxido = pal.OXIDO

    # chasis
    p.rect(4, 6, 27, 26, tono(madera, 2))
    p.banda_top(4, 6, 27, 26, tono(madera, 3))
    p.banda_izq(4, 6, 27, 26, tono(madera, 3))
    p.banda_der(4, 6, 27, 26, tono(madera, 1))
    p.banda_bot(4, 6, 27, 26, tono(madera, 0))
    for x, y in ((4, 6), (27, 6), (4, 26), (27, 26)):
        p.pset(x, y, (0, 0, 0, 0))

    # marco de la pantalla
    p.rect(6, 8, 20, 20, tono(madera, 1))
    # CRT
    p.rect(7, 9, 19, 19, tono(cristal, 1))
    p.banda_izq(7, 9, 19, 19, tono(cristal, 2))
    p.banda_top(7, 9, 19, 19, tono(cristal, 2))
    p.banda_der(7, 9, 19, 19, tono(cristal, 0))
    p.banda_bot(7, 9, 19, 19, tono(cristal, 0))
    p.hlinea(7, 19, 14, tono(cristal, 0))
    p.hlinea(7, 19, 15, tono(cristal, 0))
    p.pset(9, 10, tono(cristal, 4))
    p.pset(10, 11, tono(cristal, 3))
    p.pset(8, 11, tono(cristal, 3))

    # panel de perillas
    p.rect(21, 8, 26, 20, tono(madera, 1))
    p.elipse(23, 11, 1.5, 1.5, tono(acero, 3), contorno=tono(carbon, 0))
    p.pset(24, 10, tono(carbon, 0))
    p.elipse(23, 15, 1.5, 1.5, tono(acero, 3), contorno=tono(carbon, 0))
    p.pset(24, 14, tono(carbon, 0))
    p.pset(23, 18, tono(carbon, 1))
    p.pset(24, 18, tono(carbon, 2))

    # rejilla de altavoz
    p.rect(6, 21, 26, 25, tono(carbon, 1))
    p.hlinea(6, 26, 22, tono(carbon, 2))
    p.hlinea(6, 26, 24, tono(carbon, 2))
    p.hlinea(6, 26, 25, tono(carbon, 0))

    # antenas en V
    p.pset(12, 6, tono(pal.HIERRO, 2))
    p.pset(16, 6, tono(pal.HIERRO, 2))
    for xx, yy in ((11, 5), (10, 4), (9, 3), (8, 2), (7, 1)):
        p.pset(xx, yy, tono(acero, 4))
    p.pset(7, 1, tono(acero, 5))
    for xx, yy in ((17, 5), (18, 4), (19, 3), (20, 2), (21, 1)):
        p.pset(xx, yy, tono(acero, 4))
    p.pset(21, 1, tono(acero, 5))

    # patas
    p.rect(7, 27, 8, 29, tono(madera, 0))
    p.rect(23, 27, 24, 29, tono(madera, 0))

    # desgaste
    p.pset(26, 19, tono(oxido, 1))
    p.pset(10, 25, tono(oxido, 1))
    p.pset(5, 14, tono(madera, 4))


DIBUJOS = {
    "motor_grua_sovietica": motor_grua_sovietica,
    "contador_geiger_pripyat": contador_geiger_pripyat,
    "mascarilla_gp5": mascarilla_gp5,
    "bateria_tanque_t72": bateria_tanque_t72,
    "televisor_rubin": televisor_rubin,
}
