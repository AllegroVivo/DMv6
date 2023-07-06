from __future__ import annotations

from typing     import (
    TYPE_CHECKING,
    Optional,
    TypeVar,
    Union
)

from .context  import DMContext
from utilities  import *

if TYPE_CHECKING:
    from ..game import DMGame
    from ...objects.unit import DMUnit
    from ...objects.room import DMRoom
################################################################################

__all__ = ("AttackContext", )

CTX = TypeVar("CTX", bound="AttackContext")

################################################################################
class DamageComponent:

    __slots__ = (
        "_base",
        "_scalar",
        "flat_increase",
        "_damage_override",
        "_total"
    )

################################################################################
    def __init__(self, damage: int):

        self._base: int = damage
        self._scalar: float = 1.0
        self.flat_increase: int = 0

        self._damage_override: Optional[int] = None

        self._total: int = None  # type: ignore

################################################################################
    def scale_damage(self, scalar: float) -> None:

        if not isinstance(scalar, float):
            raise ArgumentTypeError(
                "AttackContext.scale_damage()",
                type(scalar),
                type(float)
            )

        self._scalar += scalar

################################################################################
    def increase_damage(self, amount: Union[int, float]) -> None:

        if not isinstance(amount, (int, float)):
            raise ArgumentTypeError(
                "AttackContext.reduce_damage()",
                type(amount),
                type(int)
            )

        self.flat_increase += int(amount)

################################################################################
    def override(self, amount: Union[int, float]) -> None:

        if not isinstance(amount, (int, float)):
            raise ArgumentTypeError(
                "AttackContext.override_damage()",
                type(amount),
                type(int)
            )

        self._damage_override = int(amount)

################################################################################
    def calculate(self) -> int:

        if self._damage_override is not None:
            self._total = self._damage_override
        else:
            damage = self._base if self._total is None else self._total
            self._total = max(int((damage * self._scalar) + self.flat_increase), 0)

        return self._total

################################################################################
class AttackContext(DMContext):

    __slots__ = (
        "_source",
        "_target",
        "_damage",
        "_fail",
    )

################################################################################
    def __init__(
        self,
        state: DMGame,
        attacker: Union[DMUnit],
        defender: DMUnit,
        base_damage: Optional[int] = None
    ):

        super().__init__(state)

        self._source: Union[DMUnit] = attacker
        self._target: DMUnit = defender

        if base_damage is None:
            try:
                base_damage = self._source.attack
            except AttributeError:
                raise ArgumentMissingError("AttackContext.__init__()", "base_damage", type(int))

        self._damage: DamageComponent = DamageComponent(base_damage)
        self._fail: bool = False

################################################################################
    def __repr__(self) -> str:

        return(
            "<AttackContext:\n"
            f"attacker: {self.source}, defender: {self.target}\n"
            f"cur dmg: {self.damage}>"
        )

################################################################################
    def __eq__(self, other: AttackContext) -> bool:

        return self._id == other._id

################################################################################
    @property
    def damage(self) -> int:

        if self._fail:
            return 0

        return self._damage.calculate()

################################################################################
    @property
    def room(self) -> DMRoom:

        return self._source.room

################################################################################
    @property
    def source(self) -> Union[DMUnit]:

        return self._source

################################################################################
    @property
    def target(self) -> DMUnit:

        return self._target

################################################################################
    def override_damage(self, amount: Union[int, float]) -> None:

        self._damage.override(amount)

################################################################################
    def execute(self) -> None:

        if not self.will_fail:
            self.source.play_attack_animation()
            self.target.damage(self.damage)

################################################################################
    def scale_damage(self, scalar: float) -> None:

        self._damage.scale_damage(scalar)

################################################################################
    def increase_damage_flat(self, amount: int) -> None:

        self._damage.increase_damage(amount)

################################################################################
    def reduce_damage_flat(self, amount: int) -> None:

        self._damage.increase_damage(-amount)

################################################################################
    @property
    def will_fail(self) -> bool:

        return self._fail or self.damage == 0

################################################################################
    @will_fail.setter
    def will_fail(self, value: bool) -> None:

        if not isinstance(value, bool):
            raise ArgumentTypeError(
                "AttackContext.will_fail",
                type(value),
                type(bool)
            )

        self._fail = value

################################################################################
    def would_kill(self, unit: Optional[DMUnit] = None) -> bool:

        if not isinstance(unit, DMUnit):
            raise ArgumentTypeError("AttackContext.would_kill()", type(unit), type(DMUnit))

        # If the attack is already marked to fail, we can just return.
        if self.will_fail:
            return False

        # Select the CTX's defender as the default check.
        if unit is None:
            unit = self.target

        return unit.life + unit.defense - self.damage <= 0

################################################################################
    def redirect(self, new_target: DMUnit) -> None:

        self._target = new_target

################################################################################
