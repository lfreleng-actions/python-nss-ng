# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""
Type stubs for nss.error module.

This file provides type hints for the C extension module nss.error.

The module exposes:

- ``NSPRError`` -- base exception class raised for NSPR / NSS errors.
- ``CertVerifyError`` -- subclass raised for certificate verification
  failures, carrying additional usage and log information.
- A large set of integer constants whose names match the C-level NSPR
  / NSS error codes (e.g. ``PR_END_OF_FILE_ERROR``, ``SEC_ERROR_*``,
  ``SSL_ERROR_*``, ...). These are dynamically registered by the C
  extension via ``PyModule_AddIntConstant`` from the ``nspr_errors``
  table. Rather than enumerate every one of the hundreds of error
  constants here, a module-level ``__getattr__`` returning ``int``
  is provided so static type checkers accept any such attribute
  access.
"""

from typing import Any, List, Tuple

# ---------------------------------------------------------------------------
# Exception classes
# ---------------------------------------------------------------------------

class NSPRError(Exception):
    """Base exception for NSPR / NSS errors.

    Instances carry both the numeric NSPR error code and the
    associated symbolic name and human-readable message.
    """

    #: The numeric NSPR error code (e.g. ``PR_END_OF_FILE_ERROR``).
    errno: int

    #: The symbolic name corresponding to ``errno``
    #: (e.g. ``"PR_END_OF_FILE_ERROR"``).
    error_desc: str

    #: The human-readable error message.
    error_message: str

    def __init__(self, *args: Any) -> None: ...
    def __str__(self) -> str: ...

class CertVerifyError(NSPRError):
    """Exception raised when certificate verification fails.

    In addition to the base ``NSPRError`` attributes, this exception
    carries information about which certificate usages were being
    checked and a structured log of the verification failures.
    """

    #: Bitmask of ``certificateUsage*`` flags that were being checked.
    usages: int

    #: A list of ``(depth, cert, error)`` style tuples describing the
    #: per-certificate verification failures recorded by NSS.
    log: List[Tuple[Any, ...]]

    def __init__(self, *args: Any) -> None: ...

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def nspr_error_name(errno: int) -> str:
    """Return the symbolic name (e.g. ``"PR_END_OF_FILE_ERROR"``)
    associated with ``errno``, or a generic placeholder if the code
    is not recognised by NSPR / NSS."""
    ...

def nspr_error_string(errno: int) -> str:
    """Return the human-readable description string associated with
    ``errno``, or a generic placeholder if the code is not recognised
    by NSPR / NSS."""
    ...

def lookup_nspr_error(errno: int) -> Tuple[int, str, str] | None:
    """Look up an NSPR / NSS error code.

    Returns a ``(errno, name, string)`` tuple if the code is known,
    otherwise ``None``.
    """
    ...

# ---------------------------------------------------------------------------
# Dynamic constants
# ---------------------------------------------------------------------------
#
# The C extension registers hundreds of integer constants for the
# NSPR / NSS error codes (``PR_*_ERROR``, ``SEC_ERROR_*``,
# ``SSL_ERROR_*``, etc.) at module init time. Enumerating every one
# of them here would be both tedious and brittle, so we expose a
# module-level ``__getattr__`` that satisfies static type checkers
# for any such attribute access.
def __getattr__(name: str) -> int: ...
