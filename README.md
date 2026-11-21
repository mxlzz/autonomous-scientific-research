# Autonomous Scientific Research

Investigación metodológica y experimental sobre **autonomía científica verificable** y **eficiencia de agentes de IA**. El objeto de estudio es determinar cuándo un sistema puede investigar con rigor y autonomía progresiva, y cuándo conviene usar un solo agente, varios agentes o modelos de distinta capacidad. No se presupone que haya que crear un framework.

**H0 sigue en corrección.** Qwen3 4B completó dos episodios científicos sobre el mismo caso. El primero entregó una predicción con un error de 14.861 veces el ruido del sensor. El segundo completó nueve turnos y terminó sin entregar. Se conserva esta configuración como referencia negativa. [Primer episodio](evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md) · [Réplica efectiva](evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md).

**Al retomar, leer [STATE.json](STATE.json).** D-0062 incorpora el [dictamen de dirección](audits/DICTAMEN-DIRECCION-CIENTIFICA-2026-11-21.md). La [guía de continuidad](benchmarks/H0-DECISION-BASELINE.md) y el [protocolo T0.55](experiments/T0.55-protocolo-comparacion.md) documentan una comparación de descomposición diseñada offline, **sin habilitar corridas** ([autoverificación](audits/T0.55-DECISION-H0.md)). El usuario eligió para T0.54 cifrado `age` con recipient público y conserva exclusivamente la identidad privada. La [prueba sintética T0.54](evidence/T0.54-age-synthetic-custody-2026-11-21.md) pasó en [Actions 44916003316](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44916003316) ([autoverificación](audits/T0.54-AGE-CUSTODY-GATE-2026-11-21.md)); **aún NO se integró en el runner científico ni se autorizó almacenar trazas reales**. El propietario confirmó la creación local de `trace.tar` al descifrar el artifact sintético; es declaración del usuario, no examen independiente. La [inspección T0.56](evidence/T0.56-sciresearch-trace-integration-no-go-2026-11-21.md) verificó el contrato de escritura del harness original y dejó un adaptador mínimo, **sin probarlo en el runner científico** ([autoverificación NO-GO](audits/T0.56-TRACE-INTEGRATION-2026-11-21.md)). La [decisión T0.57](experiments/T0.57-baseline-feasibility-decision-2026-11-21.md) evaluó alternativas y costo de oportunidad: **no seguir afinando Qwen4B/CPU ni infraestructura auxiliar**, mantener SciResearch como instrumento y **proponer solo un piloto con modelo más capaz bajo autorización expresa de gasto/acceso**, o **PAUSAR H0** si se mantiene gasto USD0 ([autoverificación](audits/T0.57-SCIENCE-OPPORTUNITY-COST-2026-11-21.md)). El usuario posteriormente autorizó **una única calibración sintética con Gemini Free**, sin material SciResearch. [T0.58 run 44934173643](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44934173643): evaluador y flujo falso PASS, pero primera solicitud al modelo `gemini-3.8-flash` finalizó en `transport_error` tras 45 segundos: **NO_SCORE**, cero respuestas y cero mediciones ([evidencia](evidence/T0.58-gemini-free-synthetic-first-attempt-2026-11-21.md), [autoverificación no independiente](audits/T0.58-GEMINI-ONE-EPISODE-TRANSPORT-NOSCORE-2026-11-21.md)). **No se reintentó**, no se activaron APIs pagas ni se autorizaron trazas reales. La [revisión T0.59](evidence/T0.59-gemini-transport-offline-cause-decision-2026-11-21.md) encontró un atajo que invalidaba el scorer original: permitía medir directamente el objetivo. Se quitó el disparador `push` del workflow para impedir reruns accidentales. El [prerregistro corregido T0.60](experiments/T0.60-gemini-original-synthetic-calibration-repaired-preregister-2026-11-21.md) establece identificabilidad lineal, target reservado y pruebas adversariales offline. **T0.61 espera autorización explícita para una segunda prueba gratuita independiente, con cuota de modelo verificada**; sin permiso no se invocará Gemini. H0 CORREGIR.

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

**Actualización T0.61:** [Gemini 3.5 Flash-Lite Free completó una calibración sintética corregida](evidence/T0.61-gemini-3.5-flash-lite-one-authorized-v2-pass-2026-11-21.md) (run [44938583860](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44938583860)): dos mediciones discriminantes, coeficientes correctos, 11°C con error 0°C, en 3 solicitudes y ~2.1 s de controlador. **No constituye validación del hito H0 ni comparación de modelos**; rationale no evaluada independientemente. El workflow queda manual-only y siguiente T0.62 evalúa en forma offline si merece la pena diseñar comparaciones entre modelos con casos más difíciles. H0 CORREGIR.


**Decisión T0.62:** [comparar más modelos en el mismo toy es poco informativo](experiments/T0.62-gemini-model-comparison-marginal-value-2026-11-21.md) (posible efecto techo). Se propone **solo condicionalmente** un pequeño estudio pareado de Flash-Lite y Flash sobre casos originales más difíciles, con autorización y scorer previos; alternativa STOP a toys y volver a H0 con tratamiento de datos apto. Estado persistido en STATE, H0 CORREGIR.


**Actualización T0.65:** [cuatro episodios exploratorios Gemini Free](evidence/T0.65-paired-gemini-free-n1-results-2026-11-21.md) con dos tareas sintéticas y dos modelos: Gemini 3.5 Flash-Lite obtuvo 1 `GRADED_PASS` y 1 `GRADED_FAIL`; Gemini 3.8 Flash obtuvo 2 `NO_SCORE HTTP503` (sin respuestas), no comparables en capacidad. [Run44940482339](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44940482339), evaluadores/mocks PASS, sin reintentos ni uso de benchmarks de terceros. Siguiente T0.66 evalúa STOP-LOSS y alternativas con evaluación científica más robusta; **H0 CORREGIR**.
