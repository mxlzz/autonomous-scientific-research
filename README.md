# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / GATE DE HERRAMIENTAS NEGATIVO.** [T0.22](evidence/T0.22-sciresearch-naive-heuristic-paired-2026-11-20.md) emparejó políticas `naive` y `heuristic`: cobertura parámetros 0% vs100% con 465x unidades de simulación para heuristic, una sola tarea dev y sin LLM. **[T0.23](evidence/T0.23-agenttools-condition-gate-2026-11-20.md)** ejecutó [cinco pruebas upstream y control de seguridad en CI44810011059](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44810011059): schemas de condición A no ofrecen shell/FS y nombres inexistentes fueron rechazados, pero `AgentTools.call("update_state",...)` **aceptó una herramienta no anunciada** en A. No se observó fuga de datos ni existe aislamiento OS demostrado. [Autoverificación](audits/T0.23-AGENTTOOLS-CAPABILITY-GATE-2026-11-20.md) · [datos](experiments/T0.23-agenttools-api-security-observations.json). **D-0031/T0.24:** probar gate mínimo de autorización en despachador con regresión de condiciones A/B/C/D **antes** de conectar un LLM; mantener al agente sin acceso a archivos privados. H0 no cerrada ni H1/H2 iniciadas. [STATE.json](STATE.json).

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