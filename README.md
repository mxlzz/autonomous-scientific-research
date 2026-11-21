# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR, todavía sin resultado científico LLM puntuado.** Qwen3 1.7B inició dos episodios SciResearch sin `submit`, y T0.38 corrigió instrumento cache/stop. Qwen3 4B Instruct2507 Q4 validó tools T0.41 y [T0.43](evidence/T0.43-qwen4b-cgroup-memory-pressure-measured-2026-11-20.md) encontró presión real en cgroup5GiB (+387 eventos max). [T0.44](evidence/T0.44-resource-choice-after-cgroup-pressure-2026-11-20.md) seleccionó cap8GiB en GitHub público gratuito. **[T0.45](evidence/T0.45-qwen4b-original-science-timeout-no-score-2026-11-20.md)** superó probe `budget_status` y memoria 8GiB (eventos max/oom/oomkill=0), inició un episodio SciResearch original dev con grader/scorer pinned, pero el monitor lo **censuró a los 361.25s por `SCIENCE_TIMEOUT`**, antes de persistir summary/submit/score, [run44854060047](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44854060047). Una etiqueta interna `SCORE_CENSORED_BY_MEMORY` fue bug de clasificación, no memoria. **D-0053/T0.46 siguiente:** diagnosticar timeout y añadir telemetría de progreso/censura privada y verificable antes de otro LLM. 0 API paga/GPU, H0 abierto sin H1/H2. [STATE](STATE.json).

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