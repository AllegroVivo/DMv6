from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game    import DMGame
################################################################################

__all__ = ("LizardmanGirl",)

################################################################################
class LizardmanGirl(DMMonster):

    def __init__(self, game: DMGame, start_cell: Optional[Vector2] = None):

        super().__init__(
            game, start_cell,
            _id="MON-125",
            name="Lizardman Girl",
            life=110,
            atk=15,
            defense=6.5,
            rank=3,
        )

################################################################################
