#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
#
# Build and install NSS/NSPR from source
# This script is used in GitHub Actions CI for python-nss-ng

set -euo pipefail

# Configuration
NSS_VERSION="${NSS_VERSION:-3.133}"
NSPR_VERSION="${NSPR_VERSION:-4.39}"
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr}"
BUILD_DIR="${BUILD_DIR:-$HOME/nss-build}"

echo "========================================"
echo "NSS/NSPR Build and Installation"
echo "========================================"
echo "NSS Version:    ${NSS_VERSION}"
echo "NSPR Version:   ${NSPR_VERSION}"
echo "Install Prefix: ${INSTALL_PREFIX}"
echo "Build Dir:      ${BUILD_DIR}"
echo "========================================"

# Install build dependencies
echo ""
echo "Installing build dependencies..."
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    pkg-config \
    zlib1g-dev \
    libsqlite3-dev \
    gyp \
    ninja-build \
    meson \
    wget

# Create build directory
# Verify file checksum
verify_checksum() {
    local file="$1"
    local expected_sha256="$2"
    local file_basename
    file_basename=$(basename "$file")

    if [ -z "$expected_sha256" ]; then
        echo "WARNING: No checksum provided for $file_basename - skipping verification" >&2
        return 0
    fi

    echo "Verifying checksum for $file_basename..."

    if command -v sha256sum &> /dev/null; then
        local actual_sha256
        actual_sha256=$(sha256sum "$file" | awk '{print $1}')
    elif command -v shasum &> /dev/null; then
        local actual_sha256
        actual_sha256=$(shasum -a 256 "$file" | awk '{print $1}')
    else
        echo "ERROR: Neither sha256sum nor shasum found." >&2
        echo "Cannot verify checksums." >&2
        exit 1
    fi

    if [ "$actual_sha256" != "$expected_sha256" ]; then
        echo "ERROR: Checksum verification failed for $file_basename" >&2
        echo "Expected: $expected_sha256" >&2
        echo "Got:      $actual_sha256" >&2
        echo "This could indicate a compromised download or network issue." >&2
        exit 1
    fi

    echo "✓ Checksum verified for $file_basename"
}

# Known SHA256 checksums for NSS/NSPR releases
# These should be updated when versions change
# Source: https://ftp.mozilla.org/pub/security/nss/releases/ and https://ftp.mozilla.org/pub/nspr/releases/
get_nss_checksum() {
    local version="$1"
    case "$version" in
        3.133)
            echo "4d752526b9846a1d962588cfbd09b7cc2a4f6a4effbd9157d58a30e8a2573065"
            ;;
        3.118)
            echo "06f2d34c7c421da430b9d78fc6590105500b9439efa19cdaa0a57ed7dc948aad"
            ;;
        *)
            echo ""  # Return empty for unknown versions - will trigger warning
            ;;
    esac
}

get_nspr_checksum() {
    local version="$1"
    case "$version" in
        4.39)
            echo "bbd02ee87a55676063a63e5bc819e0227de2666b47307b2a0134414cdf42368e"
            ;;
        4.37)
            echo "5f9344ed0e31855bd38f88b33c9d9ab94f70ce547ef3213e488d1520f61840fa"
            ;;
        *)
            echo ""  # Return empty for unknown versions - will trigger warning
            ;;
    esac
}

echo ""
echo "Creating build directory..."
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

# Download and extract NSS
echo ""
echo "Downloading NSS ${NSS_VERSION}..."
NSS_URL="https://ftp.mozilla.org/pub/security/nss/releases"
NSS_FILE="nss-${NSS_VERSION}.tar.gz"
NSS_RELEASE_TAG="NSS_${NSS_VERSION//./_}_RTM"
NSS_CHECKSUM=$(get_nss_checksum "${NSS_VERSION}")

wget -q "${NSS_URL}/${NSS_RELEASE_TAG}/src/${NSS_FILE}"

verify_checksum "${NSS_FILE}" "${NSS_CHECKSUM}"

echo "Extracting NSS..."
tar -xzf "${NSS_FILE}"
rm "${NSS_FILE}"

# Download and extract NSPR
echo ""
echo "Downloading NSPR ${NSPR_VERSION}..."
NSPR_URL="https://ftp.mozilla.org/pub/nspr/releases"
NSPR_FILE="nspr-${NSPR_VERSION}.tar.gz"
NSPR_CHECKSUM=$(get_nspr_checksum "${NSPR_VERSION}")

wget -q "${NSPR_URL}/v${NSPR_VERSION}/src/${NSPR_FILE}"

verify_checksum "${NSPR_FILE}" "${NSPR_CHECKSUM}"

echo "Extracting NSPR..."
tar -xzf "${NSPR_FILE}"
rm "${NSPR_FILE}"

# Build NSPR
echo ""
echo "========================================"
echo "Building NSPR ${NSPR_VERSION}..."
echo "========================================"
cd "${BUILD_DIR}/nspr-${NSPR_VERSION}/nspr"
./configure --prefix="${INSTALL_PREFIX}" \
    --with-mozilla \
    --with-pthreads \
    --enable-64bit
make
echo "Installing NSPR..."
sudo make install

# Build NSS
echo ""
echo "========================================"
echo "Building NSS ${NSS_VERSION}..."
echo "========================================"

# Set PKG_CONFIG_PATH so NSS can find NSPR
export PKG_CONFIG_PATH="${INSTALL_PREFIX}/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
echo "PKG_CONFIG_PATH=${PKG_CONFIG_PATH}"

cd "${BUILD_DIR}/nss-${NSS_VERSION}/nss"

# Verify build.sh exists
if [ ! -f build.sh ]; then
    echo "ERROR: build.sh not found in $(pwd)" >&2
    ls -la
    exit 1
fi

chmod +x build.sh

# Build NSS
./build.sh \
    --opt \
    --disable-tests \
    --system-sqlite \
    --system-nspr \
    --enable-libpkix

# Install NSS
echo ""
echo "========================================"
echo "Installing NSS ${NSS_VERSION}..."
echo "========================================"
cd "${BUILD_DIR}/nss-${NSS_VERSION}/dist"

# Headers are in dist/public/nss and dist/private/nss
echo "Installing headers..."
sudo mkdir -p "${INSTALL_PREFIX}/include/nss"
sudo cp -r public/nss/* "${INSTALL_PREFIX}/include/nss/"
sudo cp -r private/nss/* "${INSTALL_PREFIX}/include/nss/"

# Libraries and binaries are in dist/Release
echo "Installing libraries..."

# Detect architecture and set appropriate library directory
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    # On ARM64, use the multiarch lib directory
    LIB_DIR="${INSTALL_PREFIX}/lib/aarch64-linux-gnu"
    echo "Detected ARM64 architecture - installing to ${LIB_DIR}"
    sudo mkdir -p "${LIB_DIR}"
    sudo cp -L Release/lib/*.so "${LIB_DIR}/"
    # Also install to standard lib for pkg-config
    sudo cp -L Release/lib/*.so "${INSTALL_PREFIX}/lib/"
elif [ "$ARCH" = "x86_64" ]; then
    # On x86_64, use the multiarch lib directory
    LIB_DIR="${INSTALL_PREFIX}/lib/x86_64-linux-gnu"
    echo "Detected x86_64 architecture - installing to ${LIB_DIR}"
    sudo mkdir -p "${LIB_DIR}"
    sudo cp -L Release/lib/*.so "${LIB_DIR}/"
    # Also install to standard lib for pkg-config
    sudo cp -L Release/lib/*.so "${INSTALL_PREFIX}/lib/"
else
    # Fallback to standard lib directory
    echo "Using standard lib directory for architecture: ${ARCH}"
    sudo cp -L Release/lib/*.so "${INSTALL_PREFIX}/lib/"
fi

echo "Installing binaries..."
sudo cp -L Release/bin/* "${INSTALL_PREFIX}/bin/" 2>/dev/null || true

# Remove old system NSS/NSPR libraries to avoid conflicts
echo ""
echo "Removing old system NSS/NSPR libraries to avoid version conflicts..."
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    # Remove old ARM64 system libraries
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnss3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnspr4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnssutil3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnsssysinit.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnssckbi.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnssdbm3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libnssdbm3.chk 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libplc4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libplds4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libsmime3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/aarch64-linux-gnu/libssl3.so* 2>/dev/null || true
elif [ "$ARCH" = "x86_64" ]; then
    # Remove old x86_64 system libraries
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnss3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnspr4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnssutil3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnsssysinit.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnssckbi.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnssdbm3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libnssdbm3.chk 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libplc4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libplds4.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libsmime3.so* 2>/dev/null || true
    sudo rm -f /usr/lib/x86_64-linux-gnu/libssl3.so* 2>/dev/null || true
fi

# Ensure /usr/lib is in the dynamic linker search path
echo ""
echo "Configuring dynamic linker..."
echo "/usr/lib" | sudo tee /etc/ld.so.conf.d/nss-custom.conf > /dev/null

# Create additional symlinks in /lib for better compatibility
echo "Creating library symlinks in /lib..."
sudo ln -sf /usr/lib/libnss3.so /lib/libnss3.so 2>/dev/null || true
sudo ln -sf /usr/lib/libnspr4.so /lib/libnspr4.so 2>/dev/null || true
sudo ln -sf /usr/lib/libnssutil3.so /lib/libnssutil3.so 2>/dev/null || true
sudo ln -sf /usr/lib/libssl3.so /lib/libssl3.so 2>/dev/null || true
sudo ln -sf /usr/lib/libsmime3.so /lib/libsmime3.so 2>/dev/null || true
sudo ln -sf /usr/lib/libplc4.so /lib/libplc4.so 2>/dev/null || true
sudo ln -sf /usr/lib/libplds4.so /lib/libplds4.so 2>/dev/null || true

# Update library cache
echo "Updating library cache..."
sudo ldconfig

# Verify libraries are in cache
echo ""
echo "Verifying NSS/NSPR in ldconfig cache:"
ldconfig -p | grep -E '(nss3|nspr4)' || echo "WARNING: NSS/NSPR not in cache"

# Create pkg-config files
echo ""
echo "Creating pkg-config files..."
sudo tee "${INSTALL_PREFIX}/lib/pkgconfig/nss.pc" > /dev/null <<EOF
prefix=${INSTALL_PREFIX}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include/nss

Name: NSS
Description: Network Security Services
Version: ${NSS_VERSION}
Requires: nspr >= ${NSPR_VERSION}
Libs: -L\${libdir} -lssl3 -lsmime3 -lnss3 -lnssutil3
Cflags: -I\${includedir}
EOF

sudo tee "${INSTALL_PREFIX}/lib/pkgconfig/nspr.pc" > /dev/null <<EOF
prefix=${INSTALL_PREFIX}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include/nspr

Name: NSPR
Description: Netscape Portable Runtime
Version: ${NSPR_VERSION}
Libs: -L\${libdir} -lplds4 -lplc4 -lnspr4
Cflags: -I\${includedir}
EOF

# Verify installation
echo ""
echo "========================================"
echo "Verifying installation..."
echo "========================================"
echo "NSS version:  $(pkg-config --modversion nss)"
echo "NSPR version: $(pkg-config --modversion nspr)"
echo ""
echo "NSS headers:  ${INSTALL_PREFIX}/include/nss/"
find "${INSTALL_PREFIX}/include/nss/" -maxdepth 1 -type f 2>/dev/null | head -5 || true
echo "..."
echo ""
echo "NSS libraries: ${INSTALL_PREFIX}/lib/"
find "${INSTALL_PREFIX}/lib/" -maxdepth 1 -name "libnss*" 2>/dev/null | head -5 || true
echo ""
echo "========================================"
echo "NSS/NSPR installation complete! ✅"
echo "========================================"
