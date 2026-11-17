# Contrato operativo de cualquier investigador

**Objetivo aprobado:** la única fuente canónica del propósito y alcance es [OBJECTIVE.md](OBJECTIVE.md). Este documento regula el procedimiento y no cambia el objetivo. GitHub es fuente de verdad. El mensaje **Continuá** activa una sola unidad de trabajo verificable.

## Antes de actuar
1. Desde el repositorio actual, leer README.md, OBJECTIVE.md, PLAN.md, METHODOLOGY.md, STATE.json y secciones relevantes de RESEARCH.md y LOG.md; leer auditorías pendientes.
2. Confirmar que SHA de HEAD, estado y referencias sean consistentes; comprobar cambios de otros ejecutores, bloqueos, duplicaciones, evidencias o auditorías faltantes.
3. Determinar la tarea indicada por STATE.json, su relación con el hito y antecedentes ya investigados. Si falta una acción crítica, registrar bloqueo; nunca adivinar el próximo paso.
4. Formular resultado específico, criterio de aceptación y fuentes de verificación antes de ejecutar; priorizar reutilización.

## Ejecutar
- Hacer una sola unidad completa, comprobable. Búsqueda, análisis, experimento o desarrollo según tarea; no convertir investigaciones en programación innecesaria.
- Consultar antecedentes para evitar duplicación y clasificar evidencia A/B/C/D según METHODOLOGY.md.
- No inventar resultados, métricas, licencias, accesos, citas, recursos ni trabajo terminado. Registrar procedimiento exacto y errores.
- Mantener separados hechos, inferencias e hipótesis; evaluar desvío del objetivo antes de aceptar caminos nuevos.
- Sin gasto de recursos pagos sin autorización expresa. Código ajeno en entorno controlado; no revelar secretos.

## Cerrar (orden estricto)
1. Contrastar producto con criterio de aceptación; anotar fallas y resultados negativos.
2. Guardar y verificar evidencias en evidence/ o experiments/, registro fuente RESEARCH.md, avances PLAN.md (si procede), auditoría pertinente y LOG.md. Referenciar commits/paths con identificadores concretos.
3. Leer de nuevo los archivos modificados y confirmar que GitHub guarda los contenidos correctos; resolver conflictos sin sobrescribir a ciegas.
4. **Por último**, actualizar STATE.json con siguiente tarea, referencias verificadas, bloqueos y auditorías pendientes. Comprobar su lectura final. No afirmar completitud si esta actualización falla.
5. Comunicar sucintamente resultado, evidencia, decisión y próxima acción; indicar qué no se comprobó.

## Auditoría por hito
Auditar pruebas, criterios, coherencia con objetivo y sesgos; decidir continuar/corregir/replantear/retroceder con historial. Preferir persona o sistema distinto del ejecutor; si lo hace el mismo agente, llamarlo **autoverificación**.

## Recuperación
Si STATE.json está ausente o contradice commits, no continuar ejecutando experimentos. Usar LOG.md, archivos y commits para reconstruir el último estado confirmado; documentar incidente y restaurar consistencia. No recuperar desde supuesta memoria del chat.

## Cambios
El objetivo y alcance en OBJECTIVE.md permanecen estables. Métodos, hipótesis operativas y tareas pueden ajustarse con evidencia, justificación y trazabilidad; cambios sustantivos del objetivo/alcance requieren aprobación del usuario. Cada tarea debe ser suficientemente pequeña para un resultado verificable, pero no subdividir sin beneficio demostrado.