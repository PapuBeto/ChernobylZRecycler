"""Prueba de estilos para las texturas base (16x16).

Genera docs/style_test/styles.png con 3 estilos x 3 items para elegir
la direccion artistica antes de producir los 97 iconos.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("docs/style_test")
SCALE = 8

PALETTES = {
    "A": {
        "name": "A - Vanilla limpio",
        "cloth": {"base": (214, 203, 176), "light": (238, 229, 206), "dark": (168, 156, 128), "outline": (58, 50, 38)},
        "metal": {"base": (158, 164, 172), "light": (200, 206, 214), "dark": (100, 106, 114), "outline": (32, 35, 40), "rust": (156, 92, 50)},
        "ingot": {"base": (112, 120, 132), "light": (152, 160, 172), "dark": (72, 78, 88), "outline": (24, 26, 30), "rust": (150, 88, 48)},
    },
    "B": {
        "name": "B - Rust gastado",
        "cloth": {"base": (166, 154, 126), "light": (192, 180, 152), "dark": (116, 106, 84), "outline": (40, 36, 28), "stain": (108, 92, 66)},
        "metal": {"base": (116, 118, 114), "light": (148, 150, 144), "dark": (76, 78, 74), "outline": (26, 26, 24), "rust": (136, 76, 38)},
        "ingot": {"base": (88, 90, 88), "light": (120, 122, 118), "dark": (56, 58, 56), "outline": (20, 20, 18), "rust": (132, 72, 36)},
    },
    "C": {
        "name": "C - Detallado",
        "cloth": {"base": (224, 214, 190), "light": (248, 241, 222), "mid": (198, 186, 158), "dark": (148, 136, 110), "outline": (50, 42, 32)},
        "metal": {"base": (150, 158, 168), "light": (212, 220, 230), "mid": (118, 126, 138), "dark": (72, 78, 88), "outline": (22, 24, 28), "rust": (162, 96, 52)},
        "ingot": {"base": (110, 118, 130), "light": (196, 204, 216), "mid": (140, 148, 160), "dark": (66, 72, 82), "outline": (18, 20, 24), "rust": (168, 98, 50)},
    },
    "D": {
        "name": "D - Hibrido limpio + desgaste",
        "cloth": {"base": (186, 174, 146), "light": (214, 203, 176), "dark": (138, 126, 100), "outline": (48, 42, 32), "stain": (112, 96, 70)},
        "metal": {"base": (138, 142, 146), "light": (180, 186, 192), "dark": (88, 92, 98), "outline": (30, 32, 36), "rust": (146, 84, 42)},
        "ingot": {"base": (98, 104, 112), "light": (150, 158, 168), "dark": (62, 66, 74), "outline": (22, 24, 28), "rust": (152, 88, 44)},
    },
}


def canvas():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color[:3])


def px(d, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        d.point((x, y), fill=color)


# ---------------------------------------------------------------------------
# Tela
# ---------------------------------------------------------------------------

def cloth(style):
    img, d = canvas()
    pal = PALETTES[style]["cloth"]

    if style in ("A", "D"):
        # Pila de dos telas dobladas, contorno limpio
        d.polygon([(3, 5), (12, 5), (13, 6), (13, 9), (3, 9), (2, 8), (2, 6)],
                  fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 9), (13, 9), (14, 10), (14, 12), (13, 13), (2, 13), (1, 12), (1, 10)],
                  fill=pal["base"], outline=pal["outline"])
        d.line([(3, 9), (12, 9)], fill=pal["dark"])
        # Pliegues y puntadas
        d.line([(4, 7), (10, 7)], fill=pal["dark"])
        d.line([(4, 11), (12, 11)], fill=pal["dark"])
        for x in (5, 7, 9, 11):
            px(d, x, 6, pal["dark"])
            px(d, x, 12, pal["dark"])
        # Dobladillo claro
        d.line([(3, 5), (11, 5)], fill=(255, 255, 255))

    elif style == "B":
        # Tela sucia, borde deshilachado y remiendo
        d.polygon([(2, 5), (12, 4), (13, 6), (13, 9), (3, 9), (1, 7)],
                  fill=pal["light"], outline=pal["outline"])
        d.polygon([(1, 9), (13, 8), (14, 10), (13, 12), (11, 13), (9, 12), (7, 13),
                   (5, 12), (3, 13), (1, 12)],
                  fill=pal["base"], outline=pal["outline"])
        d.line([(2, 9), (12, 8)], fill=pal["dark"])
        # Remiendo
        d.rectangle([8, 9, 12, 11], fill=pal["stain"], outline=pal["dark"])
        for x in (9, 11):
            px(d, x, 10, pal["light"])
        # Manchas
        px(d, 3, 6, pal["stain"])
        px(d, 5, 11, pal["stain"])
        px(d, 6, 10, pal["stain"])
        d.line([(4, 6), (7, 6)], fill=pal["stain"])

    else:
        # Pila con tejido visible y sombra interior
        d.polygon([(3, 4), (12, 4), (13, 5), (13, 8), (3, 8), (2, 7), (2, 5)],
                  fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 8), (13, 8), (14, 9), (14, 12), (13, 13), (2, 13), (1, 12), (1, 9)],
                  fill=pal["base"], outline=pal["outline"])
        # Trama
        for x in range(3, 13, 2):
            d.line([(x, 9), (x, 12)], fill=pal["mid"])
        for y in (10, 12):
            d.line([(2, y), (13, y)], fill=pal["mid"])
        d.line([(3, 8), (12, 8)], fill=pal["dark"])
        # Brillo del doblez
        d.line([(3, 5), (11, 5)], fill=(255, 255, 255))
        d.line([(3, 6), (4, 6)], fill=pal["dark"])
        # Costura
        for x in (5, 8, 11):
            px(d, x, 7, pal["dark"])

    return img


# ---------------------------------------------------------------------------
# Scrap
# ---------------------------------------------------------------------------

def scrap(style):
    img, d = canvas()
    pal = PALETTES[style]["metal"]

    if style in ("A", "D"):
        # Tres placas apiladas con pernos
        d.polygon([(3, 8), (8, 6), (13, 8), (12, 12), (5, 13), (2, 11)],
                  fill=pal["base"], outline=pal["outline"])
        d.polygon([(4, 4), (10, 3), (13, 6), (9, 9), (4, 8)],
                  fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 11), (6, 9), (11, 10), (9, 13)],
                  fill=pal["dark"], outline=pal["outline"])
        d.line([(4, 5), (9, 4)], fill=(255, 255, 255))
        for x, y in ((6, 11), (9, 11), (7, 6), (11, 7)):
            px(d, x, y, pal["outline"])
            px(d, x, y - 1, pal["light"])

    elif style == "B":
        # Chapa doblada + trozo de tubo oxidado
        d.polygon([(1, 8), (9, 6), (13, 9), (11, 13), (4, 13), (1, 11)],
                  fill=pal["base"], outline=pal["outline"])
        d.polygon([(9, 3), (13, 4), (14, 7), (11, 9), (8, 7)],
                  fill=pal["light"], outline=pal["outline"])
        d.line([(2, 9), (8, 8)], fill=pal["dark"])
        d.line([(3, 11), (9, 10)], fill=pal["dark"])
        # Oxido
        for x, y in ((3, 12), (6, 11), (10, 10), (11, 6), (12, 5)):
            px(d, x, y, pal["rust"])
        px(d, 4, 10, shade(pal["rust"], 0.8))
        # Perno
        px(d, 6, 9, pal["outline"])
        px(d, 6, 8, pal["light"])
        # Borde roto
        px(d, 13, 10, pal["outline"])
        px(d, 12, 11, pal["outline"])

    else:
        # Monton de chatarra con cuatro piezas y remaches
        d.polygon([(2, 9), (7, 7), (13, 9), (12, 13), (4, 13)],
                  fill=pal["base"], outline=pal["outline"])
        d.polygon([(3, 5), (9, 3), (12, 5), (9, 8), (4, 8)],
                  fill=pal["mid"], outline=pal["outline"])
        d.polygon([(10, 4), (13, 5), (14, 8), (11, 9), (9, 7)],
                  fill=pal["light"], outline=pal["outline"])
        d.line([(3, 10), (8, 9)], fill=pal["dark"])
        d.line([(5, 12), (11, 11)], fill=pal["dark"])
        d.line([(4, 6), (8, 5)], fill=(255, 255, 255))
        for x, y in ((5, 11), (9, 11), (6, 6), (12, 7)):
            px(d, x, y, pal["outline"])
            px(d, x, y - 1, pal["light"])
        for x, y in ((7, 12), (10, 8), (12, 12)):
            px(d, x, y, pal["rust"])

    return img


# ---------------------------------------------------------------------------
# Lingote pesado
# ---------------------------------------------------------------------------

def ingot(style):
    img, d = canvas()
    pal = PALETTES[style]["ingot"]

    if style in ("A", "D"):
        # Lingote clasico en perspectiva
        d.polygon([(4, 4), (12, 4), (14, 7), (2, 7)], fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 7), (14, 7), (13, 12), (3, 12)], fill=pal["base"], outline=pal["outline"])
        d.line([(3, 11), (13, 11)], fill=pal["dark"])
        d.line([(4, 5), (12, 5)], fill=(255, 255, 255))
        d.line([(4, 8), (12, 8)], fill=pal["dark"])
        # Marca
        px(d, 7, 9, pal["dark"])
        px(d, 8, 9, pal["dark"])
        px(d, 8, 10, pal["dark"])

    elif style == "B":
        # Lingote picado y oxidado
        d.polygon([(3, 4), (12, 3), (14, 6), (2, 7)], fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 7), (14, 6), (13, 12), (4, 13), (2, 11)],
                  fill=pal["base"], outline=pal["outline"])
        d.line([(4, 11), (12, 10)], fill=pal["dark"])
        # Oxido y golpes
        for x, y in ((4, 8), (6, 9), (9, 8), (11, 10), (5, 5), (10, 5)):
            px(d, x, y, pal["rust"])
        px(d, 8, 11, pal["rust"])
        px(d, 3, 9, pal["dark"])
        px(d, 12, 8, pal["dark"])
        d.line([(5, 4), (10, 3)], fill=(210, 210, 205))

    else:
        # Lingote con tres tonos, brillo y marca estampada
        d.polygon([(4, 3), (12, 3), (14, 6), (2, 6)], fill=pal["light"], outline=pal["outline"])
        d.polygon([(2, 6), (14, 6), (13, 11), (3, 11)], fill=pal["mid"], outline=pal["outline"])
        d.polygon([(3, 11), (13, 11), (12, 13), (4, 13)], fill=pal["base"], outline=pal["outline"])
        d.line([(4, 4), (11, 4)], fill=(255, 255, 255))
        d.line([(3, 7), (13, 7)], fill=pal["dark"])
        d.line([(3, 12), (12, 12)], fill=pal["dark"])
        # Reflejo
        px(d, 5, 8, (255, 255, 255))
        px(d, 6, 8, pal["light"])
        # Marca estampada
        d.rectangle([7, 8, 10, 10], outline=pal["dark"])
        px(d, 8, 9, pal["dark"])
        px(d, 9, 9, pal["dark"])

    return img


# ---------------------------------------------------------------------------
# Hoja comparativa
# ---------------------------------------------------------------------------

WEAR = {
    "tela": [(3, 6), (5, 11), (9, 6), (11, 11), (7, 10)],
    "scrap": [(3, 9), (6, 11), (10, 10), (12, 6), (5, 5)],
    "lingote_pesado": [(4, 8), (7, 9), (10, 8), (5, 5), (11, 10)],
}


def add_wear(img, item_id):
    """Aplica manchas de oxido/suciedad sobre la geometria limpia del estilo A."""
    if item_id == "tela":
        color = PALETTES["D"]["cloth"]["stain"]
    elif item_id == "scrap":
        color = PALETTES["D"]["metal"]["rust"]
    else:
        color = PALETTES["D"]["ingot"]["rust"]

    d = ImageDraw.Draw(img)
    for x, y in WEAR[item_id]:
        if img.getpixel((x, y))[3] > 0:
            px(d, x, y, color)
    # Un par de golpes oscuros
    for x, y in WEAR[item_id][:2]:
        if img.getpixel((x + 1, y))[3] > 0:
            px(d, x + 1, y, shade(color, 0.65))
    return img


def label_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def build_sheet(images):
    cell = 16 * SCALE
    gap = 14
    label_w = 150
    header_h = 34
    styles = ["A", "B", "C", "D"]
    items = [("tela", "Tela"), ("scrap", "Scrap"), ("lingote_pesado", "Lingote Pesado")]

    width = label_w + len(items) * (cell + gap) + gap
    height = header_h + len(styles) * (cell + gap) + gap
    sheet = Image.new("RGBA", (width, height), (32, 34, 36, 255))
    d = ImageDraw.Draw(sheet)
    font = label_font(16)
    small = label_font(13)

    for col, (_, title) in enumerate(items):
        x = label_w + col * (cell + gap) + cell // 2
        d.text((x, 10), title, font=font, fill=(225, 225, 220), anchor="ma")

    for row, style in enumerate(styles):
        y = header_h + row * (cell + gap)
        d.text((10, y + cell // 2), PALETTES[style]["name"], font=small,
               fill=(200, 200, 195), anchor="lm")
        for col, (item_id, _) in enumerate(items):
            x = label_w + col * (cell + gap)
            icon = images[style][item_id].resize((cell, cell), Image.NEAREST)
            sheet.alpha_composite(icon, (x, y))
            d.rectangle([x - 1, y - 1, x + cell, y + cell], outline=(70, 72, 76))

    return sheet


def main():
    images = {}
    for style in ("A", "B", "C", "D"):
        images[style] = {
            "tela": cloth(style),
            "scrap": scrap(style),
            "lingote_pesado": ingot(style),
        }
        for item_id, img in images[style].items():
            if style == "D":
                add_wear(img, item_id)
            path = OUT / style / f"{item_id}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            img.save(path)

    OUT.mkdir(parents=True, exist_ok=True)
    build_sheet(images).save(OUT / "styles.png")
    print(f"OK: {OUT / 'styles.png'}")


if __name__ == "__main__":
    main()
