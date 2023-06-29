from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...core.game.game import DMGame
    from ...core.objects.unit import DMUnit
################################################################################

__all__ = ("MovementComponent",)

################################################################################
class MovementComponent:

    __slots__ = (
        "_parent",
        "_screen_pos",
        "_direction",
        "_target_pos",
    )

################################################################################
    def __init__(self, parent: DMUnit):

        self._parent: DMUnit = parent

        self._screen_pos = None
        self._direction = None
        self._target_pos = None

################################################################################
    @property
    def game(self) -> DMGame:

        return self._parent.game

################################################################################
    def update(self, dt: float) -> None:

        if self._parent._moving:
            self.move(dt)

################################################################################
    def move(self, dt: float) -> None:

        if self.screen_position is None:
            self._parent._screen_pos = self.game.dungeon.entrance.center

        if self._direction is None:
            return
        if self._direction.x != 0:
            self._parent._screen_pos.x += self._direction.x * HERO_SPEED * dt
        elif self._direction.y != 0:
            self._parent._screen_pos.y += self._direction.y * HERO_SPEED * dt

        if self.arrived_at_target():
            self.cancel_movement()
            self.arrived_in_cell()

################################################################################
