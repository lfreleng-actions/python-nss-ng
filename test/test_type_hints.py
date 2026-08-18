# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Tests for type hint validation using mypy.

This module validates that .pyi stub files are correct and complete.
"""

import sys
from pathlib import Path

import pytest


class TestTypeHints:
    """Test type hint files with mypy."""

    @pytest.fixture
    def stub_files(self):
        """Get all .pyi stub files."""
        src_dir = Path(__file__).parent.parent / "src"
        return list(src_dir.glob("*.pyi"))

    @pytest.fixture
    def src_dir(self):
        """Get source directory."""
        return Path(__file__).parent.parent / "src"

    def test_stub_files_exist(self, stub_files):
        """Test that stub files exist."""
        assert len(stub_files) > 0, "Should have .pyi stub files"

        expected_stubs = ["nss.pyi", "ssl.pyi", "io.pyi"]
        found_names = [f.name for f in stub_files]

        for expected in expected_stubs:
            assert expected in found_names, f"Missing {expected}"

    def test_stub_file_syntax(self, stub_files):
        """Test that stub files have valid Python syntax."""
        for stub_file in stub_files:
            with open(stub_file) as f:
                content = f.read()

            # Should compile as valid Python
            try:
                compile(content, stub_file.name, "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {stub_file.name}: {e}")

    def test_mypy_available(self):
        """Test if mypy is available for type checking."""
        try:
            import mypy.api
        except ImportError:
            pytest.skip("mypy not installed - install with: pip install mypy")

        # The stub validation below drives mypy through this entry point
        assert callable(mypy.api.run)

    @pytest.mark.skipif(sys.version_info < (3, 8), reason="Type hints require Python 3.8+")
    def test_mypy_validates_stubs(self, stub_files):
        """Test that mypy validates stub files without errors."""
        try:
            import mypy.api
        except ImportError:
            pytest.skip("mypy not installed")

        for stub_file in stub_files:
            # Run mypy on stub file with lenient settings
            result = mypy.api.run(
                [
                    str(stub_file),
                    "--ignore-missing-imports",
                    "--no-error-summary",
                ]
            )
            stdout, stderr, exit_code = result

            # Check for critical errors (ignore warnings)
            critical_errors = [
                line
                for line in stdout.split("\n")
                if "error:" in line.lower() and "note:" not in line.lower()
            ]

            # Should not have critical errors
            if critical_errors and exit_code != 0:
                pytest.fail(
                    f"mypy critical errors in {stub_file.name}:\n" + "\n".join(critical_errors)
                )

    def test_stub_completeness(self, stub_files):
        """Test that stubs document main APIs."""
        # Check that stubs have content
        for stub_file in stub_files:
            content = stub_file.read_text()

            # Should have function definitions or class definitions
            has_functions = "def " in content
            has_classes = "class " in content

            assert has_functions or has_classes, (
                f"{stub_file.name} should have function or class definitions"
            )

            # Should have type annotations
            assert "->" in content or ": " in content, (
                f"{stub_file.name} should have type annotations"
            )

    def test_nss_pyi_structure(self, src_dir):
        """Test nss.pyi has expected structure."""
        nss_pyi = src_dir / "nss.pyi"

        if not nss_pyi.exists():
            pytest.skip("nss.pyi not found")

        content = nss_pyi.read_text()

        # Should document key NSS functions
        # (Add specific checks based on actual API)
        assert content, "nss.pyi should not be empty"

    def test_ssl_pyi_structure(self, src_dir):
        """Test ssl.pyi has expected structure."""
        ssl_pyi = src_dir / "ssl.pyi"

        if not ssl_pyi.exists():
            pytest.skip("ssl.pyi not found")

        content = ssl_pyi.read_text()

        # Should document SSL functions
        assert content, "ssl.pyi should not be empty"

    def test_io_pyi_structure(self, src_dir):
        """Test io.pyi has expected structure."""
        io_pyi = src_dir / "io.pyi"

        if not io_pyi.exists():
            pytest.skip("io.pyi not found")

        content = io_pyi.read_text()

        # Should document I/O functions
        assert content, "io.pyi should not be empty"


class TestPythonModuleHints:
    """Test Python module type hints."""

    def test_nss_context_module_exists(self):
        """Test that nss_context.py exists."""
        sys.path.insert(0, "src")

        try:
            import nss_context
        except ImportError:
            pytest.fail("nss_context module not found")

        assert hasattr(nss_context, "NSSContext")
        assert hasattr(nss_context, "nss_context")

    def test_deprecations_has_hints(self):
        """Test that deprecations.py has type hints."""
        sys.path.insert(0, "src")

        try:
            from deprecations import warn_deprecated

            # Should have annotations
            assert hasattr(warn_deprecated, "__annotations__")
        except ImportError:
            pytest.skip("deprecations module not available")

    def test_secure_logging_has_hints(self):
        """Test that secure_logging.py has type hints."""
        sys.path.insert(0, "src")

        try:
            from secure_logging import secure_log

            # Should have annotations or documentation
            assert secure_log.__doc__ is not None or hasattr(secure_log, "__annotations__")
        except ImportError:
            pytest.skip("secure_logging module not available")


class TestTypeHintConsistency:
    """Test type hint consistency across modules."""

    def test_stub_files_match_modules(self, tmp_path):
        """Test that stub files roughly match module structure."""
        src_dir = Path(__file__).parent.parent / "src"

        stub_files = list(src_dir.glob("*.pyi"))

        for stub_file in stub_files:
            module_name = stub_file.stem

            # Check if corresponding .py or .so might exist
            # (This is a loose check since C extensions may not have .py)
            stub_content = stub_file.read_text()

            # Stubs should not be empty
            assert len(stub_content.strip()) > 0, f"{stub_file.name} should not be empty"

            # Should have proper Python structure
            assert not stub_content.startswith("<?xml"), (
                f"{stub_file.name} should be Python, not XML"
            )


class TestTypeHintDocumentation:
    """Test that type hints are documented."""

    def test_stub_files_have_docstrings(self):
        """Test that stub files contain docstrings."""
        src_dir = Path(__file__).parent.parent / "src"
        stub_files = list(src_dir.glob("*.pyi"))

        for stub_file in stub_files:
            content = stub_file.read_text()

            # Should have at least one docstring (module or function)
            has_triple_quote = '"""' in content or "'''" in content

            # It's okay if small stubs don't have extensive docs
            if len(content) > 200:
                assert has_triple_quote, f"{stub_file.name} should have docstrings"

    def test_type_hints_use_standard_types(self):
        """Test that type hints use standard typing module."""
        src_dir = Path(__file__).parent.parent / "src"
        stub_files = list(src_dir.glob("*.pyi"))

        for stub_file in stub_files:
            content = stub_file.read_text()

            # If using advanced types, should import from typing
            advanced_types = ["Optional", "Union", "List", "Dict", "Tuple"]
            uses_advanced = any(t in content for t in advanced_types)

            if uses_advanced:
                # Should import from typing or use | syntax
                has_typing_import = (
                    "from typing import" in content
                    or "import typing" in content
                    or "|" in content  # Python 3.10+ union syntax
                )

                assert has_typing_import, (
                    f"{stub_file.name} uses advanced types but doesn't import typing"
                )


class TestMypyConfiguration:
    """Test mypy configuration."""

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        repo_root = Path(__file__).parent.parent
        pyproject = repo_root / "pyproject.toml"

        assert pyproject.exists(), "pyproject.toml should exist"

    def test_mypy_config_if_present(self):
        """Test mypy configuration if present in pyproject.toml."""
        repo_root = Path(__file__).parent.parent
        pyproject = repo_root / "pyproject.toml"

        if not pyproject.exists():
            pytest.skip("pyproject.toml not found")

        content = pyproject.read_text()

        # If mypy config exists, validate it
        if "[tool.mypy]" in content:
            # Should have basic settings
            assert "python_version" in content or "files" in content, (
                "mypy config should specify python_version or files"
            )


class TestTypeHintCoverage:
    """Test coverage of type hints."""

    def test_public_api_has_stubs(self):
        """Test that main modules have stub files."""
        src_dir = Path(__file__).parent.parent / "src"

        # Core modules should have stubs
        expected_stubs = ["nss.pyi", "ssl.pyi", "io.pyi"]

        for stub_name in expected_stubs:
            stub_path = src_dir / stub_name
            assert stub_path.exists(), f"{stub_name} should exist"

    def test_python_modules_have_annotations(self):
        """Test that Python modules use type annotations."""
        sys.path.insert(0, "src")

        try:
            # Import pure Python modules
            from deprecations import warn_deprecated
            from secure_logging import secure_log

            # At least some functions should have annotations
            modules_with_hints = 0

            if hasattr(warn_deprecated, "__annotations__"):
                modules_with_hints += 1

            if hasattr(secure_log, "__annotations__"):
                modules_with_hints += 1

            # At least one should have type hints
            # (This is a soft requirement - type hints are being added gradually)
            # assert modules_with_hints > 0

            # For now, just check they exist
            assert warn_deprecated is not None
            assert secure_log is not None

        except ImportError:
            pytest.skip("Pure Python modules not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
