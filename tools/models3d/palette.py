"""Fase 0 — paleta del sistema de diseño 3D de ChernobylZ.

Fuente única de verdad para las specs de modelos y el renderizador de
previews. Los valores reproducen la paleta de las texturas 2D
(tools/textures.py, tools/objects.py) para que el arte 2D y el 3D
describan el mismo mundo: equipo soviético de los años 70-90, funcional,
con desgaste moderado y cero ornamentación gratuita.

Convención de cita de color en las specs:
- material con variante: "material.variante" (p. ej. "acero.oscuro");
- sin variante se entiende "base" ("acero" == "acero.base");
- desgaste: cita directa ("oxido", "hollin", "patina_rad", ...).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Materiales
# ---------------------------------------------------------------------------

MATERIALES = {
    # Metales
    "acero":        {"base": (138, 142, 146), "claro": (182, 188, 194), "oscuro": (88, 92, 98)},
    "hierro":       {"base": (96, 100, 104),  "claro": (142, 148, 154), "oscuro": (58, 62, 66)},
    "metal_oscuro": {"base": (82, 86, 88),    "claro": (120, 126, 128), "oscuro": (50, 54, 56)},
    "aluminio":     {"base": (168, 174, 180), "claro": (208, 214, 220), "oscuro": (116, 122, 128)},
    "plomo":        {"base": (106, 112, 120), "claro": (150, 156, 164), "oscuro": (70, 74, 82)},
    "cobre":        {"base": (184, 112, 64),  "claro": (224, 156, 98),  "oscuro": (118, 64, 34)},
    "laton":        {"base": (188, 158, 82),  "claro": (226, 200, 122), "oscuro": (126, 102, 48)},
    # Cerámicos, vidrio y pantallas
    "vidrio":        {"base": (84, 152, 192),  "claro": (172, 222, 246), "oscuro": (44, 96, 132)},
    "vidrio_oscuro": {"base": (40, 48, 52),    "claro": (64, 76, 82),    "oscuro": (24, 30, 32)},
    "porcelana":     {"base": (222, 220, 212), "claro": (240, 238, 228), "oscuro": (168, 162, 150)},
    "pantalla":      {"base": (64, 84, 52),    "claro": (120, 158, 84),  "oscuro": (34, 46, 28)},
    # Lacas y plásticos soviéticos
    "verde_oliva":          {"base": (98, 112, 74),   "claro": (136, 152, 102), "oscuro": (64, 76, 48)},
    "verde_militar":        {"base": (70, 116, 68),   "claro": (108, 154, 98),  "oscuro": (40, 74, 44)},
    "baquelita":            {"base": (110, 84, 58),   "claro": (150, 116, 80),  "oscuro": (72, 52, 32)},
    "baquelita_negra":      {"base": (52, 50, 48),    "claro": (80, 78, 72),    "oscuro": (30, 28, 26)},
    "plastico_amarillento": {"base": (204, 196, 156), "claro": (230, 224, 190), "oscuro": (148, 140, 104)},
    "beige_aparato":        {"base": (190, 184, 166), "claro": (224, 218, 200), "oscuro": (136, 130, 114)},
    "goma":                 {"base": (78, 82, 78),    "claro": (112, 116, 110), "oscuro": (48, 50, 48)},
    # Acentos de peligro y química
    "amarillo_peligro": {"base": (204, 172, 70), "claro": (226, 200, 106), "oscuro": (142, 116, 40)},
    "rojo_desgastado":  {"base": (150, 70, 60),  "claro": (190, 100, 86),  "oscuro": (100, 44, 38)},
    "verde_acido":      {"base": (128, 186, 76), "claro": (178, 226, 118), "oscuro": (74, 124, 42)},
    # Hospital
    "blanco_lab":      {"base": (198, 204, 204), "claro": (230, 236, 236), "oscuro": (142, 148, 148)},
    "azul_quirurgico": {"base": (88, 132, 148),  "claro": (124, 172, 188), "oscuro": (54, 88, 102)},
    "hazmat":          {"base": (176, 180, 92),  "claro": (210, 214, 124), "oscuro": (116, 120, 56)},
    # Textiles y materias blandas
    "caqui":      {"base": (140, 132, 96),  "claro": (176, 168, 126), "oscuro": (96, 90, 62)},
    "kevlar":     {"base": (128, 136, 110), "claro": (166, 174, 142), "oscuro": (92, 98, 74)},
    "tela_crema": {"base": (190, 178, 150), "claro": (220, 208, 182), "oscuro": (140, 128, 102)},
    "pelaje":     {"base": (110, 92, 72),   "claro": (150, 128, 102), "oscuro": (74, 60, 46)},
    "madera":     {"base": (122, 88, 56),   "claro": (160, 120, 78),  "oscuro": (80, 56, 34)},
}

# Colores de desgaste (citas directas, sin variante).
WEAR = {
    "oxido":        (148, 84, 42),   # óxido vivo en juntas y bordes de metal
    "oxido_oscuro": (104, 58, 28),   # óxido seco / quemado
    "mugre":        (94, 88, 74),    # grasa y polvo, tercio inferior y asas
    "hollin":       (36, 34, 32),    # humedades de fuego, chimeneas, motores
    "imprimacion":  (128, 122, 114), # pintura saltada, se ve el cebado
    "sulfato":      (176, 186, 192), # cristales blancos de baterías de plomo
    "sulfato_azul": (122, 152, 180), # eflorescencia azul de pilas alcalinas
    "goteo_acido":  (128, 186, 76),  # canales y gotas de corrosión ácida
    "patina_rad":   (150, 142, 86),  # pátina amarillo-oliva radiactiva, en juntas
    "moho":         (96, 110, 84),   # textiles y madera húmeda
    "yodo":         (150, 92, 54),   # manchas de iodinnie / antiséptico en hospital
    "quemado":      (74, 64, 56),    # plástico o madera chamuscada, sin hollín puro
}

CONTORNO = (28, 30, 34)  # límites internos de los renders y líneas de roturas

# ---------------------------------------------------------------------------
# Zonas y categorías
# ---------------------------------------------------------------------------

ZONAS = ("industrial", "chemical", "military", "hospital", "residential", "electrical")

ZONA_TIER = {
    "industrial": 2,
    "chemical": 3,
    "military": 3,
    "hospital": 2,
    "residential": 1,
    "electrical": 1,
}

ZONA_INFO = {
    "industrial": {
        "dominantes": ("acero", "hierro", "metal_oscuro", "aluminio"),
        "acento": "amarillo_peligro",
        "nota": "maquinaria pesada: franjas de peligro en bandas, óxido en juntas",
    },
    "chemical": {
        "dominantes": ("hazmat", "verde_oliva", "goma", "vidrio", "blanco_lab", "baquelita"),
        "acento": "verde_acido",
        "nota": "instrumentos y filtros: manchas ácidas y pátina radiactiva en juntas",
    },
    "military": {
        "dominantes": ("verde_oliva", "verde_militar", "caqui", "metal_oscuro", "baquelita"),
        "acento": "rojo_desgastado",
        "nota": "equipo de campaña: marcas de peligro pequeñas y piezas mayormente intactas",
    },
    "hospital": {
        "dominantes": ("blanco_lab", "azul_quirurgico", "acero", "aluminio"),
        "acento": "rojo_desgastado",
        "nota": "porcelana y plásticos limpios con señales de emergencia",
    },
    "residential": {
        "dominantes": ("tela_crema", "madera", "beige_aparato", "pelaje", "porcelana"),
        "acento": "rojo_desgastado",
        "nota": "objeto doméstico evacuado: mugre, hollín y moho",
    },
    "electrical": {
        "dominantes": ("cobre", "laton", "porcelana", "goma", "plastico_amarillento", "vidrio"),
        "acento": "amarillo_peligro",
        "nota": "herrajes con cableado saliente y hollín de chispa",
    },
}

CATEGORIAS = ("maquinaria", "electronica", "recipiente", "medico", "textil", "metal", "prop")

# ---------------------------------------------------------------------------
# Clases de tamaño y presupuesto por tier de valor
# ---------------------------------------------------------------------------

CLASES = {
    "pequena": {"altura": (6, 10),  "huella": 10, "gui": 0.90, "mundo": 0.60},
    "media":   {"altura": (10, 15), "huella": 16, "gui": 0.78, "mundo": 0.50},
    "grande":  {"altura": (14, 16), "huella": 16, "gui": 0.68, "mundo": 0.40},
}

TIER_RULES = {
    1: {"elementos_max": 24, "acentos_max": 2, "altura": (6, 12)},
    2: {"elementos_max": 48, "acentos_max": 4, "altura": (8, 15)},
    3: {"elementos_max": 64, "acentos_max": 5, "altura": (10, 16)},
}

# ---------------------------------------------------------------------------
# Displays estándar de Minecraft
# ---------------------------------------------------------------------------

def display_estandar(clase="media"):
    """Bloque `display` JSON de Minecraft escalado a la clase del modelo.

    En 1.20.1 los valores de `scale` son vec3:  se escribe [x, y, z].
    """
    clase = clase if clase in CLASES else "media"
    g = CLASES[clase]["gui"]
    w = CLASES[clase]["mundo"]
    return {
        "gui":                    {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [g, g, g]},
        "ground":                 {"rotation": [0, 0, 0],    "translation": [0, 0, 0], "scale": [w, w, w]},
        "fixed":                  {"rotation": [0, 0, 0],    "scale": [w, w, w]},
        "firstperson_righthand":  {"rotation": [0, 135, 0],  "translation": [0, 0, 0], "scale": [w, w, w]},
        "firstperson_lefthand":   {"rotation": [0, 225, 0],  "translation": [0, 0, 0], "scale": [w, w, w]},
        "thirdperson_righthand":  {"rotation": [0, 135, 0],  "translation": [0, 0, 0], "scale": [w, w, w]},
        "thirdperson_lefthand":   {"rotation": [0, 225, 0],  "translation": [0, 0, 0], "scale": [w, w, w]},
    }

# ---------------------------------------------------------------------------
# Citas de color
# ---------------------------------------------------------------------------

def color_ref(ref):
    """Valida una cita de color ("acero.oscuro", "oxido") y la normaliza."""
    if not isinstance(ref, str) or not ref:
        raise ValueError(f"cita de color inválida: {ref!r}")
    if ref in WEAR:
        return ref
    mat, _, var = ref.partition(".")
    if mat not in MATERIALES:
        raise ValueError(f"material '{mat}' no existe en la paleta")
    if var and var not in MATERIALES[mat]:
        raise ValueError(f"variante '{var}' no existe en '{mat}'")
    return f"{mat}.{var or 'base'}"


def resolver(ref):
    """Convierte una cita de color en RGB (magenta si la cita es errónea)."""
    try:
        color_ref(ref)
    except ValueError:
        return (255, 0, 255)
    if ref in WEAR:
        return WEAR[ref]
    mat, _, var = ref.partition(".")
    return MATERIALES[mat].get(var or "base", (255, 0, 255))
