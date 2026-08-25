# Matriz de contraste WCAG — paleta Movistar

Parte del Brand Guardian v4 (spec autoritativa, 2026-06-08; antes §6 del documento monolítico). La paleta Movistar cumple los ratios de contraste WCAG; estas tablas indican qué combinaciones son accesibles y cuáles están prohibidas.

## Niveles de ratio (criterio Movistar)
- **AAA:** contraste mínimo **7:1**. Completamente accesible.
- **AA:** contraste mínimo **4.5:1**. Accesible para titulares > 16 pt, iconos y grafismos.
- **A:** contraste mínimo **3:1**. Accesible para titulares > 24 pt, iconos y grafismos.

## Colores semánticos (estado regular y hover)
El Azul Movistar es el acento para acciones principales; mostaza para alertas; rojo para mensajes negativos; verde para confirmaciones/feedback positivo.

| Rol      | Hex regular | Hex hover |
| -------- | ----------- | --------- |
| Acento   | `#0066ff`   | `#005eeb` |
| Positivo | `#048239`   | `#036d30` |
| Alerta   | `#926c00`   | `#745600` |
| Negativo | `#c10000`   | `#ad0000` |

> Los colores regulares se usan en estado por defecto; los hover en estados interactivos (cursor sobre botón o enlace).

## Matriz de contraste de color (WCAG)
Nivel de conformidad WCAG para combinaciones entre elementos gráficos y fondos. **"Prohibido"** = no alcanza el contraste mínimo recomendado.

| Elementos gráficos (hex) | Fondo Azul Movistar | Fondo Negro Movistar | Fondo Blanco Movistar | Fondo Azul claro | Fondo Verde claro | Fondo Amarillo claro | Fondo Coral claro |
| ------------------------ | ------------------- | -------------------- | --------------------- | ---------------- | ----------------- | -------------------- | ----------------- |
| `#0066ff`                | —                   | A                    | AA                    | A                | A                 | A                    | A                 |
| `#262423`                | A                   | —                    | AAA                   | AAA              | AAA               | AAA                  | AAA               |
| `#fffaf5`                | AA                  | AAA                  | —                     | Prohibido        | Prohibido         | Prohibido            | Prohibido         |
| `#d3eeff`                | A                   | AAA                  | Prohibido             | —                | Prohibido         | Prohibido            | Prohibido         |
| `#cef7bf`                | A                   | AAA                  | Prohibido             | Prohibido        | —                 | Prohibido            | Prohibido         |
| `#ffe99c`                | A                   | AAA                  | Prohibido             | Prohibido        | Prohibido         | —                    | Prohibido         |
| `#ffc5a8`                | A                   | AAA                  | Prohibido             | Prohibido        | Prohibido         | Prohibido            | —                 |

## Lectura clave
- **Negro Movistar `#262423`** sobre cualquier fondo claro = AAA: es el color de texto más seguro sobre claros.
- **Blanco Movistar `#fffaf5`** y los **secundarios claros** (`#d3eeff` `#cef7bf` `#ffe99c` `#ffc5a8`) sobre fondos claros = **Prohibido**: nunca texto/grafismo claro sobre fondo claro.
- **Azul Movistar `#0066ff`** sobre Blanco = AA (vale para titulares > 16 pt e iconos), pero solo A sobre fondos de color: cuidado con cuerpo de texto pequeño.
