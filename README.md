# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / SIN EPISODIO CIENTÍFICO IA PUNTUADO.** T0.29 observó una llamada `budget_status` válida con Qwen3 0.6B pero sin score; T0.30 falló el probe (0.6B); [T0.32](evidence/T0.32-qwen17b-original-science-tool-gate-2026-11-20.md) con Qwen3 1.7B verificó pesos/aislamiento pero falló también el probe y no inició ciencia, score=null. **[T0.33](evidence/T0.33-ollama-qwen-tool-format-documentary-2026-11-20.md)** auditó templates Ollama, thinking soft vs control explícito, contrato `max_tokens=128` y defectos de observabilidad: causas de probes inválidos **desconocidas**. [Autoverificación](audits/T0.33-QWEN-OLLAMA-TOOL-DOCUMENTARY-2026-11-20.md). **D-0041 / T0.34 siguiente:** instrumento de métricas de forma validado offline; verificar capacidades reales de Ollama pinned; solo entonces un probe controlado de `reasoning_effort:"none"` con el mismo Qwen1.7B, sin API paga ni escalamiento ciego. H0 sigue CORREGIR; no H1/H2. [STATE](STATE.json).

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