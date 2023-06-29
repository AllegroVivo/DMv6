from __future__ import annotations

from time       import time
from typing     import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from .game import DMGame
################################################################################

__all__ = ("DMGenerator",)

################################################################################
class DMGenerator:
    """A generator for random numbers and other random behavior.

    This is a Python implementation of the Mersenne Twister algorithm, which
    is a pseudorandom number generator. It is used to generate random numbers
    for the game, and is seeded with the current time when the game is started.

    Attributes:
    -----------
    _state: :class:`DMGame`
        The game instance that this generator is attached to.

    _MT: :class:`List[int]`
        The array of 624 numbers that are used to generate random numbers.

    _seed: :class:`int`
        The seed that was used to generate the initial array of numbers.

    _index: :class:`int`
        The current index of the array of numbers.

    Methods:
    --------
    _generate_initial_array() -> None:
        Generate the initial array of 624 numbers.

    _generate() -> None:
        Generate the next 624 numbers in the array.

    next() -> int:
        Return the next random number in the array.

    choice(seq: :class:`List[Any]`) -> Any:
        Return a random element from the given sequence.

    sample(seq: :class:`List[Any]`, k: :class:`int`) -> List[Any]:
        Return a list of k random elements from the given sequence.

    weighted_choice(seq: List[Any], _weights: Dict[:class:`int`, :class:`float`], k: :class:`int`) -> List[Any]:
        Return a random element from the given sequence, with weights.

    from_range(start: :class:`float`, stop: :class:`float`) -> :class:`float`:
        Return a random number from the given range. Returns a float with
        precision of 2 decimal places.

    chance(percentage: Union[:class:`int`, :class:`float`]) -> :class:`bool`:
        Return True if the given percentage is greater than a random number.
    """

    __slots__ = (
        "_state",
        "_MT",
        "_seed",
        "_index",
    )

################################################################################
    def __init__(self, state: DMGame, seed: int = None):

        self._state: DMGame = state

        self._MT: List[int] = [0] * 624
        self._seed: int = seed if seed is not None else int(time())
        self._MT[0] = self._seed
        self._index: int = 624

        self._generate_initial_array()

################################################################################
    def _generate_initial_array(self) -> None:
        """Generate the initial array of 624 numbers.

        This is done by seeding the first number with the seed, and then
        generating the rest of the array from that number.
        """

        for i in range(1, 624):
            self._MT[i] = (
                (0x6c078965 * (self._MT[i - 1] ^ (self._MT[i - 1] >> 30)) + i) & 0xFFFFFFFF
            )

################################################################################
    def _generate(self):
        """Generate the next 624 numbers in the array.

        This is done by iterating through the array and generating each number
        from the previous number.
        """

        for i in range(624):
            y = (self._MT[i] & 0x80000000) + (self._MT[(i+1) % 624] & 0x7fffffff)
            self._MT[i] = self._MT[(i+397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self._MT[i] ^= 0x9908b0df

################################################################################
    def next(self) -> float:
        """Return the next random number in the sequence."""

        if self._index >= 624:
            self._generate()
            self._index = 0

        y = self._MT[self._index]
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9d2c5680)
        y ^= ((y << 15) & 0xefc60000)
        y ^= (y >> 18)

        self._index += 1
        return y / 0xFFFFFFFF

################################################################################
    def choice(self, seq: List[Any], *, exclude: Optional[Any] = None) -> Optional[Any]:
        """Return a random element from the sequence `seq`. If seq is empty, it
        will return nothing.
         
        You may optionally exclude a specific element from the sequence.
         
        Parameters:
        -----------
        seq : List[Any]
            The sequence to choose from.

        exclude : Optional[Any]
            An element to exclude from the sequence. Defaults to None.
            
        Returns:
        --------
        Optional[Any]
            A random element from the sequence, or None if the sequence was empty.
         """

        if exclude is not None:
            seq = [item for item in seq if item != exclude]

        try:
            return seq[int(self.next() * len(seq))]
        except IndexError:
            return None

################################################################################
    def sample(self, seq: List[Any], k: int = 1, *, exclude: Optional[Any] = None) -> List[Any]:
        """Return a list of k elements from the sequence `seq`. If seq is empty,
        it will return an empty list.
        
        You may optionally exclude a specific element from the sequence.
        
        Parameters:
        -----------
        seq : List[Any]
            The sequence to choose from.

        k : :class:`int`
            The number of elements to choose. Defaults to 1.

        exclude : Optional[Any]
            An element to exclude from the sequence. Defaults to None.
            
        Returns:
        --------
        List[Any]
            A list of k elements from the sequence, or an empty list if the
            sequence was empty.
        """

        if exclude is not None:
            seq = [item for item in seq if item != exclude]

        return [self.choice(seq, exclude=exclude) for _ in range(k)]

################################################################################
    def weighted_choice(self, seq: List[Any], _weights: Dict[int, float], k: int) -> List[Any]:
        """Return a list of k elements from the sequence `seq`, where each
        element has a weighted chance of being chosen.

        Parameters:
        -----------
        seq : List[Any]
            The sequence to choose from.

        _weights : Dict[int, float]
            A dictionary of weights, where the key is the rank of the element
            in the sequence, and the value is the weight of that element.

        k : :class:`int`
            The number of elements to choose.

        Returns:
        --------
        List[Any]
            A list of k elements from the sequence.

        Raises:
        -------
        :exc:`AssertionError`
            If the array and weights do not have the same length, if any of the
            weights are negative, or if none of the weights are positive.

        Notes:
        ------
        The weights do not need to add up to 1.0, but they must be non-negative
        and at least one of them must be positive.

        The weights are scaled so that they add up to 1.0, and then a random
        number is chosen between 0 and 1.0. The first element is chosen if the
        random number is less than the weight of the first element. Otherwise,
        the random number is subtracted from the weight of the first element,
        and the second element is chosen if the random number is less than the
        weight of the second element. This continues until an element is chosen.
        """

        weights = [_weights.get(item.rank, 0) for item in seq]

        assert len(seq) == len(weights), "Array and weights must have the same length"
        assert all(weight >= 0 for weight in weights), "Weights must be non-negative"
        assert any(weight > 0 for weight in weights), "At least one weight must be positive"

        total_weight = sum(weights)
        scaled_weights = [weight / total_weight for weight in weights]

        choices = []
        for _ in range(k):
            r = self.next()
            for i, weight in enumerate(scaled_weights):
                if r < weight:
                    choices.append(seq[i])
                    break
                r -= weight

        return choices

################################################################################
    # def scaling_damage(self, room: DMRoom) -> int:
    #     """Intended to calculate the damage dealt by objects, usually traps,
    #     that deal random damage from within a range for each of their levels."""
    #
    #     try:
    #         x = room._damage_range
    #     except AttributeError:
    #         raise AttributeError("Room must have a _damage_range attribute to use this method.")
    #
    #     base_damage = 1 + int(self.next() * x)
    #     additional_damage = sum(int(self.next() * (x - 1)) for _ in range(room.level))
    #
    #     return base_damage + additional_damage

################################################################################
    def from_range(self, start: float, stop: float) -> float:
        """Return a random integer from the range [start, stop]. Returns
        precision to 2 decimal places.

        Parameters:
        -----------
        start : :class:`float`
            The start of the range.

        stop : :class:`float`
            The end of the range.

        Returns:
        --------
        :class:`float`
            A random integer from the range [start, stop].

        Raises:
        -------
        :exc:`AssertionError`
            If start is greater than stop.

        Notes:
        ------
        The range is inclusive of both start and stop.

        This method is intended to be used for generating random floats from
        within a range, rather than random integers. For example, if you want
        to generate a random float between 0.0 and 1.0, you would use
        `from_range(0.0, 1.0)`.
        """

        def frange(begin, end):
            i = begin
            while i < end:
                yield i
                i += 0.01

        return self.choice([i for i in frange(start, stop + 1)])

################################################################################
#     def hero(self, room: Optional[DMRoom] = None, *, exclude: Optional[DMHero] = None) -> Optional[DMHero]:
#         """Return a random hero from the provided room, or from the dungeon if
#         no room is provided.
#
#         Parameters:
#         -----------
#         room : Optional[:class:`DMRoom`]
#             The room to choose a hero from. Defaults to None.
#         exclude : Optional[:class:`DMHero`]
#             A hero to exclude from the selection. Defaults to None.
#
#         Returns:
#         --------
#         Optional[:class:`DMHero`]
#             A random hero from the room, or from the dungeon if no room is
#             provided.
#         """
#
#         # If we've provided a room, we'll choose a hero from that room.
#         if room is not None:
#             return self.choice(room.heroes, exclude=exclude)
#
#         # Otherwise, we'll choose a hero from the dungeon overall.
#         return self.choice(self._state.dungeon.heroes, exclude=exclude)
#
# ################################################################################
#     def monster(
#         self,
#         room: Optional[DMRoom] = None,
#         *,
#         exclude: Optional[DMMonster] = None,
#         inventory: bool = False
#     ) -> Optional[DMHero]:
#         """Return a random monster from the provided room, or from the dungeon if
#         no room is provided. Alternatively, if `inventory` is True, this will
#         override any other behavior and return a random monster from the player's
#         inventory.
#
#         Parameters:
#         -----------
#         room : Optional[:class:`DMRoom`]
#             The room to choose a monster from. Defaults to None.
#         exclude : Optional[:class:`DMMonster`]
#             A monster to exclude from the selection. Defaults to None.
#         inventory : :class:`bool`
#             Whether to choose a monster from the inventory. Defaults to False.
#             Silently overrides all other behavior if True.
#
#         Returns:
#         --------
#         Optional[:class:`DMMonster`]
#             A random monster from the room, dungeon, or player's inventory,
#             depending on the parameters.
#         """
#
#         # If we're choosing from the player's inventory, we'll do that.
#         if inventory:
#             return self.choice(self._state.inventory.monsters, exclude=exclude)
#
#         # If we've provided a room, we'll choose a monster from that room.
#         if room is not None:
#             return self.choice(room.monsters)
#
#         # Otherwise, we'll choose a monster from the dungeon overall.
#         return self.choice(self._state.dungeon.deployed_monsters)

################################################################################
    def chance(self, n: Union[int, float]) -> bool:
        """Return True with a probability of n/100. If n is greater than 1, it
        will be divided by 100. If n is less than 0, it will be treated as 0.

        Parameters:
        -----------
        n : Union[:class:`int`, :class:`float`]
            The probability of returning True. For readability, it can be an
            integer - any value greater than 1 will be divided by 100.

        Returns:
        --------
        :class:`bool`
            True with a probability of n/100.
        """

        if n not in range(0, 101):
            raise ValueError("Chance must be between 0 and 100")

        if n > 1:
            n /= 100
        elif n < 0:
            n = 0

        return self.next() <= n

################################################################################
