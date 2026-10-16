import sys, json
from bs4 import BeautifulSoup
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

arts = json.load(open('data/articles.json', encoding='utf-8'))
for i in range(10):
    art = arts[i]
    soup = BeautifulSoup(art['content_html'], 'html.parser')
    lis = [li.get_text(strip=True) for li in soup.find_all('li')]
    c_lis = Counter(lis)
    dups_li = [k for k, v in c_lis.items() if v > 1 and len(k) > 10]
    ps = [p.get_text(strip=True) for p in soup.find_all('p')]
    c_ps = Counter(ps)
    dups_p = [k for k, v in c_ps.items() if v > 1 and len(k) > 15]
    print(f"=== Article {i}: {art.get('title_ko', '')} (slug: {art.get('slug')}) ===")
    for d in dups_li[:3]:
        print(f"  [LI x{c_lis[d]}]: {d[:70]}")
    for d in dups_p[:3]:
        print(f"  [P x{c_ps[d]}]: {d[:70]}")
