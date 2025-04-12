# 🔄 Complete Guide to Migrating pdf-markdown-converter from Poetry to Uv

<a id="top"></a>

## 📋 Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Migration Steps](#migration-steps)
  - [Step 1: Install Uv](#step-1)
  - [Step 2: Create a Backup](#step-2)
  - [Step 3: Convert pyproject.toml](#step-3)
  - [Step 4: Create a Virtual Environment](#step-4)
  - [Step 5: Install Dependencies](#step-5)
  - [Step 6: Test Your Application](#step-6)
- [Fixing Test Issues](#fixing-test-issues)
  - [Update pytest.ini](#update-pytest-ini)
  - [Fix Permission Errors](#fix-permission-errors)
  - [Handle External Dependencies](#handle-external-dependencies)
  - [Fix Multiprocessing Tests](#fix-multiprocessing-tests)
- [Creating a Local Test Dataset](#local-test-dataset)
- [Cleanup and Final Steps](#cleanup)
- [Daily Development with Uv](#daily-development)
- [Troubleshooting](#troubleshooting)

<a id="introduction"></a>

## 📢 Introduction

[🔼 Back to TOC](#top)

This guide provides a step-by-step process for migrating your Python project from Poetry to Uv. Uv is a modern package manager built in Rust that offers significant performance improvements over Poetry, especially for large projects.

<a id="prerequisites"></a>

## 🛠️ Prerequisites

[🔼 Back to TOC](#top)

Before you begin, ensure you have:

- An existing Poetry project with `pyproject.toml` and `poetry.lock` files
- Python 3.7+ installed
- Administrator privileges to install new tools
- A backup of your project (preferably in a version control system)

<a id="migration-steps"></a>

## 🚀 Migration Steps

[🔼 Back to TOC](#top)

<a id="step-1"></a>

### Step 1: Install Uv

[🔼 Back to TOC](#top)

First, install Uv using pip:

```bash
pip install uv
```

Verify the installation:

```bash
uv --version
```

You should see output like: `uv 0.6.13 (a0f5c7250 2025-04-07)`

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

### Step 3: Convert pyproject.toml

[🔼 Back to TOC](#top)

Create a new Uv-compatible `pyproject.toml` file:

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
requires-python = ">=3.7"  # Adjust as needed
dependencies = [
    # List your dependencies here with versions
    # "requests>=2.28.1",
]

[project.optional-dependencies]
# Define optional dependency groups
dev = [
    # Development dependencies
]
test = [
    # Test dependencies
]

[project.scripts]
# Define console scripts here
# my-script = "my_package.module:function"

[tool.uv]
link-mode = "copy"

[tool.hatch.build.targets.wheel]
packages = ["src/your_package"]  # Adjust to match your package structure
```

Fill in the dependencies section based on your Poetry dependencies. Convert from Poetry format to Uv/PEP 621 format:

| Poetry Format | Uv/PEP 621 Format |
|---------------|-------------------|
| `[tool.poetry]` | `[project]` |
| `[tool.poetry.dependencies]` | `dependencies = []` under `[project]` |
| `[tool.poetry.dev-dependencies]` | `[project.optional-dependencies]` |
| `[tool.poetry.scripts]` | `[project.scripts]` |

Version constraints should use `>=` instead of Poetry's `^`.

<a id="step-4"></a>

### Step 4: Create a Virtual Environment

[🔼 Back to TOC](#top)

Create a new virtual environment using Uv:

```bash
uv venv --python 3.13  # Replace with your target Python version
```

Activate it:

```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

<a id="step-5"></a>

### Step 5: Install Dependencies

[🔼 Back to TOC](#top)

Install your project dependencies:

```bash
# Install the project and all dependencies
uv pip install -e .

# For development dependencies
uv pip install -e ".[dev]"

# For test dependencies
uv pip install -e ".[test]"
```

After installing dependencies, sync your environment:

```bash
uv sync
```

<a id="step-6"></a>

### Step 6: Test Your Application

[🔼 Back to TOC](#top)

Run your tests to verify the migration:

```bash
pytest
```

Also check that your application runs correctly:

```bash
python -m your_package
```

<a id="fixing-test-issues"></a>

## 🔧 Fixing Test Issues

[🔼 Back to TOC](#top)

After migrating to Uv, you might encounter test issues, particularly if your tests depend on external resources.

<a id="update-pytest-ini"></a>

### Update pytest.ini

Create or update your `pytest.ini` file to register custom markers:

```ini
[pytest]
markers =
    external_data: Marks tests that require external data
    config: Marks tests with specific configuration
    filename: Marks tests with specific test file
    output_format: Marks tests with specific output format
```

To create this file on Windows PowerShell:

```powershell
echo "[pytest]" > pytest.ini
echo "markers =" >> pytest.ini
echo "    external_data: Marks tests that require external data" >> pytest.ini
echo "    config: Marks tests with specific configuration" >> pytest.ini
echo "    filename: Marks tests with specific test file" >> pytest.ini
echo "    output_format: Marks tests with specific output format" >> pytest.ini
```

<a id="fix-permission-errors"></a>

### Fix Permission Errors

If you encounter permission errors with temporary files (especially on Windows), update your fixtures:

```python
@pytest.fixture(scope="function")
def temp_image():
    # Create a temporary file path first
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        temp_path = f.name
    
    # Create and save the image
    img = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Hello, World!", fill="black")
    img.save(temp_path)
    
    # Yield the file path
    yield temp_path
    
    # Clean up after test
    try:
        os.remove(temp_path)
    except:
        pass
```

<a id="handle-external-dependencies"></a>

### Handle External Dependencies

If your tests depend on external datasets (like "datalab-to/pdfs"), you can:

1. **Skip these tests temporarily**:

Update your `conftest.py` to skip tests that require external resources:

```python
@pytest.fixture(scope="session")
def pdf_dataset():
    # Skip tests that require the external dataset
    pytest.skip("Skipping tests that require the external 'datalab-to/pdfs' dataset")
```

2. **Create a mock dataset**:

```python
@pytest.fixture(scope="session")
def pdf_dataset():
    class MockDataset:
        def __init__(self):
            self.data = {
                'filename': ['adversarial.pdf', 'adversarial_rot.pdf'],
                'pdf': [b'mock pdf content', b'mock pdf content']
            }
        
        def __getitem__(self, key):
            return self.data[key]
    
    return MockDataset()
```

<a id="fix-multiprocessing-tests"></a>

### Fix Multiprocessing Tests

For tests using multiprocessing with external resources:

```python
# Create a file in tests/builders/test_overriding_mp_skip.py
import pytest
pytest.skip('Skipping multiprocessing test that requires external datasets', allow_module_level=True)
```

Or modify the test to check for test files first:

```python
def test_overriding_mp():
    # Check for test files first
    import os
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    pdf_list = ["adversarial.pdf", "adversarial_rot.pdf"]
    
    all_files_exist = all(os.path.exists(os.path.join(test_data_dir, pdf)) for pdf in pdf_list)
    if not all_files_exist:
        import pytest
        pytest.skip("Required test files not available")
    
    # Rest of the test...
```

<a id="local-test-dataset"></a>

## 📊 Creating a Local Test Dataset

[🔼 Back to TOC](#top)

For a more permanent solution, create a local test dataset:

1. **Create a test data directory**:

```bash
mkdir -p tests/data
```

2. **Add sample PDFs** for testing in this directory.

3. **Update the pdf_dataset fixture** in `conftest.py`:

```python
@pytest.fixture(scope="session")
def pdf_dataset():
    class LocalDataset:
        def __init__(self):
            self.data = {
                'filename': [],
                'pdf': []
            }
            # Load all PDFs from the test data directory
            test_data_dir = os.path.join(os.path.dirname(__file__), "data")
            if os.path.exists(test_data_dir):
                for filename in os.listdir(test_data_dir):
                    if filename.endswith('.pdf'):
                        self.data['filename'].append(filename)
                        with open(os.path.join(test_data_dir, filename), 'rb') as f:
                            self.data['pdf'].append(f.read())
        
        def __getitem__(self, key):
            return self.data[key]
    
    return LocalDataset()
```

4. **Update util functions** to work with local files:

```python
# In tests/utils.py
def setup_pdf_provider(pdf, config):
    from marker.providers.pdf import PdfProvider
    import os
    
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")
    test_file_path = os.path.join(test_data_dir, pdf)
    
    if os.path.exists(test_file_path):
        return PdfProvider(test_file_path, config)
    else:
        import pytest
        pytest.skip(f"Test file {pdf} not available")
```

<a id="cleanup"></a>

## 🧹 Cleanup and Final Steps

[🔼 Back to TOC](#top)

Once your migration is successful:

1. **Remove Poetry artifacts**:

```bash
# Remove poetry.lock
rm poetry.lock

# Optionally uninstall Poetry
pip uninstall poetry -y
```

2. **Update documentation**:

Update your README.md and other documentation to reflect the new Uv workflow.

3. **Update CI/CD pipelines**:

If you use CI/CD pipelines, update them to use Uv:

```yaml
# GitHub Actions example
name: Tests

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
        python-version: '3.13'
    - name: Install uv
      run: pip install uv
    - name: Install dependencies
      run: |
        uv venv
        source .venv/bin/activate
        uv pip install -e ".[dev]"
    - name: Run tests
      run: |
        source .venv/bin/activate
        pytest
```

<a id="daily-development"></a>

## 💻 Daily Development with Uv

[🔼 Back to TOC](#top)

Here are the common Uv commands for daily development:

### Installing Dependencies

```bash
# Install all dependencies
uv pip install -e ".[dev]"
```

### Adding New Dependencies

```bash
# Add a package
uv add package_name
```

### Removing Dependencies

```bash
# Remove a package
uv remove package_name
```

### Updating Dependencies

```bash
# Sync your environment
uv sync
```

<a id="troubleshooting"></a>

## ⚠️ Troubleshooting

[🔼 Back to TOC](#top)

### Common Issues and Solutions

1. **Permission Errors with Temporary Files**

   On Windows, use `delete=False` with `tempfile.NamedTemporaryFile` and manually clean up.

2. **Missing Dependencies**

   Ensure you've installed all dependency groups:
   ```bash
   uv pip install -e ".[dev,test]"
   ```

3. **Path Issues in Windows**

   Use `os.path.join()` instead of hardcoded forward slashes.

4. **Environment Activation Problems**

   Make sure you're not mixing different virtual environment tools. Use only Uv's commands.

5. **Test Hanging**

   If a test is hanging, it might be trying to access external resources. Use `-v` flag to identify which test is hanging and skip or mock it.

---

By following this guide, you should be able to successfully migrate your project from Poetry to Uv, fix common test issues, and set up a robust development environment.