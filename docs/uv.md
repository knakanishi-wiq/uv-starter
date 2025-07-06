# UV Package Management

UV is an extremely fast Python package manager and project manager, written in Rust. It serves as a drop-in replacement for pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more.

## Installation

UV is already configured in this project. If you need to install UV separately:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv
```

## Project Setup

### Initial Setup
```bash
# Install all dependencies including dev dependencies
uv sync --all-groups

# Install only production dependencies
uv sync
```

### Adding Dependencies

```bash
# Add a production dependency
uv add requests

# Add a development dependency
uv add --group dev pytest-mock

# Add with version constraints
uv add "fastapi>=0.100.0"
```

### Removing Dependencies

```bash
# Remove a dependency
uv remove requests

# Remove from specific group
uv remove --group dev pytest-mock
```

## Running Code

```bash
# Run a Python script
uv run src/uv-starter/hello.py

# Run a module
uv run -m pytest

# Run with environment variables
uv run --env-file .env.production python script.py
```

## Virtual Environment Management

```bash
# UV automatically manages virtual environments
# but you can access them directly:

# Show virtual environment path
uv venv --python 3.11

# Activate virtual environment (if needed)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## Lock File Management

UV uses `uv.lock` for reproducible builds:

```bash
# Update lock file
uv lock

# Update specific dependency
uv lock --upgrade-package requests

# Install from lock file (automatic with uv sync)
uv sync
```

## Configuration

UV configuration is primarily in `pyproject.toml`:

```toml
[project]
dependencies = [
    "loguru>=0.7.3",
    "pydantic>=2.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3.5",
    "ruff>=0.11.2",
]
```

## Common Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install dependencies from lock file |
| `uv sync --all-groups` | Install all dependency groups |
| `uv add <package>` | Add a new dependency |
| `uv remove <package>` | Remove a dependency |
| `uv run <command>` | Run command in virtual environment |
| `uv lock` | Update lock file |
| `uv tree` | Show dependency tree |
| `uv pip list` | List installed packages |

## Migration from Other Tools

### From Poetry
- `poetry install` → `uv sync --all-groups`
- `poetry add <package>` → `uv add <package>`
- `poetry run <command>` → `uv run <command>`

### From pip + requirements.txt
- `pip install -r requirements.txt` → `uv sync`
- `pip install <package>` → `uv add <package>`

### From pip-tools
- `pip-sync requirements.txt` → `uv sync`
- `pip-compile requirements.in` → `uv lock`

## Performance Benefits

UV is significantly faster than traditional Python package managers:

- **10-100x faster** than pip for package resolution
- **2-10x faster** than poetry for dependency installation
- **Parallel downloads** and installations
- **Disk space efficient** with global package cache

## Troubleshooting

### Common Issues

**Lock file conflicts:**
```bash
# Regenerate lock file
rm uv.lock
uv lock
```

**Dependency resolution errors:**
```bash
# Clear cache and retry
uv cache clean
uv sync --all-groups
```

**Python version issues:**
```bash
# Specify Python version
uv sync --python 3.11
```

## Advanced Usage

### Custom Indices
```bash
# Add custom package index
uv add --index-url https://custom.pypi.org/simple/ custom-package
```

### Environment Variables
```bash
# Use different lock file
UV_LOCK_FILE=production.lock uv sync

# Disable lock file
UV_NO_SYNC=1 uv run script.py
```

## Integration with Make

The project includes Make targets that wrap UV commands:

```bash
make setup    # uv sync --all-groups && pre-commit install
make pytest   # uv run pytest
```

This provides a consistent interface while leveraging UV's speed underneath.