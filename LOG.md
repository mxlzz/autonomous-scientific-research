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
