.PHONY: clean deepclean install dev prerequisites mypy ruff ruff-format pyproject-fmt codespell lint pre-commit test-run test build publish doc-watch doc-build doc-coverage doc

########################################################################################
# Variables
########################################################################################

# Documentation target directory, will be adapted to specific folder for readthedocs.
PUBLIC_DIR := $(shell [ "$$READTHEDOCS" = "True" ] && echo "$${READTHEDOCS_OUTPUT}html" || echo "public")

# Determine the Python version used by pipx.
PIPX_PYTHON_VERSION := $(shell `pipx environment --value PIPX_DEFAULT_PYTHON` -c "from sys import version_info; print(f'{version_info.major}.{version_info.minor}')")

########################################################################################
# Development Environment Management
########################################################################################

# Remove common intermediate files.
clean:
	-rm -rf \
		$(PUBLIC_DIR) \
		.coverage \
		.mypy_cache \
		.pdm-build \
		.pdm-python \
		.pytest_cache \
		.ruff_cache \
		Pipfile* \
		__pypackages__ \
		build \
		coverage.xml \
		dist
	find . -name '*.egg-info' -print0 | xargs -0 rm -rf
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '.DS_Store' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -print0 | xargs -0 rm -rf

# Remove pre-commit hook, virtual environment alongside itermediate files.
deepclean: clean
	if command -v pre-commit > /dev/null 2>&1; then pre-commit uninstall; fi
	if command -v pdm >/dev/null 2>&1 && pdm venv list | grep -q in-project ; then pdm venv remove --yes in-project >/dev/null 2>&1; fi

# Install the package in editable mode.
install:
	pdm sync --prod

# Install the package in editable mode with specific optional dependencies.
dev-%:
	pdm sync --dev --group $*

# Prepare the development environment.
# Install the package in editable mode with all optional dependencies and pre-commit hook.
dev:
	pdm sync
	if [ "$(CI)" != "true" ] && command -v pre-commit > /dev/null 2>&1; then pre-commit install; fi

# Install standalone tools
prerequisites:
	pipx install --force codespell[toml]==2.3.0
	pipx install --force pdm==2.16.1
ifeq ($(PIPX_PYTHON_VERSION), 3.8)
	pipx install --force pre-commit==3.5.0
else
	pipx install --force pre-commit==3.7.1
endif
	pipx install --force pyproject-fmt==2.1.4
	pipx install --force ruff==0.5.4
	pipx install --force watchfiles==0.22.0

########################################################################################
# Lint and pre-commit
########################################################################################

# Check lint with mypy.
mypy:
	pdm run python -m mypy . --html-report $(PUBLIC_DIR)/reports/mypy

# Lint with ruff.
ruff:
	ruff check .

# Format with ruff.
ruff-format:
	ruff format --check .

# Check lint with pyproject-fmt.
pyproject-fmt:
	pyproject-fmt pyproject.toml

# Check lint with codespell.
codespell:
	codespell

# Check lint with all linters.
lint: mypy ruff ruff-format pyproject-fmt codespell

# Run pre-commit with autofix against all files.
pre-commit:
	pre-commit run --all-files --hook-stage manual

########################################################################################
# Test
########################################################################################

# Clean and run test with coverage.
test-run:
	pdm run python -m coverage erase
	pdm run python -m coverage run -m pytest

# Generate coverage report for terminal and xml.
test: test-run
	pdm run python -m coverage report
	pdm run python -m coverage xml

########################################################################################
# Package
########################################################################################

# Build the package.
build:
	pdm build

# Publish the package.
publish:
	pdm publish

########################################################################################
# Documentation
########################################################################################

# Generate documentation with auto build when changes happen.
doc-watch:
	pdm run python -m http.server --directory public &
	watchfiles "make doc-build" docs src README.md

# Build documentation only from src.
doc-build:
	pdm run sphinx-build -a docs $(PUBLIC_DIR)

# Generate html coverage reports with badge.
doc-coverage: test-run
	pdm run python -m coverage html -d $(PUBLIC_DIR)/reports/coverage
	pdm run bash scripts/generate-coverage-badge.sh $(PUBLIC_DIR)/_static/badges

# Generate all documentation with reports.
doc: doc-build mypy doc-coverage

########################################################################################
# End
########################################################################################
