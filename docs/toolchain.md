# Development Toolchain

This project uses a modern Python development toolchain focused on speed, reliability, and developer experience.

## Code Quality Tools

### Ruff - Linting & Formatting

[Ruff](https://docs.astral.sh/ruff/) is an extremely fast Python linter and code formatter, written in Rust.

#### Configuration

Ruff is configured in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

#### Usage

```bash
# Check for linting issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format . --check

# Via Make
make lint     # Check linting and formatting
make format   # Auto-format code
```

### pytest - Testing Framework

[pytest](https://pytest.org/) is a mature testing framework that makes it easy to write simple and scalable tests.

#### Configuration

Configured in `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
```

#### Usage

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_example.py

# Run tests matching pattern
uv run pytest -k "test_config"

# Via Make
make pytest              # Run all tests
make pytest-integration  # Run integration tests
```

#### Test Structure

```python
# tests/test_example.py
import pytest
from uv_starter.hello import main

def test_main():
    """Test the main function."""
    result = main()
    assert result is not None

@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

## Pre-commit Hooks

[Pre-commit](https://pre-commit.com/) runs checks before each commit to catch issues early.

### Configuration

Configured in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-yaml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Setup & Usage

```bash
# Install hooks (done by make setup)
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate

# Skip hooks for emergency commits
git commit -m "Emergency fix" --no-verify
```

## Code Coverage

### pytest-cov Integration

```bash
# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html

# Generate terminal coverage report
uv run pytest --cov=src --cov-report=term-missing

# Set minimum coverage threshold
uv run pytest --cov=src --cov-fail-under=80
```

### Coverage Configuration

Add to `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Makefile Commands

The project includes convenient Make targets:

```bash
make setup           # Setup development environment
make lint            # Run linting checks
make format          # Auto-format code
make pytest          # Run tests
make pytest-integration  # Run integration tests
make coverage        # Generate coverage report
make all-checks      # Run all quality checks
make clean           # Clean build artifacts
```

## CI/CD Integration

The toolchain integrates with GitHub Actions for automated quality checks:

```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: uv sync --all-groups

- name: Run linting
  run: uv run ruff check .

- name: Run tests
  run: uv run pytest --cov=src
```

## Performance Optimizations

### Ruff vs. Traditional Tools

| Tool | Speed | Features |
|------|-------|----------|
| Ruff | **10-100x faster** | Linting + Formatting |
| flake8 + black + isort | Baseline | Separate tools |

### pytest Optimizations

```bash
# Run tests in parallel
uv run pytest -n auto  # Requires pytest-xdist

# Only run failed tests
uv run pytest --lf

# Exit on first failure
uv run pytest -x
```

## Troubleshooting

### Common Issues

**Ruff not found:**
```bash
uv sync --all-groups
```

**Pre-commit hooks failing:**
```bash
pre-commit clean
pre-commit install
pre-commit run --all-files
```

**Tests not discovered:**
```bash
# Check pytest configuration
uv run pytest --collect-only
```

**Import errors in tests:**
```bash
# Ensure package is installed in development mode
uv sync --all-groups
```

## Customization

### Adding New Tools

To add a new tool (e.g., mypy):

1. Add to `pyproject.toml`:
```toml
[dependency-groups]
dev = [
    # ... existing deps
    "mypy>=1.0.0",
]
```

2. Add Make target:
```makefile
typecheck: ## Run type checking
	uv run mypy src/
```

3. Add to pre-commit:
```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.0.0
  hooks:
    - id: mypy
```

4. Update CI workflow to include the new check.