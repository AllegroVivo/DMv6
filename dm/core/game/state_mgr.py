from __future__ import annotations

import pygame

from typing import TYPE_CHECKING, List, Optional, Union

from dm.core.game.state     import DMState
from dm.states  import _STATE_MAPPINGS
from utilities  import *

if TYPE_CHECKING:
    from pygame         import Surface
    from pygame.event   import Event

    from dm.core.game.game   import DMGame
################################################################################

__all__ = ("DMStateMachine",)

################################################################################
class DMStateMachine:
    """The state machine for the game.

    Attributes:
    -----------
    _game : :class:`DMGame`
        The game instance.

    _states : List[:class:`DMState`]
        The list of states.

    _previous_state : Optional[:class:`DMState`]
        The previous state, if any.

    Methods:
    --------
    __repr__() -> :class:`str`
        Returns a string representation of the state stack.

    Properties:
    -----------
    game : :class:`DMGame`
        Returns the game instance.

    previous_state : Optional[:class:`DMState`]
        Returns the previous state, if any.

    current_state : :class:`DMState`
        Returns the current state.

    states : List[:class:`DMState`]
        Returns the list of states.

    Methods:
    --------
    push_state(state: Union[:class:`str`, :class:`DMState`]) -> None
        Pushes a state onto the stack.

    pop_state() -> None
        Pops a state off the stack.

    switch_state(state: Union[:class:`str`, :class:`DMState`]) -> None
        Switches to a new state.

    clear_previous_state() -> None
        Clears the previous state.

    handle_event(event: :class:`Event`) -> None
        Handles a game event.

    update(dt: :class:`float`) -> None
        Updates the state stack.

    draw(screen: :class:`Surface`) -> None
        Draws the state stack to the screen.
    """

    __slots__ = (
        "_game",
        "_states",
        "_previous_state"
    )

################################################################################
    def __init__(self, game: DMGame):

        self._game: DMGame = game

        self._states: List[DMState] = []
        self._previous_state: Optional[DMState] = None

################################################################################
    def __repr__(self) -> str:
        """Returns a string representation of the state stack.

        Returns:
        --------
        :class:`str`
            The string representation of the state stack.
        """

        ret = f"<StateStackManager -- Stack breakdown from current to last:"
        count = 1

        for state in reversed(self._states):
            ret += f"\n{count}. {state}"
            count += 1

        return ret + ">"

################################################################################
    @property
    def game(self) -> DMGame:
        """Returns the game instance."""

        return self._game

################################################################################
    @property
    def previous_state(self) -> Optional[DMState]:
        """Returns the previous state, if any."""

        return self._previous_state

################################################################################
    @property
    def current_state(self) -> DMState:
        """Returns the current state."""

        return self._states[-1]

################################################################################
    @property
    def states(self) -> List[DMState]:
        """Returns the current list of states."""

        return self._states

################################################################################
    def push_state(self, state: Union[str, DMState]) -> None:
        """Pushes a new state onto the stack.

        Parameters:
        -----------
        state: Union[:class:`str`, :class:`DMState`]
            The state to push onto the stack.

        Notes:
        ------
        If a :class:`str` is passed, it will be mapped to a :class:`DMState`
        using the :data:`dm.states._STATE_MAPPINGS` dictionary.

        If a :class:`DMState` is passed, it will be pushed onto the stack
        directly.
        """

        if isinstance(state, str):
            cls = _STATE_MAPPINGS.get(state)
            if cls:
                self._states.append(cls(self.game))
        elif isinstance(state, DMState):
            self._states.append(state)

################################################################################
    def pop_state(self) -> bool:
        """Pops the current state off the stack.

        Returns:
        --------
        :class:`bool`
            Whether there are any states left on the stack.

        Notes:
        ------
        If there are no states left on the stack, the game will quit.
        """

        if not self._states:
            return False

        self._previous_state = self._states.pop()

        return True

################################################################################
    def switch_state(self, state: Union[str, DMState]) -> None:
        """Switches the current state to a new state. **This will pop the current
        state off the stack, not simply push a new state on top of the stack.**

        Parameters:
        -----------
        state: Union[:class:`str`, :class:`DMState`]
            The state to switch to.

        Notes:
        ------
        If a :class:`str` is passed, it will be mapped to a :class:`DMState`
        using the :data:`dm.states._STATE_MAPPINGS` dictionary.

        If a :class:`DMState` is passed, it will be pushed onto the stack
        directly.
        """

        if self._states:
            self._previous_state = self._states.pop()

        self.push_state(state)

################################################################################
    def clear_previous_state(self) -> None:
        """Clears the previous state."""

        self._previous_state = None

################################################################################
    def handle_event(self, event: Event) -> None:
        """Relays events down to the current state for handling.

        Parameters:
        -----------
        event: :class:`Event`
            The event to handle.
        """

        if self._states:
            self.current_state.handle_event(event)

################################################################################
    def update(self, dt: float) -> None:
        """Updates the current state.

        Parameters:
        -----------
        dt: :class:`float`
            The time since the last frame.
        """

        if self._states:
            state = self.current_state
            state.update(dt)

            if state.quit:
                self._previous_state = self._states.pop()
                if not self._states:
                    self.game.quit()
            elif state.next_state:
                self.push_state(state.next_state)
                state.next_state = None

################################################################################
    def draw(self, screen: Surface):
        """Draws the current state.

        Parameters:
        -----------
        screen: :class:`Surface`
            The screen to draw to.
        """

        if self._states:
            # screen.fill(BLACK)
            self.current_state.draw(screen)

            pygame.display.flip()

################################################################################
