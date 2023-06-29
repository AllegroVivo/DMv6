from __future__ import annotations

import pygame.image

from pygame     import Rect, Surface, Vector2
from typing     import TYPE_CHECKING, Optional, Type, TypeVar

from ._graphical import GraphicalComponent
from utilities   import *

if TYPE_CHECKING:
    from dm.core.objects.room import DMRoom
################################################################################

__all__ = ("DMRoomGraphics",)

RG = TypeVar("RG", bound="RoomGraphics")

################################################################################
class DMRoomGraphics(GraphicalComponent):

    __slots__ = (
        "_rect",
    )

################################################################################
    def __init__(self, parent: DMRoom):

        super().__init__(parent)

        self._rect: Rect = None  # type: ignore

        self._load_sprites()

################################################################################
    def _load_sprites(self) -> None:

        # If we're copying a pre-existing graphical component, we don't need to
        # load the sprites again.
        if self._static is not None:
            return

        self._static = pygame.image.load(
            f"assets/sprites/rooms/{class_to_file_name(self._parent)}.png"
        )

        # Scale the image to fit the room.
        if type(self.parent).__name__ != "BossRoom":
            self._static = pygame.transform.scale(self._static, (ROOM_SIZE - 30, ROOM_SIZE - 30))
        else:
            self._static = pygame.transform.scale(self._static, (ROOM_SIZE + 40, ROOM_SIZE + 25))

        # Flip the entry symbol. Looks better.
        if type(self._parent).__name__ == "EntranceRoom":
            self._static = pygame.transform.flip(self._static, True, False)

################################################################################
    @property
    def parent(self) -> DMRoom:

        return self._parent  # type: ignore

################################################################################
    @property
    def topleft(self) -> Vector2:

        return Vector2(
            self.parent.vector.x * (ROOM_SIZE + GRID_PADDING) + 50,
            self.parent.vector.y * (ROOM_SIZE + GRID_PADDING) + 50
        )

################################################################################
    @property
    def center(self) -> Vector2:

        return Vector2(self._rect.center)

################################################################################
    def calculate_rect(self) -> None:

        self._rect = Rect(self.topleft.x, self.topleft.y, ROOM_SIZE, ROOM_SIZE)

################################################################################
    def draw(self, screen: Surface) -> None:

        self.calculate_rect()
        bg = ROOM_BG if type(self.parent).__name__ != "EntranceRoom" else BLACK
        pygame.draw.rect(screen, bg, self._rect)

        # if self._highlighted:
        #     pygame.draw.rect(screen, RED, self._rect, BORDER_THICKNESS)

        idle_rect = self._static.get_rect(center=self.center)
        screen.blit(self._static, idle_rect)

################################################################################
    def _copy(self, parent: DMRoom) -> DMRoomGraphics:

        new_obj: Type[RG] = super()._copy(parent)  # type: ignore

        new_obj._rect = self._rect.copy() if self._rect is not None else None

        return new_obj

################################################################################
