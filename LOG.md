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

## 2026-11-17 — D-0008: T0.3 — diseño de siete slots y gates

- Estado recuperado de GitHub H0/T0.3, HEAD inicial `5b244f3b91fc2db8d15233b7a0476f59ca752618`, documentos y auditorías canónicas leídos antes de trabajar.
- Se diseñaron **7 slots** ([protocolo](benchmarks/H0-PILOT-v0.1-2026-11-17.md)): P01–P03 DS-1000 `validation` IDs reales 513,974,18 en split fijado; P04 CORE-bench `train/dev`, P05 LitQA2 `dev`, P06 DiscoveryBench `validation` y P07 E2E Discovery `validation` **sin IDs de dataset por falta de acceso**. Se documentó algoritmo determinista para congelarlos sin mirar gold ni puntaje.
- AstaBench `0.5.5` / suite 1.0.0 / dataset HF revision `a600dc7` / scorer aislado Inspect 0.3.225; C1/C2 dependencias distintas, no validadas. C3 solo si mismos contratos. Prueba aritmética demo no cuenta como ciencia.
- **D-0008:** HF AstaBench gated y prohíbe redistribución; no copiar prompts/gold al repo público. Scorer DiscoveryBench `gpt-4o-2024-08-06`, E2E `claude-sonnet-4-6`, costos no autorizados. No considerar 7 instancias congeladas ni inferir validez científica desde un scorer solo.
- [Autoverificación T0.3](audits/T0.3-PILOT-DESIGN-2026-11-17.md) propia, no independiente. Ningún experimento/descarga/uso API/compra. **Próxima unidad T0.4**: chequeos de entorno, permisos y costos, o bloqueo con intervención precisa.

## 2026-11-17 — D-0009: T0.4 — Preflight negativo, BLOQUEO operativo

- Se partió desde STATE H0/T0.4 tras validar HEAD `4ef23e3bc4301a036bf741a62179f0ab8d85887e` y T0.3. Preflight con comandos no destructivos en **runtime efímero**: Linux, Python 3.13.5, 4 GiB cgroup, 4 vCPU, PyTorch CPU, sin CUDA/GPU visible, sin Docker ni `inspect_ai`/`astabench`/`smolagents`. No se inspeccionó PC del usuario.
- HF `allenai/asta-bench` gated con prohibición de redistribución; aceptación por cuenta no verificada. C1/C2 versiones no compatibilizadas, C3 sin adaptador. P06/P07 utilizan GPT-4o/Claude como scorers, sin precio/clave/autorización; máximo autorizado de gasto pago `0`.
- **D-0009: T0.4 NO completada.** Recursos/permiso insuficientes para ejecutar el piloto aquí. No inferir falla científica ni avanzar a T0.5. [Evidencia de comandos, versiones y gates](evidence/T0.4-environment-preflight-2026-11-17.md); [autoverificación de bloqueo](audits/T0.4-BLOCKED-2026-11-17.md). Intervención: acceso lícito HF por titular, entorno con Docker/Python apropiado y modelo/costo aprobado o vía gratuita comprobada.
- **Gasto pagado cero**, instalación/benchmarks/ejecución de código ajeno cero. Tras intervención, repetir preflight y registrar recuperación con CAS GitHub, actualizar STATE al final.

## 2026-11-18 — D-0010: T0.4 — HF_TOKEN y runner de GitHub verificados

- Recuperado HEAD `14a032900d848dda72e71018a63b4f8de663de77`, H0/T0.4 bloqueada; lectura de README/OBJECTIVE/PLAN/METHODOLOGY/AGENTS/STATE/LOG/RESEARCH, piloto y auditoría. Repo confirmado **público** y sin workflows previos.
- Creado [preflight HEAD de Hugging Face](.github/workflows/h0-hf-access-preflight.yml) (commit `dcd5fdeb5d5b5cf77fc9a776ac0dfe149d66f49b`). [Run 44440776634](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44440776634) **success**; logs `HF_TOKEN_PRESENT=true`, `HF_ACCESS_RESULT=confirmed`: autenticación al archivo `DBDev_w_hypothesis.json` en revisión HF `a600dc7`. No descarga de datos ni impresión del secreto; licencias siguen vigentes.
- Creado [preflight runner](.github/workflows/h0-runner-preflight.yml) (commit `113d1dc9838a4d874315b7cc5f4eb40447d695a7`). [Run 44440919736](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44440919736) **success**, 4 vCPU, ~16 GB RAM, Docker 28.0.4, Python3.12.3, sin 3.11/uv/NVIDIA. Los dos jobs usaron runner estándar de repo público (gratis según documentación oficial); timeout 4 minutos, permisos contents:read.
- **D-0010:** gates G-DATA (acceso a archivo) y G-HW (runner con Docker) superados parcialmente; ahora hay ruta técnica para proseguir T0.4 **sin intervención inmediata**. No se declara T0.4 completa: entornos C1/C2/scorer, disponibilidad/licencia modelo gratuito y más muestras pendientes; los jueces pagos siguen excluidos.
- [Informe técnico](evidence/T0.4-hf-and-actions-preflight-2026-11-18.md) · [autoverificación](audits/T0.4-RECHECK-2026-11-18.md). **0 gastos, 0 experimentos con agentes, 0 datos gated descargados**. Próximo: evaluar smoke de harness con modelo ficticio sin APIs o modelo pequeño gratuito con controles, verificar compatibilidad en workflow, nunca sustituir scorer ni confundir con resultado científico.

## 2026-11-19 — D-0011: reconciliación de CI y cierre restringido T0.4

- HEAD inicial recuperado `01338791641d62771e28e50f6f0b3729e3188441`, mientras STATE continuaba T0.4 en blob `20b2660bff90a3413024ed6b21a2718b0ef81433`; 17 commits externos previos a esta sesión agregaron ocho workflows y [reporte](evidence/T0.4-execution-preflight-2026-11-18.md), **ninguno cambió archivos canónicos/STATE**. Se inspeccionaron y evitaron repeticiones duplicadas.
- [P01 `generate`+Qwen local run 44446153287](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44446153287): DS1000 validation513 `ds1000_scorer=I`; negativo verificado, **no resultado C1**.
- ReAct C1 original en Qwen/Ollama falló [runs 44449013450 y 44449902121](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44449013450), también [aritmética pública run 44451155217](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44451155217) con `TypeError: float + Timeout`. Pin `openai==2.30.0` corrigió integración sin alterar solver ni scorer ([run 44451480318](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44451480318)); aritmética se evaluó incorrecta, sin error de ejecución.
- **D-0011:** [Run C1 44451780572](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44451780572), `ds1000_validation` muestra 513, `status=success`, `error=false`, SHA256 log `fc6978d9b7017087c22c424ec73238062affde02d5d0880b1160024ed52fa106`, sin scoring. [Evidencia](evidence/T0.4-reconciliation-and-c1-2026-11-19.md) y [autoverificación](audits/T0.4-FEASIBILITY-GATE-2026-11-19.md). **Cerrar T0.4 únicamente para viabilidad C1/P01**, sin afirmar ciencia reproducida ni viabilidad C2/C3/otros slots.
- C2 timeout de Docker; C3 no integrado; P06/P07 jueces pagos no aprobados; CI sin GPU, modelo pequeño. **Próxima T0.5**: puntuar y reproducir sólo C1/P01 con scorer original aislado y logs legalmente preservables. Presupuesto API pagas=0, no usar test ni subir prompts/golds al repo público.

## 2026-11-19 — D-0012: T0.5 — replicación exploratoria C1/P01 con score negativo

- HEAD inicial T0.5 `c3bc587481d8028c21eeead4b73344c1273fa6c7`; se leyeron STATE y documentos canónicos; el producto se restringió a **C1/P01** conforme al cierre T0.4.
- Se construyó [workflow de scoring aislado](.github/workflows/h0-c1-ds1000-scored.yml) y se intentó dos veces: [44457571911](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44457571911) y [44458771354](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44458771354), `solve=success` en muestra 513, pero `inspect score` con env congelado Asta0.5.5/Inspect0.3.225 **falló sin puntuar**; segundo fallo `LookupError/registry`. No alterar scorer. Se detectó que DS1000 original depende de sandbox durante scoring; hipótesis de conflicto con re-score de log, no diagnóstico único del LookupError.
- Se validó [adaptación de dependencias conservando código C1 original](.github/workflows/h0-c1-frozen-scoring-public-smoke.yml) en [smoke público 44459185759](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44459185759): Asta0.5.5/Inspect0.3.258, scorer inline, un sample aritmético válido sin API paga.
- **D-0012:** [run 44459486187](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44459486187), *mismo workflow* [inline original scorer](.github/workflows/h0-c1-ds1000-inline-scored.yml), dos intentos (jobs 135342496215 y 135345630230) sobre `ds1000_validation` ID513, Qwen3 0.6B local, original ReAct SHA, código scorer original: **I/I (incorrectos ambos)**, status success/error false, hashes de JSON diferentes conservados en [evidencia](evidence/T0.5-C1-DS1000-scoring-2026-11-19.md). No equivalencia binaria del runtime scorer congelado ni score de referencia publicado. Modelo minúsculo no validado para investigación científica.
- [Autoverificación T0.5](audits/T0.5-C1-DS1000-2026-11-19.md) **no independiente**: aceptar T0.5 sólo como calibración exploratoria de C1/P01 con duplicación del score negativo; **no** H0 completo ni H1/H2 autorizados. Scores + hashes y logs de CI públicos; trazas completas privadas eliminadas con runners; CPU/energía sin precio, gasto API pago cero.
- **Próxima T0.6:** auditoría crítica de H0, evaluar validez del instrumento, sesgos, necesidad de evidencia de autonomía/arquitectura/modelos y decisión continuar/corregir/replantear/retroceder. Mantener OBJECTIVE.md intacto.

## 2026-11-19 — D-0013: T0.6 — auditoría del hito H0 (NO APROBADO; CORREGIR)

- Leídos HEAD inicial `81cc173b186590789de0808a1d83c4ac0b517817`, STATE H0/T0.6, OBJECTIVE/PLAN/METHODOLOGY/AGENTS/README/RESEARCH/LOG, piloto y auditorías referenciadas. Verificada [run 44459486187](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44459486187) como 2 intentos de C1/P01 con puntuación externa original **`I/I`**; un sample, no dos. No se ejecutaron nuevos experimentos.
- [Registro de brechas T0.6](evidence/T0.6-H0-gap-register-2026-11-19.md) cuantifica 14 antecedentes, 3 candidatos (sólo C1 ejecutado), 7 slots diseñados (sólo ID513 puntuado), 2 intentos `I/I`, 29 workflow runs en API (17 success/12 failure de CI, **no scores**), costo API pagado 0 y costo total no mensurable.
- **Hallazgo nuevo de procedencia:** `inspect_evals.ds1000_dataset()` lee `xlangai/DS-1000` **split=test de origen**; AstaBench filtra por su propia validación 100/test 900. No afirmar `validation` nativa de HF ni exposición del test reservado de AstaBench sin distinguir partición. `xlang-ai/DS-1000` declara CC BY-SA4; `allenai/asta-bench` gated tiene condiciones separadas. Artefactos de GitHub Actions público no equivalen a traza privada.
- [Autoverificación de hito H0](audits/H0-MILESTONE-T0.6-2026-11-19.md) **no independiente**: T0.6 completa como auditoría, pero H0 **NO CUMPLE** el cierre (no investigación autónoma, un solo problema de código, trazas privadas perdidas, no comparación C2/C3 ni costos; scorer frozen0.3.225 no pudo puntuar).
- **D-0013: CORREGIR / CONTINUAR H0**, no retroceder investigación documental ni saltar a H1/H2. Prioridad T0.7: opciones existentes de conservación lícita/auditable de evidencias, con fuentes/licencias/privacidad/recursos; T0.8: tarea científica end-to-end con scorer viable; T0.9 condicional: calibración y comparación. Objetivo aprobado intacto. Cero gasto de API paga, cero experimentos en T0.6.

## 2026-11-19 — D-0014: T0.7 — procedencia y conservación de trazas

- HEAD inicial `e14ceb0f6cbddec825ad514af63a401188eb13bb`, STATE H0/T0.7; leídos canónicos y auditoría T0.6. Sin nuevos ensayos, gastos, secretos ni aceptación de licencias.
- [Matriz T0.7](evidence/T0.7-provenance-trace-retention-2026-11-19.md) verifica DS1000 CC BY-SA4 vs AstaBench gated no redistribución, split original/derivado, condiciones de campos del log, permisos de artifacts GitHub público y cuota eventual de Actions privado. Evaluadas seis alternativas de custodia/reconstrucción.
- **D-0014:** estándar mínimo **manifiesto público sanitizado + fuentes/licencias inmutables rehidratables por auditor autorizado**; **raw trace** sólo en destino con acceso controlado **y** derechos por campo confirmados. Ninguna infraestructura privada nueva creada ni tokens compartidos; raw logs históricos de T0.5 siguen irrecuperables. Si se requiere archivo histórico exacto para nuevas pruebas, queda pendiente acordar destino y acceso.
- [Autoverificación T0.7](audits/T0.7-PROVENANCE-RETENTION-2026-11-19.md), mismo ejecutor; cumplimiento **documental** de T0.7, no prueba real de persistencia privada ni independencia. Próxima **T0.8**: buscar tarea científica E2E con licencias/score viable, presupuesto API cero. H0 permanece no cerrado, H1/H2 no habilitadas.

## 2026-11-19 — D-0015: T0.8 — selección de benchmark de proceso científico

- Recuperado HEAD `e57fe63f53a97702cb5f53744f3d7f97281ec240`, STATE H0/T0.8; consultadas fuentes de R06–R08 y ResearchGym, y alternativas adicionales FIRE-Bench, DiscoveryWorld, OpenDiscoveryTrace y DFM-Bench; metadatos y código oficiales revisados, sin nuevos ensayos ni gasto de API paga.
- [Informe T0.8](evidence/T0.8-scientific-task-selection-2026-11-19.md) distingue generación de código (DS1000/ScienceAgentBench), reproducción de papers (CORE), redescubrimiento de ciencia real costoso (FIRE/ResearchGym), trazas para auditoría (OpenDiscoveryTrace/DFM) y **ciclo experimental completo simulado** (DiscoveryWorld).
- **D-0015:** adoptar condicionalmente **DiscoveryWorld Ai2** código Apache2 SHA `fd591323...` como **primer instrumento de calibración del método científico** (no resultado real). Instancia de desarrollo `Plant Nutrients Normal seed0`, original scorecard binario/procedural, conocimiento sujeto a revisor; solo 0 API paga, sin usar art/assets en GitHub. Reservar seeds1–4 localmente, no alegar holdout ciego.
- [Autoverificación T0.8](audits/T0.8-SCIENTIFIC-TASK-SELECTION-2026-11-19.md) no independiente; selección documental aprobada, **ejecutabilidad no probada**. Próxima T0.9: smoke instrumental sin LLM de API/scorer/retención para GitHub Actions, antes de cualquier campaña de agente. H0 sigue abierto.
