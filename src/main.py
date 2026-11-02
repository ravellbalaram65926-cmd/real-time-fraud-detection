"""ETL demo: validate transactions and derive rolling velocity features."""

import argparse
import csv
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "sample_transactions.csv"
DEFAULT_OUTPUT = ROOT / "data" / "gold" / "scored_transactions.csv"


def score_transactions(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    rows.sort(key=lambda row: (row["card_id"], row["timestamp"], row["transaction_id"]))
    windows: dict[str, deque[tuple[datetime, float]]] = defaultdict(deque)
    window_totals: dict[str, float] = defaultdict(float)
    seen = set()
    result = []
    for row in rows:
        tx_id = row["transaction_id"]
        if tx_id in seen:
            continue
        seen.add(tx_id)
        timestamp = datetime.fromisoformat(row["timestamp"])
        amount = float(row["amount"])
        if amount < 0:
            raise ValueError(f"Transaction {tx_id} has a negative amount")
        window = windows[row["card_id"]]
        cutoff = timestamp - timedelta(minutes=10)
        while window and window[0][0] < cutoff:
            _, expired_amount = window.popleft()
            window_totals[row["card_id"]] -= expired_amount
        prior_count = len(window)
        prior_mean = window_totals[row["card_id"]] / prior_count if prior_count else 0.0
        row.update(
            {
                "transactions_prior_10m": str(prior_count),
                "prior_amount_mean": f"{prior_mean:.2f}",
                "rule_alert": str(int(amount >= 500 or prior_count >= 5)),
            }
        )
        result.append(row)
        window.append((timestamp, amount))
        window_totals[row["card_id"]] += amount
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = score_transactions(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    print(f"Processed {len(rows)} transactions to {args.output}")


if __name__ == "__main__":
    main()
