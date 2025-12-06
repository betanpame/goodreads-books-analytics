SHELL := /bin/bash

.PHONY: metrics-catalog core-metrics

metrics-catalog:
	docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm \
	  app python -m src.analyses.support.documentation.metrics_catalog \
	  --books-csv data/derived/books_clean.csv \
	  --output-markdown outputs/phase04_metrics_catalog.md

core-metrics:
	docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm \
	  app python -m src.analyses.portfolio.p03_core_metrics_suite \
	  --books-csv data/derived/books_clean.csv \
	  --output-dir outputs/phase04_core_metrics
