# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / PRIMER MODELO CIENTÍFICO AÚN SIN EJECUTAR.** [Auditoría H0 T0.27](audits/H0-MILESTONE-T0.27-2026-11-20.md) confirmó scorer y baselines de física térmica simulada ([T0.26](evidence/T0.26-sciresearch-four-dev-pairs-2026-11-20.md): 7/8 episodios puntuados) pero no hay **ningún LLM investigando ciencia**, costo IA por resultado válido ni aislamiento actor/private probado. **[T0.28](evidence/T0.28-free-local-qwen-toolonly-gate-2026-11-20.md)** seleccionó documentalmente Qwen3 0.6B/Ollama gratuito ya probado CPU con digest observado, pero **tool-calling OpenAI y RAM bajo 2CPU/3GiB siguen NO VERIFICADOS**. El adaptador SciResearch-Eval envía `tool_choice` no soportado según docs Ollama; requiere copia mínima sin ese campo, guard de herramienta de [T0.25](evidence/T0.25-sciresearch-original-harness-dispatch-2026-11-20.md) y **actor Ollama en contenedor sin archivos privados**, evaluador/grader en otro contenedor. [Autoverificación T0.28](audits/T0.28-LOCAL-QWEN-TOOLONLY-GATE-2026-11-20.md). **D-0036 GO documental condicional / próximo T0.29:** un único gate gratuito de identidad, herramienta y aislamiento y, solo si pasa, una trayectoria IA corta con scorer original. No pagar/GPU/infra nueva ni H1/H2. [STATE.json](STATE.json).

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