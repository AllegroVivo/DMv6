from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core.game.game    import DMGame
################################################################################

__all__ = ("Slime", )

################################################################################
class Slime(DMMonster):

    def __init__(self, game: DMGame, level: int = 1):

        super().__init__(
            game,
            level,
            _id="MON-101",
            name="Slime",
            life=50,
            attack=5,
            defense=2.0,
            rank=1,
            idle_frames=6
        )

################################################################################
