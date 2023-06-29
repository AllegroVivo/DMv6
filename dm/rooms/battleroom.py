from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, List, Optional, Type, TypeVar

from dm.core.objects.room import DMRoom
from utilities      import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("DMBattleRoom",)

BR = TypeVar("BR", bound="DMBattleRoom")

################################################################################
class DMBattleRoom(DMRoom):

    __slots__ = (

    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        position: Vector2,
        *,
        _id: str,
        name: str,
        description: str,
        rank: int,
        unlock: Optional[UnlockPack] = None,
    ):

        super().__init__(state, position, _id, name, description, rank, unlock)

################################################################################
    @staticmethod
    def is_battle_room() -> bool:

        return True

################################################################################
    def _copy(self, **kwargs) -> DMBattleRoom:

        new_obj: Type[BR] = super()._copy(**kwargs)  # type: ignore

        return new_obj  # type: ignore

################################################################################
