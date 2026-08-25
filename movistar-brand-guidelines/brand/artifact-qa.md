# QA de Artifacts HTML/React — catálogo de anti-patrones + auto-verificación forzada

> Complementa a `scripts/lint_artifact.py` (gate mecánico, 15 checks) y a la sección "QA específico
> para artifacts HTML/React" de `SKILL.md`. El linter atrapa lo que se puede detectar por patrón;
> este fichero cubre lo que requiere criterio (si un fondo de foto tiene contraste real en la zona
> del texto, si falta riqueza visual) y fuerza una revisión explícita, elemento por elemento.

> ⚠️ **Movistar es DISTINTA de las 4 marcas del paraguas Mahou (Mahou/San Miguel/Alhambra/Solán) en
> dos puntos que invierten su QA. No apliques la doctrina de esas marcas aquí:**
> 1. **La fuente la inyecta el runtime.** En artifacts web NO se pega ningún `@font-face` en base64:
>    solo se declara `font-family:'Movistar Sans'`. Pegar el base64 es un **FAIL**
>    (`fontface_base64_pegado`). En las otras marcas es al revés (allí FALTA el base64 lo que falla).
> 2. **Color plano.** Movistar NO tiene degradados: cualquier `linear/radial/conic-gradient` es
>    **FAIL** (`color_plano`). En Mahou algunos degradados de marca son válidos; aquí ninguno.

## Índice

- **Cómo se usa** — flujo linter -> tabla -> riqueza visual.
- **Tabla de auto-verificación forzada** — una fila por elemento posicionado/imagen/texto sobre
  foto/texto de marca (+ el ejercicio real hecho sobre `patterns.html`).
- **Catálogo de anti-patrones** (síntoma -> nº):

  | # | Síntoma | Regla del linter |
  |---|---|---|
  | 1 | `@font-face` con la fuente en base64 (el runtime YA la inyecta) | `fontface_base64_pegado` |
  | 2 | Cualquier degradado (Movistar es color plano) | `color_plano` |
  | 3 | Blanco/negro PURO (`#fff`/`#000`) en vez de Blanco/Negro Movistar | `blanco_negro_puro` |
  | 4 | Texto/grafismo CLARO sobre fondo CLARO (combinación "Prohibido") | `combinacion_prohibida` |
  | 5 | Contraste por debajo de AA | `contraste_bajo` |
  | 6 | Em-dash "—" en el copy | `em_dash` |
  | 7 | "movistar" con "m" minúscula en texto visible | `marca_m_minuscula` |
  | 8 | Titular terminado en punto | `titular_con_punto` (WARN) |
  | 9 | Exclamación/pregunta sin signo RAE de apertura | `exclamacion/interrogacion_sin_apertura` (WARN) |
  | 10 | Texto sobre FOTO sin scrim ni z-index | `texto_sobre_foto_sin_scrim` |
  | 11 | Imagen sin dimensiones | `img_sin_dimensiones` |
  | 12 | La M (un solo `<path>`) repetida sin `<symbol>`+`<use>` | `logo_duplicado` (WARN) |
  | 13 | Selector complejo que define color/fondo (o shorthand `font:`) | `selector_no_soportado` (WARN) |
  | 14 | Color fuera de la paleta de marca | `color_fuera_paleta` (WARN) |
  | 15 | Clase usada pero nunca definida en CSS | `clase_sin_definir` |

- **Cómo dar riqueza visual a una sección plana** — recursos válidos SIN degradado + lo que NO hacer.
- **Auto-verificación de riqueza visual** — la pregunta final obligatoria.

## Cómo se usa

1. Genera el artifact. **Reutiliza `assets/html/brand-tokens.css` + `assets/html/patterns.html`**: los
   pares fondo->texto, el scrim y el logo ya vienen resueltos, así no eliges color a mano.
2. Ejecuta `python3 scripts/lint_artifact.py <fichero>`. Corrige todo `FAIL`; repite hasta 0 `FAIL`.
3. Para cada `WARN` que quede, y para cada elemento posicionado/imagen/texto sobre foto/texto de
   marca del artifact, rellena la **tabla de auto-verificación** de abajo — no la resumas, no la
   saltes por "obviamente está bien".
4. Si alguna celda es "no" o "?", corrige antes de entregar.

## Tabla de auto-verificación forzada (rellénala, no la simules)

Una fila por cada elemento posicionado (`position:absolute/fixed`), cada `<img>`/fondo con imagen,
cada bloque de texto sobre FOTO, y cada texto de marca.

| Elemento | ¿padre `relative` dimensionado Y el propio elemento `absolute`? | ¿img con w/h/object-fit? | ¿scrim + z-index si texto sobre FOTO? | ¿color de texto correcto por fondo (Negro sobre claro · Blanco sobre Azul/Negro/oscuro · NUNCA claro sobre claro)? | ¿copy OK (sin "—", M mayúscula, titular sin punto, signos RAE)? | ¿`font-family:'Movistar Sans'` y SIN `@font-face` base64? |
|---|---|---|---|---|---|---|
| (fila de ejemplo) | | | | | | |

Si el artifact no tiene ningún elemento de estos tipos, dilo explícitamente ("no aplica") en vez de
omitir la tabla.

**Selectores CSS (motor v2):** define `color`/`background` con **selectores de una sola clase**
(`.clase`), nunca descendiente/hijo/hermano/atributo/pseudo-elemento (`.hero p`, `.card > .x`,
`[data-x]`). El linter solo resuelve selectores simples; para los complejos que definen color/fondo
emite el WARN `selector_no_soportado` y el contraste de esos nodos NO queda cubierto — reescríbelos
como una sola clase, o verifica el contraste a mano y justifícalo aquí. Evita también el shorthand
`font:` (el linter no lo expande — usa `font-family`/`font-size` longhand).

### Ejercicio real — `assets/html/patterns.html` (los 12 bloques, hecho de verdad, no simulado)

| Elemento | ¿padre `relative`+`absolute`? | ¿img w/h/object-fit? | ¿scrim si foto? | ¿color de texto correcto por fondo? | ¿copy OK? | ¿fuente inyectada, sin base64? |
|---|---|---|---|---|---|---|
| HERO_PORTADA_AZUL — logo `<img src="movistar://logo-m-white">` | n/a (flujo normal) | sí (w/h attr + `object-fit:contain`) | n/a | n/a (logo, no texto) | n/a | n/a |
| HERO_PORTADA_AZUL — eyebrow/h1/subtítulo (`.bg-azul`) | n/a | n/a | n/a | sí (Blanco heredado de `.bg-azul`, 4.66:1) | sí | sí |
| HERO_PORTADA_AZUL — destacado (`.mvst-badge .bg-amarillo-claro`) | n/a | n/a | n/a | sí (Negro sobre Amarillo claro, 12.8:1 — destacado en secundario claro, no en Blanco ni Azul) | sí | sí |
| HERO_FOTO — contenedor + `<img src="movistar://libertad-azul-movistar">` | sí (`position:relative;height:420px` + `background:#262423` de reserva) | sí (`object-fit:cover`, w/h 100%) | n/a (es la imagen) | n/a | n/a | n/a |
| HERO_FOTO — texto (`.mvst-over`) + M Blanca (sprite) | sí | n/a | sí (`.mvst-scrim` hermano + `.mvst-over` con `position:absolute;inset:0;z-index:2`) | sí (Blanco; el linter salta el contraste sobre foto y el fondo de reserva es Negro, no claro->claro) | sí | sí |
| TARJETA_BLANCA — h2 Negro + palabra en `.text-azul` + cuerpo (`.bg-blanco`) | n/a | n/a | n/a | sí (Negro 14.9:1; destacado Azul sobre Blanco 4.66:1) | sí (titular sin punto) | sí |
| SECCION_SECUNDARIO (`.bg-verde-claro`) | n/a | n/a | n/a | sí (Negro sobre Verde claro, 13.0:1) | sí | sí |
| BLOQUE_NEGRO_PREMIUM (`.bg-negro`) + M Azul (sprite) | n/a | n/a | n/a | sí (Blanco 14.9:1; M en Azul sobre Negro = uso excepcional válido, §2.1.2) | sí | sí |
| STAT_ROW — 3 columnas Azul/Blanco/Azul | n/a | n/a | n/a | sí (Blanco sobre Azul ×2; Negro + destacado Azul sobre Blanco) | sí | sí |
| CTA_SECTION — botón `.mvst-cta` + copy con "¡…!" y "¿…?" | n/a | n/a | n/a | sí (Blanco sobre Azul en el botón, 4.66:1) | sí (exclamación y pregunta con signos RAE de apertura y cierre) | sí |
| LOGO_USAGE — 3 tiles (M Azul sprite, M Blanca sprite, M Azul blob) | n/a | sí (el `<img>` blob con w/h/object-fit) | n/a | n/a (logo) | n/a | n/a |
| DESTACADOS — 4 chips en secundarios claros (`.bg-*-claro`) | n/a | n/a | n/a | sí (Negro sobre cada secundario claro) | sí | sí |
| ESTADOS_SEMANTICOS — `.text-positivo/.text-alerta/.text-negativo` sobre Blanco | n/a | n/a | n/a | sí (semánticos como texto SOLO sobre Blanco: 4.76 / 4.64 / 6.20:1) | sí | sí |
| FOOTER_LEGAL (`.bg-azul`) + M Blanca (sprite) | n/a | n/a | n/a | sí (Blanco sobre Azul) | sí | sí |
| SECTION_SCAFFOLD | plantilla vacía — no aplica ninguna columna | | | | | |

**Verificado con `lint_artifact.py` real** (no simulado): **0 FAIL, 0 WARN**. Notas de cómo se llegó
a un set limpio (útiles para no repetir los tropiezos):
- El `<title>` estaba fuera de `<body>` y sin `font-family` heredable -> disparaba
  `fuente_no_declarada`. Se resolvió declarando `html { font-family: var(--mvst-font); }` en
  `brand-tokens.css` (además de en `body`). Un em-dash en el `<title>` también disparó `em_dash`
  (el linter SÍ lee el texto del `<title>`) — sustituido por dos puntos.
- El texto Blanco de HERO_FOTO resolvía su fondo al `body` (Blanco) porque el scrim es un HERMANO,
  no un ancestro -> `combinacion_prohibida` (claro sobre claro). Se resolvió dando al contenedor de
  la foto un `background:#262423` de reserva (Negro Movistar): el fondo resuelto pasa a ser oscuro,
  y el contraste real sobre la foto lo garantiza el scrim. **Lección**: cuando pongas texto Blanco
  sobre foto, dale al contenedor un fondo sólido oscuro de reserva, no dejes que caiga al `body`.

## Catálogo de anti-patrones (código incorrecto -> correcto)

### 1. `@font-face` con la fuente en base64 — el runtime YA la inyecta (LA inversión de Movistar)

❌ **Incorrecto** — teclear el `@font-face` con la fuente en base64 es un **FAIL**: en Movistar el
runtime de `artifact-flow` inyecta Movistar Sans en el artifact web (`injectBrandFont`). Pegar el
base64 cuesta ~15s de tokens y arriesga cortar el stream (`docs/FONT-RUNTIME-INJECTION-PROPOSAL.md`):
```html
<style>
  @font-face { font-family:'Movistar Sans'; src:url(data:font/woff2;base64,d09GMg…) format('woff2'); }
  body { font-family:'Movistar Sans', sans-serif; }
</style>
```

✅ **Correcto** — declara solo la familia (ya viene en `brand-tokens.css` sobre `html`/`body`);
NO pegues ningún `@font-face`:
```html
<style> body { font-family: 'Movistar Sans', system-ui, sans-serif; } </style>
```
Para HTML standalone / PDF (donde NADIE inyecta la fuente) usa `url('file://…')` a la fuente
bundleada, nunca base64 (ver `SKILL.md` §Tipografía). En un artifact web, jamás.

### 2. Degradado — Movistar es color plano

❌ **Incorrecto** — cualquier `linear/radial/conic-gradient` es **FAIL** (`color_plano`). A
diferencia de Mahou, en Movistar NO hay degradados de marca:
```css
.hero { background: linear-gradient(180deg, #0066ff, #022d67); }
```

✅ **Correcto** — color plano de la paleta (usa una clase `.bg-*` de `brand-tokens.css`). Para
riqueza cromática, alterna fondos planos o usa una foto de banco:
```html
<section class="bg-azul">…</section>
```

### 3. Blanco / negro PURO

❌ **Incorrecto** — Movistar no usa `#ffffff` ni `#000000` (`blanco_negro_puro`):
```html
<div style="background:#ffffff; color:#000000;">…</div>
```

✅ **Correcto** — Blanco Movistar `#fffaf5` y Negro Movistar `#262423` (o las clases `.bg-blanco`/
`.bg-negro`):
```html
<div class="bg-blanco">…</div>
```
(Un `rgba(38,36,35,0.55)` como scrim/sombra SÍ vale — el linter solo marca el hex sólido puro.)

### 4. Texto/grafismo CLARO sobre fondo CLARO (combinación "Prohibido")

❌ **Incorrecto** — Blanco Movistar o un secundario claro como TEXTO sobre un fondo claro es la
combinación "Prohibido" de `brand/contrast-matrix.md` (`combinacion_prohibida`):
```html
<section class="bg-verde-claro"><p style="color:#fffaf5;">Texto</p></section>
```

✅ **Correcto** — sobre CUALQUIER fondo claro (Blanco o secundario claro), el texto va en Negro
Movistar (las clases `.bg-*` claras ya lo traen). Blanco solo sobre Azul/Negro/secundario oscuro:
```html
<section class="bg-verde-claro"><p>Texto</p></section> <!-- Negro heredado, 13.0:1 -->
```

### 5. Em-dash "—" en el copy

❌ **Incorrecto** — Movistar no usa el em-dash (`em_dash`, regla nº1). Ojo: el linter lee incluso el
`<title>`:
```html
<h2 class="mvst-h2">Fibra sin líos — y sin miedo</h2>
```

✅ **Correcto** — usa comas, dos puntos o frases cortas:
```html
<h2 class="mvst-h2">Fibra sin líos. Y sin miedo</h2>
```

### 6. "movistar" con "m" minúscula

❌ **Incorrecto** — la "M" de Movistar va SIEMPRE en mayúscula (`marca_m_minuscula`, §1.3 principio 1):
```html
<p class="mvst-body">Cámbiate a movistar hoy</p>
```

✅ **Correcto**:
```html
<p class="mvst-body">Cámbiate a Movistar hoy</p>
```
(En un `src="movistar://…"` NO pasa nada: es un atributo, no texto visible — el linter no lo marca.)

### 7. Titular terminado en punto

❌ **Incorrecto** — los titulares de Movistar van abiertos, sin punto final (`titular_con_punto`,
WARN; §1.3 principio 14). Aplica a `h1`-`h6` y a las clases `.mvst-h*`/`.mvst-eyebrow`:
```html
<h1 class="mvst-h1">Donde hay familia, que esté Movistar.</h1>
```

✅ **Correcto** (los puntos suspensivos SÍ se permiten, principio 13):
```html
<h1 class="mvst-h1">Donde hay familia, que esté Movistar</h1>
```

### 8. Exclamación / pregunta sin signo RAE de apertura

❌ **Incorrecto** — Movistar sí usa exclamaciones y preguntas retadoras, pero SIEMPRE con los signos
de apertura y cierre de la RAE (`exclamacion_sin_apertura`/`interrogacion_sin_apertura`, WARN; §1.3
principio 12):
```html
<h3 class="mvst-h3">Vive todo el fútbol!</h3>
```

✅ **Correcto**:
```html
<h3 class="mvst-h3">¡Vive todo el fútbol!</h3>
```

### 9. Texto sobre FOTO sin scrim

❌ **Incorrecto** — contraste no garantizado; depende de qué haya detrás del texto en esa foto
concreta (`texto_sobre_foto_sin_scrim`, regla nº8):
```html
<div style="position:relative;">
  <img src="movistar://libertad-azul-movistar" width="1408" height="768" style="width:100%;height:100%;object-fit:cover;">
  <h2 style="position:absolute; top:40%; color:#fffaf5;">Titular</h2>
</div>
```

✅ **Correcto** — usa `.mvst-scrim` + `.mvst-over` de `brand-tokens.css`, y dale al contenedor un
fondo sólido oscuro de reserva (para que el color de fondo resuelto NO sea claro->claro):
```html
<div style="position:relative; height:420px; background:#262423;">
  <img src="movistar://libertad-azul-movistar" width="1408" height="768" style="width:100%;height:100%;object-fit:cover;">
  <div class="mvst-scrim"></div>
  <div class="mvst-over"><h2 class="mvst-h1">Titular</h2></div>
</div>
```

### 10. Imagen sin dimensiones

❌ **Incorrecto** (`img_sin_dimensiones`) — puede desbordar y solapar el texto:
```html
<img src="movistar://router-movistar-hogar">
```

✅ **Correcto** — `width`/`height` + `object-fit`:
```html
<img src="movistar://router-movistar-hogar" width="1920" height="1072"
     style="width:100%; height:100%; object-fit:cover;">
```

### 11. La M (el logo) — recolorear o duplicar

❌ **Incorrecto** — recrear/recolorear la M a mano, o repetir su `<path>` (un solo path) muchas
veces incrustado (`logo_duplicado`, WARN). La M va SIEMPRE en Azul Movistar (o Blanca solo sobre
Azul Movistar / foto azulada legible), nunca en otro color:
```html
<svg viewBox="0 0 425.2 355.01"><path fill="#c10000" d="M340.39,…Z"/></svg>
<svg viewBox="0 0 425.2 355.01"><path fill="#c10000" d="M340.39,…Z"/></svg>
```

✅ **Correcto** — dos vías, ambas en `patterns.html`. Preferente por blob; o sprite `<symbol>`+
`<use>` con el color por `currentColor` (Azul por defecto, Blanco sobre Azul):
```html
<img src="movistar://logo-m-blue" width="120" height="100" style="width:72px;height:60px;object-fit:contain;">
<!-- o -->
<svg width="0" height="0" style="width:0;height:0;overflow:hidden;"><symbol id="mvst-m" viewBox="0 0 425.2 355.01"><path fill="currentColor" d="M340.39,…Z"/></symbol></svg>
<svg viewBox="0 0 425.2 355.01" style="color:#0066ff;width:72px;height:60px;"><use href="#mvst-m"></use></svg>
```

### 12. Selector complejo / shorthand `font:` — invisibles para el linter

❌ **Incorrecto** — un color/fondo definido en un selector complejo no lo resuelve el motor
(`selector_no_soportado`, WARN), y el shorthand `font:` no se expande (el linter cree que no hay
`font-family` propia):
```css
.hero p { color: #fffaf5; }
.label { font: 12px monospace; }
```

✅ **Correcto** — selectores de una sola clase para color/fondo, y `font-family` longhand:
```css
.hero-text { color: #fffaf5; }
.label { font-family: monospace; font-size: 12px; }
```

## Inventario COMPLETO de hallazgos del linter (20)

> ⚠️ **Por qué existe esta tabla.** El catálogo de anti-patrones de arriba explica **12** casos con
> su código incorrecto y su corrección — es la parte pedagógica. Pero el linter emite **20
> hallazgos distintos**, así que hay ~8 que un artifact puede disparar sin que este documento los
> nombrase. Se detectó construyendo la guía de marca de
> `dist/produccion-real/movistar-v4/`: hubo que leer `scripts/lint_artifact.py` entero para saber
> qué comprueba el gate, que es exactamente lo que este fichero debería evitar.
>
> Los ids y su severidad salen **del propio código** (`_f(...)`/`Finding(...)`), no de memoria. Si
> añades un check, añádelo aquí.

| Id del hallazgo | Severidad |
|---|---|
| `absolute_sin_relative` | **FAIL** |
| `blanco_negro_puro` | **FAIL** |
| `clase_sin_definir` | **FAIL** |
| `color_plano` | **FAIL** |
| `combinacion_prohibida` | **FAIL** |
| `contraste_bajo` | **FAIL** |
| `em_dash` | **FAIL** |
| `fuente_no_movistar` | **FAIL** |
| `hero_overlay_no_cubre` | **FAIL** |
| `img_sin_dimensiones` | **FAIL** |
| `marca_m_minuscula` | **FAIL** |
| `texto_sobre_foto_sin_scrim` | **FAIL** |
| `color_fuera_paleta` | WARN |
| `exclamacion_sin_apertura` | WARN |
| `fuente_no_declarada` | WARN |
| `img_sin_object_fit` | WARN |
| `interrogacion_sin_apertura` | WARN |
| `logo_duplicado` | WARN |
| `selector_no_soportado` | WARN |
| `titular_con_punto` | WARN |

Los **FAIL bloquean** la entrega del artifact; los **WARN** piden revisión a ojo pero no bloquean.
Los que NO están en el catálogo de anti-patrones de arriba, y conviene conocer:

- **`absolute_sin_relative`** — un elemento `position:absolute` cuyo padre no es `relative` con
  dimensión: se posiciona contra el viewport y se descoloca al cambiar de ancho.
- **`hero_overlay_no_cubre`** — el `.mvst-over` de un hero con foto no cubre el contenedor
  (`position:absolute; inset:0`). Es el defecto que corrigió la v1.0.1 de esta skill.
- **`img_sin_object_fit`** (WARN) — imagen con dimensiones pero sin `object-fit`: se deforma.
- **`fuente_no_declarada`** (WARN) / **`fuente_no_movistar`** (FAIL) — la pieza no declara
  `font-family:'Movistar Sans'`, o declara otra. Recuerda la inversión de Movistar: la fuente la
  inyecta el runtime, así que se DECLARA pero no se embebe.
- **`clase_sin_definir`** — se usa una clase `.mvst-*`/`.bg-*`/`.text-*` que no existe en el CSS de
  la pieza. Suele ser copiar un bloque de `patterns.html` sin traerse su token.
- **`color_fuera_paleta`** (WARN) / **`color_plano`** (FAIL) — color que no está en la paleta, y
  degradado (Movistar es color plano).
- **`selector_no_soportado`** (WARN) — selector complejo que define color o fondo: el linter no
  puede resolverlo, hay que revisarlo a mano.

### Limitación conocida del gate

`check_contrast` **no modela `opacity` ni `alpha`**. Un texto correcto al que se le baja la opacidad
puede caer por debajo de AA y el linter no lo verá. No es teórico: `.mvst-eyebrow` llevaba
`opacity: 0.9` y daba 4,05:1 sobre Azul, y dos entradillas de `patterns.html` llevaban `0.95`
(4,36:1) — tres fallos AA que vivieron en los **assets de referencia** hasta el 2026-07-27 porque
ningún gate podía verlos. **Para bajar jerarquía en un texto usa COLOR de la paleta, nunca alfa.**

## Cómo dar riqueza visual a una sección plana (SIN degradado — Movistar es color plano)

1. **Foto real del banco** vía `movistar://<id>` (bloques `HERO_FOTO`) — 81 ids en
   `imagery/imagery-index.json`; sigue el algoritmo de `imagery/imagery-guide.md`. Prioriza las de
   afinidad cromática azul (`libertad-azul-movistar`, `playa-espejo-atardecer`,
   `movil-naranja-fondo-azul`). SIEMPRE con scrim si va texto encima.
2. **Fondos de color plano alternados** (`.bg-azul` / `.bg-blanco` / `.bg-negro` / secundarios) entre
   secciones, respetando la proporción cromática objetivo ~40% Azul · 30% Blanco · 10% Negro · 20%
   secundarios (§4.1.3). El Negro Movistar aporta un aire premium; úsalo con medida.
3. **Un color secundario por sección** como acento de capítulo (Azul claro / Verde claro / Amarillo
   claro / Coral claro), con texto Negro y, si acaso, UNA palabra del titular en Azul. Nunca mezcles
   dos secundarios distintos en la misma pieza (§4.4.4).
4. **Tipografía como recurso gráfico**: un titular breve y potente a gran escala en Movistar Sans
   (`.mvst-h1`), con mucho aire alrededor (§Copy — "titulares generosos, respira").
5. **Lo que NO hacer**: no inventes un degradado "para dar variedad" (FAIL); no pongas la M en otro
   color que no sea Azul (o Blanco sobre Azul); no uses más de un secundario por pieza; no incrustes
   binarios de foto (usa `movistar://<id>`); no pegues la fuente en base64 (la inyecta el runtime).

## Auto-verificación de riqueza visual (una pregunta, respóndela explícitamente)

> ¿Esta sección quedaría visualmente pobre/plana tal como está? Si sí: ¿usé alguna de las
> alternativas de arriba (una foto real vía `movistar://<id>`, un fondo de color plano de marca, un
> acento secundario, la tipografía como recurso), o la dejé plana sin más? Si la dejaste plana a
> propósito (p.ej. una sección de puro texto legal), dilo — no lo dejes en silencio. Recuerda: la
> riqueza en Movistar viene del color plano bien usado y la foto, NUNCA de un degradado.
