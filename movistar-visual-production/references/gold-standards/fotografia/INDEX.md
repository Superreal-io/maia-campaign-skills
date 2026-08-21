# Banco Fotografico - Track A

> Fotografias puras y anclas de estilo para el Art Director (D).
> Uso: referencia visual (`--ref`) en prompts de generacion que piden "fotografia pura, sin texto".
> Requisito minimo: 300 px en ambos lados, sin texto/logos/marcos superpuestos.

## Resumen

| Familia | Crops (A) | Seeds (B) | Seeds (C) | Total | Estado |
|---|---|---|---|---|---|
| _anclas | - | 4 | - | 4 | Completa |
| exterior-ocio | 1 | 1 | 0 | 2 | Cubierta |
| exterior-urbano | 3 | 1 | 0 | 4 | Cubierta |
| interior-domestico | 1 | 1 | 0 | 2 | Cubierta |
| producto-en-mano | 0 | 0 | 3 | 3 | Cubierta |
| retail-tienda | 0 | 1 | 1 | 2 | Cubierta |
| **Total** | **5** | **8** | **4** | **17** | **5/5 familias cubiertas** |

## Anclas de estilo (_anclas/)

Imagenes generadas con gpt-image-2 que definen el look fotografico de cada familia.
Se usan como `--ref` de nivel 3 en la cascada de seleccion del Art Director.

| Archivo | Tamanio | Familias que cubre | Descripcion |
|---|---|---|---|
| ancla-interior-luz-calida.jpg | 1536x1024 | interior-domestico | Familia de 3 en sofa, lampara dorada ~3000K, fotos en pared, manta |
| ancla-exterior-luz-natural.jpg | 1536x1024 | exterior-urbano, exterior-ocio | Pareja paseando en plaza de Valencia, golden hour, reflejos en piedra |
| ancla-producto-en-mano.jpg | 1536x1024 | producto-en-mano | Manos con smartphone en cafe, angulo 3/4, espresso, bokeh calido |
| ancla-retail-luz-tienda.jpg | 1536x1024 | retail-tienda | Asesor Movistar mostrando telefono a clienta en mostrador, track 4500K |

## Escenas por familia

### exterior-ocio/

| Archivo | Tamanio | Origen | Contenido |
|---|---|---|---|
| foto-casa-verano-terraza-mar.jpg | 1000x505 | Crop: meta/meta-feed-foto-hogar-fibra-verano-1080.jpg | Casa mediterranea con terraza y vista al mar |
| foto-pareja-playa-golden-hour.jpg | 1536x1024 | Seed: gpt-image-2 (Capa B descarte) | Pareja joven en playa mediterranea al atardecer, golden hour |

### exterior-urbano/

| Archivo | Tamanio | Origen | Contenido |
|---|---|---|---|
| foto-futbolista-retrato-cielo.jpg | 1020x770 | Crop: exterior/exterior-mupi-futbol-retrato-individual.jpg | Retrato de futbolista mirando al cielo, fondo azul |
| foto-futbolistas-grupo-campo.jpg | 1072x750 | Crop: exterior/exterior-mupi-futbol-multijugadores.jpg | Grupo de futbolistas corriendo en campo (composicion) |
| foto-joven-camiseta-cielo.jpg | 530x420 | Crop: exterior/exterior-metro-futbol-fan-landscape.jpg | Joven sonriendo con camiseta a rayas, cielo azul |
| foto-grupo-terraza-pueblo-blanco.jpg | 1536x1024 | Seed: gpt-image-2 (Capa B descarte) | Grupo de 4 amigos en terraza de pueblo blanco andaluz |

### interior-domestico/

| Archivo | Tamanio | Origen | Contenido |
|---|---|---|---|
| foto-abuelo-bebe-movil-sofa.jpg | 400x750 | Crop: digital/digital-vertical-titular-xl-foto-documental.jpg | Abuelo con gafas sosteniendo bebe en sofa, luz calida |
| foto-pareja-cocinando-noche.jpg | 1536x1024 | Seed: gpt-image-2 (Capa B descarte) | Pareja cocinando en cocina espanola, pendant 3000K, vino |

### producto-en-mano/

| Archivo | Tamanio | Origen | Contenido |
|---|---|---|---|
| foto-tablet-regazo-tren.jpg | 1536x1024 | Seed Capa C: gpt-image-2 (--ref ancla-producto) | Mujer en tren con tablet mostrando streaming espanol, luz ventana + pantalla |
| foto-smartwatch-muneca-parque.jpg | 1536x1024 | Seed Capa C: gpt-image-2 (--ref ancla-producto) | Smartwatch en muneca con resumen fitness, banco de parque, golden hour |
| foto-auriculares-escritorio-casa.jpg | 1536x1024 | Seed Capa C: gpt-image-2 (--ref ancla-producto) | Auriculares inalambricos en escritorio, mano alcanzando, flexo 3000K |

### retail-tienda/

| Archivo | Tamanio | Origen | Contenido |
|---|---|---|---|
| foto-asesor-cliente-mayor-mostrador.jpg | 1536x1024 | Seed: gpt-image-2 (Capa B descarte) | Asesor joven ayudando a cliente mayor en mostrador, track 4500K |
| foto-clienta-probando-telefono-mesa.jpg | 1536x1024 | Seed Capa C: gpt-image-2 (--ref ancla-retail) | Clienta probando telefono en mesa expositor, asesor en segundo plano |

## Crops descartados (Capa A)

| Archivo | Motivo |
|---|---|
| foto-pareja-embarazada-salon.jpg | Texto superpuesto imposible de eliminar (full-bleed) |
| foto-tienda-flagship-interior.jpg | Senaletica Movistar integrada en entorno |
| _(digital-display-pack halfpage)_ | Crop resultante < 300px en alto |

## Resultados de validacion

### Paso D: Orden de dominancia (2026-08-21)

Test A/B en 3 familias (interior-domestico, exterior-urbano, producto-en-mano), 6 generaciones.

**Decision: ancla siempre como ref 1, escena como ref 2.**

- D1 (interior): ancla-first preserva casting del prompt y look calido. Escena-first contamina casting.
- D2 (exterior): empate tecnico.
- D3 (producto): empate. Hallazgo adicional: la escena puede dominar la composicion independientemente del orden. Reforzar encuadre en el prompt cuando difiera de la escena.

### Paso F: Con/sin Track A (2026-08-21)

Comparativo interior-domestico (baseline sin ref vs con ref). Exterior tambien regenerado con refs.

**Decision: Track A es la opcion por defecto para toda fotografia de escena.**

- Coherencia de luz: con ref mantiene dorado 3000K consistente; sin ref sale mas neutra/plana.
- Casting espanol: mejora ligera con ref.
- Textura y grano: la version con ref transfiere la textura del ancla.

Ambas decisiones documentadas en SKILL.md.

## Historial de ejecucion

- **Capa A** (2026-08-21): 5 crops extraidos de gold standards existentes. 2 descartados por texto, 1 por tamanio.
- **Capa B** (2026-08-21): 20 candidatas generadas (5 por ancla). 4 ganadoras seleccionadas + 4 descartadas reutilizadas como seeds.
- **Capa C** (2026-08-21): 4 seeds generadas con anclas como --ref (3 producto + 1 retail). Cobertura 5/5 familias alcanzada.
- **Paso D** (2026-08-21): 6 generaciones A/B en 3 familias. Regla fija: ancla como ref 1.
- **Paso F** (2026-08-21): 4 generaciones comparativas. Track A confirmado como default.
