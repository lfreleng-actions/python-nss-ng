# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Type stubs for nss.ssl module.

This file provides type hints for the C extension module nss.ssl.
"""

import socket
from collections.abc import Callable
from typing import Any

# SSL Policy
def set_domestic_policy() -> None:
    """Set domestic (strong) SSL policy."""
    ...

def set_export_policy() -> None:
    """Set export (weak) SSL policy."""
    ...

def set_france_policy() -> None:
    """Set France-specific SSL policy."""
    ...

# SSL Options
def set_ssl_default_option(option: int, value: bool) -> None:
    """Set a default SSL option for all new sockets."""
    ...

def get_ssl_default_option(option: int) -> bool:
    """Get a default SSL option value."""
    ...

# Cipher preferences
def set_default_cipher_pref(cipher: int, enabled: bool) -> None:
    """Set default cipher preference for all new sockets."""
    ...

def get_default_cipher_pref(cipher: int) -> bool:
    """Get default cipher preference."""
    ...

def set_cipher_policy(cipher: int, policy: int) -> None:
    """Set cipher policy."""
    ...

def get_cipher_policy(cipher: int) -> int:
    """Get cipher policy."""
    ...

# SSL Version Range
#
# Functions returning a version range accept the optional ``repr_kind``
# keyword argument (one of the ``nss.As*`` constants) to control how
# the returned tuple members are represented.
def get_default_ssl_version_range(repr_kind: int = ...) -> tuple[Any, Any]:
    """Get the default SSL/TLS version range."""
    ...

def set_default_ssl_version_range(
    min_version: int | str, max_version: int | str, variant: int = 0
) -> None:
    """Set the default SSL/TLS version range.

    Each version argument may be either a
    ``SSL_LIBRARY_VERSION_*`` enumerated constant (int) or its
    string equivalent (e.g. ``'tls1.2'``).
    """
    ...

def get_supported_ssl_version_range(repr_kind: int = ...) -> tuple[Any, Any]:
    """Get the supported SSL/TLS version range."""
    ...

def get_ssl_version_from_major_minor(major: int, minor: int) -> int:
    """Get SSL version from major and minor version numbers."""
    ...

def ssl_library_version_name(version: int = 0, repr_kind: int = ...) -> str:
    """Get the name of an SSL library version."""
    ...

def ssl_library_version_from_name(name: str) -> int:
    """Get the SSL library version from its name."""
    ...

# Cipher suite info
def get_cipher_suite_info(cipher: int) -> SSLCipherSuiteInfo:
    """Get information about a cipher suite."""
    ...

def ssl_cipher_suite_name(cipher: int) -> str:
    """Get the name of a cipher suite."""
    ...

def ssl_cipher_suite_from_name(name: str) -> int:
    """Get the cipher suite from its name."""
    ...

# Session cache management
def config_server_session_id_cache(
    max_cache_entries: int = 0,
    timeout: int = 0,
    ssl3_timeout: int = 0,
    directory: str | None = None,
) -> None:
    """Configure the server session ID cache."""
    ...

def config_mp_server_sid_cache(
    max_cache_entries: int = 0,
    timeout: int = 0,
    ssl3_timeout: int = 0,
    directory: str | None = None,
) -> None:
    """Configure multi-process server session ID cache."""
    ...

def config_server_session_id_cache_with_opt(
    timeout: int = 0,
    ssl3_timeout: int = 0,
    directory: str | None = None,
    max_cache_entries: int = 0,
    max_cert_cache_entries: int = 0,
    max_srv_name_cache_entries: int = 0,
) -> None:
    """Configure server session ID cache with additional options."""
    ...

def get_max_server_cache_locks() -> int:
    """Get the maximum number of server cache locks."""
    ...

def set_max_server_cache_locks(max_locks: int) -> None:
    """Set the maximum number of server cache locks."""
    ...

def clear_session_cache() -> None:
    """Clear the SSL session cache."""
    ...

def shutdown_server_session_id_cache() -> None:
    """Shutdown the server session ID cache."""
    ...

# SSL Constants

# Protocol versions
SSL_LIBRARY_VERSION_2: int
SSL_LIBRARY_VERSION_3_0: int
SSL_LIBRARY_VERSION_TLS_1_0: int
SSL_LIBRARY_VERSION_TLS_1_1: int
SSL_LIBRARY_VERSION_TLS_1_2: int
SSL_LIBRARY_VERSION_TLS_1_3: int

# SSL Options
SSL_SECURITY: int
SSL_SOCKS: int
SSL_REQUEST_CERTIFICATE: int
SSL_HANDSHAKE_AS_CLIENT: int
SSL_HANDSHAKE_AS_SERVER: int
SSL_ENABLE_SSL2: int
SSL_ENABLE_SSL3: int
SSL_NO_CACHE: int
SSL_REQUIRE_CERTIFICATE: int
SSL_ENABLE_FDX: int
SSL_V2_COMPATIBLE_HELLO: int
SSL_ENABLE_TLS: int
SSL_ROLLBACK_DETECTION: int
SSL_NO_STEP_DOWN: int
SSL_BYPASS_PKCS11: int
SSL_NO_LOCKS: int
SSL_ENABLE_SESSION_TICKETS: int
SSL_ENABLE_DEFLATE: int
SSL_ENABLE_RENEGOTIATION: int
SSL_REQUIRE_SAFE_NEGOTIATION: int
SSL_ENABLE_FALSE_START: int
SSL_CBC_RANDOM_IV: int
SSL_ENABLE_OCSP_STAPLING: int
SSL_ENABLE_NPN: int
SSL_ENABLE_ALPN: int
SSL_REUSE_SERVER_ECDHE_KEY: int
SSL_ENABLE_FALLBACK_SCSV: int
SSL_ENABLE_SERVER_DHE: int
SSL_ENABLE_EXTENDED_MASTER_SECRET: int
SSL_ENABLE_SIGNED_CERT_TIMESTAMPS: int
SSL_REQUIRE_DH_NAMED_GROUPS: int
SSL_ENABLE_0RTT_DATA: int
SSL_RECORD_SIZE_LIMIT: int

# Renegotiation options
SSL_RENEGOTIATE_NEVER: int
SSL_RENEGOTIATE_UNRESTRICTED: int
SSL_RENEGOTIATE_REQUIRES_XTN: int
SSL_RENEGOTIATE_TRANSITIONAL: int

# Certificate request types
SSL_REQUEST_NEVER: int
SSL_REQUEST_FIRST_HANDSHAKE: int
SSL_REQUEST_SUBSEQUENT_HANDSHAKES: int
SSL_REQUEST_ALWAYS: int

# Variant types
ssl_variant_stream: int
ssl_variant_datagram: int

# Additional types
SSLChannelInfo = Any
SSLCipherSuiteInfo = Any

class SSLSocket:
    """SSL socket class wrapping NSPR sockets."""

    def __init__(self, family: int = socket.AF_INET) -> None:
        """
        Create a new SSL socket.

        Args:
            family: Address family (AF_INET or AF_INET6)
        """
        ...

    def set_ssl_option(self, option: int, value: bool) -> None:
        """
        Set an SSL socket option.

        Args:
            option: SSL option constant (e.g., SSL_SECURITY)
            value: Boolean value to set
        """
        ...

    def get_ssl_option(self, option: int) -> bool:
        """
        Get an SSL socket option value.

        Args:
            option: SSL option constant

        Returns:
            Current value of the option
        """
        ...

    def set_hostname(self, hostname: str) -> None:
        """
        Set the expected hostname for certificate verification.

        Args:
            hostname: Expected hostname
        """
        ...

    def get_hostname(self) -> str:
        """Get the expected hostname."""
        ...

    def set_handshake_callback(self, callback: Callable[..., None] | None) -> None:
        """
        Set callback function called when SSL handshake completes.

        Args:
            callback: Function to call on handshake completion
        """
        ...

    def set_auth_certificate_callback(
        self, callback: Callable[..., bool] | None, *args: Any
    ) -> None:
        """
        Set callback function for certificate authentication.

        Args:
            callback: Function to verify certificates
            *args: Additional arguments passed to callback
        """
        ...

    def set_client_auth_data_callback(
        self, callback: Callable[..., Any] | None, *args: Any
    ) -> None:
        """
        Set callback function for client authentication.

        The C extension accepts a callback returning a
        ``(certificate, private_key)`` tuple on success or any
        falsey value (``None``, ``False``) to decline; the static
        signature is intentionally permissive (``Callable[..., Any]``)
        to accommodate both forms.

        Args:
            callback: Function to provide client certificate
            *args: Additional arguments passed to callback
        """
        ...

    def set_pkcs11_pin_arg(self, pin_arg: Any) -> None:
        """Set PKCS#11 PIN argument for certificate operations."""
        ...

    def get_pkcs11_pin_arg(self) -> Any:
        """Get PKCS#11 PIN argument."""
        ...

    def set_ssl_version_range(
        self,
        min_version: int | str,
        max_version: int | str,
    ) -> None:
        """
        Set the SSL/TLS version range for this socket.

        Args:
            min_version: Minimum protocol version. Either a
                ``SSL_LIBRARY_VERSION_*`` enumerated constant (int) or
                its string equivalent (e.g. ``'tls1.1'``).
            max_version: Maximum protocol version. Either a
                ``SSL_LIBRARY_VERSION_*`` enumerated constant (int) or
                its string equivalent (e.g. ``'tls1.2'``).
        """
        ...

    def get_ssl_version_range(self, repr_kind: int = ...) -> tuple[Any, Any]:
        """
        Get the SSL/TLS version range.

        Args:
            repr_kind: One of the ``nss.As*`` constants controlling
                the representation of the returned tuple members
                (defaults to ``nss.AsEnum`` in the C extension).

        Returns:
            Tuple of (min_version, max_version)
        """
        ...

    def reset_handshake(self, as_server: bool = False) -> None:
        """
        Reset the SSL handshake state.

        Args:
            as_server: True if acting as server, False for client
        """
        ...

    def force_handshake(self) -> None:
        """Force the SSL handshake to complete."""
        ...

    def config_secure_server(self, cert: Any, private_key: Any, kea_type: int) -> None:
        """Configure socket as a secure server."""
        ...

    def get_peer_certificate(self, force_handshake: bool = False) -> Any:
        """Get the peer's certificate after handshake."""
        ...

    def get_certificate(self, force_handshake: bool = False) -> Any:
        """Get the local certificate."""
        ...

    def invalidate_session(self) -> None:
        """Invalidate the current SSL session."""
        ...

    def data_pending(self) -> int:
        """Check if data is pending on the socket."""
        ...

    def get_security_status(self) -> tuple[int, str, int, int, str, str, str]:
        """Get security status information."""
        ...

    def get_session_id(self) -> bytes:
        """Get the SSL session ID."""
        ...

    def set_sock_peer_id(self, peer_id: str) -> None:
        """Set the peer ID for session caching."""
        ...

    def set_certificate_db(self, certdb: Any) -> None:
        """Set the certificate database for this socket."""
        ...

    def force_handshake_timeout(self, timeout: int) -> None:
        """Force handshake with timeout."""
        ...

    def rehandshake(self, flush_cache: bool = False) -> None:
        """Initiate SSL renegotiation."""
        ...

    def rehandshake_timeout(self, flush_cache: bool, timeout: int) -> None:
        """Initiate SSL renegotiation with timeout."""
        ...

    @staticmethod
    def import_tcp_socket(sock: socket.socket) -> SSLSocket:
        """Import a Python TCP socket as an SSL socket."""
        ...

    def get_ssl_channel_info(self) -> SSLChannelInformation:
        """Get SSL channel information."""
        ...

    def get_negotiated_host(self) -> str:
        """Get the negotiated hostname (SNI)."""
        ...

    def connection_info_format_lines(self, level: int = 0) -> Any:
        """Format connection information as indented lines."""
        ...

    def connection_info_format(self, level: int = 0, indent: str = "    ") -> str:
        """Format connection information as a string."""
        ...

    def connection_info_str(self) -> str:
        """Get connection information as a string."""
        ...

    def set_cipher_pref(self, cipher: int, enabled: bool) -> None:
        """
        Set cipher suite preference.

        Args:
            cipher: Cipher suite identifier
            enabled: True to enable, False to disable
        """
        ...

    def get_cipher_pref(self, cipher: int) -> bool:
        """Get cipher suite preference."""
        ...

    # Socket operations (NSPR socket interface)
    def connect(self, addr: Any, timeout: int | None = None) -> None:
        """
        Connect to a remote address.

        Args:
            addr: Network address object
            timeout: Connection timeout in milliseconds
        """
        ...

    def bind(self, addr: Any) -> None:
        """Bind to a local address."""
        ...

    def listen(self, backlog: int = 5) -> None:
        """Listen for connections."""
        ...

    def accept(self, timeout: int | None = None) -> tuple[SSLSocket, Any]:
        """
        Accept an incoming connection.

        Returns:
            Tuple of (connected_socket, peer_address)
        """
        ...

    def send(self, data: bytes, flags: int = 0) -> int:
        """
        Send data over the socket.

        Returns:
            Number of bytes sent
        """
        ...

    def recv(self, bufsize: int, flags: int = 0) -> bytes:
        """
        Receive data from the socket.

        Returns:
            Received data
        """
        ...

    def close(self) -> None:
        """Close the socket."""
        ...

    def shutdown(self, how: int = socket.SHUT_RDWR) -> None:
        """Shutdown the socket connection."""
        ...

    def set_socket_option(self, option: int, value: Any) -> None:
        """Set a socket option."""
        ...

    def get_socket_option(self, option: int) -> Any:
        """Get a socket option value."""
        ...

    def fileno(self) -> int:
        """Get the file descriptor number."""
        ...

    def readline(self, size: int = -1) -> bytes:
        """Read a single line from the SSL socket.

        Returns the line including the trailing newline byte (if any).
        """
        ...

    def makefile(self, mode: str = "r", buffering: int = -1) -> Any:
        """Create a file-like object from the socket."""
        ...

class SSLChannelInformation:
    """Information about an SSL channel."""

    @property
    def protocol_version(self) -> int:
        """Get the negotiated protocol version."""
        ...

    @property
    def cipher_suite(self) -> int:
        """Get the negotiated cipher suite."""
        ...

    @property
    def auth_key_bits(self) -> int:
        """Get the authentication key length in bits."""
        ...

    @property
    def key_exchange_key_bits(self) -> int:
        """Get the key exchange key length in bits."""
        ...

    @property
    def creation_time(self) -> int:
        """Get the creation time."""
        ...

    @property
    def last_access_time(self) -> int:
        """Get the last access time."""
        ...

    @property
    def expiration_time(self) -> int:
        """Get the expiration time."""
        ...

    @property
    def compression_method(self) -> int:
        """Get the compression method."""
        ...

    @property
    def compression_method_name(self) -> str:
        """Get the compression method name."""
        ...

    def format_lines(self, level: int = 0) -> Any:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class SSLCipherSuiteInformation:
    """Information about an SSL cipher suite."""

    @property
    def cipher_suite(self) -> int:
        """Get the cipher suite identifier."""
        ...

    @property
    def cipher_suite_name(self) -> str:
        """Get the cipher suite name."""
        ...

    @property
    def auth_algorithm(self) -> int:
        """Get the authentication algorithm."""
        ...

    @property
    def auth_algorithm_name(self) -> str:
        """Get the authentication algorithm name."""
        ...

    @property
    def kea_type(self) -> int:
        """Get the key exchange algorithm type."""
        ...

    @property
    def kea_type_name(self) -> str:
        """Get the key exchange algorithm name."""
        ...

    @property
    def symmetric_cipher(self) -> int:
        """Get the symmetric cipher algorithm."""
        ...

    @property
    def symmetric_cipher_name(self) -> str:
        """Get the symmetric cipher name."""
        ...

    @property
    def mac_algorithm(self) -> int:
        """Get the MAC algorithm."""
        ...

    @property
    def mac_algorithm_name(self) -> str:
        """Get the MAC algorithm name."""
        ...

    @property
    def effective_key_bits(self) -> int:
        """Get the effective key length in bits."""
        ...

    @property
    def is_fips(self) -> bool:
        """Check if the cipher suite is FIPS compliant."""
        ...

    @property
    def is_exportable(self) -> bool:
        """Check if the cipher suite is exportable."""
        ...

    def format_lines(self, level: int = 0) -> Any:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

# Cipher suite constants (examples - there are many more)
TLS_NULL_WITH_NULL_NULL: int
TLS_RSA_WITH_NULL_MD5: int
TLS_RSA_WITH_NULL_SHA: int
TLS_RSA_WITH_RC4_128_MD5: int
TLS_RSA_WITH_RC4_128_SHA: int
TLS_RSA_WITH_3DES_EDE_CBC_SHA: int
TLS_RSA_WITH_AES_128_CBC_SHA: int
TLS_RSA_WITH_AES_256_CBC_SHA: int
TLS_RSA_WITH_AES_128_CBC_SHA256: int
TLS_RSA_WITH_AES_256_CBC_SHA256: int
TLS_RSA_WITH_AES_128_GCM_SHA256: int
TLS_RSA_WITH_AES_256_GCM_SHA384: int
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256: int
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384: int
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256: int
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384: int
TLS_AES_128_GCM_SHA256: int
TLS_AES_256_GCM_SHA384: int
TLS_CHACHA20_POLY1305_SHA256: int

# ---------------------------------------------------------------------------
# Dynamic module attributes
# ---------------------------------------------------------------------------
#
# The C extension registers many further integer constants at module
# init time -- the full set of ``SSL_*`` cipher-suite identifiers,
# ``SSL_LIBRARY_VERSION_*`` enumerators, ``SSL_*`` option flags, and
# legacy aliases such as ``ssl_implemented_ciphers``. Enumerating every
# one of them here would be both tedious and brittle, so a
# module-level ``__getattr__`` returning ``Any`` is provided to
# satisfy static type checkers for any such attribute access. Symbols
# that are explicitly typed above retain their precise types; this
# fallback only kicks in for names not already declared.
def __getattr__(name: str) -> Any: ...
