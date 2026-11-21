# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR; sin score científico LLM válido.** Qwen3 1.7B tuvo trayectorias SciResearch sin `submit`; Qwen3 4B Instruct2507 Q4 validó tool calls y memoria8GiB. [T0.47](evidence/T0.47-qwen4b-science-first-request-timeout-2026-11-21.md) probó una ventana global científica600s y recuperó heartbeat + resumen, pero **el primer request de SciResearch agotó un timeout HTTP90s** antes de completar turno, grader `submitted=false`, score=null y cgroup sin presión. [T0.48](evidence/T0.48-first-request-adapter-timeout-offline-audit-2026-11-21.md) verificó las fuentes originales SciResearch y **Ollama v0.40.16**: el adapter usa `urllib.request.urlopen(timeout=90)` (copia experimental), mientras modelo cargado `/api/ps` y tiempos de carga/pre-fill/tokens están disponibles en API nativa solo cuando se obtienen respuestas completas. No hay medida del tamaño ni de la latencia interna del prompt científico y no corresponde atribuir causa al modelo. **D-0056/T0.49 siguiente:** piloto condicionado con un único cambio de timeout HTTP90→180s, mismo scorer/modelo/CPU y metadatos numéricos/loaded boolean sin privados, sin APIs pagas/GPU. H1/H2 sin iniciar. [STATE](STATE.json).

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