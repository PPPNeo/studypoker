"""
Deep article generator: Processes all 369 articles from raw_ghost_full.json
and generates in-depth, multi-section Korean study guides with embedded solver charts,
detailed breakdowns, specific takeaways, and original links.
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'raw_ghost_full.json'), encoding='utf-8') as f:
    posts = json.load(f)

# Load existing hand-crafted rich articles if any
with open(os.path.join(BASE_DIR, 'data', 'articles.json'), encoding='utf-8') as f:
    existing_articles = json.load(f)
existing_map = {a['slug']: a for a in existing_articles}

# Headings translation dictionary
HEADING_MAP = {
    'introduction': '개요 및 핵심 전략 배경',
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

def translate_heading(raw_h):
    h = clean_html(raw_h).replace("’", "'").strip()
    h_lower = h.lower().rstrip(':').rstrip('.')
    if h_lower in HEADING_MAP:
        return HEADING_MAP[h_lower]
    for k, v in HEADING_MAP.items():
        if k in h_lower:
            return f"{h} ({v})"
    return h

def extract_sections(html):
    normalized = re.sub(r'<h3[^>]*>', '<h2>', html)
    normalized = re.sub(r'</h3>', '</h2>', normalized)
    parts = re.split(r'<h2[^>]*>', normalized)
    sections = []
    
    # Intro
    intro_paras = [clean_html(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', parts[0], re.DOTALL) if clean_html(p)]
    intro_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', parts[0])
    if intro_paras:
        sections.append({
            'title': '개요 및 핵심 전략 배경',
            'paragraphs': intro_paras,
            'images': intro_imgs
        })
        
    for part in parts[1:]:
        m = re.match(r'^(.*?)</h2>(.*)', part, re.DOTALL)
        if not m:
            continue
        raw_h = m.group(1)
        body = m.group(2)
        paras = [clean_html(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL) if clean_html(p)]
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', body)
        if paras or imgs:
            sections.append({
                'title': translate_heading(raw_h),
                'paragraphs': paras,
                'images': imgs
            })
    return sections

print("Deep generator module ready")
