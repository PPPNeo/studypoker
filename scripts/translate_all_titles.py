import json
import re

# Comprehensive dictionary and pattern replacements for poker concepts
TRANSLATION_MAP = {
    # Full specific title overrides
    "Responding to 3-bets in Straddle+Ante Games": "스트래들+앤티 게임에서 3벳 대응 전략",
    "Stealing and Restealing in Straddle+Ante Games": "스트래들+앤티 게임의 스틸 및 리스틸 전략",
    "Now Live: Preflop ICM Solving": "프리플랍 ICM 솔빙 기능 공식 출시",
    "Exploiting Profiles: Episode V – The LAG": "상대 프로필별 익스플로잇 V – 루즈 어그레시브(LAG)",
    "Exploiting Profiles: Episode IV – The TAG": "상대 프로필별 익스플로잇 IV – 타이트 어그레시브(TAG)",
    "Exploiting Profiles: Episode III – The Maniac": "상대 프로필별 익스플로잇 III – 매니악(Maniac)",
    "Exploiting Profiles: Episode II – The Nit": "상대 프로필별 익스플로잇 II – 니트(Nit)",
    "Exploiting Profiles: Episode I – The Calling Station": "상대 프로필별 익스플로잇 I – 콜링 스테이션",
    "PLO Upgrades: Custom HU Solving, Postflop ICM, Nodelocking & More": "PLO 업그레이드: 커스텀 헤즈업 솔빙, 포스트플랍 ICM & 노드락",
    "Playing Under 10bb – Part 2: ICM": "10bb 이하 숏스택 플레이 2편: ICM 상황",
    "Playing Under 10bb – Part 1: cEV": "10bb 이하 숏스택 플레이 1편: 칩EV(cEV) 기준",
    "The Four-Point Checklist for Calling Turn Barrels": "턴 배럴에 콜하기 전 확인해야 할 4가지 체크리스트",
    "3-Way: How to Exploit a Calling Station?": "3웨이 팟: 콜링 스테이션을 익스플로잇하는 방법",
    "Small Blind, Big Problems: When to Size Up From OOP BvB": "스몰 블라인드의 고민: BvB 아웃포지션에서 벳 사이징을 키워야 할 때",
    "Is Limping Preflop Viable in Mississippi Straddle Games?": "미시시피 스트래들 게임에서 프리플랍 림프는 유효할까?",
    "Navigating BvB OOP After Check-Calling the Flop": "플랍 첵-콜 이후 BvB 아웃포지션 턴/리버 운영법",
    "When to Open Shove vs. Different Player Profiles": "상대 성향(프로필)별 오픈 셔브 기준과 타이밍",
    "Probing in 3-Way Pots": "3웨이 팟에서의 프로브 벳(Probe Bet) 전략",
    "Playing In Position Against Two Callers": "두 명의 콜러를 상대로 인포지션(IP) 플레이하기",
    "Monkey in the Middle: 3-Way Pot Heuristics": "3웨이 팟 한가운데 샌드위치되었을 때의 휴리스틱",
    "The Trouble With Implied Odds": "임플라이드 오즈(Implied Odds)의 함정과 한계",
    "The Art of Value Bluffing From the Button": "버튼에서의 밸류 블러핑(Value Bluffing)의 기술",
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
    "The Case for the Hero Check: Why Great Players Know When Not to Bet": "히어로 체크: 고수들이 벳을 참는 이유",
}

# General patterns for translation
PATTERNS = [
    (r'(?i)\bHow to Play\b', '플레이 가이드:'),
    (r'(?i)\bHow to\b', '~하는 법:'),
    (r'(?i)\bThe Art of\b', '완벽 가이드:'),
    (r'(?i)\bA Guide to\b', '완벽 가이드:'),
    (r'(?i)\bComplete Guide to\b', '완벽 가이드:'),
    (r'(?i)\bMastering\b', '마스터하기:'),
    (r'(?i)\bExploiting\b', '익스플로잇:'),
    (r'(?i)\bCrushing\b', '정복하기:'),
    (r'(?i)\bWhen to\b', '언제 ~해야 하는가:'),
    (r'(?i)\bWhy You(?:\'re| are)\b', '왜 당신이'),
    (r'(?i)\bWhat is\b', '무엇인가:'),
    (r'(?i)\bIn-Position\b', '인포지션(IP)'),
    (r'(?i)\bOut of Position\b', '아웃포지션(OOP)'),
    (r'(?i)\bSmall Blind\b', '스몰 블라인드(SB)'),
    (r'(?i)\bBig Blind\b', '빅 블라인드(BB)'),
    (r'(?i)\bButton\b', '버튼(BTN)'),
    (r'(?i)\bSingle Raised Pot\b', 'SRP(싱글 레이즈드 팟)'),
    (r'(?i)\b3-Bet Pot\b', '3벳 팟'),
    (r'(?i)\b4-Bet Pot\b', '4벳 팟'),
    (r'(?i)\bCash Games?\b', '캐시 게임'),
    (r'(?i)\bTournaments?\b', '토너먼트'),
    (r'(?i)\bCheck-Raising\b', '체크-레이즈'),
    (r'(?i)\bCheck-Calling\b', '체크-콜'),
    (r'(?i)\bOverbetting\b', '오버벳'),
    (r'(?i)\bOverbets?\b', '오버벳'),
    (r'(?i)\bBlockers?\b', '블로커'),
    (r'(?i)\bBluff Catching\b', '블러프 캐칭'),
    (r'(?i)\bBluffing\b', '블러핑'),
    (r'(?i)\bEquity Realization\b', '에퀴티 실현(EQR)'),
    (r'(?i)\bExpected Value\b', '기대값(EV)'),
    (r'(?i)\bMinimum Defense Frequency\b', '최소 방어 빈도(MDF)'),
    (r'(?i)\bPot Odds\b', '팟 오즈'),
    (r'(?i)\bImplied Odds\b', '임플라이드 오즈'),
]

def translate(title):
    # Check exact match first
    if title in TRANSLATION_MAP:
        return TRANSLATION_MAP[title]
    
    # Check normalized match
    clean = title.strip().replace("’", "'")
    if clean in TRANSLATION_MAP:
        return TRANSLATION_MAP[clean]

    # Partial / keyword smart translations
    t = clean
    for pat, rep in PATTERNS:
        t = re.sub(pat, rep, t)
    
    if t != clean:
        return t
    
    # If untouched, provide friendly poker topic format
    return f"{title} (GTO 분석)"

if __name__ == '__main__':
    with open('scripts/all_titles.txt', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]
    
    translated = [translate(t) for t in titles]
    print(f"Sample translations (total {len(translated)}):")
    for orig, trans in zip(titles[:15], translated[:15]):
        print(f"EN: {orig}\nKO: {trans}\n")
