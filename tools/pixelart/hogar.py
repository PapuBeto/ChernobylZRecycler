# -*- coding: utf-8 -*-
"""Objetos domesticos y vestimenta: pixel art 32x32."""
from __future__ import annotations

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import cilindro, rejilla_lineas


def abrigo_afghanka(p):
    """Abrigo Afghanka: guerrera oliva con cuello, bolsillos y cinturon."""
    oliva, carbon, hierro = pal.OLIVA, pal.CARBON, pal.HIERRO
    # cuerpo
    p.poligono([(7, 15), (11, 11), (21, 11), (25, 15), (25, 28), (7, 28)],
               tono(oliva, 2))
    p.hlinea(7, 25, 28, tono(oliva, 0))
    # cuello alzado
    p.rect(12, 8, 20, 11, tono(oliva, 3))
    p.hlinea(12, 20, 8, tono(oliva, 4))
    # cierre con cremallera
    p.vlinea(16, 11, 28, tono(carbon, 0))
    p.vlinea(17, 11, 28, tono(oliva, 3))
    # bolsillos con solapa
    p.rect(9, 18, 15, 23, tono(oliva, 1))
    p.hlinea(9, 15, 18, tono(oliva, 0))
    p.rect(17, 18, 23, 23, tono(oliva, 1))
    p.hlinea(17, 23, 18, tono(oliva, 0))
    p.pset(11, 20, tono(carbon, 0))
    p.pset(21, 20, tono(carbon, 0))
    # mangas
    p.rect(3, 16, 8, 26, tono(oliva, 2))
    p.hlinea(3, 8, 16, tono(oliva, 3))
    p.rect(24, 16, 29, 26, tono(oliva, 2))
    p.hlinea(24, 29, 16, tono(oliva, 3))
    p.hlinea(3, 8, 26, tono(oliva, 0))
    p.hlinea(24, 29, 26, tono(oliva, 0))
    # cinturon
    p.hlinea(7, 25, 27, tono(carbon, 1))
    p.rect(15, 26, 17, 28, tono(hierro, 3))
    # parche de hombrera
    p.pset(9, 13, tono(carbon, 1))
    p.pset(22, 13, tono(carbon, 1))
    # polvo de afganistan
    p.pset(11, 25, tono(pal.BEIGE, 1))
    p.pset(20, 24, tono(pal.OXIDO, 1))


def microondas_dnepr(p):
    """Microondas Dnepr: carcasa de chapa con puerta blindada y panel."""
    beige, carbon, hierro, cristal = (pal.BEIGE, pal.CARBON, pal.HIERRO,
                                      pal.CRISTAL)
    # carcasa
    p.rect(3, 8, 28, 25, tono(beige, 2))
    p.hlinea(3, 28, 8, tono(beige, 3))
    p.hlinea(3, 28, 25, tono(beige, 0))
    p.vlinea(3, 8, 25, tono(beige, 3))
    # puerta con ventana
    p.rect(5, 10, 20, 23, tono(beige, 1))
    p.hlinea(5, 20, 10, tono(beige, 0))
    p.rect(8, 12, 17, 21, tono(carbon, 0))
    p.rect(9, 13, 16, 20, tono(cristal, 0))
    p.hlinea(9, 16, 14, tono(cristal, 1))
    p.pset(10, 14, tono(cristal, 2))
    # rejilla de ventilacion de la puerta
    rejilla_lineas(p, 6, 18, 7, 22, tono(beige, 0), tono(carbon, 0), 2)
    # panel de control
    p.rect(22, 10, 26, 23, tono(hierro, 1))
    p.hlinea(22, 26, 10, tono(hierro, 2))
    p.elipse(24, 12, 1.6, 1.6, tono(hierro, 4), contorno=tono(carbon, 0))
    p.pset(24, 17, tono(pal.ROJO, 2))
    p.rect(23, 19, 25, 21, tono(carbon, 1))
    # marcas de quemado en la esquina
    p.pset(25, 24, tono(carbon, 0))
    p.pset(24, 24, tono(carbon, 1))
    p.pset(26, 23, tono(carbon, 1))
    # placa oxidada
    p.pset(6, 24, tono(pal.OXIDO, 1))
    p.pset(7, 24, tono(pal.OXIDO, 2))


def lavadora_vyatka(p):
    """Lavadora Vyatka: cilindro con panel, perilla y ventana de tambor."""
    blanco, acero, hierro, carbon, cristal = (pal.BEIGE, pal.STEEL,
                                              pal.HIERRO, pal.CARBON,
                                              pal.CRISTAL)
    # cuerpo cilindrico
    p.rect(7, 7, 24, 26, tono(blanco, 2))
    p.hlinea(7, 24, 7, tono(blanco, 3))
    p.hlinea(7, 24, 26, tono(hierro, 0))
    p.vlinea(8, 8, 26, tono(blanco, 3))
    p.vlinea(24, 8, 26, tono(hierro, 1))
    # tapa con bisagras
    p.rect(6, 5, 25, 8, tono(blanco, 3))
    p.hlinea(6, 25, 5, tono(blanco, 4))
    p.hlinea(6, 25, 8, tono(blanco, 1))
    p.pset(7, 6, tono(hierro, 3))
    p.pset(24, 6, tono(hierro, 3))
    # perilla giratoria
    p.elipse(11, 13, 1.8, 1.8, tono(hierro, 2), contorno=tono(carbon, 0))
    p.pset(10, 12, tono(hierro, 4))
    p.pset(12, 14, tono(carbon, 0))
    # ventana del tambor
    p.elipse(19, 13, 4.4, 4.4, tono(carbon, 0), contorno=tono(hierro, 1))
    p.elipse(19, 13, 2.8, 2.8, tono(cristal, 0))
    p.pset(17, 11, tono(cristal, 2))
    p.pset(18, 11, tono(cristal, 3))
    p.hlinea(17, 21, 17, tono(cristal, 1))
    # botoneria
    rejilla_lineas(p, 10, 20, 22, 23, tono(blanco, 1), tono(blanco, 0), 4)
    p.pset(11, 20, tono(pal.ROJO, 2))
    p.pset(19, 20, tono(pal.SULFATO, 2))
    # pie de goma antivibracion
    p.pset(9, 27, tono(carbon, 1))
    p.pset(22, 27, tono(carbon, 1))
    # decoloracion de uso
    p.pset(10, 24, tono(pal.OXIDO, 1))
    p.pset(23, 25, tono(pal.OXIDO, 2))


def maquina_coser_podolsk(p):
    """Maquina de coser Podolsk: columna negra con volante y aguja."""
    carbon, hierro, laton, madera, polvo = (pal.CARBON, pal.HIERRO,
                                            pal.LATON, pal.MADERA,
                                            pal.BEIGE)
    # mesa base de madera
    p.rect(3, 22, 28, 27, tono(madera, 2))
    p.hlinea(3, 28, 22, tono(madera, 3))
    p.hlinea(3, 28, 27, tono(madera, 0))
    # cuerpo negro (columna y brazo)
    p.rect(8, 8, 22, 22, tono(carbon, 1))
    p.hlinea(8, 22, 8, tono(carbon, 2))
    p.hlinea(8, 22, 22, tono(carbon, 0))
    p.rect(22, 6, 27, 14, tono(carbon, 1))
    p.hlinea(22, 27, 6, tono(carbon, 2))
    # volante dorado
    p.elipse(27, 9, 3, 3, tono(laton, 2), contorno=tono(carbon, 0))
    p.elipse(26, 8, 1.4, 1.4, tono(laton, 4))
    p.elipse(27, 9, 1, 1, tono(carbon, 0))
    # aguja y placa
    p.vlinea(14, 14, 22, tono(hierro, 3))
    p.pset(14, 13, tono(hierro, 4))
    p.rect(10, 20, 18, 22, tono(hierro, 2))
    # caballetes decorados (adorno dorado de linea)
    p.linea(10, 12, 16, 12, tono(laton, 2))
    p.linea(10, 13, 16, 13, tono(laton, 1))
    # piñones de cadena
    p.pset(20, 19, tono(hierro, 4))
    p.pset(21, 20, tono(hierro, 3))
    # tela roja en la aguja
    p.rect(9, 23, 17, 25, tono(pal.ROJO, 1))
    p.hlinea(9, 17, 23, tono(pal.ROJO, 2))
    p.pset(11, 24, tono(pal.ROJO, 0))
    # polvo depositado
    p.pset(10, 7, tono(polvo, 1))
    p.pset(24, 16, tono(polvo, 0))


def aspiradora_raketa(p):
    """Aspiradora Raketa: lata de chapa con manguera y boquilla."""
    acero, hierro, carbon, beige = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.BEIGE)
    # cuerpo lata
    p.rect(6, 10, 22, 26, tono(acero, 2))
    p.hlinea(6, 22, 10, tono(acero, 3))
    p.hlinea(6, 22, 26, tono(hierro, 0))
    p.vlinea(8, 11, 26, tono(acero, 5))
    # tapa con muelle
    p.rect(5, 7, 23, 10, tono(hierro, 2))
    p.hlinea(5, 23, 7, tono(hierro, 3))
    p.hlinea(5, 23, 10, tono(hierro, 0))
    p.pset(8, 8, tono(acero, 4))
    p.pset(20, 8, tono(acero, 4))
    # manguera corrugada (sale arriba, baja en S)
    for x, y in ((24, 9), (25, 10), (26, 11), (26, 12), (26, 13), (25, 14),
                 (24, 15), (24, 16), (25, 17), (27, 18), (29, 19), (30, 20)):
        p.pset(x, y, tono(carbon, 2))
    # boquilla
    p.rect(29, 20, 32, 22, tono(carbon, 1))
    p.pset(30, 22, tono(carbon, 0))
    # rejilla de escape
    rejilla_lineas(p, 9, 13, 19, 15, tono(acero, 1), tono(carbon, 0), 2)
    # etiqueta de marca
    p.rect(9, 18, 14, 24, tono(beige, 1))
    p.hlinea(9, 14, 18, tono(beige, 2))
    p.hlinea(9, 14, 24, tono(beige, 0))
    # leva de rodamiento
    p.pset(20, 22, tono(hierro, 4))
    # polvo en la base
    p.pset(10, 27, tono(pal.BEIGE, 1))
    p.pset(21, 27, tono(pal.BEIGE, 0))


def gorro_ushanka(p):
    """Ushanka: gorro de piel con orejeras abiertas y visera."""
    arena = pal.BEIGE
    madera, carbon, rojo = pal.MADERA, pal.CARBON, pal.ROJO
    # copa
    p.poligono([(7, 12), (10, 6), (23, 6), (26, 12), (25, 17), (8, 17)],
               tono(arena, 2))
    p.hlinea(10, 23, 6, tono(arena, 3))
    # faja de piel (borde)
    p.rect(5, 17, 28, 21, tono(arena, 1))
    p.hlinea(5, 28, 17, tono(arena, 2))
    p.hlinea(5, 28, 21, tono(arena, 0))
    # veta de piel
    for x in range(7, 27, 3):
        p.pset(x, 19, tono(arena, 3))
        p.pset(x + 1, 20, tono(arena, 0))
    # orejeras caidas
    p.rect(3, 19, 8, 27, tono(arena, 1))
    p.hlinea(3, 8, 19, tono(arena, 2))
    p.rect(25, 19, 30, 27, tono(arena, 1))
    p.hlinea(25, 30, 19, tono(arena, 2))
    for y in (21, 24):
        p.pset(5, y, tono(arena, 0))
        p.pset(27, y, tono(arena, 0))
    # cordones atados
    p.linea(8, 25, 12, 27, tono(carbon, 1))
    p.linea(25, 25, 21, 27, tono(carbon, 1))
    # insignia roja
    p.rect(14, 12, 18, 15, tono(rojo, 2))
    p.hlinea(14, 18, 12, tono(rojo, 3))
    p.hlinea(14, 18, 15, tono(rojo, 0))
    p.pset(16, 13, tono(rojo, 4))
    # pelo revuelto en la copa
    p.pset(12, 8, tono(arena, 3))
    p.pset(20, 7, tono(arena, 3))
    p.pset(17, 9, tono(arena, 0))


def vaqueros_rasgados(p):
    """Vaqueros rasgados: perniles con rotura y bolsillos."""
    jeans = pal.OLIVA
    carbon, hierro, oxido = pal.CARBON, pal.HIERRO, pal.OXIDO
    # perna izquierda
    p.poligono([(5, 6), (15, 6), (13, 28), (4, 28)], tono(jeans, 1))
    p.hlinea(5, 15, 6, tono(jeans, 2))
    p.hlinea(4, 13, 28, tono(jeans, 0))
    # perna derecha
    p.poligono([(17, 6), (27, 6), (28, 28), (19, 28)], tono(jeans, 2))
    p.hlinea(17, 27, 6, tono(jeans, 3))
    p.hlinea(19, 28, 28, tono(jeans, 0))
    # entrepierna
    p.vlinea(16, 10, 28, tono(jeans, 0))
    # costuras
    for y in range(8, 28, 3):
        p.pset(4, y, tono(pal.AMARILLO, 2))
        p.pset(19, y, tono(pal.AMARILLO, 2))
    # bolsillos
    p.linea(6, 9, 10, 6, tono(jeans, 0))
    p.linea(25, 9, 21, 6, tono(jeans, 0))
    # roturas (la piel asoma)
    p.rect(9, 16, 12, 18, tono(carbon, 0))
    p.pset(10, 15, tono(carbon, 1))
    p.pset(23, 20, tono(carbon, 0))
    p.pset(24, 21, tono(carbon, 1))
    # desflecado
    for y in (19, 22):
        p.vlinea(9, y, y, tono(carbon, 1))
    # remache de cobre
    p.pset(6, 10, tono(pal.LATON, 3))
    p.pset(26, 10, tono(pal.LATON, 3))
    # felpilla de desgaste
    p.pset(11, 12, tono(jeans, 2))
    p.pset(22, 14, tono(jeans, 3))


def alfombra_persa(p):
    """Alfombra persa enrollada parcialmente con franjas de urdimbre."""
    rojo, carbon, laton, madera = pal.ROJO, pal.CARBON, pal.LATON, pal.MADERA
    # fardo enrollado
    p.elipse(10, 17, 7, 9, tono(madera, 1), contorno=tono(carbon, 0))
    p.elipse(8, 15, 5, 7, tono(madera, 2))
    p.elipse(9, 17, 2.4, 2.4, tono(carbon, 0))
    p.pset(8, 15, tono(carbon, 2))
    # tapete extendido
    p.poligono([(15, 9), (28, 12), (29, 26), (13, 28)], tono(rojo, 1))
    # primera franja del tapete
    p.linea(16, 12, 28, 13, tono(carbon, 0))
    p.linea(14, 20, 29, 21, tono(carbon, 0))
    p.linea(14, 25, 29, 26, tono(laton, 2))
    # medallon central
    p.elipse(21, 18, 4, 3, tono(laton, 2), contorno=tono(carbon, 0))
    p.elipse(21, 18, 1.6, 1.6, tono(carbon, 0))
    # rombos de borde
    for x, y in ((18, 15), (25, 16)):
        p.pset(x, y, tono(laton, 3))
    # borlas del tapete
    p.linea(14, 27, 11, 30, tono(madera, 1))
    p.linea(29, 27, 31, 30, tono(madera, 1))
    p.pset(10, 30, tono(madera, 0))
    p.pset(31, 30, tono(madera, 0))
    # taza de polvo
    p.pset(24, 23, tono(pal.BEIGE, 1))


def muneca_irradiada(p):
    """Muneca irradiada: muneco de trapo con hilachas y manchas."""
    beige, rojo, carbon, madera = pal.BEIGE, pal.ROJO, pal.CARBON, pal.MADERA
    # cabeza cosida
    p.elipse(17, 8, 4.4, 4.4, tono(beige, 2), contorno=tono(carbon, 0))
    p.elipse(16, 7, 3, 3, tono(beige, 3))
    # ojillos (botones de fieltro)
    p.pset(15, 8, tono(carbon, 0))
    p.pset(19, 8, tono(carbon, 0))
    p.pset(17, 10, tono(rojo, 2))          # boquita cosida
    # pelo de hilachas
    for x, y in ((14, 4), (16, 3), (18, 3), (20, 4), (22, 5)):
        p.pset(x, y, tono(madera, 1))
    p.pset(13, 5, tono(madera, 0))
    # cuerpo de trapo
    p.poligono([(13, 12), (21, 12), (22, 21), (12, 21)], tono(rojo, 1))
    p.hlinea(13, 21, 12, tono(rojo, 2))
    p.hlinea(12, 22, 21, tono(rojo, 0))
    # brazos de retales
    p.rect(9, 13, 12, 16, tono(rojo, 1))
    p.rect(22, 13, 25, 16, tono(rojo, 1))
    p.hlinea(9, 12, 13, tono(rojo, 2))
    p.hlinea(22, 25, 13, tono(rojo, 2))
    # piernas descolgadas
    p.rect(13, 21, 15, 29, tono(madera, 1))
    p.rect(19, 21, 21, 29, tono(madera, 1))
    p.hlinea(13, 15, 29, tono(madera, 0))
    p.hlinea(19, 21, 29, tono(madera, 0))
    # parche de remiendo
    p.rect(15, 16, 18, 19, tono(beige, 1))
    p.hlinea(15, 18, 16, tono(beige, 0))
    # quemadura de radiacion en la cara
    p.pset(18, 6, tono(pal.OXIDO, 2))
    p.pset(19, 7, tono(pal.ROJO, 1))
    p.pset(18, 11, tono(pal.ROJO, 1))
    # costura abierta (relleno saliendo)
    p.linea(21, 14, 21, 18, tono(carbon, 0))
    p.pset(22, 13, tono(beige, 4))


def taza_peltre(p):
    """Taza de peltre: lata con asa, labio y viruta de desgaste."""
    acero, hierro, carbon, rojo = pal.STEEL, pal.HIERRO, pal.CARBON, pal.ROJO
    # cuerpo
    p.rect(7, 9, 21, 25, tono(acero, 2))
    p.hlinea(7, 21, 9, tono(acero, 3))
    p.hlinea(7, 21, 25, tono(hierro, 0))
    p.vlinea(9, 10, 25, tono(acero, 5))
    # labio reforzado
    p.rect(6, 7, 22, 9, tono(acero, 3))
    p.hlinea(6, 22, 7, tono(acero, 4))
    p.hlinea(6, 22, 9, tono(hierro, 1))
    # asa
    p.elipse(24, 15, 2.6, 3.4, tono(acero, 1), contorno=tono(hierro, 0))
    p.elipse(24, 15, 1, 1.8, (0, 0, 0, 0))
    # mancha de te derramado
    madera = pal.MADERA
    p.rect(8, 7, 13, 9, tono(madera, 1))
    p.linea(9, 7, 12, 9, tono(madera, 0))
    # abolladura
    p.pset(18, 14, tono(hierro, 1))
    p.pset(17, 15, tono(hierro, 3))
    p.pset(19, 15, tono(acero, 1))
    # banda de esmalte quemado
    p.rect(7, 21, 21, 22, tono(carbon, 1))
    p.hlinea(7, 21, 21, tono(carbon, 2))
    # muesca de viruta en el labio
    p.pset(12, 7, tono(hierro, 0))
    p.pset(12, 8, tono(acero, 0))
    # fondo con sarro
    p.hlinea(8, 20, 25, tono(pal.SULFATO, 0))


def olla_presion(p):
    """Olla a presion: caldera con tapa manometro, valvula y asas."""
    acero, hierro, carbon, rojo = pal.STEEL, pal.HIERRO, pal.CARBON, pal.ROJO
    # caldera
    p.rect(6, 10, 24, 26, tono(acero, 2))
    p.hlinea(6, 24, 10, tono(acero, 4))
    p.hlinea(6, 24, 26, tono(hierro, 0))
    p.vlinea(9, 11, 26, tono(acero, 5))
    # tapa hermetica con banda
    p.rect(5, 7, 25, 10, tono(acero, 3))
    p.hlinea(5, 25, 7, tono(acero, 4))
    p.hlinea(5, 25, 10, tono(hierro, 1))
    # valvula de contrapeso
    p.rect(13, 3, 17, 7, tono(hierro, 2))
    p.hlinea(13, 17, 3, tono(hierro, 3))
    p.hlinea(13, 17, 7, tono(hierro, 0))
    p.pset(15, 5, tono(carbon, 0))
    # manometro lateral
    p.elipse(21, 8, 2, 2, tono(hierro, 3), contorno=tono(carbon, 0))
    p.linea(20, 8, 21, 7, tono(carbon, 0))
    # asa termica
    p.rect(25, 13, 29, 15, tono(carbon, 1))
    p.hlinea(25, 29, 13, tono(carbon, 2))
    p.pset(28, 14, tono(acero, 4))
    # asa izquierda
    p.rect(2, 13, 6, 15, tono(carbon, 1))
    p.hlinea(2, 6, 13, tono(carbon, 2))
    # perilla de cierre en la tapa
    p.rect(4, 8, 6, 10, tono(hierro, 1))
    p.rect(24, 8, 26, 10, tono(hierro, 1))
    # vapor
    p.pset(15, 2, tono(pal.BEIGE, 3))
    p.pset(15, 1, tono(pal.BEIGE, 2))
    # mancha de fogata
    p.pset(11, 26, tono(carbon, 0))
    p.pset(18, 26, tono(carbon, 0))


def radiador_hierro(p):
    """Radiador de hierro: columnas con pies y tapones."""
    hierro, acero, oxido, carbon = (pal.HIERRO, pal.STEEL, pal.OXIDO,
                                    pal.CARBON)
    # columnas de aluminio fundido
    for k, x0 in enumerate((4, 9, 14, 19)):
        p.rect(x0, 6, x0 + 3, 25, tono(hierro, 2))
        p.vlinea(x0, 7, 25, tono(hierro, 3))
        p.vlinea(x0 + 3, 7, 25, tono(hierro, 0))
        p.hlinea(x0, x0 + 3, 6, tono(hierro, 4))
        p.hlinea(x0, x0 + 3, 25, tono(hierro, 0))
        # nervadura horizontal central
        p.hlinea(x0 + 1, x0 + 2, 15, tono(hierro, 1))
    # aletas acanaladas
    p.hlinea(4, 22, 10, tono(hierro, 3))
    p.hlinea(4, 22, 20, tono(hierro, 3))
    # tapones
    p.rect(2, 9, 4, 12, tono(acero, 3))
    p.rect(23, 9, 26, 12, tono(acero, 3))
    p.hlinea(23, 26, 9, tono(acero, 4))
    p.pset(3, 10, tono(acero, 5))
    p.pset(24, 10, tono(acero, 5))
    # pies
    p.rect(4, 26, 8, 29, tono(hierro, 1))
    p.rect(19, 26, 23, 29, tono(hierro, 1))
    p.hlinea(4, 8, 29, tono(carbon, 0))
    p.hlinea(19, 23, 29, tono(carbon, 0))
    # purga con mancha de pintura
    p.pset(22, 12, tono(pal.AMARILLO, 2))
    p.pset(23, 12, tono(pal.AMARILLO, 3))
    # goteo de oxido en las columnas
    for x, y in ((6, 22), (11, 23), (16, 22), (21, 24)):
        p.pset(x, y, tono(oxido, 2))
        p.pset(x, y + 1, tono(oxido, 1))


def botas_goma_descontaminantes(p):
    """Botas de goma: borceguis negros con puntera y suela estriada."""
    carbon, hierro, acero = pal.CARBON, pal.HIERRO, pal.STEEL
    # bota trasera
    p.poligono([(4, 12), (12, 12), (13, 22), (3, 22)], tono(carbon, 1))
    p.hlinea(4, 12, 12, tono(carbon, 2))
    p.rect(3, 22, 13, 27, tono(carbon, 1))
    p.hlinea(3, 13, 22, tono(carbon, 2))
    p.hlinea(3, 13, 27, tono(hierro, 0))
    # recorte de caña
    p.vlinea(8, 13, 20, tono(carbon, 0))
    # bota delantera
    p.poligono([(17, 14), (25, 14), (27, 22), (25, 24), (15, 24), (14, 19)],
               tono(carbon, 2))
    p.hlinea(17, 25, 14, tono(carbon, 3))
    p.rect(15, 22, 28, 27, tono(carbon, 1))
    p.hlinea(15, 28, 22, tono(carbon, 2))
    p.hlinea(15, 28, 27, tono(hierro, 0))
    # suelas estriadas
    for x in range(4, 12, 2):
        p.pset(x, 28, tono(hierro, 2))
    for x in range(16, 27, 2):
        p.pset(x, 28, tono(hierro, 2))
    # rebordes de goma
    for y in (16, 19):
        p.hlinea(5, 11, y, tono(carbon, 0))
        p.hlinea(17, 24, y + 2, tono(carbon, 0))
    # mancha de quimico residuo
    p.pset(20, 20, tono(pal.SULFATO, 1))
    p.pset(21, 21, tono(pal.SULFATO, 0))
    # grieta de ozono
    p.pset(10, 18, tono(hierro, 1))
    p.pset(11, 19, tono(hierro, 0))


def cubiertos_acero(p):
    """Cubiertos de acero: tenedor, cuchara y cuchillo en paralelo."""
    acero, hierro, carbon = pal.STEEL, pal.HIERRO, pal.CARBON
    # tenedor
    p.rect(6, 6, 7, 13, tono(acero, 2))
    for x in (5, 6, 7, 8):
        p.vlinea(x, 4, 5, tono(acero, 3))
        p.pset(x, 3, tono(acero, 4))
    p.vlinea(6, 5, 24, tono(acero, 3))
    p.vlinea(7, 5, 24, tono(acero, 1))
    p.rect(5, 25, 8, 28, tono(acero, 2))
    p.hlinea(5, 8, 25, tono(acero, 3))
    # cuchara
    p.elipse(16, 6, 2.4, 2.6, tono(acero, 3), contorno=tono(hierro, 0))
    p.pset(15, 5, tono(acero, 4))
    p.vlinea(16, 9, 27, tono(acero, 3))
    p.vlinea(17, 9, 27, tono(acero, 1))
    p.rect(15, 25, 18, 28, tono(acero, 2))
    p.hlinea(15, 18, 25, tono(acero, 3))
    # cuchillo
    p.poligono([(23, 4), (28, 6), (28, 14), (24, 14)], tono(acero, 3))
    p.pset(27, 5, tono(acero, 4))
    p.linea(24, 5, 27, 13, tono(acero, 1))
    p.vlinea(25, 14, 27, tono(hierro, 1))
    p.vlinea(26, 14, 27, tono(hierro, 0))
    p.rect(24, 25, 27, 28, tono(carbon, 1))
    p.hlinea(24, 27, 25, tono(carbon, 2))
    # reflejos
    p.pset(7, 10, tono(acero, 5))
    p.pset(16, 12, tono(acero, 5))
    # manchita de grasa
    p.pset(6, 24, tono(pal.OXIDO, 0))
    p.pset(16, 24, tono(pal.OXIDO, 1))


DIBUJOS = {
    "abrigo_afghanka": abrigo_afghanka,
    "microondas_dnepr": microondas_dnepr,
    "lavadora_vyatka": lavadora_vyatka,
    "maquina_coser_podolsk": maquina_coser_podolsk,
    "aspiradora_raketa": aspiradora_raketa,
    "gorro_ushanka": gorro_ushanka,
    "vaqueros_rasgados": vaqueros_rasgados,
    "alfombra_persa": alfombra_persa,
    "muneca_irradiada": muneca_irradiada,
    "taza_peltre": taza_peltre,
    "olla_presion": olla_presion,
    "radiador_hierro": radiador_hierro,
    "botas_goma_descontaminantes": botas_goma_descontaminantes,
    "cubiertos_acero": cubiertos_acero,
}
