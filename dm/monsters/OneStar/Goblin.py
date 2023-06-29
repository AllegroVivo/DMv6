from __future__ import annotations

from typing     import TYPE_CHECKING

from dm.core.objects.monster import DMMonster

if TYPE_CHECKING:
    from dm.core    import DMGame
################################################################################

__all__ = ("Goblin", )

################################################################################
class Goblin(DMMonster):

    def __init__(self, game: DMGame, level: int = 1):

        super().__init__(
            game,
            level,
            _id="MON-103",
            name="Goblin",
            life=50,
            attack=4,
            defense=1.0,
            rank=1
        )

################################################################################
