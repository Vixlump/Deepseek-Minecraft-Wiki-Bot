import ollama
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from .config import Config
from .embeddings import EmbeddingsGenerator

class MinecraftChatbot:
    def __init__(self):
        self.config = Config()
        self.embeddings_data = None
        self.embeddings_matrix = None
        
    def load_embeddings(self):
        #Load embeddings for similarity search
        #Import inside the method to avoid circular imports
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from src.embeddings import EmbeddingsGenerator
        
        generator = EmbeddingsGenerator()
        self.embeddings_data = generator.load_embeddings()
        
        #Create embeddings matrix
        self.embeddings_matrix = np.array([item['embedding'] for item in self.embeddings_data])
    
    def find_relevant_context(self, query, top_k=3):
        #Find most relevant context for user query
        if self.embeddings_data is None:
            self.load_embeddings()
        
        #Generate query embedding
        try:
            response = ollama.embeddings(
                model=self.config.EMBEDDING_MODEL,
                prompt=query
            )
            query_embedding = np.array(response['embedding']).reshape(1, -1)
            
            #Calculate similarities
            similarities = cosine_similarity(query_embedding, self.embeddings_matrix)[0]
            
            #Get top matches
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            relevant_contexts = []
            
            for idx in top_indices:
                if similarities[idx] > 0.1:  #Similarity threshold
                    relevant_contexts.append({
                        'content': self.embeddings_data[idx]['content'],
                        'page': self.embeddings_data[idx]['page'],
                        'section': self.embeddings_data[idx]['section'],
                        'similarity': float(similarities[idx])
                    })
            
            return relevant_contexts
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    def generate_response(self, query, context):
        #Generate response using Ollama with context
        #Prepare context string
        context_str = "\n\n".join([f"From {ctx['page']} - {ctx['section']}:\n{ctx['content']}" 
                                 for ctx in context])
        
        prompt = f"""You are a helpful Minecraft wiki assistant. Use the following context to answer the user's question accurately and concisely.

Context:
{context_str}

User Question: {query}

STRICT RULES (FOLLOW EXACTLY):
1. **Use ONLY the provided context.**
   - If a detail is not in the context, do NOT invent or guess it.
   - Ignore any outside Minecraft knowledge you may have.

2. **If the context does not fully answer the question:**
   - Say: "I don't know based on the provided context."
   - OR: "The provided context does not include enough information to answer this."
   - Never fabricate missing details.

3. **No speculation or assumptions.**
   - No guessing items, mechanics, steps, values, or features.
   - Avoid words like "probably", "maybe", or "it might".

4. **Stay strictly within Minecraft.**
   - If the context doesn’t talk about a mechanic, item, mob, or process, don’t discuss it.

5. **Multi-part questions:**
   - Answer only the parts supported by context.
   - Clearly state which parts cannot be answered.

6. **No chain-of-thought or internal reasoning.**
   - Provide only the final answer.

ANSWER FORMAT:
- Start with a direct answer.
- If helpful, add a short explanation referencing the context.
- If unknown, clearly state it.

Now produce the best possible answer **following all rules above**.
"""
        
        try:
            response = ollama.generate(
                model=self.config.OLLAMA_MODEL,
                prompt=prompt,
                options={
                    'temperature': 0.3,
                    'top_k': 40,
                    'top_p': 0.9,
                }
            )
            
            return response['response']
            
        except Exception as e:
            return f"Error generating response: {e}"
    
    def chat(self):
        #Start interactive chat session
        print("Minecraft Wiki Chatbot initialized!")
        print("Type 'quit' to exit, 'reset' to clear conversation")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                elif user_input.lower() == 'reset':
                    print("Conversation reset.")
                    continue
                
                #Find relevant context
                print("Searching wiki...")
                context = self.find_relevant_context(user_input)
                
                if not context:
                    print("Bot: I couldn't find relevant information in the wiki for that question.")
                    continue
                
                #Generate response
                print("Generating response...")
                response = self.generate_response(user_input, context)
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")