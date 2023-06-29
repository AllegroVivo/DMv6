from typing     import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from ..core.objects.room    import DMRoom
################################################################################

__all__ = ("ALL_ROOMS", )

################################################################################
# Packages
from .OneStar       import *
# from .TwoStar       import *
# from .ThreeStar     import *

from .special       import *
################################################################################
# All Rooms
ALL_ROOMS: List[Type["DMRoom"]] = [
    # Special (0-Star)
    BossRoom, EmptyRoom, EntranceRoom,

    # 1-Star
    Battle  # Arena, Arrow, Barrier, Battle, Ice, Pit, Rockslide,

    # 2-Star
    # Ambush, Betrayal, BloodAltar, Darkness, Distortion, Excess, Frenzy, Guillotine,
    # Hatchery, Hunger, Ignition, Incineration, IronMaiden, Meditation, PanicRoom,
    # Rage, Return, Sloth, Solitude, Sprout, SwordAndShield, Venom,

    # 3-Star

]

################################################################################
