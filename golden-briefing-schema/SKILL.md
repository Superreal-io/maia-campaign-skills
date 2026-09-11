---
name: Golden Briefing Schema
key: golden-briefing-schema
description: Schema canonico del Golden Briefing. Artefacto que el Strategist produce y que los Agentes B, C y D consumen como ground truth. Versionado, JSON-parseable, trazable. Un Golden Briefing por stream.
version: 3.0.0
owner: agente-a
status: active
---

# Golden Briefing Schema

El Golden Briefing es el **contrato versionado** entre el Strategist y el resto del workflow. Todos los agentes downstream lo leen. Solo el Strategist lo escribe (y solo tras aprobación en el gate humano).

Se produce **un Golden Briefing por stream**. El plan comercial mensual tiene 2 streams (Growth-Value combinado y Dispositivos), por lo que se producen 2 Golden Briefings independientes. Dentro del stream Growth-Value, Growth y Value son sub-corrientes con corrientes de demanda distintas.

## Principios

1. **JSON-parseable, no prosa**. Un humano puede leerlo, pero un agente lo consume sin ambiguedad.
2. **Versionado**. Cada cambio es una nueva versión con diff y rationale.
3. **Trazable**. Cada campo referencia su evidencia en el documento original (rango de página, parrafo o cita).
4. **Permisivo con gaps**. Los campos pueden estar vacios o marcados como `pending` con razon. La rúbrica detecta y la pregunta va al formulario.

## Schema completo (v2)

```yaml
brief:
  # Identidad
  id: "uuid-v4"
  version: 1                                # int, incremental
  previous_version: null                    # int de versión anterior o null
  case_id: "string"                         # ej. "growth-value-agosto-26"
  stream: "growth-value|dispositivos"        # obligatorio
  client: "string"                          # ej. "Movistar"
  periodo: "string"                         # ej. "Julio 2026"
  created_by: "agente-a"
  created_at: "ISO8601"

  # Documento(s) fuente
  source_documents:
    - filename: "string"
      format: "pptx|xlsx|docx|pdf|md|email"
      pages_referenced: "string"            # ej. "1-12" o "todo"
      hash: "sha256:..."

  # ── Bloque 1: Lectura estratégica ──

  foco:
    statement: "string (1-2 frases: la lectura clave del mes para este stream)"
    evidence: "string"
    status: "claro|confuso|ausente"

  lectura_ejecutiva:
    puntos:                                 # 5-7 puntos estrategicos ordenados por importancia
      - texto: "string"
        procedencia: { nivel: "string", fuente: "string", validacion: "string" }
    evidence: "string"
    status: "claro|confuso|ausente"

  arquitectura_mes:                         # sustituye a mensaje_paraguas (v3.0)
    - movimiento: "string (un verbo de negocio, derivado del briefing de ESTE mes)"
      territorios: ["string"]
      racional: "string (1 frase)"
  # PROHIBIDO: mensaje_paraguas, claim_mes, idea_unica o cualquier campo que contenga
  # una promesa verbal unica para todo el stream. Eliminado en v3.0.

  flags_dato_a_validar:                     # discrepancias dentro del propio original
    - concepto: "string"
      valor_usado: "string"
      valor_alternativo: "string"
      fuente_usada: "string"
      fuente_alternativa: "string"
      accion_sugerida: "string"

  decisiones_pendientes:
    - pregunta: "string"
      depende_de: "string"                  # quien decide (área, comunicación, director, etc.)
      bloqueante: true|false
      criterion_id: 0                       # vinculado a la rúbrica
    - ...

  # ── Bloque 2: Corrientes de demanda ──

  corrientes_demanda:                       # 2-4 corrientes por stream
    - nombre: "string"                      # ej. "Ventana de futbol", "Demanda estacional de verano"
      tipo: "ventana_temporal|estacional|lanzamiento|alianza|captación|retención"
      territorios:                          # territorios que pertenecen a esta corriente
        - nombre: "string"
          descripcion: "string (1 frase: rol estratégico)"
          detalle: "string (contexto operativo)"
      fecha_clave: "string|null"            # ej. "Desde el 15 de julio"
      validacion: "string|null"             # items pendientes de validar
      procedencia: { nivel: "plan_area|insight_estrategia|propuesta", fuente: "string", validacion: "confirmado|a_validar|no_confirmado" }
    - ...

  # ── Bloque 3: Jerarquia de territorios ──

  jerarquia_territorios:
    - territorio: "string"
      prioridad: "alta|media|apoyo|condicional"
      tipo_badge: "compra|consideración|contextual|desarrollo|upsell|estacional|viaje|hogar|captación|consumo|retención|value"
      justificacion: "string"
      condicion: "string|null"              # solo si prioridad = condicional
      procedencia: { nivel: "plan_area|insight_estrategia|propuesta", fuente: "string", validacion: "confirmado|a_validar|no_confirmado" }
    - ...

  # ── Bloque 4: Audiencia y mecánica ──

  audiencia_mecanica:
    segmentos:
      - nombre: "string"                    # ej. "No cliente, solo móvil"
        descripcion: "string"
        volumen_estimado: "string|null"
        procedencia: { nivel: "string", fuente: "string", validacion: "string" }
    modelo_segmentacion: "string"           # ej. "Modelo geolocalización (2a residencia)"
    mecanica_principal: "string"            # mecánica de activación

  # ── Bloque 5: Rol de canales ──

  rol_canales:
    - canal: "string"                       # ej. "CRM / Email", "Digital", "BTL", "M+", "Tienda", "TV", "Exterior"
      mision: "string"                      # para que sirve este canal en este stream (no solo presencia)
      notas: "string|null"                  # restricciones o aclaraciones
      procedencia: { nivel: "plan_area|insight_estrategia|propuesta", fuente: "string", validacion: "confirmado|a_validar|no_confirmado" }
    - ...

  # ── Bloque 6: Recomendación de publicidad ──

  recomendacion_publicidad:
    # Sin idea unica del mes ni claim. La coherencia del periodo vive en arquitectura_mes.
    reglas_del_mes:                         # que no puede faltar, que no puede aparecer
      - texto: "string"                     # referida a un producto, canal o timing concreto
        procedencia: { nivel: "plan_area|insight_estrategia|propuesta", fuente: "string", validacion: "confirmado|a_validar|no_confirmado" }
    condiciones_legales: "string|null"
    status: "claro|confuso|ausente"

  # ── Bloque 7: Primer paso ──

  primer_paso: "string"                     # acción concreta recomendada como siguiente paso

  # ── Campos heredados (mantenidos para trazabilidad) ──

  fechas:
    inicio: "YYYY-MM-DD | null"
    fin: "YYYY-MM-DD | null"
    hitos:
      - fecha: "YYYY-MM-DD"
        descripcion: "string"
        procedencia: { nivel: "string", fuente: "string", validacion: "string" }
    evidence: "string"
    status: "claro|confuso|ausente"

  riesgos:
    - descripción: "string"
      severidad: "alta|media|baja"
      mitigacion_sugerida: "string"
    - ...

  restricciones_mandatorios:
    - tipo: "marca|operativo|legal"
      descripcion: "string"
      procedencia: { nivel: "plan_area|insight_estrategia|propuesta", fuente: "string", validacion: "confirmado|a_validar|no_confirmado" }
      # El campo `origen` queda sustituido por `procedencia.fuente` (v3.0).
    - ...

  # Evaluación contra la rúbrica
  rubric_evaluation:
    - criterion_id: "C01"
      criterion_name: "Estrategia antes que catálogo"
      status: "cubierto|parcial|ausente"
      points: 2                             # max del criterio (2 para C01-C07, 1 para C08-C14)
      score: 2                              # points x factor (cubierto=1.0, parcial=0.5, ausente=0)
      evidence: "string"
      question_for_area: "string | null"
    - ... (uno por cada uno de los 14 criterios, total max 21 pts)

  # Estado del Brief
  approval:
    status: "draft|pending|approved|superseded"
    approved_by: "human:<email>"
    approved_at: "ISO8601"
    notes: "string"

  # Outputs vinculados (rellenado por el Strategist)
  linked_outputs:
    estrategia_one_pager: "path/al/estrategia_<stream>_v<N>.html"
    formulario_area: "path/al/formulario_area_<stream>_v<N>.docx"

  # Change log (para versiones > 1)
  change_log:
    - versión: 2
      timestamp: "ISO8601"
      changes:
        - field: "jerarquia_territorios[0].prioridad"
          from: "media"
          to: "alta"
          rationale: "Respuesta del área: dispositivo flagship se confirma como prioridad máxima"
          source: "formulario_response_2026-07-03.md"
```

## Mapeo con el schema v1 (migración)

| Campo v1 | Campo v2 | Notas |
|---|---|---|
| objetivo_comunicación | foco + lectura_ejecutiva | El objetivo se descompone en foco (1 frase) y lectura ejecutiva (puntos estrategicos) |
| contexto_negocio | Absorbido en lectura_ejecutiva.puntos | El contexto de negocio se integra como puntos de la lectura |
| públicos | audiencia_mecanica.segmentos | Estructura más rica con modelo de segmentación |
| productos_prioritarios | corrientes_demanda[].territorios | Los productos se organizan dentro de territorios y corrientes |
| mensaje_principal | arquitectura_mes | La coherencia del mes son 3-4 movimientos estrategicos, no una promesa verbal unica |
| accion_esperada | primer_paso | Más concreto y accionable |
| canales_posibles | rol_canales | Cada canal tiene mision específica, no solo presencia |
| criterios_exito | Absorbido en corrientes_demanda[].validación + riesgos | Los criterios se vinculan a las corrientes |
| (nuevo) | stream | Obligatorio: identifica a que stream pertenece el brief |
| (nuevo) | período | Mes y ano del plan |
| (nuevo) | corrientes_demanda | Estructura central nueva: agrupa territorios por tipo de oportunidad |
| (nuevo) | jerarquia_territorios | Priorización explicita de territorios con badge tipificado |
| (nuevo) | arquitectura_mes | 3-4 movimientos estrategicos que ordenan el mes. Sustituye a `mensaje_paraguas` |
| (nuevo) | flags_dato_a_validar | Discrepancias detectadas dentro del propio plan comercial |
| (nuevo) | recomendacion_publicidad | Reglas del mes para publicidad. Sin idea única ni claim: la coherencia del mes vive en `arquitectura_mes` |

## Validación

Antes de publicar un Golden Briefing, valida:

1. `id`, `versión`, `case_id`, `stream`, `client`, `período` estan presentes.
2. `stream` es uno de: growth-value, dispositivos.
3. Cada uno de los 14 criterios tiene una entrada en `rubric_evaluation` (criterion_id C01 a C14).
4. `foco.statement` no esta vacio si `foco.status` es "claro".
5. `lectura_ejecutiva.puntos` tiene entre 5 y 7 entradas.
6. `arquitectura_mes` tiene entre 3 y 4 movimientos, cada uno con al menos un territorio asignado. Todos los territorios del stream estan asignados a algun movimiento. No existe ningun campo con una promesa verbal unica para todo el stream.
6b. Toda afirmacion con valor informativo del brief tiene bloque `procedencia` con `nivel` (`plan_area|insight_estrategia|propuesta`), `fuente` concreta y `validacion` (`confirmado|a_validar|no_confirmado`). Definicion completa en la seccion 7 de `contexto-sistema-maia`.
6c. Toda cifra marcada `validacion: "a_validar"` tiene su entrada correspondiente en `flags_dato_a_validar`, y viceversa. Los dos conteos coinciden.
7. `corrientes_demanda` tiene al menos 2 entradas, cada una con al menos 1 territorio.
8. `jerarquia_territorios` tiene al menos 1 entrada con prioridad "alta".
9. `rol_canales` tiene al menos 2 entradas con `mision` no vacia.
10. Si `decisiones_pendientes` tiene entradas `bloqueante: true`, el `approval.status` no puede ser `approved` sin nota explicita del humano.
11. `source_documents` tiene al menos 1 entrada.
12. Si `versión > 1`, `previous_version` apunta a un Brief valido y hay entrada en `change_log`.
13. `linked_outputs.estrategia_one_pager` y `linked_outputs.formulario_area` apuntan a archivos existentes.
14. Todas las `evidence` referencian el documento fuente de forma trazable.

## Mantenimiento

Cambios al schema requieren:
- Incrementar `version` del SKILL.
- Actualizar el prompt del Maia Strategist (`agentes/01-strategist.md`) con el set de campos nuevos.
- Actualizar todos los Briefs existentes con migración o marcarlos `legacy`.
