---
name: movistar-visual-production
description: Stack de produccion visual del Art Director (D) para piezas Movistar presentables a cliente. Assets de marca como archivos (fuentes, logos, tokens), fotografia real via OpenAI (gpt-image-2), ensamblado programatico por slots, y bucle de verificacion visual con render. Sustituye a visual-01-brand-assets, visual-02-brand-typography y el enfoque base64 de visual-03.
version: 1.4.0
owner: superreal
status: active
loaded_by: D (Art Director)
requires_env:
  - OPENAI_API_KEY
---

# Movistar Visual Production

Esta skill convierte la Estrategia Creativa en piezas finales presentables a cliente. Regla central: **el modelo nunca genera base64 ni copia assets a mano**. Escribe HTML con slots, y los scripts ensamblan, generan fotografia y renderizan.

> **El campo `version` del frontmatter no lleva tilde.** Es una clave YAML, no prosa: Paperclip busca `version` y con `versión` no detecta el update. No pases correctores ortograficos sobre el frontmatter ni sobre bloques de codigo de este archivo.

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
└── gold-standards/
    ├── INDEX.md      Que referencia pasar segun canal y modo. Rutas listas para copiar
    ├── <canal>/      email, digital, exterior, tienda, movistarplus, marca, meta
    │                 PIEZAS COMPLETAS curadas. Para generar piezas completas
    └── fotografia/   CROPS de zona fotografica pura, sin texto ni logos.
        └── INDEX.md  Escena, luz, casting, encuadre y para que sirve cada crop
guidelines/
├── app-email.md      Plantilla email observada en piezas reales (9 bloques)
├── app-ads.md        Geometrias OOH y display con layouts ASCII
├── app-web.md        Landing de campana vs web generica
├── app-meta.md       Formatos Meta/Social: feed, story, landscape. 8 familias
├── app-movistarplus.md  Formatos Movistar+: WOW, videocartela, banner web
├── magic-prompt.md   Como escribir prompts de fotografia de marca + prompts calibrados
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
├── generate_image.py Fotografia via OpenAI (OPENAI_API_KEY, gpt-image-2). Soporta --ref y --dry-run
├── render.py         HTML a PNG para verificacion visual
└── mockup_composer.py  Incrusta la pieza en un entorno real
```

## Verificacion de arranque (30 segundos, obligatoria)

Antes de producir nada, en cada ticket:

```bash
head -6 movistar-visual-production/SKILL.md               # confirma la version del bundle
ls movistar-visual-production/references/gold-standards/  # debe listar los canales + fotografia
```

Si la version no es la esperada o falta una carpeta, pide un `git pull origin main` del workspace antes de producir. Un upload manual al repo puede haber revertido el stack: tras cualquier pull, verifica con `--dry-run` antes de generar. Motivo: una tanda entera de 17 piezas se produjo sin referencias porque el workspace estaba clavado en un commit anterior.

## Las tres carpetas de referencias

No las confundas. Cada una tiene un uso y solo uno:

| Carpeta | Que contiene | Para que |
|---|---|---|
| `references/pieces/` | Las 41 piezas originales | **MIRAR** con Read antes de disenar. NO se pasan al generador: muchas son capturas de navegador, mockups con perspectiva o llevan logos de terceros que el modelo reproduciria |
| `references/gold-standards/<canal>/` | Piezas completas curadas y normalizadas (JPEG q90, lado largo max 1536 px) | **PASAR con `--ref`** cuando generas una PIEZA COMPLETA, con su texto dentro de la imagen |
| `references/gold-standards/fotografia/` | Crops de zona fotografica pura: sin titular, sin precio, sin logo, sin marcos | **PASAR con `--ref`** cuando generas SOLO FOTOGRAFIA para una zona de imagen de un HTML |

## Workflow por pieza (obligatorio, en este orden)

### 1. Referencias antes de disenar

Lee 2-3 piezas reales del formato en `references/pieces/` (usa `references/INDEX.md` para elegirlas) y el bloque del formato en `brand/audit-report.md`. Son ground truth: mas fiables que cualquier regla escrita.

### 2. Construir el HTML con slots

Parte de la plantilla del formato en `templates/html/` si existe; si no, construye HTML de dimensiones fijas siguiendo el patron del audit-report. Reglas duras:

- Tipografia: escribe `{{FONT_FACE_MIN}}` (o `{{FONT_FACE}}` si necesitas italicas o pesos 300/500). NUNCA escribas un @font-face con base64.
- Tokens: escribe `{{TOKENS_CSS}}` y usa las variables. Paleta cerrada: cualquier HEX fuera de tokens es error. **Verifica el nombre del token contra el archivo, no contra tu memoria:** `grep -oE "\-\-movistar-[a-z-]+" brand/tokens/colors.css | sort -u`. Un `var()` inexistente NO da error: cae al valor por defecto y produce fondos blancos con texto invisible. Rompio 2 piezas de M+ en un ciclo anterior.
- Logos: usa los slots `{{LOGO_MARK}}`, `{{LOGO_MARK_INVERSE}}`, `{{LOGO_LOCKUP}}`, etc. NUNCA dibujes la M ni copies un SVG a mano. Variante inverse sobre fondo oscuro o azul. **No hay asset de Movistar Plus+:** compon con `{{LOGO_MARK_INVERSE}}` + "+" tipografico y flaggea `logo_mplus_compuesto`.
- Fotografia: escribe `{{IMG:outputs/<slug>-<zona>.png}}` con `data-prompt` (el prompt usado), `data-refs` (nombres de archivo de las referencias) y `data-modo` (`foto` o `pieza-completa`).
- Emails: sin slots de fuente (ensambla con `--no-font`); HEX directos de la paleta; tablas.
- Formatos ex-SVG (social, tienda, exterior, M+): produce HTML de dimensiones fijas y entrega el PNG renderizado. Solo produce SVG si piden vector editable.

### 3. Generar la imagen

#### 3.0 Decide el MODO antes de nada

Es la decision mas importante del paso y determina que referencias usar. Esta medido en produccion (18-19/08/2026): equivocarse aqui anula la referencia y produce piezas mediocres.

| Modo | Que genera la llamada | Referencias | El prompt |
|---|---|---|---|
| **FOTO** | Solo la zona fotografica, sin ningun texto ni logo. El resto de la pieza es HTML con texto vivo | `gold-standards/fotografia/` | Describe la ESCENA. Puede decir "no text, no typography, no logos" |
| **PIEZA COMPLETA** | La pieza entera, con su texto dentro de la imagen. El HTML es lienzo a sangre | `gold-standards/<canal>/` del mismo formato | Describe LA PIEZA con sus textos literales entre comillas. **NUNCA** dice "no text" |

**LA REGLA DE EMPAREJAMIENTO (no negociable):** la clase de referencia tiene que coincidir con lo que pides.

- Prompt de foto pura + referencia de pieza completa = **la referencia queda anulada**. El prompt prohibe el texto, el marco y el logo que la referencia aporta, asi que solo se hereda luz y paleta. Verificado con los prompts literales de una tanda real.
- Prompt de pieza completa + referencia de foto = la referencia no puede transmitir reticula ni jerarquia.

**Modo por formato:**

- **PIEZA COMPLETA**: WOW y videocartela de M+, pantalla digital de tienda, caballete, MUPI, lona. El HTML queda como lienzo exacto del soporte con la imagen a sangre; conserva ademas la version editable con texto vivo como alternativa.
- **FOTO**: email, web/landing, display, Meta feed y story. Un email real nunca puede ser una imagen unica: el texto va vivo en el HTML y solo se genera el hero.

Si el manifiesto de C pide otro criterio para una pieza concreta, gana el manifiesto: anotalo en el rationale.

#### 3.A0 Si el canal tiene prototyper, leelo primero

`guidelines/prototypers/` tiene el prompt calibrado de email, movistarplus, tienda-plv y meta: familias visuales, composicion por formato, paleta del canal, reglas criticas (CTA link en M+, sin boton en Meta, beneficio antes que precio en tienda) y alertas de validacion. Cada archivo empieza con un bloque de adaptacion que mapea dimensiones a los flags del script. **En su canal, el prototyper manda sobre la doctrina generica de `magic-prompt.md`.** Sus alertas de validacion se incorporan al QA visual.

#### 3.A Elegir las referencias

Abre el INDEX de la carpeta que corresponda al modo:

- PIEZA COMPLETA → `references/gold-standards/INDEX.md`, tabla "Que referencias pasar segun lo que estes generando".
- FOTO → `references/gold-standards/fotografia/INDEX.md`, con escena, luz, casting y encuadre de cada crop.

Reglas, por orden de prioridad:

1. **2 o 3 referencias. Nunca mas.** Diluyen la senal y se facturan como tokens: `gpt-image-2` procesa las entradas siempre en alta fidelidad.
2. **El orden importa: la primera domina.** Conserva el detalle mas fino y la textura mas rica. Pon primero la que mas se parezca a lo que quieres; si hay caras, la de las caras primera. El `--dry-run` marca cual es.
3. **En modo PIEZA COMPLETA, mismo formato:** videocartela con videocartelas, feed con feeds, chevalet con chevalets.
4. **En modo FOTO, combina por escena**, no por canal: un crop de interior domestico sirve para email, display y tienda. Lo que importa es que escena, luz y casting se parezcan a lo que quieres.
5. **Movistar+ solo con Movistar+.** Su codigo real es azul con pastilla blanca y keyword azul; el modo oscuro lo pone el key art, no un fondo negro plano. Mezclarlo con otros canales lo contamina.
6. **El co-branding de las referencias es oficial** (partners de Movistar): usalas sin miedo. Regla de contenido: si la pieza nueva promociona otros titulos u otros dispositivos, describe el contenido nuevo en el prompt para no arrastrar el de la referencia. Pieza 100% Movistar sin partner: anade exclusion de logos ajenos (referencias sin partner: `tienda-plv-etiqueta-sin-ip.jpg` y `exterior-cartel-tipografico-paleta.jpg`).
7. **Columna `Ojo` del INDEX = exclusion explicita en el prompt.** El modelo copia los defectos igual que las virtudes. Casos registrados:
   - `exterior-mupi-producto-sobre-azul.jpg`: M azul sobre azul, contraste insuficiente → pedir contraste alto en el simbolo.
   - `fotografia/retrato-aficionado-cielo-contrapicado.jpg`: **contagia patrones de club** (camisetas y bufandas a rayas, escudos). Siempre con exclusion literal: "plain solid garments, no striped shirts or scarves, no club crests, no team colour patterns, no sponsor trims". Sin ella costo 7 generaciones para 3 piezas.
   - `tienda-plv-etiqueta-sin-ip.jpg`: el texto de la pieza esta en catalan → pedir castellano o zona de texto limpia.
8. **Cero referencias es correcto en dos casos, y solo en esos dos:**
   - Modo FOTO y **ninguno de los crops se parece a la escena** que necesitas. Esta medido: forzar un crop de escena distinta aporta menos que no poner ninguno, y ademas arrastra sus defectos. Ejemplo real: no hay crop de interior domestico, asi que una escena de salon va sin `--ref`.
   - Canal sin gold standard del formato: BTL, TMKS, D2D, SMS, push.

   En ambos casos: genera sin `--ref`, flaggea `sin_gold_standard` y explica el motivo en el rationale. **Nunca sustituyas por una referencia del otro modo ni de otra escena.** Una referencia equivocada es peor que ninguna.

**Limite conocido del set de fotografia (19/08/2026):** solo 4 crops (retrato de aficionado, calle con movil, parada de bus diurna, entorno de casa mediterranea). **No hay interior domestico, ni bar/Horecas, ni deporte sin marcas**, que son las escenas que mas piden las piezas. La dependencia real es el banco de imagenes de marca: ver `PETICION-REFERENCIAS-MOVISTAR.md`.

#### 3.B Comprobar antes de gastar credito

Una vez por sesion:

```bash
python3 scripts/generate_image.py -p "test" -o /tmp/t.png --aspect <ratio> \
  --ref references/gold-standards/<canal-o-fotografia>/<archivo>.jpg \
  --ref references/gold-standards/<canal-o-fotografia>/<archivo>.jpg \
  --dry-run
```

Debe decir `endpoint: .../v1/images/edits`, `encoding: multipart/form-data` y `refs: 2`. Si dice `generations` y `refs: 0`, las referencias no se estan pasando: para y arreglalo antes de generar la tanda.

#### 3.C Generar

Reglas del prompt, validadas en produccion. Son la diferencia medida entre pieza buena y pieza mediocre:

1. **El prompt describe la pieza (o la escena), nunca la referencia.** PROHIBIDO "following the reference", "the template", "the gold standard" o equivalentes. Escribe como si la referencia no existiera: que se ve, donde, con que luz, con que jerarquia, con que textos EXACTOS. La referencia entra solo por `--ref`.
2. **En modo PIEZA COMPLETA, cada texto literal y entre comillas**, precedido de su rol: `The white extrabold headline reads exactly "<titular>" in sentence case`. Lo que no describas, lo heredas de la referencia: incluido su titular y sus titulos de contenido.
3. **En modo FOTO, describe solo la escena** y cierra con las exclusiones de texto y logo.
4. **Parte del prompt calibrado del canal** si existe en `guidelines/magic-prompt.md` seccion "Entradas". Sustituye las variables por el copy real y no toques la parte fija.
5. **Toda cifra del prompt debe existir literal en el `copy_prototype`.** El modelo inventa precios plausibles: una cifra no aprobada llega a cliente. Si no esta, no la pongas.
6. **`--quality high` para entregables.** `medium` solo para pruebas.
7. **Exclusiones al final:** precio si la pieza no lo lleva, captions inventados junto al QR, logos de terceros no previstos, urgencia artificial, y las de la columna `Ojo` de cada referencia usada.

```bash
python3 scripts/generate_image.py \
  -p "<prompt>" -o outputs/<slug>-<zona>.png --aspect <ratio> --quality high \
  --ref references/gold-standards/<canal-o-fotografia>/<archivo-1>.jpg \
  --ref references/gold-standards/<canal-o-fotografia>/<archivo-2>.jpg
```

Las rutas de `--ref` son relativas a `movistar-visual-production/`. Ejecuta el script desde ahi. Si dice `ERROR: referencia no encontrada`, te imprime el cwd actual.

Limites del generador: lados multiplos de 16, lado maximo 3840 px, ratio maximo 3:1, referencias PNG/JPG/WEBP de menos de 25 MB.

**Tecnicas de produccion validadas (conservalas):**

- **Logo M en pieza generada:** el modelo no lo reproduce bien. Tapa la M generada con un parche del color exacto del fondo y superpon el SVG real de `brand/logos/`.
- **Formatos que exceden el ratio 3:1** (WOW 1920x384 = 5:1): genera el key art al ratio valido mas cercano y compon la pieza final programaticamente (crop + tipografia y logos reales sobre el color exacto). WOW y videocartela de la misma campana comparten key art.
- **La foto se genera al ratio real de su zona**, nunca a otro ratio para recortar despues.
- **La M en pantallas PLV de tienda no va en la pieza** (vive en los frames bumper). En el soporte impreso si va, segun pida el copy.

#### 3.D Documentar

En el design rationale, seccion Fotografia, por cada imagen: modo (FOTO o PIEZA COMPLETA) y por que · prompt literal · **referencias usadas por nombre de archivo** y por que esas · exclusiones metidas y de que columna `Ojo` vienen · generaciones necesarias y que fallo en las descartadas. Una entrada sin la linea de referencias esta incompleta.

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

MIRA el PNG (herramienta Read) y evalua. **Los puntos 6 a 13 son checks deterministas: se responden si o no, no se interpretan.** Salieron de defectos reales de una tanda de 17 piezas y son los que mas se escapan.

1. **Azul #0066FF presente**, maximo un color secundario, solo Movistar Sans, sentence case, CTAs especificos sin exclamacion.
2. **Fondo correcto del canal.** #FFFAF5 es la base en piezas offline, pero hay excepciones legitimas: display (fondo segun campana, ver `app-ads.md`), Meta (fondos variados por familia, incluidos salmon y verde claro, ver `app-meta.md`), M+ (modo claro/oscuro/foto, ver `app-movistarplus.md`), landing web (blanco puro + #EFF5FB, ver `app-web.md`). Consulta el guideline del canal antes de marcar un fondo como error.
3. **El patron del formato** en `brand/audit-report.md` (jerarquia, posicion de la M, estructura).
4. **Nada solapado, cortado ni desbordado.** Legibilidad a la distancia del soporte.
5. **La foto integra:** luz creible, personas reales, sin look CGI, coherente con el tono.
6. **El titular cierra con punto.** El sistema tipografico Movistar cierra el titular con punto final. Regla incondicional, no solo en impreso. En una tanda real faltaba en 14 de 17 piezas.
7. **El logo M donde manda el canal.** Meta: **abajo derecha**. Resto: arriba derecha o segun playbook. Pantalla PLV de tienda: sin M en pieza.
8. **El CTA del tipo correcto.** M+ (WOW y videocartela): **link subrayado con `>`, nunca boton**. Meta: **sin boton CTA en la imagen**. Resto: pill relleno azul.
9. **Sin jerga interna en copy de cliente.** Prohibido en pieza: "BAF", "Stand Alone", "Horecas", "SA", "winback", "churn", codigos internos. Si el copy de C los trae, traduce y flaggea `jerga_corregida`.
10. **Todo en sentence case.** Sin Title Case residual: "Vuelta al cole" no "Vuelta al Cole"; eyebrows sin mayusculas completas.
11. **Si el texto esta DENTRO de la imagen generada, lectura letra a letra con zoom.** Tildes, ñ, dieresis, signos de apertura, cifras y simbolo €. Y lectura semantica: ¿la frase tiene sentido? Caso real: "vuelve a sonar" donde el copy decia "sonar". Una errata es bloqueante.
12. **Fisica de escena** en la fotografia: sombras de contacto, objetos con apoyo creible, reflejos coherentes, sin duplicados imposibles. Es lo que delata la IA ante cliente.
13. **Producto hero:** si la pieza ensena un dispositivo concreto, que sea ese modelo. El modelo falla aqui (caso real: iPhone X donde iba un iPhone 17). Si no puedes garantizarlo, pide dispositivo generico o flaggea `producto_no_verificado`.
14. **Test de parecido:** puesta junto a las referencias reales, encaja como una mas.

Si algo falla, corrige y repite. Maximo 2 iteraciones. Si a la segunda el texto dentro de imagen no sale limpio, produce esa pieza con el HTML editable (texto vivo) y flaggea `texto_en_imagen_fallido`. Para el resto, entrega con flag `qa_visual_fallido` y detalle.

### 6. Mockup contextual (si es para presentar a cliente)

Sigue `guidelines/mockup-workflow.md`: pieza plana en PNG + template de `templates/mockups/` + `scripts/mockup_composer.py`. Si no hay template del formato, genera el entorno con `generate_image.py` (prompt de entorno vacio, sin branding), anota las esquinas en `.corners.json` y guardalo en la subcarpeta para reutilizar.

## Entregables por pieza

- `outputs/<pieza>.html` ensamblado (autocontenido) o `.slots.html` + assets si piden editable
- `outputs/<pieza>.png` render verificado
- Mockup contextual si aplica
- Entrada en el design rationale con modo, prompt, referencias y resultado del QA visual

## Anti-patrones

- Escribir base64 a mano (fuentes, logos, imagenes): NUNCA. Es la causa historica de tipografia rota.
- **Mezclar modos de referencia**: pieza completa como referencia de una foto pura, o al reves.
- **Mencionar la referencia dentro del prompt.**
- **Poner una cifra que no esta en el `copy_prototype`.**
- Placeholder dashed en una entrega final: solo con flag `imagen_provisional` y motivo.
- SVG a mano alzada con coordenadas para formatos fotograficos: usar HTML fijo + render.
- Entregar sin haber mirado el render: prohibido.
- Inventar HEX o tokens: si falta un valor, TODO + flag. Y verifica el nombre del token contra `colors.css`.
- Pasar un corrector ortografico sobre el frontmatter o los bloques de codigo de esta skill.
