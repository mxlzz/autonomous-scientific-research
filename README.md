# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / PRIMER CONTRASTE CIENTÍFICO SIMULADO.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). [**T0.22**](evidence/T0.22-sciresearch-naive-heuristic-paired-2026-11-20.md) comparó en [run44809114440 SUCCESS](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44809114440) dos políticas originales `naive` vs `heuristic` de [SciResearch-Eval](https://github.com/Btwestyo/sciresearch-eval) sobre **una misma tarea dev** `task_525abee377`, con scorer matemático original sin LLM: cobertura de parámetros **0% vs 100%**, intervalo0.361734 vs0.000840 (menor mejor), atribución0 vs1, **71300 vs33175201** unidades simuladas (heuristic **465.29x** costosa), target cubierto por ambas. [Datos reconstruidos del log](experiments/T0.22-sciresearch-dev-naive-vs-heuristic-observations.json) · [autoverificación](audits/T0.22-SCIRESEARCH-PAIRED-2026-11-20.md). N=1, no heldout ni generalización; los scripts originales y verdad privada comparten proceso evaluador, **OS FS isolation NO verificada**. **D-0030/T0.23:** gate de `AgentTools` original para actor LLM **solo texto/herramientas y sin FS/shell**; no ejecutar LLM con permisos de archivos mientras no se verifique. H0 no cerrado; H1/H2 no iniciados. [Estado canónico](STATE.json).

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