# -*- coding: utf-8 -*-
"""Infraestructura electrica y tableros: pixel art 32x32."""
from __future__ import annotations

import math

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import cilindro, rejilla_lineas


def transformador_subestacion(p):
    """Transformador: tanque de bornes con aletas y bushing ceramico."""
    hierro, acero, oxido, amarillo = (pal.HIERRO, pal.STEEL, pal.OXIDO,
                                      pal.AMARILLO)
    # caldera cuadrada
    p.rect(4, 13, 25, 28, tono(hierro, 2))
    p.hlinea(4, 25, 13, tono(hierro, 3))
    p.hlinea(4, 25, 28, tono(hierro, 0))
    p.vlinea(5, 14, 28, tono(hierro, 3))
    # aletas del radiador
    for x in (8, 13, 18):
        p.rect(x - 1, 16, x + 1, 25, tono(hierro, 1))
        p.hlinea(x - 1, x + 1, 16, tono(hierro, 3))
        p.hlinea(x - 1, x + 1, 25, tono(hierro, 0))
    # bushing de porcelana (tallado)
    cilindro(p, 10, 4, 4, 9, pal.BEIGE, cuerpo=2)
    p.hlinea(10, 13, 7, tono(pal.BEIGE, 0))
    p.hlinea(10, 13, 10, tono(pal.BEIGE, 0))
    p.rect(20, 4, 23, 13, tono(pal.BEIGE, 2))
    p.hlinea(20, 23, 4, tono(pal.BEIGE, 3))
    p.hlinea(20, 23, 10, tono(pal.BEIGE, 1))
    # bornes con cables
    p.pset(11, 3, tono(acero, 3))
    p.linea(12, 3, 18, 2, tono(carbon := pal.CARBON, 2))
    p.pset(21, 3, tono(acero, 3))
    # placa de senales
    p.rect(16, 18, 23, 22, tono(amarillo, 2))
    p.hlinea(16, 23, 18, tono(amarillo, 3))
    p.hlinea(16, 23, 22, tono(amarillo, 0))
    p.pset(18, 20, tono(carbon, 0))
    p.pset(20, 20, tono(carbon, 0))
    # oxido de estacion
    p.pset(6, 26, tono(oxido, 2))
    p.pset(7, 27, tono(oxido, 1))
    p.pset(24, 27, tono(oxido, 1))


def panel_control_reactor(p):
    """Panel del reactor: mesa de mandos con pantallas, pilotos y palancas."""
    acero, hierro, carbon, cristal, beige = (pal.STEEL, pal.HIERRO,
                                            pal.CARBON, pal.CRISTAL,
                                            pal.BEIGE)
    # mesa inclinada
    p.poligono([(3, 14), (28, 14), (30, 20), (2, 20)], tono(beige, 2))
    p.hlinea(3, 28, 14, tono(beige, 3))
    p.hlinea(2, 30, 20, tono(beige, 0))
    # consola superior trasera
    p.rect(5, 5, 27, 13, tono(acero, 1))
    p.hlinea(5, 27, 5, tono(acero, 2))
    # pantallas de telemetria
    p.rect(7, 7, 14, 11, tono(carbon, 0))
    p.rect(8, 8, 13, 10, tono(cristal, 1))
    p.linea(8, 8, 10, 10, tono(pal.SULFATO, 3))
    p.rect(17, 7, 24, 11, tono(carbon, 0))
    p.rect(18, 8, 23, 10, tono(cristal, 1))
    p.linea(19, 9, 22, 9, tono(pal.SULFATO, 2))
    # pilotos de estado
    p.pset(7, 15, tono(pal.ROJO, 3))
    p.pset(9, 15, tono(pal.AMARILLO, 3))
    p.pset(11, 15, tono(pal.SULFATO, 3))
    p.pset(24, 15, tono(pal.ROJO, 2))
    # perillas
    p.elipse(18, 17, 1.8, 1.8, tono(carbon, 1), contorno=tono(carbon, 0))
    p.pset(17, 16, tono(carbon, 2))
    p.elipse(22, 17, 1.8, 1.8, tono(carbon, 1), contorno=tono(carbon, 0))
    p.pset(21, 16, tono(carbon, 2))
    # palancas de AZ-5
    p.vlinea(27, 14, 18, tono(pal.ROJO, 2))
    p.pset(27, 13, tono(pal.ROJO, 3))
    p.pset(26, 12, tono(pal.ROJO, 1))
    # canalete de papeles
    p.rect(2, 21, 30, 24, tono(acero, 2))
    p.hlinea(2, 30, 21, tono(acero, 3))
    p.hlinea(2, 30, 24, tono(hierro, 0))
    p.rect(4, 22, 9, 23, tono(beige, 1))
    # pie de la mesa
    p.vlinea(6, 24, 30, tono(hierro, 1))
    p.vlinea(24, 24, 30, tono(hierro, 1))
    p.hlinea(4, 27, 30, tono(hierro, 0))
    # etiqueta de la zona
    p.pset(12, 22, tono(pal.AMARILLO, 2))
    p.pset(13, 22, tono(pal.AMARILLO, 1))


def alternador_generador_diesel(p):
    """Alternador diesel: motor en V con deposito, radiador y polea."""
    oliva, acero, hierro, carbon, amarillo = (pal.OLIVA, pal.STEEL,
                                              pal.HIERRO, pal.CARBON,
                                              pal.AMARILLO)
    # motor ciego (V-block grande)
    p.rect(4, 9, 22, 25, tono(oliva, 2))
    p.hlinea(4, 22, 9, tono(oliva, 3))
    p.hlinea(4, 22, 25, tono(oliva, 0))
    # campana delantero V
    p.poligono([(8, 6), (18, 6), (22, 9), (4, 9)], tono(oliva, 3))
    p.vlinea(13, 6, 8, tono(oliva, 1))
    p.pset(13, 5, tono(hierro, 2))
    p.pset(14, 5, tono(hierro, 2))
    # tapa de valvulas
    p.rect(6, 11, 12, 17, tono(hierro, 2))
    p.hlinea(6, 12, 11, tono(hierro, 3))
    rejilla_lineas(p, 8, 13, 11, 16, tono(hierro, 3), tono(hierro, 0), 2)
    # alternador lateral (cilindro alado)
    p.rect(23, 12, 29, 22, tono(acero, 2))
    p.hlinea(23, 29, 12, tono(acero, 3))
    p.hlinea(23, 29, 22, tono(hierro, 0))
    rejilla_lineas(p, 25, 14, 28, 20, tono(acero, 1), tono(acero, 3), 3)
    # polea y correa
    p.elipse(23, 17, 2, 3, tono(carbon, 1), contorno=tono(hierro, 0))
    p.linea(23, 7, 30, 12, tono(carbon, 1))
    # deposito amarillo de combustible
    p.rect(15, 1, 21, 6, tono(amarillo, 2))
    p.hlinea(15, 21, 1, tono(amarillo, 3))
    p.hlinea(15, 21, 6, tono(amarillo, 0))
    # tuberia de escape
    p.linea(10, 1, 14, 5, tono(carbon, 2))
    p.pset(10, 1, tono(carbon, 0))
    # borne amarillo de alto voltaje
    p.pset(3, 11, tono(amarillo, 2))
    p.pset(2, 12, tono(amarillo, 1))
    # gasto de aceite
    p.pset(8, 26, tono(carbon, 1))
    p.pset(9, 27, tono(carbon, 0))


def estabilizador_voltaje(p):
    """Estabilizador de voltaje: torre con voltimetro y ventilas."""
    acero, hierro, carbon, beige = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.BEIGE)
    # torre
    p.rect(7, 6, 23, 26, tono(beige, 2))
    p.hlinea(7, 23, 6, tono(beige, 3))
    p.hlinea(7, 23, 26, tono(hierro, 0))
    p.vlinea(8, 7, 26, tono(beige, 3))
    # voltimetro analogico
    p.elipse(15, 12, 5, 4, tono(carbon, 0), contorno=tono(hierro, 1))
    p.hlinea(12, 18, 13, tono(pal.BEIGE, 2))
    for x in range(12, 19, 2):
        p.pset(x, 12, tono(pal.BEIGE, 3))
    p.linea(15, 14, 12, 11, tono(pal.ROJO, 3))
    p.elipse(15, 15, 0.8, 0.8, tono(acero, 4))
    # ventilas inferiores
    rejilla_lineas(p, 9, 19, 21, 24, tono(beige, 1), tono(carbon, 0), 2)
    # interruptor de barrita
    p.rect(9, 7, 11, 10, tono(hierro, 1))
    p.hlinea(9, 11, 7, tono(hierro, 2))
    p.rect(20, 7, 22, 10, tono(hierro, 1))
    p.hlinea(20, 22, 7, tono(hierro, 2))
    # luz indicadora
    p.pset(17, 8, tono(pal.SULFATO, 2))
    p.pset(18, 8, tono(pal.SULFATO, 1))
    # etiqueta de servicio
    p.rect(10, 26, 20, 28, tono(pal.AMARILLO, 2))
    p.hlinea(10, 20, 28, tono(pal.AMARILLO, 1))
    # cable de toma inferior
    p.linea(12, 29, 8, 31, tono(carbon, 2))
    p.linea(20, 29, 24, 31, tono(carbon, 2))
    # suciedad de tablero
    p.pset(9, 15, tono(pal.OXIDO, 1))


def bateria_ups_servidor(p):
    """Bateria UPS de rack: caja negra con frontal LED y bornes."""
    carbon, acero, hierro, rojo, amarillo = (pal.CARBON, pal.STEEL,
                                             pal.HIERRO, pal.ROJO,
                                             pal.AMARILLO)
    # caja rack
    p.rect(4, 7, 27, 26, tono(carbon, 1))
    p.hlinea(4, 27, 7, tono(carbon, 2))
    p.hlinea(4, 27, 26, tono(carbon, 0))
    p.vlinea(4, 7, 26, tono(hierro, 3))
    # frontal de rack con orejas
    p.rect(2, 9, 4, 24, tono(acero, 1))
    p.hlinea(2, 4, 9, tono(acero, 2))
    p.rect(27, 9, 29, 24, tono(acero, 1))
    p.hlinea(27, 29, 9, tono(acero, 2))
    p.pset(3, 10, tono(hierro, 4))
    p.pset(28, 10, tono(hierro, 4))
    # franja de LEDs de estado
    p.rect(7, 10, 24, 12, tono(carbon, 0))
    p.pset(8, 11, tono(pal.SULFATO, 3))
    p.pset(10, 11, tono(pal.SULFATO, 2))
    p.pset(12, 11, tono(amarillo, 3))
    p.pset(14, 11, tono(rojo, 2))
    p.pset(23, 11, tono(carbon, 2))
    # rejilla de ventilacion
    rejilla_lineas(p, 7, 15, 24, 23, tono(hierro, 1), tono(carbon, 0), 3)
    # boton de silencio
    p.elipse(25, 19, 1.6, 1.6, tono(acero, 3), contorno=tono(carbon, 0))
    # bornes superiores
    p.vlinea(9, 4, 7, tono(acero, 3))
    p.elipse(9, 4, 1.4, 1.4, tono(hierro, 3))
    p.vlinea(22, 4, 7, tono(acero, 3))
    p.elipse(22, 4, 1.4, 1.4, tono(hierro, 3))
    # pegatina de peligro
    p.rect(17, 4, 19, 6, tono(amarillo, 2))
    p.pset(18, 5, tono(carbon, 0))
    # polvo de servidor
    p.pset(9, 24, tono(pal.BEIGE, 0))
    p.pset(22, 25, tono(pal.BEIGE, 0))


def caja_disyuntores_trifasicos(p):
    """Caja de disyuntores: gabinete con palancas negras y rail."""
    acero, hierro, carbon, beige, rojo = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                          pal.BEIGE, pal.ROJO)
    # gabinete
    p.rect(4, 6, 28, 26, tono(acero, 1))
    p.hlinea(4, 28, 6, tono(acero, 2))
    p.hlinea(4, 28, 26, tono(hierro, 0))
    # rail DIN y disyuntores (3 columnas)
    p.hlinea(6, 26, 16, tono(hierro, 3))
    for k, x0 in enumerate((7, 13, 19)):
        p.rect(x0, 9, x0 + 4, 15, tono(carbon, 1))
        p.hlinea(x0, x0 + 4, 9, tono(carbon, 2))
        p.hlinea(x0, x0 + 4, 15, tono(carbon, 0))
        # palanca: arriba encendido
        p.rect(x0 + 1, 11, x0 + 3, 13, tono(carbon, 0))
        p.pset(x0 + 2, 10, tono(pal.SULFATO, 2))
    # medidor de la caja
    p.rect(6, 18, 12, 23, tono(carbon, 0))
    p.vlinea(9, 19, 22, tono(rojo, 2))
    p.hlinea(7, 11, 21, tono(pal.BEIGE, 2))
    # bloque de bornas inferiores
    p.rect(14, 18, 26, 23, tono(beige, 1))
    p.hlinea(14, 26, 18, tono(beige, 2))
    p.hlinea(14, 26, 23, tono(beige, 0))
    for x in (16, 20, 24):
        p.pset(x, 20, tono(acero, 3))
        p.vlinea(x, 24, 26, tono(carbon, 1))
    # sellos de precinto amarillo
    p.rect(5, 4, 8, 6, tono(pal.AMARILLO, 2))
    p.rect(24, 4, 27, 6, tono(pal.AMARILLO, 2))
    # quemado en un carril
    p.pset(21, 14, tono(carbon, 0))
    p.pset(22, 15, tono(carbon, 0))


def cable_telefonico(p):
    """Cable telefonico: carrete de cable trenzado con clavija RJ."""
    carbon, acero, hierro, oxido = pal.CARBON, pal.STEEL, pal.HIERRO, pal.OXIDO
    # bobina de cable vista de lado (tres vueltas apiladas)
    for k, yy in enumerate((13, 17, 21)):
        p.elipse(12, yy, 8, 3,
                 tono(carbon, 3) if k % 2 else tono(carbon, 1),
                 contorno=tono(carbon, 0))
    # cable colgante con clavija RJ
    p.linea(20, 12, 26, 8, tono(carbon, 2))
    p.pset(26, 8, tono(carbon, 0))
    p.rect(26, 4, 30, 7, tono(acero, 1))
    p.hlinea(26, 30, 4, tono(acero, 2))
    p.hlinea(26, 30, 7, tono(hierro, 0))
    for x in (27, 29):
        p.pset(x, 5, tono(pal.LATON, 3))
    # lata del cable que se descuelga
    p.linea(6, 24, 9, 27, tono(carbon, 2))
    p.linea(9, 27, 12, 28, tono(carbon, 1))
    # mordisqueo de rata (cable pelado)
    p.pset(12, 28, tono(pal.ROJO, 1))
    p.pset(13, 28, tono(pal.LATON, 2))
    # etiqueta del circuito
    p.rect(7, 10, 10, 12, tono(pal.BEIGE, 1))
    p.hlinea(7, 10, 12, tono(pal.BEIGE, 0))


def aislador_ceramico(p):
    """Aislador ceramico: campana blanca tallada con gancho de hierro."""
    beige, hierro, acero, carbon = (pal.BEIGE, pal.HIERRO, pal.STEEL,
                                    pal.CARBON)
    # gancho de suspension
    p.pset(16, 2, tono(acero, 3))
    p.vlinea(16, 3, 6, tono(acero, 3))
    p.vlinea(17, 3, 6, tono(acero, 1))
    p.pset(15, 2, tono(acero, 2))
    # campanas talladas de porcelana
    p.elipse(16, 12, 7, 7, tono(beige, 2), contorno=tono(beige, 0))
    p.elipse(16, 12, 9, 4, tono(beige, 1))
    p.elipse(16, 17, 8, 3, tono(beige, 2))
    p.elipse(16, 22, 6, 3, tono(beige, 1))
    p.elipse(16, 26, 4, 2, tono(beige, 2))
    p.hlinea(10, 22, 12, tono(beige, 0))
    # brillos de porcelana
    p.pset(11, 9, tono(beige, 3))
    p.pset(12, 8, tono(beige, 4))
    p.pset(13, 18, tono(beige, 3))
    # mancha de hollin en el hombro
    p.pset(20, 14, tono(carbon, 1))
    p.pset(21, 15, tono(carbon, 0))
    # fisura del viento
    p.pset(19, 20, tono(beige, 0))
    p.pset(20, 21, tono(beige, 0))
    p.pset(20, 19, tono(carbon, 1))


def fusible_porcelana(p):
    """Fusible de porcelana: cartucho blanco con vertidera y bornes."""
    beige, acero, hierro, carbon = (pal.BEIGE, pal.STEEL, pal.HIERRO,
                                    pal.CARBON)
    # cuerpo blanco estriado
    p.rect(8, 12, 23, 20, tono(beige, 2))
    p.hlinea(8, 23, 12, tono(beige, 3))
    p.hlinea(8, 23, 20, tono(beige, 0))
    for x in (11, 14, 17, 20):
        p.vlinea(x, 13, 19, tono(beige, 1))
    # vertidera metalica
    p.rect(4, 11, 8, 21, tono(hierro, 2))
    p.hlinea(4, 8, 11, tono(hierro, 3))
    p.hlinea(4, 8, 21, tono(hierro, 0))
    p.rect(23, 11, 27, 21, tono(hierro, 2))
    p.hlinea(23, 27, 11, tono(hierro, 3))
    p.hlinea(23, 27, 21, tono(hierro, 0))
    # lineas de rejilla en la vertidera
    for y in (14, 17):
        p.hlinea(4, 8, y, tono(hierro, 0))
        p.hlinea(23, 27, y, tono(hierro, 0))
    # bornes
    p.rect(2, 14, 4, 18, tono(acero, 2))
    p.hlinea(2, 4, 14, tono(acero, 3))
    p.rect(27, 14, 29, 18, tono(acero, 2))
    p.hlinea(27, 29, 14, tono(acero, 3))
    # ventana de hilo fundido
    p.rect(12, 14, 19, 18, tono(carbon, 0))
    p.linea(13, 16, 18, 16, tono(pal.LATON, 3))
    # fusible reventado (hilo roto)
    p.pset(15, 16, tono(carbon, 0))
    p.pset(16, 15, tono(pal.ROJO, 1))
    p.pset(17, 17, tono(carbon, 0))
    # suciedad de porcelana
    p.pset(10, 15, tono(pal.SULFATO, 0))
    p.pset(22, 18, tono(pal.SULFATO, 1))


def carcasa_enchufe(p):
    """Carcasa de enchufe: disco de baquel con dos polos y cable."""
    carbon, hierro, acero, beige = (pal.CARBON, pal.HIERRO, pal.STEEL,
                                    pal.BEIGE)
    # carcasa central
    p.elipse(14, 16, 8, 8, tono(carbon, 1), contorno=tono(carbon, 0))
    p.elipse(13, 14, 6, 6, tono(carbon, 2))
    # ojos de chapa (bornes)
    p.elipse(11, 15, 1.6, 1.6, tono(hierro, 3))
    p.elipse(14, 12, 1.6, 1.6, tono(hierro, 3))
    # tapa inferior con tornillo
    p.elipse(14, 16, 3, 3, tono(carbon, 0))
    # salida de cable al frente
    p.linea(20, 20, 25, 24, tono(carbon, 2))
    p.linea(21, 21, 26, 25, tono(carbon, 1))
    p.pset(26, 25, tono(carbon, 0))
    # clavija al extremo (dos rejas)
    p.rect(27, 26, 29, 28, tono(acero, 1))
    p.hlinea(27, 29, 26, tono(acero, 2))
    p.pset(27, 29, tono(hierro, 2))
    p.pset(29, 28, tono(hierro, 2))
    # zapata de pared con tornilleria
    p.rect(4, 22, 9, 27, tono(beige, 1))
    p.hlinea(4, 9, 22, tono(beige, 2))
    p.hlinea(4, 9, 27, tono(beige, 0))
    p.pset(5, 23, tono(hierro, 3))
    p.pset(8, 26, tono(hierro, 3))
    # chispas eléctricas
    p.pset(11, 20, tono(amarillo := pal.AMARILLO, 3))
    p.pset(10, 22, tono(amarillo, 2))
    # suciedad de grafito
    p.pset(19, 9, tono(beige, 0))


def tubo_fluorescente(p):
    """Tubo fluorescente: vidrio opaco con capuchones y bornes."""
    cristal, acero, hierro, carbon = (pal.CRISTAL, pal.STEEL, pal.HIERRO,
                                      pal.CARBON)
    # vidrio
    p.rect(5, 12, 26, 19, tono(cristal, 2))
    p.hlinea(5, 26, 12, tono(cristal, 3))
    p.hlinea(5, 26, 19, tono(cristal, 1))
    # brillo interno (fosforo)
    p.rect(7, 14, 24, 17, tono(cristal, 3))
    p.hlinea(7, 24, 14, tono(cristal, 4))
    p.pset(9, 14, tono(pal.SULFATO, 2))
    p.pset(10, 15, tono(pal.SULFATO, 1))
    # extremos acanalados
    p.rect(1, 10, 5, 21, tono(hierro, 2))
    p.hlinea(1, 5, 10, tono(hierro, 3))
    p.hlinea(1, 5, 21, tono(hierro, 0))
    for y in (13, 16, 19):
        p.hlinea(1, 5, y, tono(hierro, 1))
    p.rect(26, 10, 30, 21, tono(hierro, 2))
    p.hlinea(26, 30, 10, tono(hierro, 3))
    p.hlinea(26, 30, 21, tono(hierro, 0))
    for y in (13, 16, 19):
        p.hlinea(26, 30, y, tono(hierro, 1))
    # bornes de contacto
    p.pset(2, 15, tono(acero, 4))
    p.pset(2, 18, tono(acero, 4))
    p.pset(29, 15, tono(acero, 4))
    p.pset(29, 18, tono(acero, 4))
    # pinzas del soporte
    p.rect(14, 9, 17, 12, tono(hierro, 1))
    p.hlinea(14, 17, 9, tono(hierro, 2))
    p.rect(14, 19, 17, 22, tono(hierro, 1))
    # manchas de mercurio
    p.pset(20, 16, tono(carbon, 1))
    p.pset(21, 15, tono(carbon, 2))
    # extremo fundido del tubo
    p.pset(6, 15, tono(carbon, 1))
    p.pset(7, 16, tono(carbon, 2))


def placa_disipadora_aluminio(p):
    """Disipador de aluminio: base con aletas dentadas y tornillo."""
    acero, hierro, carbon, beige = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.BEIGE)
    # base
    p.rect(5, 20, 27, 27, tono(acero, 2))
    p.hlinea(5, 27, 20, tono(acero, 3))
    p.hlinea(5, 27, 27, tono(hierro, 0))
    # aletas verticales dentadas
    for x0 in (7, 11, 15, 19, 23):
        p.poligono([(x0, 20), (x0 + 2, 20), (x0 + 3, 9), (x0 + 1, 7),
                    (x0 - 1, 9)], tono(acero, 3))
        p.linea(x0 + 1, 8, x0 + 2, 20, tono(acero, 1))
        p.pset(x0 + 1, 7, tono(acero, 4))
    # rayita de zocalo
    p.hlinea(6, 26, 25, tono(acero, 1))
    # tornillo central
    p.elipse(16, 23, 1.6, 1.6, tono(hierro, 3), contorno=tono(carbon, 0))
    p.pset(16, 22, tono(acero, 4))
    p.linea(15, 23, 17, 23, tono(carbon, 0))
    # pasta termica expuesta
    p.rect(10, 22, 13, 24, tono(pal.SULFATO, 1))
    # pastilla de silicio quemada al lado
    p.rect(20, 22, 23, 24, tono(carbon, 0))
    p.pset(21, 23, tono(carbon, 1))
    # arista irrompible de aluminio
    p.pset(6, 19, tono(acero, 4))
    p.pset(27, 20, tono(acero, 1))


DIBUJOS = {
    "transformador_subestacion": transformador_subestacion,
    "panel_control_reactor": panel_control_reactor,
    "alternador_generador_diesel": alternador_generador_diesel,
    "estabilizador_voltaje": estabilizador_voltaje,
    "bateria_ups_servidor": bateria_ups_servidor,
    "caja_disyuntores_trifasicos": caja_disyuntores_trifasicos,
    "cable_telefonico": cable_telefonico,
    "aislador_ceramico": aislador_ceramico,
    "fusible_porcelana": fusible_porcelana,
    "carcasa_enchufe": carcasa_enchufe,
    "tubo_fluorescente": tubo_fluorescente,
    "placa_disipadora_aluminio": placa_disipadora_aluminio,
}
