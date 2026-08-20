---
name: Checklist de Validación MAIA
key: validacion-maia-checklist
description: 17 criterios de validación del sistema MAIA. Los usa el Campaign Manager en Cierre como capa de control de calidad transversal.
version: 2.0.0
owner: system
status: active
---

# Checklist de Validación MAIA

Cargada por el Campaign Manager. Define los 17 criterios de validación que el Campaign Manager ejecuta en Cierre (post-Art Director) sobre el paquete completo de la campaña.

Esta skill formaliza la "Validación MAIA": una capa de control transversal que cruza todos los outputs de todos los agentes en un único paso final.

---

## Criterios de validación

### Cierre (post-Art Director, sobre el paquete completo)

El Campaign Manager evalúa el paquete completo (brief + estrategia + estrategia creativa + mockups) contra estos 17 criterios:

| # | Criterio | Que verificar | Fuente |
|---|---|---|---|
| V01 | Coherencia con principios por canal | Cada campaña tiene check_principios. Ningun pasa_global: false sin justificación valida. | channel-playbook-* |
| V02 | Coherencia con CRM | Si hay email/CRM, respeta los principios del canal: idea dominante, CTA único, personalización no invasiva. | channel-playbook-email |
| V03 | Coherencia con tienda | Si hay tienda, respeta los principios: reducir ansiedad, no folleto, soportes con mision única. | channel-playbook-tienda |
| V04 | Coherencia con Movistar+ | Si hay M+, los formatos se usan según su rol (banner =/= preroll =/= First Impression). No como inventario genérico. | channel-playbook-movistarplus |
| V05 | Coherencia con digital | Si hay digital, cada pieza sabe en que fase del funnel esta. No todo es performance. | channel-playbook-digital |
| V06 | Coherencia de funnel y segmentos | La fase de funnel del briefing corresponde con los canales activados y la presión propuesta. La `segmentacion_creativa` de C cubre todos los `segmentos_operativos` de B sin omisiones ni invenciones. | matriz-objetivo-canal, campaign-output-format |
| V07 | Coherencia de marca | Los copies respetan tono y voz. No hay retailización de marca en fases altas del funnel. | brand-voice-movistar, tesis-estratégica-movistar |
| V08 | Nivel de presión y reglas heredadas | La presión comercial por canal es proporcional al valor aportado y al momento mental del cliente. Las `reglas_presion_heredadas` de C son copia literal de las `reglas_presion_comercial` de B. Si C propuso desviaciones, estan documentadas en `desviaciones_propuestas` con justificación. | tesis-estratégica-movistar, campaign-output-format |
| V09 | Frecuencia | Hay frecuencia definida por canal. No hay canales sin limite de impactos. | reglas-planner-movistar (P08) |
| V10 | Riesgo de saturación | No hay acumulación excesiva de canales sobre el mismo cliente en el mismo período. | journey-canales-movistar |
| V11 | Contradicciones entre canales | No hay mensajes contradictivos entre canales ni canibalización evidente. Coherencia con principios transversales de orquestación. | channel-playbook-transversales, Análisis cross-canal |
| V12 | Mandatorios de marca | Restricciones de marca y operativas del brief se respetan en el output final. | brief + brand-visual-guidelines-movistar |
| V13 | Identidad visual | Los mockups (HTML, imagen, otros) usan colores, tipografías y espaciados de brand-visual-guidelines-movistar. | brand-visual-guidelines-movistar |
| V14 | Calidad de pieza | Cada pieza tiene rationale, los placeholders estan documentados, los mockups son editables o tienen dimensiones reales del soporte. | Inspección directa |
| V15 | Calendario integrado | El `calendario_integrado` de C concreta la `secuencia_sugerida` de B. Hay al menos una entrada por semana del período. No hay semanas vacias sin justificación ni acumulación excesiva en una sola semana. | campaign-output-format |
| V16 | Tesis estratégica | La `tesis_estrategica` de C es coherente con la `idea_dominante` de B y el `foco` y `mensaje_paraguas` del brief. Todos los territorios de campaña se conectan con la tesis. | campaign-output-format, golden-briefing-schema |
| V17 | Copy prototype y scoring CRM | Cada campaña tiene `copy_prototype` por canal activo con `notas_para_d` no vacias. Cada pieza tiene `scoring_crm` con score calculado correctamente (base_60 + modulacion_40 = score). Scores < 70 tienen flag correspondiente con severidad media. El `tema_a_vigilar` es específico de la pieza, no genérico. | campaign-output-format |

---

## Como aplicar

1. El Campaign Manager recorre la tabla en orden. Para cada criterio, marca: OK, FLAG (con descripción), o NO_APLICA.
2. Los flags se incluyen en el resumen ejecutivo de cierre en el bloque correspondiente ([B1]-[B6]).
3. Si un criterio requiere cargar una skill que el Campaign Manager no tiene en ese momento, la carga antes de evaluar.
4. Un flag en V01-V07 puede ser bloqueante si contradice un principio sin justificación. V08-V11 son generalmente flags de riesgo (no bloqueantes por si solos).

---

## Relación con el self-check del Campaign Manager

Esta checklist complementa el self-check que el Campaign Manager ejecuta antes de publicar el resumen ejecutivo. El self-check verifica que el resumen refleja correctamente los datos; esta checklist verifica que los datos son correctos contra los principios del sistema.
