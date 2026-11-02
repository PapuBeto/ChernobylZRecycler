package com.chernobylz.recycler.command;

import com.chernobylz.recycler.util.Zone;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import com.mojang.brigadier.suggestion.SuggestionProvider;
import java.util.Collection;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.tags.ITag;
import net.minecraftforge.registries.tags.ITagManager;

/**
 * Comando de administracion para entregar loot de una zona (eventos, crates, pruebas).
 *
 * <pre>
 * /czrecycler loot &lt;jugadores&gt; &lt;zona&gt; [cantidad]
 * /czrecycler zones
 * </pre>
 */
public final class CzRecyclerCommand {

    private static final SuggestionProvider<CommandSourceStack> ZONE_SUGGESTIONS =
            (context, builder) -> SharedSuggestionProvider.suggest(Zone.ids(), builder);

    public static void register(RegisterCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();

        dispatcher.register(Commands.literal("czrecycler")
                .requires(source -> source.hasPermission(2))
                .then(Commands.literal("loot")
                        .then(Commands.argument("targets", EntityArgument.players())
                                .then(Commands.argument("zone", StringArgumentType.word())
                                        .suggests(ZONE_SUGGESTIONS)
                                        .executes(context -> giveLoot(context, 1))
                                        .then(Commands.argument("count", IntegerArgumentType.integer(1, 64))
                                                .executes(context -> giveLoot(context, IntegerArgumentType.getInteger(context, "count")))))))
                .then(Commands.literal("zones")
                        .executes(CzRecyclerCommand::listZones)));
    }

    private static int giveLoot(CommandContext<CommandSourceStack> context, int count) throws CommandSyntaxException {
        CommandSourceStack source = context.getSource();
        String zoneId = StringArgumentType.getString(context, "zone");
        Zone zone = Zone.byId(zoneId).orElse(null);
        if (zone == null) {
            source.sendFailure(Component.translatable("commands.chernobylz_recycler.unknown_zone", zoneId));
            return 0;
        }

        ITagManager<Item> tagManager = ForgeRegistries.ITEMS.tags();
        ITag<Item> tag = tagManager == null ? null : tagManager.getTag(zone.tag());
        if (tag == null || tag.isEmpty()) {
            source.sendFailure(Component.translatable("commands.chernobylz_recycler.loot.empty", zone.id()));
            return 0;
        }

        Collection<ServerPlayer> players = EntityArgument.getPlayers(context, "targets");
        RandomSource random = source.getLevel().getRandom();

        for (ServerPlayer player : players) {
            for (int i = 0; i < count; i++) {
                tag.getRandomElement(random).ifPresent(item -> {
                    ItemStack stack = new ItemStack(item);
                    if (!player.getInventory().add(stack)) {
                        player.drop(stack, false);
                    }
                });
            }
        }

        int total = count * players.size();
        source.sendSuccess(() -> Component.translatable("commands.chernobylz_recycler.loot.success",
                total, zone.displayName(), players.size()), true);
        return total;
    }

    private static int listZones(CommandContext<CommandSourceStack> context) {
        CommandSourceStack source = context.getSource();
        ITagManager<Item> tagManager = ForgeRegistries.ITEMS.tags();
        source.sendSuccess(() -> Component.translatable("commands.chernobylz_recycler.zones.header", Zone.ids().size()), false);
        for (Zone zone : Zone.values()) {
            int size = tagManager == null ? 0 : tagManager.getTag(zone.tag()).size();
            source.sendSuccess(() -> Component.translatable("commands.chernobylz_recycler.zones.entry",
                    zone.displayName(), size), false);
        }
        return 1;
    }

    private CzRecyclerCommand() {
    }
}
