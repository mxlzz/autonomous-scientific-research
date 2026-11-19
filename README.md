# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado:** **H0 activo, NO cerrado.** [Auditoría T0.6](audits/H0-MILESTONE-T0.6-2026-11-19.md) determinó **CORREGIR**: la evidencia existente cubre una muestra de programación científica (DS1000 validation513), evaluada dos veces con `ds1000_scorer=I/I` sobre ReAct+Qwen3 0.6B, pero **no** un ciclo de investigación autónoma, ni trazas completas auditables, comparadores emparejados o costos totales. [Registro de brechas](evidence/T0.6-H0-gap-register-2026-11-19.md) · [resultado T0.5](evidence/T0.5-C1-DS1000-scoring-2026-11-19.md). **T0.7 completada documentalmente:** [matriz de procedencia y retención](evidence/T0.7-provenance-trace-retention-2026-11-19.md) · [autoverificación](audits/T0.7-PROVENANCE-RETENTION-2026-11-19.md): manifiestos públicos sanitizados y datos rehidratables de fuentes lícitas por defecto; trazas completas sólo en almacén autorizado, sin confiar en artifacts de Actions públicos. **Próxima T0.8:** seleccionar un caso de investigación científica con datos y verificación externos, sin costo de API. H1/H2 no habilitadas. Estado canónico: [STATE.json](STATE.json).

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