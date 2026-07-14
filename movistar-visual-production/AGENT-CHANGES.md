# Cambios necesarios en 04-art-director.md al adoptar esta skill

No aplicar hasta que el bundle este importado en Paperclip y el secret configurado.

## 1. Contrato del agente (parrafo inicial)

Antes: "Tu output no es arte final de produccion. Es un mockup".
Despues: el output es una pieza presentable a cliente sin retoque: composicion final, fotografia real generada, tipografia y logos reales, verificada visualmente. Lo que queda para produccion es adaptacion de formatos secundarios y assets definitivos de producto.

## 2. Eliminar los pasos de copia de base64

- Track A, Paso A1: sustituir "Copia LITERALMENTE el bloque @font-face... y el bloque :root" por "escribe los slots {{FONT_FACE_MIN}} y {{TOKENS_CSS}}; assemble.py los rellena".
- Track B, Paso B2 (embeber tipografia en SVG copiando base64): eliminar completo.
- Seccion Logo: sustituir "copia el data URI del logo" por los slots {{LOGO_*}}.

## 3. Sustituir Track B (SVG a mano) por HTML de dimensiones fijas + render

Social, tienda, exterior y M+ pasan a producirse como HTML fijo (ej. 1080x1080) renderizado a PNG con scripts/render.py. La tabla de "Pieza representativa por canal" cambia los formatos SVG por "HTML fijo + PNG". SVG solo bajo peticion explicita de vector.

## 4. Sustituir la politica de placeholders por generacion real

Antes: "No generas fotografias via API externa. Las fotografias van como placeholders".
Despues: cada hueco de imagen se genera con scripts/generate_image.py usando un prompt estilo magic-prompt.md. El placeholder con data-prompt queda solo como fallback flaggeado (`imagen_provisional`) si la API falla.

## 5. Anadir el paso de QA visual al proceso

Nuevo Paso 5 tras el ensamblaje: renderizar, mirar el PNG, checklist visual de la skill (5 non-negotiables + patron del audit-report + solapes + integracion de foto + test de parecido con referencias). Maximo 2 iteraciones de correccion. El QA textual actual (tokens, HEX, grafias) se mantiene, pero ya no es suficiente para entregar.

## 6. Anadir "referencias antes de disenar"

En el Paso 1 (Concepto visual): antes de articular el concepto, leer 2-3 piezas reales del formato en references/pieces/ y el bloque del formato en brand/audit-report.md.

## 7. Skills asociadas

- Anadir: `movistar-visual-production` (OBLIGATORIA).
- Retirar de la lista: `brand-assets-movistar` y `brand-typography-movistar` (sustituidas por brand/ del bundle). `html-component-library` se mantiene por sus patrones de layout, pero sus instrucciones de copiar base64 quedan anuladas por esta skill.
- `brand-visual-guidelines-movistar`, `brand-visual-composition-movistar`, `communication-tiers-movistar`, `estilo-terminologia-movistar` y los playbooks siguen igual.

## 8. Config del agente en Paperclip

```json
{ "env": { "OPENAI_API_KEY": "$secret:openai-image-key" } }
```

El secret se crea a nivel de compania en la seccion Secrets con la clave de Google AI Studio.

## 9. Requisito de runtime

El workspace del agente necesita un backend de render (playwright + chromium o chrome headless). Verificar en el primer run: `python3 scripts/render.py -i templates/html/feed-1080.slots.html -o /tmp/test.png` (fallara por slots sin ensamblar, pero confirma si hay navegador). Si no lo hay, anadir al setup del agente:

```bash
pip install playwright --break-system-packages && python3 -m playwright install chromium
```
