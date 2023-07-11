from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game    import DMGame
################################################################################

__all__ = ("DarkSlime",)

################################################################################
class DarkSlime(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):

        super().__init__(
            game, start_cell,
            _id="MON-105",
            name="Dark Slime",
            life=90,
            atk=11,
            defense=4.0,
            rank=2,
            anim_frames=6
        )

################################################################################
