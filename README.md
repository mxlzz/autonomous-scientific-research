# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR / aún no hay score científico de LLM.** Qwen3 1.7B validó `budget_status` e inició SciResearch-Eval real en [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) y [T0.36](evidence/T0.36-eight-turns-tool-errors-no-score-2026-11-20.md), pero sin `submit`; el último intento tuvo **6 calls/5 errores**, score=null. [T0.37](evidence/T0.37-cache-input-stop-instrument-audit-2026-11-20.md) comprobó que el STOP mezcla turnos y tokens con caché no registrada, y halló metadata obsoleta `max_turns=4` aunque módulo cargó 8. **[T0.38](evidence/T0.38-offline-cache-guard-test-2026-11-20.md)** validó un helper para contabilidad y causa exacta del guard con 8 fixtures/12 inválidos, sin LLM, [CI44850611363](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44850611363). **Próxima T0.39:** comparar con rigor alternativas reales de modelos no-thinking, RAM, latencia y recursos antes de gastar más CPU en otra corrida. Sin API paga/GPU, sin H1/H2. [STATE](STATE.json).

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