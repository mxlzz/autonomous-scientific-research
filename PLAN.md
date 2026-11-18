# Plan y criterios de aceptación — versión 1

Objetivo canónico: [OBJECTIVE.md](OBJECTIVE.md). Hipótesis H1–H6 definidas allí. Orden dependiente de resultados; la construcción de software nuevo no es un hito obligatorio.

## H0 — Reproducir y auditar lo existente (activo)
**Resultado:** al menos una línea base científicamente evaluable, reproducible y documentada; matriz de opciones adoptar/adaptar/combinar/desarrollar. Si ninguna puede ejecutarse, registrar impedimentos y proponer un sustituto antes de H1.

- **T0.1 (COMPLETADA DOCUMENTALMENTE; H0 sigue abierto):** Inventario crítico de antecedentes y licencias. **Aceptación:** mínimo 12 fuentes pertinentes con ficha de fuente primaria, versión/commit o desconocido explícito, licencia confirmada o pendiente, claims separados de evidencia, comparación y decisión provisional. Auditoría de cobertura, enlaces y duplicaciones.
  - **T0.1.1 (COMPLETADA DOCUMENTALMENTE; sin reproducción)**: auditar EvoScientist (R01) documentalmente: repositorio y paper, funcionalidades demostradas vs anunciadas, arquitectura real, licencia, requisitos, fecha, revisión del commit concreto, límites y potencial de reutilización. Conservar resultados en RESEARCH.md y evidencia en evidence/. **Aceptación:** ficha completa o campos faltantes explícitos con motivos, enlaces directos, SHA/versión, fuentes primarias y registro del protocolo empleado; sin instalación ni gastos.
  - **T0.1.2 (COMPLETADA DOCUMENTALMENTE; sin reproducción):** revisar R02 DeepScientist con el mismo criterio; contrastar con R01. [Ficha](evidence/R02-DeepScientist-2026-11-17.md) · [Autoverificación](audits/T0.1.2-R02-2026-11-17.md).
  - **T0.1.3 (COMPLETADA DOCUMENTALMENTE, sin reproducir):** R04 autoresearch como posible control simple y R03 AI Scientist v2 como comparador complejo; licencias, commits y limitaciones registrados. [R04](evidence/R04-autoresearch-2026-11-17.md) · [R03](evidence/R03-AI-Scientist-v2-2026-11-17.md) · [Comparación](evidence/T0.1.3-contrast-2026-11-17.md) · [Autoverificación](audits/T0.1.3-R03-R04-2026-11-17.md).
  - **T0.1.4 (COMPLETADA DOCUMENTALMENTE):** R06–R08 y R09–R14 inspeccionados; matriz de **14 fuentes R01–R14**, separaciones de licencia/código/datos, vacíos y duplicados. [Matriz auditada](evidence/T0.1.4-benchmark-matrix-2026-11-17.md) · [Auditoría de cobertura (autoverificación)](audits/T0.1-COVERAGE-2026-11-17.md). R15–R16 fuera del umbral.
- **T0.2 (PRÓXIMA UNIDAD):** Elegir 2–4 sistemas candidatos. **Aceptación:** criterios de selección y exclusión por reproducibilidad, cobertura, costo, requisitos y mantenimiento; evitar benchmark sesgado.
- T0.3 Diseñar piloto de aproximadamente 6–8 tareas (no potencia estadística confirmatoria). **Aceptación:** evaluadores externos, entradas/salidas, dificultad, fugas posibles, recursos, partición desarrollo/prueba reservada.
- T0.4 Probar viabilidad de ejecución sin exceder recursos autorizados. **Aceptación:** versiones fijadas, entorno descrito, presupuesto de CPU/GPU y API, límites y riesgos.
- T0.5 Reproducir un resultado de referencia sin alterar evaluador. **Aceptación:** datos, comando, logs, outputs, hash, réplica y resultado comparado.
- T0.6 Auditar H0. **Aceptación:** evidencia suficiente para continuar o decisión explícita de corregir/retroceder con historial.

## H1 — Granularidad y arquitectura
Comparar agente único, agente estructurado y variantes multiagente; separar número de agentes de profundidad de tareas. **Aceptación:** diseño controlado, al menos una comparación emparejada con repeticiones, incertidumbre y costos; **auditoría:** detectar presupuestos desiguales, filtración y confusores.

## H2 — Modelos pequeños y enrutamiento
Probar modelos locales, remotos y asignación dinámica. **Aceptación:** curva costo-calidad por familia de tarea, tasas de escalamiento y error, energía/hardware cuando corresponda; **auditoría:** confirmar costos integrales y que no cambie el evaluador.

## H3 — Persistencia y autonomía prolongada
Ejecutar sesiones sucesivas, fallos inducidos controlados y recuperación de estados. **Aceptación:** métricas de desviación, duplicación, pérdida de evidencia e intervenciones, con logs completos; **auditoría:** contrastar GitHub frente a los resultados en disco/entorno.

## H4 — Validación integrada y decisión final
Adoptar/componer únicamente componentes que hayan demostrado beneficio y evaluar con tareas reservadas. **Aceptación:** conclusiones reproducibles, intervalos/incertidumbre, límites, costos y decisión de ingeniería respaldada; **auditoría:** de preferencia por revisor distinto del ejecutor.

## Dependencias y prioridades
H0 -> H1 y H2 (pueden alternarse según recursos) -> H3 -> H4. Se puede modificar el orden con justificación y trazabilidad, nunca alterar el objetivo sin aprobación. Para cada hito se documenta su auditoría en audits/; no llamar independiente a la autoevaluación.

## Regla de avance
Un «Continuá» implica **una unidad de trabajo verificable**, no completar arbitrariamente todo H0 ni diseñar antes de medir. Un cierre inconcluso debe indicar bloqueo, evidencia y siguiente acción. El estado vigente está solo en [STATE.json](STATE.json).