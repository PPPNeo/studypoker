import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
articles_path = os.path.join(BASE_DIR, 'data', 'articles.json')

with open(articles_path, encoding='utf-8') as f:
    articles = json.load(f)

from process_deep_knowledge_base import categorize_and_level

for a in articles:
    # Build pseudo post for categorize_and_level
    post = {
        'title': a.get('title_en', ''),
        'slug': a.get('slug', ''),
        'tags': [{'name': a.get('category', '')}]
    }
    cat, lvl = categorize_and_level(post)
    a['category'] = cat
    a['level'] = lvl

with open(articles_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Updated metadata for {len(articles)} articles!")

# Report distribution
cats = {}
lvls = {}
matrix = {}
for a in articles:
    c = a['category']
    l = a['level']
    cats[c] = cats.get(c, 0) + 1
    lvls[l] = lvls.get(l, 0) + 1
    matrix[(c, l)] = matrix.get((c, l), 0) + 1

print("\nCATEGORIES:")
for c, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {cnt}")

print("\nLEVELS:")
for l, cnt in sorted(lvls.items(), key=lambda x: -x[1]):
    print(f"  {l}: {cnt}")
