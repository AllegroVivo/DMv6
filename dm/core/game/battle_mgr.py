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
class DMHeroSpawner:

    __slots__ = (
        "_parent",
        "_spawn_cd",
        "_base_qty",
        "_scalar",
        "_flat_additional",
    )

    SPAWN_RATE = 2.0  # 1 hero spawned every 2 seconds

################################################################################
    def __init__(self, parent: DMBattleManager):

        self._parent: DMBattleManager = parent

        self._spawn_cd: float = 1.0  # Start this at 1 for timing purposes
        self._base_qty: int = 3
        self._scalar: float = 1.0
        self._flat_additional: int = 0

################################################################################
    def reset_cooldown(self) -> None:

        self._spawn_cd = self.SPAWN_RATE

################################################################################
    @property
    def game(self) -> DMGame:

        return self._parent.game

################################################################################
    @property
    def max_heroes(self) -> int:

        return int((self._base_qty * self._scalar) + self._flat_additional)

################################################################################
    def increase_base_count(self) -> None:

        self._base_qty += 1

################################################################################
    def scale(self, scalar: float) -> None:

        self._scalar += scalar

################################################################################
    def increase(self, amount: int) -> None:

        self._flat_additional += amount

################################################################################
    @property
    def finished_spawning(self) -> bool:

        return len(self.game.heroes) >= self.max_heroes

################################################################################
    def update(self, dt: float) -> None:

        if self.finished_spawning:
            return

        self._spawn_cd -= dt

        if self._spawn_cd <= 0.0:
            self.game.spawn_hero()
            self._spawn_cd = self.SPAWN_RATE

################################################################################
class DMBattleManager:

    __slots__ = (
        "_state",
        "_running",
        "_encounters",
        "_hero_spawner",
    )

################################################################################
    def __init__(self, state: DMGame):

        self._state: DMGame = state
        self._hero_spawner: DMHeroSpawner = DMHeroSpawner(self)

        self._running: bool = False
        self._encounters: List[Any] = []

################################################################################
    @property
    def game(self) -> DMGame:

        return self._state

################################################################################
    @property
    def running(self) -> bool:

        return self._running

################################################################################
    def update(self, dt: float) -> None:

        for encounter in self._encounters:
            if not encounter.in_progress:
                self._encounters.remove(encounter)
            else:
                encounter.update(dt)

        self._hero_spawner.update(dt)

        self.check_battle_over()

################################################################################
    def draw(self, screen: Surface) -> None:

        pass

################################################################################
    def start_battle(self, _type: str) -> None:

        self._running = True

################################################################################
    def engage(self, attacker: DMUnit, defender: DMUnit) -> None:

        # Maybe broadcast this as an event?

        attacker._opponent = defender
        defender._opponent = attacker

        self._encounters.append(DMEncounter(self.game, attacker, defender))

################################################################################
    def check_battle_over(self) -> None:

        if not self._hero_spawner.finished_spawning:
            return

        if any(e.in_progress for e in self._encounters):
            return

        if not any(h.is_alive for h in self.game.heroes):
            self.end_battle()

################################################################################
    def end_battle(self) -> None:

        print("Battle over!")
        self._running = False

################################################################################
