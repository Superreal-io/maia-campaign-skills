# Gramática de nombres de arquetipo — Movistar PPTX v4

> La verdad ejecutable de este documento vive en [`scripts/_contracts.py`](../scripts/_contracts.py)
> (`FAMILIES`, `VARIANT_COLORS`, `MODIFIERS`, `parse_name()`). `build_catalog.py` valida cada
> nombre contra ese módulo y **falla el build** si no encaja. Este fichero explica el porqué.

## Por qué hace falta una gramática

A 54 arquetipos el nombre podía ser descriptivo-libre. A ~157 el nombre **es la interfaz
principal** con el modelo: si es predecible, el modelo deduce el arquetipo correcto sin abrir
ningún fichero; si no lo es, tiene que buscarlo, y buscar cuesta tokens y tiempo dentro del
límite de 20 minutos de SuperStudio.

## La regla

```
NOMBRE := FAMILIA [ "_" TOKEN ]* [ "_" SISTEMA ] [ "_" VARIANTE ]
```

| Parte | Vocabulario | Notas |
|---|---|---|
| **FAMILIA** | **cerrado, 14**: `AVISO · PORTADA · INDICE · SEPARADOR · TITULAR · INTERIOR · GRID · DATOS · QUOTE · LISTA · PASOS · COMPARATIVA · TIMELINE · CIERRE` | Siempre el primer token |
| **TOKEN** | modificadores (`STACK`, `SANGRE`, `SCRIM`, `SPLIT`, `DER`/`IZQ`…) o **cardinalidad** (`2IMG`, `3COL`, `5KPI`, `6CHART`, `01`…) | Regla dura: si dos arquetipos difieren **solo** en cuántos bloques tienen, el número va en el nombre |
| **SISTEMA** | `CLASICO` o ausente | **Ausente = sistema vigente** (`250917`, el refresh). `CLASICO` = el segundo `slideMaster` (v9) |
| **VARIANTE** | **cerrado**: `AZUL · AZULCLARO · AZULOSCURO · VERDE · VERDEOSCURO · AMARILLO · CORAL · NEGRO · CREMA · BLANCO · ESPEJO` | Siempre el último token |

Ejemplos válidos: `QUOTE_CLASICO_VERDE` · `SEPARADOR_NUMERO_04_VERDE` ·
`INTERIOR_TXT_2IMG_STACK` · `DATOS_DASHBOARD_6CHART_CLASICO_02` · `PORTADA_SPLIT_IMG_ESPEJO`.

## El sufijo cromático es DERIVADO, no tecleado

El token de variante sale de resolver el `<p:bg>` de la diapositiva y buscarlo en
`SEMANTIC_BY_HEX`. Nadie escribe "esta es la verde": el build lo deduce del binario. Por eso el
naming definitivo ocurre **después** de la normalización de paleta — antes, el mismo verde
tendría tres hexes distintos según de qué plantilla venga.

`build_catalog.py` comprueba además que la variante declarada en el manifiesto coincide con la
derivada del fondo. Si no coinciden, el build falla: es la señal de que alguien tecleó un
nombre a mano.

## Los 54 heredados NO se renombran

Movistar es la única marca del catálogo con tráfico real en producción. Renombrar rompería
`SKILL.md`, `capability-recipe.md`, cualquier prompt guardado en SuperStudio y —lo que más
importa— el *prior* del propio modelo, que ya ha visto esos nombres. El beneficio sería
cosmético.

Los 54 nombres actuales siguen siendo los **canónicos** y quedan exentos de la validación
estricta (`LEGACY_CANONICAL`). Los que la gramática nombraría de otra forma tienen un **alias
resoluble** (`STRICT_ALIASES`), aceptado como entrada por `use()`, `describe()` y
`find_slides()`:

| Alias que el modelo deduciría | Canónico real |
|---|---|
| `DATOS_CHART` · `DATOS_CHART_ANCHO` · `DATOS_TABLA` · `DATOS_GAUGES_5KPI` | `INTERIOR_CHART` · `INTERIOR_CHART_L23` · `INTERIOR_TABLA` · `INFOGRAFIA_GAUGES` |
| `INDICE_5COL_AZUL` · `INDICE_5COL_NEGRO` | `AGENDA_5COL_CLARO` · `AGENDA_5COL_OSCURO` |
| `SEPARADOR_PALABRA_{AZUL,NEGRO,CORAL,CREMA,VERDE}` | `SEPARADOR_PALABRA_{IMAGINA_AZUL,INSPIRA_NEGRO,INNOVA_CORAL,SUENA_CREMA,CREA_VERDE}` |
| `PORTADA_FOTO_SCRIM` · `_MEDIO` | `PORTADA_FOTO_BLEED_SCRIM` · `_MEDIO` |
| `TITULAR_IDEA` · `INTERIOR_TXT_2IMG_LADO` | `TITULAR_GRANDE` · `INTERIOR_TXT_2IMG` |

`slide_names()` devuelve **solo** los canónicos; `slide_names(include_aliases=True)` los dos.

> Los `SEPARADOR_PALABRA_*` son el peor caso heredado: codifican la palabra de *contenido*
> (IMAGINA, INSPIRA, INNOVA…) en el nombre del arquetipo, cuando el único eje real es el color
> de fondo. El alias lo corrige sin romper nada.

## Tres arquetipos obsoletos

`COMPARATIVA_2_PANEL`, `COMPARATIVA_3_PANEL` y `TIMELINE_3_FASES` se dibujaron a mano con
primitivas de python-pptx porque, cuando se construyó la v3, la skill solo miraba una de las
dos plantillas del cliente. El arte real existía en la otra (`2 Panel`, `3 Panel`,
`Panagrama 03`). Ahora se sirven desde ese arte real: los nombres viejos siguen resolviendo
(`DEPRECATED_ALIASES`) con un aviso, durante una versión.

## Si necesitas un token nuevo

Se añade a `MODIFIERS` en `_contracts.py` y se re-ejecuta el build. **Nunca** se hardcodea en
una pieza suelta: el vocabulario cerrado es lo único que impide que 157 nombres se conviertan
en 157 criterios distintos.
