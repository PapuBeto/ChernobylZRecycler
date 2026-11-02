package com.chernobylz.recycler.recipe;

import com.chernobylz.recycler.registry.ModRecipes;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.NonNullList;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.Container;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;

/**
 * Receta de la recicladora.
 *
 * <p>Una misma receta cubre las dos fases del sistema:</p>
 * <ul>
 *   <li>Fase 1: objeto compuesto -> recursos base + componentes utiles.</li>
 *   <li>Fase 2: componente util -> recursos base (se define en el JSON con {@code "phase": 2}).</li>
 * </ul>
 */
public class RecyclingRecipe implements Recipe<Container> {

    private final ResourceLocation id;
    private final Ingredient ingredient;
    private final int processingTime;
    private final int phase;
    private final NonNullList<ItemStack> baseOutputs;
    private final NonNullList<ItemStack> componentOutputs;
    private final List<ItemStack> allOutputs;

    public RecyclingRecipe(ResourceLocation id, Ingredient ingredient, int processingTime, int phase,
                           NonNullList<ItemStack> baseOutputs, NonNullList<ItemStack> componentOutputs) {
        this.id = id;
        this.ingredient = ingredient;
        this.processingTime = Math.max(1, processingTime);
        this.phase = phase == 2 ? 2 : 1;
        this.baseOutputs = copyOf(baseOutputs);
        this.componentOutputs = copyOf(componentOutputs);

        List<ItemStack> outputs = new ArrayList<>(this.baseOutputs.size() + this.componentOutputs.size());
        outputs.addAll(this.baseOutputs);
        outputs.addAll(this.componentOutputs);
        this.allOutputs = List.copyOf(outputs);
    }

    private static NonNullList<ItemStack> copyOf(NonNullList<ItemStack> stacks) {
        NonNullList<ItemStack> copy = NonNullList.createWithCapacity(stacks.size());
        for (ItemStack stack : stacks) {
            if (!stack.isEmpty()) {
                copy.add(stack.copy());
            }
        }
        return copy;
    }

    @Override
    public boolean matches(Container container, Level level) {
        return this.ingredient.test(container.getItem(0));
    }

    @Override
    public ItemStack assemble(Container container, RegistryAccess registries) {
        return this.baseOutputs.isEmpty() ? ItemStack.EMPTY : this.baseOutputs.get(0).copy();
    }

    @Override
    public boolean canCraftInDimensions(int width, int height) {
        return true;
    }

    @Override
    public ItemStack getResultItem(RegistryAccess registries) {
        if (!this.baseOutputs.isEmpty()) {
            return this.baseOutputs.get(0).copy();
        }
        return this.componentOutputs.isEmpty() ? ItemStack.EMPTY : this.componentOutputs.get(0).copy();
    }

    @Override
    public NonNullList<Ingredient> getIngredients() {
        NonNullList<Ingredient> ingredients = NonNullList.create();
        ingredients.add(this.ingredient);
        return ingredients;
    }

    @Override
    public ResourceLocation getId() {
        return this.id;
    }

    @Override
    public RecipeSerializer<?> getSerializer() {
        return ModRecipes.RECYCLING_SERIALIZER.get();
    }

    @Override
    public RecipeType<?> getType() {
        return ModRecipes.RECYCLING_TYPE;
    }

    public Ingredient getIngredient() {
        return this.ingredient;
    }

    public int getProcessingTime() {
        return this.processingTime;
    }

    public int getPhase() {
        return this.phase;
    }

    public NonNullList<ItemStack> getBaseOutputs() {
        return this.baseOutputs;
    }

    public NonNullList<ItemStack> getComponentOutputs() {
        return this.componentOutputs;
    }

    /** Todos los stacks que entrega la receta, en orden (base primero, luego componentes). */
    public List<ItemStack> getAllOutputs() {
        return this.allOutputs;
    }
}
