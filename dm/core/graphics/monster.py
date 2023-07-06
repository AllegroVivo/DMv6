from __future__ import annotations

import pygame

from pygame     import Rect, Surface
from typing     import TYPE_CHECKING, Optional, Tuple, Type, TypeVar

from ._animator  import AnimatorComponent
from .unit    import UnitGraphical
from utilities      import *

if TYPE_CHECKING:
    from dm.core.objects.object    import DMObject
    from dm.core.game.game         import DMGame
    from dm.core.objects.monster      import DMMonster
################################################################################

__all__ = ("MonsterGraphical",)

MG = TypeVar("MG", bound="MonsterGraphical")

################################################################################
class MonsterGraphical(UnitGraphical):

    __slots__ = (

    )

################################################################################
    def __init__(self, parent: DMObject, frame_count: int = 5):

        super().__init__(parent, frame_count)

################################################################################
    @property
    def screen_pos(self) -> Tuple[int, int]:

        parent_room = self.parent.room  # type: ignore
        room_x, room_y = parent_room._graphics.topleft
        # If there are no monsters in the room, the spacing will be 0
        # but that doesn't matter because there are no monsters to draw.
        monster_spacing = ROOM_SIZE / (len(parent_room.monsters) + 1)

        index = self.parent.room.monsters.index(self.parent)  # type: ignore

        monster_x = room_x + 25
        monster_y = room_y + monster_spacing * (index + 1)

        return monster_x, monster_y

################################################################################
    def _copy(self, parent: DMMonster) -> MonsterGraphical:

        new_obj: Type[MG] = super()._copy(parent)  # type: ignore

        return new_obj

################################################################################
