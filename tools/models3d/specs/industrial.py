"""Specs de la zona industrial — tier 2.

Maquinaria pesada de la esclusa y las plantas: motores, prensas, carro.
Geometría maciza apoyada en el suelo, detalle mecánico explicado por
componentes reales (carcasa, aletas, eje, engranaje, bornes, tuberías),
desgaste concentrado en juntas y bases.
"""

SPECS = [
    {
        "id": "motor_grua_sovietica",
        "nombre": "Motor de Grúa Soviética Oxidado",
        "zona": "industrial",
        "tier": 2,
        "categoria": "maquinaria",
        "clase": "media",
        "silueta": "motor eléctrico de grúa en bancada: carcasa de acero con "
                   "aletas de refrigeración a flancos y arriba, tapa de "
                   "bancada de aluminio al Este con eje y collar, volante-"
                   "engranaje de latón con dientes al frente, caja de bornes "
                   "y tubo de escape oxidado con capuchón arriba, bota "
                   "hidráulica con vástago y copa al sur, caja de bornes de "
                   "cobre en el flanco oeste y placa de marca de latón",
        "permitir_flotantes": False,
        "notas": [
            "Historia visual: motor de grúa abandonado en la esclusa; óxido "
            "en el escape (acento 1), hollín bajo la boca (acento 2) y mugre "
            "delante de la zapata (acento 3).",
            "Cada pieza es un componente real: aletas de refrigeración (3 por "
            "flanco + 2 arriba), tapa de bancada, eje con collar, volante "
            "con 6 dientes y centro, caja de bornes, escape con capuchón, "
            "bota hidráulica con vástago y copa, caja de cobre con tornillos.",
            "El desgaste queda en 3 acentos de desgaste (tope t2: 4).",
        ],
        "piezas": [
            # --- bancada ---
            {"nombre": "zapata", "desde": [0, 0, 2], "hasta": [16, 2, 14],
             "material": "metal_oscuro.base"},
            {"nombre": "rem_base_fe", "desde": [1, 2, 3], "hasta": [2, 3, 4],
             "material": "aluminio.oscuro", "nota": "remache de bancada"},
            {"nombre": "rem_base_fd", "desde": [14, 2, 3], "hasta": [15, 3, 4],
             "material": "aluminio.oscuro"},
            {"nombre": "rem_base_be", "desde": [1, 2, 12], "hasta": [2, 3, 13],
             "material": "aluminio.oscuro"},
            {"nombre": "rem_base_bd", "desde": [14, 2, 12], "hasta": [15, 3, 13],
             "material": "aluminio.oscuro"},
            # --- pies y carcasa ---
            {"nombre": "pie_izq", "desde": [2, 1, 5], "hasta": [4, 3, 11],
             "material": "hierro.base"},
            {"nombre": "pie_der", "desde": [12, 1, 5], "hasta": [14, 3, 11],
             "material": "hierro.base"},
            {"nombre": "carcaza", "desde": [3, 3, 5], "hasta": [13, 10, 11],
             "material": "acero.oscuro"},
            # --- aletas de refrigeración ---
            {"nombre": "aleta_oeste_1", "desde": [2, 4, 6], "hasta": [4, 10, 7],
             "material": "acero.base"},
            {"nombre": "aleta_oeste_2", "desde": [2, 4, 8], "hasta": [4, 10, 9],
             "material": "acero.base"},
            {"nombre": "aleta_oeste_3", "desde": [2, 4, 10], "hasta": [4, 10, 11],
             "material": "acero.base"},
            {"nombre": "aleta_sup_1", "desde": [4, 9, 6], "hasta": [5, 11, 10],
             "material": "acero.base"},
            {"nombre": "aleta_sup_2", "desde": [6, 9, 6], "hasta": [7, 11, 10],
             "material": "acero.base"},
            # --- acople conjunto: tapa, eje, collar ---
            {"nombre": "tapa_delantera", "desde": [12, 3, 4], "hasta": [14, 10, 12],
             "material": "aluminio.oscuro",
             "nota": "tapa de bancada: 1 px enterrada en la carcaza, 1 saliente en Este"},
            {"nombre": "eje", "desde": [12, 6, 7], "hasta": [16, 8, 9],
             "material": "acero.claro", "nota": "punta de eje, enterrada en la tapa"},
            {"nombre": "collar", "desde": [14, 5, 6], "hasta": [15, 9, 10],
             "material": "hierro.oscuro", "nota": "bozal de acople sobre el eje"},
            # --- volante con dientes ---
            {"nombre": "volante", "desde": [3, 3, 10], "hasta": [8, 8, 13],
             "material": "laton.base", "caras": {"sur": "laton.claro"},
             "nota": "disco de engranaje: 1 px enterrado, 2 px al frente"},
            {"nombre": "diente_a1", "desde": [3, 7, 13], "hasta": [4, 8, 14],
             "material": "laton.oscuro"},
            {"nombre": "diente_a2", "desde": [5, 7, 13], "hasta": [6, 8, 14],
             "material": "laton.oscuro"},
            {"nombre": "diente_a3", "desde": [7, 7, 13], "hasta": [8, 8, 14],
             "material": "laton.oscuro"},
            {"nombre": "diente_b1", "desde": [3, 3, 13], "hasta": [4, 4, 14],
             "material": "laton.oscuro"},
            {"nombre": "diente_b2", "desde": [5, 3, 13], "hasta": [6, 4, 14],
             "material": "laton.oscuro"},
            {"nombre": "diente_b3", "desde": [7, 3, 13], "hasta": [8, 4, 14],
             "material": "laton.oscuro"},
            {"nombre": "centro", "desde": [5, 5, 13], "hasta": [6, 6, 14],
             "material": "hierro.oscuro", "nota": "centro de eje del volante"},
            # --- caja de bornes y escape ---
            {"nombre": "caja_bornes", "desde": [8, 9, 6], "hasta": [11, 12, 9],
             "material": "metal_oscuro.base"},
            {"nombre": "escape", "desde": [9, 9, 4], "hasta": [10, 14, 6],
             "material": "oxido", "nota": "tubo oxidado: entra en la caja de bornes; sube 4 px"},
            {"nombre": "tapa_escape", "desde": [8, 14, 3], "hasta": [11, 15, 6],
             "material": "metal_oscuro.base", "nota": "capuchón de lluvia"},
            # --- bota hidráulica ---
            {"nombre": "bota", "desde": [10, 4, 10], "hasta": [12, 7, 14],
             "material": "metal_oscuro.base",
             "nota": "cilindro hidráulico: 1 px enterrado, 3 px al frente"},
            {"nombre": "vastago", "desde": [10, 7, 14], "hasta": [12, 12, 15],
             "material": "aluminio.claro", "nota": "pistón de aluminio"},
            {"nombre": "copa", "desde": [9, 11, 13], "hasta": [13, 13, 15],
             "material": "hierro.claro", "nota": "copa de anclaje del pistón"},
            # --- caja de bornes de cobre, placa, tapones de inspección ---
            {"nombre": "caja_cobre", "desde": [1, 4, 5], "hasta": [4, 7, 11],
             "material": "cobre.oscuro",
             "nota": "caja de bornes de cobre: 1 px enterrada en la carcaza"},
            {"nombre": "tornillo_cobre_a", "desde": [0, 5, 6], "hasta": [2, 6, 7],
             "material": "cobre.claro"},
            {"nombre": "tornillo_cobre_b", "desde": [0, 5, 9], "hasta": [2, 6, 10],
             "material": "cobre.claro"},
            {"nombre": "placa_marca", "desde": [8, 4, 10], "hasta": [10, 5, 12],
             "material": "laton.claro", "nota": "placa de marca КРАН-14"},
            {"nombre": "puerto_1", "desde": [5, 8, 10], "hasta": [6, 9, 12],
             "material": "aluminio.claro", "nota": "tapa de inspección"},
            {"nombre": "puerto_2", "desde": [11, 8, 10], "hasta": [12, 9, 12],
             "material": "aluminio.claro"},
            # --- desgaste ---
            {"nombre": "hollin_escape", "desde": [10, 2, 3], "hasta": [12, 3, 5],
             "material": "hollin"},
            {"nombre": "mugre_zapata", "desde": [3, 2, 13], "hasta": [6, 3, 15],
             "material": "mugre"},
        ],
    },
]
