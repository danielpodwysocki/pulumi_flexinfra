.PHONY: test clean

venv/bin/activate:
	python3 -m venv venv
	./venv/bin/pip install .
	./venv/bin/pip install -r test_requirements.txt


test: venv/bin/activate
	./venv/bin/python -m pytest
	./venv/bin/python -m black --check .
	./venv/bin/python -m flake8 tests
	./venv/bin/python -m flake8 pulumi_flexinfra

clean:
	rm -rf venv

