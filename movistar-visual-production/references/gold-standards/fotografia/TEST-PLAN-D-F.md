# Test Plan: Paso D (Dominancia) + Paso F (Con/Sin Track A)

> Documento listo para ejecutar en Paperclip.
> Coste estimado total: ~3 EUR (9 generaciones gpt-image-2 quality medium).
> Tiempo estimado: ~30 min.

---

## PASO D: A/B de orden de dominancia

### Objetivo

Cuando el Art Director pasa dos `--ref` (ancla + escena), el modelo da mas peso a la primera.
Este test genera la misma foto 2 veces cambiando el orden para decidir una regla fija.

**Resultado esperado:** una regla tipo "siempre ancla primero" o "siempre escena primero" que se documenta en SKILL.md.

### Familias seleccionadas

| # | Familia | Ancla | Escena |
|---|---|---|---|
| D1 | interior-domestico | `_anclas/ancla-interior-luz-calida.jpg` | `interior-domestico/foto-pareja-cocinando-noche.jpg` |
| D2 | exterior-urbano | `_anclas/ancla-exterior-luz-natural.jpg` | `exterior-urbano/foto-grupo-terraza-pueblo-blanco.jpg` |
| D3 | producto-en-mano | `_anclas/ancla-producto-en-mano.jpg` | `producto-en-mano/foto-tablet-regazo-tren.jpg` |

### Prompts para Paperclip

Ruta base de refs: `Skills/movistar-visual-production/references/gold-standards/fotografia/`

#### D1: interior-domestico (2 generaciones)

Prompt de fotografia:

```
A Spanish grandfather in his late sixties sitting on a gray sofa with his teenage granddaughter, both looking at a tablet screen. Warm pendant lamp casting 3000K golden light from above. The living room has a wooden bookshelf, family photos on the wall, and a ceramic bowl on the coffee table. Skin with real texture and subtle grain. Candid domestic moment, 35mm lens feel, no flash, no studio lighting. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# D1-A: ancla primero
python3 scripts/generate_image.py \
  -p "<prompt D1>" \
  -o outputs/test-D1-ancla-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg \
  --ref references/gold-standards/fotografia/interior-domestico/foto-pareja-cocinando-noche.jpg

# D1-B: escena primero
python3 scripts/generate_image.py \
  -p "<prompt D1>" \
  -o outputs/test-D1-escena-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/interior-domestico/foto-pareja-cocinando-noche.jpg \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg
```

#### D2: exterior-urbano (2 generaciones)

Prompt de fotografia:

```
Two young Spanish men in their twenties sitting at a small metal table outside a bar in a narrow Mediterranean street. One checks his phone while the other gestures mid-conversation. Late afternoon light enters from the left, casting warm shadows on the ochre wall behind them. Two small coffee cups on the table. Documentary street photography feel, 50mm lens, moderate depth of field. Skin with natural texture, visible stubble. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# D2-A: ancla primero
python3 scripts/generate_image.py \
  -p "<prompt D2>" \
  -o outputs/test-D2-ancla-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-exterior-luz-natural.jpg \
  --ref references/gold-standards/fotografia/exterior-urbano/foto-grupo-terraza-pueblo-blanco.jpg

# D2-B: escena primero
python3 scripts/generate_image.py \
  -p "<prompt D2>" \
  -o outputs/test-D2-escena-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/exterior-urbano/foto-grupo-terraza-pueblo-blanco.jpg \
  --ref references/gold-standards/fotografia/_anclas/ancla-exterior-luz-natural.jpg
```

#### D3: producto-en-mano (2 generaciones)

Prompt de fotografia:

```
Close-up of a young Spanish woman's hands holding a smartphone horizontally, watching a video on the screen. She sits on a wooden bench in a park with soft bokeh of green trees behind her. Late afternoon golden light from the right. The phone screen reflects a faint glow on her fingers. Visible skin texture, short natural nails, a thin silver ring on one finger. 85mm lens feel, shallow depth of field. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# D3-A: ancla primero
python3 scripts/generate_image.py \
  -p "<prompt D3>" \
  -o outputs/test-D3-ancla-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-producto-en-mano.jpg \
  --ref references/gold-standards/fotografia/producto-en-mano/foto-tablet-regazo-tren.jpg

# D3-B: escena primero
python3 scripts/generate_image.py \
  -p "<prompt D3>" \
  -o outputs/test-D3-escena-first.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/producto-en-mano/foto-tablet-regazo-tren.jpg \
  --ref references/gold-standards/fotografia/_anclas/ancla-producto-en-mano.jpg
```

### Criterios de evaluacion Paso D

Para cada par (A vs B), evaluar 1-5 en:

| Criterio | Que mide |
|---|---|
| **Fidelidad al look del ancla** | Temperatura de color, tipo de luz, grano, contraste |
| **Composicion propia** | No copia la composicion de la escena, genera una nueva |
| **Calidad tecnica** | Sin artefactos, piel natural, geometria correcta |
| **Casting espanol** | Los personajes tienen apariencia mediterranea |

**Decision:** gana la variante que mejor mantiene el look del ancla SIN copiar la composicion de la escena. Eso es lo que queremos: que el ancla defina el "como se ve" y el prompt defina el "que se ve".

---

## PASO F: Comparar con/sin Track A

### Objetivo

Medir si Track A (usar refs del banco fotografico) mejora visiblemente la fotografia generada respecto a generarla solo con texto (como hasta ahora).

### Piezas de test

| # | Pieza original (sin ref) | Familia | Que se ve en la foto original |
|---|---|---|---|
| F1 | `test-movistar-feed-fibra.png` | exterior-urbano | Pareja mayor en bici por calle de piedra. Aspecto algo generico/stock, luz plana |
| F2 | `test-movistar-mupi.png` | exterior-urbano | Dos mujeres en calle espanola con telefono. Buena golden hour, bastante natural |
| F3 | (generar baseline) | interior-domestico | Familia en salon -- generar sin ref para tener baseline |

### Generaciones

#### F1: Feed fibra -- regenerar CON ref

Prompt original (reconstruido de la pieza):

```
A mature Spanish couple in their sixties riding a tandem bicycle through a historic stone street. The woman sits behind laughing with her feet up, the man pedals wearing a straw hat and light blue shirt. Natural daylight, warm stone building facade with carved details. Documentary candid feel, slight motion blur on the wheels, 50mm lens. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# F1: con Track A refs (exterior)
python3 scripts/generate_image.py \
  -p "<prompt F1>" \
  -o outputs/test-F1-con-ref.png \
  --aspect 1:1 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-exterior-luz-natural.jpg \
  --ref references/gold-standards/fotografia/exterior-urbano/foto-grupo-terraza-pueblo-blanco.jpg
```

Comparar con: `_referencias/test-movistar-feed-fibra.png` (la foto de la pieza, sin ref)

#### F2: MUPI fibra -- regenerar CON ref

Prompt original (reconstruido de la pieza):

```
Two Spanish women in their mid-thirties walking down a cobblestone Mediterranean street at golden hour. The one on the left wears an olive green linen shirt and holds a phone, the other in a light blue t-shirt leans in to look at the screen. Warm backlight from the setting sun creates rim light on their hair. Woven straw bag on one shoulder. Blurred buildings and pedestrians in the background. Natural candid framing, 50mm lens, moderate film grain. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# F2: con Track A refs (exterior)
python3 scripts/generate_image.py \
  -p "<prompt F2>" \
  -o outputs/test-F2-con-ref.png \
  --aspect 2:3 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-exterior-luz-natural.jpg \
  --ref references/gold-standards/fotografia/exterior-ocio/foto-pareja-playa-golden-hour.jpg
```

Comparar con: `_referencias/test-movistar-mupi.png` (la foto de la pieza, sin ref)

#### F3: Interior domestico -- generar baseline + version con ref

Prompt:

```
A Spanish family of four gathered around a dining table in a warm apartment at night. The father serves paella from a large pan while the mother pours water. Two children, around 8 and 12, sit excitedly watching. Overhead pendant lamp casts warm 3000K light. The dining room has terracotta floor tiles, a wooden sideboard with a fruit bowl, and a half-open balcony door showing blue evening sky. Skin with natural texture and grain. Authentic family dinner moment, 35mm lens, candid framing. Pure photograph, no text, no logos, no graphic elements.
```

```bash
# F3-baseline: SIN ref (como hasta ahora)
python3 scripts/generate_image.py \
  -p "<prompt F3>" \
  -o outputs/test-F3-sin-ref.png \
  --aspect 3:2 --quality medium

# F3-track-a: CON ref (banco fotografico)
python3 scripts/generate_image.py \
  -p "<prompt F3>" \
  -o outputs/test-F3-con-ref.png \
  --aspect 3:2 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg \
  --ref references/gold-standards/fotografia/interior-domestico/foto-pareja-cocinando-noche.jpg
```

### Criterios de evaluacion Paso F

Para cada par (sin ref vs con ref), evaluar 1-5 en:

| Criterio | Que mide | Por que importa |
|---|---|---|
| **Coherencia de luz** | La temperatura, direccion e intensidad de la luz son consistentes | Las piezas Movistar tienen un look calido y natural definido |
| **Casting espanol** | Los personajes parecen espanoles, no genericos | Movistar es una marca espanola, el publico nota lo generico |
| **Realismo fotografico** | Parece foto real, no render AI | Menos "look de stock", mas editorial |
| **Textura y grano** | La piel tiene poros, las superficies tienen textura | Indicador de que el modelo "aprendio" del ancla |
| **Composicion natural** | Encuadre candido, no posado de estudio | Alineado con el estilo documental de la marca |

**Decision:** si la version con ref gana en 3+ criterios de forma clara, Track A se confirma como obligatorio en la cascada. Si la diferencia es marginal, Track A pasa a ser opcional (ahorra coste de mantenimiento del banco).

---

## Resumen de generaciones

| Test | Output | Refs | Coste aprox |
|---|---|---|---|
| D1-A | test-D1-ancla-first.png | ancla-interior + escena-interior | ~0.03 USD |
| D1-B | test-D1-escena-first.png | escena-interior + ancla-interior | ~0.03 USD |
| D2-A | test-D2-ancla-first.png | ancla-exterior + escena-exterior | ~0.03 USD |
| D2-B | test-D2-escena-first.png | escena-exterior + ancla-exterior | ~0.03 USD |
| D3-A | test-D3-ancla-first.png | ancla-producto + escena-producto | ~0.03 USD |
| D3-B | test-D3-escena-first.png | escena-producto + ancla-producto | ~0.03 USD |
| F1 | test-F1-con-ref.png | ancla-exterior + escena-exterior | ~0.03 USD |
| F2 | test-F2-con-ref.png | ancla-exterior + escena-ocio | ~0.03 USD |
| F3-base | test-F3-sin-ref.png | ninguna | ~0.03 USD |
| F3-ref | test-F3-con-ref.png | ancla-interior + escena-interior | ~0.03 USD |
| **Total** | **10 generaciones** | | **~0.30 USD (~0.30 EUR)** |

> Nota: el coste real depende del pricing actual de gpt-image-2. Con quality medium y 1024px, cada generacion cuesta ~0.03-0.08 USD. Total estimado < 1 EUR.

---

## Despues del test

1. **Evaluar** cada par con la tabla de criterios
2. **Documentar resultado D** en SKILL.md: regla de orden de dominancia
3. **Documentar resultado F** en SKILL.md: si Track A es obligatorio u opcional
4. **Actualizar RUNBOOK** marcando Pasos D y F como completados
5. **Sincronizar** resultados a maia-skills-github/
