from __future__ import annotations

from uuid       import UUID, uuid4
from typing     import TYPE_CHECKING, Callable, Optional, Type, TypeVar

from utilities  import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from dm.core.objects.room import DMRoom
    from dm.core.game.rng import DMGenerator
################################################################################

__all__ = ("DMObject", )

DMObj = TypeVar("DMObj", bound="DMObject")

################################################################################
class DMObject:
    """The base class for most objects in the game.

    Attributes:
    -----------
    _uuid: :class:`UUID`
        The unique identifier for this object.

    _state: :class:`DMGame`
        The game state that this object belongs to.

    _id: :class:`str`
        The unique identifier for this object.

    _name: :class:`str`
        The name of this object. This is what will be displayed to the player.

    _description: Optional[:class:`str`]
        The description of this object, if present.

    _rank: :class:`int`
        The rank of this object.

    Properties:
    -----------
    name: :class:`str`
        Returns the name of the object.

    description: Optional[:class:`str`]
        Returns the description of the object, if any.

    rank: :class:`int`
        Returns the rank of the object.

    game: :class:`DMGame`
        Returns the game state that this object belongs to.

    room: Optional[:class:`DMRoom`]
        Returns the room that this object belongs to, if any.

    random: :class:`DMGenerator`
        Returns the random number generator for the game.

    Methods:
    --------
    listen(event: :class:`str`, callback: Optional[:class:`Callable`]) -> None
        Adds an event callback for the object.

    notify(event: :class:`str`, *args) -> None
        Notifies the game of an event.

    _copy(**kwargs) -> :class:`DMObject`
        Returns a copy of the object. Should be augmented by subclasses.

    is_room() -> :class:`bool`
        Returns whether or not the object is a room.

    is_monster() -> :class:`bool`
        Returns whether or not the object is a monster.

    is_hero() -> :class:`bool`
        Returns whether or not the object is a hero.

    is_relic() -> :class:`bool`
        Returns whether or not the object is a relic.

    is_status() -> :class:`bool`
        Returns whether or not the object is a status.

    is_skill() -> :class:`bool`
        Returns whether or not the object is a skill.
    """

    __slots__ = (
        "_uuid",
        "_state",
        "_id",
        "_name",
        "_description",
        "_rank",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        _id: str,
        name: str,
        description: Optional[str],
        rank: int = 0
    ):

        self._uuid: UUID = uuid4()
        self._state: DMGame = state

        self._id: str = _id
        self._name: str = name
        self._description: Optional[str] = description
        self._rank: int = rank

################################################################################
    def __eq__(self, other: DMObject) -> bool:
        """Returns whether or not the two objects are equal."""

        if not isinstance(other, DMObject):
            return False

        return self._uuid == other._uuid

################################################################################
    @property
    def name(self) -> str:
        """Returns the name of the object.

        Returns:
        --------
        :class:`str`
            The name of the object.
        """

        return self._name

################################################################################
    @property
    def description(self) -> Optional[str]:
        """Returns the description of the object, if any.

        Returns:
        --------
        Optional[:class:`str`]
            The description of the object, if present.
        """

        return self._description

################################################################################
    @property
    def rank(self) -> int:
        """Returns the object's rank.

        Returns:
        --------
        :class:`int`
            The object's rank.
        """

        return self._rank

################################################################################
    @property
    def game(self) -> DMGame:
        """Returns the main game instance."""

        return self._state

################################################################################
    @property
    def room(self) -> DMRoom:
        """Returns the room where this object is located, if applicable."""

        raise NotImplementedError

################################################################################
    @property
    def random(self) -> DMGenerator:
        """Returns the game's random number generator."""

        return self._state._rng

################################################################################
    def listen(self, event: str, callback: Optional[Callable] = None) -> None:
        """Automatically listens to the given event with the provided method.
        If no method is provided, it will default to `self.notify`.

        Parameters:
        -----------
        event: :class:`str`
            The event to listen to.

        callback: Optional[:class:`Callable`]
            The method to call when the event is triggered. If no callback
            is provided, it will default to `self.notify`.
        """

        self.game.subscribe_event(event, callback or self.notify)

################################################################################
    def notify(self, *args) -> None:
        """Predefined notification method for listening to events."""

        raise NotImplementedError

################################################################################
    def _copy(self, **kwargs) -> DMObject:
        """Returns a clean copy of the current object type with any given
        kwargs substituted in. The UUID **is** regenerated.

        Returns:
        --------
        :class:`DMObject`
            A fresh copy of the current DMObject.
        """

        cls: Type[DMObj] = type(self)
        new_obj = cls.__new__(cls)

        new_obj._uuid = uuid4()
        new_obj._state = self._state

        new_obj._id = self._id
        new_obj._name = self.name
        new_obj._description = self.description

        new_obj._rank = self.rank

        return new_obj

################################################################################
    @staticmethod
    def is_room() -> bool:
        """Returns whether or not the object is a room."""

        return False

################################################################################
    @staticmethod
    def is_monster() -> bool:
        """Returns whether or not the object is a monster."""

        return False

################################################################################
    @staticmethod
    def is_hero() -> bool:
        """Returns whether or not the object is a hero."""

        return False

################################################################################
    @staticmethod
    def is_status() -> bool:
        """Returns whether or not the object is a status."""

        return False

################################################################################
    @staticmethod
    def is_relic() -> bool:
        """Returns whether or not the object is a relic."""

        return False

################################################################################
    @staticmethod
    def is_skill() -> bool:
        """Returns whether or not the object is a skill."""

        return False

################################################################################
