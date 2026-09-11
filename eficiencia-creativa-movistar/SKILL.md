---
name: Eficiencia creativa Movistar
key: eficiencia-creativa-movistar
description: Principio de reutilizar antes que producir y framework de decision REUSE / ADAPT / REFRESH / CREATE por territorio. Define cuanto trabajo creativo nuevo hay que hacer realmente cada mes.
version: 1.0.0
owner: comunicacion-movistar
status: active
loaded_by: Maia Copywriter, Maia Campaign Manager, Maia Storyteller
---

# Eficiencia creativa Movistar

## 1. El principio

**No partimos de cero cada mes.** Priorizamos el uso de activos, códigos y formatos ya construidos y validados. La creación nueva se concentra allí donde existe una nueva necesidad de comunicación o donde los activos actuales no cumplen el objetivo.

Dicho de otra forma: reutilizar antes que producir. Si ya existe una idea, pieza, formato o recurso que ha funcionado y sigue siendo válido, se reaprovecha. La creatividad nueva se reserva para cuando cambia de verdad el problema de comunicación, el producto o el contexto.

Este principio va **antes** de toda la sección de orientación de comunicación en el documento ejecutivo, no como nota al pie. Cambia la pregunta que se hace el comité: no solo "qué vamos a comunicar" sino "cuánto trabajo nuevo hay realmente que hacer".

No tiene sentido que octubre genere una campaña nueva para todo simplemente porque empieza un mes nuevo.

---

## 2. Las cuatro decisiones

Cada territorio lleva una decisión previa, antes de cualquier orientación creativa.

| Decisión | Cuándo se aplica |
|---|---|
| REUSE | La pieza existente sigue resolviendo el objetivo y funciona en ese soporte. |
| ADAPT | La idea funciona, pero hay que actualizar fecha, oferta, producto, target o CTA. |
| REFRESH | Se mantiene el territorio o el código, pero necesita novedad o relevancia para el momento. |
| CREATE | No existe un activo válido, o el problema de comunicación ha cambiado sustancialmente. |

La decisión se toma **por territorio**, no por pieza. Un territorio puede tener matices por soporte (REUSE en digital, ADAPT en CRM), y en ese caso se declara la decisión dominante y el matiz en el racional.

---

## 3. Estado actual: la decisión es una propuesta, no un dato

El criterio para decidir qué activo merece seguir vivo, cuál hay que adaptar, cuál retirar y dónde de verdad hace falta crear algo nuevo debería basarse en datos de rendimiento de los activos existentes.

**Hoy el sistema no dispone de esos datos.** No existe un inventario consultable de activos Movistar vivos ni de su rendimiento histórico. Mientras esa fuente no exista:

1. La decisión REUSE / ADAPT / REFRESH / CREATE se emite siempre con `nivel: propuesta` y `validacion: no_confirmado` (ver sección 7 de `contexto-sistema-maia`).
2. El racional es cualitativo y explícito: por qué se cree que ese activo sigue vivo, qué señal lo respalda.
3. **Está prohibido presentar la decisión como basada en datos.** Nada de "según el rendimiento histórico" ni "los datos indican" mientras no haya inventario. Presentar un juicio cualitativo como decisión basada en datos es exactamente el problema que este sistema intenta resolver.
4. Cada decisión lleva un campo `necesita_validacion_inventario: true` que el Maia Campaign Manager cuenta y reporta en el cierre.

Cuando exista el inventario de activos, esta sección se sustituye por el criterio basado en datos y las decisiones podrán emitirse con `validacion: confirmado`.

---

## 4. Señales cualitativas admisibles

Sin datos de rendimiento, estas son las señales que sí se pueden usar para argumentar una decisión, siempre etiquetadas con su procedencia:

- **El propio plan comercial plantea continuidad.** Si la PPT del área habla de continuidad de formatos y espacios en lugar de reinvención, es señal de REUSE o ADAPT (`nivel: plan_area`).
- **Existe una campaña de marca viva que el plan pide conectar.** Si el plan pide explícitamente enganchar el BTL con una campaña de TV en emisión, es REUSE del código de campaña más ADAPT al servicio concreto (`nivel: plan_area`).
- **El territorio funcional está establecido pero el problema de octubre es nuevo.** Si el mensaje base sigue siendo válido y lo que cambia es una fricción concreta a resolver, es ADAPT o REFRESH (`nivel: propuesta`).
- **Hay códigos de producto o campaña ya construidos.** Si el territorio se apoya en códigos que el mercado ya reconoce, la tarea es orquestar y actualizar, no producir un universo nuevo (`nivel: propuesta`).
- **El producto o el contexto competitivo ha cambiado de verdad.** Solo aquí CREATE está justificado (`nivel: plan_area` si el cambio viene declarado, `insight_estrategia` si viene de trend flash o mercado).

Una decisión CREATE sin ninguna de estas señales que la respalde es la que más escrutinio necesita. El sesgo por defecto del sistema es hacia REUSE.

---

## 5. Schema

```json
"decision_produccion": {
  "decision": "REUSE | ADAPT | REFRESH | CREATE",
  "activo_referencia": "string | null",
  "racional": "string (2-3 frases: que senal respalda esta decision)",
  "matiz_por_soporte": "string | null",
  "necesita_validacion_inventario": true,
  "procedencia": {
    "nivel": "propuesta",
    "fuente": "Recomendacion Maia Copywriter",
    "validacion": "no_confirmado"
  }
}
```

El campo `activo_referencia` nombra el activo, código o campaña que se reutiliza, con el nombre que usa el equipo de Movistar. Es `null` solo cuando la decisión es CREATE.

---

## 6. Cómo lo usa cada agente

**Maia Copywriter.** Emite la decisión por territorio antes de escribir la orientación de comunicación. La decisión condiciona la orientación: un territorio en REUSE no necesita "por dónde explorar", necesita decir qué activo se reactiva y qué se ajusta.

**Maia Campaign Manager.** Verifica que todo territorio lleva decisión, que ninguna se presenta como basada en datos, y cuenta cuántas tienen `necesita_validacion_inventario: true` para el resumen de cierre.

**Maia Storyteller.** Renderiza el principio de eficiencia creativa arriba de la sección de orientación, y la decisión por territorio en la sección de producción, agrupada por tipo de decisión para que el comité vea de un vistazo cuánto trabajo nuevo hay.

---

## 7. Dependencia pendiente

Esta skill está operativa pero incompleta. Le falta la fuente que la haría rigurosa: un inventario de activos Movistar vivos (códigos de campaña, territorios construidos, piezas y formatos en uso) con datos de rendimiento asociados. Ese inventario lo tiene que aportar el cliente; no se puede reconstruir desde los outputs de MAIA.

Mientras no exista, el sistema opera con el modo degradado de la sección 3 y lo declara abiertamente en el documento.
