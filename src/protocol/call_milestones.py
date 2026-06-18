from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from protocol.prompt_modes import PromptMode


CORE_PROMPT_MODES: tuple[PromptMode, PromptMode] = (
    PromptMode.DISTRIBUTION,
    PromptMode.DESCRIPTIVE_VERDICT,
)

DISAGREEMENT_BINS: tuple[str, ...] = (
    "high_consensus",
    "moderate_consensus",
    "low_consensus",
    "diffuse",
)

CONTESTED_BINS: tuple[str, str] = ("low_consensus", "diffuse")
MODEL_COUNT = 5


class MilestoneComponentType(StrEnum):
    CORE_CROSS_FORMAT = "core_cross_format"
    REPEATED_SAMPLING = "repeated_sampling"
    PARAPHRASE_AUDIT = "paraphrase_audit"
    PILOT_BUFFER = "pilot_buffer"
    NORMATIVE_CERTAINTY = "normative_certainty"
    LABEL_ORDER_RESERVE = "label_order_reserve"


class MilestoneDecision(StrEnum):
    CONTINUE = "continue"
    REVISE = "revise"
    STOP = "stop_or_redesign"


@dataclass(frozen=True)
class BinAllocation:
    high_consensus: int
    moderate_consensus: int
    low_consensus: int
    diffuse: int

    @property
    def total_items(self) -> int:
        return self.high_consensus + self.moderate_consensus + self.low_consensus + self.diffuse

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class MilestoneComponent:
    name: str
    component_type: MilestoneComponentType
    item_count: int
    model_count: int = MODEL_COUNT
    prompt_modes: tuple[PromptMode, ...] = CORE_PROMPT_MODES
    samples_per_item: int = 1
    bin_allocation: BinAllocation | None = None
    role: str = ""

    @property
    def planned_calls(self) -> int:
        return self.item_count * self.model_count * len(self.prompt_modes) * self.samples_per_item

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["component_type"] = self.component_type.value
        payload["prompt_modes"] = [mode.value for mode in self.prompt_modes]
        payload["planned_calls"] = self.planned_calls
        if self.bin_allocation is not None:
            payload["bin_allocation"] = self.bin_allocation.to_dict()
        return payload


@dataclass(frozen=True)
class MilestoneThresholds:
    overall_validity_min: float
    per_model_mode_validity_min: float | None = None
    positive_gap_models_min: int | None = None
    positive_surplus_models_min: int | None = None
    low_diffuse_gap_min: float | None = None
    low_diffuse_surplus_min: float | None = None
    positive_sampling_models_min: int | None = None
    require_low_diffuse_gt_high_consensus: bool = False
    require_low_diffuse_surplus_gt_high_consensus: bool = False
    require_paraphrase_preserves_direction: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CallMilestone:
    name: str
    planned_call_budget: int
    role: str
    components: tuple[MilestoneComponent, ...]
    continue_thresholds: MilestoneThresholds
    normative_certainty_allowed: bool = False
    use_as_confirmatory: bool = False

    @property
    def planned_calls(self) -> int:
        return sum(component.planned_calls for component in self.components)

    def component(self, component_type: MilestoneComponentType | str) -> MilestoneComponent:
        requested = MilestoneComponentType(component_type)
        for component in self.components:
            if component.component_type == requested:
                return component
        raise KeyError(f"{self.name} has no {requested.value!r} component")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "planned_call_budget": self.planned_call_budget,
            "planned_calls": self.planned_calls,
            "role": self.role,
            "components": [component.to_dict() for component in self.components],
            "continue_thresholds": self.continue_thresholds.to_dict(),
            "normative_certainty_allowed": self.normative_certainty_allowed,
            "use_as_confirmatory": self.use_as_confirmatory,
        }


def _core(items: int, allocation: BinAllocation) -> MilestoneComponent:
    return MilestoneComponent(
        name="Core cross-format sample",
        component_type=MilestoneComponentType.CORE_CROSS_FORMAT,
        item_count=items,
        prompt_modes=CORE_PROMPT_MODES,
        bin_allocation=allocation,
        role="distribution mode plus descriptive verdict/agreement mode",
    )


def _engineering_core(calls: int) -> MilestoneComponent:
    if calls == 1:
        return MilestoneComponent(
            name="Engineering route check",
            component_type=MilestoneComponentType.CORE_CROSS_FORMAT,
            item_count=1,
            model_count=1,
            prompt_modes=(PromptMode.DISTRIBUTION,),
            role="one real provider call to verify credentials, routing, parsing, and ledger writes",
        )
    if calls == 10:
        return MilestoneComponent(
            name="Engineering cross-provider core check",
            component_type=MilestoneComponentType.CORE_CROSS_FORMAT,
            item_count=1,
            model_count=5,
            prompt_modes=CORE_PROMPT_MODES,
            role="all five models across distribution and descriptive verdict modes",
        )
    if calls == 50:
        return MilestoneComponent(
            name="Engineering schema and latency check",
            component_type=MilestoneComponentType.CORE_CROSS_FORMAT,
            item_count=5,
            model_count=5,
            prompt_modes=CORE_PROMPT_MODES,
            role="small cross-provider sample to catch schema, parsing, latency, and outlier behavior",
        )
    raise ValueError(f"unsupported engineering milestone size {calls}")


def _repeated(items: int, samples: int, allocation: BinAllocation) -> MilestoneComponent:
    return MilestoneComponent(
        name="Repeated-sampling subset",
        component_type=MilestoneComponentType.REPEATED_SAMPLING,
        item_count=items,
        prompt_modes=(PromptMode.SAMPLING,),
        samples_per_item=samples,
        bin_allocation=allocation,
        role="behavioral sampling-compression check",
    )


def _paraphrase(items: int, allocation: BinAllocation | None = None) -> MilestoneComponent:
    return MilestoneComponent(
        name="Paraphrase / contamination audit",
        component_type=MilestoneComponentType.PARAPHRASE_AUDIT,
        item_count=items,
        prompt_modes=(PromptMode.PARAPHRASED_DISTRIBUTION, PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT),
        bin_allocation=allocation,
        role="prompt robustness and contamination check",
    )


CALL_MILESTONES: tuple[CallMilestone, ...] = (
    CallMilestone(
        name="1",
        planned_call_budget=1,
        role="engineering shakedown: one-call provider hookup test excluded from study analyses",
        components=(_engineering_core(1),),
        continue_thresholds=MilestoneThresholds(overall_validity_min=1.0),
    ),
    CallMilestone(
        name="10",
        planned_call_budget=10,
        role="engineering shakedown: five-model core route/schema test excluded from study analyses",
        components=(_engineering_core(10),),
        continue_thresholds=MilestoneThresholds(overall_validity_min=0.90),
    ),
    CallMilestone(
        name="50",
        planned_call_budget=50,
        role="engineering shakedown: small schema, latency, and outlier screen excluded from study analyses",
        components=(_engineering_core(50),),
        continue_thresholds=MilestoneThresholds(overall_validity_min=0.95),
    ),
    CallMilestone(
        name="3k",
        planned_call_budget=3000,
        role="engineering and measurement smoke test",
        components=(
            _core(200, BinAllocation(30, 40, 80, 50)),
            _repeated(20, 5, BinAllocation(3, 3, 8, 6)),
            _paraphrase(50, BinAllocation(8, 10, 20, 12)),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            per_model_mode_validity_min=0.90,
            positive_gap_models_min=3,
        ),
    ),
    CallMilestone(
        name="6k",
        planned_call_budget=6000,
        role="first directional signal check",
        components=(
            _core(400, BinAllocation(60, 80, 160, 100)),
            _repeated(50, 6, BinAllocation(8, 10, 20, 12)),
            _paraphrase(50, BinAllocation(8, 10, 20, 12)),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            positive_gap_models_min=4,
            positive_surplus_models_min=4,
            low_diffuse_gap_min=0.08,
            positive_sampling_models_min=3,
            require_low_diffuse_gt_high_consensus=True,
            require_low_diffuse_surplus_gt_high_consensus=True,
        ),
    ),
    CallMilestone(
        name="13k",
        planned_call_budget=13000,
        role="serious pre-confirmatory diagnostic run",
        components=(
            _core(800, BinAllocation(120, 150, 320, 210)),
            _repeated(100, 8, BinAllocation(15, 20, 40, 25)),
            _paraphrase(100, BinAllocation(15, 20, 40, 25)),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            per_model_mode_validity_min=0.90,
            positive_gap_models_min=4,
            positive_surplus_models_min=4,
            low_diffuse_gap_min=0.10,
            low_diffuse_surplus_min=0.10,
            positive_sampling_models_min=3,
            require_low_diffuse_gt_high_consensus=True,
            require_low_diffuse_surplus_gt_high_consensus=True,
            require_paraphrase_preserves_direction=True,
        ),
    ),
    CallMilestone(
        name="25k",
        planned_call_budget=24750,
        role="lean journal-capable sampled audit",
        components=(
            _core(1500, BinAllocation(250, 300, 550, 400)),
            _repeated(150, 10, BinAllocation(25, 30, 55, 40)),
            _paraphrase(125, BinAllocation(20, 25, 50, 30)),
            MilestoneComponent(
                name="Pilot buffer / prompt validation",
                component_type=MilestoneComponentType.PILOT_BUFFER,
                item_count=100,
                prompt_modes=CORE_PROMPT_MODES,
                role="predefined prompt-validation buffer",
            ),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            per_model_mode_validity_min=0.90,
            positive_gap_models_min=4,
            positive_surplus_models_min=4,
            low_diffuse_gap_min=0.10,
            low_diffuse_surplus_min=0.10,
            positive_sampling_models_min=3,
            require_low_diffuse_gt_high_consensus=True,
            require_low_diffuse_surplus_gt_high_consensus=True,
            require_paraphrase_preserves_direction=True,
        ),
        use_as_confirmatory=True,
    ),
    CallMilestone(
        name="35k",
        planned_call_budget=35000,
        role="minimum-defensible bridge between the lean and full reduced study",
        components=(
            _core(1500, BinAllocation(250, 300, 550, 400)),
            _repeated(300, 10, BinAllocation(50, 60, 110, 80)),
            _paraphrase(200, BinAllocation(30, 40, 80, 50)),
            MilestoneComponent(
                name="Secondary normative-certainty subset",
                component_type=MilestoneComponentType.NORMATIVE_CERTAINTY,
                item_count=500,
                prompt_modes=(PromptMode.NORMATIVE_VERDICT,),
                bin_allocation=BinAllocation(80, 100, 190, 130),
                role="clearly secondary certainty endpoint",
            ),
            MilestoneComponent(
                name="Label-order / prompt-validation reserve",
                component_type=MilestoneComponentType.LABEL_ORDER_RESERVE,
                item_count=50,
                prompt_modes=CORE_PROMPT_MODES,
                role="predefined reserve, not exploratory effect chasing",
            ),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            per_model_mode_validity_min=0.90,
            positive_gap_models_min=4,
            positive_surplus_models_min=4,
            low_diffuse_gap_min=0.10,
            low_diffuse_surplus_min=0.10,
            positive_sampling_models_min=3,
            require_low_diffuse_gt_high_consensus=True,
            require_low_diffuse_surplus_gt_high_consensus=True,
            require_paraphrase_preserves_direction=True,
        ),
        normative_certainty_allowed=True,
        use_as_confirmatory=True,
    ),
    CallMilestone(
        name="50k",
        planned_call_budget=47500,
        role="preferred full reduced first-paper study",
        components=(
            _core(2000, BinAllocation(350, 400, 750, 500)),
            _repeated(400, 10, BinAllocation(70, 80, 150, 100)),
            _paraphrase(250, BinAllocation(40, 50, 100, 60)),
            MilestoneComponent(
                name="Optional normative-certainty subset",
                component_type=MilestoneComponentType.NORMATIVE_CERTAINTY,
                item_count=1000,
                prompt_modes=(PromptMode.NORMATIVE_VERDICT,),
                bin_allocation=BinAllocation(160, 200, 380, 260),
                role="secondary endpoint",
            ),
        ),
        continue_thresholds=MilestoneThresholds(
            overall_validity_min=0.95,
            per_model_mode_validity_min=0.90,
            positive_gap_models_min=4,
            positive_surplus_models_min=4,
            low_diffuse_gap_min=0.10,
            low_diffuse_surplus_min=0.10,
            positive_sampling_models_min=3,
            require_low_diffuse_gt_high_consensus=True,
            require_low_diffuse_surplus_gt_high_consensus=True,
            require_paraphrase_preserves_direction=True,
        ),
        normative_certainty_allowed=True,
        use_as_confirmatory=True,
    ),
)

CALL_MILESTONE_BY_NAME = {milestone.name: milestone for milestone in CALL_MILESTONES}


def get_call_milestone(name: str) -> CallMilestone:
    try:
        return CALL_MILESTONE_BY_NAME[name]
    except KeyError as exc:
        raise ValueError(f"unknown call milestone {name!r}; expected one of {tuple(CALL_MILESTONE_BY_NAME)}") from exc


def call_milestone_payload() -> list[dict[str, Any]]:
    return [milestone.to_dict() for milestone in CALL_MILESTONES]
