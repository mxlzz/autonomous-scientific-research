# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / MODELO 1.7B NO PASÓ GATE DE HERRAMIENTAS.** Tras [T0.29](evidence/T0.29-qwen-real-toolonly-first-science-2026-11-20.md) y [T0.30](evidence/T0.30-qwen-toolcall-negative-2026-11-20.md) con Qwen0.6B (una tool call real correcta, otra inválida, **ningún score IA**), [T0.31](evidence/T0.31-toolonly-alternatives-2026-11-20.md) seleccionó Qwen3 1.7B Q4 para un solo ensayo gratuito. **[T0.32](evidence/T0.32-qwen17b-original-science-tool-gate-2026-11-20.md)** [CI44819424064](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44819424064) verificó digest completo `8f68893c...`, fuente/scorer y aislamiento de archivos privados del modelo en Docker CPU3/6GiB, **pero la prueba real `budget_status` no cumplió el contrato y la ciencia NO EMPEZÓ; score=null**. [Autoverificación](audits/T0.32-QWEN17B-TOOL-GATE-2026-11-20.md). **D-0040 / T0.33:** antes de probar otro modelo, revisar documentalmente templates `tool_call`/thinking y límites del probe, sin tuning ciego ni API paga. No H1/H2. [STATE](STATE.json).

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