from __future__ import annotations

import pygame

from pygame     import Rect, Surface
from typing     import TYPE_CHECKING, Optional, Tuple, Type, TypeVar

from ._animator  import AnimatorComponent
from ._graphical    import GraphicalComponent
from utilities      import *

if TYPE_CHECKING:
    from dm.core.objects.object    import DMObject
    from dm.core.game.game         import DMGame
################################################################################

__all__ = ("UnitGraphical",)

UG = TypeVar("UG", bound="UnitGraphical")

################################################################################
class UnitGraphical(GraphicalComponent):

    __slots__ = (
        "_attack",
        "_animator",
        "_spritesheet",
        "_frame_count",
        "_frame_size",
        "_frames",
    )

################################################################################
    def __init__(self, parent: DMObject):

        super().__init__(parent)

        self._attack: Optional[Surface] = None
        self._animator: Optional[AnimatorComponent] = AnimatorComponent(self)
        self._spritesheet: Optional[Surface] = None

        self._load_sprites()

################################################################################
    def _load_sprites(self) -> None:

        if self._attack is None:
            self._attack = pygame.image.load(
                f"assets/sprites/monsters/{class_to_file_name(self._parent)}/attack.png"
            )
        if self._spritesheet is None:
            self._spritesheet = pygame.image.load(
                f"assets/sprites/monsters/{class_to_file_name(self._parent)}/idle.png"
            )

            self._assert_frame_size()
            self._split_spritesheet()

################################################################################
    def _assert_frame_size(self) -> None:

        if self._frame_size is None:
            sheet_width, sheet_height = self._spritesheet.get_size()
            self._frame_size = sheet_width // self._frame_count, sheet_height

################################################################################
    def _split_spritesheet(self) -> None:

        self._frames = []
        for i in range(self._frame_count):
            frame_location = (i * self._frame_size[0], 0)
            self._frames.append(self._spritesheet.subsurface(Rect(frame_location, self._frame_size)))

################################################################################
    def draw(self, screen: Surface) -> None:

        screen.blit(self.current_frame, (100, 100))

################################################################################
    def update(self, dt: float) -> None:

        self._animator.update(dt)

################################################################################
    def monster_topleft(self) -> Tuple[int, int]:

        parent_room = self.parent.room  # type: ignore
        room_x, room_y = parent_room._graphics.topleft
        monster_spacing = ROOM_SIZE / (len(parent_room.monsters) + 1)

        index = parent_room.monsters.index(self.parent)  # type: ignore

        monster_x = room_x
        monster_y = room_y - 20 + monster_spacing * (index + 1)

        return monster_x, monster_y

################################################################################
    @property
    def current_frame(self) -> Surface:

        return self._animator.current_frame

################################################################################
    def _copy(self, parent: DMObject) -> UnitGraphical:

        new_obj: Type[UG] = super()._copy(parent)  # type: ignore

        new_obj._attack = self._attack.copy()
        new_obj._animator = self._animator._copy(new_obj)
        new_obj._spritesheet = self._spritesheet.copy()

        return new_obj

################################################################################
