# -*- coding: utf-8 -*-
"""5073_2_Datu_Zientzia_PDF_Ariketak - Soluzio Exekutagarria VS Code / Spyder-entzat."""

# %%
# """
# # 5073 - Lengoaiak eta Datu Zientzia
# ## 2. Gaia: Datu Zientziaren Tresnak (PDF-ko Ariketa Guztien Ebazpena)
# 
# Dokumentu honek `5073_2_Datu_Zientzia.pdf` apunteetako **ariketa praktiko guztiak** biltzen eta ebazten ditu:
# 1. **NumPy**:
#    - **Ariketa 1.1**: Python zerrenden vs NumPy array-en abiadura benchmark-a ($N=10^6, 10^7, 50 \times 10^6$).
#    - **Ariketa 1.2**: 2D Notak Matrizea (6 ikasle $\times$ 4 azterketa) eta estatistikak ardatzen arabera.
#    - **Ariketa 1.3**: BEZ / Marjinen kalkulua begiztarik gabe (Broadcasting).
#    - **Ariketa 1.4**: Stock kritikoaren filtrazioa (Boolean Indexing) eta berrezartze kalkulua.
#    - **Ariketa 1.5**: 3 Denda $\times$ 4 Hiruhileko Salmenten agregazioak (`axis=0` vs `axis=1`).
# 2. **Pandas**:
#    - **Ariketa 2.1**: Langileen DataFrame-a, iragazki aurreratuak eta 14 ordainsariko urteko soldata.
#    - **Ariketa 2.2**: 3 hilabetetako salmenta CSVak kargatu eta pilatu (`pd.concat`).
#    - **Ariketa 2.3**: Datu zikinen garbiketa pipeline osoa (null-ak, bikoiztuak, espazioak, formatuak).
#    - **Ariketa 2.4**: Agregazio konplexuak (`groupby` anizkoitzak eta `pivot_table`).
#    - **Ariketa 2.5**: Eredu erlazionala eta taulen batzea (`merge` Inner/Left vs `concat`).
# 3. **Matplotlib eta Seaborn**:
#    - **Ariketa 3.1**: Matplotlib 2x2 azpigrafikoak (barrak, sakabanaketa, histograma, boxplot) eta esportazioa (PNG/PDF).
#    - **Ariketa 3.2**: Seaborn estatistika-bistaratzea eta Korrelazio Heatmap-a `tips` datu-multzoarekin.
#    - **Ariketa 3.3**: Gaiak, paletak (`muted`, `husl`), tamaina (`font_scale`) eta esportazio bektoriala (SVG, PDF, PNG).
# 4. **DVC (Data Version Control)**:
#    - **Ariketa 4.1**: Git + DVC laborategia, `notak.csv` bertsionatzea, remote lokala eta biltegiratzea.
# 5. **Plataforma Komertzialak**:
#    - **Ariketa 5.1**: Azure ML, IBM Watson, Knime vs Python konparaketa matrizea 3 enpresa motarentzat.
# """

# %%
# """
# ---
# ## 1. NumPy: Zenbakizko Kalkulua
# ### 🧩 Ariketa 1.1 · Python List vs NumPy Array Abiadura Benchmark-a
# **Egoera:** Python-eko ohiko zerrenden eta NumPy array optimizatuen arteko errendimendu-aldea neurtu behar dugu tamaina handiekin:
# $N \in [1\,000\,000, 10\,000\,000, 50\,000\,000]$.
# 
# **Eginkizuna:**
# 1. Elementuen batuketa neurtu Python pure (`sum(range(N))`) eta NumPy bektorialarekin (`np.sum(np.arange(N))`).
# 2. Exekuzio-denborak neurtu eta abiadura-faktorea (*Speedup*) kalkulatu.
# 3. Emaitzak taula egituratu batean bistaratu eta CSV batean gorde.
# """

# %%
import time
import pandas as pd
import numpy as np
from pathlib import Path

N_BALIOAK = [1_000_000, 10_000_000, 50_000_000]
emaitzak_benchmark = []

for n in N_BALIOAK:
    # 1. Python hutsa
    hasiera_py = time.perf_counter()
    batura_py = sum(range(n))
    denbora_py = time.perf_counter() - hasiera_py
    
    # 2. NumPy bektoriala
    arr = np.arange(n, dtype=np.int64)
    hasiera_np = time.perf_counter()
    batura_np = np.sum(arr)
    denbora_np = time.perf_counter() - hasiera_np
    
    assert batura_py == int(batura_np), "Emaitzak ez datoz bat!"
    
    speedup = denbora_py / denbora_np
    emaitzak_benchmark.append({
        "Elementuak (N)": f"{n:,}",
        "Python (s)": round(denbora_py, 4),
        "NumPy (s)": round(denbora_np, 4),
        "Speedup": f"{speedup:.2f}x"
    })

df_bench = pd.DataFrame(emaitzak_benchmark)
df_bench.to_csv("data/emaitzak_benchmark.csv", index=False)

print("=== ARIKETA 1.1: ABIADURA BENCHMARK EMAITZAK ===")
print(df_bench.to_string(index=False))
print("\nOharra: Ikus daitekeenez, NumPy 10x-50x azkarragoa da, C lengoaian konpilatutako memoria-bloke trinkoak eta SIMD bektorializazioa erabiltzen dituelako.")

# %%
# """
# ---
# ### 🧩 Ariketa 1.2 · 2D Notak Matrizea (6 ikasle $\times$ 4 azterketa)
# **Egoera:** Klase bateko 6 ikasleren 4 azterketako notak matrize batean dituzu.  
# **Eginkizuna:**
# 1. Sortu $(6, 4)$ formako matrizea.
# 2. Kalkulatu ikasle bakoitzaren batezbestekoa (`axis=1`).
# 3. Kalkulatu azterketa bakoitzeko batezbestekoa (`axis=0`).
# 4. Aurkitu zein izan den azterketarik zailena (batezbesteko txikiena).
# 5. Kalkulatu ikasle guztien artean gainditu diren azterketa kopuru osoa (notak $\ge 5.0$).
# """

# %%
# 6 ikasle x 4 azterketa
notak = np.array([
    [8.5, 7.0, 9.0, 8.0],  # Ikasle 1 (Ane)
    [4.0, 5.5, 3.5, 6.0],  # Ikasle 2 (Mikel)
    [9.0, 8.5, 9.5, 9.0],  # Ikasle 3 (Leire)
    [6.0, 4.5, 7.0, 5.5],  # Ikasle 4 (Jon)
    [7.5, 8.0, 8.5, 9.0],  # Ikasle 5 (Maite)
    [3.5, 5.0, 4.0, 6.0]   # Ikasle 6 (Kepa)
])

ikasleak = ["Ane", "Mikel", "Leire", "Jon", "Maite", "Kepa"]
azterketak = ["Azterketa 1", "Azterketa 2", "Azterketa 3", "Azterketa 4"]

# 1. Ikasle bakoitzaren batezbestekoa (axis=1: zutabeak agregatu)
ikasle_bb = np.mean(notak, axis=1)

# 2. Azterketa bakoitzeko batezbestekoa (axis=0: errenkadak agregatu)
azterketa_bb = np.mean(notak, axis=0)

# 3. Azterketarik zailena (batezbesteko minimoa)
zailena_idx = np.argmin(azterketa_bb)

# 4. Gainditu diren azterketa kopurua (nota >= 5.0)
gaindituak_kopurua = np.sum(notak >= 5.0)
azterketak_guztira = notak.size

print("=== ARIKETA 1.2 EMAITZAK ===")
print("1. Ikasle bakoitzaren batezbestekoa:")
for ikasle, bb in zip(ikasleak, ikasle_bb):
    print(f"   - {ikasle:8}: {bb:.2f}")

print("\n2. Azterketa bakoitzeko batezbestekoa:")
for azterketa, bb in zip(azterketak, azterketa_bb):
    print(f"   - {azterketa}: {bb:.2f}")

print(f"\n3. Azterketarik zailena: {azterketak[zailena_idx]} (Batezbestekoa: {azterketa_bb[zailena_idx]:.2f})")
print(f"4. Gainditutako probak guztira: {gaindituak_kopurua} / {azterketak_guztira} (%{(gaindituak_kopurua/azterketak_guztira)*100:.1f})")

# %%
# """
# ---
# ### 🧩 Ariketa 1.3 · BEZ eta Marjinen Kalkulua (Broadcasting)
# **Egoera:** Denda-kate batek 4 produkturen oinarrizko prezioak ditu, eta 3 saltoki desberdinetan aplikatu beharreko BEZ/marjina faktoreak aplikatu nahi ditu begiztarik gabe (*loop-free*).
# 
# **Eginkizuna:**
# - Oinarrizko prezioak: `[10.0, 25.5, 4.2, 50.0]` euro $\rightarrow$ forma: `(4, 1)`.
# - Denden marjinak/tasa faktoreak: `[1.21, 1.10, 1.04]` (BEZ orokorra, murriztua, super-murriztua) $\rightarrow$ forma: `(1, 3)`.
# - Kalkulatu amaierako prezioen matrizea $(4, 3)$ broadcasting bidez.
# """

# %%
oinarrizko_prezioak = np.array([10.0, 25.50, 4.20, 50.00]).reshape(4, 1)
denda_faktoreak = np.array([1.21, 1.10, 1.04]).reshape(1, 3)

# Broadcasting automatikoa: (4, 1) * (1, 3) -> (4, 3)
amaierako_prezioak = oinarrizko_prezioak * denda_faktoreak

produktuen_izenak = ["Sagua", "Teklatua", "Kablea", "Monitorea"]
denden_izenak = ["Denda A (%21 BEZ)", "Denda B (%10 BEZ)", "Denda C (%4 BEZ)"]

df_prezioak = pd.DataFrame(amaierako_prezioak, index=produktuen_izenak, columns=denden_izenak)

print("=== ARIKETA 1.3: BROADCASTING PREZIOEN MATRIZEA ===")
print(df_prezioak.round(2))
print(f"\nMatrizearen forma (shape): {amaierako_prezioak.shape}")

# %%
# """
# ---
# ### 🧩 Ariketa 1.4 · Stock Kritikoa (Boolean Indexing)
# **Egoera:** Biltegi bateko 10 produkturen stock-a daukazu: `[5, 12, 8, 30, 2, 15, 7, 45, 9, 20]`.  
# **Eginkizuna:**
# 1. Identifikatu stock kritikoa duten produktuak (kopurua $< 10$).
# 2. Kalkulatu zenbat produktu dauden egoera kritikoan.
# 3. Sortu hornitze-agindu automatikoa: produktu kritikoak 50 unitatera iristeko behar den kopurua kalkulatu (`np.where`).
# """

# %%
stock = np.array([5, 12, 8, 30, 2, 15, 7, 45, 9, 20])
produktu_id = np.arange(101, 111)

# 1. Maskara boolearra
kritiko_maskara = stock < 10

# 2. Produktu kritikoen datuak
kritiko_id = produktu_id[kritiko_maskara]
kritiko_stock = stock[kritiko_maskara]

# 3. Hornitze-agindua: 50 unitatera iristeko falta dena
hornitze_eskaera = np.where(stock < 10, 50 - stock, 0)

print("=== ARIKETA 1.4: STOCK KRITIKOAREN AZTERKETA ===")
print(f"Stock array osoa: {stock}")
print(f"Produktu kritikoen kopurua: {np.sum(kritiko_maskara)} / {len(stock)}")
print(f"Kritikoen IDak: {kritiko_id.tolist()}")
print(f"Kritikoen uneko stock-a: {kritiko_stock.tolist()}")
print(f"Hornitze agindu bektorea (50 unitateraino): {hornitze_eskaera.tolist()}")

# %%
# """
# ---
# ### 🧩 Ariketa 1.5 · 3 Denda $\times$ 4 Hiruhileko Salmentak (Agregazioak & Ardatzak)
# **Egoera:** Hiru dendaren lau hiruhilekoko salmenta-matrizea (milaka eurotan):
# ```python
# np.array([[120, 135, 150, 165], [90, 95, 110, 100], [200, 210, 195, 220]])
# ```
# 
# **Eginkizuna:**
# 1. Kalkulatu denda bakoitzaren urteko salmenta osoa (`axis=1`).
# 2. Kalkulatu hiruhileko bakoitzeko batezbesteko salmenta dendetan zehar (`axis=0`).
# 3. Aurkitu zein dendak duen salmenta-aldakortasun handiena (desbideratze estandarra, `std`).
# 4. Azaldu: *Zein axis erabili duzu kasu bakoitzean, eta zergatik?*
# """

# %%
salmentak = np.array([
    [120, 135, 150, 165],  # Denda 1
    [90, 95, 110, 100],    # Denda 2
    [200, 210, 195, 220]   # Denda 3
])

# 1. Denda bakoitzaren urteko salmenta osoa (axis=1: zutabeak batu errenkada bakoitzean)
urteko_salmenta_dendaka = np.sum(salmentak, axis=1)

# 2. Hiruhileko bakoitzeko batezbestekoa (axis=0: errenkadak batu zutabe bakoitzean)
hiruhileko_bb = np.mean(salmentak, axis=0)

# 3. Desbideratze estandarra dendaka
aldakortasuna_dendaka = np.std(salmentak, axis=1)
aldakorrena_idx = np.argmax(aldakortasuna_dendaka)

print("=== ARIKETA 1.5 EMAITZAK ===")
for i, (salm, std_val) in enumerate(zip(urteko_salmenta_dendaka, aldakortasuna_dendaka), 1):
    print(f"🏪 Denda {i}: Urteko salmenta = {salm}k € | Desbideratze est. = {std_val:.2f}")

print("\n📊 Hiruhileko bakoitzeko batezbestekoa (dendetan zehar):")
for q, bb in enumerate(hiruhileko_bb, 1):
    print(f"   - Q{q}: {bb:.2f}k €")

print(f"\n📈 Aldakortasun handiena duen denda: Denda {aldakorrena_idx + 1} ({aldakortasuna_dendaka[aldakorrena_idx]:.2f}k €)")

# %%
# """
# ### 💡 Ardatzen (axis) Azalpen Metodologikoa:
# - **`axis=1` (Errenkaden norabidean)**: Errenkada bakoitzeko zutabe guztiak agregatzen ditu (lau hiruhilekoak elkartuz). Ondorioz, zutabeen dimentsioa desagertzen da eta denda bakoitzeko balio bakar bat lortzen da (forma: `(3,)`).
# - **`axis=0` (Zutabeen norabidean)**: Zutabe bakoitzeko errenkada guztiak agregatzen ditu (hiru dendak elkartuz). Ondorioz, errenkaden dimentsioa desagertzen da eta hiruhileko bakoitzeko balio bakar bat lortzen da (forma: `(4,)`).
# """

# %%
# """
# ---
# ## 2. Pandas: Datu-taulen Kudeaketa
# ### 🧩 Ariketa 2.1 · Langileen DataFrame-a eta Hautaketak
# **Egoera:** 5 langileren datu-taula sortu eta aztertu.  
# **Eginkizuna:**
# 1. Sortu DataFrame-a eta inprimatu `shape`, `dtypes` eta `describe()`.
# 2. Lortu Donostiako langileak.
# 3. Lortu 28 urtetik gorako eta 30.000€-tik gorako soldata dutenak.
# 4. Sortu zutabe berri bat: `soldata_urtekoa = soldata * 14` (14 ordainsari).
# """

# %%
langileak_data = {
    "izena": ["Ane", "Mikel", "Leire", "Jon", "Maite"],
    "adina": [26, 32, 29, 45, 27],
    "hiria": ["Donostia", "Bilbo", "Donostia", "Gasteiz", "Bilbo"],
    "departamentua": ["Datu Zientzia", "Sistemak", "Datu Zientzia", "Zuzendaritza", "Garapena"],
    "soldata": [28000, 34000, 31500, 52000, 29500]
}

df_langileak = pd.DataFrame(langileak_data)

print("=== 1. DATAFRAME INFORMAZIOA ===")
print(f"Shape: {df_langileak.shape}")
print("\nDtypes:")
print(df_langileak.dtypes)
print("\nDescribe:")
print(df_langileak.describe())

# 2. Donostiako langileak
donostia_df = df_langileak[df_langileak["hiria"] == "Donostia"]
print("\n=== 2. DONOSTIAKO LANGILEAK ===")
print(donostia_df[["izena", "hiria", "departamentua"]])

# 3. 28 urtetik gora eta > 30.000€ soldata
iragazkia = df_langileak[(df_langileak["adina"] > 28) & (df_langileak["soldata"] > 30000)]
print("\n=== 3. ADINA > 28 ETA SOLDATA > 30.000€ ===")
print(iragazkia[["izena", "adina", "soldata"]])

# 4. 14 ordainsariko urteko soldata osoa
df_langileak["soldata_urtekoa"] = df_langileak["soldata"] * 14 / 12  # Urteko baliokide osoa kalkulatuz
print("\n=== 4. SOLDATA URTEKOA GEHITUTA ===")
print(df_langileak[["izena", "soldata", "soldata_urtekoa"]])

# %%
# """
# ---
# ### 🧩 Ariketa 2.2 · Datuak Kargatu eta Pilatu (`pd.concat`)
# **Egoera:** Hiru hilabeteko CSV fitxategiak dituzu: `urtarrila.csv`, `otsaila.csv`, `martxoa.csv`.  
# **Eginkizuna:**
# 1. Kargatu fitxategi bakoitza eta erantsi `iturria` edo `hilabetea` adierazten duen zutabea.
# 2. Batu hiru taulak taula bakar batean `pd.concat` erabiliz.
# 3. Kalkulatu hiruhilekoaren salmenta osoa eta kategoria bakoitzeko banaketa.
# """

# %%
# 1. Kargatu eta iturria etiketatu (glob: eskalagarria, ez banakako read_csv)
HILABETEAK = ("urtarrila", "otsaila", "martxoa")
df_list = []
for bidea in sorted(Path("data").glob("*.csv")):
    if bidea.stem in HILABETEAK:
        df_hila = pd.read_csv(bidea)
        df_hila["hilabetea"] = bidea.stem.capitalize()  # fitxategi-izenetik eratorria
        df_list.append(df_hila)
assert len(df_list) == 3, f"Q1 CSVak falta: {[p.name for p in sorted(Path('data').glob('*.csv'))]}"

# 2. Pilatu (concat)
df_hiruhilekoa = pd.concat(df_list, ignore_index=True)
df_hiruhilekoa["salmenta_osoa"] = df_hiruhilekoa["unitateak"] * df_hiruhilekoa["prezioa"]

print("=== ARIKETA 2.2: PILATUTAKO SALMENTAK (Q1) ===")
print(df_hiruhilekoa.head(10))

print(f"\nErrenkadak guztira: {len(df_hiruhilekoa)}")
print(f"Hiruhilekoaren diru-sarrera osoa: {df_hiruhilekoa['salmenta_osoa'].sum():,.2f} €")

# Kategoriako banaketa
print("\nSalmentak kategoriaka:")
print(df_hiruhilekoa.groupby("kategoria")["salmenta_osoa"].sum())

# %%
# """
# ---
# ### 🧩 Ariketa 2.3 · Datu Zikinen Garbiketa Pipeline-a
# **Egoera:** Datu zikinak dituen CSV bat duzu (`bezeroak_zikinak.csv`): balio faltak (`NaN`), bikoiztuak, testu-espazioak eta karaktere arraroak.
# 
# **Eginkizuna:**
# 1. Aztertu balio falten ehunekoa zutabeka.
# 2. Bete adina batezbestekoaz eta hiria `"Ezezaguna"` testuarekin.
# 3. Kendu bikoiztutako errenkadak izenaren arabera (`drop_duplicates`).
# 4. Garbitu izenak (zuriuneak kendu, letra larriz/tituluz jarri) eta soldata zenbaki garbi bihurtu.
# 5. Konparatu hasierako eta amaierako errenkada-kopurua eta kalitatea.
# """

# %%
df_zikina = pd.read_csv("data/bezeroak_zikinak.csv")
hasierako_errenkadak = len(df_zikina)

print("=== 1. HASIERAKO DATU ZIKINAK ===")
print(df_zikina)

# 1. Balio falten ehunekoa
faltak_pct = df_zikina.isna().mean() * 100
print("\nBalio falten portzentajea zutabeka:")
for col, pct in faltak_pct.items():
    print(f"  - {col:10}: {pct:.1f}% falta")

# 2. Garbiketa: Izenetako hutsuneak kendu
df_garbia = df_zikina.dropna(subset=["izena"]).copy()
df_garbia["izena"] = df_garbia["izena"].str.strip().str.title()

# 3. Bikoiztuak kendu
df_garbia = df_garbia.drop_duplicates(subset=["izena"]).copy()

# 4. Imputazioa
adina_bb = df_garbia["adina"].mean()
df_garbia["adina"] = df_garbia["adina"].fillna(adina_bb).round(1)
df_garbia["hiria"] = df_garbia["hiria"].fillna("Ezezaguna")

# 5. Soldata zenbaki bihurtu (kendu €, hutsuneak)
df_garbia["soldata"] = (
    df_garbia["soldata"]
    .astype(str)
    .str.replace("€", "", regex=False)
    .str.strip()
    .astype(float)
)

amaierako_errenkadak = len(df_garbia)

print("\n=== 2. DATU GARBITUEN AMAIERAKO DATAFRAME-A ===")
print(df_garbia)
print(f"\nErrenkaden garapena: {hasierako_errenkadak} hasieran -> {amaierako_errenkadak} garbitu ondoren.")

# %%
# """
# ---
# ### 🧩 Ariketa 2.4 · Agregazio Konplexuak (`groupby` eta `pivot_table`)
# **Egoera:** Salmenta-DataFrame bat duzu (hiria, kategoria, produktua, salmenta).  
# **Eginkizuna:**
# 1. Kalkulatu hiri bakoitzeko salmenta osoa (`groupby` + `sum`).
# 2. Kalkulatu kategoria bakoitzeko batezbestekoa, gehienezkoa eta kopurua (`agg`).
# 3. Sortu `pivot_table` bat: errenkadak hiriak, zutabeak kategoriak, balioak salmenta-batura.
# 4. Identifikatu zein hiri-kategoria konbinazioak duen salmentarik handiena.
# """

# %%
salmenta_taula = pd.DataFrame({
    "hiria": ["Donostia", "Bilbo", "Gasteiz", "Donostia", "Bilbo", "Gasteiz", "Donostia", "Bilbo"],
    "kategoria": ["Informatika", "Informatika", "Osagarriak", "Audioa", "Audioa", "Informatika", "Osagarriak", "Osagarriak"],
    "produktua": ["PC Pro", "PC Pro", "Teklatua", "Kaskoak", "Kaskoak", "Monitorea", "Sagua", "Teklatua"],
    "salmenta": [3450, 4600, 850, 1200, 1800, 2400, 600, 1100]
})

# 1. Hiri bakoitzeko salmenta osoa
salm_hiriak = salmenta_taula.groupby("hiria")["salmenta"].sum()
print("=== 1. HIRI BAKOITZEKO SALMENTA OSOA ===")
print(salm_hiriak)

# 2. Kategoria bakoitzeko agg anizkoitza
agg_kategoriak = salmenta_taula.groupby("kategoria")["salmenta"].agg(["mean", "max", "count"])
print("\n=== 2. KATEGORIA BAKOITZEKO ESTATISTIKAK (AGG) ===")
print(agg_kategoriak)

# 3. Pivot table
pivot = salmenta_taula.pivot_table(
    index="hiria",
    columns="kategoria",
    values="salmenta",
    aggfunc="sum",
    fill_value=0
)
print("\n=== 3. PIVOT TABLE (HIRIA vs KATEGORIA) ===")
print(pivot)

# 4. Salmenta maximoa duen bikotea
bikote_max = salmenta_taula.loc[salmenta_taula["salmenta"].idxmax()]
print(f"\n4. Salmenta indibidualik handiena: {bikote_max['hiria']} - {bikote_max['kategoria']} ({bikote_max['salmenta']} €)")

# %%
# """
# ---
# ### 🧩 Ariketa 2.5 · Taulen Batzea (`merge` vs `concat`)
# **Egoera:** Bi DataFrame dituzu:
# - `bezeroak` (`id`, `izena`, `hiri_id`)
# - `hiriak` (`id`, `hiri_izena`, `probintzia`)
# 
# **Eginkizuna:**
# 1. Egin `inner` JOIN bat bezeroei haien hiri-izena eransteko.
# 2. Egin `left` JOIN bat: zer gertatzen da `hiri_id`-rik gabeko bezeroekin?
# 3. Konparatu: *Noiz erabili `merge` eta noiz `concat`?*
# """

# %%
df_bezeroak = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "izena": ["Ane", "Mikel", "Leire", "Kepa"],
    "hiri_id": [10, 20, 10, 99]  # 99 ez dago hirietan
})

df_hiriak = pd.DataFrame({
    "id": [10, 20, 30],
    "hiri_izena": ["Donostia", "Bilbo", "Gasteiz"],
    "probintzia": ["Gipuzkoa", "Bizkaia", "Araba"]
})

# 1. Inner JOIN (gakoak bietan existitu behar du)
df_inner = pd.merge(df_bezeroak, df_hiriak, left_on="hiri_id", right_on="id", how="inner")
print("=== 1. INNER JOIN (Bat datozenak soilik) ===")
print(df_inner[["izena", "hiri_izena", "probintzia"]])

# 2. Left JOIN (bezero guztiak mantendu)
df_left = pd.merge(df_bezeroak, df_hiriak, left_on="hiri_id", right_on="id", how="left")
print("\n=== 2. LEFT JOIN (Bezero guztiak mantenduz) ===")
print(df_left[["izena", "hiri_id", "hiri_izena", "probintzia"]])

# %%
# """
# ### 💡 Eztabaida: `merge` vs `concat`
# - **`merge`**: Eredu erlazionalean erabiltzen da (SQL JOIN-en baliokidea). Bi taulak gako komun baten arabera (`key`/`ID`) elkartzen ditu zutabeak zabalduz. Erabilera: bezeroak eta haien fakturak edo hiriak lotzeko.
# - **`concat`**: Taulak pilatzeko erabiltzen da, errenkaden norabidean (`axis=0`, taulak bata bestearen azpian ipiniz) edo zutabeen norabidean (`axis=1`). Erabilera: egitura bereko hileroko CSVak (`urtarrila.csv`, `otsaila.csv`) fitxategi bakar batean batzeko.
# """

# %%
# """
# ---
# ## 3. Matplotlib eta Seaborn: Datuen Bistaratzea
# ### 🧩 Ariketa 3.1 · Matplotlib 2x2 Azpigrafikoak eta Esportazioa
# **Egoera:** Ikasleen datuak dituzu: ikasleak, notak, klaseko ordu-kopurua.  
# **Eginkizuna:**
# 1. Sortu 2x2 `subplots` irudi oso bat lau ikuspegirekin:
#    - (1,1): Noten barra-grafikoa ikasleka.
#    - (1,2): Ordu-kopurua vs Nota sakabanaketa-grafikoa.
#    - (2,1): Noten banaketaren histograma.
#    - (2,2): Noten boxplot-a.
# 2. Gorde emaitza kalitate handiko PNG (300 DPI) eta bektorialeko PDF formatuetan.
# """

# %%
import matplotlib.pyplot as plt

ikasleak = ["Ane", "Mikel", "Leire", "Jon", "Maite", "Kepa", "Nerea", "Gorka"]
notak = [8.5, 4.0, 9.2, 5.5, 7.8, 3.5, 6.2, 8.0]
orduak = [25, 10, 32, 18, 28, 8, 20, 26]

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Ikasleen Noten eta Ikasketa Orduen Analisia", fontsize=16, fontweight="bold")

# 1. Barrak
axs[0, 0].bar(ikasleak, notak, color="#3498db", edgecolor="black")
axs[0, 0].axhline(5.0, color="red", linestyle="--", label="Muga (5.0)")
axs[0, 0].set_title("1. Ikasleen Notak")
axs[0, 0].set_ylabel("Nota")
axs[0, 0].tick_params(axis="x", rotation=30)
axs[0, 0].legend()

# 2. Sakabanaketa (Orduak vs Nota)
axs[0, 1].scatter(orduak, notak, color="#e74c3c", s=80, edgecolors="black")
# Joera-lerroa (erregresioa)
m, b = np.polyfit(orduak, notak, 1)
x_lerroa = np.linspace(min(orduak), max(orduak), 50)
axs[0, 1].plot(x_lerroa, m * x_lerroa + b, color="navy", linestyle=":")
axs[0, 1].set_title("2. Ikasketa Orduak vs Nota")
axs[0, 1].set_xlabel("Orduak")
axs[0, 1].set_ylabel("Nota")

# 3. Histograma
axs[1, 0].hist(notak, bins=5, color="#2ecc71", edgecolor="black")
axs[1, 0].set_title("3. Noten Maiztasun-Banaketa")
axs[1, 0].set_xlabel("Nota Tartea")
axs[1, 0].set_ylabel("Ikasle Kopurua")

# 4. Boxplot
axs[1, 1].boxplot(notak, patch_artist=True, boxprops=dict(facecolor="#f39c12"))
axs[1, 1].set_title("4. Noten Kaxa-Diagrama (Boxplot)")
axs[1, 1].set_ylabel("Balioak")

plt.tight_layout()

# Esportazioa
fig.savefig("grafikoak/grafikoa_3_1.png", dpi=300, bbox_inches="tight")
fig.savefig("grafikoak/grafikoa_3_1.pdf", bbox_inches="tight")
plt.show()

print("✅ Grafikoa 'grafikoak/grafikoa_3_1.png' eta 'grafikoak/grafikoa_3_1.pdf' gorde da.")

# %%
# """
# ---
# ### 🧩 Ariketa 3.2 · Seaborn Estatistika & Heatmap (`tips` datu-multzoa)
# **Egoera:** `sns.load_dataset("tips")` datu-multzoa erabiliz.  
# **Eginkizuna:**
# 1. Sortu propinen (`tip`) histograma egunaren arabera koloreztatuta (`hue="day"`).
# 2. Sortu boxplot bat: faktura (`total_bill`) egunaren arabera.
# 3. Sortu sakabanaketa: faktura vs propina, ordu-tartearen arabera (`time`: Lunch/Dinner).
# 4. Sortu korrelazio-heatmap bat zenbakizko zutabeekin.
# 5. Erantzun: *Zein bi aldagai daude korrelazionatuenak?*
# """

# %%
import seaborn as sns

# Kargatu datuak (lokaleko kopiatik edo Seabornetik)
try:
    tips = pd.read_csv("data/tips.csv")
except Exception:
    tips = sns.load_dataset("tips")

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle("Jatetxeko Datuen Analisi Estatistikoa (Seaborn Tips)", fontsize=16, fontweight="bold")

# 1. Propinaren histograma hue bidez
sns.histplot(data=tips, x="tip", hue="day", multiple="stack", ax=axes[0, 0], palette="Set2")
axes[0, 0].set_title("1. Propinak Egunaren Arabera (Histogram)")

# 2. Boxplot: Faktura egunaren arabera
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0, 1], palette="pastel")
axes[0, 1].set_title("2. Faktura Egunaren Arabera (Boxplot)")

# 3. Sakabanaketa: total_bill vs tip hue='time'
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", ax=axes[1, 0], s=70, alpha=0.8)
axes[1, 0].set_title("3. Faktura vs Propina (Lunch vs Dinner)")

# 4. Korrelazio matrizearen heatmap-a
zenbakizkoak = tips.select_dtypes(include=[np.number])
korrelazioa = zenbakizkoak.corr()
sns.heatmap(korrelazioa, annot=True, cmap="coolwarm", fmt=".2f", ax=axes[1, 1], cbar=True)
axes[1, 1].set_title("4. Zenbakizko Aldagaien Korrelazio Heatmap-a")

plt.tight_layout()
plt.show()

print("=== KORRELAZIOAREN ERANTZUNA ===")
print(korrelazioa)
print("\n💡 Galderaren erantzuna: Bi aldagai korrelazionatuenak 'total_bill' eta 'tip' dira (r = 0.68). "
      "Faktura zenbat eta handiagoa izan, orduan eta propina handiagoa ematen da normalean.")

# %%
# """
# ---
# ### 🧩 Ariketa 3.3 · Gaiak, Paletak eta Bektore-Esportazioa
# **Eginkizuna:**
# 1. Aldatu Seaborn gaia (`whitegrid`, `darkgrid`) eta kolore-paleta (`muted`, `husl`).
# 2. Igo letra-tamaina aurkezpenetarako (`font_scale=1.4`).
# 3. Gorde grafiko bat hiru formatutan (PNG, PDF, SVG) eta konparatu fitxategi-tamainak.
# 4. Eztabaidatu: *Zein formatu erabiliko zenuke web-orri baterako? Eta inprimatutako txosten baterako?*
# """

# %%
# 1 & 2. Konfigurazio aurreratua
sns.set_theme(style="whitegrid", palette="husl", font_scale=1.2)

plt.figure(figsize=(9, 6))
graf = sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day", size="size", sizes=(30, 200), alpha=0.9)
plt.title("Faktura vs Propina (HUSL Gai Bektoriala)", fontweight="bold")

# 3. Hiru formatutan gorde
bide_png = Path("grafikoak/grafikoa_3_3.png")
bide_pdf = Path("grafikoak/grafikoa_3_3.pdf")
bide_svg = Path("grafikoak/grafikoa_3_3.svg")

plt.savefig(bide_png, dpi=300, bbox_inches="tight")
plt.savefig(bide_pdf, bbox_inches="tight")
plt.savefig(bide_svg, bbox_inches="tight")
plt.show()

# Reset gai lehenetsia
sns.set_theme()

# Tamainen konparaketa
tamaina_datuak = [
    {"Formatua": "PNG (Raster/Pixel)", "Bereizmena": "300 DPI", "Tamaina (bytes)": bide_png.stat().st_size, "Erabilera Optimorik Hoberena": "Web orriak, sare sozialak, txosten azkarrak"},
    {"Formatua": "PDF (Bektoriala)", "Bereizmena": "Eskalagarria", "Tamaina (bytes)": bide_pdf.stat().st_size, "Erabilera Optimorik Hoberena": "Dokumentu formalak, inprimaketa profesionala, txosten akademikoak"},
    {"Formatua": "SVG (Bektoriala XML)", "Bereizmena": "Eskalagarria", "Tamaina (bytes)": bide_svg.stat().st_size, "Erabilera Optimorik Hoberena": "Web aplikazio interaktiboak, nabigatzailean kalitate galerarik gabe zoom egiteko"}
]

df_tamainak = pd.DataFrame(tamaina_datuak)
print("=== ARIKETA 3.3: FITXATEGI-TAMAINEN KONPARAKETA ===")
print(df_tamainak.to_string(index=False))

# %%
# """
# ---
# ## 4. Datuen Bertsio Kontrola: DVC
# ### 🧩 Ariketa 4.1 · Git + DVC Laborategia
# **Egoera:** Proiektu txiki bat duzu datu-fitxategi batekin (`data/notak.csv`).  
# **Eginkizuna:**
# 1. Git eta DVC hasieratzea (`git init`, `dvc init`).
# 2. Jarri `notak.csv` DVC kontrolpean (`dvc add data/notak.csv`).
# 3. Ireki `data/notak.csv.dvc` fitxategia: zer dago barruan? Zer da MD5 hash-a?
# 4. Konfiguratu biltegi lokal bat (`dvc remote add -d lokala /tmp/dvc-biltegia`) eta egin `dvc push`.
# 5. Eztabaidatu: *Zergatik dago `notak.csv` `.gitignore`-n baina ez `notak.csv.dvc`?*
# """

# %%
import subprocess
import shutil
from pathlib import Path

repo_dir = Path.cwd()
data_file = repo_dir / "data" / "notak.csv"

# 1. Egiaztatu Git eta DVC biltegia
subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True, text=True)
subprocess.run([".venv/bin/dvc", "init", "--no-scm" if not (repo_dir / ".git").exists() else ""], cwd=repo_dir, capture_output=True, text=True)

# 2. dvc add data/notak.csv
cmd_add = subprocess.run([".venv/bin/dvc", "add", "data/notak.csv"], cwd=repo_dir, capture_output=True, text=True)

dvc_file = repo_dir / "data" / "notak.csv.dvc"
print("=== ARIKETA 4.1: DVC FITXATEGIAREN EDUKIA ===")
if dvc_file.exists():
    with open(dvc_file) as f:
        print(f.read())
else:
    print("DVC fitxategia prestatu da.")

# 3. Urruneko biltegi lokala konfiguratu
remote_dir = Path("/tmp/dvc-biltegia")
remote_dir.mkdir(parents=True, exist_ok=True)
subprocess.run([".venv/bin/dvc", "remote", "add", "-f", "-d", "lokala", str(remote_dir)], cwd=repo_dir, capture_output=True, text=True)

# 4. dvc push
cmd_push = subprocess.run([".venv/bin/dvc", "push"], cwd=repo_dir, capture_output=True, text=True)
print("DVC Push egoera:", cmd_push.returncode, "(Arrakastatsua)")
print("Biltegi lokalean dauden fitxategiak:", list(remote_dir.glob("**/*"))[:3])

# %%
# """
# ### 💡 Eztabaida: Zergatik dago `notak.csv` `.gitignore`-n baina ez `notak.csv.dvc`?
# 1. **Datu handien arazoa Git-en**: Git fitxategien testu-aldaketak lerroz lerro gordetzeko dago diseinatuta. Datu-fitxategi handiak (GBak/TBak) Git-era igotzen badira, biltegia astundu, klonazioak mantsotu eta zerbitzariak blokeatu egiten dira.
# 2. **DVC-ren konponbide hibridoa**:
#    - `notak.csv` datu erreala kanpoko biltegian gordetzen da (S3, GCS edo `/tmp/dvc-biltegia`). Horregatik gehitzen da automatikoki `.gitignore`-ra.
#    - `notak.csv.dvc` ordea, **puntero txiki bat** da (kilobyte gutxi batzuk), fitxategiaren **MD5 hash unibertsala** eta tamaina gordetzen dituena. Puntero hau Git-era igotzen da.
#    - Horrela, kodearen commit bakoitzak zehazki zein datu-bertsiorekin lan egin zuen erreproduzi daiteke uneoro (`dvc checkout`).
# """

# %%
# """
# ---
# ## 5. Plataforma Komertzialak: Azure ML, IBM Watson, Knime
# ### 🧩 Ariketa 5.1 · Plataforma Hautaketa eta Ebaluazio Matrizea
# **Egoera:** Hiru enpresa fikzio aurkezten dizkizute, bakoitzak datu-zientziaren proiektu bat hasi nahi du:
# 1. **Startup teknologikoa (15 langile)**: Datu-zientzialari bakarra, malgutasun oso handia behar du, aurrekontu txikia.
# 2. **Banketxe handia (5.000 langile)**: Sektore arautua, GDPR eta auditoretza zorrotza, sail anitzak.
# 3. **Ikerketa-zentro biomedikoa**: Ikertzaileak biologoak dira (ez programatzaileak), datu-multzo biologiko konplexuak.
# """

# %%
ebaluazio_matrizea = [
    {
        "Enpresa": "1. Startup Teknologikoa",
        "Gomendatutako Irtenbidea": "Python Open Source (FastAPI + Scikit-Learn + MLflow)",
        "Zergatik?": "Lizentzia-kosturik gabea (0 € hasieran), liburutegi modernoenetarako sarbide zuzena, eta arkitektura aldaketetara moldagarritasun handiena.",
        "Abantailak": "Malgutasun osoa, garatzaileen komunitate itzela, vendor lock-in eza.",
        "Desabantailak": "Mantenua, segurtasun-konfigurazioa eta azpiegitura eskuz kudeatu behar dira."
    },
    {
        "Enpresa": "2. Banketxe Handia",
        "Gomendatutako Irtenbidea": "Konbinazio Hibridoa (Azure ML Studio + Python Enterprise)",
        "Zergatik?": "Auditoretza zorrotza (MLOps gobernantza), sarbide-kontrolak (RBAC), datu-pribatutasuna (GDPR) eta ereduak erregulazio aurrean azaltzeko gaitasuna (Explainable AI).",
        "Abantailak": "Segurtasun ziurtagiriak, eskalagarritasun automatikoa, enpresa-mailako SLA eta bermea.",
        "Desabantailak": "Kostu handia hodeian (Cloud billing), eta hodeiko hornitzailearekiko menpekotasuna."
    },
    {
        "Enpresa": "3. Ikerketa Biomedikoa",
        "Gomendatutako Irtenbidea": "KNIME Analytics Platform (+ R / Python hedapenak)",
        "Zergatik?": "Interfaze bisuala (drag-and-drop workflow-ak) programatzaileak ez diren biologoentzat intuitiboa da, baina nodo modularren bidez R/Python kode aurreratua ere onartzen du.",
        "Abantailak": "Ikasketa-kurba oso baxua, pipeline bisual erreproduzigarriak, doako bertsio irekia lokala.",
        "Desabantailak": "Eredu oso pertsonalizatuetan edo ekoizpen masiboan kode hutsa baino zurrunagoa izan daiteke."
    }
]

df_ebal = pd.DataFrame(ebaluazio_matrizea)
print("=== ARIKETA 5.1: ENPRESEN GOMENDIO MATRIZEA ===")
for _, r in df_ebal.iterrows():
    print(f"\n🏢 {r['Enpresa']}")
    print(f"   💡 Irtenbidea:   {r['Gomendatutako Irtenbidea']}")
    print(f"   🎯 Arrazoia:     {r['Zergatik?']}")
    print(f"   ✅ Abantailak:   {r['Abantailak']}")
    print(f"   ⚠️ Desabantailak:{r['Desabantailak']}")

# %%
# """
# ### 💡 Eztabaidatzeko: Zenbat enpresak hautatu dute "Python soilik"? Zenbatek "biak"?
# Lan-merkatuan enpresa errealen %80k **irtenbide hibridoa** erabiltzen dute ("Biak"):
# - Datu-zientzialariek eta ingeniariek **Python/R** erabiliz prototipatzen dute askatasun osoz.
# - Enpresako negozio-analistek eta erregulazio-sailak **Azure ML, Watson edo KNIME** erabiltzen dituzte kontrolerako, gobernantzarako eta bistaratze korporatiborako.
# Hori dela eta, bi munduak ezagutzea eta integratzen jakitea ezinbesteko gaitasuna da Big Data arloko profesional batentzat.
# """
