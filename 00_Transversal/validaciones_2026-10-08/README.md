# Ejercicios y validación — Moodle 8 de octubre de 2026

Trabajo local en `feat/ejercicios-moodle-2026-10-08`, conservando los cambios preexistentes. No se hizo push, merge ni entrega en Moodle.

## Fuentes revisadas y novedades

Último ciclo observado: 11:02 CEST, `Result=success`, `ExecMainStatus=0`, 13 secciones, 77 actividades, cero errores/fuentes inaccesibles. Snapshot remoto `moodle-sync/master/2026-10-08`, `92752dc40fb0`; todavía no integrado en master al comenzar este trabajo. [Hashes actuales](moodle_hashes.json): todos los archivos coinciden con el manifiesto. Las 11 tareas de entrega son las mismas que master; no se infiere un envío/nota del alumnado.

- [Boosting](../../03_ML_5072/soluzioak/Boosting/README.md): dos PDF nuevos; cuatro ejemplos Python y tres cálculos manuales completos, script/notebook, gráfica, test diabetes separado y baseline. No existe rúbrica de entrega adicional visible.
- [Elastic Stack P18–P22](../../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-08/README.md): cinco ejercicios nuevos, todas sus preguntas, pipelines y pruebas. Comparadas las dos versiones de hoy del PDF: el último cambio binario no añade texto al enunciado.
- Cuaderno del tema 3: ejemplos curl y carga `.env`; se conservan los originales sincronizados. Los cambios de documentación no añaden otra actividad práctica numerada.
- La nueva referencia de vídeo es apoyo docente, no una tarea de entrega. La revisión cubre el ciclo observado; no garantiza novedades posteriores a esa hora.

## Pruebas ejecutadas ahora

[Registro de tests](tests.json): **92 pruebas finales pasadas**. CNC Guard 18, Moodle/publicación 39, API ML 8, estructura Frameworks 2, regresión CSV 3, Kafka mock 1, Kafka Medallion 12, tears_style 5, Faker/fecha 1 y Boosting 3. El primer comando Medallion omitía Pandas: 10 pass/2 fail; se conserva el fallo y se repitió con la dependencia completa, 12 pass. No se cambió código para ocultar ese fallo de entorno.

[Programación batch](programazioa_batch.json): cinco series ejecutables (Lengoaiak, Datu Zientzia, sus dos variantes PDF y Programazioa), todas exit 0, en copias aisladas con datos propios. Incluye el benchmark de 1/10/50 millones: sus tiempos no constituyen una comparativa portable entre máquinas. Los archivos originales no se sobrescribieron.

[Seguridad/privacidad](seguridad_privacidad.json): seis scripts del 7 de octubre, todos exit 0. Se observan los bypasses que el detector sencillo no detecta y se conserva la distinción entre simulación de ruido y garantía de privacidad diferencial.

[Apps locales](apps_locales.json): FastAPI HTTP real 404/201/409/200/422/204/404 y cierre del servidor; Streamlit AppTest, formulario/contador/predicción/métricas. AppTest no se atribuye a interacción de navegador. Series temporales y script Pipeline/API ejecutados otra vez; SVM repetido sin diferencias en su JSON. Sus resultados sintéticos no se convierten en evidencia industrial o clínica.

Elastic: Grok Debugger real en Kibana 9.5.4 para P18 y seis entradas P20/P21; snapshots/capturas y valores guardados. El pattern original coincide parcialmente sin fecha y con status como string; el corregido exige línea completa y convierte a entero. Compose P20 ejecutado realmente, tres eventos y exit 0. Los otros eventos reales de Logstash y cuatro casos negativos están en la carpeta de práctica. Kibana mostró errores de recursos/plugin (por ejemplo user_profile 404 en el lab sin seguridad); la simulación Grok terminó correctamente. No se declara la consola completamente limpia.

NiFi: ejecutado `nifi_lab_validar_evidencias.py`, evidencia archivada de seis casos coherente. **No es otro runtime NiFi**, ni cierra la falta de captura de Canvas o la variante MariaDB.

Boosting: notebook ejecutado, script ejecutado por separado y tres regresiones conceptuales pasadas. `uv.lock` propio, `pip-audit` sin vulnerabilidades conocidas detectadas. Sin llamadas Gemini, carga de pickle ajeno ni descarga de modelos.

## Lo que todavía necesita información o acceso externo

Se han revisado las filas parciales/requiere datos humanos de [la auditoría](../AUDITORIA_EJERCICIOS.md). Las soluciones/plantillas ya existentes se mantienen; sus requisitos pendientes no se sustituyen por datos inventados:

| Pendiente | Motivo concreto |
|---|---|
| CNC Guard: contrato, roles, propuestas 63276/63277, controles, presentación y evaluaciones | Requiere decisiones/acuerdos/firmas/participación del equipo y ejecución del proyecto a lo largo del curso. |
| Ética 02-06, 02-09 y parte de 02-13 | No están disponibles los notebooks docentes 3.1 de fairness hospitalaria, 12.0 compliance SHAP/LIME y 6.1 ALTAI; el 3.1 de privacidad recién descargado es otro ejercicio. No reconstruimos datos o rúbricas desconocidas. |
| Ética 02-07/02-12/02-13 | Debate y acuerdo real del grupo, rúbrica/puntuaciones de ALTAI y selección confirmada del sistema. |
| Lengoaiak 1.2/2.1/2.2/2.4/2.5/4.3/4.4 | Presentación, IDE de clase/Pylance, archivos reales de un compañero, comparación de respuestas reales y colaboración/PR de participantes. Ejecutar código local no acredita esos actos. |
| Gemini/LLM/RAG | Cuenta/clave/cuota y documentos privados de la práctica; no se leen credenciales para inventar permisos ni se hacen llamadas externas sin el acceso requerido. |
| NiFi DF1.1 | Captura Canvas del flujo en el laboratorio original; los datos y provenance ya tienen evidencia histórica. |
| NiFi DF2.2 | La ejecución original completa validó MySQL 8.4, no MariaDB, y no hay benchmark repetido; se conserva la diferencia. |
| NiFi DF2.3 | AEMET necesita clave y configuración real; la variante Open-Meteo no equivale a AEMET/AWS. |
| Kafka K3 | El-tiempo.net dio 405 en la evidencia anterior; Open-Meteo es una variante declarada. Las 12 pruebas locales no prueban que el proveedor original esté operativo hoy. |
| Orange/SVM y Moodle | Los artefactos existentes no acreditan una nueva entrega, una nota ni requisitos de una rúbrica no visible. |

Los dos servicios GUI temporales están detenidos y sus contenedores/volumen se conservan como evidencia. Logstash termina al completar la lectura. No se alteraron servicios anteriores ni se borraron bases/volúmenes. Las salidas brutas `.log` se conservan localmente e ignoran para publicación; los JSON/capturas elegidos documentan los resultados portables.
