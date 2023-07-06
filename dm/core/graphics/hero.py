from __future__ import annotations

import pygame

from pygame     import Rect, Surface, Vector2
from typing     import TYPE_CHECKING, Optional, Tuple, Type, TypeVar

from ._animator  import AnimatorComponent
from .unit    import UnitGraphical
from utilities      import *

if TYPE_CHECKING:
    from dm.core.objects.object    import DMObject
    from dm.core.game.game         import DMGame
    from dm.core.objects.monster      import DMMonster
################################################################################

__all__ = ("HeroGraphical",)

HG = TypeVar("HG", bound="HeroGraphical")

################################################################################
class HeroGraphical(UnitGraphical):

    __slots__ = (

    )

################################################################################
    def __init__(self, parent: DMObject, frame_count: int = 5):

        super().__init__(parent, frame_count)

################################################################################
    @property
    def screen_pos(self) -> Vector2:

        position = self.parent.screen_pos
        if self.parent.engaged:
            position = Vector2(self.parent._opponent.screen_pos)
            position.x += 80
            position.y += 20

        return position

################################################################################
    def draw(self, screen: Surface) -> None:

        if not self._attacking:
            pos_rect = self.current_frame.get_rect(center=self.screen_pos)
            screen.blit(self.current_frame, pos_rect)
        else:
            pos_rect = self._attack.get_rect(center=self.screen_pos)
            screen.blit(self._attack, pos_rect)

################################################################################
    def _copy(self, parent: DMMonster) -> HeroGraphical:

        new_obj: Type[HG] = super()._copy(parent)  # type: ignore
        return new_obj

################################################################################
