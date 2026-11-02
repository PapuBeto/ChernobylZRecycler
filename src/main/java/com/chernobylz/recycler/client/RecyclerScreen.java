package com.chernobylz.recycler.client;

import com.chernobylz.recycler.ChernobylZRecycler;
import com.chernobylz.recycler.menu.RecyclerMenu;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;

/**
 * Pantalla de la recicladora, tema oscuro tipo panel industrial (acento verde).
 *
 * <p>El PNG mide exactamente 176x166 y el blit usa ese tamano; ya no el blit de
 * 7 argumentos, que asume 256x256 y deforma la textura.</p>
 */
public class RecyclerScreen extends AbstractContainerScreen<RecyclerMenu> {

    private static final ResourceLocation TEXTURE =
            new ResourceLocation(ChernobylZRecycler.MODID, "textures/gui/recycler.png");

    /** Tamano real del PNG. */
    private static final int TEXTURE_WIDTH = 176;
    private static final int TEXTURE_HEIGHT = 166;

    /** Hueco de la barra de progreso dentro de la textura (80 px / 5 segmentos). */
    private static final int BARRA_X = 48;
    private static final int BARRA_Y = 45;
    private static final int BARRA_ANCHO = 80;
    private static final int BARRA_ALTO = 11;
    private static final int SEGMENTOS = 5;

    /** Paleta del panel oscuro. */
    private static final int COLOR_TITULO = 0xFFE8E8E8;
    private static final int COLOR_ETIQUETA = 0xFFA0A0A0;
    private static final int COLOR_AVANCE = 0xFF4E9A57;
    private static final int COLOR_SEPARADOR = 0xFF0A0B0D;

    /** Etiquetas ENTRADA/SALIDA compactas (escala 0.75) al costado de cada
     *  fila de slots. Coordenadas en panel a tamano completo. */
    private static final float ETIQUETA_ESCALA = 0.75F;
    private static final int ENTRADA_LABEL_X = 138;
    private static final int ENTRADA_LABEL_Y = 28;
    private static final int SALIDA_LABEL_X = 138;
    private static final int SALIDA_LABEL_Y = 64;

    public RecyclerScreen(RecyclerMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
        this.inventoryLabelX = 8;
        this.inventoryLabelY = 78;
    }

    @Override
    protected void renderBg(GuiGraphics guiGraphics, float partialTick, int mouseX, int mouseY) {
        int x = this.leftPos;
        int y = this.topPos;
        guiGraphics.blit(TEXTURE, x, y, this.imageWidth, this.imageHeight,
                0.0F, 0.0F, TEXTURE_WIDTH, TEXTURE_HEIGHT, TEXTURE_WIDTH, TEXTURE_HEIGHT);

        int progress = this.menu.getScaledProgress(BARRA_ANCHO);
        if (progress > 0) {
            guiGraphics.fill(x + BARRA_X, y + BARRA_Y, x + BARRA_X + progress,
                    y + BARRA_Y + BARRA_ALTO, COLOR_AVANCE);
        }
        // Separadores de los 5 segmentos, encima del relleno (estilo medidor).
        for (int i = 1; i < SEGMENTOS; i++) {
            int separador = x + BARRA_X + i * (BARRA_ANCHO / SEGMENTOS);
            guiGraphics.fill(separador, y + BARRA_Y, separador + 1,
                    y + BARRA_Y + BARRA_ALTO, COLOR_SEPARADOR);
        }
    }

    @Override
    protected void renderLabels(GuiGraphics guiGraphics, int mouseX, int mouseY) {
        guiGraphics.drawString(this.font, this.title, this.titleLabelX, this.titleLabelY,
                COLOR_TITULO, false);
        guiGraphics.drawString(this.font, this.playerInventoryTitle,
                this.inventoryLabelX, this.inventoryLabelY, COLOR_ETIQUETA, false);
        // Nombres de las filas de la maquina, compactos al costado de cada fila
        PoseStack pose = guiGraphics.pose();
        pose.pushPose();
        pose.scale(ETIQUETA_ESCALA, ETIQUETA_ESCALA, 1.0F);
        int entradaX = Math.round(ENTRADA_LABEL_X / ETIQUETA_ESCALA);
        int entradaY = Math.round(ENTRADA_LABEL_Y / ETIQUETA_ESCALA);
        int salidaX = Math.round(SALIDA_LABEL_X / ETIQUETA_ESCALA);
        int salidaY = Math.round(SALIDA_LABEL_Y / ETIQUETA_ESCALA);
        guiGraphics.drawString(this.font,
                Component.translatable("container.chernobylz_recycler.recycler.in"),
                entradaX, entradaY, COLOR_ETIQUETA, false);
        guiGraphics.drawString(this.font,
                Component.translatable("container.chernobylz_recycler.recycler.out"),
                salidaX, salidaY, COLOR_ETIQUETA, false);
        pose.popPose();
    }
}
