from __future__ import annotations

from typing import Type, Union

from utilities import *
################################################################################

__all__ = ("StatComponent", "UnitStats")

################################################################################
class StatComponent:

    __slots__ = (
        "__base",
        "_flat_additional",
        "_scalar",
        "_current",
        "_max",  # Only used for LifeComponent
        "_type"
    )

################################################################################
    def __init__(self, base: Union[int, float], _type: StatComponentType):

        self.__base: float = float(base)

        self._current: float = float(base)
        self._max: float = float(base)

        self._type: StatComponentType = _type

        self._flat_additional: int = 0
        self._scalar: float = 1.0

################################################################################
    def _copy(self) -> StatComponent:

        return StatComponent(self.__base, self._type)

################################################################################
    def scale(self, scalar: Union[int, float]) -> None:

        if not isinstance(scalar, (int, float)):
            raise ArgumentTypeError(
                "StatComponent.scale()",
                type(scalar),
                type(int), type(float)
            )

        self._scalar += float(scalar)

################################################################################
    def increase(self, amount: Union[int, float]) -> None:

        if not isinstance(amount, (int, float)):
            raise ArgumentTypeError(
                "StatComponent.modify()",
                type(amount),
                type(int), type(float)
            )

        self._flat_additional += int(amount)

################################################################################
    def calculate(self) -> None:

        self._current = (self._current * self._scalar) + self._flat_additional
        self.reset()

################################################################################
    @property
    def current(self) -> float:

        self.calculate()
        return self._current

################################################################################
    def damage(self, amount: int) -> None:

        if not self._type == StatComponentType.Life:
            raise ValueError("Cannot damage a non-life StatComponent.")

        self._current = max(self._current - amount, 0)

################################################################################
    def heal(self, amount: int) -> None:

        if not self._type == StatComponentType.Life:
            raise ValueError("Cannot heal a non-life StatComponent.")

        self._current = min(self._current + amount, self._max)

################################################################################
    def reset(self) -> None:

        self._scalar = 1.0
        self._flat_additional = 0

################################################################################
class UnitStats:

    __slots__ = (
        "_life",
        "_attack",
        "_defense",
        "_dex",
        "_combat",
        "_num_attacks",
        "_move_speed"
    )

################################################################################
    def __init__(self, life: int, attack: int, defense: float):

        self._life: StatComponent = StatComponent(life, StatComponentType.Life)
        self._attack: StatComponent = StatComponent(attack, StatComponentType.Attack)
        self._defense: StatComponent = StatComponent(defense, StatComponentType.Defense)
        self._dex: StatComponent = StatComponent(1.0, StatComponentType.Dex)
        self._combat: StatComponent = StatComponent(1.0, StatComponentType.Combat)
        self._num_attacks: StatComponent = StatComponent(1, StatComponentType.NumAttacks)
        self._move_speed: StatComponent = StatComponent(1.0, StatComponentType.Speed)

################################################################################
    @property
    def life(self) -> int:

        return int(self._life.current)

################################################################################
    @property
    def max_life(self) -> int:

        return int(self._life._max)

################################################################################
    def damage(self, amount: int) -> None:

        self._life.damage(amount)

################################################################################
    def heal(self, amount: int) -> None:

        self._life.heal(amount)

################################################################################
    @property
    def attack(self) -> int:

        return int(self._attack.current)

################################################################################
    @property
    def defense(self) -> float:

        return self._defense.current

################################################################################
    @property
    def dex(self) -> float:

        return self._dex.current

################################################################################
    @property
    def combat(self) -> float:

        return self._combat.current

################################################################################
    @property
    def num_attacks(self) -> int:

        return int(self._num_attacks.current)

################################################################################
    @property
    def move_speed(self) -> float:

        return self._move_speed.current

###############################################################################
    def scale_stat(self, stat: str, scalar: Union[int, float]) -> None:

        if not isinstance(scalar, (int, float)):
            raise ArgumentTypeError(
                "BaseStats.scale_stat()",
                type(scalar),
                type(int), type(float)
            )

        match stat:
            case "attack":
                self._attack.scale(scalar)
            case "defense":
                self._defense.scale(scalar)
            case "dex":
                self._dex.scale(scalar)
            case "combat":
                self._combat.scale(scalar)
            case "num_attacks":
                self._num_attacks.scale(scalar)
            case "speed":
                self._move_speed.scale(scalar)
            case _:
                raise ValueError(f"Invalid stat: {stat}")

################################################################################
    def _copy(self) -> UnitStats:

        copy = type(self).__new__(type(self))

        copy._life = self._life._copy()
        copy._attack = self._attack._copy()
        copy._defense = self._defense._copy()
        copy._dex = self._dex._copy()
        copy._combat = self._combat._copy()
        copy._num_attacks = self._num_attacks._copy()

        return copy

################################################################################
