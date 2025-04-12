# 🔄 Migrating from Poetry to Uv: A Comprehensive Guide

<a id="top"></a>

## 📋 Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Migration Steps](#migration-steps)
  - [Step 1: Install Uv](#step-1)
  - [Step 2: Create a Backup](#step-2)
  - [Step 3: Export Dependencies](#step-3)
  - [Step 4: Convert pyproject.toml](#step-4)
  - [Step 5: Create a Virtual Environment](#step-5)
  - [Step 6: Install Dependencies](#step-6)
  - [Step 7: Test Your Application](#step-7)
  - [Step 8: Update CI/CD Pipelines](#step-8)
  - [Step 9: Remove Poetry Files](#step-9)
- [Common Issues and Solutions](#common-issues)
- [References](#references)

<a id="introduction"></a>

## 📢 Introduction

[🔼 Back to TOC](#top)

Astral Uv is a modern Python package manager and installer built with Rust, offering significant performance improvements over existing tools like Poetry and pip. This guide provides a detailed, step-by-step process for migrating your Python project from Poetry to Uv while preserving all your dependencies, scripts, and configurations.

Uv brings several advantages:

- ⚡ Significantly faster package installation and dependency resolution
- 🔍 Enhanced compatibility with PEP standards
- 🔒 Improved security and reliability
- 🧩 Simpler dependency management

<a id="prerequisites"></a>

## 🛠️ Prerequisites

[🔼 Back to TOC](#top)

Before starting the migration process, ensure you have:

- An existing Poetry project with `pyproject.toml` and `poetry.lock` files
- Python 3.7+ installed
- Administrative permissions to install new tools
- A backup of your project (preferably in a version control system)

<a id="migration-steps"></a>

## 🚀 Migration Steps

[🔼 Back to TOC](#top)

<a id="step-1"></a>

### Step 1: Install Uv

[🔼 Back to TOC](#top)

First, install Uv. There are several methods available:

#### Using pip (recommended for most users):

```bash
pip install uv
```

#### Using Homebrew (macOS):

```bash
brew install astral/tap/uv
```

#### Using the installer script (Unix-like systems):

```bash
curl -sSf https://astral.sh/uv/install.sh | sh
```

Verify the installation was successful:

```bash
uv --version
```

You should see output similar to: `uv 0.6.13 (a0f5c7250 2025-04-07)`

<a id="step-2"></a>

### Step 2: Create a Backup

[🔼 Back to TOC](#top)

Always create backups before beginning a migration:

```bash
# Backup your pyproject.toml
cp pyproject.toml pyproject.toml.backup

# Backup your poetry.lock if it exists
if [ -f poetry.lock ]; then
    cp poetry.lock poetry.lock.backup
fi
```

<a id="step-3"></a>

### Step 3: Export Dependencies

[🔼 Back to TOC](#top)

If you have Poetry installed and working, export your dependencies to a requirements file:

```bash
poetry export --without-hashes -f requirements.txt > requirements.txt

# If you have dev dependencies
poetry export --without-hashes --with dev -f requirements.txt > requirements-dev.txt
```

If Poetry is not available, you'll need to manually extract dependencies from your `pyproject.toml` file in the next step.

<a id="step-4"></a>

### Step 4: Convert pyproject.toml

[🔼 Back to TOC](#top)

Create a new Uv-compatible `pyproject.toml` file. Here's a template that you can adapt to your project:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-package-name"  # Replace with your package name
version = "0.1.0"  # Replace with your version
description = "Your package description"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
readme = "README.md"
license = {text = "MIT"}  # Replace with your license
requires-python = ">=3.7"  # Adjust as needed for your project
dependencies = [
    # List your dependencies here, for example:
    # "requests>=2.25.1",
    # "numpy>=1.20.0",
]

[project.optional-dependencies]
# Define optional dependency groups, equivalent to Poetry's extras
dev = [
    # Development dependencies
]

[project.scripts]
# Define console scripts here
# my-script = "my_package.module:function"

[tool.uv]
link-mode = "copy"

[tool.hatch.build.targets.wheel]
packages = ["src/your_package"]  # Adjust to match your package structure

[tool.hatch.build.targets.sdist]
include = [
    # Include additional files in the source distribution
]

[tool.hatch.metadata]
allow-direct-references = true
```

Key differences between Poetry and Uv/PEP 621 format:

| Poetry Format | Uv/PEP 621 Format |
|---------------|-------------------|
| `[tool.poetry]` | `[project]` |
| `[tool.poetry.dependencies]` | `dependencies = []` under `[project]` |
| `[tool.poetry.dev-dependencies]` | `[project.optional-dependencies]` |
| `[tool.poetry.scripts]` | `[project.scripts]` |

For a real-world example, here's a more complete conversion from Poetry to Uv format:

#### Original Poetry Format:

```toml
[tool.poetry]
name = "example-app"
version = "1.2.3"
description = "An example application"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.1"
pandas = "^1.5.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"
black = "^22.10.0"

[tool.poetry.scripts]
example-cli = "example_app.cli:main"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

#### Converted Uv/PEP 621 Format:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example-app"
version = "1.2.3"
description = "An example application"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.1",
    "pandas>=1.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.10.0",
]

[project.scripts]
example-cli = "example_app.cli:main"

[tool.uv]
link-mode = "copy"

[tool.hatch.build.targets.wheel]
packages = ["example_app"]
```

Note the following key changes:
- Dependencies moved from `[tool.poetry.dependencies]` to arrays under `[project].dependencies`
- Version constraints use `>=` instead of `^`
- Author format changes from strings to objects with name and email fields
- Dev dependencies moved to `[project.optional-dependencies].dev`

<a id="step-5"></a>

### Step 5: Create a Virtual Environment

[🔼 Back to TOC](#top)

Create a new virtual environment using Uv:

```bash
uv venv --python 3.10  # Replace with your target Python version
```

This will create a `.venv` directory in your project. Activate it:

#### On Windows:

```bash
.venv\Scripts\activate
```

#### On macOS/Linux:

```bash
source .venv/bin/activate
```

<a id="step-6"></a>

### Step 6: Install Dependencies

[🔼 Back to TOC](#top)

Install your project dependencies using one of these methods:

#### From the updated pyproject.toml:

```bash
uv pip install -e .
```

#### From the exported requirements file:

```bash
uv pip install -r requirements.txt
```

#### For development dependencies:

```bash
# If using pyproject.toml with optional dependencies
uv pip install -e ".[dev]"

# Or if using a separate requirements file
uv pip install -r requirements-dev.txt
```

After installing dependencies, you can use `uv sync` to ensure all dependencies are synced to your environment:

```bash
uv sync
```

<a id="step-7"></a>

### Step 7: Test Your Application

[🔼 Back to TOC](#top)

Verify that your application works correctly with the new package manager:

1. Run your test suite:
   ```bash
   pytest
   ```

2. Run your application locally:
   ```bash
   python -m your_package
   ```

3. Check that all entry points and scripts work correctly.

If you encounter issues, see the [Common Issues](#common-issues) section.

<a id="step-8"></a>

### Step 8: Update CI/CD Pipelines

[🔼 Back to TOC](#top)

Update your CI/CD configuration files to use Uv instead of Poetry. Here are examples for common CI systems:

#### GitHub Actions:

```yaml
name: Python tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - name: Install uv
      run: pip install uv
    - name: Create virtual environment
      run: uv venv
    - name: Install dependencies
      run: uv pip install -e ".[dev]"
    - name: Run tests
      run: pytest
```

#### GitLab CI:

```yaml
test:
  image: python:3.10
  before_script:
    - pip install uv
    - uv venv
    - source .venv/bin/activate
    - uv pip install -e ".[dev]"
  script:
    - pytest
```

#### CircleCI:

```yaml
version: 2.1
jobs:
  build-and-test:
    docker:
      - image: cimg/python:3.10
    steps:
      - checkout
      - run:
          name: Install uv
          command: pip install uv
      - run:
          name: Create virtual environment
          command: uv venv
      - run:
          name: Install dependencies
          command: |
            source .venv/bin/activate
            uv pip install -e ".[dev]"
      - run:
          name: Run tests
          command: |
            source .venv/bin/activate
            pytest
```

<a id="step-9"></a>

### Step 9: Remove Poetry Files

[🔼 Back to TOC](#top)

Once you're confident the migration is successful, you can remove Poetry-specific files:

```bash
# Remove poetry.lock
rm poetry.lock

# Optional: Remove Poetry from your development environment
pip uninstall poetry -y
```

Update your documentation and contributor guidelines to reflect the use of Uv instead of Poetry.

<a id="common-issues"></a>

## ⚠️ Common Issues and Solutions

[🔼 Back to TOC](#top)

### Hardlink Warnings

**Problem:** You see warnings about hardlinks failing:
```
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
```

**Solution:** Add the `link-mode = "copy"` setting in the `[tool.uv]` section of your pyproject.toml, or set the environment variable:
```bash
export UV_LINK_MODE=copy
```

### Dependency Resolution Errors

**Problem:** Uv cannot resolve dependencies that worked with Poetry.

**Solution:**
1. Try loosening version constraints (use `>=` instead of strict versions)
2. Check for direct GitHub/URL dependencies, which may need special handling
3. Install problem dependencies individually:
   ```bash
   uv pip install problematic-package==specific-version
   ```

### Missing Scripts or Entry Points

**Problem:** Command-line scripts defined in Poetry aren't available after migration.

**Solution:** Ensure you've correctly defined scripts in the `[project.scripts]` section and reinstall your package with:
```bash
uv pip install -e .
```

### Package Build Issues

**Problem:** Your package doesn't build correctly with the new build backend.

**Solution:**
1. Check the `[tool.hatch.build.targets.wheel]` section to ensure it points to the correct package directory
2. Verify any include/exclude patterns in the build configuration
3. Try building manually to see detailed errors:
   ```bash
   uv pip install build
   python -m build
   ```

<a id="references"></a>

## 📚 References

[🔼 Back to TOC](#top)

- [Uv Official Documentation](https://github.com/astral-sh/uv)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Hatchling Documentation](https://hatch.pypa.io/latest/config/build/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## Claude.ai created this a comprehensive guide to migrating from Poetry to Uv. The document includes all the necessary steps with detailed explanations, formatted with your requested navigation elements (table of contents, anchors, "Back to TOC" links) and includes helpful icons for visual organization.

### The guide covers:

1. An introduction to Uv and its benefits
1. Prerequisites before migration
1. A detailed 9-step migration process:

    - Installing Uv
    - Creating backups
    - Exporting dependencies
    - Converting pyproject.toml (with examples)
    - Creating a virtual environment
    - Installing dependencies
    - Testing the application
    - Updating CI/CD pipelines
    - Cleaning up Poetry artifacts
