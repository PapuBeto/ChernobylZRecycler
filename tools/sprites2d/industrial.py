# -*- coding: utf-8 -*-
"""Sprites 2D de la zona INDUSTRIAL (dibujo por codigo).

Cada entrada de DIBUJOS recibe un Lienzo (maestro 512) y pinta el item
centrado, con luz global arriba-izquierda y desgaste coherente.
"""
from __future__ import annotations

import math

from tools.sprites2d.base import (Lienzo, _tono, arco_bandas, descascarillado,
                                  manchas_oxido, mugre, rayitas)
from tools.sprites2d.paleta import (ACERO, CAUCHO, OXIDO, PRIMER)

# tonos particulares del motor
_PINTURA = (93, 101, 95)          # gris industrial verdoso gastado
_HIERRO = (74, 76, 79)            # fundicion sin pintar
_HIERRO_OSC = (56, 58, 61)
_REJA = (52, 54, 56)
_LATON = (158, 126, 78)
_ANILLO = (150, 152, 155)


def _polar(centro, r, grados):
    a = math.radians(grados)
    return (centro[0] + r * math.cos(a), centro[1] + r * math.sin(a))


def motor_grua_sovietica(l: Lienzo):
    """Motor de grua sovietico: campana con rejilla a la izquierda (recibe la
    luz), carcaza repujada recediendo a la derecha, caja de bornes con cable
    de goma, gato de izado, placa de laton, pies, y oxidacion con chorreados."""
    C = (164, 240)            # centro de la campana frontal
    R_CAM = 112
    rng = l.rng

    # sombras de contacto -----------------------------------------------------
    l.sombra_contacto((70, 428, 478, 490), alpha=58, difum=10)
    l.sombra_contacto((140, 418, 452, 464), alpha=42, difum=7)

    # pie lejano (detras de la carcaza, lado derecho, unido a la tapa) --------
    l.poligono([(428, 286), (464, 282), (466, 302), (430, 306)], "hierro",
               _tono(_HIERRO, 0.94), contorno=1.0)
    pie_lejano = [(430, 300), (468, 294), (470, 364), (432, 370)]
    l.oclusion(pie_lejano, desplaz=(0, 6), alpha=40)
    l.poligono(pie_lejano, "hierro", _HIERRO, fases=[(0.0, 1.06), (1.0, 0.6)],
               bisel=(2.5, 0.14, 0.3))
    l.poligono([(426, 360), (474, 354), (476, 374), (428, 380)], "hierro",
               _tono(_HIERRO, 0.84), contorno=1.0)
    l.tuerca(449, 366, 5, ACERO, rot=0.5)

    # tapa trasera del rotor asomando a la derecha ----------------------------
    l.oclusion([(438, 172), (466, 172), (466, 250), (438, 250)],
               desplaz=(-2, 4), alpha=46)
    l.elipse((438, 158, 476, 286), "hierro", _HIERRO,
             fases=[(0.0, 1.12), (1.0, 0.74)], bisel=(2.5, 0.1, 0.24))
    for bx, by in ((452, 196), (468, 222), (450, 246)):
        l.remache(bx, by, 3.0, _tono(ACERO, 0.85))

    # carcaza (cuerpo repujado recediendo a la derecha) -----------------------
    cuerpo = [(264, 154), (436, 146), (436, 292), (264, 338)]

    def retoca_cuerpo(rgb, caja, rg):
        rgb = mugre(rgb, caja, rg, fuerza=0.10, en_bordes=0.55)
        x0, y0, x1, y1 = caja
        sub = (x0, y1 - int((y1 - y0) * 0.45), x1, y1)
        abajo = manchas_oxido(rgb.crop(sub),
                              (0, 0, sub[2] - sub[0], sub[3] - sub[1]),
                              rg, densidad=6, escala=0.8, chorreos=0.4)
        rgb = rgb.copy()
        rgb.paste(abajo, (sub[0], sub[1]))
        rgb = rayitas(rgb, caja, rg, n=4, alpha=55)
        return rgb

    l.oclusion(cuerpo, desplaz=(0, 8), alpha=48)
    l.poligono(cuerpo, None, _PINTURA, fases=[(0.0, 1.15), (0.5, 1.0), (1.0, 0.56)],
               retocar=retoca_cuerpo)

    # aletas de repuje vertical (con filo de luz en su cara izquierda)
    for xv in (296, 322, 348, 374, 400, 424):
        t = (xv - 264) / (436 - 264)
        arriba = 154 + (146 - 154) * t
        abajo = 338 + (292 - 338) * t
        l.oclusion([(xv - 7, arriba - 5), (xv + 6, arriba - 5),
                    (xv + 6, abajo + 4), (xv - 7, abajo + 4)],
                   desplaz=(-4, 0), alpha=36, difum=3)
        l.poligono([(xv - 5, arriba - 6), (xv + 5, arriba - 6),
                    (xv + 5, abajo + 4), (xv - 5, abajo + 4)], "hierro",
                   _tono(_PINTURA, 1.05), fases=[(0.0, 1.12), (1.0, 0.66)],
                   bisel=(1.4, 0.5, 0.2))
        l.poligono([(xv - 5, arriba - 5), (xv - 2.4, arriba - 5),
                    (xv - 2.4, abajo + 3), (xv - 5, abajo + 3)], None,
                   _tono(_PINTURA, 1.28), contorno=0)

    # brida inferior (flanco de zapata del carter)
    def retoca_brida(rgb, caja, rg):
        rgb = manchas_oxido(rgb, caja, rg, densidad=5, escala=0.75, chorreos=0.5)
        rgb = descascarillado(rgb, caja, rg, n=2)
        return rgb

    l.poligono([(264, 338), (436, 292), (436, 306), (264, 352)], None,
               _tono(_PINTURA, 0.9), fases=[(0.0, 1.1), (1.0, 0.6)],
               contorno=1.0, retocar=retoca_brida)

    # pie cercano --------------------------------------------------------------
    pie = [(182, 344), (272, 336), (276, 420), (186, 424)]
    l.oclusion(pie, desplaz=(0, 8), alpha=52)
    l.poligono(pie, "hierro", _HIERRO, fases=[(0.0, 1.06), (1.0, 0.55)],
               bisel=(3, 0.15, 0.3),
               retocar=lambda rgb, caja, rg: manchas_oxido(rgb, caja, rg,
                                                           densidad=4,
                                                           escala=0.7,
                                                           chorreos=0.4))
    l.poligono([(176, 420), (280, 414), (284, 438), (180, 444)], "hierro",
               _tono(_HIERRO, 0.86), contorno=1.1)
    l.tuerca(212, 430, 5.5, ACERO, rot=0.2)
    l.tuerca(252, 426, 5.5, ACERO, rot=1.1)

    # placa de caracteristicas de laton ----------------------------------------
    placa = [(334, 246), (398, 240), (398, 268), (334, 274)]
    l.poligono(placa, "acero", _LATON, fases=[(0.0, 1.22), (1.0, 0.68)],
               bisel=(1.2, 0.4, 0.3), contorno=1.0)
    for fila in range(3):
        yv = 253 + fila * 6
        l.poligono([(342, yv), (390, yv - 4), (390, yv - 2), (342, yv + 2)],
                   None, _tono(_LATON, 0.55), contorno=0)
    l.remache(340, 256, 2.6, ACERO)
    l.remache(392, 250, 2.6, ACERO)

    # caja de bornes ------------------------------------------------------------
    caja_f = [(338, 96), (410, 90), (410, 146), (338, 152)]
    caja_t = [(338, 96), (358, 76), (430, 70), (410, 90)]
    caja_l = [(338, 96), (358, 76), (358, 132), (338, 152)]
    l.oclusion(caja_f, desplaz=(0, 7), alpha=60)
    l.poligono(caja_l, "hierro", _tono(_HIERRO, 0.9),
               fases=[(0.0, 1.14), (1.0, 0.66)], contorno=1.0)
    l.poligono(caja_t, "hierro", _HIERRO,
               fases=[(0.0, 1.32), (1.0, 0.85)], contorno=1.0)
    l.poligono(caja_f, "hierro", _HIERRO, fases=[(0.0, 1.1), (1.0, 0.55)],
               bisel=(2.5, 0.14, 0.3),
               retocar=lambda rgb, caja, rg: mugre(rgb, caja, rg, 0.12))

    # junta de la tapa + filas de archivos gravados (sin texto legible)
    l.poligono([(338, 128), (410, 122), (410, 126), (338, 132)], None,
               _tono(_HIERRO, 0.7), contorno=0)
    for fila, yv in enumerate((104, 110)):
        dv = 0 if fila == 0 else 6
        l.poligono([(356, yv + dv), (396, yv - 6 + dv), (396, yv - 4 + dv),
                    (356, yv + 2 + dv)], None, _tono(_HIERRO, 0.62), contorno=0)
    l.tuerca(348, 144, 4.6, ACERO, rot=0.4)
    l.tuerca(400, 140, 4.6, ACERO, rot=1.9)

    # gato de izado (anillo de elevacion) --------
    l.poligono([(308, 116), (318, 116), (316, 152), (310, 152)], "hierro",
               _tono(_HIERRO, 0.8), contorno=0.8)
    l.anillo((294, 82, 328, 116), 7, "acero", _ANILLO,
             fases=[(0.0, 1.25), (1.0, 0.6)], contorno=1.0)
    l.brillito((306, 92), 6, alpha=42, difum=4)

    # campana frontal: base, aro con pernos, rejilla (clamshell)
    # AO proyectada solo a la derecha: debes caer sobre la carcaza, no rozar
    # el borde izquierdo del circulo
    l.oclusion([(C[0], C[1] - R_CAM + 10), (C[0] + R_CAM, C[1] - R_CAM + 10),
                (C[0] + R_CAM, C[1] + R_CAM), (C[0], C[1] + R_CAM)],
               desplaz=(10, 6), alpha=44, difum=7)

    def retoca_campana(rgb, caja, rg):
        rgb = mugre(rgb, caja, rg, fuerza=0.07, en_bordes=0.45)
        rgb = rayitas(rgb, caja, rg, n=3, alpha=50)
        return rgb

    l.circulo(C, R_CAM, None, _PINTURA,
              fases=[(0.0, 1.18), (0.42, 1.04), (1.0, 0.6)],
              retocar=retoca_campana)

    # aro exterior con pernos
    l.anillo((C[0] - 100, C[1] - 100, C[0] + 100, C[1] + 100), 17, "hierro",
             _tono(_PINTURA, 0.94), fases=[(0.0, 1.14), (1.0, 0.62)], contorno=1.1)
    for grados in (12, 72, 132, 192, 252, 312):
        px, py = _polar(C, 92, grados)
        l.tuerca(px, py, 6.4, ACERO, rot=grados * 0.01)

    # rejilla oscura con anillos concentricos y radios
    l.circulo(C, 77, "oscuro", _REJA, fases=[(0.0, 1.1), (1.0, 0.5)],
              bisel=(2.5, 0.35, 0.4), contorno=1.2)
    for rr in (64, 48, 32):
        l.anillo((C[0] - rr, C[1] - rr, C[0] + rr, C[1] + rr), 5.5, "oscuro",
                 _tono(_REJA, 1.45), fases=[(0.0, 1.2), (1.0, 0.7)], contorno=0.8)
    for grados in range(0, 360, 45):
        a = grados + 22
        p0 = _polar(C, 26, a)
        p1 = _polar(C, 74, a)
        l.curva([p0, _polar(C, 50, a + 1), p1], 2.6, "oscuro",
                _tono(_REJA, 1.7), contorno=0)
    # buje central con pernos
    l.circulo(C, 21, "acero", _tono(ACERO, 0.94),
              fases=[(0.0, 1.18), (1.0, 0.6)], bisel=(2, 0.3, 0.3), contorno=1.0)
    for grados in (40, 160, 280):
        px, py = _polar(C, 12.5, grados)
        l.remache(px, py, 3.0, _tono(ACERO, 0.9))

    # destellos especulares de la campana
    l.brillito((C[0] - 42, C[1] - 62), 26, alpha=60, difum=20)
    l.brillito((C[0] - 18, C[1] - 90), 12, alpha=45, difum=10)
    # luz de borde en el labio superior-izquierdo del aro
    l.velo(l._mascara(lambda d: d.polygon(
        l._es(arco_bandas(C, R_CAM - 14, R_CAM - 2, 188, 254)), fill=255)),
        (214, 224, 214), 70, difum=2)

    # desgaste del borde inferior de la campana: oxido + imprimacion
    l.velo(l._mascara(lambda d: d.polygon(
        l._es(arco_bandas(C, R_CAM - 22, R_CAM - 2, 20, 155)), fill=255)),
        OXIDO, 38, difum=2)
    l.velo(l._mascara(lambda d: d.polygon(
        l._es(arco_bandas(C, R_CAM - 20, R_CAM - 4, 30, 92)), fill=255)),
        PRIMER, 130, difum=1)
    l.velo(l._mascara(lambda d: d.polygon(
        l._es(arco_bandas(C, R_CAM - 18, R_CAM - 2, 98, 142)), fill=255)),
        OXIDO, 110, difum=1)
    # manchas de oxido dentro del aro (nunca fuera de la silueta)
    for a in (rng.uniform(36, 66), rng.uniform(96, 126), rng.uniform(140, 168)):
        px, py = _polar(C, R_CAM - 14, a)
        rr = abs(6.0 + 2.0 * math.sin(a))
        l.velo(l._mascara(lambda d, cx=px, cy=py, rd=rr:
                          d.ellipse(l._caja_es((cx - rd, cy - rd * 0.72,
                                                cx + rd, cy + rd * 0.72)),
                                    fill=255)),
               OXIDO, 96, difum=2.2)

    # oxido corriendo bajo la caja de bornes
    for xx, y0, y1 in ((356, 156, 232), (388, 148, 214)):
        l.velo(l._mascara(lambda d, xv=xx, ya=y0, yb=y1:
                          d.polygon(l._es([(xv - 2.4, ya), (xv + 2.4, ya),
                                           (xv + 1.6, yb), (xv - 1.6, yb)]),
                                    fill=255)),
               OXIDO, 96, difum=1.2)

    # oxido en la tapa trasera
    l.velo(l._mascara(lambda d: d.ellipse(
        l._caja_es((448, 250, 472, 276)), fill=255)), OXIDO, 80, difum=3)

    # prensaestopas + latiguillo de goma con guarda de chapa -------------------
    l.curva([(340, 148), (330, 150), (320, 150)], 13, "acero",
            _tono(_HIERRO, 0.78), contorno=0.8)
    l.curva([(320, 154), (302, 184), (290, 214), (286, 248), (292, 278)],
            12, "caucho", CAUCHO, contorno=1.1)
    l.curva([(292, 272), (298, 288)], 13, "caucho", _tono(CAUCHO, 1.45),
            contorno=0.8)
    l.poligono([(312, 166), (326, 162), (328, 174), (314, 178)], "acero",
               _tono(_HIERRO, 0.9), contorno=0.8)


DIBUJOS = {"motor_grua_sovietica": motor_grua_sovietica}
