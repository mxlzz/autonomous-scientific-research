# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / CORREGIR.** [Auditoría de hito](audits/H0-MILESTONE-T0.6-2026-11-19.md). [T0.17](evidence/T0.17-expso-single-cpu-baseline-failure-2026-11-20.md) y [T0.18](evidence/T0.18-expso-single-diagnostic-retry-2026-11-20.md) hicieron **dos intentos CPU acotados** de una reproducción real CORE ExPSO: cápsula/imagen/wheels verificados, `pip install PASS`, pero `script runtime exit1` tras 2.375s en el reintento, sin reporte ni scorer. **No hay score ni evidencia de fracaso científico del algoritmo.** [Autoverificación T0.18](audits/T0.18-EXPSO-NO-GO-2026-11-20.md). **D-0025:** ExPSO diferida como primer piloto, sin tercer intento. **Próximo T0.19:** evaluar rápidamente la cápsula científica CORE `capsule-2011424` BorderT-GRAANK con derechos/CPU/scorer y producir una línea base si pasa; evitar preflights sin beneficio. Sin gasto en API paga, H0 sin autonomía científica de extremo a extremo. [STATE.json](STATE.json).

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