from __future__ import annotations

from pygame     import Surface
from typing     import TYPE_CHECKING, Optional, Type, TypeVar

if TYPE_CHECKING:
    from dm.core.objects.object    import DMObject
    from dm.core.game.game         import DMGame
################################################################################

__all__ = ("GraphicalComponent",)

GC = TypeVar("GC", bound="GraphicalComponent")

################################################################################
class GraphicalComponent:
    """A basic graphical component for a DMObject. Intended to be subclassed.

    Attributes:
    -----------
    _parent : :class:`DMObject`
        The parent DMObject this graphical component belongs to.

    _static : Optional[:class:`Surface`]
        The base static sprite for the object.

    Properties:
    -----------
    game : :class:`DMGame`
        The game instance.

    static : Optional[:class:`Surface`]
        The base static sprite for the object.

    Methods:
    --------
    _load_sprites() -> None
        Loads the sprites for the graphical component.

    draw(screen: :class:`Surface`) -> None
        Draws the graphical component to the screen.

    update(dt: :class:`float`) -> None
        Updates the graphical component.

    _copy() -> :class:`GraphicalComponent`
        Returns a clean copy of the current graphical component.
    """

    __slots__ = (
        "_parent",
        "_static",
    )

################################################################################
    def __init__(self, parent: DMObject):

        self._parent: DMObject = parent
        self._static: Optional[Surface] = None

################################################################################
    @property
    def game(self) -> DMGame:
        """The game instance."""

        return self._parent.game

################################################################################
    @property
    def parent(self) -> DMObject:
        """The parent DMObject this graphical component belongs to. This should
        be overridden by subclasses to be more specific for type checking."""

        raise NotImplementedError

################################################################################
    @property
    def static(self) -> Optional[Surface]:
        """The base static sprite for the parent object."""

        return self._static

################################################################################
    def _load_sprites(self) -> None:
        """Loads the sprites for the graphical component. Must be further
        implemented by subclasses."""

        raise NotImplementedError

################################################################################
    def draw(self, screen: Surface) -> None:
        """Draws the graphical component to the screen.

        Parameters:
        -----------
        screen : :class:`Surface`
            The surface to draw to.
        """

        raise NotImplementedError

################################################################################
    def update(self, dt: float) -> None:
        """Updates the graphical component.

        Parameters:
        -----------
        dt : :class:`float`
            The time since the last frame.
        """

        pass

################################################################################
    def _copy(self, parent: DMObject) -> GraphicalComponent:
        """Returns a clean copy of the current object's graphics data.

        There are no kwargs available for this implementation.

        Returns:
        --------
        :class:`GraphicalComponent`
            A fresh copy of the current Graphical component.
        """

        cls: Type[GC] = type(self)
        new_obj = cls.__new__(cls)

        new_obj._parent = parent
        new_obj._static = self._static

        return new_obj

################################################################################