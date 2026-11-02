import unittest
from pathlib import Path

from src.main import score_transactions


class FraudPipelineTests(unittest.TestCase):
    def test_features_are_prior_only_and_rule_is_explicit(self):
        sample = Path(__file__).resolve().parents[1] / "data/raw/sample_transactions.csv"
        rows = score_transactions(sample)
        card_a = [row for row in rows if row["card_id"] == "CARD-A"]
        self.assertEqual(card_a[0]["transactions_prior_10m"], "0")
        self.assertEqual(card_a[2]["transactions_prior_10m"], "2")
        self.assertEqual(card_a[2]["rule_alert"], "1")


if __name__ == "__main__":
    unittest.main()
