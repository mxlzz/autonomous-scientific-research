# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / REPLANTEAR BENCHMARK.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). **T0.20 [verificó disponibilidad anónima del manifiesto de imagen preservada Code Ocean](evidence/T0.20-codeocean-preserved-image-gate-and-benchmark-pivot-2026-11-20.md)**: 9 capas/225794596B comprimidos, pero tres controladores abortaron **antes de descargar imagen o ejecutar ciencia**; el último no ubicó `run` en staging esperado, sin probar ausencia global del tar. **Ningún score científico, ningún LLM ni API paga**; CORE se detiene como **primer piloto**, no se concluye que el algoritmo falle. [Autoverificación](audits/T0.20-CODEOCEAN-NOGO-PIVOT-2026-11-20.md). **D-0027 / próximo T0.21:** validar una línea base `dev` no-LLM del benchmark existente **[SciResearch-Eval](https://github.com/Btwestyo/sciresearch-eval)**, de experimentos térmicos y `grader` matemático (sin juez LLM), en CPU controlada; comparar con TruthInsightBench/ScienceAgentBench/DiscoveryBench según restricciones. El benchmark no fue ejecutado todavía y H0 no está cerrado. [STATE.json](STATE.json).

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