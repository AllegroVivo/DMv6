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
    from dm.core.objects.hero         import DMHero
################################################################################

__all__ = ("HeroGraphical",)

HG = TypeVar("HG", bound="HeroGraphical")

################################################################################
class HeroGraphical(UnitGraphical):

    __slots__ = (
        "_death",
    )

################################################################################
    def __init__(self, parent: DMHero, frame_count: int = 5):

        # Instantiate this first so it's present when we call `_load_sprites` in the parent.
        self._death: Optional[Surface] = None

        super().__init__(parent, frame_count)

################################################################################
    def _load_sprites(self) -> None:

        super()._load_sprites()

        if self._death is None:
            self._death = pygame.image.load(
                f"assets/sprites/heroes/{class_to_file_name(self._parent)}/death.png"
            )

################################################################################
    def _init_screen_pos(self) -> None:

        self.parent.set_screen_pos(self.room.center.copy())

################################################################################
    @property
    def current_frame(self) -> Surface:

        if self._mover.dying:
            return self._death

        return super().current_frame

################################################################################
    def assume_attack_position(self) -> None:

        if self.parent.engaged:
            position = Vector2(self.parent._opponent.screen_pos)
            position.x += (self.parent._opponent._graphics.current_frame.get_width() / 2) + 5
            self._screen_pos = position

################################################################################
    def _copy(self, parent: DMMonster) -> HeroGraphical:

        new_obj: Type[HG] = super()._copy(parent)  # type: ignore

        new_obj._death = self._death.copy()

        return new_obj

################################################################################
