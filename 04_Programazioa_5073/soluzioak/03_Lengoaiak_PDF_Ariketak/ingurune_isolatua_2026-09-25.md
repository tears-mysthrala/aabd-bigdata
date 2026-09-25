# 2.2 eta 2.3: Python ingurune isolatuko exekuzioa

2026-09-25ean `/tmp/aabd-venv-5073-20260925` venv garbia sortu da
`uv venv --seed --python 3.13` erabilita. `pip`-ekin paketeak **banaka**
instalatu dira. `pip list --format=freeze`-ko pakete kopuruak:

| Urratsa | Pakete kopurua | Gehitu direnak |
|---|---:|---|
| Venv berria | 1 | `pip` |
| `pip install requests` | 6 | `requests`, `urllib3`, `idna`, `charset-normalizer`, `certifi` |
| `pip install pandas` | 10 | `pandas`, `numpy`, `python-dateutil`, `six` |
| `pip install scikit-learn` | 16 | `scikit-learn`, `scipy`, `joblib`, `threadpoolctl`, `narwhals`, `cloudpickle` |

Venv-eko `python -c 'import numpy; print(numpy.__version__)'` → `2.5.3`.
Sistemako `python3.13 -c 'import numpy'` → exit code 1 eta
`ModuleNotFoundError: No module named 'numpy'`. Sistemako beste Python
bertsio batean NumPy egon daiteke; ondorioak interprete horri dagozkio.

Kopuru hauek ez dira pakete horien ezaugarri finkoak. Bertsio, plataforma,
aurretik instalatutako pakete eta `pip` bertsioaren araberakoak dira.
Antigravity GUI-ko urratsak ez dira hemen egin; terminaleko isolamendu bera
erakutsi da, baina IDEaren pantaila/konfigurazioa giza egiaztapenaren zain da.

## 2.4 koadernoko aldaera: requirements bidez birsortzea

Beste venv garbi bat sortu da `/tmp/aabd-req-5073-20260925` bidean.
Karpeta honetako `requirements.txt` erabiliz 52 pakete instalatu dira
`uv pip install -r` komandoarekin, exit code 0. Venv berriko Pythonarekin
`ariketa_1_3_bihurgailua.py` exekutatu da, exit code 0: bost bezeroen JSON
YAML eta XML formatuetara bihurtu ditu. Horrek emandako scriptaren
menpekotasunen berrinstalazioa erakusten du; ez du 2.4 PDFko taldekidearen
benetako `main.py` eta CSV fitxategien eskualdaketa ordezkatzen.
