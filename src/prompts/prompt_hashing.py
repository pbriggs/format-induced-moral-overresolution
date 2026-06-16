from __future__ import annotations

from utils.hashing import stable_hash


def prompt_hash(rendered_prompt: str) -> str:
    return stable_hash(rendered_prompt)

