# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Type stubs for nss.nss module.

This file provides type hints for the C extension module nss.nss.
"""

from typing import Any, Callable, List, Tuple, Union

# Version information
def nss_get_version() -> str:
    """Get the NSS library version string."""
    ...

def nss_version_check(version: str) -> bool:
    """Check if NSS version meets minimum requirement."""
    ...

# NSS initialization and shutdown
def nss_init(cert_dir: str) -> None:
    """Initialize NSS with a certificate database directory."""
    ...

def nss_init_nodb() -> None:
    """Initialize NSS without a certificate database."""
    ...

def nss_init_read_write(cert_dir: str) -> None:
    """Initialize NSS with read-write access to certificate database."""
    ...

def nss_shutdown() -> None:
    """Shutdown NSS and free resources."""
    ...

def nss_is_initialized() -> bool:
    """Check if NSS has been initialized."""
    ...

def set_shutdown_callback(callback: Callable[..., bool] | None, *args: Any) -> None:
    """Set a callback function to be called when NSS shuts down."""
    ...

# Password callback
def set_password_callback(callback: Callable[..., str] | None) -> None:
    """Set a callback function for password requests."""
    ...

# Certificate database
def get_default_certdb() -> Any:
    """Get the default certificate database."""
    ...

# Certificate lookup
def find_cert_from_nickname(nickname: str, *pin_args: Any) -> Certificate:
    """Find a certificate by its nickname."""
    ...

def find_certs_from_nickname(nickname: str, *pin_args: Any) -> List[Certificate]:
    """Find all certificates with the given nickname."""
    ...

def find_certs_from_email_addr(email: str, *pin_args: Any) -> List[Certificate]:
    """Find certificates associated with an email address."""
    ...

def find_key_by_any_cert(cert: Certificate, *pin_args: Any) -> Any:
    """Find the private key associated with a certificate."""
    ...

def get_cert_nicknames(certdb: Any, what: int, *user_data: Any) -> List[str]:
    """Get certificate nicknames from the database.

    Args:
        certdb: Certificate database object
        what: SEC_CERT_NICKNAMES_ALL, SEC_CERT_NICKNAMES_USER, or SEC_CERT_NICKNAMES_SERVER
        *user_data: Optional callback parameters

    Returns:
        List of certificate nicknames
    """
    ...

def generate_random(num_bytes: int) -> bytes:
    """Generate random bytes using NSS PRNG."""
    ...

def get_fips_mode() -> bool:
    """Check if FIPS mode is enabled."""
    ...

# Digest/hash functions
def md5_digest(data: bytes) -> bytes:
    """Compute MD5 digest of data."""
    ...

def sha1_digest(data: bytes) -> bytes:
    """Compute SHA-1 digest of data."""
    ...

def sha256_digest(data: bytes) -> bytes:
    """Compute SHA-256 digest of data."""
    ...

def sha512_digest(data: bytes) -> bytes:
    """Compute SHA-512 digest of data."""
    ...

def hash_buf(algorithm: int, data: bytes) -> bytes:
    """Compute hash of data using specified algorithm."""
    ...

# Utility functions
def read_hex(hex_string: str, separator: str | None = None) -> bytes:
    """Convert hex string to bytes."""
    ...

def oid_str(oid: Union[int, str, SecItem]) -> str:
    """Get the string representation of an OID.

    ``oid`` may be an integer tag, a string (tag name, AVA
    short-name, or dotted-decimal form), or a ``SecItem`` holding
    the encoded OID.
    """
    ...

# OCSP and validation settings
def get_use_pkix_for_validation() -> bool:
    """Get whether PKIX validation is enabled."""
    ...

def set_use_pkix_for_validation(enable: Any) -> bool:
    """Enable or disable PKIX validation.

    The C extension performs its own runtime coercion of the
    ``enable`` argument (accepting bools, ints, and even strings in
    some legacy code paths), so the signature is intentionally
    permissive here to match observed behaviour.

    Returns the previous value of the PKIX-validation flag (the
    underlying C function is documented as
    ``set_use_pkix_for_validation(flag) -> prev_flag``).
    """
    ...

def enable_ocsp_checking(certdb: Any | None = None) -> None:
    """Enable OCSP checking."""
    ...

def disable_ocsp_checking(certdb: Any | None = None) -> None:
    """Disable OCSP checking."""
    ...

def set_ocsp_cache_settings(
    max_cache_entries: int,
    minimum_seconds_to_next_fetch: int,
    maximum_seconds_before_cached_response_reused: int,
) -> None:
    """Set OCSP cache parameters."""
    ...

def set_ocsp_failure_mode(mode: int) -> None:
    """Set the OCSP failure mode."""
    ...

def set_ocsp_timeout(seconds: Any) -> None:
    """Set the OCSP timeout in seconds.

    Accepts any value the C extension can coerce to an integer
    timeout. Tests intentionally pass non-integer values to exercise
    the runtime type-checking paths, so the static type is left as
    ``Any``.
    """
    ...

def clear_ocsp_cache() -> None:
    """Remove all items currently stored in the OCSP cache."""
    ...

def set_ocsp_default_responder(
    certdb: Any,
    url: str,
    nickname: str,
) -> None:
    """Set the default OCSP responder for ``certdb``.

    ``url`` is the responder location (e.g.
    ``"http://foo.com:80/ocsp"``) and ``nickname`` identifies the
    certificate that is trusted to sign OCSP responses.
    """
    ...

def enable_ocsp_default_responder(certdb: Any | None = None) -> None:
    """Enable the default OCSP responder."""
    ...

def disable_ocsp_default_responder(certdb: Any | None = None) -> None:
    """Disable the default OCSP responder."""
    ...

# Digest and cryptographic operations
def create_digest_context(algorithm: int) -> Any:
    """Create a digest context for the specified algorithm."""
    ...

def create_context_by_sym_key(
    mechanism: int, operation: int, key: Any, params: Any | None = None
) -> Any:
    """Create a cryptographic context using a symmetric key."""
    ...

def create_pbev2_algorithm_id(
    pbe_alg: int,
    cipher_alg: int,
    prf_alg: int,
    key_length: int,
    iterations: int,
    salt: bytes | None = None,
) -> AlgorithmID:
    """Create a PBKDF2 algorithm ID."""
    ...

# Algorithm constants for digest
SEC_OID_MD5: int
SEC_OID_SHA1: int
SEC_OID_SHA256: int
SEC_OID_SHA384: int
SEC_OID_SHA512: int

# RepresentationKind constants
#
# These integer constants are exported by the C extension (see
# AddIntConstant calls in src/py_nss.c) and are used as the
# ``repr_kind=`` keyword argument on many functions/methods that can
# return a value in multiple representations (an enumerated integer,
# the symbolic name of that enumerator, a human-readable description,
# a SecItem object, etc.).
AsObject: int
AsString: int
AsTypeString: int
AsTypeEnum: int
AsLabeledString: int
AsEnum: int
AsEnumName: int
AsEnumDescription: int
AsIndex: int
AsDottedDecimal: int

# PK11 slot and token operations
def get_best_slot(mechanism: int) -> PK11Slot:
    """Get the best slot for a given mechanism."""
    ...

def get_internal_slot() -> PK11Slot:
    """Get the internal cryptographic slot."""
    ...

def get_internal_key_slot() -> PK11Slot:
    """Get the internal key slot."""
    ...

def get_all_tokens(
    mechanism: int = 0, need_rw: bool = False, load_certs: bool = False, *pin_args: Any
) -> List[PK11Slot]:
    """Get all available tokens."""
    ...

def find_slot_by_name(name: str) -> PK11Slot:
    """Find a slot by its name."""
    ...

def pk11_logout_all() -> None:
    """Log out from all slots."""
    ...

def need_pw_init() -> bool:
    """Check if password initialization is needed."""
    ...

def token_exists(mechanism: int) -> bool:
    """Check if a token exists for the given mechanism."""
    ...

def is_fips() -> bool:
    """Check if FIPS mode is enabled."""
    ...

# Key and parameter operations
def import_sym_key(
    slot: PK11Slot, mechanism: int, origin: int, operation: int, key_data: Union[bytes, SecItem]
) -> Any:
    """Import a symmetric key.

    ``key_data`` accepts either raw ``bytes`` or a ``SecItem``
    wrapping the key material.
    """
    ...

def pub_wrap_sym_key(mechanism: int, pub_key: Any, sym_key: Any) -> bytes:
    """Wrap a symmetric key with a public key."""
    ...

def param_from_iv(
    mechanism: int,
    iv: Union[bytes, SecItem, None] = None,
) -> SecItem:
    """Create parameters from an initialization vector.

    ``iv`` may be ``None``, raw ``bytes``, or a ``SecItem`` wrapping
    the IV bytes.
    """
    ...

def param_from_algid(alg_id: AlgorithmID) -> SecItem:
    """Create parameters from an algorithm ID."""
    ...

def generate_new_param(mechanism: int, sym_key: Any | None = None) -> SecItem:
    """Generate new parameters for a mechanism."""
    ...

def algtag_to_mechanism(algtag: int) -> int:
    """Convert an algorithm tag to a mechanism."""
    ...

def mechanism_to_algtag(mechanism: int) -> int:
    """Convert a mechanism to an algorithm tag."""
    ...

def get_iv_length(mechanism: int) -> int:
    """Get the IV length for a mechanism."""
    ...

def get_block_size(mechanism: int, params: SecItem | None = None) -> int:
    """Get the block size for a mechanism."""
    ...

def get_pad_mechanism(mechanism: int) -> int:
    """Get the padding mechanism for a given mechanism."""
    ...

# Data conversion utilities
def data_to_hex(
    data: bytes,
    octets_per_line: int = 16,
    separator: Union[str, None] = ":",
) -> str:
    """Convert binary data to hexadecimal string.

    ``separator`` controls the inter-octet delimiter (default ``":"``).
    Passing ``None`` disables the separator and produces an
    unbroken hex string.
    """
    ...

def make_line_fmt_tuples(
    level: int,
    *lines: Union[str, List[str], Tuple[str, ...]],
) -> List[Tuple[int, str]]:
    """Create formatted line tuples for indented output.

    Each positional ``lines`` argument may be a single string or a
    sequence (list/tuple) of strings; in the latter case each element
    becomes its own line at the given indent ``level``.
    """
    ...

def indented_format(tuples: List[Tuple[int, str]]) -> str:
    """Format indented text from line tuples."""
    ...

def read_der_from_file(filepath: str, ascii: bool = False) -> bytes:
    """Read DER-encoded data from a file."""
    ...

def base64_to_binary(data: str) -> bytes:
    """Convert base64 string to binary data."""
    ...

def fingerprint_format_lines(fingerprint: bytes, level: int = 0) -> List[Tuple[int, str]]:
    """Format fingerprint as indented lines."""
    ...

# Name and type conversion functions
def key_mechanism_type_name(mechanism: int) -> str:
    """Get the name of a key mechanism type."""
    ...

def key_mechanism_type_from_name(name: str) -> int:
    """Get the mechanism type from its name."""
    ...

def pk11_attribute_type_name(attr_type: int) -> str:
    """Get the name of a PK11 attribute type."""
    ...

def pk11_attribute_type_from_name(name: str) -> int:
    """Get the PK11 attribute type from its name."""
    ...

def pk11_disabled_reason_str(reason: int) -> str:
    """Get the string description of a disabled reason."""
    ...

def pk11_disabled_reason_name(reason: int) -> str:
    """Get the name of a disabled reason."""
    ...

def oid_tag_name(tag: Union[int, str, SecItem]) -> str:
    """Get the name of an OID tag.

    ``tag`` may be an integer tag value, a string (tag name, AVA
    short-name, or dotted-decimal form), or a ``SecItem`` holding
    the encoded OID.
    """
    ...

def oid_tag(oid: Union[str, SecItem]) -> int:
    """Get the tag for an OID."""
    ...

def oid_dotted_decimal(oid: Union[int, str, SecItem]) -> str:
    """Get the dotted decimal representation of an OID.

    ``oid`` may be an integer tag, a string (a tag name like
    ``"SEC_OID_AVA_COMMON_NAME"``, an AVA short-name like ``"cn"``,
    or a dotted-decimal string like ``"2.5.4.3"``), or a ``SecItem``
    holding the encoded OID.
    """
    ...

def list_certs(certdb: Any, *user_data: Any) -> List[Certificate]:
    """List all certificates in the database."""
    ...

def cert_crl_reason_name(reason: int) -> str:
    """Get the name of a CRL reason code."""
    ...

def cert_crl_reason_from_name(name: str) -> int:
    """Get the CRL reason code from its name."""
    ...

def cert_general_name_type_name(name_type: int) -> str:
    """Get the name of a general name type."""
    ...

def cert_general_name_type_from_name(name: str) -> int:
    """Get the general name type from its name."""
    ...

# Certificate and key usage flags
def cert_usage_flags(usage: int) -> List[str]:
    """Get list of certificate usage flag names."""
    ...

def key_usage_flags(usage: int) -> List[str]:
    """Get list of key usage flag names."""
    ...

def cert_type_flags(cert_type: int) -> List[str]:
    """Get list of certificate type flag names."""
    ...

def nss_init_flags(flags: int) -> List[str]:
    """Get list of NSS init flag names."""
    ...

def x509_key_usage(flags: int, repr_kind: int = 0) -> Union[str, List[str]]:
    """Get X.509 key usage representation."""
    ...

def x509_cert_type(flags: int, repr_kind: int = 0) -> Union[str, List[str]]:
    """Get X.509 certificate type representation."""
    ...

def x509_ext_key_usage(oid_seq: SecItem, repr_kind: int = 0) -> Union[str, List[str]]:
    """Get X.509 extended key usage representation."""
    ...

def x509_alt_name(gen_names: Any, repr_kind: int = 0) -> Union[str, List[str]]:
    """Get X.509 alternative name representation."""
    ...

# CRL operations
def import_crl(certdb: Any, der_crl: bytes, url: str | None = None, crl_type: int = 0) -> Any:
    """Import a CRL into the certificate database."""
    ...

def decode_der_crl(der_crl: bytes, crl_type: int = 0) -> Any:
    """Decode a DER-encoded CRL."""
    ...

# PKCS#12 operations
def pkcs12_enable_cipher(cipher: int, enable: bool) -> None:
    """Enable or disable a PKCS#12 cipher."""
    ...

def pkcs12_enable_all_ciphers() -> None:
    """Enable all PKCS#12 ciphers."""
    ...

def pkcs12_set_preferred_cipher(cipher: int, enable: bool) -> None:
    """Set the preferred PKCS#12 cipher."""
    ...

def pkcs12_cipher_name(cipher: int) -> str:
    """Get the name of a PKCS#12 cipher."""
    ...

def pkcs12_cipher_from_name(name: str) -> int:
    """Get the PKCS#12 cipher from its name."""
    ...

def pkcs12_map_cipher(old_cipher: int, prefer_des: bool = False) -> int:
    """Map a PKCS#12 cipher to a new cipher."""
    ...

def pkcs12_set_nickname_collision_callback(callback: Callable[..., Any]) -> None:
    """Set a callback for handling nickname collisions during PKCS#12 import.

    The callback's return value is interpreted by the C extension and
    may be either a replacement nickname (``str``) or a tuple of
    ``(nickname, cancel)`` where ``cancel`` is a truthy/falsey value;
    the static type is therefore left as ``Any``.
    """
    ...

def pkcs12_export(
    nickname: str,
    output_file: Union[str, None] = None,
    pk12_passwd: Union[str, None] = None,
    cert_db_passwd: Union[str, None] = None,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Export a certificate and its private key to a PKCS#12 file.

    The C extension supports several overloaded calling conventions
    for this function (returning either ``None`` or a ``bytes``
    blob, depending on whether ``output_file`` is supplied), so the
    signature is intentionally permissive.
    """
    ...

# Constants
CKA_ENCRYPT: int
CKA_DECRYPT: int
CKA_SIGN: int
CKA_VERIFY: int

# Certificate usage constants
certificateUsageSSLClient: int
certificateUsageSSLServer: int
certificateUsageSSLServerWithStepUp: int
certificateUsageSSLCA: int
certificateUsageEmailSigner: int
certificateUsageEmailRecipient: int
certificateUsageObjectSigner: int
certificateUsageUserCertImport: int
certificateUsageVerifyCA: int
certificateUsageProtectedObjectSigner: int
certificateUsageStatusResponder: int
certificateUsageAnyCA: int

# Certificate nickname types
SEC_CERT_NICKNAMES_ALL: int
SEC_CERT_NICKNAMES_USER: int
SEC_CERT_NICKNAMES_SERVER: int

# OCSP mode constants
ocspMode_FailureIsVerificationFailure: int
ocspMode_FailureIsNotAVerificationFailure: int

# Algorithm OIDs (examples - add more as needed)
SEC_OID_PKCS5_PBKDF2: int
SEC_OID_AES_256_CBC: int
SEC_OID_HMAC_SHA1: int

class SecItem:
    """Represents a security item (binary data)."""

    def __init__(self, data: Union[bytes, str] | None = None, ascii: bool = False) -> None:
        """
        Create a SecItem.

        Args:
            data: Binary data or base64 string
            ascii: If True, data is treated as base64
        """
        ...

    def to_base64(self, chars_per_line: int = 64) -> str:
        """Convert to base64 string."""
        ...

    @property
    def data(self) -> bytes:
        """Get the raw binary data."""
        ...

class Certificate:
    """Represents an X.509 certificate.

    Certificates expose a large number of attributes and helper
    methods that are populated dynamically by the C extension. The
    most commonly used ones are typed below; less common attributes
    are accepted via ``__getattr__`` to keep the stub permissive.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def new_from_der(cls, der: bytes) -> Certificate:
        """Create a Certificate from DER-encoded data."""
        ...

    @classmethod
    def trust_flags(
        cls,
        flags: int,
        repr_kind: int = ...,
    ) -> Union[str, List[str], List[int]]:
        """Decode an integer trust-flag bitmask into a list of
        flag names / enums / descriptions.

        ``repr_kind`` selects the representation (one of the
        ``As*`` constants); defaults to ``AsEnumDescription``.
        """
        ...

    @property
    def subject(self) -> str:
        """Get the certificate subject."""
        ...

    @property
    def issuer(self) -> str:
        """Get the certificate issuer."""
        ...

    @property
    def serial_number(self) -> int:
        """Get the certificate serial number."""
        ...

    @property
    def version(self) -> int:
        """X.509 certificate version (typically 1, 2 or 3)."""
        ...

    @property
    def signature_algorithm(self) -> AlgorithmID:
        """Algorithm identifier for the certificate signature."""
        ...

    @property
    def valid_not_before(self) -> int:
        """Validity start time as a NSPR ``PRTime`` value."""
        ...

    @property
    def valid_not_after(self) -> int:
        """Validity end time as a NSPR ``PRTime`` value."""
        ...

    @property
    def valid_not_before_str(self) -> str:
        """Validity start time as a human-readable string."""
        ...

    @property
    def valid_not_after_str(self) -> str:
        """Validity end time as a human-readable string."""
        ...

    @property
    def subject_public_key_info(self) -> SubjectPublicKeyInfo:
        """The certificate's ``SubjectPublicKeyInfo`` structure."""
        ...

    @property
    def signed_data(self) -> SignedData:
        """The certificate's ``SignedData`` structure (TBS plus
        signature algorithm and signature value)."""
        ...

    @property
    def der_data(self) -> bytes:
        """Full DER encoding of the certificate."""
        ...

    @property
    def extensions(self) -> List[CertificateExtension]:
        """List of X.509 extensions on the certificate."""
        ...

    @property
    def cert_type(self) -> int:
        """Bitmask of ``NS_CERT_TYPE_*`` flags for the certificate."""
        ...

    def is_ca_cert(self, return_type: bool = False) -> Any:
        """Return whether the certificate is a CA certificate.

        When called with no arguments (or ``return_type=False``)
        returns a plain boolean. When called with ``return_type=True``
        the C extension instead returns a ``(is_ca, cert_type)``
        tuple where ``cert_type`` is the bitmask of
        ``NS_CERT_TYPE_*`` flags. The static type is therefore
        declared as ``Any`` to cover both forms.
        """
        ...

    def verify_now(
        self, certdb: Any, check_sig: bool = True, required_usages: int = 0, *pin_args: Any
    ) -> int:
        """Verify the certificate."""
        ...

    def verify(self, *args: Any, **kwargs: Any) -> int:
        """Verify the certificate (older convenience API)."""
        ...

    def verify_with_log(self, *args: Any, **kwargs: Any) -> Any:
        """Verify the certificate, returning a verification log."""
        ...

    def verify_hostname(self, hostname: str) -> bool:
        """Verify the certificate hostname."""
        ...

    def check_valid_times(self, time: Union[int, None] = None, allow_override: bool = False) -> int:
        """Check whether the certificate is currently within its
        validity period."""
        ...

    def has_signer_in_ca_names(self, ca_names: Any) -> bool:
        """Return ``True`` if the certificate's issuer appears in
        the supplied list of acceptable CA names."""
        ...

    def find_kea_type(self) -> int:
        """Return the key-exchange algorithm type for the
        certificate's public key."""
        ...

    def set_trust_attributes(
        self,
        trust: str,
        certdb: Any,
        slot: Any,
        *user_data: Any,
    ) -> None:
        """Set the certificate's trust attributes from a NSS-style
        trust string (e.g. ``"CT,C,C"``).

        The C-level signature is
        ``set_trust_attributes(trust, certdb, slot, [user_data1, ...])``;
        ``certdb`` and ``slot`` are required positional arguments
        and any further arguments are passed through to the
        password / pin callback as ``user_data`` items.
        """
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format certificate as indented lines."""
        ...

    # The C extension exposes additional attributes and methods that
    # are not enumerated above (e.g. fingerprint helpers, key-usage
    # bitstrings, extension-specific accessors). Allow them through.
    def __getattr__(self, name: str) -> Any: ...

class SymKey:
    """Represents a symmetric cryptographic key."""

    @property
    def key_type(self) -> int:
        """Get the key type."""
        ...

    @property
    def key_length(self) -> int:
        """Get the key length in bits."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format key information as indented lines."""
        ...

class AlgorithmID:
    """Represents a cryptographic algorithm identifier."""

    def get_pbe_crypto_mechanism(self, key: SymKey) -> Tuple[int, SecItem]:
        """Get the cryptographic mechanism and parameters."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format algorithm ID information as indented lines."""
        ...

class Context:
    """Represents a cryptographic context."""

    def cipher_op(self, data: bytes) -> bytes:
        """Perform a cipher operation on data."""
        ...

    def digest_final(self) -> bytes:
        """Finalize the digest and return remaining data."""
        ...

class PK11Slot:
    """Represents a PKCS#11 cryptographic slot."""

    @property
    def token_name(self) -> str:
        """Get the token name."""
        ...

    @property
    def slot_name(self) -> str:
        """Get the slot name."""
        ...

    def is_hw(self) -> bool:
        """Check if this is a hardware slot."""
        ...

    def is_present(self) -> bool:
        """Check if the token is present in the slot."""
        ...

    def is_read_only(self) -> bool:
        """Check if the slot is read-only."""
        ...

    def is_internal(self) -> bool:
        """Check if this is an internal slot."""
        ...

    def need_login(self) -> bool:
        """Check if login is needed."""
        ...

    def need_user_init(self) -> bool:
        """Check if user initialization is needed."""
        ...

    def is_friendly(self) -> bool:
        """Check if the slot is friendly."""
        ...

    def is_removable(self) -> bool:
        """Check if the token is removable."""
        ...

    def is_logged_in(self) -> bool:
        """Check if logged in to the slot."""
        ...

    def has_protected_authentication_path(self) -> bool:
        """Check if the slot has a protected authentication path."""
        ...

    def is_disabled(self) -> bool:
        """Check if the slot is disabled."""
        ...

    def has_root_certs(self) -> bool:
        """Check if the slot has root certificates."""
        ...

    def get_disabled_reason(self) -> int:
        """Get the reason why the slot is disabled."""
        ...

    def user_disable(self) -> None:
        """Disable the slot."""
        ...

    def user_enable(self) -> None:
        """Enable the slot."""
        ...

    def authenticate(self, force: bool = False, *pin_args: Any) -> None:
        """Authenticate to the slot."""
        ...

    def check_security_officer_passwd(self, password: str) -> None:
        """Check the security officer password."""
        ...

    def check_user_passwd(self, password: str) -> None:
        """Check the user password."""
        ...

    def change_passwd(self, old_passwd: str | None = None, new_passwd: str | None = None) -> None:
        """Change the slot password."""
        ...

    def init_pin(self, passwd: str | None = None) -> None:
        """Initialize the PIN."""
        ...

    def logout(self) -> None:
        """Log out from the slot."""
        ...

    def get_best_wrap_mechanism(self) -> int:
        """Get the best wrap mechanism for this slot."""
        ...

    def get_best_key_length(self, mechanism: int) -> int:
        """Get the best key length for a mechanism."""
        ...

    def key_gen(
        self, mechanism: int, params: SecItem | None = None, key_size: int = 0, *pin_args: Any
    ) -> Any:
        """Generate a key."""
        ...

    def generate_key_pair(
        self, mechanism: int, params: Any | None = None, *pin_args: Any
    ) -> Tuple[Any, Any]:
        """Generate a key pair."""
        ...

    def list_certs(self) -> List[Certificate]:
        """List all certificates in the slot."""
        ...

    def pbe_key_gen(self, alg_id: AlgorithmID, password: str) -> Any:
        """Generate a password-based encryption key."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format slot information as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format slot information as a string."""
        ...

class PK11SymKey:
    """Represents a PKCS#11 symmetric key."""

    @property
    def key_type(self) -> int:
        """Get the key type."""
        ...

    @property
    def key_length(self) -> int:
        """Get the key length in bits."""
        ...

    @property
    def slot(self) -> PK11Slot:
        """Get the slot containing this key."""
        ...

    def derive(
        self,
        mechanism: int,
        params: SecItem | None = None,
        target: int = 0,
        operation: int = 0,
        key_size: int = 0,
    ) -> PK11SymKey:
        """Derive a new key from this key."""
        ...

    def wrap_sym_key(
        self, mechanism: int, params: SecItem | None, wrapping_key: PK11SymKey
    ) -> bytes:
        """Wrap this symmetric key with another key."""
        ...

    def unwrap_sym_key(
        self,
        mechanism: int,
        params: SecItem | None,
        wrapped_key: bytes,
        target: int,
        operation: int,
        key_size: int,
    ) -> PK11SymKey:
        """Unwrap a symmetric key."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format key information as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format key information as a string."""
        ...

class PK11Context:
    """Represents a PKCS#11 cryptographic context."""

    def digest_key(self, key: PK11SymKey) -> None:
        """Digest a key."""
        ...

    def clone_context(self) -> PK11Context:
        """Clone this context."""
        ...

    def digest_begin(self) -> None:
        """Begin a digest operation."""
        ...

    def digest_op(self, data: bytes) -> None:
        """Update the digest with data."""
        ...

    def cipher_op(self, data: bytes) -> bytes:
        """Perform a cipher operation on data."""
        ...

    def finalize(self) -> bytes:
        """Finalize the operation and return remaining data."""
        ...

    def digest_final(self) -> bytes:
        """Finalize the digest and return the hash."""
        ...

class CertDB:
    """Represents a certificate database."""

    def find_crl_by_name(self, name: str, crl_type: int = 0) -> Any:
        """Find a CRL by name."""
        ...

    def find_crl_by_cert(self, cert: Certificate, crl_type: int = 0) -> Any:
        """Find a CRL by certificate."""
        ...

class DN:
    """Represents a Distinguished Name.

    A ``DN`` behaves both as a sequence of ``RDN`` objects and as a
    mapping keyed by attribute name (e.g. ``"cn"``, ``"ou"``) or
    OID. It supports ``len()``, iteration, indexed access, ``in``
    membership tests, and convenience attribute accessors for the
    common RDN types (``common_name``, ``email_address``, ...).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __str__(self) -> str:
        """Get string representation."""
        ...

    def __len__(self) -> int: ...
    def __iter__(self) -> Any: ...
    def __getitem__(self, key: Union[int, slice, str]) -> Any: ...
    def __contains__(self, key: object) -> bool: ...
    def has_key(self, key: Union[str, int, SecItem]) -> bool:
        """Check if the DN has a specific key."""
        ...

    def add_rdn(self, rdn: Any) -> None:
        """Add an RDN to the DN."""
        ...

    # Convenience attribute accessors for common RDN component types
    # exposed by the C extension. Not every DN will have every one
    # of these populated; access may raise or return an empty value.
    @property
    def common_name(self) -> Any: ...
    @property
    def email_address(self) -> Any: ...
    @property
    def country_name(self) -> Any: ...
    @property
    def locality_name(self) -> Any: ...
    @property
    def state_name(self) -> Any: ...
    @property
    def org_name(self) -> Any: ...
    @property
    def org_unit_name(self) -> Any: ...
    @property
    def dc_name(self) -> Any: ...
    @property
    def cert_uid(self) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...

class RDN:
    """Represents a Relative Distinguished Name.

    An ``RDN`` behaves as a sequence of ``AVA`` objects and supports
    ``len()``, iteration, indexed access, and ``in`` membership
    tests by attribute short-name or OID.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Any: ...
    def __getitem__(self, key: Union[int, slice, str]) -> Any: ...
    def __contains__(self, key: object) -> bool: ...
    def __lt__(self, other: RDN) -> bool: ...
    def __le__(self, other: RDN) -> bool: ...
    def __gt__(self, other: RDN) -> bool: ...
    def __ge__(self, other: RDN) -> bool: ...
    def has_key(self, key: Union[str, int, SecItem]) -> bool:
        """Check if the RDN has a specific key."""
        ...

    def __getattr__(self, name: str) -> Any: ...

class AVA:
    """An Attribute / Value Assertion within an :class:`RDN`.

    The C extension exposes ``AVA`` as a constructible class with
    several overloaded signatures (``AVA()``, ``AVA(oid)``,
    ``AVA(oid, value)``, etc.). Only the most permissive form is
    typed here.

    ``AVA`` instances are comparable (the C extension defines a
    rich-comparison slot that orders them by OID and value), so the
    standard ordering dunders are declared here to keep static type
    checkers happy when AVAs are sorted or compared directly.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def oid(self) -> Any: ...
    @property
    def oid_tag(self) -> int: ...
    @property
    def value(self) -> Any: ...
    @property
    def value_str(self) -> str: ...
    def __lt__(self, other: AVA) -> bool: ...
    def __le__(self, other: AVA) -> bool: ...
    def __gt__(self, other: AVA) -> bool: ...
    def __ge__(self, other: AVA) -> bool: ...
    def __getattr__(self, name: str) -> Any: ...

class GeneralName:
    """Represents a general name in a certificate."""

    def get_name(self, repr_kind: int = 0) -> Union[str, Tuple[int, str]]:
        """Get the name representation."""
        ...

class CRLDistributionPt:
    """Represents a CRL distribution point."""

    def get_general_names(self, repr_kind: int = 0) -> Any:
        """Get the general names."""
        ...

    def get_reasons(self, repr_kind: int = 0) -> Any:
        """Get the reasons."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class SignedCRL:
    """Represents a signed CRL."""

    def delete_permanently(self) -> None:
        """Delete this CRL permanently from the database."""
        ...

class CertificateExtension:
    """Represents a certificate extension."""

    @property
    def oid(self) -> int:
        """Get the extension OID."""
        ...

    @property
    def critical(self) -> bool:
        """Check if the extension is critical."""
        ...

    @property
    def value(self) -> SecItem:
        """Get the extension value."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class PrivateKey:
    """Represents a private key."""

    @property
    def key_type(self) -> int:
        """Get the key type."""
        ...

class PublicKey:
    """Represents a public key."""

    @property
    def key_type(self) -> int:
        """Get the key type."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class RSAPublicKey:
    """Represents an RSA public key."""

    @property
    def modulus(self) -> SecItem:
        """Get the modulus."""
        ...

    @property
    def exponent(self) -> SecItem:
        """Get the exponent."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class DSAPublicKey:
    """Represents a DSA public key."""

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class SignedData:
    """Represents signed data."""

    @property
    def data(self) -> SecItem:
        """Get the data."""
        ...

    @property
    def signature(self) -> SecItem:
        """Get the signature."""
        ...

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class SubjectPublicKeyInfo:
    """Represents subject public key info."""

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

class KEYPQGParams:
    """Represents PQG parameters for key generation."""

    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

# ---------------------------------------------------------------------------
# Additional C-extension classes
# ---------------------------------------------------------------------------
#
# The C extension exposes a number of further classes (X.509 extension
# wrappers, PKCS#12 helpers, certificate request types, ...). These
# are stubbed permissively so that examples and tests which reference
# them type-check cleanly. Each class accepts arbitrary constructor
# arguments and any attribute access via ``__getattr__``.

class AuthKeyID:
    """X.509 Authority Key Identifier extension wrapper."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

    def __getattr__(self, name: str) -> Any: ...

class BasicConstraints:
    """X.509 Basic Constraints extension wrapper."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

    def __getattr__(self, name: str) -> Any: ...

class CRLDistributionPts:
    """Container for X.509 CRL Distribution Points."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Any: ...
    def __getitem__(self, key: Union[int, slice]) -> Any: ...
    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

    def __getattr__(self, name: str) -> Any: ...

class AuthorityInfoAccesses:
    """Container for X.509 Authority Information Access entries."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Any: ...
    def __getitem__(self, key: Union[int, slice]) -> Any: ...
    def format_lines(self, level: int = 0) -> List[Tuple[int, str]]:
        """Format as indented lines."""
        ...

    def format(self, level: int = 0, indent: str = "    ") -> str:
        """Format as a string."""
        ...

    def __getattr__(self, name: str) -> Any: ...

class CertificateRequest:
    """PKCS#10 certificate request wrapper."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

class CertAttribute:
    """A PKCS#10 certificate request attribute."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

class PKCS12Decoder:
    """PKCS#12 decoder for importing key/certificate bundles."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: Union[int, slice]) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...

# ---------------------------------------------------------------------------
# Default octets-per-line for hex-dump style helpers
# ---------------------------------------------------------------------------

#: Default value used by helpers like :func:`data_to_hex` when no
#: ``octets_per_line`` argument is supplied.
OCTETS_PER_LINE_DEFAULT: int

# ---------------------------------------------------------------------------
# Dynamic module attributes
# ---------------------------------------------------------------------------
#
# The C extension registers a very large number of integer constants
# at module init time -- algorithm OIDs (``SEC_OID_*``), PKCS#11
# mechanism identifiers (``CKM_*``, ``CKA_*``), certificate database
# trust flags (``CERTDB_*``), key origins (``PK11_OriginUnwrap``
# etc.), and many more. Enumerating every one of them here would be
# both tedious and brittle.
#
# A module-level ``__getattr__`` returning ``Any`` is provided so
# that static type checkers accept any such attribute access on the
# module without having to mirror every C-level constant in this
# stub file. Symbols that are explicitly typed above retain their
# precise types; this fallback only kicks in for names that are not
# already declared.
def __getattr__(name: str) -> Any: ...
