# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-19): H0 ABIERTO / CORREGIR.** [Auditoría de hito](audits/H0-MILESTONE-T0.6-2026-11-19.md). T0.7 estableció [evidencia y licencias](evidence/T0.7-provenance-trace-retention-2026-11-19.md); T0.8 seleccionó [DiscoveryWorld como simulador científico](evidence/T0.8-scientific-task-selection-2026-11-19.md); T0.9 verificó el [entorno CPU y scorer original](evidence/T0.9-discoveryworld-cpu-preflight-2026-11-19.md); T0.10 auditó [la frontera con el oráculo](evidence/T0.10-discoveryworld-agent-evaluator-contract-2026-11-19.md). **T0.11: [9 denegaciones y 3 positivos pasaron, pero Qwen3 0.6B no completó ninguna acción del mundo](evidence/T0.11-local-qwen-action-bridge-2026-11-19.md)** pese a salida JSON válida y feedback; [autoverificación](audits/T0.11-LOCAL-LLM-BRIDGE-2026-11-19.md). No se demostró autonomía científica ni efecto multiagente. **Siguiente T0.12:** evaluar si hay línea base local más apta y viable o si conviene realinear H0. API paga USD0. [STATE.json](STATE.json).

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