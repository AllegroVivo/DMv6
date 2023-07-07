from __future__ import annotations

from pygame import Surface, Vector2
from typing import TYPE_CHECKING, List, Optional, Type, Union

from utilities import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from dm.core.objects.room import DMRoom
    from dm.rooms.special.Empty import EmptyRoom
    from dm.core.objects.monster import DMMonster
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

        EmptyRm: Type[EmptyRoom] = self._state.spawn.room(obj_id="ROOM-000", init_obj=False)  # type: ignore
        for col in range(6):
            if col in {0, 5}:
                room = None
            else:
                room = EmptyRm(self._state, position=Vector2(col, self._idx))
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

################################################################################
    def __getitem__(self, idx: int) -> DMMapRow:

        if not isinstance(idx, int):
            raise TypeError(f"Invalid index type: {type(idx)}")

        return self._rows[idx - 1]

################################################################################
    @property
    def game(self) -> DMGame:

        return self._state

################################################################################
    @property
    def deployed_monsters(self) -> List[DMMonster]:

        ret = []
        for row in self._rows:
            for room in row._rooms:
                if room is not None:
                    ret.extend(room.monsters)

        return ret

################################################################################
    def _init_map(self):

        for row in range(3):
            self._rows.append(DMMapRow(self._state, row))

        # Add in the special starter rooms. Definitely need a more modular way.
        self.deploy(self._state.spawn.room(obj_id="BOSS-000", position=Vector2(0, 1)), Vector2(0, 1))  # Boss Tile
        self.deploy(self._state.spawn.room(obj_id="ROOM-101", position=Vector2(4, 1)), Vector2(4, 1))  # Battle Room
        self.deploy(self._state.spawn.room(obj_id="ENTR-000", position=Vector2(5, 1)), Vector2(5, 1))  # Entrance Tile

################################################################################
    def deploy(self, room: DMRoom, position: Vector2):

        self._rows[int(position.y)]._rooms[int(position.x)] = room

################################################################################
    def get_room(self, position: Vector2) -> Optional[DMRoom]:

        if not isinstance(position, Vector2):
            raise TypeError(f"Invalid position type: {type(position)}")

        try:
            return self._rows[int(position.y)]._rooms[int(position.x)]
        except IndexError:
            return None

################################################################################
    def draw(self, surface: Surface):

        for row in self._rows:
            row.draw(surface)

################################################################################
    @property
    def all_rooms(self) -> List[DMRoom]:

        ret = []
        for row in self._rows:
            for room in row:
                if room is not None:
                    ret.append(room)

        return ret

################################################################################
    @property
    def entrance(self) -> DMRoom:

        return [r for r in self.all_rooms if r.is_entrance][0]

################################################################################
    @property
    def boss(self) -> DMRoom:

        return [r for r in self.all_rooms if r.is_boss][0]

################################################################################
    @property
    def battle_rooms(self) -> List[DMRoom]:

        return [r for r in self.all_rooms if r.is_battle_room]

################################################################################
    @property
    def trap_rooms(self) -> List[DMRoom]:

        return [r for r in self.all_rooms if r.is_trap]

################################################################################
    @property
    def facilities(self) -> List[DMRoom]:

        return [r for r in self.all_rooms if r.is_facility]

################################################################################
    @property
    def empty_rooms(self) -> List[DMRoom]:

        return [r for r in self.all_rooms if r.is_empty]

################################################################################
    def spawn_hero(self) -> None:

        hero = self.game.spawn.hero("Farmer")
        self.game.dungeon.add_hero(hero)
        hero.start_movement()

################################################################################
    def get_adjacent_rooms(
        self,
        pos: Vector2,
        show_west: bool,
        show_east: bool,
        show_north: bool,
        show_south: bool,
        all_rooms: bool,
        include_current: bool
    ) -> List[DMRoom]:

        if any((show_west, show_east, show_north, show_south)) and all_rooms:
            raise ValueError("Received conflicting arguments while completing adjacent rooms query.")
        if not any((show_west, show_east, show_north, show_south, all_rooms)):
            raise ValueError("Received literally no True arguments while completing adjacent rooms query.")

        ret = []

        # Left
        if show_west or all_rooms:
            x = Vector2(pos.x - 1, pos.y)
            west = self.get_room(x)
            if west is not None:
                ret.append(west)
        # Right
        if show_east or all_rooms:
            x = Vector2(pos.x + 1, pos.y)
            east = self.get_room(x)
            if east is not None:
                ret.append(east)
        # Up
        if show_north or all_rooms:
            x = Vector2(pos.x, pos.y - 1)
            north = self.get_room(x)
            if north is not None:
                ret.append(north)
        # Down
        if show_south or all_rooms:
            x = Vector2(pos.x, pos.y + 1)
            south = self.get_room(x)
            if south is not None:
                ret.append(south)

        final = [r for r in ret if r.__class__.__name__ != "EntranceRoom"]
        if include_current:
            final.append(self.get_room(pos))

        return ret

################################################################################
