# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / AUDITORÍA DE HITO CORREGIR.** [**Auditoría H0 T0.27**](audits/H0-MILESTONE-T0.27-2026-11-20.md) constató avances reales respecto de [T0.6](audits/H0-MILESTONE-T0.6-2026-11-19.md): `SciResearch-Eval` con scorer matemático original, [T0.22](evidence/T0.22-sciresearch-naive-heuristic-paired-2026-11-20.md) comparación `naive/heuristic`, [T0.26](evidence/T0.26-sciresearch-four-dev-pairs-2026-11-20.md) 4 tareas dev preregistradas, **7/8 scores y 1 timeout censurado**. **Pero ninguna IA investigó científicamente**: todas fueron políticas deterministas o backend falso, no hay costos integrales ni actor aislado de privados; [guard del harness](evidence/T0.25-sciresearch-original-harness-dispatch-2026-11-20.md) solo probado en copia. **D-0035 CORREGIR H0 / NO H1-H2.** Siguiente **T0.28:** verificar un modelo pequeño y gratuito de CPU con tool calls que pueda usar el harness original de manera limitada y sin shell/FS ni gold, sin ejecutar aún ni gastar. [Estado canónico](STATE.json).

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