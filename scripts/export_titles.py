import json

with open('data/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('all_articles_titles.txt', 'w', encoding='utf-8') as f:
    for i, a in enumerate(articles):
        aid = a.get('id', '')
        en = a.get('title_en', '')
        ko = a.get('title_ko', '')
        f.write(f"{i:03d}\t{aid}\t{en}\t{ko}\n")

print(f"Exported {len(articles)} titles to all_articles_titles.txt")
