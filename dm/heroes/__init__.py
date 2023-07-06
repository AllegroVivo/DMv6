from typing     import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from dm.core.objects.hero    import DMHero
################################################################################

__all__ = ("ALL_HEROES", )

################################################################################
# Basic
from .normal    import *
################################################################################

ALL_HEROES: List[Type["DMHero"]] = [
    # 1-Star
    Farmer, Villager,

    # 2-Star
    # Adventurer, Archer, Rogue, Wizard,
    #
    # # 3-Star
    # Bard, Guard, Priest, Swordsman,
    #
    # # 4-Star
    # Berserker, Knight, Monk,
    #
    # # 5-Star
    # Assassin, Paladin, RoyalGuard,
    #
    # # 6 & 7-Star
    # Angel, DragonSlayer
]

################################################################################
