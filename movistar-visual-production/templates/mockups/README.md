# Mockup templates

Fondos base para componer piezas planas dentro de un entorno real. La skill genera la creatividad, luego el script `scripts/mockup_composer.py` la incrusta sobre el template con transformación de perspectiva.

## Estructura esperada

Cada template es un PNG del entorno **sin la creatividad**, más un JSON gemelo (`.corners.json`) que define las 4 esquinas del hueco donde va la pieza. El JSON permite al script deformar la creatividad para que encaje perfecta con la perspectiva del entorno.

```
mockup-templates/
├── exterior/
│   ├── marquesina-gran-via.png
│   ├── marquesina-gran-via.corners.json
│   ├── valla-fachada.png
│   ├── valla-fachada.corners.json
│   ├── lona-edificio.png
│   ├── lona-edificio.corners.json
│   ├── wild-posting-muro.png
│   ├── wild-posting-muro.corners.json
│   └── escaparate-tienda.png
│       escaparate-tienda.corners.json
├── digital/
│   ├── iphone-portrait.png
│   ├── iphone-portrait.corners.json
│   ├── macbook-browser.png
│   ├── macbook-browser.corners.json
│   ├── ipad-portrait.png
│   ├── ipad-portrait.corners.json
│   └── desktop-monitor.png
│       desktop-monitor.corners.json
├── email/
│   ├── inbox-iphone.png
│   ├── inbox-iphone.corners.json
│   ├── inbox-desktop-mail.png
│   └── inbox-desktop-mail.corners.json
└── print/
    ├── cartel-a3-pared.png
    ├── cartel-a3-pared.corners.json
    ├── rollup-tienda.png
    ├── rollup-tienda.corners.json
    ├── chevalet-tienda.png
    └── chevalet-tienda.corners.json
```

## Formato del JSON de esquinas

```json
{
  "template": "marquesina-gran-via.png",
  "corners": {
    "top_left":     [612, 68],
    "top_right":    [948, 74],
    "bottom_right": [943, 597],
    "bottom_left":  [617, 592]
  },
  "shadow_opacity": 0.15,
  "notes": "MUPI vertical A0. Ambient luz noche cálida. Pieza va con ligera sombra proyectada al suelo."
}
```

- **corners**: coordenadas en píxeles sobre el PNG del template. Orden: top-left, top-right, bottom-right, bottom-left. El script hace warp con esas 4 esquinas.
- **shadow_opacity**: opcional. Aplica una sombra sutil al borde del inserto para integrarlo con la iluminación del entorno.
- **notes**: contexto para el operador humano y para la skill (ej. "esta plantilla es vertical A0, no metas creatividad horizontal").

## Cómo conseguir los templates iniciales

Tres vías. Ninguna es única, se combinan:

### Vía 1: Limpiar las piezas del backup con IA
Varios PNGs del `MOVISTAR creatividades backup/` ya son mockups contextuales (mupi, exterior, lona, Carteles). Se pueden reciclar:

1. Subir la pieza a un modelo de imagen (Nano Banana, Imagen, Midjourney describe+edit).
2. Prompt: *"Remove the poster content, keep the environment intact. Fill the poster area with a neutral flat surface, matching lighting of the scene."*
3. Guardar el limpio en la subcarpeta correspondiente.
4. Abrir en cualquier editor de imagen y anotar las 4 esquinas del hueco. Volcarlas al `.corners.json`.

Ver `../audit-report.md` sección 3 para el mapeo de qué archivo del backup se convierte en qué template.

### Vía 2: Descargar mockups libres y limpiarlos
Freepik / Mockup World tienen mockups gratis (MUPI, valla, iPhone). Se descarga, se elimina el placeholder, se anotan las esquinas.

### Vía 3: Generar entornos con IA
Prompt tipo *"empty subway station marquee, front view, natural morning light, no advertisement, photorealistic, 4k"* devuelve un entorno virgen listo para usar.

**Recomendación**: empieza por vía 1 con los 9 templates ya identificados en el audit. Es 90% del uso real y no requiere licencias.

## Naming convention

- kebab-case, sin espacios.
- Prefijo por tipo si aplica (`marquesina-`, `valla-`, `iphone-`, `macbook-`, `cartel-a3-`).
- Ciudad o contexto sólo si es relevante (`marquesina-gran-via` vs `marquesina-generica`).
