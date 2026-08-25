# Principios de diseño de deck — Movistar (criterio para decks de nivel)

> Esta referencia es **CRITERIO de planificación y QA**, no una licencia para tocar tamaños/colores a
> mano. La tipografía, posición y tamaño los da el **layout de la plantilla** (regla dura de la
> skill). Usa esto para: (1) planificar el deck, (2) elegir layout, (3) revisar por visión. Combina
> la **normativa oficial Movistar** (Brand Guardian v4, dividido por tema en
> `movistar-brand-guidelines/brand/*.md` — logo, tipografía, layout-grid, etc.) con buenas
> prácticas universales y tendencias 2026, adaptadas a la marca.

## 1. Las 5 reglas que más elevan un deck (aplícalas siempre)
1. **Una idea por slide.** El público debe captar cada slide en ~3 segundos (Duarte). Si una slide
   necesita más, pártela. Nada de "slide-documento".
2. **Aire = 15-20% del slide vacío como mínimo.** Márgenes amplios, menos elementos, respira. El
   vacío dirige la mirada; el amontonamiento la mata.
3. **Jerarquía clara (≈3:1).** Un solo foco por slide: titular grande → subtítulo medio → cuerpo
   pequeño. Si todo grita, nada se oye. Resalta UN dato, no cinco.
4. **Alinea todo a la retícula.** Bordes y bloques compartiendo ejes. La consistencia se nota; el
   desorden de 4 px también.
5. **Cuenta, no enumeres.** Di la conclusión ANTES del dato ("las altas crecen un 30%", no una tabla
   muda). Aproxima el deck como un guion visual, no como un informe.

## 2. Normativa Movistar destilada para slides 16:9
(De `movistar-brand-guidelines/brand/logo.md`, `layout-grid.md`; la plantilla ya la encarna — esto es
para PLANIFICAR y REVISAR.)
- **Logo (M):** lo pone el master. Posición prioritaria **esquina superior derecha** (alt. inferior
  derecha). **1 sola M por slide**, **azul `#0066FF`** (blanca solo sobre azul Movistar o foto
  azulada legible). No añadir a mano, no recolorear. Si la M va abajo-derecha, el peso del título
  va arriba-izquierda.
- **Margen de seguridad:** ~**1/16 del lado corto** del formato. En 16:9 (19,05 cm de alto) ≈ **1,2
  cm** de margen vivo; deja ese aire respecto a bordes y a la M.
- **Jerarquía tipográfica** (proporciones relativas a Y = altura de mayúscula del titular):
  H1 Bold (Extrabold en 1-2 palabras) · subtítulo **0.45Y** · bodycopy **0.30Y** · legal **0.15Y**.
  En la práctica del deck: elige el layout cuyo rol de título/cuerpo respete esta jerarquía; no
  metas un párrafo donde el layout espera un titular.
- **Color (proporción objetivo):** ~**40% azul · 30% blanco Movistar · 10% negro · 20% secundarios**.
  El azul es el ancla de marca; los secundarios (verde `#CEF7BF`, amarillo `#FFE99C`, coral
  `#FFC5A8`, azul claro `#D3EEFF`) **acentúan por capítulo**, no dominan.
- **Prohibiciones de color:** secundario claro **nunca** sobre fondo claro (combinación "Prohibido"
  de la matriz); azul Movistar **no** en el contenedor destacado (compite con la M); blanco/negro
  puro nunca (usa `#FFFAF5` / `#262423`).
- **Destacar un dato:** un único contenedor de resalte por slide, vértices redondeados, sobre una
  palabra o una línea. No abuses.
- **Precios:** formato `45€`, `5 GB`, `300Mb`; estilo de composición de precios de la Guía.

## 3. Tendencias 2026 — cómo modernizar SIN romper Movistar
- **Tipografía protagonista.** Titulares cortos y potentes (1-2 palabras → Extrabold ajustado a
  márgenes). Deja que el texto sea el grafismo. Layouts `1_Statement`/`Separador` brillan aquí.
- **Calidez para humanizar el azul.** La tendencia huye del "azul corporativo frío"; Movistar ES
  azul, así que aporta calidez por **fotografía** (momentos `atardecer`/`tarde`, mood `calido`) y
  acentos **coral/amarillo**, manteniendo el azul como ancla. Resultado: cercano, no corporativo.
- **Profundidad y asimetría con criterio.** La retícula se mantiene, pero composiciones asimétricas
  (foto a sangre + bloque de texto desplazado) dan energía. Sin sombras baratas ni 3D.
- **Data storytelling.** Convierte tablas en una conclusión + 1-2 cifras clave; usa `rows=` para
  tablas reales, no listas. Reserva el detalle para un anexo o pre-read.
- **Pensar híbrido.** El mismo deck puede vivir como keynote 16:9, PDF para enviar y, a futuro,
  vertical/web. Mantén titulares y jerarquía que funcionen recortados (ver roadmap multiformato).

## 4. Fotografía (resumen; detalle en `movistar-brand-guidelines/imagery`)
- Foto solo si **aporta** (portada, separador, momento emocional/producto/marca). En datos/texto,
  a menudo mejor sin foto.
- **Texto sobre foto SIEMPRE con zona de contraste/scrim.** Respeta `usos_evitar` (p.ej. full-bleed
  en bodegones) y **no repitas** foto en el deck.
- Alinea **momento del día** con el tono del capítulo (cálido → `atardecer`/`tarde`; sereno →
  `mediodia`/`manana`; entretenimiento → `noche`; producto → `general`).

## 5. Pre-flight de calidad (pásalo antes de entregar)
- [ ] ¿Cada slide se entiende en 3 segundos y tiene UNA idea?
- [ ] ¿Hay aire real (15-20%)? ¿Nada amontonado ni a sangre sin querer?
- [ ] ¿Jerarquía evidente (un solo foco) y todo alineado a eje?
- [ ] ¿Proporción cromática ~40/30/10/20 y azul presente en cada slide?
- [ ] ¿Variedad de layouts (no 3 iguales seguidos; <40% `Title and Content`)?
- [ ] ¿Titulares cortos, sin punto final, sin em-dash, "M" en mayúscula, es-ES?
- [ ] ¿Datos como conclusión + cifra clave (no tabla muda)?
- [ ] ¿Foto solo donde aporta, con scrim y sin repetir?
- [ ] ¿1 logo (del master) por slide, azul, sin añadir a mano?
- [ ] Cruza también el checklist de "fallos automáticos" del QA por visión (`SKILL.md`).

## 6. Referencia real: patrones de un deck de agencia (Plan Comercial B2C, jul-2026)

> Deck de agencia real (no construido sobre esta plantilla) compartido por el cliente como ejemplo de
> "buen nivel". Útil como referencia de estilo y de qué se percibe como "deck decente" en Movistar —
> **no** implica que el catálogo actual (54 slides canónicas) pueda reproducir todo
> literalmente. Se marca explícitamente qué sí es alcanzable hoy y qué no.

**Patrones que SÍ están cubiertos por el catálogo actual** (úsalos con más confianza al verlos aquí):
- Portada/separador de capítulo con foto full-bleed → `PORTADA_FOTO_BLEED_SCRIM*` y
  `SEPARADOR_FOTO_*`; con foto enmarcada → `PORTADA_FOTO_MARGEN*`.
- Cabecera de sección arriba de cada slide (p.ej. "JULIO/COMUNICACIÓN") → `set_page_header()` sobre
  el rol `title`/`subtitle` de cada interior.
- Titular como conclusión, nunca como enunciado del tema → ya es la regla nº5 de este documento.
- Tarjetas de precio/oferta lado a lado sobre fondo de color secundario claro →
  `COMPARATIVA_2_PANEL`/`COMPARATIVA_3_PANEL`.
- Timeline/roadmap exactamente de tres etapas → `TIMELINE_3_FASES`.
- Mosaicos de 2, 3 o hasta 15 imágenes → `GRID_2IMG_CAPTION`, `GRID_3IMG_CAPTION` o
  `GRID_MOSAICO_15`.
- M en la esquina inferior derecha (no solo la superior) → **confirmado como uso real**, coincide con
  la "alternativa" ya documentada en `brand/logo.md` §7.1.2 — no es una desviación de marca.

**Patrones que el catálogo actual NO puede reproducir hoy** (no los prometas ni los improvises con
primitivas sueltas — si el contenido los pide, usa la alternativa más cercana del catálogo y anótalo
en el resumen; no dibujes formas/gráficos custom fuera de los arquetipos):
- **Gráficos nativos de dato fuera de los gauges existentes** (barras con badge de variación,
  waterfall de altas/bajas/ganancia neta). Alternativa: `INTERIOR_TABLA`; para hasta 5 porcentajes,
  sí existe `INFOGRAFIA_GAUGES`.
- **Timelines de más/menos de tres fases o con ramificaciones**. `TIMELINE_3_FASES` exige exactamente
  tres hitos; para otra cardinalidad usa tabla o divide el proceso en varias slides.
- **Grids mayores de 15 imágenes o con geometría irregular**. Elige el grid canónico de 2/3/15 y
  divide el contenido en varias slides antes que improvisar una cuadrícula nueva.
- **Separadores minimalistas** (solo "M+" centrado + línea, sin número gigante). El catálogo usa
  `SEPARADOR_NUMERO_*` con número grande por diseño — no lo sustituyas por una composición improvisada.

Extender el motor con gráficos nativos adicionales (python-pptx `chart` API) sería un desarrollo
aparte — no una tarea de esta referencia.

## Fuentes
Normativa: `movistar-brand-guidelines/brand/*.md` (Brand Guardian v4 por tema) + `brand/contrast-matrix.md`. Buenas
prácticas y tendencias: Duarte *Slide:ology* (regla de los 3 s, data storytelling), guías de diseño
de presentaciones 2026 (tipografía bold, aire 15-20%, jerarquía 3:1, retícula + asimetría, decks
híbridos 16:9/9:16/PDF).
