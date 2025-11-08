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
    
    def _domain_allowed(self, url):
        host = urlparse(url).netloc.lower()
        return any(d in host for d in self.config['whitelist_domains'])
    
    def scrape_reddit_memes(self, limit=10):
        """Scrape memes from Reddit"""
        memes = []
        for source in self.config.get('meme_sources', []):
            try:
                r = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                data = r.json()
                
                for post in data['data']['children'][:limit]:
                    p = post['data']
                    if p.get('over_18'):
                        continue
                    
                    url = p.get('url', '')
                    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        if self._domain_allowed(url):
                            memes.append({'url': url, 'title': p.get('title', ''), 'score': p.get('score', 0)})
                
                time.sleep(2)
            except:
                pass
        
        return sorted(memes, key=lambda x: x['score'], reverse=True)[:limit]
    
    def scrape_reddit_videos(self, limit=5):
        """Scrape videos from Reddit"""
        videos = []
        for source in self.config.get('video_sources', []):
            try:
                r = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                data = r.json()
                
                for post in data['data']['children'][:limit]:
                    p = post['data']
                    if p.get('over_18') or p.get('is_video') != True:
                        continue
                    
                    if 'media' in p and p['media']:
                        video_url = p['media'].get('reddit_video', {}).get('fallback_url')
                        if video_url:
                            videos.append({'url': video_url, 'title': p.get('title', ''), 'score': p.get('score', 0)})
                
                time.sleep(2)
            except:
                pass
        
        return sorted(videos, key=lambda x: x['score'], reverse=True)[:limit]
    
    def get_random_quote(self):
        """Get random motivational quote"""
        try:
            source = random.choice(self.config.get('quote_sources', []))
            r = requests.get(source, timeout=10)
            data = r.json()
            
            if 'zenquotes' in source:
                return data[0]['q'] + ' - ' + data[0]['a']
            else:
                return data['content'] + ' - ' + data['author']
        except:
            # Fallback quotes
            quotes = [
                "Success is not final, failure is not fatal. - Winston Churchill",
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                "The future belongs to those who believe in their dreams. - Eleanor Roosevelt",
                "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
            ]
            return random.choice(quotes)
    
    def get_random_content(self):
        """Get random content - meme, video, or quote"""
        
        # Decide content type (60% meme, 20% video, 20% quote)
        rand = random.random()
        
        if rand < 0.6:  # Meme
            memes = self.scrape_reddit_memes(5)
            if memes:
                return memes[0]['url'], 'meme', None
            # Fallback to API image
            return f"https://picsum.photos/1920/1080?random={random.randint(1, 999999)}", 'meme', None
        
        elif rand < 0.8:  # Video
            videos = self.scrape_reddit_videos(3)
            if videos:
                return videos[0]['url'], 'video', videos[0]['title']
            # Fallback to meme if no video
            return f"https://picsum.photos/1920/1080?random={random.randint(1, 999999)}", 'meme', None
        
        else:  # Quote
            quote_text = self.get_random_quote()
            return None, 'quote', quote_text
