# Runbook: Banco Fotografico Track A

Guia paso a paso para poblar `references/gold-standards/fotografia/` con imagenes de referencia pura (sin texto, sin logos, sin marcos) que el Art Director (D) usa como `--ref` en Track A.

**Estado actual:** la estructura de carpetas y la taxonomia estan definidas en SKILL.md y magic-prompt.md, pero la carpeta esta vacia. Sin imagenes, D no puede usar Track A y cae en generacion sin referencia (stock generico).

**Resultado esperado:** 4 anclas de estilo + 15-25 escenas semilla organizadas por familia, con INDEX.md completo.

**Coste estimado:** ~20 EUR en creditos OpenAI, media jornada de trabajo.

**Requisitos:** Paperclip con `OPENAI_API_KEY` (secreto `openai-image-key`).

---

## Estructura objetivo

```
fotografia/
├── INDEX.md                  Taxonomia completa
├── RUNBOOK-banco-fotografico.md   (este archivo)
├── _anclas/
│   ├── ancla-interior-luz-calida.jpg
│   ├── ancla-exterior-luz-natural.jpg
│   ├── ancla-producto-en-mano.jpg
│   └── ancla-retail-luz-tienda.jpg
├── interior-domestico/       Salon, cocina, dormitorio, terraza cubierta
├── interior-personal/        Persona sola con dispositivo, estudio, hobby
├── interior-retail/          Tienda, asesor, mostrador, expositor
├── exterior-urbano/          Calle, terraza bar, transporte, campus
├── exterior-ocio/            Playa, parque, montana, deporte casual
└── producto/                 Dispositivo en mano, cutout lifestyle, bodegon
```

---

## CAPA A: Extraer crops de piezas existentes

**Que es:** recortar la zona de fotografia pura de piezas reales que ya tenemos (gold standards Track B y pieces/). Coste cero, ~1 hora.

**Fuentes candidatas (97 gold standards + 41 pieces = 138 imagenes):**

Las gold standards son mejor fuente porque estan normalizadas a JPEG q90, lado largo max 1536px. Las pieces/ son capturas de navegador a resoluciones variadas.

### Paso A1: Identificar piezas con fotografia cropeable

Revisar visualmente cada imagen y anotar si contiene una zona de fotografia pura (personas, escenas, producto en contexto) que se pueda recortar sin incluir texto, logos ni marcos de la pieza.

**Criterios de seleccion:**

- La zona de foto debe tener al menos 300px de lado corto despues del crop
- La foto debe ser de calidad editorial (no captura web pixelada)
- Sin textos superpuestos sobre la zona a cropear
- Sin logos de terceros visibles en la zona a cropear
- Sin marcos, bordes redondeados ni elementos graficos dentro del crop

**Candidatas por canal (basado en inspeccion de nombres y dimensiones):**

| Canal | Candidatas probables | Motivo |
|---|---|---|
| email | `email-esimflag-travel-lifestyle` (694x1536), `email-segunda-fibra-lifestyle` (457x1536), `email-renting-coches-comparativa` (897x1536) | Heroes con fotos lifestyle grandes |
| meta | `meta-feed-foto-hogar-fibra-verano-1080` (1220x1260), `meta-feed-foto-rayban-playa` (600x600), `meta-story-foto-convergente-laliga`, `meta-story-foto-hogar-fibra` | Fotos a sangre o con zona foto dominante |
| exterior | `exterior-mupi-foto-sangre` (1536x864), `exterior-mupi-foto-pareja-seleccion` (630x929), `exterior-mupi-futbol-retrato-individual` (1078x1536), `exterior-mupi-futbol-multijugadores` (1072x1536), `exterior-metro-futbol-fan-landscape` (1536x628) | Fotos a sangre o con foto dominante |
| movistarplus | `movistarplus-banner-deportes-motogp` (1536x469) | Foto a sangre de circuito |
| tienda | `tienda-chevalet-foto-mundial-tv` (1101x1536), `tienda-entorno-flagship-granvia` (1536x864), `tienda-entorno-muro-verbos` (1536x864) | Fotos de tienda real o evento |
| pieces/ | `exterior.jpg` (1600x900), `lona_movistar.jpg` (699x424), `MOVISTAR-X-LA-SELECCION.jpg` (1200x675) | Fotos grandes con zona cropeable |

### Paso A2: Hacer los crops

Para cada candidata aprobada:

```bash
# Desde la carpeta movistar-visual-production/
python3 -c "
from PIL import Image
im = Image.open('references/gold-standards/<canal>/<archivo>.jpg')
# Coordenadas del crop: (left, upper, right, lower)
crop = im.crop((LEFT, UPPER, RIGHT, LOWER))
crop.save('references/gold-standards/fotografia/<familia>/<nombre-descriptivo>.jpg', 'JPEG', quality=90)
print(f'Crop: {crop.width}x{crop.height}')
"
```

**Convencion de nombre del crop:**

```
<familia>-<escena>-<detalle>.jpg

Ejemplos:
interior-domestico-familia-sofa-tablet.jpg
exterior-urbano-pareja-terraza-verano.jpg
producto-iphone-mano-angulo34.jpg
interior-retail-tienda-granvia-mostrador.jpg
```

### Paso A3: Clasificar por familia

Mover cada crop a su carpeta de familia segun la taxonomia:

| Familia | Que incluye | Ancla asociada |
|---|---|---|
| `interior-domestico` | Salon, cocina, dormitorio, familia en casa, sofa, mesa | `ancla-interior-luz-calida` |
| `interior-personal` | Persona sola, estudio, hobby, trabajo remoto | `ancla-interior-luz-calida` |
| `interior-retail` | Tienda Movistar, mostrador, asesor, expositor | `ancla-retail-luz-tienda` |
| `exterior-urbano` | Calle, terraza bar, transporte, campus, oficina exterior | `ancla-exterior-luz-natural` |
| `exterior-ocio` | Playa, parque, montana, deporte casual, viaje | `ancla-exterior-luz-natural` |
| `producto` | Dispositivo en mano, cutout con contexto, bodegon lifestyle | `ancla-producto-en-mano` |

### Paso A4: Validar umbral de calidad

Despues de todos los crops, verificar:

```bash
# Listar crops con lado corto < 300px (descartables)
for f in references/gold-standards/fotografia/*/*.jpg; do
  python3 -c "
from PIL import Image
im = Image.open('$f')
if min(im.width, im.height) < 300:
    print(f'DESCARTABLE ({im.width}x{im.height}): $f')
" 2>/dev/null
done
```

**Resultado esperado Capa A:** 8-15 crops validos. Probablemente la mayoria en exterior (mas fotos a sangre) y menos en interior-retail (pocas fotos de tienda real).

---

## CAPA B: Generar las 4 anclas de estilo

**Que es:** crear las 4 imagenes ancla que definen el look fotografico de cada familia. Son las referencias "de ultimo recurso" en la cascada (nivel 3) y la referencia secundaria habitual (nivel 1-2). Coste ~5 EUR, ~40 min.

**Prerequisito:** Paperclip con OPENAI_API_KEY.

### Paso B1: Generar 5 candidatas por ancla

Para cada ancla, escribir un prompt basado en la descripcion textual de `magic-prompt.md` (seccion "Anclas de estilo") y generar 5 variantes.

**Ancla 1: interior-luz-calida**

```bash
# Generar 5 candidatas (cambiar el seed/prompt ligeramente en cada una)
for i in 1 2 3 4 5; do
python3 scripts/generate_image.py \
  -p "A Spanish family of three in their living room at dusk. The mother sits on a linen sofa scrolling a tablet, the father leans on the kitchen counter behind with a warm overhead pendant lamp casting golden light. A floor lamp fills the shadows with soft bounced warmth. Skin has real texture and visible grain, golden undertone from the 3000K light. The apartment has lived-in details: a wool throw, ceramic mugs, books. Camera at eye level, natural framing with slight asymmetry, 35mm lens feel. No flash, no overhead hard light, no studio look." \
  -o outputs/ancla-interior-candidata-$i.png \
  --aspect 3:2 --quality high
done
```

**Ancla 2: exterior-luz-natural**

```bash
for i in 1 2 3 4 5; do
python3 scripts/generate_image.py \
  -p "A young Spanish woman in her late twenties walking through a sunlit Mediterranean street in the late afternoon. She wears a light blue linen shirt and carries a phone loosely in one hand. Direct golden-hour sunlight enters from the left, casting defined shadows on the warm stone facade behind her. Skin shows real texture with subtle imperfections, moderate contrast. The setting is a residential Spanish neighborhood with terracotta pots, an iron balcony, and dappled tree shadows on the ground. Documentary editorial feel, slightly imperfect framing, 50mm lens. No studio, no neutral background." \
  -o outputs/ancla-exterior-candidata-$i.png \
  --aspect 3:2 --quality high
done
```

**Ancla 3: producto-en-mano**

```bash
for i in 1 2 3 4 5; do
python3 scripts/generate_image.py \
  -p "Close-up of real human hands holding a smartphone at a three-quarter angle in a cafe setting. The hands show natural texture with visible veins, knuckle lines, and short clean nails. Mixed lighting: warm ambient from the cafe and cool glow from the phone screen reflecting on the fingers. Selective focus keeps the hands and screen sharp while the wooden table and blurred espresso cup fall into soft bokeh. Subtle film grain. No white background, no floating product, no studio isolation. The device is naturally integrated into a moment of reading or browsing." \
  -o outputs/ancla-producto-candidata-$i.png \
  --aspect 3:2 --quality high
done
```

**Ancla 4: retail-luz-tienda**

```bash
for i in 1 2 3 4 5; do
python3 scripts/generate_image.py \
  -p "Interior of a modern Movistar retail store. A young advisor in a branded blue polo assists a customer at a display table with phones on white pedestals. Commercial track lighting from above creates neutral 4500K illumination with medium contrast. The store has visible materials: light wood counters, brushed metal fixtures, glass display cases, terrazo floor. A large backlit Movistar logo panel glows blue in the background. The interaction is natural and relaxed, not posed. Documentary framing, 28mm wide lens, subtle grain. No overlay graphics, no text in the scene." \
  -o outputs/ancla-retail-candidata-$i.png \
  --aspect 3:2 --quality high
done
```

### Paso B2: Seleccion humana

Mostrar las 5 candidatas de cada ancla al equipo (o al propio operador). Criterios de seleccion:

1. **Fidelidad al look descrito** en magic-prompt.md (luz, temperatura, grano, contraste)
2. **Versatilidad como referencia:** que no sea tan especifica que limite las escenas derivadas
3. **Calidad tecnica:** sin artefactos de IA visibles, piel natural, geometria correcta
4. **Diversidad de casting:** representacion espanola, no monolitica

### Paso B3: Normalizar y guardar

```bash
# Para cada ancla ganadora:
python3 -c "
from PIL import Image
im = Image.open('outputs/ancla-interior-candidata-X.png')
# Normalizar a JPEG q90, lado largo max 1536px
ratio = 1536 / max(im.width, im.height)
if ratio < 1:
    im = im.resize((int(im.width*ratio), int(im.height*ratio)), Image.LANCZOS)
im.save('references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg', 'JPEG', quality=90)
print(f'Guardada: {im.width}x{im.height}')
"
```

Repetir para las 4 anclas con sus nombres canonicos:
- `_anclas/ancla-interior-luz-calida.jpg`
- `_anclas/ancla-exterior-luz-natural.jpg`
- `_anclas/ancla-producto-en-mano.jpg`
- `_anclas/ancla-retail-luz-tienda.jpg`

---

## CAPA C: Completar escenas semilla

**Que es:** generar escenas fotograficas para familias que quedaron vacias o con pocos crops despues de la Capa A. Coste ~10 EUR, ~1 hora.

**Prerequisito:** Capas A y B completadas. Las anclas se usan como `--ref` para las escenas.

### Paso C1: Inventario de gaps

Despues de la Capa A, contar cuantos crops hay por familia:

```bash
for d in references/gold-standards/fotografia/*/; do
  familia=$(basename "$d")
  [ "$familia" = "_anclas" ] && continue
  count=$(ls "$d"*.jpg 2>/dev/null | wc -l)
  echo "$familia: $count crops"
done
```

**Objetivo minimo por familia:** 2-3 escenas. Si una familia tiene 0-1, necesita escenas semilla.

### Paso C2: Generar escenas con ancla como referencia

Para cada familia con gaps, generar 2-3 escenas usando el ancla de la familia como `--ref` principal.

**Ejemplo: interior-domestico (si tiene 0-1 crops)**

```bash
# Escena 1: familia en sofa con tablet
python3 scripts/generate_image.py \
  -p "A Spanish couple in their thirties sitting on a gray linen sofa in a warm living room at night. She holds a tablet showing a blue interface, he leans in looking at the screen. A floor lamp behind them casts soft golden light. The room has a bookshelf, a wool blanket, and a ceramic vase with dried flowers. Skin has real texture and subtle grain. Relaxed domestic evening mood. Natural framing, 35mm lens, no flash." \
  -o outputs/semilla-interior-domestico-sofa-tablet.png \
  --aspect 3:2 --quality high \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg

# Escena 2: madre e hijo en cocina
python3 scripts/generate_image.py \
  -p "A Spanish mother and her teenage son standing at a kitchen island, both looking at a smartphone she holds. Warm pendant light above creates a 3200K glow. The kitchen has wooden counters, white tiles, and a fruit bowl. Evening light from a small window adds a cool rim. Skin with natural imperfections, visible pores. Authentic interaction, slightly candid framing. 40mm lens feel, shallow depth of field on the background." \
  -o outputs/semilla-interior-domestico-cocina-madre.png \
  --aspect 3:2 --quality high \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg
```

**Escenas semilla sugeridas por familia:**

| Familia | Escenas a generar si faltan |
|---|---|
| `interior-domestico` | Familia sofa tablet, madre hijo cocina, pareja dormitorio lectura |
| `interior-personal` | Joven estudia escritorio, persona yoga salon, freelancer portatil |
| `interior-retail` | Cliente probando telefono, asesor explicando pantalla, zona de espera |
| `exterior-urbano` | Pareja terraza bar, joven bici campus, grupo amigos plaza |
| `exterior-ocio` | Familia playa, pareja senderismo, amigos parque picnic |
| `producto` | Mano con telefono en cafe, tablet en regazo en tren, auriculares en escritorio |

### Paso C3: Normalizar y clasificar

Mismo proceso que B3: JPEG q90, lado largo max 1536px, nombre descriptivo, mover a la familia correspondiente.

---

## PASO D: A/B del orden de dominancia

**Que es:** probar si el resultado mejora pasando ancla como ref 1 + escena como ref 2, o al reves. Coste ~1 EUR, ~20 min.

### Procedimiento

Elegir 2-3 familias con al menos 1 escena y 1 ancla. Para cada una, generar la misma pieza dos veces:

```bash
# Variante A: ancla primero, escena segundo
python3 scripts/generate_image.py \
  -p "<mismo prompt>" -o outputs/ab-test-ancla-first.png --aspect 1:1 --quality medium \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg \
  --ref references/gold-standards/fotografia/interior-domestico/<escena>.jpg

# Variante B: escena primero, ancla segundo
python3 scripts/generate_image.py \
  -p "<mismo prompt>" -o outputs/ab-test-escena-first.png --aspect 1:1 --quality medium \
  --ref references/gold-standards/fotografia/interior-domestico/<escena>.jpg \
  --ref references/gold-standards/fotografia/_anclas/ancla-interior-luz-calida.jpg
```

Comparar visualmente: cual mantiene mejor el look del ancla sin copiar la composicion de la escena? Documentar el resultado y actualizar la regla de cascada en SKILL.md si hace falta.

---

## PASO E: Completar INDEX.md

Crear el INDEX de fotografia/ con la taxonomia completa:

```markdown
# INDEX -- Fotografia (Track A)

## Anclas de estilo

| Ancla | Archivo | Familias que cubre |
|---|---|---|
| Interior luz calida | `_anclas/ancla-interior-luz-calida.jpg` | interior-domestico, interior-personal |
| Exterior luz natural | `_anclas/ancla-exterior-luz-natural.jpg` | exterior-urbano, exterior-ocio |
| Producto en mano | `_anclas/ancla-producto-en-mano.jpg` | producto |
| Retail luz tienda | `_anclas/ancla-retail-luz-tienda.jpg` | interior-retail |

## Escenas por familia

### interior-domestico (ancla: interior-luz-calida)

| Archivo | Escena | Origen | Resolucion |
|---|---|---|---|
| interior-domestico-familia-sofa-tablet.jpg | Familia en sofa con tablet | Crop de email-esimflag | 800x600 |
| ... | ... | ... | ... |

[repetir para cada familia]
```

---

## PASO F: Regenerar y comparar

**Que es:** tomar 2-3 piezas que D genero anteriormente SIN referencia, y regenerarlas CON las nuevas referencias Track A. Comparar lado a lado para medir el impacto. Coste ~3 EUR, ~40 min.

### Procedimiento

1. Buscar en outputs/ piezas anteriores donde la foto salio generica
2. Usar el mismo prompt original pero ahora con `--ref` del banco fotografico
3. Poner el antes y el despues lado a lado
4. Documentar: que mejoro (luz, casting, composicion, realismo) y que no cambio

---

## Checklist de ejecucion

```
CAPA A (gratis, ~1h)
- [ ] Revisar visualmente las 97 gold standards + 41 pieces
- [ ] Anotar candidatas con zona foto cropeable > 300px lado corto
- [ ] Hacer los crops con PIL
- [ ] Clasificar por familia
- [ ] Descartar crops < 300px
- [ ] Contar crops por familia, anotar gaps

CAPA B (~5 EUR, ~40min) -- requiere Paperclip
- [ ] Generar 5 candidatas ancla-interior-luz-calida
- [ ] Generar 5 candidatas ancla-exterior-luz-natural
- [ ] Generar 5 candidatas ancla-producto-en-mano
- [ ] Generar 5 candidatas ancla-retail-luz-tienda
- [ ] Seleccion humana: 1 ganadora por ancla
- [ ] Normalizar y guardar en _anclas/

CAPA C (~10 EUR, ~1h) -- requiere Paperclip + Capa B
- [ ] Inventario de gaps por familia
- [ ] Generar 2-3 escenas semilla por familia deficitaria
- [ ] Normalizar y clasificar

PASO D (~1 EUR, ~20min)
- [ ] A/B test de orden de dominancia en 2-3 familias
- [ ] Documentar resultado

PASO E (gratis, ~20min)
- [ ] Escribir INDEX.md con taxonomia completa

PASO F (~3 EUR, ~40min)
- [ ] Elegir 2-3 piezas sin referencia anteriores
- [ ] Regenerar con Track A
- [ ] Comparar y documentar
```

---

## Notas operativas

- **Todos los comandos se ejecutan desde** `Skills/movistar-visual-production/`
- **El secreto de API** se lee del secreto Paperclip `openai-image-key`, nunca en plaintext
- **Ratio 3:1 max** de gpt-image-2 aplica tambien aqui. Los crops y anclas se generan a 3:2 (horizontal) o 2:3 (vertical), ambos dentro del limite
- **La Capa A se puede ejecutar sin Paperclip** (solo recorta imagenes que ya estan en disco)
- **Despues de ejecutar todo, sincronizar a maia-skills-github/** con el mismo proceso de siempre
