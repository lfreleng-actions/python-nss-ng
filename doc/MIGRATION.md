<!--
SPDX-License-Identifier: MPL-2.0
SPDX-FileCopyrightText: 2025 The Linux Foundation
-->

# Migration Guide: Legacy to Modern Python Project Structure

This document describes the modernization changes made to the python-nss-ng
project to bring it up to current Python packaging standards (2025).

## Overview

The python-nss-ng project was originally built with the legacy
`distutils` build system. This migration updates the project to:

- Support Python 3.11+ (3.11, 3.12, 3.13, 3.14, 3.15)
- Use modern packaging standards (PEP 517, PEP 518, PEP 621)
- Use dynamic versioning from git tags
- Support modern development tools (uv, pytest, ruff)

## Key Changes

### 1. Build System Migration

#### Legacy Setup

```python
# setup.py - Full configuration in Python code
from distutils.core import setup, Extension

setup(
    name='python-nss-ng',
    version='1.0.0',  # Hardcoded version
    # ... all configuration here
)
```

```ini
# setup.cfg - Minimal configuration
[sdist]
formats = bztar
dist-dir =
```

#### Modern Setup

```toml
# pyproject.toml - Declarative configuration
[build-system]
requires = ["setuptools>=68.0", "setuptools-scm>=8.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "python-nss-ng"
dynamic = ["version"]
requires-python = ">=3.11"
# ... modern metadata
```

```python
# setup.py - C extension configuration
from setuptools import Extension, setup

def get_extensions():
    # Extension configuration
    ...

if __name__ == "__main__":
    setup(ext_modules=get_extensions())
```

### 2. Version Management

#### Legacy Approach

- Version hardcoded in `setup.py` (`version = "1.0.0"`)
- Manual version updating via `update_version()` function
- Version written to `src/__init__.py` at build time

#### Modern Approach

- Dynamic versioning using `setuptools-scm`
- Version derived from git tags (e.g., `PYNSS_RELEASE_1_0_0`)
- Version automatically written to `src/_version.py`
- Import fallback using `importlib.metadata`

```python
# src/__init__.py
try:
    from ._version import __version__
except ImportError:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("python-nss-ng")
    except PackageNotFoundError:
        __version__ = "0.0.0+unknown"
```

### 3. Package Structure

#### Legacy Structure

```text
python-nss-ng/
├── setup.py          # All configuration
├── setup.cfg         # Minimal config
├── MANIFEST          # Generated manifest
└── src/
    └── __init__.py
```

#### Modern Structure

```text
python-nss-ng/
├── pyproject.toml    # Main configuration (PEP 621)
├── setup.py          # C extension config
├── MANIFEST.in       # Source manifest template
├── README.md         # Markdown documentation
└── src/
    ├── __init__.py
    └── _version.py   # Auto-generated
```

### 4. Dependency Management

#### Legacy Dependencies

- No formal dependency specification
- No development dependencies
- No optional dependencies

#### Modern Dependencies

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "build>=1.0.0",
]
```

### 5. Python Version Support

#### Legacy Support

- Used `distutils` (deprecated in Python 3.10, removed in 3.12)
- Used legacy packaging tools

#### Modern Support

- Explicit support: Python 3.11, 3.12, 3.13, 3.14, 3.15
- Modern `setuptools` build backend
- Compatible with PEP 517/518 build frontends (pip, build, uv)

### 6. C Extension Configuration

#### Legacy Detection

- Include/library paths detected in `setup.py`
- Limited platform support
- No runtime library path configuration

#### Modern Detection

- Enhanced path detection with Homebrew support (macOS)
- Better error messages for missing dependencies
- Runtime library path (`rpath`) configuration on Linux
- Environment variable support (`NSS_INCLUDE_ROOTS`)

```python
# setup.py - Enhanced detection
def find_include_dir(dir_names, include_files, include_roots=None):
    if not include_roots:
        include_roots = ['/usr/include', '/usr/local/include']
        # Add Homebrew paths for macOS
        if sys.platform == 'darwin':
            # ... auto-detect brew prefix
```

### 7. Testing Infrastructure

#### Legacy Testing

- Custom test runner (`test/run_tests`)
- No formal test configuration
- No pytest integration

#### Modern Testing

```toml
[tool.pytest.ini_options]
testpaths = ["test"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--strict-markers", "--tb=short"]
```

### 8. Code Quality Tools

#### Legacy Tooling

- No linting configuration
- No formatting standards
- No type checking

#### Modern Tooling

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.coverage.run]
source = ["nss"]
branch = true
```

## Migration Steps Performed

1. **Created `pyproject.toml`**
   - Defined build system requirements
   - Specified project metadata (PEP 621)
   - Configured tools (pytest, ruff, coverage)

2. **Updated `setup.py`**
   - Removed all metadata (moved to pyproject.toml)
   - Kept C extension configuration
   - Enhanced library/include detection
   - Added macOS Homebrew support

3. **Created `MANIFEST.in`**
   - Explicit file inclusion rules
   - Proper exclusion of build artifacts
   - Source distribution optimization

4. **Updated `src/__init__.py`**
   - Removed hardcoded version
   - Added dynamic version import
   - Fallback to importlib.metadata

5. **Created `README.md`**
   - Comprehensive project documentation
   - Installation instructions
   - Known issues documentation

6. **Updated `.gitignore`**
   - Added modern Python patterns
   - Excluded generated version files
   - Included old setup files in ignore

7. **Removed Legacy Files**
   - Archived `setup.py.old`
   - Archived `setup.cfg.old`
   - Removed generated `MANIFEST`

## Installing the Modernized Package

### Using uv (Recommended)

```bash
# Development environment
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Building Distributions

```bash
python -m build
```

## Compatibility Notes

### Breaking Changes

- **Lower Bound Python version**: Now requires Python 3.11+
- **Build system**: `python setup.py install` no longer recommended
- **Import changes**: None (backward compatible)

### Non-Breaking Changes

- Package name is now `python-nss-ng`
- Import path remains `import nss`
- Public API unchanged
- License unchanged

## Known Issues

### C Extension Compilation

The C extension code has compatibility issues with NSS 3.100+. The code
targets older NSS APIs and needs updates:

- Struct member access errors
- API changes in modern NSS
- Requires code review and updates

### Temporary Workarounds

Until the C code receives updates:

- Use older NSS versions (3.x series before 3.100)
- Or contribute fixes for modern NSS compatibility

## Benefits of Modernization

1. **Standards Compliance**: Follows PEP 517, 518, 621
2. **Tool Support**: Works with modern tools (uv, pip, build)
3. **Version Automation**: Automatic versioning from git tags
4. **Better DX**: Improved developer experience
5. **CI/CD Ready**: Compatible with GitHub Actions workflows
6. **Future Proof**: Ready for Python 3.14 and beyond

## Testing the Migration

### Verify Package Metadata

```bash
python -c "from importlib.metadata import version; print(version('python-nss-ng'))"
```

### Check Build System

```bash
python -m build --sdist
python -m build --wheel
```

### Audit Dependencies

```bash
pip install pip-audit
uv pip install pip-audit
uv run pip-audit
```

## Next Steps

1. **Fix C Extension Compatibility**
   - Update code for NSS 3.100+ APIs
   - Fix struct member access issues
   - Test on different NSS versions

2. **Enhance Testing**
   - Add more comprehensive tests
   - Set up CI/CD pipelines
   - Add coverage reporting

3. **Documentation**
   - Generate API documentation
   - Add examples for modern Python
   - Create migration guide for users

4. **Type Hints**
   - Add type stubs for C extensions
   - Type hint Python code
   - Enable mypy checking

## References

- [PEP 517 - Build System Interface](https://peps.python.org/pep-0517/)
- [PEP 518 - Build System Requirements](https://peps.python.org/pep-0518/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [setuptools-scm Documentation](https://setuptools-scm.readthedocs.io/)
- [Python Packaging User Guide](https://packaging.python.org/)
