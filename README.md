# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR, primera tarea científica puntuada pero sin calidad ni replicación suficientes.** [T0.49](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) completó **8 turnos/8 tools**, 2 errores y un `submit` puntuado por el grader original SciResearch en Qwen3 4B Instruct2507 Q4, [Actions44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967). Sin presión de memoria con actor2CPU/8GiB, no API paga/GPU. Resultado científico **débil**: cobertura de intervalos0, error objetivo14861 veces sigma, atribución0, **cero nuevas mediciones**. El límite operativo de entrada24k fue **blando**: consumo real28,248 con última llamada de entrega (+17.7%). **[Auditoría T0.50](evidence/T0.50-h0-milestone-first-scored-quality-budget-assessment-2026-11-21.md)** confirmó fuente de grader/harness, falta de réplica y trazas privadas verificables: **H0 sigue CORREGIR**, H1/H2 no comenzaron. **D-0058/T0.51 próximo:** diseñar offline presupuesto realmente comparable y telemetría por categorías sin contenido privado antes de decidir una réplica n2. [STATE](STATE.json).

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