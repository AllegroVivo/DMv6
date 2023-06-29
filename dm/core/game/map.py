from __future__ import annotations

from pygame import Surface, Vector2
from typing import TYPE_CHECKING, List, Optional, Type, Union

from utilities import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from dm.core.objects.room import DMRoom
    from dm.rooms.special.Empty import EmptyRoom
################################################################################

__all__ = ("DMDungeonMap", "DMMapRow")

################################################################################
class DMMapRow:

    __slots__ = (
        "_state",
        "_rooms",
        "_idx",
    )

################################################################################
    def __init__(self, state: DMGame, index: int):

        self._state: DMGame = state

        self._idx: int = index
        self._rooms: List[DMRoom] = []

        self._init_row()

################################################################################
    def _init_row(self):

        empty: Type[EmptyRoom] = self._state.spawn.room(obj_id="ROOM-000", init_obj=False)  # type: ignore
        for col in range(6):
            if col in {0, 5}:
                room = None
            else:
                room = empty(self._state, position=Vector2(col, self._idx))
            self._rooms.append(room)

################################################################################
    def __getitem__(self, idx: int) -> DMRoom:

        return self._rooms[idx]

################################################################################
    def draw(self, surface: Surface):

        for room in self._rooms:
            if room is not None:
                room.draw(surface)

################################################################################
class DMDungeonMap:

    __slots__ = (
        "_state",
        "_rows",
        "_highlighting",
    )

################################################################################
    def __init__(self, state: DMGame):

        self._state: DMGame = state
        self._rows: List[DMMapRow] = []

        self._init_map()

################################################################################
    def __getitem__(self, idx: int) -> DMMapRow:

        if not isinstance(idx, int):
            raise TypeError(f"Invalid index type: {type(idx)}")

        return self._rows[idx]

################################################################################
    @property
    def game(self) -> DMGame:

        return self._state

################################################################################
    def _init_map(self):

        for row in range(3):
            self._rows.append(DMMapRow(self._state, row))

        # Add in the special starter rooms. Definitely need a more modular way.
        self.deploy(self._state.spawn.room(obj_id="BOSS-000", position=Vector2(0, 1)), Vector2(0, 1))  # Boss Tile
        self.deploy(self._state.spawn.room(obj_id="ROOM-101", position=Vector2(3, 1)), Vector2(3, 1))  # Battle Room
        self.deploy(self._state.spawn.room(obj_id="ENTR-000", position=Vector2(5, 1)), Vector2(5, 1))  # Entrance Tile

################################################################################
    def deploy(self, room: DMRoom, position: Vector2):

        self._rows[int(position.y)]._rooms[int(position.x)] = room

################################################################################
    def draw(self, surface: Surface):

        for row in self._rows:
            for room in row:
                if room is not None:
                    room.draw(surface)

################################################################################
