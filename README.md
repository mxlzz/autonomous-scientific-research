# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-19): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). [T0.13](evidence/T0.13-qwen4b-single-cpu-probe-2026-11-19.md) agotó 15min sin score; [T0.14](evidence/T0.14-corebench-train-capsule-gate-2026-11-19.md) priorizó CORE ExPSO train. **T0.15 [verificó la cápsula oficial `capsule-5975162` por HTTP](evidence/T0.15-core-capsule-5975162-static-provenance-2026-11-19.md):** archivo 303245 B, SHA256 `5668df38...`, 47 entradas, sin enlaces/rutas inseguras detectadas, dos LICENSE GPL y script de 856 B presentes; no se ejecutó código científico. [Autoverificación](audits/T0.15-CAPSULE-STATIC-2026-11-19.md). **T0.16 siguiente:** análisis estático de dependencias/sandbox sin privilegios, scorer externo y trazas con watchdog, antes de autorizar un microexperimento. Sin gasto en APIs pagas, ninguna línea base científica validada aún. [STATE.json](STATE.json).

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