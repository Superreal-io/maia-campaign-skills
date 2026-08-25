# Documentos Word (.docx) — criterio de marca Movistar

> Criterio para generar `.docx` con identidad Movistar **hoy**: usa la skill prebuilt **`docx`** de
> Anthropic (mecánica de construcción — creación, tablas, TOC, cabeceras) + este fichero (criterio de
> marca: jerarquía de estilos, tamaños, colores). Mismo patrón que decks `.pptx` (prebuilt `pptx` +
> `movistar-pptx`), pero aquí no hay un helper Python dedicado — aplica esta jerarquía directamente
> con las herramientas que da la skill `docx`.
>
> Fuente: estilos extraídos de una plantilla Word corporativa heredada (`2025_ Word_ Movistar.docx`,
> nombres internos "Telefónica"). La **estructura** (jerarquía, tamaños relativos, espaciados, qué
> existe) es reutilizable tal cual; los **valores de fuente y color de esa plantilla NO lo son** —
> ver remapeo obligatorio abajo.

## ⚠️ Remapeo obligatorio (la plantilla origen no es brand-compliant)

La plantilla heredada usa **Arial** (tema completo, ninguna referencia a Movistar Sans) y colores de
un tema genérico que no coinciden con el `.ase` oficial. Al generar un `.docx` real:

1. **Fuente: Movistar Sans en vez de Arial**, en todos los estilos de la tabla de abajo. Si el motor
   de generación no puede embeber la variable/OTF en el `.docx`, usa el fallback documentado en
   `SKILL.md` (§Tipografía) y dilo en el resumen — nunca dejes Arial silenciosamente.
2. **Color: paleta oficial en vez de los hex del tema heredado** — remapeo exacto:

| Hex de la plantilla heredada | Rol | Usa en su lugar |
|---|---|---|
| `#0C6DFF` (azul del tema, `dk1`/`dk2`) | acento/títulos | **Azul Movistar `#0066FF`** |
| `#606060` (gris del tema, `lt1`) | cuerpo de texto | **Negro Movistar `#262423`**, o gama de grises `color-palette.md` §4.5 si se busca un gris intermedio |
| `#FFFFFF` (`lt2`) | fondo claro | **Blanco Movistar `#FFFAF5`** (nunca blanco puro) |
| `#005DE6` (estilo `URL`) | enlaces | Azul Movistar `#0066FF` (unificar, no mantener un tercer azul) |
| `#9D83A3` / `#007635` (código/rutas) | resaltado técnico | sin equivalente de marca — mantener como color funcional neutro si el documento incluye bloques de código, no forzarlos a la paleta de marca |

## Página

- **Tamaño**: A4 (21 × 29,7 cm), orientación vertical.
- **Portada**: márgenes a sangre (sin margen lateral) — diseño full-bleed, fondo de color plano o
  foto del banco (`imagery/`) con texto centrado encima. Si es color plano, usa un color de marca
  (Azul Movistar por defecto); si es foto, aplica las mismas reglas de scrim/contraste que en pptx.
- **Contenido**: márgenes 2,5cm arriba/abajo, 3cm izquierda/derecha.

## Portada (título/subtítulo/nombre-fecha, con variante "sobre fondo oscuro")

| Rol | Tamaño | Color (ya remapeado) | Alineación | Notas |
|---|---|---|---|---|
| Título de portada | 28pt | Negro Movistar sobre fondo claro / Blanco Movistar sobre fondo azul u oscuro | centrado | — |
| Subtítulo de portada | 14pt | gris (paso intermedio de la gama §4.5) | centrado | line-spacing 1.0 |
| Nombre y fecha | tamaño normal | gris | centrado | line-spacing 0.8 (compacto) |
| Título de barra lateral | 14pt | Azul Movistar | no centrado | para un bloque lateral en la portada |

## Título y cuerpo de página interior

| Rol | Tamaño | Color | Espaciado | Notas |
|---|---|---|---|---|
| Título de página (H1) | 18pt | Azul Movistar | before/after 12pt, no partir de la página siguiente | — |
| Subtítulo de página (H2) | 12pt bold | gris/negro | before 12pt | sangría francesa |
| Párrafo (cuerpo estándar) | normal (~11pt) | Negro Movistar | before 6pt / after 12pt, line-spacing **1.2** | — |
| Destacado (cifra/frase hero) | 22pt | gris/negro (o Azul Movistar para más impacto) | — | para una cifra o frase destacada dentro del cuerpo, variante "sobre fondo oscuro" en Blanco Movistar |
| Texto utilitario pequeño | 9-10pt | gris | — | notas al pie, leyendas |

**Jerarquía de tamaño relativa** (mayor a menor): Título portada 28pt → Título página 18pt →
Destacado 22pt (dentro del cuerpo, no es un título) → Subtítulo página 12pt → Párrafo ~11pt →
utilitario 9-10pt → cabecera/pie 9pt.

## Tablas

- **Bordes finos** en un gris de la gama de neutros (`color-palette.md` §4.5), centrado vertical en
  cada celda.
- **Fila de cabecera**: bold, **Azul Movistar**, ~11pt, centrado, con borde ligeramente más marcado
  que el resto de la tabla.
- **Cuerpo de tabla**: Negro Movistar o gris intermedio, sin negrita.

## Código y rutas de archivo (si el documento incluye bloques técnicos)

- **Bloques de código**: fuente monoespacio (Consolas u otra disponible), color funcional neutro —
  no se fuerza a la paleta de marca (no hay equivalente de "código" en el Brand Guardian).
- **Rutas de fichero**: mismo tratamiento monoespacio, color distinto al de código para diferenciar
  visualmente ambos usos.
- **URLs/enlaces**: Azul Movistar, sin resaltado de fondo.

## Cabecera y pie de página

- Texto pequeño (9-10pt), gris, alineado a la izquierda (o centrado si el documento lo pide).
- Metadatos (fecha, versión, confidencialidad) en itálica, mismo gris.
- El logo "M" puede ir en la cabecera (ver `logo.md` para posición y área de protección) — no lo
  añadas al pie salvo que el diseño lo pida explícitamente.

## Relación con PDF

Esta misma jerarquía de tamaños/espaciados/colores es igualmente válida si el output final es un
PDF (vía WeasyPrint/reportlab u otro motor) en vez de un `.docx` — son decisiones de sistema
tipográfico, no mecánica específica de Word. Lo que no se traslada es la mecánica de estilos de
Word en sí (`w:style`, temas `.xml`); un PDF necesita su propio CSS/plantilla, pero puede partir de
esta misma jerarquía ya remapeada a la paleta oficial.
