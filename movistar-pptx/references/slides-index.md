# Índice de diapositivas — Movistar PPTX (catálogo v4)

> **AUTOGENERADO** por `scripts/build_catalog.py` en la misma pasada que `slides-catalog-movistar.json`. No lo edites a mano: se regenera y perderías el cambio. Se genera para que no pueda desviarse del catálogo — y cualquier umbral que aparezca aquí sale de `assets/brand-config.json`, nunca de la memoria de nadie.

**156 arquetipos · 127 composiciones · 12 familias · 2 sistemas de diseño en un mismo `.pptx`.**

## Cómo se lee

Una fila por **composición** (la maqueta física); las variantes de color o de espejo de la misma composición van en la columna **Variantes**, porque son intercambiables sin recolocar nada. Para clonar usa el nombre completo: la base, o la base + `_` + el sufijo de la variante.

| Marca | Significa |
|---|---|
| `[C]` | Es la elección **por defecto** de su familia: úsala si no tienes una razón para otra. |
| Sistema `refresh` | Sistema **vigente** (refresh-2025). Sus nombres van **sin sufijo**. Es el que ve un humano al pulsar «Nueva diapositiva». |
| Sistema `clásico` | Segundo `slideMaster` (clasico). Sus nombres llevan siempre `_CLASICO`. No los mezcles con los del refresh en el mismo deck sin un motivo: son dos lenguajes visuales distintos. |
| Zonas | Zonas rellenables: `txt` texto · `img` foto · `chart` gráfica nativa · `tabla` tabla nativa. |
| n_items | Cuántos bloques repetidos tiene la maqueta (columnas, fases, tarjetas). Si dice `5 columnas`, hacen falta exactamente 5. |

La gramática de los nombres está en [`naming-grammar.md`](naming-grammar.md); el detalle de cada zona (shape_name exacto, geometría, tipografía, `max_chars_approx`) en [`slides-catalog-movistar.json`](slides-catalog-movistar.json), que lee el motor.

## Umbrales del deck (derivados de `assets/brand-config.json`)

- Longitud recomendada del deck: **8–18 diapositivas**.
- `verify_deck()` avisa si un mismo arquetipo pasa del **30%** del deck (`max_dominant_slide_ratio`) o si los divisores pasan del **25%** (`max_divider_ratio`).
- Debe abrir con `cover` y cerrar con `closing`.
- Capacidad de texto: holgura ×1.15 sobre el ejemplo cuando lo calibró el cliente (`capacity_source: medida`), ×1.5 sobre la capacidad medida de la caja cuando el ejemplo lo generó el build (`geometria`).

## AVISO — marca de confidencialidad / clasificación de la información

1 composición · 1 arquetipo · por defecto **`AVISO_CONFIDENCIALIDAD`** · ⚠️ sin zona de título: usa `set_text()`, no `set_page_header()`

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`AVISO_CONFIDENCIALIDAD`** `[C]` | 1 txt | — | — | refresh |

## PORTADA — abrir el deck

18 composiciones · 26 arquetipos · por defecto **`PORTADA_TITULO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`PORTADA_TITULO`** `[C]` | 2 txt | — | — | refresh |
| **`PORTADA_TITULO_1PORTADA`** | 2 txt | — | — | refresh |
| **`PORTADA_TITULO_2PORTADA`** | 2 txt | — | — | refresh |
| **`PORTADA_FOTO_MARGEN`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_FOTO_MARGEN_SUBTITULO`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_FOTO_BLEED_SCRIM`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_FOTO_BLEED_SCRIM_MEDIO`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_FOTO_MARGEN_1PORTADA`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_SPLIT_IMG`** | 2 txt · 1 img | — | `ESPEJO` | refresh |
| **`PORTADA_SPLIT_IMG_04`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_02_SPLIT`** | 2 txt · 1 img | — | `ESPEJO` | refresh |
| **`PORTADA_02_SPLIT_03`** | 2 txt · 1 img | — | — | refresh |
| **`PORTADA_FOTO_MARGEN_CLASICO`** | 2 txt · 1 img | — | — | clásico |
| **`PORTADA_FOTO_MARGEN_SUBTITULO_CLASICO`** | 2 txt · 1 img | — | — | clásico |
| **`PORTADA_TITULO_SOLO_CLASICO`** | 1 txt | — | — | clásico |
| **`PORTADA_TITULO_CLASICO_*`** | 2 txt | — | `VERDE` · `CORAL` · `AMARILLO` · `AZULCLARO` · `CREMA` · `AZUL` | clásico |
| **`PORTADA_SPLIT_IMG_CLASICO_*`** | 2 txt · 1 img | — | `AZULCLARO` · `AZUL` | clásico |
| **`PORTADA_FOTO_SANGRE_CLASICO`** | 2 txt · 1 img | — | — | clásico |

## INDICE — índice / agenda

6 composiciones · 6 arquetipos · por defecto **`INDICE_SIMPLE`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`INDICE_MULTI`** | 19 txt | — | — | refresh |
| **`INDICE_SIMPLE`** `[C]` | 3 txt | — | — | refresh |
| **`AGENDA_5COL_CLARO`** | 11 txt | — | — | refresh |
| **`AGENDA_5COL_OSCURO`** | 11 txt | — | — | refresh |
| **`INDICE_3COL_CLASICO`** | 10 txt | 9 columnas | — | clásico |
| **`INDICE_5COL_CLASICO`** | 16 txt | 15 columnas | — | clásico |

## SEPARADOR — abrir capítulo o sección

32 composiciones · 42 arquetipos · por defecto **`SEPARADOR_TITULO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`SEPARADOR_TITULO`** | 1 txt | — | `AZUL` · `AMARILLO` | refresh |
| **`SEPARADOR_NUMERO_01`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_02_CORAL`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_03_AMARILLO`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_04_VERDE`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_05_AZULCLARO`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_06_AZUL`** | 2 txt | — | — | refresh |
| **`SEPARADOR_NUMERO_07_NEGRO`** | 2 txt | — | — | refresh |
| **`SEPARADOR_PALABRA_IMAGINA_AZUL`** | 1 txt | — | — | refresh |
| **`SEPARADOR_PALABRA_INSPIRA_NEGRO`** | 1 txt | — | — | refresh |
| **`SEPARADOR_PALABRA_INNOVA_CORAL`** | 1 txt | — | — | refresh |
| **`SEPARADOR_PALABRA_SUENA_CREMA`** | 1 txt | — | — | refresh |
| **`SEPARADOR_PALABRA_CREA_VERDE`** | 1 txt | — | — | refresh |
| **`SEPARADOR_NUMERADA_5COL_MULTI_CLASICO`** | 16 txt | 15 columnas | — | clásico |
| **`SEPARADOR_NUMERADA_5COL_01_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_NUMERADA_5COL_02_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_NUMERADA_5COL_03_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_NUMERADA_5COL_04_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_NUMERADA_5COL_05_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_TITULO_5COL_01_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_TITULO_5COL_02_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_TITULO_5COL_03_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_TITULO_5COL_04_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_TITULO_5COL_05_CLASICO`** | 8 txt | 5 columnas | — | clásico |
| **`SEPARADOR_FOTO_5COL_01_CLASICO`** | 6 txt · 1 img | 5 columnas | — | clásico |
| **`SEPARADOR_FOTO_5COL_02_CLASICO`** | 6 txt · 1 img | 5 columnas | — | clásico |
| **`SEPARADOR_FOTO_5COL_03_CLASICO`** | 6 txt · 1 img | 5 columnas | — | clásico |
| **`SEPARADOR_FOTO_5COL_04_CLASICO`** | 6 txt · 1 img | 5 columnas | — | clásico |
| **`SEPARADOR_FOTO_5COL_05_CLASICO`** | 6 txt · 1 img | 5 columnas | — | clásico |
| **`SEPARADOR_NUMERO_CLASICO_*`** | 2 txt | — | `NEGRO` · `VERDE` · `CORAL` · `AMARILLO` · `AZULCLARO` | clásico |
| **`SEPARADOR_TITULO_CLASICO_*`** | 3 txt | — | `AZUL` · `VERDE` · `CORAL` · `AMARILLO` · `AZULCLARO` | clásico |
| **`SEPARADOR_TITULO_02_CLASICO_AZUL`** | 3 txt | — | — | clásico |

## TITULAR — una idea sin foto / cifra hero

3 composiciones · 3 arquetipos · por defecto **`TITULAR_GRANDE`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`TITULAR_GRANDE`** `[C]` | 3 txt | — | — | refresh |
| **`TITULAR_2COL`** | 7 txt | 2 columnas | — | refresh |
| **`TITULAR_IDEA_CLASICO`** | 2 txt | — | — | clásico |

## INTERIOR — idea + foto, el cuerpo del deck

30 composiciones · 34 arquetipos · por defecto **`INTERIOR_TXT_1IMG`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`INTERIOR_TXT_IMG_REDONDA_AZUL`** | 3 txt | — | — | refresh |
| **`INTERIOR_TXT_2IMG`** | 3 txt · 2 img | — | — | refresh |
| **`INTERIOR_TXT_1IMG`** `[C]` | 3 txt · 1 img | — | — | refresh |
| **`INTERIOR_TXT_2IMG_STACK`** | 3 txt · 2 img | — | — | refresh |
| **`INTERIOR_TXT_DEVICE`** | 3 txt · 3 img | — | — | refresh |
| **`INTERIOR_CHART`** | 3 txt · 1 chart | — | — | refresh |
| **`INTERIOR_TABLA`** | 2 txt · 1 tabla | — | — | refresh |
| **`INTERIOR_CHART_L23`** | 2 txt · 1 chart | — | — | refresh |
| **`INTERIOR_TXT_CLASICO`** | 3 txt | — | — | clásico |
| **`INTERIOR_TXT_2COL_CLASICO`** | 4 txt | 2 columnas | — | clásico |
| **`INTERIOR_TXT_4COL_CLASICO`** | 6 txt | 4 columnas | — | clásico |
| **`INTERIOR_TXT_5COL_CLASICO`** | 7 txt | 5 columnas | — | clásico |
| **`INTERIOR_TXT_6PANEL_CLASICO`** | 9 txt | 7 columnas | — | clásico |
| **`INTERIOR_TXT_3IMG_CAPTION_CLASICO`** | 6 txt | 4 columnas | — | clásico |
| **`INTERIOR_TXT_2IMG_CAPTION_CLASICO`** | 5 txt | 3 columnas | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_MEDIO_HERO_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_FOTO_ANCHO_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_2IMG_CLASICO`** | 3 txt · 2 img | — | — | clásico |
| **`INTERIOR_TXT_6STACK_1IMG_DER_CLASICO`** | 7 txt · 1 img | 6 filas | — | clásico |
| **`INTERIOR_TXT_2PANEL_CLASICO`** | 4 txt | 2 columnas | — | clásico |
| **`INTERIOR_TXT_PLANO_CLASICO_*`** | 3 txt | — | `VERDE` · `CORAL` · `AMARILLO` · `AZULCLARO` | clásico |
| **`INTERIOR_TXT_1IMG_DER_ANCHO_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_SANGRE_CLASICO_*`** | 3 txt · 1 img | — | `CREMA` · `VERDE` | clásico |
| **`INTERIOR_TXT_SANGRE_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_FOTO_MARGEN_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_3IMG_STACK_CLASICO`** | 3 txt · 3 img | — | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_MEDIO_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_COMPACTA_PANEL_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_ANCHO_PANEL_CLASICO`** | 3 txt · 1 img | — | — | clásico |
| **`INTERIOR_TXT_1IMG_DER_COMPACTA_FOTO_CLASICO`** | 3 txt · 1 img | — | — | clásico |

## GRID — mosaico / galería de fotos con pie

18 composiciones · 19 arquetipos · por defecto **`GRID_3IMG_CAPTION`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`GRID_2IMG_CAPTION`** | 3 txt · 2 img | — | — | refresh |
| **`GRID_3IMG_CAPTION`** `[C]` | 4 txt · 3 img | — | — | refresh |
| **`GRID_MOSAICO_15`** | 16 txt · 15 img | — | — | refresh |
| **`GRID_2IMG_CAPTION_ANCHO_CLASICO`** | 5 txt · 2 img | 2 columnas | — | clásico |
| **`GRID_MOSAICO_2_CLASICO_*`** | 3 txt · 2 img | — | `CREMA` · `CORAL` | clásico |
| **`GRID_2IMG_CAPTION_MEDIO_CLASICO`** | 6 txt · 2 img | 4 columnas | — | clásico |
| **`GRID_3IMG_CAPTION_HERO_CLASICO`** | 8 txt · 3 img | 6 columnas | — | clásico |
| **`GRID_3IMG_CAPTION_HERO_02_CLASICO`** | 8 txt · 3 img | 6 columnas | — | clásico |
| **`GRID_3IMG_CAPTION_COMPACTA_CLASICO`** | 8 txt · 3 img | 6 columnas | — | clásico |
| **`GRID_4IMG_CAPTION_COMPACTA_CLASICO`** | 10 txt · 4 img | 8 columnas | — | clásico |
| **`GRID_MOSAICO_12_CLASICO`** | 3 txt · 12 img | — | — | clásico |
| **`GRID_6IMG_CAPTION_COMPACTA_LADO_CLASICO`** | 15 txt · 6 img | 12 columnas | — | clásico |
| **`GRID_6IMG_CAPTION_COMPACTA_CLASICO`** | 15 txt · 6 img | 12 columnas | — | clásico |
| **`GRID_MOSAICO_6_CLASICO`** | 3 txt · 6 img | — | — | clásico |
| **`GRID_3IMG_CAPTION_ANCHO_CLASICO`** | 9 txt · 3 img | 6 columnas | — | clásico |
| **`GRID_MOSAICO_3_CLASICO`** | 3 txt · 3 img | — | — | clásico |
| **`GRID_2IMG_CAPTION_ANCHO_TITULO_CLASICO`** | 7 txt · 2 img | 4 columnas | — | clásico |
| **`GRID_MOSAICO_2_MARGEN_CLASICO_CREMA`** | 3 txt · 2 img | — | — | clásico |

## DATOS — gráfico, tabla, KPI, dashboard

5 composiciones · 5 arquetipos · por defecto **`DATOS_CHART_CLASICO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`INFOGRAFIA_GAUGES`** | 19 txt | — | — | refresh |
| **`DATOS_CHART_CLASICO`** `[C]` | 3 txt · 1 chart | — | — | clásico |
| **`DATOS_CHART_HERO_CLASICO`** | 4 txt · 1 chart | — | — | clásico |
| **`DATOS_DASHBOARD_6CHART_CLASICO`** | 21 txt · 6 chart | 12 columnas | — | clásico |
| **`DATOS_TABLA_CLASICO`** | 3 txt · 1 tabla | — | — | clásico |

## QUOTE — cita o frase protagonista

3 composiciones · 7 arquetipos · por defecto **`QUOTE_PLANO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`QUOTE_PLANO`** `[C]` | 2 txt | — | — | refresh |
| **`QUOTE_FOTO`** | 2 txt · 1 img | — | — | refresh |
| **`QUOTE_PLANO_CLASICO_*`** | 1 txt | — | `CREMA` · `VERDE` · `CORAL` · `AMARILLO` · `AZULCLARO` | clásico |

## COMPARATIVA — paneles enfrentados

2 composiciones · 2 arquetipos · por defecto **`COMPARATIVA_2_PANEL_CLASICO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`COMPARATIVA_2_PANEL_CLASICO`** `[C]` | 8 txt | 6 columnas | — | clásico |
| **`COMPARATIVA_3_PANEL_CLASICO`** | 14 txt | 12 columnas | — | clásico |

## TIMELINE — cronología / roadmap

3 composiciones · 3 arquetipos · por defecto **`TIMELINE_PROCESO_CLASICO`**

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`TIMELINE_PROCESO_CLASICO`** `[C]` | 47 txt | 7 columnas | — | clásico |
| **`TIMELINE_TABLA_CLASICO`** | 2 txt · 1 tabla | — | — | clásico |
| **`TIMELINE_MULTI_CLASICO`** | 27 txt | 25 columnas | — | clásico |

## CIERRE — cerrar el deck

6 composiciones · 8 arquetipos · por defecto **`CIERRE_M`** · ⚠️ sin zona de título: usa `set_text()`, no `set_page_header()`

| Composición | Zonas | n_items | Variantes (sufijo) | Sistema |
|---|---|---|---|---|
| **`CIERRE_M`** `[C]` | 0 txt | — | — | refresh |
| **`CIERRE_M_V2`** | 0 txt | — | — | refresh |
| **`CIERRE_M_CLASICO_*`** | 0 txt | — | `AZUL` · `NEGRO` | clásico |
| **`CIERRE_TELEFONICA_CLASICO_AZUL`** | 0 txt | — | — | clásico |
| **`CIERRE_M_TELEFONICA_CLASICO_AZUL`** | 0 txt | — | — | clásico |
| **`CIERRE_TITULO_CLASICO_*`** | 1 txt | — | `AZUL` · `NEGRO` | clásico |

## Alias aceptados como entrada

`use()`, `describe()` y `find_slides()` los resuelven al nombre canónico; `slide_names()` devuelve solo los canónicos.

| Alias | Resuelve a | Por qué |
|---|---|---|
| `DATOS_CHART` | `INTERIOR_CHART` | el nombre histórico no sigue la gramática actual |
| `DATOS_CHART_ANCHO` | `INTERIOR_CHART_L23` | el nombre histórico no sigue la gramática actual |
| `DATOS_GAUGES_5KPI` | `INFOGRAFIA_GAUGES` | el nombre histórico no sigue la gramática actual |
| `DATOS_TABLA` | `INTERIOR_TABLA` | el nombre histórico no sigue la gramática actual |
| `INDICE_5COL_AZUL` | `AGENDA_5COL_CLARO` | el nombre histórico no sigue la gramática actual |
| `INDICE_5COL_NEGRO` | `AGENDA_5COL_OSCURO` | el nombre histórico no sigue la gramática actual |
| `INTERIOR_TXT_2IMG_LADO` | `INTERIOR_TXT_2IMG` | el nombre histórico no sigue la gramática actual |
| `PORTADA_FOTO_SCRIM` | `PORTADA_FOTO_BLEED_SCRIM` | el nombre histórico no sigue la gramática actual |
| `PORTADA_FOTO_SCRIM_MEDIO` | `PORTADA_FOTO_BLEED_SCRIM_MEDIO` | el nombre histórico no sigue la gramática actual |
| `SEPARADOR_PALABRA_AZUL` | `SEPARADOR_PALABRA_IMAGINA_AZUL` | el nombre histórico no sigue la gramática actual |
| `SEPARADOR_PALABRA_CORAL` | `SEPARADOR_PALABRA_INNOVA_CORAL` | el nombre histórico no sigue la gramática actual |
| `SEPARADOR_PALABRA_CREMA` | `SEPARADOR_PALABRA_SUENA_CREMA` | el nombre histórico no sigue la gramática actual |
| `SEPARADOR_PALABRA_NEGRO` | `SEPARADOR_PALABRA_INSPIRA_NEGRO` | el nombre histórico no sigue la gramática actual |
| `SEPARADOR_PALABRA_VERDE` | `SEPARADOR_PALABRA_CREA_VERDE` | el nombre histórico no sigue la gramática actual |
| `TITULAR_IDEA` | `TITULAR_GRANDE` | el nombre histórico no sigue la gramática actual |
| `COMPARATIVA_2_PANEL` | `COMPARATIVA_2_PANEL_CLASICO` | **obsoleto**: era una composición dibujada a mano; ahora se sirve el arte real del cliente |
| `COMPARATIVA_3_PANEL` | `COMPARATIVA_3_PANEL_CLASICO` | **obsoleto**: era una composición dibujada a mano; ahora se sirve el arte real del cliente |
| `TIMELINE_3_FASES` | `TIMELINE_PROCESO_CLASICO` | **obsoleto**: era una composición dibujada a mano; ahora se sirve el arte real del cliente |

