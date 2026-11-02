"""Specs de la zona military — tier 3.

Equipo militar soviético: baterías de tanque, radio de campaña, óptica.
Cajas verdes y metales de bornería, costras de sulfato y mugre como
desgaste firma. Geometría de componentes reales: tapones, bornes con
tornillo, abrazaderas, rejilla, teclado, antena telescópica.
"""

SPECS = [
    {
        "id": "bateria_tanque_t72",
        "nombre": "Batería de Tanque T-72 Sulfatada",
        "zona": "military",
        "tier": 3,
        "categoria": "electronica",
        "clase": "media",
        "silueta": "caja ebonítica pesada de batería de tanque sobre peana "
                   "recesada: tapa con deck de goma y seis tapones de celdas, "
                   "dos torres de borne de plomo con bozal y tornillos, dos "
                   "correas de hierro sobre la tapa (una con hebilla y "
                   "óxido), costras de sulfato blanco devorando el borne "
                   "izquierdo y corriendo el derecho, manija de transporte, "
                   "placa de datos de latón en el flanco",
        "permitir_flotantes": False,
        "notas": [
            "Historia visual: batería de tanque abandonada años atrás; el "
            "sulfato cristalizado (acentos 1-2) cuenta el abandono químico, "
            "óxido en la correa Este (acento 3) y mugre al pie.",
            "Componentes: peana recesada bajo la caja, tapa con deck de "
            "goma, 6 tapones de celda, torres de borne con bozal y tornillo "
            "transversal, 2 correas de seguro sobre la tapa (la Oeste con "
            "hebilla), manija.",
            "Los tornillos de borne nacen por debajo de las costras para "
            "que cada una deje ver un tornillo libre.",
            "Tensión y logging van en la textura del atlas (Fase 1.5).",
        ],
        "piezas": [
            # --- peana y caja ---
            {"nombre": "peana", "desde": [1, 0, 3], "hasta": [13, 2, 11],
             "material": "baquelita_negra.oscuro", "nota": "peana recesada: la caja la tapa 1 px por cada lado"},
            {"nombre": "caja", "desde": [0, 2, 2], "hasta": [14, 10, 12],
             "material": "baquelita_negra.base"},
            # --- tapa con tapones ---
            {"nombre": "tapa", "desde": [1, 9, 3], "hasta": [13, 11, 11],
             "material": "goma.base", "nota": "deck de goma: 1 px enterrado, 1 px saliente"},
            {"nombre": "tapon_f1", "desde": [2, 10, 4], "hasta": [4, 12, 6],
             "material": "aluminio.base"},
            {"nombre": "tapon_f2", "desde": [6, 10, 4], "hasta": [8, 12, 6],
             "material": "aluminio.base"},
            {"nombre": "tapon_f3", "desde": [10, 10, 4], "hasta": [12, 12, 6],
             "material": "aluminio.base"},
            {"nombre": "tapon_b1", "desde": [2, 10, 8], "hasta": [4, 12, 10],
             "material": "aluminio.base"},
            {"nombre": "tapon_b2", "desde": [6, 10, 8], "hasta": [8, 12, 10],
             "material": "aluminio.base"},
            {"nombre": "tapon_b3", "desde": [10, 10, 8], "hasta": [12, 12, 10],
             "material": "aluminio.base"},
            # --- torres de borne ---
            {"nombre": "torre_izq", "desde": [1, 9, 6], "hasta": [3, 14, 8],
             "material": "plomo.claro", "nota": "1 px enterrada en la tapa, sube 3 px"},
            {"nombre": "bozal_izq", "desde": [1, 13, 5], "hasta": [3, 14, 9],
             "material": "hierro.oscuro", "nota": "bozal oscuro sobre el poste"},
            {"nombre": "tornillo_izq", "desde": [0, 10, 6], "hasta": [2, 11, 8],
             "material": "hierro.claro", "nota": "tornillo transversal, 1 px visible al Oeste"},
            {"nombre": "torre_der", "desde": [11, 9, 6], "hasta": [13, 14, 8],
             "material": "plomo.claro"},
            {"nombre": "bozal_der", "desde": [11, 13, 5], "hasta": [13, 14, 9],
             "material": "hierro.oscuro"},
            {"nombre": "tornillo_der", "desde": [12, 10, 6], "hasta": [14, 11, 8],
             "material": "hierro.claro", "nota": "tornillo transversal, 1 px visible al Este"},
            # --- sulfato ---
            {"nombre": "costra_izq", "desde": [0, 11, 4], "hasta": [2, 13, 9],
             "material": "sulfato", "nota": "cristales devorando el borne izquierdo"},
            {"nombre": "costra_der", "desde": [12, 11, 4], "hasta": [14, 13, 9],
             "material": "sulfato", "nota": "costra corriendo el borde derecho"},
            # --- correas de seguro sobre la tapa y herrajes ---
            {"nombre": "corchete_oeste", "desde": [1, 10, 3], "hasta": [3, 12, 11],
             "material": "hierro.claro", "nota": "correa metálica sobre la tapa, extremo Oeste"},
            {"nombre": "corchete_este", "desde": [11, 10, 3], "hasta": [13, 12, 11],
             "material": "hierro.claro", "nota": "correa metálica sobre la tapa, extremo Este"},
            {"nombre": "hebilla", "desde": [1, 10, 10], "hasta": [3, 12, 13],
             "material": "hierro.oscuro", "nota": "hebilla de tensado al frente de la correa Oeste"},
            {"nombre": "manija", "desde": [6, 10, 6], "hasta": [9, 12, 7],
             "material": "hierro.oscuro", "nota": "asa de transporte"},
            {"nombre": "oxido_correa", "desde": [11, 10, 10], "hasta": [13, 11, 13],
             "material": "oxido", "nota": "óxido reventando el frente de la correa Este"},
            # --- placa y desgaste ---
            {"nombre": "placa_datos", "desde": [0, 7, 6], "hasta": [2, 9, 8],
             "material": "laton.base", "nota": "etiqueta 48ТН-125 en el flanco oeste"},
            {"nombre": "mugre_pie", "desde": [4, 2, 11], "hasta": [6, 3, 14],
             "material": "mugre", "nota": "mugre al pie de la caja frontal"},
        ],
    },
    {
        "id": "radio_campana_r159",
        "nombre": "Radio de Campaña Cifrada \"R-159\"",
        "zona": "military",
        "tier": 3,
        "categoria": "electronica",
        "clase": "media",
        "silueta": "radio de campaña verde con rejilla de altavoz entizada "
                   "dominante al frente con barras de aluminio, botonera de "
                   "campo bajo con teclas claras y selector con marcador, "
                   "doble LED de estado entre ambos, antena telescópica con "
                   "seguro en la esquina, módulo de cifrado verde militar "
                   "apilado al Este con dos bornes, asa de goma y prensas de "
                   "eslinga a los flancos",
        "permitir_flotantes": False,
        "notas": [
            "Historia visual: radio de un puesto abandonado; el módulo verde "
            "apilado al Este es el equipo de cifrado con bornes probados, "
            "la mugre al pie de la botonera cuenta el uso de campo "
            "(acento 1) y la pátina radiactiva del borde cheme (acento 2) "
            "sella el destino del puesto.",
            "Componentes: rejilla con 2 barras salientes, botonera con 4 "
            "teclas, selector con marcador de cerámica, 2 LED, antena "
            "telescópica (soporte + varilla + seguro), módulo con bornes, "
            "asa de goma, prensas de eslinga a ambos flancos.",
            "Los pies de goma asoman 1 px al Norte y al Sur de la caja.",
        ],
        "piezas": [
            # --- caja y pies ---
            {"nombre": "caja", "desde": [1, 0, 3], "hasta": [10, 12, 11],
             "material": "verde_oliva.base"},
            {"nombre": "pie_fl", "desde": [2, 0, 2], "hasta": [4, 2, 4],
             "material": "goma.oscuro", "nota": "asoma 1 px al Norte"},
            {"nombre": "pie_fr", "desde": [7, 0, 2], "hasta": [9, 2, 4],
             "material": "goma.oscuro"},
            {"nombre": "pie_bl", "desde": [2, 0, 10], "hasta": [4, 2, 12],
             "material": "goma.oscuro", "nota": "asoma 1 px al Sur"},
            {"nombre": "pie_br", "desde": [7, 0, 10], "hasta": [9, 2, 12],
             "material": "goma.oscuro"},
            # --- rejilla de altavoz ---
            {"nombre": "reja", "desde": [2, 5, 10], "hasta": [9, 10, 13],
             "material": "metal_oscuro.base", "nota": "1 px enterrada, 2 px salientes al Sur"},
            {"nombre": "barra_reja_a", "desde": [2, 6, 12], "hasta": [9, 7, 14],
             "material": "aluminio.oscuro", "nota": "barra de aluminio, 1 px saliente"},
            {"nombre": "barra_reja_b", "desde": [2, 8, 12], "hasta": [9, 9, 14],
             "material": "aluminio.oscuro"},
            # --- botonera, teclas y selector ---
            {"nombre": "teclado", "desde": [2, 1, 10], "hasta": [6, 4, 12],
             "material": "metal_oscuro.base", "nota": "piso de botonera"},
            {"nombre": "tecla_a", "desde": [3, 1, 11], "hasta": [4, 2, 13],
             "material": "plastico_amarillento.oscuro"},
            {"nombre": "tecla_b", "desde": [5, 1, 11], "hasta": [6, 2, 13],
             "material": "plastico_amarillento.oscuro"},
            {"nombre": "tecla_c", "desde": [3, 3, 11], "hasta": [4, 4, 13],
             "material": "plastico_amarillento.oscuro"},
            {"nombre": "tecla_d", "desde": [5, 3, 11], "hasta": [6, 4, 13],
             "material": "plastico_amarillento.oscuro"},
            {"nombre": "selector", "desde": [7, 1, 10], "hasta": [9, 3, 12],
             "material": "baquelita_negra.base", "nota": "mando giratorio"},
            {"nombre": "marcador", "desde": [8, 2, 11], "hasta": [9, 3, 13],
             "material": "plastico_amarillento", "nota": "aguja del selector"},
            # --- LED de estado ---
            {"nombre": "led_verde", "desde": [8, 4, 10], "hasta": [9, 5, 12],
             "material": "verde_acido", "nota": "LED de comprobación"},
            {"nombre": "led_rojo", "desde": [6, 4, 10], "hasta": [7, 5, 12],
             "material": "rojo_desgastado", "nota": "LED de cifrado"},
            # --- antena telescópica ---
            {"nombre": "prolongador", "desde": [2, 11, 6], "hasta": [4, 13, 8],
             "material": "aluminio.base", "nota": "soporte rosado de la antena"},
            {"nombre": "varilla", "desde": [3, 12, 7], "hasta": [4, 15, 8],
             "material": "aluminio.claro", "nota": "varilla telescópica"},
            {"nombre": "seguro", "desde": [2, 13, 6], "hasta": [4, 14, 8],
             "material": "aluminio.base", "nota": "anillo de seguro en el tramo"},
            # --- módulo de cifrado ---
            {"nombre": "modulo_cifrado", "desde": [9, 4, 5], "hasta": [12, 10, 9],
             "material": "verde_militar.base",
             "nota": "equipo de cifrado: 1 px enterrado, 2 px salientes al Este"},
            {"nombre": "borne_mod_a", "desde": [11, 5, 6], "hasta": [13, 6, 7],
             "material": "metal_oscuro.base"},
            {"nombre": "borne_mod_b", "desde": [11, 8, 6], "hasta": [13, 9, 7],
             "material": "metal_oscuro.base"},
            # --- asa y prensas ---
            {"nombre": "asa", "desde": [5, 11, 6], "hasta": [8, 13, 7],
             "material": "goma.oscuro", "nota": "asa abatible"},
            {"nombre": "prensa_oeste", "desde": [0, 9, 2], "hasta": [2, 11, 4],
             "material": "metal_oscuro.base", "nota": "argolla de eslinga: 1 px enterrada"},
            {"nombre": "prensa_este", "desde": [9, 9, 2], "hasta": [11, 11, 4],
             "material": "metal_oscuro.base"},
            # --- desgaste ---
            {"nombre": "patina_borde", "desde": [7, 10, 10], "hasta": [9, 11, 12],
             "material": "patina_rad", "nota": "franja de pátina bajo la rejilla"},
            {"nombre": "mugre_pie", "desde": [3, 0, 10], "hasta": [5, 1, 13],
             "material": "mugre", "nota": "mugre de campo al pie de la tecla"},
        ],
    },
]
