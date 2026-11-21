# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR, primer SciResearch puntuado pero baja calidad y sin reproducción.** [T0.49](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) produjo 8 turnos y 8 tools/2 errores, `submit` puntuado por grader original, pero `param_coverage=0`, error objetivo14861sigma y **0 mediciones nuevas**, run [44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967). [T0.50](evidence/T0.50-h0-milestone-first-scored-quality-budget-assessment-2026-11-21.md) comprobó que input24k es umbral **soft** (última entrega elevó el total a28,248), sin justificación para H1/H2 todavía. **[T0.51](evidence/T0.51-offline-soft-budget-tool-category-n2-gate-2026-11-21.md)** validó offline un registro por categorías de herramientas, sin contenido privado ni modificación de scorer, [CI44908726893](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44908726893); condición A no incluye herramienta de `update_state`. **D-0059/T0.52 siguiente:** preregistrar y ejecutar **una sola réplica exploratoria n2** del mismo dev/Qwen4B/scorer/CPU/soft budget y obtener categorías/uso real para evaluar repetibilidad; no inferir causalidad ni asumir éxito científico. H0 abierto, sin APIs pagas/GPU. [STATE](STATE.json).

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