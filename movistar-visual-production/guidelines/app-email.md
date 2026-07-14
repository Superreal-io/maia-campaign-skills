# Aplicación : Email

Versión enriquecida con los patrones reales observados en las piezas de referencia (ver `../reference-pieces/INDEX.md`, sección Email, y `../audit-report.md` §1).

---

## Especificaciones técnicas

| Propiedad | Valor |
|-----------|-------|
| Ancho del layout | 600px |
| Fondo del email (wrapper) | `#F5F5F5` (gris muy claro para contraste con el cuerpo) |
| Fondo del cuerpo | `#FFFAF5` (Blanco Movistar) |
| Tipografía | `"Helvetica Neue", Helvetica, Arial, sans-serif` (Movistar Sans no se garantiza en todos los clientes) |
| Fuente body | 16px / Regular |
| Fuente small / legal | 12px / Light (300 → 400 en email) |
| Ancho máximo de imagen | 600px (100% del layout) |
| Espaciado entre secciones | 32px vertical (más denso que en web) |

---

## Estructura estándar Movistar (patrón observado)

Todos los emails de campaña siguen esta secuencia. **No inventes bloques nuevos; usa esta plantilla.**

```
1. PREHEADER          Texto minúsculo centrado sobre fondo gris claro.
                      "Si no puedes ver este email, haz clic aquí".
                      12px, color muted.

2. HEADER             Fondo Blanco Movistar. 60-72px de alto.
                      Izquierda: lockup horizontal (logo M + wordmark azul).
                      Derecha: "Accede a miMovistar" con icono de perfil azul.
                      Link, no botón.

3. HERO               Imagen de fondo full-width (fotografía real) o color pleno.
                      Titular superpuesto: Movistar Sans Bold 28-32px.
                      Subtítulo Regular 16px, 2-3 líneas máximo.
                      CTA pill azul filled centrado bajo el copy.
                      Cursiva azul aceptable en una palabra clave del titular
                      (ej. "Tus ventajas Movistar *para este verano*").

4. INTRO A VENTAJAS   Titular breve centrado azul: "Disfruta de más ventajas
                      ser cliente Movistar" (Bold 20px).
                      La palabra "ventajas" a veces en secundario destacado.

5. 3 VENTAJAS         Grid de 3 cards paralelas (o 2 filas de 2 en mobile).
                      Cada card:
                      - Chip circular 48px con icono en azul-claro/azul.
                      - Título Bold 16px (azul o color secundario emparejado).
                      - Body 14px Regular, 3-4 líneas.
                      - Imagen 4:3 debajo del texto (fotografía real).
                      - CTA outline pill: "Ver [beneficio]".
                      Cada card puede usar un secundario distinto
                      (excepción a la regla "un secundario por pieza":
                      aquí se trata como serie interna).

6. TRUST STRIP        Franja azul-claro `#D3EEFF`, 4 columnas.
                      Cada columna: icono outline azul 20px + 2 líneas de copy 12px.
                      Contenido tipo: "Ventajas exclusivas", "Te asesoramos",
                      "Instalación rápida", "Confianza Movistar".

7. CTA PANEL FINAL    Card ancho fondo blanco con imagen a la derecha
                      y copy + CTA a la izquierda.
                      Titular "Este verano, estés donde estés,
                      Movistar va contigo." (Bold 20px azul).
                      CTA pill azul filled.

8. CANALES ALTERNOS   Línea horizontal debajo del CTA panel.
                      Icono + texto en fila:
                      "miMovistar App", "Tiendas Movistar", "1004".
                      Cada uno con icono azul pequeño 16px.

9. FOOTER LEGAL       Fondo blanco, texto muted 12px centrado.
                      "© Telefónica de España S.A.U. Todos los derechos reservados."
                      Línea de links: "Aviso legal | Protección de datos |
                      Política de cookies | Baja de comunicaciones".
```

Referencia visual: `../reference-pieces/INDEX.md` → sección Email (email.png, email2-5.png).

---

## Tipos de email y variaciones

El patrón anterior es el molde de **email de campaña**. Ajustes por tipo:

| Tipo | Cambios respecto al patrón |
|------|---------------------------|
| Bienvenida | Hero más grande. Sin ventajas 3-up. CTA único potente. |
| Campaña producto | Patrón completo. Precio protagonista en hero si aplica. |
| Transaccional (factura, alerta) | Header + cuerpo texto + footer legal. Sin marketing, sin CTAs promocionales. |
| Newsletter | Sustituir 3 ventajas por 3 artículos con thumbnail + título + resumen + "Leer más". |
| Incidencia / aviso | Añadir franja amarillo `#FFE99C` bajo el header con icono alerta + copy. |

---

## Botón CTA principal (código listo)

```html
<a href="[URL]" style="
  display: inline-block;
  padding: 12px 32px;
  background-color: #0066FF;
  color: #FFFAF5;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none;
  border-radius: 9999px;
  letter-spacing: 0.01em;
">Ver mis ventajas de verano</a>
```

**CTA secundario en card de ventaja:**

```html
<a href="[URL]" style="
  display: inline-block;
  padding: 10px 20px;
  background-color: transparent;
  color: #0066FF;
  border: 1px solid #0066FF;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border-radius: 9999px;
">Ver Fibra Adicional</a>
```

---

## Reglas de copy en email

- **Asunto:** máximo 50 caracteres. Directo, sin hype. Ejemplo bueno: "Tus ventajas Movistar para este verano". Ejemplo malo: "¡No te pierdas esto!".
- **Pre-header:** complementa el asunto, no lo repite. Máximo 90 caracteres.
- **Titular hero:** sentence case, máximo 6-7 palabras.
- **Cards de ventaja:** título 2-3 palabras (nombre del producto), body promesa concreta con número o nombre.
- **CTA principal:** verbo imperativo + beneficio concreto ("Ver mis ventajas de verano", no "Descubre más").
- **CTAs secundarios:** "Ver [producto]" es el patrón dominante.
- **Emails transaccionales:** cero marketing.
- **Personalización:** cuando la haya, va en el hero como saludo aparte ("Hola Carlos,") o embebida en el copy.
- **Footer legal:** unsubscribe link siempre presente. Dirección postal de Telefónica. Política de privacidad.

---

## Accesibilidad en email

- `alt` en todas las imágenes, incluso las decorativas (`alt=""`).
- Contraste mínimo AA para todo el texto.
- No depender del color para transmitir información.
- Modo oscuro: usar `@media (prefers-color-scheme: dark)` para ajustar fondos, invertir logo M al lockup-inverse.
- El chip azul-claro de icono debe seguir siendo legible en dark mode (usa `#D3EEFF` con icono `#0066FF`, no invertir).

---

## Checklist antes de enviar

- [ ] Header lleva lockup horizontal + "Accede a miMovistar" a la derecha.
- [ ] Hero tiene fotografía real, no stock ni IA visible.
- [ ] Un solo secundario dominante por email (excepto en las 3 ventajas donde cada card puede usar uno).
- [ ] CTA principal es único y específico.
- [ ] Trust strip presente en emails de campaña.
- [ ] Canales alternos visibles (App, Tiendas, 1004).
- [ ] Legal + baja de comunicaciones en el footer.
- [ ] Sin em dashes en el copy.
