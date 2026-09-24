"""Ariketa 3.1 ebazpena Moodle-ko datu ofizialekin (ikasleak_notak_100.csv).

PDFko 3.1 Ariketaren eskakizunak:
1. Ikasleen noten barra-grafikoa (lagin esanguratsua edo sailkapena).
2. Sakabanaketa-grafikoa: ikasketa orduak (x) vs nota (y), erregresio-lerroarekin.
3. 2x2 subplots irudi osoa (barrak, scatter, histograma, boxplot).
4. PNG (300 DPI) eta PDF formatuetan esportatzea.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ikasleak_notak_100.csv"
OUT_DIR = BASE_DIR / "grafikoak"
OUT_PNG = OUT_DIR / "grafikoa_3_1_ofiziala.png"
OUT_PDF = OUT_DIR / "grafikoa_3_1_ofiziala.pdf"


def kargatu_datuak() -> pd.DataFrame:
    """Kargatu Moodleko ikasleak_notak_100.csv fitxategia (; bereizlea, , hamartarra)."""
    df = pd.read_csv(DATA_PATH, sep=";", decimal=",", encoding="utf-8")
    return df


def sortu_grafikoak(df: pd.DataFrame) -> tuple[Path, Path]:
    """Sortu 2x2 irudia eta gorde PNG zein PDF formatuetan."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axs = plt.subplots(2, 2, figsize=(14, 11))
    fig.suptitle(
        "Ariketa 3.1: Ikasleen Noten eta Ikasketa Orduen Analisia (N=100)",
        fontsize=16,
        fontweight="bold",
    )

    # 1. (0, 0) Barra-grafikoa lehen 15 ikasleekin (irakurgarritasuna bermatzeko)
    lagina = df.head(15)
    axs[0, 0].bar(lagina["Ikaslea"], lagina["Nota"], color="#3498db", edgecolor="black")
    axs[0, 0].axhline(5.0, color="red", linestyle="--", label="Gainditua (5.0)")
    axs[0, 0].set_title("1. Ikasleen Notak (Lehen 15 ikasle)")
    axs[0, 0].set_ylabel("Nota (0-10)")
    axs[0, 0].tick_params(axis="x", rotation=45)
    axs[0, 0].legend()
    axs[0, 0].grid(axis="y", linestyle=":", alpha=0.7)

    # 2. (0, 1) Scatter plot: Orduak vs Nota erregresio lerroarekin
    axs[0, 1].scatter(
        df["Orduak"], df["Nota"], color="#e74c3c", alpha=0.7, edgecolors="black", s=60
    )
    # Joera zuzena kalkulatu
    m, b = np.polyfit(df["Orduak"], df["Nota"], 1)
    x_vals = np.linspace(df["Orduak"].min(), df["Orduak"].max(), 100)
    axs[0, 1].plot(
        x_vals,
        m * x_vals + b,
        color="darkblue",
        linestyle="--",
        linewidth=2,
        label=f"Erregresioa (y = {m:.2f}x + {b:.2f})",
    )
    axs[0, 1].set_title("2. Ikasketa Orduak (x) vs Nota (y)")
    axs[0, 1].set_xlabel("Ikasketa Orduak")
    axs[0, 1].set_ylabel("Nota (0-10)")
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle=":", alpha=0.7)

    # 3. (1, 0) Histograma / Maiztasun-banaketa
    axs[1, 0].hist(
        df["Nota"], bins=10, color="#2ecc71", edgecolor="black", range=(0, 10)
    )
    axs[1, 0].axvline(
        df["Nota"].mean(),
        color="black",
        linestyle="-.",
        linewidth=2,
        label=f"Batez bestekoa: {df['Nota'].mean():.2f}",
    )
    axs[1, 0].set_title("3. Noten Maiztasun-Banaketa (100 ikasle)")
    axs[1, 0].set_xlabel("Nota tartea")
    axs[1, 0].set_ylabel("Ikasle kopurua")
    axs[1, 0].legend()
    axs[1, 0].grid(axis="y", linestyle=":", alpha=0.7)

    # 4. (1, 1) Boxplot
    box = axs[1, 1].boxplot(
        df["Nota"],
        patch_artist=True,
        tick_labels=["Notak"],
        boxprops=dict(facecolor="#f39c12", color="black"),
        medianprops=dict(color="red", linewidth=2),
    )
    axs[1, 1].set_title("4. Noten Kaxa-Diagrama (Boxplot)")
    axs[1, 1].set_ylabel("Balioak")
    axs[1, 1].grid(axis="y", linestyle=":", alpha=0.7)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUT_PNG, dpi=300)
    plt.savefig(OUT_PDF)
    plt.close()
    return OUT_PNG, OUT_PDF


def main() -> None:
    df = kargatu_datuak()
    print(f"Kargatutako datuak: {len(df)} errenkada, zutabeak: {list(df.columns)}")
    print(f"Batez besteko nota: {df['Nota'].mean():.2f}, batez besteko orduak: {df['Orduak'].mean():.1f}")
    r = np.corrcoef(df["Orduak"], df["Nota"])[0, 1]
    print(f"Korrelazio koefizientea (Orduak - Nota): r = {r:.3f} (oso sendoa)")
    png, pdf = sortu_grafikoak(df)
    print(f"Grafikoak gordeta:\n  - {png}\n  - {pdf}")


if __name__ == "__main__":
    main()
