import os

class Config:
    #Wiki settings
    WIKI_BASE_URL = "https://minecraft.wiki/api.php"
    WIKI_PAGES = [
        "Minecraft",
        "Gameplay",
        "Items",
        "Blocks", 
        "Mobs",
        "Crafting",
        "Biomes",
        "Enchanting",
        "Redstone",
        "Commands"
    ]
    
    #Processing settings
    MIN_TEXT_LENGTH = 50
    MAX_TEXT_LENGTH = 1000
    
    #Model settings
    OLLAMA_MODEL = "deepseek-r1:7b"
    EMBEDDING_MODEL = "nomic-embed-text"
    
    #Paths
    DATA_DIR = "data"
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")