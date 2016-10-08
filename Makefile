.SILENT:
PYTHON=$(shell which python)
PIP=venv/bin/pip
PYTEST=$(shell which py.test)

clean:
	find . \( -name *.py[co] -o -name __pycache__ \) -delete

venv:
	virtualenv venv --python=python3

setup: venv
	${PIP} install -U pip
	${PIP} install -r requirements.txt

setup-local: setup
	${PIP} install -r requirements_dev.txt

test: clean
	 MONK_TEST=True\
	 PYTHONPATH=. ${PYTEST} tests/ -s -r a --color=yes -vvv

test-cov: clean
	MONK_TEST=True
	PYTHONPATH=. ${PYTEST} tests/ --cov=app

run: clean
	PYTHONPATH=. ${PYTHON} run.py
