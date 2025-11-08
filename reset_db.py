import sqlite3, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

db = sqlite3.connect('bot.db')

db.execute('DROP TABLE IF EXISTS posts')
print("✅ Dropped old table")

db.execute('''CREATE TABLE posts (
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
db.close()

print("✅ Database reset with new schema (memes, videos, quotes support)")
