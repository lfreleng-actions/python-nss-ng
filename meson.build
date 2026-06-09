# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

project(
  'python-nss-ng',
  'c',
  # Dynamic versioning: the version is derived from the most recent
  # `v*` git tag (or, for builds from an sdist, the baked-in
  # `_version.txt`). See scripts/meson-version.py for the resolution
  # logic and `meson.add_dist_script` below for the sdist fallback.
  version: run_command(
    'scripts/meson-version.py',
    check: true,
  ).stdout().strip(),
  license: 'MPL-2.0 OR GPL-2.0-or-later OR LGPL-2.0-or-later',
  default_options: [
    'warning_level=2',
    'c_std=c99',
  ],
  meson_version: '>=1.2.0',
)

# Bake the resolved version into the source distribution so that wheels
# built from the sdist (which has no `.git`) can recover the correct
# version. The script writes `$MESON_DIST_ROOT/_version.txt`, which
# scripts/meson-version.py reads back as its fallback.
meson.add_dist_script('scripts/meson-version.py', '--bake-dist')

# Import Python module
py = import('python').find_installation(pure: false)

# Find NSS and NSPR dependencies using pkg-config
# These will automatically handle include paths, library paths, and link flags
# Require NSS 3.100+ for modern cryptographic key types (edKey, ecMontKey, mldsaKey)
# Fedora provides NSS 3.117+ which includes all modern features
nss_dep = dependency('nss', version: '>=3.100', required: true)
nspr_dep = dependency('nspr', version: '>=4.35', required: true)

# Get Python dependency
py_dep = py.dependency()

# Compiler configuration
cc = meson.get_compiler('c')

# Suppress specific pedantic warnings in legacy C code
# Keep critical warnings enabled (type errors, undefined behavior, etc.)
warning_flags = []
if cc.get_id() == 'clang' or cc.get_id() == 'gcc'
  # Suppress warnings for legacy C code patterns
  warning_flags += cc.get_supported_arguments([
    '-Wno-missing-field-initializers',  # Designated initializers handle this in C99
    '-Wno-unused-parameter',             # Many Python C API functions have unused params
    '-Wno-cast-function-type',           # Python C API requires function pointer casts
    '-Wno-cast-function-type-strict',    # Newer clang warning for strict function casts
  ])
endif

# Set up RPATH so extension modules can find NSS/NSPR libraries
# This ensures the .so files can load even when LD_LIBRARY_PATH isn't set
link_args = []
if host_machine.system() == 'linux'
  # Add RPATH for standard library locations
  link_args += [
    '-Wl,-rpath,/usr/lib',
    '-Wl,-rpath,/usr/lib/x86_64-linux-gnu',
    '-Wl,-rpath,/usr/lib/aarch64-linux-gnu',
  ]
endif

# Common include directories
inc_dirs = include_directories('src')

# Common source dependencies (headers that extensions depend on)
common_headers = files(
  'src/py_nspr_common.h',
  'src/py_nspr_error.h',
)

# Extension: nss.error
py.extension_module(
  'error',
  'src/py_nspr_error.c',
  dependencies: [py_dep, nss_dep, nspr_dep],
  include_directories: inc_dirs,
  c_args: warning_flags,
  link_args: link_args,
  install: true,
  subdir: 'nss',
)

# Extension: nss.io
py.extension_module(
  'io',
  'src/py_nspr_io.c',
  dependencies: [py_dep, nss_dep, nspr_dep],
  include_directories: inc_dirs,
  c_args: warning_flags,
  link_args: link_args,
  install: true,
  subdir: 'nss',
)

# Extension: nss.nss
py.extension_module(
  'nss',
  'src/py_nss.c',
  dependencies: [py_dep, nss_dep, nspr_dep],
  include_directories: inc_dirs,
  c_args: warning_flags,
  link_args: link_args,
  install: true,
  subdir: 'nss',
)

# Extension: nss.ssl
py.extension_module(
  'ssl',
  'src/py_ssl.c',
  dependencies: [py_dep, nss_dep, nspr_dep],
  include_directories: inc_dirs,
  c_args: warning_flags,
  link_args: link_args,
  install: true,
  subdir: 'nss',
)

# Install Python source files
py.install_sources(
  'src/__init__.py',
  'src/deprecations.py',
  'src/nss_context.py',
  'src/secure_logging.py',
  subdir: 'nss',
  preserve_path: false,
)

# Install type stub files (.pyi)
py.install_sources(
  'src/io.pyi',
  'src/nss.pyi',
  'src/ssl.pyi',
  subdir: 'nss',
  preserve_path: false,
)

# Build summary
summary({
  'NSS version': nss_dep.version(),
  'NSPR version': nspr_dep.version(),
  'Python version': py.language_version(),
  'Install prefix': get_option('prefix'),
}, section: 'Configuration')
