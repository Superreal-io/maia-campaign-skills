# Aplicación : Email / CRM

Version enriquecida con patrones reales de 11 emails de Figma + 17 emails Gold Standard (FTTR, MPA, Dispositivos, Dispositivos2/Swap, Equipamiento/iPhone17Pro, JV Repsol, Movistar Plus, Renting Coches, Segunda Fibra, Ventajas Verano, Ventajas2/Protección Digital, Futbol/Champions, Futbol2/Mundial, Deportes/Motor-Golf-Tenis, Ficción/HBO-Sky-Apple-Disney, miMovistar Convergente, eSimFLAG).

---

## Especificaciones técnicas

| Propiedad | Valor |
|-----------|-------|
| Ancho de producción MAIA | **600px** (desktop, formato estandar del canal) |
| Referencia mobile | 375-390px (las piezas de Figma incluyen versiones mobile como referencia) |
| Fondo wrapper | `#F5F5F5` (gris muy claro, crea contraste con el cuerpo) |
| Fondo cuerpo | `#FFFAF5` (Blanco Movistar) |
| Tipografia email-safe | `"Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif` |
| Body | 16px Regular, line-height 1.5 |
| Legal/small | 12px, color muted `#6F7176` |
| Espaciado entre secciones | 32px vertical |

**MAIA produce la versión desktop (600px).** Es el formato estandar del canal email y el que entra en el pipeline visual (HTML -> assemble -> render -> PNG). La adaptación mobile la gestiona el equipo de maquetación. Los 11 ejemplos de Figma incluyen mayoritariamente versiones mobile como referencia visual, pero la pieza que genera el Art Director es a 600px.

---

## Estructura modular

Los emails NO siguen una única plantilla fija. Son modulares: cada email se construye combinando bloques según el producto y la campaña. Los bloques disponibles (observados en los 11 ejemplos reales) son:

### Bloque 1: Header

**Patron dominante (10/11 emails):** M logo azul en top-right sobre fondo blanco `#FFFAF5`. Sin navegación, sin texto adicional. Solo el logo.

**Co-branding:** cuando hay partner (Prosegur, Repsol), el header muestra un lockup conjunto: M + logo del partner. Ejemplo: "MOVISTAR PROSEGUR ALARMAS" con ambos logos en línea.

Altura header: 60-72px.

### Bloque 2: Hero

Cinco variantes observadas:

**2a. Titular-hero con foto lifestyle** (lo más comun)
Fondo `#FFFAF5`. Titular ExtraBold 28-36px en negro, 2-3 líneas. Una palabra clave en azul `#0066FF` o en italic para énfasis (ej. "precio *imbatible*", "*Superseguridad*"). Foto lifestyle debajo o al lado derecho. CTA pill azul debajo.

**2b. Titular-hero con producto**
Similar pero con producto en cutout en lugar de foto lifestyle. Tipico en emails de dispositivos. Puede incluir etiqueta de producto flotante.

**2c. Dark hero** (tech/premium)
Fondo oscuro (negro o navy). Graficos 3D, líneas neon, ilustración técnica. Texto blanco. Logo M en blanco. Usado para FTTR, productos tecnologicos.

**2d. Photo hero full-bleed**
Fotografía ocupando todo el ancho. Texto blanco superpuesto con sombra sutil o sobre banda semitransparente. Tipico en emails de deporte/eventos.

**2e. Card hero** (dispositivos)
Imagen de producto(s) sobre fondo degradado azul palido. Cards de producto integradas en el hero.

**2f. Blue hero** (value-add/servicios)
Fondo azul solido `#0066FF`. Texto blanco ExtraBold. Productos en cutout sobre el azul. M logo blanco top-right. Usado para Renting Coches, servicios digitales. El nombre del producto puede incluir una keyword destacada en amarillo/dorado (ej. "Movistar **Renting** Coches" con "Renting" en pill dorado).

**2g. Photo scene hero** (lifestyle estacional)
Escena fotografica completa con productos integrados en el entorno (ej. dispositivos junto a una piscina, sobre una mesa de terraza). No son cutouts sobre fondo plano sino composición dentro de la foto. Fondo natural (cielo, agua, vegetación). Texto superpuesto en negro/azul.

**2h. Black hero** (dispositivos premium)
Fondo negro puro con producto como protagonista visual absoluto. El dispositivo ocupa la mitad derecha del hero, con iluminación dramatica que destaca su color y materiales (ej. iPhone 17 Pro naranja sobre negro). Texto blanco ExtraBold a la izquierda. Logo M azul top-right. Puede incluir logo de fabricante (Apple) y tagline del producto. Distinto del dark hero (2c): aquí el negro es escaparate de lujo para el producto, no una estetica tech/neon. Gold Standards: email-equipamiento, email-dispositivos2.

**2i. Warm hero** (contenido/entretenimiento estacional)
Fondo calido amarillo/dorado (`#F5D060` a `#FFD700` range). Thumbnails de contenido (peliculas, series) integrados como mosaico dentro del hero. M logo azul top-right. Texto negro ExtraBold. Transmite calidez estacional (ej. "Vacaciones por M+"). Gold Standard: email-movistarplus.

**2j. Navy sport hero** (deporte)
Fondo navy oscuro (`#001A33` a `#0A1628`) con fotografía a sangre de jugadores/deportistas. Texto blanco ExtraBold. M logo blanco. Puede incluir badges de competiciones (Champions, LaLiga) en fila debajo del titular. Distinto del dark hero (2c, tech/neon) y del blue hero (2f, azul solido): aquí el fondo es navy muy oscuro con atmosfera deportiva y fotografica. Gold Standards: email-futbol, email-futbol2.

### Bloque 3: Badge "Ser cliente tiene ventajas"

Pill azul filled (`#0066FF`) con texto blanco en sentence case. Aparece como overline encima del titular hero. Observado en 4/11 emails. Se usa cuando el email comunica un beneficio exclusivo para clientes existentes.

```
┌────────────────────────────────────┐
│  [Ser cliente tiene ventajas]      │  <- pill badge
│                                    │
│  Fibra en tu 2ª casa a             │  <- titular
│  un precio imbatible               │
└────────────────────────────────────┘
```

### Bloque 4: Precio protagonista

Bloque de precio XXL, misma composición que en otros canales:

- **Overline**: "Por ser cliente" o "Desde" en azul, ~14px
- **Numero XXL**: ExtraBold 48-72px, negro o blanco según fondo
- **Unidad**: "€/mes" en tamaño menor (~18px)
- **Precio anterior**: tachado, tamaño menor, gris
- **Condición**: "Sin permanencia" o similar en regular, debajo
- **Variante sobre card azul filled**: número en blanco, fondo `#0066FF`

**Repetición:** en emails largos (>2000px), el bloque de precio se repite al final del email antes del legal, exactamente igual.

### Bloque 5: CTA primario

Boton pill azul filled. Puede aparecer 2 veces en emails largos (tras el hero y antes del footer).

```html
<a href="#" style="
  display:inline-block;
  padding:14px 32px;
  background:#0066FF;
  color:#FFFAF5;
  text-decoration:none;
  font-weight:700;
  border-radius:9999px;
  font-size:16px;
">Quiero mi alarma</a>
```

**Patrones de texto CTA observados:**
- Primera persona: "Quiero mi alarma", "Quiero mi 2ª fibra al mejor precio", "Quiero mejor cobertura"
- Imperativo: "Activa el Mundial en un clic", "Activalo en un clic", "Recargar ahora", "Descubrelo"
- Descriptivo: "Ver dispositivos", "Descubre tu oferta", "DESCUBRE EL CATALOGO", "Ver calendario completo"

Sentence case por defecto. Algun email usa ALL CAPS para el CTA, pero no es la norma.

### Bloque 6: Beneficios/ventajas

Tres patrones observados:

**6a. Grid 2x2 de iconos en cards**
Cards con fondo claro (`#EFF5FB` o `#FFFAF5`), bordes redondeados. Cada card: icono outline azul 48px + título bold 16px + body 14px 2-3 líneas. Ejemplo: "Cobertura total / en todos los rincones, sin puntos ciegos". 2 columnas, 2 filas.

**6b. Lista vertical de beneficios**
Filas horizontales sobre cards beige (`~#F5F0EB`). Cada fila: icono outline azul a la izquierda + texto bold a la derecha, 1 línea. Sin body adicional. Más compacto. Ejemplo: prepago (llamar, navegar, controlar gasto).

**6c. 3-up horizontal** (patron "3 ventajas")
Tres columnas sin cards, sobre fondo blanco. Icono + título centrado + body centrado. Cada columna puede usar un color secundario distinto (excepción documentada a "un secundario por pieza"). Ejemplo: Repsol (Descuentos exclusivos, Más ahorro, Más facilidad).

### Bloque 7: Cards de producto

Para emails de dispositivos o catálogo:

- Fondo claro (`#EFF5FB`), bordes redondeados 8px
- Imagen de producto en cutout
- Nombre de producto en bold (marca + modelo)
- "Con tu pack desde **XX €/mes**" en azul + bold
- "Renuevalo cada XX meses" en verde `#00C48C` (solo Swap)
- Etiqueta energetica (badge pequeno, bottom-right)
- Layout: 1 card grande + 2 cards menores debajo en 2 columnas

### Bloque 8: Grid de categorias

Para emails de descuento en dispositivos. Grid 2x3 de botones outline:

- Borde azul `#0066FF`, fondo blanco, border-radius 8px
- Icono azul + texto: "Moviles", "Smartwatch", "Tablets", "Portatiles", "Hogar y ocio", "Gaming"
- Funciona como menu de navegación dentro del email

### Bloque 9: Programación deportiva

Dos variantes observadas según el tipo de deporte:

**9a. Tabla de partidos (futbol)**
Secciones agrupadas por competición, apiladas verticalmente. Cada sección:

- Logo de competición centrado (Champions, LaLiga, Copa del Rey, DAZN + FIFA para Mundial)
- Tab de color con nombre de fase/jornada (ej. "Semifinales Vuelta", "Jornada 35", "Fase de grupos")
- Filas de partido: dia + fecha centrados en bold, hora debajo, escudo/bandera + nombre de equipo a cada lado
- Fondo blanco, bordes redondeados en la card contenedora
- Las pills de fase usan colores de la competición (azul Champions, rojo Copa del Rey, verde Conferencia)

```
┌─────────────────────────────────────┐
│         [Logo Champions]            │
│                                     │
│  ┌─ Semifinales Vuelta ──────────┐  │
│  │      Martes 5 de mayo         │  │
│  │  [Arsenal]  21:00h  [Atletico]│  │
│  │      Miercoles 6 de mayo      │  │
│  │  [Bayern]   21:00h  [PSG]     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌─ La gran final ───────────────┐  │
│  │      Sabado 30 de mayo        │  │
│  │           18:00h              │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

Gold Standards: email-futbol, email-futbol2.

**9b. Programación multi-deporte (motor, golf, tenis)**
Agrupada por categoria deportiva, con etiqueta de categoria a la izquierda:

- Etiqueta de categoria en bold (ej. "Motor", "Golf", "Tenis") como separador lateral o superior
- Cada evento: logos de plataforma + competición (DAZN + MotoGP, DAZN + F1), nombre del evento en bold azul, ubicación/circuito en regular, pill de fecha con fondo verde
- Para golf/tenis: layout más compacto, logo de torneo a la izquierda + rango de fechas a la derecha
- Fondo blanco, sin bordes en las cards individuales (más abierto que la variante futbol)

Gold Standard: email-deportes.

### Bloque 10: Sección "Asi funciona"

Pasos numerados o con icono que explican el funcionamiento de un producto:

- Titulo centrado bold: "Asi Funciona" en negro + nombre del producto en azul `#0066FF` (ej. "Asi Funciona **Movistar Swap**")
- Parrafo introductorio de 1-2 líneas que resume el mecanismo
- 3 pasos verticales, cada uno: icono outline azul (dentro de un cuadrado redondeado gris claro ~48px) + título bold 16px + body regular 14px 1-2 líneas
- Todo sobre card con fondo `#F5F0EB` o `#EFF5FB`, bordes redondeados 12px, padding generoso
- Patron idéntico al componente "3 pasos" de la component library
- Usado en: FTTR, Movistar Swap

**Variante Swap** (la más frecuente, aparece en email-dispositivos2 y email-equipamiento):
```
┌─────────────────────────────────────┐
│  Asi Funciona                       │
│  Movistar Swap  (azul)              │
│                                     │
│  Estrenas tu iPhone, lo disfrutas   │
│  durante 24 meses y puedes volver   │
│  a estrenar el ultimo modelo...     │
│                                     │
│  [ico] Estrenas tu iPhone           │
│        Elige tu nuevo iPhone con    │
│        Swap Movistar                │
│                                     │
│  [ico] Lo disfrutas 24 meses       │
│        Usas tu iPhone con toda      │
│        la tranquilidad de Movistar  │
│                                     │
│  [ico] Vuelves a estrenar           │
│        Puedes renovar al ultimo     │
│        modelo cuando toque          │
└─────────────────────────────────────┘
```

### Bloque 11: Social proof

Observado en 1/11 emails (Prosegur):

- Titulo: "La opinion de nuestros clientes, nuestra mejor garantia"
- Grid 2x2 de badges: Compromiso cliente, Experiencia cliente, Trustpilot estrellas, Google Reviews
- Fondo claro, bordes redondeados

### Bloque 12: Cross-sell

Sección secundaria debajo del contenido principal que promueve un producto complementario:

- Separador visual (línea o cambio de fondo a azul claro)
- Titular: "¿No te llega la fibra?" / "Y además si traes tu contrato de luz..."
- Precio y CTA propios
- Más compacto que el hero principal

### Bloque 12b: Tabla comparativa

Para productos que necesitan justificar su valor frente a la alternativa tradicional (ej. Renting Coches):

- Dos columnas lado a lado con bordes redondeados
- Columna izquierda: "Compra tradicional" con iconos X rojos/grises
- Columna derecha: "Movistar [Producto]" con iconos check azules, borde azul
- 5-6 filas de comparación (ej. "Desembolso inicial" vs "Sin entrada")
- Fondo blanco, bordes `#0066FF` en la columna Movistar

### Bloque 12c: Multi-producto showcase

Para emails que presentan varios productos/servicios del ecosistema Movistar (ej. "Tus ventajas para este verano"):

- Cada producto en su propia sección: foto lifestyle + card de color con titular, subtitulo, body y CTA pill
- Colores de card alternan entre secundarios: verde `#E8F5E9`, mint `#E0F7FA`, beige `#FFFAF5`
- CTA pill outline (borde azul, fondo blanco) en lugar de filled
- 3-4 productos en secuencia vertical
- Sección final con grid 2x2 de iconos de confianza (Ventajas exclusivas, Asesoramiento, Instalación rápida, Confianza Movistar)

### Bloque 12d: Grid de contenido categorizado

Para emails de contenido/entretenimiento (ej. Movistar Plus):

- Titular de categoria sobre fondo de color (amarillo para M+ Vacaciones, etc.)
- Grid de 2-4 thumbnails de posters/portadas debajo del titular
- Categorias separadas: "Cine de estreno", "Series para todos", "Documentales imperdibles", "Contenidos exclusivos"
- Logos de competiciones deportivas en fila al pie si aplica

### Bloque 12e: Video embed

Thumbnail de video con boton play circular. Usado para explicar productos complejos (ej. FTTR). Aparece al final del email, antes del footer:

- Titulo centrado azul: "Asi funciona la Solución FTTR Movistar:"
- Imagen de plano de casa / diagrama técnico
- Boton play circular outline (circulo azul + triangulo)

### Bloque 12f: Opciones de precio lado a lado

Para productos con dos tiers de suscripción (ej. Ficción Total vs Ficción Total con Disney+):

- Dos cards paralelas en fila, mismo alto, fondo azul oscuro o degradado oscuro
- Cada card: logo/icono de plataforma en la cabecera + nombre de producto en bold blanco + descripción breve + precio XXL blanco + duración ("Durante 3 meses") + CTA pill individual
- La card premium puede tener un borde o acento diferenciador (ej. logo Disney+ adicional)
- Ancho: 50/50 del cuerpo del email (~280px cada card en desktop 600px)
- Ambos CTAs usan el mismo texto y estilo (pill azul filled o pill verde)

```
┌──────────────────┐  ┌──────────────────┐
│  [M+ icon]       │  │  [M+ + Disney+]  │
│  Ficción Total   │  │  Ficción Total   │
│                  │  │  con Disney+     │
│  Cine, series... │  │  Una opción para │
│                  │  │  sumar...        │
│  10 €/mes        │  │  14 €/mes        │
│  Durante 3 meses │  │  Durante 3 meses │
│  [Activalo]      │  │  [Activalo]      │
└──────────────────┘  └──────────────────┘
```

Gold Standard: email-ficción.

### Bloque 12g: Proceso visual secuencial con fotografía

Secuencia de etapas de un servicio explicada con fotografias reales y tabs de color. Distinto del Bloque 10 (Asi funciona), que usa iconos y pasos numerados. Este bloque usa fotos full-width por etapa:

- Titulo de concepto en bold centrado (ej. "SuperSeguridad")
- Subtitulo descriptivo 1-2 líneas
- 3 etapas verticales, cada una con:
  - Tab de color con nombre de etapa en bold blanco (colores distintos por etapa: amarillo, azul, naranja)
  - Fotografía full-width debajo del tab mostrando la etapa en acción
  - Chevron/flecha apuntando hacia abajo entre etapas
- Fondo `#FFFAF5`, sin cards contenedoras (las fotos y tabs son los separadores visuales)

```
┌─────────────────────────────────────┐
│       SuperSeguridad                │
│  es la tranquilidad de que no te    │
│  entren, roben, ni ocupen...        │
│                                     │
│  ┌─ Disuadimos ──────────────────┐  │
│  │  [foto: placa de alarma]      │  │
│  └───────────────────────────────┘  │
│              ∨                      │
│  ┌─ Protegemos ──────────────────┐  │
│  │  [foto: equipo vigilancia]    │  │
│  └───────────────────────────────┘  │
│              ∨                      │
│  ┌─ Actuamos ────────────────────┐  │
│  │  [foto: intervención]         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

Gold Standard: email-MPA.

### Bloque 12h: Garantias y compromisos de marca

Sección de sellos/badges de garantia que refuerzan la confianza en un servicio. Distinto del Bloque 11 (social proof con reviews/ratings de terceros). Este bloque muestra compromisos propios de la marca o del partner:

- Titulo centrado en bold: "Y nos comprometemos"
- Fondo azul claro (`#EFF5FB`) o card con bordes redondeados
- 2-4 badges circulares o con forma de sello, dispuestos en fila o grid 2x2
- Cada badge: icono/sello + texto descriptivo debajo (ej. "Garantia Antiocupación", "Garantia Antirrobo")
- Usado en servicios con componente de seguridad o compromiso contractual

Gold Standard: email-MPA.

### Bloque 12i: Specs de pack convergente

Para emails que venden packs combinados (fibra + móvil + TV). Grid compacto que resume las specs del pack:

- Fondo claro (`#EFF5FB`), bordes redondeados 12px
- 2 columnas, cada una con: icono outline azul + título bold azul (ej. "Fibra optica simetrica", "2 líneas móviles incluidas") + 1-2 líneas de detalle en regular
- Debajo, card separada para contenido TV con icono + título bold + parrafo descriptivo con nombres de competiciones/contenidos en bold
- Al pie, fila de "Beneficios incluidos sin coste" con 3 iconos centrados (Movistar Cloud, Protección Digital, Movistar eSim)

```
┌─────────────────────────────────────┐
│  [ico] Fibra optica   [ico] 2 líneas│
│        simetrica            móviles │
│  Router Smart WiFi.   Y hasta 4    │
│  Instalación gratuita.líneas adicionales│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  [ico] Los mejores contenidos       │
│        de television                │
│  Tenis, baloncesto, futbol con      │
│  LALIGA, Champions, Europa League...│
└─────────────────────────────────────┘

  [Cloud]  [Protección Digital]  [eSim]
  Beneficios incluidos sin coste
```

Gold Standard: email-mimovistar-convergente.

### Bloque 12j: Vinculación de cuenta

Sección informativa para usuarios que ya tienen suscripción activa en plataformas OTT (HBO, SkyShowtime, Apple TV, Disney+):

- Card con fondo claro, bordes redondeados, borde superior sutil
- Titulo en bold centrado: "¿Ya tienes una cuenta?"
- Texto explicativo 2-3 líneas: como vincular su cuenta existente para disfrutar la promoción sin perder historial
- Sin CTA propio (la acción ya está cubierta por el CTA principal del email)

Gold Standard: email-ficción.

### Bloque 13: Footer marketing band

Banda de color solido (#0066FF o negro) con texto blanco bold centrado. Funciona como cierre emocional ANTES del footer legal.

Patrones observados:
- "Lo mejor del futbol. Siempre en Movistar"
- "Lo mejor del deporte. Siempre en Movistar"
- "Movistar, la red oficial de nuestra selección"

No todos los emails la usan. Es más comun en emails de contenido/deporte.

### Bloque 14: Canales alternos

Fila horizontal con iconos:
- "miMovistar App" + icono móvil
- "Tiendas Movistar" + icono tienda
- "1004" + icono telefono
- "Entrega gratuita" + "Financiación a tu medida" (en emails de dispositivos)

### Bloque 15: Footer legal

Fondo blanco. Texto muted 12px centrado. Contiene:
- Condiciones de la oferta (2-4 líneas)
- "© Telefónica de Espana S.A.U."
- Links: Aviso legal | Protección de datos | Politica de cookies | Baja de comunicaciones
- Link de unsubscribe siempre presente

---

## Composición por tipo de email

No todos los emails usan todos los bloques. Combinaciones observadas:

| Tipo de email | Bloques que usa |
|---------------|-----------------|
| **Producto hogar** (Fibra, FTTR) | 1 + 2a/2c + 3 + 4 + 5 + 6a + 12 + 5 + 12e + 15 |
| **Deporte futbol** (Champions, Liga, Mundial) | 1 + 2j/2d + 4 + 5 + 9a + 4 + 5 + 13 + 15 |
| **Deporte multi-sport** (Motor, Golf, Tenis) | 1 + 2d + 4 + 5 + 9b + 13 + 15 |
| **Entretenimiento** (Movistar Plus) | 1 + 2i + 4 + 5 + 12d + 13 + 15 |
| **Ficción/OTT** (HBO, SkyShowtime, Apple TV, Disney+) | 1 + 2c + 12f + 12j + 12d + 15 |
| **Dispositivos** (Swap, Ventaja Personal) | 1 + 2b/2h/2g + 5 + 7 + 8 + 10 + 14 + 15 |
| **Dispositivos premium** (iPhone Pro, equipamiento) | 1 + 2h + 5 + 7 + 10 + 14 + 15 |
| **Seguridad/Alarmas** (Prosegur) | 1(co-brand) + 2a + 5 + 12g + 12h + 11 + 5 + 15 |
| **Cross-sell/partner** (Repsol) | 1(co-brand) + 2a + 4 + 5 + 6c + 5 + 15 |
| **Servicio simple** (Prepago, Fibra Adicional) | 1 + 2a + 3 + 4 + 5 + 6b + 12 + 5 + 15 |
| **Value-add/servicio** (Renting Coches) | 1 + 2f + 5 + 6a + 12b + 15 |
| **Multi-producto** (Ventajas Verano) | 1 + 2a + 12c + 14 + 15 |
| **Convergente** (Fibra + móvil + TV) | 1 + 2a(con thumbnails TV) + 5 + 12i + 6b + 15 |
| **Value-add lifestyle** (eSimFLAG) | 1 + 2a + 5 + 10 + 12 + 15 |

---

## Reglas de color en email

- **Fondo dominante**: `#FFFAF5` (Blanco Movistar). Valido en email porque es canal offline.
- **Secciones alternas**: `#EFF5FB` (azul muy claro) o `#D3EEFF` para énfasis.
- **Cards beneficios**: fondo `#EFF5FB` o beige claro `#F5F0EB`.
- **Dark hero**: para productos tech/premium (FTTR). Negro puro con graficos/líneas neon.
- **Black hero**: para dispositivos premium (iPhone Pro). Negro puro como escaparate de lujo, iluminación dramatica sobre el producto. Distinto del dark hero.
- **Navy sport hero**: `#001A33` a `#0A1628`. Fotografía deportiva a sangre. Exclusivo de emails de deporte/futbol.
- **Warm hero**: amarillo/dorado (`#F5D060` a `#FFD700`). Thumbnails de contenido integrados. Exclusivo de entretenimiento estacional (M+ Vacaciones).
- **Blue hero** `#0066FF`: para value-add/servicios (Renting Coches). Texto blanco. Keyword destacada en dorado/amarillo.
- **Footer band**: `#0066FF` o negro.
- **Acento verde**: `#00C48C` solo para Swap/renovación.
- **Co-branding**: el color del partner puede aparecer en su sección específica, nunca dominar el email.

---

## Tipografia en email

- **Titular hero**: ExtraBold 28-36px, sentence case, negro `#262423`. Una palabra clave puede ir en azul `#0066FF` o italic para énfasis.
- **Subtitular sección**: Bold 20-24px, azul o negro.
- **Body**: Regular 14-16px, `#262423` o `#6F7176` (muted).
- **Overline**: "Por ser cliente" / "Ser cliente tiene ventajas" en azul, 12-14px.
- **Precio XXL**: ExtraBold 48-72px.
- **Legal**: 12px, `#6F7176`.
- **Italic selectivo**: se permite en una palabra del titular para énfasis emocional ("precio *imbatible*", "*Superseguridad*"). No abusar: máximo una palabra por titular.

---

## Reglas de copy en email

- **Asunto:** máximo 50 caracteres. Directo, sin hype. Ejemplo bueno: "Tu Fibra Adicional desde 15 eur/mes". Ejemplo malo: "¡No te pierdas esto!".
- **Pre-header:** complementa el asunto, no lo repite. Máximo 90 caracteres.
- **Titular hero:** sentence case, máximo 6-7 palabras, una keyword destacada.
- **CTA primario:** primera persona ("Quiero mi...") o imperativo ("Activa...", "Descubre..."). Siempre con beneficio concreto.
- **Repetición de CTA:** en emails >1500px, repetir el CTA idéntico cerca del footer.
- **Personalización:** nombre del cliente en saludo ("Hola Carlos,") cuando este disponible.
- **Sin em dashes** en todo el copy.

---

## Co-branding en email

Patrones observados con 3 partners distintos:

- **Header**: lockup conjunto (M + partner logo)
- **Sección partner**: card o zona con logo del partner, precio/oferta del partner, colores del partner limitados a esa zona
- **CTA**: puede usar el color del partner si el email es 100% de co-branding. Si es un email Movistar con mención al partner, CTA sigue en azul `#0066FF`.
- **Logos de competición** (DAZN, F1, MotoGP): se muestran como badges pequenos dentro de event cards, no en el header.

---

## Accesibilidad en email

- `alt` en todas las imagenes, incluso las decorativas (`alt=""`).
- Contraste mínimo AA para todo el texto.
- No depender del color para transmitir información.
- Modo oscuro: `@media (prefers-color-scheme: dark)` para fondos e invertir logo M.
- Botones CTA con tamaño mínimo tactil 44x44px.

---

## Checklist antes de entregar

- [ ] Header con M logo top-right (o lockup co-brand si aplica)
- [ ] Hero tiene fotografía real o producto real, no stock genérico ni IA visible
- [ ] Precio XXL presente si la campaña lo requiere
- [ ] CTA primario: pill azul filled, texto accionable y específico
- [ ] CTA repetido si el email supera ~1500px de alto
- [ ] Máximo un color secundario dominante por email (excepción: grid de beneficios puede usar uno por card)
- [ ] Badge "Ser cliente tiene ventajas" si el email es para clientes existentes
- [ ] Bloques modulares en orden lógico (hero -> precio -> CTA -> beneficios -> cross-sell -> CTA -> legal)
- [ ] Footer legal con unsubscribe link
- [ ] Sin em dashes en el copy
- [ ] Ortografia castellana correcta (tildes, ene, signos de apertura)
