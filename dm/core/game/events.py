from __future__ import annotations

from typing     import TYPE_CHECKING, Callable, Dict, List

from utilities  import _EVENT_REFERENCE

if TYPE_CHECKING:
    from .game  import DMGame
    from .contexts import DMContext
################################################################################

__all__ = ("DMEventManager", )

################################################################################
class DMEventManager:
    """The event manager for the game.

    Attributes:
    -----------
    _state: :class:`DMGame`
        The game state that the event manager is attached to.

    _subscribers: :class:`Dict[str, List[Callable]]`
        The dictionary of subscribers for the event manager.

    Methods:
    --------
    _init_subscriber_dict() -> None:
        Initialize the subscriber dictionary with all possible events.

    subscribe(event_type: :class:`str`, callback: :class:`Callable`) -> None:
        Subscribe a callback to an event type.

    unsubscribe(event_type: :class:`str`, callback: :class:`Callable`) -> None:
        Unsubscribe a callback from an event type.

    dispatch(event_type: :class:`str`, *context) -> None:
        Notify all subscribers of an event type.
    """

    __slots__ = (
        "_state",
        "_subscribers",
    )

################################################################################
    def __init__(self, game: DMGame):

        self._state: DMGame = game

        self._subscribers: Dict[str, List[Callable]] = {}
        self._init_subscriber_dict()

################################################################################
    def _init_subscriber_dict(self) -> None:
        """Initialize the subscriber dictionary with all possible events."""

        for event in _EVENT_REFERENCE:
            self._subscribers[event] = []

################################################################################
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe a callback to an event type.

        Parameters:
        -----------
        event_type: :class:`str`
            The event type to subscribe to.

        callback: :class:`Callable`
            The callback to subscribe to the given event.

        Raises:
        -------
        :exc:`TypeError`:
            If the event type is not a valid event type or if the callback is not callable.
        """

        if event_type not in self._subscribers:
            raise TypeError(f"Invalid event name ['{event_type}'] passed to EventManager.subscribe().")

        if not callable(callback):
            raise TypeError("Invalid observer callback passed to EventManager.subscribe().")

        if callback in self._subscribers[event_type]:
            return

        self._subscribers[event_type].append(callback)

################################################################################
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe a callback from an event type.

        Parameters:
        -----------
        event_type: :class:`str`
            The event type to unsubscribe from.

        callback: :class:`Callable`
            The callback to unsubscribe from the given event.

        Raises:
        -------
        :exc:`TypeError`:
            If the event type is not a valid event type.
        """

        if event_type not in self._subscribers:
            raise TypeError("Invalid event name passed to EventManager.unsubscribe().")

        self._subscribers[event_type].remove(callback)

################################################################################
    def dispatch(self, event_type: str, *context: DMContext) -> None:
        """Dispatch an event to all subscribers.

        Parameters:
        -----------
        event_type: :class:`str`
            The event type to dispatch.

        *context: :class:`Any`
            The context to pass to the callback.

        Raises:
        -------
        TypeError:
            If the event type is not a valid event type.
        """

        # Might just make this a pass depending on if I go crazy making event types
        if event_type not in self._subscribers:
            raise TypeError(f"Invalid event name `{event_type}` passed to EventManager.dispatch().")

        for callback in self._subscribers[event_type]:
            try:
                callback(*context)
            except Exception as e:
                print(f"Invalid callback |{callback}| found in EventManager.dispatch() for event {event_type}.")
                continue

################################################################################
