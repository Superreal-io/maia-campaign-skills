# GOTCHAS — motor de clonado sobre la plantilla real (rebuild bi-master, v4.0.0)

> ⚠️ **Los gotchas de la numeración ANTERIOR a este fichero (motor de layouts abstractos) quedaron
> OBSOLETOS** — no confundir con los G1-G24 de abajo, que son los vigentes. Describían
> bugs del motor VIEJO basado en 101 slideLayouts abstractos (`Portado 02`, `Separador 01`, `Agenda
> 02 x5`, `Title and 3 Content`...) que ya no existen — el motor de esta versión clona 54 diapos
> reales de la plantilla oficial nov-2025. Se han retirado en vez de mantenerse junto a información
> que ya no aplica (podría confundirse con un gotcha vigente). Los de abajo son los reales,
> encontrados y verificados construyendo ESTE motor.

## Índice

| # | Síntoma |
|---|---|
| [G1](#g1--nombre-de-familia-tt-en-los-ttf-de-marca) | Nombre de familia "TT" en los TTF de marca |
| [G2](#g2--la-mayoría-del-texto-hereda-de-layoutmaster-no-tiene-szcolor-propios) | La mayoría del texto hereda de layout/master |
| [G3](#g3--python-pptx-marca-placeholder-un-picture-placeholder-ya-relleno) | python-pptx marca PLACEHOLDER un picture placeholder ya relleno |
| [G4](#g4--duplicados-anidados-en-grupos-no-solo-nivel-superior) | Duplicados anidados en grupos |
| [G5](#g5--notesslide-compartida-al-clonar) | notesSlide compartida al clonar |
| [G6](#g6--físico--lógico-tras-clonarborrar) | Físico == lógico tras clonar/borrar |
| [G7](#g7--%E2%9B%94-retractado--agenda_5col_claro-nunca-tuvo-texto-blanco-sobre-crema) | ⛔ **RETRACTADO** — AGENDA_5COL_CLARO nunca tuvo texto blanco sobre crema |
| [G8](#g8--set_page_header-es-por-slide-no-por-deck) | `set_page_header()` es por-slide, no por-deck |
| [G9](#g9--infografia_gauges-sin-tamaño-de-fuente-resoluble) | INFOGRAFIA_GAUGES sin tamaño de fuente resoluble |
| [G10](#g10--nunca-slideexport-de-powerpoint-com-para-qa-visual) | Nunca `Slide.Export()` de PowerPoint COM para QA visual |
| [G11](#g11--%E2%9B%94-retractado--soffice-tenía-razón-ese-fondo-es-azul) | ⛔ **RETRACTADO** — `soffice` tenía razón: ese fondo ES azul |
| [G12](#g12--set_text-con-varias-líneas-colapsaba-a-un-solo-párrafo-indice_simple) | `set_text()` con varias líneas colapsaba a un solo párrafo (INDICE_SIMPLE) |
| [G13](#g13--el-número-de-un-separador_numero_0x-coincide-por-diseño-con-su-propio-texto-de-ejemplo) | El número de un `SEPARADOR_NUMERO_0X` coincide por diseño con su ejemplo |
| [G14](#g14--quote_plano--cita-larga-podía-pisar-la-línea-autor-fijo-2026-07-27) | `QUOTE_PLANO` — cita larga podía pisar la línea "Autor" (FIJO) |
| [G15](#g15--heurística-de-descubrimiento-del-bundle-de-imagery-podía-confundir-un-zip-de-test-ajeno-con-el-real-fijo-2026-07-27) | Heurística de imagery podía confundir un zip de test ajeno (FIJO) |
| [G16](#g16--set_table_data-dejaba-filascolumnas-sobrantes-en-blanco-sin-avisar-fijo-2026-07-27) | `set_table_data()` dejaba filas/columnas sobrantes en blanco sin avisar (FIJO) |
| [G17](#g17--%E2%9B%94-retractado--el-título-de-esa-agenda-tampoco-era-invisible) | ⛔ **RETRACTADO** — el título de esa agenda tampoco era invisible |
| [G18](#g18--zonas-de-imagen-que-no-se-podían-rellenar--y-las-5-que-resultaron-no-ser-zonas-de-imagen-fijo-v400) | Zonas de imagen no rellenables — y las 5 que resultaron ser TARJETAS de color (FIJO) |
| [G19](#g19--la-plantilla-en-producción-embebía-calibri-etiquetado-como-movistar-sans) | La plantilla en producción embebía **Calibri** etiquetado como Movistar Sans |
| [G20](#g20--libreoffice-ignora-las-fuentes-eot-embebidas-y-sustituye-por-una-más-ancha) | LibreOffice ignora las fuentes embebidas y sustituye por una más ancha |
| [G21](#g21--el-orden-de-los-shapes-no-es-el-orden-visual-permutación-silenciosa-de-bloques) | El orden de los shapes no es el visual: bloques permutados en silencio (FIJO) |
| [G22](#g22--add_chart-sobre-content_rect-sale-con-la-paleta-de-office-no-la-de-movistar) | `add_chart()` sobre `content_rect()` sale con la paleta de Office |
| [G23](#g23--12-de-las-35-entradas-del-banco-de-fotos-son-fondos-de-color-plano) | 12 de las 35 fotos del banco son fondos de color plano (FIJO: aviso) |
| [G24](#g24--max_chars_approx-puede-ser-absurdo-cuando-el-texto-de-ejemplo-es-una-palabra) | `max_chars_approx` absurdo cuando el ejemplo es una sola palabra (conocido) |
| [G25](#g25--set_table_data-escribía-texto-invisible-en-las-celdas-que-la-plantilla-dejaba-vacías-fijo-v400) | `set_table_data()` escribía texto INVISIBLE en celdas vacías de la plantilla (FIJO) |
| [G26](#g26--la-gráfica-del-refresh-es-una-tarta-y-el-fill-spec-no-lo-decía-fijo-v400) | La gráfica del refresh es una TARTA y el fill-spec no lo decía (FIJO) |
| [G27](#g27--título-de-la-gráfica-el-gate-de-título-de-ejemplo-solo-cubría-una-de-las-dos-cadenas-fijo-v400) | «Título de la gráfica»: el gate de título de ejemplo se le escapaba (FIJO) |
| [G28](#g28--el-sufijo-_n-de-una-familia-de-zonas-no-siempre-es-el-orden-visual-aviso-v400) | El sufijo `_N` no siempre es el orden visual (AVISO nuevo) |
| [G29](#g29--zonas-del-mismo-rol-donde-una-contiene-a-otra-los-anillos-de-infografia_gauges-aviso-v400) | Zonas del mismo rol donde una contiene a otra: los anillos de los gauges (AVISO) |
| [G30](#g30--set_textszona-none-escribía-la-cadena-literal-none-fijo-v400) | `set_texts({zona: None})` escribía la cadena literal "None" (FIJO) |
| [G31](#g31--tres-arquetipos-del-cliente-cuyo-propio-texto-de-ejemplo-desborda-no-es-el-renderizador) | 3 arquetipos cuyo propio texto de ejemplo desborda (no es el renderizador) |
| [G32](#g32--indice_simple-la-numeración-se-desalinea-si-un-tema-ocupa-dos-líneas) | `INDICE_SIMPLE`: la numeración se desalinea si un tema ocupa dos líneas |
| [G33](#g33--aviso_confidencialidad-lleva-una-instrucción-al-autor-impresa-en-la-diapositiva) | `AVISO_CONFIDENCIALIDAD` lleva una instrucción al autor impresa en la diapo |
| [G34](#g34--dos-use-del-mismo-arquetipo-de-gráfica-compartían-el-chart-part-fijo) | Dos `use()` de la misma gráfica compartían el `chart` part → datos destruidos en silencio (FIJO) |
| [G35](#g35--portada_foto_bleed_scrim-no-tiene-scrim-defecto-de-plantilla-conocido) | `PORTADA_FOTO_BLEED_SCRIM` no tiene scrim: titular a 1,7:1 (conocido) |
| [G36](#g36--interior_chart_l23-etiquetas-de-dato-ilegibles-defecto-de-plantilla-conocido) | `INTERIOR_CHART_L23`: etiquetas a 1,19:1 → sin gráfica de columnas en el sistema vigente |

## G1 · Nombre de familia "TT" en los TTF de marca

Los `.ttf` reales de Movistar Sans (`movistar-brand-guidelines-v1/assets/fonts/ttf/`) declaran
internamente el nombre de familia como `"Movistar Sans TT..."` (con sufijo "TT"), pero los runs de
la plantilla y la plantilla vieja de producción (B, 101 layouts) referencian `"Movistar Sans..."`
(SIN el sufijo). Si embebes el TTF tal cual (EOT), el nombre interno del `.fntdata` no coincide con
el `typeface` que declaran los runs → PowerPoint no encuentra la fuente embebida y sustituye por una
de sistema, en silencio. **Fix** (`build_template.py::_rename_ttf_family`): quita "TT" de la tabla
`name` del TTF ANTES de envolverlo en EOT, para que nombre interno == `typeface` del run == la
convención ya probada en producción por la plantilla B.

## G2 · La mayoría del texto hereda de layout/master (no tiene sz/color propios)

A diferencia de San Miguel/Alhambra (donde casi todo run real fija su propio tamaño/color), la
mayoría de los runs de la plantilla nueva de Movistar **no llevan `sz`/`solidFill` explícitos** —
heredan del placeholder equivalente del slideLayout (por `idx`, con fallback a `type` si el `idx` es
un valor centinela `4294967295`), y de ahí del `titleStyle`/`bodyStyle` del slideMaster, resolviendo
`schemeClr`+`lumMod`/`lumOff` contra el `clrMap`/`clrScheme` del tema y `+mn-lt`/`+mj-lt` contra el
`fontScheme`. `build_catalog.py` implementa esta cadena completa (`_effective_run_props`) — verificado
contra el XML crudo antes de escribir el código, no asumido. Si añades un check nuevo que lea
tamaño/color de un run, resuelve la herencia con esa misma cadena — leer solo el run se queda `None`
en la mayoría de los casos.

## G3 · python-pptx marca PLACEHOLDER un picture placeholder YA relleno

`shape.shape_type` de python-pptx devuelve `PLACEHOLDER` (no `PICTURE`) para cualquier picture
placeholder nativo, INCLUSO cuando ya tiene una foto real dentro (`<p:pic>` + `<p:ph type="pic">`).
Un primer catalogador que solo miraba `shape_type == PICTURE` perdía TODOS los slots de imagen
nativos (0 imágenes detectadas en `INTERIOR_TXT_1IMG`, que sí tiene una). **Fix**: detecta también
`ph.get("type") == "pic"` independientemente de `shape_type`. Verificado: el conteo de imágenes del
catálogo pasó de 0 a 34 tras el fix.

## G4 · Duplicados anidados en grupos, no solo nivel superior

San Miguel solo tenía duplicados de nombre a nivel superior de la slide. En Movistar, los 6 slides
con nombres repetidos los tienen ANIDADOS en `<p:grp>` (`13 CuadroTexto`×10 en las 2 agendas,
`Picture Placeholder 40`×2/×3/×15 en los grids, `Oval 9`×6 en la infografía). `_dedupe_shape_names`
recorre TODO el árbol (`slide._element.iter(qn("p:cNvPr"))`, cualquier profundidad), no solo los
shapes de nivel superior — necesario para que `use()`/`set_text()` puedan direccionar cada shape por
nombre sin ambigüedad.

## G5 · notesSlide compartida al clonar

Mismo bug que Alhambra/San Miguel: si el clon y el original comparten el mismo `notesSlide`, ese
`notesSlide` "resucita" al original ya borrado de `sldIdLst` tras `save()`, y el paquete queda con
partes físicas huérfanas (PowerPoint pide "Reparar"). `use()` usa `_CLONE_SKIP_RELTYPES` para NO
copiar la relación `notesSlide` al clonar. `verify_pptx.py` lo detecta como gate duro (notesSlide
compartida por 2+ slides) por si se reintroduce.

## G6 · Físico == lógico tras clonar/borrar

`save()` elimina las diapos canónicas no usadas antes de entregar — verificado SIEMPRE que el nº de
partes físicas `ppt/slides/*.xml` en el zip crudo coincide con `len(Presentation(...).slides)`
(no basta con que python-pptx reabra el fichero sin error). Confirmado independientemente en la
verificación de este rebuild (deck de prueba de 2 y de 6 slides, ambos con match exacto).

## G7 · ⛔ RETRACTADO — `AGENDA_5COL_CLARO` nunca tuvo texto blanco sobre crema

> **Este gotcha era FALSO y su "fix" era una regresión. Retractado el 2026-07-27 con evidencia
> dura. G11 y G17 caen con él: los tres se apoyaban en la misma premisa equivocada.**

**Lo que decía G7:** que `AGENDA_5COL_CLARO` tiene fondo crema y que sus 5 títulos + 5 números
en `srgbClr FFFFFF` eran invisibles; y que el fix era forzar los 30 runs a `#262422`.

**Lo que pasa en realidad.** El fondo de ese arquetipo **no es crema, es azul Movistar**. La
cadena completa, verificada byte a byte sobre el binario:

```
AGENDA_5COL_CLARO  →  slideLayout2.xml ("1_Portada 01")
   <p:cSld><p:bg>            = schemeClr bg1 → lt1 → FEF9F5   (crema)   ← lo que miró G7
   <p:cSld><p:spTree>
       <p:sp name="Rectangle 1" userDrawn="1">
           off=(0,0)  ext=(12192000, 6858000)                 ← A SANGRE COMPLETA
           <a:solidFill><a:schemeClr val="tx2"/>              ← TAPA el <p:bg>
   clrMap: tx2 → dk2 ;  clrScheme "MOVISTAR": dk2 = 0066FF    → AZUL MOVISTAR
```

El `<p:bg>` sí es crema, pero está cubierto por un rectángulo a sangre. **G7 miró
`<p:bg>` + `clrMap` + `clrScheme` y nunca el `spTree` del layout** — exactamente el error de
San Miguel G23/G24, pero invertido: allí se inventaron defectos inexistentes, aquí se descartó
uno real. Su hermana `AGENDA_5COL_OSCURO` usa el mismo patrón con `tx1` (≈ negro), que es
coherente.

**El fix empeoró la diapositiva.** Contrastes medidos:

| Combinación | Ratio | Veredicto |
|---|---|---|
| Blanco `FFFFFF` sobre azul `0066FF` — **el original del cliente** | **4,83:1** | Pasa AA · combinación **aprobada** por la guía de marca |
| `#262422` sobre azul — **lo que puso `_fix_agenda_claro_contrast`** | **3,20:1** | Falla AA · combinación **prohibida** por `brand/color-palette.md` §4.2.1 |
| Blanco sobre crema `FEF9F5` — el defecto que G7 creía arreglar | 1,05:1 | **Nunca existió** |

Confirmado por tres caminos independientes: trazado del XML, el auditor de contraste nuevo
(`scripts/contrast_audit.py`, que sí construye la pila de pintura incluyendo el `spTree` del
layout), y un render del **fichero original intacto del cliente** aislado en un mini-deck —
fondo azul, "Agenda" y los 5 títulos **en blanco**. La diapositiva nunca estuvo rota.

**Estado.** `_fix_agenda_claro_contrast` se retira en la v4 y se sustituye por un contra-gate
que hace fallar el build si alguien vuelve a oscurecer esa diapositiva. ⚠️ **La v3.2.3/3.2.4 que
está en `dev` sí lleva la regresión** — pendiente de decidir si se parchea allí.

**Defecto real que SÍ queda** (preexistente, del cliente, no tocado): el "Texto secundario, 12
puntos" va en `#262422` sobre el azul = 3,20:1, por debajo de AA. Está en la allowlist de
`contrast_audit.py` con su motivo.

**La lección de proceso, que es lo que hay que llevarse:** para saber de qué color es el fondo
bajo un texto **no basta con `<p:bg>`**. Hay que componer la pila real: `<p:bg>` de
master → layout → slide, y encima el `spTree` **del layout** y el de la slide, en z-order y
resolviendo transforms de grupo. Un rectángulo a sangre en el layout es un patrón normal de
plantilla, no una rareza.

## G8 · `set_page_header()` es por-slide, no por-deck

**Divergencia deliberada respecto a `set_deck_title()` de San Miguel** (que se llama UNA vez al
final y rellena la cabecera de TODAS las slides reales por igual). En Movistar, verificado contra el
XML crudo, el título/subtítulo de página de cada diapo interior es contenido genuinamente DISTINTO
por slide (no una cabecera corrida compartida) — llamar una sola vez al final con el mismo texto
habría escrito el MISMO titular en todas las interiores, algo activamente incorrecto. `set_page_header
(slide, title, subtitle=None, number=None)` se llama una vez POR slide de contenido, resolviendo los
shapes por `role` del catálogo ("title"/"subtitle"/"page_number"), nunca por nombre fijo (el nombre
literal del shape varía por arquetipo). El campo de número de página es un campo dinámico real de
PowerPoint (`<a:fld type="slidenum">`) — verificado por XML y por render (mostró "5" en la slide 5
real) — por eso queda excluido del gate duro de texto-de-ejemplo y `number=` es opcional/cosmético.

## G9 · INFOGRAFIA_GAUGES sin tamaño de fuente resoluble

Las 5 etiquetas de porcentaje de este arquetipo son autoshapes sueltas sin placeholder, con
`lstStyle` vacío — no hay tamaño de fuente resoluble en NINGÚN punto de la cadena de herencia OOXML
(verificado contra el XML crudo, no es un artefacto del extractor). Documentado como hueco cosmético
conocido en el catálogo (`font_pt: null` en esos 5 elementos) — clónalo tal cual, es un arquetipo muy
custom sin flexibilidad de reflow esperable.

## G10 · Nunca `Slide.Export()` de PowerPoint COM para QA visual

Mismo gotcha que San Miguel G8: `Slide.Export()` de PowerPoint vía COM tiene su propio bug de
sustitución de fuente al rasterizar, no relacionado con el fichero — un falso positivo real
encontrado en otra marca de este repo. El QA visual de este rebuild se hizo con `soffice` → PDF →
PyMuPDF/`fitz` (o `qa_render.py`, que degrada a `qa_flag: "qa_sin_render"` si `soffice` y ningún
rasterizador `fitz`/`pdftoppm` están disponibles) — nunca con `Slide.Export()`.

## G11 · ⛔ RETRACTADO — `soffice` tenía razón: ese fondo ES azul

> **Retractado el 2026-07-27. Ver G7 para la evidencia completa.** G11 concluyó que `soffice`
> pintaba `AGENDA_5COL_CLARO` de azul "por un artefacto de fuga de estado de tema en documentos
> grandes", porque el XML "resolvía a crema". El XML resuelve a crema solo si miras `<p:bg>` e
> ignoras el `Rectangle 1` a sangre del layout, que lleva `schemeClr tx2` = `0066FF`. **El fondo
> es azul y `soffice` lo estaba renderizando bien.** Sus pasos 3 y 4 ("aislada sale crema") solo
> se explican si el aislamiento perdió el layout — al aislar hay que arrastrar el slideLayout y
> su master, no solo el `spTree` de la slide.
>
> Lo que SÍ sigue siendo válido de G11 es la disciplina que proponía, y conviene conservarla:
> ante una duda de color de fondo, **aísla la diapositiva y re-renderiza antes de concluir**.
> Solo que el aislamiento tiene que ser fiel.

### Texto original (conservado por trazabilidad, NO seguir sus conclusiones)

`soffice` renderiza mal el fondo de AGENDA_5COL_CLARO SOLO dentro del deck completo

**Hallazgo real, verificado con una cadena de aislamiento completa** (no una sospecha sin comprobar):
al hacer el QA visual de un deck de prueba generado con el motor, la diapo `AGENDA_5COL_CLARO`
renderizaba con **fondo Azul Movistar `#0066FF`** en vez del crema esperado — y con las 5 secciones/
números en el color oscuro que fija G7, eso habría sido texto oscuro sobre azul, justo la
combinación que `brand/color-palette.md` §4.2.1 prohíbe explícitamente. Antes de tocar nada (ni
revertir G7 ni "arreglar" el fondo), se verificó paso a paso:

1. **El XML de la diapo/layout/máster no declara azul en ningún punto de la cadena.** El layout
   (`1_Portada 01`) declara su propio `<p:bg>` = `schemeClr bg1`; el `clrMap` del máster dice
   `bg1→lt1`; el tema dice `lt1 = #FEF9F5` (crema). Resolución 100% spec-correcta = crema, no azul.
2. **El `clrMap`/tema de esa diapo en `movistar.pptx` son BYTE-IDÉNTICOS a los del fichero original
   del cliente (209 MB) para la misma diapo** — descartado que `build_template.py` haya tocado
   `<p:bg>`/`clrMap`/`clrScheme` (de hecho no los toca en ningún punto del script).
3. **Aislando esa MISMA diapo del fichero de 209 MB original en un mini-deck de 1 sola diapo** →
   `soffice` la renderiza **crema** (`#FEF9F5`, muestreado por píxel).
4. **Aislando esa MISMA diapo de `movistar.pptx` (mi build) en un mini-deck de 1 sola diapo** →
   `soffice` TAMBIÉN la renderiza **crema**.
5. **Solo cuando se renderiza como parte del deck completo** (`movistar.pptx` entero, hoy 54 diapos, o
   un deck generado con `use()` que la incluya) → `soffice` la renderiza **azul**.

**Conclusión**: es un bug/artefacto de `soffice` al resolver el color de fondo de ESTA diapo
concreta en el contexto de un documento con muchas diapositivas (probable fuga de estado de tema
entre diapositivas dentro de una misma conversión) — **no un defecto real del fichero ni de este
rebuild**. El fondo verdadero (el que vería PowerPoint real) es crema, así que **el fix de G7 (texto
oscuro `#262422`) es correcto y NO se revierte**.

**Implicación práctica para el QA de esta plantilla concreta**: si un render completo con `soffice`
muestra un color de fondo que no cuadra con `background_treatment` del catálogo, **no asumas que el
catálogo/fichero está mal** — aísla esa diapo sola (extraerla a un mini-`.pptx` de 1 diapo, mismo
patrón que aquí) y vuelve a renderizar antes de "corregir" nada. No se ha comprobado si esto afecta a
otras diapos además de `AGENDA_5COL_CLARO` (las demás inspeccionadas visualmente en esta sesión
—portada, separador, titular grande, cierre— renderizaron correctamente tanto aisladas como en el
deck completo) — **recomendado confirmar en PowerPoint real antes de dar el pptx por cerrado del
todo**, mismo espíritu que G10.

## G12 · `set_text()` con varias líneas colapsaba a un solo párrafo (INDICE_SIMPLE)

**Bug real, encontrado generando un deck de demostración con contenido real** (no hipotético):
`INDICE_SIMPLE` trae la lista de 5 capítulos como **un único shape con 5 párrafos separados**
(`"Subtitulo del capítulo"` repetido 5 veces, uno por `<a:p>`) — a diferencia de San Miguel, que
tiene un shape por línea. La primera versión de `set_text()` solo editaba `paragraphs[0].runs[0]` y
BORRABA el resto de párrafos — si el modelo pasaba las 5 líneas reales unidas con `"\n"` (lo natural
al rellenar una lista), el resultado NO eran 5 párrafos con una línea cada uno: era **1 solo párrafo
con el carácter `\n` crudo dentro de `<a:t>`**, que en OOXML **no es un salto de línea real** —
PowerPoint no garantiza romper ahí (space/lo ignora según visor). El deck se guardaba sin error
(`save()`/`verify_pptx` no lo detectan, no es un problema de integridad OPC) pero el índice habría
salido con las 5 líneas corridas en una sola, ilegible.

**Fix** (`set_text()`): si el texto trae `"\n"` Y el shape original tiene AL MENOS ese número de
párrafos, reparte una línea por párrafo EXISTENTE (conservando el formato propio de cada uno,
incluido el primer run) en vez de crear un párrafo nuevo o meter el salto crudo. Si hay menos
párrafos que líneas, cae al comportamiento de siempre (una sola línea). Verificado: `INDICE_SIMPLE`
con 5 líneas reales → 5 párrafos con el texto correcto cada uno; un titular normal de una sola línea
→ sin cambios de comportamiento (regresión comprobada).

**Para quien rellene `INDICE_SIMPLE`** (o cualquier arquetipo futuro con el mismo patrón de varias
líneas en un shape): pasa las líneas unidas con `"\n"` a `set_text()`, una por capítulo — el motor ya
las reparte bien. No intentes llamar `set_text()` varias veces sobre el mismo shape para líneas
distintas (cada llamada borra el contenido previo del shape, ver el propio código).

## G13 · El número de un `SEPARADOR_NUMERO_0X` coincide por diseño con su propio texto de ejemplo

**Encontrado generando el deck de demostración con contenido real** (17 diapos, historia/portfolio/
posicionamiento/resultados/reconocimiento — no es un caso sintético): rellenar
`SEPARADOR_NUMERO_02_CORAL` con el número real de su capítulo ("02", el segundo capítulo del deck) y
`INDICE_SIMPLE` con la numeración real de sus 5 puntos ("1./2./3./4./5.") hacía que `save()`
bloqueara con "texto de ejemplo sin reemplazar" — porque, verificado contra el catálogo, el
`example_text` de esos shapes es LITERALMENTE "02" y "1.\n2.\n3.\n4.\n5." respectivamente: cada
`SEPARADOR_NUMERO_0X` trae de fábrica su propio número como texto de ejemplo, y la numeración de
`INDICE_SIMPLE` ya viene correcta para un índice de 5 puntos. No hay "otro" texto correcto que
escribir ahí — el valor real coincide, por diseño de la plantilla, con el de ejemplo.

`remove_shape()` no es la escapatoria correcta aquí (si se borra el número, no aparece en absoluto,
y SÍ se quiere que aparezca). **Fix**: nueva función `confirm_example_text(slide, shape_name)`,
hermana de `remove_shape()` — confirma explícitamente que el texto actual (aunque coincida con el
ejemplo) es contenido real correcto, y `save()`/`verify_deck()` dejan de tratarlo como sin reemplazar.
Uso excepcional, solo para este patrón de coincidencia por diseño — nunca para saltarse rellenar
contenido de verdad distinto del de ejemplo. Verificado: con `confirm_example_text()` la zona deja de
listarse como problema; sin llamarlo, una zona genuinamente sin tocar (p.ej. el titular de
`PORTADA_TITULO` de fábrica) sigue bloqueando `save()` con normalidad (regresión comprobada).

## G14 · `QUOTE_PLANO` — cita larga podía pisar la línea "Autor" (FIJO, 2026-07-27)

**Encontrado por QA visual real** (deck de prueba con una cita de 59 caracteres, bastante por encima
de los 38 del `max_chars_approx` orientativo del catálogo — no un límite duro): la caja de texto de
la cita ("Content Placeholder 11", 80pt, anclaje vertical centrado, `<a:bodyPr>` con
`<a:noAutofit/>`) envolvía a 3 líneas y la 3ª empujaba lo suficiente hacia abajo como para pisar
visualmente "Content Placeholder 5" (la línea "Autor", justo debajo). Reproducido con la misma
fuente embebida que el resto del deck — no es un artefacto de sustitución de fuente del
renderizador (a diferencia de G11).

**Fix**: `build_template.py::_fix_quote_plano_autofit` sustituye `noAutofit` por `normAutofit` en esa
caja concreta — PowerPoint/LibreOffice reducen automáticamente el tamaño de fuente si el texto no
cabe, en vez de desbordar. Única caja tocada; no afecta a `QUOTE_FOTO` ni a ninguna otra.

## G15 · Heurística de descubrimiento del bundle de imagery podía confundir un zip de test ajeno con el real (FIJO, 2026-07-27)

**Encontrado por QA visual real, en esta máquina compartida**: `list_brand_images()` resolvió una
foto contra un fixture de test abandonado de una sesión anterior
(`/tmp/movistar_helper_.../zzz-movistar-bundle.zip`, con imágenes stub de 1×1 píxel) — el fixture
declaraba `brand: Movistar` en su propio `imagery-index.json` y sus nombres de fichero coincidían con
entradas reales del índice, así que pasaba la validación existente (`_zip_movistar_index`: brand +
intersección de stems). No es un riesgo de producción real (ahí el bundle viene siempre de un
`imageryBundleFileId` real vía `container_upload`), pero merecía endurecerse: la búsqueda amplia
(`_search_roots()` incluye `/tmp`/cwd) puede toparse con ficheros ajenos en una máquina compartida.

**Fix**: `_zip_movistar_index` ahora exige además que al menos una de las imágenes coincidentes pese
`>= _MIN_PLAUSIBLE_PHOTO_BYTES` (3000 bytes) — la foto real más pequeña del banco bundleado pesa
~25 KB, un stub de 1×1 pesa un puñado de bytes; ningún bundle real deja de pasar este umbral.

## G16 · `set_table_data()` dejaba filas/columnas sobrantes en blanco sin avisar (FIJO, 2026-07-27)

**Encontrado por QA visual real**: `INTERIOR_TABLA` tiene 7 filas de cuerpo; un deck de prueba con
solo 5 filas de contenido real se guardó sin error, pero el render mostraba 2 filas completamente en
blanco con la banda de color de la plantilla — visible y embarazoso en un deck real, y sin ningún
aviso previo (a diferencia del desbordamiento de texto, que sí avisa).

**Fix**: `set_table_data()` ahora avisa (`[deck-qa]`, no bloquea) cuando los datos suministrados son
más pequeños que la tabla, indicando el tamaño exacto que hace falta. El catálogo (`build_catalog.py`)
también expone ahora `rows`/`cols` para cada elemento `kind: "table"`, así el llamador puede consultar
la capacidad real antes de generar los datos, en vez de adivinar.

## G17 · ⛔ RETRACTADO — el título de esa agenda tampoco era invisible

> **Retractado el 2026-07-27. Ver G7.** G17 dio por invisible el `Text Placeholder 6` porque
> heredaba `schemeClr bg1` (= crema) y creía que el fondo era crema. El fondo es **azul
> `0066FF`**, así que ese título heredado en crema daba 4,62:1 — legible y correcto. Forzarlo a
> `#262422` lo dejó en 3,20:1. El fix se retira con el de G7.

### Texto original (conservado por trazabilidad, NO seguir sus conclusiones)

`AGENDA_5COL_CLARO` — el título de página era invisible (FIJO, 2026-07-27)

**Segundo defecto real del mismo arquetipo que G7** (encontrado generando una pieza de demostración
con contenido real, no un caso sintético): el título de página ("Text Placeholder 6", texto
"Agenda") no tenía ningún `<a:rPr>`/`<a:solidFill>` propio — heredaba vía `schemeClr bg1`, que el
tema resuelve a `lt1` = `#FEF9F5` (confirmado leyendo `clrMap` + `clrScheme` del tema, no solo por
render). El fondo de la propia diapositiva (layout) es TAMBIÉN `schemeClr bg1` = `#FEF9F5` — el
título era literalmente del mismo color que su fondo, invisible.

**Por qué no se detectó en el fix de G7 ni en el QA visual de esta misma ronda**: el artefacto de
`soffice` documentado en G11 (fondo azul en vez de crema, solo dentro de esta plantilla) hace que en
CUALQUIER render disponible en este entorno el título (crema) se vea con contraste aceptable contra
un fondo que en realidad no es el real — enmascarando por completo el problema. Ni el render del
deck completo ni el render aislado de la sola diapositiva revelan el fondo cream real en este
entorno (a diferencia del hallazgo equivalente en Repsol G13, donde aislar la diapositiva SÍ reveló
el problema) — la única confirmación posible aquí fue leer el tema (`clrMap`/`clrScheme`) y
comprobar que ambos colores son el mismo valor exacto, no una aproximación visual.

**Fix**: mismo valor `#262422` ya usado y verificado en el resto del arquetipo (G7), forzando un
`<a:rPr>` explícito en el título (el run no tenía ninguno). Extiende `_fix_agenda_claro_contrast`
en vez de crear una función nueva — mismo archetype, misma familia de defecto, mismo color de
destino. **Recomendado confirmar en PowerPoint real** antes de dar el arquetipo por cerrado del
todo (mismo espíritu que G11) — la lectura del tema da confianza alta, pero un render real de
PowerPoint sería la confirmación definitiva.

## G18 · Zonas de imagen que no se podían rellenar — y las 5 que resultaron no ser zonas de imagen (FIJO, v4.0.0)

Había **tres** formas físicas distintas de "hueco de foto" en esta plantilla, y `set_image()` de la
v3 solo entendía una (sustituir un `<p:blipFill>` existente). El manifiesto y el catálogo discrepaban
justo sobre las otras dos, así que el arreglo empezó por decidir cuál de los dos tenía razón. La
respuesta no fue la esperada.

**Caso 1 · placeholder `pic` VACÍO — sí era el defecto que parecía. FIJO.**
`INTERIOR_TXT_2IMG` tiene "Picture Placeholder 6" y "Picture Placeholder 10" con `ph_type="pic"` y
`<p:spPr/>` vacío, sin ningún `<p:blipFill>`: defecto real del original del cliente
(`250917_Movistar_PlantillaPPT.pptx`, diapositiva fuente 38), a diferencia de
`INTERIOR_TXT_2IMG_STACK`, cuyos dos placeholders sí venían poblados. La v3 lanzaba `ValueError` y el
gotcha recomendaba evitar el arquetipo. **`set_image()` de la v4 los rellena**: detecta que el proxy
expone `insert_picture()`, inserta la foto, **restaura el `shape_name`** (la inserción sustituye el
elemento `<p:sp>` por un `<p:pic>` y el nombre se perdería) y aplica el mismo crop-to-fill centrado.
Verificado por render: las dos fotos salen con su geometría, su redondeo y su recorte correctos.

**Caso 2 · AUTO_SHAPE nombrada `imagen_N` — la mecánica se implementa, pero estas 5 NO son huecos de
foto.** `INTERIOR_TXT_3IMG_CAPTION_CLASICO` (3) e `INTERIOR_TXT_2IMG_CAPTION_CLASICO` (2) tienen
formas `roundRect` de color plano llamadas `imagen_1..3`, sin `blipFill`, a las que el manifiesto
asignó `role: image` y que el catálogo descarta como decorativas. La conclusión razonable era "el
catálogo se equivoca, hay que poder rellenarlas". **Es al revés, y lo demostró el render**: cada una
de las 5 tiene ENCIMA (>50% de solape, medido sobre el binario) una zona de texto `cuerpo_N` escrita
en un secundario OSCURO (`#38552B` verde, `#6A2C13` coral) sobre el relleno secundario CLARO de la
propia forma (`accent2` CEF7BF, `accent4` FFC5A8). **Son TARJETAS de color con texto encima**, y el
`_CAPTION` de sus nombres es un artefacto del heurístico de nombrado del build, no un pie de foto.
Rellenarlas con una foto deja ese texto sin fondo de contraste: exactamente el fallo que prohíbe
`brand/contrast-matrix.md`, y en el render de prueba el texto verde oscuro quedaba ilegible sobre la
fotografía.

La v4 hace las dos cosas: implementa la conversión de AUTO_SHAPE en hueco de foto real
(`_inject_blipfill()`: sustituye el `solidFill` por un `<a:blipFill>` con `<a:srcRect>` de recorte y
`<a:stretch>`, respetando el orden de hijos de `<p:spPr>` para que PowerPoint no pida reparar el
fichero, y preservando geometría, redondeo y contorno) **y** pone el guardarraíl:
`_overlapping_text_zone()` mide el solape sobre la diapositiva real y, si hay texto encima,
`set_image()` lanza explicando que es una tarjeta y dando las dos salidas (rellenar su texto con
`set_text()`, o `remove_shape()` de ese texto antes del `set_image()` si de verdad se quiere una
foto). Se mide sobre la diapositiva y no contra una tabla fija a propósito: si el modelo ya retiró
ese texto, la forma pasa a ser un hueco de foto legítimo y funciona. Verificado por render en el
mismo deck: `imagen_1` como tarjeta coral con su texto, `imagen_2` como foto real con crop-to-fill.

**Consecuencia para el catálogo (pendiente, fuera del motor):** `references/metadata/_metadata_interior.py`
sigue diciendo de `INTERIOR_TXT_2IMG` «evítalo, está roto de origen, `set_image()` lanza» — ya no es
cierto. Y el `role: image` que el manifiesto asigna a las 5 `imagen_N` es incorrecto: debería ser una
forma decorativa o una tarjeta. Ambas cosas se corrigen editando `references/metadata/` y
`build_template.py` y regenerando; el motor ya se comporta bien sin eso.

## G21 · El orden de los shapes NO es el orden visual (permutación silenciosa de bloques)

**Encontrado por render, no por lectura de código.** En `AGENDA_5COL_OSCURO`, las 10 zonas editables
se llaman `13 CuadroTexto`, `__2`, `__3`… y el orden en que viven en el `spTree` **no** es el orden
en pantalla: `__3` (x = 2,38 cm) es la PRIMERA columna y `13 CuadroTexto` (x = 8,45 cm) la segunda.
Rellenar "en orden de nombre" produce un deck que sale lleno, bien maquetado y con los bloques
**permutados** — en el render de prueba la agenda leía 2, 1, 3, 4, 5. Es el mismo modo de fallo que
`repsol-pptx` documenta en su G9, y afecta a cualquier arquetipo multi-columna cuyos nombres se
desambiguaron con sufijo `__N`.

**Fix**: el fill-spec que imprime `use()` (y `fill_spec()`) ordena las zonas por **orden de lectura**
—banda vertical de 1,5 cm, luego x— usando la geometría real de la diapositiva clonada, o `x_cm`/`y_cm`
del catálogo cuando se pide por nombre. El listado impreso ES el orden en que se lee la diapositiva,
así que rellenar siguiéndolo no puede permutar nada. **Regla para el modelo: no asignes bloques por
el número del sufijo; asígnalos en el orden en que `use()` los imprime.**

## G22 · `add_chart()` sobre `content_rect()` sale con la paleta de Office, no la de Movistar

`content_rect(slide)` (portado de `repsol-pptx`) devuelve el rectángulo libre bajo la cabecera para
insertar una tabla o una gráfica con la API nativa de python-pptx. En Repsol es el camino normal
porque ninguno de sus arquetipos trae gráfica precargada; **en Movistar no lo es**: hay 10 gráficas
nativas ya compuestas y con la paleta de marca aplicada, todas con workbook embebido y por tanto
editables con `set_chart_data()`. Una gráfica creada de cero con `add_chart()` hereda el ciclo de
color por defecto de Office (azul/naranja/gris) y sale del deck sin que ningún gate lo vea: es un
fallo de marca silencioso. Por eso `content_rect()` está documentado como **último recurso** y no
aparece en el flujo principal del `SKILL.md`.

Riesgo hermano, este sí cubierto: `set_chart_data()` avisa si le pasas más series de las que la
gráfica tiene diseñadas (`n_series` del catálogo), porque las series extra también salen con la
paleta de Office.

## G23 · 12 de las 35 entradas del banco de fotos son fondos de color plano

**Encontrado por render.** `list_brand_images()` devuelve las 35 entradas del índice de
`movistar-brand-guidelines` sin distinguir categoría, y **12 de ellas son `categoria: "fondo"`**:
fondos de color plano con el isotipo M y el claim "es por todos.", de uso muy acotado. Coger una por
descuido (un `list_brand_images()[5]` cualquiera) para un hueco de contenido llena la zona con una
tarjeta publicitaria en vez de una fotografía — y el deck sale aparentemente correcto, con logo y
todo. Pasó en un deck de prueba de esta ronda: las 3 zonas de `GRID_MOSAICO_3_CLASICO` salieron como
tres rectángulos de color.

**Fix**: `set_image()` avisa si el fichero elegido es uno de los 12 fondos y la zona destino no es a
sangre; el docstring de `list_brand_images()` y el §IMÁGENES del `SKILL.md` lo dicen explícitamente.
**Regla**: filtra por `categoria` (`personas`, `hogar`, `urbano`, `paisaje`, `deporte`, `producto`,
`conectividad`) o descarta `'fondo'` a mano.

## G24 · `max_chars_approx` puede ser absurdo cuando el texto de ejemplo es una palabra

`capacity_source: "medida"` calcula la capacidad como `len(texto_de_ejemplo) × 1,15`. Funciona cuando
el diseñador escribió un ejemplo representativo, pero cuando el ejemplo es literalmente `"Autor"`
(la línea de autoría de `QUOTE_PLANO`, `Content Placeholder 5`) el resultado son **6 caracteres**, y
cualquier nombre real de autor dispara el aviso de capacidad sin que haya ningún problema de
maquetación. Lo mismo pasa con `"Agenda"` (7) o `"Planograma"` (12) como títulos.

No se ha cambiado la fórmula: moverla desplazaría `max_chars_approx` en los 51 arquetipos heredados y
el fichero-oro `references/roles-baseline-54.json` haría fallar el build (que es exactamente su
trabajo). **Trátalo como lo que es: un aviso orientativo.** Cuando la capacidad reportada es
sospechosamente pequeña (menos de ~15 caracteres en una zona que claramente admite una línea),
compárala con `capacity_geom_chars` de la misma zona, que es la medida geométrica de la caja.

## G19 · La plantilla en producción embebía CALIBRI etiquetado como Movistar Sans

Encontrado el 2026-07-27 parseando la **cabecera EOT** de cada parte `.fntdata`, no la lista
declarada. `assets/template/movistar-template.pptx` —la plantilla que corría en producción— tiene
un `<p:embeddedFontLst>` impecable que declara `Movistar Sans`, `Movistar Sans Medium` y
`Movistar Sans Extrabold`… y 12 partes `.fntdata` que son **4 blobs de Calibri** repetidos:

```
EOT family  = "Calibri"  (Regular / Bold / Italic / Bold Italic)
PANOSE      = 020F0502020204030204        (= Calibri exacto)
version     = 0x00020002 · MicroType Express (comprimido) · fsType = 8
peso total  = 6,85 MB
```

**Impacto real**: en cualquier máquina sin Movistar Sans instalada, el deck se renderiza en
Calibri. Y PowerPoint no avisa, porque desde su punto de vista la fuente *está* embebida. Es un
fallo silencioso de marca en el peor sitio posible.

El rebuild v3 ya lo había corregido sin que nadie lo notara: `movistar.pptx` trae 10 EOT reales
(`Movistar Sans`/`Medium`/`Extrabold`, versión `0x00020001`, sin comprimir, `fsType=0`, 1,28 MB).
Es decir, **`_build_eot_bytes()` no es código redundante heredado de San Miguel: es el fix.** La
planificación del rebuild bi-master llegó a proponer eliminarlo, razonando que las fuentes del v9
estaban "probadas en producción" — lo estaban, pero eran incorrectas. Probado ≠ correcto.

**Cómo se comprueba** (`scripts/font_embed.py`):

```python
audit_embedded_fonts(pptx)   # lee la CABECERA EOT de cada blob y la cruza con la lista declarada
assert_brand_fonts(pptx)     # gate duro: familia real ∈ EXPECTED_FONT_FAMILIES, sin comprimir,
                             # fsType == 0, version == 0x00020001, sin blobs huérfanos
```

**Regla**: no des por buena una fuente embebida porque `<p:embeddedFontLst>` diga lo correcto.
Decodifica el blob. Es literalmente lo que ocultó este defecto.

## G20 · LibreOffice ignora las fuentes EOT embebidas y sustituye por una más ancha

> ⚠️ **CORREGIDO el 2026-07-27 (cierre del rebuild bi-master): esto YA NO ES CIERTO para la
> plantilla v4.** La afirmación de abajo se midió sobre los EOT de la plantilla VIEJA, que van
> **comprimidos con MicroType Express** (`0x00020002`, `fsType=8`, los 6,85 MB de Calibri de G19).
> LibreOffice no sabe descomprimir ese formato, así que los ignoraba. Los **10 EOT de la v4 van sin
> comprimir** (`0x00020001`, `fsType=0`, verificado con `font_embed.audit_embedded_fonts()`) y
> LibreOffice **sí los carga**.
>
> Evidencia medida, no impresión:
>
> - Movistar Sans **no está instalada** en la máquina de QA (ni en `C:\Windows\Fonts`, ni en el
>   registro, ni en las fuentes de usuario) y aun así el PDF que produce `soffice` **embebe**
>   `MovistarSans`, `MovistarSans-Bold` y `MovistarSansMedium-Bold`. El único `ArialMT` que aparece
>   es el glifo de viñeta `•`, que la fuente de marca no trae.
> - Sobre 24 titulares y párrafos idénticos de las mismas páginas en los dos PDF (LibreOffice y
>   PowerPoint vía COM `SaveAs(…, 32)`), la razón de anchos **LO/PowerPoint = 0,996 de media**, con
>   desviación máxima del 7,3 % en un solo caso (el titular de `INFOGRAFIA_GAUGES`). Nada parecido a
>   un 19,4 %.
>
> **Consecuencia práctica, que es la que importa: los desbordes que veas en un render de
> LibreOffice de la v4 son REALES.** Ya no valen como excusa. Tres de ellos se documentan en G31, y
> se confirmaron abriendo el fichero en PowerPoint de verdad.
>
> **Lo que sigue siendo cierto** es el efecto colateral: `soffice` pinta a veces el *prompt* del
> `slideLayout` debajo de la diapositiva («Click to edit Master text styles», visible en ~12
> páginas). Eso **no** lo hace PowerPoint (comparado página a página en `TIMELINE_MULTI_CLASICO`), y
> tampoco lo introduce el build: el `.pptx` original intacto del cliente presenta las mismas
> ocurrencias. Ese sí es ruido del renderizador.
>
> Y sigue en pie la regla de G10: **nunca** `Slide.Export()` de PowerPoint COM para rasterizar. Usa
> `SaveAs(ruta, 32)` (PDF) y rasteriza el PDF con `fitz`.

*Texto original, conservado para trazabilidad:* «Verificado el 2026-07-27 de forma directa: se
injertaron los 12 `.fntdata` en una copia de QA y los 53 renders salieron byte-idénticos a los de la
copia sin fuentes. Para "Movistar Sans" en negrita sustituye por Arial Black, un 19,4 % más ancha».
La medición era correcta; la generalización a *cualquier* plantilla, no.

## G25 · `set_table_data()` escribía texto INVISIBLE en las celdas que la plantilla dejaba vacías (FIJO v4.0.0)

Encontrado renderizando un deck real con `INTERIOR_TABLA`: la cabecera de la primera columna
(«Comunidad») **no aparecía**. No era el renderizador — está en el XML:

```xml
<!-- Tabla 7, celda (0,0) — tal como la entrega el cliente -->
<a:tc><a:txBody><a:p><a:r><a:t></a:t></a:r></a:p></a:txBody>
  <a:tcPr><a:noFill/></a:tcPr>   <!-- transparente: deja ver el fondo crema de la diapo -->
</a:tc>
```

La celda va **vacía por diseño** (la esquina de esa tabla no lleva rótulo) y por eso no tiene ningún
`rPr`. Al escribir en ella, el run nuevo hereda el color de la banda `firstRow` del estilo de tabla
`{5C22544A-…}` («Medium Style 2 – Accent 1»), que es `<a:schemeClr val="lt1"/>` = **Blanco Movistar
`FFFAF5`**… sobre un fondo `FFFAF5`. Contraste **1,00:1**.

Y no es un caso raro: `capability-recipe.md` manda rellenar **exactamente las 8×7 celdas** (§G16),
así que todo deck con esa tabla perdía ese rótulo.

**Fix** (`mvst_pptx.set_table_data()` → `_fix_illegible_cell_text()`): tras escribir, si el run no
tiene color propio, se resuelve la tinta heredada (bandas del estilo de tabla, en orden
`firstRow > lastRow > firstCol > lastCol > wholeTbl`) y el fondo efectivo (relleno propio de la
celda; si es `noFill` explícito, el `bg_hex` del arquetipo). **Solo si el contraste baja de 2:1** se
fija tinta legible por luminancia, y **solo el color**: tamaño y tipografía siguen heredándose como
los diseñó el cliente.

⚠️ **Dos trampas que costaron dos iteraciones y conviene no repetir:**

1. La primera versión copiaba el `rPr` de una celda hermana como "donante". Cambiaba el tamaño de
   fuente de 43 celdas que se veían perfectamente. Un gate de contraste no debe tocar tipografía.
2. El gris de las celdas de datos es `schemeClr tx1` con `lumMod 25% + lumOff 75%`. Sin aplicar esos
   modificadores se lee como Negro Movistar y **todas** las decisiones de contraste salen invertidas.
   `_apply_color_transforms()` implementa `lumMod`/`lumOff` (en el canal L de HSL) y `tint`/`shade`.

Comprobación: en el deck de QA salta **1 vez** (celda 0,0 de `Tabla 7`) y ninguna en las tablas del
sistema clásico — cuyo estilo solo define `wholeTbl` con tinta oscura, así que su esquina vacía ya
era legible. Verificado por render antes y después.

## G26 · La gráfica del refresh es una TARTA, y el fill-spec no lo decía (FIJO v4.0.0)

`INTERIOR_CHART` trae `chart_type: PIE` en el catálogo y su `use_when` dice «servida de origen como
tarta de seis porciones». Pero el fill-spec —que es lo único que `SKILL.md` autoriza a mirar— solo
imprimía `chart 1s×6c`. Con esa información, meter una serie temporal de seis años es la lectura
natural… y produce una tarta donde «2024 es el 12 % de todos los años», que no significa nada.
Ocurrió en el primer deck de QA de esta ronda.

**Fix**: el fill-spec imprime el tipo (`chart tarta 1s×6c`, `chart columnas 3s×4c`, `chart columnas
100% 2s×1c`) y `set_chart_data()` avisa si una gráfica de parte-de-un-total recibe categorías que
son años. Los 5 arquetipos con gráfica: `INTERIOR_CHART` y `DATOS_CHART_HERO_CLASICO` son tarta; los
otros 3, columnas.

## G27 · «Título de la gráfica»: el gate de título de ejemplo solo cubría una de las dos cadenas (FIJO v4.0.0)

La 3.2.4 añadió la retirada automática del título de gráfica sin editar, con un conjunto cerrado:
`{"chart title", "título del gráfico", "titulo del grafico"}`. La plantilla del cliente usa el
**femenino**: «Título de la gráfica». No estaba en la lista, y salía impreso en el deck entregado
(visto en el render de `DATOS_CHART_CLASICO`).

**Fix**: patrón `^(chart\s+title|t[íi]tulo\s+(de\s+la|del|de)\s+gr[áa]fic[ao])$` en vez de lista
cerrada. Barrido de los 5 arquetipos con gráfica: 2 cadenas distintas en 3 zonas, **las 2
detectadas**. Lección repetida: un conjunto cerrado de cadenas en español acaba fallando por el
género o el artículo.

## G28 · El sufijo `_N` de una familia de zonas no siempre es el orden visual (AVISO v4.0.0)

En `DATOS_DASHBOARD_6CHART_CLASICO` los seis porcentajes grandes se llaman `subtitulo_2..subtitulo_7`
pero, de izquierda a derecha, son **4, 5, 6, 3, 2, 7**. Rellenarlos en orden de sufijo —lo natural—
deja cada número sobre la barra y la etiqueta de OTRA columna. La diapositiva sale llena, maquetada y
creíble, **con los datos cambiados de sitio**: es el fallo más caro de todos porque no se ve.

El orden de lectura del fill-spec tampoco los ordenaba bien: cada número flota sobre su barra, a
distinta altura (`y` de 6,33 a 11,28 cm), así que caen en bandas distintas de `_reading_key()` y se
ordenan por banda antes que por `x`. Misma clase de defecto que `repsol-pptx` G9, pero dentro de una
sola fila.

**Aviso nuevo** (`_suffix_order_warnings()`): el fill-spec imprime el orden visual explícito. Solo
dispara en una FILA horizontal de zonas del mismo rol con `x` distintas (≥1 cm de separación), para
no señalar rejillas de dos filas como `GRID_MOSAICO_12_CLASICO`, donde `imagen_1..6` arriba y
`imagen_7..12` abajo es correcto. Barrido de los 156: **3 arquetipos** —
`DATOS_DASHBOARD_6CHART_CLASICO`, `AGENDA_5COL_OSCURO` (columnas 1 y 2 permutadas) y
`SEPARADOR_TITULO_5COL_04_CLASICO` (`etiqueta_4`/`etiqueta_5`). `AGENDA_5COL_CLARO` **no** está
afectada: su numeración sí va en orden.

## G29 · Zonas del mismo rol donde una contiene a otra: los anillos de `INFOGRAFIA_GAUGES` (AVISO v4.0.0)

`INFOGRAFIA_GAUGES` publica **7** zonas con rol `gauge_percent` para **5** indicadores:

| shape | x_cm | w_cm | qué es |
|---|---:|---:|---|
| `Oval 9__5` | 2,45 | 4,10 | anillo del gauge 1 — **no escribas aquí** |
| `Oval 9__4` | 8,64 | 4,10 | anillo del gauge 2 — **no escribas aquí** |
| `Oval 9__6` · `Oval 11` · `Oval 13` · `Oval 15` · `Oval 33` | 3,14 · 9,29 · 15,47 · 21,67 · 27,66 | 2,78 | los 5 círculos del número, columnas 1-5 |

Escribir en un anillo no lanza y no se ve (el círculo interior lo tapa), así que los cinco valores
quedan **corridos una posición** respecto a sus etiquetas. Ocurrió en el deck mixto de QA.

**Aviso nuevo** (`_covered_zone_warnings()`): si dos zonas de TEXTO del mismo rol se contienen, el
fill-spec dice cuál usar. Se limita a zonas de texto a propósito: en el dashboard el número grande
está *encima* de su gráfica por diseño y eso no es un texto tapado. Único arquetipo afectado de 156.

Nota relacionada: el **arco de color de cada gauge es arte estático**, no un dato. Cambiar el número
no mueve el arco. Si la cifra tiene que ser fiel al arco, usa `DATOS_DASHBOARD_6CHART_CLASICO`, cuyas
seis barras sí son gráficas nativas con datos.

## G30 · `set_texts({zona: None})` escribía la cadena literal "None" (FIJO v4.0.0)

`set_texts()` hacía `str(value)` sin filtrar, así que pasar `None` para "esta zona la relleno aparte"
—la forma natural de pasar el fill-spec completo dejando fuera las zonas de imagen— escribía **la
palabra "None"** en la diapositiva, sin ningún aviso. Ahora las zonas con valor `None` se omiten.

## G31 · Tres arquetipos del cliente cuyo propio texto de ejemplo desborda (no es el renderizador)

Confirmado en **PowerPoint real** y en LibreOffice, con el mismo resultado en los dos (ver la
corrección de G20). No son defectos del rebuild: el arte del cliente trae un texto-guía más largo de
lo que cabe. Con contenido real corto se ven bien; con contenido largo, no.

| Arquetipo | Qué pasa | Regla práctica |
|---|---|---|
| `INTERIOR_TXT_2PANEL_CLASICO` | el panel blanco redondeado se superpone al `titulo`: «Título de sección compues…» queda cortado a media palabra. La capacidad declarada (78, por geometría) no sabe del panel | máx. ~22 caracteres por línea (≈45 en dos líneas) |
| `GRID_3IMG_CAPTION_HERO_02_CLASICO` | la 2ª línea del `titulo` la pisa el borde superior de las fotos; un `cuerpo_N` de 2 líneas se sale de su placa blanca | `titulo` de UNA línea; `cuerpo_N` ≤ 39 y de una línea |
| `TIMELINE_MULTI_CLASICO` | con su propio ejemplo, `cuerpo_16..21` y `cuerpo_05/06` se solapan entre sí. Es el arquetipo más denso (27 zonas, 25 bloques) | respeta las capacidades al pie de la letra (`cuerpo_16..19` ≤ 30, `cuerpo_20/21` ≤ 10) o usa `TIMELINE_PROCESO_CLASICO` / `TIMELINE_TABLA_CLASICO` |

Las capacidades del catálogo son honestas (medidas por geometría); lo que desborda es el texto de
ejemplo del cliente, que las supera. `set_text()` avisa cuando te pasas: **hazle caso**.

## G32 · `INDICE_SIMPLE`: la numeración se desalinea si un tema ocupa dos líneas

La numeración (`1.` `2.` `3.`) y los temas viven en **dos cajas de texto distintas**, alineadas línea
a línea. Si un tema envuelve a dos líneas, la caja de temas crece y a partir de ahí cada número
apunta al tema equivocado — visible y feo. Mismo patrón en cualquier arquetipo con una columna de
numeración separada.

**Regla**: en `INDICE_SIMPLE`, cada tema en **una sola línea** (≈35-40 caracteres con la fuente
real). Si no cabe, usa `INDICE_3COL_CLASICO` o `AGENDA_5COL_*`, donde número y texto van juntos en la
misma columna.

## G33 · `AVISO_CONFIDENCIALIDAD` lleva una instrucción al autor impresa en la diapositiva

La diapositiva de aviso trae a pie de página: «Por favor, rellene el uso que considere en el espacio
reservado dentro de la presentación **como "inserte tipo uso seguridad"** ubicado en la parte
superior derecha de la diapositiva». Es una instrucción **para quien monta el deck** y se entrega al
cliente tal cual.

Dos cosas verificadas sobre el fichero (no supuestas):

1. El gate de texto-de-ejemplo **no puede verla**: la diapositiva solo tiene UNA forma con texto
   propio (`2 Marcador de contenido`, con «INSERTE TIPO USO SEGURIDAD», que sí es rellenable y sí
   está en el catálogo). Todo el resto del aviso —los cuatro cuadros de clasificación y esta
   instrucción, `TextBox 15`— vive en el **slideLayout** `Aviso`
   (`ppt/slideLayouts/slideLayout109.xml`), compartido.
2. Por eso **`remove_shape()` no sirve**: no hay nada que borrar en la diapositiva. Quitarlo exige
   editar el layout en `build_template.py`, lo que afecta a todos los decks.

No se toca en esta versión: es arte oficial del cliente y retirarlo es una decisión de diseño.
**Pendiente de confirmar con Silvia** (ver el handoff `dist/handoff/movistar-v4/`). Mientras tanto:
si el deck sale a un cliente externo, o no uses `AVISO_CONFIDENCIALIDAD`, o acepta que la línea
aparece — pero rellena siempre `2 Marcador de contenido` con la clasificación real, porque dejarla
como «INSERTE TIPO USO SEGURIDAD» es lo único que empeora la situación (y eso sí lo bloquea
`save()`).

## G34 · Dos `use()` del mismo arquetipo de gráfica compartían el `chart` part (FIJO)

Encontrado generando el deck de demostración de `dist/produccion-real/movistar-v4/`, no leyendo
código. Reproducido y verificado antes de tocar nada:

```
d = new_deck(); a = use(d, "INTERIOR_CHART"); b = use(d, "INTERIOR_CHART")
set_chart_data(a, "Chart Placeholder 26", ["A","B"], {"S":[10,20]})
set_chart_data(b, "Chart Placeholder 26", ["C","D"], {"S":[90,80]})
→ ANTES: las dos slides apuntaban a ppt/charts/chart9.xml, y el fichero entregado contenía
          ['S','C','D','90','80'] — los datos de la PRIMERA gráfica destruidos, sin ningún aviso.
          El deck salía con las dos gráficas mostrando los números de la última.
```

**Causa.** `_duplicate_slide()` re-ligaba TODAS las relaciones del original con
`dest.part.relate_to(rel.target_part, ...)`, es decir apuntando a la MISMA parte. Para una imagen
eso es correcto y deseable (es un blob de solo lectura, compartirlo ahorra peso). Para una gráfica
no: `chartN.xml` **lleva los datos dentro** y `set_chart_data()` lo reescribe.

Misma familia que **G5** (notesSlide compartida): una parte con estado propio que acaba compartida
entre clones. La lección general: *al clonar, pregúntate si la parte es de solo lectura o si el
motor la va a REESCRIBIR. Solo las primeras se comparten.*

**Fix** (`mvst_pptx.py::_clone_chart_part`): la relación `/chart` se re-liga a una **copia
independiente** del `chart` part, y con ella se duplica también su libro de Excel incrustado
(`/package`), porque `replace_data()` lo reescribe. `colors*.xml`/`style*.xml` sí se comparten (solo
lectura). Verificado: dos `chartN.xml` + dos `.xlsx`, cada slide con el suyo y con SUS datos.

**Gate permanente**: `verify_pptx.py` check 6c — un `chart` referenciado por 2+ slides es error.
Probado en negativo (desactivando el fix, `verify` sale exit 1 con el mensaje).

⚠️ Trampa al implementarlo: la firma real es `XmlPart.load(partname, content_type, package, blob)`.
Equivocar el orden **no falla al construir**: falla mucho después con un `AttributeError` opaco
(`'Package' object has no attribute 'chart'`). Compruébala con `inspect.signature`, no de memoria.

## G35 · `PORTADA_FOTO_BLEED_SCRIM` no tiene scrim (defecto de plantilla, conocido)

El nombre promete un velo que la diapositiva no lleva. Medido sobre el render con la mejor foto del
banco, el titular blanco queda en **1,7:1**. Se midió la luminancia bajo el titular de las 14 fotos
usables del banco: **solo 1 da contraste suficiente**, y es un bodegón de producto.

Ni `set_image()` ni `verify_deck()` miran el contraste **bajo el texto** al colocar una foto, así
que nada avisa: el deck se entrega con el titular ilegible. `needs_scrim: true` del catálogo dice
que *hace falta* scrim, no que *lo haya*.

Mientras no se añada el velo en `build_template.py`, para portada con foto usa
**`PORTADA_SPLIT_IMG`** (texto sobre fondo plano, foto en su propia mitad) o mide la luminancia de
la zona antes de aceptar la composición.

## G36 · `INTERIOR_CHART_L23`: etiquetas de dato ilegibles (defecto de plantilla, conocido)

Sus etiquetas de dato van en `accent3` (`#FFE99C`, amarillo claro) sobre crema `#FFFAF5` =
**1,19:1**, en todas las series. Consecuencia práctica: **el sistema vigente se queda sin gráfica de
columnas usable** — la otra que tiene (`INTERIOR_CHART`) es una tarta. Para columnas hay que ir a
`DATOS_CHART_CLASICO`, que es del sistema clásico (y cuya leyenda tiene layout manual de 4,9 × 0,6
cm: con nombres de serie de más de ~12 caracteres solo entran 2 de 3 y la tercera se recorta sin
avisar).

Arreglable en `build_template.py` recoloreando las etiquetas a `tx1`; requiere regenerar la
plantilla y un `templateFileId` nuevo, así que queda documentado y no parcheado en esta ronda.
