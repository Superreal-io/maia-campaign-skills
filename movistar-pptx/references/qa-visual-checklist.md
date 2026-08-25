# QA visual por render — checklist

> **Esto NO se ejecuta en la primera entrega de SuperStudio.** El turno tiene un límite duro de 20
> minutos y este QA no cabe: pertenece a una evaluación offline o a un turno posterior que el usuario
> pida explícitamente. En el turno inicial, el control de calidad son los gates deterministas de
> `save()` + los avisos `[deck-qa]` de `verify_deck()`.

## Cómo se rasteriza

```python
from qa_render import render
pngs = render(ruta_pptx)        # pptx -> PDF (soffice) -> PNG por diapositiva
```

**Nunca uses `Slide.Export()` de PowerPoint COM** para esto: tiene su propio bug de sustitución de
fuente al rasterizar, ajeno al fichero (`GOTCHAS.md` G10). Usa siempre `qa_render.py`/`soffice`.

## Lo que hay que mirar en cada PNG

| # | Defecto | Qué hacer |
|---|---|---|
| a | Texto recortado o encogido en exceso | acortar el texto (respeta `max_chars_approx` del fill-spec) |
| b | Columnas, tarjetas o pies vacíos | rellenarlos, o cambiar a un arquetipo con menos bloques |
| c | Imagen distorsionada | `set_image()` recorta, no estira: si se ve estirada, es que la zona no era un hueco de foto |
| d | Texto ilegible sobre la foto | arquetipo con scrim, o mover el texto a un bloque de color plano |
| e | Bloques permutados entre columnas | el fill-spec de `use()` sale en orden de LECTURA: reasigna siguiéndolo (G21) |
| f | Apertura y cierre | `AVISO_CONFIDENCIALIDAD` (si aplica) + `PORTADA_*` al principio, `CIERRE_*` al final |
| g | Idioma ≠ es-ES en cualquier texto visible | reescribir |

## ⛔ Fallos automáticos de marca

Se cruzan con `movistar-brand-guidelines` (también por visión). Cualquiera de estos = corregir y
**regenerar al MISMO filename** (no versiones el nombre; máximo 2 pasadas):

1. **Texto sobre foto sin zona de contraste ni scrim.**
2. Combinación **"Prohibido"** de la matriz: secundario claro (`#D3EEFF`/`#CEF7BF`/`#FFE99C`/`#FFC5A8`)
   o Blanco Movistar sobre fondo claro, o contraste por debajo de WCAG
   (`/skills/movistar-brand-guidelines/brand/contrast-matrix.md`).
3. **M recoloreada.** La M la pone la plantilla en Azul Movistar `#0066FF`; nunca la añadas a mano.
4. **Blanco puro `#FFFFFF` o negro puro `#000000`** en vez de Blanco/Negro Movistar
   (`#FFFAF5`/`#262423`).
5. **Titular con punto final**, o **"M" en minúscula** en "Movistar".
6. **Em-dash `—`** en el copy.
7. **Fondo de color plano del banco** (los 12 `categoria: fondo`, con el claim "es por todos.") usado
   como si fuera una fotografía de contenido. `set_image()` ya avisa (G23).

## ✅ Los desbordes que ves en el render SON REALES (corrección de G20)

Este documento decía antes que LibreOffice ignora las fuentes embebidas y sustituye por una tipografía
un 19,4 % más ancha, y por tanto que un desborde en el render podía no existir en PowerPoint. **Ya no
es cierto con esta plantilla** y usarlo como excusa hace que se entreguen desbordes de verdad.

Medido al cerrar la v4 (`GOTCHAS.md` G20): los 10 EOT de esta plantilla van **sin comprimir**, así que
`soffice` **sí** los carga (su PDF embebe `MovistarSans`/`-Bold`/`Medium-Bold` en una máquina donde la
fuente no está instalada). Sobre 24 textos idénticos, la razón de anchos LibreOffice/PowerPoint es
**0,996 de media**. La medición vieja se hizo contra los EOT comprimidos de la plantilla anterior.

**Regla: si en el render se desborda, acorta el texto.** No lo achaques al renderizador.

## ⚠️ Lo que SÍ es artefacto del renderizador

- `soffice` pinta a veces el *prompt* del `slideLayout` debajo de la diapositiva («Click to edit
  Master text styles», ~12 páginas de la plantilla). Comprobado que **PowerPoint no lo hace** y que el
  original intacto del cliente presenta las mismas ocurrencias.
- `soffice` puede equivocarse con el **fondo** de una diapositiva dentro de un deck grande. Ante la
  duda de color de fondo, **aísla esa diapositiva en un `.pptx` propio y re-renderiza** antes de dar
  el defecto por real (G7/G11/G17 son tres retractaciones por no haber hecho esto bien).

## 🔎 Cuatro comprobaciones concretas que salieron del QA de la v4

| Arquetipo | Qué mirar |
|---|---|
| `DATOS_DASHBOARD_6CHART_CLASICO` | que **cada número esté sobre SU barra y SU etiqueta**. El sufijo `subtitulo_N` no es el orden visual (van 4-5-6-3-2-7 de izquierda a derecha); el fill-spec lo dice, pero la diapositiva sale creíble aunque estén cambiados (G28) |
| `INFOGRAFIA_GAUGES` | que se vean **5** números, uno por gauge. Si ves 4 o alguno corrido, escribiste en un anillo (`Oval 9__4`/`Oval 9__5`) en vez de en el círculo (G29). El arco de color es arte estático: no refleja la cifra |
| `INDICE_SIMPLE` | que **cada número siga alineado con su tema**. Numeración y temas son dos cajas distintas: si un tema envuelve a dos líneas, todo lo de abajo se descuadra (G32) |
| `INTERIOR_TXT_2PANEL_CLASICO` · `GRID_3IMG_CAPTION_HERO_02_CLASICO` · `TIMELINE_MULTI_CLASICO` | el arte del cliente ya desborda con su propio texto de ejemplo: titulares de UNA línea y respetar las capacidades al pie de la letra (G31) |
