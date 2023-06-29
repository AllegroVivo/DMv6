from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from ...core.objects.room   import DMRoom
from utilities              import *

if TYPE_CHECKING:
    from ...core    import DMGame
################################################################################

__all__ = ("EmptyRoom",)

################################################################################
class EmptyRoom(DMRoom):

    def __init__(self, game: DMGame, position: Vector2):

        super().__init__(
            game, position,
            _id="ROOM-000",
            name="Empty",
            description="There's... nothing here...",
            rank=0,
            unlock=None
        )

################################################################################
