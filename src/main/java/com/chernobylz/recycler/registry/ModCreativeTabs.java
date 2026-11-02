package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public final class ModCreativeTabs {

    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ChernobylZRecycler.MODID);

    public static final RegistryObject<CreativeModeTab> RECYCLING = TABS.register("recycling",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup." + ChernobylZRecycler.MODID))
                    .icon(() -> new ItemStack(ModBlocks.RECYCLER_ITEM.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(ModBlocks.RECYCLER_ITEM.get());
                        ModItems.ALL.forEach(item -> output.accept(item.get()));
                    })
                    .build());

    public static void register(IEventBus modBus) {
        TABS.register(modBus);
    }

    private ModCreativeTabs() {
    }
}
