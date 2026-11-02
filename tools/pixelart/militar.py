# -*- coding: utf-8 -*-
"""Material militar y de supervision de la Zona: pixel art 32x32."""
from __future__ import annotations

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import (cara, cilindro, corroer, costuras,
                                   pernos_esquinas, rejilla_lineas,
                                   rejilla_puntos, terminal)


def traje_hazmat_liquidador(p):
    """Traje de liquimador: silueta integral de PVC con capucha y botas."""
    verde, carbon, hierro, cristal = (pal.OLIVA, pal.CARBON, pal.HIERRO,
                                      pal.CRISTAL)
    # cuerpo (bata voluminosa)
    p.poligono([(8, 14), (23, 14), (26, 28), (5, 28)], tono(verde, 2))
    p.poligono([(8, 14), (13, 12), (19, 12), (23, 14), (20, 16), (11, 16)],
               tono(verde, 3))
    p.hlinea(5, 26, 28, tono(verde, 0))
    p.vlinea(5, 16, 28, tono(verde, 1))
    # capucha con visor
    p.rect(11, 5, 20, 13, tono(verde, 2))
    p.hlinea(11, 20, 5, tono(verde, 3))
    p.poligono([(11, 5), (20, 5), (22, 9), (9, 9)], tono(verde, 3))
    p.pset(10, 7, tono(verde, 0))
    p.pset(21, 7, tono(verde, 0))
    # visor de PVC
    p.rect(12, 7, 19, 12, tono(carbon, 1))
    p.hlinea(12, 19, 7, tono(carbon, 2))
    p.pset(13, 8, tono(cristal, 3))
    p.pset(14, 8, tono(cristal, 4))
    p.hlinea(12, 19, 12, tono(cristal, 0))
    # cuello de junta
    p.rect(10, 13, 21, 15, tono(carbon, 1))
    p.hlinea(10, 21, 13, tono(carbon, 2))
    # guantes caidos (brazos)
    p.rect(3, 17, 7, 26, tono(verde, 1))
    p.hlinea(3, 7, 17, tono(verde, 2))
    p.rect(24, 17, 28, 26, tono(verde, 1))
    p.hlinea(24, 28, 17, tono(verde, 2))
    p.rect(3, 26, 7, 28, tono(carbon, 1))
    p.rect(24, 26, 28, 28, tono(carbon, 1))
    # botas
    p.rect(9, 28, 13, 31, tono(carbon, 1))
    p.rect(18, 28, 22, 31, tono(carbon, 1))
    p.hlinea(9, 13, 31, tono(carbon, 0))
    p.hlinea(18, 22, 31, tono(carbon, 0))
    # brazalete dosimetro
    p.pset(12, 17, tono(pal.AMARILLO, 2))
    p.pset(13, 17, tono(pal.AMARILLO, 3))
    # manchas de radiacion en el faldon
    p.pset(10, 24, tono(pal.OXIDO, 2))
    p.pset(11, 24, tono(pal.OXIDO, 1))
    p.pset(20, 26, tono(pal.OXIDO, 1))


def respirador_papr(p):
    """Respirador PAPR: capucha con unidad de insuflacion y filtro."""
    carbon, oliva, hierro, acero = (pal.CARBON, pal.OLIVA, pal.HIERRO,
                                    pal.STEEL)
    # capucha transparente
    p.poligono([(6, 6), (25, 6), (28, 12), (26, 22), (16, 26), (5, 22), (3, 12)],
               tono(oliva, 2))
    p.poligono([(8, 8), (23, 8), (25, 13), (23, 20), (16, 23), (7, 20), (5, 13)],
               tono(oliva, 3))
    # cara interior sombreada
    p.elipse(16, 15, 6, 6, tono(carbon, 1), contorno=tono(carbon, 0))
    p.pset(13, 14, tono(pal.CRISTAL, 3))
    p.pset(14, 14, tono(pal.CRISTAL, 4))
    p.pset(19, 14, tono(pal.CRISTAL, 3))
    p.pset(18, 14, tono(pal.CRISTAL, 4))
    # filtro KAB con entrada
    cilindro(p, 12, 20, 6, 8, hierro, cuerpo=2)
    p.elipse(15, 20, 2.6, 1.6, tono(hierro, 0), contorno=tono(hierro, 3))
    # unidad de ventilacion lateral
    p.rect(21, 16, 28, 23, tono(oliva, 1))
    p.hlinea(21, 28, 16, tono(oliva, 2))
    p.hlinea(21, 28, 23, tono(oliva, 0))
    rejilla_lineas(p, 22, 17, 27, 22, tono(oliva, 0), tono(carbon, 0), 2)
    p.pset(27, 19, tono(pal.ROJO, 2))
    # correas traseras
    p.vlinea(3, 12, 21, tono(carbon, 1))
    p.pset(3, 14, tono(carbon, 0))
    p.pset(3, 19, tono(carbon, 0))
    # polvo de uso
    p.pset(8, 24, tono(pal.BEIGE, 1))
    p.pset(24, 7, tono(pal.OXIDO, 1))


def chaleco_balistico_6b3(p):
    """Chaleco 6B3: bolsillos con correas y plancha frontal."""
    oliva, carbon, hierro, acero = (pal.OLIVA, pal.CARBON, pal.HIERRO,
                                    pal.STEEL)
    # gabardina del chaleco
    p.poligono([(6, 7), (25, 7), (27, 27), (4, 27)], tono(oliva, 2))
    p.hlinea(6, 25, 7, tono(oliva, 3))
    p.hlinea(4, 27, 27, tono(oliva, 0))
    # mangos escotados (hombros)
    p.pset(6, 7, tono(oliva, 4))
    p.pset(25, 7, tono(oliva, 4))
    # cuello
    p.rect(10, 4, 21, 7, tono(oliva, 1))
    p.hlinea(10, 21, 4, tono(oliva, 2))
    # placa frontal al la vista (bolso uno)
    p.rect(8, 11, 22, 17, tono(oliva, 1))
    p.hlinea(8, 22, 11, tono(oliva, 0))
    p.hlinea(8, 22, 17, tono(oliva, 0))
    # bolsillo dos con trapa
    p.rect(8, 19, 22, 25, tono(oliva, 1))
    p.hlinea(8, 22, 19, tono(oliva, 0))
    p.hlinea(8, 22, 25, tono(oliva, 0))
    p.hlinea(8, 22, 22, tono(carbon, 0))
    # correas cruzadas (portaequipo)
    for x, y in ((8, 13), (12, 13), (16, 13), (20, 13)):
        p.pset(x, y, tono(carbon, 1))
    for x, y in ((9, 21), (13, 21), (17, 21), (21, 21)):
        p.pset(x, y, tono(carbon, 1))
    # hebilla metálica
    p.rect(14, 23, 17, 25, tono(acero, 2))
    p.hlinea(14, 17, 23, tono(acero, 3))
    p.pset(15, 24, tono(hierro, 0))
    # remate manchado
    p.pset(23, 25, tono(pal.OXIDO, 1))
    p.pset(24, 26, tono(pal.OXIDO, 2))


def radio_campana_r159(p):
    """Radio R-159 de campania: caqueta de lona con pantalla yجة."""
    oliva, carbon, hierro, acero = (pal.OLIVA, pal.CARBON, pal.HIERRO,
                                    pal.STEEL)
    # caqueta de lona con solapa
    p.rect(4, 9, 27, 27, tono(oliva, 2))
    p.hlinea(4, 27, 9, tono(oliva, 3))
    p.hlinea(4, 27, 27, tono(oliva, 0))
    p.vlinea(4, 9, 27, tono(oliva, 3))
    p.rect(5, 5, 26, 8, tono(oliva, 3))            # solapa
    p.hlinea(5, 26, 5, tono(oliva, 4))
    p.hlinea(5, 26, 8, tono(oliva, 1))
    # panel de frecuencias
    p.rect(8, 12, 18, 20, tono(hierro, 0))
    p.rect(9, 13, 17, 19, tono(carbon, 1))
    p.pset(10, 14, tono(pal.CRISTAL, 3))
    p.pset(11, 14, tono(pal.CRISTAL, 4))
    p.hlinea(10, 16, 18, tono(acero, 2))
    # perillas laterales (disbeles)
    p.elipse(22, 14, 2, 2, tono(carbon, 1), contorno=tono(carbon, 0))
    p.pset(21, 13, tono(carbon, 2))
    p.elipse(22, 19, 2, 2, tono(carbon, 1), contorno=tono(carbon, 0))
    p.pset(21, 18, tono(carbon, 2))
    # antena de lanza
    p.linea(26, 8, 29, 3, tono(acero, 3))
    p.linea(27, 8, 30, 4, tono(acero, 1))
    p.pset(29, 3, tono(acero, 4))
    # asa de lona
    p.rect(12, 2, 18, 4, tono(oliva, 1))
    p.hlinea(12, 18, 2, tono(oliva, 2))
    p.hlinea(12, 18, 4, tono(oliva, 0))
    # costuras de la lona
    costuras(p, [(4, y) for y in range(10, 27, 3)], tono(oliva, 0))
    # mosquaton
    p.pset(6, 10, tono(acero, 3))


def casco_ssh68(p):
    """Casco SSH-68: bal abombado con borde, remaches y correa."""
    oliva, hierro, acero, carbon = (pal.OLIVA, pal.HIERRO, pal.STEEL,
                                    pal.CARBON)
    # copa
    p.poligono([(4, 13), (8, 4), (23, 4), (27, 13), (26, 13), (23, 12),
                (22, 16), (9, 16), (7, 12), (5, 13)], tono(oliva, 2))
    p.elipse(16, 10, 9, 6, tono(oliva, 2))
    p.elipse(15, 9, 8, 5, tono(oliva, 3))
    # borde inferior
    p.rect(2, 16, 29, 18, tono(oliva, 1))
    p.hlinea(2, 29, 16, tono(oliva, 2))
    p.hlinea(2, 29, 18, tono(oliva, 0))
    # veneras laterales del borde
    p.poligono([(2, 16), (7, 16), (7, 18), (2, 18)], tono(oliva, 1))
    p.poligono([(25, 16), (29, 16), (29, 18), (25, 18)], tono(oliva, 1))
    # remaches del borde
    for x in (5, 11, 21, 27):
        p.pset(x, 17, tono(acero, 4))
    # brillo de la copa
    for x, y in ((9, 6), (12, 5), (15, 5), (18, 6)):
        p.pset(x, y, tono(oliva, 4))
    # estrella grabada (dibujo leve)
    p.pset(16, 9, tono(pal.ROJO, 2))
    p.pset(15, 10, tono(pal.ROJO, 1))
    p.pset(17, 10, tono(pal.ROJO, 1))
    p.pset(16, 11, tono(pal.ROJO, 1))
    # correa
    p.linea(10, 25, 14, 27, tono(carbon, 1))
    p.linea(13, 26, 18, 27, tono(carbon, 2))
    p.pset(18, 27, tono(acero, 3))


def casco_minero(p):
    """Casco minero: semiesfera amarilla con ala y faro montado."""
    amarillo, carbon, acero, hierro = (pal.AMARILLO, pal.CARBON, pal.STEEL,
                                       pal.HIERRO)
    # copa amarilla
    p.elipse(16, 15, 11, 8, tono(amarillo, 2), contorno=tono(hierro, 0))
    p.elipse(15, 14, 9, 6, tono(amarillo, 3))
    # borde
    p.hlinea(5, 27, 21, tono(amarillo, 1))
    p.hlinea(5, 27, 22, tono(amarillo, 0))
    # ala frontal curva
    p.rect(3, 20, 29, 23, tono(amarillo, 2))
    p.hlinea(3, 29, 20, tono(amarillo, 3))
    p.hlinea(3, 29, 23, tono(amarillo, 0))
    p.pset(3, 22, tono(amarillo, 0))
    p.pset(29, 22, tono(amarillo, 0))
    # farol montado
    p.rect(12, 7, 19, 11, tono(hierro, 2))
    p.hlinea(12, 19, 7, tono(hierro, 3))
    p.hlinea(12, 19, 11, tono(hierro, 0))
    p.rect(13, 8, 18, 10, tono(pal.BEIGE, 2))
    p.hlinea(13, 18, 8, tono(pal.BEIGE, 3))
    p.pset(13, 9, tono(pal.BEIGE, 3))
    # arnes interior visible
    p.pset(13, 24, tono(carbon, 1))
    p.pset(15, 25, tono(carbon, 1))
    p.pset(18, 25, tono(carbon, 1))
    p.pset(20, 24, tono(carbon, 1))
    # remaches
    for x in (7, 25):
        p.pset(x, 21, tono(acero, 4))
    # suciedad de mina
    p.pset(8, 19, tono(carbon, 1))
    p.pset(23, 19, tono(carbon, 1))


def cargador_baquelita_ak74(p):
    """Cargador AK-74 de baquelita: hueso curvado con nervios."""
    carbon, hierro, acero, oxido = pal.CARBON, pal.HIERRO, pal.STEEL, pal.OXIDO
    # cuerpo curvado
    p.poligono([(10, 5), (20, 5), (24, 20), (22, 26), (16, 26), (12, 20)],
               tono(carbon, 1))
    # canal de nervadura (baquelita)
    for y in range(6, 26, 3):
        p.hlinea(12, 21, y, tono(carbon, 2))
        p.hlinea(13, 20, y, tono(carbon, 0))
    # aristas laterales de refuerzo
    p.vlinea(11, 6, 21, tono(carbon, 2))
    p.vlinea(20, 6, 22, tono(carbon, 2))
    # lengua metálica superior
    p.rect(9, 3, 21, 6, tono(acero, 1))
    p.hlinea(9, 21, 3, tono(acero, 3))
    p.hlinea(9, 21, 6, tono(hierro, 0))
    # labios de entrega
    p.rect(8, 4, 10, 6, tono(acero, 3))
    p.hlinea(8, 10, 4, tono(acero, 4))
    # base tapada
    p.rect(15, 25, 24, 28, tono(hierro, 1))
    p.hlinea(15, 24, 25, tono(hierro, 2))
    p.hlinea(15, 24, 28, tono(hierro, 0))
    # marca de calibre grabada
    p.pset(15, 10, tono(carbon, 0))
    p.pset(16, 10, tono(carbon, 0))
    # desgaste de baquelita (arista clara)
    p.pset(14, 7, tono(carbon, 3))
    p.pset(15, 12, tono(carbon, 3))


def caja_municion_50(p):
    """Caja de munición de 50: lata estancada con banda y estancias."""
    oliva, hierro, acero, carbon = (pal.OLIVA, pal.HIERRO, pal.STEEL,
                                    pal.CARBON)
    # caja
    p.rect(4, 10, 27, 25, tono(oliva, 2))
    p.hlinea(4, 27, 10, tono(oliva, 3))
    p.hlinea(4, 27, 25, tono(oliva, 0))
    pernos_esquinas(p, 4, 10, 27, 25, pal.STEEL, gap=2)
    # tapa con solapilla
    p.rect(4, 8, 27, 11, tono(oliva, 3))
    p.hlinea(4, 27, 8, tono(oliva, 4))
    p.hlinea(4, 27, 11, tono(oliva, 1))
    # banda de matriz (y oyeco)
    p.rect(9, 13, 22, 17, tono(hierro, 1))
    p.hlinea(9, 22, 13, tono(hierro, 2))
    p.hlinea(9, 22, 17, tono(hierro, 0))
    p.pset(11, 15, tono(acero, 4))
    p.pset(20, 15, tono(acero, 4))
    # cinta de precinto vertical
    p.vlinea(14, 8, 25, tono(carbon, 1))
    p.vlinea(15, 8, 25, tono(oliva, 1))
    # cartuchos asomando por la boca
    p.rect(5, 26, 8, 29, tono(pal.LATON, 2))
    p.hlinea(5, 8, 26, tono(pal.LATON, 3))
    p.hlinea(5, 8, 29, tono(pal.LATON, 0))
    p.rect(10, 26, 13, 29, tono(pal.LATON, 2))
    p.hlinea(10, 13, 26, tono(pal.LATON, 3))
    p.hlinea(10, 13, 29, tono(pal.LATON, 0))
    # mancha de ozonizada
    p.pset(24, 22, tono(oxido := pal.OXIDO, 1))
    p.pset(25, 23, tono(oxido, 2))


def red_camuflaje(p):
    """Red de camuflaje: malla con nudos y trapos verdes."""
    oliva, carbon, verde = pal.OLIVA, pal.CARBON, pal.SULFATO
    # marco de cuerda (rombo de retícula)
    # cuerda perimetral (rombo de reticula)
    p.poligono([(4, 12), (12, 7), (22, 6), (29, 11), (28, 21), (20, 27),
                (10, 25), (4, 20)], tono(oliva, 1))
    # retícula interna
    p.linea(4, 12, 20, 27, tono(oliva, 0))
    p.linea(12, 7, 28, 21, tono(oliva, 0))
    p.linea(22, 6, 10, 25, tono(oliva, 0))
    p.linea(29, 11, 4, 20, tono(oliva, 0))
    p.linea(8, 15, 24, 14, tono(oliva, 0))
    p.linea(15, 7, 18, 26, tono(oliva, 0))
    # trapo de camuflaje (bolas)
    p.elipse(9, 13, 3, 2.4, tono(oliva, 2), contorno=tono(carbon, 0))
    p.elipse(22, 11, 3, 2.2, tono(oliva, 2), contorno=tono(carbon, 0))
    p.elipse(14, 21, 3.4, 2.6, tono(oliva, 2), contorno=tono(carbon, 0))
    p.elipse(24, 22, 2.6, 2, tono(oliva, 1), contorno=tono(carbon, 0))
    # brillos de tela
    p.pset(8, 12, tono(oliva, 3))
    p.pset(21, 10, tono(oliva, 3))
    p.pset(13, 20, tono(oliva, 3))
    # nudos
    for x, y in ((16, 14), (19, 18), (12, 18)):
        p.pset(x, y, tono(carbon, 1))
    # chamuscado de quemado
    p.pset(25, 16, tono(pal.OXIDO, 2))
    p.pset(26, 17, tono(pal.OXIDO, 1))


def botas_paracaidista(p):
    """Botas de paracaidista: par con cordones y suela aguje."""
    carbon, madera, hierro, acero = (pal.CARBON, pal.MADERA, pal.HIERRO,
                                     pal.STEEL)
    # bota trasera (levantada)
    p.poligono([(4, 10), (11, 10), (12, 22), (4, 22)], tono(madera, 1))
    p.hlinea(4, 11, 10, tono(madera, 2))
    p.rect(4, 22, 12, 27, tono(madera, 1))
    p.hlinea(4, 12, 22, tono(madera, 2))
    p.hlinea(4, 12, 27, tono(hierro, 0))
    # lengua y cordones
    p.vlinea(8, 12, 18, tono(madera, 3))
    for y in range(12, 19, 2):
        p.pset(7, y, tono(carbon, 0))
        p.pset(10, y, tono(carbon, 0))
    # bota delantera (de frente-lado)
    p.poligono([(17, 14), (24, 14), (26, 22), (24, 24), (16, 24), (15, 18)],
               tono(madera, 2))
    p.hlinea(17, 24, 14, tono(madera, 3))
    p.hlinea(16, 26, 24, tono(madera, 3))
    # caña
    p.rect(16, 20, 27, 27, tono(madera, 1))
    p.hlinea(16, 27, 20, tono(madera, 2))
    p.hlinea(16, 27, 27, tono(hierro, 0))
    # ojalete y cordones cruzados
    for y in range(15, 20, 2):
        p.pset(20, y, tono(carbon, 0))
        p.pset(23, y, tono(carbon, 0))
        p.linea(20, y, 22, y + 2, tono(carbon, 1))
    # suelas
    p.hlinea(3, 12, 28, tono(carbon, 0))
    p.hlinea(15, 27, 28, tono(carbon, 0))
    for x in range(5, 11, 2):
        p.pset(x, 29, tono(carbon, 1))
    for x in range(17, 25, 2):
        p.pset(x, 29, tono(carbon, 1))
    # quiebre de cuero
    p.pset(18, 17, tono(madera, 0))
    p.pset(19, 18, tono(madera, 0))


def placa_balistica_acero(p):
    """Placa balistica: placa diagonales con arista y correa trasera."""
    acero, hierro, carbon, oliva = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.OLIVA)
    # placa trapezoidal
    p.poligono([(6, 18), (11, 8), (21, 8), (26, 18), (26, 24), (6, 24)],
               tono(acero, 2))
    # cara superior brillante
    p.poligono([(11, 8), (21, 8), (23, 11), (9, 11)], tono(acero, 3))
    # diagonales de toldo acanalado
    for k in range(4):
        x = 9 + k * 5
        p.linea(x, 13, x + 2, 22, tono(acero, 1))
        p.linea(x + 1, 13, x + 3, 22, tono(acero, 3))
    # esquinas reforzadas
    p.pset(7, 17, tono(hierro, 1))
    p.pset(25, 17, tono(hierro, 1))
    p.pset(12, 9, tono(acero, 4))
    p.pset(20, 9, tono(acero, 4))
    # rayon de impacto reparado
    p.pset(17, 15, tono(pal.OXIDO, 2))
    p.pset(18, 15, tono(pal.OXIDO, 1))
    p.pset(17, 16, tono(pal.OXIDO, 1))
    # correa de fijacion abajo
    p.rect(10, 25, 22, 27, tono(oliva, 1))
    p.hlinea(10, 22, 25, tono(oliva, 2))
    p.hlinea(10, 22, 27, tono(oliva, 0))
    p.rect(15, 26, 17, 28, tono(acero, 3))
    p.pset(16, 27, tono(hierro, 0))


def eslabon_oruga_tanque(p):
    """Eslabon de oruga: zapata dentada con pasador central."""
    hierro, acero, carbon, oxido = (pal.HIERRO, pal.STEEL, pal.CARBON,
                                    pal.OXIDO)
    # zapata perfilada
    p.poligono([(3, 14), (8, 10), (24, 10), (29, 14), (29, 24), (24, 27),
                (8, 27), (3, 24)], tono(hierro, 2))
    p.hlinea(3, 29, 27, tono(hierro, 0))
    # crucetas de refuerzo
    p.linea(8, 12, 24, 24, tono(acero, 2))
    p.linea(8, 24, 24, 12, tono(acero, 2))
    p.vlinea(16, 11, 26, tono(acero, 1))
    # dientes de paso (arriba)
    for x in (7, 13, 19, 25):
        p.rect(x, 6, x + 2, 9, tono(hierro, 1))
        p.hlinea(x, x + 2, 6, tono(hierro, 3))
        p.hlinea(x, x + 2, 9, tono(hierro, 0))
    # pasador central con cabeza
    p.elipse(16, 18, 3, 3, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(15, 17, 1.6, 1.6, tono(acero, 4))
    p.elipse(16, 18, 1.2, 1.2, tono(hierro, 1))
    # barro pegado
    p.pset(10, 26, tono(oxido, 2))
    p.pset(11, 26, tono(oxido, 1))
    p.pset(22, 26, tono(oxido, 1))
    # veta de óxido en arista
    p.pset(4, 15, tono(oxido, 1))
    p.pset(28, 19, tono(oxido, 2))


def guantes_soldador(p):
    """Guantes de soldador: par de guante de cuero con garra."""
    madera, carbon, hierro, acero = (pal.MADERA, pal.CARBON, pal.HIERRO,
                                     pal.STEEL)
    # guante izquierdo (mano abierta)
    p.poligono([(5, 9), (14, 9), (15, 20), (13, 24), (5, 24), (3, 18)],
               tono(madera, 2))
    p.hlinea(5, 14, 9, tono(madera, 3))
    p.hlinea(5, 15, 24, tono(madera, 0))
    # dedos separados
    for x in (5, 8, 11):
        p.vlinea(x, 5, 9, tono(madera, 2))
        p.vlinea(x, 25, 26, tono(madera, 0))
    p.rect(4, 3, 13, 9, tono(madera, 2))
    p.hlinea(4, 13, 3, tono(madera, 3))
    for x in (6, 9, 12):
        p.vlinea(x, 4, 8, tono(madera, 0))
    # punta del pulgar
    p.elipse(16, 14, 2, 3, tono(madera, 3), contorno=tono(madera, 0))
    # costuras
    costuras(p, [(7, 11), (7, 14), (7, 17), (7, 20)], tono(madera, 0))
    # canesú
    p.rect(14, 9, 17, 24, tono(madera, 1))
    p.hlinea(14, 17, 9, tono(madera, 2))
    p.hlinea(14, 17, 24, tono(madera, 0))
    # quemadura de proyección
    p.pset(10, 15, tono(pal.OXIDO, 3))
    p.pset(11, 16, tono(pal.OXIDO, 2))
    p.pset(10, 17, tono(pal.OXIDO, 2))


DIBUJOS = {
    "traje_hazmat_liquidador": traje_hazmat_liquidador,
    "respirador_papr": respirador_papr,
    "chaleco_balistico_6b3": chaleco_balistico_6b3,
    "radio_campana_r159": radio_campana_r159,
    "casco_ssh68": casco_ssh68,
    "casco_minero": casco_minero,
    "cargador_baquelita_ak74": cargador_baquelita_ak74,
    "caja_municion_50": caja_municion_50,
    "red_camuflaje": red_camuflaje,
    "botas_paracaidista": botas_paracaidista,
    "placa_balistica_acero": placa_balistica_acero,
    "eslabon_oruga_tanque": eslabon_oruga_tanque,
    "guantes_soldador": guantes_soldador,
}
