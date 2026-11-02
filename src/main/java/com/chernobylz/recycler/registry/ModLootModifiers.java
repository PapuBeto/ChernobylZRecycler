package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.loot.InjectTagItemsModifier;
import com.mojang.serialization.Codec;
import net.minecraftforge.common.loot.IGlobalLootModifier;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModLootModifiers {

    public static final DeferredRegister<Codec<? extends IGlobalLootModifier>> SERIALIZERS =
            DeferredRegister.create(ForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, ChernobylZRecycler.MODID);

    public static final RegistryObject<Codec<? extends IGlobalLootModifier>> INJECT_TAG_ITEMS =
            SERIALIZERS.register("inject_tag_items", () -> InjectTagItemsModifier.CODEC);

    public static void register(IEventBus modBus) {
        SERIALIZERS.register(modBus);
    }

    private ModLootModifiers() {
    }
}
