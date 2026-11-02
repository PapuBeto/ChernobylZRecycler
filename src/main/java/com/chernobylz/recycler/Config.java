package com.chernobylz.recycler;

import net.minecraftforge.common.ForgeConfigSpec;

/**
 * Configuracion del servidor ({@code config/chernobylz_recycler-common.toml}).
 */
public final class Config {

    private static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();

    private static final ForgeConfigSpec.BooleanValue ALLOW_PHASE_TWO = BUILDER
            .comment("Permite reciclar Componentes Utiles (Fase 2).")
            .comment("Si se desactiva, los componentes solo sirven para craftear.")
            .define("allowPhaseTwo", true);

    private static final ForgeConfigSpec.DoubleValue PROCESSING_SPEED = BUILDER
            .comment("Multiplicador de velocidad de la recicladora.")
            .comment("1.0 usa los tiempos definidos en las recetas; 2.0 tarda la mitad.")
            .defineInRange("processingSpeedMultiplier", 1.0D, 0.05D, 50.0D);

    private static final ForgeConfigSpec.BooleanValue ENABLE_LOOT_MODIFIERS = BUILDER
            .comment("Activa los loot modifiers del mod (basura en zombis y objetos en cofres).")
            .define("enableLootModifiers", true);

    static final ForgeConfigSpec SPEC = BUILDER.build();

    public static boolean allowPhaseTwo() {
        return ALLOW_PHASE_TWO.get();
    }

    public static double processingSpeed() {
        return PROCESSING_SPEED.get();
    }

    public static boolean enableLootModifiers() {
        return ENABLE_LOOT_MODIFIERS.get();
    }

    private Config() {
    }
}
