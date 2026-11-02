package com.chernobylz.recycler.item;

import com.chernobylz.recycler.ChernobylZRecycler;
import java.util.Arrays;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Item del mod. Solo anade lineas de tooltip segun su rol en la economia:
 * recurso base, componente (Fase 2), objeto compuesto o basura (Fase 1).
 */
public class RecyclerItem extends Item {

    private static final String LANG = "item." + ChernobylZRecycler.MODID + ".";

    private final String categoryKey;
    private final String[] extraKeys;

    public RecyclerItem(Properties properties, String... tooltipKeys) {
        super(properties);
        this.categoryKey = tooltipKeys.length > 0 ? tooltipKeys[0] : "tooltip.simple";
        this.extraKeys = tooltipKeys.length > 1
                ? Arrays.copyOfRange(tooltipKeys, 1, tooltipKeys.length)
                : new String[0];
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(LANG + categoryKey).withStyle(ChatFormatting.GRAY));
        for (String key : extraKeys) {
            tooltip.add(Component.translatable(LANG + key).withStyle(ChatFormatting.DARK_GRAY));
        }
    }
}
