---
name: Golden Briefing Schema
key: golden-briefing-schema
description: El schema canonico del Golden Briefing. Pieza central del sistema, es el artefacto que el Brief Maker produce y que los Agentes B, C y D consumen como ground truth. Versionado, JSON-parseable, trazable.
version: 1.1.0
owner: agente-a
status: active
---

# Golden Briefing Schema

El Golden Briefing es el **contrato versionado** entre el Brief Maker y el resto del workflow. Todos los agentes downstream lo leen. Solo el Brief Maker lo escribe (y solo tras aprobacion en el gate humano).

## Principios

1. **JSON-parseable, no prosa**. Un humano puede leerlo, pero un agente lo consume sin ambigüedad.
2. **Versionado**. Cada cambio es una nueva versión con diff y rationale.
3. **Trazable**. Cada campo referencia su evidencia en el documento original (rango de página, párrafo o cita).
4. **Permisivo con gaps**. Los campos pueden estar vacíos o marcados como `pending` con razón. La rúbrica detecta y la pregunta va al formulario.

## Schema completo (v1)

```yaml
brief:
  # Identidad
  id: "uuid-v4"
  version: 1                                # int, incremental
  previous_version: null                    # int de version anterior o null
  case_id: "string"                         # ej. "dispositivos-mayo-26-2026"
  client: "string"                          # ej. "Movistar"
  area_origen: "string"                     # ej. "Dispositivos", "Comercialización", "Producto"
  created_by: "agente-a"
  created_at: "ISO8601"

  # Documento(s) fuente
  source_documents:
    - filename: "string"
      format: "pptx|xlsx|docx|pdf|md|email"
      pages_referenced: "string"            # ej. "1-12" o "todo"
      hash: "sha256:..."

  # Los 12 campos canonicos
  objetivo_comunicacion:
    statement: "string (1-2 frases)"
    evidence: "string (cita o referencia del documento fuente)"
    status: "claro|confuso|ausente"

  contexto_negocio:
    statement: "string"
    evidence: "string"
    status: "claro|confuso|ausente"

  publicos:
    - nombre: "string"
      descripcion: "string"
      prioridad: "principal|secundario|terciario"
      evidence: "string"
    - ...
    status: "claro|confuso|ausente"

  productos_prioritarios:
    - nombre: "string"
      descripcion: "string"
      prioridad: "string"
      evidence: "string"
    - ...
    status: "claro|confuso|ausente"

  mensaje_principal:
    statement: "string (1 frase)"
    alternativas: ["string", "string"]      # si el documento sugiere varios
    evidence: "string"
    status: "claro|confuso|ausente"

  accion_esperada:
    statement: "string"                     # qué queremos que haga el cliente
    evidence: "string"
    status: "claro|confuso|ausente"

  fechas:
    inicio: "YYYY-MM-DD | null"
    fin: "YYYY-MM-DD | null"
    hitos: 
      - fecha: "YYYY-MM-DD"
        descripcion: "string"
    evidence: "string"
    status: "claro|confuso|ausente"

  canales_posibles:
    - canal: "email|display|tienda|meta|movistar-plus|web|otro"
      tipo: "obligado|sugerido|opcional"
      evidence: "string"
    - ...
    status: "claro|confuso|ausente"

  riesgos:
    - descripcion: "string"
      severidad: "alta|media|baja"
      mitigacion_sugerida: "string"
    - ...
    status: "claro|confuso|ausente"

  decisiones_pendientes:
    - pregunta: "string"
      depende_de: "string"                  # quién decide (area, comunicación, director, etc.)
      bloqueante: true|false
      criterion_id: 0                       # vinculado a la rúbrica
    - ...

  criterios_exito:
    - metrica: "string"
      target: "string|number"
      fuente: "string"                      # de dónde sale el dato
    - ...
    status: "claro|confuso|ausente"

  restricciones_mandatorios:
    - tipo: "marca|operativo"
      descripcion: "string"
      origen: "string"                      # quien lo impone
    - ...
    status: "claro|confuso|ausente"

  # Evaluacion contra la rubrica
  rubric_evaluation:
    - criterion_id: "C01"
      criterion_name: "Estrategia antes que catalogo"  # debe coincidir con brief-quality-rubric
      status: "cubierto|parcial|ausente"
      points: 2                                         # max del criterio (2 para C01-C07, 1 para C08-C14)
      score: 2                                          # points x factor (cubierto=1.0, parcial=0.5, ausente=0)
      evidence: "string"
      question_for_area: "string | null"
    - ... (uno por cada uno de los 14 criterios, total max 21 pts)

  # Estado del Brief
  approval:
    status: "draft|pending|approved|superseded"
    approved_by: "human:<email>"              # siempre un humano, nunca un agente
    approved_at: "ISO8601"
    notes: "string"

  # Outputs vinculados (rellenado por el Brief Maker)
  linked_outputs:
    one_pager: "path/al/one_pager.html"
    formulario_area: "path/al/formulario_area.docx"

  # Change log (para versiones > 1)
  change_log:
    - version: 2
      timestamp: "ISO8601"
      changes:
        - field: "publicos[0].prioridad"
          from: "secundario"
          to: "principal"
          rationale: "Respuesta del área en el formulario aclaró que el target prioritario era el cluster X"
          source: "formulario_response_2026-06-03.md"
```

## Validación

Antes de publicar un Golden Briefing, valida:

1. `id`, `version`, `case_id`, `client`, `area_origen` están presentes.
2. Cada uno de los 14 criterios tiene una entrada en `rubric_evaluation` (criterion_id C01 a C14).
3. Si un campo tiene `status: "claro"`, su `statement` no está vacío.
4. Si `decisiones_pendientes` tiene entradas `bloqueante: true`, el `approval.status` no puede ser `approved` sin nota explícita del humano.
5. `source_documents` tiene al menos 1 entrada.
6. Si `version > 1`, `previous_version` apunta a un Brief válido y hay entrada en `change_log`.
7. `linked_outputs.one_pager` y `linked_outputs.formulario_area` apuntan a archivos existentes en el repo.
8. Todas las `evidence` referencian el documento fuente de forma trazable (cita exacta o `pages_referenced` específica).

## Ejemplos

Ver `demo/dispositivos-mayo-26/outputs/golden_briefing_v1.json` una vez que se pueble el demo con los outputs reales del test.

## Mantenimiento

Cambios al schema requieren:
- Incrementar `version` del SKILL.
- Actualizar `Agentes/01-brief-maker.md` con el set de campos nuevos.
- Actualizar todos los Briefs existentes con migración o marcarlos `legacy`.
