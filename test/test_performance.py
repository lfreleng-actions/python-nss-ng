# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Performance and stress tests for python-nss-ng.

This module tests performance characteristics, stress conditions,
and resource handling under load.
"""

import gc
import os
import sys
import threading
import time

import pytest

# Add test directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nss.nss as nss
from nss.error import NSPRError


class TestDigestPerformance:
    """Test digest operation performance."""

    @pytest.mark.slow
    def test_digest_small_data_performance(self, nss_db_context):
        """Test digest performance with small data."""
        test_data = b"Small test data" * 10
        iterations = 1000

        start_time = time.time()
        for _ in range(iterations):
            digest = nss.sha256_digest(test_data)
            assert digest is not None
        end_time = time.time()

        elapsed = end_time - start_time
        operations_per_second = iterations / elapsed

        # Should be able to perform many operations per second
        assert operations_per_second > 100, (
            f"Performance too slow: {operations_per_second:.2f} ops/sec"
        )

    @pytest.mark.slow
    def test_digest_large_data_performance(self, nss_db_context):
        """Test digest performance with large data."""
        # 10 MB of data
        test_data = b"X" * (10 * 1024 * 1024)
        iterations = 10

        start_time = time.time()
        for _ in range(iterations):
            digest = nss.sha256_digest(test_data)
            assert digest is not None
        end_time = time.time()

        elapsed = end_time - start_time

        # Should complete in reasonable time
        assert elapsed < 30, f"Large data digest too slow: {elapsed:.2f} seconds"

    @pytest.mark.slow
    def test_incremental_digest_performance(self, nss_db_context):
        """Test incremental digest performance."""
        chunk_size = 4096
        chunks = [b"X" * chunk_size for _ in range(100)]
        iterations = 100

        start_time = time.time()
        for _ in range(iterations):
            context = nss.create_digest_context(nss.SEC_OID_SHA256)
            context.digest_begin()
            for chunk in chunks:
                context.digest_op(chunk)
            digest = context.digest_final()
            assert digest is not None
        end_time = time.time()

        elapsed = end_time - start_time
        operations_per_second = iterations / elapsed

        # Should handle incremental digests efficiently
        assert operations_per_second > 10, (
            f"Incremental digest too slow: {operations_per_second:.2f} ops/sec"
        )

    @pytest.mark.slow
    def test_multiple_algorithm_performance(self, nss_db_context):
        """Test performance with multiple algorithms."""
        test_data = b"Test data" * 100
        iterations = 100

        algorithms = [
            (nss.md5_digest, "MD5"),
            (nss.sha1_digest, "SHA1"),
            (nss.sha256_digest, "SHA256"),
            (nss.sha512_digest, "SHA512"),
        ]

        for algo_func, algo_name in algorithms:
            start_time = time.time()
            for _ in range(iterations):
                digest = algo_func(test_data)
                assert digest is not None
            end_time = time.time()

            elapsed = end_time - start_time
            # All algorithms should complete reasonably fast
            assert elapsed < 5, f"{algo_name} too slow: {elapsed:.2f} seconds"


class TestCertificatePerformance:
    """Test certificate operation performance."""

    @pytest.mark.slow
    def test_certificate_lookup_performance(self, nss_db_context):
        """Test certificate lookup performance."""
        iterations = 100

        start_time = time.time()
        for _ in range(iterations):
            try:
                cert = nss.find_cert_from_nickname("test_ca")
                if cert is not None:
                    # Access basic properties
                    subject = cert.subject
            except NSPRError:
                # Certificate might not exist, but test performance
                pass
        end_time = time.time()

        elapsed = end_time - start_time
        operations_per_second = iterations / elapsed

        # Certificate lookups should be reasonably fast
        assert operations_per_second > 10, (
            f"Certificate lookup too slow: {operations_per_second:.2f} ops/sec"
        )

    @pytest.mark.slow
    def test_certificate_validation_performance(self, nss_db_context):
        """Test certificate validation performance."""
        try:
            cert = nss.find_cert_from_nickname("test_server")
        except NSPRError:
            pytest.skip("test_server certificate not available")

        iterations = 50

        start_time = time.time()
        for _ in range(iterations):
            try:
                approved_usage = cert.verify_now(
                    nss_db_context, True, nss.certificateUsageSSLServer
                )
            except NSPRError:
                # Validation might fail, but test performance
                pass
        end_time = time.time()

        elapsed = end_time - start_time

        # Validation should be reasonably fast
        assert elapsed < 10, f"Certificate validation too slow: {elapsed:.2f} seconds"


class TestMemoryUsage:
    """Test memory usage patterns."""

    @pytest.mark.slow
    def test_digest_memory_stable(self, nss_db_context):
        """Test that digest operations don't leak memory."""
        test_data = b"Memory test data" * 1000
        iterations = 1000

        # Force garbage collection
        gc.collect()
        baseline_blocks = sys.getallocatedblocks()

        # Perform many digest operations
        for _ in range(iterations):
            digest = nss.sha256_digest(test_data)
            assert digest is not None

        # Force garbage collection
        gc.collect()

        # sha256_digest returns bytes, which the cyclic GC does not track, so
        # count CPython allocator blocks instead: a retained result costs one
        # block per iteration. Native NSS allocations stay invisible here.
        growth = sys.getallocatedblocks() - baseline_blocks
        assert growth < iterations // 10, f"Digest operations leaked {growth} blocks"

    @pytest.mark.slow
    def test_certificate_reference_memory(self, nss_db_context):
        """Test that certificate references don't leak memory."""
        iterations = 500

        # Force garbage collection
        gc.collect()
        baseline_blocks = sys.getallocatedblocks()

        found = 0
        for _ in range(iterations):
            cert = nss.find_cert_from_nickname("test_ca")
            if cert is not None:
                # Access properties
                subject = cert.subject
                found += 1
            # Let cert go out of scope

        # Force garbage collection
        gc.collect()

        # The nss_db_context fixture creates test_ca, so every lookup has to
        # return a certificate; without this the loop could allocate nothing
        # and leave the growth check below unable to fail.
        assert found == iterations, f"Only {found} of {iterations} lookups found test_ca"

        # CertificateType carries no Py_TPFLAGS_HAVE_GC, so a retained wrapper
        # never reaches gc.get_objects(); it does cost an allocator block.
        growth = sys.getallocatedblocks() - baseline_blocks
        assert growth < iterations // 10, f"Certificate lookups leaked {growth} blocks"

    @pytest.mark.slow
    def test_digest_context_memory(self, nss_db_context):
        """Test that digest contexts don't leak memory."""
        iterations = 500

        # Force garbage collection
        gc.collect()
        baseline_blocks = sys.getallocatedblocks()

        for _ in range(iterations):
            context = nss.create_digest_context(nss.SEC_OID_SHA256)
            context.digest_begin()
            context.digest_op(b"test data")
            digest = context.digest_final()
            assert digest is not None
            # Let context go out of scope

        # Force garbage collection
        gc.collect()

        # PK11ContextType is likewise untracked by the cyclic GC; the allocator
        # block count still rises by one per retained context.
        growth = sys.getallocatedblocks() - baseline_blocks
        assert growth < iterations // 10, f"Digest contexts leaked {growth} blocks"


class TestStressConditions:
    """Test system behavior under stress."""

    @pytest.mark.slow
    def test_many_digest_contexts(self, nss_db_context):
        """Test creating many digest contexts."""
        contexts = []

        # Create many contexts
        for i in range(100):
            context = nss.create_digest_context(nss.SEC_OID_SHA256)
            context.digest_begin()
            context.digest_op(f"Data {i}".encode())
            contexts.append(context)

        # Finalize all contexts
        digests = []
        for context in contexts:
            digest = context.digest_final()
            assert digest is not None
            digests.append(digest)

        # All digests should be valid
        assert len(digests) == 100

    @pytest.mark.slow
    def test_rapid_context_creation_destruction(self, nss_db_context):
        """Test rapid creation and destruction of contexts."""
        iterations = 500
        expected = nss.sha256_digest(b"test")

        for _ in range(iterations):
            context = nss.create_digest_context(nss.SEC_OID_SHA256)
            context.digest_begin()
            context.digest_op(b"test")
            digest = context.digest_final()
            # Rapid churn must not carry state between contexts
            assert digest == expected
            # Context destroyed immediately

    @pytest.mark.slow
    def test_large_data_chunks(self, nss_db_context):
        """Test processing very large data."""
        # 50 MB of data
        large_data = b"X" * (50 * 1024 * 1024)

        # Should handle large data without crashing
        digest = nss.sha256_digest(large_data)
        assert digest is not None
        assert len(digest) == 32

    @pytest.mark.slow
    def test_many_small_operations(self, nss_db_context):
        """Test many small operations in sequence."""
        iterations = 5000
        test_data = b"small"
        expected = nss.sha256_digest(test_data)

        for _ in range(iterations):
            digest = nss.sha256_digest(test_data)
            assert digest == expected


class TestConcurrentPerformance:
    """Test concurrent operation performance."""

    @pytest.mark.slow
    @pytest.mark.skipif(
        os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true",
        reason="NSS has threading race conditions in CI environments",
    )
    def test_concurrent_digest_performance(self, nss_db_context):
        """Test performance with concurrent digest operations.

        Note: Skipped in CI due to NSS threading race conditions.
        """
        test_data = b"Concurrent test" * 100
        iterations_per_thread = 100
        num_threads = 5

        def worker():
            for _ in range(iterations_per_thread):
                digest = nss.sha256_digest(test_data)
                assert digest is not None

        threads = []
        start_time = time.time()

        for _ in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=30)

        end_time = time.time()
        elapsed = end_time - start_time

        total_operations = iterations_per_thread * num_threads
        operations_per_second = total_operations / elapsed

        # Concurrent operations should complete reasonably fast
        assert elapsed < 20, f"Concurrent operations too slow: {elapsed:.2f} seconds"
        assert operations_per_second > 50, (
            f"Throughput too low: {operations_per_second:.2f} ops/sec"
        )

    @pytest.mark.slow
    @pytest.mark.skipif(
        os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true",
        reason="NSS certificate database operations are not thread-safe in CI",
    )
    def test_thread_contention(self, nss_db_context):
        """Test behavior under thread contention.

        Note: Skipped in CI due to NSS threading issues with certificate database.
        """
        num_threads = 10
        iterations_per_thread = 50
        errors = []

        def worker(thread_id):
            try:
                for _ in range(iterations_per_thread):
                    # Mix of operations
                    digest = nss.sha256_digest(b"test data")
                    assert digest is not None

                    try:
                        cert = nss.find_cert_from_nickname("test_ca")
                    except NSPRError:
                        pass
            except Exception as e:
                errors.append((thread_id, e))

        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=30)

        # Should complete without errors
        assert len(errors) == 0, f"Thread errors: {errors}"


class TestResourceLimits:
    """Test behavior at resource limits."""

    @pytest.mark.slow
    def test_maximum_data_size(self, nss_db_context):
        """Test with maximum practical data size."""
        # 100 MB (practical limit for testing)
        try:
            large_data = b"X" * (100 * 1024 * 1024)
            digest = nss.sha256_digest(large_data)
            assert digest is not None
        except MemoryError:
            pytest.skip("Not enough memory for test")

    @pytest.mark.slow
    def test_long_running_operation(self, nss_db_context):
        """Test long-running digest operation."""
        # Create context and feed it data over time
        context = nss.create_digest_context(nss.SEC_OID_SHA256)
        context.digest_begin()

        # Feed data in chunks over time
        chunk = b"X" * 1024
        for _ in range(1000):
            context.digest_op(chunk)

        digest = context.digest_final()
        assert digest is not None

    @pytest.mark.slow
    def test_context_reuse_limits(self, nss_db_context):
        """Test limits of context reuse."""
        # A context should not be reusable after finalization
        context = nss.create_digest_context(nss.SEC_OID_SHA256)
        context.digest_begin()
        context.digest_op(b"test")
        digest = context.digest_final()
        assert digest is not None

        # Attempting to reuse should fail or require new begin
        # Behavior may vary
        try:
            context.digest_op(b"more")
            # Some implementations might allow this
        except (NSPRError, RuntimeError):
            # Expected - context is finalized
            pass


class TestScalability:
    """Test scalability characteristics."""

    @pytest.mark.slow
    def test_scales_with_data_size(self, nss_db_context):
        """Test that performance scales linearly with data size."""
        base_size = 1024
        base_data = b"X" * base_size

        # Time small data
        start = time.time()
        for _ in range(100):
            nss.sha256_digest(base_data)
        small_time = time.time() - start

        # Time larger data (10x size)
        large_data = b"X" * (base_size * 10)
        start = time.time()
        for _ in range(100):
            nss.sha256_digest(large_data)
        large_time = time.time() - start

        # Larger data should take more time, but not excessively more
        # Allow up to 15x time for 10x data (generous for overhead)
        ratio = large_time / small_time
        assert ratio < 15, f"Poor scaling: {ratio:.2f}x time for 10x data"

    @pytest.mark.slow
    def test_scales_with_operation_count(self, nss_db_context):
        """Test that performance is acceptable for many operations."""
        test_data = b"Test" * 100

        # Run many operations and ensure reasonable throughput
        # This test verifies we can handle sustained load without hanging
        num_operations = 1000
        start = time.time()
        for _ in range(num_operations):
            nss.sha256_digest(test_data)
        elapsed = time.time() - start

        # Should complete 1000 operations in under 5 seconds even on slow CI
        # This is a very conservative threshold (200 ops/sec minimum)
        assert elapsed < 5.0, f"Too slow: {num_operations} operations took {elapsed:.2f}s"

        # Calculate and log throughput for informational purposes
        ops_per_sec = num_operations / elapsed
        # Throughput should be reasonable (at least 200 ops/sec)
        assert ops_per_sec > 200, f"Low throughput: {ops_per_sec:.0f} ops/sec"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
