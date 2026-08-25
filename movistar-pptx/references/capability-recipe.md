# Recetas compactas — decks de capacidades Movistar

Usa una de estas recetas cuando la petición enumera muchas capacidades a la vez y quieres evitar
cualquier consulta. Los nombres de arquetipo y de zona están **verificados contra la plantilla y
usados en decks reales**; aun así, `use()` te imprime las zonas al clonar y ese listado manda.

**Hay una receta por sistema de diseño y no se mezclan.** Elige una y quédate en ella
(`SKILL.md` §DOS SISTEMAS).

> ⚠️ La receta anterior a la v4 usaba `COMPARATIVA_2_PANEL`, `COMPARATIVA_3_PANEL` y
> `TIMELINE_3_FASES` con zonas tipo `Synthetic Title` / `Panel 1 Body` / `Phase 1 Header`. **Esas
> zonas ya no existen**: eran composiciones dibujadas a mano con primitivas y se han sustituido por el
> arte REAL del cliente, que vive en el sistema clásico y tiene otros nombres de zona. Los nombres
> viejos siguen aceptándose como alias y `use()` avisa, pero el relleno cambia: usa la Receta B.

---

## Receta A — sistema **refresh** (12 diapositivas)

| # | Capacidad | Arquetipo | Zonas a rellenar |
|---:|---|---|---|
| 1 | Aviso legal | `AVISO_CONFIDENCIALIDAD` | `2 Marcador de contenido` |
| 2 | Portada con foto | `PORTADA_FOTO_BLEED_SCRIM` | `Text Placeholder 1/2` + `Picture 6` |
| 3 | Agenda | `INDICE_SIMPLE` | `Text Placeholder 3` (título), `1` (numeración), `2` (temas) |
| 4 | Separador cap. 01 | `SEPARADOR_NUMERO_06_AZUL` | `Title 1`, `Text Placeholder 3` (número) |
| 5 | Idea + foto | `INTERIOR_TXT_1IMG` | cabecera, `Text Placeholder 4`, `Content Placeholder 8` |
| 6 | Idea sin foto | `TITULAR_GRANDE` | cabecera, `Text Placeholder 4` |
| 7 | Gráfico | `INTERIOR_CHART` | cabecera, `Text Placeholder 4`, `Chart Placeholder 26` (1 serie × 6 cat.) |
| 8 | Tabla | `INTERIOR_TABLA` | cabecera, `Text Placeholder 4`, `Tabla 7` (**exactamente 8×7**) |
| 9 | Galería de 3 fotos | `GRID_3IMG_CAPTION` | `Title 1`, `Text Placeholder 4/6/8`, `Picture Placeholder 40`, `40__2`, `40__3` |
| 10 | Dos columnas de texto | `TITULAR_2COL` | `titulo`, `entradilla_1/2`, `subtitulo_1/2`, `cuerpo_1/2` |
| 11 | Cita | `QUOTE_PLANO` | `Content Placeholder 11` (≤38), `Content Placeholder 5` (autor) |
| 12 | Cierre | `CIERRE_M` | no se rellena |

**El refresh no tiene comparativas ni timeline.** Si la petición los exige, o usas la Receta B
completa, o aceptas explícitamente la mezcla de sistemas (y `verify_deck()` lo avisará si el clásico
queda por debajo del 25% del deck).

```python
# Gráfico editable sin tocar estilos: 1 serie, 6 categorías (lo que trae diseñado).
set_chart_data(chart_slide, "Chart Placeholder 26",
               ["2026", "2027", "2028", "2029", "2030", "Resto"],
               {"Hogares (miles)": [120, 310, 470, 260, 140, 60]})

# Tabla: rellena las 8x7 celdas. Menos filas/columnas dejan bandas de color vacías (G16).
set_table_data(table_slide, "Tabla 7", [
    ["Provincia", "Municipios", "Hogares", "Inicio", "Fin", "Inversión", "Estado"],
    # … 7 filas más
])
```

---

## Receta B — sistema **clásico** (14 diapositivas, cobertura completa)

Es la receta que cubre TODAS las capacidades sin mezclar sistemas: el clásico es el que tiene
comparativas, planogramas y dashboards de verdad.

| # | Capacidad | Arquetipo | Zonas a rellenar |
|---:|---|---|---|
| 1 | Portada de color | `PORTADA_TITULO_CLASICO_AZUL` | `titulo`, `subtitulo` |
| 2 | Índice de 3 capítulos | `INDICE_3COL_CLASICO` | `titulo`, `numero_1..3`, `etiqueta_1..3`, `cuerpo_1..3` |
| 3 | Separador cap. 01 | `SEPARADOR_TITULO_CLASICO_AZUL` | `titulo`, `subtitulo`, `numero` |
| 4 | Idea a texto | `INTERIOR_TXT_CLASICO` | `antetitulo`, `titulo`, `cuerpo` |
| 5 | Tres tarjetas de color | `INTERIOR_TXT_3IMG_CAPTION_CLASICO` | `antetitulo`, `titulo`, `cuerpo_1`, `cuerpo_2/3/4` (¡son tarjetas, ver abajo!) |
| 6 | Foto ancha | `INTERIOR_FOTO_ANCHO_CLASICO` | `antetitulo`, `titulo`, `subtitulo`, `imagen` |
| 7 | Separador cap. 02 | `SEPARADOR_TITULO_CLASICO_VERDE` | `titulo`, `subtitulo`, `numero` |
| 8 | Gráfico | `DATOS_CHART_CLASICO` | `antetitulo`, `titulo`, `cuerpo`, `grafico` (**3 series × 4 cat.**) |
| 9 | Tabla | `DATOS_TABLA_CLASICO` | `antetitulo`, `titulo`, `subtitulo`, `tabla` (**exactamente 6×8**) |
| 10 | Separador cap. 03 | `SEPARADOR_TITULO_CLASICO_AMARILLO` | `titulo`, `subtitulo`, `numero` |
| 11 | Comparativa de 2 | `COMPARATIVA_2_PANEL_CLASICO` | `antetitulo`, `titulo`, `numero_1/2`, `etiqueta_1/2`, `cuerpo_1/2` |
| 12 | Mosaico de 3 fotos | `GRID_MOSAICO_3_CLASICO` | `antetitulo`, `titulo`, `subtitulo`, `imagen_1/2/3` (traen foto SEMILLA: **sustitúyelas**) |
| 13 | Frase protagonista | `TITULAR_IDEA_CLASICO` | `antetitulo`, `frase` (≤48) — sin zona de título |
| 14 | Cierre | `CIERRE_M_CLASICO_AZUL` | no se rellena |

Variantes para cambiar de capacidad sin salir del sistema: comparativa de 3 →
`COMPARATIVA_3_PANEL_CLASICO`; timeline → `TIMELINE_PROCESO_CLASICO` (planograma de bandas, 47 zonas)
o `TIMELINE_TABLA_CLASICO` (tabla de fases, mucho más manejable); dashboard →
`DATOS_DASHBOARD_6CHART_CLASICO` (6 gráficas, usa `set_charts_data()`).

```python
# 3 series x 4 categorias: es lo que la grafica trae diseñado. Con más series, las extra salen
# con la paleta por defecto de Office (fallo de marca silencioso) y set_chart_data() avisa.
set_chart_data(s, "grafico", ["2022", "2023", "2024", "2025"],
               {"Centrales cerradas": [284, 612, 588, 430],
                "Bastidores retirados": [3100, 6800, 6400, 4900],
                "MWh ahorrados": [1200, 2900, 2700, 2100]})

# Las 6 graficas del dashboard, en una llamada:
set_charts_data(s, {f"grafico_{i}": (["Sí", "No"], {"Peso": [70, 30]}) for i in range(1, 7)})
```

### ⚠️ Las zonas `imagen_N` de los dos `*_CAPTION_CLASICO` NO son huecos de foto

Son **tarjetas de color secundario claro** con su propio texto encima (`cuerpo_2`, `cuerpo_3`,
`cuerpo_4`), escrito en el secundario oscuro correspondiente. El `_CAPTION` del nombre es un artefacto
del heurístico de nombrado. Ponerles una foto deja ese texto sin fondo de contraste, así que
`set_image()` se niega y te lo explica. **Rellena su texto y no toques la tarjeta.** Detalle en
`GOTCHAS.md` G18.

---

## Cosas que valen para las dos recetas

- **Todas las diapositivas de contenido llevan `set_page_header()`** (excepto las que el fill-spec
  marca como "sin zona de título": `TITULAR_IDEA_CLASICO`, `QUOTE_PLANO_CLASICO_*`, los cierres).
- **Los números que coinciden con el ejemplo por diseño** (`"01"` de un separador, la numeración
  `1./2./3.` de `INDICE_SIMPLE`) ya no bloquean `save()`: solo generan un aviso. Si quieres silenciarlo,
  `confirm_example_text(s, shape_name)`.
- **El orden en que `use()` imprime las zonas es el orden de LECTURA de la diapositiva.** Rellena
  siguiéndolo: en varios arquetipos multi-columna el orden interno de los shapes no coincide con el
  visual y asignar por nombre "en orden" permuta los bloques sin que se note (`GOTCHAS.md` G21).
- **Filtra el banco de fotos**: `list_brand_images(with_meta=True)` y descarta `categoria == "fondo"`
  (12 de 35 son fondos de color plano con el claim de marca, no fotografía).
- Guarda **una sola vez** al final y conserva el mismo nombre de archivo en las iteraciones.
