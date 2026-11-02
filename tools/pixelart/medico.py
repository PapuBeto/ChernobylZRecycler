# -*- coding: utf-8 -*-
"""Equipo medico y de laboratorio: pixel art 32x32.

Paleta de blancos envejecidos (BEIGE), acero quirurgico y rojo de senales.
"""
from __future__ import annotations

from tools.pixelart import pal
from tools.pixelart.px import P, tono
from tools.pixelart.formas import cilindro, rejilla_lineas


def desfibrilador_portatil(p):
    """Desfibrilador portatil: maleta con pantalla, palas y“One LED."""
    beige, carbon, rojo, acero = (pal.BEIGE, pal.CARBON, pal.ROJO,
                                  pal.STEEL)
    # maleta
    p.rect(4, 7, 27, 26, tono(beige, 2))
    p.hlinea(4, 27, 7, tono(beige, 3))
    p.hlinea(4, 27, 26, tono(beige, 0))
    p.vlinea(4, 7, 26, tono(beige, 3))
    # asa
    p.rect(12, 4, 20, 6, tono(carbon, 1))
    p.hlinea(12, 20, 4, tono(carbon, 2))
    # pantalla ECG
    p.rect(7, 10, 18, 18, tono(carbon, 0))
    p.rect(8, 11, 17, 17, tono(pal.CRISTAL, 1))
    p.hlinea(8, 17, 11, tono(pal.CRISTAL, 2))
    # traza del latido
    p.linea(9, 15, 13, 15, tono(pal.SULFATO, 3))
    p.linea(13, 15, 14, 12, tono(pal.SULFATO, 3))
    p.linea(14, 12, 15, 18, tono(pal.SULFATO, 3))
    p.linea(15, 18, 16, 14, tono(pal.SULFATO, 3))
    # panel de carga
    p.rect(20, 10, 25, 12, tono(rojo, 2))
    p.hlinea(20, 25, 10, tono(rojo, 3))
    p.hlinea(20, 25, 12, tono(rojo, 0))
    rejilla_lineas(p, 20, 15, 25, 20, tono(beige, 1), tono(beige, 0), 2)
    # palas colgando
    p.elipse(3, 24, 2.4, 3, tono(acero, 3), contorno=tono(carbon, 0))
    p.pset(3, 24, tono(pal.CRISTAL, 3))
    p.linea(29, 20, 31, 24, tono(carbon, 2))
    p.elipse(30, 25, 2, 2.4, tono(acero, 2), contorno=tono(carbon, 0))
    # barra de carga llena
    for x in (21, 23, 25):
        p.pset(x, 15, tono(pal.SULFATO, 2))


def microscopio_quirurgico(p):
    """Microscopio quirurgico: columna, ocular binocular y platina."""
    carbon, acero, hierro, beige = (pal.CARBON, pal.STEEL, pal.HIERRO,
                                    pal.BEIGE)
    # base pesada
    p.poligono([(5, 25), (16, 21), (22, 21), (27, 25), (27, 27), (5, 27)],
               tono(carbon, 1))
    p.hlinea(5, 27, 27, tono(carbon, 0))
    # brazo curvo
    p.poligono([(18, 6), (23, 10), (24, 20), (21, 20), (20, 12), (16, 8)],
               tono(acero, 1))
    p.poligono([(18, 6), (20, 8), (18, 10), (16, 8)], tono(acero, 3))
    # columna vertical
    p.rect(14, 8, 17, 21, tono(acero, 2))
    p.hlinea(14, 17, 8, tono(acero, 3))
    p.hlinea(14, 17, 21, tono(hierro, 0))
    # tubo binocular
    p.rect(6, 5, 15, 9, tono(hierro, 1))
    p.hlinea(6, 15, 5, tono(hierro, 2))
    p.rect(4, 4, 7, 8, tono(hierro, 2))         # ocular izq
    p.rect(4, 4, 6, 8, tono(hierro, 2))
    p.hlinea(4, 6, 4, tono(hierro, 3))
    p.pset(4, 4, tono(pal.BEIGE, 2))
    p.pset(10, 4, tono(pal.BEIGE, 2))             # ocular derecho
    # objetivo descendente
    p.rect(14, 9, 17, 13, tono(hierro, 2))
    p.pset(15, 13, tono(carbon, 0))
    p.pset(16, 13, tono(carbon, 0))
    # platina con muestra
    p.rect(8, 17, 15, 19, tono(carbon, 0))
    p.rect(9, 17, 14, 18, tono(pal.CRISTAL, 2))
    p.hlinea(9, 14, 17, tono(pal.CRISTAL, 3))
    # rueda de enfoque
    p.elipse(21, 14, 2.4, 2.4, tono(hierro, 2), contorno=tono(hierro, 0))
    p.pset(22, 13, tono(hierro, 4))
    # reflejo de quirófano
    p.pset(6, 24, tono(beige, 3))
    p.pset(7, 24, tono(beige, 2))


def ventilador_pulmonar_uci(p):
    """Ventilador pulmonar: torre con pantalla, manguera y humidificador."""
    beige, carbon, acero, cristal = (pal.BEIGE, pal.CARBON, pal.STEEL,
                                     pal.CRISTAL)
    # carro
    p.rect(5, 6, 24, 24, tono(beige, 2))
    p.hlinea(5, 24, 6, tono(beige, 3))
    p.hlinea(5, 24, 24, tono(beige, 0))
    # pantalla superior
    p.rect(8, 9, 15, 15, tono(carbon, 0))
    p.rect(9, 10, 14, 14, tono(cristal, 1))
    p.hlinea(9, 14, 10, tono(cristal, 2))
    p.linea(9, 12, 14, 12, tono(pal.SULFATO, 2))
    p.pset(10, 12, tono(rojo := pal.ROJO, 3))
    # botonera
    rejilla_lineas(p, 17, 10, 23, 14, tono(beige, 1), tono(beige, 0), 2)
    p.pset(18, 11, tono(rojo, 2))
    p.pset(20, 11, tono(pal.SULFATO, 2))
    # humidificador con agua
    cilindro(p, 10, 18, 6, 5, acero, cuerpo=1)
    p.rect(11, 19, 15, 21, tono(cristal, 0))
    p.hlinea(11, 15, 21, tono(cristal, 1))
    p.elipse(13, 19, 1, 1, tono(cristal, 4))
    # manguera corrugada
    for x, y in ((19, 17), (20, 16), (21, 15), (22, 14), (23, 13), (24, 12),
                 (25, 11), (26, 10), (27, 9), (28, 8)):
        p.pset(x, y, tono(carbon, 2))
    p.pset(28, 9, tono(carbon, 3))
    p.pset(27, 7, tono(carbon, 2))
    # ruedas
    p.elipse(8, 27, 2, 2, tono(carbon, 1), contorno=tono(carbon, 0))
    p.elipse(21, 27, 2, 2, tono(carbon, 1), contorno=tono(carbon, 0))
    # etiqueta de oxigeno
    p.pset(6, 19, tono(pal.SULFATO, 2))
    p.pset(7, 19, tono(pal.SULFATO, 1))


def monitor_signos_vitales(p):
    """Monitor de signos vitales: pantalla doble con ondas y base."""
    carbon, cristal, beige, rojo = (pal.CARBON, pal.CRISTAL, pal.BEIGE,
                                    pal.ROJO)
    # carcasa
    p.rect(4, 6, 27, 22, tono(beige, 2))
    p.hlinea(4, 27, 6, tono(beige, 3))
    p.hlinea(4, 27, 22, tono(beige, 0))
    p.vlinea(4, 6, 22, tono(beige, 3))
    # pantalla principal
    p.rect(6, 8, 22, 18, tono(carbon, 0))
    p.rect(7, 9, 21, 17, tono(cristal, 1))
    p.hlinea(7, 21, 9, tono(cristal, 2))
    # onda de pulso (verde)
    p.linea(8, 14, 12, 14, tono(pal.SULFATO, 3))
    p.linea(12, 14, 13, 11, tono(pal.SULFATO, 3))
    p.linea(13, 11, 14, 17, tono(pal.SULFATO, 3))
    p.linea(14, 17, 15, 13, tono(pal.SULFATO, 3))
    p.linea(15, 13, 20, 13, tono(pal.SULFATO, 2))
    # barras de datos a la derecha
    p.vlinea(25, 10, 20, tono(rojo, 1))
    p.rect(24, 12, 26, 14, tono(rojo, 2))
    p.rect(24, 16, 26, 18, tono(pal.SULFATO, 2))
    # botones bajo pantalla
    rejilla_lineas(p, 7, 20, 21, 21, tono(beige, 1), tono(beige, 0), 2)
    # pie con brazo
    p.vlinea(12, 23, 26, tono(acero := pal.STEEL, 2))
    p.hlinea(9, 15, 26, tono(acero, 1))
    p.hlinea(9, 15, 27, tono(carbon, 0))
    # luz de alarma apagada
    p.pset(24, 7, tono(carbon, 1))
    # suciedad en el bisel
    p.pset(6, 21, tono(pal.OXIDO, 1))


def autoclave_esterilizacion(p):
    """Autoclave de esterilizacion: caldera con puerta circular y manometro."""
    acero, hierro, carbon, beige, rojo = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                          pal.BEIGE, pal.ROJO)
    # cuerpo cilindrico
    p.rect(6, 8, 24, 26, tono(acero, 2))
    p.hlinea(6, 24, 8, tono(acero, 3))
    p.hlinea(6, 24, 26, tono(hierro, 0))
    p.vlinea(7, 9, 26, tono(acero, 3))
    # puerta circular con bornera
    p.elipse(15, 17, 6, 7, tono(acero, 1), contorno=tono(hierro, 0))
    p.elipse(14, 16, 4.4, 5, tono(acero, 3))
    # asa de rueda (manija circular)
    p.elipse(15, 17, 2.4, 2.4, tono(hierro, 2), contorno=tono(hierro, 0))
    p.linea(15, 15, 15, 20, tono(acero, 4))
    p.pset(12, 17, tono(acero, 4))
    p.pset(18, 17, tono(acero, 4))
    # perilla del manometro arriba
    p.elipse(24, 6, 2.4, 2, tono(beige, 2), contorno=tono(hierro, 0))
    p.pset(23, 5, tono(carbon, 1))
    p.linea(23, 6, 25, 5, tono(carbon, 0))
    # panel de control lateral
    p.rect(25, 10, 28, 18, tono(carbon, 1))
    p.hlinea(25, 28, 10, tono(carbon, 2))
    p.pset(26, 12, tono(pal.SULFATO, 2))
    p.pset(26, 15, tono(rojo, 2))
    # rejilla de vapor
    rejilla_lineas(p, 8, 23, 13, 26, tono(acero, 1), tono(carbon, 0), 2)
    # vapor escapando
    p.pset(24, 3, tono(pal.BEIGE, 3))
    p.pset(25, 2, tono(pal.BEIGE, 2))
    # mancha de calcario
    p.pset(9, 24, tono(pal.SULFATO, 1))


def camilla_aislamiento(p):
    """Camilla de aislamiento: mesa con colchon, barandas y ruedas."""
    beige, acero, hierro, carbon, cristal = (pal.BEIGE, pal.STEEL,
                                             pal.HIERRO, pal.CARBON,
                                             pal.CRISTAL)
    # colchon con sabana
    p.rect(4, 12, 28, 17, tono(beige, 3))
    p.hlinea(4, 28, 12, tono(beige, 4))
    p.hlinea(4, 28, 17, tono(beige, 1))
    # almohada
    p.rect(5, 10, 11, 13, tono(beige, 4))
    p.hlinea(5, 11, 10, tono(beige, 2))
    # plato de mesa
    p.rect(3, 17, 28, 19, tono(acero, 2))
    p.hlinea(3, 28, 17, tono(acero, 3))
    p.hlinea(3, 28, 19, tono(hierro, 0))
    # patas
    for x0 in (6, 24):
        p.vlinea(x0, 19, 27, tono(acero, 1))
        p.vlinea(x0 + 1, 19, 27, tono(acero, 0))
    # baranda abatible izq
    p.vlinea(2, 8, 14, tono(acero, 3))
    p.hlinea(2, 5, 8, tono(acero, 4))
    p.hlinea(2, 3, 14, tono(acero, 1))
    # ruedas con freno
    for cx in (7, 25):
        p.elipse(cx, 29, 2, 2, tono(carbon, 1), contorno=tono(carbon, 0))
        p.pset(cx, 29, tono(acero, 4))
        p.pset(cx + 1, 28, tono(carbon, 0))
    # portabandeja lateral
    p.rect(23, 15, 29, 16, tono(acero, 1))
    p.hlinea(23, 29, 15, tono(acero, 2))
    # sello de plastico aislante (cinta)
    p.rect(14, 13, 22, 15, tono(cristal, 0))
    p.hlinea(14, 22, 13, tono(cristal, 1))
    # mancha biologica en el colchon
    p.pset(19, 15, tono(pal.OXIDO, 2))
    p.pset(20, 15, tono(pal.OXIDO, 1))


def delantal_laboratorio(p):
    """Delantal de plomo: cuerpo acampanado con correa y bolsillo."""
    verde, hierro, carbon, amarillo = (pal.OLIVA, pal.HIERRO, pal.CARBON,
                                       pal.AMARILLO)
    # cuerpo
    p.poligono([(9, 8), (22, 8), (26, 28), (5, 28)], tono(verde, 2))
    p.hlinea(9, 22, 8, tono(verde, 3))
    p.hlinea(5, 26, 28, tono(verde, 0))
    # peto superior brillante
    p.rect(9, 8, 22, 14, tono(verde, 3))
    p.hlinea(9, 22, 8, tono(verde, 4))
    # cuello con broche
    p.rect(13, 4, 18, 8, tono(verde, 1))
    p.hlinea(13, 18, 4, tono(verde, 2))
    p.pset(15, 5, tono(acero := pal.STEEL, 4))
    p.pset(16, 5, tono(acero, 4))
    # bolsillo central
    p.rect(12, 17, 19, 22, tono(verde, 1))
    p.hlinea(12, 19, 17, tono(verde, 0))
    p.hlinea(12, 19, 22, tono(verde, 0))
    # plumero de lapicero en el bolsillo
    p.vlinea(17, 14, 17, tono(amarillo, 2))
    p.pset(17, 13, tono(acero, 4))
    # correas laterales
    p.vlinea(5, 14, 24, tono(verde, 1))
    p.vlinea(26, 14, 24, tono(verde, 1))
    # etiqueta de radiacion pequena
    p.pset(23, 24, tono(amarillo, 2))
    p.pset(24, 24, tono(amarillo, 3))
    # arista desgastada
    p.pset(6, 26, tono(verde, 1))
    p.pset(25, 26, tono(verde, 1))


def gradilla_tubos_ensayo(p):
    """Gradilla de tubos: bastidor con 4 tubos de cristal y labios."""
    beige, cristal, acero, carbon = (pal.BEIGE, pal.CRISTAL, pal.STEEL,
                                     pal.CARBON)
    # bastidor
    p.rect(5, 12, 26, 16, tono(beige, 2))
    p.hlinea(5, 26, 12, tono(beige, 3))
    p.hlinea(5, 26, 16, tono(beige, 0))
    p.rect(5, 24, 26, 28, tono(beige, 1))
    p.hlinea(5, 26, 24, tono(beige, 2))
    p.hlinea(5, 26, 28, tono(beige, 0))
    for x in (14, 15):
        p.vlinea(x, 12, 28, tono(beige, 1))
    # tubos de cristal
    for x0 in (7, 12, 18, 23):
        p.rect(x0, 6, x0 + 3, 26, tono(cristal, 1))
        p.rect(x0, 6, x0, 25, tono(cristal, 3))       # brillo vertical
        p.vlinea(x0 + 3, 6, 26, tono(cristal, 0))
        p.pset(x0 + 1, 6, tono(cristal, 4))
        # contenido (liquido distinto)
        if x0 == 7:
            p.rect(x0, 18, x0 + 3, 25, tono(pal.ROJO, 2))
            p.hlinea(x0, x0 + 3, 18, tono(pal.ROJO, 3))
        elif x0 == 12:
            p.rect(x0, 20, x0 + 3, 25, tono(pal.SULFATO, 2))
        elif x0 == 18:
            p.rect(x0, 16, x0 + 3, 25, tono(pal.SULFATO, 3))
        elif x0 == 23:
            p.rect(x0, 21, x0 + 3, 25, tono(carbon, 2))
        p.hlinea(x0, x0 + 3, 25, tono(cristal, 0))
    # espuma de tapon
    p.pset(8, 5, tono(beige, 1))
    p.pset(24, 5, tono(carbon, 1))
    # etiqueta al correo
    p.rect(13, 19, 17, 23, tono(beige, 0))
    p.rect(14, 20, 16, 22, tono(beige, 3))


def rollo_vendas_yodo(p):
    """Rollo de vendas con botella de yodo apoyada: paquete de botiquin."""
    beige, acero, cristal, amarillo, rojo = (pal.BEIGE, pal.STEEL,
                                             pal.CRISTAL, pal.AMARILLO,
                                             pal.ROJO)
    # rollo de hilo blanco (cilindro con vueltas)
    p.rect(4, 10, 21, 24, tono(beige, 2))
    p.poligono([(4, 10), (21, 10), (24, 13), (1, 13)], tono(beige, 3))
    p.hlinea(4, 21, 24, tono(beige, 0))
    # vueltas de tela
    for y in range(12, 24, 3):
        p.hlinea(4, 21, y, tono(beige, 1))
        p.pset(18, y, tono(beige, 4))
    # nudo y punta colgante
    p.linea(21, 12, 27, 15, tono(beige, 3))
    p.linea(20, 14, 26, 18, tono(beige, 1))
    p.linea(26, 18, 28, 22, tono(beige, 2))
    # botella de yodo
    p.rect(24, 14, 31, 14, (0, 0, 0, 0))            # limpieza (no-op real)
    p.rect(24, 15, 29, 28, tono(cristal, 1))
    p.vlinea(25, 16, 28, tono(cristal, 2))
    p.vlinea(29, 16, 28, tono(cristal, 0))
    p.rect(24, 22, 29, 28, tono(acero, 1))          # yodo denso
    p.hlinea(24, 29, 22, tono(acero, 0))
    p.rect(26, 11, 28, 14, tono(beige, 1))          # cuello
    p.rect(25, 9, 29, 11, tono(rojo, 2))            # tapon
    p.hlinea(25, 29, 9, tono(rojo, 3))
    # etiqueta amarilla
    p.rect(25, 17, 28, 20, tono(amarillo, 2))
    p.hlinea(25, 28, 20, tono(amarillo, 1))
    # cruz medica estampada
    p.pset(26, 18, tono(rojo, 2))
    p.pset(27, 18, tono(rojo, 2))
    p.pset(26, 19, tono(rojo, 2))
    p.pset(27, 19, tono(rojo, 2))


def sabana_quirurgica(p):
    """Sabana enpaquetada: fardo de tela blanco con cinta verde."""
    beige, carbon, verde, acero = (pal.BEIGE, pal.CARBON, pal.SULFATO,
                                   pal.STEEL)
    # fardo
    p.poligono([(6, 12), (22, 8), (28, 14), (26, 26), (10, 28), (3, 20)],
               tono(beige, 2))
    p.poligono([(6, 12), (22, 8), (24, 11), (8, 15)], tono(beige, 3))
    # pliegues del envoltorio
    p.linea(8, 15, 12, 27, tono(beige, 1))
    p.linea(16, 10, 24, 25, tono(beige, 1))
    p.linea(21, 10, 27, 20, tono(beige, 1))
    # cinta de esterilizacion con cucheadas
    p.linea(6, 20, 14, 22, tono(verde, 3))
    p.linea(14, 22, 27, 16, tono(verde, 3))
    for x, y in ((9, 21), (13, 22), (18, 21), (24, 18)):
        p.pset(x, y, tono(verde, 4))
    # marca de esterilizado
    p.pset(20, 19, tono(carbon, 1))
    # broche metalico
    p.pset(15, 12, tono(acero, 3))
    p.pset(16, 13, tono(acero, 4))
    # esquinas con hierro de unos
    p.pset(7, 13, tono(beige, 1))
    p.pset(27, 12, tono(beige, 0))


def bata_paciente(p):
    """Bata de paciente: bata colgada en gancho con cuello en V."""
    verde, beige, hierro, carbon = (pal.SULFATO, pal.BEIGE, pal.HIERRO,
                                    pal.CARBON)
    # gancho
    p.elipse(16, 3, 1.4, 1.4, tono(hierro, 3), contorno=tono(hierro, 0))
    p.pset(16, 4, (0, 0, 0, 0))
    p.vlinea(16, 4, 6, tono(hierro, 2))
    # cuerpo de la bata (trapecio colgado)
    p.poligono([(8, 20), (12, 13), (20, 13), (24, 20), (24, 28), (8, 28)],
               tono(beige, 2))
    p.hlinea(8, 24, 28, tono(beige, 0))
    p.hlinea(12, 20, 16, tono(beige, 3))
    # cuello en V
    p.poligono([(12, 13), (16, 9), (20, 13)], tono(beige, 3))
    p.linea(12, 13, 16, 9, tono(carbon, 0))
    p.linea(20, 13, 16, 9, tono(carbon, 0))
    p.vlinea(16, 9, 13, tono(beige, 0))
    # mangas cortas caidas
    p.rect(3, 17, 9, 22, tono(beige, 2))
    p.hlinea(3, 9, 17, tono(beige, 3))
    p.hlinea(3, 9, 22, tono(beige, 0))
    p.rect(23, 17, 29, 22, tono(beige, 2))
    p.hlinea(23, 29, 17, tono(beige, 3))
    p.hlinea(23, 29, 22, tono(beige, 0))
    # cordones de la cintura
    p.hlinea(10, 22, 21, tono(carbon, 1))
    p.linea(10, 21, 8, 24, tono(carbon, 0))
    p.linea(22, 21, 24, 24, tono(carbon, 0))
    # pliegues de tela
    p.linea(14, 17, 13, 27, tono(beige, 1))
    p.linea(19, 17, 20, 27, tono(beige, 1))
    # mancha de proceso
    p.pset(11, 25, tono(pal.OXIDO, 1))
    p.pset(22, 26, tono(pal.OXIDO, 2))


def bandeja_instrumentos(p):
    """Bandeja de inox con instrumental: pinzas, tijeras, bisturí."""
    acero, hierro, carbon, cristal = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                      pal.CRISTAL)
    # bandeja con labio
    p.rect(3, 13, 29, 26, tono(acero, 2))
    p.hlinea(3, 29, 13, tono(acero, 3))
    p.hlinea(3, 29, 26, tono(hierro, 0))
    p.rect(2, 14, 30, 15, tono(acero, 3))
    # tela esteril de fondo
    p.rect(4, 16, 28, 25, tono(cristal, 0))
    p.hlinea(4, 28, 16, tono(cristal, 1))
    # pinzas
    p.linea(6, 18, 12, 24, tono(acero, 3))
    p.linea(7, 18, 13, 24, tono(acero, 1))
    p.pset(6, 17, tono(carbon, 1))
    p.pset(7, 17, tono(carbon, 1))
    # tijeras abiertas
    p.linea(15, 18, 20, 24, tono(acero, 3))
    p.linea(19, 18, 14, 24, tono(acero, 2))
    p.elipse(13, 25, 1.4, 1.4, (0, 0, 0, 0))
    p.elipse(21, 25, 1.4, 1.4, (0, 0, 0, 0))
    p.pset(13, 25, tono(acero, 4))
    p.pset(21, 25, tono(acero, 4))
    # bisturi
    p.linea(23, 18, 27, 23, tono(acero, 3))
    p.linea(24, 18, 28, 23, tono(hierro, 0))
    p.pset(28, 24, tono(acero, 4))
    # brillo de vidrio
    p.linea(5, 20, 8, 17, tono(acero, 4))
    # gota de sangre en la bandeja
    p.pset(17, 26, tono(pal.ROJO, 2))
    p.pset(18, 26, tono(pal.ROJO, 1))


def soporte_suero(p):
    """Soporte de suero: pie con ruedas, varetas y bolsa colgante."""
    acero, hierro, carbon, cristal, beige = (pal.STEEL, pal.HIERRO,
                                             pal.CARBON, pal.CRISTAL,
                                             pal.BEIGE)
    # poste central con brazos
    p.vlinea(18, 5, 24, tono(acero, 2))
    p.vlinea(19, 5, 24, tono(acero, 0))
    p.hlinea(7, 26, 5, tono(acero, 3))
    p.hlinea(10, 24, 11, tono(acero, 1))
    # bolsa de suero colgada del brazo
    p.vlinea(11, 6, 12, tono(carbon, 2))
    p.rect(7, 12, 16, 24, tono(cristal, 1))
    p.vlinea(8, 13, 24, tono(cristal, 2))
    p.vlinea(16, 13, 24, tono(cristal, 0))
    p.rect(7, 17, 16, 24, tono(cristal, 0))
    p.hlinea(7, 16, 19, tono(cristal, 2))
    p.hlinea(7, 16, 17, tono(cristal, 2))
    # ventana de llenado
    p.rect(8, 12, 15, 16, tono(cristal, 3))
    p.hlinea(8, 15, 12, tono(cristal, 4))
    # burbujas de aire
    p.pset(10, 20, tono(cristal, 3))
    p.pset(12, 21, tono(cristal, 4))
    # salida inferior y linea
    p.pset(11, 25, tono(carbon, 2))
    p.linea(11, 25, 7, 28, tono(carbon, 1))
    # pie en estrella
    for x0, y0, x1, y1 in ((18, 24, 8, 30), (18, 24, 28, 30),
                           (18, 24, 25, 29), (18, 24, 13, 31)):
        p.linea(x0, y0, x1, y1, tono(acero, 1))
    # ruedas de la base
    for cx, cy in ((7, 30), (12, 31), (25, 29), (29, 30)):
        p.elipse(cx, cy, 1.4, 1.4, tono(carbon, 1), contorno=tono(carbon, 0))

def bolsa_desechos_biologicos(p):
    """Bolsa de residuos biologicos: saco atado con cruz de bioseguridad."""
    amarillo, carbon, rojo, hierro = (pal.AMARILLO, pal.CARBON, pal.ROJO,
                                      pal.HIERRO)
    # saco de residuos
    p.poligono([(8, 10), (24, 10), (27, 26), (5, 26)], tono(amarillo, 2))
    p.hlinea(8, 24, 10, tono(amarillo, 3))
    p.hlinea(5, 27, 26, tono(amarillo, 0))
    # pliegues del plastico
    p.linea(11, 11, 9, 26, tono(amarillo, 1))
    p.linea(21, 11, 24, 26, tono(amarillo, 1))
    p.linea(15, 11, 14, 26, tono(amarillo, 3))
    # nudo atado
    p.pset(13, 7, tono(amarillo, 3))
    p.pset(19, 7, tono(amarillo, 3))
    p.rect(13, 5, 19, 9, tono(amarillo, 2))
    p.hlinea(13, 19, 5, tono(amarillo, 4))
    p.linea(15, 2, 17, 5, tono(amarillo, 3))
    p.pset(17, 2, tono(amarillo, 4))
    # cruz de bioseguridad (circulos)
    p.elipse(16, 18, 5, 5, tono(amarillo, 3), contorno=tono(carbon, 0))
    p.elipse(16, 18, 3.2, 3.2, (0, 0, 0, 0))
    p.elipse(16, 18, 2.2, 2.2, tono(amarillo, 1))
    p.pset(14, 16, tono(carbon, 0))
    p.pset(18, 16, tono(carbon, 0))
    p.pset(16, 20, tono(carbon, 0))
    # cordon colgante
    p.linea(24, 10, 29, 7, tono(amarillo, 1))
    # marcas de residuo
    p.pset(9, 24, tono(pal.OXIDO, 1))
    p.pset(25, 25, tono(pal.BEIGE, 1))


def muleta_aluminio(p):
    """Muleta de aluminio: tubo con pomo, doble travesaño y goma."""
    acero, hierro, carbon, beige = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.BEIGE)
    # pomo axilar acolchado
    p.rect(9, 3, 21, 7, tono(beige, 3))
    p.hlinea(9, 21, 3, tono(beige, 4))
    p.hlinea(9, 21, 7, tono(beige, 1))
    # horquilla del travesaño
    p.poligono([(12, 7), (18, 7), (16, 12), (14, 12)], tono(acero, 2))
    # tubo principal
    p.rect(14, 7, 17, 26, tono(acero, 2))
    p.hlinea(14, 17, 7, tono(acero, 4))
    p.vlinea(14, 8, 26, tono(acero, 5))
    p.vlinea(17, 8, 26, tono(acero, 1))
    p.hlinea(14, 17, 26, tono(hierro, 0))
    # anillas de reglaje
    p.rect(13, 12, 18, 13, tono(hierro, 2))
    p.hlinea(13, 18, 12, tono(hierro, 3))
    p.pset(19, 12, tono(carbon, 1))
    p.rect(13, 18, 18, 19, tono(hierro, 2))
    p.hlinea(13, 18, 18, tono(hierro, 3))
    # mango grip
    p.rect(11, 15, 20, 17, tono(carbon, 1))
    p.hlinea(11, 20, 15, tono(carbon, 2))
    p.hlinea(11, 20, 17, tono(carbon, 0))
    # punta de goma
    p.rect(13, 26, 18, 29, tono(carbon, 1))
    p.hlinea(13, 18, 29, tono(carbon, 0))
    p.hlinea(12, 19, 28, tono(carbon, 0))
    # herrumbre del aluminio
    p.pset(18, 22, tono(pal.OXIDO, 1))
    p.pset(19, 23, tono(pal.OXIDO, 0))


DIBUJOS = {
    "desfibrilador_portatil": desfibrilador_portatil,
    "microscopio_quirurgico": microscopio_quirurgico,
    "ventilador_pulmonar_uci": ventilador_pulmonar_uci,
    "monitor_signos_vitales": monitor_signos_vitales,
    "autoclave_esterilizacion": autoclave_esterilizacion,
    "camilla_aislamiento": camilla_aislamiento,
    "delantal_laboratorio": delantal_laboratorio,
    "gradilla_tubos_ensayo": gradilla_tubos_ensayo,
    "rollo_vendas_yodo": rollo_vendas_yodo,
    "sabana_quirurgica": sabana_quirurgica,
    "bata_paciente": bata_paciente,
    "bandeja_instrumentos": bandeja_instrumentos,
    "soporte_suero": soporte_suero,
    "bolsa_desechos_biologicos": bolsa_desechos_biologicos,
    "muleta_aluminio": muleta_aluminio,
}
