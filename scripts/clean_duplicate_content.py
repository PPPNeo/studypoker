"""
GTO Playbook KR - Clean Duplicate Content Script
Removes redundant and repeated bullets and paragraphs within the same article.
Ensures every article delivers unique, concise, and clean poker theory insights without repetitive spam.
"""

import json
import os
import re
import sys

# Ensure UTF-8 console output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'data', 'articles.json')

def clean_articles():
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    cleaned_count = 0
    total_removed = 0

    for art in articles:
        html = art.get('content_html', '')
        seen_items = set()

        def li_filter(match):
            nonlocal total_removed
            content = match.group(1).strip()
            norm = re.sub(r'\s+', ' ', content)
            if len(norm) > 15 and norm in seen_items:
                total_removed += 1
                return ''
            seen_items.add(norm)
            return f'<li>{content}</li>'

        # 1. Deduplicate <li> tags
        cleaned_html = re.sub(r'<li>(.*?)</li>', li_filter, html, flags=re.DOTALL)

        # 2. Clean empty <ul> tags
        cleaned_html = re.sub(r'<ul[^>]*>\s*</ul>', '', cleaned_html)

        # 3. Clean empty section summary containers
        cleaned_html = re.sub(r'<div[^>]*class="[^"]*section-[^"]*box[^"]*"[^>]*>\s*(<h\d[^>]*>.*?</h\d>)?\s*</div>', '', cleaned_html, flags=re.DOTALL)

        # 4. Remove consecutive duplicate sentences or duplicated paragraph blocks
        seen_paras = set()
        def para_filter(match):
            nonlocal total_removed
            p_content = match.group(1).strip()
            norm = re.sub(r'\s+', ' ', p_content)
            if len(norm) > 40 and norm in seen_paras:
                total_removed += 1
                return ''
            seen_paras.add(norm)
            return f'<p>{p_content}</p>'

        cleaned_html = re.sub(r'<p>(.*?)</p>', para_filter, cleaned_html, flags=re.DOTALL)

        if cleaned_html != html:
            art['content_html'] = cleaned_html
            cleaned_count += 1

    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully cleaned duplicate content!")
    print(f"   Articles modified: {cleaned_count} / {len(articles)}")
    print(f"   Total duplicate blocks removed: {total_removed}")

if __name__ == '__main__':
    clean_articles()
