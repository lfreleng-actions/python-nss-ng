# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2026 The Linux Foundation

"""
Regression tests for reference leaks in NSPR error handling.

Every NSPRError raised from C used to survive for the life of the
process, together with its traceback and every frame and local variable
that traceback refers to; every NSPRError and CertVerifyError also
leaked the strings and integers it was built from. Long-lived programs
that treat PR_WOULD_BLOCK_ERROR on a non-blocking socket as ordinary
control flow grew without bound.
"""

import gc
import tracemalloc

import pytest

import nss.error
import nss.io
import nss.nss

ITERATIONS = 2000

# Generous against allocator noise; each leak measured several hundred
# bytes per iteration.
MAX_BYTES_PER_ITERATION = 16


def _live(type_name):
    return sum(1 for o in gc.get_objects() if type(o).__name__ == type_name)


def _growth(fn, type_name):
    """Return (surviving objects, traced bytes per call) for ITERATIONS calls."""
    fn()  # warm any caches before measuring
    tracemalloc.start()
    try:
        gc.collect()
        live_before = _live(type_name)
        bytes_before = tracemalloc.get_traced_memory()[0]
        for _ in range(ITERATIONS):
            fn()
        gc.collect()
        live_after = _live(type_name)
        bytes_after = tracemalloc.get_traced_memory()[0]
    finally:
        tracemalloc.stop()
    return live_after - live_before, (bytes_after - bytes_before) / ITERATIONS


@pytest.fixture
def nonblocking_listener():
    sock = nss.io.Socket(nss.io.PR_AF_INET)
    sock.set_socket_option(nss.io.PR_SockOpt_Reuseaddr, True)
    sock.bind(nss.io.NetworkAddress(nss.io.PR_IpAddrLoopback, 0))
    sock.listen(1)
    sock.set_socket_option(nss.io.PR_SockOpt_Nonblocking, True)
    yield sock
    sock.close()


class TestErrorReferenceLeaks:
    """NSPR errors must be released once nothing refers to them."""

    def test_error_raised_from_c_is_released(self, nonblocking_listener):
        def accept_nothing():
            with pytest.raises(nss.error.NSPRError) as exc_info:
                nonblocking_listener.accept()
            assert exc_info.value.errno == nss.error.PR_WOULD_BLOCK_ERROR

        survivors, per_call = _growth(accept_nothing, "NSPRError")
        assert survivors == 0
        assert per_call < MAX_BYTES_PER_ITERATION

    def test_error_with_message_raised_from_c_is_released(self):
        # A C path raising with a formatted message: that message string
        # was leaked on top of the exception itself.
        def parse_bad_name():
            with pytest.raises(nss.error.NSPRError) as exc_info:
                nss.nss.DN("this is not=a,,=valid=name")
            assert "cannot parse X500 name" in str(exc_info.value)

        survivors, per_call = _growth(parse_bad_name, "NSPRError")
        assert survivors == 0
        assert per_call < MAX_BYTES_PER_ITERATION

    def test_nspr_error_construction_does_not_leak(self):
        def construct():
            nss.error.NSPRError("message", nss.error.PR_WOULD_BLOCK_ERROR)

        survivors, per_call = _growth(construct, "NSPRError")
        assert survivors == 0
        assert per_call < MAX_BYTES_PER_ITERATION

    def test_cert_verify_error_construction_does_not_leak(self):
        def construct():
            # (error_message, error_code, usages)
            nss.error.CertVerifyError("message", nss.error.SEC_ERROR_EXPIRED_CERTIFICATE, 1)

        survivors, per_call = _growth(construct, "CertVerifyError")
        assert survivors == 0
        assert per_call < MAX_BYTES_PER_ITERATION

    def test_rejected_arguments_do_not_leak(self):
        # The message is converted before the error code is parsed; a bad
        # code used to strand the message's reference.
        message = "a message long enough to be its own allocation" * 2

        def construct_nspr_error():
            with pytest.raises(TypeError):
                nss.error.NSPRError(message + "x", "not-an-int")

        def construct_cert_verify_error():
            with pytest.raises(TypeError):
                nss.error.CertVerifyError(message + "y", "not-an-int", 1)

        for fn, type_name in (
            (construct_nspr_error, "NSPRError"),
            (construct_cert_verify_error, "CertVerifyError"),
        ):
            survivors, per_call = _growth(fn, type_name)
            assert survivors == 0
            assert per_call < MAX_BYTES_PER_ITERATION

    def test_failed_verify_with_log_does_not_leak(self, nss_clean_state):
        # The CertVerifyLog handed to the exception was a new reference
        # the caller never released. It is not tracked by the garbage
        # collector, so only its bytes show the leak.
        certdb = nss_clean_state

        def fail_verification(cert):
            exc_info = None
            try:
                with pytest.raises(nss.error.CertVerifyError) as exc_info:
                    cert.verify_with_log(certdb, True, nss.nss.certificateUsageEmailSigner, None)
                # The log still belongs to the exception, and is usable.
                assert exc_info.value.log is not None
                assert len(exc_info.value.log) >= 0
            finally:
                # A failure here would keep this frame, and with it the
                # certificate and the log, alive in its traceback.
                del cert
                exc_info = None

        # Held through a list that is emptied on every path: the fixture
        # shuts NSS down afterwards, which NSS refuses while a certificate
        # is still referenced - by a failed assertion's traceback, say.
        held = [nss.nss.find_cert_from_nickname("test_server")]
        try:
            _, per_call = _growth(lambda: fail_verification(held[0]), "CertVerifyError")
            assert per_call < MAX_BYTES_PER_ITERATION
        finally:
            held.clear()

    def test_error_attributes_survive_the_fix(self):
        err = nss.error.NSPRError("message", nss.error.PR_WOULD_BLOCK_ERROR)
        assert err.errno == nss.error.PR_WOULD_BLOCK_ERROR
        assert str(err).startswith("message: ")
        assert err.error_desc in str(err)

        bare = nss.error.NSPRError(None, nss.error.PR_WOULD_BLOCK_ERROR)
        assert str(bare) == bare.error_desc

        cve = nss.error.CertVerifyError("message", nss.error.SEC_ERROR_EXPIRED_CERTIFICATE, 5)
        assert cve.errno == nss.error.SEC_ERROR_EXPIRED_CERTIFICATE
        assert cve.usages == 5
