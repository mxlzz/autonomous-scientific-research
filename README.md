# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / primera trayectoria científica LLM SIN SCORE.** El [T0.33](evidence/T0.33-ollama-qwen-tool-format-documentary-2026-11-20.md) identificó diferencias de template y falta de observabilidad en Qwen3. El [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) probó Qwen3 1.7B Q4 con Ollama0.40.16 y `reasoning_effort:none`: **una llamada real correcta `budget_status`**, luego **4 herramientas** en SciResearch-Eval original con **2 errores y sin `submit`**, `stop=limit_turns_or_tokens`, **score=null**, [run44848550949](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44848550949). Primera trayectoria IA no es resultado científicamente validado ni demuestra causalidad del tratamiento. 10 fixtures previos de privacidad PASS, CPU3/6GiB, API paga0, sin traza cruda conservada y costos completos desconocidos. [Autoverificación](audits/T0.34-QWEN17B-NOTHINK-SCIENCE-AUTOVERIFICATION-2026-11-20.md). **D-0042 / T0.35 siguiente:** auditar el stop y los errores con fuente original antes de otra inferencia; no nuevos modelos/retuning a ciegas. H0 sigue CORREGIR; no H1/H2. [STATE](STATE.json).

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