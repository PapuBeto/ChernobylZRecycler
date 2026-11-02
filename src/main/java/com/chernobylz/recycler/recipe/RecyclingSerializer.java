package com.chernobylz.recycler.recipe;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSyntaxException;
import net.minecraft.core.NonNullList;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraftforge.registries.ForgeRegistries;
import org.jetbrains.annotations.Nullable;

/**
 * (De)serializacion de {@link RecyclingRecipe}: JSON para datapacks y
 * {@link FriendlyByteBuf} para sincronizar las recetas al cliente.
 */
public class RecyclingSerializer implements RecipeSerializer<RecyclingRecipe> {

    @Override
    public RecyclingRecipe fromJson(ResourceLocation id, JsonObject json) {
        Ingredient ingredient = Ingredient.fromJson(GsonHelper.getAsJsonObject(json, "ingredient"));
        int processingTime = GsonHelper.getAsInt(json, "processing_time", 100);
        int phase = GsonHelper.getAsInt(json, "phase", 1);

        NonNullList<ItemStack> base = readStacks(json, "base");
        NonNullList<ItemStack> components = readStacks(json, "components");

        if (base.isEmpty() && components.isEmpty()) {
            throw new JsonSyntaxException("La receta " + id + " no define ninguna salida (base/components).");
        }
        return new RecyclingRecipe(id, ingredient, processingTime, phase, base, components);
    }

    private static NonNullList<ItemStack> readStacks(JsonObject json, String key) {
        NonNullList<ItemStack> stacks = NonNullList.create();
        if (!json.has(key)) {
            return stacks;
        }
        JsonArray array = GsonHelper.getAsJsonArray(json, key);
        for (JsonElement element : array) {
            if (!element.isJsonObject()) {
                throw new JsonSyntaxException("Se esperaba un objeto en '" + key + "': " + element);
            }
            JsonObject entry = element.getAsJsonObject();
            String itemId = GsonHelper.getAsString(entry, "item");
            ResourceLocation location = ResourceLocation.tryParse(itemId);
            if (location == null) {
                throw new JsonSyntaxException("Item id invalido: " + itemId);
            }
            Item item = ForgeRegistries.ITEMS.getValue(location);
            if (item == null) {
                throw new JsonSyntaxException("Item desconocido: " + itemId);
            }
            int count = GsonHelper.getAsInt(entry, "count", 1);
            if (count <= 0) {
                throw new JsonSyntaxException("Cantidad invalida para " + itemId + ": " + count);
            }
            stacks.add(new ItemStack(item, count));
        }
        return stacks;
    }

    @Override
    public void toNetwork(FriendlyByteBuf buf, RecyclingRecipe recipe) {
        recipe.getIngredient().toNetwork(buf);
        buf.writeVarInt(recipe.getProcessingTime());
        buf.writeVarInt(recipe.getPhase());
        writeStacks(buf, recipe.getBaseOutputs());
        writeStacks(buf, recipe.getComponentOutputs());
    }

    private static void writeStacks(FriendlyByteBuf buf, NonNullList<ItemStack> stacks) {
        buf.writeVarInt(stacks.size());
        for (ItemStack stack : stacks) {
            buf.writeItem(stack);
        }
    }

    @Override
    @Nullable
    public RecyclingRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buf) {
        Ingredient ingredient = Ingredient.fromNetwork(buf);
        int processingTime = buf.readVarInt();
        int phase = buf.readVarInt();
        NonNullList<ItemStack> base = readStacks(buf);
        NonNullList<ItemStack> components = readStacks(buf);
        return new RecyclingRecipe(id, ingredient, processingTime, phase, base, components);
    }

    private static NonNullList<ItemStack> readStacks(FriendlyByteBuf buf) {
        int size = buf.readVarInt();
        NonNullList<ItemStack> stacks = NonNullList.createWithCapacity(size);
        for (int i = 0; i < size; i++) {
            stacks.add(buf.readItem());
        }
        return stacks;
    }
}
