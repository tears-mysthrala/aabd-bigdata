"""Egutegi-egunak ez du aldatzen seed finkoko salmenten emaitza."""

from datetime import date, timedelta
import unittest
from unittest.mock import patch

from faker import Faker

import generar_bezeroak
from generar_bezeroak import (
    SALMENTA_DATA_AZKENA,
    SALMENTA_DATA_HASIERA,
    generar_salmentak,
)


class SalesSeedIgnoresSystemDateTest(unittest.TestCase):
    def test_seeded_sales_are_identical_under_different_system_dates(self) -> None:
        class FakerWithClock:
            def __init__(self, system_today: date) -> None:
                self.fake = Faker("es_ES")
                self.system_today = system_today

            def date_between(self, start_date: object = "-30y", end_date: object = "today") -> date:
                # Faker-en data erlatiboak injektatutako sistema-egunaren arabera ebazten ditu.
                start = self.system_today - timedelta(days=730) if start_date == "-2y" else start_date
                end = self.system_today if end_date == "today" else end_date
                return self.fake.date_between(start, end)  # type: ignore[arg-type]

            def seed_instance(self, seed: int) -> None:
                self.fake.seed_instance(seed)

            def __getattr__(self, name: str) -> object:
                return getattr(self.fake, name)

        def run_with_today(system_today: date) -> list[dict[str, object]]:
            def faker_with_clock(seed: int | None) -> FakerWithClock:
                fake = FakerWithClock(system_today)
                if seed is not None:
                    fake.seed_instance(seed)
                return fake

            with patch.object(generar_bezeroak, "_faker", side_effect=faker_with_clock):
                return generar_salmentak(100, seed=42)

        lehenengoa = run_with_today(date(2024, 1, 1))
        bigarrena = run_with_today(date(2044, 1, 1))

        self.assertEqual(lehenengoa, bigarrena)
        self.assertTrue(
            all(
                SALMENTA_DATA_HASIERA.isoformat() <= str(salmenta["data"]) <= SALMENTA_DATA_AZKENA.isoformat()
                for salmenta in lehenengoa
            )
        )


if __name__ == "__main__":
    unittest.main()
