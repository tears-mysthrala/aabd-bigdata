# PR #1 — feat/arg-izena → master (ariketa 4.4 simulazioa, remote gabe)

## Zer
- `agur.py`: `--izena` argudioa (`argparse`), `ValueError` hutsik bada; `input()` fallback mantentzen da.
- `test_agur.py`: 4 test (`pytest`, denak ✅).

## Zergatik (4.1: Git enpresan, 3 arrazoi)
1. Histori trazatua (conventional commits).
2. Feature branching: `master` egonkor, arriskua `feat/*`-n.
3. Review atea: merge `--no-ff` + testak berde.

## Nola mergatu (lokala, remote gabe)
```bash
git checkout -b feat/arg-izena
pytest test_agur.py -v
git checkout master
git merge --no-ff feat/arg-izena -m "merge: PR #1 ..."
```

## Txekeoak
- [x] `pytest test_agur.py` 4/4 ✅
- [x] `python agur.py --izena Ane` → `Kaixo, Ane!`
- [x] Conventional commits + merge `--no-ff`
