# Logotipo — Brand Guardian v4 (Movistar)

> Parte del Brand Guardian v4 (spec autoritativa, 2026-06-08). Numeración de sección (`2.x`) conservada
> para continuidad con citas previas. Ver `movistar-brand-guidelines-v1/SKILL.md` para el índice general.

## 2. Logotipo

> **El identificador es la "M" (confirmado por cliente, nov-2025).** Solo se usa la **M**; el wordmark / lockup quedan para casos especiales. Assets oficiales vectoriales bundleados en `assets/logo/`: `movistar-m-blue.svg` (Azul `#0066FF`, sobre claro), `movistar-m-white.svg` (Blanco/Marfil `#FFFAF5`, sobre azul/foto azulada/oscuro) y `movistar-m.svg` (monocromo Negro `#262423`). Colores verificados desde los SVG oficiales. **Limitaciones:** no recolorear, no deformar ni reproporcionar, no aplicar efectos, no recrear la M a mano; la M va en Azul Movistar (blanca solo sobre fondo Azul Movistar o foto azulada legible); respeta el área de protección; máximo **1 logo por pieza**. En `.pptx`, si el master ya pone la M, no la añadas.

### 2.1 Validación del logotipo

#### 2.1.1 La M como elemento principal (Guía de marca. Pág. 8, 10 y 13)

La **M** es nuestro elemento más reconocible y nuestro principal identificador.

Hay algo que nunca cambia en ninguna de nuestras comunicaciones: nuestra M se destaca de forma independiente y siempre luce su icónico Azul Movistar. Este color es el elemento transversal que nos identifica en cualquier comunicación. Es el recurso que garantiza un reconocimiento inmediato y mantiene la coherencia de marca en cada punto de contacto.

El Azul Movistar es nuestro sello inconfundible.

#### 2.1.2 Versiones de color (Guía de marca. Pág. 18, 19 y 20)

Nuestra M debe ir siempre en azul, y solo puede ir en blanco cuando el fondo es nuestro Azul Movistar.  
La aplicación de la **Azul Movistar sobre fondo Negro Movistar no supone una infracción aunque se usará de forma excepcional**.

Orden de prioridad de uso:

1. **Prioridad 1**  
   - M: Azul Movistar (`#0066FF`)
   - Fondo: Blanco Movistar (`#FFFAF5`)

2. **Prioridad 2**  
   - M: Blanco Movistar (`#FFFAF5`)  
   - Fondo: Azul Movistar (`#0066FF`)

3. **Prioridad 3**  
   - M: Azul Movistar (`#0066FF`)
   - Fondo: se aceptan los colores secundarios: Azul claro (`#d3eeff`) o Verde claro (`#cef7bf`) o Amarillo claro (`#ffe99c`) o Coral claro (`#ffc5a8`)

4. **Prioridad 4 (uso excepcional)**  
   - M: Azul Movistar (`#0066FF`)
   - Fondo: Negro Movistar (`#262423`)

**Uso sobre fondos fotográficos**

- Sobre fondos fotográficos, nuestra M debe ir en Azul Movistar siempre que se garantice por completo su legibilidad.  
- Cuando no se garantice la legibilidad de la M azul sobre fondo fotográfico, está permitido el uso en blanco, siempre que el fondo tenga un tono similar a nuestro azul y asegure visibilidad.

#### 2.1.3 Tamaño mínimo del logotipo (Guía de marca. Pág. 24)

Para asegurar la legibilidad del logotipo:

- Tamaño mínimo en impresión: **10 mm**  
- Tamaño mínimo en digital: **20 px**

#### 2.1.4 Lockup horizontal (Guía de marca. Pág. 31, 32 y 33)

El **lockup horizontal** se utilizará en entornos donde sea necesario vincular la M con la palabra Movistar.

Su aplicación será puntual y excepcional, limitada principalmente a:

- Patrocinios (por ejemplo, equipaciones) donde se necesite un impacto visible.  
- Photocalls y entornos multimarca donde la visibilidad del logotipo debe ser alta.  
- Elementos de merchandising en los que se quiera recalcar explícitamente el rol de Movistar.

#### 2.1.5 Lockup vertical (Guía de marca. Pág. 34, 35 y 36)

Disponemos de una versión de **lockup vertical** para formatos cuadrados o estrechos, donde la composición requiera una solución más compacta.

#### 2.1.6 Uso en artifacts web (HTML/React) y outputs digitales

En un artifact web hay **dos niveles**, en este orden de preferencia:

1. **Preferente — esquema `movistar://<id>` (blob).** Emite la M como `<img src="movistar://logo-m-blue">`
   (o `-white`/`-mono`); el backend resuelve ese URI a una URL de blob firmada, exactamente igual que
   el banco de fotos (Movistar es company propia → el prefijo es `movistar://`, no el nombre de una
   sub-marca). Coste de tokens casi nulo frente a incrustar el SVG. Requiere que los ids de logo estén
   dados de alta en `BRAND_IMAGES` del backend (handoff pendiente — ver `HANDOFF-REVISION.md`); mientras
   no lo estén, usa el nivel 2.
2. **Fallback — SVG limpio con `<symbol>`/`<use>`.** Los SVG de `assets/logo/` están **limpios** (sin
   clases `.stN` de Illustrator; `fill` inline por trazo), así que se pueden incrustar sin colisión de
   `id`/clase. Define la M una vez como `<symbol id="mvst-m" viewBox="…">…</symbol>` y referénciala con
   `<use href="#mvst-m">` cada vez que aparezca — no dupliques el `<path>` completo.

En **email, `.docx` y documentos** incrusta el SVG inline directamente (no hay resolución de
`movistar://` fuera del pipeline de artifacts). La regla de color de la M no cambia por el formato:
Azul Movistar salvo sobre fondo Azul/oscuro/foto azulada (§2.1.2). El catálogo de anti-patrones de
artifacts (incluido el logo) está en `brand/artifact-qa.md`.

---

### 2.2 Validación del área de protección

#### 2.2.1 Medida de protección del logo (M sola) (Guía de marca. Pág. 23)

Es fundamental respetar el área de protección del logotipo para garantizar una comunicación clara y de calidad.

- Para generar aire alrededor de la M, se construye un **cuadrado** tomando como referencia el ancho de la propia M.  
- Ningún elemento gráfico o tipográfico debe invadir este espacio de protección.

#### 2.2.2 Medida de protección del lockup horizontal (Guía de marca. Pág. 33)

En el lockup horizontal:

- Partimos del área de protección de formatos mínimos.  
- Reducimos la M un **30%** y formamos un **cuadrado** con ella.  
- Esta medida define:
  - La distancia mínima entre la M y la palabra “Movistar”.  
  - La altura de la palabra “Movistar” dentro del lockup.

#### 2.2.3 Medida de protección del lockup vertical (Guía de marca. Pág. 36)

En el lockup vertical aplicamos el mismo criterio:

- Partimos del área de protección de formatos mínimos.  
- Reducimos la M un **30%** y formamos un **cuadrado** con ella.  
- Esta medida define:
  - La distancia mínima entre la M y la palabra “Movistar”.  
  - La altura de la palabra “Movistar” dentro del lockup vertical.

#### 2.2.4 Medida de protección en formatos reducidos (Guía de marca. Pág. 24)

En tamaños reducidos se permite:

1. Reducir la M un **30%** respecto a su tamaño estándar.  
2. Formar un **cuadrado** con esa M reducida.  
3. Establecer el área de protección en base a la M reducida, respetando siempre ese cuadrado como zona libre de elementos.
