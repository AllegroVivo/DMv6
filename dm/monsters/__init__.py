from typing     import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from ..core.objects.monster     import DMMonster
################################################################################

__all__ = ("ALL_MONSTERS", )

################################################################################
from .OneStar       import *

from .Tester        import Tester
################################################################################
# All Monsters
ALL_MONSTERS: List[Type["DMMonster"]] = [
    # 1-Star
    Bat, Goblin, Imp, Slime, Tester,

    # 2-Star
    # DarkSlime, Gargoyle, Harpy, HellHound, Lizardman, Mimic, Orc, Sahuagin,
    # Salamander, Skull, Zombie,
    #
    # # 3-Star
    # Cerberus, DireWolf, Dullahan, EntGirl, GargoyleGirl, GoblinGirl, Golem,
    # HellfireImp, HellHoundGirl, HighOrc, Honeybee, ImpGirl, KingSlime,
    # LizardmanGirl, Minotaur, MinotaurGirl, Mummy, Nightmare, NymphGirl, Ogre,
    # OrcGirl, SalamanderGirl, Siren, SkullHound, SkullKnight, SlimeGirl,
    #
    # # 4-Star
    # BlackKnightGirl, Cyclops, Ent, FireWolf, GhoulGirl, IceGolem, Lich,
    # MinotaurKing, NagaGirl, NightmareGirl, Phoenix, Reaper, Shadowmere,
    # SuccubusGirl, VampireGirl, WaterGolem, Werewolf, Zealot,
    #
    # # 5-Star
    # AncientMummy, Druid, IfritGirl, LavaGolem, LichGirl, LightningDrake,
    # LightningWolf, MedusaGirl, PhoenixGirl, ReaperGirl, SeaDrake, WispGirl,
    #
    # # 6-Star
    # Arachne, Baphomet, BoneDragon, Cleopatra, DeathKnight, Dryanid, Fairy,
    # RedWyvern, Sephiroth, Shiva, Suparna, Thetis, WhiteFang, SeedOfNature,
    # SeedOfFire, SeedOfWater, SeedOfLight, SeedOfDarkness,
    #
    # # 7-Star
    # AncientDruid, Crow, DimensionGirl, DragonMiko, Ignis, Kirin,
    # MessengerOfTheSky, SoulHarvester, CorruptedNatureElemental,
    # CorruptedShadowElemental, CorruptedWaterElemental, CorruptedFireElemental,
    # CorruptedLightElemental,
    #
    # # 8-Star
    # CorruptedGrandShadowElemental, CorruptedGrandNatureElemental,
    # CorruptedGrandWaterElemental, CorruptedGrandFireElemental,
    # CorruptedGrandLightElemental,
    #
    # # 9-Star
    # # <None?>
    #
    # # 10-Star
    # CorruptedLordOfFire, CorruptedLordOfLight, CorruptedLordOfNature,
    # CorruptedLordOfShadow, CorruptedLordOfWater
]
################################################################################
