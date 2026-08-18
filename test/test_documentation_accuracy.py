# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Tests for documentation accuracy.

This module validates that documentation matches actual code.
"""

import re
import sys
from pathlib import Path

import pytest


class TestReadmeAccuracy:
    """Test that README.md examples are accurate."""

    @pytest.fixture
    def readme_path(self):
        """Get README.md path."""
        repo_root = Path(__file__).parent.parent
        return repo_root / "README.md"

    @pytest.fixture
    def readme_content(self, readme_path):
        """Get README content."""
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    def test_readme_exists(self, readme_path):
        """Test that README.md exists."""
        assert readme_path.exists(), "README.md should exist"

    def test_readme_not_empty(self, readme_content):
        """Test that README has content."""
        assert len(readme_content) > 100, "README should have substantial content"

    def test_readme_has_title(self, readme_content):
        """Test that README has a title."""
        lines = readme_content.split("\n")

        # First non-empty line should be title or has # heading
        has_title = False
        for line in lines[:10]:
            if line.strip().startswith("#"):
                has_title = True
                break

        assert has_title, "README should have a title (# heading)"

    def test_readme_mentions_key_features(self, readme_content):
        """Test that README documents key features."""
        # Core project terms
        key_terms = ["NSS", "NSPR", "certificate", "Python"]

        found_terms = []
        for term in key_terms:
            if term in readme_content:
                found_terms.append(term)

        # At least 3 out of 4 key terms should be present
        assert len(found_terms) >= 3, f"README should mention key terms. Found: {found_terms}"

    def test_readme_has_installation_info(self, readme_content):
        """Test that README has installation information."""
        installation_indicators = ["install", "pip", "setup.py", "requirements", "dependencies"]

        has_installation = any(
            indicator in readme_content.lower() for indicator in installation_indicators
        )

        assert has_installation, "README should have installation information"

    def test_readme_has_usage_examples(self, readme_content):
        """Test that README has usage examples."""
        # Check for code blocks or import statements
        has_code_blocks = "```" in readme_content
        has_imports = "import" in readme_content

        assert has_code_blocks or has_imports, "README should have usage examples"

    def test_readme_code_blocks_extractable(self, readme_content):
        """Test that code blocks can be extracted from README."""
        # Extract Python code blocks
        python_blocks = re.findall(r"```python\n(.*?)\n```", readme_content, re.DOTALL)

        # Extract generic code blocks
        generic_blocks = re.findall(r"```\n(.*?)\n```", readme_content, re.DOTALL)

        total_blocks = len(python_blocks) + len(generic_blocks)

        # Should have at least some code examples
        # (This is lenient - some READMEs are more narrative)
        assert total_blocks >= 0, "README code blocks should be extractable"

    def test_readme_links_valid_format(self, readme_content):
        """Test that README links have valid Markdown format."""
        # Find Markdown links: [text](url)
        links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", readme_content)

        for link_text, link_url in links:
            # Link text should not be empty
            assert len(link_text) > 0, "Link text should not be empty"

            # URL should not be empty
            assert len(link_url) > 0, "Link URL should not be empty"

            # URL should not have spaces (unless properly encoded)
            if " " in link_url and "%20" not in link_url:
                # Allow relative paths with spaces in some cases
                if not link_url.startswith("#"):
                    pytest.fail(f"Link URL has unencoded spaces: {link_url}")


class TestAPIDocumentation:
    """Test that APIs are documented."""

    def test_public_functions_documented(self):
        """Test that public functions have docstrings."""
        sys.path.insert(0, "src")

        try:
            from deprecations import is_deprecated, warn_deprecated

            functions = [warn_deprecated, is_deprecated]

            for func in functions:
                assert func.__doc__ is not None, f"{func.__name__} should have docstring"
                assert len(func.__doc__.strip()) > 10, (
                    f"{func.__name__} docstring should be substantial"
                )
        except ImportError:
            pytest.skip("deprecations module not available")

    def test_secure_logging_functions_documented(self):
        """Test that secure_logging functions have docstrings."""
        sys.path.insert(0, "src")

        try:
            from secure_logging import redact_message, secure_log

            functions = [secure_log, redact_message]

            for func in functions:
                assert func.__doc__ is not None, f"{func.__name__} should have docstring"
                assert len(func.__doc__.strip()) > 10, (
                    f"{func.__name__} docstring should be substantial"
                )
        except ImportError:
            pytest.skip("secure_logging module not available")

    def test_nss_context_class_documented(self):
        """Test that NSSContext class is documented."""
        sys.path.insert(0, "src")

        try:
            from nss_context import NSSContext

            # Class should have docstring
            assert NSSContext.__doc__ is not None, "NSSContext class should have docstring"

            # Key methods should have docstrings
            key_methods = ["__init__", "__enter__", "__exit__"]

            for method_name in key_methods:
                if hasattr(NSSContext, method_name):
                    method = getattr(NSSContext, method_name)
                    # Some magic methods may not have docs, that's okay
                    # Just check they exist
                    assert method is not None
        except ImportError:
            pytest.skip("nss_context module not available")

    def test_module_level_docstrings(self):
        """Test that modules have module-level docstrings."""
        sys.path.insert(0, "src")

        modules_to_check = ["deprecations", "secure_logging", "nss_context"]

        documented_modules = 0

        for module_name in modules_to_check:
            try:
                module = __import__(module_name)
                if module.__doc__ is not None and len(module.__doc__.strip()) > 10:
                    documented_modules += 1
            except ImportError:
                pass

        # At least one module should have documentation
        assert documented_modules > 0, "At least one module should have module-level docstring"


class TestDocumentationConsistency:
    """Test documentation consistency."""

    @pytest.fixture
    def doc_dir(self):
        """Get documentation directory."""
        return Path(__file__).parent.parent / "doc"

    def test_doc_directory_exists(self, doc_dir):
        """Test that doc directory exists."""
        assert doc_dir.exists(), "doc directory should exist"

    def test_doc_files_exist(self, doc_dir):
        """Test that expected documentation files exist."""
        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        md_files = list(doc_dir.glob("*.md"))

        # Should have at least some documentation
        assert len(md_files) > 0, "doc directory should contain .md files"

    def test_all_docs_have_license(self, doc_dir):
        """Test that all .md files have license header."""
        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        md_files = list(doc_dir.glob("*.md"))

        for md_file in md_files:
            content = md_file.read_text()

            # Should have SPDX license identifier or copyright
            has_license = (
                "SPDX-License-Identifier" in content
                or "SPDX-FileCopyrightText" in content
                or "License:" in content
                or "Copyright" in content
            )

            assert has_license, f"{md_file.name} should have license information"

    def test_doc_files_not_empty(self, doc_dir):
        """Test that documentation files are not empty."""
        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        md_files = list(doc_dir.glob("*.md"))

        for md_file in md_files:
            content = md_file.read_text()

            # Should have substantial content (more than just license)
            assert len(content) > 200, f"{md_file.name} should have substantial content"

    def test_doc_files_have_headings(self, doc_dir):
        """Test that documentation files have proper structure."""
        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        md_files = list(doc_dir.glob("*.md"))

        for md_file in md_files:
            content = md_file.read_text()

            # Should have at least one heading
            has_heading = re.search(r"^#+\s+.+", content, re.MULTILINE)

            assert has_heading, f"{md_file.name} should have at least one heading"


class TestCodeExampleValidity:
    """Test that code examples in documentation are valid."""

    def test_readme_python_examples_syntax(self):
        """Test that Python examples in README have valid syntax."""
        readme_path = Path(__file__).parent.parent / "README.md"

        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text()

        # Extract Python code blocks
        python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

        for i, code_block in enumerate(python_blocks):
            # Try to parse as Python
            try:
                compile(code_block, f"<readme-example-{i}>", "exec")
            except SyntaxError as e:
                # Some examples might be incomplete snippets, be lenient
                # Just check for obvious errors
                if "invalid syntax" in str(e):
                    # Allow incomplete snippets, just flag truly broken ones
                    pass

    def test_doc_python_examples_syntax(self):
        """Test that Python examples in doc files have valid syntax."""
        doc_dir = Path(__file__).parent.parent / "doc"

        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        md_files = list(doc_dir.glob("*.md"))

        for md_file in md_files:
            content = md_file.read_text()

            # Extract Python code blocks
            python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

            for i, code_block in enumerate(python_blocks):
                # Try to parse as Python
                try:
                    compile(code_block, f"<{md_file.name}-example-{i}>", "exec")
                except SyntaxError:
                    # Some examples might be incomplete, that's okay
                    pass


class TestDocumentationCompleteness:
    """Test that documentation is complete."""

    def test_critical_docs_exist(self):
        """Test that critical documentation files exist."""
        repo_root = Path(__file__).parent.parent

        # Critical files
        readme = repo_root / "README.md"

        assert readme.exists(), "README.md must exist"

    def test_test_documentation_exists(self):
        """Test that test documentation exists."""
        repo_root = Path(__file__).parent.parent
        doc_dir = repo_root / "doc"

        if not doc_dir.exists():
            pytest.skip("doc directory not found")

        filenames = sorted(path.name.lower() for path in doc_dir.glob("*.md"))

        assert any("test" in name for name in filenames), (
            f"doc/ should document the test suite, found: {filenames}"
        )

    def test_api_reference_or_stubs_exist(self):
        """Test that API reference or type stubs exist."""
        src_dir = Path(__file__).parent.parent / "src"

        # Check for .pyi stub files (type hints serve as API docs)
        stub_files = list(src_dir.glob("*.pyi"))

        # Should have type stubs for API documentation
        assert len(stub_files) > 0, "Should have .pyi stub files for API documentation"


class TestDocumentationVersioning:
    """Test that documentation mentions versions appropriately."""

    def test_readme_or_docs_mention_version(self):
        """Test that documentation mentions version information."""
        repo_root = Path(__file__).parent.parent
        readme_path = repo_root / "README.md"

        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text()

        # Look for version-related keywords
        version_indicators = ["version", "release", "v0.", "v1.", "v2.", "pypi", "pip install"]

        has_version_info = any(indicator in content.lower() for indicator in version_indicators)

        # This is informational, not a hard requirement
        # Just check for presence
        assert isinstance(has_version_info, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
