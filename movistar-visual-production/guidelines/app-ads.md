# Aplicación: Publicidad (Display digital + OOH)

Version enriquecida con patrones reales de 23 piezas display de campaña (Ray-Ban Meta, Dispositivos, FTTR, Residencia/segunda vivienda, MovistarSwap) en 5 formatos IAB + 8 piezas OOH (MUPI, lona, carteles, exterior, wild-posting) + 4 piezas tienda (caballete, counter display, pantalla digital, flagship).

---

## PARTE 1: DISPLAY DIGITAL

### Formatos display (IAB estandar)

| Formato | Dimensiones | Uso tipico | CTA pill | Notas |
|---------|-------------|-----------|----------|-------|
| Medium Rectangle (MPU) | 300x250 | Sidebar, inline. El formato que MAIA produce como representativo | Si (cuando hay espacio) | Formato principal de MAIA |
| Half Page | 300x600 | Impacto alto, vertical extendido | Si, siempre | Más espacio para copy + precio + CTA |
| Mobile Banner | 320x100 | Móvil pie de página / interstitial | No (demasiado comprimido) | Solo titular + claim + M logo |
| Leaderboard | 728x90 | Banner horizontal cabecera | Si / outline | CTA pill o outline según campaña |
| Billboard | 980x250 | Top de home portales | Si, siempre | Composición horizontal split |

Otros formatos menos frecuentes: 160x600 (Wide Skyscraper), 320x50 (Mobile mini), 320x480 (Mobile Interstitial). MAIA produce el **300x250** como pieza representativa del canal.

---

### Anatomia de un banner display

Todos los formatos comparten estos elementos, distribuidos según el espacio disponible:

1. **M logo**: siempre presente, siempre legible. Azul sobre fondo claro, blanco sobre fondo azul/oscuro.
2. **Titular**: ExtraBold o Bold, sentence case, 1-3 líneas según formato.
3. **Imagen**: foto lifestyle o producto en cutout. Puede ocupar una zona o el fondo completo.
4. **Precio** (si aplica): XXL en formatos grandes, compacto en horizontales. Numero + "eur/mes" + condición.
5. **Claim**: "Ser cliente tiene ventajas", "Sin permanencia", o similar.
6. **CTA pill** (si cabe): azul filled por defecto, outline en formatos horizontales sobre fondo claro.
7. **Legal**: discreto al pie, solo en piezas con precio/condición.
8. **Indicador play** (triangulo): esquina superior derecha, indica pieza animada.

---

### Fondos por tipo de campaña

La regla "fondo siempre #FFFAF5" aplica a campañas de producto/hogar pero NO es universal. Las piezas reales usan fondos distintos según la campaña:

| Campaña | Fondo dominante | Logica |
|---------|----------------|--------|
| Residencia / hogar / fibra | `#FFFAF5` (beige Movistar) | Canal offline, producto domestico, tono calido |
| FTTR (tech hogar) | `#FFFAF5` + zona dark (negro/navy) | Frame awareness en beige, frame oferta en dark con mascota 3D |
| Dispositivos / co-branding tech | Verde mint claro (~`#C8E6C9`) | Diferenciación visual, asociación a "descuento exclusivo" |
| Swap (renovación móviles) | Azul solido `#0066FF` | Premium, dinamismo. Texto blanco. CTA en zona beige inferior |
| Value-add / contenido | Azul solido `#0066FF` | Alineado con identidad digital de contenido |

**Regla general**: el color de fondo NO se elige libremente. Se hereda de la sub-corriente y el tipo de campaña. Ver tabla arriba como guia.

---

### Layouts por formato

#### 300x250 (MPU) -- pieza representativa MAIA

Estructura vertical compacta. El formato más versátil y el que MAIA produce.

**Layout A: Producto/hogar (fondo claro)**
```
┌──────────────────────┐
│  Titular azul Bold   │  M logo top-right
│  2 líneas            │
├──────────────────────┤
│  [Foto lifestyle     │
│   o producto]        │
├──────────────────────┤
│  Desde 15eur/mes     │  Precio XXL
│  Sin permanencia     │
│  Ser cliente         │
│  tiene ventajas      │
└──────────────────────┘
```

**Layout B: Tech/dispositivos (fondo azul o dark)**
```
┌──────────────────────┐
│  [Zona azul/dark]    │  M logo blanco
│  Titular blanco      │
│  ExtraBold           │
│  [Productos cutout]  │
├──────────────────────┤
│  [Zona beige]        │
│  Logo partner        │
│  M logo azul         │
└──────────────────────┘
```

**Layout C: Co-branding (fondo tematico)**
```
┌──────────────────────┐
│  [Etiqueta colgante] │  Elemento visual
│  Foto / producto     │  con co-brand
│  Ray-Ban | Meta      │
├──────────────────────┤
│  Ser cliente         │
│  tiene ventajas      │  M logo bottom-right
└──────────────────────┘
```

#### 300x600 (Half Page)

Version extendida del 300x250. Misma estructura pero con más espacio para cada zona.

- Titular: 3-4 líneas, ExtraBold 24-28px.
- Imagen: puede ser grande (40-50% del alto).
- Precio: zona dedicada con overline ("Por solo", "Desde") + número XXL + condición.
- "Ser cliente tiene ventajas": debajo del precio.
- **CTA pill siempre presente** en este formato. Azul filled, 60-80% del ancho, centrado.
- M logo: bottom-right.
- En campañas bicolor: zona superior clara + zona inferior dark/azul con precio.
- Puede incluir opciones alternativas (ej. FTTR: "O un pago único de 535eur").

Textos CTA observados: "Descubre tu precio", "Contratalo ya", "Lo quiero", "Suscribete ya".

#### 320x100 (Mobile Banner)

Formato ultra-comprimido. **Sin CTA pill** (no cabe).

```
┌──────────────────────────────────────────────┐
│  Titular (2 líneas)  |  [Producto]  | M logo │
└──────────────────────────────────────────────┘
```

- Solo titular + claim + M logo. A veces producto/imagen intermedio.
- Sin precio (o precio compacto en línea).
- Sin CTA pill. El clic es el banner entero.
- M logo: derecha, azul o blanco según fondo.
- Fondo: beige, verde mint, azul o foto con overlay según campaña.

#### 728x90 (Leaderboard)

Horizontal ancho. Estructura en 3 zonas:

```
┌──────────────────────────────────────────────────────────────┐
│  [Imagen/prod]  │  Titular + claim  │  Precio + CTA + M     │
└──────────────────────────────────────────────────────────────┘
```

- Imagen o productos a la izquierda (si caben).
- Titular + claim en centro.
- Precio + CTA + M logo a la derecha.
- CTA: pill azul filled o **outline** (borde azul, fondo transparente) según campaña.
- En campañas con fondo azul (Swap): toda la zona principal es azul con texto blanco, CTA en zona beige derecha.

#### 980x250 (Billboard)

El formato más ancho. **CTA pill siempre presente.**

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Foto/productos]   │   Titular + claim   │  Precio + CTA  │  M logo │
└────────────────────────────────────────────────────────────────────────┘
```

- Composición horizontal tipo 728x90 pero con más espacio.
- Foto lifestyle o fila de productos a la izquierda (hasta 40% del ancho).
- Titular + "Ser cliente tiene ventajas" en centro.
- Precio + CTA pill a la derecha.
- M logo: extreme derecha.
- CTA: pill azul filled o outline.

---

### Animación (frames)

Las piezas display son **animadas** con varios frames, aunque MAIA produce HTML estatico (el primer frame / frame de cierre). La estructura de animación tipica observada en las capturas:

| Frame | Contenido | Duración tipica |
|-------|-----------|-----------------|
| 1 (awareness) | Titular + imagen/producto. Sin precio, sin CTA. | 2-3s |
| 2 (oferta) | Precio XXL + condiciones + CTA. Puede cambiar fondo (ej. beige -> dark). | 3-4s |
| 3 (cierre) | M logo prominente + claim de cierre + CTA. Se mantiene hasta clic. | indefinido |

**Lo que MAIA produce**: el frame de cierre (frame 3 o frame completo con todos los elementos). Es el frame más rico y el que el usuario verá si no interactúa con la animación. MAIA no produce la animación entre frames; eso lo gestiona producción.

**Reglas de animación** (para referencia, aunque MAIA no las implementa):
- Máximo 3 frames.
- Transiciones: fade-in simple o slide. Sin rotaciones, sin efectos 3D.
- Sin loops infinitos. La animación se ejecuta una vez y se detiene en el frame final.
- Duración total: 8-10 segundos máximo.

---

### CTA en Display

#### Presencia de CTA por formato

| Formato | CTA pill | Tipo | Texto tipico |
|---------|----------|------|-------------|
| 300x250 | Si (en frame de cierre) | Filled o ausente según frame | "Contratalo ya", "Descubre tu precio" |
| 300x600 | Si, siempre | Filled | "Lo quiero", "Suscribete ya", "Contratalo ya" |
| 320x100 | No | -- | El banner entero es clicable |
| 728x90 | Si | Filled u outline | "Lo quiero", "Suscribete ya", "Descubre tu precio" |
| 980x250 | Si | Filled u outline | Mismos que 728x90 |

#### Estilo CTA

- **Pill azul filled** `#0066FF` + texto blanco: estandar en formatos verticales (300x250, 300x600).
- **Pill outline** azul (borde `#0066FF`, fondo transparente, texto azul): usado en formatos horizontales (728x90, 980x250) cuando el fondo es claro y se necesita menos peso visual.
- **Pill sobre fondo azul**: el CTA se coloca en una zona beige/blanca separada. Pill outline con borde gris/azul y texto negro. Nunca pill azul sobre fondo azul.

#### Patrones de texto CTA observados

- **Imperativo**: "Contratalo ya", "Suscribete ya"
- **Primera persona**: "Lo quiero"
- **Exploración**: "Descubre tu precio"

Sentence case siempre. Sin exclamación.

---

### Elementos visuales recurrentes

#### "Ser cliente tiene ventajas"

Texto plano (no badge pill como en email). "tiene ventajas" en **bold** o **italica**. Aparece debajo del precio en formatos que lo permiten (300x250, 300x600, 728x90, 980x250). Ausente en 320x100.

#### Etiqueta "Descuento exclusivo Clientes en tecnologia"

Elemento gráfico con forma de etiqueta de precio colgante (con cuerda azul). Usado en campañas de dispositivos y co-branding tech. Contiene texto en tipografía manuscrita/informal. Siempre acompañado de "Ser cliente tiene ventajas".

#### Precio

- **XXL**: ExtraBold 48-72px en formatos verticales (300x250, 300x600).
- **Compacto**: Bold 24-36px en formatos horizontales (728x90).
- **Overline**: "Desde", "Por solo", "Ahora por" en azul, 12-14px.
- **Unidad**: "eur/mes" en tamaño menor (~18px).
- **Precio anterior tachado**: cuando hay descuento.
- **Condición**: "Sin permanencia", "Durante 48 meses" debajo del precio.
- **Alternativa**: "O un pago único de X eur" cuando aplica (FTTR).

#### M logo

| Fondo | Color | Posición | Tamano mínimo |
|-------|-------|----------|---------------|
| Claro (#FFFAF5, verde, salmon) | Azul `#0066FF` | Top-right o bottom-right | 40px en 300x250, 20px en 728x90 |
| Azul `#0066FF` | Blanco | Top-right o bottom-right (zona beige) | Mismos minimos |
| Dark (negro/navy) | Azul o blanco | Bottom-right | 40px |

En formatos muy pequenos (320x100, 728x90), logo M sin wordmark. Solo el símbolo.

#### Fotografía y producto

- **Fotos lifestyle**: familias, parejas, casas de verano. Contexto domestico, iluminación natural.
- **Productos en cutout**: sobre fondo limpio. Ángulo 3/4 para móviles. Fila horizontal para catálogo multi-producto (tablet + móvil + consola).
- **Mascota/personaje 3D**: raton animado en campaña FTTR. Sobre fondo dark.
- **iPhones en abanico**: composición dinámica para Swap (5-6 modelos en perspectiva).
- **Etiqueta energetica**: badge pequeno junto a productos electronicos.

#### Co-branding

- **Logo partner**: en posición secundaria (Ray-Ban | Meta, Apple iPhone). Nunca domina la pieza.
- **Colores partner**: limitados a la zona del partner o su logo. No invaden la pieza.
- **Apple branding**: logo Apple + nombre de producto ("iPhone 17") + claim ("Disenado para Apple Intelligence.") en zona dedicada.

---

### Sistema 1/16 para banners

X = lado corto / 16.

| Formato | X | Margen | Logo M mínimo |
|---------|---|--------|---------------|
| 300x250 | ~16px | 15px | 40px |
| 300x600 | ~19px | 24px | 56-60px |
| 320x100 | ~6px | 12px | 20-24px |
| 728x90 | ~6px | 12px | 20-24px |
| 980x250 | ~16px | 20px | 40-48px |

En formatos con lado corto < 100px, la legibilidad manda. Logo M mínimo 20px aunque el 3X salga menor.

---

### Composición por tipo de campaña

| Tipo | Fondo | Imagen | Elementos clave |
|------|-------|--------|-----------------|
| **Hogar/fibra** (residencia, 2a vivienda) | `#FFFAF5` | Foto lifestyle (casa, terraza, mar) | Titular azul + precio XXL + "Ser cliente tiene ventajas" + CTA "Lo quiero" |
| **Tech hogar** (FTTR) | `#FFFAF5` + dark | Mascota 3D + icono casa | Titular azul + "Anadelo a miMovistar" + precio + alternativa pago único + CTA "Contratalo ya" |
| **Dispositivos** (catálogo clientes) | Verde mint | Fila de productos cutout + etiqueta colgante | "Descuento exclusivo Clientes" + "Ser cliente tiene ventajas" + CTA "Descubre tu precio" |
| **Co-branding tech** (Ray-Ban Meta) | Foto playa / color suave | Producto co-brand en cutout | Etiqueta colgante + logos partner + "Ser cliente tiene ventajas" + CTA "Descubre tu precio" |
| **Swap** (renovación móviles) | Azul solido `#0066FF` | iPhones en abanico | Titular blanco + Apple branding + CTA "Suscribete ya" en zona beige |

---

### Reglas de copy en display

- **Titular**: máximo 40 caracteres en 300x250, 60 en 300x600 / 980x250.
- **Una idea, una acción.** Sin multiples mensajes en un mismo banner.
- **Sentence case** siempre.
- **Sin em dashes** en todo el copy.
- **Precio siempre visible** si es el argumento principal. eur después del número, "/mes" en subindice.
- **Legal**: al pie, 10-12px, gris muted. Solo en piezas con precio/condición. Máximo 2 líneas en display (más espacio en OOH).

---

### Checklist display antes de entregar

- [ ] Formato correcto (300x250 como pieza representativa)
- [ ] M logo presente y legible (color correcto según fondo)
- [ ] Titular ExtraBold/Bold, sentence case, máximo caracteres respetado
- [ ] Fotografía real o producto real, no stock genérico ni IA visible
- [ ] Precio XXL si la campaña lo requiere
- [ ] CTA pill presente en formatos que lo permiten (no en 320x100)
- [ ] CTA con texto accionable y específico (no "clic aquí")
- [ ] Fondo coherente con el tipo de campaña (ver tabla de fondos)
- [ ] "Ser cliente tiene ventajas" si aplica
- [ ] Contraste AA en todo texto
- [ ] Sin em dashes en el copy
- [ ] Legal al pie si hay precio/condición

---

## PARTE 2: OOH (EXTERIOR + TIENDA)

Version enriquecida con patrones de 8 piezas OOH reales (MUPI, lona, carteles, exterior, wild-posting) y 4 piezas de tienda (caballete, counter display, pantalla digital, flagship).

### Formatos OOH fisico

| Formato | Dimensiones orientativas | Patron visual |
|---------|-------------------------|---------------|
| MUPI (marquesina / bus stop) | 1190x1750mm (ratio 2:3) | Vertical, patron "MUPI" abajo |
| Lona (building wrap) | 8000x3000mm o mayor | Horizontal ancho, patron "lona" abajo |
| Valla 4x3 | 4000x3000mm | Horizontal, patron "valla" abajo |
| Exterior (poster gran formato) | Variable, tip. A0 o mayor | Vertical/cuadrado, patron "exterior" abajo |
| Cartel wild-posting | A3/A2 en serie | Vertical, patron "carteles" abajo |
| Metro (backlit) | Variable, tip. 1200x1800mm | Ver patron MUPI |
| Caballete tienda (chevalet) | 70x100cm | Vertical, patron "tienda/POS" abajo |
| Counter display (metacrilato) | A4/A5 | Adaptación compacta del caballete |
| Pantalla digital tienda | 1080x1920px (totem 55") | Vertical 9:16, patron "pantalla digital" abajo |

**Regla 1/16 en gran formato:** M = 6X (no 3X) en valla y lona. Margen amplificado 6X también.

---

### Patron MUPI vertical

Dos variantes principales observadas en piezas reales:

**A. MUPI producto (fondo solido)**
Fondo pleno azul `#0066FF` (Swap) o blanco (brand). Producto en cutout como hero central. Titular + claim arriba o al centro-izquierda. M logo bottom-right.

```
┌─────────────────┐
│   Titular       │  Movistar Sans Bold 60-72pt, sentence case,
│   sensación de  │  blanco o azul, 2-3 líneas, top-left,
│   vivir estre-  │  ocupa 20-25% del alto
│   nando.        │
│                 │
│     [Producto   │  hero: mano+dispositivo o escena
│      / gesto]   │  ocupa 50-60% del alto central
│                 │
│  Suscribete     │  nombre de oferta Bold 24pt
│  a Swap    [M]  │  M expresiva blanca BOTTOM-RIGHT
│  Estrena un iPhone
│  17 y renuevalo cada 2 anos.
└─────────────────┘
```

**B. MUPI lifestyle (foto dominante)**
Foto de persona/escena ocupa casi todo el fondo. Titular ExtraBold superpuesto. Nombre de marca/producto ("Swap") en ExtraBold grande como ancla visual. Tagline al pie ("Estrena. Disfruta. Renueva. Repite."). M logo blanco bottom-right.

**Reglas MUPI:**
- Fondo: azul solido `#0066FF`, blanco `#FFFAF5`, o foto a sangre. Nunca gradiente.
- M expresiva bottom-right, tamaño ~10-12% del ancho. Blanco sobre azul/foto, azul sobre blanco.
- Sin CTA pill. Sin precio (o precio muy compacto). El MUPI es awareness, no respuesta directa.
- Legal 8-10pt al pie, discreto pero legible a 2m.

---

### Patron lona (building wrap)

Gran formato horizontal para fachadas de edificios. Dos variantes observadas:

**A. Lona de producto (fondo azul)**
Fondo azul `#0066FF`. Titular blanco ExtraBold muy grande. Producto hero (mano + dispositivo). Mismo visual que MUPI producto pero a escala monumental. M logo blanco bottom-right.

Ejemplo real: "Suscribete a MovistarSwap / Estrena un iPhone 17 y renuevalo cada 2 anos."

**B. Lona de marca/trust (fondo blanco)**
Fondo blanco/claro. Titular azul ExtraBold XXL con recurso tipografico (comillas, signos). Body copy en gris con dato concreto. Claim emocional al pie. M logo azul centrado-bottom.

Ejemplo real: 'Vuelve a contestar "¿Si?" / 190 millones de llamadas fraudulentas bloqueadas a nuestros clientes. Seguimos. / La red más segura.'

**Reglas lona:**
- Layout horizontal, titular a la izquierda o centrado.
- Hero image derecha (a veces bleed hasta borde). En lonas de marca, el texto ES el hero.
- M expresiva: gran tamaño 8-10% del ancho. Puede ir centrada-bottom en lonas de marca.
- Sin CTA pill. Sin precio (salvo excepciones con oferta principal).
- El texto debe leerse a 20-50 metros. Tamanos de tipo enormes.

---

### Patron exterior (poster gran formato)

Poster vertical o cuadrado en fachadas o escaparates. Usado para campañas de portafolio/valor con grid de servicios.

```
┌─────────────────────┐
│  Titular ExtraBold   │  "¿Quieres saber lo que
│  pregunta/invita     │   podemos hacer por ti?"
│                 [M]  │  M azul top-right
│                      │
│  ┌────┐  ┌────┐     │  Grid 2x2 de lifestyle photos
│  │Seg.│  │Entr│     │  con label de categoria
│  │    │  │    │     │  (Seguridad, Entretenimiento,
│  └────┘  └────┘     │   Seguros, Energia solar)
│  ┌────┐  ┌────┐     │
│  │Seg.│  │Sol.│     │  Logos de partners debajo
│  │    │  │    │     │  de cada foto
│  └────┘  └────┘     │
└─────────────────────┘
```

**Reglas exterior portafolio:**
- Fondo blanco/claro.
- Titular de invitación (pregunta abierta), no de oferta concreta.
- Grid de imagenes con categories. Cada categoria con logos de partners debajo.
- Sin precio, sin CTA pill. Es awareness de ecosistema.

---

### Patron producto-tipografía (escaparate/store window)

Piezas para escaparate de tienda donde el producto en cutout se superpone e interactúa con la tipografía. Cada pieza del par tiene un fondo distinto:

```
┌─────────────────┐     ┌─────────────────┐
│      [M] azul   │     │                 │
│                 │     │  Habla    [M]   │  M blanco bottom-right
│ Una             │     │  Siente         │
│ conexión   [iPh]│     │  Inspira  [AirP]│  producto overlapping texto
│ para       [one]│     │  Crea     [od]  │
│ ti.             │     │                 │
│                 │     │  Tus nuevos     │
│ Tu nuevo iPhone │     │  AirPods con    │
│ con Movistar    │     │  Movistar       │
└─────────────────┘     └─────────────────┘
  Fondo blanco            Fondo azul #0066FF
```

**Reglas producto-tipografía:**
- Tipografia ExtraBold MUY grande, apilada verticalmente (1 palabra por línea).
- El producto en cutout se superpone parcialmente al texto (composición integrada).
- Claim al pie: "Tu nuevo [producto] con Movistar".
- Piezas en pares contrastados: una fondo blanco + una fondo azul.
- Sin precio, sin CTA. Pura aspiración de producto.

---

### Patron wild-posting / serie Carteles

Serie de piezas pegadas en secuencia sobre un muro. Cada pieza usa un secundario distinto (uno azul filled + varios secundarios claros). Dos familias de overline observadas:

**Familia A: "Ser de Movistar es..."**
Overline "Ser de Movistar es" + titulares cotidianos y emocionales ("Hablar con tus amigos jugando en la Play.", "Llamar a tu abuela que está en el pueblo con los tíos.").

**Familia B: "Por..."**
Overline "Por..." + titulares aspiracionales con foto lifestyle dominante ("Por una escapada al monte / Los mejores planes", "Por la yaya 2.0 / Tecnologia accesible para todos").

```
┌─────────────┐
│      [M]    │  M azul top-right sobre fondo secundario
│             │
│ Ser de      │  overline Regular 14pt
│ Movistar es │
│             │
│ Hablar      │  titular Bold 96-120pt en color secundario OSCURO
│ con tus     │  que empareja con el fondo (verde-oscuro sobre verde-claro,
│ amigos      │  azul-oscuro sobre azul-claro, etc.)
│ jugando     │
│ en la Play. │  termina con punto final como recurso gráfico
└─────────────┘
```

**Reglas de serie:**
- Cada pieza: 1 secundario de fondo + su pareja oscura para tipografía.
- Colores observados: azul/blanco, blanco/negro, verde mint/verde oscuro, amarillo/marrón, salmon/marron.
- Todas las piezas de la serie comparten estructura (overline + titular + M).
- No hay CTA, no hay precio, no hay producto. Pura declaración de marca.
- La primera pieza siempre en azul Movistar filled con tipo en blanco (ancla la serie).
- Familia B puede incluir foto lifestyle como fondo (la foto domina, el texto se superpone).

---

### Patron cartel tienda / POS (caballete)

Formato chevalet interior (70x100cm). Cartel A2/A1 sobre soporte tipo A.

```
┌─────────────────────┐
│       [M]           │  lockup horizontal centrado top
│   Movistar          │
│                     │
│ Ser cliente         │  titular apilado 3 líneas
│ tiene               │
│ Ventajas.           │  ultima línea AZUL con PUNTO final
│                     │
│   [productos]       │  lifestyle: iPhone + AirPods + Watch
│                     │
│  [placa AMARILLA]   │  precio/descuento en amarillo con borde suave
│  Hasta 300eur       │
│  de descuento       │
│                     │
│  [banda azul-osc]   │  co-branding con partners
│  repsol logo | 200eur extra
│                     │
│  Pregunta por tu    │  CTA suave con icono chat
│  ventaja personal.  │
└─────────────────────┘
```

**Reglas tienda caballete:**
- Fondo Blanco Movistar `#FFFAF5`.
- Placa amarilla `#FFE99C` para descuentos monetarios.
- Ultima línea del titular siempre en azul, con punto final si el titular busca énfasis dramatico.
- Partners co-branded en banda azul-oscuro estrecha abajo.
- Adaptaciones: counter display (metacrilato A4/A5 para mostrador) y folleto impreso usan el mismo diseño a menor escala, con iconos de servicio adicionales en la parte inferior.

---

### Patron pantalla digital tienda

Totem vertical 55" en escaparate o entrada de tienda. Ratio 9:16 (1080x1920px), mismo que stories.

Dos modos observados:

**A. Bienvenida/marca:** fondo azul `#0066FF`, M logo blanco centrado, "¡Bienvenidos!" debajo. Sin oferta, sin CTA.

**B. Oferta/tarifa:** fondo oscuro/navy con glow azul. Titular de producto + precio XXL + claim. Puede incluir iconos del servicio. Estetica digital (bordes luminosos, gradientes sutiles).

Ejemplo real: "Nueva Tarifa ILIMITADA / Solo 5eur/mes / Datos, llamadas y SMS" con icono de infinito.

**Reglas pantalla digital:**
- Orientación vertical obligatoria (9:16).
- Tipografia MUY grande (legible a 3-5 metros desde la calle).
- Puede usar fondo azul solido o fondo oscuro con acentos luminosos (a diferencia del caballete que es siempre blanco).
- M logo siempre visible, en la zona superior o inferior.
- Sin co-branding complejo. Mensaje único y directo.

---

## PARTE 3: REGLAS TRANSVERSALES (DISPLAY + OOH)

1. **Un mensaje, una acción.** Un titular + un CTA. Sin multiples mensajes en un mismo banner.
2. **El precio siempre visible si es el argumento principal.** eur después del número, decimal con coma, "/mes" en subindice.
3. **Logo M siempre presente y legible.** En formatos muy pequenos, logo M solo (sin wordmark).
4. **Azul Movistar siempre presente** como fondo, logo, CTA o acento.
5. **Texto legal al pie** en todos los anuncios con precio o condición.
6. **Fotografía real** de personas espanolas/LATAM en escenas cotidianas. Nunca stock corporativo, nunca IA visible.
7. **Sin em dashes** en todo el copy.

---

## Assets necesarios por campaña display

- [ ] Titular (max 40 chars en 300x250; 60 en formatos grandes)
- [ ] Subtitulo o claim (max 60 chars)
- [ ] CTA (max 20 chars)
- [ ] Precio y condiciones si aplica
- [ ] Texto legal
- [ ] Logo M en variante correcta según fondo (mark.svg / mark-inverse.svg)
- [ ] Imagen fotografica si el formato la incluye (real, no stock, no IA)

## Assets necesarios por campaña OOH

- [ ] Todo lo anterior +
- [ ] Formato final (MUPI vertical, valla horizontal, lona, cartel)
- [ ] Dimensiones exactas del soporte (mm) y sangrado (3-5mm)
- [ ] Resolución mínima 150dpi al tamaño final
- [ ] Prueba de color CMYK aprobada
