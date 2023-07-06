from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.hero import DMHero

if TYPE_CHECKING:
    from dm.core.game.game     import DMGame
################################################################################

__all__ = ("Farmer",)

################################################################################
class Farmer(DMHero):

    def __init__(self, game: DMGame):

        super().__init__(
            state=game,
            _id="HRO-101",
            name="Farmer",
            rank=1,
        )

################################################################################
