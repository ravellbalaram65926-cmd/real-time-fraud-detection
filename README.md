# Real-Time Fraud Detection

## Problem
Flag fraudulent card transactions within seconds of arrival.

## Dataset and provenance

Committed `data/raw/sample_transactions.csv` is synthetic only. A real benchmark is the [ULB credit-card fraud dataset on Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud); Kaggle account/rules apply. Keep it under ignored `data/external/` and map its schema locally; do not commit cardholder or raw transaction data.

### Download the Kaggle dataset

The downloader defaults to `mlg-ulb/creditcardfraud`. Install the Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save `kaggle.json` to `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Run `python scripts/download_kaggle.py`; files go to ignored `data/external/`. The public data's columns differ from the demo schema, so adapt them before using it as pipeline input. Do not commit raw transaction data.

## Run the ETL demo

From this directory, run `python src/main.py`. The pipeline deduplicates transaction IDs, orders events by card/time, derives prior-only 10-minute velocity features, and emits an explicitly labeled example threshold rule in `data/gold/scored_transactions.csv`. This rule is a teaching baseline, not a trained or production fraud model. Re-running replaces the same deterministic output.

Run checks with `python -m pytest -q tests`.

## Stack
Kafka, Spark Structured Streaming, XGBoost, Docker, dashboard

## Architecture
- Bronze / raw ingestion layer
- Silver / cleaned and validated data layer
- Gold / feature or serving layer
- Monitoring / validation and retraining feedback loop

## DE tasks
1. Ingest raw data with versioned file naming and timestamps.
2. Build idempotent and incremental transformations.
3. Add data quality checks and freshness alerts.
4. Create a reproducible run order using a Makefile or run script.
5. Store outputs in a warehouse, lake, or streaming sink with clear contracts.

## DS tasks
1. Run EDA and validate assumptions about seasonality, drift, and user behavior.
2. Benchmark a baseline model before trying a stronger approach.
3. Use proper time-based splits and avoid leakage.
4. Log experiments, tuning choices and key metrics.
5. Report limitations and next steps in a production-focused way.

## Deliverables
- Reproducible pipeline or app
- Tests for transformation and validation logic
- Dashboard, API, or report showing outputs
- Clear business summary with measurable impact

## Recommended repository structure
`	ext
real-time-fraud-detection/
+-- README.md
+-- requirements.txt
+-- Makefile
+-- .gitignore
+-- src/
+-- tests/
+-- notebooks/
+-- docs/
`

## Resume line
Built a streaming fraud-scoring pipeline processing transactions in real time with strong precision-recall tradeoffs and alerting.

### Kaggle dataset download

Install Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save it locally as `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Never commit or share the token. Run `python scripts/download_kaggle.py`; downloaded files go to Git-ignored `data/external/` and are not published to this repository. Review the dataset license and Kaggle terms before use; large datasets may require adapting the sample input schema.
