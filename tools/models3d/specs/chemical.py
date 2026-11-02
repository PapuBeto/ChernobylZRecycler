"""Specs de la zona chemical — tier 3.

Instrumentos químicos del puesto avanzado de Pripyat: contador Geiger de
baquelita, traje de liquidador, filtros y frascos. La primera spec
(`contador_geiger_pripyat`) es la calibración de la Fase 0; después del
rediseño mantiene esa condición de prueba con un nivel de detalle mucho
mayor: cada componente es una pieza real del aparato.
"""

SPECS = [
    {
        "id": "contador_geiger_pripyat",
        "nombre": "Contador Geiger \"Pripyat-M\" Roto",
        "zona": "chemical",
        "tier": 3,
        "categoria": "electronica",
        "clase": "media",
        "silueta": "aparato de baquelita con faldón recesado al pie, visor "
                   "enmarcado de aluminio con vidrio saliente, botonera "
                   "tallada bajo el visor con pulsador rojo y negro que "
                   "sobran, dial mecánico de latón saliente al costado Este "
                   "con volante de ajuste, asa metálica plegable medio caída "
                   "con soporte derecho roto, correa de transporte rasgada "
                   "a la mitad y tanda de toma con toma y toma de sonda​ "
                   "al costado: tubería de goma con flange, aro y ventana de "
                   "detección, conectada por cable bajo el cuerpo",
        "permitir_flotantes": False,
        "notas": [
            "Calibración del sistema de diseño (Fase 0) tras el rediseño.",
            "Historia visual: instrumento abandonado tras el accidente; asa "
            "medio caída con el soporte derecho roto, correa partida en dos, "
            "pintura saltada (acento 1) y óxido a media altura junto al "
            "visor (acento 2).",
            "El visor (vidrio oscuro) sobresale 1 px del marco; agujas y "
            "escala van en la textura del atlas (Fase 1.5).",
            "El dial lateral emplaca la cara Este en latón con cristal: "
            "placa 3 px saliente con volante de ajuste 1 px.",
            "La sonda es pieza separada apoyada al Este: tubería de goma "
            "sobre flange, aro aluminio, tapa y ventana de detección; el "
            "cable corre escondido bajo el cuerpo y sale atrás.",
        ],
        "piezas": [
            # --- cuerpo y faldón ---
            {"nombre": "cuerpo", "desde": [1, 0, 5], "hasta": [10, 10, 11],
             "material": "baquelita"},
            {"nombre": "faldon", "desde": [0, 0, 6], "hasta": [11, 2, 12],
             "material": "baquelita.oscuro",
             "nota": "zoclo recesado al Norte y saliente al Sur y a ambos flancos"},
            # --- visor enmarcado ---
            {"nombre": "arco_visor", "desde": [2, 4, 10], "hasta": [8, 11, 12],
             "material": "aluminio.base",
             "nota": "marco de aluminio: 1 px enterrado, 1 px saliente y 1 px más alto que el cuerpo"},
            {"nombre": "vidrio", "desde": [3, 5, 11], "hasta": [7, 9, 13],
             "material": "vidrio_oscuro", "nota": "cristal del visor: 1 px saliente del marco"},
            {"nombre": "remache_tl", "desde": [2, 10, 11], "hasta": [3, 12, 13],
             "material": "aluminio.claro", "nota": "remache de marco"},
            {"nombre": "remache_tr", "desde": [7, 10, 11], "hasta": [8, 12, 13],
             "material": "aluminio.claro"},
            # --- botonera ---
            {"nombre": "boton_rojo", "desde": [2, 2, 10], "hasta": [4, 4, 13],
             "material": "rojo_desgastado", "nota": "pulsador tallado: 2 px salientes"},
            {"nombre": "boton_negro", "desde": [5, 2, 10], "hasta": [7, 4, 13],
             "material": "goma.oscuro", "nota": "pulsador de goma"},
            # --- dial lateral ---
            {"nombre": "dial_lateral", "desde": [9, 4, 6], "hasta": [13, 8, 9],
             "material": "laton.base", "caras": {"este": "vidrio_oscuro"},
             "nota": "placa de escala: 1 px enterrada, 3 px salientes"},
            {"nombre": "volante_dial", "desde": [12, 5, 7], "hasta": [14, 7, 8],
             "material": "aluminio.claro", "nota": "volante de ajuste, 1 px saliente"},
            # --- asa y correa ---
            {"nombre": "post_izq", "desde": [3, 9, 6], "hasta": [4, 11, 7],
             "material": "hierro.oscuro", "nota": "soporte izq: 1 px enterrado"},
            {"nombre": "asa_barra", "desde": [3, 10, 6], "hasta": [7, 12, 7],
             "material": "hierro.claro", "nota": "asa plegable apoyada sobre el cuerpo"},
            {"nombre": "grip", "desde": [4, 11, 6], "hasta": [6, 13, 7],
             "material": "goma.oscuro", "nota": "agarra de goma del asa"},
            {"nombre": "stub_der", "desde": [7, 9, 6], "hasta": [8, 11, 7],
             "material": "hierro.oscuro", "nota": "soporte derecho roto: muñón de 1 px"},
            {"nombre": "correa_a", "desde": [2, 9, 4], "hasta": [5, 12, 6],
             "material": "tela_crema", "nota": "correa partida: 1 px enterrada en el cuerpo"},
            {"nombre": "correa_b", "desde": [7, 9, 4], "hasta": [9, 12, 6],
             "material": "tela_crema", "nota": "correa partida: grupo derecho"},
            # --- sonda y cable ---
            {"nombre": "tuerca_sonda", "desde": [11, 0, 11], "hasta": [13, 9, 13],
             "material": "goma.base", "nota": "tubería de la sonda, de pie"},
            {"nombre": "flange_sonda", "desde": [10, 0, 10], "hasta": [14, 1, 14],
             "material": "goma.oscuro", "nota": "flange de pie"},
            {"nombre": "aro_sonda", "desde": [10, 4, 10], "hasta": [14, 5, 14],
             "material": "aluminio.base", "nota": "aro real a media tubería"},
            {"nombre": "tapa_sonda", "desde": [11, 8, 11], "hasta": [13, 11, 13],
             "material": "aluminio.claro", "nota": "tapa: 1 px enterrada, 2 px saliente"},
            {"nombre": "ventana", "desde": [12, 11, 12], "hasta": [13, 12, 13],
             "material": "vidrio", "nota": "ventana sensible, 1x1x1"},
            {"nombre": "cable", "desde": [8, 0, 4], "hasta": [11, 1, 10],
             "material": "goma.oscuro", "nota": "cable escondido bajo el cuerpo y saliente tras y flanco"},
            # --- desgaste ---
            {"nombre": "imprimacion", "desde": [2, 0, 11], "hasta": [4, 2, 13],
             "material": "imprimacion", "nota": "pintura saltada sobre el zoclo"},
            {"nombre": "oxido", "desde": [8, 5, 10], "hasta": [9, 7, 12],
             "material": "oxido", "nota": "óxido junto al marco"},
        ],
    },
    {
        "id": "traje_hazmat_liquidador",
        "nombre": "Traje Hazmat de Liquidador Rasgado",
        "zona": "chemical",
        "tier": 3,
        "categoria": "textil",
        "clase": "media",
        "silueta": "mono de liquidador de pie en amarillo pálido: botas de "
                   "goma que abrazan los talones, piernas separadas, torso "
                   "macizo con cinturón de goma oscuro con hebilla metálica, "
                   "respirador al pecho con dos filtros cilíndricos, "
                   "válvula de exhalación en el flanco, capucha de dos "
                   "escalaes con visor oscuro saliente, brazos con puños de "
                   "goma y la rasgadura del antebrazo derecho asomando el "
                   "forro",
        "permitir_flotantes": False,
        "notas": [
            "Historia visual: traje de liquidador colgado de servicio; el "
            "rasgado derecho enseña el forro de goma (oscuro) — el daño es "
            "del propio traje, no desgaste de superficie.",
            "Componentes: botas abrazadas, cinturón con hebilla, respirador "
            "con 2 filtros (asoman tras el cinturón como peto de pecho), "
            "válvula de exhalación lateral, capucha de 2 escalas, visor "
            "oscuro de 2 px, puños abrochados, forro del rasgado.",
            "Brazos unidos al torso por fusion del mismo material (contacto "
            "plano permitido); capucha enterrada 1 px en el torso.",
            "Acentos: moho en la espinilla (1), pátina radiactiva en el pecho "
            "(2) y goteo ácido deslizando desde el visor (3).",
        ],
        "piezas": [
            # --- piernas y botas ---
            {"nombre": "pierna_izq", "desde": [2, 0, 6], "hasta": [5, 6, 9],
             "material": "hazmat.base"},
            {"nombre": "pierna_der", "desde": [6, 0, 6], "hasta": [9, 6, 9],
             "material": "hazmat.base"},
            {"nombre": "bota_izq", "desde": [1, 0, 5], "hasta": [5, 2, 10],
             "material": "goma.oscuro", "nota": "bota que abraza: 1 px saliente a tres lados"},
            {"nombre": "bota_der", "desde": [6, 0, 5], "hasta": [10, 2, 10],
             "material": "goma.oscuro"},
            # --- torso, cinturón, hebilla ---
            {"nombre": "torso", "desde": [2, 6, 5], "hasta": [9, 12, 10],
             "material": "hazmat.base",
             "nota": "apoya sobre las piernas por fusión del mismo material"},
            {"nombre": "cinturon", "desde": [1, 5, 4], "hasta": [10, 7, 11],
             "material": "goma.oscuro", "nota": "cinturón que rodea el torso"},
            {"nombre": "hebilla", "desde": [3, 5, 9], "hasta": [5, 6, 12],
             "material": "aluminio.claro", "nota": "hebilla metálica, 1 px saliente"},
            # --- respirador y filtros ---
            {"nombre": "respirador", "desde": [4, 8, 9], "hasta": [7, 11, 11],
             "material": "goma.base", "nota": "pestaña del respirador al pecho alto: 1 px saliente"},
            {"nombre": "filtro_izq", "desde": [3, 7, 10], "hasta": [4, 10, 13],
             "material": "metal_oscuro.base", "nota": "filtro cilíndrico, 2 px saliente"},
            {"nombre": "filtro_der", "desde": [7, 7, 10], "hasta": [8, 10, 13],
             "material": "metal_oscuro.base"},
            {"nombre": "valvula", "desde": [0, 8, 7], "hasta": [2, 9, 9],
             "material": "goma.oscuro", "nota": "válvula de exhalación al flanco oeste"},
            # --- capucha y visor ---
            {"nombre": "capucha_baja", "desde": [3, 11, 7], "hasta": [8, 13, 10],
             "material": "hazmat.base", "nota": "capucha fundida con el frente del torso (mismo material)",
            },
            {"nombre": "corona", "desde": [4, 12, 7], "hasta": [7, 14, 10],
             "material": "hazmat.base", "nota": "corona de la capucha: 1 px enterrada, 1 px arriba"},
            {"nombre": "visor", "desde": [4, 12, 9], "hasta": [7, 13, 11],
             "material": "vidrio_oscuro", "nota": "ranura oscura del visor, 1 px saliente"},
            # --- brazos, puños y rasgadura ---
            {"nombre": "brazo_izq", "desde": [0, 7, 6], "hasta": [2, 12, 8],
             "material": "hazmat.base", "nota": "manga pegada por fusión del mismo material"},
            {"nombre": "guante_izq", "desde": [0, 6, 4], "hasta": [2, 7, 10],
             "material": "goma.oscuro", "nota": "puño abrochado"},
            {"nombre": "brazo_der", "desde": [9, 7, 6], "hasta": [11, 12, 8],
             "material": "hazmat.base"},
            {"nombre": "guante_der", "desde": [9, 6, 4], "hasta": [11, 7, 10],
             "material": "goma.oscuro"},
            {"nombre": "rasgadura", "desde": [9, 8, 7], "hasta": [11, 10, 10],
             "material": "goma.oscuro", "nota": "forro expuesto del antebrazo derecho"},
            # --- desgaste ---
            {"nombre": "patina", "desde": [6, 10, 9], "hasta": [8, 11, 12],
             "material": "patina_rad", "nota": "pátina radiactiva en el pecho"},
            {"nombre": "moho", "desde": [2, 3, 8], "hasta": [3, 4, 10],
             "material": "moho", "nota": "polvo de humedad en la espinilla"},
            {"nombre": "goteo", "desde": [5, 12, 10], "hasta": [6, 14, 12],
             "material": "goteo_acido", "nota": "goteo ácido desde la ranura del visor"},
        ],
    },
]
