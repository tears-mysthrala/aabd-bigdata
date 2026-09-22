"""Tests: logika lausoa (fuzzify/infer/defuzzify monotonotasuna eta mugak)."""

from cnc_guard.fuzzy import defuzzify, fuzzify, infer, riesgo


def test_frio_suave_riesgo_bajo():
    r = riesgo(52.0, 0.5, 0.05)
    assert 0.0 <= r < 30.0, r


def test_caliente_fuerte_riesgo_muy_alto():
    r = riesgo(90.0, 7.0, 0.9)
    assert r > 70.0, r


def test_monotonia_temperatura():
    r1 = riesgo(55.0, 3.0, 0.3)
    r2 = riesgo(75.0, 3.0, 0.3)
    assert r2 > r1, (r1, r2)


def test_monotonia_vibracion():
    r1 = riesgo(68.0, 1.0, 0.3)
    r2 = riesgo(68.0, 6.0, 0.3)
    assert r2 > r1, (r1, r2)


def test_wear_eleva_riesgo():
    r1 = riesgo(68.0, 3.5, 0.1)
    r2 = riesgo(68.0, 3.5, 0.95)
    assert r2 >= r1, (r1, r2)


def test_fuzzify_particion():
    f = fuzzify(68.0, 3.5, 0.55)
    assert f["temp"]["media"] > 0.9
    assert f["vib"]["media"] == 1.0
    assert f["wear"]["medio"] == 1.0


def test_infer_activa_regla():
    f = fuzzify(90.0, 7.0, 0.9)
    out = infer(f)
    assert out["muy_alto"] > 0.5, out


def test_defuzzify_vacio_cero():
    assert defuzzify({k: 0.0 for k in ("bajo", "medio", "alto", "muy_alto")}) == 0.0


def test_riesgo_acotado_bordes():
    assert 0.0 <= riesgo(50.0, 0.0, 0.0) <= 100.0
    assert 0.0 <= riesgo(95.0, 8.0, 1.0) <= 100.0
