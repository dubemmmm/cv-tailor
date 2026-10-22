.PHONY: setup init-jobs import-cv test check

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt

init-jobs:
	@if [ -e jobs.txt ]; then \
		echo "jobs.txt already exists; leaving it unchanged"; \
	else \
		cp jobs.example.txt jobs.txt; \
		echo "Created jobs.txt. Add one job URL per line."; \
	fi

import-cv:
	.venv/bin/python scripts/import_cv.py

test:
	.venv/bin/python -m unittest discover -s tests -v

check: test
	bash -n scripts/compile.sh
	.venv/bin/python scripts/import_cv.py --help >/dev/null
