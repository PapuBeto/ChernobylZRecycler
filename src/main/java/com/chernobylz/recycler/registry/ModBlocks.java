package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.block.RecyclerBlock;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModBlocks {

    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(ForgeRegistries.BLOCKS, ChernobylZRecycler.MODID);

    /** Registro separado para los BlockItem, para no depender del orden de inicializacion. */
    public static final DeferredRegister<Item> BLOCK_ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, ChernobylZRecycler.MODID);

    public static final RegistryObject<Block> RECYCLER = BLOCKS.register("recycler",
            () -> new RecyclerBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.METAL)
                    .sound(SoundType.METAL)
                    .strength(4.0F, 8.0F)
                    .requiresCorrectToolForDrops()));

    public static final RegistryObject<Item> RECYCLER_ITEM = BLOCK_ITEMS.register("recycler",
            () -> new BlockItem(RECYCLER.get(), new Item.Properties()));

    public static void register(IEventBus modBus) {
        BLOCKS.register(modBus);
        BLOCK_ITEMS.register(modBus);
    }

    private ModBlocks() {
    }
}
