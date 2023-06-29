from __future__ import annotations

from pygame     import Vector2
from typing     import TYPE_CHECKING, Optional

from ...core.objects.room   import DMRoom
from utilities              import *

if TYPE_CHECKING:
    from ...core    import DMGame
################################################################################

__all__ = ("EntranceRoom",)

################################################################################
class EntranceRoom(DMRoom):

    def __init__(self, game: DMGame, position: Vector2):

        super().__init__(
            game, position,
            _id="ENTR-000",
            name="Entrance",
            description="An entryway into to the dungeon.",
            rank=0,
            unlock=None
        )

################################################################################
    @staticmethod
    def is_entry_room() -> bool:

        return True

################################################################################
