import os

# Mapping of original file names to new formatted names
name_map = {
    "con19.png": "obsidian_warlord.png",
    "con20.png": "shadow_striker.png",
    "con21.png": "bone_harbinger.png",
    "con22.png": "eclipse_phantom.png",
    "con23.png": "skeletal_spearman.png",
    "con24.png": "nosferos.png",
    "con25.png": "infernal_juggernaut.png",
    "con26.png": "crimson_imp.png",
    "con27.png": "hellhound.png",
    "con28.png": "abyssal_fiend.png",
    "con29.png": "flame_serpent.png",
    "con30.png": "skull_inferno.png",
    "con31.png": "forest_beast.png",
    "con32.png": "dark_raven.png",
    "con33.png": "berserker_dwarf.png",
    "con34.png": "mad_orc.png",
    "con35.png": "snow_yeti.png",
    "con36.png": "venom_cobra.png",
    "con37.png": "demon_warrior.png",
    "con38.png": "ancient_dragon.png",
    "Flame Serpent": "flame_serpent.png",
    "Skull Inferno": "skull_inferno.png",
    "Forest Beast": "forest_beast.png",
    "Dark Raven": "dark_raven.png",
    "Berserker Dwarf": "berserker_dwarf.png",
    "Mad Orc": "mad_orc.png",
    "Snow Yeti": "snow_yeti.png",
    "Venom Cobra": "venom_cobra.png",
    "Demon Warrior": "demon_warrior.png",
    "Ancient Dragon": "ancient_dragon.png",
    "con39.png": "djinn_mystic.png",
    "con40.png": "golden_devourer.png",
    "con41.png": "medusa_enchantress.png",
    "con42.png": "wyrmling_drake.png"
}

# Folder containing the images (Change this if needed)
folder_path = "./"  # Current directory

# Rename files
for old_name, new_name in name_map.items():
    # old_path = os.path.join(folder_path, old_name)
    # new_path = os.path.join(folder_path, new_name)

    # if os.path.exists(old_path):  # Check if the file exists
    #     os.rename(old_path, new_path)
    #     print(f"Renamed: {old_name} ➝ {new_name}")
    # else:
    #     print(f"File not found: {old_name}")
    print(new_name)

print("✅ Renaming complete!")
