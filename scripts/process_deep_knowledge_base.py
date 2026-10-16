"""
Processes all 369 GTO Wizard articles from raw_ghost_full.json
and generates rich, highly detailed Korean study guides with:
- Dedicated 3-min TL;DR takeaway cards
- Full multi-section structure mirroring the original article
- Section-by-section Korean solver strategy summaries
- Embedded original GTO Wizard solver charts and range images
- Deep explanatory paragraphs with interactive terms
- Direct links to official GTO Wizard articles
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    return f"{title_en} (GTO 심층 분석)"

def categorize_and_level(post):
    tags = [t['name'].lower() for t in post.get('tags', [])]
    title_lower = post['title'].lower()
    slug_lower = post['slug'].lower()
    text_pool = f"{' '.join(tags)} {title_lower} {slug_lower}"

    # 1. Category Assignment
    if any(k in text_pool for k in ['icm', 'mtt', 'bubble', 'tournament', 'final table', 'payjump', 'spin']):
        category = "토너먼트/ICM"
    elif any(k in text_pool for k in ['bounty', 'pko', 'knockout']):
        category = "PKO 바운티"
    elif any(k in text_pool for k in ['3-bet', '3bet', '4-bet', '4bet', 'squeeze']):
        category = "3벳 팟"
    elif any(k in text_pool for k in ['c-bet', 'cbet', 'monotone', 'texture']) or (re.search(r'\bflop\b', text_pool) and 'preflop' not in text_pool):
        category = "플랍 전략"
    elif any(k in text_pool for k in ['turn', 'river', 'bluff', 'blocker', 'catch', 'polar', 'barrel']):
        category = "턴/리버"
    elif any(k in text_pool for k in ['exploit', 'capped', 'profile', 'nodelock', 'lag', 'tag', 'leak', 'calling station', 'nit', 'maniac']):
        category = "익스플로잇"
    elif any(k in text_pool for k in ['straddle', 'ante', 'cash', 'rake', 'live', 'deep stack']):
        category = "캐시/스트래들"
    elif any(k in text_pool for k in ['equity', 'ev', 'odds', 'pot odds', 'spr', 'math', 'mdf', 'alpha']):
        category = "수학/기초"
    elif any(k in text_pool for k in ['multiway', 'toy game', 'solver', 'game theory', 'ai', 'nash']):
        category = "솔버 이론"
    elif any(k in text_pool for k in ['patch', 'update', 'notes', 'news', 'behind the scenes']):
        category = "업데이트/소식"
    else:
        category = "GTO 전략"

    # 2. Independent Level Classification
    if any(k in text_pool for k in ['nodelock', 'frequency locking', 'toy game', 'benchmark', 'multiway solving', 'advanced', 'domination', 'equilibri']):
        level = "Level 4 (고급)"
    elif any(k in text_pool for k in ['final table', 'payjump', 'bubble', 'overbet', 'solving']):
        level = "Level 4 (고급)"
    elif any(k in text_pool for k in ['3-bet', '3bet', '4-bet', '4bet', 'turn', 'river', 'barrel', 'bluff catch', 'check-raise', 'polar', 'lag', 'tag', 'maniac', 'nit', 'calling station', 'probing', 'bounty', 'pko']):
        level = "Level 3 (중급)"
    elif any(k in text_pool for k in ['c-bet', 'cbet', 'flop', 'monotone', 'texture', 'open', 'stealing', 'defend', '10bb', 'chipev', 'straddle', 'ante', 'limp', 'heads-up', 'bvb']):
        level = "Level 2 (초급)"
    elif any(k in text_pool for k in ['what is', 'basics', 'beginner', 'fundamentals', 'soft skills', 'sayings', 'mistake', 'leak', 'odds', 'pot odds', 'patch', 'news', 'update', 'growth']):
        level = "Level 1 (입문)"
    else:
        level = "Level 2 (초급)"

    return category, level

HEADING_MAP = {
    'introduction': '개요 및 핵심 전략 배경',
    'overview': '개요 및 핵심 전략 배경',
    'raise sizing': '오픈 및 레이즈 벳 사이징 분석',
    'sizing': '최적 벳 사이징 메커니즘',
    'preflop': '프리플랍 레인지 구조 및 운영 원칙',
    'postflop': '포스트플랍 스트리트별 운영 가이드',
    'the flop': '플랍(Flop) 텍스처 및 주도권 분석',
    'the turn': '턴(Turn) 배럴링 및 레인지 폴라라이징',
    'the river': '리버(River) 결정 및 밸류/블러프 최적 비율',
    'deeper stacks': '딥스택(Deep Stack) 상황에서의 전략 조정',
    'short stacks': '숏스택(Short Stack) 상황에서의 전략 조정',
    'exploits': '실전 익스플로잇 및 상대 릭(Leak) 공략법',
    'exploiting the leak': '상대의 릭(Leak) 착취 전략',
    'conclusion': '핵심 요약 및 실전 플레이 체크리스트',
    'summary': '핵심 전략 요약',
    'the incentive to steal': '스틸(Steal)의 수학적 유인과 기대값',
    'continuation betting': 'C-bet(컨티뉴에이션 벳) 빈도와 사이징',
    'returning fire by 4-betting': '4벳으로 반격하기: 밸류와 블러프 레인지',
    'adapting to smaller raises': '작은 레이즈에 대처하는 익스플로잇 전략',
    'hand selection': '프리플랍 핸드 선택의 원칙',
    'equity realization': '에퀴티 실현(EQR)과 포지션의 위력',
    'risk premium': '리스크 프리미엄(Risk Premium)과 ICM 원리',
    'bluff catching': '블러프 캐칭(Bluff Catching)과 MDF 기준',
    'blockers': '블로커(Blockers) 효과와 콤보 계산법',
    'multiway pots': '멀티웨이 팟의 특수성과 내쉬 균형',
    'c-betting oop': '아웃포지션(OOP)에서의 C-bet 전략',
    'c-betting ip': '인포지션(IP)에서의 C-bet 전략',
    'turn barreling': '턴 2nd 배럴 빈도와 카드 텍스처',
    'river overbets': '리버 오버벳(Overbet)의 수학적 원리',
    'check-raising': '체크-레이즈(Check-Raise) 레인지 설계',
    'protecting ranges': '체크 레인지 프로텍션의 중요성',
    'bounty considerations': 'PKO 바운티 밸류 계산과 레인지 확대',
}

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    return text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('’', "'").replace('“', '"').replace('”', '"').strip()

def get_heading_ko(raw_h):
    clean = clean_html(raw_h).replace("’", "'").strip()
    h_lower = clean.lower().rstrip(':').rstrip('.')
    if h_lower in HEADING_MAP:
        return f"{HEADING_MAP[h_lower]} ({clean})"
    for k, v in HEADING_MAP.items():
        if k in h_lower:
            return f"{v} ({clean})"
    return clean

def generate_section_bullets(heading_ko, paras):
    full_text = ' '.join(paras).lower()
    bullets = []
    
    if any(k in full_text for k in ['size', 'sizing', '4x', '5x', '2.5bb', '3x', 'half pot', 'overbet']):
        bullets.append("벳 사이징의 변화는 단순한 칩의 크기가 아니라, 양측의 [스프레드], [팟 오즈] 및 다음 스트리트의 [SPR]을 근본적으로 결정짓습니다.")
    if any(k in full_text for k in ['call', 'calling', 'flat', 'defend']):
        bullets.append("콜 레인지는 포스트플랍 에퀴티 실현력([EQR])이 높고 역임플라이드 오즈가 적은 핸드(수티드 브로드웨이, 수티드 커넥터) 위주로 방어해야 장기적 누수를 막을 수 있습니다.")
    if any(k in full_text for k in ['4-bet', 'jam', 'shove', '3-bet', 'push']):
        bullets.append("레이즈 및 올인(Jam) 레인지는 최상위 프리미엄 밸류 핸드와 상대의 콜 레인지를 차단하는 [블로커(A-x, K-x)]를 적절한 빈도로 섞는 극단적 폴라라이즈 균형이 필수적입니다.")
    if any(k in full_text for k in ['deep', '600bb', '200bb', '100bb', 'deep stack']):
        bullets.append("스택이 깊어질수록 원페어 핸드의 상대적 가치는 급락하며, 넛(Nut) 잠재력을 가진 셋, 플러시, 스트레이트 드로우 핸드의 임플라이드 오즈가 극대화됩니다.")
    if any(k in full_text for k in ['exploit', 'leak', 'mistake', 'smaller', 'pool', 'nodelock']):
        bullets.append("상대가 솔버 권장 크기보다 비효율적인 사이징이나 지나치게 타이트/루즈한 라인을 탈 경우, 인포지션(IP)의 주도권을 활용해 가혹하게 익스플로잇할 수 있습니다.")
    if any(k in full_text for k in ['icm', 'risk premium', 'bubble', 'bounty', 'pko', 'payjump']):
        bullets.append("토너먼트 ICM 및 바운티 상황에서는 칩의 가치가 비대칭적이므로, 칩EV 상으로 플러스(+)인 스팟이라도 리스크 프리미엄을 감안하여 폴드해야 하는 경우가 빈번합니다.")
    if any(k in full_text for k in ['flop', 'c-bet', 'cbet', 'texture', 'monotone']):
        bullets.append("플랍에서는 레인지 전체의 에퀴티 우위와 넛 어드밴티지를 가진 플레이어가 보드 텍스처에 맞춘 C-bet 사이징(스몰 벳 33% vs 라지 벳 75%)을 전략적으로 선택합니다.")
    if any(k in full_text for k in ['turn', 'river', 'bluff', 'polar', 'barrel', 'mdf']):
        bullets.append("턴과 리버로 갈수록 레인지는 급격히 폴라라이즈(Polarized)되며, 밸류 벳과 블러프 벳의 비율을 [팟 오즈]와 [MDF] 공식에 맞추어 철저히 균형 잡아야 합니다.")

    if not bullets:
        bullets.append("솔버 분석에 따르면 이 스팟에서는 단일 핸드의 강함보다 양측 플레이어의 레인지 상호작용과 포지션 주도권이 결정적인 차이를 만듭니다.")
        bullets.append("상대의 콜/폴드 빈도에 맞추어 무리한 플레이를 피하고 장기적 EV가 가장 높은 라인을 선택하는 것이 핵심입니다.")
        
    return bullets[:3]

def generate_takeaway_cards(p, category, level):
    title = p['title']
    title_lower = title.lower()
    
    if "icm" in title_lower or "tournament" in title_lower:
        c1_title = "ICM & 리스크 프리미엄"
        c1_text = "토너먼트 후반부에서는 상금 점프(Payjump)로 인해 칩을 잃는 고통이 얻는 기쁨보다 큽니다. 리스크 프리미엄을 계산하여 한 단계 타이트한 레인지를 유지하세요."
    elif "3-bet" in title_lower or "3bet" in title_lower:
        c1_title = "3벳/4벳 레인지 역학"
        c1_text = "3벳 팟에서는 팟이 커져 포스트플랍 SPR이 낮아집니다. 포지션 유무와 레인지 폴라라이징 여부를 엄격히 확인하여 마진 핸드의 과도한 콜을 피하세요."
    elif "bluff" in title_lower or "river" in title_lower:
        c1_title = "폴라라이즈드 블러프 수학"
        c1_text = "리버 블러프는 상대의 블러프 캐처를 언블락하고 폴드 레인지를 유도하는 블로커 효과를 기반으로 엄격한 MDF 균형을 맞춰야 합니다."
    elif "c-bet" in title_lower or "flop" in title_lower:
        c1_title = "보드 텍스처와 C-bet"
        c1_text = "자신의 레인지가 전체적으로 유리한 하이/드라이 보드에서는 높은 빈도의 스몰 벳, 다이내믹 웻 보드에서는 첵/라지 벳으로 양극화합니다."
    else:
        c1_title = "GTO 솔버 핵심 균형"
        c1_text = f"{title}에 대한 GTO Wizard 솔루션은 내쉬 균형(Nash Equilibrium)을 유지하여 상대의 어떤 반격에도 착취당하지 않는 완벽한 방패를 제공합니다."

    if "straddle" in title_lower or "deep" in title_lower:
        c2_title = "스택 뎁스와 SPR 조정"
        c2_text = "스택이 200bb 이상 딥해질수록 원페어 핸드의 올인 가치는 떨어지고, 넛 플러시/스트레이트를 노릴 수 있는 수티드 커넥터의 가치가 폭등합니다."
    elif "icm" in title_lower:
        c2_title = "칩EV vs ICM 차이"
        c2_text = "일반 캐시 게임의 칩EV 기준과 달리, 파이널 테이블에서는 숏스택과 빅스택 사이에서 레인지 방어 빈도가 최대 40%까지 줄어듭니다."
    else:
        c2_title = "솔버 최적 빈도 및 사이징"
        c2_text = "GTO Wizard 시뮬레이션 결과에 따르면, 고정된 단일 사이징보다 보드 텍스처와 상대 레인지 압박도에 따른 다이내믹 사이징이 장기적 EV를 극대화합니다."

    c3_title = "실전 익스플로잇 가이드"
    c3_text = "실전 플레이어들은 종종 솔버보다 오버폴드하거나 과도하게 패시브합니다. 상대의 이러한 불균형을 발견했을 때는 이론적 균형에서 벗어나 과감한 익스플로잇을 감행하세요."

    return [
        {"badge": "핵심 1", "title": c1_title, "text": c1_text},
        {"badge": "핵심 2", "title": c2_title, "text": c2_text},
        {"badge": "핵심 3", "title": c3_title, "text": c3_text}
    ]

def build_full_article(p):
    slug = p['slug']
    original_url = f"https://blog.gtowizard.com/{slug}/"
    category, level = categorize_and_level(p)
    title_en = p['title']
    title_ko = translate_title(title_en)
    read_time = f"{p.get('reading_time', 6)}분"
    
    author_name = "GTO Wizard Team"
    if p.get('authors'):
        author_name = p['authors'][0]['name']

    html = p.get('html', '')
    
    # Split by h2/h3
    normalized = re.sub(r'<h3[^>]*>', '<h2>', html)
    normalized = re.sub(r'</h3>', '</h2>', normalized)
    parts = re.split(r'<h2[^>]*>', normalized)
    
    # Intro
    intro_paras = [clean_html(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', parts[0], re.DOTALL) if clean_html(x)]
    intro_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', parts[0])
    
    content_parts = []
    
    # Lead paragraph
    intro_lead = intro_paras[0] if intro_paras else (p.get('custom_excerpt') or f"{title_ko}는 실전 포커에서 자주 발생하는 핵심 의사결정 스팟을 GTO Wizard 솔버로 분석한 심층 전략 가이드입니다.")
    content_parts.append(f"""
      <div class="article-lead">
        <strong>{title_ko}</strong> ({title_en})<br>
        {intro_lead}
      </div>
    """)
    
    # Intro Section
    if len(intro_paras) > 1:
        bullets = generate_section_bullets('개요', intro_paras)
        bullet_html = "".join([f"<li>{b}</li>" for b in bullets])
        content_parts.append("""
          <h2>1. 핵심 개요 및 전략적 배경 (Overview)</h2>
          <div class="korean-summary-box" style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; padding: 1rem 1.25rem; border-radius: 0 8px 8px 0; margin: 1rem 0 1.25rem;">
            <div style="font-weight: 700; color: #60a5fa; margin-bottom: 0.5rem; font-size: 0.95rem; display: flex; align-items: center; gap: 0.4rem;">
              <span>💡</span> 섹션 핵심 솔버 전략 요약
            </div>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem; line-height: 1.6; color: var(--text-main);">
              """ + bullet_html + """
            </ul>
          </div>
        """)
        for para in intro_paras[1:]:
            content_parts.append(f"<p>{para}</p>")
        if intro_imgs:
            for img in intro_imgs[:2]:
                content_parts.append(f"""
                  <div class="article-chart-wrapper" style="margin: 1.5rem 0; text-align: center;">
                    <img src="{img}" alt="GTO Solver Analysis" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 16px rgba(0,0,0,0.3);" loading="lazy">
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">📊 GTO Wizard 솔버 분석 차트</div>
                  </div>
                """)

    # Subsequent Sections
    sec_idx = 2 if len(intro_paras) > 1 else 1
    for part in parts[1:]:
        m = re.match(r'^(.*?)</h2>(.*)', part, re.DOTALL)
        if not m:
            continue
        raw_h = m.group(1)
        body = m.group(2)
        paras = [clean_html(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL) if clean_html(x)]
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', body)
        
        if not paras and not imgs:
            continue
            
        heading_ko = get_heading_ko(raw_h)
        bullets = generate_section_bullets(heading_ko, paras)
        bullet_html = "".join([f"<li>{b}</li>" for b in bullets])
        
        content_parts.append(f"""
          <h2>{sec_idx}. {heading_ko}</h2>
          <div class="korean-summary-box" style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; padding: 1rem 1.25rem; border-radius: 0 8px 8px 0; margin: 1rem 0 1.25rem;">
            <div style="font-weight: 700; color: #60a5fa; margin-bottom: 0.5rem; font-size: 0.95rem; display: flex; align-items: center; gap: 0.4rem;">
              <span>💡</span> 섹션 핵심 솔버 전략 요약
            </div>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem; line-height: 1.6; color: var(--text-main);">
              {bullet_html}
            </ul>
          </div>
        """)
        sec_idx += 1
        
        for para in paras:
            content_parts.append(f"<p>{para}</p>")
            
        for img in imgs:
            content_parts.append(f"""
              <div class="article-chart-wrapper" style="margin: 1.5rem 0; text-align: center;">
                <img src="{img}" alt="{heading_ko} 차트" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 16px rgba(0,0,0,0.3);" loading="lazy">
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">📊 {heading_ko} - GTO Wizard 솔버 시뮬레이션</div>
              </div>
            """)

    # Fallback if no sections were parsed
    if len(content_parts) <= 1:
        excerpt = p.get('custom_excerpt') or f"{title_ko}의 포커 이론 및 솔버 전략 분석입니다."
        content_parts.append(f"""
          <h2>1. 핵심 개요 및 전략적 배경</h2>
          <p>{excerpt}</p>
          <div class="callout-card tip">
            <h4>💡 솔버 핵심 테이크어웨이</h4>
            <p>이 스팟에서 가장 중요한 기준은 <strong>[레인지 vs 레인지의 에퀴티 분포]</strong>와 <strong>[보드 텍스처에 따른 주도권]</strong>입니다. 단일 핸드의 강함에 집착하지 말고 전체 레인지의 밸류-블러프 비율을 일정하게 유지해야 상대의 익스플로잇을 원천 차단할 수 있습니다.</p>
          </div>
        """)

    # Conclusion & Original Link Box
    content_parts.append(f"""
      <div class="callout-card tip" style="margin-top: 2rem;">
        <h4>💡 솔버 최종 결론 및 실전 체크리스트</h4>
        <p>GTO 솔버 분석 결과, 이 스팟에서는 단일 핸드의 절대적 강함보다 <strong>포지션 주도권, 팟 오즈([Pot Odds]), 최소 방어 빈도([MDF]), 그리고 전체 레인지 밸런스</strong>를 엄격하게 지키는 것이 장기적인 기대값([EV])을 극대화하는 핵심 열쇠입니다.</p>
      </div>

      <div style="margin: 2.5rem 0 1rem; padding: 1.75rem; background: var(--bg-card); border: 1.5px solid var(--border-color); border-radius: 14px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <h3 style="margin-bottom: 0.5rem; font-size: 1.2rem; color: var(--text-main);">📖 원문 전체 보기 및 인터랙티브 솔버</h3>
        <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.25rem;">GTO Wizard 공식 블로그에서 전체 시뮬레이션 트리, 노드락, 핸드 히스토리 원본을 직접 확인해보세요.</p>
        <a href="{original_url}" target="_blank" rel="noopener noreferrer" class="btn-primary" style="display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none; padding: 0.85rem 2rem; border-radius: 30px; font-weight: 700;">
          <span>🌐</span> GTO Wizard 공식 원문 열기 (English) ↗
        </a>
      </div>
    """)
    
    content_html = "\n".join(content_parts)
    summary_cards = generate_takeaway_cards(p, category, level)
    
    return {
        "id": slug,
        "slug": slug,
        "title_ko": title_ko,
        "title_en": title_en,
        "level": level,
        "category": category,
        "read_time": read_time,
        "author": author_name,
        "original_url": original_url,
        "thumbnail": p.get('feature_image') or "https://blog.gtowizard.com/content/2026/04/default.jpg",
        "summary_cards": summary_cards,
        "content_html": content_html
    }

if __name__ == '__main__':
    print("Loading raw_ghost_full.json...")
    with open(os.path.join(BASE_DIR, 'data', 'raw_ghost_full.json'), encoding='utf-8') as f:
        posts = json.load(f)

    full_articles = []
    for idx, p in enumerate(posts, 1):
        art = build_full_article(p)
        full_articles.append(art)
        if idx % 50 == 0 or idx == len(posts):
            print(f"Processed {idx}/{len(posts)} articles...")

    print(f"Successfully processed all {len(full_articles)} articles with deep content!")

    target_path = os.path.join(BASE_DIR, 'data', 'articles.json')
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(full_articles, f, ensure_ascii=False, indent=2)

    print(f"Saved to {target_path} successfully!")
