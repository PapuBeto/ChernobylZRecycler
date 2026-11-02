package com.chernobylz.recycler.block;

import com.chernobylz.recycler.Config;
import com.chernobylz.recycler.menu.RecyclerMenu;
import com.chernobylz.recycler.recipe.RecyclingRecipe;
import com.chernobylz.recycler.registry.ModBlockEntities;
import com.chernobylz.recycler.registry.ModRecipes;
import java.util.List;
import javax.annotation.Nullable;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Container;
import net.minecraft.world.Containers;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.common.capabilities.Capability;
import net.minecraftforge.common.capabilities.ForgeCapabilities;
import net.minecraftforge.common.util.LazyOptional;
import net.minecraftforge.items.IItemHandler;
import net.minecraftforge.items.ItemStackHandler;
import org.jetbrains.annotations.NotNull;

/**
 * Logica de la recicladora.
 *
 * <p>Estructura de inventario: slots 0..4 = entrada (cola estilo Rust), slots
 * 5..9 = salida.</p>
 *
 * <p>Es un {@link Container} para que el GUI pueda usar {@code Slot} directamente,
 * y expone un {@link IItemHandler} para tolvas: solo se puede insertar en la
 * entrada y extraer de la salida.</p>
 */
public class RecyclerBlockEntity extends BlockEntity implements MenuProvider, Container, ContainerData {

    public static final int INPUT_SLOTS = 5;
    public static final int OUTPUT_START = INPUT_SLOTS;
    public static final int OUTPUT_SLOTS = 5;
    public static final int TOTAL_SLOTS = INPUT_SLOTS + OUTPUT_SLOTS;

    private static final int RECIPE_CACHE_TICKS = 20;

    private final ItemStackHandler inventory = new ItemStackHandler(TOTAL_SLOTS) {
        @Override
        protected void onContentsChanged(int slot) {
            RecyclerBlockEntity.this.setChanged();
        }

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            return RecyclerBlockEntity.this.canPlaceItem(slot, stack);
        }
    };

    private final IItemHandler automationHandler = new IItemHandler() {
        @Override
        public int getSlots() {
            return TOTAL_SLOTS;
        }

        @Override
        @NotNull
        public ItemStack getStackInSlot(int slot) {
            return inventory.getStackInSlot(slot);
        }

        @Override
        @NotNull
        public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
            if (slot >= OUTPUT_START) {
                return stack;
            }
            return inventory.insertItem(slot, stack, simulate);
        }

        @Override
        @NotNull
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            if (slot < OUTPUT_START) {
                return ItemStack.EMPTY;
            }
            return inventory.extractItem(slot, amount, simulate);
        }

        @Override
        public int getSlotLimit(int slot) {
            return 64;
        }

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            return slot < INPUT_SLOTS && RecyclerBlockEntity.this.canPlaceItem(slot, stack);
        }
    };

    private final LazyOptional<IItemHandler> automationLazy = LazyOptional.of(() -> this.automationHandler);

    private int progress;
    private int maxProgress = 100;
    private int recipeCacheTicks;

    @Nullable
    private RecyclingRecipe cachedRecipe;
    private ItemStack cachedInput = ItemStack.EMPTY;
    @Nullable
    private Item lastInputItem;

    public RecyclerBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.RECYCLER.get(), pos, state);
    }

    // ------------------------------------------------------------------
    // Tick
    // ------------------------------------------------------------------

    public void tick() {
        if (this.level == null || this.level.isClientSide) {
            return;
        }

        if (this.recipeCacheTicks > 0) {
            this.recipeCacheTicks--;
        }

        // Primera entrada con receta valida: la cola se procesa en orden (estilo Rust).
        int targetSlot = -1;
        RecyclingRecipe recipe = null;
        for (int i = 0; i < INPUT_SLOTS; i++) {
            ItemStack stack = this.inventory.getStackInSlot(i);
            if (stack.isEmpty()) {
                continue;
            }
            RecyclingRecipe candidate = this.findRecipe(stack);
            if (candidate == null || (candidate.getPhase() == 2 && !Config.allowPhaseTwo())) {
                continue;
            }
            targetSlot = i;
            recipe = candidate;
            break;
        }
        if (targetSlot < 0 || recipe == null) {
            this.lastInputItem = null;
            this.resetProgress();
            return;
        }

        ItemStack input = this.inventory.getStackInSlot(targetSlot);
        if (input.getItem() != this.lastInputItem) {
            this.lastInputItem = input.getItem();
            this.progress = 0;
        }

        double speed = Math.max(0.05D, Config.processingSpeed());
        this.maxProgress = Math.max(1, (int) Math.round(recipe.getProcessingTime() / speed));

        if (!this.canFitOutputs(recipe)) {
            return;
        }

        this.progress++;
        if (this.progress >= this.maxProgress) {
            this.produce(recipe, targetSlot);
            this.progress = 0;
        }
        this.setChanged();
    }

    private void resetProgress() {
        if (this.progress != 0) {
            this.progress = 0;
            this.setChanged();
        }
    }

    /**
     * Busca la receta del stack de entrada. El resultado se cachea unos segundos
     * para no recorrer el RecipeManager en cada tick.
     */
    @Nullable
    public RecyclingRecipe findRecipe(ItemStack stack) {
        if (this.level == null || stack.isEmpty()) {
            return null;
        }
        if (this.cachedRecipe != null && this.recipeCacheTicks > 0
                && stack.getItem() == this.cachedInput.getItem()) {
            return this.cachedRecipe;
        }

        SimpleContainer container = new SimpleContainer(stack.copy());
        this.cachedRecipe = this.level.getRecipeManager()
                .getRecipeFor(ModRecipes.RECYCLING_TYPE, container, this.level)
                .orElse(null);
        this.cachedInput = stack.copy();
        this.recipeCacheTicks = RECIPE_CACHE_TICKS;
        return this.cachedRecipe;
    }

    private boolean canFitOutputs(RecyclingRecipe recipe) {
        ItemStack[] slots = new ItemStack[OUTPUT_SLOTS];
        for (int i = 0; i < OUTPUT_SLOTS; i++) {
            slots[i] = this.inventory.getStackInSlot(OUTPUT_START + i).copy();
        }
        for (ItemStack output : recipe.getAllOutputs()) {
            if (!simulateInsert(slots, output.copy())) {
                return false;
            }
        }
        return true;
    }

    private static boolean simulateInsert(ItemStack[] slots, ItemStack stack) {
        int remaining = stack.getCount();

        for (int i = 0; i < slots.length && remaining > 0; i++) {
            ItemStack slot = slots[i];
            if (slot.isEmpty() || !ItemStack.isSameItemSameTags(slot, stack)) {
                continue;
            }
            int limit = Math.min(slot.getMaxStackSize(), stack.getMaxStackSize());
            int room = limit - slot.getCount();
            if (room <= 0) {
                continue;
            }
            int moved = Math.min(room, remaining);
            slot.grow(moved);
            remaining -= moved;
        }

        for (int i = 0; i < slots.length && remaining > 0; i++) {
            if (!slots[i].isEmpty()) {
                continue;
            }
            ItemStack placed = stack.copy();
            int moved = Math.min(remaining, placed.getMaxStackSize());
            placed.setCount(moved);
            slots[i] = placed;
            remaining -= moved;
        }

        return remaining <= 0;
    }

    private void produce(RecyclingRecipe recipe, int targetSlot) {
        ItemStack input = this.inventory.getStackInSlot(targetSlot).copy();
        input.shrink(1);
        this.inventory.setStackInSlot(targetSlot, input.isEmpty() ? ItemStack.EMPTY : input);

        List<ItemStack> outputs = recipe.getAllOutputs();
        for (ItemStack output : outputs) {
            this.insertIntoOutputs(output.copy());
        }

        if (this.level != null) {
            this.level.playSound(null, this.worldPosition, SoundEvents.GRINDSTONE_USE, SoundSource.BLOCKS,
                    0.6F, 0.9F + this.level.random.nextFloat() * 0.2F);
        }
        this.setChanged();
    }

    private void insertIntoOutputs(ItemStack stack) {
        for (int i = OUTPUT_START; i < OUTPUT_START + OUTPUT_SLOTS && !stack.isEmpty(); i++) {
            ItemStack existing = this.inventory.getStackInSlot(i);
            if (existing.isEmpty() || !ItemStack.isSameItemSameTags(existing, stack)) {
                continue;
            }
            int limit = Math.min(existing.getMaxStackSize(), stack.getMaxStackSize());
            int room = limit - existing.getCount();
            if (room <= 0) {
                continue;
            }
            int moved = Math.min(room, stack.getCount());
            existing.grow(moved);
            stack.shrink(moved);
            this.inventory.setStackInSlot(i, existing);
        }

        for (int i = OUTPUT_START; i < OUTPUT_START + OUTPUT_SLOTS && !stack.isEmpty(); i++) {
            if (this.inventory.getStackInSlot(i).isEmpty()) {
                this.inventory.setStackInSlot(i, stack.copy());
                stack.setCount(0);
            }
        }

        if (!stack.isEmpty() && this.level != null) {
            Containers.dropItemStack(this.level, this.worldPosition.getX() + 0.5D,
                    this.worldPosition.getY() + 1.0D, this.worldPosition.getZ() + 0.5D, stack);
        }
    }

    public void dropContents(Level level, BlockPos pos) {
        for (int i = 0; i < TOTAL_SLOTS; i++) {
            ItemStack stack = this.inventory.getStackInSlot(i);
            if (!stack.isEmpty()) {
                Containers.dropItemStack(level, pos.getX() + 0.5D, pos.getY() + 0.5D, pos.getZ() + 0.5D, stack.copy());
            }
        }
        this.clearContent();
    }

    // ------------------------------------------------------------------
    // Persistencia
    // ------------------------------------------------------------------

    @Override
    protected void saveAdditional(CompoundTag tag) {
        super.saveAdditional(tag);
        tag.put("Inventory", this.inventory.serializeNBT());
        tag.putInt("Progress", this.progress);
    }

    @Override
    public void load(CompoundTag tag) {
        super.load(tag);
        if (tag.contains("Inventory")) {
            this.inventory.deserializeNBT(tag.getCompound("Inventory"));
        }
        this.progress = tag.getInt("Progress");
    }

    // ------------------------------------------------------------------
    // Container (para los slots del GUI)
    // ------------------------------------------------------------------

    @Override
    public int getContainerSize() {
        return TOTAL_SLOTS;
    }

    @Override
    public boolean isEmpty() {
        for (int i = 0; i < TOTAL_SLOTS; i++) {
            if (!this.inventory.getStackInSlot(i).isEmpty()) {
                return false;
            }
        }
        return true;
    }

    @Override
    public ItemStack getItem(int slot) {
        return this.inventory.getStackInSlot(slot);
    }

    @Override
    public ItemStack removeItem(int slot, int amount) {
        return this.inventory.extractItem(slot, amount, false);
    }

    @Override
    public ItemStack removeItemNoUpdate(int slot) {
        ItemStack stack = this.inventory.getStackInSlot(slot);
        this.inventory.setStackInSlot(slot, ItemStack.EMPTY);
        return stack;
    }

    @Override
    public void setItem(int slot, ItemStack stack) {
        this.inventory.setStackInSlot(slot, stack);
    }

    @Override
    public boolean stillValid(Player player) {
        return Container.stillValidBlockEntity(this, player);
    }

    @Override
    public void clearContent() {
        for (int i = 0; i < TOTAL_SLOTS; i++) {
            this.inventory.setStackInSlot(i, ItemStack.EMPTY);
        }
    }

    @Override
    public boolean canPlaceItem(int slot, ItemStack stack) {
        if (slot < 0 || slot >= INPUT_SLOTS) {
            return false;
        }
        RecyclingRecipe recipe = this.findRecipe(stack);
        return recipe != null && (recipe.getPhase() != 2 || Config.allowPhaseTwo());
    }

    // ------------------------------------------------------------------
    // ContainerData (progreso sincronizado al cliente)
    // ------------------------------------------------------------------

    @Override
    public int get(int index) {
        return index == 0 ? this.progress : this.maxProgress;
    }

    @Override
    public void set(int index, int value) {
        if (index == 0) {
            this.progress = value;
        } else {
            this.maxProgress = Math.max(1, value);
        }
    }

    @Override
    public int getCount() {
        return 2;
    }

    // ------------------------------------------------------------------
    // Menu / capacidades
    // ------------------------------------------------------------------

    @Override
    public Component getDisplayName() {
        return Component.translatable("block.chernobylz_recycler.recycler");
    }

    @Nullable
    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory inventory, Player player) {
        return new RecyclerMenu(containerId, inventory, this);
    }

    @Override
    public <T> LazyOptional<T> getCapability(Capability<T> capability, @Nullable Direction side) {
        if (capability == ForgeCapabilities.ITEM_HANDLER) {
            return this.automationLazy.cast();
        }
        return super.getCapability(capability, side);
    }

    @Override
    public void invalidateCaps() {
        super.invalidateCaps();
        this.automationLazy.invalidate();
    }
}
