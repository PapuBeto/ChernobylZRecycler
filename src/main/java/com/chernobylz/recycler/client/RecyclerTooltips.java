package com.chernobylz.recycler.client;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.Config;
import com.chernobylz.recycler.recipe.RecyclingRecipe;
import com.chernobylz.recycler.registry.ModRecipes;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Muestra en el tooltip exactamente lo que entrega la receta de reciclaje.
 * Asi el jugador no necesita JEI para entender la economia.
 */
@Mod.EventBusSubscriber(modid = ChernobylZRecycler.MODID, value = Dist.CLIENT)
public final class RecyclerTooltips {

    private static final String LANG = "item." + ChernobylZRecycler.MODID + ".tooltip.";

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {
        if (event.getEntity() == null) {
            return;
        }
        Level level = Minecraft.getInstance().level;
        if (level == null) {
            return;
        }

        ItemStack stack = event.getItemStack();
        RecyclingRecipe recipe = level.getRecipeManager()
                .getRecipeFor(ModRecipes.RECYCLING_TYPE, new SimpleContainer(stack.copy()), level)
                .orElse(null);
        if (recipe == null) {
            return;
        }
        if (recipe.getPhase() == 2 && !Config.allowPhaseTwo()) {
            return;
        }

        List<Component> tooltip = event.getToolTip();

        if (!recipe.getBaseOutputs().isEmpty()) {
            String key = recipe.getPhase() == 2 ? "phase2" : "phase1";
            tooltip.add(Component.translatable(LANG + key, listing(recipe.getBaseOutputs()))
                    .withStyle(ChatFormatting.GRAY));
        }

        if (!recipe.getComponentOutputs().isEmpty()) {
            tooltip.add(Component.translatable(LANG + "components", listing(recipe.getComponentOutputs()))
                    .withStyle(ChatFormatting.DARK_AQUA));
        }
    }

    private static MutableComponent listing(List<ItemStack> stacks) {
        MutableComponent result = Component.empty();
        for (int i = 0; i < stacks.size(); i++) {
            if (i > 0) {
                result.append(Component.literal(", "));
            }
            ItemStack stack = stacks.get(i);
            result.append(Component.translatable("item." + ChernobylZRecycler.MODID + ".tooltip.entry",
                    stack.getCount(), stack.getHoverName()));
        }
        return result;
    }

    private RecyclerTooltips() {
    }
}
