import requests, json, random, time
from pathlib import Path
from urllib.parse import urlparse

class ContentScraper:
    def __init__(self, config):
        self.config = config
        self.memes_dir = Path('content/memes')
        self.videos_dir = Path('content/videos')
        self.quotes_dir = Path('content/quotes')
        
        self.memes_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.quotes_dir.mkdir(parents=True, exist_ok=True)
    
    def scrape_reddit_memes(self, limit=10):
        """Scrape memes from safe subreddits"""
        memes = []
        
        for source in self.config['meme_sources']:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(source, headers=headers, timeout=10)
                data = r.json()
                
                for post in data['data']['children'][:limit]:
                    p = post['data']
                    
                    # Skip NSFW
                    if p.get('over_18'):
                        continue
                    
                    url = p.get('url', '')
                    
                    # Only image posts
                    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        if self._domain_allowed(url):
                            memes.append({
                                'url': url,
                                'title': p.get('title', ''),
                                'score': p.get('score', 0)
                            })
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Reddit scrape error: {e}")
        
        return sorted(memes, key=lambda x: x['score'], reverse=True)[:limit]
    
    def _domain_allowed(self, url):
        host = urlparse(url).netloc.lower()
        return any(d in host for d in self.config['whitelist_domains'])
    
    def get_random_content(self):
        """Get random content - always use fresh API images"""
        
        # Always use image API with unique random number
        img_source = random.choice(self.config['image_sources'])
        if '?' in img_source and img_source.endswith('='):
            img_source += str(random.randint(1, 999999))
        else:
            img_source = f"https://picsum.photos/1920/1080?random={random.randint(1, 999999)}"
        
        return img_source, 'api'
