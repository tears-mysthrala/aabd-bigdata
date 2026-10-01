# Cuaderno 1: Python, JSON, archivos y Git

Este bloque resuelve los 25 ejercicios del
[cuaderno de lenguajes](../../materialak/notebooks/5073_1_Lengoaiak_Ariketak.ipynb).
Abre la [solución Jupyter](5073_1_Lengoaiak_Ariketak.ipynb) para leer enunciado,
razonamiento y comprobación juntos. El [script](5073_1_Lengoaiak_Ariketak.py)
presenta la misma secuencia con comentarios y celdas `# %%`.

## Preparación y ejecución

Requiere Python 3, Git y `uv` en el PATH. El script solo importa la biblioteca
estándar; `uv` se utiliza en el ejercicio 2.3 para crear un entorno de prueba.
Desde la raíz del repositorio:

```bash
cd 04_Programazioa_5073/soluzioak/01_Lengoaiak_Ariketak
python 5073_1_Lengoaiak_Ariketak.py
```

Para Jupyter, abre el `.ipynb` en un editor compatible y usa un kernel Python;
la carpeta de trabajo debe ser esta. Reinicia el kernel y ejecuta todo en orden.
El setup crea los datos de ejemplo; no necesitas descargar archivos ni usar APIs.

**Efectos:** se regeneran `data/test.json` y `data/test.txt`; los ejercicios
crean `berria.json`, `agurra.txt`, `datuak.pkl` y `karpeta_berria/readme.md`.
2.3 usa `uv venv --clear data/test_env`: reemplaza el entorno de prueba si ya
existe. 2.4/2.5 ejecutan `git init` y `git add` dentro de `data/karpeta_berria`,
sin hacer commit ni enviar nada. Usa una copia de esta carpeta si has guardado
trabajo propio en esas rutas.

## Recorrido y resultados esperados

| Ejercicios | Idea que debes entender | Comprobación |
|---|---|---|
| 1.1–1.5 | `loads/dumps` trabajan con cadenas; `load/dump`, con archivos. JSON representa datos, no código ejecutable. | Un diccionario con `izena=Mikel`, una cadena con `Bilbo`, `aktiboa=true` en el archivo nuevo y JSON indentado. |
| 2.1–2.5 | El directorio de trabajo decide dónde se escriben rutas relativas. Un venv aísla dependencias; `git add` prepara cambios para un commit. | Carpeta y entorno creados; `readme.md` aparece en `git status --porcelain` del repositorio de prueba. |
| 3.1–3.5 | Una comprehension transforma o filtra; el orden de los `for` importa al aplanar. | Cuadrados de 1 a 10, pares `[2,4,6,8]`, mayúsculas, iniciales y lista `[1,2,3,4,5,6]`. |
| 4.1–4.5 | `lambda` expresa una operación breve; `map` transforma, `filter` selecciona y `sorted(key=...)` elige el criterio. | Producto `3*4=12`, dobles `[2,4,6,8]`, nombres con vocal, orden por nota y resultado `[16,14]`. |
| 5.1–5.5 | Los modos `w/r` son texto y `wb/rb` binarios. Releer un archivo permite comprobar lo escrito. | Saludo `Epa!`, dos líneas, diccionario recuperado igual al original y `puntuazioa=100` al final. |

El último ejercicio modifica `test.json`: volver solo a 1.3 sin repetir el setup
puede leer la versión modificada. En 5.4 carga únicamente el pickle que acabas
de crear en 5.3; cargar un pickle ajeno puede ejecutar código.

## Cómo comprobar tu comprensión

Predice el resultado antes de ejecutar. Cambia un valor y explica qué assert
debería fallar. Distingue dato en memoria, texto JSON y archivo en disco.
Si todos los pasos terminan sin excepción, las comprobaciones incorporadas han
pasado. El [registro histórico](../egiaztapena_2026-09-28.md) no sustituye una
ejecución de tu copia actual.
