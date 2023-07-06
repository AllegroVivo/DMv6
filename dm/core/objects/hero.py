from __future__ import annotations

from pygame     import Surface, Vector2
from typing     import TYPE_CHECKING, Optional, Type, TypeVar

from .unit import DMUnit
from ..graphics.hero import HeroGraphical
from ..graphics.movement import MovementComponent
from dm.core.game.stats import UnitStats

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from dm.core.objects.room import DMRoom
################################################################################

__all__ = ("DMHero",)

H = TypeVar("H", bound="DMHero")

################################################################################
class DMHero(DMUnit):
    """Represents a hero in the game."""

    __slots__ = (
        "_mover",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        start_cell: Optional[Vector2] = None,
        *,
        _id: str,
        name: str,
        description: Optional[str] = None,
        rank: int = 0
    ):

        super().__init__(
            state=state,
            _id=_id,
            name=name,
            description=description,
            graphics=HeroGraphical(self),
            rank=rank,
            start_cell=start_cell,
            stats=UnitStats(1, 1, 1.0)
        )

################################################################################
    @property
    def mover(self) -> MovementComponent:

        return self._mover

################################################################################
    def draw(self, screen: Surface) -> None:
        """Draws the hero to the screen.

        Parameters:
        -----------
        screen: :class:`Surface`
            The screen to draw the hero to.
        """

        self.graphics.draw(screen)

################################################################################
    def _copy(self, **kwargs) -> DMHero:
        """Copies the hero.

        Parameters:
        -----------
        kwargs: :class:`dict`
            The keyword arguments to pass to the new object's constructor.

        Returns:
        --------
        :class:`DMHero`
            The new object.
        """

        new_obj: Type[H] = super()._copy(  # type: ignore
            room=self.game.dungeon.entrance_tile.grid_pos
        )

        return new_obj

################################################################################
    @staticmethod
    def is_hero() -> bool:

        return True

################################################################################
    def set_target_cell(self, cell: DMRoom) -> None:
        """Sets the target cell for the hero.

        Parameters:
        -----------
        cell: :class:`Vector2`
            The target cell.
        """

        self._mover.set_target_cell(cell.grid_pos)

################################################################################
