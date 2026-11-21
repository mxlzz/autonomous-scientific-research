# A-H0-T0.50 — Auditoría formal tras primer episodio SciResearch puntuado

**2026-11-21 AR.** Auditor = mismo agente que ejecutó/reconcilió T0.49; **AUTOVERIFICACIÓN, NO INDEPENDIENTE**. Fuente canónica del objetivo [OBJECTIVE.md](../OBJECTIVE.md), criterio [PLAN.md](../PLAN.md) y [auditoría anterior T0.6](H0-MILESTONE-T0.6-2026-11-19.md). [Evidencia documental T0.50](../evidence/T0.50-h0-milestone-first-scored-quality-budget-assessment-2026-11-21.md), [T0.49](../evidence/T0.49-first-scored-sciresearch-qwen4b-poor-quality-2026-11-21.md), [run 44907008967](https://github.com/mxlzz/autonomous-scientific-research/actions/runs/44907008967).

## Controles de origen

- [x] HEAD inicial 726898a5a1e9c00887a6d662c528ea12531e01ec, STATE T0.50. T0.49 SCI-RESEARCH dev original, Qwen3-4B-Instruct2507 Q4 exact SHA, Ollama0.40.16, actor CPU2/8GiB, eval CPU1/1GiB, scorer original pinned grader.py Git blob 8194044d11b17b6d9d2b040a5115ff35bb798b64, harness 194a4b36caf4cd702caee34044ec457247644aee; seed 0 del entorno, no seed de generación.
- [x] Sourced `grader.grade`: `interval_score` menor mejor y cobertura de intervalos booleana por parámetro, `experiments_used` nuevas mediciones, `compute_fraction` solo cómputo de entorno. Un score vector no equivale a éxito universal.
- [x] Un único primer score legítimo: 8 model turns/tools, 2 tool_errors, scorer SUBMITTED, summary hash 3c623791be6a76adcd2f6f63325a7d4214318a1d674fb9f46e12c3d1a10ca43e; calidad deficiente: cobertura 0, target error 14861 sigma, target interval score 593803 menor mejor, experimentos nuevos 0 y atribución 0.
- [x] `T0.38` y `harness` explican límite **blando**: check tokens/turnos al comienzo del loop, al llegar umbral se concede vuelta final solo submit. Antes de la vuelta final (turno7), entrada total era **7064+17920=24984**, ya sobre 24000 por 984 debido a la solicitud que acababa de concluir; última vuelta añadió 3264 (fresh3260+cached4) y quedó **28248 vs 24000**, exceso4248 tokens17.7%. No afirmar que se controló estrictamente el gasto input ni declarar comparable con un hard-cap.
- [x] No hay evidencia publicada de secuencia detallada de acciones/hipótesis, ni de por qué fallaron dos tools. `experiments_used=0` solo dice que no hubo medición experimental nueva; no infiere 0 simulaciones/fits/state updates. No existe duplicado científico: los dos archivos suplementarios T0.49 provienen del MISMO run y quedaron etiquetados como duplicados en LOG.
- [x] Duración requests sum441.350s, controller442.373s, último request178.750s próximo límite180, cgroup actor sin max/oom/oom_kill ni swap, 8GiB; zero API facturada/GPU no implica electricidad/CPU cero. Cambio timeout90→180 no demostrado causalmente útil para primer request T0.49 (84.234s < 90s).
- [ ] Repetibilidad/variación estadística: **NO**; una sola muestra dev, generación sin seed fija y evaluación no replicada.
- [ ] Revisión de traza completa por auditor independiente o sin exponer oro privado: **NO**.
- [ ] Baseline comparativo equipresupuestario y costos por resultado válido: **NO**.
- [ ] Evidencia de investigación rigurosa científicamente correcta: **NO** en la muestra observada.

## Criterio de H0 y veredicto

**PASS parcial**: primera línea de base con scorer de investigación original accesible, fin de episodio y resultados numéricos, source/hardware/timeout pinned y metadatos seguros; mejora concreta frente a T0.6, que solo había registrado un caso DS1000 de programación.

**FAIL para cierre**: no resultado científicamente reproducido, calidad muy baja y presupuesto no estrictamente emparejable, trazas privadas no auditables, ningún control equivalente ni costo total. El objetivo aprobado NO exige buen score absoluto como gate inventado, pero sí condiciones verificables de rigor y costo para comparar. **Veredicto formal D-0058: CORREGIR H0, NO CERRAR, NO ABRIR H1/H2.** Mantener scorer y protocolo original; no implementar arquitectura multiagente.

**Siguiente T0.51 SOLO OFFLINE:** decidir presupuesto efectivo equivalente (soft 24k+vuelta final o stop estricto nuevo), diseñar métricas de herramienta por clase pública/estado sin argumentos/oro, y validadores con fixtures para permitir una única réplica SciResearch Qwen4B dev n2 tras nuevo prereg, bajo mismo modelo/scorer/CPU y costos acotados. No tocar privados ni correr modelos en T0.50/T0.51. Si no se pueden preservar privacidad y comparabilidad, NO-GO e informar intervención requerida; no asumir que aumentar timeout o modelo arregla calidad.

**Independencia:** no hubo auditor separado, se declara explícitamente autoverificación. Los documentos creados son nueva evidencia documental sobre el mismo run, no replicaciones científicas.
