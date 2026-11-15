# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Deprecation registry and utilities for python-nss-ng.

This module provides a centralized registry of deprecated functionality
and utilities for emitting deprecation warnings.
"""

import warnings

# Central registry of deprecated functionality
# Key: deprecated symbol name
# Value: replacement/migration guidance
DEPRECATED_REGISTRY: dict[str, str] = {
    "io.NetworkAddress()": (
        "NetworkAddress initialization from a string parameter only works for IPv4. "
        "Use io.AddrInfo instead for proper IPv4/IPv6 support."
    ),
    "io.NetworkAddress.set_from_string()": (
        "NetworkAddress.set_from_string() only works for IPv4. "
        "Use io.AddrInfo instead for proper IPv4/IPv6 support."
    ),
    "io.NetworkAddress.hostentry": (
        "HostEntry objects only support IPv4. This property will be removed. "
        "Use io.AddrInfo instead for proper IPv4/IPv6 support."
    ),
    "io.HostEntry.get_network_addresses()": (
        "Use iteration instead (e.g., 'for net_addr in hostentry'). "
        "The port parameter is not respected; port will be the value when "
        "HostEntry object was created."
    ),
    "io.HostEntry.get_network_address()": (
        "Use indexing instead (e.g., 'hostentry[i]'). "
        "The port parameter is not respected; port will be the value when "
        "HostEntry object was created."
    ),
    "io.Socket() without family": (
        "Socket initialization without explicit family parameter is deprecated. "
        "The default family parameter of PR_AF_INET is deprecated because when "
        "iterating through NetworkAddress objects returned by AddrInfo, some "
        "addresses may be IPv6. Use the family property of the NetworkAddress "
        "object associated with the socket, e.g., Socket(net_addr.family)."
    ),
    "ssl.SSLSocket() without family": (
        "SSLSocket initialization without explicit family parameter is deprecated. "
        "The default family parameter of PR_AF_INET is deprecated because when "
        "iterating through NetworkAddress objects returned by AddrInfo, some "
        "addresses may be IPv6. Use the family property of the NetworkAddress "
        "object associated with the socket, e.g., SSLSocket(net_addr.family)."
    ),
}


def warn_deprecated(symbol_name: str, alternative: str | None = None, stacklevel: int = 2) -> None:
    """
    Emit a deprecation warning for a deprecated symbol.

    Args:
        symbol_name: The name of the deprecated symbol (should be in DEPRECATED_REGISTRY)
        alternative: Optional alternative guidance (overrides registry if provided)
        stacklevel: Stack level for the warning (default: 2, caller of this function)
    """
    if alternative is None:
        alternative = DEPRECATED_REGISTRY.get(symbol_name, "This functionality is deprecated.")

    message = f"{symbol_name} is deprecated. {alternative}"

    warnings.warn(message, category=DeprecationWarning, stacklevel=stacklevel)


def is_deprecated(symbol_name: str) -> bool:
    """
    Check if a symbol is in the deprecation registry.

    Args:
        symbol_name: The name of the symbol to check

    Returns:
        True if the symbol is deprecated, False otherwise
    """
    return symbol_name in DEPRECATED_REGISTRY


def get_deprecation_message(symbol_name: str) -> str | None:
    """
    Get the deprecation message for a symbol.

    Args:
        symbol_name: The name of the deprecated symbol

    Returns:
        The deprecation message, or None if the symbol is not deprecated
    """
    return DEPRECATED_REGISTRY.get(symbol_name)


def list_deprecated() -> dict[str, str]:
    """
    Get a copy of the entire deprecation registry.

    Returns:
        Dictionary mapping deprecated symbols to their deprecation messages
    """
    return DEPRECATED_REGISTRY.copy()
