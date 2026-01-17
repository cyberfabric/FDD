.PHONY: test test-verbose test-quick validate validate-feature validate-code validate-code-feature install clean help

# Detect Python version with pytest installed
PYTHON := $(shell python3.11 -c "import pytest" 2>/dev/null && echo python3.11 || echo python3)

# Default target
help:
	@echo "FDD Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make test                          - Run all tests"
	@echo "  make test-verbose                  - Run tests with verbose output"
	@echo "  make test-quick                    - Run fast tests only (skip slow integration tests)"
	@echo "  make validate                      - Validate core methodology feature"
	@echo "  make validate-feature FEATURE=name - Validate specific feature"
	@echo "  make validate-code                 - Validate codebase traceability (entire project)"
	@echo "  make validate-code-feature FEATURE=name - Validate code traceability for specific feature"
	@echo "  make install                       - Install Python dependencies"
	@echo "  make clean                         - Remove Python cache files"
	@echo "  make help                          - Show this help message"

# Run all tests
test:
	@echo "Running FDD tests with $(PYTHON)..."
	@$(PYTHON) -c "import pytest" 2>/dev/null || { \
		echo ""; \
		echo "ERROR: pytest not installed"; \
		echo ""; \
		echo "Install it with:"; \
		echo "  pip3 install pytest pytest-cov"; \
		echo ""; \
		echo "Or use python3.11:"; \
		echo "  python3.11 -m pip install pytest pytest-cov"; \
		echo ""; \
		exit 1; \
	}
	$(PYTHON) -m pytest tests/ -v --tb=short

# Run tests with verbose output
test-verbose:
	@echo "Running FDD tests (verbose) with $(PYTHON)..."
	$(PYTHON) -m pytest tests/ -vv

# Run quick tests only
test-quick:
	@echo "Running quick tests with $(PYTHON)..."
	$(PYTHON) -m pytest tests/ -v -m "not slow"

# Validate core methodology feature
validate:
	@echo "Validating core methodology feature..."
	$(PYTHON) skills/fdd/scripts/fdd.py validate \
		--artifact architecture/features/feature-core-methodology/CHANGES.md \
		--design architecture/features/feature-core-methodology/DESIGN.md

# Validate specific feature
validate-feature:
	@if [ -z "$(FEATURE)" ]; then \
		echo "Error: FEATURE parameter required"; \
		echo "Usage: make validate-feature FEATURE=feature-name"; \
		exit 1; \
	fi
	@echo "Validating feature: $(FEATURE)..."
	@python3.11 skills/fdd/scripts/fdd.py validate \
		--artifact architecture/features/$(FEATURE)/CHANGES.md \
		--design architecture/features/$(FEATURE)/DESIGN.md

# Validate codebase traceability for entire project
validate-code:
	@echo "Validating codebase traceability..."
	@python3.11 skills/fdd/scripts/fdd.py validate --artifact .

# Validate code traceability for specific feature
validate-code-feature:
	@if [ -z "$(FEATURE)" ]; then \
		echo "Error: FEATURE parameter required"; \
		echo "Usage: make validate-code-feature FEATURE=feature-name"; \
		exit 1; \
	fi
	@echo "Validating code traceability for feature: $(FEATURE)..."
	@python3.11 skills/fdd/scripts/fdd.py validate --artifact architecture/features/$(FEATURE)

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	python3 -m pip install --user pytest pytest-cov

# Clean Python cache
clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"
