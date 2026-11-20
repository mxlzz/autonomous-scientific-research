# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / FILTRO DE CAPACIDADES PROBADO SOLO LOCALMENTE.** [T0.22](evidence/T0.22-sciresearch-naive-heuristic-paired-2026-11-20.md) comparó `naive` vs `heuristic` con scorer original (cobertura parámetros 0% vs100%, a 465× cómputo de simulador, una tarea dev). [T0.23](evidence/T0.23-agenttools-condition-gate-2026-11-20.md) detectó que `AgentTools.call` acepta `update_state` no anunciada en condición A. **[T0.24](evidence/T0.24-agenttools-trusted-allowlist-2026-11-20.md)** validó en [CI44810721415](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44810721415) un **filtro mínimo de nombre** bajo condiciones A/B/C/D (4/4 PASS) manteniendo herramientas originales, CPU gratis, cero LLM; **no se aplicó al harness upstream**: su fallo permanece por control negativo. [Autoverificación T0.24](audits/T0.24-ALLOWLIST-PROTOTYPE-2026-11-20.md). **D-0032/T0.25:** probar el filtro integrado en copia del despachador `agents/harness.py` con backend falso offline; no usar modelos con shell/FS ni afirmar aislamiento de private. H0 no cerrada ni H1/H2 iniciadas. [Estado canónico](STATE.json).

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