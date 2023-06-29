from __future__ import annotations

import math

from typing     import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
################################################################################

__all__ = ("DMDay",)

################################################################################
class DMDay:
    """A class that keeps track of the current game day.

    Attributes
    ----------
    _state: :class:`DMGame`
        The game state that this day counter is attached to.

    _day: :class:`int`
        The current day.

    Properties
    ----------
    game: :class:`DMGame`
        Returns the game state that this day counter is attached to.

    current: :class:`int`
        Returns the current day.

    base_hero_count: :class:`int`
        Returns the base number of heroes that will invade on the current day.

    Methods
    -------
    advance() -> None
        Advance the day counter.
    """

    __slots__ = (
        "_state",
        "_day",
    )

################################################################################
    def __init__(self, state: DMGame):

        self._state: DMGame = state
        self._day: int = 1

################################################################################
    @property
    def game(self) -> DMGame:
        """Returns the game state."""

        return self._state

################################################################################
    @property
    def current(self) -> int:
        """Returns the current day."""

        return self._day

################################################################################
    @property
    def base_hero_count(self) -> int:

        # Calculate the ratio of the current step to the total number of steps
        ratio = math.sqrt(self.current / 2000)  # "Max" days can be 2000. Anything after that is dumb lol.

        # Linearly interpolate between the start and end values (8 and 50)
        # They represent how many heroes are invading on day 1 and day 2000,
        # respectively. (Before increases.)
        return int(8 + ratio * (50 - 8))

################################################################################
    def advance(self) -> None:
        """Advance the day counter."""

        self._day += 1

################################################################################
