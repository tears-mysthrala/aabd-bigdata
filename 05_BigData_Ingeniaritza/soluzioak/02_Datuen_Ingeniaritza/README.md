# Faker: bezeroak eta salmentak

> **Datu sintetikoak dira.** Fitxategi hauetako izen, helbide elektroniko, hiri eta salmenta guztiak Faker-ek sortuak dira; ez dira benetako bezeroen datuak eta ez dira merkataritza-transakzioak.

Ariketa honen azalpen laburra, seed-ari eta CSV/JSON hautuei buruzko erantzunekin, [ariketen ebazpen osoan (12–15 atalak)](Ariketak_01_02_Datuen_Ingeniaritza_Ebazpena.md) dago. Sorgailu exekutagarria [generar_bezeroak.py](generar_bezeroak.py) da; [koadernoak](generar_bezeroak.ipynb) funtzio horiek erabiltzen ditu, kodea bikoiztu gabe.

## Exekutatzea

Python 3.13 edo berriagoa eta `uv` behar dira. Mendekotasunak modulu honetako ingurune birtualean instalatzen dira, ez sistema-Python globalean:

```sh
uv sync --locked
uv run python generar_bezeroak.py
```

`main()` exekutatzean CSV eta JSON fitxategiak berridazten dira `data/` karpetan. Bezeroentzako ariketak seed gabe sortzen dira, beraz izenak/atributuak exekuzioen artean alda daitezke; salmenten dataset-ak `seed=42` finkoa darabil, emaitza errepikatzeko. IDak dataset bakoitzean 1etik hasten dira.

## Emaitzak

| Fitxategia | Edukia |
|---|---|
| [bezeroak_100.csv](data/bezeroak_100.csv) | 100 bezero sintetiko, goiburuarekin |
| [bezeroak_10000.csv](data/bezeroak_10000.csv) | 10.000 bezero sintetiko, eskala alderatzeko |
| [bezeroak.json](data/bezeroak.json) | 100 bezeroen CSVtik sortutako `{"bezeroak": [...]}` objektua |
| [salmentak_10000.csv](data/salmentak_10000.csv) | Enuntziatuko zortzi zutabeekin, 10.000 salmenta sintetiko |
| [salmentak_10000.json](data/salmentak_10000.json) | Salmenta berak `{"salmentak": [...]}` objektuan |

Bezeroen zutabeak `id, izena, emaila, hiria, adina` dira; adina 18 eta 80 urte artean dago. Salmenten goiburu zehatza `id,data,bezeroa,hiria,produktua,kategoria,prezioa,unitateak` da. Kategoriak enuntziatuko lau balioetara mugatzen dira; prezioa 5–2.000 € da eta unitateak 1–10.

## Seed eta datu-formatua

Scriptak seed gabe sortutako bezeroen lehen bostak bi exekuziotan erakusten ditu; ondoren `seed=42` erabilita beste bi exekuzio egiten ditu eta emaitzak berdinak direla egiaztatzen du. Test automatikoetan seed finkoak fixture errepikagarriak ahalbidetzen ditu; gelako guztiek seed bera erabiltzeak emaitzak alderatzea errazten du. Faker-en bertsioa aldatzeak seed berarekin sortutako eduki zehatza alda dezake; horregatik mendekotasun-muga eta `uv.lock` daude.

JSON objektuak argi erakusten du erregistroen bildumaren izena eta objektu bakoitzeko eremu-izenak, baina array osoa memorian eraiki eta kargatzea garestia izan daiteke. Ariketako 10 milioi erregistroko kasuan ez litzateke array bakar osoa memorian sortu behar: erregistroak zatika idatzi/irakurri, JSONL fluxu-prozesamendua erabili edo analisi zutabeetarako Parquet eta Spark aukeratu. Errepositorioan ez da 10 milioiko fitxategirik sortu.

## Modulu-fitxategiak

- [Sorgailu eta balidazio kodea](generar_bezeroak.py)
- [Jupyter koadernoa](generar_bezeroak.ipynb)
- [Mendekotasunen deklarazioa](pyproject.toml)
- [Erreprodukziorako lock-fitxategia](uv.lock)
