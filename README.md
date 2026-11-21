# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR / ciencia LLM iniciada SIN SCORE.** [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) verificó la llamada real `budget_status` de Qwen3 1.7B con `reasoning_effort:none`, y primera trayectoria SciResearch con 4 tools/2 errores sin `submit`. [T0.35](evidence/T0.35-sci-llm-stop-error-source-audit-2026-11-20.md) auditó `MAX_TURNS4` + turno final; no se comprobó causa exacta de los errores. [T0.36](evidence/T0.36-eight-turns-tool-errors-no-score-2026-11-20.md) amplió **solo MAX_TURNS4→8** con tool cap4; un único run gratuito produjo 6 tools/**5 errores**, sin `submit`, score=null; [CI44849636063](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44849636063). Contador de entrada publicado 7810 excluye posibles tokens de cache; harness de parada computa cache, así que **se corrige inferencia previa de stop por turnos** como no demostrada. Modelo/scorer originales, CPU3/6GiB, GPU/API paga0; costos totales desconocidos, sin trazas crudas retenidas. D-0044 **T0.37 siguiente**: auditoría puramente documental de token-cache vs turn limits y priorización antes de otra inferencia. H0 abierta, no H1/H2. [STATE](STATE.json).

## Navegación
- [Objetivo estable, alcance y criterios](OBJECTIVE.md)
- [Estado del arte e inventario de fuentes](RESEARCH.md)
- [Plan, hitos y tareas](PLAN.md)
- [Metodología y protocolos de evaluación](METHODOLOGY.md)
- [Reglas del investigador](AGENTS.md)
- [Instrucciones para proyecto ChatGPT](PROJECT_INSTRUCTIONS.md)
- [Estado actual](STATE.json) y [bitácora](LOG.md)
- [Benchmarks](benchmarks/README.md), [experimentos](experiments/README.md), [evidencias](evidence/README.md), [auditorías](audits/README.md)

## Principios
1. Adoptar, adaptar o reproducir soluciones antes de inventar otra.
2. Separar hechos comprobados, afirmaciones externas, inferencias e hipótesis.
3. Medir validez científica, no solo éxito aparente del agente.
4. Registrar pruebas negativas, gastos, errores, recuperación y desvíos.
5. Nunca declarar completado o persistido un resultado que no se haya verificado en GitHub.

## Inicio
En un chat con acceso de lectura/escritura al repositorio, usar las instrucciones de [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) y escribir **Continuá**. La primera ejecución debe leer los archivos canónicos y realizar exclusivamente la tarea indicada en STATE.json. No hay experimentos ejecutados por este proyecto a la fecha de inicialización.