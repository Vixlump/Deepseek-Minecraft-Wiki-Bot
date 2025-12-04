import os

class Config:
    #Wiki settings
    WIKI_BASE_URL = "https://minecraft.wiki/api.php"
    WIKI_PAGES = [
        # Core game
        "Minecraft",
        "Gameplay",
        "History",
        "Development",
        "Java Edition",
        "Bedrock Edition",
        "Editions",

        # Player mechanics
        "Player",
        "Health",
        "Hunger",
        "Experience",
        "Leveling",
        "Movement",
        "Status Effects",
        "Death",
        "Spawn",

        # World & environment
        "Overworld",
        "Nether",
        "End",
        "Biomes",
        "Dimensions",
        "World generation",
        "Terrain",
        "Weather",
        "Light",
        "Time",
        "Difficulty",
        "Hardcore mode",
        "Adventure mode",
        "Spectator mode",

        # Blocks
        "Blocks",
        "Block entity",
        "Natural blocks",
        "Generated blocks",
        "Technical blocks",
        "Decorative blocks",
        "Utility blocks",
        "Redstone blocks",
        "Light blocks",

        # Items & mechanics
        "Items",
        "Tools",
        "Weapons",
        "Armor",
        "Food",
        "Materials",
        "Raw materials",
        "Farming Materials",
        "Music Discs",
        "Potions",
        "Arrows",
        "Books",
        "Fireworks",
        "Transport items",
        "Throwable items",

        # Crafting & systems
        "Crafting",
        "Smelting",
        "Blasting",
        "Smoking",
        "Stonecutting",
        "Smithing",
        "Anvil",
        "Loom",
        "Cartography Table",
        "Enchanting",
        "Brewing",
        "Furnace",
        "Fletching Table",
        "Grindstone",
        "Composter",

        # Redstone & technical
        "Redstone",
        "Redstone mechanics",
        "Power",
        "Redstone components",
        "Pistons",
        "Observers",
        "Hoppers",
        "Minecarts",
        "Rails",
        "Note Blocks",
        "Command Blocks",
        "Structure Blocks",
        "Functions",
        "Scoreboards",

        # Mobs
        "Mobs",
        "Passive mobs",
        "Neutral mobs",
        "Hostile mobs",
        "Boss mobs",
        "Utility mobs",
        "Breedable mobs",
        "Taming",
        "Spawning",
        "Mob AI",
        "Villager",
        "Villager professions",
        "Raids",
        "Wandering Trader",

        # Exploration & environment
        "Structures",
        "Generated structures",
        "Villages",
        "Dungeons",
        "Mineshafts",
        "Strongholds",
        "Ocean monuments",
        "Shipwrecks",
        "Ruined portals",
        "Bastions",
        "Fortresses",
        "Ancient Cities",
        "Trial Chambers",

        # Trading & economy
        "Trading",
        "Economy",
        "Bartering",
        "Loot tables",
        "Treasure",

        # Game systems
        "Commands",
        "Command syntax",
        "Game rules",
        "Options",
        "World border",
        "Difficulty settings",

        # UI & interaction
        "Inventory",
        "HUD",
        "Controls",
        "Accessibility options",
        "Chat",
        "Advancements",
        "Statistics",
        "Achievements (Legacy)",

        # Survival & progression
        "Mining",
        "Farming",
        "Fishing",
        "Hunting",
        "Building",
        "Exploring",
        "Combat",
        "Defense",
        "Navigation",

        # Transportation
        "Boats",
        "Minecarts",
        "Horses",
        "Elytra",
        "Nether travel",
        "Maps",

        # Community & meta
        "Servers",
        "Multiplayer",
        "Realms",
        "Resource packs",
        "Data packs",
        "Mods",
        "Snapshots",
        "Speedrunning",
        "Technical Minecraft",
        "Hardcore community",
        "Adventure maps",

        # Tutorials
        "Tutorials",

        # Miscellaneous & deep knowledge
        "Music",
        "Soundtrack",
        "Trivia",
        "Lore",
        "Unused features",
        "Removed features",
        "Technical details",
        "Chunk",
        "Tick",
        "Game engine",
        "NBT format",
        "Resource locations",
        "Server.properties"
    ]

    
    #Processing settings
    MIN_TEXT_LENGTH = 50
    MAX_TEXT_LENGTH = 1000
    
    #Model settings
    OLLAMA_MODEL = "deepseek-r1:14b"
    EMBEDDING_MODEL = "nomic-embed-text"
    
    #Paths
    DATA_DIR = "data"
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")