from __future__ import annotations

from protocol.label_schema import LABELS

ALIASES: dict[str, str] = {
    "a": "author",
    "author": "author",
    "narrator": "author",
    "op": "author",
    "wrong_author": "author",
    "o": "other",
    "other": "other",
    "wrong_other": "other",
    "e": "everybody",
    "everyone": "everybody",
    "everybody": "everybody",
    "both": "everybody",
    "both_sides": "everybody",
    "n": "nobody",
    "none": "nobody",
    "nobody": "nobody",
    "no_one": "nobody",
    "i": "info",
    "info": "info",
    "not_enough_info": "info",
    "cannot_tell": "info",
    "unclear": "info",
}


def normalize_label(value: str) -> str:
    key = value.strip().lower().replace("-", "_").replace(" ", "_")
    label = ALIASES.get(key)
    if label is None or label not in LABELS:
        raise ValueError(f"cannot normalize label {value!r}")
    return label

