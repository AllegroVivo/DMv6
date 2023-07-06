from __future__ import annotations

from pygame     import Vector2
from typing import TYPE_CHECKING, Optional, Type, TypeVar

from utilities import *

if TYPE_CHECKING:
    from ...core.game.game import DMGame
    from ...core.objects.unit import DMUnit
    from ...core.objects.room import DMRoom
################################################################################

__all__ = ("MovementComponent",)

MC = TypeVar("MC", bound="MovementComponent")

################################################################################
class MovementComponent:

    __slots__ = (
        "_parent",
        "_screen_pos",
        "_direction",
        "_target_pos",
        "_moving",
        "_move_cooldown",
        "_death_timer",
        "_death_start",
        "_death_end",
    )

    DIRECTIONS = [Vector2(-1, 0), Vector2(1, 0), Vector2(0, -1), Vector2(0, 1)]
    DEATH_TIME = 2.0  # Time in seconds to show the death sprite
    DEATH_HEIGHT = 50  # Height of the death arc in pixels

################################################################################
    def __init__(self, parent: DMUnit):

        self._parent: DMUnit = parent

        self._screen_pos: Vector2 = None  # type: ignore
        self._direction: Optional[Vector2] = Vector2(-1, 0)  # Moving left from the entrance into the dungeon.
        self._target_pos: Optional[Vector2] = None

        self._death_timer: Optional[float] = None
        self._death_start: Optional[Vector2] = None
        self._death_end: Optional[Vector2] = None

        self._moving: bool = True
        self._move_cooldown: float = 0

################################################################################
    @property
    def game(self) -> DMGame:

        return self._parent.game

################################################################################
    @property
    def room(self) -> DMRoom:

        return self._parent.room

################################################################################
    @property
    def screen_pos(self) -> Vector2:

        if self._screen_pos is None:
            self._screen_pos = self.game.dungeon.entrance_tile.center
            # Only one valid adjacent tile when at the entrance. (Kinda hacky...)
            target_room = self.game.dungeon.entrance_tile.adjacent_rooms[0]
            self._target_pos = target_room.center

        return self._screen_pos

################################################################################
    @property
    def moving(self) -> bool:

        return self._moving

################################################################################
    @property
    def dying(self) -> bool:

        return self._death_timer is not None

################################################################################
    def update(self, dt: float) -> None:

        if self.dying:
            self.update_death(dt)
        if self.moving:
            self.update_movement(dt)

################################################################################
    def update_movement(self, dt: float) -> None:

        if self._move_cooldown > 0:
            self._move_cooldown -= dt
            return
        self.move(dt)

################################################################################
    def update_death(self, dt: float) -> None:

        print(f"Before: {self._screen_pos}")
        self._death_timer += dt
        t = self._death_timer / self.DEATH_TIME
        if t > 1:
            self.finish_death()
        else:
            # Update position based on a parabolic function
            self._screen_pos.x = lerp(self._death_start.x, self._death_end.x, t)
            self._screen_pos.y = self._death_start.y - self.DEATH_HEIGHT * (4 * t * (1 - t))
            print(f"After: {self._screen_pos}")

################################################################################
    def move(self, dt: float) -> None:

        if self._direction is None:
            self.choose_direction()

        if self._direction.x != 0:
            self.screen_pos.x += self._direction.x * HERO_SPEED * dt
        elif self._direction.y != 0:
            self.screen_pos.y += self._direction.y * HERO_SPEED * dt

        current_grid_pos = pixel_to_grid(self.screen_pos)
        if self.room != self.game.get_room_at(current_grid_pos):
            self._parent.set_room(current_grid_pos)

        if self.arrived_at_target():
            self.stop_movement()
            # self.sync_screen_pos()
            self.check_for_encounter()

################################################################################
    def check_for_encounter(self) -> None:

        self._parent.check_for_encounter()

################################################################################
    def sync_screen_pos(self) -> None:

        self._screen_pos = self._target_pos
        self._target_pos = None

################################################################################
    def start_movement(self) -> None:

        self.set_target_pos()
        self._moving = True

################################################################################
    def stop_movement(self) -> None:

        self._moving = False
        self._direction = None
        self._move_cooldown = 0.2

################################################################################
    def play_death(self) -> None:

        self._death_timer = 0
        self._death_start = self.screen_pos

        death_direction = 1 if self._parent.is_hero() else -1
        self._death_end = self.screen_pos + Vector2(100 * death_direction, 0)

################################################################################
    def finish_death(self) -> None:

        self._death_timer = None
        self._death_start = None
        self._death_end = None

################################################################################
    def set_target_pos(self) -> None:

        if self._direction is None:
            self.choose_direction()

        target_room = self.game.get_room_at(self.room.grid_pos + self._direction)
        if target_room is None:
            self.choose_direction()
            self.set_target_pos()
        else:
            self._target_pos = target_room.center

################################################################################
    def choose_direction(self) -> None:

        self._direction = self._parent.random.choice(self.DIRECTIONS)
        target_room = self.game.get_room_at(self.room.grid_pos + self._direction)
        if target_room is None or target_room.is_entrance:
            self.choose_direction()

################################################################################
    def arrived_at_target(self) -> bool:

        if self._direction is None or self._target_pos is None:
            return False

        return self.screen_pos.distance_to(self._target_pos) <= EPSILON

################################################################################
    def _copy(self, parent: DMUnit) -> MovementComponent:

        cls: Type[MC] = type(self)
        new_obj = cls.__new__(cls)

        new_obj._parent = parent

        new_obj._screen_pos = None
        new_obj._direction = Vector2(-1, 0)
        new_obj._moving = True
        new_obj._target_pos = None
        new_obj._move_cooldown = 0

        new_obj._death_timer = None
        new_obj._death_start = None
        new_obj._death_end = None

        return new_obj

################################################################################
