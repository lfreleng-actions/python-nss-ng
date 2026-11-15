# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Type stubs for nss.io module.

This file provides type hints for the C extension module nss.io (NSPR I/O).
"""

import socket
from typing import Any

# Time conversion utilities
def seconds_to_interval(seconds: float) -> int:
    """
    Convert seconds to NSPR interval (microseconds).

    Args:
        seconds: Time in seconds

    Returns:
        Time in NSPR interval units (microseconds)
    """
    ...

def interval_to_seconds(interval: int) -> float:
    """
    Convert NSPR interval to seconds.

    Args:
        interval: Time in NSPR interval units (microseconds)

    Returns:
        Time in seconds
    """
    ...

def milliseconds_to_interval(milliseconds: int) -> int:
    """Convert milliseconds to NSPR interval."""
    ...

def interval_to_milliseconds(interval: int) -> int:
    """Convert NSPR interval to milliseconds."""
    ...

def microseconds_to_interval(microseconds: int) -> int:
    """Convert microseconds to NSPR interval."""
    ...

def interval_to_microseconds(interval: int) -> int:
    """Convert NSPR interval to microseconds."""
    ...

def interval_now() -> int:
    """Get current time as NSPR interval."""
    ...

def ticks_per_second() -> int:
    """Get the number of ticks per second."""
    ...

# Network byte order conversion
def htons(value: int) -> int:
    """Convert 16-bit integer from host to network byte order."""
    ...

def htonl(value: int) -> int:
    """Convert 32-bit integer from host to network byte order."""
    ...

def ntohs(value: int) -> int:
    """Convert 16-bit integer from network to host byte order."""
    ...

def ntohl(value: int) -> int:
    """Convert 32-bit integer from network to host byte order."""
    ...

# Protocol lookup
def get_proto_by_name(name: str) -> int:
    """Get protocol number by name."""
    ...

def get_proto_by_number(number: int) -> str:
    """Get protocol name by number."""
    ...

def addr_family_name(family: int) -> str:
    """Get the name of an address family."""
    ...

# Network address family constants
PR_AF_INET: int
PR_AF_INET6: int
PR_AF_LOCAL: int

# Socket type constants
SOCK_STREAM: int
SOCK_DGRAM: int

# Shutdown constants
PR_SHUTDOWN_RCV: int
PR_SHUTDOWN_SEND: int
PR_SHUTDOWN_BOTH: int

# Socket option constants
PR_SockOpt_Nonblocking: int
PR_SockOpt_Reuseaddr: int
PR_SockOpt_Keepalive: int
PR_SockOpt_RecvBufferSize: int
PR_SockOpt_SendBufferSize: int
PR_SockOpt_IpTimeToLive: int
PR_SockOpt_IpTypeOfService: int
PR_SockOpt_AddMember: int
PR_SockOpt_DropMember: int
PR_SockOpt_McastInterface: int
PR_SockOpt_McastTimeToLive: int
PR_SockOpt_McastLoopback: int
PR_SockOpt_NoDelay: int
PR_SockOpt_MaxSegment: int
PR_SockOpt_Broadcast: int

# Network address manipulation
class NetworkAddress:
    """Represents a network address (IPv4 or IPv6)."""

    def __init__(
        self,
        addr: str | int | tuple[str, int] | None = None,
        port: int = 0,
        family: int = PR_AF_INET,
    ) -> None:
        """
        Create a network address.

        Args:
            addr: IP address. May be an integer wildcard sentinel
                such as ``PR_IpAddrAny`` / ``PR_IpAddrLoopback``, an
                IP address string, or a ``(host, port)`` tuple.
            port: TCP/UDP port number.
            family: Address family (``PR_AF_INET`` or
                ``PR_AF_INET6``).
        """
        ...

    @property
    def family(self) -> int:
        """Get the address family."""
        ...

    @property
    def port(self) -> int:
        """Get the port number."""
        ...

    @port.setter
    def port(self, value: int) -> None:
        """Set the port number."""
        ...

    @property
    def address(self) -> str:
        """Get the IP address as a string."""
        ...

    def __str__(self) -> str:
        """String representation of the address."""
        ...

    def __repr__(self) -> str:
        """Detailed string representation."""
        ...

    def set_from_string(self, addr_str: str, family: int = PR_AF_INET) -> None:
        """
        Set address from string representation.

        Args:
            addr_str: Address string
            family: Address family
        """
        ...

class HostEntry:
    """Represents a host entry from name resolution."""

    @property
    def name(self) -> str:
        """Get the canonical hostname."""
        ...

    @property
    def aliases(self) -> list[str]:
        """Get list of hostname aliases."""
        ...

    @property
    def addresses(self) -> list[NetworkAddress]:
        """Get list of network addresses."""
        ...

    def get_network_addresses(self, family: int = PR_AF_INET) -> list[NetworkAddress]:
        """Get network addresses filtered by family."""
        ...

    def get_network_address(self, family: int = PR_AF_INET) -> NetworkAddress:
        """Get first network address matching family."""
        ...

class AddrInfo:
    """Address information for host name resolution."""

    def __init__(self, hostname: str, family: int = PR_AF_INET, flags: int = 0) -> None:
        """
        Resolve hostname to network addresses.

        Args:
            hostname: Hostname to resolve
            family: Address family filter
            flags: Resolution flags
        """
        ...

    def __iter__(self) -> AddrInfo:
        """Iterate over resolved addresses."""
        ...

    def __next__(self) -> NetworkAddress:
        """Get next resolved address."""
        ...

    @property
    def hostname(self) -> str:
        """Get the hostname."""
        ...

    @property
    def canonical_name(self) -> str:
        """Get the canonical hostname."""
        ...

# Host resolution
def get_host_by_name(hostname: str) -> HostEntry:
    """
    Resolve hostname to host entry.

    Args:
        hostname: Hostname to resolve

    Returns:
        HostEntry with resolved information
    """
    ...

def get_host_by_addr(addr: str) -> HostEntry:
    """
    Reverse resolve IP address to hostname.

    Args:
        addr: IP address string

    Returns:
        HostEntry with resolved information
    """
    ...

class Socket:
    """NSPR socket (non-SSL).

    The C extension exposes additional methods on the socket object
    that are not enumerated in this stub (e.g. SSL-layer callbacks
    such as ``set_handshake_callback`` are reachable on plain
    ``Socket`` instances once the socket has been imported into the
    SSL layer). A permissive ``__getattr__`` is provided to keep
    static type checkers from flagging those access patterns.
    """

    def __init__(self, family: int = PR_AF_INET) -> None:
        """
        Create a new NSPR socket.

        Args:
            family: Address family (PR_AF_INET or PR_AF_INET6)
        """
        ...

    def set_handshake_callback(self, callback: Any) -> None:
        """Set the SSL handshake-completion callback.

        Although logically an SSL-layer concern, the C extension
        exposes this method on the plain socket type as well, so it
        is declared here to keep callers using the base ``Socket``
        type passing static type checks.
        """
        ...

    def __getattr__(self, name: str) -> Any: ...
    def connect(self, addr: NetworkAddress, timeout: int | None = None) -> None:
        """
        Connect to remote address.

        Args:
            addr: Network address to connect to
            timeout: Connection timeout in NSPR intervals
        """
        ...

    def bind(self, addr: NetworkAddress) -> None:
        """
        Bind socket to local address.

        Args:
            addr: Local address to bind to
        """
        ...

    def listen(self, backlog: int = 5) -> None:
        """
        Listen for incoming connections.

        Args:
            backlog: Maximum length of pending connection queue
        """
        ...

    def accept(self, timeout: int | None = None) -> tuple[Socket, NetworkAddress]:
        """
        Accept an incoming connection.

        Args:
            timeout: Accept timeout in NSPR intervals

        Returns:
            Tuple of (connected_socket, peer_address)
        """
        ...

    def send(self, data: bytes, flags: int = 0, timeout: int | None = None) -> int:
        """
        Send data over the socket.

        Args:
            data: Data to send
            flags: Send flags
            timeout: Send timeout in NSPR intervals

        Returns:
            Number of bytes sent
        """
        ...

    def recv(self, bufsize: int, flags: int = 0, timeout: int | None = None) -> bytes:
        """
        Receive data from socket.

        Args:
            bufsize: Maximum number of bytes to receive
            flags: Receive flags
            timeout: Receive timeout in NSPR intervals

        Returns:
            Received data
        """
        ...

    def sendto(
        self, data: bytes, flags: int, addr: NetworkAddress, timeout: int | None = None
    ) -> int:
        """Send data to specific address (UDP)."""
        ...

    def recvfrom(
        self, bufsize: int, flags: int = 0, timeout: int | None = None
    ) -> tuple[bytes, NetworkAddress]:
        """
        Receive data and sender address (UDP).

        Returns:
            Tuple of (data, sender_address)
        """
        ...

    def close(self) -> None:
        """Close the socket."""
        ...

    def shutdown(self, how: int = PR_SHUTDOWN_BOTH) -> None:
        """
        Shutdown socket connection.

        Args:
            how: Shutdown mode (PR_SHUTDOWN_RCV, SEND, or BOTH)
        """
        ...

    def set_socket_option(self, option: int, value: Any) -> None:
        """
        Set a socket option.

        Args:
            option: Socket option constant
            value: Option value
        """
        ...

    def get_socket_option(self, option: int) -> Any:
        """
        Get a socket option value.

        Args:
            option: Socket option constant

        Returns:
            Current option value
        """
        ...

    def get_peer_name(self) -> NetworkAddress:
        """Get the peer's network address."""
        ...

    def get_sock_name(self) -> NetworkAddress:
        """Get the local socket address."""
        ...

    def fileno(self) -> int:
        """Get the file descriptor number."""
        ...

    def read(self, size: int = -1, timeout: int | None = None) -> bytes:
        """Read data from socket."""
        ...

    def readline(self, size: int = -1, timeout: int | None = None) -> bytes:
        """Read a line from socket."""
        ...

    def readlines(self, sizehint: int = -1, timeout: int | None = None) -> list[bytes]:
        """Read lines from socket."""
        ...

    def sendall(self, data: bytes, flags: int = 0, timeout: int | None = None) -> None:
        """Send all data over socket."""
        ...

    def accept_read(
        self, buf_size: int = 4096, timeout: int | None = None
    ) -> tuple[Socket, NetworkAddress, bytes]:
        """Accept connection and read data in one operation."""
        ...

    def makefile(self, mode: str = "r", buffering: int = -1) -> Any:
        """Create file-like object from socket."""
        ...

    @staticmethod
    def new_tcp_pair() -> tuple[Socket, Socket]:
        """Create a pair of connected TCP sockets."""
        ...

    @staticmethod
    def poll(
        poll_desc_list: list[tuple[Socket, int, int]], timeout: int | None = None
    ) -> list[tuple[Socket, int, int]]:
        """Poll multiple sockets for I/O events."""
        ...

    @staticmethod
    def import_tcp_socket(sock: socket.socket) -> Socket:
        """Import a Python TCP socket as an NSPR socket."""
        ...

# File I/O operations
class FileDesc:
    """NSPR file descriptor."""

    def read(self, size: int = -1) -> bytes:
        """Read data from file descriptor."""
        ...

    def write(self, data: bytes) -> int:
        """Write data to file descriptor."""
        ...

    def close(self) -> None:
        """Close the file descriptor."""
        ...

    def fileno(self) -> int:
        """Get the file descriptor number."""
        ...

# Error handling
class NSPRError(Exception):
    """NSPR error exception."""

    def __init__(self, errno: int = 0, strerror: str = "") -> None:
        """
        Create NSPR error.

        Args:
            errno: Error number
            strerror: Error string description
        """
        ...

    @property
    def errno(self) -> int:
        """Get the error number."""
        ...

    @property
    def strerror(self) -> str:
        """Get the error description."""
        ...

def set_error(errno: int) -> None:
    """Set the NSPR error code."""
    ...

def get_error() -> int:
    """Get the current NSPR error code."""
    ...

def get_error_text(errno: int | None = None) -> str:
    """
    Get error text description.

    Args:
        errno: Error number (uses current error if None)

    Returns:
        Error description string
    """
    ...

# ---------------------------------------------------------------------------
# Dynamic module attributes
# ---------------------------------------------------------------------------
#
# The C extension registers many integer constants at module init
# time -- address-family flags (``PR_AF_INET``, ``PR_AF_UNSPEC``,
# ...), wildcard address sentinels (``PR_IpAddrAny``, ``PR_IpAddrLoopback``,
# ...), shutdown modes, socket-option identifiers, and assorted error
# codes. Enumerating every one of them here would be both tedious
# and brittle, so a module-level ``__getattr__`` returning ``Any``
# is provided to satisfy static type checkers for any such attribute
# access. Symbols that are explicitly typed above retain their
# precise types; this fallback only kicks in for names not already
# declared.
def __getattr__(name: str) -> Any: ...
