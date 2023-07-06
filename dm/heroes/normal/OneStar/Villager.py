from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.hero import DMHero

if TYPE_CHECKING:
    from dm.core.game.game     import DMGame
################################################################################

__all__ = ("Villager",)

################################################################################
class Villager(DMHero):

    def __init__(self, game: DMGame):

        super().__init__(
            state=game,
            _id="HRO-102",
            name="Villager",
            rank=1,
        )

################################################################################
