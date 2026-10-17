import json
import os
import re
import sys
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXACT_CAPTION_MAP = {
    "Vs GTO": "GTO 기준 플레이",
    "vs GTO": "GTO 기준 플레이",
    "Vs a Maniac": "매니악(Maniac) 상대 플레이",
    "vs a Maniac": "매니악(Maniac) 상대 플레이",
    "Vs LAG": "LAG(루즈 어그레시브) 상대 플레이",
    "vs LAG": "LAG(루즈 어그레시브) 상대 플레이",
    "Vs TAG": "TAG(타이트 어그레시브) 상대 플레이",
    "vs TAG": "TAG(타이트 어그레시브) 상대 플레이",
    "Vs a Calling Station": "콜링 스테이션 상대 플레이",
    "vs a Calling Station": "콜링 스테이션 상대 플레이",
    "Vs Calling Station": "콜링 스테이션 상대 플레이",
    "vs Calling Station": "콜링 스테이션 상대 플레이",
    "Vs Nit": "니트(Nit) 상대 플레이",
    "vs Nit": "니트(Nit) 상대 플레이",
    "GTO Reaction": "GTO 이론적 대응",
    "TAG Reaction": "TAG 상대 시 반응",
    "LAG Reaction": "LAG 상대 시 반응",
    "GTO Donking Strategy": "GTO 동크 벳 전략",
    "LAG Donking Strategy": "LAG 동크 벳 전략",
    "C-Bet Vs GTO Opponent": "GTO 상대를 향한 C-bet 전략",
    "C-bet vs LAG": "LAG 상대를 향한 C-bet 전략",
    "Response to 25% Pot GTO Lead": "GTO의 25% 팟 리드 벳에 대한 대응",
    "Response to 25% Pot LAG lead": "LAG의 25% 팟 리드 벳에 대한 대응",
    "Vs GTO Lead": "GTO 리드 벳에 대한 대응",
    "Vs LAG Lead": "LAG 리드 벳에 대한 대응",
    "Classic": "클래식 토너먼트 레인지",
    "PKO": "PKO (바운티) 토너먼트 레인지",
    "Supported sites": "지원 포커 룸 및 사이트",
    "How to get your hand histories": "핸드 히스토리 추출 및 업로드 방법",
    "Upload Hands": "핸드 히스토리 업로드",
    "Sharpen Your Game With Our Most Customizable GTO Trainer Ever": "GTO 트레이너 실전 훈련 모드",
    "Watch the walkthrough of PLO in GTO Wizard": "GTO Wizard PLO 기능 시연 및 둘러보기",
    "Strategy View shows how your range plays at every decision point.": "각 의사결정 지점별 레인지 액션 전략 뷰",
    "The Ranges tab lets you compare both players’ ranges side by side.": "양 플레이어의 전체 레인지를 나란히 비교 분석하는 레인지 탭",
    "Stack sizes of players": "각 플레이어별 스택 크기 분포",
    "Response to 75% sizing": "75% 팟 사이징에 대한 대응",
    "Response to 100% sizing": "100% 팟(팟 사이즈)에 대한 대응",
    "Imbalanced": "익스플로잇 불균형 전략",
    "Exploitative": "익스플로잇 전략",
    "GTO": "GTO 균형 전략",
    "Chip EV": "칩EV (cEV) 기준",
    "chip EV": "칩EV (cEV) 기준",
    "ICM": "ICM (토너먼트 상금 모델) 기준",
    "Mastering PKOs With Custom Aggregated Reports": "어그리게이티드 리포트로 PKO 마스터하기",
    "Custom Profiles Go Live + PokerArena Season 5": "커스텀 프로필 기능 및 포커아레나 시즌 5",
    "Handling Loose-Passive Limpers": "루즈-패시브 림퍼 상대 전략",
    "How To Negotiate Final Table Deals": "파이널 테이블 딜 협상 가이드",
    "Quirks of Nash Equilibrium in Multiway": "멀티웨이 팟에서 내쉬 균형의 특징과 특이점",
    "Discipline, Study, Rest: The 3 Pillars of Poker Success": "규율, 복기, 휴식: 포커 성공의 3대 기둥",
    "A Guide To Game Selection in Poker": "테이블 및 게임 셀렉션 실전 가이드",
    "Top 5 Leaks in Low Stakes MTTs": "로우 스테이크 MTT 5대 핵심 릭(Leak)",
    "The Five Imbalances of Exploitative Poker": "익스플로이티브 포커의 5가지 불균형 원리",
    "Study the Games You Actually Play": "실제 플레이하는 게임 구조별 분석",
    "Pre-Solved vs Custom Solving : How It Works": "사전 솔빙 vs 커스텀 솔빙 구동 원리",
    "Hand Upload Integration": "핸드 히스토리 업로드 및 연동",
    "Nodelocking & Exploits": "노드락 설정 및 익스플로잇 분석",
    "Roadmap & Current Limitations": "로드맵 및 기능 안내",
    "Why Late-Stage Decisions Matter": "토너먼트 후반부 의사결정의 중요성",
    "2026 Main Event Example": "2026 WSOP 메인 이벤트 실전 핸드 분석",
    "The Limitations of Nash Equilibrium in ICM Spots": "ICM 상황에서 내쉬 균형의 한계와 실전 적용",
    "Fixing a Poker Leak Part 1: Spotting and Correcting Errors": "포커 릭(Leak) 교정 1편: 오류 포착 및 수정",
    "Fixing a Poker Leak Part 2: The Mental Game": "포커 릭(Leak) 교정 2편: 멘탈 게임 강화",
    "How Payout Structures Reshape Postflop Strategy": "페이아웃 구조가 포스트플랍 전략을 바꾸는 메커니즘",
    "The Limits of Nodelocking": "노드락(Nodelocking)의 한계와 주의점",
    "Mastering Thin Value Bets in Checked-Down Pots": "첵-다운 팟에서 씬 밸류 벳(Thin Value) 구사하기",
    "When To Encourage Multiway Pots in PKOs": "PKO 토너먼트에서 멀티웨이 팟을 유도해야 하는 스팟",
    "The Importance of Board Coverage": "보드 커버리지(Board Coverage)의 전략적 중요성",
    "Mastering Postflop ICM: Avoid These Common Mistakes": "포스트플랍 ICM 마스터: 자주 범하는 실수 방지법",
    "PKO Versus Classic: Responding to 3-Bets": "PKO vs 클래식: 3벳 대응 전략 비교",
    "How Stack Sizes Change Your Range": "스택 크기가 레인지에 미치는 영향 분석",
    "The Worst Turn Card": "가장 위험한 턴 카드와 전략적 대응",
    "GTO Wizard Themes Competition Winners": "GTO Wizard 커스텀 테마 수상작",
}

def is_valid_caption(text):
    if not text:
        return False
    t = text.strip()
    if len(t) < 3:
        return False
    if re.match(r'^(image|photo|picture|screenshot|screen shot|img|figure|untitled)[\s\d\-_]*$', t, re.IGNORECASE):
        return False
    if re.match(r'^data[\s\-_]src[\s\-_]image', t, re.IGNORECASE):
        return False
    if re.search(r'gto wizard .* (image|photo)', t, re.IGNORECASE):
        return False
    if re.match(r'^\d+$', t):
        return False
    return True

def clean_raw_caption(text):
    if not text:
        return ""
    t = re.sub(r'<[^>]+>', '', text).strip()
    t = re.sub(r'\s+', ' ', t)
    return t

def translate_caption_to_korean(raw_text, section_title="", filename=""):
    clean = clean_raw_caption(raw_text)
    
    if not is_valid_caption(clean):
        if filename:
            fn = os.path.splitext(filename)[0]
            fn_clean = re.sub(r'^[0-9]+[\.\-_]+', '', fn)
            fn_clean = re.sub(r'[\-_]+', ' ', fn_clean).strip()
            if is_valid_caption(fn_clean):
                clean = fn_clean
        if not is_valid_caption(clean):
            if section_title:
                sec_clean = re.sub(r'^[0-9]+\.\s*', '', section_title)
                sec_clean = re.sub(r'\s*\([^\)]*\)', '', sec_clean).strip()
                return f"{sec_clean} 솔버 시뮬레이션 분석"
            return "GTO Wizard 솔버 시뮬레이션 분석 차트"

    korean_chars = len(re.findall(r'[\uac00-\ud7a3]', clean))
    if korean_chars > len(clean) * 0.4:
        return clean

    if clean in EXACT_CAPTION_MAP:
        return EXACT_CAPTION_MAP[clean]

    res = clean

    # Arrow symbols in comparison charts
    res = re.sub(r'\(?\s*↑\s*\)?\s*and\s*\(?\s*↓\s*\)?', '(상단) 및 (하단) 비교', res)
    res = re.sub(r'\(?\s*↑\s*\)?', '(상단)', res)
    res = re.sub(r'\(?\s*↓\s*\)?', '(하단)', res)

    # Board descriptions: on [Board]
    res = re.sub(r'\bon\s+([AKQJT2-9]{2,3})\s*r\b', r'(\1 레인보우 보드에서)', res)
    res = re.sub(r'\bon\s+([AKQJT2-9]{2,3})\s*tt\b', r'(\1 투톤 보드에서)', res)
    res = re.sub(r'\bon\s+([AKQJT2-9]{2,3})\s*m\b', r'(\1 모노톤 보드에서)', res)
    res = re.sub(r'\bon\s+([AKQJT2-9][♠♥♦♣][AKQJT2-9][♠♥♦♣][AKQJT2-9][♠♥♦♣](?:\s*[AKQJT2-9][♠♥♦♣])*(?:\s*[AKQJT2-9][♠♥♦♣])*)\b', r'(\1 보드에서)', res)

    # Position on Board: e.g. "Two-Blind on 763tt"
    res = re.sub(r'\bTwo[- ]Blinds?\s+on\s+([AKQJT2-9]{2,3})\s*tt\b', r'\1 투톤 보드: 투 블라인드 상황', res, flags=re.IGNORECASE)
    res = re.sub(r'\bTwo[- ]Blinds?\s+on\s+([AKQJT2-9]{2,3})\s*r\b', r'\1 레인보우 보드: 투 블라인드 상황', res, flags=re.IGNORECASE)
    res = re.sub(r'\bButton\s+Straddles?\s+on\s+([AKQJT2-9]{2,3})\s*tt\b', r'\1 투톤 보드: 버튼 스트래들 상황', res, flags=re.IGNORECASE)
    res = re.sub(r'\bButton\s+Straddles?\s+on\s+([AKQJT2-9]{2,3})\s*r\b', r'\1 레인보우 보드: 버튼 스트래들 상황', res, flags=re.IGNORECASE)

    # Convert core poker actions before grammar assembly
    res = re.sub(r'(?<![a-zA-Z])open[- ]raises?(?![a-zA-Z])', '오픈 레이즈', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])3-bets?(?![a-zA-Z])', '3벳', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])4-bets?(?![a-zA-Z])', '4벳', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])5-bets?(?![a-zA-Z])', '5벳', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])c-bets?(?![a-zA-Z])', 'C-bet', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])donk\s+bets?(?![a-zA-Z])', '동크 벳', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])probe\s+bets?(?![a-zA-Z])', '프로브 벳', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])turn-probe(?![a-zA-Z])', '턴 프로브 벳', res, flags=re.IGNORECASE)

    # Grammar structural replacements (Position vs Position actions)
    res = re.sub(r'([A-Z0-9+]+)\s+response\s+vs\s+([A-Z0-9+]+)\s+(오픈 레이즈|open|3벳|4벳|raise|shove|jam)',
                r'\2의 \3에 대한 \1의 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'([A-Z0-9+]+)\s+response\s+when\s+opened\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)\s+and\s+(\w+)\s+(?:3벳|3-bets?)\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)',
                r'\1의 \2 오픈 후 \3의 \4 3벳에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'([A-Z0-9+]+)\s+response\s+when\s+opened\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)\s+and\s+(?:3벳|3-bet)\s+by\s+(\w+)\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)',
                r'\1의 \2 오픈 후 \3의 \4 3벳에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'response\s+when\s+opened\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)\s+and\s+(\w+)\s+(?:3벳|3-bets?)\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)',
                r'\1 오픈 후 \2의 \3 3벳에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'response\s+when\s+opened\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)\s+and\s+(?:3벳|3-bet)\s+by\s+(\w+)\s+to\s*(\d+(?:\.\d+)?(?:bb|str)?)',
                r'\1 오픈 후 \2의 \3 3벳에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'response\s+vs\s+([A-Z0-9+]+)[’\']s\s+(\d+%?\s*pot\s+)?(C-bet|동크 벳|프로브 벳|턴 프로브 벳|bet|raise|shove|jam)',
                r'\1의 \2\3에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'response\s+vs\s+([A-Z0-9+]+)\s+(오픈 레이즈|open|3벳|raise|shove|jam)',
                r'\1의 \2에 대한 대응', res, flags=re.IGNORECASE)
    res = re.sub(r'response\s+to\s+(\d+%?\s*pot\s+)?(C-bet|동크 벳|프로브 벳|bet|raise|sizing|jam|shove)',
                r'\1\2에 대한 대응', res, flags=re.IGNORECASE)

    # Opponent conditions: "when BB plays GTO"
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+plays\s+GTO\b', r'\1가 GTO로 플레이할 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+is\s+a\s+Calling\s+Station\b', r'\1가 콜링 스테이션일 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+is\s+a\s+Maniac\b', r'\1가 매니악일 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+is\s+a\s+TAG\b', r'\1가 TAG일 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+is\s+a\s+LAG\b', r'\1가 LAG일 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+is\s+a\s+Nit\b', r'\1가 니트일 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+checks?\b', r'\1가 체크했을 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+3-bets?\b', r'\1가 3벳했을 때', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+([A-Z0-9+]+)\s+c-bets?\b', r'\1가 C-bet했을 때', res, flags=re.IGNORECASE)

    # Flop board dynamic adjectives
    res = re.sub(r'\bDisconnected\s+flop\b', '언커넥티드 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bConnected\s+flop\b', '커넥티드 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bPaired\s+flop\b', '페어 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bMonotone\s+flop\b', '모노톤 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bTwo[- ]tone\s+flop\b', '투톤 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bRainbow\s+flop\b', '레인보우 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bDry\s+flop\b', '드라이 플랍', res, flags=re.IGNORECASE)
    res = re.sub(r'\bWet\s+flop\b', '웻(다이내믹) 플랍', res, flags=re.IGNORECASE)

    # Sizing and stacks
    res = re.sub(r'\bto\s+(\d+(?:\.\d+)?(?:bb|str))\b', r'\1로', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(\d+(?:\.\d+)?(?:bb|str))\s+deep\b', r'\1 딥', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(\d+(?:\.\d+)?(?:bb|str))\s+starting\b', r'시작 스택 \1', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(\d+(?:\.\d+)?(?:bb|str))\s+effective\b', r'유효 스택 \1', res, flags=re.IGNORECASE)
    res = re.sub(r'\bno\s+ante\s+game\b', '노 앤티 게임', res, flags=re.IGNORECASE)
    res = re.sub(r'\bno\s+rake\b', '노 레이크', res, flags=re.IGNORECASE)
    res = re.sub(r'\braked\b', '레이크 적용', res, flags=re.IGNORECASE)
    res = re.sub(r'\bunraked\b', '노 레이크', res, flags=re.IGNORECASE)
    res = re.sub(r'\bTwo[- ]blinds?\s+Hold’em\b', '투 블라인드 홀덤', res, flags=re.IGNORECASE)
    res = re.sub(r'\bTwo[- ]blinds?\b', '투 블라인드', res, flags=re.IGNORECASE)
    res = re.sub(r'\bButton\s+Straddles?\b', '버튼 스트래들', res, flags=re.IGNORECASE)
    res = re.sub(r'\bMississippi\s+Straddles?\b', '미시시피 스트래들', res, flags=re.IGNORECASE)
    res = re.sub(r'\bstraddle\+ante\b', '스트래들+앤티', res, flags=re.IGNORECASE)
    res = re.sub(r'\bstraddles?\b', '스트래들', res, flags=re.IGNORECASE)
    res = re.sub(r'\bno\s+ante\b', '노 앤티', res, flags=re.IGNORECASE)
    res = re.sub(r'\bante\b', '앤티', res, flags=re.IGNORECASE)

    res = re.sub(r'\baggregate\s+flop\s+c-betting\b', '전체 플랍 C-bet 어그리게이트 빈도', res, flags=re.IGNORECASE)
    res = re.sub(r'\baggregate\s+c-bet\s+flop\s+strategy\b', '전체 플랍 C-bet 어그리게이트 전략', res, flags=re.IGNORECASE)
    res = re.sub(r'\bflop\s+c-bet\s+aggregate\s+report\b', '플랍 C-bet 전체 종합 리포트', res, flags=re.IGNORECASE)

    res = re.sub(r'\bManhattan\s+plot\s+of\s+([A-Z0-9+]+)[’\']s\s+c-bet\s+strategy\s+across\s+all\s+flops\b',
                r'전체 플랍 기준 \1의 C-bet 전략 맨해튼 플롯 분포도', res, flags=re.IGNORECASE)

    res = re.sub(r'\bnodelocked\s+to\s+call\s+straights\s+and\s+below\b', '스트레이트 이하 콜로 노드락 적용', res, flags=re.IGNORECASE)
    res = re.sub(r'\bnodelocked\s+to\s+call\s+sets\s+and\s+below\b', '셋 이하 콜로 노드락 적용', res, flags=re.IGNORECASE)
    res = re.sub(r'\bnodelocked\s+to\s+call\b', '콜 빈도 노드락 적용', res, flags=re.IGNORECASE)
    res = re.sub(r'\bnodelocked\b', '노드락 적용', res, flags=re.IGNORECASE)

    res = re.sub(r'\bEQ\s+buckets\s+for\s+([A-Z0-9+]+)[’\']s\s+x/r\s+flop\s+range\b',
                r'\1의 플랍 첵-레이즈 레인지 에퀴티 버킷 분포', res, flags=re.IGNORECASE)

    res = re.sub(r'\bwhen\s+flop\s*=\s*X-B33-C\b', '플랍 첵-33%벳-콜 라인 진행 시', res, flags=re.IGNORECASE)
    res = re.sub(r'\bwhen\s+flop\s+checked\s+through\b', '플랍 첵-쓰루 진행 시', res, flags=re.IGNORECASE)

    res = re.sub(r'\bshort\s+stack\s+\(final\s+table\)\b', '파이널 테이블 숏스택 상황', res, flags=re.IGNORECASE)
    res = re.sub(r'\bshort\s+stack\b', '숏스택', res, flags=re.IGNORECASE)
    res = re.sub(r'\bdeep\s+stack\b', '딥스택', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])starting(?![a-zA-Z])', '시작 스택', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])effective(?![a-zA-Z])', '유효 스택', res, flags=re.IGNORECASE)
    res = re.sub(r'(?<![a-zA-Z])deep(?![a-zA-Z])', '딥', res, flags=re.IGNORECASE)

    # General replacements
    replacements = [
        (r'\bvs\.?\s*GTO\b', 'GTO 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*a?\s*LAG\b', 'LAG 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*a?\s*TAG\b', 'TAG 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*a?\s*Maniac\b', '매니악 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*a?\s*Calling Station\b', '콜링 스테이션 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*a?\s*Nit\b', '니트 상대 시', re.IGNORECASE),
        (r'\bvs\.?\s*', 'vs '),
        (r'\bresponse\s+to\b', '대응:', re.IGNORECASE),
        (r'\bresponse\s+vs\b', '대응: vs', re.IGNORECASE),
        (r'\bfacing\s+a\b', '직면 시:', re.IGNORECASE),
        (r'\bfacing\b', '직면 시', re.IGNORECASE),
        (r'\bopening\s+ranges?\b', '오픈 레인지', re.IGNORECASE),
        (r'\bopen\s+shove\b', '오픈 셔브', re.IGNORECASE),
        (r'\bcalling\s+ranges?\b', '콜링 레인지', re.IGNORECASE),
        (r'\bshove\s+ranges?\b', '셔브 레인지', re.IGNORECASE),
        (r'\bpush\s+ranges?\b', '푸시(올인) 레인지', re.IGNORECASE),
        (r'\bdefending\s+ranges?\b', '방어 레인지', re.IGNORECASE),
        (r'\b3-bet\s+jam\b', '3벳 잼(올인)', re.IGNORECASE),
        (r'\b3-bet\s+range\b', '3벳 레인지', re.IGNORECASE),
        (r'\b4-bet\s+range\b', '4벳 레인지', re.IGNORECASE),
        (r'\bc-bet\s+flop\s+strategy\b', '플랍 C-bet 전략', re.IGNORECASE),
        (r'\bflop\s+c-bet(ting)?\s+strategy\b', '플랍 C-bet 전략', re.IGNORECASE),
        (r'\bflop\s+c-bet(ting)?\b', '플랍 C-bet', re.IGNORECASE),
        (r'\bcontinuation\s+bet(ting)?\b', 'C-bet', re.IGNORECASE),
        (r'\bdonking\b', '동크 벳', re.IGNORECASE),
        (r'\bturn-probe\b', '턴 프로브 벳', re.IGNORECASE),
        (r'\btriple-barrel\s+river\s+strategy\b', '리버 트리플 배럴 전략', re.IGNORECASE),
        (r'\btriple-barrel\b', '트리플 배럴', re.IGNORECASE),
        (r'\bdouble-barrel\b', '더블 배럴', re.IGNORECASE),
        (r'\bbarrel\s+turn\s+strategy\b', '턴 배럴 전략', re.IGNORECASE),
        (r'\bbarrel\b', '배럴', re.IGNORECASE),
        (r'\bbarreling\b', '배럴링', re.IGNORECASE),
        (r'\bcheck-raise\b', '첵-레이즈', re.IGNORECASE),
        (r'\bx/r\b', '첵-레이즈', re.IGNORECASE),
        (r'\bcheck-call\b', '첵-콜', re.IGNORECASE),
        (r'\bx/c\b', '첵-콜', re.IGNORECASE),
        (r'\bcheck-fold\b', '첵-폴드', re.IGNORECASE),
        (r'\bx/f\b', '첵-폴드', re.IGNORECASE),
        (r'\bchecks?\s+through\b', '첵-쓰루', re.IGNORECASE),
        (r'\bchecked\s+through\b', '첵-쓰루', re.IGNORECASE),
        (r'\bflop\s+strategy\b', '플랍 전략', re.IGNORECASE),
        (r'\bturn\s+strategy\b', '턴 전략', re.IGNORECASE),
        (r'\briver\s+strategy\b', '리버 전략', re.IGNORECASE),
        (r'\bpreflop\s+strategy\b', '프리플랍 전략', re.IGNORECASE),
        (r'\bstrategy\b', '전략', re.IGNORECASE),
        (r'\bequity\s+realization\b', '에퀴티 실현(EQR)', re.IGNORECASE),
        (r'\bequity\b', '에퀴티(승률)', re.IGNORECASE),
        (r'\brange\s+compositions?\b', '레인지 구성', re.IGNORECASE),
        (r'\branges?\b', '레인지', re.IGNORECASE),
        (r'\baggregate\s+report\b', '전체 종합 리포트', re.IGNORECASE),
        (r'\baggregate\b', '전체 종합', re.IGNORECASE),
        (r'\bfinal\s+table\b', '파이널 테이블', re.IGNORECASE),
        (r'\bnear\s+bubble\b', '버블 직전', re.IGNORECASE),
        (r'\bbubble\b', '버블', re.IGNORECASE),
        (r'\bpot\s+odds\b', '팟 오즈', re.IGNORECASE),
        (r'\bpot\b', '팟', re.IGNORECASE),
        (r'\bsizings?\b', '사이징', re.IGNORECASE),
        (r'\bExploitative\b', '익스플로잇', re.IGNORECASE),
        (r'\bImbalanced\b', '불균형', re.IGNORECASE),
        (r'\bComparison\s+of\b', '비교:', re.IGNORECASE),
        (r'\bgame\b', '게임', re.IGNORECASE),
        (r'\bsingle-raised\s+pot\b', '싱글 레이즈드 팟(SRP)', re.IGNORECASE),
        (r'\bSRP\b', '싱글 레이즈드 팟(SRP)', re.IGNORECASE),
        (r'\b3BP\b', '3벳 팟(3BP)', re.IGNORECASE),
        (r'\b4BP\b', '4벳 팟(4BP)', re.IGNORECASE),
        (r'\bsymmetric\s+vs\s+asymmetric\s+stacks\b', '대칭 vs 비대칭 스택', re.IGNORECASE),
        (r'\bacross\s+all\s+flops\b', '전체 플랍 기준', re.IGNORECASE),
        (r'\bEQ\s+buckets\b', '에퀴티 버킷(구간별 분포)', re.IGNORECASE),
        (r'\bgood\s+hands\b', '강한 핸드', re.IGNORECASE),
        (r'\bto\s+call\s+straights\s+and\s+below\b', '스트레이트 이하 핸드로 콜', re.IGNORECASE),
        (r'\bto\s+call\s+sets\s+and\s+below\b', '셋 이하 핸드로 콜', re.IGNORECASE),
        (r'\bflop\s+report\s+sorted\s+by\s+bet\b', '베팅별 플랍 리포트 정렬:', re.IGNORECASE),
        (r'\bgrouped\s+by\s+connectedness\b', '보드 연결성(Connectedness)별 분류', re.IGNORECASE),
    ]

    for item in replacements:
        pat = item[0]
        rep = item[1]
        flag = item[2] if len(item) > 2 else 0
        res = re.sub(pat, rep, res, flags=flag)

    res = re.sub(r'\s+', ' ', res).strip()
    res = re.sub(r'\s*:\s*', ' : ', res)
    res = re.sub(r'\s*,\s*', ', ', res)
    return res

def process_articles():
    print("Loading datasets...")
    raw_path = os.path.join(BASE_DIR, 'data', 'raw_ghost_all.json')
    if not os.path.exists(raw_path):
        import urllib.request
        print("raw_ghost_all.json not found. Fetching from Ghost Content API...")
        api_key = 'cb7e32915ecd73eb2ca84c4b92'
        all_posts = []
        for page in range(1, 5):
            url = f'https://admin.blog.gtowizard.com/ghost/api/content/posts/?key={api_key}&limit=100&page={page}&fields=slug,title,html'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                all_posts.extend(data.get('posts', []))
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, ensure_ascii=False)
        print(f"Fetched and cached {len(all_posts)} posts.")

    with open(raw_path, encoding='utf-8') as f:
        raw_posts = json.load(f)

    with open(os.path.join(BASE_DIR, 'data', 'articles.json'), encoding='utf-8') as f:
        articles = json.load(f)

    print("Indexing raw Ghost figures with H3 fallback...")
    raw_img_map = {}
    for p in raw_posts:
        slug = p['slug']
        soup = BeautifulSoup(p.get('html', ''), 'html.parser')
        figs = soup.find_all('figure')
        
        last_valid_cap = ""
        for fig in figs:
            img = fig.find('img')
            if not img: continue
            src = img.get('src', '').strip()
            if not src: continue
            cap = fig.find('figcaption')
            cap_txt = cap.get_text(separator=' ', strip=True) if cap else ''
            alt_txt = img.get('alt', '').strip()

            target_txt = ""
            if is_valid_caption(cap_txt):
                target_txt = cap_txt
                last_valid_cap = cap_txt
            elif is_valid_caption(alt_txt):
                target_txt = alt_txt
                last_valid_cap = alt_txt
            else:
                prev_h = fig.find_previous(['h3', 'h4'])
                h_txt = prev_h.get_text(strip=True) if prev_h else ""
                if is_valid_caption(h_txt):
                    target_txt = h_txt
                elif last_valid_cap:
                    target_txt = f"{last_valid_cap} 세부 분석"

            raw_img_map[(slug, src)] = target_txt
            raw_img_map[(slug, src.split('?')[0])] = target_txt
            if src not in raw_img_map:
                raw_img_map[src] = target_txt
            if src.split('?')[0] not in raw_img_map:
                raw_img_map[src.split('?')[0]] = target_txt

    total_images_updated = 0
    total_duplicates_pruned = 0

    print("Updating articles with localized image captions...")
    for art in articles:
        slug = art['slug']
        html = art.get('content_html', '')
        if not html: continue

        parts = re.split(r'(<h2[^>]*>.*?</h2>)', html, flags=re.DOTALL)
        new_parts = []
        new_parts.append(parts[0])

        i = 1
        current_heading = ""
        while i < len(parts):
            h2_tag = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ""
            i += 2

            current_heading = re.sub(r'<[^>]+>', '', h2_tag).strip()

            wrapper_pattern = r'<div class=[\'"]article-chart-wrapper[\'"][^>]*>[\s\S]*?</div>\s*</div>'
            wrappers = re.findall(wrapper_pattern, body)

            if not wrappers:
                new_parts.append(h2_tag)
                new_parts.append(body)
                continue

            seen_last_src = None
            processed_wrappers = []

            for w in wrappers:
                src_match = re.search(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', w)
                if not src_match:
                    processed_wrappers.append(w)
                    continue
                
                img_src = src_match.group(1).strip()
                if img_src == seen_last_src:
                    total_duplicates_pruned += 1
                    continue
                seen_last_src = img_src

                target_raw = raw_img_map.get((slug, img_src)) or raw_img_map.get((slug, img_src.split('?')[0])) or raw_img_map.get(img_src) or ""
                filename = img_src.split('/')[-1]
                korean_cap = translate_caption_to_korean(target_raw, section_title=current_heading, filename=filename)

                new_wrapper = (
                    f'<div class="article-chart-wrapper" style="margin: 1.75rem 0; text-align: center;">\n'
                    f'  <img src="{img_src}" alt="{korean_cap}" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 16px rgba(0,0,0,0.3);" loading="lazy">\n'
                    f'  <div class="article-chart-caption" style="font-size: 0.84rem; color: var(--text-muted); margin-top: 0.55rem; font-weight: 600; line-height: 1.45; word-break: keep-all;">📊 {korean_cap}</div>\n'
                    f'</div>'
                )
                processed_wrappers.append(new_wrapper)
                total_images_updated += 1

            split_body = re.split(wrapper_pattern, body)
            reconstructed_body = ""
            for idx, text_chunk in enumerate(split_body):
                reconstructed_body += text_chunk
                if idx < len(processed_wrappers):
                    reconstructed_body += "\n" + processed_wrappers[idx] + "\n"

            new_parts.append(h2_tag)
            new_parts.append(reconstructed_body)

        art['content_html'] = "".join(new_parts)

    print(f"Total charts updated with Korean captions: {total_images_updated}")
    print(f"Total consecutive duplicate charts removed: {total_duplicates_pruned}")

    target_path = os.path.join(BASE_DIR, 'data', 'articles.json')
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved updated articles to {target_path}!")

if __name__ == '__main__':
    process_articles()
