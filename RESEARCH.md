# Estado del arte y registro de antecedentes

**Corte inicial:** 2026-11-17. Registro preliminar basado en publicaciones y documentación originales enlazadas. Enlaces contrastados durante el diseño; **ninguna implementación ha sido instalada, ejecutada o reproducida por este proyecto**. Licencias efectivas, dependencias, versiones, commits y claims cuantitativos se verificarán en T0.1. No se afirma exhaustividad de la revisión.

## Inventario inicial (fuente única de referencias)
| ID | Sistema / fuente primaria | Función | Decisión preliminar | Estado |
|---|---|---|---|---|
| R01 | [EvoScientist código](https://github.com/EvoScientist/EvoScientist) · [artículo v2](https://arxiv.org/html/2603.08127v2) | Agentes, memoria y ejecución de investigaciones computacionales | **Comparar; reproducción condicional** | **Auditoría documental T0.1.1 cerrada**: código 0.4.3 @ [`15f3e25`](https://github.com/EvoScientist/EvoScientist/tree/15f3e25bf86e55557d511367e16a3711c0f36934), Apache-2.0; no ejecutado. [Ficha](evidence/R01-EvoScientist-2026-11-17.md) · [Autoverificación](audits/T0.1.1-R01-2026-11-17.md) |
| R02 | [DeepScientist](https://github.com/ResearAI/DeepScientist) · [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4f64494ecc3442f1c9261baa036378bc-Abstract-Conference.html) | Investigación experimental de larga duración | Candidato a reproducir | Enlace; afirmaciones de autores |
| R03 | [AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) | Búsqueda de ideas, experimentos y elaboración de artículos | Comparar / adaptar | Enlace; sin reproducción |
| R04 | [autoresearch](https://github.com/karpathy/autoresearch) | Ciclo experimental sencillo con métrica | Baseline conceptual | Enlace; sin reproducción |
| R05 | [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | Pipeline de investigación asistida | Comparar | Enlace; sin reproducción |
| R06 | [AstaBench](https://github.com/allenai/asta-bench) · [baselines](https://github.com/allenai/agent-baselines) | Evaluación y agentes de referencia | Benchmark prioritario | Enlace; sin ejecución |
| R07 | [ResearchGym](https://github.com/Anikethh/ResearchGym) · [artículo](https://arxiv.org/abs/2602.15112) | Investigación computacional de extremo a extremo | Benchmark candidato | Enlace; sin ejecución |
| R08 | [ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) | Código y resultados científicos | Benchmark candidato | Enlace; sin ejecución |
| R09 | [ScientistOne](https://arxiv.org/abs/2605.26340) | Cadena de evidencia y verificación de afirmaciones | Adaptar criterios | Publicación, sin validar claims |
| R10 | [LongHorizon-Harness](https://arxiv.org/abs/2608.01964) · [código](https://github.com/AMAP-ML/LongHorizon-Harness) | Gestión de estado y recuperación prolongada | Comparar/adaptar | Publicación y repositorio; sin prueba |
| R11 | [Minions](https://mlanthology.org/iclrw/2025/narayan2025iclrw-costefficient/) | Delegación local/remota para eficiencia | Inspirar contraste H3 | Publicación; generalización abierta |
| R12 | [RouteLLM](https://arxiv.org/abs/2406.18665) · [proyecto](https://sky.cs.berkeley.edu/project/routellm/) | Selección de modelos según costo/rendimiento | Adaptar enrutamiento | Publicación; sin prueba científica |
| R13 | [Capable language models can outgrow the benefits of collaboration](https://www.nature.com/articles/s42256-026-01268-y) | Comparación controlada de arquitecturas | Fundamentar H2 | Publicación revisada por pares |
| R14 | [LangGraph](https://github.com/langchain-ai/langgraph) · [persistencia](https://langchain-ai.github.io/langgraph/reference/checkpoints/) | Checkpoints y recuperación técnica | Componente candidato | Documentación; no implica rigor científico |
| R15 | [OpenHands](https://github.com/All-Hands-AI/OpenHands) | Ejecutar y modificar código | Infraestructura candidata | Documentación; no implica descubrimiento |
| R16 | [Asta recursos](https://allenai.org/asta/resources) | Herramientas y evaluación homogénea | Adoptar si es viable | Documentación institucional |

## Comparación / vacío identificado
- R01, R02, R03 y R05 integran varias partes del ciclo científico. **Falta verificar** reproducibilidad, condiciones de fallo, costos y transferencia a otras tareas.
- R04 constituye un control más simple; no equiparar optimizar una métrica fija a investigar preguntas abiertas.
- R06–R08 ofrecen instrumentos para evitar evaluaciones autodeclaradas, pero sus tareas, licencias y recursos deben auditarse.
- R09 prioriza la integridad de afirmaciones; R10 y R14, el estado técnico. Debemos comprobar si su combinación previene conclusiones inválidas en ejecuciones prolongadas.
- R11–R12 muestran posibilidades de eficiencia; **no demuestran** que sustituir modelos grandes por pequeños preserve rigor científico general.
- R13 advierte contra asumir beneficios universales del multiagente. La arquitectura debe compararse, no prefijarse.

## Decisión de adopción actual
**Adoptar para evaluación:** benchmark y baselines existentes si son reproducibles. **Reproducir primero:** candidatos R01, R02 y baseline R04 según viabilidad de H0. **Adaptar condicionalmente:** cadena de evidencia, verificadores, persistencia y enrutamiento. **Desarrollar:** solo si falla una capacidad exigida y queda demostrada la necesidad.

## Pendientes metodológicos de revisión
T0.1 debe ampliar fuentes originales relevantes, verificar licencias, versiones y resultados, clasificar evidencia y detectar duplicaciones. Antes de experimentos: comprobar filtración de benchmark, modelos contaminados, validez de métricas y equiparación de presupuestos. No atribuir capacidades o cifras más allá de lo demostrado por la fuente.

## Formato obligatorio para ampliar el registro
ID | autor/año | enlace primario | fecha de acceso | versión/commit y licencia (o desconocido) | claim preciso | tipo de evidencia (documentación, estudio, reproducción independiente) | límites | relevancia | decisión (adoptar/adaptar/comparar/descartar) | evidencia local asociada.

La primera unidad T0.1.1 examinará **R01 EvoScientist** en profundidad, sin ejecutar código. [Plan](PLAN.md) | [protocolo](METHODOLOGY.md).
## Auditoría documental R01 — EvoScientist (T0.1.1, 2026-11-17)

- **Autor / publicación:** Lyu et al., 2026, [arXiv 2603.08127v2](https://arxiv.org/html/2603.08127v2) (5 de octubre); **consulta:** 2026-11-17.
- **Código público fijado:** `EvoScientist/EvoScientist@15f3e25bf86e55557d511367e16a3711c0f36934`; versión `0.4.3`; **licencia Apache-2.0** comprobada; Python >=3.11. No hay ejecución ni validación de equivalencia entre código y paper.
- **Claim (nivel C):** 3 roles RA/EA/EMA y 2 memorias; estudios con 30 consultas de IA, éxito de código según autores de 34,39 % a 44,56 % tras evolución; 6/6 manuscritos aceptados en pista IA de ICAIS 2025. Evidencia: artículo, no réplica independiente.
- **Dato inspeccionado:** repositorio actual basado en DeepAgents con seis subagentes operativos documentados, memoria por observaciones/AutoSkills y checkpoint SQLite. **No identificar** automáticamente esta versión con la implementación del paper.
- **Límites:** éxito de ejecución y calificación de propuestas no equivalen a validez científica; evidencia restringida a investigación computacional; ausencia de paquete de reproducción identificado en el árbol actual; costo por resultado científicamente válido y contraste mono/multiagente no evaluados.
- **Decisión:** comparar en H0 y eventualmente probar como baseline si resulta viable; no copiar ni afirmar superioridad. **Detalle y fuentes fijas:** [evidence/R01-EvoScientist-2026-11-17.md](evidence/R01-EvoScientist-2026-11-17.md). **Autoverificación:** [audits/T0.1.1-R01-2026-11-17.md](audits/T0.1.1-R01-2026-11-17.md).
