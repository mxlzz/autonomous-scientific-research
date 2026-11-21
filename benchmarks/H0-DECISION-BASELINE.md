# H0 · Decisión sobre la línea base e instrucciones de continuidad

**Vigente desde D-0062, después de T0.53.** La réplica prevista en el dictamen ya se ejecutó. El próximo agente empieza por `STATE.json`. Si el estado avanzó, usa el estado más reciente y cita este documento como criterio del método. [Objetivo](../OBJECTIVE.md) · [Dictamen histórico](../audits/DICTAMEN-DIRECCION-CIENTIFICA-2026-11-21.md) · [Comparación observada](../evidence/T0.53-n1-n2-final-submit-trace-custody-options-2026-11-21.md).

## Qué entra en el análisis

Una fila por ejecución de Actions e intento, identificando además el episodio si un job ejecuta varios. La columna de inicio se refiere al episodio científico. Separar llamadas de preparación, errores de infraestructura y resultados científicos. En este caso todos los jobs fueron el intento 1 de su respectivo run.

| Ejecución original | Infraestructura | Inicio de ciencia | Resultado del evaluador | Entrada efectiva | Uso |
|---|---|---|---|---:|---|
| [T0.49 · 44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967) | Finalizó | Sí, 8 turnos | Entrega puntuada, error objetivo 14.861,23 σ, cobertura de parámetros 0 | 28.248 | Primer episodio |
| [T0.52 · 44909209749](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909209749) | Falló fixture previo al modelo | No | Sin observación | — | Costo de preparación |
| [T0.52 · 44909303221](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909303221) | Job verde, controlador falló al importar | No. Un llamado sintético de preparación | Sin observación | — | Costo de preparación |
| [T0.52 · 44909561018](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44909561018) | Finalizó tras reparar la importación | Sí, 9 turnos | Sin entrega, `NO_SCORE`, vector nulo | 31.351 | Segundo episodio |

Dos episodios científicos del mismo caso de desarrollo, una entrega puntuada. Publicar esa fracción únicamente como descripción de estos intentos. La regla de entrada era un umbral blando de 24.000 con una oportunidad final de entrega. El motivo por el cual el modelo no entregó en el segundo episodio sigue sin observarse. El hash de un resumen sirve para comprobar una copia recuperable. Por sí solo no permite reconstruir la trayectoria. Se conserva la configuración Qwen4B/CPU como referencia negativa. La auditoría desaconseja gastar otro episodio para obtener un mejor resultado en este caso.

## T0.55 · Preparar una comparación que pueda decidirse

Una sola unidad offline. Usar las fuentes y los controles ya disponibles. Se admiten código local y fixtures sintéticos. No hace falta acceder a datos privados, iniciar un LLM, descargar pesos ni cambiar permisos para completar esta unidad.

1. **Escribir la pregunta y el contraste.** En `experiments/T0.55-protocolo-comparacion.md` especificar la hipótesis de descomposición explícita frente a trabajo libre con un solo agente. Mantener constantes modelo, herramientas, información disponible, presupuesto, entorno, evaluador y regla de entrega. Archivar la diferencia exacta entre las instrucciones de ambos tratamientos. Las políticas `naive` y `heuristic` son referencias externas. Su acceso directo al simulador y su número de acciones impiden atribuir causalmente a la arquitectura la diferencia frente a Qwen.
2. **Elegir la muestra antes de ver resultados.** Usar identificadores públicos de desarrollo o una regla de selección determinista basada en metadatos públicos. Excluir el caso de calibración y declarar los casos ya vistos en T0.26. Fijar casos, repeticiones, orden emparejado o contrabalanceado y límite *total* de recursos antes de considerar una corrida. Reservar los casos confirmatorios. Ofrecer una justificación concreta si el volumen factible solo permite explorar.
3. **Definir qué sería válido.** Fijar por anticipado la métrica primaria, sus unidades, el umbral o margen científicamente justificado y los defectos que invalidan la inferencia. Considerar error de predicción en σ, calidad de los intervalos y evidencia de comprobación del método cuando sea pertinente al caso. La puntuación de intervalos premia precisión y cobertura a la vez. Requerir una medición nueva en todos los casos penalizaría controles que resolvieron bien con los datos iniciales. Si faltan trazas para evaluar un criterio, declararlo no evaluable o escoger un caso auditable. Aplicar las fórmulas de [METHODOLOGY](../METHODOLOGY.md#5-métricas). Un presupuesto en tokens, tiempo de CPU y revisión sin precio acordado se reporta por unidad, sin fingir un costo monetario total.
4. **Probar el instrumento con datos sintéticos.** Reutilizar la proyección pública indicada abajo. Probar el recorrido desde un resultado de ejemplo, su clasificación y costo, hasta la fila usada para decidir. Incluir entrega válida, entrega puntuada pero inválida, ausencia de entrega, fallo anterior a ciencia y costo desconocido. Comprobar a mano el denominador y el caso de cero válidos. Los campos faltantes siguen ausentes para los experimentos históricos.
5. **Emitir una sola decisión y registrarla** en `audits/T0.55-DECISION-H0.md`, con los criterios cumplidos y pendientes. Si hay una comparación informativa, reproducible y factible, dejar el protocolo preparado para la auditoría de salida de H0. Si necesita custodia privada, registrar exactamente qué afirmación la necesita y retomar T0.54 con el usuario antes de ejecutar. Si ambos tratamientos quedarían indistinguibles, el control comparable es inviable o no hay observables suficientes, cerrar esta vía de Qwen4B/CPU. Evaluar un sustituto ya existente y auditable dentro del alcance aprobado o pausar el proyecto si no existe una opción factible. El cierre de T0.55 no abre por sí mismo H1/H2. Para una decisión positiva sobre el hito hay que satisfacer los criterios originales del plan. Mantener la ausencia de revisión independiente explícita.

**Custodia pendiente.** T0.54 queda diferida y abierta. Las condiciones de D-0061 siguen aplicando a las trazas privadas y a nuevas corridas con LLM. Documentar el destino y la autorización concreta si llegan. No asumir que el usuario eligió almacenar trazas cifradas, habilitó una cuenta privada o aceptó rebajar el alcance de la auditoría. Un análisis de métricas públicas puede sustentar afirmaciones limitadas. No reemplaza la inspección histórica de hipótesis y decisiones.

## Cómo registrar resultados futuros de SciResearch

En el evaluador, después de que el harness cierre el episodio y antes de la limpieza, ejecutar con la ruta exacta del `result.json` original de ese episodio:

```bash
python scripts/sciresearch_public_result.py "$episode_result"
```

Consumir la salida JSON del comando como registro público de ciencia. Emitirlo una vez en un canal que acepte su esquema completo y comprobar su lectura al final. La proyección se alimenta de la salida del evaluador original. El monitor histórico `T052_` solo sirve para reconstruir el protocolo ya cerrado. La nueva ruta evita su conversión de todos los campos `SCORE_*` a flotantes. Conservar `target_covered`, `checked_convergence` y `final_fit_converged` como booleanos, incluido el nulo cuando corresponde. El exportador permite exclusivamente campos conocidos y descarta textos o etiquetas del caso. Un `NO_SCORE` real emite JSON con `score: null`. Un archivo ausente, mal formado o contradictorio da salida 2: registrar por separado el motivo de infraestructura conocido, una censura documentada o «desconocido». Nunca asignarle un score cero. Si el evaluador no arrancó, conservar sus marcadores de arranque y preparación. `SCORED` describe que se obtuvo un vector. El criterio prerregistrado determina la validez.

Para futuras ejecuciones, probar antes de descargar pesos el arranque real con la misma imagen, rutas y módulos montados que usará el evaluador, un caso sintético y un backend de prueba sin inferencia. Verificar la carga del controlador, las herramientas anunciadas, el recorrido de una entrega simulada hasta el registro y el fallo visible si falta una dependencia. Los resultados sintéticos solo validan el instrumento. Usar un identificador de protocolo nuevo para una intervención que cambie el acceso, el modelo, el límite efectivo o la política de entrega. Conservar las corridas históricas con sus commits originales.

Prueba reproducible de la proyección:

```bash
python -m unittest discover -s scripts -p 'test_sciresearch_public_result.py' -v
```

## Actualización operativa posterior D-0065 (2026-11-21)

Esta sección **prevalece** sobre las referencias históricas de D-0062 a una decisión A/B/C aún no tomada. El usuario eligió A, aportó su recipient público age, y la unidad T0.54 ejecutó **solo un ensayo sintético** de cifrado y publicación cifrada en [Actions44916003316](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44916003316). Referencias: [evidencia](../evidence/T0.54-age-synthetic-custody-2026-11-21.md) · [autoverificación](../audits/T0.54-AGE-CUSTODY-GATE-2026-11-21.md). La identidad privada permanece en el equipo del usuario, sin custodia del agente. El archivo sintético se cifró con su recipient pero **no** se descifró con su identidad; el roundtrip completo fue con una identidad de prueba distinta. No solicitar su private key.

T0.55 también cerró como [diseño exploratorio offline](../experiments/T0.55-protocolo-comparacion.md), no como una prueba de dos tratamientos. **Siguiente T0.56:** integración sin inferencia de la custodia `age` con el harness/runner original, rights/retention y fail-closed, evitando que datos en claro salgan del evaluador. Los resultados originales T0.49/T0.52 siguen sin traza recuperable. H0 CORREGIR, ningún nuevo LLM ni H1/H2 autorizado por este gate.
