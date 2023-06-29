from __future__ import annotations

from abc        import abstractmethod
from typing     import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from pygame         import Surface
    from pygame.event   import Event
################################################################################

__all__ = ("DMState",)

################################################################################
class DMState:
    """The base class for all states.

    Attributes:
    -----------
    _game : :class:`DMGame`
        The game instance.

    quit : :class:`bool`
        Whether or not the state should quit.

    next_state : Optional[:class:`str`]
        The next state to switch to.

    Methods:
    --------
    handle_event(event: :class:`Event`) -> None
        Handles events for the state.

    update(dt: :class:`float`) -> None
        Updates the state.

    draw(screen: :class:`Surface`) -> None
        Draws the state to the screen.

    __repr__() -> :class:`str`
        Returns a string representation of the state.

    Properties:
    -----------
    game : :class:`DMGame`
        Returns the game instance.
    """

    __slots__ = (
        "_game",
        "quit",
        "next_state",
    )

################################################################################
    def __init__(self, game: DMGame):

        self._game: DMGame = game
        self.quit: bool = False
        self.next_state: Optional[str] = None

################################################################################
    def __repr__(self) -> str:
        """Returns a string representation of the state.

        Returns:
        --------
        :class:`str`
            A string representation of the state.
        """

        return f"<DMState: {self.__class__.__name__}>"

################################################################################
    @property
    def game(self) -> DMGame:
        """Returns the game instance."""

        return self._game

################################################################################
    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """Handles events for the state.

        Parameters:
        -----------
        event : :class:`Event`
            The event to handle.
        """

        # Make sure to override K_RETURN behavior in subclasses.
        pass

################################################################################
    @abstractmethod
    def update(self, dt: float) -> None:
        """Updates the state.

        Parameters:
        -----------
        dt : :class:`float`
            The time since the last frame.
        """

        pass

################################################################################
    @abstractmethod
    def draw(self, screen: Surface) -> None:
        """Draws the state to the screen.

        Parameters:
        -----------
        screen : :class:`Surface`
            The screen to draw to.
        """

        pass

################################################################################
