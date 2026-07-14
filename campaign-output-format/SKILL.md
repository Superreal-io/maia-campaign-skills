---
name: Campaign Output Format
key: campaign-output-format
description: Schema canónico de los artefactos que producen los Agentes B y C -- Estrategia por Canal (B) y Estrategia Creativa (C). Define formato, validación y trazabilidad al Golden Briefing.
version: 2.0.0
owner: system
status: active
---

# Campaign Output Format

Este skill define dos artefactos principales y los outputs visuales asociados:

1. **Estrategia por Canal** (`media_strategy.json`) -- output del Planner. Acompanado de `media_strategy_v<N>.docx` (narrativo visual) y 8 one-pagers HTML: `calendario_<subcorriente>_v<N>.html` y `brief_canales_<subcorriente>_v<N>.html` para cada sub-corriente (Growth, Value, Dispositivos), mas 2 globales: `calendario_canales_global_v<N>.html` y `carga_soporte_global_v<N>.html`.
2. **Estrategia Creativa** (`campaign_creative-strategy.json`) -- output del Creative Copywriter. Acompanado de `campaign_creative-strategy_v<N>.docx` (narrativo visual) y `campaign_creative-strategy_v<N>.html` (mapa de territorios creativos). Las campanas se agrupan por sub-corriente (Growth, Value, Dispositivos).

Todos los JSON-parseables, versionados, trazables al Golden Briefing del que dependen.

---

## 1. Estrategia por Canal -- output del Planner

```yaml
media_strategy:
  # Identidad
  id: "uuid-v4"
  version: 1
  brief_id: "uuid-del-brief"                 # FK a brief.id
  golden_briefing_version: 1                           # FK a brief.version
  case_id: "string"
  created_by: "agente-b"
  created_at: "ISO8601"

  # Priorizacion de territorios (obligatorio si >10 territorios, opcional si menos)
  priorizacion_territorios:
    - territorio: "string"
      bloque: "P1|P2|apoyo_tactico|revisar"
      justificacion: "string"

  # Comentarios expertos (maximo 3, solo cuando aportan valor real)
  comentarios_expertos:
    - observacion: "string (dato concreto detectado)"
      por_que_importa: "string (consecuencia si no se actua)"
      recomendacion: "string (accion concreta)"

  # Resumen ejecutivo (para humano de Comunicacion / Campaign Manager)
  executive_summary:
    sintesis: "string (3-5 frases)"
    foco_recomendado: "string (1 frase)"
    canales_activos: ["email", "display", "tienda"]
    ajustes_propuestos_al_brief: 
      - field: "publicos[0].prioridad"
        propuesta: "Subir a prioridad principal"
        razon: "El playbook de Meta indica que este público responde mejor en ese canal y debería ser cabecera"
        bloqueante: false
    decisiones_pendientes_remanentes:
      - pregunta: "string"
        depende_de: "string"

  # Tabla de Territorios y Medios (columnas fijas Movistar)
  tabla_territorios_medios:
    - territorio: "string"
      bloque_prioridad: "P1|P2|apoyo_tactico|revisar"
      rol_estrategico: "string (tier + funcion en 1 linea)"
      audiencia_segmento: "string"
      mensaje_principal: "string"
      crm_btl: "string|null (activacion, cadencia, presion)"
      movistar_plus: "string|null"
      digital: "string|null"
      tienda_plv: "string|null"
      otros_medios: "string|null"
      comentario_estrategico: "string|null"

  # Tabla de Calendario (columnas fijas Movistar)
  tabla_calendario:
    - semana_ventana: "string (rango de fechas)"
      territorio: "string (territorio(s) activos)"
      objetivo: "string"
      mensaje: "string"
      canales_principales: ["string"]
      presion: "baja|media|alta"
      dependencias: "string|null"

  # Detalle por canal
  channels:
    - channel: "email"
      origen: "briefing|Recomendacion Planner"   # etiqueta de inferencia
      funcion: "string (papel del canal en esta campaña)"
      mensaje_a_priorizar: "string (del Brief)"
      mensaje_descartado: 
        - mensaje: "string"
          razon: "string (por qué no en este canal)"
      no_meter:
        - "elemento concreto que NO debe aparecer"
      cadencia:
        n_piezas: 4
        frecuencia: "semanal"
        ventana: "2026-06-01 a 2026-06-30"
        justificacion: "string"
      publicos:
        - nombre: "string (del Brief)"
          que_recibe: "string (subset del mensaje)"
      racional: "string (2-3 frases -- por qué esta recomendación)"
      kpis:
        - metrica: "string"
          target: "string|number"
      check_principios:
        - principio_id: "email-frecuencia"
          pasa: true|false|"no_evaluable"    # no_evaluable cuando la skill está en skeleton
          razon: "string | null"             # obligatorio si pasa: false o no_evaluable
        - principio_id: "email-cta-unico"
          pasa: true|false|"no_evaluable"
          razon: "string | null"
      check_principios_resumen:
        evaluables: 2                        # n principios con skill poblada
        no_evaluables: 0                     # n principios contra skill skeleton
        pct_evaluable: 100                   # % de checks con skill real

    - channel: "display"
      # ... mismo schema ...

  # Handoff a Creative Copywriter (bloque obligatorio)
  handoff_to_c:
    objetivo_principal: "string (1 frase -- objetivo real diagnosticado)"
    fase_funnel: "upper|mid|lower|loyalty|service"
    territorio_principal: "string"
    territorios_secundarios: ["string"]
    idea_dominante: "string (frase madre que ordena la campana)"
    audiencia_principal: "string (target + relacion con Movistar)"
    segmentos_operativos:
      - nombre: "string (ej. Clientes sin 1RTR)"
        tamano_estimado: "string|null (ej. 1,0M)"
        situacion: "string (estado del cliente)"
        rol_crm: "string (oportunidad que representa)"
        territorios_prioritarios: ["string"]
        presion_recomendada: "baja|media|media-alta|alta"
        presion_justificacion: "string"
    reglas_presion_comercial:
      - regla: "string (ej. Maximo 2 impactos comerciales por cliente/semana)"
        aplicacion: "string (cuando y como se aplica)"
    canales_principales: ["string"]
    canales_apoyo: ["string"]
    canales_condicionados:
      - canal: "string"
        restriccion: "string"
    canales_no_recomendados:
      - canal: "string"
        motivo: "string"
    presion_por_canal:
      - canal: "string"
        nivel: "baja|media|media-alta|alta"
        justificacion: "string"
    cta_principal: "string"
    secuencia_sugerida: "string (journey de impactos)"
    reglas_criticas: ["string"]
    recomendaciones_creativas: "string"
    riesgos: ["string"]

  # Aprobacion
  approval:
    status: "draft|pending|approved|superseded"
    approved_by: "human:julian@superreal.io | director"
    approved_at: "ISO8601"
    notes: "string"

  # Trazabilidad
  linked_outputs:
    campaign_creative-strategy: "path/al/campaign_creative-strategy.json"      # rellenado por Creative Copywriter
```

### Validación de la Estrategia por Canal

1. `brief_id` y `golden_briefing_version` referencian un Brief existente y aprobado.
2. `executive_summary.canales_activos` ⊆ canales listados en `brief.rol_canales`.
3. Cada canal en `channels` tiene un playbook cargado correspondiente.
4. Cada `mensaje_a_priorizar` es coherente con `brief.lectura_ejecutiva.mensaje_paraguas` y los territorios del brief.
5. Cada `check_principios[].pasa: true` puede ser auditado por el Campaign Manager cargando los `channel-playbook-*` correspondientes.
6. Si una skill referenciada tiene `status: skeleton-pending-content`, el check correspondiente DEBE ser `no_evaluable`, nunca `true`. Los agentes no validan contra contenido que no existe.
7. El `check_principios_resumen.pct_evaluable` debe aparecer en el resumen ejecutivo de la entrega. Si es inferior al 50%, se flaggea como riesgo.
8. Si hay `ajustes_propuestos_al_brief` bloqueantes, se registran como flag de severidad alta para revisión del Campaign Manager en el gate post-C (ver política de gates del Campaign Manager).

### Outputs visuales de B (one-pagers por stream)

Ademas del JSON y el .docx, el Planner produce 8 one-pagers HTML (6 por sub-corriente + 2 globales):

**Por sub-corriente** (Growth, Value, Dispositivos):

| Archivo | Contenido |
|---|---|
| `calendario_<subcorriente>_v<N>.html` | Gantt semanal: territorios x semanas, barras coloreadas por sub-corriente, chips de medios |
| `brief_canales_<subcorriente>_v<N>.html` | Matriz: territorios x canales (TV, Exterior, M+, BTL, Digital, Tienda PLV, Tienda Caballete), checks azules con especificacion |

**Globales** (consolidan las 3 sub-corrientes):

| Archivo | Contenido |
|---|---|
| `calendario_canales_global_v<N>.html` | Gantt cross-stream + matriz de canales cruzada. Detecta solapes de presion entre sub-corrientes. |
| `carga_soporte_global_v<N>.html` | Heatmap semanal de carga por canal. Detecta picos criticos y sugiere redistribucion. |

Versionado: comparten version con el JSON y el .docx. Paleta: identidad Movistar (#0066FF, #262423, #6F7176, #F5F7FA, #FFFFFF) + colores de sub-corriente (verde #00C48C Dispositivos, azul #0066FF Growth, morado #8B5CF6 Value). Tipografia: system-ui.

---

## 2. Estrategia Creativa -- output del Creative Copywriter

```yaml
campaign_creative-strategy:
  # Identidad
  id: "uuid-v4"
  version: 1
  brief_id: "uuid-del-brief"
  media_strategy_id: "uuid-de-la-estrategia"
  case_id: "string"
  created_by: "agente-c"
  created_at: "ISO8601"

  # ── Nivel 1: Marco estrategico (1 por ciclo) ──
  marco_estrategico:
    tesis_estrategica: "string (idea rectora que conecta todos los territorios)"
    ajuste_rector:                               # null si no hay ajuste
      descripcion: "string (que cambia y por que)"
      tipo: "ajuste_propuesto"
      severidad: "alta|media"
    segmentacion_creativa:
      - segmento: "string (nombre del segmento de B)"
        territorios: ["string"]
        angulo: "string (enfoque creativo para este segmento)"
        tono: "string (ej. aspiracional, racional, urgencia)"
    calendario_integrado:
      - semana: "string (ej. Semana 1 - 2-8 junio)"
        impactos_principales: "string (envios/piezas clave de esa semana)"
        objetivo_semana: "string"
    reglas_presion_heredadas:                    # copia literal de B
      - regla: "string"
        aplicacion: "string"
      desviaciones_propuestas:                   # solo si C detecta inviabilidad
        - regla_original: "string"
          propuesta: "string"
          justificacion: "string"
    fase_funnel: "upper|mid|lower|loyalty|service"   # heredada de B

  # ── Nivel 2: Campanas por sub-corriente y territorio ──
  campaigns:                                       # agrupadas por sub_corriente
    - id: "uuid"
      sub_corriente: "growth|value|dispositivos"   # obligatorio
      slug: "string-corto-para-rutas"              # ej. "apple-swap-junio-26"
      nombre: "string (descriptivo)"
      canales: ["email", "display"]            # uno o varios coherentes
      audiencia:
        segmento: "string (nombre del segmento de B)"
        criterio_adicional: "string|null (refinamiento de C si aplica)"
      mensaje_principal: "string (uno solo)"
      
      idea_creativa:
        territorio: "string (idea madre)"
        descripcion: "string (2-3 frases)"
        referencias: ["url o ejemplo si lo hay"]
      
      rol_estrategico_canal:
        - canal: "string"
          rol: "string (ej. venta directa, consideracion, recordatorio, cierre)"
      
      copies:
        - canal: "email"
          formato: "newsletter|transaccional|cross-sell"
          titular: "string"
          subtitulo: "string"
          body: "string"
          cta_principal: "string"
          cta_secundaria: "string|null"
          variantes:
            - hipotesis: "string (que testa)"
              tipo: "emocional|comercial|otro"
              titular: "string"
              cta_principal: "string"
              por_que_funciona: "string (1-2 frases)"
        - canal: "display"
          # ... mismo schema con campos especificos del canal ...
      
      formatos_recomendados:
        - canal: "email"
          formatos: ["hero + recordatorio", "push principal"]
        - canal: "display"
          formatos: ["banner 300x250", "banner 728x90"]
        - canal: "tienda"
          formatos: ["cartel A3", "pantalla digital"]
      
      ideas_visuales:
        - descripcion: "string (que se ve en la pieza)"
          referencia_visual: "string|null"
          notas_para_agente_d: "string"
      
      jerarquia:
        principal: "string (lo primero que se ve)"
        secundario: "string"
        terciario: "string"
      
      cadencia_ideal:                            # tabla detallada por semana/momento
        - momento: "string (ej. Semana 2 - martes)"
          tipo_pieza: "string (ej. push principal, email explicativo)"
          publico: "string"
          mensaje: "string"
          cta: "string"
      
      kpis:
        - metrica: "string"
          target: "string|number"
          fuente: "string"
      
      check_principios:
        - canal: "email"
          principios_evaluados:
            - id: "email-cta-unico"
              pasa: true|false|"no_evaluable"
              razon: "string | null"
          pasa_global: true|false|"parcial"
        - canal: "display"
          principios_evaluados:
            - id: "display-1-mensaje-por-pieza"
              pasa: true|false|"no_evaluable"
              razon: "string | null"
          pasa_global: true|false|"parcial"
      check_principios_resumen:
        evaluables: 3
        no_evaluables: 0
        pct_evaluable: 100
      
      formal_rules_check:
        - canal: "string"
          reglas_violadas: []
          reglas_corregidas:
            - regla: "string"
              original: "string"
              corregido: "string"
          checks_estilo:
            precios_iva: true|false
            velocidades_formato: true|false
            grafias_producto: true|false
            terminos_prohibidos: true|false
            titular_sin_punto: true|false
            emoji_max_1: true|false
            lenguaje_inclusivo: true|false
            trato_tu: true|false
      
      flags:
        - tipo: "ajuste_propuesto|riesgo|conflicto_canal"
          severidad: "alta|media|baja"
          descripcion: "string"
          accion_sugerida: "string"
      
      # ── Copy Prototype por canal (OBLIGATORIO) ──
      copy_prototype:
        - canal: "string"
          formato: "string (ej. email hero, banner 728x90, cartel A3)"
          bloques:                              # lista ordenada de arriba a abajo
            - orden: 1
              tipo: "logo|hero_image|titular|subtitulo|body|cta|legal|badge|precio|footer"
              contenido: "string (copy final asignado o descripcion si es imagen)"
              peso_visual: "string (ej. 40% del espacio, dominante, secundario)"
          notas_para_d: "string (indicaciones concretas para Art Director)"

      # ── Scoring CRM por pieza (OBLIGATORIO) ──
      scoring_crm:
        - pieza: "string (id unico de la pieza)"
          canal: "string"
          territorio: "string"
          score: 84                             # 0-100
          base_60:
            idea_dominante: 5                   # 0-6 cada uno
            tres_segundos: 6
            hero_manda: 5
            curaduria: 6
            cta_unico: 6
            ventaja_personal_reconocimiento: 4
            swap_facilita: 6
            beneficios_confianza: 5
            claridad: 6
            edicion: 5
          modulacion_40:
            coherencia_concepto: 8              # 0-10 cada uno
            especificidad_canal: 7
            gestion_riesgo: 8
            personalizacion: 7
          tema_a_vigilar: "string (1 frase -- el mayor riesgo de esta pieza)"

      # ── Nivel 3: Profundidad por pieza clave ──
      piezas_clave:
        - canal: "string"
          tipo: "string (ej. push principal, email explicativo)"
          asunto_o_titular: "string"
          preheader: "string|null"              # solo email
          alternativas:
            - texto: "string"
              por_que_funciona: "string"
          variante_emocional: "string|null"
          variante_comercial: "string|null"
          cuando_usar_cada_una: "string|null"
          razonamiento_creativo: "string (2-3 frases)"
          racional: "string (3 frases max -- por que este territorio, concepto, canal, audiencia, momento)"

  # Aprobacion
  approval:
    status: "draft|pending|approved|superseded"
    approved_by: "human:julian@superreal.io | director"
    approved_at: "ISO8601"
    notes: "string"

  # Trazabilidad
  linked_outputs:
    html_outputs_dir: "path/al/directorio/de/htmls"
```

### Validacion de la Estrategia Creativa

**Marco estrategico (Nivel 1):**

1. `brief_id` y `media_strategy_id` referencian artefactos existentes y aprobados.
2. `marco_estrategico.tesis_estrategica` no esta vacio.
3. `marco_estrategico.segmentacion_creativa` cubre todos los segmentos de `media_strategy.handoff_to_c.segmentos_operativos`. No se acepta un segmento omitido sin flag.
4. `marco_estrategico.reglas_presion_heredadas` es copia literal de `media_strategy.handoff_to_c.reglas_presion_comercial`. Cualquier desviacion debe estar en `desviaciones_propuestas` con justificacion.
5. `marco_estrategico.calendario_integrado` tiene al menos una entrada por semana del periodo de campana.
6. `marco_estrategico.fase_funnel` coincide con `media_strategy.handoff_to_c.fase_funnel` salvo flag de ajuste.

**Campanas por territorio (Nivel 2):**

7. Cada `campaigns[].mensaje_principal` es UNO solo. No se acepta una campana con 2+ mensajes principales.
8. Cada `campaigns[].canales` esta dentro de los canales activos en la Estrategia de Medios.
9. Cada `campaigns[].audiencia.segmento` referencia un segmento existente en `marco_estrategico.segmentacion_creativa`.
10. Cada `copies[]` tiene `titular` y `cta_principal` no vacios.
11. Cada `copies[].variantes[]` tiene `hipotesis` y `por_que_funciona` no vacios. No se acepta variante sin justificacion.
12. Cada campana tiene `formatos_recomendados` con al menos un formato por canal activo.
13. Cada campana tiene `cadencia_ideal` con al menos una entrada.
14. Si `check_principios[].pasa_global: false` en alguna campana, se flaggea como severidad alta para el Campaign Manager.
15. Si `check_principios[].pasa_global: "parcial"` (hay checks `no_evaluable`), el resumen ejecutivo debe declarar el porcentaje evaluable.
16. Si una campana tiene `flags[]` con severidad `alta`, el Campaign Manager decide si bloquea o acepta el riesgo.
17. `formal_rules_check` presente en cada campana con al menos un canal verificado.

**Copy Prototype y Scoring CRM:**

18. Cada campana tiene al menos 1 entrada en `copy_prototype` por canal activo.
19. Cada `copy_prototype[]` tiene al menos 3 bloques ordenados y `notas_para_d` no vacio.
20. Cada campana tiene al menos 1 entrada en `scoring_crm` por pieza principal.
21. Cada `scoring_crm[].score` es la suma de `base_60` (10 campos x 0-6) + `modulacion_40` (4 campos x 0-10). La suma debe coincidir con `score`.
22. Cada `scoring_crm[].tema_a_vigilar` no esta vacio.
23. Si `scoring_crm[].score < 70`, debe existir un flag correspondiente con severidad media.
24. Cada campana tiene `sub_corriente` con valor `growth`, `value` o `dispositivos`. Debe haber al menos 1 campana por cada sub-corriente presente en el output del Planner.

**Profundidad por pieza (Nivel 3):**

25. Cada campana tiene al menos 1 entrada en `piezas_clave` (la pieza lider del canal principal).
26. Cada `piezas_clave[]` tiene `razonamiento_creativo` y `racional` no vacios.

---

## Anti-patrones que deben detectarse en validación

- ❌ Campaña con 5 copies para el mismo formato sin variantes justificadas.
- ❌ `mensaje_principal` con conjunciones que delatan multi-mensaje (ej. "Promo X + descuento Y + Mundial").
- ❌ Estrategia que activa 5 canales pero todos con el mismo mensaje y misma cadencia (síntoma de "shotgun").
- ❌ Estrategia Creativa sin `idea_creativa` clara (solo copies).
- ❌ KPIs ambiguos ("engagement", "branding") sin métrica concreta.

---

## Ejemplos

Ver `demo/dispositivos-mayo-26/outputs/media_strategy.json` y `demo/dispositivos-mayo-26/outputs/campaign_creative-strategy.json` una vez que se pueble el demo.
