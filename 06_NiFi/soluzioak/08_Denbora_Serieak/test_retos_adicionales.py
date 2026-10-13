import pandas as pd
import pytest

from retos_adicionales import alert_episodes


@pytest.mark.parametrize("dtype", ["float64", "Float64"])
def test_one_alert_per_sustained_episode_and_nan_resets(dtype):
    series = pd.Series(
        [49, 51, 52, 53, 54, float("nan"), 55, 56, 57],
        index=pd.date_range("2026-10-01", periods=9, freq="min"),
        dtype=dtype,
    )
    assert alert_episodes(series).tolist() == [
        False,
        False,
        False,
        True,
        False,
        False,
        False,
        False,
        True,
    ]


def test_missing_timestamp_breaks_sequence_and_threshold_is_strict():
    series = pd.Series(
        [51, 52, 53, 54],
        index=pd.to_datetime(
            [
                "2026-10-01 00:00",
                "2026-10-01 00:01",
                "2026-10-01 00:03",
                "2026-10-01 00:04",
            ]
        ),
    )
    assert not alert_episodes(series).any()
    series = pd.Series(
        [50, 51, 52], index=pd.date_range("2026-10-01", periods=3, freq="min")
    )
    assert not alert_episodes(series).any()
