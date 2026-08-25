# Tipografía — Brand Guardian v4 (Movistar)

> Parte del Brand Guardian v4 (spec autoritativa, 2026-06-08). Numeración de sección (`3.x`) conservada
> para continuidad con citas previas. Ver `movistar-brand-guidelines-v1/SKILL.md` para el índice general.

## 3. Tipografía

### 3.1 Validación de la tipografía

#### 3.1.1 Movistar Sans (Guía de marca. Pág. 94, 95, 96, 97, 98 y 99)

Movistar Sans es nuestra tipografía corporativa: con licencia exclusiva, internacional y perpetua.  
Es una tipografía variable que incluye 5 pesos estáticos con sus versiones itálicas. Dispone de funciones OpenType, amplio soporte de idiomas, más de 800 caracteres y archivos en formatos `.ttf`, `.otf`, `.woff` y `.woff2`.

La tipografía cuenta con un conjunto completo de caracteres que cubre todas las necesidades de comunicación de la marca: letras, números, signos de puntuación y símbolos esenciales. Esto garantiza versatilidad, funcionalidad y coherencia en cualquier aplicación, idioma o contexto.

La morfología de los caracteres toma inspiración directa de la M de Movistar. Curvas, terminales y detalles formales mantienen una coherencia visual que refuerza la identidad de marca.

> 🛠 **Gotcha con los ficheros de `assets/fonts/` — lee esto ANTES de embeber la fuente.**
> Los ficheros se llaman `MovistarSans-Regular.ttf`, `-Bold.ttf`, etc., pero su **nombre de familia
> interno** (tabla `name`, nameID 1) es **`Movistar Sans TT`** / `Movistar Sans TT Medium` /
> `Movistar Sans TT Extrabold` — **con el sufijo “TT”**. El nombre que se usa en todas partes
> (`font-family` del CSS, `typeface` de los runs de un `.pptx`, estilos de Word) es **sin “TT”**.
>
> Si embebes el `.ttf` tal cual, el nombre interno no coincide con el que declara el documento y el
> visor **sustituye por una fuente de sistema, en silencio**. No da error: solo sale mal.
>
> - **HTML**: da igual, `@font-face` fija el `font-family` que tú digas. Ojo: en Movistar el runtime
>   inyecta la tipografía y el linter **prohíbe** `@font-face` en base64 (`check_fontface_not_pasted`).
>   Solo se embebe en una copia autocontenida para enviar fuera de SuperStudio.
> - **PDF (reportlab)**: da igual, la fuente se registra con el nombre que le pases.
> - **`.pptx` y `.docx`**: **SÍ importa**. Hay que reescribir la tabla `name` del TTF quitando el
>   “TT” antes de embeberlo. Implementación ya probada y reutilizable:
>   `movistar-pptx-v1/scripts/font_embed.py::rename_ttf_family()` (y su gotcha G1).
>
> Este detalle ha costado tiempo a dos piezas distintas de forma independiente. Compruébalo con
> `fontTools` (`TTFont(p)["name"].getDebugName(1)`), no lo deduzcas del nombre del fichero.

La familia tipográfica cuenta con cinco pesos y sus respectivas itálicas oblicuas.  
Las itálicas se utilizarán exclusivamente para resaltar palabras o conceptos clave, así como términos en otros idiomas, manteniendo claridad, énfasis y consistencia en el sistema tipográfico.

**Pesos disponibles:**

- Movistar Sans Extrabold  
- Movistar Sans Bold  
- Movistar Sans Medium  
- Movistar Sans Regular  
- Movistar Sans Light

#### 3.1.2 Movistar Sans Variable (Guía de marca. Pág. 100)

Para un mayor control y precisión tipográfica, la familia cuenta también con formato **Variable**.  
Este formato permite ajustar el peso de forma continua, afinando el diseño según las necesidades específicas de cada aplicación o soporte.
