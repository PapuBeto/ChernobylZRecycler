# Listado de objetos y recetas

Generado por `tools/generate.py` a partir de `tools/items.json`.

## Recursos base

| Item | Nombre (ES) | Nombre (EN) |
| :--- | :--- | :--- |
| `chernobylz_recycler:tela` | Tela | Cloth |
| `chernobylz_recycler:scrap` | Scrap | Scrap |
| `chernobylz_recycler:lingote_pesado` | Lingote Pesado | Heavy Ingot |

## Componentes (Fase 2)

| Item | Nombre (ES) | Al reciclar | Uso |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:engranaje_titanio` | Engranaje de Titanio | 1x lingote_pesado, 4x scrap | Puertas blindadas, torretas automáticas y mecanismos de cerrojo pesado. |
| `chernobylz_recycler:piston_hidraulico` | Pistón Hidráulico | 2x lingote_pesado, 6x scrap | Exoesqueletos de carga, prensas de munición y trampas de aplastamiento. |
| `chernobylz_recycler:tubo_presion` | Tubo de Presión | 1x lingote_pesado, 4x scrap | Cañones artesanales, lanzallamas y destiladores de agua radiactiva. |
| `chernobylz_recycler:valvula_antirretorno` | Válvula Antirretorno | 6x scrap | Lanzallamas, bombas de combustible y sistemas de filtrado de base. |
| `chernobylz_recycler:bobina_cobre` | Bobina de Cobre | 6x scrap | Motores eléctricos, generadores eólicos y cargadores de baterías. |
| `chernobylz_recycler:cableado_alta_tension` | Cableado de Alta Tensión | 6x scrap | Red eléctrica de bases, cercas electrificadas y generadores. |
| `chernobylz_recycler:placa_circuito_impreso` | Placa de Circuito Impreso | 6x scrap | Estaciones de radio, paneles solares y cerraduras electrónicas. |
| `chernobylz_recycler:condensador_alto_voltaje` | Condensador de Alto Voltaje | 6x scrap | Armas electromagnéticas, modificaciones eléctricas y bobinas Tesla. |
| `chernobylz_recycler:motor_paso_a_paso` | Motor Paso a Paso | 1x lingote_pesado, 8x scrap | Drones, torretas centinela y servos de armaduras pesadas. |
| `chernobylz_recycler:microprocesador_militar` | Microprocesador Militar | 10x scrap | Miras térmicas, radares de proximidad y terminales de hackeo. |
| `chernobylz_recycler:sensor_dosimetrico` | Sensor Dosimétrico | 10x scrap | Contadores Geiger avanzados y alarmas de tormenta radiactiva. |
| `chernobylz_recycler:lente_optica_precision` | Lente Óptica de Precisión | 6x scrap | Miras telescópicas, visores nocturnos y telémetros láser. |
| `chernobylz_recycler:filtro_carbon_activado` | Filtro de Carbón Activado | 4x tela, 5x scrap | Máscaras de gas, cascos Hazmat y purificadores de aire. |
| `chernobylz_recycler:tejido_kevlar_plomado` | Tejido de Kevlar Plomado | 6x tela, 1x lingote_pesado | Trajes antirradiación de élite y chalecos antibalas nivel 3. |
| `chernobylz_recycler:celda_litio_militar` | Celda de Litio Militar | 1x lingote_pesado, 6x scrap | Visores nocturnos, miras holográficas y linternas UV. |
| `chernobylz_recycler:nucleo_plomo_sellado` | Núcleo de Plomo Sellado | 3x lingote_pesado, 2x scrap | Munición perforante, escudos antidisturbios y cofres ocultos. |

## Zona Industrial

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:motor_grua_sovietica` (compound) | 4x lingote_pesado, 18x scrap | 2x engranaje_titanio, 1x piston_hidraulico, 2x bobina_cobre | 170 |
| `chernobylz_recycler:taladro_percutor_mina` (compound) | 2x lingote_pesado, 12x scrap | 1x engranaje_titanio, 1x tubo_presion, 1x cableado_alta_tension | 170 |
| `chernobylz_recycler:compresor_aire_fabrica` (compound) | 3x lingote_pesado, 15x scrap | 2x tubo_presion, 1x valvula_antirretorno, 1x piston_hidraulico | 170 |
| `chernobylz_recycler:bomba_hidraulica_refrigeracion` (compound) | 3x lingote_pesado, 10x scrap | 2x valvula_antirretorno, 2x tubo_presion | 170 |
| `chernobylz_recycler:soldadora_arco_portatil` (compound) | 1x lingote_pesado, 16x scrap | 2x bobina_cobre, 2x cableado_alta_tension, 1x placa_circuito_impreso | 170 |
| `chernobylz_recycler:caja_engranajes_tractor` (compound) | 3x lingote_pesado, 12x scrap | 3x engranaje_titanio, 1x piston_hidraulico | 170 |
| `chernobylz_recycler:viga_acero_retorcida` (simple) | 2x lingote_pesado | - | 100 |
| `chernobylz_recycler:contrapeso_grua` (simple) | 3x lingote_pesado | - | 100 |
| `chernobylz_recycler:cadena_remolque` (simple) | 1x lingote_pesado, 6x scrap | - | 100 |
| `chernobylz_recycler:lamina_techo_corrugada` (simple) | 10x scrap | - | 100 |
| `chernobylz_recycler:caja_clavos_tuercas` (simple) | 8x scrap | - | 100 |
| `chernobylz_recycler:guantes_soldador` (simple) | 6x tela, 2x scrap | - | 100 |
| `chernobylz_recycler:casco_minero` (simple) | 5x scrap, 2x tela | - | 100 |

## Zona Química

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:traje_hazmat_liquidador` (compound) | 14x tela, 6x scrap | 2x tejido_kevlar_plomado, 1x filtro_carbon_activado, 1x lente_optica_precision | 240 |
| `chernobylz_recycler:contador_geiger_pripyat` (compound) | 10x scrap | 1x sensor_dosimetrico, 1x placa_circuito_impreso, 1x celda_litio_militar | 240 |
| `chernobylz_recycler:respirador_papr` (compound) | 8x tela, 8x scrap | 2x filtro_carbon_activado, 1x tubo_presion, 1x celda_litio_militar | 240 |
| `chernobylz_recycler:centrifugadora_muestras` (compound) | 2x lingote_pesado, 14x scrap | 1x motor_paso_a_paso, 2x valvula_antirretorno, 1x placa_circuito_impreso | 240 |
| `chernobylz_recycler:contenedor_isotopos` (compound) | 4x lingote_pesado, 8x scrap | 1x nucleo_plomo_sellado, 1x sensor_dosimetrico, 1x valvula_antirretorno | 240 |
| `chernobylz_recycler:rociador_descontaminacion` (compound) | 4x tela, 10x scrap | 2x tubo_presion, 1x valvula_antirretorno, 1x filtro_carbon_activado | 240 |
| `chernobylz_recycler:ladrillo_blindaje_plomo` (simple) | 3x lingote_pesado | - | 140 |
| `chernobylz_recycler:delantal_laboratorio` (simple) | 6x tela, 2x lingote_pesado | - | 140 |
| `chernobylz_recycler:bidon_acido` (simple) | 8x scrap | - | 140 |
| `chernobylz_recycler:botas_goma_descontaminantes` (simple) | 5x tela, 4x scrap | - | 140 |
| `chernobylz_recycler:lona_cuarentena` (simple) | 10x tela | - | 140 |
| `chernobylz_recycler:mascarilla_gp5` (simple) | 4x tela, 4x scrap | - | 140 |
| `chernobylz_recycler:gradilla_tubos_ensayo` (simple) | 6x scrap | - | 140 |

## Zona Militar

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:bateria_tanque_t72` (compound) | 5x lingote_pesado, 12x scrap | 2x nucleo_plomo_sellado, 2x celda_litio_militar | 240 |
| `chernobylz_recycler:visor_nocturno_pnv57` (compound) | 4x tela, 10x scrap | 2x lente_optica_precision, 1x microprocesador_militar, 1x celda_litio_militar | 240 |
| `chernobylz_recycler:chaleco_balistico_6b3` (compound) | 16x tela, 2x lingote_pesado | 3x tejido_kevlar_plomado, 1x engranaje_titanio | 240 |
| `chernobylz_recycler:radio_campana_r159` (compound) | 1x lingote_pesado, 16x scrap | 2x microprocesador_militar, 2x placa_circuito_impreso, 1x bobina_cobre | 240 |
| `chernobylz_recycler:modulo_punteria_btr` (compound) | 3x lingote_pesado, 14x scrap | 2x lente_optica_precision, 1x motor_paso_a_paso, 1x microprocesador_militar | 240 |
| `chernobylz_recycler:dron_reconocimiento` (compound) | 1x lingote_pesado, 18x scrap | 2x motor_paso_a_paso, 1x microprocesador_militar, 1x celda_litio_militar, 1x lente_optica_precision | 240 |
| `chernobylz_recycler:placa_balistica_acero` (simple) | 3x lingote_pesado | - | 140 |
| `chernobylz_recycler:eslabon_oruga_tanque` (simple) | 4x lingote_pesado | - | 140 |
| `chernobylz_recycler:caja_municion_50` (simple) | 1x lingote_pesado, 6x scrap | - | 140 |
| `chernobylz_recycler:casco_ssh68` (simple) | 1x lingote_pesado, 4x scrap | - | 140 |
| `chernobylz_recycler:cargador_baquelita_ak74` (simple) | 7x scrap | - | 140 |
| `chernobylz_recycler:red_camuflaje` (simple) | 14x tela | - | 140 |
| `chernobylz_recycler:botas_paracaidista` (simple) | 8x tela, 3x scrap | - | 140 |

## Zona Hospital

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:desfibrilador_portatil` (compound) | 4x tela, 12x scrap | 2x condensador_alto_voltaje, 1x celda_litio_militar, 1x cableado_alta_tension | 170 |
| `chernobylz_recycler:microscopio_quirurgico` (compound) | 1x lingote_pesado, 8x scrap | 3x lente_optica_precision, 1x engranaje_titanio | 170 |
| `chernobylz_recycler:ventilador_pulmonar_uci` (compound) | 6x tela, 12x scrap | 1x motor_paso_a_paso, 2x tubo_presion, 1x filtro_carbon_activado, 1x placa_circuito_impreso | 170 |
| `chernobylz_recycler:monitor_signos_vitales` (compound) | 12x scrap | 2x placa_circuito_impreso, 1x sensor_dosimetrico, 1x condensador_alto_voltaje | 170 |
| `chernobylz_recycler:autoclave_esterilizacion` (compound) | 2x lingote_pesado, 10x scrap | 2x valvula_antirretorno, 1x tubo_presion, 1x bobina_cobre | 170 |
| `chernobylz_recycler:camilla_aislamiento` (compound) | 18x tela, 10x scrap | 1x tejido_kevlar_plomado, 2x tubo_presion, 1x filtro_carbon_activado | 170 |
| `chernobylz_recycler:rollo_vendas_yodo` (simple) | 8x tela | - | 100 |
| `chernobylz_recycler:sabana_quirurgica` (simple) | 12x tela | - | 100 |
| `chernobylz_recycler:bata_paciente` (simple) | 9x tela | - | 100 |
| `chernobylz_recycler:bandeja_instrumentos` (simple) | 1x lingote_pesado, 5x scrap | - | 100 |
| `chernobylz_recycler:soporte_suero` (simple) | 9x scrap | - | 100 |
| `chernobylz_recycler:bolsa_desechos_biologicos` (simple) | 4x tela, 6x scrap | - | 100 |
| `chernobylz_recycler:muleta_aluminio` (simple) | 7x scrap, 2x tela | - | 100 |

## Zona Residencial

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:abrigo_afghanka` (compound) | 18x tela, 2x scrap | 1x tejido_kevlar_plomado | 120 |
| `chernobylz_recycler:microondas_dnepr` (compound) | 1x lingote_pesado, 10x scrap | 1x bobina_cobre, 1x condensador_alto_voltaje, 1x placa_circuito_impreso | 120 |
| `chernobylz_recycler:televisor_rubin` (compound) | 12x scrap | 2x bobina_cobre, 1x condensador_alto_voltaje, 1x placa_circuito_impreso | 120 |
| `chernobylz_recycler:lavadora_vyatka` (compound) | 2x lingote_pesado, 12x scrap | 1x motor_paso_a_paso, 1x tubo_presion, 1x valvula_antirretorno | 120 |
| `chernobylz_recycler:maquina_coser_podolsk` (compound) | 1x lingote_pesado, 8x scrap, 6x tela | 2x engranaje_titanio | 120 |
| `chernobylz_recycler:aspiradora_raketa` (compound) | 8x tela, 8x scrap | 1x tubo_presion, 1x bobina_cobre, 1x cableado_alta_tension | 120 |
| `chernobylz_recycler:taza_peltre` (simple) | 3x scrap | - | 70 |
| `chernobylz_recycler:olla_presion` (simple) | 8x scrap | - | 70 |
| `chernobylz_recycler:radiador_hierro` (simple) | 2x lingote_pesado, 4x scrap | - | 70 |
| `chernobylz_recycler:gorro_ushanka` (simple) | 7x tela | - | 70 |
| `chernobylz_recycler:vaqueros_rasgados` (simple) | 8x tela | - | 70 |
| `chernobylz_recycler:alfombra_persa` (simple) | 16x tela | - | 70 |
| `chernobylz_recycler:muneca_irradiada` (simple) | 4x scrap, 3x tela | - | 70 |
| `chernobylz_recycler:cubiertos_acero` (simple) | 5x scrap | - | 70 |

## Componentes Eléctricos

| Objeto | Fase 1 | Componentes | Tiempo (ticks) |
| :--- | :--- | :--- | :--- |
| `chernobylz_recycler:transformador_subestacion` (compound) | 3x lingote_pesado, 14x scrap | 3x bobina_cobre, 2x condensador_alto_voltaje, 1x cableado_alta_tension | 120 |
| `chernobylz_recycler:panel_control_reactor` (compound) | 1x lingote_pesado, 16x scrap | 2x placa_circuito_impreso, 1x sensor_dosimetrico, 2x cableado_alta_tension | 120 |
| `chernobylz_recycler:alternador_generador_diesel` (compound) | 2x lingote_pesado, 10x scrap | 2x bobina_cobre, 1x engranaje_titanio, 1x cableado_alta_tension | 120 |
| `chernobylz_recycler:estabilizador_voltaje` (compound) | 12x scrap | 2x condensador_alto_voltaje, 1x placa_circuito_impreso, 1x bobina_cobre | 120 |
| `chernobylz_recycler:bateria_ups_servidor` (compound) | 2x lingote_pesado, 8x scrap | 1x nucleo_plomo_sellado, 1x celda_litio_militar, 1x placa_circuito_impreso | 120 |
| `chernobylz_recycler:caja_disyuntores_trifasicos` (compound) | 10x scrap | 2x cableado_alta_tension, 1x condensador_alto_voltaje, 1x bobina_cobre | 120 |
| `chernobylz_recycler:cable_telefonico` (simple) | 7x scrap | - | 70 |
| `chernobylz_recycler:aislador_ceramico` (simple) | 6x scrap | - | 70 |
| `chernobylz_recycler:fusible_porcelana` (simple) | 5x scrap | - | 70 |
| `chernobylz_recycler:carcasa_enchufe` (simple) | 4x scrap | - | 70 |
| `chernobylz_recycler:tubo_fluorescente` (simple) | 8x scrap | - | 70 |
| `chernobylz_recycler:placa_disipadora_aluminio` (simple) | 1x lingote_pesado, 3x scrap | - | 70 |

## Texturas

Las 97 texturas estan en `src/main/resources/assets/chernobylz_recycler/textures/item/`.
Se generan con `tools/textures.py` (recursos y componentes) y `tools/objects.py`
(objetos por zona). Reemplaza cada PNG por tu arte de Blockbench manteniendo el mismo
nombre; `tools/generate.py` no sobreescribe texturas existentes.
