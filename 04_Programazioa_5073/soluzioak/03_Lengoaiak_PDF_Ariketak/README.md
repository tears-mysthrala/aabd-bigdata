# 03_Lengoaiak_PDF_Ariketak (5073 Modulua - 1. Gaia)

Karpeta honek `5073_1_Lengoaiak.pdf` apunte-dokumentuko ariketa praktiko guztiak biltzen ditu, modu antolatu, modular eta erreproduzigarrian.

## Edukia eta Fitxategiak
- **`5073_1_Lengoaiak_PDF_Ariketak.ipynb`**: Ebazpenak eta irteera historikoak dituen Jupyter koadernoa; talde/GUI ariketen entrega osoa ez du frogatzen.
- **`5073_1_Lengoaiak_PDF_Ariketak.py`**: Koadernoaren baliokide zuzena den Python fitxategia, `# %%` gelaxka interaktiboekin (VS Code eta Spyder bateragarria).
- **`ariketa_1_1_nif.py`**: NIF/NAN balioztatzaile profesionala (Python script-aren anatomia osoa).
- **`ariketa_1_3_bihurgailua.py`**: JSON $\rightarrow$ YAML eta XML bihurtzaile automatikoa.
- **`katalogoa.json` & `katalogoa.yaml`**: Hipermerkatuaren produktuen fitxategiak (Ariketa 3.3).
- **`AGENTS.md`**: Agenteen jarduera eta segurtasun-arauak finkatzen dituen konfigurazioa (Ariketa 2.5).
- **`agur.py`**: Git-erako agur pertsonalizatua (Ariketa 4.2).
- **`PULL_REQUEST_TEMPLATE.md`**: Pull Request profesionaletarako txantiloia (Ariketa 4.4).
- **`.gitignore` & `.env.example`**: Sekretuak babesteko konfigurazioak (Ariketa 4.4).
- **`.venv/`**: `uv`-rekin sortutako ingurune birtual isolatua.
- **`requirements.txt`**: Proiektuko liburutegien gutxieneko bertsioak.

## Preparación, ejecución y comprobación

Desde la raíz del repositorio, con Python 3 y `uv` disponibles:

```bash
cd 04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python 5073_1_Lengoaiak_PDF_Ariketak.py
```

La `.venv` no se distribuye con Git. `requirements.txt` declara rangos mínimos,
no versiones exactas bloqueadas. Para Jupyter, abre el notebook con el intérprete
de ese entorno y esta carpeta como directorio de trabajo. El script escribe
`katalogoa.json` y `katalogoa.yaml` en la carpeta actual: usa una copia de
prácticas si ya tienes modificaciones propias.

El programa verifica ejemplos de NIF y el roundtrip JSON/YAML; imprime propuestas
de entorno y Git. **No ejecuta toda la secuencia de comandos mostrada en esas
propuestas ni crea una PR.** Comprueba además que existen `.gitignore`,
`.env.example` y la plantilla PR; su existencia no prueba que un secreto esté
correctamente ignorado. [Registros locales](ingurune_isolatua_2026-09-25.md)
y [comprobación aislada de gitignore](gitignore_isolatua_2026-09-25.md).

Los ejemplos de NIF prueban formato/letra de control, no identidad de personas.
Distingue `json.loads` (cadena) de `json.load` (archivo) y comprueba que YAML y
JSON recuperan la misma estructura. Las respuestas escritas y las variantes
requieren leer y razonar; ejecutar el script no completa el trabajo en equipo.

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
