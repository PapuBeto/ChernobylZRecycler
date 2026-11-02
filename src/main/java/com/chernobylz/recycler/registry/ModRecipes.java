package com.chernobylz.recycler.registry;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.recipe.RecyclingRecipe;
import com.chernobylz.recycler.recipe.RecyclingSerializer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModRecipes {

    public static final DeferredRegister<RecipeSerializer<?>> SERIALIZERS =
            DeferredRegister.create(ForgeRegistries.RECIPE_SERIALIZERS, ChernobylZRecycler.MODID);

    public static final RegistryObject<RecipeSerializer<?>> RECYCLING_SERIALIZER =
            SERIALIZERS.register("recycling", RecyclingSerializer::new);

    /**
     * Tipo de receta propio. Forge expone {@link RecipeType#simple(ResourceLocation)}
     * justamente para mods que no necesitan una entrada extra en el registro.
     */
    public static final RecipeType<RecyclingRecipe> RECYCLING_TYPE =
            RecipeType.simple(new ResourceLocation(ChernobylZRecycler.MODID, "recycling"));

    public static void register(IEventBus modBus) {
        SERIALIZERS.register(modBus);
    }

    private ModRecipes() {
    }
}
