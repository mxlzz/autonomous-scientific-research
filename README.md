# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**H0 sigue en corrección.** Qwen3 4B completó dos episodios científicos sobre el mismo caso. El primero entregó una predicción con un error de 14.861 veces el ruido del sensor. El segundo completó nueve turnos y terminó sin entregar. Se conserva esta configuración como referencia negativa. [Primer episodio](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) · [Réplica efectiva](evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md).

**Al retomar, leer [STATE.json](STATE.json).** D-0062 incorpora el [dictamen de dirección](audits/DICTAMEN-DIRECCION-CIENTIFICA-2026-11-21.md). La [guía de continuidad](benchmarks/H0-DECISION-BASELINE.md) especifica T0.55, un protocolo offline para decidir si se puede medir el efecto de dividir el trabajo con recursos comparables. T0.54 sigue pendiente de una decisión explícita del usuario sobre las trazas privadas. Esta tarea offline puede avanzar mientras tanto.

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
En un chat con acceso de lectura/escritura al repositorio, usar las instrucciones de [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) y escribir **Continuá**. Empezar por la unidad vigente y aplicar las reglas de cierre y recuperación de AGENTS.md.