from __future__ import annotations

from typing     import TYPE_CHECKING, List
from uuid       import UUID, uuid4

from .contexts.attack  import AttackContext

if TYPE_CHECKING:
    from ..game.game    import DMGame
    from ..objects.unit import DMUnit
################################################################################

__all__ = ("DMEncounter",)

################################################################################
class DMEncounter:

    __slots__ = (
        "_id",
        "_state",
        "_unit1",
        "_unit2",
        "_attacks",
        "_unit1_action_cd",
        "_unit2_action_cd",
        "_final_cd",
        "_in_progress",
    )

################################################################################
    def __init__(self, state: DMGame, unit1: DMUnit, unit2: DMUnit):

        self._id: UUID = uuid4()
        self._state: DMGame = state

        self._in_progress: bool = True

        self._unit1: DMUnit = unit1
        self._unit2: DMUnit = unit2

        self._unit1_action_cd: float = 1.0
        self._unit2_action_cd: float = 0.5
        self._final_cd: float = 1.0

        self._attacks: List[AttackContext] = []

################################################################################
    def __eq__(self, other: DMEncounter) -> bool:

        return self._id == other._id

################################################################################
    @property
    def game(self) -> DMGame:

        return self._state

################################################################################
    @property
    def unit1(self) -> DMUnit:

        return self._unit1

################################################################################
    @property
    def unit2(self) -> DMUnit:

        return self._unit2

################################################################################
    def update(self, dt: float) -> None:

        # Decrement cooldown timers
        self._unit1_action_cd -= dt * self._unit1.dex
        self._unit2_action_cd -= dt * self._unit2.dex

        if self._unit1_action_cd <= 0:
            ctx = self.attack(self._unit1, self._unit2)
            self._unit1_action_cd = 1.0  # Reset cooldown timer

            if not self._unit1.is_alive or not self._unit2.is_alive:
                self.disengage(ctx)

        if self._unit2_action_cd <= 0:
            ctx = self.attack(self._unit2, self._unit1)
            self._unit2_action_cd = 1.0  # Reset cooldown timer

            if not self._unit1.is_alive or not self._unit2.is_alive:
                self.disengage(ctx)

        if len(self._attacks) >= 6:  # 24 == 12 rounds worth of attacks (1 per unit).
            self.disengage(self._attacks[-1])
            return

################################################################################
    def attack(self, attacker: DMUnit, defender: DMUnit) -> AttackContext:

        ctx = AttackContext(self.game, attacker, defender)

        self.game.dispatch_event("on_attack", ctx)

        ctx.execute()
        self._attacks.append(ctx)

        return ctx

################################################################################
    def disengage(self, ctx: AttackContext) -> None:

        print("Disengaging encounter")

        if not ctx.source.is_alive or not ctx.target.is_alive:
            self.game.dispatch_event("on_death", ctx)

        self._unit1.disengage()
        self._unit2.disengage()

        self._in_progress = False

################################################################################
