---
name: movistar-visual-production
description: Stack de produccion visual del Art Director (D) para piezas Movistar presentables a cliente. Assets de marca como archivos (fuentes, logos, tokens), fotografia real via OpenAI (gpt-image-2), ensamblado programatico por slots, y bucle de verificacion visual con render. Sustituye a visual-01-brand-assets, visual-02-brand-typography y el enfoque base64 de visual-03.
version: 1.0.0
owner: superreal
status: active
loaded_by: D (Art Director)
requires_env:
  - OPENAI_API_KEY
---

# Movistar Visual Production

Esta skill convierte la Estrategia Creativa en piezas finales presentables a cliente. Regla central: **el modelo nunca genera base64 ni copia assets a mano**. Escribe HTML con slots, y los scripts ensamblan, generan fotografia y renderizan.

## Estructura del bundle

```
brand/
├── fonts/            Movistar Sans woff2 (10 variantes)
├── logos/            mark, mark-inverse, mark-dark, lockups, wordmarks (SVG)
├── tokens/           colors.css, spacing.css, typography.css, tokens.json
└── audit-report.md   Composicion por formato destilada de 41 piezas reales. LEER SIEMPRE.
references/
├── INDEX.md          Catalogo de piezas reales por formato
└── pieces/           Las 41 creatividades reales (imagenes que puedes Read)
guidelines/
├── app-email.md      Plantilla email observada en piezas reales (9 bloques)
├── app-ads.md        Geometrias OOH y display con layouts ASCII
├── app-web.md        Landing de campana vs web generica
├── magic-prompt.md   Como escribir prompts de fotografia de marca
└── mockup-workflow.md  Cuando y como componer mockups contextuales
templates/
├── html/             Plantillas slot-based por formato
└── mockups/          Entornos + corners.json para el composer
scripts/
├── assemble.py       Rellena slots (fuentes, logos, tokens, imagenes)
├── generate_image.py Fotografia via OpenAI (OPENAI_API_KEY, gpt-image-2)
├── render.py         HTML a PNG para verificacion visual
└── mockup_composer.py  Incrusta la pieza en un entorno real
```

## Workflow por pieza (obligatorio, en este orden)

### 1. Referencias antes de disenar
Lee 2-3 piezas reales del formato en `references/pieces/` (usa `references/INDEX.md` para elegirlas) y el bloque del formato en `brand/audit-report.md`. Son ground truth: mas fiables que cualquier regla escrita.

### 2. Construir el HTML con slots
Parte de la plantilla del formato en `templates/html/` si existe; si no, construye HTML de dimensiones fijas siguiendo el patron del audit-report. Reglas duras:

- Tipografia: escribe `{{FONT_FACE_MIN}}` (o `{{FONT_FACE}}` si necesitas italicas o pesos 300/500). NUNCA escribas un @font-face con base64.
- Tokens: escribe `{{TOKENS_CSS}}` y usa las variables. Paleta cerrada: cualquier HEX fuera de tokens es error.
- Logos: usa los slots `{{LOGO_MARK}}`, `{{LOGO_MARK_INVERSE}}`, `{{LOGO_LOCKUP}}`, etc. NUNCA dibujes la M ni copies un SVG a mano. Variante inverse sobre fondo oscuro o azul.
- Fotografia: escribe `{{IMG:outputs/<slug>-<zona>.png}}` con un atributo `data-prompt` describiendo la foto.
- Emails: sin slots de fuente (ensambla con `--no-font`); HEX directos de la paleta; tablas.
- Formatos ex-SVG (social, tienda, exterior, M+): produce HTML de dimensiones fijas y entrega el PNG renderizado. Solo produce SVG si piden vector editable.

### 3. Generar la fotografia
Por cada `{{IMG:...}}`: escribe el prompt siguiendo `guidelines/magic-prompt.md` (4-5 frases cinematograficas en ingles, realismo editorial, universo Movistar) y ejecuta:

```bash
python3 scripts/generate_image.py -p "<prompt>" -o outputs/<slug>-<zona>.png --aspect <ratio>
```

Si la API no esta disponible, usa como stand-in un crop coherente de `references/pieces/` y flaggea `imagen_provisional`.

### 4. Ensamblar

```bash
python3 scripts/assemble.py -i pieza.slots.html -o outputs/pieza.html          # normal
python3 scripts/assemble.py -i email.slots.html -o outputs/email.html --no-font  # email
```

Si el script avisa de slots sin resolver, corrige antes de seguir.

### 5. Verificacion visual (el paso que separa mockup de pieza final)

```bash
python3 scripts/render.py -i outputs/pieza.html -o outputs/pieza.png --width <W> --height <H>
```

MIRA el PNG (herramienta Read) y evalua contra esta checklist:

1. Las 5 non-negotiables: azul #0066FF presente; fondo #FFFAF5 (nunca blanco puro); max un secundario; solo Movistar Sans; sentence case y CTAs especificos sin exclamacion.
2. El patron del formato en audit-report (jerarquia, posicion de la M, estructura).
3. Nada solapado, cortado ni desbordado; legibilidad a la distancia del soporte.
4. La foto integra: luz creible, personas reales, sin look CGI.
5. Test de parecido: puesta junto a las referencias reales, encaja como una mas.

Si algo falla, corrige el HTML y repite ensamblado + render. Maximo 2 iteraciones; si a la segunda no pasa, entrega con flag `qa_visual_fallido` y detalle.

### 6. Mockup contextual (si es para presentar a cliente)
Sigue `guidelines/mockup-workflow.md`: pieza plana en PNG + template de `templates/mockups/` + `scripts/mockup_composer.py`. Si no hay template del formato, genera el entorno con `generate_image.py` (prompt de entorno vacio, sin branding), anota las esquinas en `.corners.json` y guardalo en la subcarpeta para reutilizar.

## Entregables por pieza

- `outputs/<pieza>.html` ensamblado (autocontenido) o `.slots.html` + assets si piden editable
- `outputs/<pieza>.png` render verificado
- Mockup contextual si aplica
- Entrada en el design rationale con el resultado del QA visual

## Anti-patrones

- Escribir base64 a mano (fuentes, logos, imagenes): NUNCA. Es la causa historica de tipografia rota.
- Placeholder dashed en una entrega final: solo se admite con flag `imagen_provisional` y motivo.
- SVG a mano alzada con coordenadas para formatos fotograficos: usar HTML fijo + render.
- Entregar sin haber mirado el render: prohibido.
- Inventar HEX o tokens: si falta un valor, TODO + flag.
