# Contrato operativo de cualquier investigador

**Objetivo aprobado:** la única fuente canónica del propósito y alcance es [OBJECTIVE.md](OBJECTIVE.md). Este documento regula el procedimiento y no cambia el objetivo. GitHub es fuente de verdad. El mensaje **Continuá** activa un **ciclo de unidades de trabajo verificables y sucesivas dentro del mismo turno activo**, sin pedir autorización entre tareas ordinarias; cada unidad debe cerrarse y verificarse antes de comenzar la siguiente.

## Antes de actuar
1. Desde el repositorio actual, leer README.md, OBJECTIVE.md, PLAN.md, METHODOLOGY.md, STATE.json y secciones relevantes de RESEARCH.md y LOG.md; leer auditorías pendientes.
2. Confirmar que SHA de HEAD, estado y referencias sean consistentes; comprobar cambios de otros ejecutores, bloqueos, duplicaciones, evidencias o auditorías faltantes.
3. Determinar la tarea indicada por STATE.json, su relación con el hito y antecedentes ya investigados. Si falta una acción crítica, registrar bloqueo; nunca adivinar el próximo paso.
4. Formular resultado específico, criterio de aceptación y fuentes de verificación antes de ejecutar; priorizar reutilización.

## Cómo contar un resultado y decidir el avance

- Para H0 leer la [guía de decisión y registro de episodios](benchmarks/H0-DECISION-BASELINE.md). Al retomar, comprobar el identificador run/intento/episodio en la bitácora y el log original. Diferenciar preparación, inicio de ciencia, entrega, puntuación y validez. Un job verde o varios informes del mismo job no constituyen réplicas.
- Antes de lanzar una comparación fijar pregunta, factor que cambia, controles, unidad de análisis, criterio de resultado válido, tratamiento de faltantes y presupuesto total. Registrar qué decisión cambiaría con cada desenlace, incluido un resultado negativo reproducible. Aplicar [la métrica corregida](METHODOLOGY.md#5-métricas).
- Distinguir **hito Hn** (PLAN) de **hipótesis Hn** (OBJECTIVE) al registrar una tarea. El hito de enrutamiento es H2 y estudia la hipótesis H3. Medir la continuidad del agente experimental exige observarlo en episodios sucesivos.
- Un bloqueo de custodia o permisos se aplica a las operaciones y afirmaciones que dependen de él. Respetar la decisión pendiente y seguir solo una unidad independiente identificada en STATE, dentro del alcance y de los recursos autorizados.

## Ejecutar
- Ejecutar una unidad completa y comprobable **por iteración**, y encadenar las siguientes cuando su estado confirmado lo permita. Búsqueda, análisis, experimento o desarrollo según la tarea; no convertir investigaciones en programación innecesaria.
- Consultar antecedentes para evitar duplicación y clasificar evidencia A/B/C/D según METHODOLOGY.md.
- No inventar resultados, métricas, licencias, accesos, citas, recursos ni trabajo terminado. Registrar procedimiento exacto y errores.
- Mantener separados hechos, inferencias e hipótesis; evaluar desvío del objetivo antes de aceptar caminos nuevos.
- Sin gasto de recursos pagos sin autorización expresa. Código ajeno en entorno controlado; no revelar secretos.

## Continuidad sin autorización intermedia (dentro del turno)

1. Ante **«Continuá»** o **«continuá hasta necesitar mi intervención»**, empezar por `STATE.json`. **No fijar de antemano una cantidad de unidades**: ejecutar la primera y, si queda concluida con evidencias persistidas, pasar a la próxima identificada **exclusivamente por el nuevo `STATE.json` leído de GitHub**.
2. **Cada iteración es transaccional:** leer HEAD/estado/antecedentes relevantes; ejecutar sólo la unidad actual con criterio de aceptación; guardar evidencia, métricas, auditoría y LOG; leer de vuelta; escribir `STATE.json` **último** y leer de vuelta; comprobar HEAD y ausencia de conflictos. **Solamente entonces** iniciar otra iteración, releyendo HEAD y `STATE.json`. No agrupar cambios de varias tareas bajo una actualización final de estado.
3. **Continuar automáticamente** con tareas previstas o justificadas dentro de `OBJECTIVE.md` y los recursos autorizados, incluso si requieren investigar, comparar, programar o experimentar. No pedir confirmaciones rutinarias. Ante errores técnicos menores, diagnosticar y corregir de forma **acotada y documentada**, sin secuencias indefinidas de reintentos ni cambios ocultos de condiciones experimentales.
4. **Detenerse y pedir decisión/autorización** antes de: modificar objetivo o alcance; gastar en API, GPU, infraestructura u otros recursos pagos; habilitar permisos o credenciales nuevos; acceder a datos o sistemas de terceros no autorizados; alterar, borrar o publicar datos sensibles; asumir riesgos significativos; o aprobar un replanteo sustantivo que el método y los criterios vigentes no permitan resolver objetivamente.
5. **Detenerse sin declarar éxito** ante HEAD concurrente sin reconciliar, `STATE.json` incoherente no reparable con evidencia, falta de criterio verificable, bloqueo técnico relevante, pérdida de trazabilidad, o cualquier acción no ejecutable de forma segura. Explicar qué está persistido y cuál es la intervención concreta necesaria. Al cerrar un hito, auditarlo antes de avanzar; si el mismo ejecutor audita, indicar **autoverificación** y no fingir independencia.
6. Si el turno termina por límites reales de herramientas, contexto o tiempo, **cerrar la última unidad completa**, persistir el estado de recuperación y comunicar el siguiente paso. **No prometer trabajo diferido** ni ejecutar entre mensajes: este protocolo solamente rige mientras el usuario está interactuando y las herramientas están activas. La instrucción para continuar en otro turno es volver a escribir «Continuá».

## Cerrar (orden estricto)
1. Contrastar producto con criterio de aceptación; anotar fallas y resultados negativos.
2. Guardar y verificar evidencias en evidence/ o experiments/, registro fuente RESEARCH.md, avances PLAN.md (si procede), auditoría pertinente y LOG.md. Referenciar commits/paths con identificadores concretos.
3. Leer de nuevo los archivos modificados y confirmar que GitHub guarda los contenidos correctos; resolver conflictos sin sobrescribir a ciegas.
4. **Por último**, actualizar STATE.json con siguiente tarea, referencias verificadas, bloqueos y auditorías pendientes. Comprobar su lectura final. No afirmar completitud si esta actualización falla.
5. Durante el turno, comunicar hallazgos relevantes y límites sin interrumpir la cadena; **al finalizar**, resumir unidades completadas, evidencia, decisiones, bloqueos y próxima acción. Indicar qué no se comprobó.

## Auditoría por hito
Auditar pruebas, criterios, coherencia con objetivo y sesgos; decidir continuar/corregir/replantear/retroceder con historial. Preferir persona o sistema distinto del ejecutor; si lo hace el mismo agente, llamarlo **autoverificación**.

## Recuperación
Si STATE.json está ausente o contradice commits, no continuar ejecutando experimentos. Usar LOG.md, archivos y commits para reconstruir el último estado confirmado; documentar incidente y restaurar consistencia. No recuperar desde supuesta memoria del chat.

## Cambios
El objetivo y alcance en OBJECTIVE.md permanecen estables. Métodos, hipótesis operativas y tareas pueden ajustarse con evidencia, justificación y trazabilidad; cambios sustantivos del objetivo/alcance requieren aprobación del usuario. Cada tarea debe ser suficientemente pequeña para un resultado verificable, pero no subdividir sin beneficio demostrado.