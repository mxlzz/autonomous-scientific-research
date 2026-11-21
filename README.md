# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR; aún sin score científico LLM.** Qwen3 1.7B ejecutó episodios reales [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) y [T0.36](evidence/T0.36-eight-turns-tool-errors-no-score-2026-11-20.md), pero sin `submit`; [T0.37](evidence/T0.37-cache-input-stop-instrument-audit-2026-11-20.md) detectó cache no reportada y [T0.38](evidence/T0.38-offline-cache-guard-test-2026-11-20.md) validó un instrumento seguro offline de límites. [T0.39](evidence/T0.39-alternative-baseline-qwen4b-instruct-feasibility-2026-11-20.md) seleccionó Qwen3 4B Instruct2507 Q4 como alternativa condicionada; **[T0.40](evidence/T0.40-qwen4b-instruct-metadata-preflight-2026-11-20.md) confirmó descarga/digest completo, herramientas declaradas y plantilla en Ollama0.40.16 bajo 2CPU/5GiB**, [run44851631640](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44851631640); **0 inferencias**. **D-0048/T0.41 siguiente:** un único probe sintético de tool-call real con límites y observabilidad seguros, antes de cualquier ciencia. Ningún gasto en APIs/GPU, ni H1/H2. [STATE](STATE.json).

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