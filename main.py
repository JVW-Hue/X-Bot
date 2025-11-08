import os, json, time, random, hashlib, sqlite3, sys, threading
from datetime import datetime, timedelta
from pathlib import Path
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import tweepy
from dotenv import load_dotenv
from scraper import ContentScraper
from trends import TrendDetector

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def keep_alive():
    while True:
        time.sleep(600)
        print("🔄 Keep-alive ping")

threading.Thread(target=keep_alive, daemon=True).start()

class JVWBot:
    def __init__(self):
        self.config = json.load(open('config.json'))
        self.cache_dir = Path('cache')
        self.cache_dir.mkdir(exist_ok=True)
        self.db = self._init_db()
        self.scraper = ContentScraper(self.config)
        
        auth = tweepy.OAuth1UserHandler(
            os.getenv('X_API_KEY'),
            os.getenv('X_API_SECRET'),
            os.getenv('X_ACCESS_TOKEN'),
            os.getenv('X_ACCESS_SECRET')
        )
        self.api_v1 = tweepy.API(auth)
        self.client = tweepy.Client(
            bearer_token=os.getenv('X_BEARER_TOKEN'),
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_SECRET')
        )
        
        self.post_count = 0
        self.last_post_time = 0
        self.trend_detector = TrendDetector()
        self._learn_from_analytics()
        
    def _init_db(self):
        db = sqlite3.connect('bot.db', check_same_thread=False)
        db.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            tweet_id TEXT,
            content_hash TEXT UNIQUE,
            source_url TEXT,
            content_type TEXT,
            caption TEXT,
            caption_type TEXT,
            hashtags TEXT,
            posted_at TIMESTAMP,
            posted_hour INTEGER,
            impressions INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            retweets INTEGER DEFAULT 0,
            replies INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0
        )''')
        db.commit()
        return db
    
    def _learn_from_analytics(self):
        if not self.config.get('learning_enabled'):
            return
        
        rows = self.db.execute('''
            SELECT posted_hour, AVG(engagement_rate) as avg_eng
            FROM posts WHERE posted_at > datetime('now', '-7 days') AND impressions > 0
            GROUP BY posted_hour ORDER BY avg_eng DESC LIMIT 6
        ''').fetchall()
        
        if rows:
            self.config['best_hours'] = [r[0] for r in rows]
            print(f"📊 Learned best hours: {self.config['best_hours']}")
        
        rows = self.db.execute('''
            SELECT content_type, AVG(engagement_rate) as avg_eng, COUNT(*) as cnt
            FROM posts WHERE posted_at > datetime('now', '-7 days') AND impressions > 0
            GROUP BY content_type ORDER BY avg_eng DESC
        ''').fetchall()
        
        if rows:
            print(f"📊 Best content: {rows[0][0]} ({rows[0][1]:.2%} engagement)")
    
    def _is_duplicate(self, content_hash):
        """Check if content was already posted (EVER)"""
        cur = self.db.execute('SELECT 1 FROM posts WHERE content_hash=?', (content_hash,))
        return cur.fetchone() is not None
    
    def _download_optimize(self, url):
        r = requests.get(url, timeout=15, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        
        # Hash actual image content (not URL)
        img_data = r.content
        content_hash = hashlib.sha256(img_data).hexdigest()[:16]
        cache_path = self.cache_dir / f"{content_hash}.jpg"
        
        if cache_path.exists():
            return str(cache_path), content_hash
        
        img = Image.open(BytesIO(img_data)).convert('RGB')
        img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
        img.save(cache_path, 'JPEG', quality=85, optimize=True)
        
        return str(cache_path), content_hash
    
    def _generate_caption(self, content_type, extra_text=None):
        templates = {
            'meme': ["Double tap if you agree 💯", "Tag someone 👇", "RT if this is you 🔄", "Facts or facts? 💭", "This hits different ✨"],
            'video': ["Watch this 🎥", "This is powerful 💪", "Save this for later 💾", "You need to see this 👀", "Motivation incoming 🚀"],
            'quote': ["Daily reminder 📌", "Words to live by ✨", "Think about this 💭", "Save this 🔖", "Needed this today 🎯"]
        }
        
        caption = random.choice(templates.get(content_type, templates['meme']))
        
        if extra_text:
            caption = extra_text[:200]
        
        emojis = ['🔥', '💪', '⚡', '🚀', '💡', '✨', '👀', '💯']
        if random.random() < 0.3:
            caption += ' ' + random.choice(emojis)
        
        # Use smart trending hashtags
        base_tags = self.config['hashtags'].get(content_type, self.config['hashtags']['general'])
        tags = self.trend_detector.get_smart_hashtags(content_type, base_tags)
        
        if random.random() < 0.4:
            tags.append(random.choice(self.config['brand_tags']))
        
        hashtags = ' '.join(tags[:5])
        caption += '\n\n' + hashtags
        
        return caption, hashtags
    
    def _rate_limit_check(self):
        now = time.time()
        elapsed = now - self.last_post_time
        if elapsed < self.config['min_interval_seconds']:
            time.sleep(self.config['min_interval_seconds'] - elapsed)
    
    def post_content(self):
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                content_url, content_type, extra_text = self.scraper.get_random_content()
                
                if content_type == 'quote':
                    content_hash = hashlib.sha256(extra_text.encode()).hexdigest()[:16]
                    if self._is_duplicate(content_hash):
                        print(f"⏭️ Skip duplicate quote (attempt {attempt+1}/{max_attempts})")
                        continue
                    
                    caption, hashtags = self._generate_caption(content_type, extra_text)
                    self._rate_limit_check()
                    response = self.client.create_tweet(text=caption)
                    tweet_id = response.data['id']
                else:
                    img_path, content_hash = self._download_optimize(content_url)
                    if self._is_duplicate(content_hash):
                        print(f"⏭️ Skip duplicate {content_type} (attempt {attempt+1}/{max_attempts})")
                        continue
                    
                    media = self.api_v1.media_upload(img_path)
                    caption, hashtags = self._generate_caption(content_type, extra_text)
                    self._rate_limit_check()
                    response = self.client.create_tweet(text=caption, media_ids=[media.media_id_string])
                    tweet_id = response.data['id']
            
                posted_hour = datetime.now().hour
                self.db.execute('''INSERT INTO posts 
                    (tweet_id, content_hash, source_url, content_type, caption, hashtags, posted_at, posted_hour)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (tweet_id, content_hash, content_url or 'quote', content_type, caption, hashtags, datetime.now().isoformat(), posted_hour))
                self.db.commit()
                
                self.last_post_time = time.time()
                self.post_count += 1
                print(f"✅ Posted {content_type} #{self.post_count}: {caption[:40]}... | ID: {tweet_id}")
                return True
                
            except Exception as e:
                print(f"❌ Post attempt {attempt+1} failed: {e}")
                if attempt == max_attempts - 1:
                    return False
                time.sleep(5)
        
        print(f"❌ Failed to find unique content after {max_attempts} attempts")
        return False
    
    def run_forever(self):
        print("🚀 JVW BOT STARTING - 24/7 VIRAL GROWTH MODE")
        print(f"🎯 Target: {self.config['posts_per_day']} posts/day")
        print(f"📊 Learning: {'ON' if self.config['learning_enabled'] else 'OFF'}")
        print(f"🔥 Best hours: {self.config['best_hours']}\n")
        
        while True:
            try:
                current_hour = datetime.now().hour
                
                if current_hour in self.config['best_hours']:
                    interval = random.randint(self.config['min_interval_seconds'], self.config['max_interval_seconds'])
                    print(f"⚡ PEAK HOUR {current_hour} - High activity mode")
                else:
                    interval = random.randint(self.config['min_interval_seconds'], self.config['max_interval_seconds'])
                    if random.random() < 0.25:
                        print(f"💤 Off-peak hour {current_hour} - Skipping")
                        time.sleep(interval)
                        continue
                
                self.post_content()
                
                if self.post_count % 10 == 0 and self.post_count > 0:
                    print("\n📊 LEARNING FROM ANALYTICS...")
                    self._learn_from_analytics()
                
                print(f"⏰ Next post in {interval//60} min {interval%60} sec\n")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                time.sleep(300)

if __name__ == '__main__':
    bot = JVWBot()
    bot.run_forever()
