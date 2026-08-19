# Aplicación : Movistar Plus+ (M+)

Canal de publicidad dentro de la plataforma de streaming Movistar Plus+. Las piezas se muestran en el carousel hero de la home de la app M+ y como videocartelas de contenido expandido.

Fuente: 6 entregables de Figma (eSimFLAG, Fibra Adicional, FTTR, Ventaja Personal, Verano Dispositivos, Motor F1) + 11 piezas gold standard (FTTR, MPA, Ficción, Deportes, Dispositivos, Futbol).

---

## Tipos de pieza

Cada entregable M+ consta de 2 o 3 piezas con nomenclatura interna fija:

| Codigo | Nombre | Obligatoria | Función |
|--------|--------|-------------|---------|
| **WOW** | Banner horizontal | Si | Hero del carousel en la home de M+. Es la pieza principal que genera el Art Director. |
| **NUX/MUX** | Banner en contexto app | Si | Screenshot/mockup que muestra el WOW dentro de la UI real de M+ (fondo oscuro, carousel, nav, categorias). Sirve de preview para el cliente. |
| **VIDEOCARTELA** (o TEL) | Pieza standalone | No (4/6 casos) | Version expandida del WOW con más detalle: QR, telefono, body copy, pasos. Se usa cuando hay precio o acción concreta. |

**El Art Director produce la WOW y la VIDEOCARTELA.** La NUX/MUX es un mockup contextual que se genera montando la WOW sobre una captura de la app M+; no requiere diseño creativo propio.

---

## WOW -- Banner horizontal

### Dimensiones y ratio

- Ancho: ~1600-2335px (varia según entregable)
- Alto: ~320-470px
- Ratio aproximado: **5:1** (muy apaisado)
- Para MAIA, usar **1920x640px** como dimensión estándar (ratio 3:1)

### Layout

```
┌──────────────────────────────────────────────────────┐
│  M (azul)                                            │
│                                                      │
│  [Overline opcional]         ┌──────────────────────┐│
│  Titular Bold               │                      ││
│  grande                     │    VISUAL            ││
│                             │    (foto/producto/   ││
│  [Precio si aplica]         │     gráfico)         ││
│                             │                      ││
│  CTA link >                 └──────────────────────┘│
│                                                      │
└──────────────────────────────────────────────────────┘
```

- **Zona izquierda (~40%):** copy, precio, CTA
- **Zona derecha (~60%):** visual (fotografía, producto en cutout, gráfico)
- **M azul** siempre en top-left (no M+, solo la M de Movistar). Usar slot `{{LOGO_MARK}}` en fondo claro, `{{LOGO_MARK_INVERSE}}` en fondo oscuro.

### Reglas tipograficas

- **Overline** (opcional): sentence case, regular, ~14px, texto en blanco o azul según fondo. Ejemplos: "Por ser de Movistar, 30% de descuento", "Fin de semana de doble adrenalina"
- **Titular**: Bold o ExtraBold, ~28-40px, sentence case, 2-3 líneas máximo. En blanco sobre fondo oscuro, en negro sobre fondo claro.
- **Subtitulo/body**: Regular, ~16px, 1-2 líneas máximo. Secundario respecto al titular.
- **Precio** (cuando aplica): número XXL (~48-64px) ExtraBold + eur/mes en tamaño menor. Precio anterior tachado si hay descuento.

### CTA

**Siempre link con underline y flecha `>`.** Nunca boton relleno ni outline en el WOW.

- Texto: sentence case, sin exclamación. Ejemplos: "Más información >", "Contrata aquí >", "Descubre el catálogo >", "Contratalo aquí >"
- Color: azul `#0066FF` en fondo claro, azul claro en fondo oscuro
- Posición: debajo del titular o del precio, alineado a la izquierda

### Fondos

Cuatro modos observados:

1. **Claro** (`#FFFAF5`): para productos de hogar/familia (eSimFLAG, Fibra Adicional). Visual = fotografía lifestyle a la derecha.
2. **Oscuro** (negro/navy): para productos tech/premium (FTTR, MPA Alarmas, Dispositivos/Swap). Visual = graficos neon, fotos dramaticas, producto en cutout. Texto en blanco.
3. **Azul** (`#0066FF`): para contenido/entretenimiento (Ficción, Cine). Texto en blanco. Visual = fila de thumbnails de contenido a la derecha.
4. **Foto a sangre**: para productos estacionales y deportes (Verano, Mundial, Futbol). La foto ocupa todo el fondo (estadio, campo). Texto en blanco con posible sombra sutil.

**Regla**: el fondo del WOW determina el fondo de la VIDEOCARTELA. Son coherentes.

### Variantes de visual en zona derecha

La zona derecha (~60%) del WOW admite tres patrones de visual:

- **Producto hero**: producto en cutout a gran escala (iPhone, camara, router). Puede usar el color propio del producto como dominante visual (ej. iPhone 17 Pro en naranja sobre fondo negro).
- **Fila de thumbnails de contenido**: 4-5 posters verticales de peliculas/series en fila. Fondo azul. Usado para campañas de cine/contenido M+.
- **Foto a sangre**: la foto ocupa toda la zona (o todo el banner). Estadio aereo, paisaje deportivo, escena de competición.

### Logos de partners

Cuando hay co-branding (DAZN, MotoGP, F1, Samsung, LG), los logos de partner aparecen en línea horizontal debajo del CTA o debajo del precio. Tamano pequeno (~24-32px alto), en blanco sobre fondo oscuro.

---

## NUX/MUX -- Banner en contexto app

**El Art Director NO diseña esta pieza desde cero.** Es un montaje del WOW sobre la UI real de M+.

### Estructura de la app M+ (referencia)

```
┌──────────────────────────────────────────────────────┐
│  M+  (logo blanco)                    21 abr 14:54   │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  < [        WOW BANNER aquí        ] >    ●○○○○│  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Apps | Q | ☰ | UHD | Originales | Cine | Series ... │
│                                                      │
│  ┌────┐ ┌────────┐ ┌──────────────┐ ┌───────────┐   │
│  │ M+ │ │ Cine   │ │Documentales  │ │ Originales│   │
│  └────┘ └────────┘ └──────────────┘ └───────────┘   │
│                                                      │
│  Tendencias M+ | Originales M+ | DAZN | Netflix ...  │
│                                                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ thumb  │ │ thumb  │ │ thumb  │ │ thumb  │        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
└──────────────────────────────────────────────────────┘
```

- Fondo general: oscuro (la app M+ es dark mode)
- Carousel: flechas `<` `>` en los laterales, indicadores de dots abajo derecha (5 dots, uno activo)
- Debajo del carousel: barra de navegación horizontal (Apps, Originales, Cine, Series, Deportes, Netflix, Infantil, Documentales, Musica)
- Debajo: pills de categorias con colores (M+ blanco, Cine rojo, Comedia amarillo, Documentales verde, Originales naranja, Deportes rojo, Series rosa, Acción...)
- Debajo: chips de filtro (Tendencias M+, Originales M+, DAZN, Netflix, SkyShowtime, Disney+, Prime Video)
- Debajo: thumbnails de contenido

**Para producción:** si el sistema necesita generar un NUX/MUX, montar el render del WOW sobre un screenshot base de la app M+. No recrear toda la UI.

---

## VIDEOCARTELA -- Pieza standalone

### Dimensiones y ratio

- Ancho: ~1700-2047px
- Alto: ~960-1151px
- Ratio aproximado: **16:9** o ligeramente más alto
- Para MAIA, usar **1920x1080px** como dimensión estandar

### Layout

La videocartela es una versión expandida del WOW. Mismo visual, misma foto, pero con más espacio para:

```
┌──────────────────────────────────────────────────────┐
│  M (azul)                                            │
│                                                      │
│  Titular Bold               ┌──────────────────────┐│
│  muy grande                 │                      ││
│  (más que en WOW)           │    VISUAL            ││
│                             │    (misma foto/      ││
│  Subtitulo / body copy      │     gráfico que WOW  ││
│  extendido                  │     pero más grande) ││
│                             │                      ││
│  ┌────────┐ ┌─────┐        └──────────────────────┘│
│  │ Precio │ │ QR  │                                 │
│  │ grande │ │ +M  │                                 │
│  └────────┘ └─────┘                                 │
│  [Legal / telefono ayuda]                            │
└──────────────────────────────────────────────────────┘
```

### Elementos adicionales respecto al WOW

- **Titular más grande**: ~48-72px, mismo texto o versión expandida
- **Body copy**: 2-4 líneas de texto explicativo (ausente en el WOW)
- **Bloque de precio expandido**: nombre del producto (ej. "Fibra Adicional") + precio XXL + eur/mes + "Sin permanencia" + precio anterior tachado si aplica
- **QR con watermark M**: código QR azul con la M de Movistar integrada en el centro. Siempre presente cuando hay acción de contratación.
- **Telefono de ayuda** (opcional): "Si necesitas ayuda, llama al 900 xxx xxx" en texto pequeno
- **Pasos numerados** (opcional): "Activa tu descuento en tres pasos:" con circulos azules numerados (1, 2, 3) + texto. Patron idéntico al componente "3 pasos" de las landing web.
- **Logos de partners** (si aplica): misma posición que en WOW pero con más espacio
- **CTA texto** (opcional): "Ver el catálogo" junto al QR

### Fondo

Sigue el mismo modo que el WOW del entregable:
- WOW claro -> VIDEOCARTELA fondo `#FFFAF5`
- WOW oscuro -> VIDEOCARTELA fondo oscuro/negro
- WOW foto a sangre -> VIDEOCARTELA misma foto expandida

---

## Paleta de colores

Las piezas M+ usan la paleta cerrada de Movistar, con estas particularidades:

- **Fondo claro**: `#FFFAF5` (Blanco Movistar). Valido aquí porque M+ es canal offline/app, no web.
- **Fondo oscuro**: negro puro o navy muy oscuro. Se usa para campañas tech/premium/deporte.
- **Texto sobre fondo claro**: `#262423` (Negro Movistar)
- **Texto sobre fondo oscuro**: `#FFFAF5` o blanco puro
- **Acentos**: `#0066FF` (Azul Movistar) para CTA, overlines, nombre de producto
- **Precio**: blanco sobre fondo azul filled, o negro sobre fondo claro
- **Precio tachado**: gris `#6F7176` o en tamaño menor junto al precio actual

**Excepción fondo oscuro**: las piezas con fondo oscuro usan colores dramaticos (neon azul en FTTR, tonos verdes de campo en Mundial). Estos no forman parte de la paleta cerrada sino que vienen de la fotografía/gráfico. El texto y los CTAs siguen en la paleta cerrada.

---

## Reglas de fotografía/visual

- **Fondo claro lifestyle**: fotos de personas en contexto domestico/viaje, sin filtros dramaticos, luz natural. Producto secundario o ausente.
- **Fondo oscuro tech**: graficos 3D, neon, líneas de luz. Sin personas o personas en silueta. Producto como protagonista si aplica.
- **Fondo foto a sangre**: escena completa (playa, estadio, campo). Productos en cutout superpuestos sobre la foto. Etiquetas de producto debajo de cada item.
- **Productos en pedestal**: en campañas de dispositivos, los productos se presentan sobre pedestales circulares blancos 3D. Cada pedestal lleva etiqueta con marca + modelo debajo.

---

## Naming convention de archivos

Basado en los nombres de capa de Figma:

```
AAMMDD_[TIPO]_[CODIGO-CAMPANA]_[DESCRIPCION]

Ejemplos:
260525_BANNERS_ESIM_VERANO_WOW
260525_BANNERS_ESIM_VERANO_NUXMUX
260525_BANNERS_ESIM_VERANO_VIDEOCARTELA
260528_WOW_PAC33634_FTTR
260528_NUX_MUX4_PAC33634_FTTR
260528_VIDEOCARTELA_PAC33634_FTTR
260612_PAC33726_WOW_MOTOR
260622_PAC33726_NUX_MUX4_MOTOR
```

Los prefijos PAC son códigos internos de campaña en Movistar.

---

## Checklist antes de entregar

### WOW

- [ ] Ratio ~3:1 (1920x640px)
- [ ] M azul en top-left (slot correcto según fondo)
- [ ] Titular bold, sentence case, 2-3 líneas máximo
- [ ] CTA = link con underline y `>`, nunca boton
- [ ] Precio prominente si la campaña lo requiere
- [ ] Visual en zona derecha (~60%), no cortado
- [ ] Fondo coherente con el tono de la campaña
- [ ] Logos de partners si aplica
- [ ] Sin em dashes en copy
- [ ] Ortografia castellana correcta (tildes, ene, signos apertura)

### VIDEOCARTELA

- [ ] Ratio ~16:9 (1920x1080px o similar)
- [ ] Mismo fondo que el WOW
- [ ] Titular más grande que en el WOW
- [ ] Body copy extendido (2-4 líneas)
- [ ] Bloque de precio expandido si aplica
- [ ] QR con watermark M si hay acción de contratación
- [ ] Telefono de ayuda si aplica
- [ ] Pasos numerados si aplica
- [ ] Legal si aplica
- [ ] Coherencia visual total con el WOW (misma foto, mismos colores)
