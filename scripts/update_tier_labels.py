"""
Update required_level and level labels in data/articles.json and data/quizzes.json
to align with the 1~100 level and 6-tier promotion system:
- Tier 0: [입문] 동네 피쉬 (Lv.1~9) -> req: 1
- Tier 1: [1차 전직] 펍 레귤러 (Lv.10~24) -> req: 10
- Tier 2: [2차 전직] 마이크로 그라인더 (Lv.25~44) -> req: 25
- Tier 3: [3차 전직] 로우스테이크 크러셔 (Lv.45~64) -> req: 45
- Tier 4: [4차 전직] 미드스테이크 프로 (Lv.65~84) -> req: 65
- Tier 5/6: [5차 전직/최종] 하이롤러 & 챔피언 (Lv.85~100) -> req: 85
"""

import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'data', 'articles.json')
QUIZZES_FILE = os.path.join(BASE_DIR, 'data', 'quizzes.json')

TIER_MAP = {
    1: { "req": 1, "label": "[입문] 동네 피쉬 (Lv.1~9)" },
    2: { "req": 10, "label": "[1차 전직] 펍 레귤러 (Lv.10~24)" },
    3: { "req": 25, "label": "[2차 전직] 마이크로 그라인더 (Lv.25~44)" },
    4: { "req": 45, "label": "[3차 전직] 로우스테이크 크러셔 (Lv.45~64)" },
    5: { "req": 65, "label": "[4차 전직] 미드스테이크 프로 (Lv.65~84)" },
    6: { "req": 85, "label": "[5차 전직/최종] 하이롤러 & 챔피언 (Lv.85~100)" }
}

def update_articles():
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    for art in articles:
        tier_num = art.get('tier_num')
        if not tier_num:
            level_str = art.get('level', '')
            for t in range(1, 7):
                if f"Level {t}" in level_str or f"Lv.{t}" in level_str or f"{t}차 전직" in level_str:
                    tier_num = t
                    break
        if not tier_num:
            tier_num = 1

        target = TIER_MAP[tier_num]
        art['tier_num'] = tier_num
        art['required_level'] = target['req']
        art['tier_category'] = f"Level {tier_num}"
        art['level'] = target['label']

    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {len(articles)} articles with promotion tier labels and required_levels.")

def update_quizzes():
    with open(QUIZZES_FILE, 'r', encoding='utf-8') as f:
        quizzes = json.load(f)

    for q in quizzes:
        tier_num = q.get('tier_num')
        if not tier_num:
            level_str = q.get('level', '')
            for t in range(1, 7):
                if f"Lv.{t}" in level_str or f"{t}차 전직" in level_str:
                    tier_num = t
                    break
            if not tier_num:
                old_req = q.get('required_level', 1)
                tier_num = old_req if old_req in TIER_MAP else 1

        target = TIER_MAP[tier_num]
        q['tier_num'] = tier_num
        q['required_level'] = target['req']
        q['level'] = target['label']

    with open(QUIZZES_FILE, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {len(quizzes)} quizzes with promotion tier labels and required_levels.")

if __name__ == '__main__':
    update_articles()
    update_quizzes()
