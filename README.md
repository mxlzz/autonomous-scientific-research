# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / CALIBRACIÓN CIENTÍFICA PARCIAL.** [Auditoría de hito H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). **T0.21 [obtuvo la primera línea base de CIENCIA TÉRMICA SIMULADA puntuada](evidence/T0.21-sciresearch-eval-dev-naive-baseline-2026-11-20.md)** con [SciResearch-Eval](https://github.com/Btwestyo/sciresearch-eval) original congelado: [run 44804607488 SUCCESS](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44804607488), dos funciones de test de puntuación/privacidad PASS, una política `naive` sin LLM en dev `task_525abee377`, `param_interval_score=0.3617`, cobertura de parámetros **0%**, target cubierto, grader matemático original y trazas. [JSON de observaciones](experiments/T0.21-sciresearch-dev-naive-observations.json) y [autoverificación](audits/T0.21-SCIRESEARCH-DEV-BASELINE-2026-11-20.md). **Límites:** 1 caso/0 modelos, resultados no ciegos, privado disponible en mismo proceso aunque las salidas públicas no lo revelaron, costo total desconocido. **D-0028 / próximo T0.22:** comparar naive vs heuristic en condiciones emparejadas y comprobar separación actor/gold antes de dar herramientas a LLM; no framework nuevo. H0 no aprobado y H1/H2 no iniciados. [STATE.json](STATE.json).

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