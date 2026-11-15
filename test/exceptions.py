# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: Copyright (c) 2010-2025 python-nss-ng contributors

"""Common exceptions for python-nss-ng test utilities."""

from collections.abc import Sequence


class PythonNSSError(Exception):
    """Base exception for python-nss-ng related errors."""

    pass


class CommandExecutionError(PythonNSSError):
    """Exception raised when an external command fails during certificate or database operations."""

    def __init__(
        self,
        cmd_args: Sequence[str],
        returncode: int,
        message: str | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
    ):
        """Initialize CommandExecutionError.

        Args:
            cmd_args: The command and arguments that were executed
            returncode: The return code from the command
            message: Optional custom error message
            stdout: Optional stdout output from the command
            stderr: Optional stderr output from the command
        """
        self.cmd_args = cmd_args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

        if message is None:
            self.message = f"Command failed with error code {returncode}"
            if stderr:
                self.message += f": {stderr.strip()}"
            self.message += f"\nCommand: {' '.join(str(arg) for arg in cmd_args)}"
        else:
            self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class CertificateError(PythonNSSError):
    """Exception raised for certificate-related errors."""

    pass


class DatabaseError(PythonNSSError):
    """Exception raised for NSS database-related errors."""

    pass


class ConfigurationError(PythonNSSError):
    """Exception raised for configuration-related errors."""

    pass


# For backward compatibility, alias CmdError to CommandExecutionError
CmdError = CommandExecutionError
