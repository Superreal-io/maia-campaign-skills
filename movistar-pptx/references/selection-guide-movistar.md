# Índice de selección — RETIRADO en la v4

> **Este fichero ya no es un índice de arquetipos.** Se conserva solo como redirección, porque
> `SKILL.md` y prompts guardados en SuperStudio lo citaban por su ruta.

## Por qué se retiró

Era un índice **escrito a mano** de los 54 arquetipos de la v3. A 156 arquetipos en dos sistemas de
diseño, un segundo catálogo mantenido a mano no se sostiene: cada arquetipo nuevo obliga a editarlo, y
en cuanto se olvida una vez empieza a mentir. Ya estaba mintiendo cuando se retiró:

- decía **«54 diapos canónicas»** (hoy son 156, en 12 familias y 2 `slideMaster`);
- decía que `verify_deck()` avisa si los divisores pasan de **«~15%»** del deck, cuando el umbral que
  el motor lee de `assets/brand-config.json` era 40% (y hoy es 25%);
- mandaba **«consulta SIEMPRE el catálogo JSON antes de `use()`»**, que en la v4 es exactamente lo que
  no hay que hacer: son 1,1 MB y no caben en el turno.

## A dónde ir en su lugar

| Si quieres… | Usa |
|---|---|
| elegir familia y arquetipo de un deck normal | **§MAPA DE FAMILIAS de `SKILL.md`** (resuelve la mayoría sin abrir nada) |
| filtrar por nº de bloques, foto, gráfica, color, sistema… | `find_slides(family=…, n_items=…, has_image=…, variant=…, master=…)` |
| la ficha de un arquetipo (cuándo sí, cuándo no, hermanos) | `describe("NOMBRE")` |
| las zonas exactas y su capacidad | `fill_spec(s)` — o simplemente `use()`, que las imprime |
| ver todas las maquetas de un vistazo | [`slides-index.md`](slides-index.md) — **autogenerado** en la misma pasada que el catálogo, así que no puede desviarse de él |
| una receta ya montada de deck completo | [`capability-recipe.md`](capability-recipe.md) |

La sustitución de este fichero por `slides-index.md` no es un cambio de formato: es que el índice pasa
a **derivarse** del binario y del catálogo, con los umbrales tomados de `assets/brand-config.json`, en
vez de depender de que alguien se acuerde de actualizarlo.
