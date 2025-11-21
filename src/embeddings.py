import ollama
import json
import numpy as np
import os
from .config import Config

class EmbeddingsGenerator:
    def __init__(self):
        self.config = Config()
        os.makedirs(self.config.EMBEDDINGS_DIR, exist_ok=True)
    
    def generate_embeddings(self, segments):
        #Generate embeddings for text segments
        embeddings_data = []
        
        for i, segment in enumerate(segments):
            print(f"Generating embedding {i+1}/{len(segments)}")
            
            try:
                #Generate embedding using Ollama
                response = ollama.embeddings(
                    model=self.config.EMBEDDING_MODEL,
                    prompt=segment['normalized_content']
                )
                
                embedding = response['embedding']
                
                embeddings_data.append({
                    'id': segment['id'],
                    'page': segment['page'],
                    'section': segment['section'],
                    'content': segment['content'],
                    'embedding': embedding
                })
                
            except Exception as e:
                print(f"Error generating embedding for {segment['id']}: {e}")
                continue
        
        #Save embeddings
        output_file = os.path.join(self.config.EMBEDDINGS_DIR, "wiki_embeddings.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
        
        return embeddings_data
    
    def load_embeddings(self):
        #Load pre-generated embeddings
        embeddings_file = os.path.join(self.config.EMBEDDINGS_DIR, "wiki_embeddings.json")
        
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            return json.load(f)