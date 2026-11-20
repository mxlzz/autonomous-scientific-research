# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). [T0.16](evidence/T0.16-exPSO-static-code-scorer-gate-2026-11-20.md) validó el scorer CORE en 4 casos sintéticos. **T0.17 [intentó una reproducción CPU segura de ExPSO](evidence/T0.17-expso-single-cpu-baseline-failure-2026-11-20.md)**: fuente, digest de imagen y wheels PASS; contenedor científico `exit1` a 2,461s, sin reporte ni evaluación externa; el instrumento descartó el error preciso. **No hay score científico, ni evidencia de que la CPU sea inviable**. [Autoverificación](audits/T0.17-CPU-BASELINE-NEGATIVE-2026-11-20.md). **T0.18 siguiente:** reparar sólo la observabilidad de fallo y permitir máximo un reintento idéntico; si no puede puntuarse, pasar a otra cápsula oficial con un gate breve. Sin API paga, H0 sin baseline autónoma ni comparación costo/validez. [STATE.json](STATE.json).

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