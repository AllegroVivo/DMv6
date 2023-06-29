from __future__ import annotations

import random

from pygame         import Surface, Vector2
from typing     import TYPE_CHECKING, Dict, List, Optional, Tuple, Type, Union

# Bulk type imports for the pool
# from ...fates       import ALL_FATES, SPAWNABLE_FATES
# from ...heroes      import ALL_HEROES
# from ...monsters    import ALL_MONSTERS
# from ...relics      import ALL_RELICS
from ...rooms       import ALL_ROOMS
# from ...statuses    import ALL_STATUSES

from utilities      import *

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from ..objects.room     import DMRoom
    from dm.core.objects.object import DMObject
################################################################################

__all__ = ("DMObjectPool",)

################################################################################
class DMObjectPool:

    __slots__ = (
        "_state",
        "__master",
        "__monster_types",
        "__hero_types",
        "__room_types",
        "__status_types",
        "__relic_types",
        "__fate_types",
        "__monsters",
        "__heroes",
        "__rooms",
        "__statuses",
        "__relics",
        "__fates",
    )

################################################################################
    def __init__(self, state: DMGame):

        self._state: DMGame = state

        # self.__monster_types: List[Type[DMMonster]] = ALL_MONSTERS.copy()
        # self.__hero_types: List[Type[DMHero]] = ALL_HEROES.copy()
        self.__room_types: List[Type[DMRoom]] = ALL_ROOMS.copy()
        # self.__status_types: List[Type[DMStatus]] = ALL_STATUSES.copy()
        # self.__relic_types: List[Type[DMRelic]] = ALL_RELICS.copy()
        # self.__fate_types: List[Type[DMFateCard]] = SPAWNABLE_FATES.copy()

        # self.__monsters: List[DMMonster] = [m(self._state) for m in self.__monster_types]  # type: ignore
        # self.__heroes: List[DMHero] = [h(self._state) for h in self.__hero_types]  # type: ignore
        self.__rooms: List[DMRoom] = [r(self._state, Vector2()) for r in self.__room_types]  # type: ignore
        # self.__statuses: List[DMStatus] = [s(self._state, None) for s in self.__status_types]  # type: ignore
        # self.__relics: List[DMRelic] = [relic(self._state) for relic in self.__relic_types]  # type: ignore
        # self.__fates: List[DMFateCard] = [f(self._state, 0, 0) for f in self.__fate_types]  # type: ignore

        self.__master: List[DMObject] = self.__rooms.copy()
        #     self.__monsters.copy() +   # type: ignore
        #     self.__heroes.copy() +
        #     self.__relics.copy() +
        #     self.__statuses.copy() +
        #     [f(self._state, 0, 0) for f in ALL_FATES].copy()  # type: ignore
        # )

################################################################################
    def room(
        self,
        _n: Optional[str] = None,
        *,
        obj_id: Optional[str] = None,
        start_rank: int = 1,
        end_rank: int = 3,
        weighted: bool = True,
        init_obj: bool = True,
        **kwargs
    ) -> Union[DMRoom, Type[DMRoom]]:

        # Try spawning by name or object ID if provided.
        if _n is not None or obj_id is not None:
            # Get a list of matches for the current source list.
            matches = [r for r in self.__rooms if r.name == _n or r._id == obj_id]
            # If no matches were found, first search the full object pool to
            # see if the object exists but is not in the current source list.
            # (And raise an error to that extent if it is.)
            if len(matches) == 0:
                fallback = [
                    o.__class__.__name__ for o in self.__master
                    if o.name == _n or o._id == obj_id
                ]
                raise SpawnNotFound(_n or obj_id, "room", fallback)
            elif len(matches) > 1:
                raise ValueError(
                    f"Multiple rooms with name |{_n}| or ID |{obj_id}| found in ObjectPool.room()."
                )

            # If an object was found, return it, initialized or not
            # depending on parameters.
            if init_obj:
                return matches[0]._copy(**kwargs)
            else:
                return matches[0].__class__

        # Otherwise, spawn a random room.
        return self._spawn_random(  # type: ignore
            SpawnType.Room,
            start_rank,
            end_rank,
            weighted,
            init_obj,
            **kwargs
        )

################################################################################
    def _spawn_random(
        self,
        obj_type: SpawnType,
        start_rank: int,
        end_rank: int,
        weighted: bool,
        init_obj: bool,
        **kwargs
    ) -> Union[DMObject, Type[DMObject]]:
        """Spawns a random object of the given type."""

        # Get a dict of all objects mapped to their ranks.
        objs = {}
        for obj in self._get_source_list(obj_type):
            try:
                objs[obj.rank].append(type(obj))
            except KeyError:
                objs[obj.rank] = [type(obj)]

        # Get the eligible objects based on the provided start and end ranks.
        eligible_objs = {rank: objs[rank] for rank in range(start_rank, end_rank + 1)}
        if not eligible_objs:
            raise ValueError(
                f"No eligible objects of type |{obj_type}| found in ObjectPool._spawn_random()."
            )

        # Get weights if weighted is True.
        eligible_weights = None
        if weighted:
            weights = self._generate_weights(obj_type)
            eligible_weights = [weights[rank] for rank in range(start_rank, end_rank + 1)]

        # Going to use random here instead of our own RNG because it already
        # accepts the weights in this configuration. <_<
        chosen_idx = random.choices(
            list(eligible_objs.keys()), weights=eligible_weights, k=1
        )[0]
        result = eligible_objs[chosen_idx]

        if not init_obj:
            return result

        return result(self._state)._copy(**kwargs)

################################################################################
    def _get_source_list(self, spawn_type: SpawnType) -> List[DMObject]:

        if spawn_type is SpawnType.Room:
            return self.__rooms
        elif spawn_type is SpawnType.Monster:
            return self.__monsters
        elif spawn_type is SpawnType.Hero:
            return self.__heroes
        elif spawn_type is SpawnType.Relic:
            return self.__relics
        elif spawn_type is SpawnType.Status:
            return self.__statuses
        elif spawn_type is SpawnType.Fate:
            return self.__fates
        else:
            raise ValueError(f"Invalid spawn type |{spawn_type}|.")

################################################################################
    def _generate_weights(self, spawn_type: SpawnType) -> Dict[int, float]:
        """Generates a weight mapping for the given spawn type based on the current day.

        Parameters:
        -----------
        spawn_type: :class:`SpawnType`
            The type of object being spawned.

        Returns:
        --------
        Dict[:class:`int`, :class:`float`]
            A mapping of rank to weight.

        Notes:
        ------
        The weights are generated based on the current day and the rank of the object.
        The higher the rank, the lower the weight. The weights are also normalized so
        that they sum to 1.

        The weights are generated based on the following formula:

        - `weight = start_weight + ((end_weight - start_weight) * (current_day / max_day))`

        Where `start_weight` and `end_weight` are the weights for the first and last
        ranks respectively, `current_day` is the current day, and `max_day` is the
        maximum day to consider.
        """
        # Define the start and end weights for each rank
        rank_weights = self._base_weights(spawn_type)

        # Calculate the weight for each rank based on the current day
        weights = {}
        for rank, (start_weight, end_weight) in rank_weights.items():
            weight = start_weight + ((end_weight - start_weight) * (self._state.day.current / 2000))  # 2000 is the "max" day
            weights[rank] = weight

        # Normalize the weights so they sum to 1
        total_weight = sum(weights.values())
        normalized_weights = {rank: weight / total_weight for rank, weight in weights.items()}

        return normalized_weights

################################################################################
    @staticmethod
    def _base_weights(_type: SpawnType) -> Dict[int, Tuple[int, int]]:
        """Returns a rank vs. weight-over-time mapping for the given spawn type.

        Parameters:
        -----------
        _type: :class:`str`
            The type of object to generate weights for.

        Returns:
        --------
        Dict[:class:`int`, Tuple[:class:`int`, :class:`int`]]
            A mapping of rank to a tuple of (start_weight, end_weight) for that rank.

        Raises:
        -------
        ValueError
            If an invalid spawn type is provided.
        """

        if _type == SpawnType.Monster:
            return {
                1: (100, 50),
                2: (50, 40),
                3: (10, 30),
                4: (5, 15),
                5: (1, 5),
            }
        elif _type == SpawnType.Hero:
            return {
                1: (100, 50),
                2: (50, 40),
                3: (10, 30),
                4: (5, 15),
                5: (1, 5),
            }
        elif _type == SpawnType.Relic:
            return {
                1: (100, 100),
                2: (40, 40),
                3: (30, 30),
                4: (15, 15),
                5: (2, 5),
            }
        elif _type == SpawnType.Fate:
            return {
                1: (100, 100),
                2: (40, 40),
                3: (30, 30),
                4: (15, 15),
                5: (2, 5),
            }
        elif _type == SpawnType.Room:
            return {
                1: (100, 100),
                2: (40, 60),
                3: (5, 20)
            }
        else:
            raise ValueError(
                f"Invalid spawn type |{_type}| provided to ObjectPool._base_weights()."
            )

################################################################################
