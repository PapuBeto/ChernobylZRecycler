"""Texturas de objetos por zona (estilo D).

Empieza por la zona industrial. Genera una hoja de revision en
docs/style_test/final/industrial.png y, con --install, copia los PNG al mod.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from textures import (
    BLACK,
    BRASS,
    COPPER,
    GLASS,
    LEAD,
    LEAD_DARK,
    LEAD_LIGHT,
    METAL,
    OUTLINE,
    OUTLINE_WARM,
    RED,
    STEEL,
    WHITE,
    YELLOW,
    bevel,
    bolt,
    canvas,
    px,
    rust_spots,
    shade,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src/main/resources/assets/chernobylz_recycler/textures/item"
REVIEW = ROOT / "docs/style_test/final"
SCALE = 8

IRON = {"base": (96, 100, 104), "light": (142, 148, 154), "dark": (58, 62, 66), "rust": (144, 82, 42)}
RUST = (148, 84, 42)
HAZARD = (198, 166, 64)
WOOD = {"base": (122, 88, 56), "light": (160, 120, 78), "dark": (80, 56, 34)}


# ---------------------------------------------------------------------------
# Industrial
# ---------------------------------------------------------------------------

def motor_grua_sovietica():
    img, d = canvas()
    p = IRON
    d.rectangle([1, 12, 14, 14], fill=p["dark"], outline=OUTLINE)
    bolt(d, 2, 13)
    bolt(d, 13, 13)
    # Cuerpo cilindrico
    d.rectangle([3, 5, 12, 11], fill=p["base"], outline=OUTLINE)
    d.ellipse([2, 5, 4, 11], fill=p["base"], outline=OUTLINE)
    d.ellipse([11, 5, 13, 11], fill=p["base"], outline=OUTLINE)
    for x in (5, 7, 9, 11):
        d.line([(x, 6), (x, 10)], fill=p["dark"])
    d.line([(4, 6), (11, 6)], fill=p["light"])
    # Caja de conexiones
    d.rectangle([6, 2, 9, 5], fill=p["dark"], outline=OUTLINE)
    d.line([(7, 3), (8, 3)], fill=HAZARD)
    # Cáncamo
    d.ellipse([7, 0, 8, 2], outline=OUTLINE)
    # Eje y polea
    d.rectangle([12, 7, 14, 9], fill=(170, 176, 184), outline=OUTLINE)
    d.ellipse([12, 6, 15, 10], fill=p["dark"], outline=OUTLINE)
    d.ellipse([13, 7, 14, 9], fill=(170, 176, 184))
    rust_spots(d, [(4, 10), (9, 9), (11, 6)], p["rust"])
    return img


def taladro_percutor_mina():
    img, d = canvas()
    p = IRON
    # Broca
    d.polygon([(0, 7), (4, 6), (4, 9), (0, 9)], fill=(182, 188, 194), outline=OUTLINE)
    d.line([(1, 8), (3, 7)], fill=WHITE)
    d.line([(1, 9), (3, 9)], fill=p["dark"])
    # Cuerpo
    d.rectangle([4, 5, 12, 10], fill=p["base"], outline=OUTLINE)
    d.line([(5, 5), (11, 5)], fill=p["light"])
    d.rectangle([4, 8, 12, 9], fill=HAZARD)
    d.line([(4, 8), (12, 8)], fill=(160, 132, 48))
    for x in (6, 8, 10):
        d.line([(x, 6), (x, 7)], fill=p["dark"])
    # Empunadura y gatillo
    d.rectangle([8, 10, 11, 14], fill=p["dark"], outline=OUTLINE)
    d.rectangle([7, 10, 8, 12], fill=p["dark"], outline=OUTLINE)
    d.line([(9, 11), (10, 11)], fill=p["light"])
    # Manguera
    d.line([(12, 7), (14, 9), (14, 12)], fill=OUTLINE)
    d.line([(13, 8), (13, 11)], fill=(60, 60, 60))
    rust_spots(d, [(5, 9), (11, 6)], p["rust"])
    return img


def compresor_aire_fabrica():
    img, d = canvas()
    p = IRON
    # Caldera
    d.rectangle([3, 5, 11, 13], fill=p["base"], outline=OUTLINE)
    d.ellipse([2, 5, 4, 13], fill=p["base"], outline=OUTLINE)
    d.ellipse([10, 5, 12, 13], fill=p["base"], outline=OUTLINE)
    d.line([(3, 8), (11, 8)], fill=p["dark"])
    d.line([(3, 11), (11, 11)], fill=p["dark"])
    d.line([(4, 6), (10, 6)], fill=p["light"])
    # Motor
    d.rectangle([5, 2, 9, 5], fill=p["dark"], outline=OUTLINE)
    for x in (6, 7, 8):
        d.line([(x, 2), (x, 4)], fill=p["light"])
    # Manometro
    d.ellipse([11, 3, 14, 6], fill=OUTLINE)
    d.ellipse([12, 4, 13, 5], fill=(224, 224, 214))
    d.line([(12, 5), (13, 4)], fill=RED)
    # Patas
    d.rectangle([2, 13, 4, 14], fill=p["dark"], outline=OUTLINE)
    d.rectangle([10, 13, 12, 14], fill=p["dark"], outline=OUTLINE)
    # Manguera
    d.line([(12, 10), (14, 11), (14, 14)], fill=OUTLINE)
    d.line([(13, 11), (13, 13)], fill=(60, 60, 60))
    rust_spots(d, [(4, 10), (9, 12), (6, 7)], p["rust"])
    return img


def bomba_hidraulica_refrigeracion():
    img, d = canvas()
    p = IRON
    # Voluta
    d.ellipse([1, 5, 13, 15], fill=OUTLINE)
    d.ellipse([2, 6, 12, 14], fill=p["base"])
    d.ellipse([4, 8, 10, 13], fill=p["dark"])
    d.arc([2, 6, 12, 14], 200, 300, fill=p["light"])
    # Impulsor
    d.ellipse([6, 9, 9, 12], fill=(70, 110, 130), outline=OUTLINE)
    d.line([(7, 9), (8, 11)], fill=(130, 180, 200))
    d.line([(9, 10), (7, 11)], fill=(130, 180, 200))
    # Motor superior
    d.rectangle([5, 1, 9, 5], fill=p["dark"], outline=OUTLINE)
    for x in (6, 7, 8):
        d.line([(x, 1), (x, 4)], fill=p["light"])
    # Bridas de entrada/salida
    d.rectangle([0, 8, 2, 11], fill=p["dark"], outline=OUTLINE)
    d.rectangle([12, 8, 14, 11], fill=p["dark"], outline=OUTLINE)
    bolt(d, 1, 9)
    bolt(d, 13, 9)
    # Base
    d.rectangle([2, 14, 12, 15], fill=p["dark"], outline=OUTLINE)
    rust_spots(d, [(3, 7), (10, 12), (6, 13)], p["rust"])
    return img


def soldadora_arco_portatil():
    img, d = canvas()
    body = (140, 68, 48)
    light = (182, 98, 68)
    dark = (92, 42, 30)
    # Asa
    d.arc([4, 1, 11, 7], 180, 360, fill=OUTLINE)
    # Cuerpo
    bevel(d, 2, 5, 13, 11, body, light, dark)
    for x in (4, 6, 8, 10):
        d.line([(x, 7), (x, 9)], fill=dark)
    # Selector
    d.ellipse([3, 6, 5, 8], fill=OUTLINE)
    px(d, 4, 7, WHITE)
    # Cables y pinza
    d.line([(13, 9), (15, 11), (15, 14)], fill=OUTLINE)
    d.line([(14, 10), (14, 13)], fill=(58, 58, 58))
    d.rectangle([13, 13, 15, 14], fill=(58, 58, 58), outline=OUTLINE)
    d.line([(14, 13), (15, 12)], fill=HAZARD)
    # Patas
    d.rectangle([3, 11, 4, 12], fill=dark)
    d.rectangle([11, 11, 12, 12], fill=dark)
    rust_spots(d, [(6, 10), (11, 7)], RUST)
    return img


def caja_engranajes_tractor():
    img, d = canvas()
    p = IRON
    # Cuerpo de fundicion
    d.polygon([(2, 5), (12, 4), (14, 7), (13, 12), (3, 13), (1, 10)],
              fill=p["base"], outline=OUTLINE)
    d.line([(3, 6), (12, 5)], fill=p["light"])
    # Ventana con engranaje
    d.ellipse([5, 6, 10, 11], fill=OUTLINE)
    d.ellipse([6, 7, 9, 10], fill=BRASS["base"])
    d.ellipse([7, 8, 8, 9], fill=OUTLINE)
    for x, y in ((7, 6), (9, 6), (7, 10), (9, 10), (5, 8), (10, 8)):
        px(d, x, y, BRASS["light"])
    # Eje de entrada
    d.rectangle([12, 8, 15, 10], fill=(170, 176, 184), outline=OUTLINE)
    d.line([(13, 8), (14, 8)], fill=WHITE)
    # Palanca
    d.rectangle([7, 2, 8, 5], fill=p["dark"], outline=OUTLINE)
    d.ellipse([6, 1, 9, 3], fill=p["dark"], outline=OUTLINE)
    bolt(d, 3, 11)
    bolt(d, 12, 11)
    rust_spots(d, [(4, 9), (11, 6)], p["rust"])
    return img


def viga_acero_retorcida():
    img, d = canvas()
    p = IRON
    # Viga doblada
    d.line([(2, 13), (6, 9), (9, 9), (13, 5)], fill=OUTLINE, width=5)
    d.line([(2, 13), (6, 9), (9, 9), (13, 5)], fill=p["base"], width=3)
    d.line([(3, 12), (6, 9), (9, 9), (12, 6)], fill=p["light"])
    # Alas en los extremos
    d.line([(1, 11), (4, 14)], fill=p["dark"], width=2)
    d.line([(11, 3), (14, 6)], fill=p["dark"], width=2)
    d.line([(1, 11), (4, 14)], fill=p["light"])
    d.line([(11, 3), (14, 6)], fill=p["light"])
    # Agujeros
    px(d, 5, 10, OUTLINE)
    px(d, 10, 8, OUTLINE)
    rust_spots(d, [(4, 12), (8, 9), (12, 6)], p["rust"])
    return img


def contrapeso_grua():
    img, d = canvas()
    p = (92, 92, 88)
    light = (132, 132, 126)
    dark = (58, 58, 56)
    # Bloque fragmentado
    d.polygon([(2, 6), (12, 5), (14, 8), (13, 13), (8, 14), (3, 12), (1, 9)],
              fill=p, outline=OUTLINE)
    d.line([(3, 7), (11, 6)], fill=light)
    d.line([(3, 12), (7, 13)], fill=dark)
    # Grieta
    d.line([(8, 6), (7, 9), (9, 11), (8, 13)], fill=OUTLINE)
    d.line([(8, 7), (9, 8), (7, 10)], fill=dark)
    # Cáncamo
    d.ellipse([6, 1, 9, 4], outline=OUTLINE)
    d.rectangle([7, 3, 8, 5], fill=dark, outline=OUTLINE)
    # Esquina de peligro
    d.rectangle([2, 11, 4, 13], fill=HAZARD, outline=OUTLINE)
    px(d, 3, 12, BLACK)
    rust_spots(d, [(4, 9), (11, 10)], RUST)
    return img


def cadena_remolque():
    img, d = canvas()
    p = IRON

    def ring_v(x0, y0, x1, y1):
        d.rounded_rectangle([x0, y0, x1, y1], radius=2, fill=p["base"], outline=OUTLINE)
        d.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], radius=1, fill=(0, 0, 0, 0))
        d.line([(x0 + 1, y0 + 2), (x0 + 1, y1 - 2)], fill=p["light"])

    def ring_h(x0, y0, x1, y1):
        d.rounded_rectangle([x0, y0, x1, y1], radius=2, fill=p["base"], outline=OUTLINE)
        d.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], radius=1, fill=(0, 0, 0, 0))
        d.line([(x0 + 2, y0 + 1), (x1 - 2, y0 + 1)], fill=p["light"])

    ring_v(1, 9, 6, 15)
    ring_h(4, 6, 10, 11)
    ring_v(8, 2, 13, 8)
    # Gancho
    d.arc([10, 0, 14, 4], 180, 360, fill=OUTLINE)
    d.arc([11, 1, 13, 3], 180, 360, fill=p["base"])
    d.line([(12, 0), (12, 1)], fill=p["base"])
    rust_spots(d, [(2, 10), (6, 7), (9, 3), (12, 1)], p["rust"])
    return img


def lamina_techo_corrugada():
    img, d = canvas()
    p = METAL
    # Chapa
    d.polygon([(2, 3), (13, 2), (14, 11), (3, 13)], fill=p["base"], outline=OUTLINE)
    # Corrugado
    for x in (4, 6, 8, 10, 12):
        d.line([(x, 4), (x + 1, 11)], fill=p["light"])
        d.line([(x + 1, 4), (x + 2, 11)], fill=p["dark"])
    # Esquina doblada
    d.polygon([(3, 13), (7, 12), (6, 14)], fill=p["dark"], outline=OUTLINE)
    # Agujeros de clavo
    for x, y in ((3, 4), (12, 3), (4, 11), (13, 10)):
        px(d, x, y, OUTLINE)
    rust_spots(d, [(5, 8), (9, 6), (11, 12)], p["rust"])
    return img


def caja_clavos_tuercas():
    img, d = canvas()
    w = WOOD
    # Caja
    d.polygon([(2, 7), (12, 7), (13, 9), (13, 13), (3, 14), (1, 12), (1, 9)],
              fill=w["base"], outline=OUTLINE)
    d.line([(2, 8), (12, 8)], fill=w["light"])
    d.line([(2, 9), (12, 9)], fill=w["dark"])
    # Interior
    d.polygon([(3, 8), (11, 8), (11, 10), (3, 10)], fill=(54, 42, 30), outline=OUTLINE)
    # Clavos
    for x, y in ((4, 9), (6, 8), (8, 9)):
        d.line([(x, y), (x + 2, y - 4)], fill=(180, 186, 192))
        px(d, x + 2, y - 5, (212, 218, 224))
    # Tuercas
    for x, y in ((6, 10), (9, 10)):
        d.rectangle([x, y, x + 2, y + 2], fill=(140, 146, 152), outline=OUTLINE)
        px(d, x + 1, y + 1, OUTLINE)
    rust_spots(d, [(3, 12), (10, 12)], RUST)
    return img


def guantes_soldador():
    img, d = canvas()
    char = (74, 56, 42)
    char_light = (110, 84, 60)
    char_dark = (44, 34, 26)
    cuff = (150, 120, 82)

    # Guante izquierdo
    d.rectangle([2, 11, 6, 14], fill=cuff, outline=OUTLINE_WARM)
    d.rectangle([2, 7, 6, 11], fill=char, outline=OUTLINE_WARM)
    for x in (2, 4, 5):
        d.rectangle([x, 3, x + 1, 7], fill=char, outline=OUTLINE_WARM)
    d.rectangle([1, 8, 2, 11], fill=char, outline=OUTLINE_WARM)
    d.line([(3, 8), (5, 8)], fill=char_light)
    # Guante derecho
    d.rectangle([9, 11, 13, 14], fill=cuff, outline=OUTLINE_WARM)
    d.rectangle([9, 7, 13, 11], fill=char, outline=OUTLINE_WARM)
    for x in (9, 11, 12):
        d.rectangle([x, 3, x + 1, 7], fill=char, outline=OUTLINE_WARM)
    d.rectangle([13, 8, 14, 11], fill=char, outline=OUTLINE_WARM)
    d.line([(10, 8), (12, 8)], fill=char_light)
    # Quemaduras
    px(d, 3, 9, char_dark)
    px(d, 5, 10, char_dark)
    px(d, 10, 9, char_dark)
    px(d, 12, 10, char_dark)
    d.line([(4, 5), (4, 6)], fill=char_dark)
    d.line([(11, 5), (11, 6)], fill=char_dark)
    return img


def casco_minero():
    img, d = canvas()
    yellow = (198, 166, 64)
    light = (230, 200, 100)
    dark = (138, 110, 34)
    # Casco
    d.ellipse([2, 3, 13, 12], fill=yellow, outline=OUTLINE)
    d.rectangle([1, 9, 14, 12], fill=yellow, outline=OUTLINE)
    d.line([(2, 9), (13, 9)], fill=light)
    d.line([(2, 12), (13, 12)], fill=dark)
    # Lámpara
    d.ellipse([6, 5, 9, 8], fill=(170, 176, 184), outline=OUTLINE)
    d.ellipse([7, 6, 8, 7], fill=WHITE)
    # Grietas y desgaste
    d.line([(4, 6), (5, 8), (4, 10)], fill=dark)
    d.line([(11, 7), (10, 9)], fill=dark)
    px(d, 3, 8, dark)
    px(d, 12, 6, dark)
    px(d, 9, 10, dark)
    return img


# ---------------------------------------------------------------------------
# Quimica
# ---------------------------------------------------------------------------

HAZMAT = {"base": (176, 180, 92), "light": (210, 214, 124), "dark": (116, 120, 56)}
RUBBER = {"base": (78, 82, 78), "light": (112, 116, 110), "dark": (48, 50, 48)}
CHEM_GREEN = {"base": (98, 138, 74), "light": (140, 178, 104), "dark": (58, 88, 44)}
ACID = {"base": (128, 186, 76), "light": (178, 226, 118), "dark": (74, 124, 42)}
LAB_WHITE = {"base": (198, 200, 192), "light": (230, 232, 224), "dark": (142, 144, 136)}


def traje_hazmat_liquidador():
    img, d = canvas()
    p = HAZMAT
    # Piernas y botas
    d.rectangle([4, 11, 7, 15], fill=p["base"], outline=OUTLINE)
    d.rectangle([8, 11, 11, 15], fill=p["base"], outline=OUTLINE)
    d.rectangle([3, 14, 7, 15], fill=OUTLINE)
    d.rectangle([8, 14, 12, 15], fill=OUTLINE)
    # Cuerpo
    d.polygon([(4, 5), (11, 5), (12, 7), (11, 12), (4, 12), (3, 7)],
              fill=p["base"], outline=OUTLINE)
    d.line([(5, 6), (10, 6)], fill=p["light"])
    # Brazos y guantes
    d.rectangle([1, 6, 4, 12], fill=p["base"], outline=OUTLINE)
    d.rectangle([11, 6, 14, 12], fill=p["base"], outline=OUTLINE)
    d.rectangle([1, 12, 4, 14], fill=RUBBER["base"], outline=OUTLINE)
    d.rectangle([11, 12, 14, 14], fill=RUBBER["base"], outline=OUTLINE)
    # Capucha y visor
    d.ellipse([4, 0, 11, 6], fill=p["base"], outline=OUTLINE)
    d.ellipse([6, 1, 9, 5], fill=GLASS["dark"], outline=OUTLINE)
    d.line([(7, 2), (8, 2)], fill=GLASS["light"])
    # Simbolo y rasgon
    d.ellipse([7, 7, 8, 8], fill=YELLOW)
    px(d, 7, 7, BLACK)
    px(d, 8, 8, BLACK)
    d.line([(9, 9), (10, 11), (9, 12)], fill=OUTLINE)
    d.line([(10, 10), (11, 12)], fill=OUTLINE)
    return img


def contador_geiger_pripyat():
    img, d = canvas()
    p = (150, 148, 132)
    bevel(d, 2, 4, 12, 13, p, (182, 180, 164), (108, 106, 92))
    # Pantalla
    d.rectangle([4, 6, 10, 8], fill=(40, 72, 44), outline=OUTLINE)
    d.line([(5, 7), (9, 7)], fill=(120, 200, 130))
    d.line([(5, 8), (7, 8)], fill=(80, 150, 90))
    # Aguja y boton
    d.ellipse([4, 10, 6, 12], fill=OUTLINE)
    d.ellipse([5, 10, 5, 11], fill=(224, 224, 214))
    px(d, 8, 11, RED)
    for x in (9, 10):
        px(d, x, 11, OUTLINE)
    # Sonda
    d.line([(12, 4), (14, 2)], fill=OUTLINE)
    d.line([(13, 3), (14, 2)], fill=METAL["light"])
    d.rectangle([13, 1, 14, 2], fill=METAL["light"], outline=OUTLINE)
    # Grieta
    d.line([(6, 5), (7, 6), (6, 7)], fill=OUTLINE)
    return img


def respirador_papr():
    img, d = canvas()
    # Mascara
    d.ellipse([1, 5, 9, 12], fill=RUBBER["base"], outline=OUTLINE)
    d.ellipse([2, 6, 7, 9], fill=GLASS["base"], outline=OUTLINE)
    d.line([(3, 7), (5, 7)], fill=GLASS["light"])
    # Filtro
    d.rectangle([0, 8, 2, 11], fill=STEEL["dark"], outline=OUTLINE)
    d.line([(1, 9), (1, 10)], fill=STEEL["light"])
    # Manguera
    d.line([(9, 9), (12, 11), (12, 13)], fill=OUTLINE)
    d.line([(10, 10), (11, 11)], fill=(60, 60, 60))
    # Equipo
    bevel(d, 11, 10, 15, 15, STEEL["base"], STEEL["light"], STEEL["dark"])
    for y in (12, 14):
        d.line([(12, y), (14, y)], fill=STEEL["dark"])
    px(d, 13, 11, YELLOW)
    # Correa
    d.line([(2, 5), (4, 3), (8, 3)], fill=OUTLINE)
    return img


def centrifugadora_muestras():
    img, d = canvas()
    p = LAB_WHITE
    bevel(d, 2, 5, 13, 13, p["base"], p["light"], p["dark"])
    # Tapa
    d.rectangle([3, 3, 12, 6], fill=(170, 174, 168), outline=OUTLINE)
    d.rectangle([5, 4, 10, 5], fill=GLASS["dark"], outline=OUTLINE)
    # Rotor
    d.ellipse([4, 7, 11, 13], fill=OUTLINE)
    d.ellipse([5, 8, 10, 12], fill=(120, 124, 120))
    d.ellipse([7, 9, 8, 11], fill=OUTLINE)
    for x, y, c in ((6, 9, RED), (9, 9, CHEM_GREEN["base"]),
                    (6, 11, YELLOW), (9, 11, GLASS["base"])):
        px(d, x, y, c)
    # Controles
    d.ellipse([3, 7, 5, 9], fill=OUTLINE)
    px(d, 4, 8, WHITE)
    d.rectangle([11, 7, 12, 8], fill=RED, outline=OUTLINE)
    px(d, 3, 11, YELLOW)
    return img


def contenedor_isotopos():
    img, d = canvas()
    bevel(d, 3, 4, 12, 13, LEAD, LEAD_LIGHT, LEAD_DARK)
    d.rectangle([2, 3, 13, 5], fill=LEAD_LIGHT, outline=OUTLINE)
    d.line([(3, 5), (12, 5)], fill=LEAD_DARK)
    # Asa
    d.arc([6, 1, 9, 4], 180, 360, fill=OUTLINE)
    # Trefoil
    d.ellipse([5, 6, 10, 11], fill=YELLOW, outline=OUTLINE)
    d.pieslice([6, 7, 9, 10], 60, 120, fill=BLACK)
    d.pieslice([6, 7, 9, 10], 180, 240, fill=BLACK)
    d.pieslice([6, 7, 9, 10], 300, 360, fill=BLACK)
    px(d, 7, 8, BLACK)
    px(d, 8, 8, BLACK)
    # Fuga
    d.line([(11, 12), (12, 13), (12, 14)], fill=ACID["base"])
    px(d, 12, 15, ACID["light"])
    px(d, 4, 12, ACID["dark"])
    px(d, 5, 13, ACID["base"])
    return img


def rociador_descontaminacion():
    img, d = canvas()
    p = CHEM_GREEN
    bevel(d, 1, 5, 8, 14, p["base"], p["light"], p["dark"])
    d.rectangle([2, 4, 7, 6], fill=p["dark"], outline=OUTLINE)
    # Bomba
    d.rectangle([4, 2, 5, 4], fill=STEEL["light"], outline=OUTLINE)
    d.line([(4, 2), (6, 1)], fill=STEEL["light"])
    # Manguera y lanza
    d.line([(8, 7), (11, 6), (13, 4)], fill=OUTLINE)
    d.line([(9, 7), (11, 6)], fill=(60, 60, 60))
    d.line([(13, 4), (15, 3)], fill=STEEL["base"])
    d.rectangle([14, 2, 15, 3], fill=STEEL["light"], outline=OUTLINE)
    d.line([(11, 6), (11, 8)], fill=OUTLINE)
    # Etiqueta
    d.rectangle([3, 9, 6, 11], fill=YELLOW, outline=OUTLINE)
    px(d, 4, 10, BLACK)
    # Correas
    d.line([(1, 6), (0, 8)], fill=OUTLINE)
    d.line([(8, 8), (9, 10)], fill=OUTLINE)
    return img


def ladrillo_blindaje_plomo():
    img, d = canvas()
    d.rectangle([2, 6, 13, 12], fill=LEAD, outline=OUTLINE)
    d.rectangle([6, 4, 9, 6], fill=LEAD_LIGHT, outline=OUTLINE)
    d.line([(3, 7), (12, 7)], fill=LEAD_LIGHT)
    d.line([(3, 11), (12, 11)], fill=LEAD_DARK)
    # Marca
    d.rectangle([5, 8, 10, 10], outline=LEAD_DARK)
    px(d, 7, 9, LEAD_DARK)
    px(d, 8, 9, LEAD_DARK)
    # Esquina rota
    d.polygon([(11, 12), (13, 10), (13, 12)], fill=(0, 0, 0, 0), outline=OUTLINE)
    rust_spots(d, [(4, 10), (9, 12)], RUST)
    return img


def delantal_laboratorio():
    img, d = canvas()
    p = LEAD
    # Correas
    d.line([(5, 1), (6, 4)], fill=OUTLINE)
    d.line([(10, 1), (9, 4)], fill=OUTLINE)
    # Peto y falda
    d.polygon([(4, 4), (11, 4), (12, 8), (3, 8)], fill=p, outline=OUTLINE)
    d.polygon([(3, 8), (12, 8), (13, 14), (2, 14)], fill=p, outline=OUTLINE)
    d.line([(4, 9), (11, 9)], fill=LEAD_LIGHT)
    d.line([(4, 13), (11, 13)], fill=LEAD_DARK)
    # Cintas
    d.line([(2, 8), (0, 9)], fill=OUTLINE)
    d.line([(13, 8), (15, 9)], fill=OUTLINE)
    # Simbolo
    d.ellipse([7, 5, 8, 6], fill=YELLOW)
    px(d, 7, 5, BLACK)
    px(d, 8, 6, BLACK)
    # Desgarro
    d.line([(10, 10), (9, 12)], fill=OUTLINE)
    return img


def bidon_acido():
    img, d = canvas()
    p = (176, 150, 60)
    d.rectangle([3, 3, 12, 13], fill=p, outline=OUTLINE)
    d.ellipse([3, 2, 12, 5], fill=(210, 184, 86), outline=OUTLINE)
    d.ellipse([3, 11, 12, 14], fill=(130, 108, 40), outline=OUTLINE)
    d.line([(3, 6), (12, 6)], fill=(130, 108, 40))
    d.line([(3, 9), (12, 9)], fill=(130, 108, 40))
    # Corrosion
    for x, y in ((5, 7), (8, 10), (10, 5)):
        px(d, x, y, ACID["dark"])
        px(d, x + 1, y, ACID["base"])
    # Goteo
    d.line([(9, 13), (9, 15)], fill=ACID["base"])
    px(d, 9, 15, ACID["light"])
    # Etiqueta
    d.rectangle([4, 7, 7, 9], fill=BLACK, outline=OUTLINE)
    px(d, 5, 8, YELLOW)
    return img


def botas_goma_descontaminantes():
    img, d = canvas()
    p = HAZMAT
    # Bota izquierda
    d.rectangle([2, 4, 6, 12], fill=p["base"], outline=OUTLINE)
    d.rectangle([1, 11, 7, 14], fill=p["base"], outline=OUTLINE)
    d.rectangle([1, 14, 7, 15], fill=OUTLINE)
    d.line([(3, 5), (5, 5)], fill=p["light"])
    # Bota derecha
    d.rectangle([9, 4, 13, 12], fill=p["base"], outline=OUTLINE)
    d.rectangle([8, 11, 14, 14], fill=p["base"], outline=OUTLINE)
    d.rectangle([8, 14, 14, 15], fill=OUTLINE)
    d.line([(10, 5), (12, 5)], fill=p["light"])
    # Perforaciones
    px(d, 4, 8, OUTLINE)
    px(d, 5, 9, OUTLINE)
    px(d, 11, 7, OUTLINE)
    px(d, 12, 9, OUTLINE)
    # Parches
    d.rectangle([3, 10, 5, 11], fill=RUBBER["base"], outline=OUTLINE)
    d.rectangle([10, 10, 12, 11], fill=RUBBER["base"], outline=OUTLINE)
    return img


def lona_cuarentena():
    img, d = canvas()
    p = (198, 172, 64)
    d.polygon([(2, 3), (13, 4), (14, 12), (3, 14), (1, 9)], fill=p, outline=OUTLINE)
    d.line([(3, 4), (12, 5)], fill=(230, 204, 100))
    d.line([(3, 13), (13, 11)], fill=(140, 116, 36))
    # Ojales
    for x, y in ((2, 4), (13, 5), (13, 11), (3, 13)):
        px(d, x, y, OUTLINE)
    # Franjas de peligro
    for x in (9, 11):
        d.line([(x, 6), (x + 2, 9)], fill=BLACK)
    # Simbolo
    d.ellipse([5, 7, 8, 10], fill=BLACK)
    px(d, 6, 8, p)
    px(d, 7, 9, p)
    # Desgarro
    d.line([(6, 12), (7, 14)], fill=OUTLINE)
    return img


def mascarilla_gp5():
    img, d = canvas()
    p = (90, 96, 88)
    d.ellipse([1, 4, 13, 13], fill=p, outline=OUTLINE)
    # Lentes
    d.ellipse([3, 6, 6, 9], fill=GLASS["dark"], outline=OUTLINE)
    d.ellipse([8, 6, 11, 9], fill=GLASS["dark"], outline=OUTLINE)
    px(d, 4, 7, GLASS["light"])
    px(d, 9, 7, GLASS["light"])
    # Filtro
    d.ellipse([5, 9, 9, 13], fill=STEEL["base"], outline=OUTLINE)
    d.ellipse([6, 10, 8, 12], fill=STEEL["dark"])
    d.line([(6, 11), (8, 11)], fill=STEEL["light"])
    # Correas
    d.line([(1, 7), (0, 9)], fill=OUTLINE)
    d.line([(13, 7), (15, 9)], fill=OUTLINE)
    # Borde derretido
    d.line([(10, 12), (12, 13), (11, 14)], fill=OUTLINE)
    return img


def gradilla_tubos_ensayo():
    img, d = canvas()
    # Gradilla
    d.rectangle([2, 8, 13, 13], fill=WOOD["base"], outline=OUTLINE)
    d.rectangle([2, 5, 13, 7], fill=WOOD["light"], outline=OUTLINE)
    d.line([(3, 9), (12, 9)], fill=WOOD["dark"])
    # Tubos
    colors = [CHEM_GREEN["base"], YELLOW, RED]
    for i, x in enumerate((4, 7, 10)):
        d.rectangle([x, 2, x + 1, 9], fill=(200, 220, 220), outline=OUTLINE)
        d.rectangle([x, 6, x + 1, 8], fill=colors[i])
        d.ellipse([x - 1, 1, x + 2, 3], fill=(220, 240, 240), outline=OUTLINE)
    # Tubo roto
    d.line([(10, 2), (11, 4)], fill=OUTLINE)
    px(d, 12, 3, (200, 220, 220))
    # Gradilla derretida
    d.line([(3, 12), (5, 13)], fill=OUTLINE)
    return img


# ---------------------------------------------------------------------------
# Militar
# ---------------------------------------------------------------------------

MIL_OLIVE = {"base": (98, 112, 74), "light": (136, 152, 102), "dark": (64, 76, 48)}
KHAKI = {"base": (140, 132, 96), "light": (176, 168, 126), "dark": (96, 90, 62)}
GUNMETAL = {"base": (82, 86, 88), "light": (120, 126, 128), "dark": (50, 54, 56)}


def bateria_tanque_t72():
    img, d = canvas()
    p = MIL_OLIVE
    bevel(d, 2, 5, 13, 12, (54, 58, 48), (86, 90, 74), (32, 34, 28))
    d.rectangle([2, 4, 13, 6], fill=(70, 74, 58), outline=OUTLINE)
    # Terminales
    d.rectangle([4, 2, 5, 4], fill=LEAD_LIGHT, outline=OUTLINE)
    d.rectangle([11, 2, 12, 4], fill=LEAD_LIGHT, outline=OUTLINE)
    # Tapones
    for x in (5, 7, 9, 11):
        d.ellipse([x, 4, x + 1, 5], fill=(100, 104, 86), outline=OUTLINE)
    # Etiqueta
    d.rectangle([4, 7, 11, 10], fill=(120, 110, 70), outline=OUTLINE)
    d.line([(5, 8), (10, 8)], fill=WHITE)
    d.line([(5, 9), (8, 9)], fill=WHITE)
    # Fuga de acido
    d.line([(12, 11), (13, 13), (13, 14)], fill=(150, 190, 120))
    px(d, 13, 15, (180, 220, 150))
    d.line([(3, 10), (4, 12)], fill=OUTLINE)
    rust_spots(d, [(4, 11), (10, 11)], RUST)
    return img


def visor_nocturno_pnv57():
    img, d = canvas()
    p = MIL_OLIVE
    d.rectangle([3, 5, 12, 11], fill=p["base"], outline=OUTLINE)
    d.rectangle([1, 6, 3, 10], fill=p["dark"], outline=OUTLINE)
    d.rectangle([12, 6, 14, 10], fill=p["dark"], outline=OUTLINE)
    # Lentes
    d.ellipse([2, 4, 7, 10], fill=OUTLINE)
    d.ellipse([3, 5, 6, 9], fill=GLASS["dark"])
    d.ellipse([4, 6, 5, 8], fill=GLASS["light"])
    d.ellipse([9, 4, 14, 10], fill=OUTLINE)
    d.ellipse([10, 5, 13, 9], fill=GLASS["dark"])
    d.ellipse([11, 6, 12, 8], fill=GLASS["light"])
    # Mando
    d.rectangle([7, 2, 8, 4], fill=p["dark"], outline=OUTLINE)
    # Correa
    d.line([(1, 6), (0, 4)], fill=OUTLINE)
    d.line([(14, 6), (15, 4)], fill=OUTLINE)
    d.line([(4, 5), (6, 5)], fill=p["light"])
    return img


def chaleco_balistico_6b3():
    img, d = canvas()
    p = MIL_OLIVE
    # Hombreras
    d.rectangle([2, 3, 5, 7], fill=p["base"], outline=OUTLINE)
    d.rectangle([10, 3, 13, 7], fill=p["base"], outline=OUTLINE)
    # Cuerpo
    d.polygon([(3, 5), (12, 5), (13, 9), (12, 13), (3, 13), (2, 9)],
              fill=p["base"], outline=OUTLINE)
    d.line([(4, 6), (11, 6)], fill=p["light"])
    # Placas
    d.rectangle([4, 7, 7, 11], fill=p["dark"], outline=OUTLINE)
    d.rectangle([8, 7, 11, 11], fill=p["dark"], outline=OUTLINE)
    # Correas
    d.line([(5, 5), (5, 3)], fill=p["dark"])
    d.line([(10, 5), (10, 3)], fill=p["dark"])
    # Impacto
    d.ellipse([9, 9, 10, 10], fill=OUTLINE)
    d.line([(10, 9), (12, 8)], fill=OUTLINE)
    d.line([(9, 10), (8, 12)], fill=OUTLINE)
    px(d, 4, 12, p["light"])
    px(d, 11, 6, p["light"])
    return img


def radio_campana_r159():
    img, d = canvas()
    p = MIL_OLIVE
    bevel(d, 2, 5, 11, 13, p["base"], p["light"], p["dark"])
    # Panel
    d.rectangle([3, 7, 10, 11], fill=p["dark"], outline=OUTLINE)
    d.ellipse([4, 8, 6, 10], fill=OUTLINE)
    px(d, 5, 9, WHITE)
    d.rectangle([7, 8, 9, 9], fill=(60, 80, 60), outline=OUTLINE)
    px(d, 8, 8, (120, 200, 120))
    px(d, 4, 12, RED)
    px(d, 7, 12, YELLOW)
    # Antena
    d.line([(10, 5), (14, 0)], fill=OUTLINE)
    d.line([(11, 4), (14, 1)], fill=(150, 150, 140))
    # Auricular
    d.rectangle([12, 8, 14, 12], fill=p["dark"], outline=OUTLINE)
    d.line([(13, 9), (13, 11)], fill=p["light"])
    d.line([(2, 6), (1, 9)], fill=OUTLINE)
    return img


def modulo_punteria_btr():
    img, d = canvas()
    p = {"base": (78, 86, 80), "light": (112, 120, 112), "dark": (48, 54, 50)}
    bevel(d, 2, 5, 13, 12, p["base"], p["light"], p["dark"])
    # Lente principal
    d.ellipse([3, 6, 8, 11], fill=OUTLINE)
    d.ellipse([4, 7, 7, 10], fill=GLASS["dark"])
    d.ellipse([5, 8, 6, 9], fill=GLASS["light"])
    d.line([(4, 8), (7, 8)], fill=(120, 200, 160))
    d.line([(5, 7), (5, 10)], fill=(120, 200, 160))
    # Ocular
    d.ellipse([10, 7, 13, 10], fill=OUTLINE)
    d.ellipse([11, 8, 12, 9], fill=GLASS["base"])
    # Soporte
    d.rectangle([5, 12, 10, 14], fill=p["dark"], outline=OUTLINE)
    d.rectangle([7, 3, 8, 5], fill=p["dark"], outline=OUTLINE)
    d.line([(3, 6), (12, 6)], fill=(120, 128, 120))
    return img


def dron_reconocimiento():
    img, d = canvas()
    p = (60, 64, 66)
    # Brazos
    d.line([(7, 7), (2, 2)], fill=OUTLINE, width=2)
    d.line([(8, 7), (13, 2)], fill=OUTLINE, width=2)
    d.line([(7, 8), (2, 13)], fill=OUTLINE, width=2)
    d.line([(8, 8), (13, 13)], fill=OUTLINE, width=2)
    # Rotores
    for cx, cy in ((2, 2), (13, 2), (2, 13), (13, 13)):
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(80, 84, 86), outline=OUTLINE)
        d.line([(cx - 2, cy), (cx + 2, cy)], fill=(150, 154, 156))
    # Cuerpo
    d.rectangle([6, 6, 9, 9], fill=p, outline=OUTLINE)
    d.line([(7, 6), (8, 6)], fill=(100, 104, 106))
    # Camara
    d.ellipse([6, 9, 9, 12], fill=OUTLINE)
    d.ellipse([7, 10, 8, 11], fill=GLASS["base"])
    # Antena
    d.line([(8, 6), (8, 4)], fill=OUTLINE)
    px(d, 8, 3, RED)
    return img


def placa_balistica_acero():
    img, d = canvas()
    p = (96, 104, 96)
    d.polygon([(3, 3), (12, 3), (14, 6), (13, 13), (2, 13), (1, 6)],
              fill=p, outline=OUTLINE)
    d.line([(4, 4), (11, 4)], fill=(140, 148, 140))
    d.line([(3, 12), (12, 12)], fill=(60, 66, 60))
    # Abolladuras
    for x, y in ((5, 7), (9, 9), (7, 11)):
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(70, 76, 70), outline=OUTLINE)
    # Impacto
    d.ellipse([10, 6, 11, 7], fill=OUTLINE)
    d.line([(11, 7), (12, 9)], fill=OUTLINE)
    # Correas
    d.line([(2, 5), (0, 4)], fill=OUTLINE)
    d.line([(13, 5), (15, 4)], fill=OUTLINE)
    rust_spots(d, [(4, 10), (8, 6)], RUST)
    return img


def eslabon_oruga_tanque():
    img, d = canvas()
    p = (84, 88, 90)
    d.rectangle([2, 8, 13, 13], fill=p, outline=OUTLINE)
    d.line([(3, 9), (12, 9)], fill=(120, 124, 126))
    # Cleat
    d.rectangle([6, 5, 9, 8], fill=(100, 104, 106), outline=OUTLINE)
    d.line([(7, 5), (8, 5)], fill=(140, 144, 146))
    # Pasadores
    for x in (4, 11):
        d.ellipse([x - 1, 10, x + 1, 12], fill=OUTLINE)
        d.ellipse([x, 10, x, 11], fill=(150, 154, 156))
    d.line([(2, 10), (1, 12)], fill=OUTLINE)
    d.line([(13, 10), (14, 12)], fill=OUTLINE)
    rust_spots(d, [(3, 12), (12, 11), (6, 6)], RUST)
    return img


def caja_municion_50():
    img, d = canvas()
    p = MIL_OLIVE
    bevel(d, 2, 5, 13, 12, p["base"], p["light"], p["dark"])
    d.rectangle([1, 4, 14, 6], fill=p["light"], outline=OUTLINE)
    d.line([(2, 5), (13, 5)], fill=p["dark"])
    d.arc([6, 2, 9, 5], 180, 360, fill=OUTLINE)
    # Cierres
    d.rectangle([3, 6, 4, 8], fill=p["dark"], outline=OUTLINE)
    d.rectangle([11, 6, 12, 8], fill=p["dark"], outline=OUTLINE)
    # Rotulo 50 (fuente 3x5)
    for x, y in ((5, 7), (6, 7), (7, 7), (5, 8), (5, 9), (6, 9), (7, 9),
                 (7, 10), (5, 11), (6, 11), (7, 11)):
        px(d, x, y, WHITE)
    for x, y in ((9, 7), (10, 7), (11, 7), (9, 8), (11, 8), (9, 9), (11, 9),
                 (9, 10), (11, 10), (9, 11), (10, 11), (11, 11)):
        px(d, x, y, WHITE)
    # Desgaste
    px(d, 4, 11, p["dark"])
    px(d, 11, 11, p["dark"])
    return img


def casco_ssh68():
    img, d = canvas()
    p = MIL_OLIVE
    d.ellipse([2, 3, 13, 12], fill=p["base"], outline=OUTLINE)
    d.rectangle([1, 9, 14, 12], fill=p["base"], outline=OUTLINE)
    d.line([(2, 9), (13, 9)], fill=p["light"])
    d.line([(2, 12), (13, 12)], fill=p["dark"])
    # Estrella roja
    for x, y in ((7, 5), (8, 5), (6, 6), (7, 6), (8, 6), (9, 6),
                 (7, 7), (8, 7), (6, 8), (9, 8)):
        px(d, x, y, RED)
    # Abolladuras
    d.line([(4, 6), (5, 8)], fill=p["dark"])
    px(d, 11, 7, p["dark"])
    px(d, 10, 10, p["dark"])
    return img


def cargador_baquelita_ak74():
    img, d = canvas()
    p = (152, 86, 46)
    light = (192, 118, 68)
    dark = (100, 52, 26)
    d.polygon([(4, 2), (10, 2), (11, 6), (10, 10), (8, 14), (4, 14), (6, 10), (5, 6)],
              fill=p, outline=OUTLINE)
    for y in (5, 7, 9, 11):
        d.line([(5, y), (10, y)], fill=dark)
    d.line([(5, 3), (9, 3)], fill=light)
    d.line([(4, 14), (8, 14)], fill=dark)
    # Cartucho superior
    d.rectangle([6, 1, 8, 2], fill=BRASS["base"], outline=OUTLINE)
    d.line([(7, 8), (8, 10)], fill=OUTLINE)
    return img


def red_camuflaje():
    img, d = canvas()
    d.polygon([(2, 3), (13, 4), (14, 12), (3, 14), (1, 9)],
              fill=(110, 106, 78), outline=OUTLINE)
    # Manchas de camuflaje
    for x, y, w, h, c in (
        (3, 5, 3, 2, (80, 92, 58)),
        (8, 4, 3, 2, (140, 132, 96)),
        (4, 8, 4, 3, (70, 80, 52)),
        (9, 8, 3, 3, (150, 142, 104)),
        (5, 12, 3, 2, (80, 92, 58)),
    ):
        d.rectangle([x, y, x + w, y + h], fill=c)
    for x in range(3, 14, 3):
        d.line([(x, 4), (x - 1, 13)], fill=(80, 78, 58))
    # Agujero quemado
    d.ellipse([9, 10, 12, 13], fill=(0, 0, 0, 0), outline=OUTLINE)
    d.line([(2, 3), (13, 4)], fill=(160, 150, 110))
    return img


def botas_paracaidista():
    img, d = canvas()
    p = (110, 82, 52)
    light = (146, 112, 72)
    dark = (70, 50, 32)
    # Bota izquierda
    d.rectangle([2, 4, 6, 12], fill=p, outline=OUTLINE)
    d.rectangle([1, 11, 7, 14], fill=p, outline=OUTLINE)
    d.rectangle([1, 14, 7, 15], fill=dark)
    d.line([(3, 5), (5, 5)], fill=light)
    for y in (6, 8, 10):
        d.line([(3, y), (5, y)], fill=(190, 170, 130))
    # Bota derecha
    d.rectangle([9, 4, 13, 12], fill=p, outline=OUTLINE)
    d.rectangle([8, 11, 14, 14], fill=p, outline=OUTLINE)
    d.rectangle([8, 14, 14, 15], fill=dark)
    d.line([(10, 5), (12, 5)], fill=light)
    for y in (6, 8, 10):
        d.line([(10, y), (12, y)], fill=(190, 170, 130))
    px(d, 4, 9, dark)
    px(d, 11, 9, dark)
    return img


# ---------------------------------------------------------------------------
# Hospital
# ---------------------------------------------------------------------------

MED_WHITE = {"base": (198, 204, 204), "light": (230, 236, 236), "dark": (142, 148, 148)}
SURG_BLUE = {"base": (88, 132, 148), "light": (124, 172, 188), "dark": (54, 88, 102)}
STEEL_MED = {"base": (150, 158, 164), "light": (196, 204, 210), "dark": (96, 104, 110)}


def desfibrilador_portatil():
    img, d = canvas()
    p = MED_WHITE
    bevel(d, 2, 5, 12, 12, p["base"], p["light"], p["dark"])
    # Pantalla
    d.rectangle([4, 6, 9, 8], fill=(40, 70, 60), outline=OUTLINE)
    d.line([(5, 7), (8, 7)], fill=(120, 220, 140))
    # Selector
    d.ellipse([4, 10, 6, 12], fill=OUTLINE)
    px(d, 5, 11, WHITE)
    # Cruz roja
    d.rectangle([9, 10, 11, 11], fill=RED)
    d.rectangle([10, 9, 10, 12], fill=RED)
    # Paletas
    d.rectangle([12, 3, 14, 5], fill=(70, 74, 78), outline=OUTLINE)
    d.rectangle([13, 5, 15, 7], fill=(70, 74, 78), outline=OUTLINE)
    d.line([(12, 5), (10, 7)], fill=OUTLINE)
    d.line([(14, 7), (12, 9)], fill=OUTLINE)
    # Asa
    d.arc([5, 2, 9, 5], 180, 360, fill=OUTLINE)
    return img


def microscopio_quirurgico():
    img, d = canvas()
    p = MED_WHITE
    # Base
    d.rectangle([2, 13, 13, 15], fill=(90, 96, 100), outline=OUTLINE)
    d.line([(3, 14), (12, 14)], fill=(140, 146, 150))
    # Columna
    d.rectangle([6, 6, 8, 13], fill=(110, 116, 120), outline=OUTLINE)
    # Mandos de enfoque
    d.ellipse([4, 8, 6, 10], fill=OUTLINE)
    px(d, 5, 9, (160, 166, 170))
    d.ellipse([8, 8, 10, 10], fill=OUTLINE)
    px(d, 9, 9, (160, 166, 170))
    # Brazo
    d.rectangle([7, 4, 11, 6], fill=(110, 116, 120), outline=OUTLINE)
    # Cabezal
    d.rectangle([9, 2, 13, 5], fill=p["base"], outline=OUTLINE)
    # Oculares
    d.rectangle([9, 0, 10, 2], fill=(150, 156, 160), outline=OUTLINE)
    d.rectangle([12, 0, 13, 2], fill=(150, 156, 160), outline=OUTLINE)
    px(d, 9, 0, WHITE)
    px(d, 12, 0, WHITE)
    # Objetivo
    d.rectangle([10, 5, 11, 8], fill=(70, 76, 80), outline=OUTLINE)
    d.ellipse([9, 8, 12, 10], fill=GLASS["dark"], outline=OUTLINE)
    px(d, 10, 8, GLASS["light"])
    # Platina
    d.rectangle([6, 10, 11, 11], fill=(150, 156, 160), outline=OUTLINE)
    d.line([(7, 10), (10, 10)], fill=(200, 206, 210))
    return img


def ventilador_pulmonar_uci():
    img, d = canvas()
    p = MED_WHITE
    bevel(d, 2, 4, 12, 12, p["base"], p["light"], p["dark"])
    # Pantalla
    d.rectangle([4, 5, 9, 8], fill=(40, 64, 80), outline=OUTLINE)
    d.line([(5, 6), (6, 7), (7, 6), (8, 7)], fill=(120, 220, 240))
    # Mandos
    d.ellipse([4, 10, 6, 12], fill=OUTLINE)
    px(d, 5, 11, WHITE)
    d.rectangle([8, 10, 10, 11], fill=(90, 96, 100), outline=OUTLINE)
    # Tubos
    d.line([(10, 9), (13, 10), (14, 12)], fill=OUTLINE)
    d.line([(10, 10), (12, 11), (13, 13)], fill=OUTLINE)
    d.line([(11, 10), (13, 11)], fill=(150, 200, 210))
    # Soporte
    d.rectangle([6, 12, 7, 14], fill=(90, 96, 100), outline=OUTLINE)
    d.rectangle([4, 14, 9, 15], fill=(70, 76, 80), outline=OUTLINE)
    return img


def monitor_signos_vitales():
    img, d = canvas()
    p = (70, 74, 78)
    bevel(d, 2, 3, 12, 12, p, (110, 114, 118), (42, 46, 50))
    # Pantalla
    d.rectangle([4, 5, 10, 9], fill=(30, 50, 40), outline=OUTLINE)
    d.line([(5, 7), (6, 7), (6, 6), (7, 8), (8, 5), (9, 8), (10, 7)],
           fill=(120, 230, 150))
    # Botones
    for x in (4, 6, 8):
        px(d, x, 11, (180, 184, 188))
    d.rectangle([10, 10, 11, 11], fill=RED, outline=OUTLINE)
    # Soporte
    d.rectangle([6, 12, 7, 14], fill=(70, 74, 78), outline=OUTLINE)
    d.rectangle([4, 14, 9, 15], fill=(50, 54, 58), outline=OUTLINE)
    return img


def autoclave_esterilizacion():
    img, d = canvas()
    p = MED_WHITE
    # Camara
    d.rectangle([2, 6, 13, 12], fill=p["base"], outline=OUTLINE)
    d.ellipse([1, 6, 3, 12], fill=p["base"], outline=OUTLINE)
    d.ellipse([12, 6, 14, 12], fill=p["base"], outline=OUTLINE)
    d.line([(3, 7), (12, 7)], fill=p["light"])
    # Puerta
    d.rectangle([2, 6, 5, 12], fill=(150, 156, 160), outline=OUTLINE)
    d.ellipse([3, 7, 4, 11], fill=GLASS["dark"], outline=OUTLINE)
    d.line([(5, 8), (5, 10)], fill=(90, 96, 100))
    # Manometro
    d.ellipse([10, 4, 12, 6], fill=OUTLINE)
    d.ellipse([10, 4, 11, 5], fill=(220, 220, 210))
    d.line([(10, 5), (11, 4)], fill=RED)
    # Patas
    d.rectangle([3, 12, 4, 14], fill=(90, 96, 100), outline=OUTLINE)
    d.rectangle([11, 12, 12, 14], fill=(90, 96, 100), outline=OUTLINE)
    # Vapor
    px(d, 13, 3, (200, 220, 220))
    px(d, 14, 2, (180, 200, 200))
    return img


def camilla_aislamiento():
    img, d = canvas()
    # Bastidor
    d.rectangle([1, 9, 14, 12], fill=(110, 116, 120), outline=OUTLINE)
    d.line([(2, 10), (13, 10)], fill=(160, 166, 170))
    # Ruedas
    for x in (2, 12):
        d.ellipse([x, 12, x + 2, 14], fill=OUTLINE)
        px(d, x + 1, 13, (150, 156, 160))
    # Cobertura
    d.polygon([(3, 4), (12, 4), (13, 9), (2, 9)], fill=(180, 210, 220), outline=OUTLINE)
    d.line([(4, 5), (11, 5)], fill=(220, 240, 246))
    # Cremallera
    d.line([(8, 4), (8, 9)], fill=OUTLINE)
    # Simbolo
    d.ellipse([4, 6, 6, 8], fill=YELLOW, outline=OUTLINE)
    px(d, 5, 7, BLACK)
    # Silueta
    d.line([(6, 6), (9, 8)], fill=(120, 140, 150))
    return img


def rollo_vendas_yodo():
    img, d = canvas()
    # Rollo
    d.ellipse([3, 4, 12, 13], fill=(220, 220, 210), outline=OUTLINE)
    d.ellipse([5, 6, 10, 11], fill=(190, 190, 180), outline=OUTLINE)
    d.ellipse([7, 8, 8, 9], fill=OUTLINE)
    d.arc([4, 5, 11, 12], 180, 360, fill=(160, 160, 150))
    # Manchas de yodo
    for x, y in ((4, 7), (6, 10), (9, 5), (10, 9)):
        px(d, x, y, (150, 90, 50))
    # Extremo suelto
    d.polygon([(10, 10), (14, 9), (14, 12), (11, 12)],
              fill=(220, 220, 210), outline=OUTLINE)
    return img


def sabana_quirurgica():
    img, d = canvas()
    d.polygon([(2, 4), (13, 4), (14, 12), (3, 13), (1, 9)],
              fill=(210, 220, 220), outline=OUTLINE)
    d.line([(3, 5), (12, 5)], fill=(240, 248, 248))
    d.line([(3, 12), (13, 11)], fill=(170, 180, 180))
    d.line([(5, 6), (4, 11)], fill=(180, 190, 190))
    d.line([(10, 6), (11, 10)], fill=(180, 190, 190))
    # Mancha de sangre
    d.ellipse([6, 7, 9, 10], fill=(150, 52, 44), outline=(110, 30, 26))
    d.ellipse([7, 8, 8, 9], fill=(120, 36, 30))
    # Esquina doblada
    d.polygon([(13, 4), (14, 8), (10, 4)], fill=(230, 238, 238), outline=OUTLINE)
    return img


def bata_paciente():
    img, d = canvas()
    p = (180, 200, 210)
    dark = (130, 150, 160)
    d.polygon([(4, 4), (11, 4), (12, 7), (11, 13), (4, 13), (3, 7)],
              fill=p, outline=OUTLINE)
    d.rectangle([1, 5, 4, 9], fill=p, outline=OUTLINE)
    d.rectangle([11, 5, 14, 9], fill=p, outline=OUTLINE)
    # Escote en V
    d.polygon([(6, 4), (9, 4), (8, 7), (7, 7)], fill=(0, 0, 0, 0), outline=OUTLINE)
    # Cintas
    d.line([(4, 7), (2, 8)], fill=dark)
    d.line([(11, 7), (13, 8)], fill=dark)
    # Mancha
    px(d, 6, 10, (150, 52, 44))
    px(d, 7, 11, (150, 52, 44))
    d.line([(4, 13), (11, 13)], fill=dark)
    return img


def bandeja_instrumentos():
    img, d = canvas()
    # Bandeja con borde
    d.polygon([(1, 8), (14, 8), (13, 13), (2, 13)], fill=(120, 126, 130), outline=OUTLINE)
    d.polygon([(2, 9), (13, 9), (12, 12), (3, 12)], fill=(180, 186, 190), outline=OUTLINE)
    # Paño
    d.rectangle([3, 9, 12, 11], fill=(60, 96, 116), outline=OUTLINE)
    # Bisturi
    d.line([(4, 10), (7, 10)], fill=(230, 236, 240))
    d.line([(7, 10), (9, 9)], fill=(200, 206, 210))
    px(d, 9, 9, WHITE)
    # Tijeras
    d.ellipse([4, 11, 5, 12], outline=(230, 236, 240))
    d.ellipse([6, 11, 7, 12], outline=(230, 236, 240))
    d.line([(5, 11), (8, 10)], fill=(230, 236, 240))
    # Jeringa
    d.line([(9, 10), (12, 10)], fill=(230, 236, 240))
    px(d, 12, 10, RED)
    return img


def soporte_suero():
    img, d = canvas()
    # Poste
    d.rectangle([7, 2, 8, 13], fill=(150, 156, 160), outline=OUTLINE)
    # Base
    d.rectangle([4, 13, 11, 15], fill=(90, 96, 100), outline=OUTLINE)
    d.ellipse([2, 14, 13, 15], fill=OUTLINE)
    # Gancho
    d.arc([6, 1, 9, 3], 180, 360, fill=OUTLINE)
    # Bolsa
    d.rectangle([4, 3, 7, 7], fill=(170, 210, 220), outline=OUTLINE)
    d.line([(5, 4), (6, 4)], fill=(220, 245, 250))
    d.line([(4, 6), (7, 6)], fill=(80, 140, 160))
    # Tubo
    d.line([(7, 7), (9, 9), (9, 12)], fill=OUTLINE)
    d.line([(8, 8), (8, 11)], fill=(170, 210, 220))
    return img


def bolsa_desechos_biologicos():
    img, d = canvas()
    p = (198, 172, 64)
    d.polygon([(3, 4), (12, 4), (13, 13), (2, 13)], fill=p, outline=OUTLINE)
    d.line([(4, 5), (11, 5)], fill=(230, 204, 100))
    # Nudo
    d.polygon([(5, 2), (10, 2), (9, 4), (6, 4)], fill=(160, 136, 40), outline=OUTLINE)
    d.line([(5, 2), (6, 0)], fill=OUTLINE)
    d.line([(10, 2), (9, 0)], fill=OUTLINE)
    # Simbolo
    d.ellipse([6, 7, 9, 10], fill=BLACK)
    px(d, 7, 8, p)
    px(d, 8, 9, p)
    # Franja roja
    d.rectangle([3, 11, 12, 12], fill=(150, 52, 44), outline=OUTLINE)
    return img


def muleta_aluminio():
    img, d = canvas()
    p = (170, 176, 182)
    d.rectangle([4, 1, 11, 3], fill=(90, 96, 100), outline=OUTLINE)
    d.rectangle([5, 3, 6, 13], fill=p, outline=OUTLINE)
    d.rectangle([9, 3, 10, 13], fill=p, outline=OUTLINE)
    d.rectangle([5, 8, 10, 9], fill=(120, 126, 130), outline=OUTLINE)
    d.line([(5, 4), (6, 4)], fill=WHITE)
    d.rectangle([6, 13, 9, 15], fill=(60, 64, 68), outline=OUTLINE)
    for y in (5, 7, 11):
        px(d, 5, y, OUTLINE)
        px(d, 9, y, OUTLINE)
    return img


# ---------------------------------------------------------------------------
# Residencial
# ---------------------------------------------------------------------------

WOOD_DARK = {"base": (122, 88, 56), "light": (160, 120, 78), "dark": (80, 56, 34)}
APPLIANCE = {"base": (190, 184, 166), "light": (224, 218, 200), "dark": (136, 130, 114)}
FADED_RED = {"base": (150, 70, 60), "light": (190, 100, 86), "dark": (100, 44, 38)}
FUR = {"base": (110, 92, 72), "light": (150, 128, 102), "dark": (74, 60, 46)}


def abrigo_afghanka():
    img, d = canvas()
    p = (110, 104, 76)
    light = (146, 138, 102)
    dark = (74, 70, 50)
    # Mangas
    d.rectangle([1, 6, 4, 12], fill=p, outline=OUTLINE)
    d.rectangle([11, 6, 14, 12], fill=p, outline=OUTLINE)
    # Cuerpo
    d.polygon([(3, 4), (12, 4), (13, 7), (12, 14), (3, 14), (2, 7)],
              fill=p, outline=OUTLINE)
    # Cuello de piel
    d.rectangle([4, 2, 11, 4], fill=(130, 112, 86), outline=OUTLINE)
    d.line([(5, 3), (10, 3)], fill=(160, 140, 110))
    # Cinturon
    d.rectangle([2, 9, 13, 10], fill=dark, outline=OUTLINE)
    d.rectangle([6, 9, 8, 10], fill=(160, 140, 80), outline=OUTLINE)
    # Botones y costura
    for y in (6, 8, 12):
        px(d, 7, y, (180, 170, 130))
    d.line([(7, 4), (7, 14)], fill=dark)
    px(d, 10, 11, dark)
    return img


def microondas_dnepr():
    img, d = canvas()
    p = APPLIANCE
    bevel(d, 2, 4, 13, 12, p["base"], p["light"], p["dark"])
    # Puerta
    d.rectangle([3, 5, 10, 11], fill=(160, 154, 138), outline=OUTLINE)
    d.rectangle([4, 6, 9, 9], fill=(60, 62, 64), outline=OUTLINE)
    d.line([(5, 7), (8, 7)], fill=(90, 92, 94))
    d.line([(9, 6), (9, 9)], fill=(120, 116, 104))
    # Panel
    d.rectangle([11, 5, 12, 11], fill=(150, 144, 128), outline=OUTLINE)
    for y in (6, 8, 10):
        px(d, 11, y, (80, 80, 78))
    # Quemadura
    d.line([(3, 10), (5, 12)], fill=(40, 36, 32))
    d.line([(4, 10), (6, 12)], fill=(40, 36, 32))
    d.rectangle([3, 12, 4, 13], fill=p["dark"])
    d.rectangle([11, 12, 12, 13], fill=p["dark"])
    return img


def televisor_rubin():
    img, d = canvas()
    p = WOOD_DARK
    bevel(d, 2, 4, 13, 13, p["base"], p["light"], p["dark"])
    # Pantalla
    d.rectangle([3, 5, 10, 10], fill=(44, 58, 54), outline=OUTLINE)
    d.line([(4, 6), (6, 6)], fill=(90, 120, 110))
    d.line([(4, 7), (5, 7)], fill=(70, 100, 90))
    d.line([(7, 6), (6, 8), (8, 9)], fill=(20, 24, 22))
    # Controles
    d.rectangle([11, 5, 12, 10], fill=p["dark"], outline=OUTLINE)
    for y in (6, 8):
        d.ellipse([11, y, 12, y + 1], fill=(180, 180, 170), outline=OUTLINE)
    # Antenas
    d.line([(7, 4), (5, 0)], fill=OUTLINE)
    d.line([(9, 4), (11, 0)], fill=OUTLINE)
    d.line([(7, 3), (5, 0)], fill=(160, 160, 150))
    d.line([(9, 3), (11, 0)], fill=(160, 160, 150))
    d.rectangle([3, 13, 4, 14], fill=p["dark"])
    d.rectangle([11, 13, 12, 14], fill=p["dark"])
    return img


def lavadora_vyatka():
    img, d = canvas()
    p = (198, 198, 190)
    light = (230, 230, 222)
    dark = (142, 142, 134)
    bevel(d, 2, 3, 13, 13, p, light, dark)
    # Panel
    d.rectangle([3, 4, 12, 6], fill=(170, 170, 162), outline=OUTLINE)
    d.ellipse([4, 4, 6, 6], fill=OUTLINE)
    px(d, 5, 5, WHITE)
    d.rectangle([8, 4, 10, 5], fill=(90, 90, 86), outline=OUTLINE)
    # Puerta
    d.ellipse([4, 7, 11, 13], fill=OUTLINE)
    d.ellipse([5, 8, 10, 12], fill=(120, 140, 150))
    d.ellipse([6, 9, 9, 11], fill=(160, 190, 200))
    d.arc([5, 8, 10, 12], 200, 300, fill=(200, 220, 230))
    # Oxido
    px(d, 12, 12, (140, 80, 40))
    px(d, 3, 12, (140, 80, 40))
    return img


def maquina_coser_podolsk():
    img, d = canvas()
    p = (48, 48, 50)
    light = (86, 86, 88)
    dark = (28, 28, 30)
    # Base
    d.rectangle([1, 12, 14, 14], fill=(120, 86, 52), outline=OUTLINE)
    # Cuerpo
    d.rectangle([4, 6, 10, 12], fill=p, outline=OUTLINE)
    # Brazo
    d.rectangle([4, 4, 12, 6], fill=p, outline=OUTLINE)
    # Volante
    d.ellipse([11, 6, 14, 9], fill=OUTLINE)
    d.ellipse([12, 7, 13, 8], fill=light)
    d.line([(12, 7), (13, 8)], fill=dark)
    # Barra de aguja
    d.rectangle([3, 7, 4, 12], fill=(150, 156, 160), outline=OUTLINE)
    # Calcomanias
    d.line([(5, 7), (9, 7)], fill=(188, 158, 82))
    d.line([(5, 9), (8, 9)], fill=(188, 158, 82))
    # Carrete
    d.rectangle([8, 2, 9, 4], fill=(160, 120, 80), outline=OUTLINE)
    return img


def aspiradora_raketa():
    img, d = canvas()
    p = FADED_RED
    # Canister
    d.rectangle([2, 7, 11, 12], fill=p["base"], outline=OUTLINE)
    d.ellipse([1, 7, 3, 12], fill=p["base"], outline=OUTLINE)
    d.ellipse([10, 7, 12, 12], fill=p["base"], outline=OUTLINE)
    d.line([(3, 8), (10, 8)], fill=p["light"])
    # Ruedas
    d.ellipse([2, 12, 4, 14], fill=OUTLINE)
    d.ellipse([9, 12, 11, 14], fill=OUTLINE)
    # Manguera
    d.line([(11, 8), (14, 6), (14, 3)], fill=OUTLINE)
    d.line([(12, 8), (13, 6)], fill=(80, 80, 80))
    d.rectangle([13, 1, 14, 3], fill=(80, 80, 80), outline=OUTLINE)
    # Asa
    d.arc([4, 4, 8, 7], 180, 360, fill=OUTLINE)
    return img


def taza_peltre():
    img, d = canvas()
    p = (150, 156, 162)
    light = (196, 202, 208)
    dark = (100, 106, 112)
    # Taza
    d.rectangle([3, 5, 10, 12], fill=p, outline=OUTLINE)
    d.ellipse([3, 4, 10, 6], fill=light, outline=OUTLINE)
    d.line([(4, 6), (4, 11)], fill=light)
    d.line([(9, 6), (9, 11)], fill=dark)
    # Asa
    d.arc([10, 6, 14, 11], 270, 90, fill=OUTLINE)
    d.arc([11, 7, 13, 10], 270, 90, fill=p)
    # Emblema
    d.ellipse([5, 8, 8, 11], fill=(150, 60, 50))
    px(d, 6, 9, YELLOW)
    px(d, 7, 10, YELLOW)
    px(d, 5, 11, dark)
    return img


def olla_presion():
    img, d = canvas()
    p = (170, 176, 182)
    light = (210, 216, 222)
    dark = (110, 116, 122)
    # Olla
    d.rectangle([3, 7, 12, 12], fill=p, outline=OUTLINE)
    d.ellipse([2, 7, 4, 12], fill=p, outline=OUTLINE)
    d.ellipse([11, 7, 13, 12], fill=p, outline=OUTLINE)
    d.line([(4, 8), (11, 8)], fill=light)
    # Tapa
    d.ellipse([2, 5, 13, 8], fill=light, outline=OUTLINE)
    d.line([(3, 6), (12, 6)], fill=WHITE)
    # Valvula
    d.rectangle([7, 3, 8, 5], fill=dark, outline=OUTLINE)
    d.ellipse([6, 2, 9, 4], fill=dark, outline=OUTLINE)
    # Asas
    d.rectangle([1, 8, 3, 9], fill=dark, outline=OUTLINE)
    d.rectangle([12, 8, 14, 9], fill=dark, outline=OUTLINE)
    px(d, 5, 10, dark)
    px(d, 10, 11, dark)
    return img


def radiador_hierro():
    img, d = canvas()
    p = (110, 104, 96)
    light = (150, 144, 134)
    dark = (70, 66, 60)
    for x in (2, 4, 6, 8, 10, 12):
        d.rectangle([x, 4, x + 1, 12], fill=p, outline=OUTLINE)
        d.line([(x, 5), (x, 11)], fill=light)
    d.rectangle([2, 3, 13, 4], fill=dark, outline=OUTLINE)
    d.rectangle([2, 12, 13, 13], fill=dark, outline=OUTLINE)
    d.rectangle([3, 13, 4, 15], fill=dark, outline=OUTLINE)
    d.rectangle([11, 13, 12, 15], fill=dark, outline=OUTLINE)
    rust_spots(d, [(5, 8), (9, 10), (12, 6)], RUST)
    return img


def gorro_ushanka():
    img, d = canvas()
    p = FUR
    # Copa
    d.ellipse([3, 3, 12, 10], fill=p["base"], outline=OUTLINE)
    d.rectangle([3, 7, 12, 10], fill=p["base"], outline=OUTLINE)
    # Frente
    d.rectangle([4, 6, 11, 9], fill=p["light"], outline=OUTLINE)
    # Orejeras
    d.polygon([(1, 7), (4, 7), (4, 13), (2, 12)], fill=p["base"], outline=OUTLINE)
    d.polygon([(11, 7), (14, 7), (13, 12), (11, 13)], fill=p["base"], outline=OUTLINE)
    for x in (5, 7, 9):
        px(d, x, 5, p["light"])
    d.ellipse([7, 7, 8, 8], fill=RED)
    d.line([(2, 12), (2, 14)], fill=p["dark"])
    return img


def vaqueros_rasgados():
    img, d = canvas()
    p = (70, 96, 130)
    light = (100, 130, 166)
    dark = (44, 64, 92)
    d.rectangle([3, 2, 12, 4], fill=p, outline=OUTLINE)
    d.line([(4, 3), (11, 3)], fill=light)
    d.polygon([(3, 4), (7, 4), (7, 14), (3, 14)], fill=p, outline=OUTLINE)
    d.polygon([(8, 4), (12, 4), (12, 14), (8, 14)], fill=p, outline=OUTLINE)
    d.line([(5, 5), (5, 13)], fill=dark)
    d.line([(10, 5), (10, 13)], fill=dark)
    # Desgarros
    d.polygon([(3, 9), (5, 9), (4, 11)], fill=(0, 0, 0, 0), outline=OUTLINE)
    d.polygon([(9, 8), (11, 8), (10, 10)], fill=(0, 0, 0, 0), outline=OUTLINE)
    d.rectangle([3, 2, 12, 3], fill=dark, outline=OUTLINE)
    d.rectangle([9, 11, 11, 12], fill=light, outline=OUTLINE)
    return img


def alfombra_persa():
    img, d = canvas()
    p = (140, 50, 44)
    light = (180, 80, 70)
    d.rectangle([2, 3, 13, 12], fill=p, outline=OUTLINE)
    d.rectangle([3, 4, 12, 11], outline=YELLOW)
    d.ellipse([6, 6, 9, 9], fill=(60, 70, 110), outline=YELLOW)
    d.ellipse([7, 7, 8, 8], fill=light)
    for x in (4, 11):
        px(d, x, 6, YELLOW)
        px(d, x, 9, YELLOW)
    for y in (4, 6, 8, 10):
        px(d, 1, y, (200, 190, 150))
        px(d, 14, y, (200, 190, 150))
    d.polygon([(11, 12), (13, 10), (13, 12)], fill=(0, 0, 0, 0), outline=OUTLINE)
    return img


def muneca_irradiada():
    img, d = canvas()
    skin = (210, 190, 170)
    dress = (120, 140, 100)
    hair = (90, 70, 50)
    d.ellipse([5, 2, 10, 7], fill=skin, outline=OUTLINE)
    d.arc([5, 1, 10, 6], 180, 360, fill=hair)
    px(d, 6, 4, OUTLINE)
    px(d, 9, 4, (80, 140, 80))
    px(d, 7, 6, (150, 80, 70))
    d.line([(8, 2), (8, 4), (9, 5)], fill=OUTLINE)
    d.polygon([(5, 7), (10, 7), (11, 12), (4, 12)], fill=dress, outline=OUTLINE)
    d.line([(4, 8), (2, 11)], fill=skin)
    d.line([(11, 8), (13, 11)], fill=skin)
    d.rectangle([5, 12, 6, 15], fill=skin, outline=OUTLINE)
    d.rectangle([9, 12, 10, 15], fill=skin, outline=OUTLINE)
    px(d, 5, 9, (120, 200, 100))
    px(d, 10, 10, (120, 200, 100))
    px(d, 3, 12, (120, 200, 100))
    return img


def cubiertos_acero():
    img, d = canvas()
    p = (160, 166, 172)
    light = (210, 216, 222)
    dark = (100, 106, 112)
    # Tenedor
    d.rectangle([2, 5, 3, 13], fill=p, outline=OUTLINE)
    d.line([(2, 3), (2, 5)], fill=p)
    d.line([(3, 3), (3, 5)], fill=p)
    d.line([(2, 6), (3, 6)], fill=light)
    # Cuchillo
    d.rectangle([6, 5, 7, 13], fill=p, outline=OUTLINE)
    d.polygon([(6, 3), (7, 3), (7, 6), (6, 6)], fill=light, outline=OUTLINE)
    # Cuchara
    d.ellipse([10, 3, 13, 7], fill=p, outline=OUTLINE)
    d.rectangle([11, 7, 12, 13], fill=p, outline=OUTLINE)
    d.line([(11, 4), (12, 4)], fill=light)
    d.line([(2, 13), (3, 13)], fill=dark)
    d.line([(6, 13), (7, 13)], fill=dark)
    d.line([(11, 13), (12, 13)], fill=dark)
    return img


# ---------------------------------------------------------------------------
# Electrica
# ---------------------------------------------------------------------------

def transformador_subestacion():
    img, d = canvas()
    p = (90, 96, 100)
    bevel(d, 2, 5, 13, 12, p, (130, 136, 140), (54, 60, 64))
    for x in (3, 5, 7, 9, 11):
        d.line([(x, 6), (x, 11)], fill=(60, 66, 70))
        d.line([(x + 1, 6), (x + 1, 11)], fill=(110, 116, 120))
    # Aisladores
    for x in (4, 8, 12):
        d.rectangle([x - 1, 2, x, 4], fill=(180, 176, 160), outline=OUTLINE)
        d.rectangle([x - 1, 1, x, 2], fill=(120, 116, 104), outline=OUTLINE)
    # Peligro
    d.rectangle([5, 8, 8, 10], fill=YELLOW, outline=OUTLINE)
    px(d, 6, 9, BLACK)
    d.rectangle([2, 12, 13, 13], fill=(54, 60, 64), outline=OUTLINE)
    return img


def panel_control_reactor():
    img, d = canvas()
    p = (70, 80, 90)
    bevel(d, 1, 3, 14, 13, p, (104, 114, 124), (40, 48, 56))
    # Indicadores
    for x in (3, 7):
        d.ellipse([x, 5, x + 2, 7], fill=OUTLINE)
        d.ellipse([x, 5, x + 1, 6], fill=(220, 220, 210))
        d.line([(x + 1, 6), (x + 1, 5)], fill=RED)
    # Pantalla
    d.rectangle([3, 8, 7, 10], fill=(40, 70, 60), outline=OUTLINE)
    d.line([(4, 9), (6, 9)], fill=(120, 220, 140))
    # Interruptores
    for x in (9, 11, 13):
        d.rectangle([x, 5, x, 7], fill=(160, 160, 150), outline=OUTLINE)
        px(d, x, 5, (80, 200, 80))
    # Boton rojo
    d.ellipse([9, 8, 11, 10], fill=OUTLINE)
    d.ellipse([9, 8, 10, 9], fill=RED)
    # Franjas
    for x in range(2, 14, 3):
        d.line([(x, 11), (x + 1, 12)], fill=YELLOW)
    d.line([(6, 3), (7, 5), (6, 6)], fill=OUTLINE)
    return img


def alternador_generador_diesel():
    img, d = canvas()
    p = STEEL
    d.rectangle([2, 6, 12, 11], fill=p["base"], outline=OUTLINE)
    d.ellipse([1, 6, 3, 11], fill=p["base"], outline=OUTLINE)
    d.ellipse([11, 6, 13, 11], fill=p["base"], outline=OUTLINE)
    for x in (4, 6, 8, 10):
        d.line([(x, 7), (x, 10)], fill=p["dark"])
    d.line([(3, 6), (12, 6)], fill=p["light"])
    # Caja de conexiones
    d.rectangle([5, 3, 9, 6], fill=p["dark"], outline=OUTLINE)
    d.line([(6, 4), (8, 4)], fill=YELLOW)
    # Polea
    d.ellipse([12, 5, 15, 12], fill=OUTLINE)
    d.ellipse([13, 6, 14, 11], fill=(170, 176, 184))
    d.ellipse([13, 8, 14, 9], fill=p["dark"])
    d.rectangle([3, 11, 11, 12], fill=p["dark"], outline=OUTLINE)
    d.line([(2, 8), (1, 9)], fill=COPPER["base"])
    rust_spots(d, [(4, 10), (9, 9)], p["rust"])
    return img


def estabilizador_voltaje():
    img, d = canvas()
    p = (180, 178, 166)
    bevel(d, 3, 3, 12, 13, p, (214, 212, 200), (130, 128, 118))
    # Dial
    d.ellipse([4, 5, 11, 11], fill=OUTLINE)
    d.ellipse([5, 6, 10, 10], fill=(220, 220, 210))
    for x, y in ((8, 5), (5, 8), (11, 8), (6, 6), (10, 6), (6, 10), (10, 10)):
        px(d, x, y, (120, 120, 110))
    d.line([(8, 8), (8, 6)], fill=RED)
    px(d, 8, 8, OUTLINE)
    # Rejilla
    for x in (4, 6, 8, 10):
        px(d, x, 12, OUTLINE)
    d.rectangle([4, 12, 5, 13], fill=RED, outline=OUTLINE)
    return img


def bateria_ups_servidor():
    img, d = canvas()
    p = (60, 62, 66)
    bevel(d, 1, 4, 14, 12, p, (92, 94, 98), (36, 38, 42))
    # Terminales
    d.rectangle([3, 2, 4, 4], fill=LEAD_LIGHT, outline=OUTLINE)
    d.rectangle([11, 2, 12, 4], fill=LEAD_LIGHT, outline=OUTLINE)
    d.arc([6, 1, 9, 4], 180, 360, fill=OUTLINE)
    # Etiqueta
    d.rectangle([4, 6, 11, 9], fill=(180, 180, 170), outline=OUTLINE)
    d.line([(5, 7), (10, 7)], fill=(80, 80, 80))
    d.line([(5, 8), (8, 8)], fill=(80, 80, 80))
    px(d, 3, 10, (80, 200, 80))
    px(d, 12, 10, RED)
    d.line([(14, 9), (15, 11)], fill=OUTLINE)
    return img


def caja_disyuntores_trifasicos():
    img, d = canvas()
    p = (120, 124, 128)
    d.rectangle([1, 2, 14, 14], fill=p, outline=OUTLINE)
    d.rectangle([2, 3, 13, 13], fill=(82, 86, 90), outline=OUTLINE)
    # Riel DIN
    d.rectangle([3, 4, 12, 5], fill=(150, 154, 158), outline=OUTLINE)
    # Breakers
    for x in (4, 7, 10):
        d.rectangle([x, 5, x + 2, 10], fill=(30, 32, 36), outline=OUTLINE)
        d.rectangle([x, 5, x + 2, 6], fill=(200, 200, 190))
        d.line([(x + 1, 7), (x + 1, 9)], fill=(80, 84, 88))
    # Cableado
    d.line([(4, 10), (4, 12)], fill=RED)
    d.line([(7, 10), (7, 12)], fill=YELLOW)
    d.line([(10, 10), (10, 12)], fill=(80, 140, 200))
    d.line([(4, 12), (10, 12)], fill=(60, 64, 68))
    # Peligro
    d.polygon([(2, 11), (4, 11), (3, 9)], fill=YELLOW, outline=OUTLINE)
    px(d, 3, 10, BLACK)
    # Etiqueta
    d.line([(3, 7), (3, 9)], fill=(180, 180, 170))
    return img


def cable_telefonico():
    img, d = canvas()
    # Carrete
    d.rectangle([2, 3, 4, 13], fill=WOOD["dark"], outline=OUTLINE)
    d.rectangle([11, 3, 13, 13], fill=WOOD["dark"], outline=OUTLINE)
    d.rectangle([4, 4, 11, 12], fill=(60, 62, 66), outline=OUTLINE)
    colors = [(80, 120, 200), (180, 70, 60), (80, 160, 90), (200, 160, 60)]
    for i, y in enumerate((5, 7, 9, 11)):
        d.line([(4, y), (11, y)], fill=colors[i % 4])
        d.line([(5, y - 1), (10, y - 1)],
               fill=tuple(min(255, c + 40) for c in colors[i % 4]))
    # Cable suelto con pares
    d.line([(13, 9), (15, 10)], fill=(60, 62, 66))
    for i, (x, y) in enumerate(((14, 10), (15, 10), (14, 11), (15, 11))):
        px(d, x, y, colors[i % 4])
    return img


def aislador_ceramico():
    img, d = canvas()
    # Pasador
    d.rectangle([7, 1, 8, 14], fill=(100, 106, 112), outline=OUTLINE)
    # Discos ceramicos
    for y, w in ((2, 9), (5, 11), (8, 11), (11, 9)):
        d.ellipse([8 - w // 2, y, 8 + w // 2, y + 3],
                  fill=(200, 196, 184), outline=OUTLINE)
        d.line([(9 - w // 2, y + 1), (7 + w // 2, y + 1)], fill=(240, 238, 228))
        d.line([(9 - w // 2, y + 2), (7 + w // 2, y + 2)], fill=(160, 156, 144))
    # Soporte
    d.rectangle([4, 13, 11, 14], fill=(90, 96, 100), outline=OUTLINE)
    # Grieta
    d.line([(6, 6), (7, 8)], fill=OUTLINE)
    return img


def fusible_porcelana():
    img, d = canvas()
    d.rectangle([5, 4, 10, 12], fill=(210, 206, 194), outline=OUTLINE)
    d.ellipse([5, 3, 10, 5], fill=(230, 226, 214), outline=OUTLINE)
    d.ellipse([5, 11, 10, 13], fill=(180, 176, 164), outline=OUTLINE)
    # Casquillos
    d.rectangle([4, 4, 5, 12], fill=(150, 156, 162), outline=OUTLINE)
    d.rectangle([10, 4, 11, 12], fill=(150, 156, 162), outline=OUTLINE)
    # Ventana fundida
    d.rectangle([7, 7, 8, 9], fill=(40, 36, 32), outline=OUTLINE)
    px(d, 7, 7, (80, 70, 60))
    d.line([(6, 6), (9, 6)], fill=(120, 116, 104))
    return img


def carcasa_enchufe():
    img, d = canvas()
    p = (210, 208, 196)
    d.rectangle([2, 5, 13, 11], fill=p, outline=OUTLINE)
    d.ellipse([2, 5, 4, 11], fill=p, outline=OUTLINE)
    d.ellipse([11, 5, 13, 11], fill=p, outline=OUTLINE)
    for x in (4, 7, 10):
        d.ellipse([x, 7, x + 1, 8], fill=OUTLINE)
        d.ellipse([x, 8, x + 1, 9], fill=OUTLINE)
    d.rectangle([12, 6, 13, 7], fill=(150, 150, 140), outline=OUTLINE)
    d.line([(13, 10), (15, 12)], fill=(80, 80, 80))
    px(d, 3, 9, (120, 120, 110))
    return img


def tubo_fluorescente():
    img, d = canvas()
    # Tubo
    d.rectangle([1, 5, 14, 8], fill=(180, 220, 220), outline=OUTLINE)
    d.line([(2, 6), (13, 6)], fill=(230, 250, 250))
    d.rectangle([1, 5, 2, 8], fill=(150, 156, 162), outline=OUTLINE)
    d.rectangle([13, 5, 14, 8], fill=(150, 156, 162), outline=OUTLINE)
    # Extremo roto
    d.polygon([(10, 5), (12, 5), (11, 8), (9, 8)], fill=(0, 0, 0, 0), outline=OUTLINE)
    # Balasto
    d.rectangle([3, 9, 11, 12], fill=(90, 96, 100), outline=OUTLINE)
    d.line([(4, 10), (10, 10)], fill=(60, 66, 70))
    d.line([(4, 11), (7, 11)], fill=RED)
    d.line([(2, 8), (3, 9)], fill=OUTLINE)
    d.line([(12, 8), (11, 9)], fill=OUTLINE)
    return img


def placa_disipadora_aluminio():
    img, d = canvas()
    p = (180, 186, 192)
    light = (220, 226, 232)
    dark = (120, 126, 132)
    d.rectangle([2, 6, 13, 12], fill=p, outline=OUTLINE)
    d.line([(3, 7), (12, 7)], fill=light)
    for x in (3, 5, 7, 9, 11):
        d.rectangle([x, 3, x + 1, 9], fill=p, outline=OUTLINE)
        d.line([(x, 4), (x, 8)], fill=light)
    px(d, 3, 11, OUTLINE)
    px(d, 12, 11, OUTLINE)
    d.line([(2, 10), (5, 9)], fill=dark)
    return img


INDUSTRIAL_DESIGNS = {
    "motor_grua_sovietica": motor_grua_sovietica,
    "taladro_percutor_mina": taladro_percutor_mina,
    "compresor_aire_fabrica": compresor_aire_fabrica,
    "bomba_hidraulica_refrigeracion": bomba_hidraulica_refrigeracion,
    "soldadora_arco_portatil": soldadora_arco_portatil,
    "caja_engranajes_tractor": caja_engranajes_tractor,
    "viga_acero_retorcida": viga_acero_retorcida,
    "contrapeso_grua": contrapeso_grua,
    "cadena_remolque": cadena_remolque,
    "lamina_techo_corrugada": lamina_techo_corrugada,
    "caja_clavos_tuercas": caja_clavos_tuercas,
    "guantes_soldador": guantes_soldador,
    "casco_minero": casco_minero,
}

CHEMICAL_DESIGNS = {
    "traje_hazmat_liquidador": traje_hazmat_liquidador,
    "contador_geiger_pripyat": contador_geiger_pripyat,
    "respirador_papr": respirador_papr,
    "centrifugadora_muestras": centrifugadora_muestras,
    "contenedor_isotopos": contenedor_isotopos,
    "rociador_descontaminacion": rociador_descontaminacion,
    "ladrillo_blindaje_plomo": ladrillo_blindaje_plomo,
    "delantal_laboratorio": delantal_laboratorio,
    "bidon_acido": bidon_acido,
    "botas_goma_descontaminantes": botas_goma_descontaminantes,
    "lona_cuarentena": lona_cuarentena,
    "mascarilla_gp5": mascarilla_gp5,
    "gradilla_tubos_ensayo": gradilla_tubos_ensayo,
}

MILITARY_DESIGNS = {
    "bateria_tanque_t72": bateria_tanque_t72,
    "visor_nocturno_pnv57": visor_nocturno_pnv57,
    "chaleco_balistico_6b3": chaleco_balistico_6b3,
    "radio_campana_r159": radio_campana_r159,
    "modulo_punteria_btr": modulo_punteria_btr,
    "dron_reconocimiento": dron_reconocimiento,
    "placa_balistica_acero": placa_balistica_acero,
    "eslabon_oruga_tanque": eslabon_oruga_tanque,
    "caja_municion_50": caja_municion_50,
    "casco_ssh68": casco_ssh68,
    "cargador_baquelita_ak74": cargador_baquelita_ak74,
    "red_camuflaje": red_camuflaje,
    "botas_paracaidista": botas_paracaidista,
}

HOSPITAL_DESIGNS = {
    "desfibrilador_portatil": desfibrilador_portatil,
    "microscopio_quirurgico": microscopio_quirurgico,
    "ventilador_pulmonar_uci": ventilador_pulmonar_uci,
    "monitor_signos_vitales": monitor_signos_vitales,
    "autoclave_esterilizacion": autoclave_esterilizacion,
    "camilla_aislamiento": camilla_aislamiento,
    "rollo_vendas_yodo": rollo_vendas_yodo,
    "sabana_quirurgica": sabana_quirurgica,
    "bata_paciente": bata_paciente,
    "bandeja_instrumentos": bandeja_instrumentos,
    "soporte_suero": soporte_suero,
    "bolsa_desechos_biologicos": bolsa_desechos_biologicos,
    "muleta_aluminio": muleta_aluminio,
}

RESIDENTIAL_DESIGNS = {
    "abrigo_afghanka": abrigo_afghanka,
    "microondas_dnepr": microondas_dnepr,
    "televisor_rubin": televisor_rubin,
    "lavadora_vyatka": lavadora_vyatka,
    "maquina_coser_podolsk": maquina_coser_podolsk,
    "aspiradora_raketa": aspiradora_raketa,
    "taza_peltre": taza_peltre,
    "olla_presion": olla_presion,
    "radiador_hierro": radiador_hierro,
    "gorro_ushanka": gorro_ushanka,
    "vaqueros_rasgados": vaqueros_rasgados,
    "alfombra_persa": alfombra_persa,
    "muneca_irradiada": muneca_irradiada,
    "cubiertos_acero": cubiertos_acero,
}

ELECTRICAL_DESIGNS = {
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

LABELS = {
    "motor_grua_sovietica": "Motor grúa",
    "taladro_percutor_mina": "Taladro",
    "compresor_aire_fabrica": "Compresor",
    "bomba_hidraulica_refrigeracion": "Bomba",
    "soldadora_arco_portatil": "Soldadora",
    "caja_engranajes_tractor": "Caja cambios",
    "viga_acero_retorcida": "Viga",
    "contrapeso_grua": "Contrapeso",
    "cadena_remolque": "Cadena",
    "lamina_techo_corrugada": "Chapa",
    "caja_clavos_tuercas": "Tornillería",
    "guantes_soldador": "Guantes",
    "casco_minero": "Casco",
    "traje_hazmat_liquidador": "Traje hazmat",
    "contador_geiger_pripyat": "Geiger",
    "respirador_papr": "PAPR",
    "centrifugadora_muestras": "Centrífuga",
    "contenedor_isotopos": "Isótopos",
    "rociador_descontaminacion": "Rociador",
    "ladrillo_blindaje_plomo": "Ladrillo Pb",
    "delantal_laboratorio": "Delantal",
    "bidon_acido": "Bidón ácido",
    "botas_goma_descontaminantes": "Botas goma",
    "lona_cuarentena": "Lona",
    "mascarilla_gp5": "GP-5",
    "gradilla_tubos_ensayo": "Tubos",
    "bateria_tanque_t72": "Batería T-72",
    "visor_nocturno_pnv57": "PNV-57",
    "chaleco_balistico_6b3": "Chaleco 6B3",
    "radio_campana_r159": "Radio R-159",
    "modulo_punteria_btr": "Mira BTR",
    "dron_reconocimiento": "Dron",
    "placa_balistica_acero": "Placa balística",
    "eslabon_oruga_tanque": "Eslabón oruga",
    "caja_municion_50": "Munición .50",
    "casco_ssh68": "SSh-68",
    "cargador_baquelita_ak74": "Cargador AK",
    "red_camuflaje": "Red camuflaje",
    "botas_paracaidista": "Botas tácticas",
    "desfibrilador_portatil": "Desfibrilador",
    "microscopio_quirurgico": "Microscopio",
    "ventilador_pulmonar_uci": "Ventilador",
    "monitor_signos_vitales": "Monitor",
    "autoclave_esterilizacion": "Autoclave",
    "camilla_aislamiento": "Camilla",
    "rollo_vendas_yodo": "Vendas yodo",
    "sabana_quirurgica": "Sábana",
    "bata_paciente": "Bata",
    "bandeja_instrumentos": "Bandeja",
    "soporte_suero": "Suero",
    "bolsa_desechos_biologicos": "Bolsa bio",
    "muleta_aluminio": "Muleta",
    "abrigo_afghanka": "Abrigo",
    "microondas_dnepr": "Microondas",
    "televisor_rubin": "Televisor",
    "lavadora_vyatka": "Lavadora",
    "maquina_coser_podolsk": "M. coser",
    "aspiradora_raketa": "Aspiradora",
    "taza_peltre": "Taza",
    "olla_presion": "Olla",
    "radiador_hierro": "Radiador",
    "gorro_ushanka": "Ushanka",
    "vaqueros_rasgados": "Vaqueros",
    "alfombra_persa": "Alfombra",
    "muneca_irradiada": "Muñeca",
    "cubiertos_acero": "Cubiertos",
    "transformador_subestacion": "Transformador",
    "panel_control_reactor": "Panel reactor",
    "alternador_generador_diesel": "Alternador",
    "estabilizador_voltaje": "Estabilizador",
    "bateria_ups_servidor": "UPS",
    "caja_disyuntores_trifasicos": "Disyuntores",
    "cable_telefonico": "Cable tel.",
    "aislador_ceramico": "Aislador",
    "fusible_porcelana": "Fusible",
    "carcasa_enchufe": "Enchufe",
    "tubo_fluorescente": "Fluorescente",
    "placa_disipadora_aluminio": "Disipador",
}

ZONE_TITLES = {
    "industrial": "Zona industrial",
    "chemical": "Zona química",
    "military": "Zona militar",
    "hospital": "Zona hospital",
    "residential": "Zona residencial",
    "electrical": "Componentes eléctricos",
}

ZONE_DESIGNS = {
    "industrial": INDUSTRIAL_DESIGNS,
    "chemical": CHEMICAL_DESIGNS,
    "military": MILITARY_DESIGNS,
    "hospital": HOSPITAL_DESIGNS,
    "residential": RESIDENTIAL_DESIGNS,
    "electrical": ELECTRICAL_DESIGNS,
}

DESIGNS = {
    item_id: render
    for designs in ZONE_DESIGNS.values()
    for item_id, render in designs.items()
}


def font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def build_sheet(images, title):
    cols = 5
    cell = 16 * SCALE
    gap = 12
    label_h = 20
    rows = (len(images) + cols - 1) // cols
    width = cols * (cell + gap) + gap
    height = 38 + rows * (cell + label_h + gap) + gap
    sheet = Image.new("RGBA", (width, height), (32, 34, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((width // 2, 10), f"{title} - estilo D", font=font(18),
           fill=(228, 228, 222), anchor="ma")
    small = font(12)
    for index, (item_id, img) in enumerate(images.items()):
        row, col = divmod(index, cols)
        x = gap + col * (cell + gap)
        y = 38 + row * (cell + label_h + gap)
        sheet.alpha_composite(img.resize((cell, cell), Image.NEAREST), (x, y))
        d.rectangle([x - 1, y - 1, x + cell, y + cell], outline=(70, 72, 76))
        d.text((x + cell // 2, y + cell + 3), LABELS.get(item_id, item_id),
               font=small, fill=(200, 200, 194), anchor="ma")
    return sheet


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    total = 0
    install = "--install" in sys.argv

    for zone, designs in ZONE_DESIGNS.items():
        images = {}
        for item_id, render in designs.items():
            img = render()
            images[item_id] = img
            img.save(REVIEW / f"{item_id}.png")
            if install:
                img.save(ASSETS / f"{item_id}.png")
        build_sheet(images, ZONE_TITLES.get(zone, zone)).save(REVIEW / f"{zone}.png")
        total += len(images)
        print(f"Revision {zone}: {REVIEW / (zone + '.png')} ({len(images)} texturas)")

    if install:
        print(f"Instaladas {total} texturas de objetos en {ASSETS}")


if __name__ == "__main__":
    main()
