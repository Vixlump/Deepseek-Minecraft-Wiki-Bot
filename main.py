import os
import argparse
from src.scraper import WikiScraper
from src.processor import TextProcessor
from src.embeddings import EmbeddingsGenerator
from src.chatbot import MinecraftChatbot

def main():
    parser = argparse.ArgumentParser(description='Minecraft Wiki Chatbot')
    parser.add_argument('--setup', action='store_true', help='Setup the chatbot')
    parser.add_argument('--chat', action='store_true', help='Start chat interface')
    
    args = parser.parse_args()
    
    if args.setup:
        print("Setting up Minecraft Wiki Chatbot")
        
        #Step 1: Scrape wiki data
        print("Step 1: Scraping wiki data")
        scraper = WikiScraper()
        wiki_data = scraper.scrape_all_pages()
        
        #Step 2: Process data
        print("Step 2: Processing text data")
        processor = TextProcessor()
        segments = processor.process_all_data()
        
        #Step 3: Generate embeddings
        print("Step 3: Generating embeddings")
        generator = EmbeddingsGenerator()
        embeddings = generator.generate_embeddings(segments)
        
        print("Setup complete!")
    
    if args.chat:
        print("Starting Minecraft Wiki Chatbot")
        chatbot = MinecraftChatbot()
        chatbot.chat()

if __name__ == "__main__":
    main()