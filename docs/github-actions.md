# GitHub Actions CI/CD

This project includes automated CI/CD workflows using GitHub Actions for testing, documentation deployment, and quality assurance.

## Available Workflows

### Documentation Deployment (`.github/workflows/docs.yml`)

Automatically builds and deploys documentation to GitHub Pages.

**Triggers:**
- Push to `main` branch (with doc changes)
- Pull requests (build only, no deployment)
- Manual trigger via `workflow_dispatch`

**Features:**
- Uses UV for fast dependency installation
- Builds documentation with MkDocs Material
- Deploys to GitHub Pages with proper permissions
- Only deploys from main branch

**Setup Requirements:**
1. Enable GitHub Pages in repository settings
2. Set Pages source to "GitHub Actions"
3. Ensure repository has proper permissions

## Workflow Configuration

### Documentation Workflow Details

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/docs.yml'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write
```

**Key Features:**
- **Path filtering**: Only runs when documentation files change
- **Proper permissions**: Minimal required permissions for security
- **Concurrency control**: Prevents multiple deployments running simultaneously
- **UV integration**: Uses UV for fast, reliable dependency management

### Jobs Breakdown

#### Build Job
1. **Checkout code** with full history (`fetch-depth: 0`)
2. **Setup Python 3.11** using official action
3. **Install UV** using official UV setup action
4. **Install dependencies** with `uv sync --all-groups`
5. **Build documentation** with strict mode enabled
6. **Upload artifacts** for Pages deployment

#### Deploy Job
1. **Conditional execution**: Only runs on main branch pushes
2. **GitHub Pages environment**: Proper environment configuration
3. **Deploy to Pages**: Uses official Pages deployment action

## Issue Templates

The project includes comprehensive issue templates for better project management.

### Bug Report Template (`.github/ISSUE_TEMPLATE/bug_report.yml`)

Structured form for bug reports including:
- **Bug description** with clear formatting
- **Reproduction steps** in numbered format
- **Expected vs actual behavior** comparison
- **Environment details** (OS, Python version, etc.)
- **Log output** with proper syntax highlighting
- **Validation checklist** to ensure quality submissions

### Feature Request Template (`.github/ISSUE_TEMPLATE/feature_request.yml`)

Comprehensive feature request form with:
- **Problem statement** explaining the need
- **Proposed solution** with detailed description
- **Alternative solutions** for comparison
- **Use case scenarios** to justify the feature
- **Priority levels** (Low, Medium, High, Critical)
- **Implementation willingness** checkbox

### Template Configuration (`.github/ISSUE_TEMPLATE/config.yml`)

- **Disables blank issues** to ensure structured submissions
- **Contact links** for discussions and documentation
- **Community guidelines** integration

## Setting Up Additional Workflows

### CI Testing Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install UV
        uses: astral-sh/setup-uv@v3
      
      - name: Install dependencies
        run: uv sync --all-groups
      
      - name: Run linting
        run: uv run ruff check .
      
      - name: Run formatting check
        run: uv run ruff format --check .
      
      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Release Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install UV
        uses: astral-sh/setup-uv@v3
      
      - name: Build package
        run: uv build
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

### Security Scanning Workflow

Create `.github/workflows/security.yml`:

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday 2 AM

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install UV
        uses: astral-sh/setup-uv@v3
      
      - name: Install dependencies
        run: uv sync --all-groups
      
      - name: Run Bandit security scan
        run: uv run bandit -r src/
      
      - name: Run Safety dependency scan
        run: uv run safety check
```

## Secrets Management

### Required Secrets

For full CI/CD functionality, add these secrets in repository settings:

```bash
PYPI_API_TOKEN          # For PyPI publishing
CODECOV_TOKEN          # For code coverage reporting
```

### Adding Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add name and value
4. Use in workflows: `${{ secrets.SECRET_NAME }}`

## Workflow Optimization

### UV Integration Benefits

Using UV in workflows provides:
- **10-100x faster** dependency installation
- **Reliable dependency resolution** with lock files
- **Consistent environments** across local and CI
- **Reduced workflow runtime** and costs

### Caching Strategies

```yaml
- name: Cache UV dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

### Matrix Testing

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.11", "3.12"]
```

## Monitoring and Notifications

### Workflow Status Badges

Add to README.md:

```markdown
![CI](https://github.com/username/repo/workflows/CI/badge.svg)
![Docs](https://github.com/username/repo/workflows/Deploy%20Documentation/badge.svg)
```

### Slack Notifications

```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

## Troubleshooting

### Common Issues

**Workflow not triggering:**
- Check branch protection rules
- Verify file paths in `paths:` filters
- Ensure proper YAML syntax

**Permission errors:**
- Check repository permissions
- Verify GITHUB_TOKEN scope
- Update workflow permissions block

**UV installation issues:**
- Use latest `astral-sh/setup-uv` action version
- Check Python version compatibility
- Verify UV cache configuration

**Documentation deployment failures:**
- Ensure GitHub Pages is enabled
- Check Pages source is set to "GitHub Actions"
- Verify MkDocs configuration is valid

### Debugging Workflows

```yaml
- name: Debug Environment
  run: |
    echo "Python version: $(python --version)"
    echo "UV version: $(uv --version)"
    echo "Working directory: $(pwd)"
    echo "Files: $(ls -la)"
```

### Local Testing

Test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Test workflow
act push

# Test specific job
act -j test
```

## Best Practices

### Workflow Design
- **Use path filters** to avoid unnecessary runs
- **Implement proper caching** for dependencies
- **Use matrix testing** for multiple environments
- **Set appropriate timeouts** to prevent hanging jobs

### Security
- **Use minimal permissions** required for each job
- **Pin action versions** to specific tags or SHAs
- **Store sensitive data** in repository secrets
- **Regular security updates** for actions

### Performance
- **Use UV** for fast dependency management
- **Cache dependencies** between runs
- **Parallelize independent jobs**
- **Optimize Docker layer caching** if using containers

### Maintenance
- **Keep actions updated** to latest versions
- **Monitor workflow run times** and optimize bottlenecks
- **Review and update** security policies regularly
- **Document workflow purposes** and dependencies