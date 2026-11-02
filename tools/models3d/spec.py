"""Fase 0 — esquema de specs de modelos 3D.

Una Spec describe un item como piezas en la rejilla 0..16, en las mismas
unidades que las texturas y los modelos JSON de Minecraft. El validador
comprueba los límites del sistema de diseño antes de generar previews o
JSON de item (ver docs/DISENO_3D.md).

Reglas base:
- coordenadas enteras dentro de 0..16, con desde < hasta en cada eje;
- rotaciones de elemento solo ±22.5 / ±45 grados (limitación de Minecraft);
- las piezas de detalle sobresalen 1 px y penetran >= 1 px en el cuerpo
  (evita caras coplanares = z-fighting en el motor);
- el modelo apoya en y=0 (meta desde.y == 0), salvo "permitir_flotantes";
- el color se cita por referencia a la paleta ("material.variante" o
  color de desgaste directo "oxido", "hollin", ...).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .palette import (CLASES, CATEGORIAS, TIER_RULES, WEAR, ZONA_TIER,
                      ZONAS, color_ref)

ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CARAS = ("norte", "sur", "este", "oeste", "arriba", "abajo")
EJES = ("x", "y", "z")
ANGULOS = (-45.0, -22.5, 22.5, 45.0)


def _pt3(valor):
    if not isinstance(valor, (list, tuple)) or len(valor) != 3:
        raise ValueError(f"se esperaba un punto [x, y, z], no {valor!r}")
    return tuple(int(round(float(n))) for n in valor)


@dataclass
class Rotacion:
    """Rotación de elemento al estilo Minecraft (eje, ángulo, origen)."""

    eje: str
    angulo: float
    origen: tuple


@dataclass
class Pieza:
    """Un cubo del modelo.

    material: cita a la paleta, p. ej. "acero.oscuro".
    caras:    overrides opcionales por cara {"sur": "pantalla.claro"}.
    rotacion: Rotacion opcional (angulos validos: ±22.5, ±45).
    """

    nombre: str
    desde: tuple
    hasta: tuple
    material: str
    caras: dict = field(default_factory=dict)
    rotacion: Rotacion | None = None
    nota: str = ""

    def dimensiones(self):
        return tuple(b - a for a, b in zip(self.desde, self.hasta))

    @staticmethod
    def de_dict(d):
        rot = d.get("rotacion")
        rotacion = (
            Rotacion(eje=str(rot["eje"]), angulo=float(rot["angulo"]), origen=_pt3(rot["origen"]))
            if rot
            else None
        )
        return Pieza(
            nombre=str(d["nombre"]),
            desde=_pt3(d["desde"]),
            hasta=_pt3(d["hasta"]),
            material=d["material"],
            caras={str(k): str(v) for k, v in (d.get("caras") or {}).items()},
            rotacion=rotacion,
            nota=str(d.get("nota", "")),
        )


@dataclass
class Spec:
    """Spec completa de un item 3D."""

    id: str
    nombre: str
    zona: str
    tier: int
    categoria: str
    clase: str  # pequena | media | grande
    silueta: str
    piezas: list
    notas: list = field(default_factory=list)
    permitir_flotantes: bool = False

    def bbox(self):
        """Caja límite (sin aplicar rotaciones: aproximación válida)."""
        x0 = min(p.desde[0] for p in self.piezas)
        y0 = min(p.desde[1] for p in self.piezas)
        z0 = min(p.desde[2] for p in self.piezas)
        x1 = max(p.hasta[0] for p in self.piezas)
        y1 = max(p.hasta[1] for p in self.piezas)
        z1 = max(p.hasta[2] for p in self.piezas)
        return (x0, y0, z0, x1, y1, z1)

    # -- validación ---------------------------------------------------------

    def validar(self):
        """Devuelve (errores, avisos): errores = rompe el sistema de diseño."""
        errores, avisos = [], []

        if not ID_RE.match(self.id or ""):
            errores.append(f"id '{self.id}' no encaja con {ID_RE.pattern}")
        if self.zona not in ZONAS:
            errores.append(f"zona '{self.zona}' no está en {ZONAS}")
        if self.tier not in TIER_RULES:
            errores.append(f"tier {self.tier} no está en {sorted(TIER_RULES)}")
        if self.categoria not in CATEGORIAS:
            errores.append(f"categoría '{self.categoria}' no está en {CATEGORIAS}")
        if self.clase not in CLASES:
            errores.append(f"clase '{self.clase}' no está en {sorted(CLASES)}")
        if not self.piezas:
            errores.append("spec sin piezas")

        regla = TIER_RULES.get(self.tier, TIER_RULES[3])
        if len(self.piezas) > regla["elementos_max"]:
            errores.append(
                f"{len(self.piezas)} piezas supera el tope del tier {self.tier} "
                f"({regla['elementos_max']})"
            )
        acentos = sum(1 for p in self.piezas if p.material in WEAR)
        if acentos > regla["acentos_max"]:
            avisos.append(f"{acentos} acentos de desgaste geométrico "
                          f"(tope {regla['acentos_max']} en tier {self.tier})")

        vistas = set()
        for p in self.piezas:
            for eje_i in range(3):
                a, b = p.desde[eje_i], p.hasta[eje_i]
                if not (0 <= a < b <= 16):
                    errores.append(
                        f"[{p.nombre}] eje '{'xyz'[eje_i]}': {a}..{b} no cumple 0 <= desde < hasta <= 16"
                    )
            try:
                color_ref(p.material)
            except ValueError as e:
                errores.append(f"[{p.nombre}] {e}")
            for cara, ref in p.caras.items():
                if cara not in CARAS:
                    errores.append(f"[{p.nombre}] cara '{cara}' no está en {CARAS}")
                try:
                    color_ref(ref)
                except ValueError as e:
                    errores.append(f"[{p.nombre}] cara '{cara}': {e}")
            if p.rotacion is not None:
                r = p.rotacion
                if r.eje not in EJES:
                    errores.append(f"[{p.nombre}] eje de rotación '{r.eje}' no está en {EJES}")
                if float(r.angulo) not in ANGULOS:
                    errores.append(
                        f"[{p.nombre}] ángulo {r.angulo} no está en {ANGULOS} "
                        f"(limitación de elementos de Minecraft)"
                    )
                for v in r.origen:
                    if not 0 <= v <= 16:
                        errores.append(f"[{p.nombre}] origen de rotación {r.origen} fuera de 0..16")
            dx, dy, dz = p.dimensiones()
            if (dx == 1) + (dy == 1) + (dz == 1) >= 2:
                avisos.append(
                    f"[{p.nombre}] pieza 1x1x1: reservada a remaches y conectores"
                )
            clave = (p.desde, p.hasta, p.material)
            if clave in vistas:
                avisos.append(f"[{p.nombre}] pieza duplicada en {p.desde}..{p.hasta}")
            vistas.add(clave)

        x0, y0, z0, x1, y1, z1 = self.bbox()
        if self.piezas and y0 > 0 and not self.permitir_flotantes:
            avisos.append("el modelo no toca el plano de suelo (y=0)")
        if self.piezas and not regla["altura"][0] <= (y1 - y0) <= regla["altura"][1]:
            avisos.append(
                f"altura {y1 - y0} fuera de la banda del tier {self.tier} {regla['altura']}"
            )
        clase = CLASES.get(self.clase)
        if self.piezas and clase:
            alto = y1 - y0
            if not clase["altura"][0] <= alto <= clase["altura"][1]:
                avisos.append(f"altura {alto} fuera de la banda de la clase '{self.clase}' {clase['altura']}")
            huella = max(x1 - x0, z1 - z0)
            if huella > clase["huella"]:
                avisos.append(f"huella {huella} > {clase['huella']} de la clase '{self.clase}'")
        esperado = ZONA_TIER.get(self.zona)
        if esperado is not None and esperado != self.tier:
            avisos.append(f"tier {self.tier} poco habitual en la zona '{self.zona}' ( suele ser {esperado})")

        return errores, avisos

    # -- construcción --------------------------------------------------------

    @staticmethod
    def de_dict(d):
        return Spec(
            id=str(d["id"]),
            nombre=str(d.get("nombre", d["id"])),
            zona=str(d["zona"]),
            tier=int(d["tier"]),
            categoria=str(d["categoria"]),
            clase=str(d.get("clase", "media")),
            silueta=str(d.get("silueta", "")),
            piezas=[Pieza.de_dict(p) for p in d.get("piezas", [])],
            notas=list(d.get("notas", [])),
            permitir_flotantes=bool(d.get("permitir_flotantes", False)),
        )
