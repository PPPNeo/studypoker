"""
GTO Wizard Blog Scraper & Parser
Extracts article content, images, headings, and metadata from blog.gtowizard.com
"""

import urllib.request
import json
import os
import re
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://blog.gtowizard.com/'
}

def fetch_sitemap_urls():
    """Fetches list of all article URLs from GTO Wizard sitemap."""
    url = 'https://blog.gtowizard.com/sitemap-posts.xml'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'xml')
            return [loc.text.strip() for loc in soup.find_all('loc')]
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def scrape_article(url_or_slug):
    """Scrapes a single article given URL or slug."""
    if not url_or_slug.startswith('http'):
        url = f"https://blog.gtowizard.com/{url_or_slug.strip('/')}/"
    else:
        url = url_or_slug
        
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            title_el = soup.find('h1')
            title = title_el.text.strip() if title_el else ""
            
            # Author & Date
            author_el = soup.find('span', class_='author-name') or soup.find('a', class_='gh-article-author')
            author = author_el.text.strip() if author_el else "GTO Wizard Team"
            
            # Featured Image
            img_el = soup.find('img', class_='gh-feature-image') or soup.find('meta', property='og:image')
            featured_image = img_el.get('src') or img_el.get('content') if img_el else ""
            
            # Content
            content_div = soup.find('div', class_='gh-content') or soup.find('article')
            if not content_div:
                return None
                
            # Extract sections
            sections = []
            curr_title = "Introduction"
            curr_paragraphs = []
            
            for child in content_div.children:
                if child.name in ['h2', 'h3']:
                    if curr_paragraphs:
                        sections.append({
                            'heading': curr_title,
                            'text': "\n\n".join(curr_paragraphs)
                        })
                        curr_paragraphs = []
                    curr_title = child.text.strip()
                elif child.name in ['p', 'ul', 'ol', 'blockquote']:
                    text = child.text.strip()
                    if text:
                        curr_paragraphs.append(text)
                        
            if curr_paragraphs:
                sections.append({
                    'heading': curr_title,
                    'text': "\n\n".join(curr_paragraphs)
                })
                
            return {
                'url': url,
                'slug': url.strip('/').split('/')[-1],
                'title': title,
                'author': author,
                'featured_image': featured_image,
                'sections': sections,
                'raw_html': str(content_div)
            }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == '__main__':
    print("Testing GTO Wizard scraper...")
    test_slug = "understanding-blockers-in-poker"
    data = scrape_article(test_slug)
    if data:
        print(f"Success! Scraped '{data['title']}' with {len(data['sections'])} sections.")
        print("First section heading:", data['sections'][0]['heading'])
