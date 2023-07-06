from __future__ import annotations

from pygame     import Surface, Vector2
from typing     import (
    TYPE_CHECKING,
    Optional,
    Type,
    TypeVar,
)

from .unit import DMUnit
from ..graphics.monster import MonsterGraphical
from dm.core.game.stats import UnitStats

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("DMMonster",)

M = TypeVar("M", bound="DMMonster")

################################################################################
class DMMonster(DMUnit):

    __slots__ = (

    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        start_cell: Optional[Vector2],
        *,
        _id: str,
        name: str,
        life: int,
        atk: int,
        defense: float,
        description: Optional[str] = None,
        rank: int = 0,
        anim_frames: int = 5
    ):

        super().__init__(
            state=state,
            _id=_id,
            name=name,
            description=description,
            graphics=MonsterGraphical(self, anim_frames),
            rank=rank,
            start_cell=start_cell,
            stats=UnitStats(life, atk, defense)
        )

################################################################################
    def _copy(self, **kwargs) -> DMMonster:

        new_obj: Type[M] = super()._copy(**kwargs)  # type: ignore

        return new_obj

################################################################################
    @staticmethod
    def is_monster() -> bool:

        return True

################################################################################
