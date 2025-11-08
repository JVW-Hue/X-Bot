import requests
import json
from collections import Counter

class TrendDetector:
    def __init__(self):
        self.trending_hashtags = []
    
    def get_trending_hashtags(self):
        """Get trending hashtags from multiple sources"""
        trends = []
        
        # Method 1: Scrape from trending topics
        try:
            # Reddit trending
            r = requests.get('https://www.reddit.com/r/all/hot.json', 
                           headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            data = r.json()
            
            for post in data['data']['children'][:20]:
                title = post['data'].get('title', '').lower()
                # Extract hashtag-like words
                words = [w for w in title.split() if len(w) > 4]
                trends.extend(words[:3])
        except:
            pass
        
        # Method 2: Common trending topics
        evergreen_trends = [
            'motivation', 'success', 'mindset', 'entrepreneur', 
            'AI', 'tech', 'innovation', 'productivity', 'growth',
            'funny', 'meme', 'viral', 'trending'
        ]
        
        # Combine and get most common
        all_trends = trends + evergreen_trends
        trend_counts = Counter(all_trends)
        
        self.trending_hashtags = ['#' + t for t, _ in trend_counts.most_common(15)]
        return self.trending_hashtags
    
    def get_smart_hashtags(self, content_type, base_hashtags):
        """Mix base hashtags with trending ones"""
        if not self.trending_hashtags:
            self.get_trending_hashtags()
        
        # 70% base hashtags, 30% trending
        import random
        num_base = 3
        num_trending = 2
        
        selected = random.sample(base_hashtags, min(num_base, len(base_hashtags)))
        selected += random.sample(self.trending_hashtags, min(num_trending, len(self.trending_hashtags)))
        
        return selected[:5]
