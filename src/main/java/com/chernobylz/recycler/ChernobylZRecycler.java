package com.chernobylz.recycler;

import com.chernobylz.recycler.command.CzRecyclerCommand;
import com.chernobylz.recycler.registry.ModBlockEntities;
import com.chernobylz.recycler.registry.ModBlocks;
import com.chernobylz.recycler.registry.ModCreativeTabs;
import com.chernobylz.recycler.registry.ModItems;
import com.chernobylz.recycler.registry.ModLootModifiers;
import com.chernobylz.recycler.registry.ModMenus;
import com.chernobylz.recycler.registry.ModRecipes;
import com.mojang.logging.LogUtils;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;

/**
 * Punto de entrada del mod de reciclaje de Chernobyl Z.
 *
 * <p>El mod es 100% compatible con servidor dedicado: la logica de reciclaje,
 * las recetas y el loot viven en el servidor. El cliente solo necesita el jar
 * para dibujar el GUI de la recicladora y los tooltips.</p>
 */
@Mod(ChernobylZRecycler.MODID)
public final class ChernobylZRecycler {

    public static final String MODID = "chernobylz_recycler";
    public static final Logger LOGGER = LogUtils.getLogger();

    public ChernobylZRecycler(FMLJavaModLoadingContext context) {
        IEventBus modBus = context.getModEventBus();

        ModBlocks.register(modBus);
        ModItems.register(modBus);
        ModBlockEntities.register(modBus);
        ModMenus.register(modBus);
        ModRecipes.register(modBus);
        ModLootModifiers.register(modBus);
        ModCreativeTabs.register(modBus);

        context.registerConfig(ModConfig.Type.COMMON, Config.SPEC);

        MinecraftForge.EVENT_BUS.addListener(CzRecyclerCommand::register);

        LOGGER.info("Chernobyl Z: Reciclaje inicializado.");
    }
}
