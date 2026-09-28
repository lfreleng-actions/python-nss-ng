# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Tests for OCSP (Online Certificate Status Protocol) functionality.

This module tests OCSP configuration, cache management, and validation settings.
"""

import pytest

import nss.nss as nss
from nss.error import NSPRError

# -------------------------------------------------------------------------------


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPCache:
    """Test OCSP cache functionality."""

    def test_ocsp_cache_settings(self, nss_clean_state):
        """Test setting OCSP cache parameters."""
        # Set cache with specific values
        # Parameters: max_cache_entries, minimum_seconds_to_next_fetch, maximum_seconds_before_cached_response_reused
        nss.set_ocsp_cache_settings(100, 10, 20)

        # Clear the cache - should not raise
        nss.clear_ocsp_cache()

    def test_ocsp_cache_clear_multiple_times(self, nss_clean_state):
        """Test that clearing cache multiple times is safe."""
        nss.set_ocsp_cache_settings(50, 5, 15)

        # Clear multiple times - should be idempotent
        nss.clear_ocsp_cache()
        nss.clear_ocsp_cache()
        nss.clear_ocsp_cache()

    def test_ocsp_cache_different_settings(self, nss_clean_state):
        """Test various cache setting combinations."""
        # Test with minimum values
        nss.set_ocsp_cache_settings(1, 1, 1)
        nss.clear_ocsp_cache()

        # Test with larger values
        nss.set_ocsp_cache_settings(1000, 60, 3600)
        nss.clear_ocsp_cache()

        # Test with zero values (may or may not be valid)
        try:
            nss.set_ocsp_cache_settings(0, 0, 0)
        except (NSPRError, ValueError):
            # Some implementations may reject zero values
            pass


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPTimeout:
    """Test OCSP timeout configuration."""

    def test_ocsp_timeout_valid_value(self, nss_clean_state):
        """Test setting valid OCSP timeout."""
        # Set timeout to 10 seconds
        nss.set_ocsp_timeout(10)

        # Set various valid timeouts
        nss.set_ocsp_timeout(1)
        nss.set_ocsp_timeout(30)
        nss.set_ocsp_timeout(60)

    def test_ocsp_timeout_rejects_string(self, nss_clean_state):
        """Test that timeout rejects non-integer values."""
        with pytest.raises(TypeError):
            nss.set_ocsp_timeout("ten")

        with pytest.raises(TypeError):
            nss.set_ocsp_timeout("30")

    def test_ocsp_timeout_rejects_float(self, nss_clean_state):
        """Test that timeout rejects float values."""
        with pytest.raises(TypeError):
            nss.set_ocsp_timeout(10.5)

    def test_ocsp_timeout_boundary_values(self, nss_clean_state):
        """Test timeout with boundary values."""
        # Test with zero (may disable timeout)
        try:
            nss.set_ocsp_timeout(0)
        except (NSPRError, ValueError):
            # Some implementations may reject zero
            pass

        # Test with negative value
        # Note: NSS doesn't validate negative values, it accepts them
        # This is arguably a bug in NSS, but we test actual behavior
        try:
            nss.set_ocsp_timeout(-1)
            # If it doesn't raise, that's the current NSS behavior
        except (NSPRError, ValueError, TypeError):
            # Some NSS versions might validate and reject
            pass


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPFailureMode:
    """Test OCSP failure mode configuration."""

    def test_ocsp_failure_mode_strict(self, nss_clean_state):
        """Test setting OCSP failure mode to strict (failure is verification failure)."""
        # When OCSP check fails, treat it as certificate validation failure
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsVerificationFailure)

    def test_ocsp_failure_mode_permissive(self, nss_clean_state):
        """Test setting OCSP failure mode to permissive."""
        # When OCSP check fails, don't treat it as validation failure
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsNotAVerificationFailure)

    def test_ocsp_failure_mode_toggle(self, nss_clean_state):
        """Test toggling between failure modes."""
        # Set to strict
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsVerificationFailure)

        # Set to permissive
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsNotAVerificationFailure)

        # Back to strict
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsVerificationFailure)

    def test_ocsp_failure_mode_invalid_value(self, nss_clean_state):
        """Test that invalid failure mode values are rejected."""
        with pytest.raises(NSPRError):
            nss.set_ocsp_failure_mode(-1)

        with pytest.raises(NSPRError):
            nss.set_ocsp_failure_mode(999)


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPDefaultResponder:
    """Test OCSP default responder configuration."""

    def test_ocsp_default_responder_invalid_cert(self, nss_clean_state):
        """Test that invalid certificate nickname is rejected."""
        # Should raise error if cert is not known
        with pytest.raises(NSPRError):
            nss.set_ocsp_default_responder(
                nss_clean_state, "http://foo.com:80/ocsp", "invalid_cert_nickname"
            )

    def test_ocsp_default_responder_valid_cert(self, nss_clean_state):
        """Test setting default responder with valid certificate."""
        # Set default responder with test_ca certificate
        nss.set_ocsp_default_responder(nss_clean_state, "http://foo.com:80/ocsp", "test_ca")

        # Enable default responder
        nss.enable_ocsp_default_responder()

        # Disable default responder
        nss.disable_ocsp_default_responder()

    def test_ocsp_default_responder_with_context(self, nss_clean_state):
        """Test default responder with explicit context."""
        nss.set_ocsp_default_responder(nss_clean_state, "http://ocsp.example.com:80/", "test_ca")

        # Enable with context
        nss.enable_ocsp_default_responder(nss_clean_state)

        # Disable with context
        nss.disable_ocsp_default_responder(nss_clean_state)

    def test_ocsp_default_responder_url_formats(self, nss_clean_state):
        """Test various URL formats for OCSP responder."""
        urls = [
            "http://ocsp.example.com/",
            "http://ocsp.example.com:80/ocsp",
            "http://ocsp.example.com:8080/status",
            "https://ocsp.example.com/",
        ]

        for url in urls:
            try:
                nss.set_ocsp_default_responder(nss_clean_state, url, "test_ca")
                nss.disable_ocsp_default_responder(nss_clean_state)
            except NSPRError:
                # Some URL formats may not be supported
                pass

    def test_ocsp_responder_enable_disable_sequence(self, nss_clean_state):
        """Test enable/disable sequence."""
        nss.set_ocsp_default_responder(nss_clean_state, "http://ocsp.test.com/", "test_ca")

        # Multiple enable/disable cycles
        nss.enable_ocsp_default_responder()
        nss.disable_ocsp_default_responder()
        nss.enable_ocsp_default_responder()
        nss.disable_ocsp_default_responder()


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPChecking:
    """Test OCSP checking enable/disable functionality."""

    def test_enable_ocsp_checking_global(self, nss_clean_state):
        """Test enabling OCSP checking globally."""
        nss.enable_ocsp_checking()

        # Disable to clean up
        nss.disable_ocsp_checking()

    def test_disable_ocsp_checking_global(self, nss_clean_state):
        """Test disabling OCSP checking globally."""
        # Enable first
        nss.enable_ocsp_checking()

        # Then disable
        nss.disable_ocsp_checking()

    def test_enable_ocsp_checking_with_context(self, nss_clean_state):
        """Test enabling OCSP checking with explicit context."""
        nss.enable_ocsp_checking(nss_clean_state)

        # Disable to clean up
        nss.disable_ocsp_checking(nss_clean_state)

    def test_disable_ocsp_checking_with_context(self, nss_clean_state):
        """Test disabling OCSP checking with explicit context."""
        # Enable first
        nss.enable_ocsp_checking(nss_clean_state)

        # Then disable
        nss.disable_ocsp_checking(nss_clean_state)

    def test_ocsp_checking_toggle_sequence(self, nss_clean_state):
        """Test multiple enable/disable cycles."""
        # Multiple cycles should work
        nss.enable_ocsp_checking()
        nss.disable_ocsp_checking()
        nss.enable_ocsp_checking()
        nss.disable_ocsp_checking()

        # With context
        nss.enable_ocsp_checking(nss_clean_state)
        nss.disable_ocsp_checking(nss_clean_state)
        nss.enable_ocsp_checking(nss_clean_state)
        nss.disable_ocsp_checking(nss_clean_state)

    def test_ocsp_idempotent_enable(self, nss_clean_state):
        """Test that enabling OCSP multiple times is safe."""
        nss.enable_ocsp_checking()
        nss.enable_ocsp_checking()
        nss.enable_ocsp_checking()

        # Clean up
        nss.disable_ocsp_checking()

    def test_ocsp_repeated_disable(self, nss_clean_state):
        """Disabling OCSP again reports that it is not enabled, harmlessly."""
        from nss.error import SEC_ERROR_OCSP_NOT_ENABLED

        nss.enable_ocsp_checking()
        nss.disable_ocsp_checking()

        # Documented behaviour: a disable while OCSP is off raises
        # SEC_ERROR_OCSP_NOT_ENABLED, which callers may ignore.
        for _ in range(2):
            with pytest.raises(NSPRError) as exc_info:
                nss.disable_ocsp_checking()
            assert exc_info.value.errno == SEC_ERROR_OCSP_NOT_ENABLED

        # And OCSP can still be enabled and disabled afterwards.
        nss.enable_ocsp_checking()
        nss.disable_ocsp_checking()


@pytest.mark.xdist_group("ocsp_serial")
class TestPKIXValidation:
    """Test PKIX validation mode."""

    def test_pkix_validation_get(self, nss_clean_state):
        """Test getting PKIX validation setting."""
        value = nss.get_use_pkix_for_validation()
        assert isinstance(value, bool)

    def test_pkix_validation_set_returns_previous(self, nss_clean_state):
        """Test that setting PKIX validation returns previous value."""
        value = nss.get_use_pkix_for_validation()
        assert isinstance(value, bool)

        # Set to opposite value and verify it returns previous
        prev = nss.set_use_pkix_for_validation(not value)
        assert isinstance(prev, bool)
        assert value == prev

        # Verify the new value is set
        assert nss.get_use_pkix_for_validation() == (not value)

        # Set back to original value
        prev2 = nss.set_use_pkix_for_validation(value)
        assert prev2 == (not value)
        assert nss.get_use_pkix_for_validation() == value

    def test_pkix_validation_rejects_non_integer(self, nss_clean_state):
        """Values that are not integers are rejected; integers are truthy flags."""
        original = nss.get_use_pkix_for_validation()
        try:
            with pytest.raises(TypeError):
                nss.set_use_pkix_for_validation("true")

            # The flag is parsed as an int, so 1 and 0 act as True and False.
            nss.set_use_pkix_for_validation(1)
            assert nss.get_use_pkix_for_validation() is True
            nss.set_use_pkix_for_validation(0)
            assert nss.get_use_pkix_for_validation() is False
        finally:
            nss.set_use_pkix_for_validation(original)

    def test_pkix_validation_set_true(self, nss_clean_state):
        """Test explicitly setting PKIX validation to True."""
        original = nss.get_use_pkix_for_validation()

        nss.set_use_pkix_for_validation(True)
        assert nss.get_use_pkix_for_validation() is True

        # Restore original
        nss.set_use_pkix_for_validation(original)

    def test_pkix_validation_set_false(self, nss_clean_state):
        """Test explicitly setting PKIX validation to False."""
        original = nss.get_use_pkix_for_validation()

        nss.set_use_pkix_for_validation(False)
        assert nss.get_use_pkix_for_validation() is False

        # Restore original
        nss.set_use_pkix_for_validation(original)

    def test_pkix_validation_toggle(self, nss_clean_state):
        """Test toggling PKIX validation multiple times."""
        original = nss.get_use_pkix_for_validation()

        # Toggle several times
        nss.set_use_pkix_for_validation(True)
        assert nss.get_use_pkix_for_validation() is True

        nss.set_use_pkix_for_validation(False)
        assert nss.get_use_pkix_for_validation() is False

        nss.set_use_pkix_for_validation(True)
        assert nss.get_use_pkix_for_validation() is True

        # Restore original
        nss.set_use_pkix_for_validation(original)


@pytest.mark.xdist_group("ocsp_serial")
class TestOCSPIntegration:
    """Integration tests combining multiple OCSP features."""

    def test_ocsp_full_configuration(self, nss_clean_state):
        """Test complete OCSP configuration workflow."""
        # Configure cache
        nss.set_ocsp_cache_settings(100, 10, 20)

        # Set timeout
        nss.set_ocsp_timeout(30)

        # Set failure mode
        nss.set_ocsp_failure_mode(nss.ocspMode_FailureIsVerificationFailure)

        # Configure default responder
        nss.set_ocsp_default_responder(nss_clean_state, "http://ocsp.example.com/", "test_ca")

        # Enable OCSP checking
        nss.enable_ocsp_checking(nss_clean_state)

        # Enable default responder
        nss.enable_ocsp_default_responder(nss_clean_state)

        # Clean up
        nss.disable_ocsp_default_responder(nss_clean_state)
        nss.disable_ocsp_checking(nss_clean_state)
        nss.clear_ocsp_cache()

    def test_ocsp_configuration_cleanup(self, nss_clean_state):
        """Test that OCSP configuration can be cleanly reset."""
        # Set various configurations
        nss.set_ocsp_cache_settings(50, 5, 10)
        nss.set_ocsp_timeout(15)
        nss.enable_ocsp_checking()

        # Clear and disable
        nss.clear_ocsp_cache()
        nss.disable_ocsp_checking()

        # Should be able to reconfigure
        nss.set_ocsp_cache_settings(100, 10, 20)
        nss.set_ocsp_timeout(30)
        nss.enable_ocsp_checking()

        # Final cleanup
        nss.disable_ocsp_checking()
        nss.clear_ocsp_cache()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
