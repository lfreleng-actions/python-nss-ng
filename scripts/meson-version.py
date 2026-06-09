#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2026 The Linux Foundation
"""Resolve the project version for meson-python dynamic versioning.

``meson-python`` has no native SCM/git versioning: when ``version`` is
listed in ``[project].dynamic`` it reads the version from the meson
``project()`` call. This helper supplies that value, derived from git,
so the version is driven entirely by the pushed tag.

Resolution order:

1. ``$PYTHON_NSS_NG_VERSION`` -- an explicit override for downstream
   packagers building from a context where neither git nor an sdist is
   available (e.g. a manually patched tree).
2. ``git describe`` against the surrounding work tree. This covers local
   development and CI wheel/sdist builds, where ``.git`` is present.
3. A frozen ``_version.txt`` baked into the sdist at ``meson dist`` time.
   Wheels built from the PyPI source distribution have no ``.git``, so
   the baked file is what lets them resolve the correct version.
4. ``.git_archival.txt`` substituted by ``git archive`` (export-subst).
   GitHub's auto-generated source tarballs are ``git archive`` output:
   they have no ``.git`` and no baked ``_version.txt``, but do carry the
   tag via this file, letting distro packagers build the real version.
5. As a last resort, in a git work tree with no reachable tag (a shallow
   CI checkout), a non-publishable ``0.0.0+g<sha>`` dev version.

Modes:

* default -- print the resolved version on stdout for ``run_command()``
  in ``meson.build``.
* ``--bake-dist`` -- write the resolved version to
  ``$MESON_DIST_ROOT/_version.txt`` during ``meson dist`` so the sdist
  carries a git-independent fallback.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# scripts/meson-version.py -> repository (or unpacked sdist) root
ROOT = Path(__file__).resolve().parent.parent
FALLBACK = ROOT / "_version.txt"
ARCHIVAL = ROOT / ".git_archival.txt"
ENV_OVERRIDE = "PYTHON_NSS_NG_VERSION"


def _from_env() -> str | None:
    """Return an explicit version override from the environment, if set."""
    return os.environ.get(ENV_OVERRIDE, "").strip() or None


def _from_git_archival() -> str | None:
    """Resolve the version from a ``git archive`` ``.git_archival.txt``.

    The ``describe-name`` field is substituted by ``git archive`` via the
    ``export-subst`` attribute. In a plain checkout the placeholder is not
    expanded (it still reads ``$Format:...$``), so such values are ignored.
    """
    if not ARCHIVAL.is_file():
        return None
    describe = None
    for line in ARCHIVAL.read_text(encoding="utf-8").splitlines():
        if line.startswith("describe-name:"):
            describe = line.split(":", 1)[1].strip()
            break
    if not describe or describe.startswith("$Format:"):
        return None
    return _to_pep440(describe)


def _run_git(args: list[str]) -> str | None:
    """Run a git command in ROOT, returning stripped stdout or None."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def _git_describes_this_tree() -> bool:
    """True only when ROOT is the top of a real git work tree.

    Guards against an unpacked sdist that happens to live inside an
    unrelated parent git repository (e.g. a build temp dir), which would
    otherwise yield a bogus version from the wrong project.
    """
    top = _run_git(["rev-parse", "--show-toplevel"])
    return top is not None and Path(top).resolve() == ROOT


def _to_pep440(describe: str) -> str:
    """Convert ``git describe`` output to a PEP 440 version string."""
    # Drop the conventional leading "v" (v1.0.6 -> 1.0.6).
    text = describe.lstrip("vV")
    # Exact tag (no trailing -<distance>-g<sha>): use it verbatim.
    match = re.fullmatch(r"(?P<tag>.+?)-(?P<distance>\d+)-g(?P<sha>[0-9a-f]+)", text)
    if match is None:
        return text
    # Commits after the tag: PEP 440 post-release with a local segment,
    # e.g. 1.0.6.post3+g1a2b3c4. Local-segment versions are intentionally
    # not publishable to PyPI; only exact tags produce clean versions.
    return f"{match.group('tag')}.post{match.group('distance')}+g{match.group('sha')}"


def resolve_version() -> str:
    """Resolve the project version from git or the baked fallback file."""
    env_version = _from_env()
    if env_version:
        return env_version
    in_git_tree = _git_describes_this_tree()
    if in_git_tree:
        describe = _run_git(["describe", "--tags", "--match", "v[0-9]*"])
        if describe:
            return _to_pep440(describe)
    if FALLBACK.is_file():
        return FALLBACK.read_text(encoding="utf-8").strip()
    archival = _from_git_archival()
    if archival:
        return archival
    if in_git_tree:
        # A git work tree with no reachable v* tag -- typically a shallow
        # CI checkout (fetch-depth: 1) that did not fetch tags, as used by
        # the test/audit/SBOM jobs that reinstall from source. Emit a
        # non-publishable dev version built from the short commit SHA so
        # those non-release builds still succeed. The local-version
        # segment ('+g...') is rejected by PyPI, so it can never be
        # mistaken for or published as a real release; release builds
        # check out the tag and take the branch above instead.
        sha = _run_git(["rev-parse", "--short", "HEAD"])
        if sha:
            return f"0.0.0+g{sha}"
    sys.exit(
        f"meson-version: cannot resolve version: set ${ENV_OVERRIDE}, or "
        "build from a git checkout, an sdist, or a git archive"
    )


def main(argv: list[str]) -> int:
    version = resolve_version()
    if "--bake-dist" in argv:
        dist_root = os.environ.get("MESON_DIST_ROOT")
        if not dist_root:
            sys.exit("meson-version: --bake-dist requires MESON_DIST_ROOT")
        target = Path(dist_root) / "_version.txt"
        target.write_text(version + "\n", encoding="utf-8")
        print(f"meson-version: baked {version} into {target}")
        return 0
    print(version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
