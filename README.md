# uv-starter

A modern Python project starter template using UV with a complete development toolchain.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo>
cd uv-starter
make setup

# Run the example
uv run -m uv_starter.demo_module

# Start the API server
uv run fastapi dev src/uv_starter/api/main.py

# Run tests
make pytest

# Check code quality
make lint
```

## 🛠️ Toolchain Overview

This template includes a production-ready development environment:

### **Package Management**
- **[UV](https://docs.astral.sh/uv/)** - Ultra-fast Python package manager (replaces pip/poetry)
- **Lock file** (`uv.lock`) for reproducible builds
- **Dependency groups** for dev/test separation

### **API Development**
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs

### **Code Quality & Testing**
- **[Ruff](https://docs.astral.sh/ruff/)** - Lightning-fast linter and formatter
- **[pytest](https://pytest.org/)** - Modern testing framework with coverage
- **[pre-commit](https://pre-commit.com/)** - Git hooks for automated quality checks

### **Configuration Management**
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** - Type-safe environment variable handling
- **`.env` file support** - Local development configuration

### **Documentation**
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** - Beautiful documentation site
- **GitHub Pages** - Automatic documentation deployment

### **CI/CD & Automation**
- **GitHub Actions** - Automated testing and documentation deployment
- **Docker support** - Container-ready configuration
- **Makefile** - Common development commands

## 📁 Project Structure

```
├── src/uv_starter/          # Main package code
│   ├── api/                # FastAPI application
│   │   ├── __init__.py     
│   │   └── main.py         # API endpoints
│   ├── demo_module.py      # Example module
│   └── config.py           # Settings management
├── tests/                  # Test files
│   ├── api/                # API tests
│   └── unit_tests/         # Unit tests
├── docs/                   # Documentation source
├── .github/                # GitHub Actions & templates
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── Makefile                # Development commands
└── Dockerfile              # Container configuration
```

## 🔧 Available Commands

```bash
make setup          # Setup development environment
make pytest         # Run tests
make lint           # Check code quality
make format         # Auto-format code
make docs-serve     # Serve documentation locally
make docs-deploy    # Deploy docs to GitHub Pages
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **[UV Setup & Usage](docs/uv.md)** - Package management with UV
- **[Development Toolchain](docs/toolchain.md)** - Code quality tools setup
- **[Configuration Management](docs/configuration.md)** - Environment variables & settings
- **[GitHub Actions](docs/github-actions.md)** - CI/CD workflows

## 🤝 Contributing

1. Create an issue using our templates
2. Fork the repository
3. Create a feature branch
4. Make your changes with tests
5. Submit a pull request

See our [issue templates](.github/ISSUE_TEMPLATE/) for bug reports and feature requests.
