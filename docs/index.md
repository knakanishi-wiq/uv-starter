# UV Starter

A modern Python project starter template using UV with a complete development toolchain.

## Overview

UV Starter provides a production-ready foundation for Python projects, featuring ultra-fast package management with UV and a comprehensive development toolchain focused on code quality, testing, and automation.

## Key Features

### ⚡ **Ultra-Fast Package Management**
- **[UV](https://docs.astral.sh/uv/)** - 10-100x faster than pip
- Lock file support for reproducible builds
- Dependency groups for clean separation

### 🛠️ **Complete Development Toolchain**
- **[Ruff](https://docs.astral.sh/ruff/)** - Lightning-fast linting and formatting
- **[pytest](https://pytest.org/)** - Modern testing framework with coverage
- **[pre-commit](https://pre-commit.com/)** - Automated quality checks

### ⚙️ **Type-Safe Configuration**
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** - Environment variable management
- `.env` file support with validation
- Production-ready defaults

### 📚 **Beautiful Documentation**
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** - Modern documentation site
- Automatic deployment to GitHub Pages
- Search, syntax highlighting, and responsive design

### 🚀 **CI/CD Ready**
- GitHub Actions workflows for testing and deployment
- Docker support with optimized builds
- Comprehensive issue templates

## Quick Start

Get started in minutes:

```bash
# Clone the template
git clone https://github.com/your-username/uv-starter.git my-project
cd my-project

# Setup development environment
make setup

# Run the example
uv run src/uv-starter/hello.py

# Run tests
make pytest

# Check code quality
make lint
```

## Project Structure

```
├── src/uv-starter/          # Main package code
│   ├── hello.py            # Example module
│   └── config.py           # Settings management
├── tests/                  # Test files
├── docs/                   # Documentation source
├── .github/                # GitHub Actions & templates
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── Makefile                # Development commands
├── mkdocs.yml              # Documentation config
└── Dockerfile              # Container configuration
```

## Why UV Starter?

### **Performance First**
UV's Rust-based implementation provides:
- **10-100x faster** dependency resolution than pip
- **2-10x faster** installation than poetry
- Parallel downloads and efficient caching

### **Developer Experience**
Modern tooling that just works:
- **Zero configuration** - Sensible defaults out of the box
- **Type safety** - Catch errors before runtime
- **Automation** - Pre-commit hooks and CI/CD workflows

### **Production Ready**
Built for real-world projects:
- **Security scanning** with Bandit and Safety
- **Docker optimization** with multi-stage builds
- **Configuration management** for different environments

## Getting Help

- **[Documentation](https://your-username.github.io/uv-starter/)** - Complete guides and API reference
- **[GitHub Issues](https://github.com/your-username/uv-starter/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/your-username/uv-starter/discussions)** - Community Q&A

## Next Steps

Ready to build something awesome? Start with these guides:

1. **[UV Package Management](uv.md)** - Learn UV basics and commands
2. **[Development Toolchain](toolchain.md)** - Configure your development environment
3. **[Configuration Management](configuration.md)** - Handle settings and environment variables
4. **[GitHub Actions](github-actions.md)** - Set up CI/CD workflows

---

*Happy coding! 🐍✨*