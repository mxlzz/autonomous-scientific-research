# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). Tras el [tar real y licencia de T0.15](evidence/T0.15-core-capsule-5975162-static-provenance-2026-11-19.md), **T0.16 [inspeccionó AST de ExPSO y el scorer CORE original](evidence/T0.16-exPSO-static-code-scorer-gate-2026-11-20.md)**: Dockerfile exige TensorFlow2.15, PyTorch2.1 y ejecuta `postInstall`, aunque script central importa ExPSO/numpy; **4 tests sintéticos del scorer PASS**, sin ejecutar la cápsula. Primer CI falló por sintaxis del inspector, segundo pasó; [autoverificación](audits/T0.16-STATIC-SCORER-2026-11-20.md). **Próximo T0.17:** una prueba de reproducción científica real con CPU/sandbox sin privilegios, o descartar ExPSO como primer piloto si las dependencias y seguridad impiden medirlo; evitar más preflights de bajo rendimiento. H0 todavía sin baseline end-to-end ni comparaciones de autonomía/costo. [STATE.json](STATE.json).

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