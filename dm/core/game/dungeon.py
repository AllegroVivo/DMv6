from __future__ import annotations

import random

from pygame         import Surface, Vector2
from typing         import TYPE_CHECKING, List, Optional, Tuple, Union

from .map           import DMDungeonMap
from utilities      import *

if TYPE_CHECKING:
    from .game import DMGame
    from .map import DMMapRow
################################################################################

__all__ = ("DMDungeon",)

################################################################################
class DMDungeon:

    __slots__ = (
        "_state",
        "_map",
    )

################################################################################
    def __init__(self, game: DMGame):

        self._state: DMGame = game
        self._map = DMDungeonMap(game)

################################################################################
    def __getitem__(self, index: int) -> DMMapRow:

        return self._map[index]

################################################################################
    def draw(self, screen: Surface) -> None:

        self._map.draw(screen)

################################################################################
