from dataclasses    import dataclass
################################################################################

__all__ = (
    "Effect",
    "SkillEffect",
)

################################################################################
@dataclass
class Effect:

    name: str
    base: int
    per_lv: float

################################################################################
@dataclass
class SkillEffect:

    base: int
    scalar: float

################################################################################
