.PHONY: setup import-cv test check

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt

import-cv:
	.venv/bin/python scripts/import_cv.py

test:
	.venv/bin/python -m unittest discover -s tests -v

check: test
	bash -n scripts/compile.sh
	.venv/bin/python scripts/import_cv.py --help >/dev/null
