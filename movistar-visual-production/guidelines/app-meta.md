# Aplicación: Meta / Social

Version basada en 20 piezas reales de campaña (feed 1:1, stories 9:16, feed landscape 1.91:1) extraidas de producción final de Movistar.

---

## Especificaciones técnicas

| Propiedad | Valor |
|-----------|-------|
| Formato principal MAIA | **Feed 1080x1080** (1:1, cuadrado) |
| Formato secundario | **Stories 1080x1920** (9:16, vertical) |
| Formato adicional (si plan lo pide) | **Feed landscape 1200x628** (1.91:1, horizontal) |
| Fondo dominante | Colores solidos suaves: `#FFFAF5`, salmon, verde mint, azul claro `#EFF5FB` / `#D3EEFF`, o azul solido `#0066FF` |
| Tipografia | `"Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif` |
| Pipeline | HTML fijo + assemble.py + render.py -> PNG |

**MAIA produce el formato feed 1080x1080 como pieza representativa.** Stories 1080x1920 se produce solo si el plan de medios asigna volumen significativo a stories. Feed landscape es excepcional.

---

## Formatos y ratios

| Formato | Ratio | Dimensiones | Uso principal |
|---------|-------|-------------|---------------|
| Feed cuadrado | 1:1 | 1080x1080 | Pieza principal. Producto, dispositivos, value-add, deporte, co-branding |
| Stories | 9:16 | 1080x1920 | Convergente, contenido+futbol, dispositivos. Más espacio para precio + specs + CTA telefono |
| Feed landscape | 1.91:1 | 1200x628 | Adaptación horizontal para Facebook link ads. Menos frecuente |

Las piezas feed y stories pueden ser versiones del mismo concepto adaptadas al ratio. El contenido es el mismo, la composición cambia.

---

## Layouts por formato

### Feed 1080x1080 (7 variantes observadas)

**A. Producto hero central**
Fondo de color solido suave (verde mint, azul claro, salmon, beige). Producto en cutout centrado o ligeramente desplazado. Titular ExtraBold + Regular alternado (2-3 líneas). Elemento visual complementario (ej. etiqueta precio colgante). Cierre: "Ser Cliente tiene ventajas" + M logo en bottom. Co-branding logos si aplica.

```
┌──────────────────────────────┐
│  [Etiqueta visual]  TITULAR  │
│                     ExtraBold│
│                     + Regular│
│       [PRODUCTO]             │
│                  Co-brand    │
│                              │
│  Ser Cliente       [M logo]  │
│  tiene ventajas              │
└──────────────────────────────┘
```

**B. Multi-producto**
Fondo neutro (beige/salmon). Titular ExtraBold negro arriba. Fila de 2-3 productos en cutout. Precio "Desde X eur/mes" XXL. Claim de urgencia ("!Por un tiempo limitado!") sobre banda oscura. Sin M logo prominente (la plataforma ya lo marca).

**C. Fondo azul solido (contenido/value-add)**
Fondo `#0066FF`. M logo blanco grande (top-right). Titular blanco ExtraBold, sentence case. Subtitulo blanco regular o italica. Precio si aplica. Franja inferior con contenido visual (fotos de partidos, logos competiciones). Badge de ahorro (pill amarillo/dorado).

**D. Fondo azul solido (deporte)**
Variante de C con ilustración deportiva, fotos reales de partidos en strip inferior. Logos de competiciones (LaLiga, DAZN, Champions, etc.) en fila al pie.

### Stories 1080x1920 (4 variantes observadas)

**E. Convergente/producto**
M logo top (centrado). "miMovistar" label. Titular ExtraBold negro/azul (2-4 líneas). Specs en fila compacta (Fibra | líneas | TV), separados por pipes o barras. Foto lifestyle o productos debajo. Precio XXL (con precio anterior tachado si hay descuento). "Sin permanencia". CTA telefono al pie ("Llama gratis al 900 XX XX XX" + icono). Legal mínimo.

```
┌────────────────────┐
│      [M logo]      │
│     miMovistar     │
│                    │
│  Fibra + móvil     │
│  + TV por solo     │
│  53 eur/mes        │
│  Sin permanencia   │
│                    │
│  [FOTO / PRODUCTO] │
│                    │
│  Y elige disp.    │
│  desde 0 eur/mes   │
│                    │
│  Llama gratis al   │
│  900 XX XX XX      │
└────────────────────┘
```

**F. Contenido + convergente (Netflix, futbol)**
Fondo bicolor: azul (#0066FF o navy) arriba, blanco abajo. Titular con logo del partner (NETFLIX en bold). Grid de thumbnails de contenido (3-4 posters). Specs + logos de plataformas. Claim emocional ("Y además todo el futbol"). Precio con tachado. Legal al pie.

**G. Dispositivos**
Fondo salmon/neutro. Titular emocional o de ocasion ("Este San Valentin regala Google Pixel"). Productos en cutout centrados (2-3 modelos). "Desde 0 eur/mes con miMovistar". Badge de ahorro en verde `#00C48C`.

### Feed landscape 1200x628

**H. Split horizontal**
Mitad izquierda: M logo + "miMovistar" + specs + precio. Mitad derecha: foto lifestyle + productos superpuestos. CTA telefono al pie. Fondo blanco o beige claro.

---

## Patrones de color

### Fondos

- **Beige Movistar** `#FFFAF5`: fondo dominante en piezas convergentes y dispositivos. Valido en META porque es canal offline.
- **Salmon suave** (~`#FDDCCC` / `#F5D5C8`): usado para dispositivos, San Valentin, ofertas estacionales.
- **Verde mint** (~`#C8E6C9`): usado para co-branding tech (Ray-Ban Meta).
- **Azul claro** `#EFF5FB` / `#D3EEFF`: usado para packs convergentes con contenido.
- **Azul solido** `#0066FF`: para piezas de contenido/deporte y value-add (ChatGPT, futbol). Texto blanco.
- **Bicolor azul + blanco**: stories de contenido (Netflix, futbol). Zona superior azul con contenido visual, zona inferior blanca con precio.

### Regla general

En META no se usa fondo blanco puro `#FFFFFF`. Siempre hay un tono calido, azul o de color. Esto ayuda a diferenciarse en el feed y es coherente con la regla offline del brand book.

### Acento verde

`#00C48C` solo para badges de ahorro en dispositivos y Swap. Nunca como fondo general.

---

## Tipografia

| Elemento | Peso | Tamano (1080x1080) | Color |
|----------|------|---------------------|-------|
| Titular principal | ExtraBold | 64-96px | Negro `#262423` (fondo claro) o blanco (fondo azul) |
| Keyword highlight | ExtraBold | Mismo que titular | Azul `#0066FF` (sobre fondo claro) |
| Subtitulo / body | Regular | 36-48px | Negro, gris `#6F7176`, o blanco |
| Italica descriptiva | Regular Italic | 36-48px | Blanco (sobre azul) |
| Specs (Fibra, líneas, TV) | Bold | 28-36px | Negro o blanco |
| Precio XXL | ExtraBold | 96-144px | Negro o azul `#0066FF` |
| Precio anterior tachado | Regular | ~48px | Gris `#6F7176` |
| "Sin permanencia" | Regular | 28-36px | Negro |
| Legal | Regular | 20-24px | Gris `#6F7176` |

### Regla de énfasis en titulares

Una keyword se destaca en azul `#0066FF` o en bold cuando el resto es regular. Patron alternancia: "Pregunta **lo que quieras,** sin sacar el móvil." (ExtraBold en azul + Regular en negro). Máximo una keyword por titular.

### Sentence case

Siempre sentence case en titulares. No ALL CAPS salvo logos de partner (NETFLIX, DAZN).

---

## CTA y acción

### Diferencia clave con otros canales

En META, **el CTA principal lo proporciona la plataforma** (boton nativo del anuncio: "Más información", "Comprar", "Llamar ahora"). La pieza visual NO necesita un boton CTA pill como en email o web.

### Patrones de acción observados

- **Telefono**: "Llama gratis al 900 XX XX XX" con icono telefono. Usado en stories convergentes. Es un refuerzo, no el CTA principal.
- **Claim de urgencia**: "!Por un tiempo limitado!" sobre banda oscura. Usado en piezas de dispositivos con oferta temporal.
- **Badge de ahorro**: pill con "Ahorra hasta X eur" en verde o amarillo.
- **Sin CTA explicito**: muchas piezas feed no tienen ningún CTA en la imagen. El copy del anuncio y el boton nativo hacen ese trabajo.

### Lo que MAIA NO debe hacer

- NO incluir boton CTA pill azul dentro de la pieza META (eso es para email/web).
- NO incluir URL ni "visita movistar.es" en la pieza. El link está en el anuncio.
- NO poner el telefono 900 en piezas feed 1:1 (no hay espacio y el boton nativo es mejor). Solo en stories si el plan lo requiere.

---

## Elementos recurrentes

### M logo

Siempre presente. Posición y color según fondo:

| Fondo | Color logo | Posición tipica |
|-------|-----------|-----------------|
| Claro (beige, salmon, verde, azul claro) | Azul `#0066FF` | Bottom-right |
| Azul solido `#0066FF` | Blanco | Top-right |
| Bicolor | Blanco (en zona azul) | Top-right o top-left |

### "miMovistar"

Label que aparece sobre el precio en piezas convergentes (Fibra+móvil+TV). Indica el paquete. Texto azul, regular, encima del titular o encima del precio.

### "Ser Cliente tiene ventajas"

Claim de fidelización. Texto negro, "tiene ventajas" en italica. Aparece en bottom-left. Usado en piezas de dispositivos y value-add para clientes existentes. En META aparece como texto plano (no como badge pill azul como en email).

### "Sin permanencia"

Claim de confianza. Siempre debajo del precio, en regular, tamaño menor.

### Precio anterior tachado

Cuando hay descuento: precio anterior en gris/tachado a la izquierda o arriba, precio nuevo XXL en negro o azul.

### Badge de ahorro

Pill redondeado con "Ahorra hasta X eur" o "Ahorra X eur". Verde `#00C48C` para dispositivos, amarillo/dorado para value-add.

### Logos de partner / competición

- **Co-branding producto**: logos del partner en posición secundaria (Ray-Ban | Meta, ChatGPT). Nunca dominan la pieza.
- **Logos de competición/plataforma**: LaLiga, DAZN, Champions, Netflix, M+, Apple TV, etc. En fila horizontal al pie o en zona dedicada. Tamano pequeno.
- **Etiquetas energeticas**: badges pequenos junto al producto.

---

## Fotografía y producto

### Fotos lifestyle

Familias o parejas usando dispositivos (tablet, portatil). Contexto domestico, iluminación natural, tono calido. Siempre reales (no stock genérico ni IA visible).

### Productos en cutout

Sobre fondo limpio. Sin sombra pesada. Ángulo 3/4 para dispositivos. Si hay varios, jerarquía de tamaño: producto principal más grande, secundarios menores. Etiqueta energetica si aplica.

### Contenido visual (posters, partidos)

Para piezas de contenido: grid de 3-4 thumbnails de series/peliculas, o strip horizontal con fotos de partidos reales. Calidad alta, sin bordes blancos entre thumbnails.

### Ilustración

Permitida en piezas de deporte (estilo Movistar: jugador en movimiento, balones). Combina con fotos reales en la misma pieza.

---

## Composición por tipo de campaña

| Tipo | Layout feed | Layout stories | Fondo | Elementos clave |
|------|-------------|----------------|-------|-----------------|
| **Convergente** (Fibra+móvil+TV) | -- | E | Beige `#FFFAF5` o azul claro | miMovistar + specs + precio + foto lifestyle + telefono |
| **Convergente + contenido** (Netflix, futbol) | -- | F | Bicolor azul + blanco | Logo partner + grid contenidos + specs + precio tachado |
| **Dispositivos** | B | G | Salmon o beige | Productos cutout + precio 0eur + badge ahorro |
| **Dispositivos + co-branding** | A | -- | Color suave tematico (verde, azul, salmon) | Etiqueta exclusiva + producto + "Ser Cliente" |
| **Contenido/deporte** | C, D | -- | Azul solido `#0066FF` | M blanco + titular emocional + fotos/logos competición |
| **Value-add** (ChatGPT, etc.) | C | -- | Azul solido `#0066FF` | Logo partner + beneficio + duración + badge ahorro |
| **Solo fibra/producto simple** | -- | E | Beige `#FFFAF5` | Foto lifestyle + precio + router incluido + telefono |

---

## Reglas de copy en META

- **Titular**: máximo 6-8 palabras. Directo, sin hype. Beneficio o emoción concreta.
- **Una keyword en azul** o en bold para énfasis. No más.
- **Specs**: en fila compacta con separadores (Fibra 1Gb | 2 líneas 5G+ | TV). No en parrafos.
- **Precio**: siempre XXL. Si hay descuento, precio anterior tachado + precio nuevo.
- **Legal**: al mínimo indispensable. Solo en stories (pie, 20-24px). En feed, el legal va en el copy del anuncio, no en la imagen.
- **Sin em dashes** en todo el copy.
- **Sentence case** siempre.
- **No emojis** en la pieza visual (los emojis van en el copy del anuncio si procede, no en la imagen).

---

## Co-branding en META

Tres patrones observados:

### Producto tech (Ray-Ban Meta)
- Etiqueta visual tematica ("Descuento exclusivo Clientes en tecnologia") como elemento gráfico.
- Producto en cutout con logos co-brand (Ray-Ban | Meta) debajo.
- "Ser Cliente tiene ventajas" + M logo.
- Multiples variantes de copy con mismo layout y fondos distintos (A/B testing visual).

### Plataforma de contenido (Netflix, DAZN)
- Logo del partner integrado en el titular ("Un mundo de pelis y series con NETFLIX").
- Grid de contenido real de la plataforma.
- Logos de plataformas en fila al pie.

### Servicio digital (ChatGPT)
- Fondo azul solido Movistar.
- Logo del partner en zona dedicada (bottom-left) sobre fondo blanco.
- Beneficio como titular ("ChatGPT Plus sin coste").

### Regla general

El co-branding nunca domina la pieza. Movistar sigue siendo el emisor principal (M logo siempre visible, fondo y tipografía Movistar). Los colores del partner se limitan a su logo o a un badge.

---

## Variantes A/B

Patron observado: una misma campaña produce 4-6 variantes con idéntico layout pero distinto copy y/o fondo de color. El Art Director puede generar la pieza base y documentar las variantes en el design rationale. MAIA produce la pieza principal; las variantes son responsabilidad de producción.

---

## Accesibilidad

- Contraste mínimo AA en todo texto sobre fondo.
- No depender del color para transmitir información.
- Texto legible a tamanos reducidos (feed se ve a ~300px en móvil).
- Precio XXL con tamaño suficiente para leer en scroll rápido.

---

## Checklist antes de entregar

- [ ] Formato correcto: 1080x1080 (feed) o 1080x1920 (stories)
- [ ] M logo presente, color correcto según fondo
- [ ] Fotografía real o producto real, no stock genérico ni IA visible
- [ ] Precio XXL si la campaña lo requiere
- [ ] NO hay boton CTA pill en la pieza (el CTA es nativo de la plataforma)
- [ ] Máximo un color de fondo dominante (no mezclar tonos)
- [ ] Una sola keyword destacada en el titular
- [ ] Sentence case en todo el copy
- [ ] Sin em dashes en el copy
- [ ] Legal solo en stories (mínimo), no en feed
- [ ] Si hay co-branding: Movistar sigue siendo emisor principal
- [ ] Badge "Ser Cliente tiene ventajas" si el email es para clientes existentes
- [ ] Contraste AA en todo texto
