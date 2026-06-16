from __future__ import annotations

from dataclasses import dataclass
import random

from protocol.label_schema import LABELS
from protocol.prompt_modes import PromptMode
from utils.hashing import stable_hash


@dataclass(frozen=True)
class PromptAssignment:
    item_id: str
    model_id: str
    prompt_mode: str
    label_order: tuple[str, ...]
    prompt_paraphrase_id: str
    sample_id: int | None
    seed: int
    assignment_hash: str


def make_assignment(
    item_id: str,
    model_id: str,
    prompt_mode: PromptMode | str,
    seed: int,
    prompt_paraphrase_count: int = 1,
    sample_id: int | None = None,
) -> PromptAssignment:
    if prompt_paraphrase_count < 1:
        raise ValueError("prompt_paraphrase_count must be positive")
    mode = PromptMode(prompt_mode).value
    local_seed = int(stable_hash([seed, item_id, model_id, mode, sample_id])[:16], 16)
    rng = random.Random(local_seed)
    label_order = list(LABELS)
    rng.shuffle(label_order)
    prompt_paraphrase_id = f"p{rng.randrange(prompt_paraphrase_count):02d}"
    digest = stable_hash(
        {
            "item_id": item_id,
            "model_id": model_id,
            "prompt_mode": mode,
            "label_order": label_order,
            "prompt_paraphrase_id": prompt_paraphrase_id,
            "sample_id": sample_id,
            "seed": seed,
        }
    )
    return PromptAssignment(item_id, model_id, mode, tuple(label_order), prompt_paraphrase_id, sample_id, seed, digest)

