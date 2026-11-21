# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 CORREGIR / ciencia LLM sin score.** T0.34 Qwen3 1.7B logró `budget_status` válido y 4 herramientas científicas, sin `submit`; T0.36 amplió MAX_TURNS4→8 y alcanzó 6 tools/**5 errores**, sin envío ni métricas, [run44849636063](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44849636063). La [auditoría T0.37](evidence/T0.37-cache-input-stop-instrument-audit-2026-11-20.md) comprobó que el STOP combina turnos y tokens **incluida caché**, pero nuestros logs no reportaron esa caché. Además T0.36 cargó realmente MAX_TURNS8 aunque un campo de resumen quedó incorrectamente en 4. **No atribuir causalmente** el corte a un límite sin instrumentación. D-0045 y [autoverificación](audits/T0.37-CACHE-METADATA-AUDIT-2026-11-20.md): próxima T0.38 será instrumentación y fixtures offline de contabilidad, sin LLM/GPU/API pagas. No H1/H2. [STATE](STATE.json).

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