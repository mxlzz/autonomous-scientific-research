# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / VALIDADO DESPACHO DE HERRAMIENTAS SOLO EN COPIA.** [T0.22](evidence/T0.22-sciresearch-naive-heuristic-paired-2026-11-20.md) comparó `naive` vs `heuristic` en una tarea dev simulada (coverage parámetros 0% vs 100%, ~465× cómputo). [T0.23](evidence/T0.23-agenttools-condition-gate-2026-11-20.md) descubrió llamada `update_state` no anunciada aceptada bajo condición A; [T0.24](evidence/T0.24-agenttools-trusted-allowlist-2026-11-20.md) validó un guard local A/B/C/D, y **[T0.25](evidence/T0.25-sciresearch-original-harness-dispatch-2026-11-20.md)** lo insertó en una **copia del receptor original del harness**, probándolo [sin LLM con backend falso en run44811442464](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44811442464). Resultado: llamada no autorizada de condición A bloqueada en copia y válidas preservadas. **Upstream no modificado; OS/private isolation no probado.** [Autoverificación](audits/T0.25-REAL-HARNESS-DISPATCH-2026-11-20.md). **D-0033 / próximo T0.26:** priorizar 4 tareas `dev` preregistradas y políticas originales para distribución de calidad/costo; ningún LLM con shell/FS ni API paga. H0 y auditoría de hito abiertos. [STATE.json](STATE.json).

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