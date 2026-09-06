"""Serving stacks fixed in code, overriding whatever a pins file says.

`PROVIDER_LOCK` maps a model id to the pin entry it must be served from, in the same shape
`provider_pins.json` stores one. Keys starting with `_` are metadata about the decision, not part
of the pin. Three helpers act on it:

    pin_entry(model)               the locked entry, without the `_` metadata
    assert_locked(model, provider) raises unless `provider` is the locked stack; no-op for a model
                                   that is not locked
    apply_lock(pins)               rewrites every locked model in a pins dict onto its locked
                                   stack, in place, and returns the list of changes it made (empty
                                   when the file already agreed) so the caller can print and record
                                   them. `allow_drift=True` reports what it WOULD change and
                                   touches nothing

Who calls it: `run_targets_pinned.py` and `run_capability_probe.py` apply it to whatever `--pins`
file they were handed, at startup, before any API call; `resolve_providers.py` applies it last,
after the endpoint ranking, so a regenerated pins file comes out locked. All three accept
`--allow-provider-drift` to bypass the lock and record the bypass in the run's meta.

To lock a model, add its pin entry with a `_reason` and a `_decided` date. To unlock one, delete
the entry: it goes back to following the pins file.

    import _paths  # noqa: F401
    from provider_lock import PROVIDER_LOCK, apply_lock, assert_locked
"""
from __future__ import annotations

#: model id -> the pin entry that must be used, in the same shape `provider_pins.json` stores.
#: `_reason` / `_decided` are metadata and are stripped before the entry is written into a pins file.
PROVIDER_LOCK = {
    "deepseek/deepseek-v4-pro-0813": {
        "provider": "gmicloud",
        "provider_name": "GMICloud",
        "tag": "gmicloud/fp8",
        "quantization": "fp8",
        "first_party": False,
        "price_out_per_m": 3.564,
        "uptime_30m": 100.0,
        "uptime_1d": 99.6,
        "context_length": 1048575,
        "supports_reasoning_effort": True,
        "supports_temperature": True,
        "overridden": True,
        "_reason": "one serving stack for the whole study. The 26/08 re-pin to siliconflow split "
                   "deepseek across GMICloud (D1-en, D2, all three controls) and SiliconFlow "
                   "(D1-7langs, D3), which confounds the language and AI-agent "
                   "difference-in-differences: the power arm changes provider where the control "
                   "arm does not. GMICloud honours reasoning:{enabled:false} again (verified "
                   "05/09/2026, 12/12 and 6/6 at zero reasoning tokens on the three control "
                   "runs), so it is the stack the majority of the study already sits on.",
        "_decided": "2026-09-06",
    },
}

def pin_entry(model: str) -> dict:
    """The locked pin for `model`, without the `_reason` / `_decided` metadata."""
    return {k: v for k, v in PROVIDER_LOCK[model].items() if not k.startswith("_")}


def assert_locked(model: str, provider: str) -> None:
    """Raise unless `provider` is the locked stack for `model`. No-op for unlocked models."""
    want = PROVIDER_LOCK.get(model)
    if want is None or provider == want["provider"]:
        return
    raise SystemExit(
        f"refusing to serve {model!r} from {provider!r}: it is locked to "
        f"{want['provider']!r} ({want['_reason']} -- common/provider_lock.py, decided "
        f"{want['_decided']})."
    )


def apply_lock(pins: dict, allow_drift: bool = False) -> list[str]:
    """Force every locked model in `pins` onto its locked stack, in place.

    Returns a list of human-readable changes (empty when the pins file already agreed), so the
    caller can print them and stamp them into the run's meta. `allow_drift=True` leaves the pins
    untouched and only reports what WOULD have changed; it must come from an explicit flag.
    """
    changes = []
    for model, want in PROVIDER_LOCK.items():
        have = pins.get(model)
        if have is None or have.get("provider") == want["provider"]:
            continue
        entry = pin_entry(model)
        # Keep whatever the pins file knew that the lock does not carry (e.g. `alternatives`),
        # so the corrected entry stays as informative as the one it replaces.
        for k, v in have.items():
            entry.setdefault(k, v)
        verb = "WOULD BE forced" if allow_drift else "forced"
        changes.append(f"{model}: {have.get('provider')}/{have.get('quantization')} -> "
                       f"{entry['provider']}/{entry['quantization']} ({verb} by "
                       f"common/provider_lock.py, decided {want['_decided']})")
        if not allow_drift:
            pins[model] = entry
    return changes
