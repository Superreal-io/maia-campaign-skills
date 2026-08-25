# Banco de imágenes de marca Movistar — guía de selección

> Documento de referencia de la skill `movistar-brand-guidelines`. Cárgalo cuando
> un output (deck, PDF, documento, etc.) pueda mejorar con una foto de marca. El
> catálogo semántico está en `imagery/imagery-index.json`.

Banco curado de imágenes de marca, clasificadas y listas para usar. **81 imágenes**: el set temático previo (8 categorías: personas, hogar, conectividad, producto, deporte, paisaje, urbano, marca) **+ 46 fotos oficiales del banco Movistar 2025** organizadas además por **momento del día** **+ 12 fondos de color plano** (`categoria: "fondo"`, uso muy acotado — ver más abajo, no cuentan como "fotografía de marca" normal).

> Nota: el índice (`imagery/imagery-index.json`) y la guía se quedan siempre bundleados en la skill
> (son ligeros). Los **binarios** de las fotos, en cambio, pueden venir de dos sitios — no asumas
> cuál: bundleados en `imagery/assets/imagery/<carpeta>/` (algunas marcas/entornos) o inyectados por
> el backend vía `container_upload` en runtime (Azure). En `.pptx`, usa siempre `list_brand_images()`
> de `movistar-pptx` para resolver la ruta real; no la construyas a mano. Las 46 oficiales llevan
> `fuente: "oficial-movistar-2025"` y `momento_dia`.

## Estructura del banco

```
movistar-brand-guidelines/
└── imagery/
    ├── imagery-guide.md            ← este archivo (algoritmo de selección)
    ├── imagery-index.json          ← metadata semántica de cada imagen
    └── assets/imagery/<carpeta>/   ← ficheros reales: temáticas + momentos del día + fondos
```

Catálogo de 81 imágenes. Carpetas temáticas (personas, hogar, conectividad, producto, deporte, paisaje, urbano, marca), carpetas por **momento del día** del banco oficial 2025 (`atardecer`, `manana`, `mediodia`, `noche`, `tarde`, `general`), y `fondos/` (12, categoria `fondo`, ver §Fondos de color plano abajo — no entran en la selección normal). Cada entrada del índice tiene un `id` semántico y un campo **`source_file`** con la **ruta relativa a `imagery/assets/imagery/`** (p.ej. `tarde/movistar-tarde-03.png`). Para colocar una imagen en `.pptx`, resuélvela siempre vía `list_brand_images()` (no construyas la ruta a mano — ver nota de arriba).

### Fondos de color plano (`categoria: "fondo"`) — excluidos de la selección normal
Las 12 entradas con `categoria: "fondo"` llevan el lockup y el claim **fijo** "es por todos." incrustado en la imagen. **No las elijas** siguiendo el proceso normal de selección de abajo (aunque crucen bien por color/momento) — son uso muy acotado, solo cuando ese mensaje concreto encaje con la pieza (employer branding/cultura interna). Respeta siempre su `usos_evitar`/`reglas`/`notas` antes de considerarlas.

### Selección por momento del día (banco oficial 2025)
Cuando el output tenga una hora/atmósfera concreta o quieras un look de campaña coherente, filtra por **`momento_dia`**: `manana` (luz suave, familiar/cotidiano), `mediodia` (luz plena, activo/profesional), `tarde` (cálido, juvenil/senior), `atardecer` (dorado, emocional), `noche` (entretenimiento, movilidad, eventos), `general` (bodegón de producto y ambiente de hogar; sin momento). Combina `momento_dia` + `categoria` + `tags` + `mood` para elegir. El **mapa capítulo→color** del deck puede alinearse con el momento (p.ej. capítulo cálido → `atardecer`/`tarde`).

### Reglas (en el índice)
El índice trae **`reglas_globales`** (reglas duras transversales: sandbox→PPTX/PDF no web, no texto sin scrim, no repetir foto en un deck, color como hilo conductor, etc.) y un campo **`reglas`** por entrada (constraints específicas, p.ej. `evitar_full_bleed_con_texto` en bodegones de producto, `la_M_siempre_azul_movistar` en imágenes de marca). Respeta ambos al elegir y colocar una imagen.

## Cuándo usar esta guía

Siempre que estés produciendo un output Movistar y decidas que una imagen de marca lo mejora — portada, separador, fondo, hero, acompañamiento de texto. Tú decides **cuándo** conviene una foto y **cuál**. **No** usar para logos, iconos UI o capturas de pantalla: esta skill es solo para **fotografía de marca**.

**Excepción — decks `.pptx`:** dentro de un deck manda la skill `movistar-pptx`; si da sus propias reglas de imagen, variedad o colocación, prevalecen sobre esta guía.

**Disponibilidad por tipo de output:**
- **PPTX / PDF** — el fichero está en el sandbox: resuélvelo vía `list_brand_images()` (`movistar-pptx`), nunca incrustes el binario a mano.
- **Artifacts HTML/React** — **no incrustes el binario** (CSP/offline no lo permite), pero SÍ puedes referenciar una foto emitiendo `movistar://<id>` en el HTML (el `id` es el de `imagery-index.json`) — el backend lo resuelve a una URL de blob firmada antes de servir el artifact. Si esa resolución no aplica en tu contexto, prioriza copy/paleta/logo/tipografía sin foto.

## Proceso de selección (sigue este orden)

### Paso 1 — Prioridad absoluta: uploads del usuario
Si el usuario ha adjuntado imágenes propias al job (carpeta de overrides), **esas ganan siempre** al banco interno. Esta skill solo rellena lo que el usuario no haya cubierto.

### Paso 2 — Filtrar por categoría y tags según el slide
Para cada slide que necesite imagen:

1. Identifica la **categoría principal** según el tema del capítulo o del slide:
   - Fútbol / LaLiga / Movistar Plus deporte → `deporte`
   - Fibra / router / dispositivos → `producto`
   - Servicios residenciales / familia / senior → `hogar`
   - Portadas épicas / separadores de capítulo → `paisaje` o `deporte`
   - Empresas / trabajo / B2B → `urbano`
   - Uso cotidiano del móvil → `conectividad`
   - Retratos editoriales / equipo / diversidad → `personas`
   - Cierre institucional / brand / presencia retail → `marca`

2. Lee `imagery-index.json` y filtra imágenes de esa categoría.
3. Ranquea por coincidencia de `tags` con el contexto del slide (título, bullets, capítulo).
4. Aplica restricciones de `usos_recomendados` vs `usos_evitar` según el layout:
   - Slide con texto denso → no usar imágenes con `usos_evitar: ["fondo_texto_denso"]`.
   - Layout full-bleed 16:9 → preferir imágenes con `aspect: "16:9"` en `usos_recomendados: ["full_bleed"]`.
   - Layout cuadrado → `aspect: "1:1"`.

### Paso 3 — Rotación para evitar repetición

Cada vez que se genera un deck, el job trae un `deck_id` (o si no lo hay, usa la marca de tiempo). Úsalo como seed:

1. De los candidatos rankeados, ordena alfabéticamente por `id`.
2. Calcula `offset = hash(deck_id) % len(candidatos)`.
3. Elige el candidato en posición `offset`.
4. Añade ese `id` a una lista `usadas_en_este_deck` y no lo reutilices dentro del mismo deck.

Esto garantiza que dos decks sobre el mismo tema escojan imágenes distintas, y que dentro de un mismo deck no se repita la misma foto.

### Paso 4 — Afinidad cromática con el capítulo

Movistar usa 3 colores por capítulo: **Cap 01 azul** (`#0066FF`), **Cap 02 verde** (`#E2F8D5`/`#38552B`), **Cap 03 amarillo** (`#FFF0C0`/`#5E4A09`).

Si el slide está marcado con `chapter_color`, prefiere imágenes cuyos `colores_dominantes` armonicen:
- Capítulo azul → imágenes con azul profundo o cielo azul (ej. `playa-espejo-atardecer`, `movil-naranja-fondo-azul`, `libertad-azul-movistar`, `bienestar-rostro-sol`).
- Capítulo verde → tonos naturales, paisaje vegetal (ej. `camiseta-mediterraneo`, `ciclista-costa`).
- Capítulo amarillo → luz cálida, amanecer, atardecer dorado (ej. `montanero-amanecer-nieve`, `carretera-costera-motos`, `familia-padre-bebe`).

Esta afinidad es **preferencia, no obligación**. Si no hay match cromático, prioriza semántica.

## Reglas duras

1. **Nunca repitas la misma imagen dentro del mismo deck.**
2. **La imagen de `marca` (logo Movistar en fachada) solo va en portadas institucionales o slide final de cierre. No usar de forma decorativa.**
3. **`diversidad-trio-editorial` es la única imagen en aspect 1:1.** Solo para layouts que admitan cuadrado.
4. **Si el banco no tiene un match decente (score < 0.4 en relevancia), no metas una imagen irrelevante:** es mejor dejar el slide sin foto y notificar con `qa_flag: "imagen_no_encontrada"` que colocar algo forzado.
5. **Respeta `usos_evitar`** del índice — si una imagen no es apta para texto denso, no la pongas de fondo a un slide con mucha copy.

## Ejemplo práctico

Deck: "Informe social orgánico Movistar Q1 2026"
- Slide 1 (Portada): Cap 01 azul, tema general → candidato ganador `libertad-azul-movistar` o `playa-espejo-atardecer` según rotación.
- Slide 3 (Separador Cap 01 · Contexto): azul → `movil-naranja-fondo-azul`.
- Slide 5 (KPIs · uso móvil): conectividad cotidiana → `movil-cocina-casual`.
- Slide 7 (Cap 02 · Audiencia senior): verde + hogar → `senior-pareja-tablet`.
- Slide 9 (Cap 03 · Patrocinio LaLiga): amarillo + deporte → `futbol-silueta-atardecer` o `estadio-futbol-movil`.
- Slide 11 (Cierre institucional): marca → `marca-logo-fachada`.

## Extensión futura

Para añadir más imágenes:
1. Copia el archivo a la subcarpeta de categoría que corresponda en `assets/imagery/`.
2. Añade una entrada al array `images` de `imagery-index.json` con todos los campos requeridos (`id`, `source_file`, `categoria`, `tags`, `mood`, `colores_dominantes`, `w`, `h`, `aspect`, `usos_recomendados`, `notas`).
3. Actualiza `total_images` y `updated` en el header del JSON.
4. Si el banco supera las ~80 imágenes, considera mover los archivos a blob storage y dejar solo el `imagery-index.json` con URLs dentro de la skill (ver sección "Escalado" abajo).

## Escalado a banco grande

Para más de ~80 imágenes, patrón recomendado:
- `imagery-index.json` vive en la skill con campo `url` (firma temporal) en lugar de archivo local.
- Añadir tool `get_brand_image(id)` que descarga el archivo bajo demanda al sandbox del agente.
- La skill solo lleva el índice (decenas de KB). Las imágenes viven en S3/GCS.

Esto mantiene la skill ligera y permite escalar a miles de imágenes sin penalizar contexto.
