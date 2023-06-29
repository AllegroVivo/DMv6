from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from ...rooms.battleroom    import DMBattleRoom
from utilities              import *

if TYPE_CHECKING:
    from ...core.game.game    import DMGame
################################################################################

__all__ = ("BossRoom",)

################################################################################
class BossRoom(DMBattleRoom):

    __slots__ = (
    )

################################################################################
    def __init__(self, game: DMGame, position: Vector2):

        super().__init__(
            game, position,
            _id="BOSS-000",
            name="Boss Chamber",
            description="The Dungeon Boss awaits the intruders...",
            rank=0,
            unlock=None
        )

################################################################################
    @staticmethod
    def is_boss_room() -> bool:

        return True

################################################################################
