# Metodología y control de rigor — versión 1

## 1. Jerarquía de evidencia
Distinguir: (A) resultado reproducido localmente con datos/código/logs; (B) resultado de tercero documentado y auditado; (C) declaración de proyecto/publicación no comprobada; (D) hipótesis o interpretación propia. Nunca convertir C o D en A. Cada afirmación experimental debe remitir a evidencia concreta y reproducible.

## 2. Preguntas falsables y diseño causal
Hipótesis H1–H6 en OBJECTIVE.md. Factores: arquitectura (1 vs N agentes), granularidad (sin descomposición / intermedia / fina), política de modelos (grande fijo / pequeño fijo / dinámica), persistencia (simple / estado auditado), revisión (autorrevisión / auditoría separada). Separar el efecto de los factores mediante comparaciones controladas; no ejecutar un factorial completo antes del piloto. Elegir interacciones sobre evidencia piloto, preregistrar comparaciones confirmatorias y sus cambios.

## 3. Tareas y evaluadores
**Control T0.6:** distinguir **generación de código para ciencia** de **investigación científica autónoma** (hipótesis, método, ejecución, interpretación, evidencia y control de defectos). Una tarea DS1000 aislada sólo calibra herramientas/scorer; no alcanza por sí sola el criterio de H0. Documentar para cada conjunto si el split es nativo o una partición **derivada** (DS1000 original `test` → AstaBench `validation/test`) y exposición de los ejemplos antes de analizar resultados. Usar tareas de benchmarks existentes con licencias y métricas revisadas (AstaBench, ScienceAgentBench, ResearchGym) y casos propios solo con evaluador independiente predefinido. Reservar pruebas fuera de desarrollo y documentar fechas de corte y exposición al benchmark para reducir contaminación. No optimizar sobre test reservado. Medir dificultad, dominio, longitud y tipo de razonamiento para comparar grupos. **Control incorporado tras T0.5:** en tareas cuyo scorer ejecuta código vía `sandbox()` (p. ej. DS1000), comprobar que el mecanismo de puntuación mantiene el contexto original; `inspect score` separado no se presume equivalente a scoring inline. Si hay desvío de versiones entre scorer congelado y runtime compatible, fijar ambas, documentar el cambio de método, registrar fallos y no afirmar equivalencia causal sin demostrarla. [Evidencia T0.5](evidence/T0.5-C1-DS1000-scoring-2026-11-19.md).

## 4. Equidad y repetición
Mismas tareas, herramientas, acceso a datos, límite de tokens/tiempo/costo y número de intentos. Registrar modelo/versiones, temperatura/semillas cuando apliquen, prompts, llamadas, herramientas, tiempos, reintentos, paradas y especificaciones de hardware. Aleatorizar orden o bloquear por tarea. Ejecutar repeticiones independientes; intervalos de incertidumbre, tamaño muestral y análisis de potencia antes de conclusiones confirmatorias. Reportar resultados por tarea y agregados.

## 5. Métricas
**Primaria:** costo total por **resultado científicamente válido**, donde validez exige evaluador externo satisfecho + ausencia de defectos metodológicos detectados; fallos e inconclusos cuentan en denominador. Incluye invocaciones, tokens, repeticiones, ejecución, revisión humana y cómputo local (metodología de imputación declarada).
**Secundarias:** tasa de resultados válidos, defectos por tipo/severidad, evidencia por afirmación, reproducibilidad, duplicación, desvíos del objetivo, tareas inválidas, costo, tokens, duración, intervenciones, energía/CPU/GPU, recuperación tras fallos y mejoras de calidad. Distinguir falla de infraestructura de falla científica; reportar ambas.

## 6. Umbrales provisionales (NO preregistro)
Como blanco inicial para H3: al menos 50 % de reducción del costo por resultado válido, con pérdida de validez no superior a 5 puntos porcentuales respecto del control, sujeto a análisis de potencia, márgenes y viabilidad antes de etapa confirmatoria. Estos límites no autorizan a proclamar éxito en el piloto. Para H1/H2 no asumir beneficio: reportar efectos positivos, negativos y no concluyentes.

## 7. Auditoría científica
Antes: revisión de validez de evaluador, licencias y preregistro. Durante: separar datos, código y narración, con enlaces de procedencia. Después: comprobar replicabilidad desde el commit/entorno exactos, selección de métricas, leakage, errores estadísticos y afirmaciones sin evidencia. Preferir tests deterministas y revisor humano cuando factible; un segundo LLM por sí solo no constituye auditoría independiente.

## 8. Protocolo de ejecución
Cada unidad: pregunta acotada -> antecedente -> hipótesis -> criterio de aceptación -> recursos/autorización -> ejecución -> logs y outputs -> evaluación contra criterio -> auditoría -> persistencia verificada -> actualización FINAL de STATE.json. Publicar comandos, dependencias, hashes, datos o referencias a datos accesibles; si son pesados guardar manifiestos y URL/identificador inmutable. Mantener experimentos fallidos.

## 9. Persistencia y recuperación
**Protección y posibilidad de auditoría (T0.6):** tratar por separado la licencia del **dataset original**, la del **wrapper benchmark** y la del **registro de interacción generado**. Un hash sin conservar el artefacto verifica integridad sólo si puede recuperarse posteriormente; no sustituye una traza. Los artifacts de Actions en repos públicos son accesibles a lectores del repositorio: no usarlos como almacén privado de muestras o secretos. Elegir modo permitido de conservación o paquete de reproducción para auditor autorizado antes de nuevas afirmaciones científicas; documentar excepciones y evaluar herramientas existentes.

GitHub es la fuente canónica, no el chat. Antes de escribir: leer SHA del archivo y HEAD, comparar con estado esperado, no sobrescribir cambios ajenos. Guardar primero evidencia y LOG; comprobar lectura posterior; sólo entonces actualizar STATE.json. STATE debe mencionar tarea, fase, evidencia, auditoría, decisiones, bloqueos y último cambio de contenido confirmado (no puede autorreferenciar su propio commit SHA). En conflictos, detener escritura y reconciliar diferencias. Si falla el último guardado, informar estado real sin afirmar persistencia; reanudar leyendo HEAD y reconstruyendo desde contenido confirmado.

## 10. Recursos y seguridad
Sin autorización explícita, gasto pagado máximo **cero**. No asumir cuotas gratis disponibles. Ejecutar código de terceros solo en sandbox/entorno aislado y con dependencias auditadas; no incluir secretos en logs, repositorio ni prompts. No ejecutar tests costosos por mera curiosidad. El estudio no altera su objetivo por nuevos avances o ideas.

## 11. Decisiones de hito
Al cierre auditar criterio, coherencia con OBJECTIVE.md, representatividad, fuentes, negatividad y costos. Resultado obligatorio: continuar, corregir, replantear o retroceder, con motivos y enlace al registro en audits/. Sin auditoría satisfactoria no se habilita el hito siguiente.