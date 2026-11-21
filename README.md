# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR; todavía no existe score científico LLM válido.** Qwen3 1.7B ejecutó dos episodios SciResearch sin `submit`; Qwen3 4B Instruct2507 Q4 validó tool calls y memoria con cap8GiB. [T0.45](evidence/T0.45-qwen4b-original-science-timeout-no-score-2026-11-20.md) inició una tarea dev con scorer original, pero fue **censurada por timeout360s**, sin summary/submit/score, y el monitor etiquetó erróneamente memoria como causa a pesar de cgroup events0. **[T0.46](evidence/T0.46-timeout-heartbeat-offline-2026-11-20.md)** creó y verificó offline un heartbeat por request/turno/tool, con cuentas input/cache y categoría correcta de censura; 18 fixtures de parsing, 7 de censor, source patch original compilado/invariantes del evaluador intactos, **0 LLM** [CI44855353358](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44855353358). **D-0054/T0.47 siguiente:** ensayo condicional de Qwen4B con el mismo modelo/scorer/CPU2/8GiB y ventana científica 360→600s, siempre dentro del job gratuito15min y con heartbeat seguro/gate de tiempo restante. H0 ABIERTA, H1/H2 no iniciadas. [STATE](STATE.json).

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