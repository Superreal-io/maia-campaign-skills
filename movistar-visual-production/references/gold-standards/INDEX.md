# Gold Standards — referencias que se pasan al generador de imagen

Esta carpeta NO es el catálogo completo de referencias. Es la **selección curada** de piezas
reales Movistar que se pasan al modelo con `--ref` en `scripts/generate_image.py`.

El catálogo completo (41 piezas, muchas de ellas capturas de pantalla o mockups) está en
`../INDEX.md` y sirve para MIRAR con Read antes de diseñar. Los Gold Standards son las que
se pueden pasar al modelo sin ensuciar el resultado.

---

## Criterio de admisión

Una pieza entra aquí si cumple las cuatro:

1. **Es la pieza, no la captura.** Sin cromo de navegador, sin AdChoices, sin UI de terceros
   alrededor, sin dos piezas pegadas en un mismo archivo.
2. **Sin marcas de terceros dominantes.** Ni logos de plataformas, ni escudos, ni caras
   identificables de deportistas o famosos. Si el modelo ve un logo de Netflix en la
   referencia, lo reproduce.
3. **Sin defectos de marca visibles.** Erratas, M azul sobre azul, palabras pegadas.
   Si la pieza tiene un defecto pero su composición vale, entra con la columna **Ojo**
   rellena y el defecto se declara en el prompt como exclusión.
4. **Resolución suficiente para que se lea la jerarquía.** Idealmente ≥1000 px de lado largo.
   Las que están por debajo entran marcadas `res-baja` porque la composición vale aunque
   el detalle tipográfico no se lea.

Todas están normalizadas a **JPEG q90, lado largo máximo 1536 px**. Las imágenes de entrada
se facturan como tokens: pasar un PNG de 2 MB cuesta dinero y no mejora nada.

---

## Catálogo

| Archivo | Canal | Formato real | Modo | Qué demuestra | Ojo |
| --- | --- | --- | --- | --- | --- |
| `references/gold-standards/exterior/exterior-mupi-foto-sangre.jpg` | Exterior | MUPI digital vertical ~1:2, mockup en parada diurna | **FOTO** | Foto a sangre con una sola palabra-marca en blanco gigante pisando la imagen, subtítulo a 1/4 de ese cuerpo, tagline de 4 palabras con punto abajo izquierda y M azul abajo derecha sobre la propia foto. Retrato recortado sin cara, camisa cobalto que liga con la marca | — |
| `references/gold-standards/exterior/exterior-cartel-marco-color-notch.jpg` | Exterior | Serie de 3 carteles verticales ~2:3, mockup con sombra de hiedra | **FOTO** + marco plano | El sistema marco-de-color + foto con esquinas redondeadas y muesca recortada donde se aloja el titular y la M. Y la regla de contraste: sobre crema o salvia el titular va en el tono oscuro del mismo matiz y la M en azul; sobre azul Movistar, titular y M en blanco. Fotografía documental, grano suave, luz natural, gente real | — |
| `references/gold-standards/exterior/exterior-cartel-tipografico-paleta.jpg` | Exterior | Serie de 5 carteles verticales ~2:3, wild-posting en muro | **GRÁFICO** | La única referencia de paleta extendida sin foto, sin precio y sin CTA: un color plano por cartel (azul Movistar, azul hielo, verde salvia, mostaza claro, terracota), M en esquina superior derecha, eyebrow bold pequeño y remate bold grande a 4-5 líneas alineado izquierda, siempre con punto final | Los carteles de los extremos quedan cortados por el encuadre |
| `references/gold-standards/exterior/exterior-mupi-producto-sobre-azul.jpg` | Exterior | MUPI vertical ~2:3, mockup calle nocturna | MIXTO | MUPI de producto sobre color: azul Movistar con degradado radial más claro al centro, titular blanco a izquierda a 3 líneas arriba, bodegón recortado sin fondo al centro, pie con claim + legal de 1 línea + M abajo derecha | **Defecto: M azul sobre azul, contraste insuficiente.** No copiar |
| `references/gold-standards/digital/digital-vertical-titular-xl-foto-documental.jpg` | Digital | Artboard vertical 5:8 (app / display vertical) | MIXTO | Titular azul brillante enorme a 3 líneas sobre azul hielo + bajada del nombre de producto en el mismo azul a la mitad de cuerpo. Foto humana documental de verdad (luz cálida de interior, no stock brillante) recortada con radio, M azul suelta como elemento gráfico y mockup de móvil sangrando por el borde | El importe de factura va difuminado a propósito |
| `references/gold-standards/digital/digital-landing-precio-sobre-foto.jpg` | Digital | Landing / email de campaña 2:3 | MIXTO | Cómo se monta el precio SOBRE foto: caja azul sólida con radio, importe blanco gigante con los decimales a tamaño completo y `/mes` a un tercio, y sub-etiqueta blanca DENTRO de la caja para la condición. Badge circular navy arriba derecha, caja blanca de utilidad saliéndose del hero, y chips de variante dinámica | `res-baja` (595 px) |
| `references/gold-standards/digital/digital-landing-ventaja-personal-grid.jpg` | Digital | Landing de ventaja personalizada 2:3 | MIXTO | Pieza de ventaja personal: el nombre del cliente dentro del titular a 4 líneas alternando navy y azul brillante, badge circular azul con el importe, bodegón 3D sobre pedestal circular con sombra suave, y grid 2x3 donde cada celda repite el mismo patrón (foto / categoría / importe en azul bold / link con flecha) | `res-baja` (411 px) |
| `references/gold-standards/email/email-multiproducto-3-cards.jpg` | Email | Email completo 9:16 (hero + 3 cards + cierre) | MIXTO | Titular a dos voces: parte bold navy + remate estacional en cursiva manuscrita cyan. Hero de collage de 3 fotos cosidas y sistema de 3 tarjetas donde el color del icono circular y del CTA outline codifica cada submarca. **Sin ningún precio en toda la pieza** | `res-baja` (508 px) |
| `references/gold-standards/email/email-oferta-grafico-price-card.jpg` | Email | Email de oferta 100% gráfico 9:16 | **GRÁFICO** | Price-card navy a la derecha del titular: importe a 4x el cuerpo en blanco, `/mes` a un tercio, chip oscuro con el ahorro en euros y en porcentaje, y PVP de referencia en gris sin tachar. Todo lo demás en tarjetas blancas de radio grande sobre azul hielo. Los partners van escritos como texto en chips outline, sin logos | `res-baja` (454 px) |
| `references/gold-standards/email/email-oferta-comparativa-precio.jpg` | Email | Email de oferta con comparativa 2:3 | MIXTO | La jerarquía de precio más agresiva del set: caja navy con importe blanco gigante, chip amarillo con el ahorro en navy (único uso admitido del amarillo como color de urgencia), PVP tachado en rojo y flecha al precio final en caja azul claro. Checks verdes sobre la banda navy | `res-baja` (506 px). Lleva logos de plataformas en cajas blancas: si generas con esta referencia, excluye logos en el prompt |
| `references/gold-standards/tienda/tienda-chevalet-3-cajas.jpg` | Tienda | Chevalet tipo A ~2:3, mockup en punto de venta | MIXTO | Chevalet de oferta en tres cajas apiladas: caja azul hielo con `Hasta` pequeño + importe a 4x + bodegón recortado / banda navy de oferta cruzada con pastilla amarilla / caja outline azul con icono bocadillo y llamada a la acción de tienda. Titular partido en dos colores: primera mitad navy, segunda azul brillante con punto | `res-baja` (442 px). Lleva logo de partner a gran tamaño en la banda navy: excluir en el prompt |
| `references/gold-standards/tienda/tienda-entorno-muro-verbos.jpg` | Tienda | Interior de tienda flagship 16:9 | **FOTO** (entorno) | Sirve para el ENTORNO retail, no para layout de pieza: columnas de piedra, terrazo blanco, focos de teatro, mesas de madera con base azul, pantalla vertical azul con M blanca, panel amarillo puntual. Y el recurso del muro de verbos en primera persona del plural, en azul Movistar sobre azul hielo, sangrando por los cuatro lados | Úsala como referencia de mockup o de ambiente, no de composición de pieza |
| `references/gold-standards/tienda/tienda-plv-producto-precio-samsung.jpg` | Tienda | Pantalla digital PLV 16:9 (frame compuesto de vídeo) | MIXTO | La anatomía canónica de PLV de dispositivo: fondo pastel (verde menta), titular azul sentence case, nombre de producto con lockup MovistarSwap, "Desde 16€/mes" negro gigante, claim de renovación a 24 meses, legal de una línea, producto hero en render. Sin M: en las pantallas de vídeo la M vive en los frames bumper | Logo Samsung en titular y dispositivo: excluir marcas en el prompt o sustituir por dispositivo genérico |
| `references/gold-standards/tienda/tienda-plv-producto-precio-iphone.jpg` | Tienda | Pantalla digital PLV 16:9, segunda campaña | MIXTO | Misma plantilla con otro fondo (amarillo pálido), otro producto y otro precio: par con la de Samsung para abstraer el patrón, no la pieza. Incluye etiqueta energética | Logo Apple en texto y dispositivo: excluir |
| `references/gold-standards/tienda/tienda-plv-producto-precio-vertical-samsung.jpg` | Tienda | Pantalla digital PLV 9:16 (tótem vertical) | MIXTO | Cómo se reordena la misma pieza a vertical: titular arriba, producto al centro, bloque de oferta y precio abajo. Imprescindible para el tótem 1080x1920 del escaparate | Logo Samsung: excluir |
| `references/gold-standards/tienda/tienda-plv-multiproducto-verano.jpg` | Tienda | Pantalla digital PLV 16:9 multiproducto | MIXTO | La plantilla multiproducto: titular azul, 3 productos con caption cada uno, subtítulo de ventaja de cliente, legal. **Sin precio**: la PLV multiproducto comunica ventaja, no importe | Logos Xiaomi, Samsung y PlayStation en los productos: excluir |
| `references/gold-standards/tienda/tienda-plv-etiqueta-ser-cliente.jpg` | Tienda | Pantalla digital PLV 16:9, frame secundario | MIXTO | El recurso de la etiqueta colgante de papel con cordón azul ("Descuento Exclusivo Clientes") + titular "Ser cliente tiene ventajas". Es el frame 3 de la misma animación que la multiproducto: segunda composición del mismo loop | Logos de producto: excluir |
| `references/gold-standards/tienda/tienda-plv-etiqueta-sin-ip.jpg` | Tienda | Pantalla digital PLV 16:9, solo tipografía | **GRÁFICO** | **La única pieza del set 100% libre de marcas de terceros.** Etiqueta colgante 3D con cordón azul + titular en negro + legal, sobre panel pastel con marco crema. La referencia más segura para generación | Texto en catalán ("Ser client té avantatges"): el prompt debe pedir el texto en castellano o dejar la zona de texto limpia |
| `references/gold-standards/tienda/tienda-storepage-banner-compacto.jpg` | Tienda | Banner store page 600x300 | MIXTO | Cómo se condensa la pieza a formato compacto: producto a la izquierda, oferta + precio al centro y caja azul sólida con titular blanco abajo a la derecha | `res-baja` (600 px) y logo Samsung: excluir |
| `references/gold-standards/tienda/tienda-plv-mosaico-ficcion-disney.jpg` | Tienda | Pantalla digital PLV 16:9 (campaña de contenidos) | MIXTO | La plantilla de PLV de entretenimiento: titular negro arriba, subtítulo con el nombre de la oferta, fila de logos de las plataformas agregadas, mosaico de carátulas con una en foco y el resto desenfocado. Es cómo Movistar comunica contenidos de partner en tienda | Campaña reciente y oficial. El key art es del partner: si la pieza nueva lleva otros títulos, descríbelos en el prompt |
| `references/gold-standards/tienda/tienda-plv-mosaico-ficcion-disney-vertical.jpg` | Tienda | Pantalla digital PLV 9:16, misma campaña | MIXTO | La versión tótem vertical del mosaico: titular arriba, mosaico al centro, fila de logos abajo | Ídem |
| `references/gold-standards/tienda/tienda-plv-poster-destacado-ficcion.jpg` | Tienda | Pantalla digital PLV 16:9, frame secundario | MIXTO | El recurso de carátula única destacada: un solo título en grande con su línea de copyright, titular y logos arriba. Segunda composición del mismo loop que el mosaico | Ídem |
| `references/gold-standards/tienda/tienda-perimetral-mockup-6-pantallas.jpg` | Tienda | Mockup del canal perimetral (6 pantallas 16:9 en fila, 3 estados) | MIXTO | La única evidencia de cómo funciona el perimetral: mensaje troceado en 6 pantallas encadenadas, alternancia bumper (azul + M) / contenido, cada pantalla es un 16:9 estándar | Es mockup de mecánica de canal, no pieza plana: para generar una pantalla individual usa las PLV 16:9 normales |
| `references/gold-standards/movistarplus/movistarplus-videocartela-completa-qr.jpg` | Movistar+ | Videocartela 1920x1080 (Ficción Total) | MIXTO | La videocartela canónica con todos los módulos del sistema: logo Movistar arriba, titular blanco, módulo blanco con logos de las plataformas agregadas, pastilla blanca con la keyword en azul, precio grande, legal "Durante 6 meses \| Sin permanencia", QR con CTA de contratación, 3 pósters a la derecha. Sobre azul Movistar, no negro | Key art licenciado (SkyShowtime, HBO Max, Apple TV): la referencia enseña estructura, el prompt debe excluir el contenido |
| `references/gold-standards/movistarplus/movistarplus-videocartela-cobranding-disney.jpg` | Movistar+ | Videocartela 1920x1080 (co-branding Disney+) | MIXTO | La gemela de la anterior en versión co-branding de una sola marca: junto a la de Ficción Total enseñan qué es constante (estructura, QR, legal, precio) y qué es variable (marca invitada, copy). Logo del partner integrado junto al titular | Máximo co-branding: logo Disney+ y key art de sus títulos. Excluir contenido en el prompt |
| `references/gold-standards/movistarplus/movistarplus-wow-banner-ficcion.jpg` | Movistar+ | WOW banner 1920x384 (ratio ~5:1) | MIXTO | El formato WOW completo: titular blanco a 3 líneas a la izquierda, pastilla blanca con keyword azul, precio gigante, 3 pósters a la derecha, fondo azul Movistar | Key art licenciado. Par con el WOW de Disney para abstraer el patrón |
| `references/gold-standards/movistarplus/movistarplus-wow-banner-disney.jpg` | Movistar+ | WOW banner 1920x384, segunda campaña | MIXTO | Mismo patrón WOW con otra campaña y otro precio: pasadas juntas, el modelo aprende la retícula en vez de copiar una pieza | Key art Disney. Excluir contenido |
| `references/gold-standards/movistarplus/movistarplus-web-banner-ficcion.jpg` | Movistar+ | Banner web 2000x465 | MIXTO | El formato web: texto a la izquierda (titular + pastilla + precio + link subrayado "Más información >"), muro de carátulas a la derecha | Key art licenciado |
| `references/gold-standards/movistarplus/movistarplus-ui-campana-oscura-precio-tachado.jpg` | Movistar+ | Campaña dentro de la UI real de M+ (Deportes Total) | MIXTO | La única muestra del modo oscuro: la pieza es oscura por el key art, no por fondo negro plano. Y el único ejemplo de precio con tachado en M+ ("23€/mes" con 29€ tachado) + línea legal de copyright + CTA "Contrátalo aquí >". Enseña dónde vive la campaña dentro de la UI | Copyright F1 impreso en la pieza, logos DAZN y plataformas en la UI. Solo estructura |
| `references/gold-standards/movistarplus/movistarplus-smartphone-compuesto-disney.jpg` | Movistar+ | Pieza smartphone vertical compuesta (1440x2986) | MIXTO | La única muestra del formato smartphone: muro de carátulas arriba, titular con el logo del partner integrado inline, pastilla de descuento, precio, mitad inferior en azul plano. Co-branding de partner tal como Movistar lo publica | — |
| `references/gold-standards/movistarplus/movistarplus-mockup-ui-mux-disney.jpg` | Movistar+ | Emplazamiento del banner en la UI real de TV (4K) | MIXTO | Cómo vive la campaña dentro del MUX: posición en el carousel, dots, menú, fila Tendencias con los botones de las plataformas partner. Referencia de contexto y escala del formato MUX | Es emplazamiento, no pieza plana: úsala para entender dónde cae el banner, o como referencia de mockup contextual |
| `references/gold-standards/movistarplus/movistarplus-mockup-ui-mux-ficcion.jpg` | Movistar+ | Emplazamiento en UI, segunda campaña | MIXTO | El par del anterior con otra campaña: juntos enseñan qué zona del MUX ocupa el mensaje y qué zona es UI fija | Ídem: contexto, no pieza plana |
| `references/gold-standards/movistarplus/movistarplus-hero-negro-safe-area-izq.jpg` | Movistar+ | Hero 16:9 para UI de Movistar+ | MIXTO | Hero de contenido: degradado lateral izquierdo para alojar el texto, safe area en el tercio izquierdo, titular blanco con la palabra clave en marcador amarillo | `res-baja` (596 px), dos piezas pegadas en el archivo. Para hero de contenido puro; para campaña usar las de agosto 2026 |
| `references/gold-standards/marca/marca-m-expresiva-escala-humana.jpg` | Transversal | Expresión de marca, mural fotografiado 16:9 | **FOTO** | La M como territorio gráfico expresivo: degradado turquesa a azul marino, contorno negro, rayos naranja detrás. Texturas y colores fuera de paleta admitidos SOLO dentro del símbolo. Y la regla de escala humana: la M ocupa ~60% del encuadre y la persona aparece pequeña, descentrada, de perfil | No tiene tipografía ni precio: no sirve como referencia de piezas con texto |

---

## Qué referencias pasar según lo que estés generando

La regla es **2-3 referencias, nunca más**. Más diluyen la señal y encarecen la llamada.
Se elige por combinación de canal + modo, no solo por canal.

**El orden importa.** La primera referencia de la lista conserva el detalle más fino y la
textura más rica; las siguientes influyen menos. En la tabla, la primera columna de
referencias es la dominante: es la que más se parece a lo que quieres conseguir. Si en la
pieza hay caras, la de las caras va primera. El `--dry-run` marca cuál es la dominante.

**Recalibración del código Movistar+ (agosto 2026).** Con las piezas reales del cliente se
corrigió lo que teníamos escrito: las campañas de M+ van sobre **azul Movistar con pastilla
blanca y keyword en azul**, no sobre negro con marcador amarillo. El modo oscuro existe pero
lo pone el key art, no un fondo negro plano. Regla operativa: referencias de M+ solo se
combinan entre sí, nunca con las de otros canales.

**Sobre las marcas de partner en las referencias.** Muchas piezas de M+ y de tienda llevan
key art y logos de terceros (Disney+, HBO Max, Samsung, Apple...). **Es normal y correcto:
son partners de Movistar y las piezas son oficiales y aprobadas.** Estas referencias se pasan
completas. La única regla operativa es de contenido, no de legalidad: el key art de la
referencia es de SU campaña. Si la pieza nueva promociona otros títulos u otros dispositivos,
el prompt debe describir el contenido de la pieza nueva para que el modelo no arrastre el de
la referencia. Y si la pieza nueva no lleva partner (campaña 100% Movistar), añade la
exclusión de logos ajenos al prompt.

| Lo que generas | Pasa estas | Por qué esas |
| --- | --- | --- |
| Foto de escena para MUPI / cartel exterior | `references/gold-standards/exterior/exterior-mupi-foto-sangre.jpg` + `references/gold-standards/exterior/exterior-cartel-marco-color-notch.jpg` | Las dos únicas donde la foto manda y hay gente real con luz natural |
| Cartel exterior sin foto (tipográfico) | `references/gold-standards/exterior/exterior-cartel-tipografico-paleta.jpg` + `references/gold-standards/exterior/exterior-mupi-producto-sobre-azul.jpg` | Paleta extendida y color plano; la segunda aporta el degradado radial azul |
| Hero de email | `references/gold-standards/email/email-multiproducto-3-cards.jpg` + `references/gold-standards/digital/digital-landing-precio-sobre-foto.jpg` | Collage de hero y tratamiento de precio sobre foto |
| Email de oferta con precio protagonista | `references/gold-standards/email/email-oferta-grafico-price-card.jpg` + `references/gold-standards/email/email-oferta-comparativa-precio.jpg` | Las dos jerarquías de precio del sistema: sobria y agresiva |
| Display vertical / pieza de app | `references/gold-standards/digital/digital-vertical-titular-xl-foto-documental.jpg` + `references/gold-standards/digital/digital-landing-ventaja-personal-grid.jpg` | Titular XL sobre azul hielo y grid de celdas |
| PLV de dispositivo con precio (pantalla 16:9) | `references/gold-standards/tienda/tienda-plv-producto-precio-samsung.jpg` + `references/gold-standards/tienda/tienda-plv-producto-precio-iphone.jpg` | Mismo patrón con dos campañas: el modelo abstrae la plantilla, no copia la pieza |
| PLV tótem vertical (1080x1920) | `references/gold-standards/tienda/tienda-plv-producto-precio-vertical-samsung.jpg` + `references/gold-standards/tienda/tienda-plv-producto-precio-samsung.jpg` | La vertical primero (dominante) y su gemela horizontal para reforzar el sistema |
| PLV multiproducto / ventaja de cliente | `references/gold-standards/tienda/tienda-plv-multiproducto-verano.jpg` + `references/gold-standards/tienda/tienda-plv-etiqueta-sin-ip.jpg` | Plantilla de 3 productos + la única referencia sin IP ajena |
| Pieza de tienda sin marcas de terceros | `references/gold-standards/tienda/tienda-plv-etiqueta-sin-ip.jpg` + `references/gold-standards/exterior/exterior-cartel-tipografico-paleta.jpg` | Las dos referencias limpias de IP: para piezas donde no puede aparecer ningún logo ajeno |
| Chevalet impreso de oferta | `references/gold-standards/tienda/tienda-chevalet-3-cajas.jpg` + `references/gold-standards/tienda/tienda-plv-producto-precio-samsung.jpg` | Apilado de cajas del impreso + jerarquía de precio actual |
| Videocartela Movistar+ | `references/gold-standards/movistarplus/movistarplus-videocartela-completa-qr.jpg` + `references/gold-standards/movistarplus/movistarplus-videocartela-cobranding-disney.jpg` | Las dos gemelas: estructura constante, campaña variable. Solo referencias M+, nunca mezclar con otros canales |
| WOW banner Movistar+ | `references/gold-standards/movistarplus/movistarplus-wow-banner-ficcion.jpg` + `references/gold-standards/movistarplus/movistarplus-wow-banner-disney.jpg` | El par del formato WOW: misma retícula, dos campañas |
| Banner web Movistar+ | `references/gold-standards/movistarplus/movistarplus-web-banner-ficcion.jpg` + `references/gold-standards/movistarplus/movistarplus-wow-banner-ficcion.jpg` | Formato web + su hermano WOW de la misma campaña |
| Campaña M+ en modo oscuro / precio con tachado | `references/gold-standards/movistarplus/movistarplus-ui-campana-oscura-precio-tachado.jpg` **sola** | Único ejemplo del modo oscuro y del tachado. Mezclarla con las azules confunde el código |
| Pieza smartphone M+ (vertical) | `references/gold-standards/movistarplus/movistarplus-smartphone-compuesto-disney.jpg` + `references/gold-standards/movistarplus/movistarplus-videocartela-completa-qr.jpg` | Única muestra del formato smartphone + la videocartela para reforzar el sistema |
| PLV de contenidos / entretenimiento en tienda | `references/gold-standards/tienda/tienda-plv-mosaico-ficcion-disney.jpg` + `references/gold-standards/tienda/tienda-plv-poster-destacado-ficcion.jpg` | Las dos composiciones del loop de contenidos: mosaico y carátula destacada |
| PLV de contenidos en tótem vertical | `references/gold-standards/tienda/tienda-plv-mosaico-ficcion-disney-vertical.jpg` + `references/gold-standards/tienda/tienda-plv-mosaico-ficcion-disney.jpg` | La vertical dominante y su gemela horizontal |
| Mockup de emplazamiento en la UI de M+ | `references/gold-standards/movistarplus/movistarplus-mockup-ui-mux-disney.jpg` + `references/gold-standards/movistarplus/movistarplus-mockup-ui-mux-ficcion.jpg` | Para componer mockups contextuales del MUX o entender la zona útil del formato |
| Secuencia perimetral de tienda | `references/gold-standards/tienda/tienda-perimetral-mockup-6-pantallas.jpg` + una PLV 16:9 del contenido que toque | La mecánica del canal (6 pantallas, bumper/contenido) + la plantilla de la pantalla individual |
| Mockup de entorno retail | `references/gold-standards/tienda/tienda-entorno-muro-verbos.jpg` | Luz e iluminación reales de tienda |
| Foto de estilo de vida sin formato definido | `references/gold-standards/exterior/exterior-cartel-marco-color-notch.jpg` + `references/gold-standards/digital/digital-vertical-titular-xl-foto-documental.jpg` | Las dos con fotografía documental de verdad, no stock |

---

## Comando

Las rutas son **relativas a `movistar-visual-production/`**. Ejecuta el script desde ahí.

```bash
python3 scripts/generate_image.py \
  -p "<prompt de 4-5 frases segun guidelines/magic-prompt.md>" \
  -o outputs/<slug>-<zona>.png \
  --aspect 2:3 \
  --ref references/gold-standards/exterior/exterior-mupi-foto-sangre.jpg \
  --ref references/gold-standards/exterior/exterior-cartel-marco-color-notch.jpg
```

Antes de gastar crédito, comprueba que coge las referencias:

```bash
python3 scripts/generate_image.py -p "test" -o /tmp/t.png --aspect 2:3 \
  --ref references/gold-standards/exterior/exterior-mupi-foto-sangre.jpg \
  --ref references/gold-standards/exterior/exterior-cartel-marco-color-notch.jpg \
  --dry-run
```

Con `--ref` el script cambia de endpoint: usa `/v1/images/edits` con `multipart/form-data`
en vez de `/v1/images/generations` con JSON. El `--dry-run` te lo dice explícitamente.
Si dice `endpoint: .../generations` y `refs: 0`, las referencias **no** se están pasando.

---

## Huecos declarados

Esto es lo que **no** se puede referenciar hoy. Es la dependencia nº1 de la calidad visual
y está pedido a Movistar en `PETICION-REFERENCIAS-MOVISTAR.md`.

| Canal / formato | Estado | Qué falta exactamente |
| --- | --- | --- |
| **Exterior — lona gran formato** | Sin gold standard | La única que hay (`pieces/lona.png`) es un render con perspectiva y lleva dos defectos de marca dentro de la creatividad |
| **Digital — display servido limpio** | Sin gold standard | Las tres que hay son capturas de navegador con AdChoices y cromo de la web anfitriona. Habría que recortar el marco |
| ~~Movistar+~~ | **Cerrado agosto 2026** | 6 piezas nuevas: 2 videocartelas, 2 WOW, 1 web, 1 UI oscura. Todas con key art licenciado: sirven de estructura, el contenido se excluye en el prompt |
| ~~Tienda — PLV pantalla digital~~ | **Cerrado agosto 2026** | 7 piezas nuevas a 1920x1080: producto+precio (h y v), multiproducto, etiqueta, sin-IP, store page. El chevalet IMPRESO sigue solo a 442 px |
| **Tienda — caballete impreso a resolución** | Parcial | El chevalet sigue a 442 px. Las nuevas PLV son de pantalla digital, no de impreso |
| **BTL, TMKS, D2D, SMS, push** | Sin gold standard | Cero piezas de referencia en el repo. Estos canales generan a ciegas |
| **Piezas sin partner** | Escaso | Para campañas 100% Movistar (sin co-branding) solo hay 2 referencias sin ningún logo ajeno: `tienda-plv-etiqueta-sin-ip` y `exterior-cartel-tipografico-paleta`. Para el resto de casos el co-branding de las referencias es correcto: es como Movistar publica con sus partners |
| **App miMovistar** | Descartado | Los tres archivos son screenshots de 360x270 y 897x1600 con UI de producto, no creatividades |
| **Fotografía de banco aprobado** | Sin acceso | Con banco de imágenes aprobado, la mitad de estas generaciones dejarían de ser necesarias, y con ellas el riesgo de reproducir marcas de terceros |

### Lo que hay que pedir para cerrar cada hueco

Por cada formato: **10-15 piezas finales aprobadas, en el archivo original plano**
(no mockup, no captura, no render con perspectiva), a **≥1500 px de lado largo**, y a ser
posible una variante con foto y una sin foto del mismo formato. Sin esto, la mitad de la
tabla de arriba seguirá diciendo `res-baja`.

---

## Cómo añadir una pieza nueva

1. Que cumpla los cuatro criterios de admisión de arriba.
2. Normalizar: JPEG q90, lado largo máximo 1536 px.
3. Nombrar `<canal>-<modo o rasgo>-<descriptor>.jpg`, en minúsculas y sin acentos.
   El nombre tiene que decir para qué sirve: quien la elige lo hace leyendo el nombre.
4. Añadir su fila al catálogo, con la columna **Qué demuestra** escrita de forma operativa.
   Nada de "buena composición": tiene que servir para decidir si esa referencia sirve
   para la pieza que se está haciendo ahora.
5. Si la pieza tapa un hueco, quitar su fila de la tabla de huecos.
