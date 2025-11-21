import re
import json
import os
from .config import Config

class TextProcessor:
    def __init__(self):
        self.config = Config()
        os.makedirs(self.config.PROCESSED_DIR, exist_ok=True)
        
        #Game specific abbreviations
        self.abbreviations = {
            'lvl': 'level',
            'def': 'defense', 
            'atk': 'attack',
            'dmg': 'damage',
            'hp': 'health',
            'exp': 'experience',
            'inv': 'inventory',
            'mob': 'monster',
            'npc': 'non-player character',
            'biome': 'environment type',
            'ench': 'enchantment',
            'pve': 'player versus environment',
            'pvp': 'player versus player'
        }
    
    def normalize_text(self, text):
        #Normalize and clean text
        #Lowercase
        text = text.lower()
        
        #Expand abbreviations
        words = text.split()
        expanded_words = []
        for word in words:
            if word in self.abbreviations:
                expanded_words.append(self.abbreviations[word])
            else:
                expanded_words.append(word)
        text = ' '.join(expanded_words)
        
        #Remove extra whitespace and punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def segment_content(self, wiki_data):
        #Segment wiki content into chunks
        segments = []
        
        for page_title, sections in wiki_data.items():
            for section_title, section_content in sections.items():
                #Combine section content
                full_text = " ".join(section_content)
                
                #Split into manageable chunks
                chunks = self._split_into_chunks(full_text)
                
                for i, chunk in enumerate(chunks):
                    if len(chunk) >= self.config.MIN_TEXT_LENGTH:
                        segment = {
                            'id': f"{page_title}_{section_title}_{i}",
                            'page': page_title,
                            'section': section_title,
                            'content': chunk,
                            'normalized_content': self.normalize_text(chunk),
                            'length': len(chunk)
                        }
                        segments.append(segment)
        
        return segments
    
    def _split_into_chunks(self, text, max_length=500):
        #Split text into chunks of maximum length
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def process_all_data(self):
        #Process all scraped wiki data
        raw_file = os.path.join(self.config.RAW_DIR, "all_wiki_data.json")
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            wiki_data = json.load(f)
        
        segments = self.segment_content(wiki_data)
        
        #Save processed data
        output_file = os.path.join(self.config.PROCESSED_DIR, "processed_segments.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=2, ensure_ascii=False)
        
        print(f"Processed {len(segments)} text segments")
        return segments