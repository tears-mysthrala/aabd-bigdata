# CNC Guard: instalación multiplataforma + erronka ebatzia

Plantilla reproducible para preparar un entorno académico de análisis de condición de CNC con Python, JupyterLab, pandas, scikit-learn, DuckDB y Parquet, **más la resolución de la Erronka 1**: `src/cnc_guard/` (fusión difusa Mamdani + IsolationForest) y `CNC_Guard.ipynb` (EDA, diseño fuzzy, anomalías, fusión por consenso y conclusiones sobre `cnc_10M.csv`). No es software listo para conectarse a una CNC real (datos sintéticos, sin conectores industriales).

La guía completa de criterios, recursos y límites está en [INSTALACION_CNC_GUARD_UV_JUPYTER.md](INSTALACION_CNC_GUARD_UV_JUPYTER.md). Este README contiene el procedimiento operativo para instalarlo en Windows, macOS y Linux.

El enunciado oficial incorporado al proyecto está en [docs/1Erronka_ikaslearen_txostena.pdf](docs/1Erronka_ikaslearen_txostena.pdf). Las normas para colaborar y comunicar vulnerabilidades están en [CONTRIBUTING.md](CONTRIBUTING.md) y [SECURITY.md](SECURITY.md).

## Qué se instala

El proyecto exige **CPython 3.13 de 64 bits** y `uv`. `uv` crea y administra el entorno virtual `.venv`, resuelve las versiones y ejecuta todos los comandos del proyecto.

Dependencias Python base: `numpy`, `pandas`, `scipy`, `scikit-learn`, `duckdb`, `pyarrow` y `joblib`.

Grupos instalados por defecto: JupyterLab, `ipykernel`, `nbconvert`, `nbformat`, Matplotlib, pytest, Ruff y psutil. No se necesita Anaconda, Conda, Node.js, CUDA, Docker, Spark ni un servidor de base de datos.

Extras opcionales:

| Extra | Uso |
| --- | --- |
| `dashboard` | Panel local con Streamlit. |
| `opcua` | Conector OPC UA con `asyncua`. |
| `mqtt` | Telemetría MQTT con `paho-mqtt`. |
| `mongo` | Lectura o escritura en MongoDB con `pymongo`. |
| `mat73` | Archivos MATLAB/HDF5 v7.3 con `h5py`. |
| `excel` | Archivos `.xlsx` con `openpyxl`. |

Instala un extra solo cuando el proyecto lo necesite. Las versiones y rangos oficiales están en [pyproject.toml](pyproject.toml).

## Requisitos comunes

- Sistema operativo de 64 bits actualizado.
- 8 GiB de RAM como mínimo; 16 GiB es más cómodo para Jupyter y datasets medianos.
- 20 GiB libres recomendados para el entorno, caché, notebooks y datos.
- Git, un navegador y permisos de escritura en la carpeta del proyecto.
- Conexión HTTPS durante la primera instalación.

No uses `sudo pip`, `pip install --user`, `uv pip install --system`, Conda ni instalaciones `%pip` dentro de notebooks. Las dependencias del proyecto se declaran en `pyproject.toml` y se instalan con `uv`.

## 1. Obtener el proyecto

Descomprime el paquete en una carpeta nueva o clónalo:

```bash
git clone <URL-DEL-REPOSITORIO> cnc_guard_setup
cd cnc_guard_setup
```

En PowerShell, el comando `cd` es el mismo. Evita rutas dentro de OneDrive, iCloud Drive o carpetas sincronizadas si el antivirus bloquea archivos temporales. No sobrescribas otro proyecto.

## 2. Instalar herramientas del sistema

Solo necesitas `uv` y Git. El navegador puede instalarse por el método habitual de tu sistema. Si ya tienes una herramienta, compruébala y no la reinstales. Elige **un solo método para uv** por máquina.

### Windows

En PowerShell:

```powershell
winget install --exact --id astral-sh.uv
winget install --exact --id Git.Git
```

Alternativas si no tienes WinGet:

```powershell
choco install uv git -y
# o, con Scoop:
scoop install uv git
```

Cierra y vuelve a abrir PowerShell. Comprueba:

```powershell
uv --version
git --version
```

Si PyArrow muestra un error de DLL, comprueba que usas Python y Windows de 64 bits e instala el [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist) oficial. No hace falta instalar Visual Studio completo.

### macOS

Con Homebrew:

```bash
brew update
brew install uv git
```

Con MacPorts:

```bash
sudo port selfupdate
sudo port install uv git
```

Si no usas ninguno, utiliza el instalador oficial de uv, revisándolo antes de ejecutarlo:

```bash
curl -LsSf https://astral.sh/uv/install.sh -o /tmp/cnc-guard-uv-install.sh
less /tmp/cnc-guard-uv-install.sh
sh /tmp/cnc-guard-uv-install.sh
```

Comprueba `uv --version` y `git --version`. Apple Silicon es compatible si las wheels disponibles para `arm64` superan las pruebas del proyecto; no copies la `.venv` desde otra arquitectura.

### Debian, Ubuntu, Linux Mint y derivados (APT)

```bash
sudo apt update
sudo apt install -y git curl ca-certificates
```

La opción más portable para uv es el instalador oficial, sin `sudo`:

```bash
curl -LsSf https://astral.sh/uv/install.sh -o /tmp/cnc-guard-uv-install.sh
less /tmp/cnc-guard-uv-install.sh
sh /tmp/cnc-guard-uv-install.sh
```

Si tu versión de la distribución ofrece un paquete `uv` mantenido y suficientemente reciente, también puedes usar `sudo apt install uv`; comprueba después que cumple el mínimo `uv >= 0.10` del proyecto. No mezcles ese paquete con el instalador oficial.

### Fedora, RHEL, Rocky, AlmaLinux y derivados (DNF/RPM)

```bash
sudo dnf install -y git curl ca-certificates
```

Si el repositorio habilitado ofrece uv actualizado:

```bash
sudo dnf install -y uv
```

Si no lo ofrece, usa el instalador oficial sin `sudo`, como en la sección APT. `RPM` es el formato de paquetes, no un sustituto de `dnf`: no instales un `.rpm` descargado de una URL desconocida con `rpm -Uvh`. Para una instalación transaccional basada en RPM también puedes usar `rpm-ostree install uv git` en Fedora Atomic/Silverblue si el paquete está disponible en los repositorios configurados; reinicia cuando el sistema lo solicite.

### Arch, EndeavourOS y derivados (pacman/YAY)

Con repositorios oficiales:

```bash
sudo pacman -Syu --needed uv git
```

Si `uv` no está en tus repositorios o necesitas un paquete del AUR, usa `yay` y revisa el PKGBUILD y la transacción:

```bash
yay -S --needed uv git
```

No ejecutes `pacman -Sy` de forma aislada, no instales `rustup` para este proyecto y no alteres el Python global de Arch. Omarchy también sigue estas precauciones.

### openSUSE (Zypper/RPM)

```bash
sudo zypper refresh
sudo zypper install git curl ca-certificates
```

Si existe un paquete `uv` adecuado en los repositorios configurados:

```bash
sudo zypper install uv
```

En caso contrario, instala uv con el instalador oficial. No mezcles repositorios RPM de Fedora/RHEL con openSUSE.

### NixOS y otros sistemas con Nix

Instalación temporal, útil para esta sesión:

```bash
nix shell nixpkgs#uv nixpkgs#git
```

Instalación persistente en el perfil del usuario:

```bash
nix profile install nixpkgs#uv nixpkgs#git
```

Con flakes/home-manager, añade `pkgs.uv` y `pkgs.git` a la configuración declarativa y reconstruye el perfil según tu flujo habitual. Nix puede proporcionar su propio Python, pero este proyecto debe seguir usando el Python gestionado por `uv`; no mezcles `pythonPackages` de Nix con la `.venv` del proyecto.

### Flatpak

Flatpak es apropiado para aplicaciones gráficas, no para el CLI de uv ni para un entorno Python integrado con el proyecto. Puedes instalar un navegador o VS Code con Flatpak, por ejemplo:

```bash
flatpak install flathub org.mozilla.firefox
# opcional:
flatpak install flathub com.visualstudio.code
```

Instala `uv` y Git mediante APT, DNF, pacman, Nix, Homebrew/MacPorts o el instalador oficial. No dependas de un `uv` dentro de un sandbox Flatpak para ejecutar `uv sync` en una carpeta del host.

### Otros gestores

En Alpine usa `apk add git curl ca-certificates` y el instalador oficial de uv; en Gentoo usa `emerge --ask dev-vcs/git net-misc/curl` y el mismo instalador; en Void usa `sudo xbps-install -S git curl ca-certificates`. En todos los casos, verifica que `uv --version` sea al menos `0.10` y que el sistema sea de 64 bits.

## 3. Inicialización del primer equipo

Una sola persona genera el pin de Python y el lock compartido. Ejecuta estos comandos en la raíz del proyecto. Funcionan en Bash, Zsh y PowerShell:

```bash
uv python install 3.13 --no-bin --no-registry
uv run --no-project --managed-python --python 3.13 python scripts/bootstrap.py --initialize
uv lock --managed-python
uv sync --locked --managed-python
```

El script crea las carpetas de trabajo y `.python-version`; `uv lock` genera `uv.lock`. Comparte ambos archivos y `docs/uv-version.txt` con el equipo. No vuelvas a ejecutar `--initialize` cuando ya exista `.python-version` o `uv.lock`.

Registra el kernel de Jupyter dentro del entorno:

```bash
uv run --locked python -m ipykernel install --sys-prefix --name cnc-guard --display-name "Python (CNC Guard / uv)"
uv run --locked jupyter kernelspec list
```

## 4. Réplica para el resto del equipo

Este flujo requiere una copia que ya contenga `.python-version` y `uv.lock`:

```bash
uv python install --no-bin --no-registry
uv sync --locked --managed-python
uv run --locked python scripts/bootstrap.py
uv run --locked python -m ipykernel install --sys-prefix --name cnc-guard --display-name "Python (CNC Guard / uv)"
```

No ejecutes `uv lock --upgrade`, `uv init` ni el bootstrap con `--initialize`. Cada sistema operativo y arquitectura debe probarse localmente; una instalación correcta en Linux no garantiza que Windows o macOS tengan las mismas wheels o permisos.

## 5. Verificar la instalación

Ejecuta todas las comprobaciones antes de empezar el notebook final:

```bash
uv run --locked python scripts/verify_setup.py
uv run --locked pytest -q
uv run --locked ruff check src scripts tests
uv run --locked ruff format --check src scripts tests
uv run --locked python -c "import nbformat; nbformat.validate(nbformat.read('00_verificacion_entorno.ipynb', as_version=4)); print('Notebook válido')"
uv run --locked jupyter nbconvert --to notebook --execute 00_verificacion_entorno.ipynb --output 00_verificacion_entorno.ejecutado.ipynb --output-dir reports --ExecutePreprocessor.kernel_name=cnc-guard --ExecutePreprocessor.timeout=600
```

El smoke test comprueba importaciones, Parquet, DuckDB, modelos de juguete, persistencia y gráficos. No valida datos industriales ni capacidad predictiva. El estado de referencia está en [docs/VALIDACION_PLANTILLA.md](docs/VALIDACION_PLANTILLA.md).

## 6. Uso diario

```bash
uv sync --locked --managed-python
uv run --locked pytest -q
uv run --locked jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Abre la URL con token que imprime Jupyter y selecciona **Python (CNC Guard / uv)**. Mantén Jupyter en `127.0.0.1`; no lo expongas a Internet ni a una red industrial. Detén el servidor con `Ctrl+C`.

Para activar un extra ya definido:

```bash
uv sync --locked --extra excel
uv run --locked --extra excel jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Para herramientas de seguridad:

```bash
uv sync --locked --group security
uv run --locked --group security pip-audit
```

## Integración continua en GitHub

El proyecto incluye workflows en `.github/workflows/`:

- `ci.yml` instala el lock y ejecuta smoke test, pytest, Ruff y el notebook en `ubuntu-24.04`, `windows-2025` y `macos-15`.
- `security.yml` ejecuta `pip-audit` y CodeQL para Python en Ubuntu, además de una ejecución semanal.

Las acciones están fijadas a commits completos para evitar cambios silenciosos de código en el CI, y Dependabot revisa semanalmente las acciones de GitHub. Los runners usados son explícitos y actuales; si GitHub retira una imagen, actualiza la matriz y vuelve a ejecutar el workflow antes de cambiar las acciones.

## Incidencias habituales

| Síntoma | Acción |
| --- | --- |
| `uv: command not found` | Reabre la terminal y comprueba el PATH; no instales otra copia antes de revisar `uv --version`. |
| `ModuleNotFoundError` en Jupyter | Selecciona **Python (CNC Guard / uv)** y vuelve a registrar el kernel con `--sys-prefix`. |
| `uv.lock` no coincide | Ejecuta `uv sync --locked` desde la raíz y no uses `--frozen` para ocultar el desajuste. |
| Error de wheel o arquitectura | Comprueba Python/OS de 64 bits y prueba el sistema localmente; no instales compiladores a ciegas. |
| `externally managed environment` | Estás usando el Python global. Vuelve a `uv sync` y `uv run`; no uses `--system`. |
| Kernel con una ruta desaparecida | Recrea el entorno, detén Jupyter y repite el registro del kernel. |

No compartas tokens de Jupyter, credenciales, certificados privados, datasets industriales ni rutas personales. No cargues modelos `pickle`/`joblib` de terceros no confiables.

## Estructura y alcance

Incluye `pyproject.toml`, `uv.lock`, scripts de bootstrap y verificación, configuración de recursos, pruebas, `00_verificacion_entorno.ipynb` y la resolución (`src/cnc_guard/fuzzy.py`, `src/cnc_guard/anomaly.py`, `CNC_Guard.ipynb` + `CNC_Guard.py`, generados por `generar_notebook.py`). El notebook auxiliar usa datos de juguete; `CNC_Guard.ipynb` usa `cnc_10M.csv` (generado con `04_Programazioa_5073/data/generar_cnc_10M.py`, no versionado). Métricas de referencia: holdout 200k → acc=0.9863, F1=0.1762 (`reports/metrikas.json`, no versionado). No se incluyen datasets, credenciales, conectores que actúen sobre máquinas ni servicios Docker desplegados.
