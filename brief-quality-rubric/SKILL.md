---
name: Brief Quality Rubric
key: brief-quality-rubric
description: Los 14 criterios oficiales contra los que el Strategist evalua cualquier documento de input. Scoring ponderado (max 21 pts). Fuente oficial Movistar.
version: 2.0.0
owner: briefing-maker
status: active
source: Direccion de Publicidad, Marca y Patrocinios -- documento "criterios.md" oficial
---

# Brief Quality Rubric

Principio rector: "Comunicacion edita mejor cuando recibe intencion, no solo informacion."

Cuando el Strategist recibe un documento del area (Producto, Comercializacion, Dispositivos, etc.), evalua el contenido contra estos 14 criterios. Ordenados por importancia.

## Scoring

C01-C07 son criterios criticos (2 puntos cada uno = 14 pts).
C08-C14 son criterios importantes (1 punto cada uno = 7 pts).
Total maximo: 21 puntos.

Para cada criterio, tres estados posibles:

- CUBIERTO = puntuacion completa
- PARCIAL = 50% de la puntuacion
- AUSENTE = 0 puntos

Cada campo del brief se marca adicionalmente como:

- [CUBIERTO] -- hay informacion clara
- [INFERIDO] -- se puede deducir con seguridad razonable
- [PENDIENTE] -- falta y no se puede inferir

---

## Criterios criticos (2 puntos cada uno)

### C01. Estrategia antes que catalogo

Que queremos conseguir? Por que ahora? Que problema resolvemos? Que debe entender o sentir el cliente?

**Senal de fallo:** el documento empieza por los productos, no por el objetivo.

### C02. Priorizacion clara de objetivos

Cual es el objetivo #1? Que es secundario? Que estamos dispuestos a dejar fuera?

**Senal de fallo:** varios objetivos con la misma jerarquia. Si todo es prioritario, nada lo es.

### C03. Un "por que" potente

Que queremos que cambie en la mente o comportamiento del cliente? Que percepcion queremos construir o corregir?

**Senal de fallo:** el documento describe que comunicar pero no por que eso importa al cliente.

### C04. Insights de cliente, no solo datos de negocio

Que no entiende el cliente? Que le frena o genera desconfianza? Que mensajes han funcionado antes? Que objeciones aparecen?

**Senal de fallo:** solo hay datos de sell-out o cuotas. No hay perspectiva del cliente.

### C05. Audiencia bien definida

Cliente o no cliente? Logado o no logado? Tienda, web o app? Segmento concreto?

**Senal de fallo:** "clientes Movistar" sin mas especificacion.

### C06. Accion esperada clara

Que debe hacer el cliente despues de ver la comunicacion? Entrar, preguntar, logarse, comparar, comprar.

**Senal de fallo:** el documento no especifica que accion concreta se espera.

### C07. Jerarquia de mensajes

Cual es el mensaje principal? Cual el secundario? Que es imprescindible que aparezca y que no?

**Senal de fallo:** lista de "cosas que hay que incluir" sin orden de importancia.

---

## Criterios importantes (1 punto cada uno)

### C08. Condiciones comerciales simplificadas

Que aplica exactamente? A quien? Que va a legal? Que debe entenderse sin descifrar?

**Senal de fallo:** condiciones complejas o ambiguas.

### C09. Criterio de exito compartido

Como sabremos que ha funcionado? Acordado antes de lanzar, no despues.

**Senal de fallo:** "exito" no esta definido, o se medira solo con clics.

### C10. Tension real que resolver

Que barrera existe en la mente del cliente? Que contradiccion hay que desbloquear?

**Senal de fallo:** el documento asume que el cliente esta listo para comprar.

### C11. Contexto de canal

Donde vera el cliente esta comunicacion? Que sabe ya en ese punto del funnel?

**Senal de fallo:** el documento no diferencia entre canales o pide "lo mismo para todos".

### C12. Aprendizajes anteriores

Que funciono en campanas similares? Que no repetir? Que conviene escalar?

**Senal de fallo:** brief sin memoria. Se empieza desde cero.

### C13. Decisiones tomadas, no dudas delegadas

Que entra y que no en la pieza? Que va al comercial o FAQ?

**Senal de fallo:** el documento delega decisiones editoriales a Comunicacion.

### C14. Disponibilidad para iterar

Hay tiempo para revisar antes de producir? Quien aprueba?

**Senal de fallo:** fechas de entrega sin margen de revision.

---

## Bandas de aprobacion

| Score | Estado | Accion |
|---|---|---|
| 18-21 | APROBADO | Puede pasar al Planner |
| 13-17 | CON GAPS | Completar pendientes antes de producir |
| 8-12 | INCOMPLETO | Requiere sesion con el area |
| 0-7 | RECHAZADO | Es materia prima. Reiniciar con formulario completo |

Criterios parciales = 50% de la puntuacion.

---

## Senales de alerta rapida

3 preguntas para detectar la calidad del brief antes de analizar en detalle:

1. Puedo explicar en una frase que quiere conseguir y para quien? Si no: C01, C02, C05 en riesgo.
2. Se que debe hacer el cliente despues de ver la comunicacion? Si no: C06, C07 en riesgo.
3. Hay algo que no puedo incluir porque el brief no lo resuelve? Si si: C08, C13 en riesgo.

| Senal en el input | Problema | Criterios en riesgo |
|---|---|---|
| Empieza por la lista de productos | Sin estrategia | C01, C02 |
| "Para todos los clientes" | Audiencia indefinida | C05 |
| Varios objetivos con igual peso | Sin jerarquia | C02, C07 |
| "Lo mismo que el mes pasado" | Sin aprendizaje | C03, C12 |
| Solo fechas de lanzamiento | Sin margen de iteracion | C14 |
| Solo datos de sell-out | Sin insight de cliente | C04, C10 |

---

## Mapeo criterio a campo del schema

Cada criterio alimenta uno o mas campos de `golden-briefing-schema`. Esta tabla permite al Strategist saber que campo del Brief rellenar (o marcar como gap) a partir de cada evaluacion.

| Criterio | Campo(s) del schema v2 |
|---|---|
| C01. Estrategia antes que catalogo | `foco`, `lectura_ejecutiva` |
| C02. Priorizacion clara de objetivos | `foco` (statement priorizado), `jerarquia_territorios`, `decisiones_pendientes` |
| C03. Un "por que" potente | `lectura_ejecutiva.puntos` (el "por que ahora") |
| C04. Insights de cliente | `lectura_ejecutiva.puntos` (insights), `riesgos` |
| C05. Audiencia bien definida | `audiencia_mecanica` |
| C06. Accion esperada clara | `primer_paso`, `recomendacion_publicidad` |
| C07. Jerarquia de mensajes | `lectura_ejecutiva.mensaje_paraguas`, `jerarquia_territorios` |
| C08. Condiciones comerciales simplificadas | `corrientes_demanda[].territorios`, `restricciones_mandatorios` |
| C09. Criterio de exito compartido | `corrientes_demanda[].validacion` |
| C10. Tension real que resolver | `lectura_ejecutiva.mensaje_paraguas` (la tension informa el mensaje) |
| C11. Contexto de canal | `rol_canales` |
| C12. Aprendizajes anteriores | `lectura_ejecutiva.puntos` (aprendizajes), `riesgos` |
| C13. Decisiones tomadas | `decisiones_pendientes` (lo resuelto vs. lo abierto) |
| C14. Disponibilidad para iterar | `fechas` (hitos de iteracion) |

Cuando un criterio esta AUSENTE o PARCIAL, el campo correspondiente del schema se marca con `status: "ausente"` o `status: "parcial"` y se genera la pregunta candidata para el formulario del area.

---

## Como usar la rubrica

### Evaluacion

El Strategist produce, para cada criterio, una entrada en el campo `rubric_evaluation` del Golden Briefing:

```json
{
  "criterion_id": "C01",
  "criterion_name": "Estrategia antes que catalogo",
  "status": "cubierto | parcial | ausente",
  "points": 2,
  "score": 2,
  "evidence": "El documento menciona impulsar dispositivos en junio pero no aclara si el objetivo es captacion o upgrade",
  "question_for_area": "Cual es el objetivo principal de junio: captar clientes nuevos con dispositivo o renovar el parque actual?"
}
```

Score por entrada: `points` (max del criterio) x factor (`cubierto` = 1.0, `parcial` = 0.5, `ausente` = 0). Total = suma de scores.

### Seleccion de preguntas al formulario

De todos los criterios marcados como PENDIENTE, seleccionar **maximo 5** ordenados por impacto en el score. Para cada pregunta: explicar en lenguaje sencillo POR QUE importa, no solo que falta.

Prioridad de seleccion:
1. Criterios criticos (C01-C07) marcados como AUSENTE: siempre van.
2. Criterios criticos marcados como PARCIAL: casi siempre van.
3. Criterios importantes (C08-C14) con impacto directo en el output del Planner o Creative Copywriter: van si caben.

### Regla de paso

Brief con score >= 18 puede pasar directamente al Planner.
Brief con score < 18 requiere completar pendientes (formulario al area o sesion directa).
El humano puede decidir avanzar con riesgo si el score esta entre 13-17 y los gaps no son bloqueantes.

---

## Anti-patrones

- No convertir la rubrica en un examen. La rubrica es interna del agente. El area nunca ve codigos (C01, C06), badges, scores (9/21) ni lenguaje de auditoria. Ve preguntas concretas en tono conversacional.
- No pedir todo de golpe. Si el area responde 3 de las 5 preguntas, el ciclo puede avanzar y los otros quedan como decisiones pendientes.
- No usar jerga de marketing en las preguntas. "Buyer persona" se convierte en "cliente tipico para esto". "Funnel stage" se elimina y reformula.
