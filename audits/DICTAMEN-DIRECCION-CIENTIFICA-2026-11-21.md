# Dictamen de continuidad de la investigación

**21 de noviembre de 2026. Corte documental de main:** `874cf7e83168c04ef4af597374eba4c2c91a828e`. Actualización operativa verificada hasta el job del commit `08732a9da7ab9496b008189f2ab67083eec4108f`. Revisión transversal solicitada por el usuario. Autoevaluación técnica con comprobaciones en otro entorno. La revisión carece de arbitraje humano independiente. El estado de ese corte da por cerrada T0.51 y designa T0.52 como la próxima réplica operacional. Este dictamen es una propuesta para decidir y pertenece a una rama separada del historial de ejecución.

**Actualización que prevalece para ejecutar.** Este es el informe histórico de la revisión. Después, la corrida 44909561018 sí inició la réplica y terminó sin entrega. La reparación del import está en main. D-0062 incorpora los hallazgos metodológicos y sustituye la recomendación histórica de repetir por una unidad de diseño offline. Para actuar usar el [estado vigente](../STATE.json) y la [guía de decisión](../benchmarks/H0-DECISION-BASELINE.md). [Resultado de la réplica](../evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md).

## Decisión

**Continuar con una inversión limitada.** La herramienta de evaluación ya permite distinguir una política que obtiene un resultado defendible de otra que entrega una predicción gravemente equivocada. El valor propio del proyecto está en averiguar cuándo estructurar o delegar trabajo mejora la ciencia por unidad de recurso. La evidencia disponible alcanza para justificar una comparación acotada una vez validado el instrumento. Es insuficiente para justificar un framework, una jerarquía de agentes o una campaña abierta de ajustes de infraestructura.

El objetivo aprobado permanece idéntico al inicial. El plan original contemplaba reproducir una línea base en H0 y comparar arquitectura, enrutamiento y continuidad en hitos posteriores. La matriz de antecedentes, el evaluador externo, el registro de fallos y las pruebas de aislamiento sirven a H0. El caso térmico abarca decisiones bajo incertidumbre y evaluación contra una verdad externa. Su interfaz acotada y su duración dejan sin probar búsqueda bibliográfica, creación de herramientas, mantenimiento del objetivo entre sesiones y recuperación de fallos científicos. La continuidad del ejecutor mediante GitHub tampoco mide esas capacidades en el agente experimental. [Objetivo](../OBJECTIVE.md) · [Plan inicial](https://github.com/mxlzz/autonomous-scientific-research/blob/5f79f45/PLAN.md) · [Auditoría del hito](H0-MILESTONE-T0.50-FIRST-SCORED-SCIRESEARCH-2026-11-21.md).

## Evidencia contrastada

T0.26 ejecutó dos políticas programadas sobre cuatro casos de desarrollo elegidos por complejidad visible. Hubo siete puntuaciones de ocho episodios y tres pares completos. En el caso de 40 celdas la heurística sí hizo una medición adicional y redujo la puntuación de intervalo objetivo de 585,52 a 6. En el de 20 celdas el ajuste de parámetros no mejoró y el cómputo simulado creció 1,82 veces. Hay evidencia de que gastar más tiene rendimientos distintos según el caso, circunscrita a estas políticas. [Observaciones por episodio](../experiments/T0.26-sciresearch-multicase-observations.json).

Comparación descriptiva en el mismo caso `task_525abee377`, con el mismo evaluador. El error absoluto se mide en desviaciones estándar del ruido del sensor. Una puntuación de intervalo menor es mejor.

| Política | Error de predicción / sigma | Puntuación del intervalo objetivo | Cobertura de parámetros | Mediciones nuevas |
|---|---:|---:|---:|---:|
| Control programado simple | 2,274 | 6,00 | 0 % | 0 |
| Control heurístico | 0,104 | 6,00 | 100 % | 0 |
| Qwen3 4B T0.49 | 14.861,231 | 593.803,23 | 0 % | 0 |

Volví a ejecutar ambas políticas originales con un entorno nuevo para cada una, el mismo identificador y el evaluador fijado. Reproduje las cifras de la tabla a la precisión indicada. Para Qwen verifiqué directamente los marcadores del job original. Hubo 8 turnos, 8 intentos de herramienta, 2 errores y una entrega puntuada. La evidencia documental duplicada de T0.49 se refiere a ese mismo job. La inferencia del modelo no se repitió en esta auditoría. [Datos de controles](../experiments/T0.26-sciresearch-multicase-observations.json) · [Job de Qwen](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967/job/136854644115) · [Prerregistro del modelo](../experiments/T0.49-qwen4b-science-180s-request-observability-preregister-2026-11-21.md).

En este caso ambos controles obtuvieron una predicción razonable sin medición adicional. Por lo tanto, contar mediciones, herramientas o turnos por sí solo premiaría actividad sin demostrar criterio. Las políticas programadas acceden directamente a la API del entorno. El control simple realiza un ajuste y propaga la incertidumbre con hasta 24 simulaciones de muestreo además de la central. En T0.26 se registraron 28 acciones para el simple y 36 para la heurística. Qwen pasa por otra interfaz, con lecturas resumidas y umbrales de ocho turnos y ocho herramientas. Las acciones de entorno y las llamadas de interfaz tienen distinta granularidad. La diferencia de puntuación caracteriza los sistemas tal como se ejecutaron, sin identificar el efecto causal del modelo, de sus parámetros o de la arquitectura. [Políticas originales](https://github.com/Btwestyo/sciresearch-eval/blob/9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0/src/sciresearch_eval/baselines/scripted.py#L47-L71) · [Interfaz del agente](https://github.com/Btwestyo/sciresearch-eval/blob/9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0/src/sciresearch_eval/agents/tools.py#L187-L194).

## Fallos y correcciones

1. **La métrica principal admite dos cálculos incompatibles.** La sección 5 de METHODOLOGY define costo por resultado válido y agrega que los fallos cuentan en el denominador. Definir dos fórmulas separadas. Costo por válido = suma de costos de todos los intentos / cantidad de resultados válidos. Tasa de validez = válidos / intentos iniciados según una definición previa del inicio. Con cero válidos, publicar el costo acumulado y cero válidos sin estimación finita del cociente. Conservar gastos de preparación y fallos de infraestructura como partidas separadas y contabilizar su costo para la decisión de despliegue. En SciResearch, el evaluador entrega un vector y la entrega solo habilita el cálculo. Antes de ver casos nuevos, fijar qué combinación de precisión, incertidumbre y defectos metodológicos define validez. [Método](../METHODOLOGY.md#5-métricas) · [Evaluador original](https://github.com/Btwestyo/sciresearch-eval/blob/9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0/src/sciresearch_eval/grader.py#L24-L96).
2. **El registro descarta un resultado válido y omite medidas de proceso disponibles.** El controlador incluye `target_covered` como booleano. El monitor de T0.49 trata cualquier campo `SCORE_*` como flotante. Comprobé que rechaza ambas serializaciones booleanas y que acepta `0.25` en ese mismo campo. El log público no permite reconstruir ese booleano por esta vía. Además, el evaluador calcula `checked_convergence` y `final_fit_converged` a partir de la traza, pero ambos faltan en la selección del controlador. En la repetición local del caso, ambos fueron falsos para el control simple y verdaderos para la heurística. Definir una lista de métricas con tipo y admisión de nulos por campo, y probar el trayecto completo desde una calificación conocida hasta el registro público. Estos indicadores aportan evidencia de método aun cuando los argumentos y la traza se mantengan privados. Las categorías de T0.51 permiten saber si se pidió un ajuste, pero la categoría por sí sola no dice si se comprobó la convergencia. [Controlador](../scripts/h0_sciresearch_qwen_t049.py#L28-L31) · [Monitor](../scripts/h0_science_cgroup_t049.py#L37-L58) · [Medidas de proceso del evaluador](https://github.com/Btwestyo/sciresearch-eval/blob/9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0/src/sciresearch_eval/grader.py#L161-L172).
3. **Repetición y generalización requieren diseños distintos.** T0.49 llegó a 28.248 tokens de entrada frente al umbral blando de 24.000, incluida la última vuelta permitida. Mantener esa regla permite repetir la configuración. Para comparar intervenciones también hay que registrar consumo efectivo, tiempo de máquina y trabajo de revisión, ofrecer el mismo acceso a herramientas y predefinir cómo se computan fallos e inconclusos. Un segundo episodio sobre el mismo caso prueba repetibilidad operacional. Cambiar de caso y reservar otros antes del ajuste permite empezar a estudiar transferencia. Mantener el caso de calibración fuera de toda evaluación confirmatoria. [Contrato T0.51](../evidence/T0.51-offline-soft-budget-tool-category-n2-gate-2026-11-21.md) · [Auditoría de replicabilidad](H0-MILESTONE-T0.50-FIRST-SCORED-SCIRESEARCH-2026-11-21.md).
4. **H0 carece de un límite global práctico.** El plan inicial llegaba a la primera decisión de H0 en T0.6. En el corte hay 55 entradas completadas incluidas subtareas, tres auditorías formales de H0 y un solo episodio de un LLM puntuado en SciResearch. Hay resultados experimentales anteriores al de Qwen, en particular los controles. El estado lista 48 entradas bajo bloqueos y 56 bajo auditorías pendientes, con historia acumulada. Comprobé que existen las 80 rutas de evidencia y las 58 referencias de auditorías del estado. El coste organizativo es distinguir qué falta para decidir hoy entre lo que ya se intentó. Mantener los registros históricos, identificar por separado los impedimentos vigentes, asignar a cada nueva corrida un identificador único independiente de cuántos documentos la describen y resumir en una fila por corrida la pregunta, el resultado y la decisión que habilita. Para este hito usar criterios separados de reproducibilidad del instrumento y calidad del candidato. Un fracaso reproducible puede ser un resultado de H0. [Estado auditado](../STATE.json) · [Auditoría intermedia](H0-MILESTONE-T0.27-2026-11-20.md) · [Bitácora](../LOG.md).
5. **El aporte frente a trabajos existentes debe estar en la comparación.** SciResearch-Eval ya publica grader, políticas de referencia y reportes de modelos evaluados con protocolos propios. AstaBench ya abarca varias partes de la investigación. Las cifras de esos trabajos sirven como antecedentes. Para identificar un aporte propio, medir una intervención simple bajo recursos acotados y comprobar si cambia resultados, cuándo conviene usarla y cuándo empeora la ciencia. Una segunda tarea que exija escribir y ejecutar análisis será necesaria antes de extender la conclusión a investigación computacional autónoma. [Informe original de SciResearch](https://github.com/Btwestyo/sciresearch-eval/blob/9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0/results/TEST_v1.md) · [AstaBench](https://allenai.org/asta/bench).

El proyecto también emplea H3 para dos objetos diferentes. H3 en OBJECTIVE es la hipótesis de enrutamiento y H3 en PLAN es el hito de persistencia. Conviene identificar por separado hipótesis e hitos y hacer explícita su correspondencia al prerregistrar cada comparación. [Hipótesis aprobadas](../OBJECTIVE.md) · [Dependencias del plan](../PLAN.md).

## Regla de inversión propuesta

- **Primero** reconciliar los dos intentos de T0.52 descritos al final. La réplica científica sigue pendiente en el corte operativo. Antes de comprometer otro runner, probar el arranque del controlador con exactamente los módulos que se montarán en ejecución. Una nueva ejecución que se justifique debe preservar las condiciones científicas y registrarse explícitamente después del fallo de integración. Un cambio puramente observacional debe quedar identificado y probado. Registrar el signo de la diferencia respecto a los controles y la capacidad efectiva del instrumento para captar los campos acordados. Es legítimo que arroje otro negativo.
- **Si la medición y el comparador son viables**, cerrar la decisión de H0 contra sus criterios y, cuando proceda, realizar un piloto pequeño con varios casos de desarrollo seleccionados por anticipado. Usar el mismo Qwen con las mismas herramientas, modelo y política de presupuesto en dos condiciones que cambien un solo factor, por ejemplo trabajo libre frente a descomposición explícita. Mantener ambos scripts originales como referencias externas. Bloquear por caso, alternar o sortear el orden, fijar repeticiones y publicar por separado precisión, cobertura, costos efectivos, validez e intervenciones. Un piloto exploratorio pequeño solo decide si amerita una prueba mayor. Para afirmaciones confirmatorias hacen falta margen predefinido, incertidumbre y tareas reservadas.
- **Si la réplica vuelve a ser mala pero auditable**, registrar el candidato como débil bajo esas condiciones. La variación respecto al control y la capacidad de medir una sola intervención determinan si vale la pena un piloto. **Si tras esa réplica sigue siendo imposible observar el resultado científico relevante o construir un control comparable con los recursos autorizados**, cerrar la vía Qwen4B/CPU y pausar nuevas pruebas hasta identificar un sustituto viable dentro del objetivo. Si ambos tratamientos quedan en el piso de la métrica y el piloto no puede distinguir mejoras, suspender esa configuración. Ninguna de estas decisiones autoriza gasto ni modificación del objetivo.

## Comprobaciones reproducibles

Versión oficial de SciResearch usada en la auditoría: `9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0`. Entorno local Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, BLAS de un hilo. Es una reproducción de métricas redondeadas en otra instalación. La equivalencia binaria, el consumo energético, las decisiones textuales de Qwen y la independencia científica externa quedan sin verificar.

Desde el checkout de SciResearch en la revisión indicada:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src python - <<'PY'
from pathlib import Path
import numpy as np
from sciresearch_eval.baselines.scripted import naive, heuristic
from sciresearch_eval.env import ThermalEnv
from sciresearch_eval.grader import grade

fields = ("param_coverage", "target_interval_score", "target_abs_error_over_sigma",
          "experiments_used", "checked_convergence", "final_fit_converged")
for policy in (naive, heuristic):
    np.random.seed(0)
    env = ThermalEnv("task_525abee377", Path("tasks"), "dev")
    policy(env)
    scores = grade(env)
    print(policy.__name__, {key: scores[key] for key in fields})
PY
```

Desde este proyecto, con el checkout del benchmark en `../upstream-sci`:

```bash
python scripts/h0_tool_categories_t051.py --offline-test \
  --harness ../upstream-sci/src/sciresearch_eval/agents/harness.py \
  --tools ../upstream-sci/src/sciresearch_eval/agents/tools.py
PYTHONPATH=scripts python - <<'PY'
from h0_science_cgroup_t049 import classify_result_line

for value in ("True", "False", "0.25"):
    print(value, classify_result_line("T049_SCORE_TARGET_COVERED=" + value))
PY
```

Resultado de T0.51 en esta instalación: 20 fixtures válidos y 11 rechazados, con compilación del parche sobre la fuente fijada. La prueba del monitor devolvió `None`, `None` y un diccionario con `0.25`, respectivamente. Se contrastó el job de T0.49 contra el scorer oficial. No se repitió ninguna inferencia, no se usó el conjunto reservado y no se contrató cómputo.

## Actualización observada durante la revisión

Con posterioridad al corte documental, el commit `9fc91bc` activó el primer workflow T0.52. La prueba offline del monitor falló al verificar la clasificación de entradas conocidas. El job omitió la preparación de imágenes, la descarga del modelo y el episodio. Esta ejecución acredita un fallo de integración anterior a la inferencia y aporta cero observaciones científicas. El registro del job permite distinguirlo de un fracaso de Qwen. [Job T0.52](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909209749/job/136861215232).

El workflow corregido, commit `08732a9`, finalizó con estado `success`. La prueba sintética llamó una vez al modelo y funcionó. En cambio, los marcadores del episodio dicen `NO_GO_CONTROLLER`, `SCIENCE_STATUS=NOT_STARTED`, `MODEL_CALLS=0` y `STOP_CLASS=ModuleNotFoundError`. **El segundo job tampoco produjo una réplica científica.** La preparación sintética sí consumió recursos. El workflow verifica que hay un resumen legible y admite un score nulo. Eso explica que la conclusión operativa de GitHub pueda ser verde junto con un experimento que nunca empezó. [Job corregido](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909303221/job/136861487210).

Reproduje la causa con la fuente fijada y los nombres montados por el workflow. En `setup()` se importa `h0_adapter_numeric_telemetry_t052`, mientras el evaluador monta el adaptador probado como `h0_adapter_numeric_telemetry_t049.py`. Con la disposición publicada se obtiene `ModuleNotFoundError` para el primer nombre. En una copia local corregí la importación para apuntar al módulo montado, cargué las mismas fuentes con los módulos temporales en un directorio aislado y `setup()` terminó con ocho herramientas disponibles. Cero llamadas al modelo en esta comprobación. El arreglo queda verificado solo hasta la inicialización. Para aceptar una réplica, registrar por separado estado de infraestructura, arranque de ciencia, evaluación y calidad. Probar el arranque real con los mismos montajes antes de cargar pesos eliminaría este desperdicio. El prerregistro preveía una sola reparación acotada antes del modelo y ya se hizo una en el primer intento. Corresponde formalizar la decisión siguiente, sin encadenar reintentos por inercia. [Importación del controlador](https://github.com/mxlzz/autonomous-scientific-research/blob/08732a9da7ab9496b008189f2ab67083eec4108f/scripts/h0_sciresearch_qwen_t052.py#L99) · [Montajes del evaluador](https://github.com/mxlzz/autonomous-scientific-research/blob/08732a9da7ab9496b008189f2ab67083eec4108f/.github/workflows/h0-sciresearch-t052-qwen4b-n2-categories.yml#L214).

## Incorporación en main · D-0062

A partir de e484a92, la [guía de relevo](../benchmarks/H0-DECISION-BASELINE.md) identifica los cuatro jobs y los dos episodios efectivos de esta comparación. La [evidencia definitiva de T0.52](../evidence/T0.52-qwen4b-dev-n2-no-submit-tool-categories-2026-11-21.md) y el [job 136862265370](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909561018/job/136862265370) concuerdan en 9 turnos, 8 herramientas, 31.351 tokens de entrada y ninguna entrega. El fallo de arranque del job previo se corrigió en main. No corresponde programar otra réplica del caso. T0.54 permanece pendiente para la custodia y el nuevo trabajo de diseño T0.55 es offline.

Autoverificación del relevo. Los cuatro tests del [exportador por línea de comandos](../scripts/test_sciresearch_public_result.py) pasaron, incluidos subcasos de tipos, datos ausentes y nulos. Además se ejecutó el grader original de SciResearch 9d391b3 sobre un entorno sintético, una vez con entrega y otra sin ella. Se escribió cada resultado en JSON y se leyó a través del nuevo exportador. Resultado observado: SCORED con target_covered=true, checked_convergence=false y final_fit_converged=null; NO_SCORE con score=null. No se cargaron modelos ni se leyeron trazas privadas para estas pruebas. El siguiente protocolo deberá verificar el recorrido completo de su propio evaluador antes de usarlo en una comparación.
