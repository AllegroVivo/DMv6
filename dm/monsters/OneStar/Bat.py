from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("Bat",)

################################################################################
class Bat(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):

        super().__init__(
            game, start_cell,
            _id="MON-104",
            name="Bat",
            rank=1,
            anim_frames=6,
            life=40,
            atk=6,
            defense=2.0
        )

################################################################################
