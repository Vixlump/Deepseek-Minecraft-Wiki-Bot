import requests
import json
import os
from bs4 import BeautifulSoup
from .config import Config

class WikiScraper:
    def __init__(self):
        self.config = Config()
        os.makedirs(self.config.RAW_DIR, exist_ok=True)
        
    def scrape_page(self, page_title):
        #Scrape a single wiki page
        params = {
            'action': 'parse',
            'page': page_title,
            'format': 'json',
            'prop': 'text',
            'contentmodel': 'wikitext'
        }
        
        try:
            response = requests.get(self.config.WIKI_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'parse' in data and 'text' in data['parse']:
                html_content = data['parse']['text']['*']
                return self._clean_html(html_content)
            else:
                print(f"Failed to scrape {page_title}")
                return None
                
        except Exception as e:
            print(f"Error scraping {page_title}: {e}")
            return None
    
    def _clean_html(self, html_content):
        #Clean HTML and extract relevant text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        #Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'table']):
            element.decompose()
        
        #Extract text with structure
        content = {}
        current_section = "Introduction"
        content[current_section] = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol']):
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                current_section = element.get_text().strip()
                content[current_section] = []
            else:
                text = element.get_text().strip()
                if len(text) > 20:  # Minimum text length
                    content[current_section].append(text)
        
        return content
    
    def scrape_all_pages(self):
        #Scrape all configured wiki pages
        all_data = {}
        
        for page in self.config.WIKI_PAGES:
            print(f"Scraping {page}...")
            content = self.scrape_page(page)
            if content:
                all_data[page] = content
                
                #Save individual page
                with open(os.path.join(self.config.RAW_DIR, f"{page}.json"), 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
        
        #Save combined data
        with open(os.path.join(self.config.RAW_DIR, "all_wiki_data.json"), 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
            
        return all_data