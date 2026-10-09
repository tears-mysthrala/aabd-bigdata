# Contraste de las fuentes docentes y las soluciones propias

Las fuentes sincronizadas se conservan para comparar versiones y verificar
SHA-256. Sus outputs son resultados guardados por el autor; no representan una
ejecución nuestra. Las siguientes observaciones se aplican a la edición del 9
de octubre y se corrigen o explican en las soluciones propias.

| Fuente / apartado | Observación | Referencia propia |
| --- | --- | --- |
| `3_Adibide_koadernoa.ipynb`, FastAPI | El comando de arranque y la ruta del ejemplo no coinciden con `ml_api.py` y `/iragarri`. | [Pipeline/API](../08_Moodle_2026-10-07/README.md): ejecutar `uv run --frozen uvicorn ml_api:app --host 127.0.0.1 --port 8000` desde su carpeta. |
| `3_SOLUZIOAK_URLa.ipynb`, conclusiones de métricas | El texto 94%/40% no coincide con los outputs guardados 0.9575/0.7576. | [Cuaderno propio](3_Ariketa_koadernoa_RESUELTO.ipynb): métricas calculadas junto a la matriz TN/FP/FN/TP, sin copiar porcentajes estáticos. |
| Misma fuente, GridSearch | La parrilla ampliada hasta 5000 árboles cambia la restricción de 50/100; escalar antes del CV filtra información entre folds. | Pipeline dentro de GridSearch, `n_estimators=[50,100]`, `max_depth=[None,5]`, tres folds y balanced accuracy justificada. |
| Misma fuente, apartado 6.5 | Hay un NameError guardado, avisos de nombres de variables y una probabilidad vinculada a la clase predicha. | La simulación propia ejecutada valida 20 valores finitos y define explícitamente `probabilitatea=P(target=1)`; no es la confianza de la clase predicha. El contrato no se mezcla con el docente. |
| Misma fuente, autenticación API | Los tokens de ejemplo del entorno y curl no coinciden. La ausencia de cabecera puede producir 403 con el comportamiento del ejemplo. | La API propia requiere un secreto configurado, sin valor por defecto; [pruebas Bearer](../05_Frameworkak_PDF_Ariketak/test_bearer_api.py) comprueban 401 y `WWW-Authenticate: Bearer`, 200 autorizado y 422 para entrada inválida. |

Estas correcciones no certifican el contenido restante de las fuentes ni una
entrega en Moodle. La ejecución, métricas y límites de nuestra variante están
en el [README](README.md) y su informe de ejecución.
