# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-19): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). T0.13 fue una única corrida Qwen3 4B que [terminó por timeout sin score](evidence/T0.13-qwen4b-single-cpu-probe-2026-11-19.md). **T0.14 [inspeccionó CORE-Bench y sus cápsulas train](evidence/T0.14-corebench-train-capsule-gate-2026-11-19.md)**: preselección condicional `capsule-5975162` (ExPSO/Python, dos preguntas numéricas), alternativa `capsule-2916503` (R); licencia del tar, recursos y aislamiento aún no verificados. [Autoverificación](audits/T0.14-CORE-CAPSULE-REVIEW-2026-11-19.md). **Próxima T0.15:** comprobar licencia/metadata/CPU/tamaño y frontera de evaluador de una cápsula *sin ejecutar su código*. No hay baseline científica validada ni gasto de API paga. [STATE.json](STATE.json).

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