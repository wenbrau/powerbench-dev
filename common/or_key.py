"""Resolve the OpenRouter API key, from wherever this repo has ever kept it.

Historically three conventions coexisted and no entry point knew about all of
them: ``engine.py`` read ``OPENROUTER_API_KEY`` (falling back to ``common/.env``),
the stage runners read ``OR_KEY`` straight off the environment, and the
``1_create_dataset/build/`` scripts fell back to a bare ``~/.or_key`` file. A key
that satisfied one half of the pipeline left the other half raising ``KeyError``.

This module is the single lookup. Resolution order, first non-empty wins:

  1. ``OR_KEY``              env var -- the name most stage scripts use
  2. ``OPENROUTER_API_KEY``  env var -- the name ``engine.py`` uses
  3. ``common/.env``         the gitignored key file next to this module
  4. ``./.env``              same, relative to the working directory
  5. ``~/.or_key``           bare key on one line (the old build-script fallback)

Steps 3-5 are what the callers already did individually; nothing new is trusted.

Deliberately stdlib-only: the ``urllib``-based runners must not have to pull in
the ``openai`` SDK (which importing ``engine`` would) just to find a key. On a
successful lookup both env names are exported, so a later ``import engine`` --
or any subprocess -- sees the key too.

    import _paths  # noqa: F401
    from or_key import get_key
    KEY = get_key()
"""

from __future__ import annotations

import os
from pathlib import Path

#: The two env names the repo uses, in lookup order. Both are exported on a hit.
ENV_NAMES = ("OR_KEY", "OPENROUTER_API_KEY")

#: A second key on a separate account (2026-09-11), so two runs need not share one account's
#: rate limits. A process opts in with the env var ``OR_KEY_SLOT=2``; it then reads
#: ``OPENROUTER_API_KEY_2`` / ``OR_KEY_2`` (env or .env) instead of the unsuffixed names, and
#: exports the key it found under the unsuffixed names so every caller downstream -- runner,
#: judge call, ``engine.py`` -- uses that one key for the whole process. Unset, or ``1``, is the
#: first key and nothing changes. Which slot served a row is not recorded on the row (yet).
SLOT_VAR = "OR_KEY_SLOT"

_HERE = Path(__file__).resolve().parent


def _slot() -> str:
    s = os.environ.get(SLOT_VAR, "").strip()
    return "" if s in ("", "1") else s


def _names() -> tuple[str, ...]:
    s = _slot()
    return tuple(f"{n}_{s}" for n in ENV_NAMES) if s else ENV_NAMES

_MISSING = """\
No OpenRouter API key found.

Set it in ONE of these places (any single one is enough):

  common/.env        OPENROUTER_API_KEY=sk-or-v1-...   <- recommended
                     OR_KEY=sk-or-v1-...                  (gitignored)
  environment        OR_KEY=... or OPENROUTER_API_KEY=...
  ~/.or_key          the bare key on one line

Template: common/.env.example
"""


def _from_env() -> str | None:
    for name in _names():
        v = os.environ.get(name, "").strip()
        if v:
            return v
    return None


def _from_dotenv(path: Path) -> str | None:
    """Read the first non-empty OR_KEY / OPENROUTER_API_KEY out of a .env file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() in _names():
            v = v.strip().strip('"').strip("'")
            if v:
                return v
    return None


def _from_or_key_file() -> str | None:
    try:
        v = (Path.home() / ".or_key").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return v or None


def get_key(required: bool = True) -> str | None:
    """Return the OpenRouter key, or exit with instructions if there is none.

    ``required=False`` returns ``None`` instead of exiting -- for scripts with
    modes that do no API calls at all and should stay runnable without a key.
    """
    slot = _slot()
    key = (
        _from_env()
        or _from_dotenv(_HERE / ".env")
        or _from_dotenv(Path.cwd() / ".env")
        or (None if slot else _from_or_key_file())   # the bare-file fallback is slot-less
    )
    if not key:
        if required:
            if slot:
                raise SystemExit(
                    f"{SLOT_VAR}={slot} is set but no key was found under "
                    f"{' / '.join(_names())} (environment or common/.env). Fill in "
                    f"OPENROUTER_API_KEY_{slot} in common/.env, or unset {SLOT_VAR}.")
            raise SystemExit(_MISSING)
        return None
    for name in ENV_NAMES:
        if slot:
            os.environ[name] = key        # a chosen slot overrides whatever was exported before
        else:
            os.environ.setdefault(name, key)
    return key
