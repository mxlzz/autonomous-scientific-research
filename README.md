# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR, sin score científico LLM.** Qwen3 1.7B inició SciResearch en T0.34/T0.36 pero sin `submit`; [T0.38](evidence/T0.38-offline-cache-guard-test-2026-11-20.md) validó auditoría de tokens/STOP. Qwen3 4B Instruct2507 Q4 pasó descarga/verificación T0.40 y una llamada sintética real `budget_status` en **6.466s** [T0.41](evidence/T0.41-qwen4b-single-synthetic-tool-probe-2026-11-20.md), [CI44852173881](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44852173881); se observó `memory.peak=5GiB`, igual al cap. [T0.42](evidence/T0.42-linux-cgroup-memory-pressure-audit-2026-11-20.md) verificó documentación Linux/Docker: peak es cgroup agregado, no RSS modelo ni prueba OOM; eventos/anon/cache/swap no fueron medidos. **D-0050/T0.43 siguiente:** una única petición sintética del mismo 4B, esta vez con perfiles numéricos de `memory.events/stat/current/peak/swap` antes de decidir ciencia, sin cambiar RAM/contexto ni usar API paga/GPU. H0 abierta, H1/H2 no iniciados. [STATE](STATE.json).

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