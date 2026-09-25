"""Logika lausoa (Mamdani) sentsore-fusiorako: tenperatura + bibrazioa + higadura -> arriskua.

Diseinua `soluzioak/Ebazpena_CNC_Guard_eta_AA_Ereduak.md` 3. atalean.
Inplementazio propioa numpy-rekin (ez dakar menpekotasun berririk):
trian/trapezio kide-funtzioak, MIN t-norma, MAX agregazioa, zentroide defuzzifikazioa.

Higadura ez dator dataset-ean: `txv = tenperatura*bibrazioa` normalizatua
erabiltzen da proxy gisa. Une bereko bi neurrietatik eratorria da;
ez du higadura metatua neurtzen eta bi adarren arteko independentzia mugatzen du.
"""

from __future__ import annotations

import numpy as np

# Unibertsoak
TEMP_RANGE = (50.0, 95.0)
VIB_RANGE = (0.0, 8.0)
WEAR_RANGE = (0.0, 1.0)
RISK_RANGE = (0.0, 100.0)


def _tri(x: float, a: float, b: float, c: float) -> float:
    """Triangeluarra: 0 a-tik behera, 1 b-n, 0 c-tik gora."""
    x = float(x)
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a) if b != a else 1.0
    return (c - x) / (c - b) if c != b else 1.0


def _trap(x: float, a: float, b: float, c: float, d: float) -> float:
    """Trapezoidala: 0 a-tik behera, 1 [b, c]-n, 0 d-tik gora."""
    x = float(x)
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return (x - a) / (b - a) if b != a else 1.0
    return (d - x) / (d - c) if d != c else 1.0


# Sarrerak: (etiqueta, funtzioa)
TEMP_SETS = {
    "baja": lambda x: _trap(x, 50, 50, 58, 66),
    "media": lambda x: _tri(x, 60, 68, 76),
    "alta": lambda x: _trap(x, 70, 78, 95, 95),
}
VIB_SETS = {
    "suave": lambda x: _trap(x, 0, 0, 1.5, 3.0),
    "media": lambda x: _tri(x, 2.0, 3.5, 5.0),
    "fuerte": lambda x: _trap(x, 4.0, 5.5, 8, 8),
}
WEAR_SETS = {
    "bajo": lambda x: _trap(x, 0, 0, 0.2, 0.45),
    "medio": lambda x: _tri(x, 0.3, 0.55, 0.8),
    "alto": lambda x: _trap(x, 0.65, 0.85, 1, 1),
}
# Irteera: arriskua [0, 100]
RISK_SETS = {
    "bajo": lambda x: _trap(x, 0, 0, 15, 35),
    "medio": lambda x: _tri(x, 25, 50, 75),
    "alto": lambda x: _tri(x, 60, 78, 92),
    "muy_alto": lambda x: _trap(x, 85, 95, 100, 100),
}
_RISK_XS = np.linspace(*RISK_RANGE, num=201)

# Arau-basea: (tenperatura, bibrazioa, higadura|None, arriskua)
RULES = [
    ("alta", "fuerte", None, "muy_alto"),
    ("alta", "media", None, "alto"),
    ("alta", "suave", None, "medio"),
    ("media", "fuerte", None, "alto"),
    ("media", "media", None, "medio"),
    ("media", "suave", None, "bajo"),
    ("baja", "fuerte", None, "medio"),
    ("baja", "media", None, "bajo"),
    ("baja", "suave", None, "bajo"),
    # Higadurak maila bat igotzen du muturrekoetan:
    (None, None, "alto", "muy_alto"),
    (None, "fuerte", "medio", "alto"),
    (None, "media", "medio", "medio"),
]


def fuzzify(temp: float, vib: float, wear: float) -> dict[str, dict[str, float]]:
    """Sarrera crisp -> kide-mailak."""
    temp = float(np.clip(temp, *TEMP_RANGE))
    vib = float(np.clip(vib, *VIB_RANGE))
    wear = float(np.clip(wear, *WEAR_RANGE))
    return {
        "temp": {k: f(temp) for k, f in TEMP_SETS.items()},
        "vib": {k: f(vib) for k, f in VIB_SETS.items()},
        "wear": {k: f(wear) for k, f in WEAR_SETS.items()},
    }


def infer(fuzzy: dict[str, dict[str, float]]) -> dict[str, float]:
    """Mamdani MIN/MAX: arau bakoitzaren aktibazioa -> irteera multzo bakoitzeko max."""
    out = {k: 0.0 for k in RISK_SETS}
    for t, v, w, r in RULES:
        acts = []
        if t is not None:
            acts.append(fuzzy["temp"][t])
        if v is not None:
            acts.append(fuzzy["vib"][v])
        if w is not None:
            acts.append(fuzzy["wear"][w])
        strength = min(acts) if acts else 0.0
        out[r] = max(out[r], strength)
    return out


def defuzzify(activated: dict[str, float]) -> float:
    """Zentroidea: moztutako irteera-funtzioen agregazioa."""
    agg = np.zeros_like(_RISK_XS)
    for label, strength in activated.items():
        if strength <= 0:
            continue
        mf = np.array([RISK_SETS[label](x) for x in _RISK_XS])
        agg = np.maximum(agg, np.minimum(mf, strength))
    if agg.sum() <= 0:
        return 0.0
    return float((agg * _RISK_XS).sum() / agg.sum())


def riesgo(temp: float, vib: float, wear: float) -> float:
    """Arrisku crisp [0, 100] sarrera crisp-etik (pipeline osoa)."""
    return defuzzify(infer(fuzzify(temp, vib, wear)))


def riesgo_norm(temp: float, vib: float, wear: float) -> float:
    """Arriskua [0, 1] (fusiorako)."""
    return riesgo(temp, vib, wear) / 100.0
