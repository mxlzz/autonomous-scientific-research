# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-20): H0 ABIERTO / ALTERNATIVA GRATUITA ELEGIDA SOLO DOCUMENTALMENTE.** [T0.29](evidence/T0.29-qwen-real-toolonly-first-science-2026-11-20.md) probó una llamada real de Qwen3 0.6B a `budget_status`, pero el episodio científico no recibió respuesta ni score; [T0.30](evidence/T0.30-qwen-toolcall-negative-2026-11-20.md) no pasó el gate de llamada y no empezó la ciencia. **[T0.31](evidence/T0.31-toolonly-alternatives-2026-11-20.md)** comparó modelos y eligió **Qwen3 1.7B Q4** con licencia Apache2 y soporte tool declarado por Ollama, **sin afirmar competencia demostrada**; runner público gratuito GitHub estándar admite nuevo presupuesto **3CPU/6GiB** (diferente del piloto2CPU/3GiB). La [fuente oficial Ollama](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx) marca `tools` soportado, `tool_choice` no: se debe omitir en copia y validar permisos en harness. [Autoverificación](audits/T0.31-EXISTING-MODEL-CHOICE-2026-11-20.md). **D-0039 / próximo T0.32:** un solo ensayo nuevo con 1.7B, modelo aislado del private/gold, scorer original, sin API/GPU paga ni otro tuning automático. No cerrar H0 ni pasar H1/H2. [Estado](STATE.json).

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