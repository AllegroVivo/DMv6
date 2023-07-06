from __future__ import annotations

from pygame     import Surface
from typing     import TYPE_CHECKING, Any, List

from .encounter import DMEncounter
from .contexts import AttackContext
from utilities  import FateType, ArgumentTypeError

if TYPE_CHECKING:
    from dm.core.game.game import DMGame
    from dm.core.objects.hero import DMHero
    from dm.core.objects.unit import DMUnit
################################################################################

__all__ = ("DMBattleManager", )

################################################################################
class DMBattleManager:

    __slots__ = (
        "_state",
        "_encounters",
    )

################################################################################
    def __init__(self, state: DMGame):

        self._state: DMGame = state
        self._encounters: List[Any] = []

################################################################################
    @property
    def game(self) -> DMGame:

        return self._state

################################################################################
    def update(self, dt: float) -> None:

        for encounter in self._encounters:
            encounter.update(dt)

################################################################################
    def draw(self, screen: Surface) -> None:

        pass

################################################################################
    def engage(self, attacker: DMUnit, defender: DMUnit) -> None:

        # Maybe broadcast this as an event?
        self._encounters.append(DMEncounter(self.game, attacker, defender))

################################################################################
    def remove_encounter(self, encounter: DMEncounter) -> None:

        self._encounters.remove(encounter)

################################################################################
