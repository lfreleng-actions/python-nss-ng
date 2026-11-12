# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
#
# Makefile for python-nss-ng
# Handles NSS/NSPR dependencies and environment setup for CI builds

.PHONY: help deps-nss deps-test deps-test-system deps-build clean \
        env-setup env-github-actions

# Default target
help:
	@echo "python-nss-ng Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  deps-nss           - Build and install NSS/NSPR from source"
	@echo "  deps-test-system   - Install system test deps (apt only)"
	@echo "  deps-test          - Install all test dependencies (apt+pip)"
	@echo "  deps-build         - Install build dependencies"
	@echo "  env-setup          - Set up environment variables"
	@echo "  env-github-actions - Export env vars to GitHub Actions"
	@echo "  clean              - Clean build artifacts"
	@echo ""
	@echo "Environment variables:"
	@echo "  NSS_VERSION        - NSS version (default: 3.133)"
	@echo "  NSPR_VERSION       - NSPR version (default: 4.39)"
	@echo "  INSTALL_PREFIX     - Install prefix (default: /usr)"

# Configuration
NSS_VERSION ?= 3.133
NSPR_VERSION ?= 4.39
INSTALL_PREFIX ?= /usr
PKG_CONFIG_PATH := $(INSTALL_PREFIX)/lib/pkgconfig:$(PKG_CONFIG_PATH)
LD_LIBRARY_PATH := $(INSTALL_PREFIX)/lib:$(LD_LIBRARY_PATH)

# Detect platform
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    PLATFORM := macos
    LIB_PATH_VAR := DYLD_LIBRARY_PATH
else
    PLATFORM := linux
    LIB_PATH_VAR := LD_LIBRARY_PATH
endif

# Build NSS/NSPR from source
deps-nss:
	@echo "Building NSS/NSPR from source..."
	chmod +x .github/scripts/install-nss.sh
	NSS_VERSION=$(NSS_VERSION) \
	NSPR_VERSION=$(NSPR_VERSION) \
	INSTALL_PREFIX=$(INSTALL_PREFIX) \
	./.github/scripts/install-nss.sh

# Install system-level test dependencies only (apt packages)
# Use this target in CI *before* actions/setup-python so that pip installs
# are handled by the correct (hostedtoolcache) Python interpreter.
deps-test-system:
	@echo "Installing system-level test dependencies..."
ifeq ($(PLATFORM),linux)
	sudo apt-get update || true
	sudo apt-get install -y meson ninja-build || true
endif

# Install test dependencies (for test jobs)
# NOTE: This target runs pip install and should only be called *after*
# actions/setup-python so that packages are installed into the correct
# Python environment. If called with the system Python when a different
# Python will run the tests, imports will fail at test time.
deps-test: deps-test-system
	@echo "Installing pip test dependencies..."
	python -m pip install --upgrade pip || true
	python -m pip install meson-python meson ninja pytest pytest-cov pytest-timeout pytest-xdist hypothesis mypy || true

# Install build dependencies (minimal set for build jobs)
deps-build:
	@echo "Installing minimal build dependencies..."
	python -m pip install --upgrade pip
	python -m pip install build setuptools wheel setuptools-scm meson ninja

# Set up environment variables (for local development)
env-setup:
	@echo "Environment setup:"
	@echo "export PKG_CONFIG_PATH=$(PKG_CONFIG_PATH)"
	@echo "export $(LIB_PATH_VAR)=$(LD_LIBRARY_PATH)"

# Export environment to GitHub Actions
env-github-actions:
	@echo "PKG_CONFIG_PATH=$(PKG_CONFIG_PATH)" >> $(GITHUB_ENV)
	@echo "$(LIB_PATH_VAR)=$(LD_LIBRARY_PATH)" >> $(GITHUB_ENV)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true
	find . -type f -name '*.so' -delete 2>/dev/null || true
