"""Big Data Aplikatua — Makina industrial baten monitorizazioa.

Instalatu: python -m pip install pandas matplotlib
Exekutatu: python denbora_serieak.py
CSV fitxategia script-aren karpeta berean egon behar da.
"""
# 1. Inportatu Pandas eta Matplotlib liburutegiak
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. URRATSA — DATUAK KARGATU (1–5. eginkizunak)
# ============================================================
print("\n=== 1. URRATSA: DATUAK KARGATU ===")

# 2. Kargatu sentsorea.csv fitxategia, timestamp zutabea DatetimeIndex gisa erabiliz


# 3. Ordenatu datuak kronologikoki


# 4. Erakutsi lehen bost neurketak


# 5. Erakutsi zenbat errenkada eta zutabe dauden


# ============================================================
# 2. URRATSA — DENBORAREN ARABERA FILTRATU (6–7)
# ============================================================
print("\n=== 2. URRATSA: DENBORA-TARTEA ===")

# 6. Erakutsi 2026-10-01 eguneko 08:00etatik 09:00etara jasotako datuak



# 7. Kalkulatu denbora-tarte horretako tenperaturaren batezbestekoa


# ============================================================
# 3. URRATSA — RESAMPLE (8–10)
# ============================================================
print("\n=== 3. URRATSA: RESAMPLE ===")

# 8. Kalkulatu tenperaturaren eta bibrazioaren 10 minutuko batezbestekoak


# 9. Erakutsi emaitza terminalean


# 10. Erakutsi zenbat errenkada dituen taula berriak



# ============================================================
# 4. URRATSA — DATUEN KALITATEA (11–13)
# ============================================================
print("\n=== 4. URRATSA: DATUEN KALITATEA ===")

# isna(): datua falta bada, True ematen du.
# sum(): zutabe bakoitzeko True kopurua batzen du.

# 11. Erakutsi zenbat balio falta diren (NaN) zutabe bakoitzean


# 12. Bete falta diren tenperaturak interpolazioaren bidez, tenperatura_beteta izeneko zutabe berri batean


# 13. Bilatu 50ºC baino handiagoak diren neurketak


# ============================================================
# 5. URRATSA — ROLLING ETA GRAFIKOA (14–15)
# ============================================================
print("\n=== 5. URRATSA: ROLLING ETA GRAFIKOA ===")

# 14. Kalkulatu interpolatutako tenperaturaren azken bost neurketen batezbesteko mugikorra.
# Gorde emaitza tenperatura_leundua izeneko zutabe batean


# 15. Irudikatu grafiko berean: Jatorrizko tenperatura eta tenperatura leundua.
