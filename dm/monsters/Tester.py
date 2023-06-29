from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core    import DMGame
################################################################################

__all__ = ("Tester",)

################################################################################
class Tester(DMMonster):

    def __init__(self, game: DMGame, level: int = 1):

        super().__init__(
            game,
            level,
            _id="MON-XXX",
            name="Tester",
            description="A Snarfblat is upon you!",
            life=1000,
            attack=100,
            defense=1.0,
            rank=1,
            idle_frames=6
        )

################################################################################
