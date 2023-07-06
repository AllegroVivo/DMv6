from __future__ import annotations

from pygame     import Rect, Surface, Vector2
from typing     import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union
)

from ..graphics.room import DMRoomGraphics
from .object import DMObject
from utilities  import *

if TYPE_CHECKING:
    from ..game.game import DMGame
    from ..objects.monster import DMMonster
    from ..objects.unit import DMUnit
################################################################################

__all__ = ("DMRoom",)

R = TypeVar("R", bound="DMRoom")

################################################################################
class DMRoom(DMObject):
    """The base class for all rooms in the game.

    Attributes:
    -----------

    Properties:
    -----------

    Methods:
    --------
    _copy(**kwargs) -> :class:`DMRoom`
        Returns a clean copy of the current room type with any given
        kwargs substituted in.

    is_battle_room() -> bool
        Returns True if the room is a battle room, False otherwise.

    is_trap_room() -> bool
        Returns True if the room is a trap room, False otherwise.

    is_facility_room() -> bool
        Returns True if the room is a facility room, False otherwise.
    """

    __slots__ = (
        "_grid_pos",
        "_graphics",
        "_monsters",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        position: Vector2,
        _id: str,
        name: str,
        description: str,
        rank: int
    ):

        super().__init__(state, _id, name, description, rank)

        self._graphics: DMRoomGraphics = DMRoomGraphics(self)
        self._grid_pos: Vector2 = position
        self._monsters: List[DMMonster] = []

################################################################################
    @property
    def vector(self) -> Vector2:

        return self._grid_pos

################################################################################
    @property
    def topleft(self) -> Vector2:

        return self._graphics.topleft

################################################################################
    @property
    def center(self) -> Vector2:

        return self._graphics.center

################################################################################
    def _copy(self, **kwargs) -> DMRoom:
        """Returns a clean copy of the current room type with any given
        kwargs substituted in.

        All parameters are optional.

        Parameters:
        -----------


        Returns:
        --------
        :class:`DMRoom`
            A fresh copy of the current DMRoom with values substituted as defined.

        """

        new_obj: Type[R] = super()._copy()  # type: ignore

        new_obj._grid_pos = kwargs.get("position", self._grid_pos)
        new_obj._graphics = self._graphics._copy(new_obj)
        new_obj._monsters = []

        return new_obj

################################################################################
    @property
    def grid_pos(self) -> Vector2:

        return self._grid_pos

################################################################################
    @property
    def monsters(self) -> List[DMMonster]:

        return self._monsters

################################################################################
    @property
    def is_battle_room(self) -> bool:
        """Returns True if the room is a battle room, False otherwise."""

        return False

################################################################################
    @property
    def is_trap(self) -> bool:
        """Returns True if the room is a trap room, False otherwise."""

        return False

################################################################################
    @property
    def is_facility(self) -> bool:
        """Returns True if the room is a facility room, False otherwise."""

        return False

################################################################################
    @property
    def is_boss(self) -> bool:

        return False

################################################################################
    @property
    def is_entrance(self) -> bool:

        return False

################################################################################
    @property
    def is_empty(self) -> bool:

        return True

################################################################################
    def draw(self, screen: Surface) -> None:
        """Draws the room to the screen.

        Parameters:
        -----------
        screen : :class:`pygame.Surface`
            The screen to draw to.
        """

        self._graphics.draw(screen)

################################################################################
    def deploy(self, monster: DMMonster) -> None:

        if len(self._monsters) >= 3:
            raise ValueError("Room is full.")

        self._monsters.append(monster)
        monster._room = self._grid_pos

################################################################################
    @property
    def adjacent_rooms(self) -> List[DMRoom]:

        return self._state.dungeon._map.get_adjacent_rooms(
            self.grid_pos, True, True, True, True, False, False
        )

################################################################################
    def try_to_engage(self, unit: DMUnit) -> Optional[DMUnit]:

        if len(self.monsters) == 0:
            return

        for monster in self.monsters:
            if monster.is_alive:
                self.game.battle_manager.engage(monster, unit)
                return monster

################################################################################
