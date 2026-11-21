# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR, sin score científico LLM.** Qwen3 1.7B produjo 2 episodios SciResearch sin `submit`, y [T0.38](evidence/T0.38-offline-cache-guard-test-2026-11-20.md) arregló medición de stops/cache. Qwen3 4B Instruct2507 Q4 confirmó tools y metadata en T0.40/41, y [T0.43](evidence/T0.43-qwen4b-cgroup-memory-pressure-measured-2026-11-20.md) registró una función válida pero **387 eventos `memory.events.max`** bajo cap5GiB en [CI44853045984](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44853045984), sin OOM kill ni swap. [T0.44](evidence/T0.44-resource-choice-after-cgroup-pressure-2026-11-20.md) comprobó runner estándar GitHub público `ubuntu-24.04` 4CPU/16GB nominal y decidió **GO condicionado** a un piloto con actor2CPU/8GiB y evaluador1CPU/1GiB, sin costo facturado, primero con guard de memoria/tool-call y solo después ciencia original si pasa. **D-0052/T0.45 siguiente:** preregistrar y ejecutar una unidad con stop a cualquier presión o falta de recursos, evaluador SciResearch original sin alterar y score solo ante `submit`; no H1/H2, H0 abierta. [STATE](STATE.json).

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