from __future__ import annotations

import pygame

from pygame     import Rect, Surface, Vector2
from typing     import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar

from ._animator  import AnimatorComponent
from ._graphical    import GraphicalComponent
from utilities      import *

if TYPE_CHECKING:
    from dm.core.objects.object    import DMObject
    from dm.core.objects.unit import DMUnit
################################################################################

__all__ = ("UnitGraphical",)

UG = TypeVar("UG", bound="UnitGraphical")

################################################################################
class UnitGraphical(GraphicalComponent):

    __slots__ = (
        "_mover",
        "_attack",
        "_animator",
        "_spritesheet",
        "_frame_count",
        "_frame_size",
        "_attack_timer",
        "_attacking",
    )

################################################################################
    def __init__(self, parent: DMObject, frame_count: int):

        super().__init__(parent)

        self._attack: Optional[Surface] = None
        self._spritesheet: Optional[Surface] = None

        self._frame_count: int = frame_count
        self._frame_size: Optional[Tuple[int, int]] = None

        self._animator: Optional[AnimatorComponent] = AnimatorComponent(self)

        self._attacking: bool = False
        self._attack_timer: float = 0.30

        self._load_sprites()

################################################################################
    def _load_sprites(self) -> None:

        if self._attack is None:
            self._attack = pygame.image.load(
                f"assets/sprites/{self.subdir}/{class_to_file_name(self._parent)}/attack.png"
            )
            # Flip the attack sprite for monsters because it's the wrong way. Pfft.
            if self.subdir == "monsters":
                self._attack = pygame.transform.flip(self._attack, True, False)

        if self._zoom is None:
            self._zoom = pygame.image.load(
                f"assets/sprites/{self.subdir}/{class_to_file_name(self._parent)}/zoom.png"
            )
        if self._spritesheet is None:
            self._spritesheet = pygame.image.load(
                f"assets/sprites/{self.subdir}/{class_to_file_name(self._parent)}/idle.png"
            )
            # Flip the idle sprites for monsters because they're the wrong way. Pfft.
            if self.subdir == "monsters":
                self._spritesheet = pygame.transform.flip(self._spritesheet, True, False)

            self._assert_frame_size()
            self._split_spritesheet()

################################################################################
    @property
    def parent(self) -> DMUnit:

        return self._parent  # type: ignore

################################################################################
    @property
    def subdir(self) -> str:

        return "monsters" if self.parent.is_monster() else "heroes"

################################################################################
    @property
    def screen_pos(self) -> Vector2:

        raise NotImplementedError

################################################################################
    def draw(self, screen: Surface) -> None:

        pos_rect = self.current_frame.get_rect(center=self.screen_pos)
        screen.blit(self.current_frame, pos_rect)

################################################################################
    def _assert_frame_size(self) -> None:

        if self._frame_size is None:
            sheet_width, sheet_height = self._spritesheet.get_size()
            self._frame_size = sheet_width // self._frame_count, sheet_height

################################################################################
    def _split_spritesheet(self) -> None:

        frames = []
        for i in range(self._frame_count):
            frame_location = (i * self._frame_size[0], 0)
            frames.append(self._spritesheet.subsurface(Rect(frame_location, self._frame_size)))

        self._animator._frames = frames

################################################################################
    def update(self, dt: float) -> None:

        self._animator.update(dt)

        if self._attacking:
            self._attack_timer -= dt
            if self._attack_timer <= 0:
                self._attacking = False

################################################################################
    @property
    def current_frame(self) -> Surface:

        if self._attacking:
            return self._attack

        return self._animator.current_frame

################################################################################
    @property
    def rect(self) -> Rect:

        return self.current_frame.get_rect()

################################################################################
    def _copy(self, parent: DMObject) -> UnitGraphical:

        new_obj: Type[UG] = super()._copy(parent)  # type: ignore

        new_obj._attack = self._attack.copy()
        new_obj._animator = self._animator._copy(new_obj)
        new_obj._spritesheet = self._spritesheet.copy()

        new_obj._frame_count = self._frame_count
        new_obj._frame_size = self._frame_size

        new_obj._attack_timer = 0.30
        new_obj._attacking = False

        return new_obj

################################################################################
    def play_attack(self) -> None:

        self._attack_timer = 0.50
        self._attacking = True

################################################################################
    def play_death(self) -> None:

        # Implemented in the HeroGraphical class since they're the only ones that
        # have a death sprite.
        pass

################################################################################
