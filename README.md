# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / MUESTRA MULTICASE CALIBRADA.** [T0.25](evidence/T0.25-sciresearch-original-harness-dispatch-2026-11-20.md) probó en una copia del receptor original del harness el guard de herramientas, no desplegado upstream ni con aislamiento OS. **[T0.26](evidence/T0.26-sciresearch-four-dev-pairs-2026-11-20.md)** ejecutó [CI44812454823](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44812454823) sobre 4 tareas dev públicas [preregistradas](experiments/T0.26-sciresearch-preregistered-multicase-protocol-2026-11-20.md), `naive` y `heuristic` originales con scorer matemático: **7 episodios puntuados, 3 pares completos y 1 heuristic censurado a 60s** (no score0). Heuristic mejoró cobertura/calidad en unos casos, no en otros, y costó más recursos; un caso con target cubierto obtuvo penalidad de intervalo muy alta. [Datos reconstruidos](experiments/T0.26-sciresearch-multicase-observations.json) · [autoverificación](audits/T0.26-MULTICASE-2026-11-20.md). N=4 dev no aleatoria, sin modelos/heldout/API paga ni generalización. **D-0034 / próximo T0.27:** auditoría formal del hito H0 contra criterios científicos, privacidad, costos y evidencia antes de seguir experimentos. [Estado canónico](STATE.json).

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