import sqlite3, os, sys, time
from datetime import datetime, timedelta
import tweepy
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

class Analytics:
    def __init__(self):
        self.db = sqlite3.connect('bot.db')
        self.client = tweepy.Client(bearer_token=os.getenv('X_BEARER_TOKEN'))
    
    def fetch_metrics(self):
        cutoff = datetime.now() - timedelta(days=7)
        posts = self.db.execute(
            'SELECT tweet_id FROM posts WHERE posted_at > ? AND impressions = 0',
            (cutoff,)
        ).fetchall()
        
        updated = 0
        for (tweet_id,) in posts:
            try:
                tweet = self.client.get_tweet(tweet_id, tweet_fields=['public_metrics'])
                m = tweet.data.public_metrics
                
                impressions = m.get('impression_count', 0)
                likes = m['like_count']
                retweets = m['retweet_count']
                replies = m['reply_count']
                
                engagement = likes + retweets + replies
                eng_rate = (engagement / impressions * 100) if impressions > 0 else 0
                
                self.db.execute('''UPDATE posts SET 
                    impressions=?, likes=?, retweets=?, replies=?, engagement_rate=?
                    WHERE tweet_id=?''',
                    (impressions, likes, retweets, replies, eng_rate, tweet_id))
                
                updated += 1
                print(f"✅ {tweet_id}: {impressions:,} views | {likes} ❤️ | {eng_rate:.2f}%")
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ {tweet_id}: {e}")
        
        self.db.commit()
        print(f"\n✅ Updated {updated} posts\n")
    
    def show_report(self):
        print("="*70)
        print("🚀 JWV VIRAL GROWTH REPORT")
        print("="*70)
        
        # Overall
        total = self.db.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
        total_views = self.db.execute('SELECT SUM(impressions) FROM posts').fetchone()[0] or 0
        total_likes = self.db.execute('SELECT SUM(likes) FROM posts').fetchone()[0] or 0
        total_rt = self.db.execute('SELECT SUM(retweets) FROM posts').fetchone()[0] or 0
        avg_eng = self.db.execute('SELECT AVG(engagement_rate) FROM posts WHERE impressions > 0').fetchone()[0] or 0
        
        print(f"\n📊 OVERALL STATS")
        print(f"Total posts: {total}")
        print(f"Total views: {total_views:,}")
        print(f"Total likes: {total_likes:,}")
        print(f"Total retweets: {total_rt:,}")
        print(f"Avg engagement: {avg_eng:.2f}%")
        print(f"Avg views/post: {total_views//total if total else 0:,}")
        
        # Top posts
        print(f"\n🔥 TOP 5 VIRAL POSTS")
        top = self.db.execute('''
            SELECT caption, impressions, likes, retweets, engagement_rate
            FROM posts WHERE posted_at > datetime('now', '-7 days')
            ORDER BY impressions DESC LIMIT 5
        ''').fetchall()
        
        for i, (cap, imp, likes, rt, eng) in enumerate(top, 1):
            print(f"\n{i}. {cap[:55]}...")
            print(f"   👀 {imp:,} views | ❤️ {likes} | 🔄 {rt} | 📈 {eng:.2f}%")
        
        # Best hours
        print(f"\n⏰ BEST POSTING HOURS")
        hours = self.db.execute('''
            SELECT posted_hour, AVG(engagement_rate) as avg_eng, AVG(impressions) as avg_views
            FROM posts WHERE posted_at > datetime('now', '-7 days') AND impressions > 0
            GROUP BY posted_hour ORDER BY avg_eng DESC LIMIT 6
        ''').fetchall()
        
        for hour, eng, views in hours:
            print(f"  {hour:02d}:00 → {eng:.2f}% engagement | {views:,.0f} avg views")
        
        # Best content type
        print(f"\n🎨 BEST CONTENT TYPE")
        types = self.db.execute('''
            SELECT source_type, AVG(engagement_rate) as avg_eng, AVG(impressions) as avg_views, COUNT(*) as cnt
            FROM posts WHERE posted_at > datetime('now', '-7 days') AND impressions > 0
            GROUP BY source_type ORDER BY avg_eng DESC
        ''').fetchall()
        
        for ctype, eng, views, cnt in types:
            print(f"  {ctype}: {eng:.2f}% engagement | {views:,.0f} avg views ({cnt} posts)")
        
        # Best caption type
        print(f"\n💬 BEST CAPTION STYLE")
        captions = self.db.execute('''
            SELECT caption_type, AVG(engagement_rate) as avg_eng, COUNT(*) as cnt
            FROM posts WHERE posted_at > datetime('now', '-7 days') AND impressions > 0
            GROUP BY caption_type ORDER BY avg_eng DESC
        ''').fetchall()
        
        for ctype, eng, cnt in captions:
            print(f"  {ctype}: {eng:.2f}% engagement ({cnt} posts)")
        
        # 7-day trend
        print(f"\n📈 7-DAY GROWTH TREND")
        for i in range(6, -1, -1):
            day = datetime.now() - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            stats = self.db.execute('''
                SELECT COUNT(*), SUM(impressions), SUM(likes), AVG(engagement_rate)
                FROM posts WHERE DATE(posted_at) = ?
            ''', (day_str,)).fetchone()
            
            posts, views, likes, eng = stats[0], stats[1] or 0, stats[2] or 0, stats[3] or 0
            print(f"  {day.strftime('%a %m/%d')}: {posts} posts | {views:,} views | {likes} ❤️ | {eng:.2f}% eng")
        
        print("\n" + "="*70)
        print("💡 TIP: Bot learns from this data every 10 posts!")
        print("="*70 + "\n")

if __name__ == '__main__':
    analytics = Analytics()
    
    print("📊 Fetching latest metrics from X API...\n")
    analytics.fetch_metrics()
    
    analytics.show_report()
