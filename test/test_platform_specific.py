# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Platform-specific tests for python-nss-ng.

This module tests platform-specific behaviors on macOS and Linux,
including path handling, library loading, and system integration.
"""

import os
import platform
import subprocess
import sys
import sysconfig
import tempfile

import pytest

# Add test directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nss.nss as nss


class TestPlatformDetection:
    """Test platform detection and handling."""

    def test_platform_is_supported(self):
        """Test that current platform is supported."""
        current_platform = sys.platform

        # Only Linux and macOS are supported
        assert current_platform.startswith("linux") or current_platform.startswith("darwin"), (
            f"Unsupported platform: {current_platform}"
        )

    def test_windows_not_supported(self):
        """Test that Windows is correctly identified as unsupported."""
        # This test documents the requirement
        # Actual Windows check is in src/__init__.py
        if sys.platform.startswith("win"):
            pytest.fail("Tests should not run on Windows")

    def test_platform_module_available(self):
        """Test that platform information is available."""
        system = platform.system()
        assert system in ["Linux", "Darwin"], f"Expected Linux or Darwin, got {system}"

    def test_python_version_supported(self):
        """Test that Python version is supported."""
        version_info = sys.version_info

        # Should be Python 3.10+
        assert version_info.major == 3, "Python 3 required"
        assert version_info.minor >= 10, "Python 3.10+ required"


class TestMacOSSpecific:
    """macOS-specific tests."""

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_platform_detected(self):
        """Test that macOS platform is correctly detected."""
        assert sys.platform == "darwin"
        assert platform.system() == "Darwin"

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_homebrew_paths(self):
        """Test that Homebrew paths are accessible on macOS."""
        # Common Homebrew paths
        homebrew_paths = [
            "/usr/local/opt/nss",
            "/usr/local/opt/nspr",
            "/opt/homebrew/opt/nss",
            "/opt/homebrew/opt/nspr",
        ]

        # At least one should exist if installed via Homebrew
        exists = any(os.path.exists(p) for p in homebrew_paths)

        if not exists:
            pytest.skip("NSS/NSPR not installed via Homebrew")

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_library_loading(self, nss_db_context):
        """Test that NSS libraries load on macOS."""
        # If we got here, NSS initialized successfully
        assert nss.nss_is_initialized()

        # Get NSS version
        version = nss.nss_get_version()
        assert version is not None
        assert isinstance(version, str)

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_nss_tools_available(self):
        """Test that NSS tools are available on macOS."""
        try:
            from util import find_nss_tool

            certutil = find_nss_tool("certutil")
            assert certutil is not None
            assert os.path.exists(certutil)
        except (FileNotFoundError, ImportError):
            pytest.skip("certutil not in PATH")

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_path_separators(self):
        """Test that path handling works correctly on macOS."""
        # macOS uses Unix-style paths
        test_path = "/tmp/test/path"
        assert os.sep == "/"
        assert os.path.join("tmp", "test") == "tmp/test"

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_temp_directory(self):
        """Test temporary directory on macOS."""
        temp_dir = tempfile.gettempdir()

        # macOS temp is typically /var/folders/... or /tmp
        assert temp_dir.startswith("/var/") or temp_dir.startswith("/tmp")
        assert os.path.exists(temp_dir)

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_macos_case_sensitivity(self):
        """Test file system case sensitivity behavior on macOS."""
        # macOS is typically case-insensitive but case-preserving
        # This is a documentation test
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name
            f.write("test")

        try:
            # File exists with original name
            assert os.path.exists(temp_path)

            # On case-insensitive systems, this may also work
            # (but this varies by filesystem)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestLinuxSpecific:
    """Linux-specific tests."""

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_platform_detected(self):
        """Test that Linux platform is correctly detected."""
        assert sys.platform.startswith("linux")
        assert platform.system() == "Linux"

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_distribution_detected(self):
        """Test that Linux distribution can be detected."""
        # Get distribution info (Python 3.10+ has platform.freedesktop_os_release)
        try:
            import platform

            if hasattr(platform, "freedesktop_os_release"):
                os_release = platform.freedesktop_os_release()
                assert "NAME" in os_release or "ID" in os_release
        except (AttributeError, OSError):
            # May not be available on all systems
            pass

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_library_paths(self):
        """Test common Linux library paths."""
        # Common library paths
        lib_paths = [
            "/usr/lib",
            "/usr/lib64",
            "/usr/local/lib",
            "/lib",
            "/lib64",
        ]

        # At least some should exist
        exists = any(os.path.exists(p) for p in lib_paths)
        assert exists, "No standard library paths found"

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_library_loading(self, nss_db_context):
        """Test that NSS libraries load on Linux."""
        # If we got here, NSS initialized successfully
        assert nss.nss_is_initialized()

        # Get NSS version
        version = nss.nss_get_version()
        assert version is not None
        assert isinstance(version, str)

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_nss_tools_available(self):
        """Test that NSS tools are available on Linux."""
        try:
            from util import find_nss_tool

            certutil = find_nss_tool("certutil")
            assert certutil is not None
            assert os.path.exists(certutil)
        except (FileNotFoundError, ImportError):
            pytest.skip("certutil not in PATH")

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_fips_mode_detection(self):
        """Test FIPS mode detection on Linux."""
        # FIPS mode is Linux-specific
        fips_file = "/proc/sys/crypto/fips_enabled"

        if os.path.exists(fips_file):
            with open(fips_file) as f:
                fips_enabled = f.read().strip()
                # Should be '0' or '1'
                assert fips_enabled in ["0", "1"]
        else:
            pytest.skip("FIPS indicator file not found")

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_path_separators(self):
        """Test that path handling works correctly on Linux."""
        # Linux uses Unix-style paths
        test_path = "/tmp/test/path"
        assert os.sep == "/"
        assert os.path.join("tmp", "test") == "tmp/test"

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_temp_directory(self):
        """Test temporary directory on Linux."""
        temp_dir = tempfile.gettempdir()

        # Linux temp is typically /tmp
        assert temp_dir in ["/tmp", "/var/tmp"] or temp_dir.startswith("/tmp/")
        assert os.path.exists(temp_dir)

    @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
    def test_linux_case_sensitivity(self):
        """Test file system case sensitivity on Linux."""
        # Linux is typically case-sensitive
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name
            f.write("test")

        try:
            # File exists with original name
            assert os.path.exists(temp_path)

            # Create path with different case
            if temp_path.endswith(".txt"):
                different_case = temp_path[:-4] + ".TXT"

                # On case-sensitive systems, these are different files
                # Just verify original exists
                assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestPathHandling:
    """Test cross-platform path handling."""

    def test_path_normalization(self):
        """Test that paths are normalized correctly."""
        # Test with forward slashes (Unix-style)
        unix_path = "tmp/test/file.txt"
        normalized = os.path.normpath(unix_path)

        # Should be normalized for current platform
        assert normalized is not None

    def test_absolute_path_detection(self):
        """Test absolute path detection."""
        # Absolute paths start with / on Unix, drive letter on Windows
        if sys.platform.startswith("win"):
            pytest.skip("Windows not supported")

        assert os.path.isabs("/tmp/test")
        assert not os.path.isabs("tmp/test")
        assert not os.path.isabs("./tmp/test")

    def test_path_joining(self):
        """Test path joining works correctly."""
        joined = os.path.join("tmp", "test", "file.txt")

        # Should use platform-appropriate separator
        assert "tmp" in joined
        assert "test" in joined
        assert "file.txt" in joined

    def test_home_directory(self):
        """Test home directory detection."""
        home = os.path.expanduser("~")

        assert home is not None
        assert len(home) > 0
        assert os.path.isabs(home)
        assert os.path.exists(home)

    def test_temp_directory_writable(self):
        """Test that temp directory is writable."""
        temp_dir = tempfile.gettempdir()

        assert os.path.exists(temp_dir)
        assert os.access(temp_dir, os.W_OK)


class TestLibraryPaths:
    """Test library path handling."""

    def test_nss_library_findable(self, nss_db_context):
        """Test that NSS library can be found and loaded."""
        # If we got here, NSS loaded successfully
        version = nss.nss_get_version()
        assert version is not None

    def test_pkg_config_available(self):
        """Test if pkg-config can find NSS."""
        try:
            result = subprocess.run(
                ["pkg-config", "--modversion", "nss"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                assert len(version) > 0
                assert "." in version  # Version should have dots
        except FileNotFoundError:
            pytest.skip("pkg-config not available")
        except subprocess.TimeoutExpired:
            pytest.skip("pkg-config timed out")

    def test_library_version_consistency(self, nss_db_context):
        """Test that library version is consistent."""
        version1 = nss.nss_get_version()
        version2 = nss.nss_get_version()

        assert version1 == version2, "Version should be consistent"


class TestSystemIntegration:
    """Test system integration aspects."""

    def test_environment_variables_respected(self):
        """Test that environment variables are accessible."""
        # Get PATH
        path = os.environ.get("PATH")
        assert path is not None
        assert len(path) > 0

    def test_user_permissions(self):
        """Test that user has appropriate permissions."""
        # Should be able to write to temp directory
        temp_dir = tempfile.gettempdir()

        test_file = os.path.join(temp_dir, "python_nss_test_permissions.tmp")
        try:
            with open(test_file, "w") as f:
                f.write("test")

            assert os.path.exists(test_file)
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_process_id_available(self):
        """Test that process ID is available."""
        pid = os.getpid()
        assert pid > 0

    def test_working_directory_accessible(self):
        """Test that current working directory is accessible."""
        cwd = os.getcwd()
        assert cwd is not None
        assert os.path.exists(cwd)
        assert os.path.isabs(cwd)


class TestArchitectureSpecific:
    """Test architecture-specific behaviors."""

    def test_architecture_detected(self):
        """Test that system architecture is detected."""
        machine = platform.machine()
        assert machine is not None

        # Common architectures
        common_archs = ["x86_64", "amd64", "arm64", "aarch64", "i386", "i686"]
        assert machine in common_archs or len(machine) > 0

    def test_64bit_platform(self):
        """Test platform bit-width."""
        # Most modern systems are 64-bit
        is_64bit = sys.maxsize > 2**32

        # Document architecture
        if is_64bit:
            assert sys.maxsize > 2**32
        else:
            # 32-bit systems are rare but possible
            pass

    def test_byte_order(self):
        """Test system byte order."""
        byte_order = sys.byteorder
        assert byte_order in ["little", "big"]

        # Most modern systems are little-endian
        # This is just documentation


class TestCrossPlatformCompatibility:
    """Test cross-platform compatibility."""

    def test_newline_handling(self):
        """Test that newline handling is platform-aware."""
        # Python handles this automatically
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_path = f.name
            f.write("line1\nline2\n")

        try:
            with open(temp_path) as f:
                lines = f.readlines()
                assert len(lines) == 2
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_file_separators(self):
        """Test file path separator."""
        assert os.sep in ["/", "\\"]
        assert os.pathsep in [":", ";"]

    def test_executable_extension(self):
        """Test executable file extension."""
        # Unix systems: no extension
        # Windows: .exe
        if sys.platform.startswith("win"):
            pytest.skip("Windows not supported")

        assert sysconfig.get_config_var("EXE") == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
