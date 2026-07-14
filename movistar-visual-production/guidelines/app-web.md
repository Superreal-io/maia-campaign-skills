# Aplicación : Web y Landing Pages

Versión enriquecida con los patrones reales observados en las piezas (ver `../reference-pieces/INDEX.md` sección Landing web; y `../audit-report.md` §1).

---

## Dos modos: web genérica vs. landing de campaña

La skill produce dos cosas distintas y con patrones distintos:

- **Web genérica** (home, corporativa, sección producto sin CTA de compra): estructura amplia, sin personalización, layout de página completa.
- **Landing de campaña** (fibra, verano, Swap, oferta específica): estructura densa, personalización, precio protagonista, segmentación por perfil.

Ambos comparten los tokens y componentes; cambia la estructura y la densidad. **Pregunta al usuario cuál necesita antes de generar.**

---

## Estructura de web genérica

```
Nav (sticky, logo M top-right)
↓
Hero (contenedor conectado, variante blue o white)
↓
Sección de características (grid 3-4 col, feature-cards con chip de icono)
↓
Sección de stats (4 números clave con CountUp)
↓
Sección de productos / tarifas (cards con precio protagonista)
↓
Testimonial / caso de éxito
↓
CTA de cierre (banda azul con botón pill blanco)
↓
Footer (logo M bottom-right, links, legal)
```

---

## Estructura de landing de campaña (patrón observado)

Referencia: `landing.png`, `landing2.png`, `landing-mov.png`.

```
1. HEADER SIMPLIFICADO
   Logo lockup horizontal top-left.
   Saludo personalizado top-right: "Hola Carlos,".
   Sin nav completa. Máximo 1-2 links (miMovistar, cobertura).

2. HERO CON PRECIO PROTAGONISTA
   Layout 60/40 o 50/50 (copy izquierda, imagen derecha).
   
   IZQUIERDA:
   - Overline mayúscula tracked azul: "SER CLIENTE TIENE VENTAJAS" (12px, letter-spacing 0.1em)
   - Titular Bold 40-48px, sentence case, 2-3 líneas, azul o negro.
   - Bloque de precio dentro de card azul filled:
       "19,90€ /mes" : número XXL 64px blanco Extrabold + € 32px + /mes 16px
       sub-linea "Precio especial clientes miMovistar" azul-claro `#D3EEFF`
   - Body 16px con contexto (2-3 líneas).
   - CTA pill azul filled: "Ver [producto]".
   - Legal 12px muted: "Sujeto a cobertura y condiciones de contratación."
   
   DERECHA:
   - Imagen full-bleed (fotografía real, escena del producto en contexto).
   - Chip flotante azul-oscuro `#022D67` en esquina superior derecha:
     "Fibra Adicional / Para tu segunda residencia" (badge circular grande).
   - Chip de acción abajo derecha: "Comprueba tu cobertura en tu casa de verano →"
     (fondo blanco, borde suave, icono ubicación azul).

3. BENEFICIOS 3-UP HORIZONTAL
   Fila de 3 iconos + título + body. Sin cards, texto sobre fondo blanco.
   Icono azul en chip circular 48px, título Bold 16px, body 14px 2-3 líneas.
   Ejemplos: "Internet donde lo necesitas", "Activación sencilla", "Precio especial cliente".

4. SEGMENTACIÓN POR PERFIL
   Título centrado azul mayúscula tracked: "EL MENSAJE PARA TI" (12px).
   Dos cards paralelas 50/50:
   
   CARD 1: fondo azul-claro `#D3EEFF`, badge "CON FÚTBOL" en pill azul.
   Icono grande (pelota), titular Bold 20px, body 14px.
   
   CARD 2: fondo verde-claro `#CEF7BF`, badge "SIN FÚTBOL" en pill verde.
   Icono grande (sol), titular Bold 20px, body 14px.
   
   Esta segmentación es UNA excepción documentada a "un secundario por pieza":
   las dos cards funcionan como pareja binaria, no como serie de colores.

5. TOGGLE / INTERACCIÓN REAL
   Card ancho con toggle visible (no decorativo):
   Icono a la izquierda ("ON/OFF"), copy en centro, switch a la derecha.
   El switch es real (verde cuando ON), no mockup.
   Copy: "Úsala cuando la necesitas / Actívala cuando vayas a tu segunda residencia."

6. CTA PANEL FINAL
   Card ancho fondo azul-claro `#D3EEFF`.
   Icono a la izquierda (hucha, casa, según producto).
   Copy centrado: overline "Ser cliente tiene ventajas" + titular Bold + body con precio.
   CTA pill azul filled a la derecha: "Ver [producto]".

7. LEGAL EXTENSO
   Fondo blanco, texto muted 12px, 4-6 líneas.
   Condiciones completas de la oferta.
   Enlace a "movistar.es" para condiciones completas.

8. FOOTER MINIMAL
   4 links en fila con icono: "Gestionar preferencias", "Darse de baja", 
   "Privacidad", opcionalmente "Aviso legal".
   Sin logo, sin big footer (no es la home).
```

---

## Layout y grid

- **Web genérica:** max-width 1280px, padding lateral 40px desktop / 16px mobile, gap secciones 64px.
- **Landing:** max-width 1120px (más estrecho), padding lateral 40px, gap secciones 48px (más denso).
- Columnas: 12 desktop / 4 mobile.
- Gutter: 24px.

---

## Componentes por sección

| Sección | Componente | Variante recomendada |
|---------|-----------|---------------------|
| Nav | `Nav` | sticky, blanco translúcido con backdrop-blur |
| Hero web | `Hero` | blue (fondo blanco, contenedor azul) |
| Hero landing | Custom con `Card` blue filled + imagen | Ver patrón §Hero con precio protagonista |
| Features | `FeatureCard` + grid | accent blue o verde según contexto |
| Segmentación landing | Dos `Card` con badge `Badge` | azul-claro + verde-claro |
| Stats | `StatGrid` | - |
| Precios | `Card` con precio | Ver composición de precios en `../audit-report.md` §2 |
| Testimonial | `Testimonial` | Con outcome en contenedor azul claro |
| CTA | `CtaSection` | variant="blue" |
| Toggle | Custom con `input[type=checkbox]` estilizado | verde ON, gris OFF |

---

## Reglas de color por sección

- **Web genérica**: secciones impares fondo Blanco Movistar `#FFFAF5`. Secciones pares fondo Azul Movistar `#0066FF` o secundario claro.
- **Landing**: fondo dominante Blanco Movistar. Bloques de énfasis en azul filled (precio, CTA panel final). Segmentación usa DOS secundarios (excepción binaria).
- **Máximo un secundario por página**, excepto en la sección de segmentación de landing donde la dualidad es intencional.

---

## Tipografía web y landing

- **Body:** Movistar Sans Regular, 16px, line-height 1.5.
- **Máximo ancho de lectura:** 680px (`--container-prose`).
- **Titulares:** siempre sentence case. Tracking negativo en Display y H1 (-0.02 a -0.03em).
- **Overlines:** MAYÚSCULA tracked (letter-spacing 0.1em), color azul o secundario oscuro, 12px, máximo 3 palabras.
- **Precio:** Extrabold, tracking cero, número XXL con € y /mes en cuerpo pequeño.
- **Saludo personalizado ("Hola Carlos,"):** Regular 14px, muted, no destacado.

---

## Personalización

Datos personalizables en landing (por variable):

- Nombre del cliente: "Hola {nombre},"
- Nombre del pack: "en tu pack {plan}"
- Precio del cliente: "{precio_personalizado} €/mes"
- Ciudad o segunda residencia si la conocemos.

Cuando no hay datos personalizados disponibles, quitar el saludo y usar copy genérico ("Bienvenido," o simplemente empezar por el titular).

---

## Rendimiento

- Movistar Sans se sirve como woff2 desde `assets/fonts/`, no CDN externa.
- `font-display: swap` para fallback mientras carga.
- Imágenes en `webp` con fallback `jpg`. Lazy-load por defecto.
- No cargar librerías de iconos completas. Importar sólo los iconos necesarios de Lucide.
- LCP objetivo < 2.5s en landing de campaña.

---

## SEO / meta

- **OG image**: 1200×630px. Estructura: fondo Azul Movistar + titular en Blanco + logo M top-right. Reutilizar el patrón del hero.
- **Meta description**: máximo 160 caracteres, sentence case, sin hype. "Fibra de 1 Gb desde 29,90 €/mes con permanencia de 12 meses." : no "¡La mejor conexión al mejor precio!".
- **Canonical** siempre presente en landing pages de campaña.
- **Structured data (JSON-LD)**: `Product` schema con `offers` en landing de tarifa.

---

## Checklist landing antes de publicar

- [ ] Header simplificado, saludo personalizado en su sitio.
- [ ] Hero con precio protagonista en bloque azul filled.
- [ ] Overline mayúscula tracked azul en su sitio.
- [ ] Segmentación por perfil si aplica al producto (2 cards paralelas).
- [ ] Toggle o elemento interactivo si el producto lo requiere (activación remota, aviso).
- [ ] CTA panel final con imagen o icono + resumen de oferta.
- [ ] Legal completo antes del footer.
- [ ] Footer minimal (no big footer).
- [ ] Sin em dashes en copy.
- [ ] Todas las promesas tienen número o nombre concreto.
