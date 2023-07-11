from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game    import DMGame
################################################################################

__all__ = ("OrcGirl",)

################################################################################
class OrcGirl(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):

        super().__init__(
            game, start_cell,
            _id="MON-117",
            name="Orc Girl",
            life=90,
            atk=16,
            defense=7,
            rank=3,
        )

################################################################################
