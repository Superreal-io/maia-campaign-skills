# Análisis del deck fuente — rebuild de `movistar-pptx` sobre la NUEVA plantilla oficial

> Documento §1-§2 del rebuild de `movistar-pptx` siguiendo `docs/PPTX-SKILL-REBUILD-PLAYBOOK.md`.
> Analiza estructuralmente **dos** plantillas y produce una selección de arquetipos canónicos que es
> la **UNIÓN** de la cobertura de ambas (requisito explícito de Pablo — la plantilla vieja NO se
> descarta en bloque). Impulsa `build_template.py` (`CANONICAL_SLIDES`) y `build_catalog.py`.
>
> - **Plantilla A (NUEVA, base primaria)**: `250917_Movistar_PlantillaPPT.pptx` — ~60 slides reales
>   compuestas, 27 slideLayouts, tema Arial, 0 fuentes embebidas, ~209 MB de media.
>   (`C:\Users\pablo\Desktop\SRSKILLTEMP\movistar\`)
> - **Plantilla B (ACTUAL en producción)**: `assets/template/movistar-template.pptx` — 101
>   slideLayouts, 0 slides físicas (deck basado en layouts/placeholders), tema Movistar Sans,
>   fuentes embebidas. Es la que hoy documentan `references/{families,selection-guide,
>   placeholder-roles}.md` y `layouts-catalog-full.json`.

> **Índice rápido**: §0 Método y hechos de cabecera · §1 Inventario Plantilla A (60 slides →
> arquetipos) · §2 Inventario Plantilla B (101 layouts → arquetipos) · §3 Cross-map A↔B (qué
> RECUPERAR) · §4 Set canónico recomendado (~35, numerado) · §5 Datos de fuente/tema/color/media
> a confirmar para el build.

---

## §0 — Método y hechos de cabecera

**Método** (mismo espíritu que el análisis de San Miguel): se parsea el XML directamente desde el
`.zip` (no se carga la media de 209 MB en python-pptx). Por cada slide de A: layout asignado (vía
`slides/_rels/*.rels`), color de `<p:bg>` resuelto (scheme o srgb), placeholders nativos vs shapes
planas, nº de zonas de texto no vacías, geometría en % del lienzo, texto de ejemplo (para calibrar
capacidad después) y detección de nombres de shape duplicados. Para B se clusteriza la lista de
101 slideLayouts por roles de placeholder.

**Hechos compartidos por A y B** (buena noticia para el rebuild):

| | Plantilla A (nueva) | Plantilla B (vieja) |
|---|---|---|
| Tamaño lienzo | 33,87 × 19,05 cm — **16:9** (aspect 1,778) | 33,9 × 19,1 cm — **16:9** |
| `clrMap` | `bg1→lt1, tx1→dk1, bg2→lt2, tx2→dk2`, accents directos | idéntico |
| slides físicas | **60** (arquetipos reales compuestos) | 0 (solo 101 layouts) |
| slideLayouts | 27 (25 usados por slides + 2 sin instancia) | 101 |
| Tema fuente mayor/menor | **Arial / Arial** | **Movistar Sans / Movistar Sans Medium** |
| Fuentes embebidas | **NO** (`embeddedFontLst` ausente, 0 `.fntdata`) | **SÍ** (`embeddedFontLst` presente) |

Que ambas sean 16:9 con el mismo `clrMap` significa que la geometría y el sistema de color slot→hex
son directamente comparables. La diferencia crítica es fuente/tema (ver §5).

**Aviso de método (encoding)**: los textos de ejemplo de A usan acentos y comillas tipográficas;
los índices/estructura de este doc se verificaron contra el XML crudo, no contra el volcado de
consola (que mojibakea los acentos). Los índices de slide son **0-based** (slide1.xml = `#00`).

---

## §1 — Inventario de la Plantilla A (nueva) — las 60 slides

Uso de layout observado en las 60 slides: `Portada 01` ×10, `1_Portada 01` ×4, `2_Portada 01` ×2,
`3_Portada 01` ×2, `4_Portada 01` ×1, `2_Portada 02` ×2, `3_Portada 02` ×1, `Aviso` ×1, `Indice 1`
×1, `Indice 2` ×1, `Separador 01` ×8, `1_Separador 01` ×3, `Separador 02` ×5, `1_Separador 02` ×2,
`Titular Grande 1` ×1, `8_Txt_Imagen_Redonda_Fondo_Azul` ×1, `20_Interior` ×2, `21_Interior` ×2,
`22_Interior` ×1, `23_Interior` ×4, `24_Interior` ×1, `26_Interior` ×1, `27_Interior` ×1,
`2_12A_Texto_Device 2` ×1, `Cierre` ×2.

**Layouts SIN slide de ejemplo** (existen como arquetipo pero nadie los compuso): `Titular Grande 2`
(slideLayout16) y `1_Cierre` (slideLayout27). Son variantes disponibles no demostradas — no se
descartan, se marcan como "pendiente de componer" en §4.

**Chrome de página / branding** (aparece en casi todas las slides como shapes fijas, no editables):
`Gráfico 44` = **isotipo M** (SVG 155×114) arriba-derecha por defecto (alt. abajo-derecha, ~4-11%
del lienzo); `Gráfico 5` = **logotipo "movistar"** (SVG 374×105) abajo-izquierda (~6×3%). En las
slides de cierre `Gráfico 7/8` = M grande centrada. Esto confirma la regla de marca "1 M por slide,
superior derecha por defecto" del `info.md`. El build **no debe** tocar ni duplicar estas shapes.

### 1.1 — Inventario slide a slide (agrupado por arquetipo)

Leyenda: `foto` = lleva imagen (bleed = a sangre 100×100; margen = ~95×91 con marco; ph = picture
placeholder split); `chrome` = tiene cabecera de página editable (título/subtítulo/nº); `bg` = color
de fondo resuelto (`bg1`=crema `#FEF9F5`, `tx1`=negro `#201E1D`, `tx2`=**azul `#0066FF`**, `accentN`
ver §5).

| # | slide | layout | Arquetipo | foto | chrome | bg | texto de ejemplo (capacidad) |
|---|---|---|---|---|---|---|---|
| 00 | slide1 | Aviso | **AVISO_CONFIDENCIALIDAD** | — | — | crema | "INSERTE TIPO USO SEGURIDAD" (1 caja @66,1) |
| 01 | slide2 | Portada 01 | **PORTADA_TITULO** (sin foto) | — | título+sub | crema | "Ejemplo titular principal 66pt" + "Ejemplo subtitular 14 pt" |
| 02 | slide3 | 1_Portada 01 | PORTADA_TITULO (variante) | — | título+sub | crema | ídem 66pt/14pt |
| 03 | slide4 | 2_Portada 01 | PORTADA_TITULO (variante) | — | título+sub | crema | ídem 66pt/14pt |
| 04 | slide5 | Portada 01 | **PORTADA_FOTO_MARGEN** | margen (95×91) | título+sub | — | 66pt/14pt sobre foto |
| 05-07 | slide6-8 | Portada 01 | PORTADA_FOTO_MARGEN (repeticiones) | margen | título+sub | — | idénticas salvo foto de ejemplo |
| 08 | slide9 | Portada 01 | PORTADA_FOTO_MARGEN (subtítulo reposicionado @4,42) | margen | título+sub | — | 66pt/14pt |
| 09 | slide10 | Portada 01 | PORTADA_FOTO_MARGEN (repetición) | margen | título+sub | — | 66pt/14pt |
| 10 | slide11 | Portada 01 | **PORTADA_FOTO_BLEED_SCRIM** (scrim completo, `Rectangle 7` 98×100) | bleed (100×100) | título+sub | — | 66pt/14pt sobre scrim |
| 11 | slide12 | Portada 01 | PORTADA_FOTO_BLEED_SCRIM_MEDIO (scrim 47% ancho) | bleed | título+sub | — | 66pt/14pt |
| 12 | slide13 | Portada 01 | scrim 47% (repetición de #11) | bleed | título+sub | — | 66pt/14pt |
| 13 | slide14 | 1_Portada 01 | PORTADA_FOTO_MARGEN (variante layout) | margen | título+sub | — | 66pt/14pt |
| 14 | slide15 | 1_Portada 01 | ídem (repetición) | margen | título+sub | — | 66pt/14pt |
| 15 | slide16 | 3_Portada 01 | **PORTADA_SPLIT_IMG** (título izq @2,4 46×19 + pic ph derecha) | ph (pic/16) | título+sub | crema | 66pt/14pt |
| 16 | slide17 | 3_Portada 01 | PORTADA_SPLIT_IMG (espejo, pic otro lado) | ph | título+sub | crema | 66pt/14pt |
| 17 | slide18 | 4_Portada 01 | PORTADA_SPLIT_IMG_04 (variante) | ph (pic/16) | título+sub | crema | 66pt/14pt |
| 18 | slide19 | 2_Portada 02 | **PORTADA_02_SPLIT** (titular 54pt + pic ph) | ph (pic/16) | título+sub | crema | "titular principal 54pt" |
| 19 | slide20 | 2_Portada 02 | PORTADA_02_SPLIT (espejo) | ph | título+sub | crema | 54pt |
| 20 | slide21 | 3_Portada 02 | PORTADA_02_SPLIT_03 (variante) | ph (pic/16) | título+sub | crema | 54pt |
| 21 | slide22 | Indice 1 | **INDICE_MULTI** (hasta 9 capítulos, 28 ph = nº+nombre+subtítulo) | — | título "Indice" | crema | "Nombre del capítulo" / "Subtitulo del capítulo" ×9 |
| 22 | slide23 | Indice 2 | **INDICE_SIMPLE** (lista "1.2.3.4.5." + subtítulo largo) | — | título "Agenda" | crema | numeración + subtítulos concatenados |
| 23 | slide24 | (1_Portada 01 base) | **AGENDA_5COL_CLARO** (5 grupos icono/nº + texto, `13 CuadroTexto`×10) | — | título "Agenda" | crema | "Primera sección, a 24 puntos / Texto secundario, 12 puntos" + nº 1-5 |
| 24 | slide25 | (2_Portada 01 base) | **AGENDA_5COL_OSCURO** (5 grupos, fondo negro `#262422`, texto 14pt) | — | título "Agenda" | srgb `262422` | 5 columnas, texto 14pt |
| 25 | slide26 | Separador 01 | **SEPARADOR_TITULO** (título grande capítulo @2,4 68×19) | — | título | crema | "Separador con el nombre del capítulo" |
| 26 | slide27 | 1_Separador 01 | SEPARADOR_TITULO_AZUL | — | título | **azul (tx2)** | ídem |
| 27 | slide28 | 1_Separador 01 | SEPARADOR_TITULO_AZUL (repetición) | — | título | azul | ídem |
| 28 | slide29 | Separador 01 | SEPARADOR_TITULO_AMARILLO | — | título | accent3 (amarillo) | ídem |
| 29 | slide30 | Separador 02 | **SEPARADOR_NUMERO** "01" (título + nº gigante @43,15 62×68) | — | título+nº | crema | "Separador con numero" + "01" |
| 30 | slide31 | Separador 02 | SEPARADOR_NUMERO "02" | — | título+nº | **accent2 (coral)** | "02" |
| 31 | slide32 | Separador 02 | SEPARADOR_NUMERO "03" | — | título+nº | **accent3 (amarillo)** | "03" |
| 32 | slide33 | Separador 02 | SEPARADOR_NUMERO "04" | — | título+nº | **accent4 (verde)** | "04" |
| 33 | slide34 | Separador 02 | SEPARADOR_NUMERO "05" | — | título+nº | **accent5 (azul claro)** | "05" |
| 34 | slide35 | 1_Separador 02 | SEPARADOR_NUMERO "06" | — | título+nº | **azul (tx2)** | "06" |
| 35 | slide36 | 1_Separador 02 | SEPARADOR_NUMERO "07" | — | título+nº | **negro (tx1)** | "07" |
| 36 | slide37 | Titular Grande 1 | **TITULAR_GRANDE** (título 48pt + subtítulo + párrafo) | — | título 48pt+sub+nº | crema | "Titulo de página Movistar Sans 48pt" + párrafo 16pt |
| 37 | slide38 | 8_Txt_Imagen_Redonda_Fondo_Azul | **INTERIOR_TXT_IMG_REDONDA_AZUL** | (imagen redonda) | título 48pt+sub | **azul (tx2)** | título 48pt + párrafo 16pt |
| 38 | slide39 | 21_Interior | **INTERIOR_TXT_2IMG** (título 29pt + sub + párrafo + 2 pics) | ph ×2 (pic/14,15) | título 29pt+sub+nº | crema | párrafo 16pt |
| 39 | slide40 | 20_Interior | **INTERIOR_TXT_1IMG** (título 29pt + sub + párrafo + 1 pic) | ph ×1 (pic/16) | título 29pt+sub+nº | crema | párrafo 16pt |
| 40 | slide41 | 22_Interior | **INTERIOR_TXT_2IMG_STACK** (2 pics apiladas derecha) | ph ×2 (@35,5 y @35,47) | título 29pt+sub+nº | crema | párrafo 16pt |
| 41 | slide42 | 21_Interior | INTERIOR_TXT_2IMG (repetición) | ph ×2 | título+sub+nº | crema | 16pt |
| 42 | slide43 | 27_Interior | **GRID_2IMG_CAPTION** (título 32pt + 2 pics + 2 pies) | ph ×2 (`Picture Placeholder 40` dup) | título 32pt+nº | crema | "Texto descriptivo" ×2 |
| 43 | slide44 | 26_Interior | **GRID_3IMG_CAPTION** (título 32pt + 3 pics + 3 pies) | ph ×3 (dup name) | título 32pt+nº | crema | "Texto descriptivo" ×3 |
| 44 | slide45 | 24_Interior | **GRID_MOSAICO_15** (título 32pt + 15 pics + 15 pies) | ph ×15 (dup name) | título 32pt+nº | crema | "Texto descriptivo" ×15 |
| 45 | slide46 | 2_12A_Texto_Device 2 | **INTERIOR_TXT_DEVICE** (título 29pt + párrafo + mockup teléfono @43,20 16×62 + 2 pics) | ph ×3 (pic/17,22,23) | título 29pt+sub+nº | crema | párrafo 16pt |
| 46 | slide47 | 20_Interior | **INTERIOR_CHART** (título 29pt + sub + párrafo + gráfico nativo) | Chart Placeholder 26 | título 29pt+sub+nº | crema | 16pt |
| 47 | slide48 | 23_Interior | **INTERIOR_TABLA** (título 29pt + texto 12pt + tabla nativa `Tabla 7`) | tabla nativa | título 29pt+nº | crema | "Ejemplo de texto 12 pt" |
| 48 | slide49 | 23_Interior | INTERIOR_TABLA (repetición, `Table 32`) | tabla nativa | título 29pt+nº | crema | 12pt |
| 49 | slide50 | 23_Interior | **INFOGRAFIA_GAUGES** (5 donut/arco % + título/desc, `Oval 9` dup ×6, muy custom) | — (freeform+arcos) | título 29pt+nº | crema | "55% / 80% / 95% / 65% / 70%" + "Escribe aquí el título" |
| 50 | slide51 | 23_Interior | INTERIOR_CHART (variante layout, `Chart Placeholder 3`) | chart nativo | título 29pt+nº | crema | 12pt |
| 51 | slide52 | (Separador 01 base) | **QUOTE_PLANO** (frase @4,23 92×51 + autor @18,68) | — | — | crema | "«Inserta una frase inspiradora.»" + "Autor" |
| 52 | slide53 | (Separador 01 base) | **QUOTE_FOTO** (frase sobre foto a sangre + scrim `Rectangle 4`) | bleed (100×100) | — | — | mismo quote |
| 53 | slide54 | 1_Separador 01 | **SEPARADOR_PALABRA** "Imagina" (@3,45 73×19) | — | palabra | **azul (tx2)** | 1 palabra |
| 54 | slide55 | Separador 01 | SEPARADOR_PALABRA "Inspira" | — | palabra | **negro (tx1)** | 1 palabra |
| 55 | slide56 | Separador 01 | SEPARADOR_PALABRA "Innova" | — | palabra | **accent2 (coral)** | 1 palabra |
| 56 | slide57 | Separador 01 | SEPARADOR_PALABRA "Sueña" | — | palabra | crema | 1 palabra |
| 57 | slide58 | Separador 01 | SEPARADOR_PALABRA "Crea" | — | palabra | **accent4 (verde)** | 1 palabra |
| 58 | slide59 | Cierre | **CIERRE_M** (`Rectangle 20` a sangre color sólido + M centrada `Gráfico 8`) | M grande | — | color sólido | (sin texto) |
| 59 | slide60 | Cierre | CIERRE_M (variante, `Gráfico 7` + `Grupo 4`) | M grande | — | color sólido | (sin texto) |

### 1.2 — Los 6 slides con nombres de shape DUPLICADOS (crítico para `_find_shape`)

`sm_pptx.py`/`mvst_pptx.py` localizan shapes por `shape_name` (a nivel superior, no recursivo). Un
nombre duplicado hace que `set_text()`/`set_image()` no pueda apuntar a un shape concreto sin
desambiguar. Los 6 slides afectados en A:

- `#23 slide24` y `#24 slide25` (AGENDA_5COL): `13 CuadroTexto` ×10 (anidados en los 5 grupos).
- `#42 slide43` (GRID_2IMG): `Picture Placeholder 40` ×2.
- `#43 slide44` (GRID_3IMG): `Picture Placeholder 40` ×3.
- `#44 slide45` (GRID_MOSAICO_15): `Picture Placeholder 40` ×15.
- `#49 slide50` (INFOGRAFIA_GAUGES): `Oval 9` ×6.

**Consecuencia para el build**: al clonar cualquiera de estos arquetipos hay que **renombrar los
shapes duplicados de forma única** (p. ej. por `idx` de placeholder, `Picture_pic13/pic15/…`) antes
de exponerlos como zonas editables, o exponerlos por `idx`/orden en vez de por nombre. La agenda de
5 columnas y el mosaico de 15 son los peores casos (contenido en grupos + nombres repetidos); tratar
igual que San Miguel trató el contenido anidado en `<p:grp>` (documentar posición pero no exponer
como zona editable plana si no se puede desambiguar con seguridad).

---

## §2 — Inventario de la Plantilla B (vieja, 101 slideLayouts)

B no tiene slides físicas: es un deck **basado en layouts + placeholders de relleno** (el modelo
elige un layout y `add_slide` rellena sus placeholders). Los 101 layouts se clusterizan así (nombres
exactos entre comillas; roles de placeholder verificados en el XML):

| Cluster | Layouts (nombre exacto) | Composición |
|---|---|---|
| **Portada sin foto** | `Portado 01` + `Portado 01 Verde/Coral/Amarillo/Azul` | ctrTitle (+ subTitle en variantes de color); portada limpia tintada al color del capítulo |
| **Portada texto-sobre-foto** | `Portado 02`, `1_Portado 02` | ctrTitle+subTitle, color texto = fondo → **requiere foto detrás** (bug G2 heredado) |
| **Portada con pic placeholder** | `Portado 03`, `1_Portado 03`, `Portado 04`, `1_Portado 04`, `2_Portado 04` | pic + ctrTitle + subTitle |
| **Agenda (índice 1 slide)** | `Agenda 02 x3` (9 body), `Agenda 02 x5` (15 body) | nº + título + sub-descripción por capítulo |
| **Separador nº-solo** | `Separador 01-05` | "#" gigante decorativo, sin título |
| **Separador título** | `Separador 06-11` | título de capítulo + intro corta |
| **Separador multi-nº (agenda-style)** | `Separador 12-16`, `1_Separador 12` (5 "#" simultáneos), `Separador 17-21` (título+2 body), `Separador 22-26` (título+body+**pic**) | divisor tipo navegación con varios números/labels |
| **Contenido texto** | `Title and Content`, `1_/2_/3_Title and Content`, `Text and List` | título + 1-6 bloques body / lista dedicada |
| **3 contenidos secuenciales (color)** | `Title and 3 Content Verde/Coral/Amarillo/Azul` | 3 pasos apilados, columna color |
| **Paneles comparativa** | `2 Panel` (7 body), `3 Panel` (13 body) | 2/3 columnas paralelas con **tarjeta de cuerpo grande** |
| **Texto + imagen** | `Text and Image 01-20` + `1_Text and Image 01/12` | texto-al-lado-de-foto (01-03 seguros) y texto-sobre-foto (13-20) y grids de 3 (10-12) |
| **Texto + gráfico** | `Text and Chart 01/02/03` + `1_..8_Text and Chart 03` | 1 chart, o dashboard de 6 mini-charts, o grids de imagen |
| **Tabla** | `Table` | tabla nativa |
| **Timeline / proceso** | `Panagrama 01` (tbl), `Panagrama 02` (26 body), `Panagrama 03` (10 body) | cronología / hitos / step-by-step |
| **Statement / cifra hero** | `1_Statement` (Big Number) | una frase/cifra enorme, 1 idea |
| **Cita** | `Quote` + `Quote Verde/Coral/Amarillo/Azul` | frase corta a ~112pt |
| **Cierre logo** | `M`, `1_M`, `2_M`, `3_M` | logo Movistar a sangre, sin texto |
| **Cierre palabra** | `Thank You 01`, `Thank You 02` | "Gracias" a ~168pt |

Detalle fino de placeholders/idx/capacidad en `layouts-catalog-full.json`; reglas de uso en
`families.md`, `selection-guide.md`, `placeholder-roles.md`, `GOTCHAS.md`.

---

## §3 — Cross-map A ↔ B: qué cubre la nueva y qué hay que RECUPERAR

La columna "Equivalente en A" indica el arquetipo de la nueva plantilla que cubre esa función.
`RECUPERAR` = B ofrece una composición que A **no** trae y que aporta valor real → se re-expresa en
el sistema visual de la nueva plantilla (refresh Nov-2025: colores de tema de A, Movistar Sans,
chrome con M arriba-derecha + wordmark abajo-izquierda). Todo lo `RECUPERAR` queda **pendiente de
construir a mano en A** (no hay slide de origen que clonar).

| Cluster B | Equivalente en A | Veredicto |
|---|---|---|
| Portada sin foto (+ color) | PORTADA_TITULO (`#01-03`); color vía `<p:bg>` del slide | ✅ cubierto (A tinta por bg, no por layout dedicado) |
| Portada texto-sobre-foto | PORTADA_FOTO_BLEED_SCRIM (`#10-12`) — **A añade scrim real**, mejora sobre B | ✅ cubierto (mejor) |
| Portada con pic placeholder | PORTADA_SPLIT_IMG / _02 (`#15-20`) | ✅ cubierto |
| Agenda 02 x3/x5 | INDICE_MULTI (`#21`), INDICE_SIMPLE (`#22`), AGENDA_5COL claro/oscuro (`#23-24`) | ✅ cubierto (A más rico) |
| Separador nº-solo (01-05) | SEPARADOR_NUMERO (`#29-35`) — A añade título junto al número | ✅ cubierto (mejor) |
| Separador título (06-11) | SEPARADOR_TITULO (`#25-28`) | ✅ cubierto |
| Separador multi-nº agenda (12-26) | Sin equivalente exacto; función cubierta por INDICE_MULTI/AGENDA_5COL | 🟡 RECUPERAR-opcional (baja prioridad) |
| Contenido texto (Title and Content) | TITULAR_GRANDE (`#36`) + zonas texto de 20_/21_Interior | ✅ cubierto |
| **Text and List (lista dedicada)** | A no tiene layout de lista; los interiores son de párrafo | 🟠 **RECUPERAR (medio)** |
| **Title and 3 Content (3 pasos secuenciales, color)** | A no tiene 3-pasos-texto tintado; AGENDA_5COL es icónica | 🟠 **RECUPERAR (medio)** |
| **2 Panel / 3 Panel (comparativa texto)** | A **no** tiene comparativa de columnas paralelas con cuerpo sustancial | 🔴 **RECUPERAR (alto)** |
| Texto + imagen (01-20) | INTERIOR_TXT_1IMG/2IMG/STACK, redonda-azul, device (`#37-45`) | ✅ cubierto (A muy rico) |
| Texto + gráfico (Chart 01/02) | INTERIOR_CHART (`#46`, `#50`) | ✅ cubierto |
| Text and Chart 03 (dashboard 6 mini-charts) | GRID_MOSAICO/gauges parcial; sin dashboard de 6 charts exacto | 🟡 RECUPERAR-opcional (bajo) |
| Tabla | INTERIOR_TABLA (`#47-48`, tabla nativa) | ✅ cubierto |
| **Panagrama 01/02/03 (timeline / hitos / proceso)** | A **no** tiene ningún layout de cronología | 🔴 **RECUPERAR (alto)** |
| **1_Statement / Big Number (cifra hero de dato)** | A solo tiene nº de capítulo (SEPARADOR_NUMERO) y palabra-divisor; **no** una cifra hero de métrica | 🔴 **RECUPERAR (alto)** |
| Quote (+ color) | QUOTE_PLANO (`#51`), QUOTE_FOTO (`#52`) | ✅ cubierto |
| Cierre logo (M / 1_/2_/3_M) | CIERRE_M (`#58-59`) | ✅ cubierto |
| Cierre palabra (Thank You) | A no tiene cierre de palabra ("Gracias"); el default de marca es la M | 🟡 RECUPERAR-opcional (bajo — M es el cierre canónico) |

**Los 3 huecos ALTOS a recuperar** (candidatos de máxima prioridad, sin equivalente en A):

1. **TIMELINE / PANAGRAMA** — cronología, hitos, "20 años de Movistar", proceso de contratación
   en pasos. Es el hueco más claro: ninguna slide de A hace timeline. En B es `Panagrama 01`
   (relleno por `rows=`, ver `selection-guide.md`). Re-expresar en A con el chrome de página +
   Movistar Sans + una banda temporal horizontal.
2. **PANEL_COMPARATIVA 2/3** — comparar 2-3 opciones/planes/conceptos en columnas paralelas con
   cuerpo de texto sustancial (no fotos, no iconos). A solo tiene grids de imagen con pie corto.
   Re-expresar como 2/3 tarjetas de color (usando accents de A) con título + cuerpo por columna.
3. **STATEMENT_HERO** — una cifra/claim de dato a gran tamaño ("45 €/mes", "20 años", "NPS #1").
   Distinto del SEPARADOR_NUMERO de A (que es numeración de capítulo 01-07, no un dato) y del
   SEPARADOR_PALABRA (que es una palabra-divisor). Re-expresar como cifra hero centrada sobre
   fondo azul/color, sin chrome de párrafo.

**⚠️ Nota transversal para todo lo RECUPERAR**: las reglas de capacidad y los bugs de B
(`placeholder-roles.md` R1-R4, `GOTCHAS.md` G2-G13: "#" = 1 dígito, tarjetas de panel no vacías,
Statement ≤4 palabras, Quote ≤5, etc.) **siguen siendo válidas conceptualmente** pero apuntan a
geometría/tamaños/colores de B — hay que recalibrar cada límite contra la geometría real de A antes
de portarlos. No copiar los idx/sz de B a ciegas.

---

## §4 — Set canónico recomendado (~35 arquetipos)

Formato: `NOMBRE → origen`, con `rol` (portada/divider/contenido/cierre), `foto`, `header` (¿lleva
cabecera de página editable a rellenar?), y `use_when` / `use_when_not`. **[C]** = elección
conservadora/segura (preferir por defecto). Origen `A #NN` = clonar esa slide real; `RECUPERAR (B
"…")` = construir nuevo en el sistema de A a partir del arquetipo de B.

**Portadas / apertura**

1. **AVISO_CONFIDENCIALIDAD** → A `#00` (Aviso). rol=portada · foto=no · header=no · use_when: deck
   interno que requiere marca de confidencialidad/uso. use_when_not: deck comercial/externo → omitir.
2. **PORTADA_TITULO** [C] → A `#01` (Portada 01). rol=portada · foto=no · header=título+sub · use_when:
   portada/sección sin foto, cualquier longitud de titular. use_when_not: hay foto hero disponible.
   *(Mantener `#03` 2_Portada 01 como variante de tratamiento — no es duplicado exacto.)*
3. **PORTADA_FOTO_MARGEN** → A `#04` (Portada 01 + foto 95×91). rol=portada · foto=margen ·
   header=título+sub · use_when: portada con foto hero de marca y titular corto. use_when_not: la foto
   no tiene zona de contraste donde aterriza el texto.
4. **PORTADA_FOTO_BLEED_SCRIM** [C] → A `#10` (scrim completo). rol=portada · foto=a sangre + scrim ·
   header=título+sub · use_when: foto a sangre y hace falta legibilidad garantizada (el scrim la da).
   use_when_not: foto ya tiene zona oscura uniforme → usar #04 sin scrim. *(Mantener `#11` scrim-medio
   47% como variante.)*
5. **PORTADA_SPLIT_IMG** → A `#15` (3_Portada 01). rol=portada · foto=ph split · header=título+sub ·
   use_when: portada partida texto|imagen, titular largo. use_when_not: no vas a rellenar el pic ph.
   *(Mantener `#17` 4_Portada 01 y el espejo `#16` como variantes.)*
6. **PORTADA_02_SPLIT** → A `#18` (2_Portada 02, 54pt). rol=portada · foto=ph split · header=título+sub
   · use_when: portada partida con titular a 54pt. use_when_not: titular muy largo → usar #05.

**Índice / agenda**

7. **INDICE_MULTI** → A `#21` (Indice 1). rol=contenido · foto=no · header=título "Indice" · use_when:
   deck con 5-9 capítulos, mostrar todos con nº+nombre+subtítulo. use_when_not: ≤3 capítulos → #08.
8. **INDICE_SIMPLE** → A `#22` (Indice 2). rol=contenido · foto=no · header=título "Agenda" · use_when:
   índice compacto de hasta 5 puntos. use_when_not: necesitas subtítulos ricos → #07.
9. **AGENDA_5COL_CLARO** → A `#23`. rol=contenido · foto=no · header=título · use_when: 5 secciones
   con nº+título+descripción corta en columnas, fondo claro. use_when_not: >5 secciones. ⚠️ nombres
   dup (`13 CuadroTexto`×10) → desambiguar en el build.
10. **AGENDA_5COL_OSCURO** → A `#24` (fondo negro `#262422`). rol=contenido · foto=no · header=título ·
    variante oscura de #9 — mantener (color real distinto, no duplicado). ⚠️ mismos nombres dup.

**Separadores / divisores** *(mantener TODAS las variantes de color — lección San Miguel G18)*

11. **SEPARADOR_TITULO** [C] → A `#25` (Separador 01, crema). rol=divider · foto=no · header=título ·
    use_when: divisor de capítulo con nombre. use_when_not: >1 palabra corta cabe mejor en nº.
12. **SEPARADOR_TITULO_COLOR** → A `#26` (azul) / `#28` (amarillo). variantes de color de #11.
13. **SEPARADOR_NUMERO** [C] → A `#29` (Separador 02, "01"). rol=divider · foto=no · header=título+nº ·
    use_when: divisor con número de capítulo gigante + título. use_when_not: número >1 dígito.
14. **SEPARADOR_NUMERO_PALETA** → A `#30-#35` (coral/amarillo/verde/azul-claro/azul/negro). **Mantener
    las 7 variantes de color** — demuestran el sistema cromático completo, no son duplicados.
15. **SEPARADOR_PALABRA** → A `#53` "Imagina" (1_Separador 01). rol=divider · foto=no · header=1 palabra
    · use_when: divisor motivacional de 1 palabra. use_when_not: frase → QUOTE. **Mantener las 5
    variantes de color `#53-#57`** (azul/negro/coral/crema/verde).

**Contenido interior** *(todos llevan chrome de página: título + subtítulo + nº de slide a rellenar)*

16. **TITULAR_GRANDE** [C] → A `#36` (Titular Grande 1). rol=contenido · foto=no · header=título 48pt+
    sub+párrafo · use_when: 1 idea con titular grande + párrafo. use_when_not: hace falta imagen.
17. **TITULAR_GRANDE_2** → A layout `slideLayout16` (**sin slide de ejemplo — componer**). Variante de
    #16; marcar pendiente de componer y verificar por render.
18. **INTERIOR_TXT_1IMG** [C] → A `#39` (20_Interior). rol=contenido · foto=1 ph · header=título 29pt+
    sub+párrafo · use_when: idea + 1 foto de apoyo. use_when_not: comparar 2 imágenes → #19.
19. **INTERIOR_TXT_2IMG** → A `#38` (21_Interior). rol=contenido · foto=2 ph · header sí · use_when:
    2 imágenes lado a lado + texto. use_when_not: apilar vertical → #20.
20. **INTERIOR_TXT_2IMG_STACK** → A `#40` (22_Interior). rol=contenido · foto=2 ph apiladas · header sí.
21. **INTERIOR_TXT_IMG_REDONDA_AZUL** → A `#37` (8_Txt…Azul). rol=contenido · foto=redonda · header sí ·
    fondo **azul** · use_when: destacar un concepto con imagen circular sobre azul de marca.
22. **INTERIOR_TXT_DEVICE** → A `#45` (2_12A_Texto_Device 2). rol=contenido · foto=mockup teléfono+2 ·
    header sí · use_when: mostrar app/pantalla en dispositivo. use_when_not: no hay captura de device.

**Grids de imagen**

23. **GRID_2IMG_CAPTION** → A `#42` (27_Interior). rol=contenido · foto=2 ph + pies · header=título 32pt.
    ⚠️ `Picture Placeholder 40`×2 dup.
24. **GRID_3IMG_CAPTION** → A `#43` (26_Interior). rol=contenido · foto=3 ph + pies · header sí. ⚠️ dup×3.
25. **GRID_MOSAICO_15** → A `#44` (24_Interior). rol=contenido · foto=15 ph + pies · header sí ·
    use_when: catálogo/mosaico de muchos productos. use_when_not: <6 items → #23/#24. ⚠️ dup×15.

**Datos / gráficos / tabla**

26. **INTERIOR_CHART** [C] → A `#46` (20_Interior + chart nativo). rol=contenido · header sí · use_when:
    números que comparan/evolucionan (serie principal azul Movistar). *(Mantener `#50`, layout 23,
    como variante.)*
27. **INTERIOR_TABLA** [C] → A `#47` (23_Interior + tabla nativa). rol=contenido · header=título 29pt+
    texto 12pt · use_when: precios/specs/comparativas en filas y columnas. use_when_not: 1 cifra → hero.
28. **INFOGRAFIA_GAUGES** → A `#49` (23_Interior custom, 5 donuts %). rol=contenido · header sí ·
    use_when: 5 KPIs de porcentaje con título/descripción. **Muy custom** (freeform + arcos, `Oval 9`
    dup×6) — clonar tal cual, exponer solo los % y textos que sean shapes de nivel superior seguros.

**Cita**

29. **QUOTE_PLANO** → A `#51`. rol=contenido · foto=no · header=no · use_when: frase inspiradora + autor,
    fondo limpio. use_when_not: >~12 palabras.
30. **QUOTE_FOTO** → A `#52` (foto a sangre + scrim). rol=contenido · foto=a sangre · use_when: la misma
    cita sobre una foto de marca con scrim. use_when_not: foto sin zona de contraste.

**Cierre**

31. **CIERRE_M** [C] → A `#58` (Cierre, M a sangre). rol=cierre · foto=M · header=no · use_when: cierre
    de marca canónico. use_when_not: —. *(Mantener `#59` como variante; `slideLayout27` 1_Cierre sin
    slide de ejemplo → componer si se quiere una 2ª variante.)*

**RECUPERADOS de B (construir nuevo en el sistema de A — pendiente por caso)**

32. **TIMELINE_PANAGRAMA** → RECUPERAR (B `Panagrama 01`). rol=contenido · foto=no · header sí ·
    use_when: cronología/hitos/proceso por fechas o pasos. use_when_not: datos tabulares → #27.
    🔴 alto. Pendiente: banda temporal horizontal re-dibujada con colores de tema de A.
33. **PANEL_COMPARATIVA** → RECUPERAR (B `2 Panel`/`3 Panel`). rol=contenido · foto=no · header sí ·
    use_when: comparar 2-3 opciones/planes con cuerpo de texto sustancial por columna. use_when_not:
    items ≤3 líneas paralelos con foto → grids. 🔴 alto. Pendiente: tarjetas con accents de A, cuerpo
    siempre relleno (evitar el bug de tarjeta vacía G7).
34. **STATEMENT_HERO** → RECUPERAR (B `1_Statement`/Big Number). rol=contenido · foto=no · header=no ·
    use_when: 1 cifra/claim de dato a gran tamaño (métrica). use_when_not: cifra+producto concatenados
    (G9) → contenido. 🔴 alto. Pendiente: cifra centrada sobre azul/color de A, ≤4 palabras.
35. **TEXT_LIST** → RECUPERAR-opcional (B `Text and List`). rol=contenido · foto=no · header sí ·
    use_when: lista numerada/bullets clara y dedicada. 🟠 medio (los interiores de párrafo la absorben).

*(Opcionales de menor prioridad, no numerados en el set base — evaluar tras la primera ronda:
`TITLE_3_CONTENT` pasos secuenciales colorados de B; `CIERRE_GRACIAS` palabra de B `Thank You`;
`SEPARADOR_MULTINUMERO` de B `Separador 12-16`; `DASHBOARD_MINICHARTS` de B `Text and Chart 03`.)*

### 4.1 — Qué se DESCARTA (solo duplicados EXACTOS)

Se descartan **únicamente** slides que repiten layout **y** tratamiento, difiriendo solo en la foto/
texto de ejemplo — y aun así se conserva 1-2 representantes por arquetipo. NO se descarta ninguna
variante de color/composición (lección de la ronda San Miguel G18: "texto parecido" ≠ duplicado).

- PORTADA_FOTO_MARGEN: se conserva `#04` (+`#08` subtítulo reposicionado); se descartan `#05`, `#06`,
  `#07`, `#09` (misma Portada 01 + foto, solo cambia la imagen de ejemplo).
- PORTADA scrim-medio: se conserva `#11`; se descarta `#12` (repetición 47%).
- PORTADA 1_Portada 01 foto: se conserva `#13`; se descarta `#14`.
- SEPARADOR_TITULO_AZUL: se conserva `#26`; se descarta `#27`.
- INTERIOR_TXT_2IMG: se conserva `#38`; se descarta `#41`.
- INTERIOR_TABLA: se conserva `#47`; se descarta `#48`.
- CIERRE_M: se conserva `#58`; `#59` se mantiene como variante menor (lleva `Grupo 4` extra).

Todo lo demás (7 separadores-número de color, 5 palabras-divisor, agenda claro/oscuro, portada
con/sin foto/split, quote plano/foto, chart layout-20/layout-23) se **mantiene** como variante real.

---

## §5 — Datos de fuente / tema / color / media a confirmar para el build

### 5.1 — Fuentes: el riesgo #1 del rebuild

**El tema de A declara Arial (mayor y menor), pero los runs de las slides teclean "Movistar Sans"
a mano, y no hay ninguna fuente embebida.** Conteo real de `typeface=` en slides+layouts+master de A:

| typeface referenciado | nº refs | nota |
|---|---|---|
| `Movistar Sans` | 425 | hardcodeado en runs |
| `Movistar Sans Medium` | 409 | hardcodeado en runs |
| `Arial` | 180 | + `Arial Regular` ×10 |
| `+mn-lt` | 53 | referencia al tema (menor) = Arial |
| `Movistar Sans Extrabold` | 5 | titulares 1-2 palabras |
| `Movistar Sans Medium Italic` | 1 | |
| `REBOND GROTESQUE` | 18 | **cruft legacy** (latin+cs) |
| `Telefonica`, `Telefonica ExtraLight` | 1 + 6 | **cruft legacy** |
| `Calibri` | 4 | **cruft legacy** (+ theme2 = Calibri, es el tema de notas) |

Implicaciones para el build (a confirmar/decidir):

1. **Sin Movistar Sans instalada/embebida, A renderiza en Arial** (o el fallback del sistema) — el
   deck se ve "casi bien" pero no es la tipografía de marca. El pipeline de producción (`artifact-
   flow`/`sr-agents-api`) inyecta la fuente desde `assets/fonts/` de la skill (ver CLAUDE.md: "NO
   hace falta `fontsBundleFileId`"), así que el flujo actual probablemente resuelve esto — pero
   **hay que verificarlo en el render real de A** (soffice/PDF), no darlo por hecho. B **sí** embebe
   las fuentes; A **no** → es un cambio de comportamiento respecto a producción.
2. **Decisión de tema**: A pone `Arial` como fuente de tema (`+mn-lt`/`+mj-lt` → Arial). Conviene
   evaluar cambiar el `<a:fontScheme>` de A a `Movistar Sans`/`Movistar Sans Medium` (como B) para que
   los runs que usan la referencia de tema (`+mn-lt`) hereden la marca — o dejar Arial como fallback
   consciente. Cambio de tema = decisión de Pablo, no automático.
3. **Limpiar el cruft legacy** (`REBOND GROTESQUE`, `Telefonica`, `Telefonica ExtraLight`, `Calibri`)
   de los runs — son restos de versiones anteriores del cliente, no marca Movistar.
4. La escalera de tamaños **real** de A (titular portada 66pt / 54pt · título página 48pt / 32pt /
   29pt · subtítulo 14pt · párrafo 16pt · texto denso 12pt) **NO coincide** con la jerarquía del
   `info.md` del cliente (H1 100pt · H2 45pt · body 30pt · legal 14pt). Leer los tamaños del binario
   real, no del brand-doc, al extraer capacidades en `build_catalog.py`.

### 5.2 — Colores de tema (A) vs paleta de marca (`info.md`) vs plantilla vieja (B)

`clrMap` de A (idéntico en B): `bg1→lt1`, `tx1→dk1`, `bg2→lt2`, `tx2→dk2`, `accentN→accentN`.
**`tx2` = `dk2` = `#0066FF` = azul Movistar** → un fondo `scheme:tx2` es AZUL (así se pintan los
separadores azules y la interior redonda-azul).

| slot | A (nueva, refresh Nov-25) | marca `info.md` | B (vieja) | ¿coincide? |
|---|---|---|---|---|
| dk1 (negro/tx1) | `201E1D` | `262423` | `262423` | A difiere; B = marca |
| lt1 (blanco/bg1) | `FEF9F5` | `FFFAF5` | `FFFAF3` | ~aproximado |
| dk2 (azul/tx2) | **`0066FF`** | **`0066FF`** | `0068FF` | **A = marca exacto** |
| accent1 | `012D66` (azul oscuro) | `022D67` az.oscuro | `D3EEFF` (az.claro) | A≈marca; **orden de slots distinto en B** |
| accent2 | `FBC2A5` (coral) | `FFC5A8` coral cl. | `E1F7D4` | A≈marca |
| accent3 | `FEE89A` (amarillo) | `FFE99C` amar. cl. | `FFF0C0` | A≈marca |
| accent4 | `CDF7BE` (verde) | `CEF7BF` verde cl. | `FFDAC7` | A≈marca exacto |
| accent5 | `CAEFFF` (azul claro) | `D3EEFF` azul cl. | `002E6B` | A difiere de marca |
| accent6 | `3487FF` (azul medio) | — | `2F5624` | — |

Observaciones para el build:
- **Los slots de accent cambiaron de orden entre B y A.** El build debe usar el mapeo de A (coral/
  amarillo/verde/azul-claro en accent2-5), no el de B (azul-claro/verde/amarillo/coral). No portar
  colores por número de slot de B.
- **A es la fuente autoritativa de color para ESTA plantilla** (es el binario que el cliente compuso).
  Sus hexes de refresh difieren ligeramente de los del `info.md`; el `info.md` a su vez avisa de una
  inconsistencia interna del cliente en el sistema de capítulos (claros vs oscuros). Recomendación:
  usar los valores del tema de A para el `.pptx`, y dejar el `info.md`/brand-guidelines como
  referencia — **flag para confirmar con Silvia/diseño** si el refresh de A es el color definitivo.
- **El sistema de capítulos NO está codificado en el orden de los separadores de A.** La plantilla
  demuestra los 7 colores en Separador 02 (01=crema, 02=coral, 03=amarillo, 04=verde, 05=azul-claro,
  06=azul, 07=negro), que **no** es la regla "01 azul · 02 verde · 03 amarillo · 04 negro" del
  `info.md`. No derivar número→color del orden de la plantilla; tratar el color como parámetro libre.

### 5.3 — Media y de-bundle (límite de 8 MB de Console)

**A pesa ~209 MB, casi todo fotos de ejemplo**: 26 ficheros de media = 7 JPG (11-43 MB c/u; el mayor
`image20.jpg` 42,6 MB), 7 PNG (0,45-8,6 MB) y 12 SVG diminutos (<15 KB). Los SVG son el branding:
**isotipo M** (viewBox 155×114 — `image1/4/8/9/10/24/26.svg`) y **logotipo "movistar"** (viewBox
374×105 — `image2/3/5/6/11.svg`).

- **Obligatorio de-bundlear la plantilla** igual que las otras marcas: excluir las fotos de ejemplo
  del `.zip` de Console (excede el límite de 8 MB por ~26×). La plantilla de-bundleada (solo XML +
  SVG de branding) pesa <1 MB. Servir las fotos por `imageryBundleFileId`/`container_upload` y que el
  helper las resuelva por nombre (patrón `mvst_pptx.py` ya existente).
- **Los SVG de branding (M + wordmark) SÍ se quedan** en la plantilla (son cerebro ligero, chrome de
  página, no fotos intercambiables).
- Decisión de build: las fotos de ejemplo de A **no** son banco de marca reutilizable — son
  placeholders de la plantilla. Al clonar un arquetipo, el pic placeholder se rellena con foto del
  banco real de Movistar (Azure blob / imagery-index), no con la foto de ejemplo horneada.

---

## Apéndice — próximos pasos (fuera de §1-§2)

1. `build_template.py::CANONICAL_SLIDES` = los 35 del §4 (clonar los `A #NN`; construir los 4
   `RECUPERAR`). Renombrar shapes duplicados de los 6 slides de §1.2 antes de exponerlos.
2. `build_catalog.py` auto-extrae geometría/fuente/color de cada elemento — leer tamaños reales de A
   (§5.1.4), no del `info.md`.
3. Verificar por render real (soffice→PDF + rasterizado, **nunca** `Slide.Export()` COM — ver San
   Miguel GOTCHAS G8) que la fuente resuelve a Movistar Sans en el entorno de producción (§5.1.1).
4. Confirmar con diseño (Silvia) los hexes de refresh de A vs `info.md` (§5.2) y el tema Arial vs
   Movistar Sans (§5.1.2) antes de fijar el `<a:fontScheme>`/`<a:clrScheme>` de la plantilla final.

---

## §6 — Resultado del build (2026-07-23) — `scripts/build_template.py` → `assets/template/movistar.pptx`

Ejecutado el rebuild sobre la Plantilla A. `build_template.py` corre limpio y produce
`assets/template/movistar.pptx` — **54 slides, 9,4 MB** (51 de la fuente + 3 recuperadas), que pasa
`verify_pptx.py` (gate OPC) y `finalize_pptx.py`. Verificaciones (todas OK):

- **físico == lógico**: 54 partes `ppt/slides/slide*.xml` == `len(Presentation(...).slides)` == 54.
- **Fuente embebida**: `embeddedFontLst` presente (3 familias), `embedTrueTypeFonts="1"`, 10 partes
  `.fntdata`, `[Content_Types].xml` declara `fntdata`, orden de elementos correcto
  (`sldSz, notesSz, embeddedFontLst, defaultTextStyle`). Cada EOT decodifica a un TTF con el nombre
  de familia correcto (ver §6.2).
- **Sin cruft**: 0 referencias a `Arial`/`Gill Sans`/`REBOND GROTESQUE`/`Telefonica`/`Calibri`/
  `Movistar Sans Medium Italic` en runs de slides/layouts/master/notesMaster. Typefaces `<a:latin>`
  que quedan en las slides: `Movistar Sans` (505), `Movistar Sans Medium` (274), `+mn-lt` (36, ref de
  tema → Movistar Sans Medium), `Movistar Sans Extrabold` (5).
- **QA por render** (soffice → PDF → PNG, PyMuPDF; **nunca** `Slide.Export()` COM — G8): las 54
  slides renderizan (PDF de 54 páginas == 54 slides). Revisadas a ojo AVISO (#00, tenía Telefonica/
  Calibri), AGENDA_5COL_OSCURO (tenía Arial×90), PORTADA_02_SPLIT (antes oculta), interior azul, y el
  mosaico de 15 fotos: todas en **Movistar Sans** (no Arial — letterforms inequívocas), colores de
  marca correctos, isotipo M + wordmark Telefónica intactos, sin desbordes.

### 6.1 — Set canónico final (54 slides: 51 de la fuente A + 3 recuperadas)

Confirma el §4/§4.1 sin cambios de criterio. **Descartados (9 duplicados EXACTOS)**: `#05 #06 #07
#09` (repeticiones de PORTADA_FOTO_MARGEN, solo cambia la foto de ejemplo), `#12` (scrim-medio
repetido), `#14` (1_Portada 01 con foto repetida), `#27` (separador azul repetido), `#41` (2img
repetido), `#48` (tabla repetida). **Conservadas 51** = las 31 categorías de arquetipo de A + todas
sus variantes reales de color/composición (lección San Miguel G18). El mapeo exacto índice→nombre
vive en `SOURCE_CANONICAL_SLIDES` de `build_template.py` (y se imprime al final del build). Las tres
recuperadas se añaden después de ese mapeo como slides sintéticas reproducibles (ver §6.4).

> Nota sobre "31 vs 51": la nueva plantilla tiene **31 categorías de arquetipo** (los ítems 1-31 del
> §4). Se materializan en **51 slides de fuente** porque se conservan las variantes reales (7 separadores-número
> de color, 5 palabras-divisor, 3 portadas-título de tratamiento, espejos de split, agenda claro/
> oscuro, quote plano/foto, chart layout-20/23, 2 cierres). No son duplicados: difieren en color o
> composición, no solo en la foto de ejemplo. El total entregado es **54** al sumar los tres
> arquetipos recuperados.

### 6.2 — Decisiones de fuente (medidas, no supuestas)

- **Corrección de nombre de familia (riesgo #1 resuelto)**: los TTF de `movistar-brand-guidelines-v1`
  se llaman internamente `Movistar Sans TT` / `...TT Medium` / `...TT Extrabold`, pero los runs (y la
  plantilla B de producción) referencian `Movistar Sans` / `...Medium` / `...Extrabold`.
  `_rename_ttf_family` reescribe la tabla `name` del TTF (quita el " TT") ANTES de envolverlo en EOT,
  de modo que **nombre interno == atributo `p:font typeface` == typeface del run**. Es exactamente la
  convención con la que B funciona en producción hoy (B referencia `Movistar Sans` en runs y
  `embeddedFontLst`). Sin esto, PowerPoint podría registrar la fuente bajo `Movistar Sans TT` y no
  casar con los runs `Movistar Sans`.
- **Compensación de tamaño = 1.0 (NO se escala ningún `sz`)** — decisión basada en medida real con
  fontTools, NO copiada de San Miguel (cuyo deck usaba sustitutas de sistema con métricas muy
  distintas). Anchura media de avance: **Movistar Sans-Regular / Arial = 1.003** (idéntica);
  Movistar Sans / Gill Sans = 1.083; vertical (winAsc+winDesc) Movistar Sans/Arial = 1.139. Como
  Movistar Sans ES la fuente intencional (813+716 runs ya la teclean → las cajas ya están
  dimensionadas para ella) y el renombrado Arial/Gill→Movistar Sans no cambia la anchura de forma
  apreciable, escalar reduciría fidelidad. Validado por render: AGENDA_5COL (que tenía Arial×90) no
  desborda tras el swap sin compensación.
- **Tema**: `<a:fontScheme>` de theme1 pasa a `majorFont="Movistar Sans"` / `minorFont="Movistar Sans
  Medium"` (igual que B) → los runs con referencia de tema (`+mn-lt`/`+mj-lt`) heredan la marca. El
  theme2 (tema de NOTAS) se deja con sus Calibri/Aptos de Office — no es superficie de marca.
- **Cruft limpiado**: Arial/Arial Regular/Gill Sans/REBOND GROTESQUE/Telefonica/Telefonica
  ExtraLight/Calibri + el único `Movistar Sans Medium Italic` → Movistar Sans / Movistar Sans Medium.

### 6.3 — Slides des-ocultadas (hallazgo del build)

La plantilla del cliente traía **3 slides marcadas como ocultas** (`show="0"`): PORTADA_02_SPLIT y
sus 2 variantes (source `#18/#19/#20`). LibreOffice/PowerPoint las omiten al exportar/proyectar (por
eso el primer PDF salió con 48 páginas para 51 slides). Como en una plantilla de CLONADO son
arquetipos de primera clase, `_unhide_slides` les quita el `show="0"`. `show` es una propiedad de
navegación de slideshow, sin significado de marca → normalizarla es seguro. **A confirmar con diseño**
si alguna de esas 3 se ocultó por estar deprecada (no parece — renderizan bien).

### 6.4 — Arquetipos recuperados de la plantilla vieja B — **3 añadidos y verificados**

La revisión final comparó los layouts `2 Panel`, `3 Panel` y `Panagrama 03` de B con el lenguaje
visual del refresh. Se recuperan los huecos de composición que no estaban bien cubiertos en A:

- **`COMPARATIVA_2_PANEL`**: dos paneles planos coral/verde para contraste sustancial entre opciones.
- **`COMPARATIVA_3_PANEL`**: tres paneles coral/verde/amarillo para alternativas equivalentes.
- **`TIMELINE_3_FASES`**: tres fases con cabecera y milestone, reexpresadas como recorrido horizontal.

No se copió el XML de la plantilla vieja. `build_template.py` clona determinísticamente una slide
oficial de A que ya contiene el chrome correcto, elimina su contenido editable y construye solo la
composición interior con geometría, paleta y Movistar Sans del refresh. Así se mantiene el master,
la M, Telefónica, el número de página y la fuente embebida del sistema nuevo. El build fuerza partes
físicas sin colisiones (`slide61.xml`–`slide63.xml`), el catálogo nombra todas las zonas editables y
el render de 54 páginas confirma que las tres composiciones no desbordan ni pierden contraste.

`Panagrama 01/02`, `Text and List` y `Statement` no se añaden como slides extra porque su función ya
está cubierta por gráficos/tablas, interiores de texto y separadores de cifra del set de A. Esto
evita duplicar arquetipos sin aportar una composición nueva.

### 6.5 — Follow-ups de despliegue (para Pablo)

- **Migración del motor completada**: `mvst_pptx.py` usa el modelo de clonado de 54 slides,
  `slides-catalog-movistar.json` y las APIs `use()`/`set_text()`/`set_image()`/`set_page_header()`.
  El quickstart de `SKILL.md` y los decks de regresión ejercitan el contrato completo.
- **Dos plantillas coexisten** temporalmente en `assets/template/` (`movistar-template.pptx` vieja +
  `movistar.pptx` nueva). No borrar la vieja hasta confirmar el corte en producción. Ambas están
  `.skillignore`adas del zip de Console (se sirven por Files API); `_template_path()` prioriza
  `movistar.pptx` por nombre exacto.
- **Confirmar con diseño (Silvia)**: hexes de refresh de A (§5.2), y que las 3 slides des-ocultadas
  (§6.3) no estén deprecadas.
- **`templateFileId`**: al subir esta plantilla a la Files API, el `templateFileId` de Movistar
  cambia (fichero distinto al de B). Coordinar con Mario (`docs/BACKEND-INTEGRATION.md`).

## §7 — Estado v4 (rebuild bi-master, 2026-07-27): los DOS sistemas en un solo binario

Todo lo anterior (§0-§6) describe el rebuild v3, que servía **un** sistema de diseño. La v4 cambia la
premisa: el binario que se entrega contiene **los dos sistemas oficiales del cliente**, cada uno con
su propio `slideMaster` y su propio tema, fusionados por OPC.

### 7.1 — Los dos orígenes y el reparto 52 / 104

`assets/template/movistar.pptx` — 156 diapositivas físicas · 2 `slideMaster` · 128 `slideLayouts` ·
10,89 MB · físico == lógico == 156 · `verify_pptx.py` OK · 10 EOT de Movistar Sans (1,28 MB).

| Sistema | Fichero de origen del cliente | Arquetipos | De ellos, diapositiva ya compuesta | Materializados desde un layout |
|---|---|---:|---:|---:|
| **refresh-2025** (vigente, `PRIMARY_SYSTEM`) | `250917_Movistar_PlantillaPPT.pptx` | **52** | 51 | 1 |
| **clásico** | `Movistar_PPT_Plantilla_v9_Reducida_LOW.pptx` | **104** | 23 | **81** |
| | | **156** | 74 | 82 |

Los **81 materializados** son la diferencia real frente a las otras marcas: el v9 traía 101
`slideLayouts` con arte completo pero **sin ninguna diapositiva compuesta** que clonar. Igual que en
`repsol-pptx`, hubo que instanciar una diapositiva física por layout y volcar como contenido propio
el texto-guía que el propio equipo de plantillas del cliente ya había escrito en cada placeholder.
No se inventó copy: lo que ves como texto de ejemplo del sistema clásico es el del cliente.

Catálogo: 156 arquetipos · **127 composiciones** · 12 familias · 725 zonas de texto (355 con
capacidad medida por geometría). Pipeline reproducible en dos pasos:

```bash
python scripts/build_template.py --stage post   # stages A (refresh) + B (v9) + merge + post
python scripts/build_catalog.py                 # 0 discrepancias manifiesto <-> catálogo
```

### 7.2 — §6.4 queda SUPERADO: los 3 arquetipos sintéticos ya no son sintéticos

§6.4 documentaba que `COMPARATIVA_2_PANEL`, `COMPARATIVA_3_PANEL` y `TIMELINE_3_FASES` se habían
**dibujado a mano con primitivas** (`build_template.py` construía la composición interior con
geometría y paleta, sobre el chrome de una slide real del refresh) porque el sistema del refresh no
tiene comparativas ni timeline y había que cubrir el hueco.

Eso ya no hace falta: **el arte REAL del cliente para esas tres composiciones existe, y está en el
sistema clásico.** La v4 lo sirve directamente:

| Nombre v3 (sintético) | Sirve ahora | Origen |
|---|---|---|
| `COMPARATIVA_2_PANEL` | `COMPARATIVA_2_PANEL_CLASICO` | arte real del v9 |
| `COMPARATIVA_3_PANEL` | `COMPARATIVA_3_PANEL_CLASICO` | arte real del v9 |
| `TIMELINE_3_FASES` | `TIMELINE_PROCESO_CLASICO` (planograma de bandas) · `TIMELINE_TABLA_CLASICO` (tabla de fases) · `TIMELINE_MULTI_CLASICO` (multi-hito) | arte real del v9 |

Los tres nombres viejos **siguen aceptándose como alias** (`DEPRECATED_ALIASES` en
`scripts/_contracts.py`) y `use()` avisa al resolverlos, porque estaban en producción. Pero **sus
zonas se llaman distinto**: las `Synthetic Title` / `Panel 1 Body` / `Phase 1 Header` que generaba el
build ya no existen. Hay que rellenar por el fill-spec que imprime `use()`, no de memoria —
`references/capability-recipe.md` trae la receta actualizada, con una versión por sistema.

Consecuencia de criterio, no solo técnica: la razón por la que §6.4 existía («no duplicar arquetipos
sin aportar una composición nueva») se resuelve mejor con dos sistemas explícitos que con
composiciones dibujadas a mano. Lo que antes era un parche del build es ahora una elección de
sistema que el modelo declara (`SKILL.md` §DOS SISTEMAS DE DISEÑO), y `verify_deck()` avisa si un
deck deja un sistema como residuo minoritario.

### 7.3 — Lo que §5.2 dejó abierto sigue abierto (y ahora está inventariado)

§5.2 comparaba los hexes del refresh con `info.md`. La v4 los unifica en un `CANONICAL_SCHEME` único
(`scripts/palette_normalize.py`) y remapea por semántica las referencias de los dos temas viejos,
pero **las decisiones de diseño que solo puede cerrar Silvia siguen pendientes**: están
inventariadas, una a una y con su valor por defecto, en `scripts/_contracts.py::PARAMETROS_ABIERTOS`
(9 entradas) y resumidas de forma accionable en `dist/handoff/movistar-v4/README.md`. Las dos que
más importan: **cuál de los dos templates es el vigente** (la evidencia técnica apunta al v9, no al
que se decidió) y el **verde oscuro `38552B` vs `36552B`**.
