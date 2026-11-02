package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.item.RecyclerItem;
import java.util.List;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

/**
 * Registro de items. ARCHIVO GENERADO por tools/generate.py.
 * Edita tools/items.json y vuelve a ejecutar el generador.
 */
public final class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ChernobylZRecycler.MODID);

    public static final RegistryObject<Item> TELA = register("tela", 64, Rarity.COMMON, "tooltip.resource");
    public static final RegistryObject<Item> SCRAP = register("scrap", 64, Rarity.COMMON, "tooltip.resource");
    public static final RegistryObject<Item> LINGOTE_PESADO = register("lingote_pesado", 64, Rarity.COMMON, "tooltip.resource");
    public static final RegistryObject<Item> ENGRANAJE_TITANIO = register("engranaje_titanio", 64, Rarity.COMMON, "tooltip.component", "use.engranaje_titanio");
    public static final RegistryObject<Item> PISTON_HIDRAULICO = register("piston_hidraulico", 64, Rarity.COMMON, "tooltip.component", "use.piston_hidraulico");
    public static final RegistryObject<Item> TUBO_PRESION = register("tubo_presion", 64, Rarity.COMMON, "tooltip.component", "use.tubo_presion");
    public static final RegistryObject<Item> VALVULA_ANTIRRETORNO = register("valvula_antirretorno", 64, Rarity.COMMON, "tooltip.component", "use.valvula_antirretorno");
    public static final RegistryObject<Item> BOBINA_COBRE = register("bobina_cobre", 64, Rarity.COMMON, "tooltip.component", "use.bobina_cobre");
    public static final RegistryObject<Item> CABLEADO_ALTA_TENSION = register("cableado_alta_tension", 64, Rarity.COMMON, "tooltip.component", "use.cableado_alta_tension");
    public static final RegistryObject<Item> PLACA_CIRCUITO_IMPRESO = register("placa_circuito_impreso", 64, Rarity.COMMON, "tooltip.component", "use.placa_circuito_impreso");
    public static final RegistryObject<Item> CONDENSADOR_ALTO_VOLTAJE = register("condensador_alto_voltaje", 64, Rarity.COMMON, "tooltip.component", "use.condensador_alto_voltaje");
    public static final RegistryObject<Item> MOTOR_PASO_A_PASO = register("motor_paso_a_paso", 64, Rarity.COMMON, "tooltip.component", "use.motor_paso_a_paso");
    public static final RegistryObject<Item> MICROPROCESADOR_MILITAR = register("microprocesador_militar", 64, Rarity.COMMON, "tooltip.component", "use.microprocesador_militar");
    public static final RegistryObject<Item> SENSOR_DOSIMETRICO = register("sensor_dosimetrico", 64, Rarity.COMMON, "tooltip.component", "use.sensor_dosimetrico");
    public static final RegistryObject<Item> LENTE_OPTICA_PRECISION = register("lente_optica_precision", 64, Rarity.COMMON, "tooltip.component", "use.lente_optica_precision");
    public static final RegistryObject<Item> FILTRO_CARBON_ACTIVADO = register("filtro_carbon_activado", 64, Rarity.COMMON, "tooltip.component", "use.filtro_carbon_activado");
    public static final RegistryObject<Item> TEJIDO_KEVLAR_PLOMADO = register("tejido_kevlar_plomado", 64, Rarity.COMMON, "tooltip.component", "use.tejido_kevlar_plomado");
    public static final RegistryObject<Item> CELDA_LITIO_MILITAR = register("celda_litio_militar", 64, Rarity.COMMON, "tooltip.component", "use.celda_litio_militar");
    public static final RegistryObject<Item> NUCLEO_PLOMO_SELLADO = register("nucleo_plomo_sellado", 64, Rarity.COMMON, "tooltip.component", "use.nucleo_plomo_sellado");
    public static final RegistryObject<Item> MOTOR_GRUA_SOVIETICA = register("motor_grua_sovietica", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> TALADRO_PERCUTOR_MINA = register("taladro_percutor_mina", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> COMPRESOR_AIRE_FABRICA = register("compresor_aire_fabrica", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> BOMBA_HIDRAULICA_REFRIGERACION = register("bomba_hidraulica_refrigeracion", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> SOLDADORA_ARCO_PORTATIL = register("soldadora_arco_portatil", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> CAJA_ENGRANAJES_TRACTOR = register("caja_engranajes_tractor", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> TRAJE_HAZMAT_LIQUIDADOR = register("traje_hazmat_liquidador", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> CONTADOR_GEIGER_PRIPYAT = register("contador_geiger_pripyat", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> RESPIRADOR_PAPR = register("respirador_papr", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> CENTRIFUGADORA_MUESTRAS = register("centrifugadora_muestras", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> CONTENEDOR_ISOTOPOS = register("contenedor_isotopos", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> ROCIADOR_DESCONTAMINACION = register("rociador_descontaminacion", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> BATERIA_TANQUE_T72 = register("bateria_tanque_t72", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> VISOR_NOCTURNO_PNV57 = register("visor_nocturno_pnv57", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> CHALECO_BALISTICO_6B3 = register("chaleco_balistico_6b3", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> RADIO_CAMPANA_R159 = register("radio_campana_r159", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> MODULO_PUNTERIA_BTR = register("modulo_punteria_btr", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> DRON_RECONOCIMIENTO = register("dron_reconocimiento", 16, Rarity.RARE, "tooltip.compound");
    public static final RegistryObject<Item> DESFIBRILADOR_PORTATIL = register("desfibrilador_portatil", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> MICROSCOPIO_QUIRURGICO = register("microscopio_quirurgico", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> VENTILADOR_PULMONAR_UCI = register("ventilador_pulmonar_uci", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> MONITOR_SIGNOS_VITALES = register("monitor_signos_vitales", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> AUTOCLAVE_ESTERILIZACION = register("autoclave_esterilizacion", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> CAMILLA_AISLAMIENTO = register("camilla_aislamiento", 16, Rarity.UNCOMMON, "tooltip.compound");
    public static final RegistryObject<Item> ABRIGO_AFGHANKA = register("abrigo_afghanka", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> MICROONDAS_DNEPR = register("microondas_dnepr", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> TELEVISOR_RUBIN = register("televisor_rubin", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> LAVADORA_VYATKA = register("lavadora_vyatka", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> MAQUINA_COSER_PODOLSK = register("maquina_coser_podolsk", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> ASPIRADORA_RAKETA = register("aspiradora_raketa", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> TRANSFORMADOR_SUBESTACION = register("transformador_subestacion", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> PANEL_CONTROL_REACTOR = register("panel_control_reactor", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> ALTERNADOR_GENERADOR_DIESEL = register("alternador_generador_diesel", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> ESTABILIZADOR_VOLTAJE = register("estabilizador_voltaje", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> BATERIA_UPS_SERVIDOR = register("bateria_ups_servidor", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> CAJA_DISYUNTORES_TRIFASICOS = register("caja_disyuntores_trifasicos", 16, Rarity.COMMON, "tooltip.compound");
    public static final RegistryObject<Item> VIGA_ACERO_RETORCIDA = register("viga_acero_retorcida", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CONTRAPESO_GRUA = register("contrapeso_grua", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CADENA_REMOLQUE = register("cadena_remolque", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> LAMINA_TECHO_CORRUGADA = register("lamina_techo_corrugada", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CAJA_CLAVOS_TUERCAS = register("caja_clavos_tuercas", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> GUANTES_SOLDADOR = register("guantes_soldador", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CASCO_MINERO = register("casco_minero", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> LADRILLO_BLINDAJE_PLOMO = register("ladrillo_blindaje_plomo", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> DELANTAL_LABORATORIO = register("delantal_laboratorio", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BIDON_ACIDO = register("bidon_acido", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BOTAS_GOMA_DESCONTAMINANTES = register("botas_goma_descontaminantes", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> LONA_CUARENTENA = register("lona_cuarentena", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> MASCARILLA_GP5 = register("mascarilla_gp5", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> GRADILLA_TUBOS_ENSAYO = register("gradilla_tubos_ensayo", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> PLACA_BALISTICA_ACERO = register("placa_balistica_acero", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> ESLABON_ORUGA_TANQUE = register("eslabon_oruga_tanque", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CAJA_MUNICION_50 = register("caja_municion_50", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CASCO_SSH68 = register("casco_ssh68", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CARGADOR_BAQUELITA_AK74 = register("cargador_baquelita_ak74", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> RED_CAMUFLAJE = register("red_camuflaje", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BOTAS_PARACAIDISTA = register("botas_paracaidista", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> ROLLO_VENDAS_YODO = register("rollo_vendas_yodo", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> SABANA_QUIRURGICA = register("sabana_quirurgica", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BATA_PACIENTE = register("bata_paciente", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BANDEJA_INSTRUMENTOS = register("bandeja_instrumentos", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> SOPORTE_SUERO = register("soporte_suero", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> BOLSA_DESECHOS_BIOLOGICOS = register("bolsa_desechos_biologicos", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> MULETA_ALUMINIO = register("muleta_aluminio", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> TAZA_PELTRE = register("taza_peltre", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> OLLA_PRESION = register("olla_presion", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> RADIADOR_HIERRO = register("radiador_hierro", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> GORRO_USHANKA = register("gorro_ushanka", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> VAQUEROS_RASGADOS = register("vaqueros_rasgados", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> ALFOMBRA_PERSA = register("alfombra_persa", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> MUNECA_IRRADIADA = register("muneca_irradiada", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CUBIERTOS_ACERO = register("cubiertos_acero", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CABLE_TELEFONICO = register("cable_telefonico", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> AISLADOR_CERAMICO = register("aislador_ceramico", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> FUSIBLE_PORCELANA = register("fusible_porcelana", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> CARCASA_ENCHUFE = register("carcasa_enchufe", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> TUBO_FLUORESCENTE = register("tubo_fluorescente", 64, Rarity.COMMON, "tooltip.simple");
    public static final RegistryObject<Item> PLACA_DISIPADORA_ALUMINIO = register("placa_disipadora_aluminio", 64, Rarity.COMMON, "tooltip.simple");

    private static RegistryObject<Item> register(String id, int maxStack, Rarity rarity, String... tooltipKeys) {
        return ITEMS.register(id, () -> new RecyclerItem(new Item.Properties().stacksTo(maxStack).rarity(rarity), tooltipKeys));
    }

    /** Todos los items, en el orden del documento de diseno. */
    public static final List<RegistryObject<Item>> ALL = List.of(
            TELA,
            SCRAP,
            LINGOTE_PESADO,
            ENGRANAJE_TITANIO,
            PISTON_HIDRAULICO,
            TUBO_PRESION,
            VALVULA_ANTIRRETORNO,
            BOBINA_COBRE,
            CABLEADO_ALTA_TENSION,
            PLACA_CIRCUITO_IMPRESO,
            CONDENSADOR_ALTO_VOLTAJE,
            MOTOR_PASO_A_PASO,
            MICROPROCESADOR_MILITAR,
            SENSOR_DOSIMETRICO,
            LENTE_OPTICA_PRECISION,
            FILTRO_CARBON_ACTIVADO,
            TEJIDO_KEVLAR_PLOMADO,
            CELDA_LITIO_MILITAR,
            NUCLEO_PLOMO_SELLADO,
            MOTOR_GRUA_SOVIETICA,
            TALADRO_PERCUTOR_MINA,
            COMPRESOR_AIRE_FABRICA,
            BOMBA_HIDRAULICA_REFRIGERACION,
            SOLDADORA_ARCO_PORTATIL,
            CAJA_ENGRANAJES_TRACTOR,
            TRAJE_HAZMAT_LIQUIDADOR,
            CONTADOR_GEIGER_PRIPYAT,
            RESPIRADOR_PAPR,
            CENTRIFUGADORA_MUESTRAS,
            CONTENEDOR_ISOTOPOS,
            ROCIADOR_DESCONTAMINACION,
            BATERIA_TANQUE_T72,
            VISOR_NOCTURNO_PNV57,
            CHALECO_BALISTICO_6B3,
            RADIO_CAMPANA_R159,
            MODULO_PUNTERIA_BTR,
            DRON_RECONOCIMIENTO,
            DESFIBRILADOR_PORTATIL,
            MICROSCOPIO_QUIRURGICO,
            VENTILADOR_PULMONAR_UCI,
            MONITOR_SIGNOS_VITALES,
            AUTOCLAVE_ESTERILIZACION,
            CAMILLA_AISLAMIENTO,
            ABRIGO_AFGHANKA,
            MICROONDAS_DNEPR,
            TELEVISOR_RUBIN,
            LAVADORA_VYATKA,
            MAQUINA_COSER_PODOLSK,
            ASPIRADORA_RAKETA,
            TRANSFORMADOR_SUBESTACION,
            PANEL_CONTROL_REACTOR,
            ALTERNADOR_GENERADOR_DIESEL,
            ESTABILIZADOR_VOLTAJE,
            BATERIA_UPS_SERVIDOR,
            CAJA_DISYUNTORES_TRIFASICOS,
            VIGA_ACERO_RETORCIDA,
            CONTRAPESO_GRUA,
            CADENA_REMOLQUE,
            LAMINA_TECHO_CORRUGADA,
            CAJA_CLAVOS_TUERCAS,
            GUANTES_SOLDADOR,
            CASCO_MINERO,
            LADRILLO_BLINDAJE_PLOMO,
            DELANTAL_LABORATORIO,
            BIDON_ACIDO,
            BOTAS_GOMA_DESCONTAMINANTES,
            LONA_CUARENTENA,
            MASCARILLA_GP5,
            GRADILLA_TUBOS_ENSAYO,
            PLACA_BALISTICA_ACERO,
            ESLABON_ORUGA_TANQUE,
            CAJA_MUNICION_50,
            CASCO_SSH68,
            CARGADOR_BAQUELITA_AK74,
            RED_CAMUFLAJE,
            BOTAS_PARACAIDISTA,
            ROLLO_VENDAS_YODO,
            SABANA_QUIRURGICA,
            BATA_PACIENTE,
            BANDEJA_INSTRUMENTOS,
            SOPORTE_SUERO,
            BOLSA_DESECHOS_BIOLOGICOS,
            MULETA_ALUMINIO,
            TAZA_PELTRE,
            OLLA_PRESION,
            RADIADOR_HIERRO,
            GORRO_USHANKA,
            VAQUEROS_RASGADOS,
            ALFOMBRA_PERSA,
            MUNECA_IRRADIADA,
            CUBIERTOS_ACERO,
            CABLE_TELEFONICO,
            AISLADOR_CERAMICO,
            FUSIBLE_PORCELANA,
            CARCASA_ENCHUFE,
            TUBO_FLUORESCENTE,
            PLACA_DISIPADORA_ALUMINIO
    );

    public static void register(IEventBus modBus) {
        ITEMS.register(modBus);
    }

    private ModItems() {
    }
}
