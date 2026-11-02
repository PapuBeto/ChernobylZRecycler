# -*- coding: utf-8 -*-
"""Recursos y componentes: pixel art 32x32, paleta comun de la coleccion."""
from __future__ import annotations

import math

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import (cara, cilindro, corroer, rejilla_lineas,
                                   rejilla_puntos, terminal)


# ------------------------------------------------------------------ recursos
def tela(p):
    """Tela: pila de pliegues de lino envejecido."""
    beige, carbon = pal.BEIGE, pal.CARBON
    # rollo inferior
    p.rect(5, 22, 26, 28, tono(beige, 1))
    p.hlinea(5, 26, 22, tono(beige, 3))
    p.hlinea(5, 26, 28, tono(beige, 0))
    for x in range(6, 26, 4):
        p.pset(x, 24, tono(beige, 0))
    # rollo superior
    p.rect(8, 15, 25, 21, tono(beige, 2))
    p.hlinea(8, 25, 15, tono(beige, 3))
    p.hlinea(8, 25, 21, tono(beige, 1))
    for k, x in enumerate(range(9, 25, 5)):
        p.pset(x, 17 + (k % 2), tono(beige, 0))
    # pieza doblada encima
    p.rect(10, 8, 23, 14, tono(beige, 3))
    p.hlinea(10, 23, 8, tono(beige, 4))
    p.linea(11, 13, 21, 10, tono(beige, 1))
    p.hlinea(10, 23, 14, tono(beige, 1))
    # hilvanes
    for x in (12, 16, 20):
        p.pset(x, 12, tono(carbon, 1))


def scrap(p):
    """Scrap: monton de chatarra retorcida (chapas, tubos, alambre)."""
    hierro, acero, oxido = pal.HIERRO, pal.STEEL, pal.OXIDO
    # monton base
    p.poligono([(3, 28), (9, 19), (22, 16), (29, 22), (28, 28)],
               tono(hierro, 2))
    p.hlinea(3, 29, 28, tono(hierro, 0))
    # chapas superpuestas
    p.poligono([(7, 23), (15, 14), (24, 18), (18, 24)], tono(acero, 3))
    p.linea(15, 14, 24, 18, tono(acero, 4))
    p.poligono([(14, 26), (20, 20), (27, 25), (21, 27)], tono(hierro, 1))
    # tubo enhiesto
    p.vlinea(11, 9, 15, tono(acero, 2))
    p.vlinea(12, 9, 15, tono(acero, 0))
    p.pset(11, 9, tono(acero, 4))
    # alambre enroscado
    for x, y in ((23, 10), (24, 11), (25, 12), (24, 13), (23, 13), (22, 12)):
        p.pset(x, y, tono(acero, 1))
    p.vlinea(24, 13, 17, tono(acero, 1))
    # oxido
    corroer(p, [(6, 25, 2), (9, 26, 1), (20, 25, 2), (26, 24, 1),
                (13, 22, 2)], oxido)


def lingote_pesado(p):
    """Lingote pesado: bloque trapezoidal de fundicion con marcas."""
    acero, hierro, oxido = pal.STEEL, pal.HIERRO, pal.OXIDO
    # cuerpo trapezoidal
    p.poligono([(6, 24), (10, 14), (24, 14), (28, 24)], tono(acero, 2))
    # cara superior
    p.poligono([(10, 14), (24, 14), (26, 16), (8, 16)], tono(acero, 4))
    # lateral sombra
    p.poligono([(26, 16), (28, 24), (24, 24), (25, 16)], tono(acero, 0))
    p.hlinea(6, 28, 24, tono(hierro, 0))
    # rebaba y muescas
    p.pset(9, 15, tono(acero, 4))
    p.pset(21, 16, tono(acero, 3))
    p.pset(12, 13, tono(acero, 1))
    # marca de colada pintada
    p.rect(14, 18, 17, 20, tono(pal.AMARILLO, 2))
    p.hlinea(14, 17, 20, tono(pal.AMARILLO, 1))
    # oxido de fundicion
    corroer(p, [(7, 22, 2), (8, 23, 1), (24, 21, 1), (26, 20, 2),
                (11, 19, 1)], oxido)


# ----------------------------------------------------------------- componentes
def engranaje_titanio(p):
    """Engranaje de titanio: disco dentado con eje y agujero de Veryna."""
    acero, hierro = pal.STEEL, pal.HIERRO
    cx, cy, r = 16, 16, 9
    # dientes
    for grados in range(0, 360, 30):
        a = math.radians(grados)
        dx, dy = math.cos(a), math.sin(a)
        ex, ey = int(round(cx + (r + 1.6) * dx)), int(round(cy + (r + 1.6) * dy))
        p.elipse(ex, ey, 1.7, 1.7, tono(acero, 2))
    # disco
    p.elipse(cx, cy, r, r, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(cx - 1, cy - 1, r - 2, r - 2, tono(acero, 3))
    p.elipse(cx, cy, r - 4, r - 4, tono(acero, 2))
    # agujeros de reduccion de peso
    for grados in (0, 60, 120, 180, 240, 300):
        a = math.radians(grados)
        p.elipse(cx + 5 * math.cos(a), cy + 5 * math.sin(a), 1, 1,
                 tono(hierro, 1), contorno=tono(hierro, 0))
    # eje central
    p.elipse(cx, cy, 2.2, 2.2, tono(acero, 1))
    p.elipse(cx, cy, 1.2, 1.2, tono(hierro, 3))
    p.pset(cx - 1, cy - 1, tono(acero, 4))
    # cuña de la chaveta
    p.pset(cx + 1, cy, tono(hierro, 0))
    p.pset(cx + 2, cy, tono(hierro, 0))


def piston_hidraulico(p):
    """Piston hidraulico: camisa cilindrica con baqueta cromada."""
    acero, hierro, carbon = pal.STEEL, pal.HIERRO, pal.CARBON
    # camisa (cuerpo izquierdo)
    p.rect(4, 12, 15, 22, tono(acero, 1))
    p.hlinea(4, 15, 12, tono(acero, 3))
    p.hlinea(4, 15, 22, tono(hierro, 0))
    p.vlinea(4, 12, 22, tono(acero, 3))
    p.vlinea(15, 12, 22, tono(acero, 0))
    # collar con tornillos
    p.rect(3, 11, 16, 13, tono(hierro, 2))
    p.hlinea(3, 16, 11, tono(hierro, 3))
    p.pset(5, 12, tono(hierro, 4))
    p.pset(14, 12, tono(hierro, 4))
    # baqueta cromada
    p.rect(16, 15, 26, 18, tono(acero, 4))
    p.hlinea(16, 26, 15, tono(acero, 5))
    p.hlinea(16, 26, 18, tono(acero, 2))
    p.pset(26, 15, tono(acero, 5))
    # terminal ojo de la baqueta
    p.elipse(28, 16, 2, 3, tono(hierro, 2), contorno=tono(hierro, 0))
    p.elipse(28, 16, 0.8, 1.4, (0, 0, 0, 0))
    # engrasa goteo oscuro bajo la camisa
    p.pset(9, 23, tono(carbon, 0))
    p.pset(10, 23, tono(carbon, 1))


def tubo_presion(p):
    """Tubo de presion: seccion con bridas y remaches."""
    acero, hierro, amarillo = pal.STEEL, pal.HIERRO, pal.AMARILLO
    # cuerpo del tubo (horizontal)
    p.rect(7, 12, 24, 20, tono(acero, 2))
    p.hlinea(7, 24, 12, tono(acero, 4))
    p.hlinea(7, 24, 13, tono(acero, 3))
    p.hlinea(7, 24, 19, tono(acero, 1))
    p.hlinea(7, 24, 20, tono(hierro, 0))
    # boca izquierda (interior oscuro)
    p.elipse(7, 16, 2.6, 4, tono(hierro, 1), contorno=tono(hierro, 0))
    # brida trasera con remaches
    p.rect(22, 10, 25, 22, tono(hierro, 2))
    p.hlinea(22, 25, 10, tono(hierro, 3))
    p.hlinea(22, 25, 22, tono(hierro, 0))
    for y in (13, 16, 19):
        p.pset(23, y, tono(acero, 4))
    # banda de identificacion amarilla

    p.rect(11, 12, 13, 20, tono(amarillo, 2))
    p.pset(11, 12, tono(amarillo, 3))
    p.hlinea(11, 13, 20, tono(amarillo, 0))
    # remaches sobre el cuerpo
    for xy in ((9, 15), (16, 15), (19, 18)):
        p.pset(xy[0], xy[1], tono(acero, 3))


def valvula_antirretorno(p):
    """Valvula de antirretorno: cuerpo de bronce con mariposa lateral."""
    laton, acero, hierro, rojo = pal.LATON, pal.STEEL, pal.HIERRO, pal.ROJO
    # cuerpo tipo caldera redondeado
    p.elipse(14, 17, 8, 7, tono(laton, 2), contorno=tono(hierro, 0))
    p.elipse(13, 15, 6, 5, tono(laton, 3))
    p.elipse(14, 17, 4.5, 4, tono(laton, 2))
    # brida superior con vaso
    p.rect(12, 6, 17, 11, tono(laton, 1))
    p.hlinea(12, 17, 6, tono(laton, 4))
    p.hlinea(12, 17, 11, tono(laton, 0))
    # mariposa o palanca lateral
    p.linea(20, 10, 26, 7, tono(acero, 3))
    p.linea(20, 11, 26, 8, tono(acero, 1))
    p.pset(26, 7, tono(acero, 4))
    p.pset(27, 6, tono(rojo, 2))
    # puerto inferior
    p.rect(12, 23, 17, 27, tono(hierro, 2))
    p.hlinea(12, 17, 23, tono(laton, 0))
    p.hlinea(12, 17, 27, tono(hierro, 0))
    p.elipse(14, 27, 1.7, 1, tono(acero, 1))


def bobina_cobre(p):
    """Bobina de cobre: espiral sobre nucleo de acero."""
    laton, acero, carbon, oxido = pal.LATON, pal.STEEL, pal.CARBON, pal.OXIDO
    # nucleo central
    p.rect(13, 5, 18, 27, tono(acero, 1))
    p.hlinea(13, 18, 5, tono(acero, 3))
    p.hlinea(13, 18, 27, tono(hierro, 0) if False else tono(pal.HIERRO, 0))
    # espiras de cobre alrededor
    for y in range(7, 26, 3):
        p.rect(8, y, 23, y + 1, tono(laton, 2))
        p.hlinea(8, 23, y, tono(laton, 3))
        p.hlinea(8, 23, y + 1, tono(laton, 0))
    # extremos del hilo
    p.linea(23, 8, 28, 6, tono(laton, 2))
    p.pset(28, 6, tono(laton, 3))
    p.linea(8, 25, 4, 27, tono(laton, 2))
    p.pset(4, 27, tono(laton, 1))
    # brillo lateral de las espiras
    p.vlinea(9, 8, 24, tono(laton, 3))
    # verde de oxidacion acelerada
    for xy in ((21, 14), (22, 15), (10, 20)):
        p.pset(xy[0], xy[1], tono(pal.SULFATO, 1))


def cableado_alta_tension(p):
    """Cableado de alta tension: haz con malla y terminal seseado."""
    carbon, rojo, amarillo, acero = pal.CARBON, pal.ROJO, pal.AMARILLO, pal.STEEL
    # haz de cables (3 trenzados)
    for (x0, y0, x1, y1, c) in ((3, 27, 21, 5, tono(carbon, 2)),
                                (4, 27, 22, 6, tono(carbon, 1)),
                                (5, 28, 23, 7, tono(carbon, 2))):
        p.linea(x0, y0, x1, y1, c)
    # trenza: cruces oscuras
    for x, y in ((9, 21), (13, 16), (17, 11)):
        p.pset(x, y, tono(carbon, 0))
        p.pset(x + 1, y - 1, tono(carbon, 0))
    # abrazadera central
    for x, y in ((11, 18), (12, 17), (13, 16)):
        pass
    p.rect(10, 15, 14, 20, tono(acero, 2), )
    p.hlinea(10, 14, 15, tono(acero, 4))
    p.hlinea(10, 14, 20, tono(acero, 0))
    # cinta de senales color
    p.rect(16, 10, 17, 15, tono(amarillo, 2))
    p.hlinea(16, 17, 15, tono(amarillo, 0))
    p.rect(19, 6, 20, 11, tono(rojo, 2))
    p.hlinea(19, 20, 11, tono(rojo, 0))
    # terminal de anillo
    p.elipse(24, 4, 3, 3, tono(acero, 3), contorno=tono(acero, 0))
    p.elipse(24, 4, 1.2, 1.2, (0, 0, 0, 0))
    p.pset(22, 6, tono(acero, 1))


def placa_circuito_impreso(p):
    """Placa de circuito impreso: sustrato verde con pistas y chips."""
    verde = pal.OLIVA
    laton, carbon, hierro, rojo = pal.LATON, pal.CARBON, pal.HIERRO, pal.ROJO
    # sustrato con esquinas redondeadas
    p.rect(4, 6, 28, 26, tono(verde, 2))
    p.banda_top(4, 6, 28, 26, tono(verde, 3))
    p.banda_izq(4, 6, 28, 26, tono(verde, 3))
    p.banda_der(4, 6, 28, 26, tono(verde, 1))
    p.banda_bot(4, 6, 28, 26, tono(verde, 0))
    for x, y in ((4, 6), (28, 6), (4, 26), (28, 26)):
        p.pset(x, y, (0, 0, 0, 0))
    # pistas
    p.linea(7, 9, 7, 20, tono(laton, 2))
    p.linea(7, 20, 12, 20, tono(laton, 2))
    p.linea(25, 10, 25, 16, tono(laton, 2))
    p.linea(25, 16, 21, 16, tono(laton, 2))
    p.linea(11, 24, 11, 21, tono(laton, 2))
    # chip central negro
    p.rect(13, 11, 20, 17, tono(carbon, 0))
    p.hlinea(13, 20, 11, tono(carbon, 2))
    p.pset(14, 13, tono(carbon, 3))
    p.pset(15, 13, tono(carbon, 3))
    # patas del chip
    for x in range(14, 20, 2):
        p.pset(x, 10, tono(laton, 3))
        p.pset(x, 18, tono(laton, 3))
    # condensador cilindrico
    cilindro(p, 7, 20, 3, 6, pal.STEEL, cuerpo=2)
    p.pset(8, 21, tono(rojo, 2))
    p.pset(8, 22, tono(rojo, 1))
    # resistance y diodo
    p.rect(22, 19, 26, 21, tono(pal.BEIGE, 1))
    p.hlinea(22, 26, 21, tono(pal.BEIGE, 0))
    p.pset(23, 20, tono(rojo, 2))
    p.pset(25, 20, tono(rojo, 2))
    # taladros de montaje
    for x, y in ((6, 8), (27, 8), (6, 24), (27, 24)):
        p.elipse(x, y, 0.8, 0.8, tono(pal.HIERRO, 0))
        p.pset(x, y, tono(laton, 2))


def condensador_alto_voltaje(p):
    """Condensador de alta tension: Lata con disco ceramico, bornes arriba."""
    acero, hierro, rojo, carbon = pal.STEEL, pal.HIERRO, pal.ROJO, pal.CARBON
    # envolvente
    p.rect(9, 10, 22, 26, tono(acero, 2))
    p.hlinea(9, 22, 10, tono(acero, 4))
    p.hlinea(9, 22, 26, tono(hierro, 0))
    p.vlinea(10, 11, 26, tono(acero, 3))
    # banda de tension roja
    p.rect(9, 14, 22, 16, tono(rojo, 2))
    p.hlinea(9, 22, 14, tono(rojo, 3))
    p.hlinea(9, 22, 16, tono(rojo, 0))
    # rotulo metalico grabado (lineas, no letras)
    p.hlinea(12, 19, 20, tono(hierro, 1))
    p.hlinea(12, 17, 22, tono(hierro, 1))
    # bornes con capsulas
    p.vlinea(12, 6, 10, tono(acero, 3))
    p.elipse(12, 6, 1.6, 1.6, tono(hierro, 3))
    p.vlinea(19, 6, 10, tono(acero, 3))
    p.elipse(19, 6, 1.6, 1.6, tono(hierro, 3))
    p.pset(11, 5, tono(acero, 4))
    p.pset(18, 5, tono(acero, 4))
    # descarga caliente: mancha de chamuscado
    p.pset(20, 25, tono(carbon, 0))
    p.pset(21, 25, tono(carbon, 1))
    p.pset(20, 24, tono(carbon, 1))
    # tornillos de base
    p.pset(10, 26, tono(hierro, 4))
    p.pset(21, 26, tono(hierro, 4))


def motor_paso_a_paso(p):
    """Motor paso a paso: bloque compacto con eje y 'escalonas'Laterales."""
    acero, hierro, carbon, laton = pal.STEEL, pal.HIERRO, pal.CARBON, pal.LATON
    # cuerpo cubico con aletas
    p.rect(7, 11, 24, 26, tono(acero, 2))
    p.hlinea(7, 24, 11, tono(acero, 4))
    p.hlinea(7, 24, 26, tono(hierro, 0))
    for y in (14, 18, 22):
        p.hlinea(7, 24, y, tono(acero, 1))
        p.hlinea(7, 24, y + 1, tono(acero, 3))
    # placa frontal
    p.rect(6, 10, 25, 11, tono(hierro, 2))
    p.hlinea(6, 25, 10, tono(hierro, 3))
    # eje
    p.rect(13, 6, 18, 10, tono(acero, 3))
    p.hlinea(13, 18, 6, tono(acero, 4))
    p.vlinea(14, 6, 10, tono(acero, 5))
    p.vlinea(17, 7, 10, tono(acero, 1))
    p.hlinea(13, 18, 10, tono(acero, 0))
    # pestaña de montaje con orejas
    p.rect(5, 13, 6, 24, tono(hierro, 1))
    p.rect(25, 13, 26, 24, tono(hierro, 1))
    p.pset(5, 16, tono(acero, 4))
    p.pset(26, 16, tono(acero, 4))
    # caja de conexion con latiguillo
    p.rect(19, 8, 24, 10, tono(carbon, 1))
    p.linea(24, 9, 28, 12, tono(carbon, 2))
    p.pset(28, 12, tono(carbon, 0))
    # engranaje saliente
    p.elipse(20, 4, 2, 2, tono(laton, 2), contorno=tono(hierro, 0))


def microprocesador_militar(p):
    """Microprocesador militar: encapsulado ceramico con patas doradas."""
    beige, laton, hierro, carbon, verde = (pal.BEIGE, pal.LATON,
                                           pal.HIERRO, pal.CARBON, pal.OLIVA)
    # encapsulado ceramico
    p.rect(9, 9, 22, 22, tono(beige, 2))
    p.hlinea(9, 22, 9, tono(beige, 3))
    p.hlinea(9, 22, 22, tono(beige, 0))
    p.vlinea(9, 9, 22, tono(beige, 3))
    p.vlinea(22, 9, 22, tono(beige, 1))
    # crystal de silicio central
    p.rect(12, 12, 19, 19, tono(carbon, 1))
    p.pset(13, 13, tono(carbon, 3))
    p.pset(14, 14, tono(carbon, 3))
    p.pset(13, 14, tono(verde, 3))
    # marca de lote grabada
    p.hlinea(12, 19, 21, tono(beige, 1))
    p.vlinea(12, 10, 12, tono(beige, 1))
    # patas doradas en zigzag
    for x in range(10, 23, 2):
        p.pset(x, 7, tono(laton, 2))
        p.pset(x, 8, tono(laton, 3))
        p.pset(x, 23, tono(laton, 2))
        p.pset(x, 24, tono(laton, 3))
    for y in range(10, 23, 2):
        p.pset(7, y, tono(laton, 2))
        p.pset(8, y, tono(laton, 3))
        p.pset(23, y, tono(laton, 2))
        p.pset(24, y, tono(laton, 3))
    # marca de applique militar (triangle roberto)
    p.pset(20, 15, tono(rojo := pal.ROJO, 2))
    p.pset(19, 16, tono(rojo, 1))
    p.pset(20, 16, tono(rojo, 1))


def sensor_dosimetrico(p):
    """Sensor dosimetrico: sonda de lapices con ventana de mica."""
    acero, hierro, carbon, amarillo = (pal.STEEL, pal.HIERRO,
                                       pal.CARBON, pal.AMARILLO)
    # tubo sondas largo
    p.rect(12, 4, 19, 21, tono(acero, 1))
    p.hlinea(12, 19, 4, tono(acero, 3))
    p.hlinea(12, 19, 21, tono(hierro, 0))
    p.vlinea(13, 5, 21, tono(acero, 3))
    # punta
    p.pset(15, 2, tono(acero, 4))
    p.pset(16, 2, tono(acero, 4))
    p.pset(15, 3, tono(acero, 2))
    p.pset(16, 3, tono(acero, 2))
    # ventana de lectura con escala
    p.rect(12, 14, 19, 18, tono(carbon, 0))
    p.pset(13, 15, tono(amarillo, 2))
    p.pset(14, 15, tono(amarillo, 2))
    p.pset(15, 15, tono(amarillo, 3))
    p.pset(18, 15, tono(pal.ROJO, 2))
    # anillo lorena inferior
    p.rect(10, 21, 21, 24, tono(hierro, 2))
    p.hlinea(10, 21, 21, tono(hierro, 3))
    p.hlinea(10, 21, 24, tono(hierro, 0))
    p.pset(11, 22, tono(acero, 4))
    p.pset(20, 22, tono(acero, 4))
    # caratula manchada por uso
    p.pset(14, 10, tono(pal.SULFATO, 1))
    p.pset(17, 12, tono(pal.SULFATO, 0))


def lente_optica_precision(p):
    """Lente de precision: barril con apoide y cristal azul-verdoso."""
    acero, hierro, cristal, carbon = (pal.STEEL, pal.HIERRO,
                                      pal.CRISTAL, pal.CARBON)
    # barril
    p.rect(9, 11, 22, 21, tono(acero, 1))
    p.hlinea(9, 22, 11, tono(acero, 3))
    p.hlinea(9, 22, 21, tono(hierro, 0))
    # anillos del barril (roscas)
    for x in (12, 15, 18):
        p.vlinea(x, 12, 20, tono(hierro, 0))
        p.vlinea(x + 1, 12, 20, tono(acero, 3))
    # cristal frontal
    p.elipse(10, 16, 3, 5, tono(cristal, 1), contorno=tono(hierro, 0))
    p.elipse(9, 16, 1.6, 3.4, tono(cristal, 3))
    p.pset(9, 14, tono(cristal, 5))
    # vivo interior
    p.elipse(21, 16, 2.6, 5, tono(carbon, 0), contorno=tono(hierro, 0))
    p.pset(20, 15, tono(cristal, 2))
    # ojo de montaje y tapa de para-solear
    p.elipse(25, 13, 2, 2, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(25, 13, 0.8, 0.8, (0, 0, 0, 0))
    p.rect(22, 22, 25, 24, tono(hierro, 1))
    p.hlinea(22, 25, 22, tono(hierro, 2))


def filtro_carbon_activado(p):
    """Filtro de carbon activado: lata reja gruesa con malla superior."""
    hierro, acero, carbon, oliva = (pal.HIERRO, pal.STEEL,
                                    pal.CARBON, pal.OLIVA)
    # cuerpo redondeado tipo lata
    p.elipse(16, 19, 8, 10, tono(hierro, 2), contorno=tono(hierro, 0))
    p.elipse(14, 17, 6, 8, tono(acero, 3))
    # malla de entrada (arriba, boca)
    p.elipse(16, 11, 5.5, 3, tono(carbon, 0), contorno=tono(hierro, 3))
    rejilla_puntos(p, 12, 10, 3, 2, 3, tono(hierro, 3))
    # bisagra de correa
    p.rect(23, 15, 26, 18, tono(acero, 1))
    p.hlinea(23, 26, 15, tono(acero, 3))
    p.elipse(24, 16, 0.8, 0.8, (0, 0, 0, 0))
    # banda giratoria (rosca de enroque)
    p.rect(9, 16, 23, 17, tono(hierro, 1))
    p.hlinea(9, 23, 16, tono(hierro, 3))
    p.hlinea(9, 23, 17, tono(hierro, 3)) if False else None
    # rosca de tornillo grabada
    for xy in ((11, 21), (13, 23), (16, 24), (19, 23), (21, 21)):
        p.pset(xy[0], xy[1], tono(hierro, 0))
    # oxido de almacenamiento
    p.pset(11, 24, tono(pal.OXIDO, 1))
    p.pset(12, 25, tono(pal.OXIDO, 2))
    p.pset(20, 25, tono(pal.OXIDO, 1))


def tejido_kevlar_plomado(p):
    """Tejido kevlar plomado: paquete plas de placas con trama."""
    oliva, carbon, amarillo = pal.OLIVA, pal.CARBON, pal.AMARILLO
    # pila de laminas flexibles
    p.rect(6, 18, 25, 27, tono(oliva, 1))
    p.hlinea(6, 25, 18, tono(oliva, 2))
    p.hlinea(6, 25, 27, tono(oliva, 0))
    p.rect(8, 14, 26, 22, tono(oliva, 2))
    p.hlinea(8, 26, 14, tono(oliva, 3))
    p.rect(5, 9, 22, 17, tono(oliva, 3))
    p.hlinea(5, 22, 9, tono(oliva, 4))
    p.hlinea(5, 22, 13, tono(oliva, 2))
    # trama de kevlar (lineas cruzadas)
    for x in range(8, 22, 4):
        p.vlinea(x, 10, 12, tono(oliva, 1))
    for y in (16, 19, 22, 25):
        p.hlinea(7, 25, y, tono(carbon, 0))
    # sello plomado (anguila)
    p.elipse(23, 12, 3.2, 3.2, tono(pal.HIERRO, 2), contorno=tono(pal.HIERRO, 0))
    p.elipse(23, 12, 1.4, 1.4, tono(pal.HIERRO, 4))
    # cinta de identificacion amarilla
    p.pset(9, 26, tono(amarillo, 2))
    p.pset(10, 26, tono(amarillo, 2))
    p.pset(11, 26, tono(amarillo, 1))


def celda_litio_militar(p):
    """Celda de litio militar: cilindro grueso con borne y banda."""
    amarillo, acero, hierro, carbon, rojo = (pal.AMARILLO, pal.STEEL,
                                            pal.HIERRO, pal.CARBON, pal.ROJO)
    # cuerpo
    cilindro(p, 11, 8, 10, 20, acero, cuerpo=2)
    # envoltura con banda amarilla superior
    p.rect(11, 12, 20, 14, tono(amarillo, 2))
    p.hlinea(11, 20, 12, tono(amarillo, 3))
    p.hlinea(11, 20, 14, tono(amarillo, 0))
    # banda roja de aviso
    p.rect(11, 19, 20, 20, tono(rojo, 2))
    p.hlinea(11, 20, 19, tono(rojo, 3))
    p.pset(11, 20, tono(rojo, 0))
    p.pset(20, 20, tono(rojo, 0))
    # borne
    p.rect(14, 5, 17, 8, tono(acero, 4))
    p.hlinea(14, 17, 5, tono(acero, 5))
    p.elipse(15, 5, 1.5, 1, tono(hierro, 3))
    # rotulo grabado
    p.hlinea(13, 18, 23, tono(hierro, 1))
    p.hlinea(13, 16, 25, tono(hierro, 1))
    # code punta plastica
    p.pset(12, 26, tono(carbon, 1))
    p.pset(19, 26, tono(carbon, 1))


def nucleo_plomo_sellado(p):
    """NuCore de plomo sellado: bloque gris denso con banda de radiacion."""
    acero, hierro, carbon, amarillo, rojo = (pal.STEEL, pal.HIERRO,
                                            pal.CARBON, pal.AMARILLO,
                                            pal.ROJO)
    # bloque cubico denso
    p.poligono([(5, 22), (10, 12), (22, 12), (27, 22)], tono(acero, 1))
    p.poligono([(10, 12), (22, 12), (24, 15), (8, 15)], tono(acero, 3))
    p.poligono([(24, 15), (27, 22), (24, 22), (25, 15)], tono(acero, 0))
    p.hlinea(5, 27, 22, tono(hierro, 0))
    # banda de radiacion (trifolio en amarillo)
    p.rect(8, 16, 24, 20, tono(amarillo, 2))
    p.hlinea(8, 24, 16, tono(amarillo, 3))
    p.hlinea(8, 24, 20, tono(amarillo, 0))
    # trefoil simplificado de 3 sectores
    for grados in (90, 210, 330):
        a = math.radians(grados)
        p.elipse(16 + 2.6 * math.cos(a), 18 + 2.6 * math.sin(a),
                 1.2, 1.2, tono(carbon, 0))
    p.pset(16, 18, tono(carbon, 0))
    # sello de seguridad con plomo (cosa: gota)
    p.elipse(16, 24, 2.6, 2, tono(acero, 3), contorno=tono(hierro, 0))
    p.linea(14, 24, 18, 24, tono(hierro, 1))
    # marcas de moldeo en la cara superior
    p.linea(11, 13, 15, 13, tono(acero, 4))
    p.linea(18, 13, 21, 13, tono(acero, 4))


DIBUJOS = {
    "tela": tela,
    "scrap": scrap,
    "lingote_pesado": lingote_pesado,
    "engranaje_titanio": engranaje_titanio,
    "piston_hidraulico": piston_hidraulico,
    "tubo_presion": tubo_presion,
    "valvula_antirretorno": valvula_antirretorno,
    "bobina_cobre": bobina_cobre,
    "cableado_alta_tension": cableado_alta_tension,
    "placa_circuito_impreso": placa_circuito_impreso,
    "condensador_alto_voltaje": condensador_alto_voltaje,
    "motor_paso_a_paso": motor_paso_a_paso,
    "microprocesador_militar": microprocesador_militar,
    "sensor_dosimetrico": sensor_dosimetrico,
    "lente_optica_precision": lente_optica_precision,
    "filtro_carbon_activado": filtro_carbon_activado,
    "tejido_kevlar_plomado": tejido_kevlar_plomado,
    "celda_litio_militar": celda_litio_militar,
    "nucleo_plomo_sellado": nucleo_plomo_sellado,
}
