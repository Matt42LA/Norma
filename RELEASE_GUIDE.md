# Norma ORM Release Guide

This guide provides step-by-step instructions for releasing Norma ORM to PyPI.

## 🚀 Quick Release

### Prerequisites

1. **Python Environment**: Python 3.8+ with pip
2. **PyPI Account**: Register at [pypi.org](https://pypi.org/account/register/)
3. **Test PyPI Account**: Register at [test.pypi.org](https://test.pypi.org/account/register/) (recommended)

### Step 1: Install Build Tools

```bash
pip install --upgrade build twine
```

### Step 2: Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### Step 3: Build the Package

```bash
python -m build
```

This creates:
- `dist/norma_orm-0.1.0-py3-none-any.whl` (wheel distribution)
- `dist/norma_orm-0.1.0.tar.gz` (source distribution)

### Step 4: Verify the Package

```bash
twine check dist/*
```

### Step 5: Upload (Interactive)

```bash
python upload_to_pypi.py
```

Or manually:

```bash
# Test PyPI first (recommended)
twine upload --repository testpypi dist/*

# Then to real PyPI
twine upload dist/*
```

## 📋 Detailed Process

### 1. Version Management

The current version is defined in:
- `norma/__init__.py`: `__version__ = "0.1.0"`
- `pyproject.toml`: `version = "0.1.0"`  
- `setup.py`: `version="0.1.0"`

To update the version for a new release:

```bash
# Update all three files with the new version
sed -i '' 's/0\.1\.0/0.1.1/g' norma/__init__.py
sed -i '' 's/version = "0\.1\.0"/version = "0.1.1"/g' pyproject.toml
sed -i '' 's/version="0\.1\.0"/version="0.1.1"/g' setup.py
```

### 2. Package Configuration

The package is configured in `pyproject.toml`:

```toml
[project]
name = "norma-orm"
version = "0.1.0"
authors = [{name = "Geoion", email = "eski.yin@gmail.com"}]
description = "A modern Python ORM framework with dataclass support"
license = "MIT"
```

### 3. Dependencies

**Core Dependencies:**
- `pydantic>=2.0.0` - Data validation and serialization
- `typer>=0.9.0` - CLI framework
- `sqlalchemy>=2.0.0` - SQL database adapter
- `motor>=3.0.0` - MongoDB async driver
- `pymongo>=4.0.0` - MongoDB sync driver
- `asyncpg>=0.28.0` - PostgreSQL async driver
- `aiosqlite>=0.19.0` - SQLite async driver

**Optional Dependencies:**
- `postgres`: PostgreSQL support
- `cassandra`: Cassandra support  
- `dev`: Development tools
- `cli`: Rich CLI output

### 4. Build Process

The build process uses `pyproject.toml` configuration:

```bash
# Clean build
rm -rf build/ dist/ *.egg-info/

# Build both wheel and source distribution
python -m build

# Verify
twine check dist/*
```

### 5. Testing the Package

Before uploading to PyPI, test the package:

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate

# Install from local wheel
pip install dist/norma_orm-0.1.0-py3-none-any.whl

# Test basic functionality
python -c "from norma import NormaClient, BaseModel, Field; print('✅ Import successful')"

# Test CLI
norma --help

# Cleanup
deactivate
rm -rf test_env
```

### 6. Upload to Test PyPI

```bash
twine upload --repository testpypi dist/*
```

**Test PyPI URLs:**
- Package: https://test.pypi.org/project/norma-orm/
- Account: https://test.pypi.org/account/

**Test Installation:**
```bash
pip install --index-url https://test.pypi.org/simple/ norma-orm
```

### 7. Upload to Production PyPI

```bash
twine upload dist/*
```

**PyPI URLs:**
- Package: https://pypi.org/project/norma-orm/
- Account: https://pypi.org/account/

**Production Installation:**
```bash
pip install norma-orm
```

## 🔧 Authentication

### API Tokens (Recommended)

1. **Generate API Token**: Go to PyPI account settings
2. **Configure**: Create `.pypirc` file in home directory

```ini
[distutils]
index-servers = pypi testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR-API-TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-API-TOKEN
```

### Environment Variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN
```

## 📦 Package Structure

The distributed package includes:

```
norma-orm/
├── norma/
│   ├── __init__.py           # Main exports
│   ├── cli.py               # Command-line interface
│   ├── exceptions.py        # Exception classes
│   ├── adapters/            # Database adapters
│   │   ├── base_adapter.py
│   │   ├── sql_adapter.py
│   │   ├── mongo_adapter.py
│   │   └── cassandra_adapter.py
│   ├── core/                # Core components
│   │   ├── base_model.py
│   │   ├── client.py
│   │   └── field.py
│   └── schema/              # Schema generation
│       └── generator.py
├── examples/                # Usage examples
├── LICENSE                  # MIT license
├── README.md               # Documentation
└── pyproject.toml          # Package configuration
```

## 🔍 Quality Checks

Before releasing:

1. **Code Quality**:
   ```bash
   # Format code
   black norma/
   isort norma/
   
   # Type checking
   mypy norma/
   
   # Linting
   flake8 norma/
   ```

2. **Testing**:
   ```bash
   pytest tests/
   ```

3. **Package Verification**:
   ```bash
   twine check dist/*
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check `pyproject.toml` syntax
   - Ensure all required files exist
   - Verify Python version compatibility

2. **Upload Fails**:
   - Check authentication credentials
   - Verify package name availability
   - Ensure version hasn't been uploaded before

3. **Installation Issues**:
   - Check dependency compatibility
   - Verify Python version requirements
   - Test in clean environment

### Error Messages

- **"File already exists"**: Version already uploaded, increment version number
- **"Invalid authentication"**: Check API token or credentials
- **"Package name already taken"**: Choose different package name

## 📈 Post-Release

After successful upload:

1. **Verify Installation**:
   ```bash
   pip install norma-orm
   python -c "import norma; print(norma.__version__)"
   ```

2. **Update Documentation**:
   - Update GitHub README with installation instructions
   - Create release notes
   - Update version badges

3. **Announce Release**:
   - GitHub release
   - Social media
   - Developer communities

## 🔄 Continuous Integration

For automated releases, use GitHub Actions:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.8'
    - name: Install build tools
      run: pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## 📚 Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)

---

**Happy Releasing! 🎉** 