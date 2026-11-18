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
