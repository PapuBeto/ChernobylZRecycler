# -*- coding: utf-8 -*-
"""Maquinaria industrial de la Zona: pixel art 32x32."""
from __future__ import annotations

import math

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import (cara, cilindro, pernos_esquinas,
                                   rejilla_lineas, rejilla_puntos,
                                   terminal)


def taladro_percutor_mina(p):
    """Taladro percutor de mina: cuerpo con asa, morro de mandril y broca."""
    oliva, acero, hierro, carbon, amarillo = (pal.OLIVA, pal.STEEL,
                                             pal.HIERRO, pal.CARBON,
                                             pal.AMARILLO)
    # cuerpo diagonal
    p.poligono([(5, 12), (20, 7), (26, 15), (11, 21)], tono(oliva, 2))
    p.poligono([(5, 12), (11, 10), (16, 13), (10, 16)], tono(oliva, 3))
    p.poligono([(19, 8), (26, 15), (25, 18), (18, 11)], tono(oliva, 1))
    # asa con gatillo
    p.rect(9, 19, 13, 27, tono(carbon, 1))
    p.hlinea(9, 13, 19, tono(carbon, 2))
    p.pset(11, 21, tono(amarillo, 2))
    p.pset(12, 21, tono(amarillo, 1))
    # mandril
    p.rect(24, 13, 28, 19, tono(acero, 2))
    p.hlinea(24, 28, 13, tono(acero, 4))
    p.hlinea(24, 28, 19, tono(hierro, 0))
    for y in (14, 17):
        p.hlinea(24, 28, y, tono(hierro, 1))
    # broca helicoidal
    p.pset(29, 14, tono(acero, 4))
    p.pset(30, 16, tono(acero, 3))
    p.pset(29, 18, tono(acero, 4))
    p.pset(30, 20, tono(acero, 3))
    p.vlinea(29, 14, 21, tono(acero, 1))
    # carceleta de cable trasera
    p.linea(6, 15, 2, 18, tono(carbon, 2))
    p.pset(2, 18, tono(carbon, 0))
    p.pset(1, 19, tono(carbon, 0))
    # oxido de cantera
    p.pset(8, 18, tono(pal.OXIDO, 1))
    p.pset(20, 16, tono(pal.OXIDO, 2))


def compresor_aire_fabrica(p):
    """Compresor de fabrica: deposito horizontal con motor y manometro."""
    acero, hierro, oliva, amarillo, carbon = (pal.STEEL, pal.HIERRO,
                                             pal.OLIVA, pal.AMARILLO,
                                             pal.CARBON)
    # deposito
    p.rect(5, 12, 26, 22, tono(acero, 1))
    p.hlinea(5, 26, 12, tono(acero, 3))
    p.hlinea(5, 26, 22, tono(hierro, 0))
    p.elipse(26, 17, 2.4, 5, tono(acero, 2), contorno=tono(hierro, 0))
    # banda de limpieza de obra
    p.rect(12, 12, 16, 22, tono(amarillo, 2))
    p.hlinea(12, 16, 12, tono(amarillo, 3))
    p.hlinea(12, 16, 22, tono(amarillo, 0))
    # motor encima
    p.rect(7, 5, 17, 11, tono(oliva, 2))
    p.hlinea(7, 17, 5, tono(oliva, 3))
    p.hlinea(7, 17, 11, tono(oliva, 1))
    rejilla_lineas(p, 9, 6, 15, 10, tono(oliva, 1), tono(oliva, 0), 3)
    # manometro
    p.elipse(21, 8, 2.4, 2.4, tono(acero, 3), contorno=tono(hierro, 0))
    p.pset(21, 8, tono(carbon, 0))
    p.pset(20, 7, tono(hierro, 3))
    # tuberia descendente
    p.vlinea(24, 9, 12, tono(acero, 2))
    p.vlinea(25, 9, 12, tono(acero, 0))
    # pies
    p.rect(6, 23, 9, 26, tono(hierro, 1))
    p.rect(22, 23, 25, 26, tono(hierro, 1))
    p.hlinea(6, 9, 26, tono(hierro, 0))
    p.hlinea(22, 25, 26, tono(hierro, 0))
    # oxido
    p.pset(9, 20, tono(pal.OXIDO, 1))
    p.pset(19, 21, tono(pal.OXIDO, 2))


def bomba_hidraulica_refrigeracion(p):
    """Bomba hidraulica: bloque con camisa, bridas de tuberia y mtoro."""
    hierro, acero, oliva, amarillo = (pal.HIERRO, pal.STEEL, pal.OLIVA,
                                      pal.AMARILLO)
    # bloque principal
    p.rect(6, 8, 20, 24, tono(oliva, 2))
    p.hlinea(6, 20, 8, tono(oliva, 3))
    p.hlinea(6, 20, 24, tono(oliva, 0))
    for y in (11, 15, 19):
        p.hlinea(6, 20, y, tono(oliva, 1))
    pernos_esquinas(p, 6, 8, 20, 24, pal.STEEL, gap=2)
    # abaniquillo de refrigeracion (circulo con radios)
    p.elipse(13, 15, 5, 5, tono(acero, 2), contorno=tono(hierro, 0))
    for grados in range(0, 360, 45):
        a = math.radians(grados)
        p.linea(13 + 1.5 * math.cos(a), 15 + 1.5 * math.sin(a),
                13 + 4 * math.cos(a), 15 + 4 * math.sin(a),
                tono(hierro, 1))
    p.elipse(13, 15, 1.4, 1.4, tono(hierro, 3))
    # camisa de descarga
    p.rect(21, 12, 27, 20, tono(acero, 2))
    p.hlinea(21, 27, 12, tono(acero, 4))
    p.hlinea(21, 27, 20, tono(hierro, 0))
    p.rect(25, 10, 27, 22, tono(hierro, 2))
    p.hlinea(25, 27, 10, tono(hierro, 3))
    p.hlinea(25, 27, 22, tono(hierro, 0))
    # boca de aspiracion abajo
    p.rect(23, 22, 26, 27, tono(hierro, 1))
    p.hlinea(23, 26, 27, tono(hierro, 0))
    # mancha fugas
    p.pset(16, 22, tono(pal.SULFATO, 1))
    p.pset(17, 23, tono(pal.SULFATO, 0))


def soldadora_arco_portatil(p):
    """Soldadora de arco portatil: maleta de chapa con cables y pica."""
    amarillo, acero, hierro, carbon = (pal.AMARILLO, pal.STEEL, pal.HIERRO,
                                       pal.CARBON)
    # maleta
    p.rect(4, 9, 21, 25, tono(amarillo, 2))
    p.hlinea(4, 21, 9, tono(amarillo, 3))
    p.hlinea(4, 21, 25, tono(amarillo, 0))
    p.vlinea(4, 9, 25, tono(amarillo, 3))
    # franja de vinilo inferior
    p.rect(4, 13, 21, 15, tono(carbon, 1))
    p.hlinea(4, 21, 13, tono(carbon, 2))
    p.rect(10, 4, 15, 8, tono(hierro, 2))          # asa
    p.pset(10, 4, tono(hierro, 3))
    p.pset(14, 4, tono(hierro, 3))
    # rejilla de aire
    rejilla_lineas(p, 6, 17, 13, 23, tono(amarillo, 1), tono(amarillo, 0), 3)
    # perilla de ajuste
    p.elipse(17, 19, 2, 2, tono(hierro, 2), contorno=tono(hierro, 0))
    p.pset(18, 18, tono(hierro, 4))
    # cables de masa y portaelectrodo
    p.linea(21, 17, 28, 15, tono(carbon, 2))
    p.linea(22, 21, 29, 19, tono(carbon, 1))
    p.rect(26, 13, 29, 16, tono(acero, 1))
    p.hlinea(26, 29, 13, tono(acero, 3))
    p.pset(29, 16, tono(carbon, 0))
    # pica con electropodo
    p.linea(29, 19, 26, 22, tono(acero, 3))
    p.pset(25, 23, tono(carbon, 0))
    # manchas de chispas
    p.pset(17, 12, tono(pal.OXIDO, 1))
    p.pset(8, 12, tono(pal.OXIDO, 2))


def caja_engranajes_tractor(p):
    """Caja de engranajes: carcasa con ejes salientes y tapa con pernos."""
    hierro, acero, oliva, oxido = (pal.HIERRO, pal.STEEL, pal.OLIVA,
                                   pal.OXIDO)
    # carcasa
    p.rect(5, 10, 25, 24, tono(oliva, 2))
    p.hlinea(5, 25, 10, tono(oliva, 3))
    p.hlinea(5, 25, 24, tono(oliva, 0))
    pernos_esquinas(p, 5, 10, 25, 24, pal.STEEL, gap=2)
    # tapa con junta
    p.rect(8, 13, 22, 21, tono(oliva, 1))
    p.vlinea(8, 13, 21, tono(oliva, 0))
    p.hlinea(8, 22, 13, tono(oliva, 0))
    # engranaje visible en la tapa
    p.elipse(15, 17, 3.4, 3.4, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(15, 17, 1.4, 1.4, tono(hierro, 1))
    for grados in range(0, 360, 90):
        a = math.radians(grados)
        p.pset(int(15 + 3.2 * math.cos(a)), int(17 + 3.2 * math.sin(a)),
               tono(acero, 3))
    # ejes salientes
    p.rect(25, 14, 30, 18, tono(acero, 3))
    p.hlinea(25, 30, 14, tono(acero, 4))
    p.hlinea(25, 30, 18, tono(hierro, 0))
    p.elipse(29, 16, 1.2, 1.6, tono(hierro, 3))
    # engrase: gotero
    p.pset(11, 9, tono(oxido, 3))
    p.pset(12, 8, tono(oxido, 2))
    # oxido de musgo en la base
    p.pset(6, 23, tono(oxido, 1))
    p.pset(24, 23, tono(oxido, 2))


def centrifugadora_muestras(p):
    """Centrifugadora de muestras: arca de laboratorio con campana."""
    acero, beige, hierro, verde, cristal = (pal.STEEL, pal.BEIGE,
                                            pal.HIERRO, pal.OLIVA,
                                            pal.CRISTAL)
    # arca
    p.rect(5, 8, 25, 26, tono(beige, 2))
    p.hlinea(5, 25, 8, tono(beige, 3))
    p.hlinea(5, 25, 26, tono(beige, 0))
    p.vlinea(5, 8, 26, tono(beige, 3))
    # campana superior con cubierta
    p.rect(8, 5, 22, 7, tono(acero, 2))
    p.hlinea(8, 22, 5, tono(acero, 3))
    p.pset(15, 4, tono(acero, 3))
    p.pset(16, 4, tono(acero, 3))
    # ventanilla de rotor
    p.rect(9, 11, 19, 19, tono(hierro, 0))
    p.rect(10, 12, 18, 18, tono(cristal, 1))
    p.hlinea(10, 18, 12, tono(cristal, 2))
    # aspas en giro
    for grados in (30, 150, 270):
        a = math.radians(grados)
        p.linea(14 + 1.5 * math.cos(a), 15 + 1.5 * math.sin(a),
                14 + 3.4 * math.cos(a), 15 + 3.4 * math.sin(a),
                tono(acero, 3))
    p.elipse(14, 15, 1.2, 1.2, tono(hierro, 3))
    # panel con botones
    p.rect(21, 11, 24, 22, tono(acero, 1))
    p.hlinea(21, 24, 11, tono(acero, 2))
    rejilla_puntos(p, 22, 12, 1, 4, 3, tono(pal.ROJO, 2))
    p.pset(22, 20, tono(pal.AMARILLO, 2))
    # viales de muestra en la contratapa
    p.vlinea(7, 20, 24, tono(verde, 3))
    p.pset(7, 19, tono(pal.LATON, 2))
    # adhesivo de radiacion despegado
    p.pset(6, 25, tono(pal.AMARILLO, 2))
    p.pset(7, 25, tono(pal.AMARILLO, 1))


def contenedor_isotopos(p):
    """Contenedor de isotopos: cilindro de plomo con muescas y sello."""
    hierro, acero, amarillo, carbon = (pal.HIERRO, pal.STEEL, pal.AMARILLO,
                                       pal.CARBON)
    # cuerpo octogonal de plomo
    p.rect(8, 8, 23, 26, tono(hierro, 2))
    p.poligono([(8, 8), (23, 8), (25, 10), (6, 10)], tono(acero, 3))
    p.hlinea(8, 23, 26, tono(hierro, 0))
    # nervios verticales de blindaje
    for x in (11, 16, 21):
        p.vlinea(x, 11, 25, tono(hierro, 1))
        p.vlinea(x + 1, 11, 25, tono(hierro, 3))
    # banda de radiacion (estrecha, cerca de la base)
    p.rect(8, 20, 23, 23, tono(amarillo, 2))
    p.hlinea(8, 23, 20, tono(amarillo, 3))
    p.hlinea(8, 23, 23, tono(amarillo, 0))
    # trefolio: un punto por sector (sin manchas fusionadas)
    p.pset(15, 21, tono(carbon, 0))
    p.pset(14, 22, tono(carbon, 0))
    p.pset(16, 22, tono(carbon, 0))
    p.pset(15, 20, tono(carbon, 0))
    # tapa atornillada (anillo)
    p.rect(6, 6, 25, 8, tono(acero, 2))
    p.hlinea(6, 25, 6, tono(acero, 3))
    p.pset(7, 7, tono(acero, 4))
    p.pset(24, 7, tono(acero, 4))
    # precinto de plomo con sello
    p.linea(20, 3, 23, 6, tono(acero, 1))
    p.elipse(19, 3, 1.6, 1.6, tono(acero, 3), contorno=tono(hierro, 0))
    # oxido de plomo blanco
    p.pset(9, 24, tono(pal.SULFATO, 1))
    p.pset(10, 25, tono(pal.SULFATO, 0))
    p.pset(22, 25, tono(pal.SULFATO, 1))


def rociador_descontaminacion(p):
    """Rociador de descontaminacion: bomba manual con lanza y boquilla."""
    oliva, acero, hierro, cristal, carbon = (pal.OLIVA, pal.STEEL,
                                            pal.HIERRO, pal.CRISTAL,
                                            pal.CARBON)
    # deposito
    cilindro(p, 9, 8, 12, 18, acero, cuerpo=2)
    # banda superior + identificacion
    p.rect(9, 12, 20, 14, tono(oliva, 2))
    p.hlinea(9, 20, 12, tono(oliva, 3))
    p.hlinea(9, 20, 14, tono(oliva, 0))
    # ventana de nivel
    p.rect(12, 17, 15, 22, tono(cristal, 1))
    p.hlinea(12, 15, 17, tono(cristal, 3))
    p.hlinea(12, 15, 22, tono(cristal, 0))
    p.pset(13, 18, tono(cristal, 4))
    # palanca de bombeo
    p.linea(14, 4, 20, 7, tono(acero, 3))
    p.linea(14, 5, 20, 8, tono(acero, 1))
    p.pset(13, 4, tono(hierro, 0))
    # lanza
    p.linea(21, 10, 28, 13, tono(acero, 2))
    p.pset(28, 13, tono(carbon, 0))
    p.pset(29, 14, tono(hierro, 3))
    # boquilla y chorros
    p.pset(29, 12, tono(cristal, 3))
    p.pset(30, 11, tono(cristal, 1))
    p.pset(30, 13, tono(cristal, 3))
    # manguera lateral
    for x, y in ((8, 24), (7, 25), (6, 26), (6, 27)):
        p.pset(x, y, tono(carbon, 2))
    # oxido
    p.pset(10, 24, tono(pal.OXIDO, 1))
    p.pset(19, 24, tono(pal.OXIDO, 2))


def visor_nocturno_pnv57(p):
    """Visor nocturno PNV-57: dos tubos verdes con banda y diafragma."""
    carbon, cristal, hierro, oliva = (pal.CARBON, pal.CRISTAL, pal.HIERRO,
                                      pal.OLIVA)
    # monta frontal
    p.rect(4, 13, 10, 22, tono(oliva, 2))
    p.hlinea(4, 10, 13, tono(oliva, 3))
    p.hlinea(4, 10, 22, tono(oliva, 0))
    # banda de cabeza elastica
    p.rect(10, 14, 14, 21, tono(carbon, 1))
    p.hlinea(10, 14, 14, tono(carbon, 2))
    # tubo izquierdo
    p.rect(15, 8, 22, 16, tono(carbon, 1))
    p.hlinea(15, 22, 8, tono(carbon, 2))
    p.rect(21, 8, 25, 16, tono(hierro, 2))
    p.hlinea(21, 25, 8, tono(hierro, 3))
    p.elipse(25, 12, 1.6, 3.4, tono(cristal, 1), contorno=tono(hierro, 0))
    p.pset(24, 11, tono(cristal, 4))
    # tubo derecho
    p.rect(15, 18, 22, 26, tono(carbon, 1))
    p.hlinea(15, 22, 18, tono(carbon, 2))
    p.rect(21, 18, 25, 26, tono(hierro, 2))
    p.hlinea(21, 25, 18, tono(hierro, 3))
    p.elipse(25, 22, 1.6, 3.4, tono(cristal, 1), contorno=tono(hierro, 0))
    p.pset(24, 21, tono(cristal, 4))
    # brillo del tubo encendido (verde fosforo)
    p.pset(17, 12, tono(pal.SULFATO, 1))
    p.pset(17, 22, tono(pal.SULFATO, 1))
    # regulacion lateral
    p.pset(20, 7, tono(hierro, 3))
    p.pset(20, 27, tono(hierro, 3))


def modulo_punteria_btr(p):
    """Modulo de punteria BTR: visor periscopico con blindaje."""
    oliva, hierro, acero, cristal, carbon = (pal.OLIVA, pal.HIERRO,
                                            pal.STEEL, pal.CRISTAL,
                                            pal.CARBON)
    # carcasa superior blindada
    p.poligono([(4, 12), (17, 8), (27, 12), (27, 18), (4, 18)],
               tono(oliva, 2))
    p.poligono([(4, 12), (17, 8), (18, 10), (5, 14)], tono(oliva, 3))
    p.hlinea(4, 27, 18, tono(oliva, 0))
    # ventana del visor
    p.rect(12, 13, 20, 17, tono(carbon, 0))
    p.pset(13, 14, tono(cristal, 2))
    p.pset(14, 14, tono(cristal, 3))
    p.hlinea(12, 20, 17, tono(hierro, 0))
    # tubo periscopico
    p.rect(14, 4, 17, 8, tono(hierro, 2))
    p.hlinea(14, 17, 4, tono(hierro, 3))
    p.hlinea(14, 17, 8, tono(hierro, 0))
    p.elipse(15, 4, 1.4, 1, tono(acero, 4))
    # montura traseva con reguladores
    p.rect(4, 19, 10, 24, tono(oliva, 1))
    p.hlinea(4, 10, 19, tono(oliva, 2))
    p.hlinea(4, 10, 24, tono(oliva, 0))
    pernos_esquinas(p, 4, 19, 10, 24, pal.STEEL, gap=2)
    # brazo de cuna
    p.rect(20, 19, 26, 22, tono(hierro, 1))
    p.hlinea(20, 26, 19, tono(hierro, 2))
    p.hlinea(20, 26, 22, tono(hierro, 0))
    # conducto de cable
    p.linea(26, 16, 30, 19, tono(carbon, 2))
    # roce de boina de polvo
    p.pset(7, 16, tono(pal.BEIGE, 1))
    p.pset(21, 11, tono(pal.OXIDO, 1))


def dron_reconocimiento(p):
    """Dron de reconocimiento: quadricoptero plegado con camara."""
    oliva, carbon, acero, cristal, rojo = (pal.OLIVA, pal.CARBON, pal.STEEL,
                                           pal.CRISTAL, pal.ROJO)
    hierro = pal.HIERRO
    # brazos cruzados
    p.linea(5, 8, 27, 24, tono(carbon, 1))
    p.linea(27, 8, 5, 24, tono(carbon, 1))
    # cuerpo central
    p.rect(12, 12, 20, 20, tono(oliva, 2))
    p.hlinea(12, 20, 12, tono(oliva, 3))
    p.hlinea(12, 20, 20, tono(oliva, 0))
    # sensores de la cara
    p.pset(13, 14, tono(cristal, 2))
    p.pset(14, 14, tono(cristal, 3))
    p.pset(13, 15, tono(cristal, 2))
    # camara bola
    p.elipse(17, 16, 2.4, 2.4, tono(carbon, 0), contorno=tono(hierro, 0))
    p.pset(16, 15, tono(cristal, 4))
    # rotores plegados
    for cx, cy in ((5, 7), (27, 7), (5, 25), (27, 25)):
        p.elipse(cx, cy, 2.2, 1.2, tono(carbon, 1), contorno=tono(carbon, 0))
        p.pset(cx, cy, tono(acero, 3))
    # LEDs de estado
    p.pset(19, 18, tono(rojo, 3))
    p.pset(18, 18, tono(rojo, 2))
    # bateria conectada
    p.rect(14, 21, 18, 23, tono(pal.AMARILLO, 2))
    p.hlinea(14, 18, 21, tono(pal.AMARILLO, 3))
    p.hlinea(14, 18, 23, tono(pal.AMARILLO, 0))


DIBUJOS = {
    "taladro_percutor_mina": taladro_percutor_mina,
    "compresor_aire_fabrica": compresor_aire_fabrica,
    "bomba_hidraulica_refrigeracion": bomba_hidraulica_refrigeracion,
    "soldadora_arco_portatil": soldadora_arco_portatil,
    "caja_engranajes_tractor": caja_engranajes_tractor,
    "centrifugadora_muestras": centrifugadora_muestras,
    "contenedor_isotopos": contenedor_isotopos,
    "rociador_descontaminacion": rociador_descontaminacion,
    "visor_nocturno_pnv57": visor_nocturno_pnv57,
    "modulo_punteria_btr": modulo_punteria_btr,
    "dron_reconocimiento": dron_reconocimiento,
}
