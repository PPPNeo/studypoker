import sys, os, json, re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'data', 'articles.json')

# 1. Exact Heading Map for poorly translated headings
exact_heading_replacements = {
    # River ("강")
    "배럴링 강": "리버 배럴링 전략",
    "직선으로 완성되는 강": "스트레이트 완성 리버 런아웃",
    "강의 예": "리버 실전 핸드 예시",
    "사례 연구 #3: 4직선 강에 동크재밍": "사례 연구 #3: 4-스트레이트 리버에서의 동크 올인 쨈(Jam)",
    "Kevin Rabichow – 강의 평형을 더욱 중요하게 생각하세요": "Kevin Rabichow - 리버 내쉬 균형(Equilibrium)의 중요성",
    "강 해결 시간": "리버 솔버 계산 시간",
    "다른 강의 예": "또 다른 리버 실전 핸드 예시",
    "건조한 벽돌 강": "드라이한 블랭크(Brick) 리버 런아웃",
    "더 깊은 강": "딥스택 리버 전략",
    "습하고 견과류가 변하는 강": "웻하고 너츠가 바뀌는 리버 런아웃",
    "하나의 중요한 강 이용": "핵심 리버 익스플로잇 전략",
    "강 비교": "리버 전략 비교",
    "강 탐사선": "리버 프로브 벳(Probe Bet) 전략",
    "가치 베팅 강": "리버 밸류 벳(Value Bet) 전략",
    "지분 분배를 변화시키는 강": "에퀴티 분포를 변화시키는 리버 런아웃",
    "다이나믹한 강 연주하기": "다이내믹한 리버 보드 플레이",
    "강 놀이": "리버 스트리트 플레이",
    "최적의 강 크기는 얼마입니까?": "최적의 리버 벳 사이징은 얼마인가?",
    "강 실험: J̈T̈7̈ 7♥ 2♥": "리버 솔버 시뮬레이션: J-T-7-7-2",
    "가치 있는 베팅을 하려면 핸드가 얼마나 강해야 합니까?": "밸류 벳(Value Bet)을 하려면 핸드가 얼마나 강해야 할까?",
    "너무 병합됨/드로우가 심함(블러프가 너무 강함)": "과도하게 머지된(Merged) 레인지 / 과도한 블러프 비율",

    # Hand ("손")
    "손마다 다른 ISO 크기를 사용하는 이유": "핸드별로 다른 아이솔레이션(ISO) 사이징을 사용하는 이유",
    "새롭게 디자인된 분석된 손 테이블": "새롭게 디자인된 핸드 분석 테이블",
    "테이블 마법사를 사용하여 자동으로 손 업로드": "테이블 위저드를 통한 핸드 자동 업로드",
    "(손) 매트릭스를 통해 보기": "핸드 매트릭스(Hand Matrix)로 분석하기",
    "손 예시 소개": "실전 핸드 예시 소개",
    "분석기 개선 사항: 더 깊은 손 분석을 위한 강력한 새 도구": "핸드 분석기 업데이트: 심층 핸드 분석 도구",
    "손 바깥쪽에 있는 스택으로는 정확하지 않음": "스택 깊이에 따른 오차 보정 가이드",
    "트레이너 및 손 기록 분석기": "트레이너 및 핸드 히스토리 분석기",
    "어떤 손을 확인합니까?": "어떤 핸드로 체크해야 할까?",
    "손 기록 분석기 업그레이드": "핸드 히스토리 분석기 업그레이드 안내",
    "손 분석": "핸드 심층 분석",
    "어느 손에 베팅해야 할까요?": "어떤 핸드로 베팅해야 할까?",
    "짧은 손 플레이": "숏핸디드(Short-handed) 플레이 전략",
    "손 업로드 방법": "핸드 히스토리 업로드 방법",
    "한 손 업로드": "단일 핸드 히스토리 업로드",
    "손을 올렸는데 이제 어떻게 해야 할까요?": "핸드를 업로드한 후 분석 진행 방법",
    "손을 올렸는데 이제 어떡하지?": "핸드를 업로드한 후 분석 진행 방법",
    "손 분석을 진행하세요": "핸드 히스토리 분석 진행",
    "손 분석을 진행하세요.": "핸드 히스토리 분석 진행",
    "몇 개의 손을 업로드할 수 있나요?": "업로드 가능한 핸드 수 안내",
    "손은 몇 개나 업로드할 수 있나요?": "업로드 가능한 핸드 수 안내",
    "HUD에서 손 기록을 어떻게 내보내나요?": "포커 HUD에서 핸드 히스토리 내보내는 법",
    "손 2 노트": "핸드 2 실전 분석 노트",
    "어느 손을 접습니까?": "어떤 핸드를 폴드해야 할까?",
    "어느 손을 들까?": "어떤 핸드로 레이즈할까?",
    "손 읽기는 지속적인 과정입니다": "핸드 리딩(Hand Reading)은 연속적인 추론 과정이다",
    "사례 2) 일부 손만 찹": "사례 2) 특정 핸드만 찹(Chop/팟 분배)되는 경우",
    "손의 예": "실전 핸드 예시",
    "손 매트릭스": "핸드 매트릭스(Hand Matrix)",
    "스타 손": "즐겨찾기(별표) 핸드 관리",
    "손 삭제": "핸드 히스토리 삭제",
    "손 기록 도구 모음": "핸드 히스토리 툴바 안내",
    "손으로 스크롤": "핸드 목록 스크롤 탐색",
    "손을 업로드하는 방법": "핸드 히스토리 업로드 방법",
    "손이 아닌 공부 레인지!": "개별 핸드가 아닌 '레인지' 전체를 공부하라!",
    "3) 중요한 것은 손이 아니라 전체 범위를 어떻게 플레이하느냐에 관한 것입니다.": "3) 단일 핸드가 아닌 전체 레인지를 운영하는 법",
    "6) 대부분의 EV는 미친 손에서 나옵니다.": "6) 대부분의 EV는 몬스터 핸드(Monster Hand)에서 발생한다",
    "손 기록 분석기": "핸드 히스토리 분석기",
    "손 기록 분석기에 대한 우리의 계획은 무엇입니까?": "핸드 히스토리 분석기 향후 개발 계획",

    # Bluff ("허세" / "허풍")
    "(1) 허세": "(1) 블러프(Bluff)",
    "누군가가 부자연스러운 허세를 놓치면 어떻게 되나요?": "상대가 언내추럴 블러프를 놓쳤을 때의 대처",
    "나는 내 범위의 맨 아래에 있습니다. 이것은 필수 허세입니다.": "레인지 최하단 핸드의 필수 블러프 스팟",
    "2) 허세 불균형": "2) 블러프 불균형(Bluff Imbalance)",
    "1) 강력한 범위로의 허세": "1) 강력한 레인지 기반의 블러프",
    "페어로 계속 허세를 부리는 경우": "페어 핸드로 블러프 배럴을 이어가는 경우",
    "쌍으로 허풍을 멈추는 경우": "페어 핸드로 블러핑을 멈춰야 하는 경우",
    "쌍으로 허세를 부리는 경우": "페어 핸드로 블러프를 시도하는 경우",
    "페어로 허세를 부리지 말아야 할 때": "페어 핸드로 블러프를 피해야 하는 기준",
    "허세란 무엇인가?": "블러프(Bluff)의 본질과 수학",
    "AKQ 게임에서의 허세": "토이 게임(AKQ Game)에서의 블러프 수학",
    "허세 바우처": "블러프 캐쳐(Bluff Catcher) 운용법",
    "허세 찾기": "최적의 블러프 핸드 발굴하기",
    "허세 빈도": "최적 블러프 빈도(Bluff Frequency)",
    "허세를 잡아야 할까요?": "블러프 캐치(Bluff Catch)를 해야 할까?",

    # Pair ("쌍")
    "낮은 쌍": "로우 포켓페어(Low Pairs)",
    "작은 포켓 쌍": "스몰 포켓페어(Small Pocket Pairs)",
    "하지만 어느 쌍일까요?": "어떤 페어 핸드를 선택해야 할까?",
    "지배적인 쌍": "도미네이션(우세) 페어 핸드",
    "한 쌍 만들기": "페어 완성 시의 전략 가이드",

    # Draw ("무승부")
    "모든 무승부가 동일하게 생성되는 것은 아닙니다": "모든 드로우(Draw)가 동일한 가치를 갖는 것은 아니다",
    "무승부를 이용한 BTN 전략": "드로우(Draw)를 활용한 BTN 포지션 전략",
    "무승부가 없는 BTN 전략": "드로우가 없는 핸드의 BTN 포지션 전략",

    # Pot / Flop / Equity / Villain / Hero
    "EV(/냄비)": "EV (/팟 기준)",
    "삼방향 림프 냄비": "3웨이 림프 팟(3-way Limped Pot)",
    "냄비 열기": "오픈 레이즈(Open Raise) 전략",
    "냄비 기하학이란 무엇입니까?": "팟 지오메트리(Pot Geometry)의 수학적 원리",
    "1단계) 악당의 레인지 자르기": "1단계) 빌런(Villain)의 레인지 압축하기",
    "우리의 악당": "우리의 상대: 빌런(Villain)",
    "악당의 방어 범위를 최대화하세요": "빌런의 방어 레인지를 최대로 압박하라",
    "악당의 반응을 살펴보세요": "빌런의 액션 반응 분석하기",
    "영웅 카드": "히어로(Hero)의 핸드 카드",
    "2단계) 영웅의 부풀려진 자산 풍선 수축": "2단계) 히어로의 과대평가된 에퀴티 재조정",
    "영웅 카드가 없습니다": "히어로에게 적합한 카드가 없는 경우",
    "지배는 형평성을 평가하는 데 도움이 됩니다": "도미네이션과 에퀴티(Equity) 평가",
    "블러프가 콜에 대한 형평성을 유지할 때": "블러프 핸드가 콜을 상대로 에퀴티를 유지할 때",
    "\"물고기\" 프로필 활용": "\"피쉬(Fish)\" 성향 유저 익스플로잇",
    "PKO의 거품 요인": "PKO 버블 팩터(Bubble Factor)",
    "두 가지 수표에 대한 보상": "첵-첵(Check-Check) 라인의 기대 가치",
    "블록 베팅은 기본적으로 수표입니다… 아니면 그럴까요?": "블락벳(Block Bet)은 기본적으로 체크와 같을까?",
    "병합 내기": "머지드 벳(Merged Bet) 전략",
    "밀어내기 레인지": "올인 푸시(Push/Shove) 레인지",
    "모든 접기가 동일하게 생성되는 것은 아닙니다": "모든 폴드(Fold)가 다 같은 가치를 갖는 것은 아니다",
    "접는 것은 +EV입니다": "폴드(Fold)가 +EV인 상황 분석",
    "이러한 통화를 수익성 있게 만들려면 어떻게 해야 합니까?": "이러한 콜(Call)을 +EV로 만드는 조건",
    "이전 직위에 적응하기": "얼리 포지션(EP)에 적응하기",
    "1단계) 지배적인 전략을 제거하는 것부터 시작하세요": "1단계) 도미네이트된 열세 전략 제거하기",
    "스핀의 강력한 슈트!": "스핀앤고(Spin & Go)의 강력한 무기!",
    "체스가 순위를 매겼습니다. 다음은 포커입니다.": "체스의 레이팅 시스템, 포커에 적용하기",

    # Odds & Equity
    "팟 배당률 계산하기": "팟 오즈(Pot Odds) 계산하기",
    "필요한 자기자본 계산하기": "필요한 에퀴티(Required Equity) 계산법",
    "팟 배당률 계산기": "팟 오즈(Pot Odds) 계산기 활용",
    "향후 베팅이 가능할 때의 팟 배당률": "추가 스트리트 베팅이 남았을 때의 팟 오즈",
    "팟 배당률 제한 예시": "팟 오즈의 한계 실전 예시",
    "팟 배당률과 기대값": "팟 오즈와 기대값(EV)의 관계",
    "체이싱 및 임플라이드 확률": "드로우 체이싱과 임플라이드 오즈",
    "내재 확률이란 무엇입니까?": "임플라이드 오즈(Implied Odds)란 무엇인가?",
    "직접 확률과 묵시 확률": "다이렉트 팟 오즈 vs 임플라이드 오즈",
    "직접 팟 배당률 계산": "다이렉트 팟 오즈(Pot Odds) 계산법",
    "내재 확률 계산": "임플라이드 오즈(Implied Odds) 계산법",
    "역임시 배당률": "리버스 임플라이드 오즈(Reverse Implied Odds)",
    "내재 배당률과 스택 깊이의 관계": "임플라이드 오즈와 스택 깊이(Stack Depth)의 관계",
    "다중자본 보유를 통한 내재 승률 시각화": "멀티웨이 팟에서의 에퀴티 시각화",
    "플레이어의 토너먼트 자산은 무엇입니까?": "플레이어의 토너먼트 에퀴티(ICM Value)",
    "자산을 사용하지 않는 방법": "에퀴티를 잘못 해석하는 흔한 오류",
    "자기자본 지표": "에퀴티(Equity) 핵심 지표",
    "자기자본과 기대가치": "에퀴티(Equity)와 기대값(EV)",
    "과도하게 실현된 자기자본": "초과 실현된 에퀴티(Over-realized Equity)",
    "실현되지 않은 자기자본": "미실현 에퀴티(Unrealized Equity)",
    "자산 우위를 활용한 레인지 베팅": "에퀴티 우위를 활용한 레인지 베팅",
    "ICM 및 바운티 자산 하락": "ICM 및 바운티 에퀴티 변동",
    "Valor는 자산/EV/EQR과 어떤 관련이 있나요?": "핸드 밸류는 에퀴티/EV/EQR과 어떤 관련이 있는가?",

    # Flop / Wizard
    "순위 플롭 유형": "하이 카드 및 페어 플랍 유형",
    "기타 플롭": "기타 특수 플랍 유형",
    "낮은 연결 플롭": "로우 커넥티드 플랍(Low Connected Flop)",
    "미디엄 커넥티드 플롭": "미디엄 커넥티드 플랍(Medium Connected Flop)",
    "브로드웨이 플롭": "브로드웨이 플랍(Broadway Flop)",
    "레벨 2: 플롭 기초 구축": "레벨 2: 플랍 기초 전략 구축",
    "에이스 하이 플롭": "A-하이 플랍(Ace-High Flop)",
    "'액션' 플롭": "액션이 많이 발생하는 플랍 텍스처",
    "가장 큰 변화를 보이는 플롭 유형은 무엇입니까?": "전략 변화가 가장 큰 플랍 텍스처 유형",
    "종합 플롭 전략: 50bb": "50bb 스택 플랍 종합 전략",
    "플롭 콜링 스테이션과 비교": "플랍 콜링 스테이션 상대 전략 비교",
    "빅뱅플롭 이전에도 돌아가": "프리플랍과 플랍의 연계성",
    "플롭 악용 가능성:": "플랍 익스플로잇 가능성 분석:",
    "플롭 전략": "플랍 기본 전략",
    "정적 플롭": "스태틱(드라이) 플랍 분석",
    "동적 플롭": "다이내믹(웻) 플랍 분석",
    "BTN의 불량 플롭 조사": "버튼(BTN)에게 불리한 플랍 보드 분석",
    "BTN의 더 나은 플롭 조사": "버튼(BTN)에게 유리한 플랍 보드 분석",
    "로우, 커넥티드 플롭": "로우 커넥티드 플랍 분석",
    "낮은 드라이 플롭": "로우 드라이 플랍 분석",
    "샘플 플롭": "실전 플랍 예시",
    "페어플롭": "페어 보드 플랍(Paired Flop)",
    "플롭 플레이": "플랍 스트리트 플레이",
    "플롭 텍스처": "플랍 텍스처(Texture) 분류",
    "플롭 비교": "플랍 전략 비교",
    "작은 플롭 베팅에 대한 보상": "플랍 스몰 벳(Small Bet)의 기대 수익",
    "플롭 체크에 대한 보상": "플랍 체크 라인의 가치",
    "플롭 플레이의 영향": "플랍 전략이 전체 핸드에 미치는 영향",
    "드라이 플롭": "드라이 플랍(Dry Flop)",
    "젖은 플롭": "웻 플랍(Wet Flop)",
    "슈퍼 웨트 플롭": "슈퍼 웻 플랍(Super Wet Flop)",
    "C-Bet에 어떤 플롭이 사용됩니까?": "어떤 플랍 텍스처에서 C-bet을 구사할까?",
    "최악의 악몽 플롭": "가장 까다로운 악몽의 플랍 텍스처",
    "다이나믹 플롭": "다이내믹 플랍(Dynamic Flop)",
    "에이스하이플롭": "A-하이 플랍(Ace-High Flop)",
    "플롭 예제": "플랍 실전 핸드 예시",
    "에이스하이 C-Bet 플롭": "A-하이 플랍 C-bet 전략",
    "낮은 C-Bet 플롭": "로우 보드 C-bet 전략",
    "첫 번째 플롭 결정: 베팅 또는 체크?": "플랍 첫 번째 결정: 벳 vs 체크",
    "집계된 플롭 보고서": "플랍 집계 솔버 리포트",
    "블랭크 플롭": "블랭크 플랍(Blank Flop)",
    "중간 조정 플롭": "미디엄 커넥티드 플랍(Medium Connected Flop)",
    "정적 플롭 플레이": "스태틱 플랍 플레이",
    "모노톤 플롭의 전략적 원칙": "모노톤 플랍(Monotone Flop) 전략 원칙",
    "정적 플롭에서 투기꾼과 대결하기": "스태틱 플랍에서 어그레시브 빌런 상대법",
    "다이내믹한 플롭에서 투기꾼과 대결하기": "다이내믹 플랍에서 어그레시브 빌런 상대법",
    "로우 카드 플롭 플레이": "로우 카드 플랍 플레이",
    "에이스 하이 플롭 플레이하기": "A-하이 플랍 플레이 전략",
    "SB의 플롭 베팅은 얼마나 커야 할까요?": "SB의 플랍 벳 사이징 가이드",
    "SB는 어떤 플롭에 베팅해야 할까요?": "SB는 어떤 플랍 텍스처에 베팅해야 할까?",
    "유리한 플롭": "유리한 플랍 보드",
    "덜 유리한 플롭": "불리한 플랍 보드",
    "그룹화 플롭": "플랍 텍스처 그룹화 분석",
    "플롭 페어링": "플랍 페어 여부에 따른 조정",
    "플롭 연결성": "플랍 커넥티비티(Connectivity) 분석",
    "플롭 적합성": "플랍 수티드(무늬 연계성) 분석",
    "플롭 분석": "플랍 심층 분석",
    "플롭 베팅 비교에 대한 응답": "플랍 벳 직면 시 대응 전략 비교",
    "5) 견과류의 잠재력은 왕이다": "5) 너츠 잠재력(Nut Potential)의 절대적 가치",
    "6) 더 높은 내재(및 역내재) 배당률": "6) 높은 임플라이드(및 리버스 임플라이드) 오즈",
    "턴 플레이와 플롭 플레이의 차이점": "플랍과 턴 스트리트의 핵심 전략 차이점",
    "플롭 분석: A♥2♥2︎": "플랍 심층 분석: A♥2♥2︎",
    "지금 테이블 마법사를 시작해보세요": "지금 테이블 위저드를 시작해보세요",
    "GTO 마법사를 통한 통합 코칭": "GTO Wizard를 통한 통합 코칭",
    "GTO 마법사가 되기 위한 게임 계획": "GTO 마스터가 되기 위한 게임 플랜",
    "GTO 마법사에서 하위 집합을 어떻게 사용할 수 있습니까?": "GTO Wizard에서 서브셋(Subset)을 활용하는 법"
}

# 2. General Text Replacements across all html and cards
text_replacements = [
    # Flop
    (r'\b플롭\b', '플랍'),
    (r'플롭(?=[가-힣])', '플랍'),
    (r'(?<=[가-힣])플롭', '플랍'),

    # River / Showdown
    (r'\b쇼다운 가치\b', '쇼다운 밸류'),
    (r'\b쇼다운 가치는\b', '쇼다운 밸류는'),
    (r'\b최종 결전지\b', '최종 쇼다운 지점'),
    (r'\b결전지\b', '쇼다운 지점'),

    # Betting & Odds
    (r'\b가치 베팅\b', '밸류 벳'),
    (r'\b블록 베팅\b', '블락벳'),
    (r'\b팟 배당률\b', '팟 오즈'),
    (r'\b내재 배당률\b', '임플라이드 오즈'),
    (r'\b역내재 배당률\b', '리버스 임플라이드 오즈'),
    (r'\b역임시 배당률\b', '리버스 임플라이드 오즈'),
    (r'\b냄비 배당률\b', '팟 오즈'),
    (r'\b팟 기회\b', '팟 오즈'),

    # Board textures
    (r'\b단색 보드\b', '모노톤 보드'),
    (r'\b무지개 보드\b', '레인보우 보드'),
    (r'\b투 톤 보드\b', '투톤 보드'),
    (r'\b두 톤 보드\b', '투톤 보드'),

    # Equity / Tournament
    (r'\b자기자본\b', '에퀴티'),
    (r'\b거품 요인\b', '버블 팩터'),
    (r'\b부풀려진 자산 풍선 수축\b', '과대평가된 에퀴티 재조정'),
    (r'\b손 기록\b', '핸드 히스토리'),

    # General Holdem terms
    (r'\b악당의\b', '빌런의'),
    (r'\b악당\b', '빌런'),
    (r'\b영웅의\b', '히어로의'),
    (r'\b영웅\b', '히어로'),
    (r'\b견과류\b', '너츠'),
    (r'\b물고기\b', '피쉬'),
    (r'\b냄비\b', '팟'),
    (r'\b수표\b', '체크'),
    (r'\b허세\b', '블러프'),
    (r'\b허풍\b', '블러핑'),
]

print("Loading articles.json...")
with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
    articles = json.load(f)

def clean_heading(raw_h):
    clean = raw_h.strip()
    m = re.match(r'^(\d+\.\s*)(.*)$', clean)
    if m:
        num_prefix = m.group(1)
        core = m.group(2).strip()
    else:
        num_prefix = ""
        core = clean

    if core in exact_heading_replacements:
        return num_prefix + exact_heading_replacements[core]

    # Partial replacement check
    temp = core
    for k, v in exact_heading_replacements.items():
        if k in temp:
            temp = temp.replace(k, v)
    if temp != core:
        return num_prefix + temp

    # General replacements
    for pat, repl in text_replacements:
        temp = re.sub(pat, repl, temp)
    return num_prefix + temp

heading_change_count = 0
card_change_count = 0
body_change_count = 0

for a in articles:
    title_ko = a.get('title_ko', '')
    title_en = a.get('title_en', '')
    html = a.get('content_html', '')

    # 1. Update summary cards (replace title_en in card text with title_ko)
    cards = a.get('summary_cards', [])
    for card in cards:
        text = card.get('text', '')
        if title_en and title_en in text:
            card['text'] = text.replace(f"{title_en}에 대한", f"{title_ko}에 대한")
            card_change_count += 1
        for pat, repl in text_replacements:
            card['text'] = re.sub(pat, repl, card.get('text', ''))

    # 2. Update <h2> and <h3> in content_html
    def repl_h(m):
        global heading_change_count
        tag = m.group(1)
        attrs = m.group(2)
        inner = m.group(3).strip()
        new_inner = clean_heading(inner)
        if new_inner != inner:
            heading_change_count += 1
        return f"<{tag}{attrs}>{new_inner}</{tag}>"

    new_html = re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', repl_h, html, flags=re.DOTALL)

    # 3. Update chart captions in content_html
    def repl_chart_caption(m):
        prefix = m.group(1)
        caption_text = m.group(2).strip()
        suffix = m.group(3)
        new_caption = clean_heading(caption_text)
        return f"{prefix}{new_caption}{suffix}"

    new_html = re.sub(
        r'(📊\s*)(.*?)(\s*-\s*GTO Wizard 솔버 시뮬레이션)',
        repl_chart_caption,
        new_html
    )

    # 4. Update general body text
    for pat, repl in text_replacements:
        new_html = re.sub(pat, repl, new_html)

    if new_html != html:
        body_change_count += 1
        a['content_html'] = new_html

with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"DONE! Refined holdem terms across all articles:")
print(f"  Headings updated: {heading_change_count}")
print(f"  Summary cards updated: {card_change_count}")
print(f"  Articles with body text updated: {body_change_count}")
