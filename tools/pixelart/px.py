# -*- coding: utf-8 -*-
"""Motor de pixel art para ChernobylZ (texturas estilo Minecraft).

Dibujo directo en la cuadricula del sprite (16/32 px de lado): bloque solido,
escalon de tono, dither en dama en las transiciones y contorno por contraste.
Sin antialiasing, sin desenfoque, sin iluminacion pintada: cada grupo de
pixeles define una funcion visual (borde, luces, sombra, material).
"""
from __future__ import annotations

from PIL import Image, ImageDraw

LADO_POR_DEFECTO = 32


class P:
    """Cuadricula pixel RGBA transparente con primitivas de pixel art."""

    def __init__(self, lado=LADO_POR_DEFECTO):
        self.lado = lado
        self.img = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    # ------------------------------------------------------------ pixeles
    def pset(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.lado and 0 <= y < self.lado:
            self.img.putpixel((x, y), _curadors(c))

    def pget(self, x, y):
        return self.img.getpixel((int(x), int(y)))

    # ------------------------------------------------------------ rellenos
    def rect(self, x0, y0, x1, y1, c):
        self.d.rectangle((x0, y0, x1 + 1, y1 + 1), fill=_curadors(c))

    def huecarse(self, x0, y0, x1, y1):
        """Borra pixeles a transparente (recortes, huecos)."""
        self.d.rectangle((x0, y0, x1 + 1, y1 + 1), fill=(0, 0, 0, 0))

    def marco(self, x0, y0, x1, y1, c):
        self.d.rectangle((x0, y0, x1 + 1, y1 + 1),
                         outline=_curadors(c), width=1)

    def elipse(self, cx, cy, rx, ry, c, contorno=None):
        caja = (int(round(cx - rx)), int(round(cy - ry)),
                int(round(cx + rx)) + 1, int(round(cy + ry)) + 1)
        self.d.ellipse(caja, fill=_curadors(c),
                       outline=_curadors(contorno) if contorno else None)

    def disco_contorno(self, cx, cy, r, c):
        self.d.ellipse((int(cx - r), int(cy - r), int(cx + r) + 1,
                        int(cy + r) + 1), outline=_curadors(c))

    def poligono(self, puntos, c):
        self.d.polygon([(int(round(x)), int(round(y))) for x, y in puntos],
                       fill=_curadors(c))

    # ------------------------------------------------------------ lineas
    def hlinea(self, x0, x1, y, c):
        self.d.line((int(x0), int(y), int(x1), int(y)), fill=_curadors(c))

    def vlinea(self, x, y0, y1, c):
        self.d.line((int(x), int(y0), int(x), int(y1)), fill=_curadors(c))

    def linea(self, x0, y0, x1, y1, c):
        self.d.line((int(x0), int(y0), int(x1), int(y1)), fill=_curadors(c))

    # ------------------------------------------------------------ sombreado
    def banda_top(self, x0, y0, x1, y1, c, g=1):
        """Borde superior (luz) g pixeles dentro del rect."""
        self.rect(x0, y0, x1, y0 + g - 1, c)

    def banda_bot(self, x0, y0, x1, y1, c, g=1):
        self.rect(x0, y1 - g + 1, x1, y1, c)

    def banda_izq(self, x0, y0, x1, y1, c, g=1):
        self.rect(x0, y0, x0 + g - 1, y1, c)

    def banda_der(self, x0, y0, x1, y1, c, g=1):
        self.rect(x1 - g + 1, y0, x1, y1, c)

    def pasos_v(self, x0, y0, x1, y1, colores):
        """Relleno vertical: bandas solidas (colores del claro al oscuro)
        con fila de dama en cada transicion entre bandas."""
        altura = y1 - y0 + 1
        n = len(colores)
        limite = []
        for k in range(n - 1):
            limite.append(y0 + int(round(altura * (k + 1) / n)) - 1)
        y = y0
        for k in range(n):
            fin = limite[k] if k < n - 1 else y1
            if y <= fin:
                self.rect(x0, y, x1, fin, colores[k])
            if k < n - 1:
                self.dama(x0, limite[k], x1, limite[k],
                          colores[k], colores[k + 1])
            y = fin + 1

    def pasos_h(self, x0, y0, x1, y1, colores, inicio_izq=False):
        """Igual que pasos_v pero horizontal (inicio_izq = claro a la izquierda)."""
        ancho = x1 - x0 + 1
        col = list(colores)
        if not inicio_izq:
            col = list(reversed(col))
        n = len(col)
        limite = []
        for k in range(n - 1):
            limite.append(x0 + int(round(ancho * (k + 1) / n)) - 1)
        x = x0
        for k in range(n):
            fin = limite[k] if k < n - 1 else x1
            if x <= fin:
                self.rect(x, y0, fin, y1, col[k])
            if k < n - 1:
                self.dama(limite[k], y0, limite[k], y1, col[k], col[k + 1])
            x = fin + 1

    def dama(self, x0, y0, x1, y1, c_a, c_b, desfase=0):
        """Dama (checker) entre dos tonos: transicion pixeleada."""
        for yy in range(int(y0), int(y1) + 1):
            for xx in range(int(x0), int(x1) + 1):
                if (xx + yy + desfase) % 2 == 0:
                    self.img.putpixel((xx, yy), _curadors(c_a))
                else:
                    self.img.putpixel((xx, yy), _curadors(c_b))

    # ------------------------------------------------------------ salida
    def escala(self, f):
        """Ampliacion por vecino mas cercano (para docs/revision)."""
        return self.img.resize((self.lado * f, self.lado * f), Image.NEAREST)

    def guardar(self, ruta):
        self.img.save(ruta)


def _curadors(c):
    """Normaliza color: alpha 255 si no viene, y a tupla."""
    if len(c) == 3:
        return tuple(c)
    return tuple(c[:4])


def tono(rampa, i):
    """Tono de una rampa con indice recortado (atajo de escritura)."""
    return rampa[max(0, min(len(rampa) - 1, int(i)))]
