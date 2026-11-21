# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR; primera trayectoria original SciResearch puntuable, todavía de baja calidad científica.** Tras episodios Qwen3 1.7B sin `submit` y preflight de Qwen3 4B Instruct2507 Q4, [T0.47](evidence/T0.47-qwen4b-science-first-request-timeout-2026-11-21.md) terminó en `TimeoutError` HTTP90s. [T0.48](evidence/T0.48-first-request-adapter-timeout-offline-audit-2026-11-21.md) auditó adapter/telemetría. **[T0.49](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md)** con socket timeout180s completó el episodio **dev SciResearch original**: 8 turnos y 8 tools, dos errores, `submit` aceptado y `grader.grade` produjo métricas, [run44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967). Calidad **insuficiente**: cobertura de intervalos0, atribución0, error objetivo14861σ, cero nuevas mediciones; input real28248 superó el umbral24k en17.7% por último turno permitido. CGroup8GiB sin presión; 441.35s de requests del wall442.373s. **D-0057/T0.50 siguiente**: auditar offline scorer, límite blando y validez/costo antes de repetir experimentos. H0 abierta, H1/H2 no iniciados, 0 API paga/GPU. [STATE](STATE.json).

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