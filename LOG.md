# Bitácora cronológica

Fuente única para eventos y decisiones históricas. El estado operativo corriente está en STATE.json; la bibliografía está en RESEARCH.md. No duplicar todo el contenido.

## 2026-11-17 — D-0001: aprobación y preparación
- Usuario aprobó el diseño preliminar centrado en rigor, autonomía progresiva, comparación de arquitecturas y eficiencia de modelos.
- Inspección inicial del repositorio: público, rama main, README.md con título solamente; HEAD anterior 8bddb01dc9d3c48233c3361e0741d73f9fed8eac.
- Se preparó la estructura documental para H0, con primera tarea T0.1.1 (auditoría documental de EvoScientist).
- Los documentos de inicio no contienen resultados experimentales ni auditoría científica independiente. La verificación de escrituras y simulación de continuidad se registrarán aparte antes de fijar STATE.json.

## 2026-11-17 — D-0002: verificación de inicialización
- Se leyeron 14 archivos desde GitHub; los 21 enlaces internos Markdown detectados apuntan a archivos existentes.
- La primera prueba automatizada dio falso positivo por una comparación de cadena excesivamente literal; corregida y repetida.
- La simulación documental A-INIT-001 (audits/INIT-2026-11-17.md) comprobó que un ejecutor sin contexto de chat puede identificar T0.1.1 y su aceptación.
- No se ejecutaron investigaciones científicas, benchmarks ni un agente de continuidad real. No hay auditoría independiente.
- La siguiente ejecución deberá comenzar por T0.1.1.

## 2026-11-17 — D-0003: T0.1.1 EvoScientist — auditoría documental

- Se recuperó STATE.json y se ejecutó exclusivamente T0.1.1 conforme al plan; fuentes primarias: artículo arXiv 2603.08127v2 y GitHub `EvoScientist/EvoScientist@15f3e25bf86e55557d511367e16a3711c0f36934`.
- Se confirmó Apache-2.0 del código, paquete 0.4.3 y Python >=3.11; se distinguió la arquitectura RA/EA/EMA del paper de la plataforma actual con seis subagentes, memoria de observaciones y base DeepAgents.
- Resultado: hallazgos y límites en [evidence/R01-EvoScientist-2026-11-17.md](evidence/R01-EvoScientist-2026-11-17.md); [autoverificación](audits/T0.1.1-R01-2026-11-17.md) favorable, **no independiente**.
- Dictamen: candidato a comparar/reproducir **condicionalmente**; sin evidencia experimental propia ni modelo ejecutado y sin gasto. Próxima unidad: T0.1.2, DeepScientist R02.

## 2026-11-17 — D-0004: T0.1.2 DeepScientist — auditoría documental y contraste R01

- Estado operativo recuperado desde GitHub: H0/T0.1.2, sin bloqueos ni duplicación. Paper primario final ICLR 2026 y producto `ResearAI/DeepScientist@b36624417f0c6b8238ec02db37b94d6db2faa5b0`; versión 1.6.0, Apache-2.0, diferente del tag v1.6.0 y del diseño experimental del paper.
- Reportes autorales: ~5.000 hipótesis, ~1.100 ensayos, 21 Progress Findings, más de 20.000 GPU-h, costo total ~US$100.000; revisores detectan bajo soundness y ~60% de fallos de implementación en muestra de fallas. No se han replicado.
- Producto actual documenta operación single-agent-first con Git por quest, memoria y artefactos de evidencia; similitud/correspondencia con la implementación del artículo sin verificar.
- Decisión D-0004: comparar R02 con R01; no se declara superioridad científica, ni se autoriza gasto; posible infraestructura reutilizable condicionada a pruebas futuras.
- Persistidos [evidence/R02-DeepScientist-2026-11-17.md](evidence/R02-DeepScientist-2026-11-17.md) y [audits/T0.1.2-R02-2026-11-17.md](audits/T0.1.2-R02-2026-11-17.md). Esta última es **autoverificación no independiente**.
- Próxima unidad T0.1.3: R04 autoresearch (baseline simple) y R03 AI Scientist v2, según PLAN.md.

## 2026-11-17 — D-0005: T0.1.3 — auditorías documentales R04 y R03

- Se continuó exclusivamente T0.1.3 de STATE.json; lectura de código/documentación primaria desde GitHub con SHA fijo y de paper arXiv 2504.08066 para R03.
- R04 autoresearch: `karpathy/autoresearch@228791fb499afffb54b46200aca536f79142f117`, paquete 0.1.0, entrenamiento 300s, evaluación `val_bpb`, Git + TSV; **MIT declarado en README**, sin LICENSE independiente. Una GPU NVIDIA y agente de coding externo; no es por sí mismo orquestador autónomo completo.
- R03 AI Scientist v2: `SakanaAI/AI-Scientist-v2@96bd51617cfdbb494a9fc283af00fe090edfae48`; licencia propia restringida de diciembre 2025, modelos remotos/cómputo. Paper describe búsqueda en árbol y 1/3 papers de workshop aprobable (después retirado); metaselección humana de ideas y mejores ejecuciones.
- **D-0005:** R04 candidato de control simple para tarea/medición acotada, R03 comparador de mayor amplitud con condicionantes legales y de costo; no equivalen a resultados científicos reproducidos, ninguna prueba comparativa de modelos/agentes efectuada.
- Se guardaron fichas [R04](evidence/R04-autoresearch-2026-11-17.md), [R03](evidence/R03-AI-Scientist-v2-2026-11-17.md), [matriz](evidence/T0.1.3-contrast-2026-11-17.md) y [autoverificación](audits/T0.1.3-R03-R04-2026-11-17.md) no independiente; archivos releídos antes del cierre.
- Sin ejecución de terceros ni gasto pago. Próxima unidad: **T0.1.4** (R06–R08, R09–R14, matriz consolidada y auditoría T0.1).

## 2026-11-17 — D-0006: T0.1.4 / cierre documental T0.1 (14 fuentes)

- Se leyó y verificó desde GitHub `STATE.json` H0/T0.1.4 y los archivos canónicos/auditorías; HEAD inicial `9f2db001914ac61959ab6eb2395df0a6431f715a`. No existía T0.1.4 previamente documentada.
- Auditoría de fuentes R06–R08 y R09–R14: consultas a repositorios oficiales con SHA inmutable, LICENSE/pyproject/README, arXiv, PMLR, MIT/Nature, Ai2. Control complementario de R05 (MIT). Matriz de **14 entradas R01–R14**, R15 sin ficha y R16 redundante respecto R06.
- Resultados críticos: R06 AstaBench **Apache-2.0 código / dataset gated** y potencial alta RAM; R07 ResearchGym **sin licencia raíz detectada** y tareas con restricciones distintas; R08 ScienceAgentBench **MIT código / datos mayormente CC BY 4.0**, dataset corregido y evaluador GPT-4o para visualizaciones; R09 ScientistOne **sólo artefactos Apache-2.0**, motor no identificado, contribución de criterios de evidencia; R13 advierte costo/beneficio de arquitecturas multiagente según capacidad del modelo. R10/R14 estado, R11/R12 routing, sin demostración de validez científica.
- **D-0006:** T0.1 cumple criterios de cobertura documental pero no una réplica: [evidence/T0.1.4-benchmark-matrix-2026-11-17.md](evidence/T0.1.4-benchmark-matrix-2026-11-17.md), commit de evidencia `ec2fe321d057980d5662f063da332d47f83e046c`; [autoverificación de cierre](audits/T0.1-COVERAGE-2026-11-17.md), commit `69a916b1cfa1c9e6491dde009b3ad4f14cae5f1f`. No auditoría independiente.
- Sin ejecución de software ajeno, instalación, benchmark, gasto monetario ni autorización para APIs pagas. **Siguiente tarea de H0 T0.2:** seleccionar 2–4 sistemas/candidatos con controles de reproducibilidad, licencia, evaluador, costo, memoria y no contaminación; no afirmar elegidos antes de esa tarea.

## 2026-11-17 — D-0007: T0.2 — Selección condicionada de candidatos

- Se recuperaron HEAD `ba3a3c1795d6131a078a702950a75866c88e72a8` y STATE H0/T0.2; lectura de archivos canónicos/auditorías y [matriz T0.1](evidence/T0.1.4-benchmark-matrix-2026-11-17.md). Una sola unidad, sin ejecutar software.
- Inspección del código `allenai/agent-baselines@2d426deac51ad74381319bcfd77066c6e222ba30`: Basic ReAct pin AstaBench 0.5.3; SmolAgents CodeAgent pin 0.3.1 y requiere Docker; AstaBench HEAD 0.5.5, por tanto compatibilidad **no establecida**.
- Evidencia negativa: Asta-v0 utiliza modelos y servicios especializados fijados y algunos resultados `autoasta_cached_solver`; Asta E2E Panda/CodeScientist/Faker son stubs de respuestas cacheadas, no agentes ejecutando investigación fresca. No emplear como control causal mono/multiagente sin corregir confusores.
- **D-0007:** elegir para evaluación documental de viabilidad **tres candidatos**: C1 Basic ReAct (control simple), C2 SmolAgents coder (acciones Python) y C3 EvoScientist (ciclo y memoria/subagentes, elegibilidad **condicionada a evaluador compartido**). Referente primario R06 AstaBench `validation`; secundario R08 ScienceAgentBench sujeto a derechos/datos/scorer; R07 ResearchGym diferido por licencia, R02/R05 reservados. No se demuestra superioridad de modelos ni arquitectura.
- [Matriz ponderada y exclusiones](evidence/T0.2-candidate-selection-2026-11-17.md), primer commit `229c6ba28ccc07edb0a834ec640d203b8f138423`; [autoverificación T0.2](audits/T0.2-CANDIDATE-SELECTION-2026-11-17.md), primer commit `b8ed1f50465761871965230c5180f08c84a0f7e0`. **No independiente**.
- Sin API paga, instalación, GPU, benchmark, scripts de terceros ni reproducción propia; sigue abierto H0. **Próxima unidad:** T0.3, especificar piloto de 6–8 tareas y gates, con split y evaluador congelados.
