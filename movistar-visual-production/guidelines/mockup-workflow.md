# Mockup workflow: piezas en contexto

Guía interna para la skill. Cuándo montar una pieza dentro de un entorno real y cómo hacerlo.

## Cuándo aplicar mockup contextual

**Sí, siempre que:**
- El usuario pida "un mupi", "una valla", "una lona", "un cartel en tienda", "un cartel en escaparate".
- El usuario pida "un email para clientes" y quiera verlo dentro de una bandeja / móvil.
- El usuario pida "una landing" y quiera verla en un navegador o móvil.
- El brief mencione "presentación a cliente", "propuesta creativa", "cómo se vería" (implica querer el mockup).

**No, si:**
- El usuario quiere el archivo maestro plano para producción (imprenta, agencia externa).
- Está iterando sobre la creatividad y quiere ver cambios rápido (el mockup añade tiempo).
- Es una pieza puramente digital sin analogía física (widget interno, dashboard).

Regla de oro: **si es para persuadir, va con mockup. Si es para producir, va plano.** En duda, ofrece las dos.

## Flujo estándar (2 pasos)

### Paso 1: generar la pieza plana
Sigue las reglas del design system y las referencias en `../reference-pieces/INDEX.md` del formato pedido. Salida: PNG rectangular con la creatividad final.

### Paso 2: incrustar en template
1. Elegir template. Ver `../mockup-templates/` y las subcarpetas por tipo. Si el usuario no especifica, elige el más natural para el formato:
   - MUPI → `exterior/marquesina-*.png`
   - Valla/lona → `exterior/lona-*.png` o `exterior/valla-*.png`
   - Cartel A3 → `exterior/wild-posting-muro.png` o `print/cartel-a3-pared.png`
   - Email → `email/inbox-iphone.png` o `email/inbox-desktop-mail.png`
   - Landing → `digital/macbook-browser.png` o `digital/iphone-portrait.png`
   - Display → `digital/desktop-monitor.png`
   - Cartel tienda → `print/chevalet-tienda.png` o `print/rollup-tienda.png`
   - Escaparate → `exterior/escaparate-tienda.png`

2. Correr el script (desde la raíz del skill o el pack):
   ```bash
   python MOV_Skill_Extension/scripts/mockup_composer.py \
     -c out/creativa.png \
     -t MOV_Skill_Extension/mockup-templates/exterior/marquesina-gran-via.png \
     -o out/mupi-final.png
   ```
   El script lee automáticamente `marquesina-gran-via.corners.json` si está al lado del template.

3. Entregar tanto el plano (`creativa.png`) como el contextual (`mupi-final.png`). El usuario decide cuál usar.

## Flujo alto realismo (opcional, para presentación cliente)

Cuando el resultado del paso 2 no basta (iluminación compleja, reflejos, sombras del entorno) y hay tiempo:

1. Genera el mockup con el script como base.
2. Pasa la salida por un modelo de imagen (Nano Banana, Imagen) con prompt de refinamiento:
   *"Preserve the poster content and its position exactly. Match the scene lighting: add cast shadows, reflections on the glass frame, subtle ambient light integration. Do not alter the poster typography or colors."*
3. Comparar con la base. Aceptar sólo si mejora sin distorsionar textos ni logos.

**Riesgo**: los modelos de imagen a veces "reescriben" el titular o desplazan la M expresiva. Verifica letra por letra antes de entregar.

## Reglas de integración visual

- **Ilumación coherente**: si el template es nocturno (mupi Gran Vía), aplica sombras cálidas de sodio. Si es diurno, sombra fría suave.
- **Sombra proyectada** al suelo o pared cuando la pieza está en soporte físico (mupi, chevalet). El campo `shadow_opacity` en el JSON de esquinas lo activa.
- **Reflejos** en cristal (marquesina, escaparate, pantalla iPhone) son deseables pero difíciles con PIL; delegar al flujo de alto realismo.
- **Escala del logo**: la M expresiva en la pieza plana debe verse legible tras el warp. Si el template comprime mucho la esquina donde va la M, generar la creativa con la M algo más grande de lo normal.
- **Textos legales**: si el mockup queda a media distancia (mupi, lona), el legal pequeño se pierde. Está bien; el mockup es para persuadir, no para leer.

## Fallback si no hay template disponible

Si el formato pedido no tiene template en `mockup-templates/`:

1. Ofrecer al usuario el plano como entrega.
2. Sugerir generar un entorno con IA:
   *"Photorealistic front view of an empty [MUPI vertical / bus stop marquee / A3 poster wall / MacBook Pro], neutral lighting, no branding, high resolution."*
3. Guardarlo en la subcarpeta correspondiente. Anotar las esquinas.
4. Componer.

## Nomenclatura de salida

Convención: `{formato}-{campaign-slug}-{variant}.png`

Ejemplos:
- `mupi-swap-madrid.png` (mupi de Swap en Madrid)
- `email-verano-desktop.png` (email verano en desktop)
- `landing-fibra-mobile.png` (landing fibra en móvil)

Así el usuario reconoce qué es cada archivo sin abrirlo.
