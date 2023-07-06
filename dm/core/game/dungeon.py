from __future__ import annotations

import random

from pygame         import Surface, Vector2
from typing         import TYPE_CHECKING, List, Optional, Tuple, Union

from .map           import DMDungeonMap
from utilities      import *

if TYPE_CHECKING:
    from .game import DMGame
    from .map import DMMapRow
    from ..objects.monster import DMMonster
    from ..objects.room import DMRoom
    from ..objects.hero import DMHero
################################################################################

__all__ = ("DMDungeon",)

################################################################################
class DMDungeon:

    __slots__ = (
        "_state",
        "_map",
        "_heroes",
    )

################################################################################
    def __init__(self, game: DMGame):

        self._state: DMGame = game
        self._map = DMDungeonMap(game)

        self._heroes: List[DMHero] = []

################################################################################
    def __getitem__(self, index: int) -> DMMapRow:

        return self._map[index]

################################################################################
    @property
    def deployed_monsters(self) -> List[DMMonster]:

        return self._map.deployed_monsters

################################################################################
    @property
    def heroes(self) -> List[DMHero]:

        return self._heroes

################################################################################
    def draw(self, screen: Surface) -> None:

        self._map.draw(screen)

        for monster in self.deployed_monsters:
            monster.draw(screen)

        for hero in self.heroes:
            hero.draw(screen)

################################################################################
    def update(self, dt: float) -> None:

        for monster in self.deployed_monsters:
            monster.update(dt)

        for hero in self.heroes:
            hero.update(dt)

################################################################################
    def get_room_at(self, pos: Union[Vector2, Tuple[int, int]]) -> Optional[DMRoom]:

        return self._map.get_room(pos)

################################################################################
    @property
    def entrance_tile(self) -> DMRoom:

        return self._map.entrance

################################################################################
    @property
    def boss_tile(self) -> DMRoom:

        return self._map.boss

################################################################################
    @property
    def battle_rooms(self) -> List[DMRoom]:

        return self._map.battle_rooms

################################################################################
    @property
    def trap_rooms(self) -> List[DMRoom]:

        return self._map.trap_rooms

################################################################################
    @property
    def facilities(self) -> List[DMRoom]:

        return self._map.facilities

################################################################################
    @property
    def all_rooms(self) -> List[DMRoom]:

        return self._map.all_rooms

################################################################################
    def spawn_hero(self) -> None:

        self._map.spawn_hero()

################################################################################
    @property
    def heroes(self) -> List[DMHero]:

        return self._heroes

################################################################################
    def add_hero(self, hero: DMHero) -> None:

        self._heroes.append(hero)

################################################################################
