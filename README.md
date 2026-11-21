# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR; aún sin score científico LLM válido.** Qwen3 1.7B completó trayectorias SciResearch sin `submit`; Qwen3 4B Instruct2507 Q4 validó llamadas a herramientas y uso seguro de memoria con límite8GiB. [T0.45](evidence/T0.45-qwen4b-original-science-timeout-no-score-2026-11-20.md) fue censurada por science timebox360s sin summary. [T0.46](evidence/T0.46-timeout-heartbeat-offline-2026-11-20.md) validó heartbeat por turnos/requests. **[T0.47](evidence/T0.47-qwen4b-science-first-request-timeout-2026-11-21.md)** inició el primer request real SciResearch dev con un nuevo timebox600s, pero el **adapter agotó su propio timeout90s** antes de completar un turno; heartbeat y summary recuperados, 0 herramientas/turnos completados, grader sin `submit` y **score=null**, [run44855889008](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44855889008). Cgroup max/oom/oomkill=0 bajo actor8GiB. **D-0055/T0.48:** auditar offline primera request, timeout del adapter, métricas/costo/latencia antes de otro experimento; 0 API paga/GPU, H0 abierta y H1/H2 no iniciados. [STATE](STATE.json).

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