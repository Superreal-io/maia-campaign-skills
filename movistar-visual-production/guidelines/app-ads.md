# Aplicación : Publicidad (Display, OOH, Digital)

Versión enriquecida con los patrones reales observados en las piezas (ver `../reference-pieces/INDEX.md` secciones Display digital, Exterior, Tienda; y `../audit-report.md` §1).

---

## Formatos display digital (IAB estándar)

| Formato | Dimensiones | Uso típico |
|---------|-------------|-----------|
| Leaderboard | 728×90px | Banner horizontal cabecera |
| Medium Rectangle | 300×250px | El más común, sidebar |
| Wide Skyscraper | 160×600px | Banner vertical lateral |
| Half Page | 300×600px | Impacto alto |
| Billboard | 970×250px | Top de home portales |
| Mobile Banner | 320×50px | Móvil pie de página |
| Mobile Interstitial | 320×480px | Móvil transición |

---

## Patrón dominante display vertical (300×600 / half page)

Es el formato más usado en captación Movistar. Estructura fija observada en `display-mov.png`, `display-mov2/3.png`:

```
┌─────────────────────┐  ← M expresiva azul TOP-RIGHT (min 40px)
│  Titular corto azul │  ← sentence case, Bold 24px, 2 líneas
│  en 2 líneas.       │
│                     │
├─────────────────────┤
│                     │
│   [Hero fotografía  │  ← imagen real cuadrada o 4:5
│    ocupando 45%     │
│    del alto]        │
│                     │
├─────────────────────┤
│                     │
│    Desde            │  ← overline azul small 12px
│    15€ /mes         │  ← número XXL 56px + € 24px + /mes 14px
│    Sin permanencia  │  ← subline 12px muted
│    Ser cliente      │
│    tiene ventajas   │  ← "ventajas" en Bold azul
│                     │
├─────────────────────┤
│  [Lo quiero]        │  ← CTA pill azul filled ANCHO (fill 90%)
└─────────────────────┘  ← fondo Blanco Movistar todo
```

**Reglas duras:**
- Fondo siempre Blanco Movistar `#FFFAF5`, nunca azul en display vertical.
- M top-right, nunca junto al wordmark en display pequeño.
- El precio ocupa entre 15% y 25% del alto total. Es el elemento visual más dominante después del titular.
- CTA pill ocupa 90% del ancho, texto centrado, azul filled `#0066FF`.
- Sin animación en el precio. Si hay motion, sólo fade-in del titular y del CTA (200ms).

---

## Patrón display horizontal (728×90, 970×250)

Menos frecuente. Estructura:

```
┌───────────────────────────────────────────────────────────┐
│  M    Titular corto (1 línea)     Desde 15€/mes  [CTA]   │
└───────────────────────────────────────────────────────────┘
```

- Todo en una línea, izquierda a derecha: M → titular → precio → CTA.
- Fondo blanco Movistar o azul filled con inversión de colores.
- Logo M 24-32px según alto disponible.

---

## Sistema 1/16 para banners

X = lado corto ÷ 16.

- 300×250px: X = 15.6 ≈ 16px → margen 15px, logo M ≥ 40px (excepción: el 3X daría 47px, redondeamos a 40 para respirar).
- 728×90px: X = 5.6 ≈ 6px → margen 12px, logo M 20-24px (mínimo funcional).
- 300×600px: X = 18.75 ≈ 19px → margen 24px, logo M 56-60px (canónico).
- 970×250px: X = 15.6 ≈ 16px → margen 20px, logo M 40-48px.

**Nota**: en formatos con lado corto < 100px (leaderboard), la legibilidad manda. Logo M mínimo 20px aunque el 3X salga menor.

---

## Composición por tipo de fondo

| Fondo | Titular | Logo M | CTA |
|-------|---------|--------|-----|
| Blanco Movistar `#FFFAF5` | Azul Bold | Azul (mark.svg) | Pill azul filled, texto blanco |
| Azul Movistar `#0066FF` | Blanco Extrabold | Blanco (mark-inverse.svg) | Pill blanco filled, texto azul |
| Secundario claro | Color secundario oscuro Bold | Azul | Pill azul filled |

---

## Formatos OOH físico

| Formato | Dimensiones orientativas | Patrón visual |
|---------|-------------------------|---------------|
| MUPI vertical A0 | 1190×1750mm (ratio 2:3) | Vertical, patrón "MUPI" abajo |
| Cartel A3 | 297×420mm | Vertical, patrón "cartel" abajo |
| Valla 4×3 | 4000×3000mm | Horizontal, patrón "valla" abajo |
| Lona gran formato | 8000×3000mm o mayor | Horizontal ancho, patrón "lona" abajo |
| Metro (backlit) | Variable, típ. 1200×1800mm | Ver patrón MUPI |
| Cartel escaparate | A2/A1, variable | Ver Fondos-Teams-ConexionParaTi.png |

**Regla 1/16 en gran formato:** M = 6X (no 3X) en valla y lona. Margen amplificado 6X también.

---

## Patrón MUPI vertical (referencia: `mupi.png`)

```
┌─────────────────┐
│   Titular       │  ← Movistar Sans Bold 60-72pt, sentence case, blanco o azul,
│   sensación de  │     2-3 líneas, top-left, ocupa 20-25% del alto
│   vivir estre-  │
│   nando.        │
│                 │
│                 │
│     [Producto   │  ← hero: mano+dispositivo o escena
│      / gesto]   │     ocupa 50-60% del alto central
│                 │
│                 │
│                 │
│  [Producto      │  ← thumbnail pequeño 40×40 si aplica
│   secundario]                                          │
│                 │
│  Suscríbete     │  ← nombre de oferta Bold 24pt
│  a Swap    [M]  │  ← M expresiva azul BOTTOM-RIGHT
│  Estrena un iPhone   ← subline Regular 12pt
│  17 y renuévalo cada 2 años.
└─────────────────┘
```

**Reglas MUPI:**
- Fondo pleno azul Movistar `#0066FF` o Blanco `#FFFAF5`. Nunca gradiente.
- M expresiva bottom-right, tamaño ~10-12% del ancho.
- Titular arriba, nombre de oferta abajo, hero en el centro.
- Legal 8-10pt al pie, discreto pero legible a 2m.

---

## Patrón valla / lona horizontal (referencia: `lona.png`, `exterior.png`)

- Layout horizontal, titular a la izquierda o centrado.
- Hero image derecha (a veces bleed hasta borde).
- M expresiva top-right, gran tamaño 8-10% del ancho.
- Precio destacado en placa (amarillo o azul-claro) si aplica.
- Overline optativo: "Ser cliente tiene ventajas" o "Fibra en tu casa de verano".

---

## Patrón wild-posting / serie Carteles (referencia: `Carteles.png`)

Serie de piezas pegadas en secuencia sobre un muro. Cada pieza usa un secundario distinto (uno azul filled + varios secundarios claros). Estructura común:

```
┌─────────────┐
│      [M]    │  ← M azul top-right sobre fondo secundario
│             │
│ Ser de      │  ← overline Regular 14pt
│ Movistar es │
│             │
│ Hablar      │  ← titular Bold 96-120pt en color secundario OSCURO
│ con tus     │     que empareja con el fondo (verde-oscuro sobre verde-claro,
│ amigos      │     azul-oscuro sobre azul-claro, etc.)
│ jugando     │
│ en la Play. │  ← termina con punto final como recurso gráfico
└─────────────┘
```

**Reglas de serie:**
- Cada pieza: 1 secundario de fondo + su pareja oscura para tipografía.
- Todas las piezas de la serie comparten estructura (overline + titular + M).
- No hay CTA, no hay precio. Pura declaración de marca.
- La primera pieza siempre en azul Movistar filled con tipo en blanco (ancla la serie).

---

## Patrón cartel tienda / POS (referencia: `tienda.png`)

Formato chevalet interior. Cartel A2/A1 sobre soporte.

```
┌─────────────────────┐
│       [M]           │  ← lockup horizontal centrado top
│   Movistar          │
│                     │
│ Ser cliente         │  ← titular apilado 3 líneas
│ tiene               │
│ Ventajas.           │  ← última línea AZUL con PUNTO final
│                     │
│   [productos]       │  ← lifestyle: iPhone + AirPods + Watch
│                     │
│  [placa AMARILLA]   │  ← precio/descuento en amarillo con borde suave
│  Hasta 300€         │
│  de descuento       │
│                     │
│  [banda azul-osc]   │  ← co-branding con partners
│  repsol logo | 200€ extra
│                     │
│  Pregunta por tu    │  ← CTA suave con icono chat
│  ventaja personal.  │
└─────────────────────┘
```

**Reglas tienda:**
- Fondo Blanco Movistar `#FFFAF5`.
- Placa amarilla `#FFE99C` para descuentos monetarios.
- Última línea del titular siempre en azul, con punto final si el titular busca énfasis dramático.
- Partners co-branded en banda azul-oscuro `#022D67` estrecha abajo.

---

## Reglas de contenido en ads (transversales)

1. **Un mensaje, una acción.** Un titular + un CTA. Sin múltiples mensajes en un mismo banner.
2. **El precio siempre visible si es el argumento principal.** € después del número, decimal con coma, "/mes" en subíndice.
3. **Logo M siempre presente y legible.** En formatos muy pequeños, logo M solo (sin wordmark).
4. **Azul Movistar siempre presente** como fondo, logo, CTA o acento.
5. **Sin animaciones complejas** en display. Fade + traducción simple. Máximo 3 frames. Sin loops infinitos en formatos ricos.
6. **Texto legal al pie** en todos los anuncios con precio o condición. Mínimo 12px, máximo 4 líneas.
7. **Fotografía real** de personas españolas/LATAM en escenas cotidianas. Nunca stock corporativo, nunca IA visible.

---

## Assets necesarios por campaña display

- [ ] Titular (máximo 40 caracteres en 300×250; 60 en formatos verticales grandes)
- [ ] Subtítulo o dato (máximo 60 caracteres)
- [ ] CTA (máximo 20 caracteres)
- [ ] Precio y condiciones si aplica
- [ ] Texto legal
- [ ] Logo M en variante correcta según fondo (mark.svg / mark-inverse.svg)
- [ ] URL de destino (landing page con UTMs)
- [ ] Imagen fotográfica si el formato la incluye (real, no stock, no IA)

---

## Assets necesarios por campaña OOH

- [ ] Todo lo anterior +
- [ ] Formato final (mupi vertical, valla horizontal, lona, cartel)
- [ ] Dimensiones exactas del soporte (mm) y sangrado (3-5mm)
- [ ] Resolución mínima 150dpi al tamaño final
- [ ] Prueba de color CMYK aprobada
- [ ] Fecha de instalación y ubicación (para lucración de contenido geolocal)
