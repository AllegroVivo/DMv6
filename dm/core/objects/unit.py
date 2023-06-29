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
from ..graphics._graphical import GraphicalComponent
from ..graphics.movement import MovementComponent
from ...core.objects.room import DMRoom
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
        "_moving",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        _id: str,
        name: str,
        description: Optional[str],
        graphics: GraphicalComponent,
        rank: int = 0,
        start_cell: Optional[Vector2] = None
    ):

        super().__init__(state, _id, name, description, rank, unlock)

        self._room: Optional[Vector2] = start_cell

        self._graphics: GraphicalComponent = graphics
        self._mover: MovementComponent = MovementComponent(self)
        self._moving: bool = False

################################################################################
    @property
    def room(self) -> DMRoom:

        return self._mover.room

################################################################################
    @property
    def graphics(self) -> GraphicalComponent:

        return self._graphics

################################################################################
    @property
    def screen_pos(self) -> Vector2:

        return self._mover._screen_pos

################################################################################
    def draw(self, screen: Surface) -> None:

        self.graphics.draw(screen)

################################################################################
    def update(self, dt: float) -> None:

        if self._moving:
            self._mover.update(dt)
        self.graphics.update(dt)

################################################################################
    def _copy(self, **kwargs) -> DMUnit:

        new_obj: Type[U] = super()._copy()  # type: ignore

        new_obj._room = kwargs.pop("room", None)
        new_obj._graphics = self._graphics._copy(new_obj)
        # new_obj._mover = self._mover._copy(new_obj)

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
