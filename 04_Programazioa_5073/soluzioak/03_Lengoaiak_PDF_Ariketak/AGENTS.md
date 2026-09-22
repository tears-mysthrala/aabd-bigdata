# AGENTS.md — Proiektuaren Garapen Arauak eta Agente Gida

## 1. Proiektuaren Xedea
Big Data eta Datu Zientziako (5073 modulua) ariketen ebazpen automatizatu, modular eta egiaztatua.

## 2. Ingurunea eta Tresnak
- Python bertsioa: >= 3.10 (gomendatua Python 3.13)
- Pakete kudeaketa: `uv` bidez kudeatutako `.venv` isolatua
- Formatu nagusiak: `.ipynb` (Jupyter Notebook interaktiboa) eta `.py` (modulu exekutagarriak)

## 3. Hizkuntza eta Estilo Arauak
- Kodearen aldagaiak, funtzioak eta iruzkinak: Euskara edo Ingelera teknikoa (lehentasuna euskaraz ikastaroarekin bat etortzeko).
- PEP 8 estilo gida zorrotz jarraitu: tipo-oharpenak (`type hints`), funtzio modularrak eta docstring zehatzak.

## 4. Segurtasun Murrizketak (GARDENKI DEBEKATUTA)
- DEBEKATUTA dago `eval()` edo `exec()` erabiltzea erabiltzailearen sarrerak ebaluatzeko.
- DEBEKATUTA dago `pickle.load()` fidagarriak ez diren iturrietako fitxategiekin erabiltzea (erabili JSON/YAML edo formatu seguruak).
- Kredentzialak, API gakoak eta tokenak EZIN dira inoiz kodean zuzenean idatzi (`.env` fitxategian gorde behar dira).
