package com.chernobylz.recycler.loot;

import com.chernobylz.recycler.Config;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.Optional;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraftforge.common.loot.IGlobalLootModifier;
import net.minecraftforge.common.loot.LootModifier;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.tags.ITag;
import net.minecraftforge.registries.tags.ITagManager;
import org.jetbrains.annotations.NotNull;

/**
 * Loot modifier: agrega 1..N items aleatorios de un tag a una tabla de loot.
 *
 * <p>Ejemplo de JSON:</p>
 * <pre>{@code
 * {
 *   "type": "chernobylz_recycler:inject_tag_items",
 *   "conditions": [{"condition": "forge:loot_table_id", "loot_table_id": "minecraft:entities/zombie"}],
 *   "tag": "chernobylz_recycler:junk",
 *   "chance": 0.35,
 *   "min": 1,
 *   "max": 2
 * }
 * }</pre>
 */
public class InjectTagItemsModifier extends LootModifier {

    public static final Codec<InjectTagItemsModifier> CODEC = RecordCodecBuilder.create(instance ->
            codecStart(instance)
                    .and(TagKey.codec(Registries.ITEM).fieldOf("tag").forGetter(modifier -> modifier.tag))
                    .and(Codec.floatRange(0.0F, 1.0F).fieldOf("chance").orElse(1.0F).forGetter(modifier -> modifier.chance))
                    .and(Codec.intRange(0, 64).fieldOf("min").orElse(1).forGetter(modifier -> modifier.min))
                    .and(Codec.intRange(0, 64).fieldOf("max").orElse(1).forGetter(modifier -> modifier.max))
                    .apply(instance, InjectTagItemsModifier::new));

    private final TagKey<Item> tag;
    private final float chance;
    private final int min;
    private final int max;

    public InjectTagItemsModifier(LootItemCondition[] conditions, TagKey<Item> tag, float chance, int min, int max) {
        super(conditions);
        this.tag = tag;
        this.chance = chance;
        this.min = Math.max(0, min);
        this.max = Math.max(this.min, max);
    }

    @Override
    public Codec<? extends IGlobalLootModifier> codec() {
        return CODEC;
    }

    @Override
    @NotNull
    protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> generatedLoot, LootContext context) {
        if (!Config.enableLootModifiers() || this.chance <= 0.0F || context.getRandom().nextFloat() >= this.chance) {
            return generatedLoot;
        }

        ITagManager<Item> tagManager = ForgeRegistries.ITEMS.tags();
        if (tagManager == null) {
            return generatedLoot;
        }
        ITag<Item> items = tagManager.getTag(this.tag);
        if (items.isEmpty()) {
            return generatedLoot;
        }

        int rolls = this.min + (this.max > this.min ? context.getRandom().nextInt(this.max - this.min + 1) : 0);
        for (int i = 0; i < rolls; i++) {
            Optional<Item> picked = items.getRandomElement(context.getRandom());
            picked.ifPresent(item -> generatedLoot.add(new ItemStack(item)));
        }
        return generatedLoot;
    }
}
