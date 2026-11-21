# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR / ningún score científico LLM aún.** Qwen3 1.7B ejecutó 2 trayectorias científicas reales, [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) y [T0.36](evidence/T0.36-eight-turns-tool-errors-no-score-2026-11-20.md), ambas sin `submit`/score=null. [T0.37](evidence/T0.37-cache-input-stop-instrument-audit-2026-11-20.md) detectó ausencia de cache-tokens en la telemetría y metadato stale `max_turns`; [T0.38](evidence/T0.38-offline-cache-guard-test-2026-11-20.md) probó offline, sin LLM, un instrumento de `input+cache+turns/guard` con 8 fixtures PASS, 12 inválidos rechazados. [T0.39](evidence/T0.39-alternative-baseline-qwen4b-instruct-feasibility-2026-11-20.md) comparó soluciones existentes y eligió **Qwen3-4B-Instruct-2507 Q4_K_M** non-thinking/Apache2 como candidato **condicionado**; archivo 2.5GB no demuestra viabilidad real en CPU2/5GiB. **D-0047/T0.40 siguiente:** preflight gratis **sin inferencia** del tag/digest/runtime/tools en imagen Ollama pinned, luego decidir si corresponde un protocolo científico separado. Sin costo API/GPU, sin H1/H2. [STATE](STATE.json).

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