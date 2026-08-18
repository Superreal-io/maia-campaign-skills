---
name: movistar-visual-production
description: Stack de produccion visual del Art Director (D) para piezas Movistar presentables a cliente. Assets de marca como archivos (fuentes, logos, tokens), fotografia real via OpenAI (gpt-image-2), ensamblado programatico por slots, y bucle de verificacion visual con render. Sustituye a visual-01-brand-assets, visual-02-brand-typography y el enfoque base64 de visual-03.
version: 1.2.0
owner: superreal
status: active
loaded_by: D (Art Director)
requires_env:
  - OPENAI_API_KEY
---

# Movistar Visual Production

Esta skill convierte la Estrategia Creativa en piezas finales presentables a cliente. Regla central: **el modelo nunca genera base64 ni copia assets a mano**. Escribe HTML con slots, y los scripts ensamblan, generan fotografia y renderizan.

## Estructura del bundle

```
brand/
├── fonts/            Movistar Sans woff2 (10 variantes)
├── logos/            mark, mark-inverse, mark-dark, lockups, wordmarks (SVG)
├── tokens/           colors.css, spacing.css, typography.css, tokens.json
└── audit-report.md   Composicion por formato destilada de 41 piezas reales. LEER SIEMPRE.
references/
├── INDEX.md          Catalogo de las 41 piezas reales por formato. Para MIRAR con Read
├── pieces/           Las 41 creatividades reales
└── gold-standards/   Las 34 curadas y normalizadas. Para PASAR al generador con --ref
    ├── INDEX.md      Que referencia usar segun canal y modo. Rutas listas para copiar
    └── <canal>/      email, digital, exterior, tienda, movistarplus, marca
guidelines/
├── app-email.md      Plantilla email observada en piezas reales (9 bloques)
├── app-ads.md        Geometrias OOH y display con layouts ASCII
├── app-web.md        Landing de campana vs web generica
├── magic-prompt.md   Como escribir prompts de fotografia de marca
├── mockup-workflow.md  Cuando y como componer mockups contextuales
└── prototypers/      Prompts calibrados por canal (de los GPT validados por el equipo)
    ├── email.md          Familias visuales, paleta extendida y jerarquia del email
    ├── movistarplus.md   WOW vs videocartela, CTA link con >, modos de fondo
    ├── tienda-plv.md     Cartel A3 / etiqueta / stopper, beneficio antes que precio
    └── meta.md           Formatos por ratio, sin boton CTA, paleta propia del canal
templates/
├── html/             Plantillas slot-based por formato
└── mockups/          Entornos + corners.json para el composer
scripts/
├── assemble.py       Rellena slots (fuentes, logos, tokens, imagenes)
├── generate_image.py Fotografia via OpenAI (OPENAI_API_KEY, gpt-image-2)
├── render.py         HTML a PNG para verificacion visual
└── mockup_composer.py  Incrusta la pieza en un entorno real
```

## Workflow por pieza (obligatorio, en este orden)

### 1. Referencias antes de disenar
Lee 2-3 piezas reales del formato en `references/pieces/` (usa `references/INDEX.md` para elegirlas) y el bloque del formato en `brand/audit-report.md`. Son ground truth: mas fiables que cualquier regla escrita.

Dos carpetas, dos usos, no las confundas:

- `references/pieces/`: las 41 piezas reales. Se **miran** con Read. No se pasan al generador de imagen: muchas son capturas de navegador, mockups con perspectiva o llevan logos de terceros que el modelo reproduciria.
- `references/gold-standards/`: las 34 curadas y normalizadas a JPEG q90, lado largo max 1536 px. Son las que se **pasan** con `--ref` en el paso 3.

### 2. Construir el HTML con slots
Parte de la plantilla del formato en `templates/html/` si existe; si no, construye HTML de dimensiones fijas siguiendo el patron del audit-report. Reglas duras:

- Tipografia: escribe `{{FONT_FACE_MIN}}` (o `{{FONT_FACE}}` si necesitas italicas o pesos 300/500). NUNCA escribas un @font-face con base64.
- Tokens: escribe `{{TOKENS_CSS}}` y usa las variables. Paleta cerrada: cualquier HEX fuera de tokens es error.
- Logos: usa los slots `{{LOGO_MARK}}`, `{{LOGO_MARK_INVERSE}}`, `{{LOGO_LOCKUP}}`, etc. NUNCA dibujes la M ni copies un SVG a mano. Variante inverse sobre fondo oscuro o azul.
- Fotografia: escribe `{{IMG:outputs/<slug>-<zona>.png}}` con un atributo `data-prompt` describiendo la foto.
- Emails: sin slots de fuente (ensambla con `--no-font`); HEX directos de la paleta; tablas.
- Formatos ex-SVG (social, tienda, exterior, M+): produce HTML de dimensiones fijas y entrega el PNG renderizado. Solo produce SVG si piden vector editable.

### 3. Generar la fotografia

Por cada `{{IMG:...}}`: escribe el prompt siguiendo `guidelines/magic-prompt.md` (4-5 frases cinematograficas en ingles, realismo editorial, universo Movistar) y **pasa 2-3 Gold Standards con `--ref`**.

**Generar sin referencia visual esta prohibido si existe Gold Standard para el canal.** El prompt describe la escena; la referencia transmite lo que el prompt no puede describir: composicion, luz, jerarquia y codigo de marca. Sin referencia el modelo produce stock generico.

**A0. Si el canal tiene prototyper, leelo primero.** `guidelines/prototypers/` tiene el prompt calibrado de email, movistarplus, tienda-plv y meta: familias visuales, composicion por formato, paleta del canal, reglas criticas (CTA link en M+, sin boton en Meta, beneficio antes que precio en tienda) y alertas de validacion. Cada archivo empieza con un bloque de adaptacion que mapea dimensiones a los flags del script. El prototyper manda sobre la doctrina generica de magic-prompt.md en su canal.

**A. Elegir.** `references/gold-standards/INDEX.md` tiene la tabla "Que referencias pasar segun lo que estes generando" con la combinacion resuelta por canal y por modo. Reglas:

- 2 o 3 referencias. Nunca mas (diluyen la senal y se facturan como tokens), nunca cero.
- Combina por **modo**, no solo por canal: foto de escena con referencias FOTO, fondo grafico con referencias GRAFICO.
- Movistar+ solo con Movistar+: sus referencias se combinan entre si, nunca con otros canales. Su codigo real es azul con pastilla blanca y keyword azul; el modo oscuro lo pone el key art, no un fondo negro.
- El co-branding de las referencias es oficial (partners de Movistar): usalas sin miedo. Regla de contenido: si la pieza nueva promociona otros titulos u otros dispositivos, describe el contenido nuevo en el prompt para no arrastrar el de la referencia. Pieza 100% Movistar sin partner: anade exclusion de logos ajenos (referencias sin partner: tienda-plv-etiqueta-sin-ip.jpg y exterior-cartel-tipografico-paleta.jpg).
- Si la fila del INDEX tiene la columna `Ojo` rellena, ese defecto va al prompt como exclusion explicita. El modelo copia los defectos igual que las virtudes.
- Si el canal no tiene Gold Standard (BTL, TMKS, D2D, SMS, push, lona, display servido, caballete impreso): genera sin `--ref` y flaggea `sin_gold_standard`. No sustituyas por una referencia de otro canal: una referencia equivocada es peor que ninguna.

**B. Comprobar antes de gastar credito.** Una vez por sesion:

```bash
python3 scripts/generate_image.py -p "test" -o /tmp/t.png --aspect <ratio> \
  --ref references/gold-standards/<canal>/<archivo>.jpg \
  --ref references/gold-standards/<canal>/<archivo>.jpg \
  --dry-run
```

Debe decir `endpoint: .../v1/images/edits`, `encoding: multipart/form-data` y `refs: 2`. Si dice `generations` y `refs: 0`, las referencias no se estan pasando: para y arreglalo antes de generar la tanda.

**C. Generar.**

Reglas del prompt (validadas en produccion 18-08-2026, son la diferencia medida entre pieza buena y pieza mediocre):

- **El prompt describe la pieza, no la referencia.** PROHIBIDO escribir "following the reference", "the template", "the gold standard" o equivalentes dentro del prompt. Escribe el prompt como si la referencia no existiera: que se ve, donde, con que luz, con que jerarquia y con que textos EXACTOS. La referencia entra solo por `--ref`.
- **Parte del prompt calibrado del canal** si existe en `guidelines/magic-prompt.md` seccion "Entradas" (M+, tienda y email hero ya tienen). Sustituye las variables por el copy real y no toques la parte fija.
- **`--quality high` para entregables.** `medium` solo para pruebas y dry-runs de calibracion.

```bash
python3 scripts/generate_image.py \
  -p "<prompt>" -o outputs/<slug>-<zona>.png --aspect <ratio> --quality high \
  --ref references/gold-standards/<canal>/<archivo-1>.jpg \
  --ref references/gold-standards/<canal>/<archivo-2>.jpg
```

Las rutas de `--ref` son relativas a `movistar-visual-production/`. Ejecuta el script desde ahi. Si dice `ERROR: referencia no encontrada`, te imprime el cwd actual.

**D. Documentar.** En el design rationale, seccion Fotografia: prompt literal + **Gold Standards usados por nombre de archivo** + por que esos + exclusiones metidas por la columna `Ojo`. Una entrada sin la linea de Gold Standards esta incompleta.

Si la API no esta disponible, usa como stand-in un crop coherente de `references/pieces/` y flaggea `imagen_provisional`.

### 4. Ensamblar

```bash
python3 scripts/assemble.py -i pieza.slots.html -o outputs/pieza.html          # normal
python3 scripts/assemble.py -i email.slots.html -o outputs/email.html --no-font  # email
```

Si el script avisa de slots sin resolver, corrige antes de seguir.

### 5. Verificacion visual (el paso que separa mockup de pieza final)

```bash
python3 scripts/render.py -i outputs/pieza.html -o outputs/pieza.png --width <W> --height <H>
```

MIRA el PNG (herramienta Read) y evalua contra esta checklist:

1. Las 5 non-negotiables: azul #0066FF presente; fondo #FFFAF5 (nunca blanco puro); max un secundario; solo Movistar Sans; sentence case y CTAs especificos sin exclamacion.
2. El patron del formato en audit-report (jerarquia, posicion de la M, estructura).
3. Nada solapado, cortado ni desbordado; legibilidad a la distancia del soporte.
4. La foto integra: luz creible, personas reales, sin look CGI.
5. Test de parecido: puesta junto a las referencias reales, encaja como una mas.

Si algo falla, corrige el HTML y repite ensamblado + render. Maximo 2 iteraciones; si a la segunda no pasa, entrega con flag `qa_visual_fallido` y detalle.

### 6. Mockup contextual (si es para presentar a cliente)
Sigue `guidelines/mockup-workflow.md`: pieza plana en PNG + template de `templates/mockups/` + `scripts/mockup_composer.py`. Si no hay template del formato, genera el entorno con `generate_image.py` (prompt de entorno vacio, sin branding), anota las esquinas en `.corners.json` y guardalo en la subcarpeta para reutilizar.

## Entregables por pieza

- `outputs/<pieza>.html` ensamblado (autocontenido) o `.slots.html` + assets si piden editable
- `outputs/<pieza>.png` render verificado
- Mockup contextual si aplica
- Entrada en el design rationale con el resultado del QA visual

## Anti-patrones

- Escribir base64 a mano (fuentes, logos, imagenes): NUNCA. Es la causa historica de tipografia rota.
- Placeholder dashed en una entrega final: solo se admite con flag `imagen_provisional` y motivo.
- SVG a mano alzada con coordenadas para formatos fotograficos: usar HTML fijo + render.
- Entregar sin haber mirado el render: prohibido.
- Inventar HEX o tokens: si falta un valor, TODO + flag.
