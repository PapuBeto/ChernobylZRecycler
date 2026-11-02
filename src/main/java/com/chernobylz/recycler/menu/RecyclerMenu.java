package com.chernobylz.recycler.menu;

import com.chernobylz.recycler.block.RecyclerBlockEntity;
import com.chernobylz.recycler.registry.ModMenus;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

/**
 * GUI de la recicladora: 5 slots de entrada + 5 slots de salida (estilo
 * Rust) + inventario del jugador.
 */
public class RecyclerMenu extends AbstractContainerMenu {

    private static final int PLAYER_INVENTORY_START = RecyclerBlockEntity.TOTAL_SLOTS;
    private static final int PLAYER_INVENTORY_END = PLAYER_INVENTORY_START + 36;

    private final Container container;
    private final ContainerData data;

    /** Constructor del servidor: usa el BlockEntity como contenedor y como ContainerData. */
    public RecyclerMenu(int containerId, Inventory playerInventory, RecyclerBlockEntity blockEntity) {
        this(containerId, playerInventory, blockEntity, blockEntity);
    }

    /** Constructor del cliente: contenedor y datos vacios que se rellenan por paquetes. */
    public RecyclerMenu(int containerId, Inventory playerInventory) {
        this(containerId, playerInventory,
                new SimpleContainer(RecyclerBlockEntity.TOTAL_SLOTS) {
                    @Override
                    public boolean canPlaceItem(int slot, ItemStack stack) {
                        // Prediccion cliente: leniente; la receta la valida el servidor.
                        return slot < RecyclerBlockEntity.INPUT_SLOTS;
                    }
                },
                new SimpleContainerData(2));
    }

    private RecyclerMenu(int containerId, Inventory playerInventory, Container container, ContainerData data) {
        super(ModMenus.RECYCLER.get(), containerId);
        checkContainerSize(container, RecyclerBlockEntity.TOTAL_SLOTS);
        checkContainerDataCount(data, 2);

        this.container = container;
        this.data = data;
        container.startOpen(playerInventory.player);

        // Entrada: fila de 5 slots centrada (items 44, 62, 80, 98, 116 / y 24)
        for (int i = 0; i < RecyclerBlockEntity.INPUT_SLOTS; i++) {
            final int index = i;
            this.addSlot(new Slot(container, index, 44 + i * 18, 24) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return container.canPlaceItem(index, stack);
                }
            });
        }

        // Salida: fila de 5 slots centrada (y 60)
        for (int i = 0; i < RecyclerBlockEntity.OUTPUT_SLOTS; i++) {
            this.addSlot(new Slot(container, RecyclerBlockEntity.OUTPUT_START + i,
                    44 + i * 18, 60) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return false;
                }
            });
        }

        // Inventario del jugador
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, 89 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 147));
        }

        this.addDataSlots(data);
    }

    public int getProgress() {
        return this.data.get(0);
    }

    public int getMaxProgress() {
        return Math.max(1, this.data.get(1));
    }

    public int getScaledProgress(int pixels) {
        int current = this.getProgress();
        int max = this.getMaxProgress();
        return max <= 0 ? 0 : Math.min(pixels, current * pixels / max);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = this.slots.get(index);
        if (!slot.hasItem()) {
            return ItemStack.EMPTY;
        }

        ItemStack stack = slot.getItem();
        ItemStack copy = stack.copy();

        if (index < PLAYER_INVENTORY_START) {
            // Recicladora -> inventario del jugador
            if (!this.moveItemStackTo(stack, PLAYER_INVENTORY_START, PLAYER_INVENTORY_END, true)) {
                return ItemStack.EMPTY;
            }
        } else {
            // Inventario del jugador -> entrada de la recicladora (5 slots)
            if (!this.moveItemStackTo(stack, 0, RecyclerBlockEntity.INPUT_SLOTS, false)) {
                return ItemStack.EMPTY;
            }
        }

        if (stack.isEmpty()) {
            slot.setByPlayer(ItemStack.EMPTY);
        } else {
            slot.setChanged();
        }

        if (stack.getCount() == copy.getCount()) {
            return ItemStack.EMPTY;
        }

        slot.onTake(player, stack);
        return copy;
    }

    @Override
    public boolean stillValid(Player player) {
        return this.container.stillValid(player);
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        this.container.stopOpen(player);
    }
}
