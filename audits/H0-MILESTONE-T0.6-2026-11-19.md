# A-H0-T0.6 — Auditoría del hito H0 y decisión formal

**Fecha:** 2026-11-19, Buenos Aires. **Responsable:** mismo ejecutor que realizó T0.4/T0.5. **Tipo: AUTOVERIFICACIÓN, NO AUDITORÍA INDEPENDIENTE.** **Veredicto:** `CORREGIR H0`; hito **NO APROBADO / NO CERRADO**, no pasar a H1/H2. Ningún ensayo adicional se ejecutó durante esta auditoría. [Registro de brechas verificables](../evidence/T0.6-H0-gap-register-2026-11-19.md).

## 1. Contrato y alcance

Se recuperó de GitHub (no de memoria de conversación) `HEAD=81cc173b186590789de0808a1d83c4ac0b517817`, `STATE.json` H0/`current_task=T0.6`. Se leyeron `README.md`, `OBJECTIVE.md`, `PLAN.md`, `METHODOLOGY.md`, `AGENTS.md`, `RESEARCH.md`, `LOG.md`, el [protocolo de piloto](../benchmarks/H0-PILOT-v0.1-2026-11-17.md), auditores T0.3/T0.4/T0.5 y [evidencia C1/P01](../evidence/T0.5-C1-DS1000-scoring-2026-11-19.md). No hubo incoherencia de estado ni cambios concurrentes observados al comienzo.

**H0, PLAN.md:** “al menos una línea base científicamente evaluable, reproducible y documentada”; o, si ninguna puede ejecutarse, registrar impedimentos y proponer un sustituto antes de H1. **Objetivo aprobado** exige investigar con autonomía verificable, no sólo generar código; costos por resultado válido y auditoría de proceso. El estado de cada tarea T0.1–T0.5 como documental/técnico restringido no implica cumplimiento del hito completo.

## 2. Matriz de aceptación del hito

| Criterio | Verificación y distinción | Dictamen |
|---|---|---|
| Antecedentes suficientes | 14 fuentes R01–R14, versiones/licencias heterogéneas, alternativas evaluadas [T0.1/T0.2](../evidence/T0.2-candidate-selection-2026-11-17.md); hay autoverificación, no independencia | **PASS documental condicionado** |
| Selección operacional y control de alcance | C1 ReAct verificado; C2 SmolAgents con Docker timeout; C3 EvoScientist sin adaptador; evitar inventar arquitectura multiagente fue correcto | **PARTIAL**, no comparadores ejecutables |
| Diseño de tarea y evaluador | 7 slots planeados; 3 IDs DS1000 confirmados, 4 sin ID; 2 con juez remoto pago; scorer externo DS1000 fijado en commit | **PARTIAL**, no piloto de 7 casos |
| Ejecución de caso real | [run 44459486187](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44459486187), **dos intentos del mismo workflow** original C1+Qwen3 0.6B, DS1000 validación Asta ID513; `ds1000_scorer=I/I` sin fallos de muestra | **PASS técnico limitado**; resultado negativo |
| Reproducibilidad científica | Dos scores iguales con hashes diferentes, pero un solo sample (pseudorreplicación para generalizar), sin seed fijada ni datos de trayectoria persistidos; no se reproduce puntuación publicada de referencia | **FAIL** para reproducibilidad científica auditable |
| Contrato de scorer congelado | Scorer código original intacto; scorer separado AstaBench0.5.5/Inspect0.3.225 **falló**; scoring integrado AstaBench0.5.5/Inspect0.3.258 sí funciona, desvío anotado | **FAIL** de equivalencia predefinida; **PASS parcial** de calibración inline |
| Validez como investigación autónoma | DS1000 es problema de **completar código**, sin planteamiento/verificación iterativa de hipótesis científicas, ni auditoría científica distinta; no mide autonomía prolongada | **FAIL** del objetivo central de H0 |
| Datos y confidencialidad | Repo público, sin prompt/gold en archivos o logs de CI según workflows inspeccionados; **no hay JSON completo** conservado para auditoría. DS1000 original `xlangai/DS-1000` CC BY-SA 4.0, AstaBench gated tiene términos propios por dataset; evitar generalización legal | **PASS de precaución de exposición**, **FAIL de conservación y revisión** |
| Economía y equidad | Cero gasto pago de APIs; GitHub API al corte contabilizó **29 workflow runs (17 success, 12 failure)** como ingeniería, no aciertos; CPU, tokens, energía, costo de preparación y esfuerzo humanos sin cuantificar; 0 respuestas válidas en C1/P01 | **FAIL** para costo por resultado válido / comparación causal |
| Independencia y leakage | Mismo agente se autoaudita; validación ID513 repetido para depurar, no usar como test de generalización; dataset original DS1000 tiene `split="test"`, del cual AstaBench deriva **su** validación/test, especificar siempre split AstaBench | **FAIL** de independencia; **test reservado AstaBench no puntuado** |

## 3. Hallazgos de mayor importancia

**F01 — Desalineación constructo-métrica (CRÍTICO):** una tarea de generación de código DS1000 verifica el arnés de evaluación, pero no representa el proceso de investigación aprobado. Repetir ID513 o aumentar la cantidad de preguntas no subsana automáticamente esta brecha. **No atribuir resultado `I` a incapacidad general de agentes o modelos pequeños.**

**F02 — Rigor de la medición (ALTO):** `ds1000_scorer` genuino y sin modificar funcionó con Inspect0.3.258, no con el runtime separado Inspect0.3.225 del diseño T0.3. No declarar éxito del método congelado ni usar comparaciones entre entornos como si fueran el mismo tratamiento. La causa precisa del `LookupError` no está demostrada; `sandbox()` es una posible limitación adicional de scoring poshoc, no prueba de causa.

**F03 — Trazabilidad legal (ALTO):** sólo hashes de archivos efímeros y scores sanitizados. La pérdida del contenido de ejecución impide auditoría de método, defectos, posibles alucinaciones o contaminación. Las trazas completas pueden contener prompts, referencias de dataset y output de agente, por lo que no corresponde publicarlas sin analizar licencia y seguridad **por fuente**. [GitHub Docs sobre artefactos](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts): descargables para quien tiene lectura del repo; repo público no da privacidad automática. [Licencia DS1000](https://github.com/xlang-ai/DS-1000/blob/main/LICENSE) CC BY-SA4, [AstaBench HF](https://huggingface.co/datasets/allenai/asta-bench) gated: diferenciar.

**F04 — Muestra/splits (ALTO):** P01 es 1/7 del piloto, 2 corridas sobre mismo problema no son 2 tareas; P04–P07 ni siquiera IDs fijados. `inspect_evals.ds1000_dataset` carga `xlangai/DS-1000` **split test de origen** y luego AstaBench deriva una partición propia de 100 validación/900 test. El agente fue evaluado sólo en AstaBench validation513; se desconoce exposición del modelo base durante su preentrenamiento. No se ha estimado contaminación.

**F05 — Comparación/recursos (ALTO):** C1/C2/C3 no comparten contratos ejecutados; C2 tiene timeout técnico, C3 no está adaptado. `generate` recibió también `I` en 513, pero su comparación con C1 no empareja formalmente presupuesto, herramientas, solver ni repeticiones. Costo de API 0 es distinto de costo total 0: no estimar ahorro cuando el denominador (resultado válido) es cero.

**F06 — Eficiencia investigadora (MEDIO):** 29 workflow runs y 15 workflows únicos en la API al corte reflejan costo de integración del arnés; 17 éxitos de CI no son 17 aciertos científicos. Reducir ciclos de debugging no dirigido. No crear un framework nuevo ni sustituir arbitrariamente el scorer para fabricar resultados positivos.

## 4. Dictamen y decisión autorizada

**DECISIÓN `D-0013: CORREGIR / CONTINUAR H0`**, no retroceder a T0.1 ni saltar H1. El progreso documental y el pipeline de C1/scorer son reutilizables (descartarlos sería desperdicio), pero **el hito H0 no cumple su condición de salida**: no tiene una línea base representativa del acto de investigar científicamente y auditable en profundidad. No se requieren cambios a `OBJECTIVE.md`.

**Correcciones priorizadas — SIN ejecutar todavía:**

1. **T0.7 (unidad siguiente):** estudiar procedencia/licencias y **mecanismo de retención segura y auditable** de inputs, outputs, hashes, logs y muestras por tipo de dataset. Contrastar opciones existentes (GitHub artifacts públicos, repo privado bajo permisos, almacenamiento local del usuario, paquete reconstruible para auditor autorizado), condiciones reales y costo. Elegir la menos compleja que cumpla derechos, datos sensibles y reproducibilidad. No copiar secretos, datasets ni trazas restringidas como “prueba”. Si toda opción requiere cuenta/infra/permiso nuevo, documentar el bloqueo e intervención exacta.
2. **T0.8 (sólo después de T0.7):** reconsiderar la selección de **tarea realmente científica** de extremo a extremo con evaluación independiente realizable a costo autorizado 0, comparando primero opciones existentes (CORE, ScienceAgentBench, ResearchGym si licencia aclarada, benchmark con evaluador determinista). Seleccionar instancia, criterios, dificultad, splits, validez y recurso con evidencia; no fabricar nuevos evaluadores ni hacer score con juez sustituto bajo el mismo nombre. Si no existe viable, documentar impedimento y alternativa/hito limitado.
3. **T0.9 (condicionada):** calibrar un caso representativo y traza auditable, fijar entorno/scorer/evidencia y recursos por intento; **solo entonces** diseñar comparación emparejada de arquitectura/modelo y completar auditoría H0 con revisor independiente cuando haya pretensión fuerte.
4. **Gate**: sin solución de datos, modelo/cuotas pagas, contrato de scorer y tarea científica, **H1/H2 permanecen cerradas**, aunque T0.4 y T0.5 estén aceptadas en su alcance de ingeniería.

**Criterio de cierre corregido de H0:** al menos una **tarea científica pertinente** con objetivo/hypótesis, datos, ejecución y evaluación externa reproducible, trazas legalmente auditables o paquete de reproducción aceptable para auditor autorizado, modelo/infra/scorer/versiones fijados, negativos y defectos preservados, costo total estimable; decisión de adoptar/adaptar/combinar con benchmark y una alternativa justificable. No exigir que el resultado sea *correcto* para declarar herramienta reproducible: una falla puede ser válida si se puede auditar, pero no calificar éxito de investigación autónoma con un code-completion.

## 5. Auditoría de la auditoría

- [x] Estado y SHAs recuperados, fuentes primarias y jobs contrastados. 
- [x] Contabiliza resultados negativos, datos/splits, confusores, evaluación y costos, sin inferir score inexistente.
- [x] Decide explícitamente `CORREGIR H0`, sin gasto, pruebas nuevas ni cambio de objetivo.
- [x] Define siguiente tarea única verificable T0.7 y bloqueos.
- [ ] Auditor independiente: **no**; pendiente antes de reclamaciones científicas confirmatorias.
- [ ] Acceso legal a cada dataset/registro: requerirá análisis por tarea, no sustituido por este dictamen.

**Conclusión:** aceptar **T0.6 como auditoría documental/autoverificación realizada**, pero **RECHAZAR el cierre del hito H0**. Permanecer en H0 para correcciones controladas.
