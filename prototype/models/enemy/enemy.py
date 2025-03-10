from enum import Enum
from models.badge.badge import Badge
from dataclasses import dataclass

class Enemy:
    def __init__(self, id: int, name: str, description: str, health: int):
        self.id = id
        self.name = name
        self.description = description
        self.health = health
    
    def attack(self):
        pass

    def drop_badge(self):
        return Badge("Dragon Slayer", "Legendary")
    
    def to_dict(self):
        """Convert the enemy object to a dictionary."""
        enemy_type = EnemyType.get_by_name(self.name)  # Use helper function
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "file_name": enemy_type.file_name if enemy_type else None  # Handle missing cases safely
        }

@dataclass(frozen=True)
class EnemyData:
    file_name: str
    monster_name: str

class EnemyType(Enum):
    OBSIDIAN_WARLORD = EnemyData("obsidian_warlord.png", "Obsidian Warlord")
    SHADOW_STRIKER = EnemyData("shadow_striker.png", "Shadow Striker")
    BONE_HARBINGER = EnemyData("bone_harbinger.png", "Bone Harbinger")
    ECLIPSE_PHANTOM = EnemyData("eclipse_phantom.png", "Eclipse Phantom")
    SKELETAL_SPEARMAN = EnemyData("skeletal_spearman.png", "Skeletal Spearman")
    NOSFEROS = EnemyData("nosferos.png", "Nosferos")
    INFERNAL_JUGGERNAUT = EnemyData("infernal_juggernaut.png", "Infernal Juggernaut")
    CRIMSON_IMP = EnemyData("crimson_imp.png", "Crimson Imp")
    HELLHOUND = EnemyData("hellhound.png", "Hellhound")
    ABYSSAL_FIEND = EnemyData("abyssal_fiend.png", "Abyssal Fiend")
    FLAME_SERPENT = EnemyData("flame_serpent.png", "Flame Serpent")
    SKULL_INFERNO = EnemyData("skull_inferno.png", "Skull Inferno")
    FOREST_BEAST = EnemyData("forest_beast.png", "Forest Beast")
    DARK_RAVEN = EnemyData("dark_raven.png", "Dark Raven")
    BERSERKER_DWARF = EnemyData("berserker_dwarf.png", "Berserker Dwarf")
    MAD_ORC = EnemyData("mad_orc.png", "Mad Orc")
    SNOW_YETI = EnemyData("snow_yeti.png", "Snow Yeti")
    VENOM_COBRA = EnemyData("venom_cobra.png", "Venom Cobra")
    DEMON_WARRIOR = EnemyData("demon_warrior.png", "Demon Warrior")
    ANCIENT_DRAGON = EnemyData("ancient_dragon.png", "Ancient Dragon")
    DJINN_MYSTIC = EnemyData("djinn_mystic.png", "Djinn Mystic")
    GOLDEN_DEVOURER = EnemyData("golden_devourer.png", "Golden Devourer")
    MEDUSA_ENCHANTRESS = EnemyData("medusa_enchantress.png", "Medusa Enchantress")
    WYRMLING_DRAKE = EnemyData("wyrmling_drake.png", "Wyrmling Drake")

    @classmethod
    def get_by_name(cls, name: str) -> EnemyData:
        """Find an EnemyType based on monster_name."""
        for enemy in cls:
            if enemy.value.monster_name.lower() == name.lower():
                return enemy.value
        return None  # Handle cases where no match is found

