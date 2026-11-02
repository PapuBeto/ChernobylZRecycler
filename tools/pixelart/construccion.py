# -*- coding: utf-8 -*-
"""Material de construccion y demolicion: pixel art 32x32."""
from __future__ import annotations

from tools.pixelart import pal
from tools.pixelart.px import P, tono


def viga_acero_retorcida(p):
    """Viga en I torcida: carrion en diagonal con alma virada y remaches."""
    oxido, hierro, acero, carbon = (pal.OXIDO, pal.HIERRO, pal.STEEL,
                                    pal.CARBON)
    # cuerpo de la viga en diagonal (de abajo-izquierda a arriba-derecha)
    p.poligono([(3, 28), (9, 28), (30, 5), (24, 5)], tono(oxido, 3))
    # arista inferior oscura de ala
    p.linea(3, 28, 9, 28, tono(oxido, 0))
    p.linea(24, 5, 30, 5, tono(oxido, 0))
    # arista iluminada (luz superior)
    p.poligono([(3, 25), (9, 25), (28, 5), (25, 5)], tono(oxido, 4))
    # alma virada en el centro (la torsion)
    p.linea(12, 24, 22, 9, tono(hierro, 0))
    p.linea(13, 25, 23, 10, tono(oxido, 1))
    p.linea(14, 25, 24, 11, tono(oxido, 2))
    # remaches a los flancos
    for xy in ((6, 26), (10, 24), (14, 22), (18, 19), (22, 15), (25, 13),
               (28, 10)):
        p.pset(xy[0], xy[1], tono(acero, 4))
        p.pset(xy[0] + 1, xy[1] + 1, tono(hierro, 0))
    # muesca de cizalla en el extremo inferior
    p.pset(4, 27, tono(carbon, 0))
    p.pset(5, 28, tono(carbon, 0))
    # oxido con vejez
    p.pset(9, 24, tono(oxido, 1))
    p.pset(17, 16, tono(oxido, 1))
    p.pset(20, 13, tono(oxido, 0))
    p.pset(26, 9, tono(oxido, 2))


def contrapeso_grua(p):
    """Contrapeso de grua: bloque macizo con nervios y anillo."""
    hierro, oxido, acero, amarillo = (pal.HIERRO, pal.OXIDO, pal.STEEL,
                                      pal.AMARILLO)
    # bloque denso
    p.rect(4, 12, 27, 28, tono(hierro, 2))
    p.hlinea(4, 27, 12, tono(hierro, 3))
    p.hlinea(4, 27, 28, tono(hierro, 0))
    p.vlinea(5, 13, 28, tono(hierro, 3))
    # nervios de alta resistencia
    p.hlinea(4, 27, 17, tono(hierro, 1))
    p.hlinea(4, 27, 23, tono(hierro, 1))
    p.vlinea(16, 13, 28, tono(hierro, 1))
    # anillo de arriba
    p.elipse(9, 9, 2.6, 2.6, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(9, 9, 0.8, 0.8, (0, 0, 0, 0))
    p.rect(12, 9, 14, 12, tono(hierro, 2))
    p.hlinea(12, 14, 9, tono(hierro, 3))
    # aviso de peso (estampa)
    p.rect(18, 18, 25, 23, tono(amarillo, 2))
    p.hlinea(18, 25, 18, tono(amarillo, 3))
    p.hlinea(18, 25, 23, tono(amarillo, 0))
    p.rect(20, 20, 23, 21, tono(carbon := pal.CARBON, 0))
    # manchas del fraguado
    p.pset(22, 14, tono(oxido, 2))
    p.pset(7, 19, tono(oxido, 1))
    p.pset(26, 25, tono(oxido, 2))
    # cuñas de madera abajo
    p.pset(6, 29, tono(pal.MADERA, 1))
    p.pset(25, 29, tono(pal.MADERA, 1))


def cadena_remolque(p):
    """Cadena de remolque: eslabones gordos colgando en catenaria."""
    acero, hierro, carbon, oxido = (pal.STEEL, pal.HIERRO, pal.CARBON,
                                    pal.OXIDO)
    # grillete de remolque arriba
    p.rect(12, 2, 17, 6, tono(hierro, 2))
    p.hlinea(12, 17, 2, tono(hierro, 3))
    p.hlinea(12, 17, 6, tono(hierro, 0))
    p.elipse(14, 4, 1.2, 1.2, (0, 0, 0, 0))
    # cadena colgante (catenaria con eslabones alternados separados)
    eslabones = ((10, 9), (16, 12), (21, 17), (22, 23), (18, 27), (11, 28))
    for k, (cx, cy) in enumerate(eslabones):
        cuerpo = tono(acero, 2) if k % 2 == 0 else tono(acero, 3)
        if k % 2 == 0:
            # eslabon horizontal
            p.elipse(cx, cy, 3.4, 2.2, cuerpo, contorno=tono(hierro, 0))
            p.elipse(cx, cy, 2, 1.2, (0, 0, 0, 0))
            p.pset(cx - 2, cy - 1, tono(acero, 4))
        else:
            # eslabon vertical
            p.elipse(cx, cy, 2.2, 3.4, cuerpo, contorno=tono(hierro, 0))
            p.elipse(cx, cy, 1.2, 2, (0, 0, 0, 0))
            p.pset(cx - 1, cy - 2, tono(acero, 4))
    # gancho de seguridad al final
    p.poligono([(11, 21), (17, 24), (16, 29), (11, 30), (10, 26), (13, 25)],
               tono(hierro, 2))
    p.pset(13, 24, tono(acero, 3))
    # ferrugineo en los eslabones inferiores
    p.pset(9, 10, tono(oxido, 2))
    p.pset(19, 25, tono(oxido, 1))
    p.pset(12, 27, tono(oxido, 1))


def lamina_techo_corrugada(p):
    """Lamina de techo corrugada: chapa galvanizada ondulada y rotas."""
    acero, hierro, oxido, carbon = (pal.STEEL, pal.HIERRO, pal.OXIDO,
                                    pal.CARBON)
    # chapa inclinada con ondas
    p.poligono([(3, 24), (12, 5), (22, 5), (13, 24)], tono(acero, 2))
    p.poligono([(10, 9), (18, 9), (11, 24), (7, 24)], tono(acero, 1))
    # crestas de las ondas (lineas en V)
    ondas = ((7, 20), (10, 14), (13, 9), (17, 9), (14, 14), (11, 20))
    for x0, y0 in ondas:
        p.linea(x0, y0, x0 + 2, y0 - 3, tono(acero, 4))
        p.linea(x0 + 2, y0 - 3, x0 + 4, y0, tono(hierro, 0))
    # caida de la chapa corva al fondo
    p.poligono([(20, 14), (27, 18), (28, 25), (23, 25), (21, 19)],
               tono(acero, 1))
    p.linea(21, 16, 27, 21, tono(hierro, 0))
    p.linea(22, 19, 27, 24, tono(acero, 3))
    # remaches de fijacion
    p.pset(9, 7, tono(hierro, 3))
    p.pset(20, 7, tono(hierro, 3))
    p.pset(12, 22, tono(hierro, 3))
    # oxido de escorrentia
    p.pset(13, 12, tono(oxido, 2))
    p.pset(14, 13, tono(oxido, 1))
    p.pset(8, 22, tono(oxido, 1))
    p.pset(25, 23, tono(oxido, 2))
    # agujero de meteorito
    p.elipse(16, 18, 1.2, 1.2, (0, 0, 0, 0))
    p.pset(15, 17, tono(carbon, 0))
    p.pset(17, 19, tono(carbon, 0))


def caja_clavos_tuercas(p):
    """Caja de clavos y tuercas: arca de madera con latas y piezas."""
    madera, hierro, acero, carbon = (pal.MADERA, pal.HIERRO, pal.STEEL,
                                     pal.CARBON)
    # caja de madera
    p.rect(4, 10, 27, 27, tono(madera, 2))
    p.hlinea(4, 27, 10, tono(madera, 3))
    p.hlinea(4, 27, 27, tono(madera, 0))
    p.vlinea(4, 10, 27, tono(madera, 3))
    # tapa abierta apoyada detras
    p.rect(2, 6, 22, 9, tono(madera, 1))
    p.hlinea(2, 22, 6, tono(madera, 2))
    p.hlinea(2, 22, 9, tono(madera, 0))
    # viruta y tablas
    p.hlinea(6, 25, 18, tono(madera, 1))
    p.linea(5, 26, 12, 20, tono(madera, 0))
    # clavillos (chinchetas punteagudas)
    for xy in ((9, 13), (11, 16), (14, 12), (16, 15), (13, 19), (10, 22)):
        p.rect(xy[0], xy[1], xy[0], xy[1] + 3, tono(acero, 3))
        p.pset(xy[0], xy[1] + 1, tono(hierro, 0))
        p.pset(xy[0] - 1, xy[1], tono(acero, 4))
    # tuerca grande
    p.elipse(22, 21, 3, 3, tono(acero, 2), contorno=tono(hierro, 0))
    p.elipse(22, 21, 1.4, 1.4, (0, 0, 0, 0))
    p.pset(21, 20, tono(acero, 4))
    # arandela pequeña
    p.elipse(25, 15, 1.6, 1.6, tono(hierro, 2), contorno=tono(hierro, 0))
    p.elipse(25, 15, 0.6, 0.6, (0, 0, 0, 0))
    # viruta de madera en el fondo
    p.pset(7, 25, tono(pal.BEIGE, 1))
    p.pset(8, 26, tono(pal.BEIGE, 0))
    # quemadura
    p.pset(24, 26, tono(carbon, 1))


def ladrillo_blindaje_plomo(p):
    """Ladrillo de plomo: bloque denso gris con banda de peligro."""
    acero, hierro, amarillo, carbon = (pal.STEEL, pal.HIERRO, pal.AMARILLO,
                                       pal.CARBON)
    # bloque de ladrillo ancho
    p.rect(3, 12, 28, 24, tono(acero, 1))
    p.hlinea(3, 28, 12, tono(acero, 3))
    p.hlinea(3, 28, 24, tono(hierro, 0))
    p.vlinea(3, 12, 24, tono(acero, 2))
    # banda de seguridad intermedia
    p.rect(3, 17, 28, 20, tono(amarillo, 2))
    p.hlinea(3, 28, 17, tono(amarillo, 3))
    p.hlinea(3, 28, 20, tono(amarillo, 0))
    p.pset(5, 18, tono(carbon, 0))
    p.pset(6, 18, tono(carbon, 0))
    p.pset(5, 19, tono(carbon, 0))
    # superficie rugosa (granulacion de colada)
    for xy in ((8, 14), (12, 15), (17, 14), (22, 15), (26, 14)):
        p.pset(xy[0], xy[1], tono(acero, 2))
    for xy in ((10, 22), (15, 23), (20, 22), (25, 23)):
        p.pset(xy[0], xy[1], tono(hierro, 1))
    # gota de plomo fundido en el borde
    p.pset(29, 22, tono(acero, 3))
    p.pset(30, 23, tono(acero, 2))
    # fragua de oxido blanco
    p.pset(7, 23, tono(pal.SULFATO, 1))
    p.pset(24, 13, tono(pal.SULFATO, 0))


def bidon_acido(p):
    """Bidon de acido: garrafa amarilla con tecle, medidor y goteo."""
    amarillo, carbon, rojo, hierro = (pal.AMARILLO, pal.CARBON, pal.ROJO,
                                      pal.HIERRO)
    # garrafa
    p.rect(7, 8, 24, 28, tono(amarillo, 2))
    p.hlinea(7, 24, 8, tono(amarillo, 3))
    p.hlinea(7, 24, 28, tono(amarillo, 0))
    p.vlinea(8, 9, 28, tono(amarillo, 3))
    # costillas de refuerzo
    p.hlinea(7, 24, 14, tono(amarillo, 1))
    p.hlinea(7, 24, 22, tono(amarillo, 1))
    # asa superior
    p.rect(10, 5, 21, 7, tono(amarillo, 3))
    p.hlinea(10, 21, 5, tono(amarillo, 4))
    p.hlinea(10, 21, 7, tono(amarillo, 1))
    # boca con tapon roscado
    p.rect(13, 3, 18, 5, tono(carbon, 1))
    p.hlinea(13, 18, 3, tono(carbon, 2))
    # etiqueta de peligro (rombos)
    p.rect(10, 17, 21, 21, tono(amarillo, 3))
    p.hlinea(10, 21, 21, tono(amarillo, 0))
    p.rect(13, 18, 18, 20, tono(carbon, 0))
    p.pset(14, 19, tono(amarillo, 3))
    p.pset(15, 19, tono(amarillo, 3))
    p.pset(16, 19, tono(amarillo, 3))
    # goteo de acido en la base
    p.pset(6, 26, tono(pal.SULFATO, 2))
    p.pset(5, 27, tono(pal.SULFATO, 1))
    p.pset(6, 28, tono(pal.SULFATO, 2))
    # ro desconchado
    p.pset(22, 9, tono(amarillo, 1))
    p.pset(23, 9, tono(hierro, 1))
    # decal de veneno
    p.pset(16, 4, tono(rojo, 2))
    p.pset(17, 4, tono(rojo, 1))


def lona_cuarentena(p):
    """Lona de cuarentena: paquete arrugado con cinta de aviso."""
    amarillo, carbon, oxido, acero = (pal.AMARILLO, pal.CARBON, pal.OXIDO,
                                      pal.STEEL)
    # paquete doblado
    p.poligono([(5, 12), (18, 7), (28, 13), (29, 26), (7, 27)],
               tono(amarillo, 2))
    p.poligono([(5, 12), (18, 7), (20, 10), (8, 15)], tono(amarillo, 3))
    # arrugas
    p.linea(8, 15, 10, 26, tono(amarillo, 1))
    p.linea(20, 10, 27, 25, tono(amarillo, 1))
    # cinta de cuarentena (rayas inclinadas)
    for k, (x0, y0) in enumerate(((8, 19), (14, 17), (20, 16), (26, 17))):
        p.rect(x0, y0, x0 + 3, y0 + 4, tono(carbon, 0))
        p.pset(x0, y0 + 2, tono(amarillo, 3))
        p.pset(x0 + 2, y0 + 1, tono(amarillo, 3))
    # brida de cuerda
    p.linea(18, 7, 22, 3, tono(carbon, 2))
    p.pset(22, 3, tono(carbon, 0))
    # cinta adhesiva de sello
    p.rect(6, 23, 13, 26, tono(carbon, 1))
    p.hlinea(6, 13, 23, tono(carbon, 2))
    # nailon rasgado
    p.pset(24, 8, tono(carbon, 1))
    p.pset(25, 9, tono(carbon, 0))
    # suciedad de barrera
    p.pset(10, 24, tono(acero, 1))
    p.pset(28, 14, tono(oxido, 1))
    # termometro colgando
    p.pset(19, 2, tono(acero, 2))
    p.pset(19, 1, tono(pal.ROJO, 2))


DIBUJOS = {
    "viga_acero_retorcida": viga_acero_retorcida,
    "contrapeso_grua": contrapeso_grua,
    "cadena_remolque": cadena_remolque,
    "lamina_techo_corrugada": lamina_techo_corrugada,
    "caja_clavos_tuercas": caja_clavos_tuercas,
    "ladrillo_blindaje_plomo": ladrillo_blindaje_plomo,
    "bidon_acido": bidon_acido,
    "lona_cuarentena": lona_cuarentena,
}
