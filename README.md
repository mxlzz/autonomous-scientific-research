# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / primera trayectoria científica LLM SIN SCORE.** [T0.34](evidence/T0.34-qwen17b-nothink-first-science-trajectory-2026-11-20.md) logró `budget_status` válido con Qwen3 1.7B Q4/Ollama0.40.16 y `reasoning_effort:none`; primer episodio SciResearch-Eval LLM hizo 4 tool calls/2 errores y no ejecutó `submit`, sin métrica científica (`score=null`). [CI44848550949](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44848550949). [T0.35](evidence/T0.35-sci-llm-stop-error-source-audit-2026-11-20.md) auditó el código original: presupuesto reducido a 4 turnos + turno final, `submit` no garantizado por incompatibilidad `tool_choice`, función `grader` invocada pero solo retorna `submitted:false` si falta envío. Categorías de errores anteriores no recuperables; no inferir causalidad. **D-0043 / T0.36 siguiente:** una prueba condicional con mismo modelo/scorer y **solo MAX_TURNS4→8**, 4 tools y 12k tokens de entrada intactos, más telemetría sanitaria de errores, sin API paga ni GPU. [Autoverificación](audits/T0.35-FIRST-LLM-STOP-SOURCE-AUDIT-2026-11-20.md). H0 CORREGIR, no H1/H2. [STATE](STATE.json).

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