from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("Bat",)

################################################################################
class Bat(DMMonster):

    def __init__(self, game: DMGame, level: int = 1):

        super().__init__(
            game,
            level,
            _id="MON-104",
            name="Bat",
            life=40,
            attack=6,
            defense=2.0,
            rank=1,
            idle_frames=6
        )

################################################################################
