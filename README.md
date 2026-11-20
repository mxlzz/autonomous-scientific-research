# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / PRIMER TOOL-CALL REAL SIN SCORE CIENTÍFICO.** [Auditoría H0 T0.27](audits/H0-MILESTONE-T0.27-2026-11-20.md) mantiene hito CORREGIR. [T0.26](evidence/T0.26-sciresearch-four-dev-pairs-2026-11-20.md) dejó 7/8 resultados de **políticas scripted**. [**T0.29**](evidence/T0.29-qwen-real-toolonly-first-science-2026-11-20.md) ejecutó [GitHub Actions44816315367](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44816315367) con **Qwen3 0.6B real** en contenedor Ollama aislado del filesystem privado, 2CPU/3GiB combinados; modelo emitió **una función `budget_status` válida**, pero el primer request de episodio científico terminó en **error sin tokens/tool calls científicos ni `submit` ni score**. La clase de error fue enmascarada por instrumento, ~47s vs timeout45s sugiere solo posible latencia. [Autoverificación](audits/T0.29-REAL-TOOLCALL-2026-11-20.md) · [datos](experiments/T0.29-qwen-real-toolcall-observations.json). **D-0037 / T0.30:** un solo intento preregistrado de diagnóstico de transporte (propagar clase correcta, timeout90s) bajo los mismos pesos, límite CPU y scorer; no retune de ciencia ni GPU/API paga. H0 no aprobado, H1/H2 cerrados. [Estado](STATE.json).

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