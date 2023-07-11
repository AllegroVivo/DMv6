from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game    import DMGame
################################################################################

__all__ = ("GoblinGirl",)

################################################################################
class GoblinGirl(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):
        super().__init__(
            game, start_cell,
            _id="MON-118",
            name="Goblin Girl",
            life=80,
            atk=17,
            defense=7,
            rank=3,
        )

################################################################################
