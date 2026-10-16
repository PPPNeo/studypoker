import json

with open('data/articles.json', encoding='utf-8') as f:
    posts = json.load(f)

def test_classifier(p):
    tags = [t['name'].lower() for t in p.get('tags', [])]
    t = (p['title_en'] + ' ' + p['slug'] + ' ' + ' '.join(tags)).lower()
    
    # 1. Category
    if any(k in t for k in ['bounty', 'pko', 'knockout']):
        cat = 'PKO 바운티'
    elif any(k in t for k in ['3-bet', '3bet', '4-bet', '4bet', 'squeeze']):
        cat = '3벳 팟'
    elif any(k in t for k in ['flop', 'c-bet', 'cbet', 'monotone', 'texture', 'board']):
        cat = '플랍 전략'
    elif any(k in t for k in ['turn', 'river', 'bluff', 'blocker', 'catch', 'polar', 'barrel']):
        cat = '턴/리버'
    elif any(k in t for k in ['exploit', 'capped', 'profile', 'nodelock', 'lag', 'tag', 'leak', 'calling station', 'nit', 'maniac']):
        cat = '익스플로잇'
    elif any(k in t for k in ['icm', 'mtt', 'bubble', 'tournament', 'final table', 'payjump', 'spin']):
        cat = '토너먼트/ICM'
    elif any(k in t for k in ['straddle', 'ante', 'cash', 'rake', 'live', 'deep stack']):
        cat = '캐시/스트래들'
    elif any(k in t for k in ['equity', 'ev', 'odds', 'pot odds', 'spr', 'math', 'mdf', 'alpha']):
        cat = '수학/기초'
    elif any(k in t for k in ['multiway', 'toy game', 'solver', 'game theory', 'ai', 'nash']):
        cat = '솔버 이론'
    elif any(k in t for k in ['patch', 'update', 'notes', 'news', 'behind the scenes']):
        cat = '업데이트/소식'
    else:
        cat = 'GTO 전략'
        
    # 2. Independent Level
    if any(k in t for k in ['nodelock', 'frequency locking', 'toy game', 'benchmark', 'multiway solving', 'domination', 'advanced', 'deep stack hu']):
        lvl = 'Level 4 (고급)'
    elif any(k in t for k in ['icm', 'payjump', 'final table', 'bubble', 'overbet', 'solving']):
        lvl = 'Level 4 (고급)'
    elif any(k in t for k in ['3-bet', '3bet', '4-bet', '4bet', 'turn', 'river', 'barrel', 'bluff catch', 'check-raise', 'polar', 'lag', 'tag', 'maniac', 'nit', 'calling station', 'profile', 'probing', 'bounty', 'pko']):
        lvl = 'Level 3 (중급)'
    elif any(k in t for k in ['c-bet', 'cbet', 'flop', 'monotone', 'texture', 'open', 'stealing', 'defend', '10bb', 'chipev', 'straddle', 'ante', 'limp', 'heads-up', 'bvb']):
        lvl = 'Level 2 (초급)'
    elif any(k in t for k in ['what is', 'basics', 'beginner', 'fundamentals', 'soft skills', 'mistake', 'leak', 'sayings', 'patch', 'news', 'update', 'growth', 'table wizard']):
        lvl = 'Level 1 (입문)'
    else:
        lvl = 'Level 2 (초급)'
        
    return cat, lvl

matrix = {}
cat_counts = {}
lvl_counts = {}
for p in posts:
    c, l = test_classifier(p)
    cat_counts[c] = cat_counts.get(c, 0) + 1
    lvl_counts[l] = lvl_counts.get(l, 0) + 1
    key = (c, l)
    matrix[key] = matrix.get(key, 0) + 1

with open('scripts/test_matrix_out.txt', 'w', encoding='utf-8') as f:
    f.write('CATEGORIES:\n')
    for c, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        f.write(f'  {c}: {cnt}\n')
    f.write('\nLEVELS:\n')
    for l, cnt in sorted(lvl_counts.items(), key=lambda x: -x[1]):
        f.write(f'  {l}: {cnt}\n')
    f.write('\nCROSS TABULATION:\n')
    for (c, l), cnt in sorted(matrix.items()):
        f.write(f'  {c} | {l}: {cnt}\n')

print("Wrote test_matrix_out.txt")
