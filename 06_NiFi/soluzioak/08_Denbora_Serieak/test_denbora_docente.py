import hashlib
from pathlib import Path

import pandas as pd
import pytest

from denbora_serieak_docente import SOURCE, analyze, load_source, run


def test_teacher_interval_resample_interpolation_and_raw_peak():
    df = load_source()
    interval, means, enriched, above, alerts, aggregation = analyze(df)
    # Extremos incluidos y NaN omitido, no tratado como temperatura cero.
    assert interval.index[0] == pd.Timestamp("2026-10-01 08:00")
    assert interval.index[-1] == pd.Timestamp("2026-10-01 09:00")
    assert len(interval) == 61 and interval.tenperatura.count() == 60
    assert interval.tenperatura.mean() == pytest.approx(42.22833333333334)
    assert len(means) == 18
    assert means.iloc[0].tenperatura == pytest.approx(df.iloc[:10].tenperatura.mean())
    assert aggregation["size"].sum() == 180
    assert aggregation["count"].sum() == 177
    missing = df.tenperatura.isna()
    for timestamp in df.index[missing]:
        expected = (
            df.loc[timestamp - pd.Timedelta("1min"), "tenperatura"]
            + df.loc[timestamp + pd.Timedelta("1min"), "tenperatura"]
        ) / 2
        assert enriched.loc[timestamp, "tenperatura_beteta"] == pytest.approx(expected)
    pd.testing.assert_series_equal(enriched.tenperatura, df.tenperatura)
    assert enriched.tenperatura_leundua.iloc[4] == pytest.approx(
        enriched.tenperatura_beteta.iloc[:5].mean()
    )
    assert above.index.tolist() == [pd.Timestamp("2026-10-01 09:53")]
    assert above.tenperatura.iloc[0] == 84.8
    assert means.tenperatura.max() < 50 and not alerts.any()


def test_outputs_preserve_source_and_report_its_hash(tmp_path):
    original = SOURCE.read_bytes()
    report = run(tmp_path)
    assert SOURCE.read_bytes() == original
    assert report["source_sha256"] == hashlib.sha256(original).hexdigest()
    assert (tmp_path / "tenperatura.png").stat().st_size > 1000
    written = pd.read_csv(tmp_path / "operaciones.csv")
    assert len(written) == report["rows"] == 180
    assert written.tenperatura.isna().sum() == 3


@pytest.mark.parametrize("timestamps", [["bad"], ["2026-10-01", "2026-10-01"]])
def test_rejects_invalid_or_duplicate_timestamps(tmp_path, timestamps):
    source = Path(tmp_path) / "invalid.csv"
    pd.DataFrame({"timestamp": timestamps, "tenperatura": 40, "bibrazioa": 2}).to_csv(
        source, index=False
    )
    with pytest.raises(ValueError, match="timestamp|Timestamps"):
        load_source(source)
