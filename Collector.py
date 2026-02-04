# imports
import csv
import requests
from datetime import datetime
import os

# Load existing stories to prevent duplicates
def load_existing_stories():
    """Load all existing story URLs from CSV to avoid duplicates"""
    existing_urls = set()
    if os.path.exists('NewsData.csv'):
        try:
            with open('NewsData.csv', 'r', encoding='UTF8') as f:
                reader = csv.DictReader(f)
                if reader:
                    for row in reader:
                        if row.get('URL'):
                            existing_urls.add(row['URL'].strip())
        except Exception as e:
            print(f"Error loading existing stories: {e}")
    return existing_urls

# Fetch top Hacker News stories
def get_hackernews_stories(limit=5, existing_urls=None):
    """Fetch top stories from Hacker News"""
    if existing_urls is None:
        existing_urls = set()
    
    stories = []
    try:
        # Get top story IDs (fetch more to account for duplicates)
        top_ids = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()[:50]
        
        collected = 0
        for story_id in top_ids:
            if collected >= limit:
                break
            
            story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
            if story and 'title' in story:
                url = story.get('url', '')
                # Skip if no URL or if URL already exists
                if not url or url in existing_urls:
                    continue
                
                stories.append({
                    'source': 'Hacker News',
                    'title': story.get('title', ''),
                    'url': url,
                    'score': story.get('score', 0)
                })
                existing_urls.add(url)
                collected += 1
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
    
    return stories

# Fetch tech news headlines
def get_tech_news(limit=5, existing_urls=None):
    """Fetch tech news from a free RSS-to-JSON service"""
    if existing_urls is None:
        existing_urls = set()
    
    stories = []
    try:
        # Using a free tech news source
        response = requests.get('https://api.hnify.io/top/1', timeout=5)
        if response.status_code == 200:
            data = response.json()
            collected = 0
            for item in data:
                if collected >= limit:
                    break
                
                url = item.get('url', '')
                # Skip if no URL or if URL already exists
                if not url or url in existing_urls:
                    continue
                
                stories.append({
                    'source': 'Tech News',
                    'title': item.get('title', ''),
                    'url': url,
                    'score': item.get('points', 0)
                })
                existing_urls.add(url)
                collected += 1
    except Exception as e:
        print(f"Error fetching tech news: {e}")
    
    return stories

# Main collection
date = datetime.now().strftime('%Y-%m-%d')
existing_urls = load_existing_stories()

hn_stories = get_hackernews_stories(5, existing_urls)
tech_stories = get_tech_news(5, existing_urls)
all_stories = hn_stories + tech_stories

# Write to CSV only if there are new stories
if all_stories:
    with open('NewsData.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        for story in all_stories:
            writer.writerow([date, story['source'], story['title'], story['url'], story['score']])
    print(f"Collected {len(all_stories)} new stories on {date}")
else:
    print(f"No new stories collected on {date} (all duplicates or API issues)")

