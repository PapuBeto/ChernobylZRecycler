package com.chernobylz.recycler.util;

import com.chernobylz.recycler.ChernobylZRecycler;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.stream.Collectors;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;

/**
 * Zonas de riesgo del mapa. Cada zona tiene un tag de items propio
 * ({@code chernobylz_recycler:zone/<id>}) que se usa para el loot y para el
 * comando de administracion.
 */
public enum Zone {

    INDUSTRIAL("industrial"),
    CHEMICAL("chemical"),
    MILITARY("military"),
    HOSPITAL("hospital"),
    RESIDENTIAL("residential"),
    ELECTRICAL("electrical");

    private final String id;
    private final TagKey<Item> tag;

    Zone(String id) {
        this.id = id;
        this.tag = TagKey.create(Registries.ITEM, new ResourceLocation(ChernobylZRecycler.MODID, "zone/" + id));
    }

    public String id() {
        return id;
    }

    public TagKey<Item> tag() {
        return tag;
    }

    public Component displayName() {
        return Component.translatable("zone." + ChernobylZRecycler.MODID + "." + id);
    }

    public static Optional<Zone> byId(String id) {
        String normalized = id == null ? "" : id.toLowerCase(Locale.ROOT);
        return Arrays.stream(values()).filter(zone -> zone.id.equals(normalized)).findFirst();
    }

    public static List<String> ids() {
        return Arrays.stream(values()).map(Zone::id).collect(Collectors.toList());
    }
}
