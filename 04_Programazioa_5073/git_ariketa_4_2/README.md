# Git 4.2: saludo, tests y simulación de colaboración

Este ejercicio contiene `agur.py`, un saludo con `--izena` y alternativa
interactiva, y `test_agur.py`, pruebas de sus entradas. [PR_DESC.md](PR_DESC.md)
describe una simulación local de rama y merge; no demuestra una PR remota.

Desde la raíz, con Python 3 y `uv` disponibles:

```bash
cd 04_Programazioa_5073/git_ariketa_4_2
uv venv .venv
uv pip install --python .venv/bin/python pytest
.venv/bin/python agur.py --izena Ane
.venv/bin/python -m pytest test_agur.py -v
```

El saludo debe incluir el nombre y las entradas vacías deben rechazarse según
el contrato de la función. Ejecutar tests comprueba comportamiento; no crea
ramas ni merge. Practica los comandos Git de la descripción en un repositorio
de prueba independiente, para no cambiar ramas ni historia del repositorio de
estudio. Comprueba `git log --graph` para distinguir commits y merge, y
`git status` para distinguir archivos modificados, staging y commit.

La descripción conserva comprobaciones históricas; esta revisión documental no
las presenta como una ejecución nueva. Una plantilla PR o un merge local no
equivalen a revisión por otra persona.
