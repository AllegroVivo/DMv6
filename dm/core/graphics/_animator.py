from __future__ import annotations

from pygame     import Surface
from typing    import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .unit import UnitGraphical
################################################################################

__all__ = ("AnimatorComponent",)

################################################################################
class AnimatorComponent:

    __slots__ = (
        "_parent",
        "_current_frame",
        "_frames",
        "_cooldown",
        "_frame_count",
        "_frame_size",
    )

################################################################################
    def __init__(self, parent: UnitGraphical):

        self._parent: UnitGraphical = parent

        self._current_frame: int = 0
        self._frames: List[Surface] = []

        self._cooldown: float = 0

        self._load_sprites()

################################################################################
    def _load_sprites(self) -> None:

        self._frames = self._parent._frames

################################################################################
    def update(self, dt: float) -> None:

        self._cooldown += dt

        if self._cooldown >= 0.1:  # Assuming 10 FPS
            self._cooldown = 0
            self._current_frame += 1

            if self._current_frame >= len(self._frames):
                self._current_frame = 0

################################################################################
    @property
    def current_frame(self) -> Surface:

        return self._frames[self._current_frame]

################################################################################
    def draw(self, screen: Surface) -> None:

        screen.blit(self.current_frame, self._parent.rect)

################################################################################
    @staticmethod
    def _copy(parent: UnitGraphical) -> AnimatorComponent:

        return AnimatorComponent(parent)

################################################################################
