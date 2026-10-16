# -*- coding: utf-8 -*-
"""
assign_levels_to_content.py
Assigns 6 RPG progression tiers to:
- data/ranges.json (13 presets)
- data/quizzes.json (25 spot quizzes)
- data/articles.json (369 strategy articles)
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Update ranges.json
RANGE_LEVELS = {
    'btn_open': (1, 'Lv.1 동네 피쉬 탈출기'),
    'sb_open': (1, 'Lv.1 동네 피쉬 탈출기'),
    'co_open': (2, 'Lv.2 홀덤펍 로컬 레귤러'),
    'hj_open': (2, 'Lv.2 홀덤펍 로컬 레귤러'),
    'utg_open': (2, 'Lv.2 홀덤펍 로컬 레귤러'),
    'bb_vs_btn': (3, 'Lv.3 마이크로 그라인더'),
    'bb_vs_co': (3, 'Lv.3 마이크로 그라인더'),
    'sb_vs_btn': (4, 'Lv.4 온라인 세미프로'),
    'btn_vs_co': (4, 'Lv.4 온라인 세미프로'),
    'btn_vs_sb_3bet': (5, 'Lv.5 하이롤러 토너 크러셔'),
    'push_btn_15bb': (6, 'Lv.6 WSOP 챔피언'),
    'push_sb_15bb': (6, 'Lv.6 WSOP 챔피언'),
    'call_bb_vs_btn_15bb': (6, 'Lv.6 WSOP 챔피언')
}

with open(os.path.join(BASE_DIR, 'data', 'ranges.json'), 'r', encoding='utf-8') as f:
    ranges_data = json.load(f)

for p in ranges_data['presets']:
    pid = p['id']
    if pid in RANGE_LEVELS:
        lvl, title = RANGE_LEVELS[pid]
        p['required_level'] = lvl
        p['required_level_title'] = title

with open(os.path.join(BASE_DIR, 'data', 'ranges.json'), 'w', encoding='utf-8') as f:
    json.dump(ranges_data, f, ensure_ascii=False, indent=2)
print("Updated ranges.json with required levels!")

# 2. Update quizzes.json (25 quizzes across 6 levels)
QUIZ_LEVEL_MAP = {
    # Lv.1: 입문 기초 (5)
    'quiz-7': (1, 'Lv.1 입문 (동네 피쉬)'),
    'quiz-16': (1, 'Lv.1 입문 (동네 피쉬)'),
    'quiz-17': (1, 'Lv.1 입문 (동네 피쉬)'),
    'quiz-20': (1, 'Lv.1 입문 (동네 피쉬)'),
    'quiz-22': (1, 'Lv.1 입문 (동네 피쉬)'),

    # Lv.2: 초급 플랍 & 주도권 (5)
    'quiz-1': (2, 'Lv.2 초급 (펍 레귤러)'),
    'quiz-3': (2, 'Lv.2 초급 (펍 레귤러)'),
    'quiz-6': (2, 'Lv.2 초급 (펍 레귤러)'),
    'quiz-8': (2, 'Lv.2 초급 (펍 레귤러)'),
    'quiz-11': (2, 'Lv.2 초급 (펍 레귤러)'),

    # Lv.3: 중급 턴 & MDF (5)
    'quiz-4': (3, 'Lv.3 중급 (마이크로 그라인더)'),
    'quiz-9': (3, 'Lv.3 중급 (마이크로 그라인더)'),
    'quiz-12': (3, 'Lv.3 중급 (마이크로 그라인더)'),
    'quiz-18': (3, 'Lv.3 중급 (마이크로 그라인더)'),
    'quiz-19': (3, 'Lv.3 중급 (마이크로 그라인더)'),

    # Lv.4: 고급 리버 & 블로커 & ICM (4)
    'quiz-2': (4, 'Lv.4 고급 (온라인 세미프로)'),
    'quiz-5': (4, 'Lv.4 고급 (온라인 세미프로)'),
    'quiz-13': (4, 'Lv.4 고급 (온라인 세미프로)'),
    'quiz-21': (4, 'Lv.4 고급 (온라인 세미프로)'),

    # Lv.5: 심화 오버벳 & 딥스택 & 영웅 콜 (3)
    'quiz-10': (5, 'Lv.5 심화 (하이롤러 크러셔)'),
    'quiz-15': (5, 'Lv.5 심화 (하이롤러 크러셔)'),
    'quiz-24': (5, 'Lv.5 심화 (하이롤러 크러셔)'),

    # Lv.6: 마스터 멀티웨이 & WSOP 파이널 (3)
    'quiz-14': (6, 'Lv.6 마스터 (WSOP 챔피언)'),
    'quiz-23': (6, 'Lv.6 마스터 (WSOP 챔피언)'),
    'quiz-25': (6, 'Lv.6 마스터 (WSOP 챔피언)')
}

with open(os.path.join(BASE_DIR, 'data', 'quizzes.json'), 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

for q in quizzes:
    qid = q['id']
    if qid in QUIZ_LEVEL_MAP:
        lvl, title = QUIZ_LEVEL_MAP[qid]
        q['required_level'] = lvl
        q['level'] = title

# Reorder quizzes by level so 1 to 25 progresses naturally from Lv.1 to Lv.6!
quizzes.sort(key=lambda x: (x.get('required_level', 1), x.get('id', '')))

with open(os.path.join(BASE_DIR, 'data', 'quizzes.json'), 'w', encoding='utf-8') as f:
    json.dump(quizzes, f, ensure_ascii=False, indent=2)
print("Updated quizzes.json with progressive levels!")

# 3. Update articles.json (369 articles across 6 levels)
with open(os.path.join(BASE_DIR, 'data', 'articles.json'), 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Classification criteria:
# Lv.1: 수학/기초 (17) + basic EV, odds, beginner titles -> 21 articles
# Lv.6: multiway, nash equilibrium, advanced solver math, wsop final -> ~23 articles
# Lv.5: pko, high stakes, deep stack, node locking, tournament icm advanced -> ~35 articles
# Lv.4: blockers, capped ranges, exploiting lag/tag, icm fundamentals -> ~55 articles
# Lv.3: 3-bet pots, turn barreling, probe bet, protection, overfold -> ~100 articles
# Lv.2: flop strategy, c-bet, single raised pots, cash basics -> rest (~135 articles)

for a in articles:
    cat = a.get('category', '')
    title = (a.get('title_ko', '') + ' ' + a.get('title_en', '')).lower()
    slug = a.get('slug', '').lower()

    # Default based on old level
    old_lvl = a.get('level', '')

    if cat == '수학/기초' or '기대값' in title or 'equity-realization' in slug or 'sayings-that-ruin' in slug:
        lvl = 1
        lvl_str = "Level 1 (입문)"
    elif 'multiway' in slug or 'multiway' in title or 'nash' in title or '내쉬' in title or '세계 챔피언' in title:
        lvl = 6
        lvl_str = "Level 6 (마스터)"
    elif 'pko' in slug or 'pko' in title or '바운티' in title or 'node lock' in title or '노드락' in title or '200bb' in title or '하이롤러' in title:
        lvl = 5
        lvl_str = "Level 5 (심화)"
    elif 'icm' in slug or 'icm' in title or 'blocker' in slug or '블로커' in title or 'capped' in slug or '캡된' in title or 'exploiting' in slug:
        lvl = 4
        lvl_str = "Level 4 (고급)"
    elif '3-bet' in slug or '3벳' in title or 'turn' in slug or '턴' in title or 'river' in slug or '리버' in title or 'mdf' in title:
        lvl = 3
        lvl_str = "Level 3 (중급)"
    else:
        # Check old level
        if 'Level 4' in old_lvl:
            lvl = 4
            lvl_str = "Level 4 (고급)"
        elif 'Level 3' in old_lvl:
            lvl = 3
            lvl_str = "Level 3 (중급)"
        elif 'Level 1' in old_lvl:
            lvl = 1
            lvl_str = "Level 1 (입문)"
        else:
            lvl = 2
            lvl_str = "Level 2 (초급)"

    a['required_level'] = lvl
    a['level'] = lvl_str

# Count levels
counts = {}
for a in articles:
    counts[a['level']] = counts.get(a['level'], 0) + 1

print("Article breakdown by 6 levels:", counts)

with open(os.path.join(BASE_DIR, 'data', 'articles.json'), 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Updated articles.json successfully!")
