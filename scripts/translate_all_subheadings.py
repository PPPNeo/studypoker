import sys, os, json, re, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'data', 'articles.json')

# 1. Exact Heading Map for common and high-value poker articles
heading_exact_map = {
    # Expected Value article
    "Where Does EV Come From?": "기대값(EV)은 어디에서 발생하는가?",
    "Where Does EV Come From": "기대값(EV)은 어디에서 발생하는가?",
    "Fold EV, Denying Equity and Folding out Worse": "폴드 EV: 에퀴티 차단과 열세 핸드 폴드 유도",
    "Thin Block-Bet Example": "씬 블락-벳(Block-Bet) 실전 예시",
    "EV Relativity": "기대값(EV)의 상대성 원리",
    "EV Units of Measurement": "기대값(EV)의 측정 단위 (bb, $, chips)",
    "EV Defined": "기대값(EV)의 수학적 정의",
    "Deriving Other Poker Metrics from EV": "기대값(EV)으로부터 다른 포커 지표 도출하기",
    "Example 1:": "실전 예시 1:",
    "Example 2:": "실전 예시 2:",
    "Example 3:": "실전 예시 3:",
    "Example 4:": "실전 예시 4:",
    "Example 5:": "실전 예시 5:",
    "Example 1": "실전 예시 1",
    "Example 2": "실전 예시 2",
    "Example 3": "실전 예시 3",
    "Example 4": "실전 예시 4",
    "Example 5": "실전 예시 5",
    "Example": "실전 핸드 예시",

    # Preflop & Positions
    "Comparison of BTN's Responses vs. SB 3-Bets": "SB 3벳에 대한 BTN의 대응 전략 비교",
    "Responding to Re-Steals From Other Positions": "다른 포지션의 리스틸(Re-steal)에 대한 대응",
    "SB Facing BTN Open": "SB 포지션의 버튼(BTN) 오픈 대응",
    "BB Facing BTN Open": "BB 포지션의 버튼(BTN) 오픈 대응",
    "STR Facing BTN Open": "스트래들(STR) 포지션의 버튼(BTN) 오픈 대응",
    "Donk Betting": "동크 벳(Donk Bet) 전략",
    "Responding to Donk Bets": "동크 벳에 대한 올바른 대응법",
    "Flop Example": "플랍 실전 핸드 예시",
    "Turn Example": "턴 실전 핸드 예시",
    "River Example": "리버 실전 핸드 예시",
    "A Dynamic Flop": "다이내믹(웻) 플랍에서의 전략",
    "A Static Flop": "스태틱(드라이) 플랍에서의 전략",
    "A Turn Example": "턴 액션 실전 예시",
    "Study the Games You Actually Play": "실제 플레이하는 게임 포맷 집중 분석",
    "Hand Upload Integration": "핸드 히스토리 업로드 및 연동 가이드",
    "Roadmap & Current Limitations": "개발 로드맵 및 현재의 한계점",
    "Keeping the Game Fair": "게임 공정성과 무결성 유지 정책",
    "Why Late-Stage Decisions Matter": "토너먼트 후반부 의사결정이 중요한 이유",
    "Why Fold EV Isn't Always Zero": "폴드 EV가 항상 0이 아닌 이유",
    "Bubble Factors": "버블 팩터(Bubble Factor) 계산과 적용",
    "Range Advantage": "레인지 어드밴티지(Range Advantage) 분석",
    "Nut Advantage": "너트 어드밴티지(Nut Advantage) 분석",
    "Cheat Sheet": "실전 요약 치트시트",
    "The Experiment": "실전 실험 및 데이터 분석",
    "Methodology": "연구 방법론 및 솔버 세팅",
    "Practice": "실전 연습 및 트레이닝",
    "The Hand": "실전 핸드 히스토리 분석",
    "New Solutions": "신규 솔루션 업데이트",
    "New Features": "신규 기능 안내",
    "Improvements": "성능 개선 및 업데이트",
    "Bug Fixes": "오류 수정 사항",
    "What's Next?": "향후 로드맵 및 다음 단계",
    "What's Next": "향후 로드맵 및 다음 단계",
    "Looking Ahead": "향후 전망 및 발전 방향",
    "Key Takeaways": "핵심 핵심 요점 정리",
    "Final Thoughts": "최종 결론 및 실전 팁",
    "Shallower Stacks": "숏스택 상황에서의 전략",
    "Deeper Stacks": "딥스택 상황에서의 전략",
    "Asymmetric Stacks": "비대칭 스택 상황 분석",
    "Medium Stacks": "미들스택 상황에서의 전략",
    "Shallow Stacks": "숏스택 상황에서의 전략",
    "FAQ": "자주 묻는 질문 (FAQ)",
    "Quiz": "핵심 확인 퀴즈",
    "What To Take Away": "핵심 요약 및 정리",
    "How It Works": "작동 원리 및 수학적 배경",
    "GTO Wizard AI": "GTO Wizard AI 솔루션",
    "River Benchmarks": "리버 벤치마크 지표",
    "Turn Benchmarks": "턴 벤치마크 지표",
    "Flop Benchmarks": "플랍 벤치마크 지표",
    "Bluffing": "블러핑 전략과 빈도",
    "Hypotheses": "가설 설정 및 검증",
    "First Hypothesis": "첫 번째 가설 검증",
    "Second Hypothesis": "두 번째 가설 검증",
    "Third Hypothesis": "세 번째 가설 검증",
    "Turn Reports": "턴 솔버 리포트 분석",
    "Low Disconnected": "로우 디스커넥티드(Low Disconnected) 보드 분석",
    "Pricing": "요금제 안내",
    "Limitations": "한계점 및 주의사항",
    "Exploitability": "익스플로잇 가능성(Exploitability) 분석",
    "Straight-Completing Turns": "스트레이트 완성 턴 카드 분석",
    "Small C-Bet Boards": "스몰 C-bet 추천 보드",
    "Medium C-bet Boards": "미디엄 C-bet 추천 보드",
    "Large C-bet Boards": "라지 C-bet 추천 보드",
    "General Gameplan After C-Bet Gets Called": "C-bet 콜 직면 후 기본 게임 플랜",
    "The Theory of Limping": "림프(Limp)의 수학적 이론",
    "Limping From the SB": "스몰 블라인드(SB) 림프 전략",
    "Limping From the BB": "빅 블라인드(BB) 림프 전략",
    "Limping From Other Positions": "기타 포지션 림프 분석",
    "Responding to SB Limps": "SB 림프에 대한 대응 전략",
    "Responding to BB Limps": "BB 림프에 대한 대응 전략",
    "B-X-B Refresher (Equity Advantages)": "벳-첵-벳(B-X-B) 라인과 에퀴티 우위",
    "What Makes This Spot Unique?": "이 스팟이 특별한 전략적 이유",
    "Check-Calling (XC) on Low Boards": "로우 보드에서의 체크-콜(XC) 전략",
    "Constructing OOP's River Checking Range": "OOP의 리버 체크 레인지 구성법",
    "Exercise for the Reader": "실전 독자 연습 과제",
    "Constructing OOP's River Betting Range": "OOP의 리버 베팅 레인지 구성법",
    "Study Question": "핵심 스터디 문제",
    "Min or Jam?": "민 레이즈 vs 올인 쨈(Jam) 비교",
    "A Nit and a Maniac Sit at a Table": "니트(Nit)와 매니악이 테이블에 앉았을 때",
    "Hero vs. Nitty Villain": "히어로 vs 니트(Nit) 성향 빌런",
    "Hero vs. Calling Stationey Villain": "히어로 vs 콜링 스테이션 빌런",
    "Hero vs. Maniacal Villain": "히어로 vs 매니악 성향 빌런",
    "When Villain Has no Bluffs": "빌런의 레인지에 블러프가 전혀 없을 때",
    "Start With a Hypothesis": "가설 수립 및 분석 착수",
    "A Dead End": "흔히 빠지는 이론적 함정(Dead End)",
    "Same Cards, Different Order": "동일한 카드, 다른 런아웃(Runout) 비교",
    "Big Blind Responses": "빅 블라인드(BB)의 최적 대응 전략",
    "Flop Subset Results and Observations": "플랍 서브셋 결과 및 솔버 관찰",
    "Comparison With Heads-Up Strategy": "헤즈업 전략과의 차이점 비교",
    "Key Differences": "핵심 차이점 분석",
    "MTT Solutions": "토너먼트(MTT) 솔버 솔루션",
    "Solutions": "솔버 솔루션 가이드",
    "Availability": "지원 범위 및 이용 가능 환경",
    "Tier Breakdown: What's Changing for You": "티어별 세부 변경 사항 안내",
    "Free": "무료 플랜 (Free)",
    "Starter": "스타터 플랜 (Starter)",
    "Premium": "프리미엄 플랜 (Premium)",
    "Elite": "엘리트 플랜 (Elite)",
    "Ultra": "울트라 플랜 (Ultra)",
    "Thank You": "감사의 말",
    "2026 Main Event Example": "2026 메인 이벤트 실전 예시",
    "Ultra Early Bird Available Until October 15": "10월 15일까지 울트라 얼리버드 진행",
    "Insider Program": "인사이더 프로그램 안내",
    "GTO Wizard AI Upgrades": "GTO Wizard AI 업그레이드 안내",
    "PokerStars": "포커스타즈 (PokerStars)",
    "GG Poker": "GG 포커 (GG Poker)",
    "WPN (America's Card Room)": "WPN (ACR)",
    "iPoker": "아이포커 (iPoker)",
    "PPPoker": "PPPoker",
    "Unibet": "유니벳 (Unibet)",
    "PartyPoker": "파티포커 (PartyPoker)",
    "Ignition": "이그니션 (Ignition)",
    "Winamax": "위나맥스 (Winamax)",
    "PokerBros": "포커브로스 (PokerBros)",
    "Chico": "치코 (Chico)",
    "WePoker": "위포커 (WePoker)",
    "Built by Poker Players, for Poker Players": "포커 플레이어에 의해, 플레이어를 위해 설계된 플랫폼"
}

# 2. Suffix Cleaners (removes English tag artifacts from headings that already have Korean)
suffix_cleaners = [
    (r'\s*\(Overview\)\s*$', ''),
    (r'\s*\(Conclusion\)\s*$', ''),
    (r'\s*\(Summary\)\s*$', ''),
    (r'\s*\(Deeper Stacks\)\s*$', ''),
    (r'\s*\(Barreling the Turn\)\s*$', ''),
    (r'\s*\(Preflop Ranges\)\s*$', ''),
    (r'\s*\(Preflop ICM\)\s*$', ''),
    (r'\s*\(Postflop ICM\)\s*$', ''),
    (r'\s*\(Continuation Betting\)\s*$', ''),
    (r'\s*\(Preflop\)\s*$', '')
]

# 3. Regex Pattern Translators
regex_patterns = [
    (r'\bExample\s*(\d+)\s*:', r'실전 예시 \1:'),
    (r'\bExample\s*(\d+)\b', r'실전 예시 \1'),
    (r'\bExample\s*:\s*', r'실전 예시: '),
    (r'\bHypothesis\s*(\d+)\b', r'가설 \1'),
    (r'\bFacing\s+([A-Za-z0-9\-]+)\s+Open\b', r'\1 오픈 직면 시 대응 전략'),
    (r'\bFacing\s+([A-Za-z0-9\-]+)\b', r'\1 상대 시 대응 전략'),
    (r'\bResponding to\s+([A-Za-z0-9\-]+)\b', r'\1에 대한 대응 전략'),
    (r'\b([A-Za-z0-9\-]+)\s+Facing\s+([A-Za-z0-9\-]+)\b', r'\1 포지션의 \2 상대 전략'),
]

# 4. Poker Domain Post-processor (fixes machine translation inaccuracies)
poker_post_fixes = [
    (r'\b형평성\b', '에퀴티'),
    (r'\b자본\b', '에퀴티'),
    (r'\b접기\b', '폴드'),
    (r'\b접고\b', '폴드하고'),
    (r'\b접음\b', '폴드'),
    (r'\b폴드 EV\b', '폴드 EV'),
    (r'\b재훔치는 것\b', '리스틸(Re-steal)'),
    (r'\b재훔치기\b', '리스틸(Re-steal)'),
    (r'\b직위\b', '포지션'),
    (r'\b마법사\b', 'Wizard'),
    (r'\b동크 베팅\b', '동크 벳'),
    (r'\b동크베팅\b', '동크 벳'),
    (r'\bC-Bets\b', 'C-bet'),
    (r'\bC-베팅\b', 'C-bet'),
    (r'\b3-Bets\b', '3벳'),
    (r'\b3-베팅\b', '3벳'),
    (r'\b4-Bets\b', '4벳'),
    (r'\b4-베팅\b', '4벳'),
    (r'\b수표\b', '체크'),
    (r'\b수표-호출\b', '체크-콜'),
    (r'\b체크-호출\b', '체크-콜'),
    (r'\b냄비 확률\b', '팟 오즈(Pot Odds)'),
    (r'\b팟 기회\b', '팟 오즈(Pot Odds)'),
    (r'\b냄비 배당률\b', '팟 오즈(Pot Odds)'),
    (r'\b범위\b', '레인지'),
    (r'\b블록 베팅\b', '블락-벳'),
    (r'\b블록베팅\b', '블락-벳'),
    (r'\b블록 벳\b', '블락-벳'),
    (r'\b오버베팅\b', '오버벳'),
    (r'\b오버 베팅\b', '오버벳'),
    (r'\b민 레이즈\b', '민레이즈'),
    (r'\b기대치\b', '기대값(EV)'),
    (r'\b직면하다\b', '상대하기'),
    (r'\b직면한\b', '상대하는'),
]

def clean_translated_text(text):
    for pattern, repl in poker_post_fixes:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text.strip()

def translate_batch_google(lines):
    if not lines:
        return []
    q = '\n'.join(lines)
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                trans_text = ''.join([part[0] for part in res[0] if part[0]])
                out_lines = [l.strip() for l in trans_text.split('\n')]
                if len(out_lines) == len(lines):
                    return [clean_translated_text(l) for l in out_lines]
                # If line count doesn't match perfectly, handle gracefully
                res_lines = []
                for orig in lines:
                    res_lines.append(clean_translated_text(out_lines.pop(0) if out_lines else orig))
                return res_lines
        except Exception as e:
            time.sleep(1)
    # Fallback to original if network fails
    return lines

print("Loading articles.json...")
with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Collect all unique headings needing translation
headings_to_translate = set()

for a in articles:
    html = a.get('content_html', '')
    if not html:
        continue
    h_tags = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html)
    for h in h_tags:
        clean = h.strip()
        num_prefix = ""
        m = re.match(r'^(\d+\.\s*)(.*)$', clean)
        if m:
            core = m.group(2).strip()
        else:
            core = clean
        
        # Check if already in exact map
        if core in heading_exact_map:
            continue
        
        # Check if contains Korean
        if re.search(r'[\uac00-\ud7a3]', core):
            continue
            
        # If pure English or needs translation
        if re.search(r'[a-zA-Z]{2,}', core):
            headings_to_translate.add(core)

print(f"Total unique headings needing automated translation: {len(headings_to_translate)}")

# Batch translate in chunks of 25
unique_list = list(headings_to_translate)
auto_translations = {}
batch_size = 25

for i in range(0, len(unique_list), batch_size):
    chunk = unique_list[i:i+batch_size]
    print(f"Translating batch {i//batch_size + 1}/{(len(unique_list) + batch_size - 1)//batch_size} ({len(chunk)} items)...")
    translated_chunk = translate_batch_google(chunk)
    for orig, tr in zip(chunk, translated_chunk):
        auto_translations[orig] = tr
    time.sleep(0.3)

print("Batch translation complete! Now updating all articles...")

total_headings_replaced = 0

def replace_heading_tag(match):
    global total_headings_replaced
    tag = match.group(1)
    attrs = match.group(2)
    inner = match.group(3).strip()

    num_prefix = ""
    m = re.match(r'^(\d+\.\s*)(.*)$', inner)
    if m:
        num_prefix = m.group(1)
        core = m.group(2).strip()
    else:
        core = inner

    # 1. Clean trailing english suffixes like (Overview), (Conclusion)
    cleaned_suffix = False
    for pat, repl in suffix_cleaners:
        new_core = re.sub(pat, repl, core)
        if new_core != core:
            core = new_core.strip()
            cleaned_suffix = True

    # 2. Check exact map
    new_core = None
    if core in heading_exact_map:
        new_core = heading_exact_map[core]
    elif core.lower() in [k.lower() for k in heading_exact_map]:
        for k, v in heading_exact_map.items():
            if k.lower() == core.lower():
                new_core = v
                break

    # 3. Check regex patterns
    if not new_core:
        temp = core
        for pat, repl in regex_patterns:
            temp = re.sub(pat, repl, temp, flags=re.IGNORECASE)
        if temp != core:
            new_core = temp

    # 4. Check automated translations
    if not new_core and core in auto_translations:
        new_core = auto_translations[core]

    if new_core:
        total_headings_replaced += 1
        return f"<{tag}{attrs}>{num_prefix}{new_core}</{tag}>"
    elif cleaned_suffix:
        total_headings_replaced += 1
        return f"<{tag}{attrs}>{num_prefix}{core}</{tag}>"
    else:
        return match.group(0)

for a in articles:
    html = a.get('content_html', '')
    if html:
        new_html = re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', replace_heading_tag, html, flags=re.DOTALL)
        a['content_html'] = new_html

with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"DONE! Replaced/Koreanized {total_headings_replaced} headings across all {len(articles)} articles in {ARTICLES_FILE}!")
