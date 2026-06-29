---
name: "Channel Playbook -- Email / CRM"
key: channel-playbook-email
description: Playbook operativo del canal CRM con email como canal principal de ejecucion. Principios de relacion personalizada, estructura de mensaje, roles, riesgos y reglas para agentes.
version: 1.0.0
owner: client
status: active
channel: email
---

# Channel Playbook -- Email / CRM

Cargado por los Agentes B, C y (parcialmente) D cuando email es uno de los canales activos.

CRM es un canal de relacion personalizada, no un contenedor de inputs comerciales. Email es el canal principal de ejecucion del CRM. Todo lo que sale por email debe respetar los principios de este playbook.

---

## 1. Funcion del canal

Email/CRM cumple seis funciones dentro del ecosistema Movistar:

1. **Personalizar.** Adaptar mensaje, oferta y tono al perfil real del cliente.
2. **Activar.** Mover al cliente hacia una accion concreta y medible.
3. **Explicar con claridad.** Traducir lo complejo en algo que se entienda en tres segundos.
4. **Reconocer valor cliente.** Hacer que el usuario sienta que se le conoce, no que se le persigue.
5. **Desarrollar relacion.** Construir confianza a lo largo del tiempo, no solo en el momento de la oferta.
6. **Convertir cuando existe una base identificable.** Solo empujar venta cuando hay datos que justifiquen la propuesta.

Si un email no cumple al menos una de estas funciones, no deberia enviarse.

---

## 2. Principios clave

Estos diez principios son la base de evaluacion de cualquier pieza de email. Agentes B y C deben validar contra esta lista.

1. **Un email, una idea dominante.** Si no puedes resumir el mensaje en una frase, sobra algo.
2. **Tres segundos.** El usuario debe entender el mensaje en tres segundos. Si necesita leer dos veces, fallo de estructura.
3. **El hero manda.** La imagen principal define el mensaje. Si el hero no cuenta la historia por si solo, el email no funciona.
4. **Menos productos, mas curaduria.** No es catalogo. Selecciona, prioriza, recomienda.
5. **CTA unico.** Un solo llamado a la accion por email. Si hay dos CTAs compitiendo, elimina uno.
6. **Ventaja Personal es reconocimiento, no descuento generico.** El cliente debe sentir que la oferta existe porque se le conoce, no porque es un numero mas.
7. **Swap facilita, no protagoniza.** Swap funciona mejor como herramienta que habilita la decision, no como el mensaje central.
8. **Beneficios Movistar cierran confianza.** Son cierre de argumento, no extras acumulados. No listar beneficios como relleno.
9. **La claridad vende.** Lenguaje directo, sin rodeos, sin jerga innecesaria.
10. **Editar tambien es vender.** Quitar contenido es una decision comercial tan importante como agregarlo.

---

## 3. Estructura de un email eficaz

Un email CRM de Movistar debe seguir esta estructura logica:

| Bloque | Funcion | Regla |
|---|---|---|
| Asunto + preheader | Captar atencion y anticipar valor | Maximo 50 caracteres asunto. Sin clickbait. |
| Hero | Contar la historia visual del mensaje | Una imagen, una idea. Sin texto superpuesto ilegible en mobile. |
| Mensaje principal | Explicar la propuesta en lenguaje claro | Maximo 3 lineas de texto. Idea dominante visible. |
| Prueba o refuerzo | Dar razon para creer (RTB) | Dato, ventaja concreta, o reconocimiento de valor cliente. |
| CTA | Dirigir a una unica accion | Boton visible, texto de accion ("Activa tu plan", "Conoce tu oferta"). |
| Footer legal | Cumplimiento normativo | Solo lo obligatorio. No agregar mensajes comerciales aqui. |

No todos los bloques son obligatorios en cada pieza, pero el orden logico se mantiene.

---

## 4. Rol del CRM en el ecosistema

El CRM no compite con otros canales. Su rol especifico:

- **vs. Paid Media:** CRM habla a quien ya es cliente. Paid habla a desconocidos. No replicar mensajes de paid en CRM.
- **vs. Tienda:** CRM prepara la visita o la decision. No intenta cerrar lo que la tienda cierra mejor en persona.
- **vs. App/Web:** CRM activa y dirige trafico a destinos digitales. No duplica contenido que ya esta disponible en la app.

Regla general: CRM personaliza y activa. Los demas canales ejecutan o amplifican.

---

## 5. Riesgos y anti-patrones

Estas son las trampas mas comunes. Si un email cae en alguna, debe corregirse antes de salir.

| Anti-patron | Por que falla |
|---|---|
| Saturar con frecuencia excesiva | El cliente deja de abrir. Erosion de marca. |
| Mezclar demasiados mensajes en una pieza | Viola el principio de idea dominante. Nada aterriza. |
| Convertirse en folleto | Si parece un catalogo PDF, no es CRM. Es ruido. |
| Confundir personalizacion con presion | Usar datos del cliente para empujar venta agresiva destruye confianza. |
| Tratar al cliente como trafico | El cliente de CRM tiene nombre, historial y relacion. No es un clic anonimo. |
| Multiples CTAs compitiendo | El usuario no sabe que hacer. Resultado: no hace nada. |
| Hero generico o desconectado del mensaje | La imagen no comunica. El email pierde su arma principal. |
| Asunto que promete lo que el email no cumple | Clickbait destruye tasa de apertura futura. |

---

## 6. Cadencia y presion

Reglas de contacto para evitar saturacion:

- **Maximo semanal por cliente:** evaluar caso a caso, pero como regla base no mas de 2 envios semanales al mismo segmento.
- **Cooldown post-compra:** cliente que acaba de contratar no recibe oferta del mismo tipo por minimo 15 dias.
- **Exclusion por inactividad:** si un cliente no abre en 3 envios consecutivos, reducir frecuencia o cambiar enfoque antes de seguir.
- **Prioridad de mensajes:** si hay dos campanas activas para el mismo segmento, gana la que tiene mayor personalizacion, no la que tiene mayor urgencia comercial.

La presion comercial es el enemigo silencioso del CRM. Mas envios no significa mas conversion.

### Regla de presion por valor cliente

La presion BTL debe ser proporcional al valor del cliente. Un cliente de ARPU alto (300 euros o mas) tolera menos ruido y espera mas relevancia. Un cliente de ARPU bajo puede necesitar mas frecuencia pero con mayor precision en la oferta.

Regla practica: si dudas entre enviar o no enviar, pregunta "este email aporta valor al cliente o solo aporta volumen a la campana?" Si la respuesta es volumen, no enviar.

### Canales BTL mas alla de email

Estos principios aplican a todos los canales BTL, no solo email:

- **SMS**: reservado para urgencia real o confirmaciones. Un SMS comercial generico destruye la credibilidad del canal.
- **RCS**: permite interaccion rica pero no es excusa para saturar. Mismo principio de idea unica.
- **Push (app)**: el usuario controla si las acepta. Cada push irrelevante acerca al "desactivar notificaciones".
- **Banners descodificador**: impacto en contexto de ocio. No tratar como display generico.

En todos los casos: un contacto, una idea. La fragmentacion de canales BTL no es excusa para multiplicar impactos sobre el mismo cliente.

---

## 7. Ventaja Personal y Swap

Dos mecanismos que aparecen frecuentemente en campanas Movistar y requieren tratamiento especifico.

### Ventaja Personal

- Es reconocimiento, no descuento.
- Debe presentarse como algo que el cliente se ha ganado por su relacion con Movistar.
- Nunca presentar como "oferta generica disponible para todos".
- El lenguaje debe hacer sentir exclusividad real: "Para ti", "Porque llevas X tiempo con nosotros", "Tu ventaja".
- Si Ventaja Personal no aporta diferenciacion real, mejor no incluirla. Un descuento generico disfrazado de personalizacion es peor que no personalizar.

### Swap

- Es facilitador, no protagonista.
- Swap funciona cuando resuelve una friccion: "Cambia tu equipo sin complicaciones", "Renueva sin costo adicional".
- No debe ser el titular ni el hero del email. Debe aparecer como mecanismo que hace posible la oferta principal.
- Si Swap se convierte en el mensaje central, el email pierde foco. La propuesta de valor va primero; Swap es el "como".

---

## 8. Checklist rapido para agentes

Antes de dar por buena una pieza de email, validar:

- [ ] Tiene una sola idea dominante?
- [ ] Se entiende en tres segundos?
- [ ] El hero cuenta la historia sin necesidad de leer el texto?
- [ ] Hay un unico CTA claro y visible?
- [ ] Ventaja Personal se siente como reconocimiento, no como descuento?
- [ ] Swap facilita en vez de protagonizar?
- [ ] Los beneficios Movistar cierran confianza sin acumularse?
- [ ] No hay mas de un mensaje comercial competiendo?
- [ ] El tono es directo, claro, sin jerga?
- [ ] Se ha editado lo que sobra?

Si alguna respuesta es "no", la pieza necesita revision.

---

## Como usan los agentes este playbook

- **Mix Media Planner (Estrategia):** lo carga si email esta en `canales_posibles`. Usa las funciones (seccion 1) para definir el rol del email en la campana y los principios (seccion 2) para evaluar si el mensaje propuesto es viable por este canal.
- **Creative Strategist (Builder):** lo carga para escribir copies que cumplan la estructura (seccion 3), validar contra anti-patrones (seccion 5) y aplicar el checklist (seccion 8) antes de entregar.
- **Visual Designer (Design):** lo carga para asegurar que el hero manda, que el CTA es unico y visible, y que la pieza no se convierte en folleto visual.
