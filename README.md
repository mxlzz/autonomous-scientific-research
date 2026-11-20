# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**Estado (2026-11-19): H0 ABIERTO / CORREGIR.** [Auditoría H0](audits/H0-MILESTONE-T0.6-2026-11-19.md). [T0.12](evidence/T0.12-free-model-and-real-science-options-2026-11-19.md) seleccionó una sola prueba libre Qwen3 4B en CPU. **T0.13 [ejecutó el único run 44652705085](evidence/T0.13-qwen4b-single-cpu-probe-2026-11-19.md)**: seguridad/recursos/digest PASS, pero el job agotó 15 minutos **sin métricas finales de acciones ni score**; [autoverificación](audits/T0.13-QWEN4B-TIMEOUT-2026-11-19.md). No demuestra éxito, fracaso científico ni comparación de tamaños. **Siguiente T0.14:** localizar y verificar una cápsula CORE-Bench de paper real para evaluación científica CPU, derechos de datos, scorer y aislamiento, sin gasto ni nuevo modelo hasta pasar gates. [STATE.json](STATE.json).

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