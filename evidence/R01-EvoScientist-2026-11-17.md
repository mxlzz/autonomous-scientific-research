# R01 — EvoScientist: auditoría documental T0.1.1

- **Fecha de consulta:** 2026-11-17 (UTC-03).
- **Tipo:** auditoría de fuentes públicas y lectura estática; **no** instalación, ejecución, benchmark ni reproducción.
- **Autores del artículo:** Yougang Lyu y colaboradores (2026).
- **Artículo de referencia:** [arXiv:2603.08127v2 (5 octubre 2026)](https://arxiv.org/html/2603.08127v2); [ficha y versiones](https://arxiv.org/abs/2603.08127).
- **Código inspeccionado:** [EvoScientist/EvoScientist](https://github.com/EvoScientist/EvoScientist), rama `main`, commit **`15f3e25bf86e55557d511367e16a3711c0f36934`** ([enlace inmutable](https://github.com/EvoScientist/EvoScientist/tree/15f3e25bf86e55557d511367e16a3711c0f36934)). No se ha establecido que este commit reproduzca el método del artículo.
- **Versión del paquete en el commit:** `0.4.3`, en [pyproject.toml](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/pyproject.toml).
- **Licencia:** Apache-2.0 confirmada para el **repositorio de código** por [LICENSE](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/LICENSE) y `pyproject.toml`; el texto del paper en arXiv está marcado CC BY 4.0. Las dependencias y servicios externos conservan sus propias licencias y condiciones.
- **Protocolo de consulta:** lectura de arXiv HTML v2 (método, setup, resultados, apéndices); API de GitHub para metadatos, SHA y árbol recursivo (`git/trees/<SHA>?recursive=1`, respuesta `truncated=false`); lectura estática de README, LICENSE, pyproject, módulo principal, YAML de subagentes, archivos de memoria y checkpointer. Sin ejecutar código. Los datos aquí se refieren a ese corte concreto, no a cambios posteriores.

## 1. Qué afirma el artículo (evidencia C: afirmación de autores)

- **Arquitectura del estudio:** Researcher Agent (RA) formula propuestas con búsqueda en árbol y selección Elo, Engineer Agent (EA) implementa y prueba con búsqueda en árbol, Evolution Manager Agent (EMA) destila estrategias de intentos y errores; dos memorias especializadas (ideación y experimentación). Recuperación por embeddings, similitud coseno. [Método, §3](https://arxiv.org/html/2603.08127v2).
- **Configuración informada:** Gemini-2.5-Pro para ideas y escritura, Claude-4.5-Haiku para código, Gemini-3-flash como juez de ideas, embeddings `mxbai-embed-large` mediante Ollama; 21 ideas máximas, 3 trabajadores paralelos, 4 trabajadores experimentales y presupuesto de intentos [20,12,12,18] en cuatro fases. [§4.5](https://arxiv.org/html/2603.08127v2).
- **Datos / evaluación:** 30 preguntas de investigación sobre IA; comparaciones de novedad, factibilidad, relevancia y claridad contra 7 baselines por juez LLM; evaluación humana focalizada sobre 4 comparadores con tres anotadores doctorales; éxito de ejecución en sandbox para código; 6 manuscritos sometidos a ICAIS 2025. [§4](https://arxiv.org/html/2603.08127v2).
- **Resultados de los autores:** ventaja en comparaciones de ideas; éxito medio de ejecución declarado de **34,39 % a 44,56 %** (+10,17 puntos porcentuales) después de la evolución de estrategias, mientras la fase 3 (método propuesto) pasa de **20,33 % a 21,57 %** (+1,24 pp); 6/6 manuscritos aceptados en la pista de AI Scientists, con dos distinciones. [§5.1–5.4](https://arxiv.org/html/2603.08127v2). *No reproducidos por este proyecto.*
- **Ablación declarada:** retirar memoria de dirección o de validación degrada juicios de ideas; estos contrastes **no aíslan** el efecto del número de agentes, la profundidad de descomposición ni los costos. [§5.4](https://arxiv.org/html/2603.08127v2).

## 2. Qué está directamente visible en el repositorio (inspección estática, no comportamiento verificado)

| Elemento | Evidencia en código | Inferencia limitada |
|---|---|---|
| Framework | [EvoScientist.py](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/EvoScientist/EvoScientist.py) usa `create_deep_agent`; `pyproject.toml` depende de `deepagents[quickjs]~=0.7.38` | Integración real de componentes, no reproducción experimental comprobada |
| Roles | [subagents/](https://github.com/EvoScientist/EvoScientist/tree/15f3e25bf86e55557d511367e16a3711c0f36934/EvoScientist/subagents): plan, research, code, debug, data_analysis y writing; también configuración de scheduler y agentes adicionales por composición | El README actual anuncia **6 subagentes**; no equivale exactamente a los **3 roles** RA/EA/EMA del artículo |
| Memoria | [memory/](https://github.com/EvoScientist/EvoScientist/tree/15f3e25bf86e55557d511367e16a3711c0f36934/EvoScientist/memory) contiene trabajadores pos-turno, almacenamiento de observaciones, relaciones y AutoSkills | El mecanismo de memoria actual no está identificado como implementación idéntica de las dos memorias del artículo |
| Persistencia técnica | [checkpointer.py](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/EvoScientist/langgraph_dev/checkpointer.py): checkpointer SQLite | Soporta estado técnico; por sí solo no acredita integridad metodológica |
| Acciones | YAML `research.yaml`, `code.yaml` y motor de herramientas/comandos | Hay mecanismos para investigar y producir scripts; sin demostración en nuestro entorno |
| Reproducción de paper | Árbol completo de `main` inspeccionado (776 entradas, no truncado) | No se identificó en ese árbol un paquete explícito de scripts/datos/resultados para reproducir tablas y figura del paper; **no** demuestra que nunca existieran en otra versión o lugar |

## 3. Requisitos y reproducibilidad

- El paquete declara **Python >=3.11** y dependencias de orquestación (DeepAgents/LangGraph), conectores de modelos y opciones de canales; modelos remotos requieren proveedor/credenciales y pueden generar costos. [`pyproject.toml`](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/pyproject.toml).
- El proyecto actual ofrece CLI, WebUI, tareas cron y asistencia de entorno, según [README en commit fijado](https://github.com/EvoScientist/EvoScientist/blob/15f3e25bf86e55557d511367e16a3711c0f36934/README.md). Son prestaciones declaradas, no ensayadas aquí.
- Los 30 prompts del estudio aparecen en la **Figura 3** del paper; los prompts de evaluación y evolución aparecen en figuras de apéndice. La auditoría no verificó archivos independientes, salidas brutas, costes por llamada, seeds, versión exacta de implementación del paper ni un protocolo ejecutable que regenere todas las tablas.
- Versionar `main@15f3e25` hace reproducible **la inspección estática**, no los experimentos del artículo.

## 4. Límites y puntos ciegos (crítica de validez, inferencias D)

1. **Validez científica ≠ calidad de ideas:** novedad/factibilidad/claridad percibidas, ejecución exitosa y aceptación en una pista de artículos de IA son señales parciales; no prueban ausencia de errores científicos ni replicabilidad de hallazgos.
2. **Comparación acotada:** 30 preguntas en dominios de IA y sólo 6 casos de manuscritos; la elección de modelos y la ausencia de costo integral documentado impiden inferir eficiencia de modelos livianos.
3. **Cambio de objeto:** el software `0.4.3` es una plataforma evolucionada respecto del esquema RA/EA/EMA publicado; tratar sus pruebas actuales como réplica directa del paper produciría una atribución incorrecta.
4. **Efectos confundidos:** las ablaciones IDEA/VALIDACIÓN no controlan cantidad de agentes ni granularidad frente a monoagente, que son hipótesis independientes del proyecto.
5. **Procedencia de resultados:** no se halló un conjunto listo para replicación de cifras del artículo en el árbol público `main` examinado; se necesita localizar un commit de investigación, datasets y protocolo antes de pretender replicarlas.
6. **Limitación reconocida por los autores:** evaluación centrada en investigación computacional; no acredita generalización a laboratorios físicos. [§7](https://arxiv.org/html/2603.08127v2).

## 5. Relación con el objetivo aprobado y decisión

- **Directamente relevante** para H0 (alternativa existente para evaluar), H3/H4/H5/H6 (memoria, persistencia, verificación y reutilización de experiencia); su diseño inspira ensayos pero no valida las hipótesis.
- **No responde todavía** H1/H2/H3 de nuestro plan: falta contraste controlado de granularidad, mono/multiagente, política de modelos y costo por resultado **científicamente válido**.
- **Decisión T0.1.1:** **COMPARAR / CANDIDATO CONDICIONAL A REPRODUCCIÓN**. No adoptar como baseline científica validada ni desarrollar un clon. En T0.2, comparar viabilidad contra sistemas más simples y solicitar/identificar paquete reproducible si se decide ensayarlo.
- **Pendientes explícitos:** confirmar correspondencia paper↔commit experimental; archivos brutos/splits/seeds y cómputo; ejecución segura y costo, licences de dependencias; cualquier réplica independiente y calidad de hallazgos.
- **Gasto:** 0 pagos; ninguna ejecución de EvoScientist ni llamada a modelos de tercero realizada para el experimento.

**Calificación:** evidencia de código/documentación observada directamente; eficacia científica declarada por autores = nivel C, sin nivel A en este proyecto. Revisión realizada por el mismo ejecutor; **sin auditor externo**.
