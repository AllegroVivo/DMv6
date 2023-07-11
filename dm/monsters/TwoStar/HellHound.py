from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core    import DMGame
################################################################################

__all__ = ("HellHound",)

################################################################################
class HellHound(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):

        super().__init__(
            game, start_cell,
            _id="MON-112",
            name="Hell Hound",
            life=80,
            atk=10,
            defense=4.0,
            rank=2,
            anim_frames=4
        )

################################################################################
