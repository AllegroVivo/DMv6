from __future__ import annotations

from pygame     import Surface, Vector2
from typing     import (
    TYPE_CHECKING,
    List,
    Optional,
    Type,
    TypeVar,
    Union
)

from ...core.objects.object import DMObject
from ..graphics.unit import UnitGraphical
from ..graphics.movement import MovementComponent
from ...core.objects.room import DMRoom
from ..game.stats import UnitStats
from utilities              import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("DMUnit",)

U = TypeVar("U", bound="DMUnit")

################################################################################
class DMUnit(DMObject):

    __slots__ = (
        "_stats",
        "_graphics",
        "_room",
        "_mover",
        "_opponent",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        _id: str,
        name: str,
        description: Optional[str],
        graphics: UnitGraphical,
        stats: UnitStats,
        rank: int = 0,
        start_cell: Optional[Vector2] = None
    ):

        super().__init__(state, _id, name, description, rank)

        self._room: Optional[Vector2] = start_cell or Vector2(-1, -1)

        self._stats: UnitStats = stats

        self._graphics: UnitGraphical = graphics
        self._mover: Optional[MovementComponent] = None

        self._opponent: Optional[DMUnit] = None

        if self.is_hero():
            self._mover = MovementComponent(self)

################################################################################
    @property
    def room(self) -> DMRoom:

        if self._room is None:
            if self.is_hero():
                self._room = self.game.dungeon.entrance_tile.grid_pos

        return self.game.get_room_at(self._room)

################################################################################
    @property
    def graphics(self) -> UnitGraphical:

        return self._graphics

################################################################################
    @property
    def screen_pos(self) -> Vector2:

        if self._mover is not None:
            return self._mover.screen_pos

        return self._graphics.screen_pos

################################################################################
    @property
    def moving(self) -> bool:

        return self._mover.moving

################################################################################
    def draw(self, screen: Surface) -> None:

        self._graphics.draw(screen)

################################################################################
    def update(self, dt: float) -> None:

        if self._mover:
            self._mover.update(dt)

        self._graphics.update(dt)

################################################################################
    def check_for_encounter(self) -> None:

        self._opponent = self.room.try_to_engage(self)
        if not self._opponent:
            self._mover.start_movement()

################################################################################
    def _copy(self, **kwargs) -> DMUnit:

        new_obj: Type[U] = super()._copy()  # type: ignore

        new_obj._room = kwargs.pop("room")

        new_obj._graphics = self._graphics._copy(new_obj)
        new_obj._mover = self._mover._copy(new_obj) if self._mover else None
        new_obj._stats = self._stats._copy()

        new_obj._opponent = None

        return new_obj

################################################################################
    @staticmethod
    def is_monster() -> bool:

        return False

################################################################################
    @staticmethod
    def is_hero() -> bool:

        return False

################################################################################
    @property
    def is_alive(self) -> bool:

        return self.life > 0

################################################################################
    @property
    def life(self) -> int:

        return self._stats.life

################################################################################
    @property
    def max_life(self) -> int:

        return self._stats.max_life

################################################################################
    @property
    def attack(self) -> int:

        return self._stats.attack

################################################################################
    @property
    def defense(self) -> float:

        return self._stats.defense

################################################################################
    @property
    def dex(self) -> float:

        return self._stats.dex

################################################################################
    @property
    def combat(self) -> float:

        return self._stats.combat

################################################################################
    @property
    def num_attacks(self) -> int:

        return self._stats.num_attacks

################################################################################
    @property
    def move_speed(self) -> float:

        return self._stats.move_speed

################################################################################
    @property
    def engaged(self) -> bool:

        return self._opponent is not None

################################################################################
    def set_room(self, position: Union[Vector2, DMRoom]) -> None:

        if isinstance(position, DMRoom):
            position = position.grid_pos

        self._room = position

################################################################################
    def after_battle(self) -> None:

        # We attempt to reengage a monster in the room instead of moving
        # to a new room at a 15% chance.
        if self.random.chance(15):
            self.check_for_encounter()
        else:
            self.start_movement()

################################################################################
    def start_movement(self) -> None:

        self._mover.start_movement()

################################################################################
    def damage(self, amount: int) -> None:

        print(f"{self.name} took {amount} damage!")
        self._stats.damage(amount)

################################################################################
    def heal(self, amount: int) -> None:

        self._stats.heal(amount)

################################################################################
    def after_disengage(self) -> None:

        self._opponent = None

        if self.random.chance(20):
            print(f"{self.name} is checking for encounter.")
            self.check_for_encounter()
        else:
            print(f"{self.name} is moving.")
            self.start_movement()

################################################################################
    def play_attack_animation(self) -> None:

        self._graphics.play_attack()

################################################################################
