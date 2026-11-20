# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / QWEN0.6 TOOL-ONLY INSUFICIENTEMENTE CONFIABLE EN PILOTOS.** [T0.29](evidence/T0.29-qwen-real-toolonly-first-science-2026-11-20.md) probó una función OpenAI real `budget_status` bajo aislamiento de modelo/evaluador, pero el episodio de ciencia terminó en error antes de tokens y **NO_SCORE**. [T0.30](evidence/T0.30-qwen-toolcall-negative-2026-11-20.md) mantuvo pesos/modelo/CPU y preregistró corregir error/timeout90s; [CI44817585135](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44817585135) pasó identidad/mounts pero **no logró un `budget_status` válido**; la ciencia no empezó. No inferir fiabilidad de dos intentos ni atribuir el fallo a hipótesis científica. [Autoverificación](audits/T0.30-QWEN-TOOLCALL-NEGATIVE-2026-11-20.md). **D-0038:** detener tuning de Qwen0.6B, próximo **T0.31** comparar alternativas gratuitas existentes y decidir un único camino compatible antes de más implementación/experimentos. H0 no cerrado; H1/H2 no iniciados. [STATE.json](STATE.json).

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