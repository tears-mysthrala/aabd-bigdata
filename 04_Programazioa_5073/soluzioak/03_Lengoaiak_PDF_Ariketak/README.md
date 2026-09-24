# 03_Lengoaiak_PDF_Ariketak (5073 Modulua - 1. Gaia)

Karpeta honek `5073_1_Lengoaiak.pdf` apunte-dokumentuko ariketa praktiko guztiak biltzen ditu, modu antolatu, modular eta erreproduzigarrian.

## Edukia eta Fitxategiak
- **`5073_1_Lengoaiak_PDF_Ariketak.ipynb`**: Ariketa guztien ebazpena biltzen duen Jupyter koadernoa, gelaxken emaitza eta irteera guztiekin gordeta.
- **`5073_1_Lengoaiak_PDF_Ariketak.py`**: Koadernoaren baliokide zuzena den Python fitxategia, `# %%` gelaxka interaktiboekin (VS Code eta Spyder bateragarria).
- **`ariketa_1_1_nif.py`**: NIF/NAN balioztatzaile profesionala (Python script-aren anatomia osoa).
- **`ariketa_1_3_bihurgailua.py`**: JSON $\rightarrow$ YAML eta XML bihurtzaile automatikoa.
- **`katalogoa.json` & `katalogoa.yaml`**: Hipermerkatuaren produktuen fitxategiak (Ariketa 3.3).
- **`AGENTS.md`**: Agenteen jarduera eta segurtasun-arauak finkatzen dituen konfigurazioa (Ariketa 2.5).
- **`agur.py`**: Git-erako agur pertsonalizatua (Ariketa 4.2).
- **`PULL_REQUEST_TEMPLATE.md`**: Pull Request profesionaletarako txantiloia (Ariketa 4.4).
- **`.gitignore` & `.env.example`**: Sekretuak babesteko konfigurazioak (Ariketa 4.4).
- **`.venv/`**: `uv`-rekin sortutako ingurune birtual isolatua.
- **`requirements.txt`**: Proiektuko liburutegien bertsio zehatzak.

## Nola Exekutatu
```bash
# Ingurune birtuala aktibatu
source .venv/bin/activate

# Jupyter Lab edo VS Code bidez ireki
jupyter lab 5073_1_Lengoaiak_PDF_Ariketak.ipynb

# Edo Python fitxategi interaktiboa exekutatu
python 5073_1_Lengoaiak_PDF_Ariketak.py
```

## PDFko aldaera eta talde-ariketak

PDFko 1.1 NIF ariketaren sei ataleko paper-zirriborroa eta guard-aren azalpena,
2.4ko lankidearen ingurunea birsortzeko urratsak, eta 2.5eko prompt/erantzun ilustratibo,
egiaztapen eta isolamendu-erantzunak [ariketa_pdf_aldaerak.md](ariketa_pdf_aldaerak.md)
fitxategian daude. Taldekidearen benetako fitxategiak eta berrespena falta direla
adierazten du; ez du taldeko lanaren ebidentzia asmatu.

PDFko 2.5(a)rako 11 lerroko AGENTS.md adibidea
[ariketa-entregaren karpetan](exercise_2_5_entrega/AGENTS.md) dago. Esparru txikikoa
eta fikziozko ariketarako da; ez du karpeta honetako benetako
[AGENTS.md](AGENTS.md) gida ordezkatzen edo aldatzen.
