"""
Processes all 369 GTO Wizard articles from Ghost CMS API into the full study database.
Assigns Level 1~4, categories, translated titles, summaries, and original URLs.
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'raw_ghost_all.json'), encoding='utf-8') as f:
    raw_posts = json.load(f)

# Load existing deep hand-crafted articles
with open(os.path.join(BASE_DIR, 'data', 'articles.json'), encoding='utf-8') as f:
    existing_articles = json.load(f)
existing_map = {a['slug']: a for a in existing_articles}

# Title translations dictionary
SPECIFIC_TITLES = {
    "Responding to 3-bets in Straddle+Ante Games": "스트래들+앤티 게임에서 3벳 대응 전략",
    "Stealing and Restealing in Straddle+Ante Games": "스트래들+앤티 게임의 스틸 및 리스틸 전략",
    "Now Live: Preflop ICM Solving": "프리플랍 ICM 솔빙 기능 공식 출시",
    "Exploiting Profiles: Episode V – The LAG": "상대 성향별 익스플로잇 V – 루즈 어그레시브(LAG)",
    "Exploiting Profiles: Episode IV – The TAG": "상대 성향별 익스플로잇 IV – 타이트 어그레시브(TAG)",
    "Exploiting Profiles: Episode III – The Maniac": "상대 성향별 익스플로잇 III – 매니악(Maniac)",
    "Exploiting Profiles: Episode II – The Nit": "상대 성향별 익스플로잇 II – 니트(Nit)",
    "Exploiting Profiles: Episode I – The Calling Station": "상대 성향별 익스플로잇 I – 콜링 스테이션",
    "PLO Upgrades: Custom HU Solving, Postflop ICM, Nodelocking & More": "PLO 업그레이드: 헤즈업 솔빙, 포스트플랍 ICM & 노드락",
    "Playing Under 10bb – Part 2: ICM": "10bb 이하 숏스택 전략 2편: ICM 상황",
    "Playing Under 10bb – Part 1: cEV": "10bb 이하 숏스택 전략 1편: 칩EV(cEV) 기준",
    "The Four-Point Checklist for Calling Turn Barrels": "턴 배럴에 콜하기 전 확인해야 할 4가지 체크리스트",
    "3-Way: How to Exploit a Calling Station?": "3웨이 팟에서 콜링 스테이션을 익스플로잇하는 법",
    "Small Blind, Big Problems: When to Size Up From OOP BvB": "스몰 블라인드의 딜레마: BvB 아웃포지션에서 벳 사이징 키우기",
    "Is Limping Preflop Viable in Mississippi Straddle Games?": "미시시피 스트래들 게임에서 프리플랍 림프는 유효할까?",
    "Navigating BvB OOP After Check-Calling the Flop": "플랍 첵-콜 이후 BvB 아웃포지션 턴/리버 운영법",
    "When to Open Shove vs. Different Player Profiles": "상대 성향별 오픈 셔브 기준과 타이밍",
    "Probing in 3-Way Pots": "3웨이 팟에서의 프로브 벳(Probe Bet) 전략",
    "Playing In Position Against Two Callers": "두 명의 콜러를 상대로 인포지션(IP) 플레이하기",
    "Monkey in the Middle: 3-Way Pot Heuristics": "3웨이 팟 한가운데 샌드위치되었을 때의 휴리스틱",
    "The Trouble With Implied Odds": "임플라이드 오즈(Implied Odds)의 함정과 한계",
    "The Art of Value Bluffing From the Button": "버튼에서의 밸류 블러핑(Value Bluffing) 기술",
    "Mississippi Straddles: Building a C-Betting Strategy vs. BTN": "미시시피 스트래들: 버튼을 상대로 C-bet 전략 구축하기",
    "Introducing Multiway Preflop Solving": "멀티웨이 프리플랍 솔빙 기능 정식 공개",
    "GTO Wizard AI Custom Multiway Solving": "GTO Wizard AI 커스텀 멀티웨이 솔빙 분석",
    "Mississippi Straddles: How to Defend vs Raises": "미시시피 스트래들: 레이즈에 방어하는 최적의 방법",
    "Opening Strategy When the Button Straddles": "버튼 스트래들이 나왔을 때의 프리플랍 오픈 전략",
    "Mastering PKOs With Custom Aggregated Reports": "어그리게이티드 리포트로 PKO 토너먼트 완전 정복",
    "Poker Concepts You’re Using Wrong (and How They’re Hurting Your Winrate)": "잘못 알고 있는 포커 개념들과 윈레이트 누수 방지법",
    "How to Improve Your Heads-Up Game": "헤즈업 실력을 비약적으로 끌어올리는 법",
    "How Payout Structures Reshape Postflop Strategy": "페이아웃 구조가 포스트플랍 전략을 바꾸는 메커니즘",
    "How ICM Quietly Shapes Postflop Strategy From the Start": "ICM이 포스트플랍 전략을 근본부터 지배하는 원리",
    "ICM vs. ChipEV: The Hidden Logic Behind BB 3-Bets": "ICM vs 칩EV: BB 3벳 이면에 숨겨진 솔버의 논리",
    "How ICM Reshapes 3-Bet Pots (and Why You Can’t Trust cEV)": "ICM이 3벳 팟을 바꾸는 방식과 cEV의 함정",
    "Betting Draws in Position: The Real Rules": "인포지션 드로우 벳의 진짜 원칙",
    "When Checking the Nuts Beats Betting Them": "너츠(Nuts)를 들고 벳 대신 체크해야 하는 이유",
    "Why You’re Bluffing the River Wrong With Bricked Flush Draws in Cash Games": "플러시 드로우가 미스되었을 때 리버 블러프를 잘못하는 이유",
    "How to Exploit Human Mistakes After a Flop Overbet": "플랍 오버벳 이후 상대의 실수를 익스플로잇하는 법",
    "The Art of the Flop Overbet (and Why You’re Probably Doing It Wrong)": "플랍 오버벳의 예술과 자주 범하는 실수",
    "Crush Calling Stations With These 3 Solver-Approved Strategies": "솔버가 검증한 콜링 스테이션 격파 3대 전략",
    "How Pros Use Solvers To Crush Pool Leaks": "프로들이 솔버로 필드(Pool)의 집단적 릭을 응징하는 법",
    "Understanding Domination: The Hidden Logic Behind Every Bet": "도미네이션(Domination)의 이해: 모든 벳 뒤의 숨은 수학",
    "Profiles Explained: Modeling Exploitable Opponents": "익스플로잇 가능한 상대를 모델링하는 프로필 분석법",
    "Common Poker Sayings That Ruin Your Winrate": "승률을 망치는 잘못된 포커 격언들",
    "Punish the Unstudied: Capped Ranges & Bluffing Imbalances": "캡된(Capped) 레인지와 블러프 불균형 완벽 응징하기",
    "Why Your Poker Range Is a Team": "포커 레인지를 '팀'으로 보아야 하는 이유",
    "Isolating Limpers in Short Stack HU": "숏스택 헤즈업에서 림퍼 아이솔레이션 전략",
    "Are You Leaving Value on the River?": "리버에서 밸류를 놓치고 있진 않나요? 씬 밸류 벳 가이드",
    "The 3 Biggest Leaks Killing Your Winrate": "승률을 갉아먹는 가장 치명적인 3대 릭(Leak)",
    "Round Out Your Defense: The Power of Raising": "방어 레인지를 완성하는 레이즈의 위력",
    "The Hidden Cost of Late Reg in PKOs": "PKO 바운티 토너먼트 레이트 레지의 숨은 비용",
    "How to Crush Ante Cash Games": "앤티(Ante) 캐시 게임 완벽 정복 가이드",
    "Quirks of Nash Equilibrium in Multiway": "멀티웨이 내쉬 균형의 독특한 특성과 변수",
    "Register Late, Win More: The Math Behind Smarter Tournament Entry": "더 똑똑한 토너먼트 참가: 레이트 레지의 수학적 진실",
    "Punish the Unstudied: Preflop Mistakes & Sizing Tells": "프리플랍 실수와 사이징 텔(Tell)을 응징하는 법",
    "Building Better River Strategies (and When to Ignore Equity Advantage)": "더 강력한 리버 전략: 에퀴티 우위를 무시해야 할 때",
    "The Case for the Hero Check: Why Great Players Know When Not to Bet": "히어로 체크: 최고 플레이어들이 벳을 참는 이유",
    "What Is Expected Value (EV) in Poker?": "기대값(EV)이란 무엇인가: 포커 수학의 핵심 기둥",
    "How to Play Monotone Boards in Single Raised Pots": "모노톤(Monotone) 보드 운영법: SRP 플랍 전략",
    "3-Bet Pots OOP as Preflop Aggressor: Flop C-Betting": "OOP 3벳 팟 어그레서: 플랍 C-bet 전략 완벽 가이드",
    "The Mechanics of Equity Realization": "에퀴티 실현(EQR)의 메커니즘과 실전 활용",
    "ICM Fundamentals: Risk Premium Explained": "ICM 기초: 리스크 프리미엄(Risk Premium) 완벽 이해",
    "MDF and Alpha: The Math Behind Defense & Offense": "MDF와 Alpha: 방어와 공격의 수학적 균형"
}

PATTERNS = [
    (r'(?i)\bHow to Play\b', '플레이 가이드:'),
    (r'(?i)\bHow to\b', '공략법:'),
    (r'(?i)\bThe Art of\b', '완벽 가이드:'),
    (r'(?i)\bA Guide to\b', '완벽 가이드:'),
    (r'(?i)\bComplete Guide to\b', '완벽 가이드:'),
    (r'(?i)\bMastering\b', '마스터하기:'),
    (r'(?i)\bExploiting\b', '익스플로잇:'),
    (r'(?i)\bCrushing\b', '정복하기:'),
    (r'(?i)\bWhen to\b', '언제 ~해야 하는가:'),
    (r'(?i)\bWhy You(?:\'re| are)\b', '왜 당신이'),
    (r'(?i)\bWhat is\b', '이해하기:'),
    (r'(?i)\bIn-Position\b', '인포지션(IP)'),
    (r'(?i)\bOut of Position\b', '아웃포지션(OOP)'),
    (r'(?i)\bSingle Raised Pot\b', 'SRP(싱글 레이즈드 팟)'),
    (r'(?i)\b3-Bet Pot\b', '3벳 팟'),
    (r'(?i)\b4-Bet Pot\b', '4벳 팟'),
    (r'(?i)\bCheck-Raising\b', '체크-레이즈'),
    (r'(?i)\bCheck-Calling\b', '체크-콜'),
    (r'(?i)\bEquity Realization\b', '에퀴티 실현(EQR)'),
    (r'(?i)\bExpected Value\b', '기대값(EV)'),
]

def translate_title(title_en):
    clean = title_en.strip().replace("’", "'")
    if clean in SPECIFIC_TITLES:
        return SPECIFIC_TITLES[clean]
    
    t = clean
    for pat, rep in PATTERNS:
        t = re.sub(pat, rep, t)
    
    if t != clean:
        return t
    return f"{title_en} (GTO 전략)"

def categorize_and_level(post):
    tags = [t['name'].lower() for t in post.get('tags', [])]
    title_lower = post['title'].lower()
    slug_lower = post['slug'].lower()
    text_pool = f"{' '.join(tags)} {title_lower} {slug_lower}"

    # Category determination
    if any(k in text_pool for k in ['bounty', 'pko', 'knockout']):
        category = "PKO 바운티"
        level = "Level 4 (고급)"
    elif any(k in text_pool for k in ['3-bet', '3bet', '4-bet', '4bet', 'squeeze']):
        category = "3벳 팟"
        level = "Level 3 (중급)"
    elif any(k in text_pool for k in ['flop', 'c-bet', 'cbet', 'monotone', 'texture', 'board']):
        category = "플랍 전략"
        level = "Level 2 (초급)"
    elif any(k in text_pool for k in ['turn', 'river', 'bluff', 'blocker', 'catch', 'polar', 'barrel']):
        category = "턴/리버"
        level = "Level 3 (중급)"
    elif any(k in text_pool for k in ['exploit', 'capped', 'profile', 'nodelock', 'lag', 'tag', 'leak', 'calling station', 'nit', 'maniac']):
        category = "익스플로잇"
        level = "Level 3 (중급)"
    elif any(k in text_pool for k in ['icm', 'mtt', 'bubble', 'tournament', 'final table', 'payjump', 'spin']):
        category = "토너먼트/ICM"
        level = "Level 4 (고급)"
    elif any(k in text_pool for k in ['straddle', 'ante', 'cash', 'rake', 'live', 'deep stack']):
        category = "캐시/스트래들"
        level = "Level 2 (초급)"
    elif any(k in text_pool for k in ['equity', 'ev', 'odds', 'pot odds', 'spr', 'math', 'mdf', 'alpha']):
        category = "수학/기초"
        level = "Level 1 (입문)"
    elif any(k in text_pool for k in ['multiway', 'toy game', 'solver', 'game theory', 'ai', 'nash']):
        category = "솔버 이론"
        level = "Level 4 (고급)"
    elif any(k in text_pool for k in ['patch', 'update', 'notes', 'news', 'behind the scenes']):
        category = "업데이트/소식"
        level = "Level 1 (입문)"
    else:
        category = "GTO 전략"
        level = "Level 2 (초급)"

    return category, level

full_articles = []

for post in raw_posts:
    slug = post['slug']
    original_url = f"https://blog.gtowizard.com/{slug}/"
    category, level = categorize_and_level(post)
    title_en = post['title']
    title_ko = translate_title(title_en)
    read_time = f"{post.get('reading_time', 6)}분"

    author_name = "GTO Wizard Team"
    if post.get('authors'):
        author_name = post['authors'][0]['name']

    # If already hand-crafted with rich text and quiz, keep it and update meta
    if slug in existing_map and len(existing_map[slug].get('content_html', '')) > 1500:
        art = existing_map[slug]
        art['category'] = category
        art['level'] = level
        art['original_url'] = original_url
        full_articles.append(art)
        continue

    excerpt = post.get('custom_excerpt') or f"GTO Wizard 전략 연구팀의 심층 분석: {title_en}의 솔버 수학과 실전 적용 가이드입니다."
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."

    summary_cards = [
      {
        "badge": "핵심 1",
        "title": "GTO 솔버 분석",
        "text": f"{title_en}에 대한 GTO Wizard 최신 솔루션 분석 및 레인지 상호작용 원리를 다룹니다."
      },
      {
        "badge": "핵심 2",
        "title": "실전 적용 팁",
        "text": "이론적 균형(Nash Equilibrium)을 유지하면서도 상대의 인간적 릭(Leak)을 착취하는 실전 팁을 제공합니다."
      },
      {
        "badge": "핵심 3",
        "title": "원문 솔버 차트",
        "text": "상단의 [GTO Wizard 원문 보기]를 클릭하시면 인터랙티브 솔버 레인지 차트와 수치를 확인할 수 있습니다."
      }
    ]

    content_html = f"""
      <div class="article-lead">
        <strong>{title_ko}</strong> ({title_en})는 포커 플레이어들이 실전에서 자주 마주치는 복잡한 스팟을 GTO Wizard 솔버의 수학적 해법으로 명쾌하게 풀어낸 고급 전략 콘텐츠입니다.
      </div>

      <h2>1. 핵심 개요 및 전략적 배경</h2>
      <p>{excerpt}</p>
      
      <div class="callout-card tip">
        <h4>💡 솔버 핵심 테이크어웨이</h4>
        <p>이 스팟에서 가장 중요한 기준은 <strong>[레인지 vs 레인지의 에퀴티 분포]</strong>와 <strong>[보드 텍스처에 따른 주도권]</strong>입니다. 단일 핸드의 강함에 집착하지 말고 전체 레인지의 밸류-블러프 비율을 일정하게 유지해야 상대의 익스플로잇을 원천 차단할 수 있습니다.</p>
      </div>

      <h2>2. GTO Wizard 공식 원문 및 솔버 차트</h2>
      <p>본 아티클의 세부 솔버 데이터, 레인지 차트 스크린샷, 핸드 히스토리 시뮬레이션 원본은 아래의 <strong>GTO Wizard 공식 블로그 링크</strong>에서 바로 확인하실 수 있습니다.</p>
      <div style="margin: 1.5rem 0;">
        <a href="{original_url}" target="_blank" rel="noopener noreferrer" class="btn-primary" style="display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none;">
          <span>🌐</span> GTO Wizard 공식 블로그 원문 열기 ↗
        </a>
      </div>
    """

    full_articles.append({
        "id": slug,
        "slug": slug,
        "title_ko": title_ko,
        "title_en": title_en,
        "level": level,
        "category": category,
        "read_time": read_time,
        "author": author_name,
        "original_url": original_url,
        "thumbnail": post.get('feature_image') or "https://blog.gtowizard.com/content/2026/04/default.jpg",
        "summary_cards": summary_cards,
        "content_html": content_html
    })

# Write to data/articles.json
with open(os.path.join(BASE_DIR, 'data', 'articles.json'), 'w', encoding='utf-8') as f:
    json.dump(full_articles, f, ensure_ascii=False, indent=2)

print(f"Total processed full articles: {len(full_articles)}")
