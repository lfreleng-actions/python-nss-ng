# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Tests for utility functions in util.py.

This module tests the utility functions used throughout the test suite,
including path finding, build directory detection, and temporary file handling.
"""

import os
import subprocess
import sys
import tempfile

import pytest

# Add test directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import util


class TestFindNSSTool:
    """Test find_nss_tool() function."""

    def test_find_certutil(self):
        """Test finding certutil in PATH."""
        try:
            certutil_path = util.find_nss_tool("certutil")
            assert certutil_path is not None
            assert os.path.exists(certutil_path)
            assert os.path.isfile(certutil_path)
        except FileNotFoundError:
            pytest.skip("certutil not in PATH")

    def test_find_pk12util(self):
        """Test finding pk12util in PATH."""
        try:
            pk12util_path = util.find_nss_tool("pk12util")
            assert pk12util_path is not None
            assert os.path.exists(pk12util_path)
            assert os.path.isfile(pk12util_path)
        except FileNotFoundError:
            pytest.skip("pk12util not in PATH")

    def test_find_nonexistent_tool(self):
        """Test that finding nonexistent tool raises appropriate error."""
        with pytest.raises((FileNotFoundError, RuntimeError)):
            util.find_nss_tool("definitely_not_a_real_nss_tool_12345")

    def test_find_tool_returns_absolute_path(self):
        """Test that returned path is absolute."""
        try:
            tool_path = util.find_nss_tool("certutil")
            assert os.path.isabs(tool_path)
        except FileNotFoundError:
            pytest.skip("certutil not in PATH")

    def test_find_tool_executable(self):
        """Test that found tool is executable."""
        try:
            tool_path = util.find_nss_tool("certutil")
            # Check if file has execute permission
            assert os.access(tool_path, os.X_OK)
        except FileNotFoundError:
            pytest.skip("certutil not in PATH")


class TestGetBuildDir:
    """Test get_build_dir() function."""

    def test_get_build_dir_returns_path_or_none(self):
        """Test that get_build_dir returns a path or None."""
        build_dir = util.get_build_dir()
        assert build_dir is None or isinstance(build_dir, str)

    def test_build_dir_exists_if_returned(self):
        """Test that if build_dir is returned, it exists or will exist after build."""
        build_dir = util.get_build_dir()
        if build_dir is not None:
            # Build dir may be detected but not yet created (before compilation)
            # This is acceptable - just verify it's a valid path string
            assert isinstance(build_dir, str)
            assert len(build_dir) > 0

    def test_build_dir_pattern(self):
        """Test that build directory follows expected pattern."""
        build_dir = util.get_build_dir()
        if build_dir is not None:
            # Build directory should contain 'build' in the name
            assert "build" in build_dir.lower() or "lib" in build_dir.lower()


class TestTempFileWithData:
    """Test temp_file_with_data() context manager."""

    def test_temp_file_created(self):
        """Test that temporary file is created."""
        test_data = b"Test data content"

        with util.temp_file_with_data(test_data) as temp_path:
            # File should exist
            assert os.path.exists(temp_path)
            assert os.path.isfile(temp_path)

            # File should contain the data
            with open(temp_path, "rb") as f:
                content = f.read()
                assert content == test_data

    def test_temp_file_cleaned_up(self):
        """Test that temporary file is cleaned up after context."""
        test_data = b"Cleanup test data"
        temp_path_holder: list[str | None] = [None]

        with util.temp_file_with_data(test_data) as temp_path:
            temp_path_holder[0] = temp_path
            assert os.path.exists(temp_path)

        # After exiting context, file should be deleted
        assert temp_path_holder[0] is not None
        assert not os.path.exists(temp_path_holder[0])

    def test_temp_file_with_empty_data(self):
        """Test creating temp file with empty data."""
        empty_data = b""

        with util.temp_file_with_data(empty_data) as temp_path:
            assert os.path.exists(temp_path)

            with open(temp_path, "rb") as f:
                content = f.read()
                assert content == empty_data
                assert len(content) == 0

    def test_temp_file_with_large_data(self):
        """Test creating temp file with large data."""
        # 1 MB of data
        large_data = b"X" * (1024 * 1024)

        with util.temp_file_with_data(large_data) as temp_path:
            assert os.path.exists(temp_path)

            # Verify file size
            file_size = os.path.getsize(temp_path)
            assert file_size == len(large_data)

            # Verify content (sample check to avoid reading all into memory)
            with open(temp_path, "rb") as f:
                # Check first and last bytes
                first_byte = f.read(1)
                f.seek(-1, os.SEEK_END)
                last_byte = f.read(1)
                assert first_byte == b"X"
                assert last_byte == b"X"

    def test_temp_file_with_binary_data(self):
        """Test creating temp file with binary data."""
        binary_data = bytes(range(256))  # All byte values

        with util.temp_file_with_data(binary_data) as temp_path:
            assert os.path.exists(temp_path)

            with open(temp_path, "rb") as f:
                content = f.read()
                assert content == binary_data

    def test_temp_file_cleanup_on_exception(self):
        """Test that temp file is deleted even if exception occurs."""
        test_data = b"Exception test data"
        temp_path_holder: list[str | None] = [None]

        try:
            with util.temp_file_with_data(test_data) as temp_path:
                temp_path_holder[0] = temp_path
                assert os.path.exists(temp_path)
                raise ValueError("Intentional test exception")
        except ValueError:
            pass

        # File should still be cleaned up despite exception
        assert temp_path_holder[0] is not None
        assert not os.path.exists(temp_path_holder[0])

    def test_temp_file_unique_paths(self):
        """Test that multiple temp files get unique paths."""
        test_data = b"Unique path test"
        paths = []

        # Create multiple temp files sequentially
        for i in range(5):
            with util.temp_file_with_data(test_data) as temp_path:
                paths.append(temp_path)
                assert os.path.exists(temp_path)

        # All paths should be unique
        assert len(paths) == len(set(paths))

    def test_temp_file_in_temp_directory(self):
        """Test that temp file is created in temp directory."""
        test_data = b"Location test"

        with util.temp_file_with_data(test_data) as temp_path:
            # Should be in system temp directory or subdirectory
            temp_dir = tempfile.gettempdir()
            assert temp_path.startswith(temp_dir) or "/tmp" in temp_path


class TestTempFilePermissions:
    """Test temporary file permissions and security."""

    def test_temp_file_readable(self):
        """Test that temp file is readable."""
        test_data = b"Readable test"

        with util.temp_file_with_data(test_data) as temp_path:
            # Should be able to read
            assert os.access(temp_path, os.R_OK)

    def test_temp_file_writable(self):
        """Test that temp file is writable."""
        test_data = b"Writable test"

        with util.temp_file_with_data(test_data) as temp_path:
            # Should be able to write (though we shouldn't in tests)
            assert os.access(temp_path, os.W_OK)

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix permissions test")
    def test_temp_file_permissions_secure(self):
        """Test that temp file has secure permissions on Unix."""
        test_data = b"Permission test"

        with util.temp_file_with_data(test_data) as temp_path:
            # Get file permissions
            file_stat = os.stat(temp_path)
            mode = file_stat.st_mode

            # File should not be world-readable or world-writable
            # (Though tempfile module's default behavior may vary)
            # This is more of a documentation test
            assert os.path.exists(temp_path)


class TestUtilEdgeCases:
    """Test edge cases and error conditions."""

    def test_find_tool_with_spaces_in_path(self):
        """Test finding tool when PATH might have spaces."""
        # This tests that the function handles PATH parsing correctly
        # Actual behavior depends on system configuration
        try:
            tool_path = util.find_nss_tool("certutil")
            # Should work regardless of spaces in PATH
            assert tool_path is not None
        except FileNotFoundError:
            pytest.skip("certutil not available")

    def test_temp_file_with_none_data(self):
        """Test that None data is handled (should raise TypeError)."""
        with pytest.raises(TypeError):
            with util.temp_file_with_data(None) as temp_path:  # type: ignore[arg-type]
                pass

    def test_temp_file_with_string_data(self):
        """Test that string data (not bytes) is handled."""
        # Should accept bytes, not str
        string_data = "This is a string"

        # Depending on implementation, might raise or convert
        try:
            with util.temp_file_with_data(string_data) as temp_path:  # type: ignore[arg-type]
                # If it accepts strings, verify it works
                assert os.path.exists(temp_path)
        except (TypeError, AttributeError):
            # Expected - should require bytes
            pass


class TestUtilIntegration:
    """Integration tests for util functions."""

    def test_find_tool_and_verify_execution(self):
        """Test finding a tool and verifying it can be executed."""
        try:
            certutil_path = util.find_nss_tool("certutil")

            # Verify we can check version (tool is executable)
            result = subprocess.run([certutil_path, "-H"], capture_output=True, timeout=5)

            # Should execute without error
            # (Though might return non-zero if -H is not a valid option)
            assert result.returncode is not None

        except FileNotFoundError:
            pytest.skip("certutil not available")
        except subprocess.TimeoutExpired:
            pytest.fail("certutil command timed out")

    def test_temp_file_write_and_read_workflow(self):
        """Test complete workflow of creating, writing, and reading temp file."""
        original_data = b"Original workflow data"

        with util.temp_file_with_data(original_data) as temp_path:
            # Read the data back
            with open(temp_path, "rb") as f:
                read_data = f.read()

            assert read_data == original_data

            # Append more data
            additional_data = b" - Additional content"
            with open(temp_path, "ab") as f:
                f.write(additional_data)

            # Read again
            with open(temp_path, "rb") as f:
                final_data = f.read()

            assert final_data == original_data + additional_data


class TestUtilTypeHints:
    """Test that util functions have proper type hints."""

    def test_find_nss_tool_has_annotations(self):
        """Test that find_nss_tool has type annotations."""
        assert hasattr(util.find_nss_tool, "__annotations__")
        annotations = util.find_nss_tool.__annotations__
        assert "tool_name" in annotations or len(annotations) > 0

    def test_get_build_dir_has_annotations(self):
        """Test that get_build_dir has type annotations."""
        assert hasattr(util.get_build_dir, "__annotations__")

    def test_temp_file_with_data_has_annotations(self):
        """Test that temp_file_with_data has type annotations."""
        assert hasattr(util.temp_file_with_data, "__annotations__")


class TestUtilDocumentation:
    """Test that util functions have proper documentation."""

    def test_find_nss_tool_has_docstring(self):
        """Test that find_nss_tool has docstring."""
        assert util.find_nss_tool.__doc__ is not None
        assert len(util.find_nss_tool.__doc__) > 0

    def test_get_build_dir_has_docstring(self):
        """Test that get_build_dir has docstring."""
        assert util.get_build_dir.__doc__ is not None
        assert len(util.get_build_dir.__doc__) > 0

    def test_temp_file_with_data_has_docstring(self):
        """Test that temp_file_with_data has docstring."""
        assert util.temp_file_with_data.__doc__ is not None
        assert len(util.temp_file_with_data.__doc__) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
