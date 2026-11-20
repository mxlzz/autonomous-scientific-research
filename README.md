# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). **T0.19 [verificó una cápsula científica CORE distinta, BorderT-GRAANK](evidence/T0.19-border-tgraank-archive-and-cpu-pilot-2026-11-20.md)**: fuente oficial 246776 B SHA256 `012ff05f...`, código MIT y otro LICENSE CC0, 4 CSV, sin indicaciones GPU en Dockerfile; [piloto CPU adaptado](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44743969158) instaló seis ruedas, pero script terminó con **ImportError**, sin reporte ni scorer (no score0). Primer intento quedó bloqueado por codec del controlador antes de ejecutar ciencia. [Autoverificación T0.19](audits/T0.19-BORDER-REVIEW-2026-11-20.md). **D-0026/T0.20:** probar una última ruta con imagen Code Ocean **original si pública, segura, fijable por digest y barata**, sin seguir reconstruyendo versiones; de lo contrario revisar otro benchmark ya listo en CPU. No hay todavía línea base autónoma ni comparaciones costo/validez, sin API paga. [STATE.json](STATE.json).

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