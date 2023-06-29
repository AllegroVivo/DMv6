from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING

from ..battleroom   import DMBattleRoom

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("Battle",)

################################################################################
class Battle(DMBattleRoom):

    def __init__(self, game: DMGame, position: Vector2):

        super().__init__(
            game, position,
            _id="ROOM-101",
            name="Battle",
            description=(
                "Deployed monsters' maximum LIFE is increased by {value}."
            ),
            rank=1
        )

################################################################################
