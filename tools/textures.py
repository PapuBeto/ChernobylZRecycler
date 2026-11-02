"""Texturas definitivas (estilo D) para los recursos y componentes.

Genera los PNG de 16x16 y una hoja de revision en docs/style_test/final/.
Cuando esten aprobados, `python tools/textures.py --install` los copia a
src/main/resources/assets/chernobylz_recycler/textures/item/.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src/main/resources/assets/chernobylz_recycler/textures/item"
REVIEW = ROOT / "docs/style_test/final"
SCALE = 8

OUTLINE = (28, 30, 34)
OUTLINE_WARM = (52, 44, 34)

CLOTH = {
    "base": (190, 178, 150),
    "light": (220, 208, 182),
    "dark": (140, 128, 102),
    "stain": (110, 94, 68),
}
METAL = {
    "base": (138, 142, 146),
    "light": (182, 188, 194),
    "dark": (88, 92, 98),
    "rust": (146, 84, 42),
}
STEEL = {
    "base": (112, 120, 130),
    "light": (162, 170, 180),
    "dark": (68, 74, 82),
    "rust": (140, 80, 40),
}
COPPER = {
    "base": (184, 112, 64),
    "light": (224, 156, 98),
    "dark": (118, 64, 34),
}
BRASS = {
    "base": (188, 158, 82),
    "light": (226, 200, 122),
    "dark": (126, 102, 48),
}
GREEN = {
    "base": (70, 116, 68),
    "light": (108, 154, 98),
    "dark": (40, 74, 44),
}
GLASS = {
    "base": (84, 152, 192),
    "light": (172, 222, 246),
    "dark": (44, 96, 132),
}
YELLOW = (204, 172, 70)
YELLOW_DARK = (142, 116, 40)
BLACK = (40, 42, 46)
WHITE = (246, 246, 240)
RED = (168, 62, 52)
OLIVE = (98, 112, 74)
OLIVE_LIGHT = (136, 152, 102)
OLIVE_DARK = (64, 76, 48)
LEAD = (106, 112, 120)
LEAD_LIGHT = (150, 156, 164)
LEAD_DARK = (70, 74, 82)


def canvas():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color[:3])


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def px(d, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        d.point((x, y), fill=color)


def bevel(d, x0, y0, x1, y1, base, light, dark, outline=OUTLINE):
    d.rectangle([x0, y0, x1, y1], fill=dark, outline=outline)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=base)
    d.line([x0 + 1, y0 + 1, x1 - 1, y0 + 1], fill=light)
    d.line([x0 + 1, y0 + 1, x0 + 1, y1 - 1], fill=light)
    d.line([x0 + 1, y1 - 1, x1 - 1, y1 - 1], fill=dark)
    d.line([x1 - 1, y0 + 1, x1 - 1, y1 - 1], fill=dark)


def bolt(d, x, y, light=(200, 200, 196)):
    px(d, x, y, OUTLINE)
    px(d, x, y - 1, light)


def rust_spots(d, spots, color):
    for x, y in spots:
        px(d, x, y, color)
        px(d, x + 1, y, shade(color, 0.7))


# ---------------------------------------------------------------------------
# Recursos base
# ---------------------------------------------------------------------------

def tela():
    img, d = canvas()
    p = CLOTH
    d.polygon([(3, 4), (12, 4), (13, 5), (13, 8), (3, 8), (2, 7), (2, 5)],
              fill=p["light"], outline=OUTLINE_WARM)
    d.polygon([(2, 8), (13, 8), (14, 9), (14, 12), (13, 13), (2, 13), (1, 12), (1, 9)],
              fill=p["base"], outline=OUTLINE_WARM)
    d.line([(3, 8), (12, 8)], fill=p["dark"])
    d.line([(4, 6), (10, 6)], fill=p["dark"])
    d.line([(3, 11), (12, 11)], fill=p["dark"])
    for x in (5, 7, 9, 11):
        px(d, x, 7, p["dark"])
        px(d, x, 12, p["dark"])
    d.line([(3, 5), (11, 5)], fill=WHITE)
    # Deshilachado y manchas
    px(d, 13, 10, p["dark"])
    px(d, 13, 12, p["dark"])
    px(d, 4, 10, p["stain"])
    px(d, 6, 11, p["stain"])
    px(d, 9, 9, p["stain"])
    px(d, 10, 10, p["stain"])
    return img


def scrap():
    img, d = canvas()
    p = METAL
    d.polygon([(2, 9), (8, 7), (13, 9), (12, 13), (4, 13)],
              fill=p["base"], outline=OUTLINE)
    d.polygon([(4, 4), (10, 3), (13, 6), (9, 9), (4, 8)],
              fill=p["light"], outline=OUTLINE)
    d.polygon([(2, 11), (6, 9), (11, 10), (9, 13)],
              fill=p["dark"], outline=OUTLINE)
    d.line([(4, 5), (9, 4)], fill=WHITE)
    d.line([(3, 10), (8, 9)], fill=p["dark"])
    for x, y in ((6, 11), (9, 11), (7, 6), (11, 7)):
        bolt(d, x, y)
    rust_spots(d, [(3, 12), (10, 10), (12, 6), (5, 12)], p["rust"])
    return img


def lingote_pesado():
    img, d = canvas()
    p = STEEL
    d.polygon([(4, 4), (12, 4), (14, 7), (2, 7)], fill=p["light"], outline=OUTLINE)
    d.polygon([(2, 7), (14, 7), (13, 12), (3, 12)], fill=p["base"], outline=OUTLINE)
    d.line([(3, 11), (13, 11)], fill=p["dark"])
    d.line([(5, 4), (11, 4)], fill=(214, 220, 228))
    d.line([(4, 5), (5, 5)], fill=WHITE)
    d.line([(3, 7), (13, 7)], fill=p["dark"])
    # Marca estampada
    d.rectangle([7, 8, 10, 10], outline=p["dark"])
    px(d, 8, 9, p["dark"])
    px(d, 9, 9, p["dark"])
    rust_spots(d, [(4, 9), (11, 10), (6, 5)], p["rust"])
    return img


# ---------------------------------------------------------------------------
# Componentes
# ---------------------------------------------------------------------------

def engranaje_titanio():
    img, d = canvas()
    p = METAL
    for x0, y0, x1, y1 in ((7, 1, 8, 3), (7, 12, 8, 14), (1, 7, 3, 8),
                           (12, 7, 14, 8), (2, 2, 3, 3), (12, 2, 13, 3),
                           (2, 12, 3, 13), (12, 12, 13, 13)):
        d.rectangle([x0, y0, x1, y1], fill=p["base"], outline=OUTLINE)
    d.ellipse([3, 3, 12, 12], fill=OUTLINE)
    d.ellipse([4, 4, 11, 11], fill=p["base"])
    d.ellipse([5, 5, 10, 10], outline=p["dark"])
    d.ellipse([6, 6, 9, 9], fill=OUTLINE)
    d.ellipse([7, 7, 8, 8], fill=p["dark"])
    d.arc([4, 4, 11, 11], 185, 265, fill=p["light"])
    px(d, 5, 5, WHITE)
    return img


def piston_hidraulico():
    img, d = canvas()
    p = STEEL
    # Placa de montaje
    d.rectangle([1, 4, 3, 13], fill=p["dark"], outline=OUTLINE)
    bolt(d, 2, 6)
    bolt(d, 2, 11)
    # Cilindro
    d.rectangle([3, 6, 9, 11], fill=p["base"], outline=OUTLINE)
    d.line([(4, 6), (8, 6)], fill=p["light"])
    d.line([(4, 11), (8, 11)], fill=p["dark"])
    d.line([(4, 7), (4, 10)], fill=p["light"])
    d.rectangle([3, 6, 4, 11], fill=p["dark"], outline=OUTLINE)
    d.rectangle([8, 6, 9, 11], fill=p["dark"], outline=OUTLINE)
    # Vastago
    d.rectangle([9, 7, 13, 9], fill=(206, 212, 220), outline=OUTLINE)
    d.line([(10, 7), (12, 7)], fill=WHITE)
    d.line([(10, 9), (12, 9)], fill=(150, 156, 164))
    # Horquilla
    d.rectangle([13, 6, 14, 10], fill=BRASS["base"], outline=OUTLINE)
    px(d, 14, 8, OUTLINE)
    # Manguera hidraulica
    d.line([(5, 6), (5, 3), (8, 3)], fill=OUTLINE)
    d.line([(5, 5), (5, 4)], fill=(70, 70, 70))
    d.rectangle([8, 2, 9, 4], fill=BRASS["base"], outline=OUTLINE)
    rust_spots(d, [(6, 9), (8, 10)], p["rust"])
    return img


def tubo_presion():
    img, d = canvas()
    p = STEEL
    d.rectangle([3, 1, 12, 3], fill=p["dark"], outline=OUTLINE)
    d.rectangle([3, 12, 12, 14], fill=p["dark"], outline=OUTLINE)
    d.rectangle([5, 3, 10, 12], fill=p["base"], outline=OUTLINE)
    d.line([(6, 4), (6, 11)], fill=p["light"])
    d.line([(9, 4), (9, 11)], fill=p["dark"])
    for x, y in ((4, 2), (11, 2), (4, 13), (11, 13)):
        bolt(d, x, y)
    # Manometro
    d.rectangle([11, 5, 12, 6], fill=p["dark"], outline=OUTLINE)
    d.ellipse([10, 4, 13, 7], fill=OUTLINE)
    d.ellipse([11, 5, 12, 6], fill=(224, 224, 214))
    d.line([(12, 6), (12, 5)], fill=RED)
    rust_spots(d, [(7, 8), (8, 10), (6, 12)], p["rust"])
    return img


def valvula_antirretorno():
    img, d = canvas()
    p = STEEL
    red = (168, 62, 52)
    red_light = (212, 104, 88)
    red_dark = (108, 34, 28)
    # Tubos y bridas
    d.rectangle([1, 7, 2, 12], fill=p["dark"], outline=OUTLINE)
    d.rectangle([13, 7, 14, 12], fill=p["dark"], outline=OUTLINE)
    d.rectangle([2, 8, 13, 11], fill=p["base"], outline=OUTLINE)
    # Cuerpo central
    d.polygon([(6, 6), (9, 6), (11, 8), (11, 11), (9, 13), (6, 13), (4, 11), (4, 8)],
              fill=p["base"], outline=OUTLINE)
    d.line([(3, 8), (12, 8)], fill=p["light"])
    d.line([(5, 10), (10, 10)], fill=p["dark"])
    # Vastago
    d.rectangle([6, 6, 7, 8], fill=p["dark"], outline=OUTLINE)
    # Volante rojo
    d.ellipse([2, 0, 10, 8], fill=OUTLINE)
    d.ellipse([3, 1, 9, 7], fill=red, outline=red_dark)
    d.ellipse([5, 3, 7, 5], fill=(0, 0, 0, 0))
    d.line([(6, 1), (6, 3)], fill=red_dark)
    d.line([(6, 5), (6, 7)], fill=red_dark)
    d.line([(3, 4), (5, 4)], fill=red_dark)
    d.line([(7, 4), (9, 4)], fill=red_dark)
    px(d, 4, 2, red_light)
    # Pernos
    for x, y in ((2, 9), (13, 9), (2, 11), (13, 11)):
        bolt(d, x, y)
    rust_spots(d, [(5, 11), (10, 9)], p["rust"])
    return img


def bobina_cobre():
    img, d = canvas()
    p = COPPER
    d.rectangle([7, 2, 8, 13], fill=OUTLINE)
    for y in (3, 6, 9):
        d.ellipse([3, y, 12, y + 4], fill=p["base"], outline=OUTLINE)
        d.arc([3, y, 12, y + 4], 185, 300, fill=p["light"])
        px(d, 5, y + 1, p["light"])
    d.line([(12, 11), (14, 13), (14, 14)], fill=p["base"])
    d.line([(12, 12), (13, 13)], fill=p["light"])
    return img


def cableado_alta_tension():
    img, d = canvas()
    d.rectangle([2, 3, 4, 13], fill=STEEL["dark"], outline=OUTLINE)
    d.rectangle([11, 3, 13, 13], fill=STEEL["dark"], outline=OUTLINE)
    d.rectangle([4, 4, 11, 12], fill=(58, 60, 64), outline=OUTLINE)
    for y in (5, 7, 9, 11):
        d.line([(4, y), (11, y)], fill=COPPER["base"])
        d.line([(5, y - 1), (10, y - 1)], fill=COPPER["light"])
    d.line([(13, 9), (15, 11)], fill=OUTLINE)
    d.line([(13, 10), (14, 11)], fill=(40, 40, 40))
    d.rectangle([14, 11, 15, 13], fill=YELLOW, outline=OUTLINE)
    px(d, 14, 12, BLACK)
    bolt(d, 3, 4, STEEL["light"])
    bolt(d, 12, 4, STEEL["light"])
    return img


def placa_circuito_impreso():
    img, d = canvas()
    p = GREEN
    bevel(d, 2, 2, 13, 13, p["base"], p["light"], p["dark"])
    # Pistas doradas
    d.line([(3, 11), (6, 11), (6, 7), (9, 7)], fill=BRASS["base"])
    d.line([(12, 3), (12, 8), (9, 8)], fill=BRASS["base"])
    d.line([(4, 4), (7, 4)], fill=BRASS["base"])
    d.line([(3, 9), (5, 9)], fill=BRASS["base"])
    # Chip grande
    d.rectangle([4, 5, 7, 8], fill=BLACK, outline=OUTLINE)
    d.line([(5, 5), (6, 5)], fill=(90, 92, 98))
    for x in (4, 5, 6, 7):
        px(d, x, 4, METAL["light"])
        px(d, x, 9, METAL["light"])
    # Chip pequeno
    d.rectangle([9, 9, 11, 11], fill=BLACK, outline=OUTLINE)
    for y in (9, 10, 11):
        px(d, 8, y, METAL["light"])
    # Condensador
    d.ellipse([10, 4, 12, 6], fill=METAL["light"], outline=OUTLINE)
    px(d, 11, 5, (220, 220, 220))
    # Agujeros de montaje
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)):
        px(d, x, y, OUTLINE)
        px(d, x + 1, y, p["dark"])
    return img


def condensador_alto_voltaje():
    img, d = canvas()
    p = METAL
    d.rectangle([6, 0, 7, 2], fill=p["light"], outline=OUTLINE)
    d.rectangle([8, 0, 9, 2], fill=p["light"], outline=OUTLINE)
    d.rectangle([5, 2, 10, 13], fill=p["base"], outline=OUTLINE)
    d.ellipse([5, 2, 10, 5], fill=p["light"], outline=OUTLINE)
    d.ellipse([5, 11, 10, 14], fill=p["dark"], outline=OUTLINE)
    d.line([(6, 5), (6, 11)], fill=p["light"])
    d.line([(9, 5), (9, 11)], fill=p["dark"])
    # Banda azul con rayo
    d.rectangle([5, 7, 10, 9], fill=(58, 96, 160), outline=OUTLINE)
    px(d, 8, 7, YELLOW)
    px(d, 7, 8, YELLOW)
    px(d, 8, 8, YELLOW)
    px(d, 7, 9, YELLOW)
    d.line([(5, 7), (10, 7)], fill=(110, 150, 210))
    return img


def motor_paso_a_paso():
    img, d = canvas()
    p = STEEL
    d.rectangle([7, 1, 8, 4], fill=p["light"], outline=OUTLINE)
    bevel(d, 3, 4, 12, 12, p["base"], p["light"], p["dark"])
    d.ellipse([4, 5, 11, 12], fill=OUTLINE)
    d.ellipse([5, 6, 10, 11], fill=p["light"])
    d.ellipse([6, 7, 9, 10], fill=p["dark"])
    d.ellipse([7, 8, 8, 9], fill=OUTLINE)
    for x, y in ((5, 7), (10, 7), (5, 10), (10, 10)):
        px(d, x, y, OUTLINE)
    # Cables
    d.line([(5, 12), (4, 15)], fill=RED)
    d.line([(7, 12), (7, 15)], fill=YELLOW)
    d.line([(9, 12), (10, 15)], fill=BLACK)
    px(d, 4, 15, OUTLINE)
    px(d, 10, 15, OUTLINE)
    return img


def microprocesador_militar():
    img, d = canvas()
    # Patas
    for x in (4, 6, 8, 10):
        d.line([(x, 1), (x, 2)], fill=METAL["light"])
        d.line([(x, 13), (x, 14)], fill=METAL["light"])
    for y in (4, 6, 8, 10):
        d.line([(1, y), (2, y)], fill=METAL["light"])
        d.line([(13, y), (14, y)], fill=METAL["light"])
    bevel(d, 3, 3, 12, 12, (56, 58, 62), (86, 88, 94), OUTLINE)
    # Muesca y marca dorada
    px(d, 4, 4, BLACK)
    px(d, 5, 4, BLACK)
    d.rectangle([7, 7, 9, 9], fill=BRASS["base"], outline=OUTLINE)
    px(d, 8, 8, BLACK)
    d.line([(4, 5), (4, 10)], fill=(78, 80, 86))
    d.line([(5, 11), (10, 11)], fill=(78, 80, 86))
    return img


def sensor_dosimetrico():
    img, d = canvas()
    p = (176, 174, 160)
    bevel(d, 2, 5, 12, 13, p, (212, 210, 196), (120, 118, 106))
    # Pantalla
    d.rectangle([4, 7, 10, 9], fill=(38, 72, 46), outline=OUTLINE)
    d.line([(5, 8), (7, 8)], fill=(110, 190, 120))
    d.line([(5, 7), (6, 7)], fill=(80, 150, 90))
    # Botones y rejilla
    px(d, 4, 11, RED)
    px(d, 6, 11, OUTLINE)
    px(d, 8, 11, OUTLINE)
    # Etiqueta de peligro
    d.rectangle([9, 10, 11, 12], fill=YELLOW, outline=OUTLINE)
    px(d, 10, 11, BLACK)
    # Sonda
    d.line([(12, 5), (14, 2)], fill=OUTLINE)
    d.line([(13, 3), (14, 2)], fill=METAL["light"])
    d.rectangle([13, 1, 14, 2], fill=METAL["light"], outline=OUTLINE)
    return img


def lente_optica_precision():
    img, d = canvas()
    d.rectangle([7, 0, 8, 2], fill=METAL["dark"], outline=OUTLINE)
    d.ellipse([1, 2, 14, 15], fill=OUTLINE)
    d.ellipse([2, 3, 13, 14], fill=METAL["base"])
    d.ellipse([3, 4, 12, 13], fill=BRASS["base"])
    d.ellipse([4, 5, 11, 12], fill=GLASS["dark"])
    d.ellipse([5, 6, 10, 11], fill=GLASS["base"])
    d.ellipse([6, 7, 8, 9], fill=GLASS["light"])
    px(d, 6, 6, WHITE)
    px(d, 7, 6, (230, 250, 255))
    d.arc([2, 3, 13, 14], 200, 280, fill=METAL["light"])
    d.arc([3, 4, 12, 13], 200, 280, fill=BRASS["light"])
    return img


def filtro_carbon_activado():
    img, d = canvas()
    p = METAL
    # Boquilla
    d.rectangle([7, 0, 8, 2], fill=p["dark"], outline=OUTLINE)
    # Tapas
    d.rectangle([3, 2, 12, 4], fill=p["base"], outline=OUTLINE)
    d.rectangle([3, 12, 12, 14], fill=p["base"], outline=OUTLINE)
    # Cuerpo
    d.rectangle([4, 4, 11, 12], fill=(64, 66, 70), outline=OUTLINE)
    d.line([(5, 5), (5, 11)], fill=(100, 102, 106))
    d.line([(10, 5), (10, 11)], fill=(38, 40, 44))
    # Rejillas
    for x in range(4, 12, 2):
        px(d, x, 3, OUTLINE)
        px(d, x + 1, 3, p["light"])
        px(d, x, 13, OUTLINE)
        px(d, x + 1, 13, p["light"])
    # Banda amarilla
    d.rectangle([4, 7, 11, 9], fill=YELLOW, outline=OUTLINE)
    d.line([(5, 7), (10, 7)], fill=(230, 200, 100))
    # C
    px(d, 7, 7, BLACK)
    px(d, 6, 8, BLACK)
    px(d, 7, 9, BLACK)
    # Remaches
    for x, y in ((4, 2), (11, 2), (4, 12), (11, 12)):
        px(d, x, y, p["light"])
    return img


def tejido_kevlar_plomado():
    img, d = canvas()
    p = (154, 146, 122)
    d.polygon([(2, 4), (13, 4), (13, 12), (2, 12)], fill=p, outline=OUTLINE_WARM)
    # Trama
    for x in range(3, 13, 2):
        d.line([(x, 5), (x, 11)], fill=(124, 116, 94))
    for y in (6, 8, 10):
        d.line([(3, y), (12, y)], fill=(178, 170, 146))
    # Placa de plomo remachada
    bevel(d, 4, 5, 9, 9, LEAD, LEAD_LIGHT, LEAD_DARK)
    for x, y in ((4, 5), (9, 5), (4, 9), (9, 9)):
        px(d, x, y, OUTLINE)
        px(d, x, y + 1 if y == 5 else y - 1, LEAD_LIGHT)
    # Esquina doblada
    d.polygon([(13, 4), (13, 7), (10, 4)], fill=(190, 182, 158), outline=OUTLINE_WARM)
    d.line([(3, 12), (12, 12)], fill=(120, 112, 90))
    return img


def celda_litio_militar():
    img, d = canvas()
    d.rectangle([7, 0, 8, 2], fill=METAL["light"], outline=OUTLINE)
    d.rectangle([5, 2, 10, 13], fill=OLIVE, outline=OUTLINE)
    d.ellipse([5, 2, 10, 5], fill=OLIVE_LIGHT, outline=OUTLINE)
    d.ellipse([5, 11, 10, 14], fill=OLIVE_DARK, outline=OUTLINE)
    d.line([(6, 4), (6, 11)], fill=OLIVE_LIGHT)
    d.line([(9, 4), (9, 11)], fill=OLIVE_DARK)
    d.rectangle([5, 7, 10, 9], fill=YELLOW, outline=OUTLINE)
    # Rayo
    px(d, 8, 7, BLACK)
    px(d, 7, 8, BLACK)
    px(d, 8, 8, BLACK)
    px(d, 7, 9, BLACK)
    return img


def nucleo_plomo_sellado():
    img, d = canvas()
    bevel(d, 3, 4, 12, 13, LEAD, LEAD_LIGHT, LEAD_DARK)
    d.rectangle([2, 3, 13, 5], fill=LEAD_LIGHT, outline=OUTLINE)
    d.line([(3, 5), (12, 5)], fill=LEAD_DARK)
    for x, y in ((3, 4), (12, 4), (3, 12), (12, 12)):
        px(d, x, y, OUTLINE)
        px(d, x, y - 1, WHITE)
    # Simbolo de radiacion
    d.ellipse([4, 5, 11, 12], fill=YELLOW, outline=OUTLINE)
    d.pieslice([5, 6, 10, 11], 60, 120, fill=BLACK)
    d.pieslice([5, 6, 10, 11], 180, 240, fill=BLACK)
    d.pieslice([5, 6, 10, 11], 300, 360, fill=BLACK)
    px(d, 7, 8, BLACK)
    px(d, 8, 8, BLACK)
    # Franja de peligro
    d.rectangle([3, 12, 12, 13], fill=YELLOW, outline=OUTLINE)
    for x in range(4, 12, 3):
        px(d, x, 12, BLACK)
        px(d, x + 1, 13, BLACK)
    return img


DESIGNS = {
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

LABELS = {
    "tela": "Tela",
    "scrap": "Scrap",
    "lingote_pesado": "Lingote",
    "engranaje_titanio": "Engranaje",
    "piston_hidraulico": "Piston",
    "tubo_presion": "Tubo",
    "valvula_antirretorno": "Valvula",
    "bobina_cobre": "Bobina",
    "cableado_alta_tension": "Cableado",
    "placa_circuito_impreso": "PCB",
    "condensador_alto_voltaje": "Condensador",
    "motor_paso_a_paso": "Motor",
    "microprocesador_militar": "Microproc.",
    "sensor_dosimetrico": "Sensor",
    "lente_optica_precision": "Lente",
    "filtro_carbon_activado": "Filtro",
    "tejido_kevlar_plomado": "Kevlar",
    "celda_litio_militar": "Celda",
    "nucleo_plomo_sellado": "Nucleo",
}


def font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def build_sheet(images):
    cols = 5
    cell = 16 * SCALE
    gap = 12
    label_h = 20
    rows = (len(images) + cols - 1) // cols
    width = cols * (cell + gap) + gap
    height = 38 + rows * (cell + label_h + gap) + gap
    sheet = Image.new("RGBA", (width, height), (32, 34, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((width // 2, 10), "Recursos y componentes - estilo D", font=font(18),
           fill=(228, 228, 222), anchor="ma")

    small = font(12)
    for index, (item_id, img) in enumerate(images.items()):
        row, col = divmod(index, cols)
        x = gap + col * (cell + gap)
        y = 38 + row * (cell + label_h + gap)
        sheet.alpha_composite(img.resize((cell, cell), Image.NEAREST), (x, y))
        d.rectangle([x - 1, y - 1, x + cell, y + cell], outline=(70, 72, 76))
        d.text((x + cell // 2, y + cell + 3), LABELS.get(item_id, item_id), font=small,
               fill=(200, 200, 194), anchor="ma")
    return sheet


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    images = {}
    for item_id, render in DESIGNS.items():
        img = render()
        images[item_id] = img
        img.save(REVIEW / f"{item_id}.png")

    build_sheet(images).save(REVIEW / "componentes.png")

    if "--install" in sys.argv:
        for item_id, img in images.items():
            img.save(ASSETS / f"{item_id}.png")
        print(f"Instaladas {len(images)} texturas en {ASSETS}")
    else:
        print(f"Revision: {REVIEW / 'componentes.png'} ({len(images)} texturas)")


if __name__ == "__main__":
    main()
