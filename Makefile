PYTHON=python

SEARCH=
.PHONY: clean
.PHONY: test
.PHONY: build
.PHONY: testpypi
.PHONY: publish

clean:
	-@rm -rf build/
	-@rm -rf dist/
	-@rm -rf *.egg-info
	-@rm -rf .pytest_cache/

test:
	@black .
	@$(PYTHON) -m pytest tests

build:
	@$(PYTHON) setup.py sdist bdist_wheel

testpypi:
	@$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi:
	@$(PYTHON) -m twine upload dist/*

publish:
	@$(MAKE) clean
	@$(MAKE) build
	@$(MAKE) pypi
