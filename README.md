# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR, n1 puntuada de calidad baja y n2 NO_SCORE.** [T0.49](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) produjo un primer `submit` puntuado con Qwen3 4B/SciResearch original dev, 8 turnos/8 tools/2 errores, pero `param_coverage=0`, error objetivo14861 sigma y cero nuevas mediciones, [run44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967). [T0.50](evidence/T0.50-h0-milestone-first-scored-quality-budget-assessment-2026-11-21.md) identificó presupuesto input24k **soft** con última entrega permitida. [T0.51](evidence/T0.51-offline-soft-budget-tool-category-n2-gate-2026-11-21.md) validó registro seguro por categorías. **[T0.52](evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md)** ejecutó **9 turnos, 8 tools/2 errores**, pero **no presentó submit** (`NO_SCORE`); categorías observadas analysis, reading, fitting y status, sin measurement/simulation, y input efectivo **31.351** (+30,63% vs umbral soft24k), [run44909561018](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909561018). Cgroup8GiB sin presión, mismo scorer, recursos públicos gratuitos y 0 API paga/GPU. **D-0060/T0.53 siguiente:** auditoría offline de `final_turn`/no-submit, comparabilidad y custodia de trazas antes de otra inferencia; no hay replicación estadística ni rigor científico demostrado, H1/H2 no comenzados. [STATE](STATE.json).

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