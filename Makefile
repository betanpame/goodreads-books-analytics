SHELL := /bin/bash

.PHONY: metrics-catalog core-metrics

metrics-catalog:
	docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm \
	  app python -m src.analyses.metrics_catalog \
	  --books-csv data/derived/books_clean.csv \
	  --output-markdown outputs/phase04_metrics_catalog.md

core-metrics:
	docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm \
	  app python -m src.analyses.run_core_metrics \
	  --books-csv data/derived/books_clean.csv \
	  --output-dir outputs/phase04_core_metrics
