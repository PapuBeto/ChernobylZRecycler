package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.menu.RecyclerMenu;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.inventory.MenuType;
import net.minecraftforge.common.extensions.IForgeMenuType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public final class ModMenus {

    public static final DeferredRegister<MenuType<?>> MENUS =
            DeferredRegister.create(Registries.MENU, ChernobylZRecycler.MODID);

    public static final RegistryObject<MenuType<RecyclerMenu>> RECYCLER = MENUS.register("recycler",
            () -> IForgeMenuType.create((windowId, inventory, data) -> new RecyclerMenu(windowId, inventory)));

    public static void register(IEventBus modBus) {
        MENUS.register(modBus);
    }

    private ModMenus() {
    }
}
