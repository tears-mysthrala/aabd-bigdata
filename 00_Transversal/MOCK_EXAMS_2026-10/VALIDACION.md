# Validación de los simulacros revisados — 9 de octubre de 2026

[Índice](README.md). Evidencia local del paquete del PR #18, después de ajustar
preguntas y soluciones a la materia docente. No acredita una entrega ni examen
oficial, un servicio ejecutado o el resultado de CI remoto.

## Contraste docente y comprobación estructural

- Los 64 apartados de siete modelos se contrastaron con los pasajes identificados
  en la [matriz](COBERTURA.md). Incluye las 30 preguntas del test y los cuatro
  apartados prácticos de Programación. Hay 37 fuentes únicas del curso.
- El [manifiesto](manifest.json) conserva rutas y SHA-256 de esas fuentes.
  No se emplean simulacros ni soluciones propias como fuente del temario.
- Se conserva el formato docente 30 test / 3 puntos + práctica / 7 puntos.
  La guía no cuantifica la penalización: solo se registran aciertos/errores/blancos.
  Se revisaron las claves tras redistribuir opciones: A=8, B=8, C=7, D=7.
- Puntos y tiempos de los apartados comprobados; se mantienen las rúbricas
  propuestas. La revisión manual incluye PERT, métricas, costes, volumen, join,
  ventanas y lote Kafka. El comprobador no evalúa corrección conceptual.

Desde la raíz, con Python y sin dependencias adicionales:

```bash
python 00_Transversal/MOCK_EXAMS_2026-10/comprobar.py
```

El [comprobador](comprobar.py) solo lee archivos. Valida hashes, referencias por
apartado, enlaces locales, puntuaciones/tiempos, opciones/claves, sintaxis de los
seis bloques Python y conteos del CSV. Hay 201 enlaces locales comprobados.
Aborta si una fuente cambia: hay que
revisar los apartados afectados, no renovar el hash automáticamente.
Se comprobó también que rechaza una fuente alterada y un enlace roto mediante
copias temporales, sin modificar los originales.

## Ejecuciones realizadas

Los fragmentos de las soluciones de Programación, Iris y series se extrajeron
del Markdown y se ejecutaron en una carpeta temporal con los entornos aislados
ya disponibles de sus prácticas. No se instalaron paquetes ni se cambiaron
fuentes, datos de entrada o resultados anteriores. Para series se proporcionó
el CSV literal del enunciado como `csv_text`.

Python 3.13.13; NumPy 2.5.3, Pandas 3.0.6, scikit-learn 1.9.1,
Matplotlib 3.11.2 y Pydantic 2.14.0 en el entorno de Programación.

- **Programación:** 322 filas; dos duplicados; 12 inválidas; 308 válidas,
  32 positivas. Train C01–C03: 231 filas/24 positivas; test C04: 77/8.
  Comprobados grupos disjuntos, media del scaler aprendida solo en train,
  descartes/predicciones exportados, métricas y validadores de límites/NaN/inf.
- **Iris:** 105 train/45 test; dos pipelines; búsqueda de k solo en train;
  matrices suman 45. El gráfico 2D se genera con modelos nuevos sobre dos
  features y se revisó visualmente: paneles, clases y ejes con unidades.
- **Series:** intervalo inclusivo de tres filas, media 54 °C; medias de ventanas
  50.5/44; energía 7/1 kWh; interpolación 50 °C; primera rolling 146/3 °C;
  alerta en 08:03. Gráfico original/suavizada generado y revisado visualmente.

| Caso | Resultado de esta ejecución |
|---|---|
| Programación | accuracy 0.9610; recall 1.0000; precision 0.7273; F1 0.8421 |
| Programación matriz | [[66,3],[0,8]], filas reales y columnas predichas |
| Programación siempre 0 | accuracy 0.8961; recall/F1 0 |
| Iris LogReg 4D | accuracy 0.9111; matriz [[15,0,0],[0,14,1],[0,3,12]] |
| Iris KNN 4D | accuracy 0.9333; matriz [[15,0,0],[0,15,0],[0,3,12]] |

SHA-256 del CSV de entrada, conservado sin cambios:
`5d5ef215eb21486ad569b870518f6519ff05f415ffb58531db9942bbf9fa514b`.

Ruff aplicado al comprobador y al formato/imports de los fragmentos; sintaxis y
ejecuciones comprobadas. `git diff --check` sin errores. La preparación para el
estudiante sigue los entornos virtuales de los apuntes; no se evalúan preferencias
de herramientas del repositorio.

Gitleaks sobre los 22 archivos del paquete del PR, con salida redactada:
sin hallazgos. Esta comprobación no equivale a un escaneo del historial completo.

## Límites

Las métricas son de casos sintéticos y no se exigen como cifras universales.
Ocho positivos no validan una planta. El contraste con materia disponible no
certifica qué se ha impartido ya ni que el modelo cubra todos los ejercicios.
Arquitecturas, ILM, caídas de broker, Connect y flujos NiFi son respuestas de
diseño; no se aplicaron a servicios. La ejecución del código de referencia no
constituye entrega de un alumno ni subida a Moodle. El estado de publicación,
revisión y checks remotos debe consultarse en el PR.
