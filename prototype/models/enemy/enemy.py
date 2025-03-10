from enum import Enum
from models.badge.badge import Badge

class Enemy:
    def __init__(self, id: int, name: str, health: int):
        self.id = id
        self.name = name
        self.health = health
    
    def attack(self):
        pass

    def hurt(self, damage: int):
        pass

    def drop_badge():
        return Badge("Dragon Slayer", "Legendary")


class EnemyType(Enum):
    OBSIDIAN_WARLORD = "obsidian_warlord"
    SHADOW_STRIKER = "shadow_striker"
    BONE_HARBINGER = "bone_harbinger"
    ECLIPSE_PHANTOM = "eclipse_phantom"
    SKELETAL_SPEARMAN = "skeletal_spearman"
    NOSFEROS = "nosferos"
    INFERNAL_JUGGERNAUT = "infernal_juggernaut"
    CRIMSON_IMP = "crimson_imp"
    HELLHOUND = "hellhound"
    ABYSSAL_FIEND = "abyssal_fiend"
    FLAME_SERPENT = "flame_serpent"
    SKULL_INFERNO = "skull_inferno"
    FOREST_BEAST = "forest_beast"
    DARK_RAVEN = "dark_raven"
    BERSERKER_DWARF = "berserker_dwarf"
    MAD_ORC = "mad_orc"
    SNOW_YETI = "snow_yeti"
    VENOM_COBRA = "venom_cobra"
    DEMON_WARRIOR = "demon_warrior"
    ANCIENT_DRAGON = "ancient_dragon"
    DJINN_MYSTIC = "djinn_mystic"
    GOLDEN_DEVOURER = "golden_devourer"
    MEDUSA_ENCHANTRESS = "medusa_enchantress"
    WYRMLING_DRAKE = "wyrmling_drake"
