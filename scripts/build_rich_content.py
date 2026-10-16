import json
import re

# Comprehensive dictionary for headings
HEADING_TRANSLATIONS = {
    "raise sizing": "오픈 및 레이즈 벳 사이징",
    "sizing": "최적 벳 사이징 분석",
    "preflop": "프리플랍 전략 및 레인지 구성",
    "postflop": "포스트플랍 운영 메커니즘",
    "the flop": "플랍(Flop) 텍스처 및 주도권 분석",
    "the turn": "턴(Turn) 배럴링 및 레인지 변화",
    "the river": "리버(River) 결정 및 밸류/블러프 배분",
    "deeper stacks": "딥스택(Deep Stack) 상황에서의 전략 조정",
    "short stacks": "숏스택(Short Stack) 상황에서의 전략 조정",
    "exploits": "실전 익스플로잇 및 상대 릭(Leak) 착취",
    "exploiting the leak": "상대의 릭(Leak) 공략법",
    "conclusion": "핵심 요약 및 실전 체크리스트",
    "summary": "핵심 전략 요약",
    "the incentive to steal": "스틸(Steal)의 수학적 유인과 가치",
    "continuation betting": "C-bet(컨티뉴에이션 벳) 빈도 및 사이징",
    "returning fire by 4-betting": "4벳으로 반격하기: 밸류와 블러프 핸드",
    "adapting to smaller raises": "작은 레이즈에 대처하는 익스플로잇 전략",
    "hand selection": "프리플랍 핸드 선택의 원칙",
    "equity realization": "에퀴티 실현(EQR)과 포지션의 힘",
    "risk premium": "리스크 프리미엄(Risk Premium)과 ICM",
    "bluff catching": "블러프 캐칭(Bluff Catching)의 기준과 MDF",
    "blockers": "블로커(Blockers) 효과와 콤보 계산",
    "multiway pots": "멀티웨이 팟의 특수성과 내쉬 균형",
    "c-betting oop": "아웃포지션(OOP)에서의 C-bet 전략",
    "c-betting ip": "인포지션(IP)에서의 C-bet 전략",
    "turn barreling": "턴 2nd 배럴 빈도와 카드 텍스처",
    "river overbets": "리버 오버벳(Overbet)의 수학과 레인지 폴라라이징",
    "check-raising": "체크-레이즈(Check-Raise) 레인지 설계",
    "protecting ranges": "체크 레인지 프로텍션의 중요성",
    "bounty considerations": "PKO 바운티 밸류 계산과 레인지 확대",
}

def translate_section_title(title):
    clean = re.sub(r'<[^>]+>', '', title).strip().replace("’", "'").replace("&nbsp;", " ")
    lower = clean.lower().rstrip(':')
    if lower in HEADING_TRANSLATIONS:
        return HEADING_TRANSLATIONS[lower]
    for k, v in HEADING_TRANSLATIONS.items():
        if k in lower:
            return f"{clean} ({v})"
    return clean

# Sentence translation helper for poker prose
def translate_poker_sentence(s):
    s = s.strip()
    if not s:
        return ""
    # Common poker phrases
    replacements = [
        (r'\bIn this article, we(?:’ll|\'ll| will) examine\b', '본 아티클에서는 심층적으로 분석합니다:'),
        (r'\bIn this article, we(?:’ll|\'ll| will) explore\b', '본 분석에서는 다음을 다룹니다:'),
        (r'\bIn this article, we(?:’ll|\'ll| will) look at\b', '본 글에서는 다음을 살펴봅니다:'),
        (r'\bGTO Wizard\b', 'GTO Wizard'),
        (r'\bNash equilibrium\b', '내쉬 균형(Nash Equilibrium)'),
        (r'\bexpected value\b', '기대값(EV)'),
        (r'\bequity realization\b', '에퀴티 실현(EQR)'),
        (r'\bminimum defense frequency\b', '최소 방어 빈도(MDF)'),
        (r'\bindependent chip model\b', '독립 칩 모델(ICM)'),
        (r'\bpot odds\b', '팟 오즈(Pot Odds)'),
        (r'\bimplied odds\b', '임플라이드 오즈(Implied Odds)'),
        (r'\bin position\b', '인포지션(IP)'),
        (r'\bout of position\b', '아웃포지션(OOP)'),
        (r'\bsingle raised pot\b', 'SRP(싱글 레이즈드 팟)'),
        (r'\bcontinuation bet\b', 'C-bet(컨티뉴에이션 벳)'),
        (r'\bcheck-raise\b', '체크-레이즈'),
        (r'\bcheck-call\b', '체크-콜'),
        (r'\boverbet\b', '오버벳'),
        (r'\bpolarize\b', '폴라라이즈'),
        (r'\bpolarized\b', '폴라라이즈드'),
        (r'\bcondensed\b', '컨덴스드'),
        (r'\blinear\b', '리니어'),
        (r'\bstack-to-pot ratio\b', 'SPR(스택 대 팟 비율)'),
    ]
    res = s
    for pat, rep in replacements:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res

if __name__ == '__main__':
    print("Helper compiled successfully")
