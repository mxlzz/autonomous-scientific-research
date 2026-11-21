# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-21): H0 CORREGIR, trazabilidad científica completa pendiente.** [T0.49](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) obtuvo una evaluación original Qwen3 4B/SciResearch dev `submitted`, pero de calidad mala; [T0.52](evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md) completó otra ejecución de 9 turnos/8 herramientas y **NO_SCORE**, aun cuando la última solicitud anunciaba solamente `submit`. Ambos usaron input por encima del umbral soft24k (28248 y31351). **[T0.53](evidence/T0.53-n1-n2-final-submit-trace-custody-options-2026-11-21.md)** verificó que el adaptador Ollama no fuerza `tool_choice`, y comparó alternativas existentes para conservar trazas originales sin exponer datos reservados. Actualmente solo persistimos métricas y hashes; no es posible auditar íntegramente el razonamiento de cada episodio. **D-0061/T0.54 BLOQUEADA por autorización de custodia:** cifrar con `age` para guardar ciphertext en artifacts públicos (con clave pública del propietario), usar un destino privado GitHub autorizado, o seguir solo con métricas aceptando la limitación de H0. No se modificaron permisos ni se almacenó material sensible; sin nuevos LLM/API pagas/GPU. H1/H2 no iniciados. [STATE](STATE.json).

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