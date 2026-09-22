# CNC Guard — Requisitos de instalación y entorno reproducible con uv y Jupyter

**Versión del documento:** 1.0 · **Fecha de revisión:** 17 de septiembre de 2026  
**Destinatarios:** equipo de estudiantes de la especialización de Inteligencia Artificial y Big Data.  
**Objetivo:** preparar el entorno mínimo para desarrollar y entregar un notebook `.ipynb`, sin bloquear una futura adaptación a CNC reales.  
**Estado:** propuesta de instalación y dimensionamiento; no es una instalación industrial validada.

**Ruta de uso:** revisar requisitos en los apartados 3–5; una persona inicializa con el apartado 8 y el resto replica con el 9. El ZIP contiene los archivos auxiliares. Los apartados 16–18 son extensiones condicionadas, no tareas de instalación inmediata.

## 1. Decisión técnica y límites del documento

Se propone **CPython 3.13 de 64 bits + uv + JupyterLab + scikit-learn + DuckDB/Parquet**, ejecutado localmente en CPU. El notebook será el entregable académico principal. El panel independiente y los conectores industriales serán opcionales.

El enunciado exige, entre otros aspectos, aplicar aprendizaje supervisado y no supervisado, integrar distintas fuentes y tipos de datos, y tratar calidad, integridad y seguridad. Esos objetivos justifican las capacidades de este entorno, pero **el PDF no convierte esta lista concreta de paquetes en una obligación del profesorado**. La entrega mediante Jupyter Notebook es un requisito adicional indicado por el equipo en esta conversación. [E1, pp. 3–7]

Este documento separa tres niveles:

| Nivel | Alcance | Cuándo instalarlo |
|---|---|---|
| **Base académica** | Datos, modelos, gráficos, notebook, ejecución automática y pruebas. | Ahora, en todos los equipos. |
| **Extensiones justificadas** | Streamlit, formatos adicionales o servicios exigidos expresamente por una asignatura. | Solo cuando exista una necesidad confirmada. |
| **Piloto industrial** | Adquisición autorizada, protocolos de la máquina, operación controlada y mantenimiento del software. | Después de identificar CNC, controlador, interfaces y condiciones de acceso. |

**No se instalarán por defecto** CUDA, PyTorch, TensorFlow, Anaconda/Miniconda, Kubernetes, Kafka, Hadoop/Spark, un servidor SQL, Node.js/npm, Qt, compiladores ni toolchains Rust. Tampoco se instalará todo lo opcional «por si acaso».

La selección de Python 3.13 es una decisión de proyecto, no una afirmación de que sea la última versión. Esta rama mantiene un calendario de soporte publicado por Python y PyArrow documenta su compatibilidad con ella. El parche exacto se fijará durante el primer setup y se mantendrá común al equipo. No se usará una compilación experimental o free-threaded. [P1][A1]

### Estado de comprobación

La documentación oficial de las herramientas se ha consultado para preparar este plan. El manifiesto y los scripts auxiliares se entregan como base de trabajo. **No se ha podido descargar y resolver aquí el conjunto completo de dependencias**: no se adjunta un `uv.lock` inventado ni se presenta la instalación completa como probada. Los tamaños y tiempos indicados son **estimaciones de planificación**, no benchmarks.

Sí se han validado la sintaxis de los cinco archivos Python, los dos TOML y la estructura y sintaxis de celdas del notebook auxiliar. Las tres pruebas unitarias de rutas y recursos han pasado, y el bootstrap se ha probado en una copia temporal, incluyendo el rechazo de una reinicialización. Estas comprobaciones no equivalen a ejecutar el stack completo; Ruff, el smoke test integral y el notebook ejecutado quedan pendientes. El detalle figura en `docs/VALIDACION_PLANTILLA.md` del ZIP.

El primer equipo con acceso a Internet debe generar el bloqueo, completar las pruebas de este documento y compartir el resultado. La resolución de dependencias y la ejecución en cada sistema operativo forman parte de la aceptación del setup.

## 2. Qué aporta uv y qué ocurre con `.venv`

`uv` sustituye el flujo manual de instalación y sincronización; **no sustituye el concepto de entorno virtual**. En un proyecto normal crea una `.venv`, que no hace falta activar: los comandos se ejecutan con `uv run`. [U1][U2]

La fuente de verdad del equipo será:

| Archivo | Función |
|---|---|
| `pyproject.toml` | Dependencias directas, grupos, compatibilidad y configuración del proyecto. |
| `uv.lock` | Resolución concreta de versiones y artefactos de dependencias. Lo genera uv. |
| `.python-version` | Parche de Python elegido para el proyecto; se comparte sin rutas personales. |
| `docs/uv-version.txt` | Registro informativo de la versión de uv utilizada al inicializar. No es un archivo que uv interprete automáticamente. |
| `config/resources.toml` | Límites operativos y parámetros iniciales que deben aplicarse desde el código. |

El lock no congela por sí solo el sistema operativo, el navegador, todas las bibliotecas nativas, el backend de construcción, el hardware ni los datos. La reproducibilidad requiere también registrar esos componentes y comprobar resultados. [U2][U3]

**Reglas del equipo:** no usar `sudo pip`, `pip install --user`, `uv pip install --system` ni instalaciones desde celdas con `%pip`/`!pip`. Las dependencias se cambian desde la terminal mediante `uv add` y se revisan en Git. No se mezclará este proyecto con el entorno `uv tool` de Orange ni con otros proyectos.

### Entorno fuera del repositorio

La opción de menor fricción es dejar que uv gestione `.venv`. Cuando se prefiera mantenerla fuera de una carpeta sincronizada, configurar **antes del primer `uv sync`**, solo en la terminal de ese proyecto:

Linux/macOS, Bash o Zsh:

```bash
export UV_PROJECT_ENVIRONMENT="$HOME/.local/share/cnc-guard/envs/principal-py313"
```

Windows, PowerShell:

```powershell
$env:UV_PROJECT_ENVIRONMENT = Join-Path $env:LOCALAPPDATA 'cnc-guard\envs\principal-py313'
```

uv creará el entorno en esa ruta. Sigue siendo un entorno virtual gestionado por uv. **No reutilizar esa ruta para otros proyectos o worktrees**, porque la sincronización puede retirar paquetes ajenos al perfil solicitado. Cada copia de trabajo necesita una ruta propia. No apuntar a `/usr`, `/usr/local`, al Python global ni a un entorno existente de otra aplicación. [U3]

Esta variable debe estar presente en las terminales que operen sobre ese entorno externo. No añadir una misma ruta global a todos los proyectos. Para volver al comportamiento normal en una terminal nueva, no establecerla; no borrar ni mover entornos durante una sesión Jupyter activa.

## 3. Hardware y almacenamiento precalculados

Las cifras siguientes presupuestan un notebook con datos tabulares, modelos pequeños y procesamiento por lotes. No dimensionan adquisición de vibraciones de alta frecuencia ni entrenamiento profundo.

| Recurso | Base utilizable propuesta | Equipo de referencia recomendado |
|---|---|---|
| CPU | 2 núcleos disponibles; ejecución conservadora. | 4 núcleos disponibles; no ocuparlos todos simultáneamente. |
| RAM instalada | 8 GiB, con servicios opcionales detenidos. | 16 GiB para notebook, navegador y pruebas de volumen moderado. |
| Disco libre | 10 GiB para un inicio acotado. | **20–30 GiB** para caché, datos, derivados y margen. |
| GPU | No requerida por este diseño. | No comprar GPU para este alcance. |
| Sistema | Sistema operativo e intérprete de 64 bits. | Linux x86-64 o Windows x86-64 actualizado y compatible con las wheels seleccionadas. |
| Red | Acceso inicial a fuentes y repositorios autorizados. | Ejecución académica posterior sin dependencia obligatoria de Internet. |

Apple Silicon o Linux ARM64 pueden ser opciones, pero deberán superar su propia instalación y pruebas de wheels. Un único `uv.lock` no es evidencia de que todas las arquitecturas hayan sido ensayadas.

### Presupuesto inicial de disco

| Concepto | Reserva estimada |
|---|---:|
| uv y Python gestionado | 0,2–0,6 GiB |
| Entorno base: ciencia de datos, Jupyter y herramientas | 1,5–3 GiB |
| Caché y descargas de uv | 1–3 GiB |
| Datos originales, muestras y documentación | 0,1–2 GiB, según dataset |
| Datos tratados, temporales, modelos y resultados | 2–6 GiB |
| Margen de trabajo y recreación | 4–8 GiB |
| **Reserva práctica** | **20 GiB como punto de partida; 30 GiB con más margen** |

No sumar el espacio aparente de caché y entorno como si siempre fueran dos copias físicas: uv puede reutilizar archivos mediante mecanismos dependientes del sistema de archivos. Esta tabla mantiene margen y no promete una deduplicación concreta. No limpiar la caché inmediatamente antes de una defensa offline. [U4]

La descarga inicial podría situarse aproximadamente en **0,3–1 GiB**, muy dependiente de plataforma, wheels y estado previo de la caché. No incluye imágenes Docker, Chromium para PDF ni datasets grandes.

### RAM para datos tabulares

Para una matriz puramente numérica de 20 columnas `float32`, sin índices, textos, copias ni modelos:

```text
100.000 filas × 20 × 4 bytes =   8.000.000 bytes ≈   7,6 MiB
1.000.000 filas × 20 × 4     =  80.000.000 bytes ≈  76,3 MiB
5.000.000 filas × 20 × 4     = 400.000.000 bytes ≈ 381,5 MiB
```

Eso **no** es la memoria total de pandas ni del entrenamiento. Se reservan copias, índices, conversiones y estructuras de modelos. Se empezará con lotes de **100.000 filas**, se medirá el consumo y se evitará cargar el volumen sintético completo en pandas para después duplicarlo varias veces.

Presupuesto operativo inicial: hasta 2–4 GiB para kernel, datos y un entrenamiento moderado, más navegador y sistema. En un equipo de 8 GiB, empezar con `model_jobs = 1`. Estos presupuestos no garantizan ausencia de errores de memoria.

## 4. Prerrequisitos del sistema y comprobación previa

Antes de instalar, comprobar lo existente. En Omarchy/Arch no se alterarán Python global, Rust, Cargo, Orange ni sus entornos. No se usará `rustup` para este proyecto.

Linux/macOS:

```bash
command -v uv
uv --version
command -v git
git --version
uv python list --only-installed
```

PowerShell:

```powershell
Get-Command uv, git -ErrorAction SilentlyContinue
uv --version
git --version
uv python list --only-installed
```

Se necesita un navegador y permisos de escritura en la carpeta del proyecto y en las carpetas de datos de uv/Jupyter. Después de instalar uv, el flujo de Python no requiere trabajar como administradora.

### Omarchy / Arch

Si `uv` y `git` ya están disponibles, no reinstalarlos. Para los componentes que falten, usar `yay` y revisar la transacción:

```bash
yay -S --needed uv git
```

uv está disponible como paquete binario del repositorio Extra; instalarlo de este modo no requiere compilar uv con Cargo. No añadir `rustup`, `base-devel` o un conjunto de compiladores para resolver el setup Python. No hacer una sincronización aislada de índices `-Sy`; mantener el sistema mediante su procedimiento habitual, fuera de esta receta. [S1]

No instalar `apache-arrow` como supuesto prerrequisito del host: aquí se solicita **`pyarrow` dentro del proyecto**. Igualmente, `duckdb` será el paquete Python; su CLI independiente no es necesaria.

### Windows

Usar una terminal PowerShell normal y una carpeta local, por ejemplo dentro de `source`, fuera de OneDrive. Si faltan las herramientas:

```powershell
winget install --exact --id astral-sh.uv
winget install --exact --id Git.Git
```

Reabrir la terminal y comprobar `uv --version` y `git --version`. No instalar otra distribución Python ni Conda para esta receta. El método WinGet de uv está documentado por Astral y el de Git por su proyecto oficial. [U5][S4]

Si una wheel de PyArrow da un error de DLL, comprobar arquitectura y el **Microsoft Visual C++ Redistributable** correspondiente, desde Microsoft. No equivale a instalar Visual Studio completo y no debe intentarse corregir desactivando el antivirus. [A1]

### Otros Linux y macOS

Reutilizar uv existente. En macOS con Homebrew ya disponible, `brew install uv git` es una vía posible. En otros sistemas puede emplearse el instalador oficial de uv, descargado y revisado antes de ejecutarlo, sin `sudo`. No mezclar métodos de instalación de uv en una misma máquina. [U5]

```bash
curl -LsSf https://astral.sh/uv/install.sh -o /tmp/cnc-guard-uv-install.sh
less /tmp/cnc-guard-uv-install.sh
sh /tmp/cnc-guard-uv-install.sh
```

La instalación del gestor requiere confiar en su canal de distribución. La revisión del script no equivale por sí sola a una auditoría completa.

## 5. Dependencias por función

### Base de ejecución

| Paquete | Utilización prevista | Nota de alcance |
|---|---|---|
| `numpy` | Matrices y operaciones numéricas. | CPU, tipos de datos controlados. |
| `pandas` | Limpieza, unión y exploración tabular. | Mantener inicialmente la familia 2.x para reducir cambios respecto a materiales de clase; revisar esa decisión antes de uso prolongado. |
| `scipy` | Estadística, señales y lectura de archivos `.mat` compatibles. | También resulta útil si se selecciona un dataset de fresado. |
| `scikit-learn` | Supervisado, no supervisado, pipelines y métricas. | No se necesita un framework de deep learning para los modelos propuestos. |
| `duckdb` | Consultas y agregaciones sobre archivos. | Motor embebido; no exige un servicio de base de datos. |
| `pyarrow` | Lectura/escritura Parquet y procesamiento columnar. | No requiere montar Hadoop. |
| `joblib` | Persistencia de modelos propios. | No cargar modelos de procedencia desconocida. [M2] |

### Grupo `notebook`, instalado por defecto

| Paquete | Función |
|---|---|
| `jupyterlab` | Interfaz web local para desarrollar el `.ipynb`. |
| `ipykernel` | Kernel de Python del proyecto. |
| `nbconvert` | Ejecutar notebooks desde cero y exportar resultados. |
| `nbformat` | Leer y validar estructuralmente archivos `.ipynb`. |
| `matplotlib` | Gráficos estáticos incrustados en la entrega. |

**Entregar un Jupyter Notebook no obliga a instalar la interfaz clásica denominada `notebook`**. JupyterLab sirve para trabajar con el formato `.ipynb`; se reserva un grupo `classic` únicamente para una preferencia o exigencia explícita de interfaz. No se necesita Node.js para el uso normal de esta instalación binaria, sin desarrollar extensiones. [J1][J2]

### Grupo `dev`, instalado por defecto

`pytest` para pruebas; `ruff` para revisión y formato; `psutil` para observar recursos. No se añaden, por defecto, varias herramientas que hagan el mismo trabajo.

### Opcionales predefinidos

| Activación | Dependencia | Condición para instalarla |
|---|---|---|
| `--extra dashboard` | `streamlit` | Se decide mantener un panel independiente del notebook. |
| `--extra opcua` | `asyncua` | La interfaz autorizada de la CNC o del simulador es OPC UA. |
| `--extra mqtt` | `paho-mqtt` | Hay un broker definido y se necesitan suscripciones/publicaciones de telemetría. |
| `--extra mongo` | `pymongo` | MongoDB es una fuente realmente utilizada. |
| `--extra mat73` | `h5py` | El dataset concreto exige leer la estructura HDF5 de un MAT v7.3. No es un lector universal de toda estructura MATLAB. |
| `--extra excel` | `openpyxl` | Hay inventarios o partes `.xlsx` que deban procesarse. |
| `--group security` | `pip-audit` | Revisión de vulnerabilidades antes de hitos o entrega. |
| `--group classic` | `notebook` | Se exige esa interfaz, además del formato `.ipynb`. |
| `--group pdf` | `nbconvert[webpdf]` | Se exige PDF automático y se acepta instalar Playwright/Chromium. |

No instalar todos los extras de una vez. Los extras se resuelven en el lock, pero no se instalan por defecto; resolver un grupo opcional también puede revelar incompatibilidades que se deban corregir. [U2][U6]

## 6. Manifiesto inicial: `pyproject.toml`

Los rangos son una **política inicial de compatibilidad**, no versiones finales verificadas. El primer `uv lock` seleccionará versiones concretas que deberán pasar las pruebas. El proyecto local se instala en modo editable para que el notebook importe `cnc_guard` desde cualquier subcarpeta sin trucos de `sys.path`. [U2]


```toml
[project]
name = "cnc-guard"
version = "0.1.0"
description = "Demostrador académico de supervisión de condición de CNC"
requires-python = ">=3.13,<3.14"
dependencies = [
    "numpy>=2.2,<3",
    "pandas>=2.2.3,<3",
    "scipy>=1.15,<2",
    "scikit-learn>=1.6,<2",
    "duckdb>=1.2,<2",
    "pyarrow>=19",
    "joblib>=1.4,<2",
]

[project.optional-dependencies]
dashboard = ["streamlit>=1.40,<2"]
opcua = ["asyncua>=1.1,<2"]
mqtt = ["paho-mqtt>=2,<3"]
mongo = ["pymongo>=4.10,<5"]
mat73 = ["h5py>=3.12,<4"]
excel = ["openpyxl>=3.1,<4"]

[dependency-groups]
notebook = [
    "jupyterlab>=4.3,<5",
    "ipykernel>=6.29,<8",
    "nbconvert>=7.16,<8",
    "nbformat>=5.10,<6",
    "matplotlib>=3.9,<4",
]
dev = [
    "pytest>=8,<10",
    "ruff>=0.10,<1",
    "psutil>=6,<8",
]
security = ["pip-audit>=2.9,<3"]
classic = ["notebook>=7,<8"]
pdf = ["nbconvert[webpdf]>=7.16,<8"]

[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/cnc_guard"]

[tool.uv]
required-version = ">=0.10"
default-groups = ["notebook", "dev"]
# Evitar compilaciones de dependencias desde sdists. El código local
# y sus requisitos editables pueden seguir ejecutando su backend de build.
no-build = true

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

`required-version` establece un mínimo de uv para esta plantilla, no fija el ejecutable a una versión exacta. Registrar y acordar la misma versión cuando sea posible. El backend Hatchling está declarado por separado: **no afirmar que todo su entorno de construcción queda congelado por `uv.lock`**. Para una futura distribución industrial habrá que fijar y registrar también la cadena de construcción.

`no-build = true` evita recurrir a compilaciones de dependencias desde distribuciones fuente. Si no existe una wheel compatible, se debe investigar la incompatibilidad, no instalar compiladores sin más. La documentación actual aclara que los proyectos locales y requisitos editables pueden seguir ejecutando sus backends; esto **no es un sandbox ni una prohibición absoluta de ejecutar código durante la instalación**. [U7]

## 7. Estructura del proyecto y archivos auxiliares

El paquete auxiliar `CNC_GUARD_SETUP.zip` acompaña a este Markdown para evitar copiar manualmente el manifiesto y los scripts:

```text
cnc_guard_setup/
├── INSTALACION_CNC_GUARD_UV_JUPYTER.md
├── pyproject.toml
├── .python-version                 # Lo crea la inicialización; compartir después.
├── uv.lock                         # Lo genera uv; compartir después.
├── .gitignore
├── .gitattributes
├── 00_verificacion_entorno.ipynb    # Solo verifica el setup; NO es la entrega terminada.
├── CNC_Guard.ipynb                  # A desarrollar por el equipo; no incluido.
├── config/
│   └── resources.toml
├── src/cnc_guard/
│   ├── __init__.py
│   └── runtime.py
├── scripts/
│   ├── bootstrap.py
│   └── verify_setup.py
├── tests/
│   └── test_runtime.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── models/
├── reports/
└── docs/
```

Los scripts tienen estas responsabilidades:

**`bootstrap.py`** crea las carpetas y, con `--initialize`, escribe el parche exacto de Python y registra uv. Rechaza reinicializar cuando ya existe `.python-version` o `uv.lock`. No instala paquetes ni modifica otros entornos.

**`verify_setup.py`** verifica importaciones, intercambio pandas/Parquet/DuckDB, un entrenamiento de juguete supervisado y otro no supervisado, persistencia de un modelo generado por el propio script y renderizado de un PNG. Escribe versiones, huella del lock y datos básicos del entorno en `reports/environment.json`. No necesita una fábrica ni Internet. Su memoria registrada es la RSS al terminar, **no el pico de memoria**. Sus resultados no miden capacidad predictiva.

**`runtime.py`** localiza la raíz del proyecto y aplica variables de hilos antes de cargar bibliotecas numéricas. Las cuotas de cada modelo y conexión deben pasarse explícitamente al código que las utilice.

Descomprimir en una carpeta nueva. **No sobrescribir un proyecto existente** con esta plantilla. Cuando ya haya código, integrar los cambios revisando el manifiesto y los archivos uno a uno.

## 8. Primer setup: una sola persona genera la referencia

Este procedimiento supone que se ha descomprimido el paquete auxiliar y se está en su raíz. No se ejecuta desde el repositorio de Orange, MKDL u otra aplicación.

### 8.1. Instalar un Python gestionado sin cambiar el global

Los siguientes comandos son de una sola línea y valen tanto en Bash/Zsh como en PowerShell:

```bash
uv python install 3.13 --no-bin --no-registry
uv run --no-project --managed-python --python 3.13 python scripts/bootstrap.py --initialize
```

`--no-bin` evita añadir ejecutables Python al directorio de binarios de usuario. `--no-registry` evita registrar esta instalación en Windows. No usar `--default`, `--force` ni una actualización global de todos los Python gestionados. `--managed-python` impide escoger por accidente el intérprete del sistema. [U8]

El bootstrap escribe una versión concreta como `3.13.<parche resuelto>`, no una ruta como `/home/alguien/.../python`. No usar `uv python pin --resolved` para un archivo que se compartirá: esa opción fija una ruta local. [U7]

### 8.2. Resolver y sincronizar

```bash
uv lock --managed-python
uv sync --locked --managed-python
```

No intercambiar estos pasos: **`--locked` no crea un lock inexistente ni repara uno desactualizado**. Si falla la resolución, conservar el error y revisar requisitos; no eliminar el control de versiones como solución.

### 8.3. Registrar el kernel dentro del entorno del proyecto

```bash
uv run --locked python -m ipykernel install --sys-prefix --name cnc-guard --display-name "Python (CNC Guard / uv)"
uv run --locked jupyter kernelspec list
```

Se usa `--sys-prefix` para registrar el kernel dentro del mismo entorno que aloja JupyterLab, en lugar de modificar un kernel global de otra aplicación. Si se recrea o mueve el entorno, repetir el registro: la kernelspec contiene la ruta a su intérprete. [J3]

### 8.4. Probar antes de empezar a desarrollar

```bash
uv run --locked python scripts/verify_setup.py
uv run --locked pytest -q
uv run --locked ruff check src scripts tests
uv run --locked ruff format --check src scripts tests
uv run --locked jupyter nbconvert --to notebook --execute 00_verificacion_entorno.ipynb --output 00_verificacion_entorno.ejecutado.ipynb --output-dir reports --ExecutePreprocessor.kernel_name=cnc-guard --ExecutePreprocessor.timeout=600
```

Si el formateador detecta diferencias, aplicar `uv run --locked ruff format src scripts tests`, revisar el diff y repetir. **No se considera validado el setup si falla una importación, una prueba o la ejecución limpia del notebook**.

### 8.5. Abrir JupyterLab

```bash
uv run --locked jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Abrir en el navegador la dirección con token que imprime Jupyter y seleccionar **Python (CNC Guard / uv)**. Mantener el token y la autenticación; no compartirlos ni incluirlos en capturas. `Ctrl+C` permite detener el servidor desde su terminal. [J4]

### 8.6. Compartir la referencia

Revisar y versionar `pyproject.toml`, `uv.lock`, `.python-version`, `docs/uv-version.txt`, código, configuración, notebook y pruebas. No compartir `.venv`, caché de uv, certificados privados, secretos, datos industriales no autorizados ni resultados con información personal.

No ejecutar `git add .` sin revisar qué se incorpora. El paquete incluye exclusiones iniciales, pero `.gitignore` no sustituye revisar los archivos de una entrega.

## 9. Setup del resto del equipo y del profesorado

Este procedimiento necesita una copia que ya contenga **el lock generado y el pin de Python**. No ejecutar otra vez `bootstrap.py --initialize`, `uv init` ni `uv lock --upgrade`.

```bash
uv python install --no-bin --no-registry
uv sync --locked --managed-python
uv run --locked python scripts/bootstrap.py
uv run --locked python -m ipykernel install --sys-prefix --name cnc-guard --display-name "Python (CNC Guard / uv)"
uv run --locked python scripts/verify_setup.py
uv run --locked pytest -q
uv run --locked jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Al ejecutarse en la raíz del proyecto sin un objetivo de versión explícito, `uv python install` puede utilizar el pin existente. Comprobar que se está en la carpeta correcta. [U8]

Cada integrante verificará en una celda `sys.executable` y `platform.python_version()`. El ejecutable debe corresponder a su entorno del proyecto, y la versión coincidir con `.python-version`. No publicar en la entrega las rutas personales mostradas durante esa comprobación.

La estructura puede soportar varios sistemas operativos mediante las distribuciones que resuelve uv, pero **cada sistema debe probarse**. Una ejecución correcta en Linux no demuestra que los controladores, DLL o permisos funcionen en Windows.

## 10. Uso diario y cambios de dependencias

Abrir una terminal nueva en la raíz y usar `uv run --locked ...`. Cuando el repositorio haya cambiado, detener el kernel y sincronizar antes de reabrirlo:

```bash
uv sync --locked --managed-python
uv run --locked jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Las nuevas dependencias requieren una necesidad documentada. Ejemplo, **solo después de decidir que se necesitan ficheros Excel y si ese extra no estuviera ya definido**:

```bash
uv add --optional excel "openpyxl>=3.1,<4"
```

En esta plantilla el extra ya está definido; para utilizarlo basta:

```bash
uv sync --locked --extra excel
uv run --locked --extra excel jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Mantener el mismo perfil en los comandos posteriores. `uv sync` realiza por defecto una sincronización exacta y puede retirar extras no seleccionados. No confundir que un paquete siga presente tras algún `uv run` con una dependencia correctamente declarada. [U2]

Para actualizar una dependencia por una corrección justificada, hacerlo en una rama y con el kernel detenido:

```bash
uv lock --upgrade-package scikit-learn
uv sync --locked --managed-python
uv run --locked pytest -q
uv run --locked python scripts/verify_setup.py
```

Después, reejecutar el notebook completo, comparar resultados y revisar el diff de `uv.lock`. Los límites del manifiesto siguen aplicándose; una nueva versión mayor puede exigir modificar también el rango. No actualizar todo el entorno la víspera de la entrega.

**`--locked` es la opción normal de reproducibilidad:** verifica que el lock sigue correspondiendo al proyecto. `--frozen` omite esa comprobación de actualidad, por lo que no se utilizará para ocultar discrepancias. [U2]

## 11. Reglas del notebook entregable

El notebook se desarrollará de forma que pueda ejecutarse con **Restart Kernel → Run All**, sin intervención manual, variables heredadas ni celdas ejecutadas en otro orden.

La primera celda de código debe configurar recursos antes de cargar las bibliotecas numéricas. Ejemplo:

```python
from cnc_guard.runtime import configure_resources, project_root

ROOT = project_root()
SETTINGS = configure_resources(ROOT)

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier

SEED = SETTINGS["resources"]["random_seed"]
MODEL_JOBS = SETTINGS["resources"]["model_jobs"]
```

Reiniciar el kernel después de cambiar límites de hilos o dependencias. Las variables de entorno establecidas después de cargar una biblioteca numérica pueden no reconfigurar sus pools activos. Los parámetros `n_jobs` y los hilos de BLAS/OpenMP pertenecen a mecanismos diferentes; no asumir que uno controla todos los demás. [M1]

No incluir instalaciones automáticas ni descargas implícitas dentro de la ejecución evaluable. La adquisición del dataset se hará una vez, con origen, licencia, versión y huella registrados; la carga del notebook utilizará archivos locales y fallará con un mensaje útil si faltan.

El núcleo reutilizable de limpieza y predicción irá en `src/cnc_guard/`; las decisiones, explicaciones, visualizaciones y resultados irán en el notebook. **Confirmar que se pueden entregar archivos auxiliares junto al `.ipynb`**. Si la plataforma admite exclusivamente un notebook, habrá que integrar el código necesario y acordar cómo se proporcionarán los datos; no declarar autocontenido un notebook que importa módulos ausentes.

### Organización propuesta de la entrega

| Parte del notebook | Evidencia esperada |
|---|---|
| Contexto y alcance | Problema, objetivo, uso previsto y límites. |
| Entorno y procedencia | Versiones, fuentes, licencias y configuración. |
| Datos | Perfilado, calidad, varias fuentes y tratamiento de texto libre. |
| Preparación | Transformaciones, selección de entradas y prevención de fuga de información. |
| Supervisado | Referencia, entrenamiento, validación y prueba coherentes con el dataset. |
| No supervisado | Detector o algoritmo apropiado y análisis de sus resultados. |
| Visualización e integración | Gráficos justificados y aplicación a datos nuevos. |
| Recursos e integridad | Medidas reales de tiempo/memoria, lotes y prueba de errores. |
| Riesgos y conclusiones | Limitaciones técnicas, privacidad, uso industrial condicionado y conclusiones sustentadas. |

Esta organización es una propuesta para reunir las evidencias del reto, no una transcripción de una plantilla oficial de notebook. [E1, pp. 3–7]

Para la entrega final, cuando exista `CNC_Guard.ipynb`:

```bash
uv run --locked jupyter nbconvert --to notebook --execute CNC_Guard.ipynb --output CNC_Guard.ejecutado.ipynb --output-dir reports --ExecutePreprocessor.kernel_name=cnc-guard --ExecutePreprocessor.timeout=600
uv run --locked jupyter nbconvert --to html reports/CNC_Guard.ejecutado.ipynb --embed-images --output CNC_Guard.html --output-dir reports
```

`600` es el timeout inicial **por celda**, no para todo el notebook. No utilizar `--allow-errors` ni un timeout ilimitado para disimular una ejecución defectuosa. El notebook de verificación incluido no sustituye este trabajo final. [J5]

## 12. Límites de recursos que deben aplicarse en el código

Configuración inicial incluida:

```toml
[resources]
blas_threads = 1
model_jobs = 2
duckdb_threads = 2
duckdb_memory_limit = "1GB"
batch_rows = 100000
random_seed = 42

[model]
random_forest_trees = 128
random_forest_max_depth = 12
isolation_forest_trees = 100
isolation_forest_max_samples = 256
```

Son puntos de partida del prototipo, no parámetros óptimos descubiertos. El bosque de prueba del smoke test es todavía más pequeño.

Ejemplo de uso de los límites, no de una evaluación completa:

```python
forest = RandomForestClassifier(
    n_estimators=SETTINGS["model"]["random_forest_trees"],
    max_depth=SETTINGS["model"]["random_forest_max_depth"],
    random_state=SEED,
    n_jobs=MODEL_JOBS,
)

anomaly = IsolationForest(
    n_estimators=SETTINGS["model"]["isolation_forest_trees"],
    max_samples=SETTINGS["model"]["isolation_forest_max_samples"],
    random_state=SEED,
    n_jobs=MODEL_JOBS,
)
```

No paralelizar simultáneamente una búsqueda de hiperparámetros y cada estimador con todos los núcleos. La primera entrega debe poder entrenarse en un equipo normal del aula. Las semillas favorecen la repetibilidad, pero no garantizan identidad bit a bit entre sistemas y bibliotecas distintos. [M1]

Para DuckDB, aplicar `threads` y `memory_limit` a cada conexión, reservar una carpeta temporal escribible y dejar espacio para derrame a disco. **El límite del motor no es una cuota absoluta de RAM para todo Python**: otras bibliotecas y algunas operaciones pueden consumir memoria aparte. Un servicio futuro necesitará límites del sistema operativo o del contenedor además de estos parámetros. [D1]

No entrenar sobre millones de filas sintéticas creadas solo para «hacer Big Data». El ensayo de volumen se ejecutará por separado y no contaminará la evaluación predictiva.

## 13. Datos, rutas e integridad

Mantener los originales en `data/raw/`, las transformaciones en `data/processed/` y pequeñas muestras autorizadas en `data/samples/`. No sobrescribir el original desde una celda. Usar `pathlib`, rutas relativas a `ROOT`, UTF-8, unidades explícitas y fechas con zona horaria cuando existan.

Cada fuente deberá tener un registro con nombre, procedencia, licencia, fecha de adquisición, tamaño, SHA-256 y descripción de columnas/unidades. No generar una huella de referencia a partir de un archivo ya alterado y utilizarla después como supuesta prueba de integridad.

La carpeta de datasets reales puede quedar fuera de Git, pero **la entrega debe explicar cómo obtenerlos o proporcionar una copia autorizada**. Ignorar los datos no convierte por sí solo el proyecto en reproducible.

Las muestras sintéticas se marcarán como tales. Los textos de mantenimiento se conservarán como texto libre cuando corresponda; envolver una tabla en JSON no demuestra por sí solo tratamiento de datos no estructurados.

El requisito de valorar calidad e integridad en sistemas de archivos distribuidos no queda acreditado instalando PyArrow o guardando un Parquet local. Confirmar con el profesorado el laboratorio y la evidencia exigida antes de instalar HDFS/Spark. [E1, p. 7]

## 14. Seguridad del entorno y trazabilidad

La base funcionará como usuario normal, con Jupyter limitado a loopback y autenticación activa. No utilizar el notebook como servidor multiusuario expuesto a la red industrial: ejecutar notebooks implica ejecutar código con permisos del proceso. [J4]

No cargar `pickle`/`joblib` procedentes de terceros desconocidos. El hecho de que un archivo sea un «modelo de IA» no lo hace inerte; la carga de formatos basados en pickle puede ejecutar código. El smoke test solo carga el archivo que acaba de crear él mismo. [M2]

No incluir credenciales, IP industriales sensibles, nombres de operarios, tokens de Jupyter ni certificados privados en notebooks, capturas, logs o repositorios. Una variable `.env` excluida de Git no cifra el secreto y no impide que una celda lo imprima.

### Inventario y SBOM

Una vez generado y validado el lock:

```bash
uv export --locked --no-default-groups --format cyclonedx1.5 --output-file reports/sbom-runtime.cdx.json
uv export --locked --format cyclonedx1.5 --output-file reports/sbom-academico.cdx.json
uv export --locked --no-default-groups --no-emit-project --format requirements.txt --output-file reports/requirements-runtime.txt
uv tree --locked
```

El primer inventario excluye herramientas académicas por defecto; el segundo refleja los grupos académicos seleccionados. Añadir los extras realmente instalados cuando corresponda. El SBOM exportado desde el lock es una base documental, **no un inventario completo del host, del firmware o de todas las bibliotecas nativas incorporadas en wheels**. [U9]

### Revisión de vulnerabilidades

```bash
uv sync --locked --group security
uv run --locked --group security pip-audit --format json --output reports/auditoria-entorno.json
uv run --locked --group security pip-audit --disable-pip --no-deps --require-hashes -r reports/requirements-runtime.txt --format json --output reports/auditoria-runtime.json
```

Revisar la salida y el código de retorno. No añadir `--fix` ni ignorar hallazgos automáticamente. Una revisión sin hallazgos conocidos no certifica seguridad y no sustituye revisar procedencia o licencias. La consulta utiliza servicios externos de avisos de vulnerabilidades: ejecutarla en el entorno de desarrollo autorizado, no improvisar salida a Internet desde OT. [S2]

Tras una auditoría, volver al perfil base con `uv sync --locked` cuando proceda. El lock puede conservar las definiciones de grupos no instalados.

Estas medidas ayudan a aportar evidencias de seguridad y trazabilidad, pero **no acreditan por sí solas cumplimiento de RGPD, CRA, normativa de máquinas o IEC 62443**. La evaluación de aplicabilidad depende del uso, los datos y la forma de suministro; se documentará antes de un piloto real. El propio reto pide razonar riesgos legales, éticos y de privacidad. [E1, p. 3]

## 15. Puertos y conectividad previstos

| Componente | Exposición propuesta |
|---|---|
| Instalación de uv/Python/paquetes | Salida HTTPS a fuentes autorizadas y resolución DNS funcional; no abrir puertos entrantes. |
| JupyterLab | `127.0.0.1:8888`, con token; los canales internos de kernel usan puertos locales adicionales. |
| Streamlit, si se habilita | `127.0.0.1:8501` para la demostración local. |
| NiFi, si se habilita | HTTPS accesible solo desde el ámbito previsto; en el host de desarrollo, publicar en loopback cuando sea viable. |
| MongoDB, si se habilita | Solo red interna del laboratorio; evitar publicar el servicio sin necesidad. |
| CNC o broker industrial | Endpoint, certificados, permisos y puertos definidos por su propietario. No abrir puertos genéricos «para probar». |

No enlazar Jupyter a `0.0.0.0`, desactivar autenticación o exponerlo a Internet para facilitar el trabajo en grupo. El flujo inicial es Git y un entorno local por integrante. [J4]

En redes con proxy o certificados institucionales, configurar el mecanismo de confianza adecuado según la versión de uv y el sistema. No solucionar un error de TLS mediante `--allow-insecure-host` ni desactivando verificaciones. [U7]

## 16. NiFi y MongoDB: extensión de laboratorio, no base obligatoria

Si finalmente forman parte de las prácticas, ejecutar **NiFi-Net y MongoDB dockerizados en la misma red de laboratorio**, sin instalar sus servidores en el host. Reutilizar Docker/Compose existente después de comprobar:

```bash
docker version
docker compose version
```

No modificar usuarios, permisos del socket o demonios de Docker a ciegas. El acceso al demonio puede implicar capacidades privilegiadas; no usar `chmod 666 /var/run/docker.sock` como solución. [S3]

Condiciones del perfil: imágenes con versión y digest revisados, volúmenes persistentes, credenciales no triviales fuera del repositorio, límites de memoria y CPU, y un procedimiento de parada/restauración. Desde un contenedor, `localhost` no representa otro servicio: utilizar el nombre del servicio en la red compartida. No ejecutar `docker system prune` sobre un host compartido para «hacer sitio» sin revisar lo que se eliminaría.

Para esta extensión reservaría, inicialmente y pendiente de medición, **3–4 GiB para NiFi y 1–2 GiB para MongoDB**, más el entorno Python, navegador y sistema. El heap Java no equivale al consumo total del proceso. Con 16 GiB habrá que controlar concurrencia; 24–32 GiB proporcionan más margen cuando todo deba convivir. Añadir **10–20 GiB de disco** para imágenes y repositorios de prueba según flujo y retención.

La guía de NiFi consultada exige Java 21 y distingue su runtime de procesadores Python del entorno externo del notebook. Sus procesadores Python tienen compatibilidad específica y se describen como una funcionalidad beta; **no reutilizar automáticamente CPython 3.13 del notebook dentro de ellos**. Mantener inicialmente el ML en el proyecto uv y conectar mediante archivos o una interfaz definida. Java iría dentro de la imagen de NiFi, no como requisito general del host. [N1]

No instalar MongoDB solo porque haya documentos JSON, ni NiFi para duplicar una ingesta ya resuelta. El criterio es la necesidad académica o funcional, no el número de servicios desplegados.

## 17. Preparación para una CNC real

El entorno académico **no debe instalarse directamente sobre el controlador CNC, el HMI de producción o un equipo de seguridad**. El notebook se utiliza para investigación y validación; el futuro recolector y la inferencia se desplegarían como componentes separados y supervisados.

Antes de elegir un conector faltan, como mínimo: fabricante y modelo de CNC/controlador, versión de firmware, interfaz autorizada, variables y unidades disponibles, licencia de acceso, frecuencia de adquisición admisible, punto de instalación y responsable técnico.

### Dependencias condicionales

OPC UA: habilitar `asyncua` únicamente cuando corresponda a la interfaz. MQTT: habilitar `paho-mqtt` cuando exista un broker y un esquema de mensajes definidos. Son bibliotecas de comunicación; **instalarlas no garantiza interoperabilidad ni permisos de solo lectura en una máquina concreta**. [O1][O2]

```bash
uv sync --locked --extra opcua
uv run --locked --extra opcua python -c "import asyncua; print('Importación OPC UA correcta')"
```

Para MQTT, sustituir `opcua` por `mqtt` y verificar `import paho.mqtt.client`. No interpretar una importación correcta como una prueba de conexión a fábrica.

No provisionar «todos los protocolos industriales». Un SDK de fabricante, controlador nativo, gateway o licencia comercial no puede estimarse responsablemente sin conocer la máquina.

### Requisitos previos del piloto propuestos

Recogida autorizada y limitada, permisos efectivos de lectura, certificados verificados, límites de consultas y reintentos, gestión de desconexión/datos obsoletos, almacenamiento acotado, reloj coherente y una prueba de retirada sin afectar al proceso. No incluir escrituras de consignas, offsets, programas, arranques o paradas.

La segmentación y el control de comunicaciones deberán diseñarse respetando disponibilidad y seguridad física de OT. No provocar averías o sobrecargas para conseguir ejemplos. La guía NIST SP 800-82 es una referencia de diseño, no una autorización para conectarse ni una certificación de conformidad. [O3]

Un perfil de ejecución sin herramientas de desarrollo puede partir de:

```bash
uv sync --locked --no-default-groups --extra opcua
```

Ese comando es **una preparación de dependencias**, no un despliegue industrial. También cambia el entorno seleccionado y retira Jupyter de ese perfil: probarlo en una copia o equipo separado, no sobre el entorno académico en uso. Antes del piloto se revisarán los paquetes realmente necesarios para inferencia, las dependencias de construcción, la distribución no editable, las actualizaciones, el rollback y el control de versiones del modelo.

No asumir que el modelo entrenado con datos públicos será válido en la CNC. La arquitectura puede reutilizarse; el modelo y sus umbrales necesitan evaluación específica.

## 18. PDF y otros formatos: no sobreinstalar

Para entregar `.ipynb` y una copia HTML, no instalar LaTeX, Pandoc ni un navegador headless adicional. Las rutas de conversión tienen requisitos diferentes. [J5][J6]

Si se exige también PDF automático y se elige WebPDF:

```bash
uv sync --locked --group pdf
uv run --locked --group pdf playwright install chromium
uv run --locked --group pdf jupyter nbconvert --to webpdf reports/CNC_Guard.ejecutado.ipynb --output CNC_Guard.pdf --output-dir reports
```

Reservar aproximadamente **0,5–1,5 GiB adicionales**, pendiente de plataforma. Playwright necesita su navegador compatible y puede requerir bibliotecas del sistema; uv no empaqueta todos esos requisitos. En Arch/Omarchy no ejecutar recetas Debian de instalación de bibliotecas indiscriminadamente. Este perfil solo se considera listo después de probarlo en el host de conversión. [J6]

La alternativa de conversión mediante LaTeX requiere su propia cadena de herramientas y puede ser considerablemente más pesada. No añadir ambas rutas para cubrir una necesidad que aún no existe. Una exportación a HTML con imágenes incrustadas también debe probarse offline: fórmulas o extensiones pueden depender de recursos externos.

## 19. Ensayo offline, recuperación y colaboración

La instalación inicial descarga intérprete y dependencias. Para ensayar una defensa sin red, preparar primero Python, perfil seleccionado, datos y cualquier recurso adicional. Después:

```bash
uv sync --locked --offline --managed-python
uv run --locked --offline jupyter nbconvert --to notebook --execute 00_verificacion_entorno.ipynb --output 00_verificacion_entorno.offline.ipynb --output-dir reports --ExecutePreprocessor.kernel_name=cnc-guard --ExecutePreprocessor.timeout=600
```

Repetir con el notebook final cuando exista. Si faltan artefactos en la caché, uv fallará: **`--offline` no fabrica las dependencias que no se han descargado**. Una caché preparada en Linux no debe darse por válida para Windows. Además, esta opción restringe el acceso de uv, no crea una barrera de red para todo el código que ejecute el notebook; probar también con la red desconectada o mediante controles del sistema. [U4][U7]

Para recuperar un entorno defectuoso: detener Jupyter, identificar su ruta exacta y conservar los datos/código. Recrear solo el entorno de este proyecto a partir del pin y lock; no borrar la carpeta global de Python/uv ni ejecutar limpiezas generales de otras aplicaciones. Registrar de nuevo el kernel y repetir las pruebas.

Usar una copia de trabajo local por integrante. No editar el mismo `.ipynb` simultáneamente mediante una carpeta sincronizada. Repartir funciones en módulos y acordar quién integra el notebook; los conflictos de JSON requieren revisión, no aceptar una versión entera sin mirar. Los worktrees que se utilicen tendrán entornos independientes, aunque compartan caché de uv.

## 20. Tiempo de preparación previsto y reparto

Estimación para 3–4 estudiantes, con conectividad normal y sin una incidencia importante del sistema operativo:

| Tarea | Responsabilidad propuesta | Esfuerzo estimado |
|---|---|---:|
| Preparar referencia: Python, manifiesto, lock y kernel | Una persona | 1–2 horas-persona |
| Replicar en otros equipos | Cada integrante, en paralelo | 20–40 minutos por equipo adicional |
| Ejecutar pruebas y comparar versiones | Una persona integra; todas verifican | 0,5–1 hora-persona adicional |
| Datos de muestra, procedencia y ensayo offline | Una persona | 0,5–1 hora-persona |
| Margen por incidencias | Equipo | 1 hora-persona |
| **Presupuesto conjunto** | **Equipo de 3–4** | **Aproximadamente 4–7 horas-persona** |

Objetivo de calendario: dejar la base operativa en **una sesión de 2–3 horas**, paralelizando la réplica. No es una garantía. No incluye aprender todo Jupyter, implementar el modelo, desarrollar el análisis ni conectar la CNC. NiFi/MongoDB, WebPDF o problemas de acceso a fábrica se presupuestan aparte.

La persona que inicializa no debe convertirse en la única capaz de reconstruir el entorno: todos los integrantes deben ejecutar el flujo de réplica, seleccionar el kernel y explicar qué versionan los tres archivos principales.

## 21. Incidencias previsibles y respuesta

| Síntoma | Comprobación y respuesta |
|---|---|
| `uv: command not found` | Reabrir terminal, comprobar PATH y método de instalación; no instalar con otro gestor encima sin revisar. |
| «Externally managed environment» | Se está intentando usar el Python global. Volver a `uv sync`/`uv run`, sin `--system`. |
| Falta `uv.lock` | Primera inicialización incompleta: una persona genera el lock; el resto obtiene ese archivo. |
| Lock desactualizado | Comparar `pyproject.toml` y `uv.lock`; no sustituir `--locked` por `--frozen` para ocultarlo. |
| Falta wheel / intenta compilar | Revisar Python estándar, 64 bits, arquitectura y rango. No instalar Rust/compiladores automáticamente. |
| `ModuleNotFoundError: cnc_guard` | Comprobar `uv sync`, instalación editable y kernel. No arreglarlo instalando el proyecto globalmente. |
| Otro módulo existe en terminal pero no en notebook | Comparar el intérprete del kernel; registrar/seleccionar el del proyecto. |
| Kernel apunta a una ruta desaparecida | Detener Jupyter y repetir el registro tras recrear el entorno. |
| Falta un extra después de sincronizar | Se cambió de perfil; usar el mismo `--extra` o `--group` en el flujo correspondiente. |
| Error Qt/Wayland | La base de Jupyter/Matplotlib no necesita Orange ni un backend Qt. No mezclar entornos; para pruebas sin GUI se usa `Agg`. |
| DLL de PyArrow en Windows | Verificar arquitectura y Visual C++ Redistributable oficial. [A1] |
| Se agota RAM | Reducir lote y paralelismo, detener servicios opcionales, revisar copias y no renderizar millones de filas. |
| Puerto 8888 ocupado | Detener el servidor propio anterior o elegir otro puerto local, sin ampliar la exposición de red. |
| Error TLS/proxy | Revisar CA/proxy institucional; no desactivar validación de certificados. |
| Error de permisos Docker | Revisar el modelo de acceso; no abrir el socket a todos los usuarios. [S3] |
| Notebook funciona solo después de ejecutar celdas sueltas | Reiniciar y ejecutar de principio a fin; eliminar estado oculto y dependencias de rutas personales. |
| Notebook ejecutado sin errores, pero sin análisis | La prueba de instalación no cubre el contenido académico; completar interpretación y conclusiones. |

## 22. Criterios de aceptación del setup

Antes de dar el entorno por preparado, debe poder demostrarse que:

- [ ] El manifiesto, lock y parche de Python están versionados y son comunes al equipo.
- [ ] No se ha modificado Python/Rust global ni el entorno de Orange.
- [ ] Cada integrante ha completado la réplica con `uv sync --locked`.
- [ ] El kernel seleccionado corresponde al entorno correcto.
- [ ] Pasan `verify_setup.py`, `pytest`, Ruff y la ejecución limpia del notebook de verificación.
- [ ] Se puede leer/escribir Parquet, consultarlo con DuckDB y guardar un gráfico.
- [ ] Se han probado los componentes supervisado y no supervisado a nivel de instalación.
- [ ] Los extras no utilizados permanecen sin instalar.
- [ ] La auditoría está revisada o su falta de ejecución se declara expresamente.
- [ ] Hay procedencia y huellas de los datos que utilizará la entrega.
- [ ] La demostración funciona sin instalaciones o descargas desde las celdas.
- [ ] La copia de entrega no contiene secretos, tokens ni datos no autorizados.
- [ ] Se distingue la verificación del setup de la validación del modelo y del futuro piloto industrial.

**Resultado previsto:** un proyecto Python pequeño, reconstruible y con un notebook ejecutable, evitando gastar el plazo académico en infraestructura innecesaria. El siguiente trabajo será desarrollar y evaluar el análisis del reto, no añadir servicios por defecto.

## 23. Fuentes y trazabilidad

Las decisiones de alcance, presupuestos, límites iniciales y reparto de trabajo son propuestas de ingeniería de este documento. Las siguientes son fuentes primarias consultadas para los comportamientos de las herramientas. Las versiones publicadas pueden evolucionar; el lock y las pruebas del equipo fijarán la referencia concreta.

**[E1] Enunciado aportado por el equipo:** `1Erronka_ikaslearen_txostena.docx.pdf`, Uni Eibar-Ermua, *CNC Guard: Mantentze Prediktiboa*, 13 páginas. Referencias utilizadas: objetivos técnicos y riesgos, pp. 3–7; aprendizaje supervisado/no supervisado, pp. 4–5; integración, almacenamiento y calidad/integridad, pp. 6–7. El requisito de entregar `.ipynb` procede de la indicación posterior del equipo.

**[U1] Astral — Integración de uv y Jupyter.** `https://docs.astral.sh/uv/guides/integration/jupyter/`

**[U2] Astral — Locking and syncing.** `https://docs.astral.sh/uv/concepts/projects/sync/`

**[U3] Astral — Configuración de proyectos y ruta del entorno.** `https://docs.astral.sh/uv/concepts/projects/config/`

**[U4] Astral — Caché.** `https://docs.astral.sh/uv/concepts/cache/`

**[U5] Astral — Instalación de uv.** `https://docs.astral.sh/uv/getting-started/installation/`

**[U6] Astral — Dependencias, grupos y extras.** `https://docs.astral.sh/uv/concepts/projects/dependencies/`

**[U7] Astral — Referencia de comandos.** `https://docs.astral.sh/uv/reference/cli/`

**[U8] Astral — Instalación y gestión de Python.** `https://docs.astral.sh/uv/guides/install-python/` y referencia `uv python install` de [U7].

**[U9] Astral — Exportación de lockfiles, incluido CycloneDX.** `https://docs.astral.sh/uv/concepts/projects/export/`

**[P1] Python — Estado de versiones.** `https://devguide.python.org/versions/`

**[S1] Arch Linux — Paquete uv.** `https://archlinux.org/packages/extra/x86_64/uv/`

**[A1] Apache Arrow — Instalación y compatibilidad de PyArrow.** `https://arrow.apache.org/docs/python/install.html`

**[J1] JupyterLab — Instalación.** `https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html`

**[J2] JupyterLab — Notebooks.** `https://jupyterlab.readthedocs.io/en/stable/user/notebook.html`

**[J3] IPython — Instalación de kernels.** `https://ipython.readthedocs.io/en/stable/install/kernel_install.html`

**[J4] Jupyter Server — Seguridad.** `https://jupyter-server.readthedocs.io/en/latest/operators/security.html`

**[J5] nbconvert — Uso por línea de comandos.** `https://nbconvert.readthedocs.io/en/latest/usage.html`

**[J6] nbconvert — Dependencias de instalación y conversión.** `https://nbconvert.readthedocs.io/en/latest/install.html`

**[M1] scikit-learn — Paralelismo y gestión de recursos.** `https://scikit-learn.org/stable/computing/parallelism.html`

**[M2] scikit-learn — Persistencia y riesgos de cargar modelos.** `https://scikit-learn.org/stable/model_persistence.html`

**[D1] DuckDB — Ajuste de rendimiento y memoria.** `https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads` y `https://duckdb.org/docs/current/guides/performance/oom`

**[S2] PyPA — pip-audit.** `https://github.com/pypa/pip-audit`

**[S3] Docker — Seguridad de Docker Engine.** `https://docs.docker.com/engine/security/`

**[S4] Git — Instalación en Windows.** `https://git-scm.com/install/windows`

**[N1] Apache NiFi — Guía de administración y requisitos.** `https://nifi.apache.org/nifi-docs/administration-guide.html`

**[O1] FreeOpcUa — opcua-asyncio / asyncua.** `https://github.com/FreeOpcUa/opcua-asyncio`

**[O2] Eclipse — Paho MQTT Python.** `https://eclipse.dev/paho/files/paho.mqtt.python/html/`

**[O3] NIST — SP 800-82 Rev. 3, seguridad OT.** `https://csrc.nist.gov/pubs/sp/800/82/r3/final`
