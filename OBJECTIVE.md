# Objetivo aprobado — edición 1

**Aprobado por el usuario:** 2026-11-17. Cambios sustantivos requieren su autorización explícita.

## Pregunta principal
¿Bajo qué condiciones una IA puede realizar investigaciones científicas computacionales verificables durante períodos prolongados, descomponiendo y asignando trabajo entre modelos de distinta capacidad, sin perder rigor y con un costo inferior a alternativas comparables?

## Objetivo
Determinar experimentalmente qué combinación de arquitectura de agentes, granularidad de tareas, capacidad de los modelos, mecanismos de verificación y persistencia permite investigar con autonomía progresiva, continuidad del objetivo original, trazabilidad y costos controlados.

## Alcance
- Investigación de antecedentes; identificación de vacíos; hipótesis; diseño, programación y ejecución de experimentos; análisis y corrección iterativa.
- Evaluación de agente único, agente con herramientas, agente con enrutamiento y sistemas multiagente.
- Evaluación de modelos pequeños y locales, verificación, continuidad, recuperación y control de costos.
- Casos científicos computacionales con datos, código y criterios externos de evaluación disponibles.

## Exclusiones iniciales
- Desarrollo de un framework propio sin evidencia de necesidad.
- Experimentos físicos o con datos inaccesibles; afirmaciones de autonomía universal.
- Sistemas que producen solamente textos persuasivos sin evidencia reproducible.
- Gasto en APIs, infraestructura paga o uso de recursos ajenos sin autorización previa.

## Preguntas / hipótesis falsables
- H1: la profundidad de descomposición presenta beneficios dependientes de la tarea; más profundidad no es siempre mejor.
- H2: la coordinación multiagente supera al agente único solamente en ciertas condiciones.
- H3: asignar dinámicamente tareas a modelos más livianos reduce costo por resultado válido sin pérdida científica superior al margen predefinido.
- H4: estado externo verificado mejora continuidad y recuperación.
- H5: controles deterministas y auditoría separada mejoran la detección de resultados inválidos.
- H6: aprovechar registros de trabajos previos mejora la investigación iterativa frente al reinicio sin memoria.

Todas pueden resultar falsas o no concluyentes. No se transforma una hipótesis en requisito de implementación.

## Criterio de éxito final
Un informe y artefactos reproducibles que:
1. Comparen al menos una línea base robusta con variantes justificadas y recursos comparables.
2. Contengan estimaciones de validez científica, costo total por resultado válido, autonomía y recuperación, con incertidumbre.
3. Identifiquen condiciones de mejora y de empeoramiento, incluyendo resultados negativos.
4. Permitan reconstruir decisiones, código, ambientes, datos, resultados y auditorías.
5. Justifiquen **adoptar, adaptar, combinar o desarrollar**, sin presuponer ninguna de las opciones.

No implica demostrar AGI, descubrimiento original general ni éxito sobre todos los campos. [Métricas y reglas](METHODOLOGY.md) | [plan](PLAN.md).