# R04 — autoresearch: auditoría documental T0.1.3

**Fecha:** 2026-11-17 (America/Argentina/Buenos_Aires). **Autor/proyecto:** Andrej Karpathy, marzo de 2026. **Tipo:** lectura de documentación y código fuente sin instalar, ejecutar, descargar datasets ni llamar a APIs pagas.

## 1. Procedencia, versión y licencia

- **Fuente primaria:** [karpathy/autoresearch](https://github.com/karpathy/autoresearch), commit fijado `228791fb499afffb54b46200aca536f79142f117` de rama **`master`** ([árbol inmutable](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117)). Consulta: GitHub API `GET /repos/karpathy/autoresearch`; `GET /git/ref/heads/master`; directorio `GET /contents/`; `fetch_file` del README, `program.md`, `prepare.py`, `train.py`, `pyproject.toml` y `.python-version` con ref inmutable.
- **Versión del paquete:** `0.1.0` en [pyproject.toml](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/pyproject.toml). No se identificó un tag de release inmutable; **el commit** es la referencia reproducible de esta inspección.
- **Licencia:** el [README al commit](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md) termina con `## License / MIT`. La consulta de archivos raíz **no muestra un `LICENSE` separado** y los metadatos del repo devuelven `license: null`. Por tanto, existe **declaración explícita MIT del autor**, pero no se comprobó texto íntegro del permiso/copyright en archivo de licencia. En T0.2, si se considera redistribución/incorporación, verificar alcance, atribución y preferir consultar autor o historial antes de asignar una licencia jurídicamente completa.
- **Publicación formal:** no se identificó artículo científico original revisado por pares asociado a este repositorio; es una referencia de **código/documentación original**, no un estudio experimental publicado del rendimiento de agentes.

## 2. Arquitectura observada

- [README](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md) describe tres piezas: `prepare.py` fija datasets, tokenizador, evaluador y tiempo; `train.py` contiene el modelo GPT, optimizador y entrenamiento modificables; `program.md` instruye a **un agente de codificación externo**. **No es un framework de orquestación multiagente** ni incluye un runner de investigación autónoma completo dentro de sus diez archivos raíz.
- [`program.md`](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md) define ciclo: establecer baseline → modificar solo `train.py` → `uv run train.py > run.log 2>&1` → extraer `val_bpb` y VRAM → registrar todos los resultados en TSV → conservar commit si mejora / revertir si no. Instruye **no modificar `prepare.py` ni la función `evaluate_bpb`**; no es barrera de integridad técnica a nivel de control de permisos.
- **Tiempo/criterio:** [prepare.py](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/prepare.py) fija `TIME_BUDGET=300` segundos de entrenamiento (excluye carga/compilación); validador `evaluate_bpb` obtiene **bits por byte de validación, a minimizar**. Ejecución default limitada a una GPU NVIDIA/CUDA; README menciona test en H100 y soporte alternativo sólo mediante adaptaciones/forks. El conteo orientativo ≈12 runs/hora deriva de 300 s/training **sin overhead**, no fue medido en este proyecto.
- **Entorno documentado:** Python **>=3.10**, gestor `uv`, PyTorch **2.9.1** con índice `pytorch-cu128`, extensiones `kernels` y dependencias en `pyproject.toml`; descarga de shards y entreno de tokenizador para primeros runs. La compatibilidad de una GPU pequeña y el costo monetario siguen **sin medir**.
- **Persistencia propuesta:** rama `autoresearch/<tag>`, historial Git y archivo local `results.tsv` expresamente **sin commit**, con estados `keep`, `discard`, `crash`; el progreso no queda automáticamente respaldado fuera de esa carpeta. `run.log` sirve para depuración, pero no constituye por sí solo un archivo durable de resultados.
- **Indeterminación práctica:** el documento contiene `LOOP FOREVER` y `NEVER STOP`; el límite de recursos y paradas operativas deberá imponerse externamente en un ensayo controlado. No implica autorización a ejecutar bucles indefinidos con recursos ajenos.

## 3. Qué demuestra y qué no

**Hechos de código (observación estática):** existe contrato de evaluación fijo y flujo de cambios reversibles en un solo archivo. El repositorio contiene script de entrenamiento y evaluador. No se ejecutó ni se comprobó fidelidad del agente al prompt.

**Claims (nivel C):** README plantea que un agente autónomo puede iterar y mejorar el modelo durante la noche con ≈5 min/ensayo; esta afirmación operativa y cualquier mejora visual incluida en `progress.png` **no** fueron reproducidas. No hay estimación experimental propia de costo/validez.

**Inferencias (D):**
1. Es un **control arquitectónico simple** útil para estudiar continuidad, tasas de error, reintentos y costo de un agente de codificación único con evaluador determinista y fijo, siempre que se reproduzcan tareas equivalentes y el mismo presupuesto.
2. La mejora de `val_bpb` **no demuestra descubrimiento científico nuevo**, comprobación de hipótesis ni rigor de un informe. El evaluador fijo estrecha el objetivo a optimización de un modelo.
3. Riesgos de validez: repetir adaptaciones sobre la misma partición de validación puede sobreajustarla; instrucciones de no alterar `prepare.py` no son control de acceso; guardar sólo trayectoria de commits exitosos oculta negativas si falla `results.tsv`; 300 segundos entrenando no iguala costo GPU total incluyendo preprocesado/compilación/evaluación.
4. Criterio de medir únicamente una métrica es **ventaja para un control de ingeniería** y **limitación** para la pregunta central de validez científica.

## 4. Decisión provisional

**COMPARAR / CONSIDERAR BASELINE SIMPLE para H0–H1–H2, no adoptar aún como línea base validada.** Para comparar con R01/R02/R03, elegir una tarea compartida con evaluador idéntico y recursos igualados; no comparar resultados originales de `val_bpb` con calidad de papers. Un runner externo (modelo, herramienta y costo) tendría que fijarse; cambiarlo constituye factor experimental.

**Pendientes:** verificación del alcance de MIT, requisitos efectivos de CUDA y VRAM, dataset/splits/hashes, benchmarks apropiados fuera de entrenamiento nanochat, trazas completas de resultados negativos, cumplimiento efectivo de límites y costo por resultado científicamente válido. Sin gasto pagado, sin ejecución. **Tipo de evidencia:** código leído y claims del autor (C); hipótesis de utilidad experimental (D), **ningún resultado A**.
