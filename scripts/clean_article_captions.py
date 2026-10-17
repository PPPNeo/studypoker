import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Detailed mapping of (article_id, img_filename) -> (caption_text, alt_text)
CAPTION_MAPPINGS = {
    # 1. single-size-solutions-are-live-new-pricing-50x-more-solutions
    ('single-size-solutions-are-live-new-pricing-50x-more-solutions', '5-1-1-scaled.png'): (
        '토너먼트 및 캐시게임 싱글 사이즈 솔루션 차트 비교',
        '토너먼트 및 캐시게임 싱글 사이즈 솔루션 차트 비교'
    ),
    
    # 2. should-you-ever-bluff-with-a-pair
    ('should-you-ever-bluff-with-a-pair', 'gto-wizard-bluffing-pairs-in-cash-games-image-5.png'): (
        '페어로 블러핑을 계속 이어가야 하는 상황 및 핸드 분석',
        '페어로 블러핑을 계속 이어가야 하는 상황 및 핸드 분석'
    ),
    ('should-you-ever-bluff-with-a-pair', 'gto-wizard-bluffing-pairs-in-cash-games-image-12.png'): (
        '페어로 블러핑을 멈추고 쇼다운 가치를 보존해야 하는 상황',
        '페어로 블러핑을 멈추고 쇼다운 가치를 보존해야 하는 상황'
    ),
    ('should-you-ever-bluff-with-a-pair', 'gto-wizard-bluffing-pairs-in-cash-games-image-14.png'): (
        '상대 성향에 따라 블러핑 빈도를 조절(익스플로잇)하는 전략',
        '상대 성향에 따라 블러핑 빈도를 조절(익스플로잇)하는 전략'
    ),

    # 3. bringing-it-all-together-pko-review
    ('bringing-it-all-together-pko-review', 'gto-wizard-how-does-icm-impact-pko-strategy-blog-thumbnail.jpg'): (
        'PKO(프로그레시브 녹아웃) 토너먼트 ICM 영향 및 바운티 전략 가이드',
        'PKO(프로그레시브 녹아웃) 토너먼트 ICM 영향 및 바운티 전략 가이드'
    ),

    # 4. when-to-ladder-in-tournaments
    ('when-to-ladder-in-tournaments', 'image-316.png'): (
        '마이크로 스택 존재 시 숏스택의 타이트한 푸시 레인지 (3.8% = TT+, AQs, AKo)',
        '마이크로 스택 존재 시 숏스택의 타이트한 푸시 레인지'
    ),
    ('when-to-ladder-in-tournaments', 'image-317.png'): (
        '래더링 압박 상황에서의 콜링 레인지 축소 분석',
        '래더링 압박 상황에서의 콜링 레인지 축소 분석'
    ),
    ('when-to-ladder-in-tournaments', 'image-318.png'): (
        '마이크로 스택 탈락 대기 시 미들스택의 위험 회피 전략',
        '마이크로 스택 탈락 대기 시 미들스택의 위험 회피 전략'
    ),
    ('when-to-ladder-in-tournaments', 'image-319.png'): (
        '페이점프 직전 스택 크기별 EV 보존 전략',
        '페이점프 직전 스택 크기별 EV 보존 전략'
    ),

    # 5. introducing-gto-wizard-ai
    ('introducing-gto-wizard-ai', 'image-23.png'): (
        '차세대 실시간 연산 GTO Wizard AI 인터페이스',
        '차세대 실시간 연산 GTO Wizard AI 인터페이스'
    ),
    ('introducing-gto-wizard-ai', 'image-24.png'): (
        '맞춤형 벳 사이징 및 커스텀 노드 실시간 솔빙 기능',
        '맞춤형 벳 사이징 및 커스텀 노드 실시간 솔빙 기능'
    ),
    ('introducing-gto-wizard-ai', 'image-25.png'): (
        '프리플랍부터 리버까지 즉각적인 솔루션 생성 엔진',
        '프리플랍부터 리버까지 즉각적인 솔루션 생성 엔진'
    ),
    ('introducing-gto-wizard-ai', 'roadmap.png'): (
        'GTO Wizard AI 개발 로드맵 및 향후 업데이트 계획',
        'GTO Wizard AI 개발 로드맵 및 향후 업데이트 계획'
    ),
    ('introducing-gto-wizard-ai', 'image-28.png'): (
        '대규모 연산 데이터 기반의 고정밀 GTO 분석 툴',
        '대규모 연산 데이터 기반의 고정밀 GTO 분석 툴'
    ),
    ('introducing-gto-wizard-ai', 'image-29.png'): (
        '멀티웨이 및 동적 텍스처 대응 솔버 기술',
        '멀티웨이 및 동적 텍스처 대응 솔버 기술'
    ),
    ('introducing-gto-wizard-ai', 'image-30.png'): (
        '핸드 히스토리 자동 분석 및 실시간 리포트',
        '핸드 히스토리 자동 분석 및 실시간 리포트'
    ),

    # 6. the-initial-bettors-advantage
    ('the-initial-bettors-advantage', 'image-1.png'): (
        '이니셜 베터의 손익분기 블러프 공식: Risk / (Risk + Reward)',
        '이니셜 베터의 손익분기 블러프 공식'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-3.png'): (
        '이니셜 베터의 주도권 효과 및 에퀴티 우위 시각화',
        '이니셜 베터의 주도권 효과 및 에퀴티 우위 시각화'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-4.png'): (
        '플랍 C-bet 상황에서 이니셜 베터의 레인지 구성',
        '플랍 C-bet 상황에서 이니셜 베터의 레인지 구성'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-5.png'): (
        '턴 배럴링 시 베터의 압박과 상대 방어 레인지',
        '턴 배럴링 시 베터의 압박과 상대 방어 레인지'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-6.png'): (
        '리버 블러프/밸류 비율 최적화 분석',
        '리버 블러프/밸류 비율 최적화 분석'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-7.png'): (
        '인포지션(IP) 이니셜 베터의 EV 극대화 라인',
        '인포지션(IP) 이니셜 베터의 EV 극대화 라인'
    ),
    ('the-initial-bettors-advantage', 'gto-wizard-the-initial-bettors-advantage-image-8.png'): (
        '체크레이즈 직면 시 이니셜 베터의 방어 빈도',
        '체크레이즈 직면 시 이니셜 베터의 방어 빈도'
    ),

    # 7. 10-tips-multiway-pots-in-poker
    ('10-tips-multiway-pots-in-poker', 'image-69.png'): (
        '멀티웨이 폴드 확률 누적 공식: Player1 Fold% × Player2 Fold% × ...',
        '멀티웨이 폴드 확률 누적 공식'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-3.jpg'): (
        '멀티웨이 팟에서 방어 의무 분담(Shared Defense) 원리',
        '멀티웨이 팟에서 방어 의무 분담 원리'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-4.jpg'): (
        '다자간 팟에서 개별 플레이어의 타이트한 방어 레인지',
        '다자간 팟에서 개별 플레이어의 타이트한 방어 레인지'
    ),
    ('10-tips-multiway-pots-in-poker', 'image-70.png'): (
        '"Tight is Right": 멀티웨이 팟에서 밸류 레인지 엄격화',
        'Tight is Right: 멀티웨이 팟에서 밸류 레인지 엄격화'
    ),
    ('10-tips-multiway-pots-in-poker', 'image-71.png'): (
        '멀티웨이 플랍에서 퓨어 넛 중심의 벳 레인지 구성',
        '멀티웨이 플랍에서 퓨어 넛 중심의 벳 레인지 구성'
    ),
    ('10-tips-multiway-pots-in-poker', 'visualizing-implied-odds-11.gif'): (
        '멀티웨이 팟의 높은 임플라이드 오즈 및 리버스 오즈 시각화',
        '멀티웨이 팟의 높은 임플라이드 오즈 및 리버스 오즈 시각화'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-8.jpg'): (
        '멀티웨이에서 작은 벳 사이징(25~33% Pot) 활용 전략',
        '멀티웨이에서 작은 벳 사이징 활용 전략'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-9.jpg'): (
        '스몰 벳으로 에퀴티 디나이얼 및 팟 컨트롤 달성',
        '스몰 벳으로 에퀴티 디나이얼 및 팟 컨트롤 달성'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-10.jpg'): (
        '멀티웨이에서 포지션(IP)의 중요성 극대화 분석',
        '멀티웨이에서 포지션의 중요성 극대화 분석'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-11.jpg'): (
        '라스트 포지션(Last to Act)의 정보 우위와 레인지 유리함',
        '라스트 포지션의 정보 우위와 레인지 유리함'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-12.jpg'): (
        '샌드위치 포지션의 취약성과 방어 난이도',
        '샌드위치 포지션의 취약성과 방어 난이도'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-13.jpg'): (
        '멀티웨이 포스트플랍 레이즈에 대한 대응 전략',
        '멀티웨이 포스트플랍 레이즈에 대한 대응 전략'
    ),
    ('10-tips-multiway-pots-in-poker', 'image-73.png'): (
        '멀티웨이 블러퍼들의 생존율과 에퀴티 분포',
        '멀티웨이 블러퍼들의 생존율과 에퀴티 분포'
    ),
    ('10-tips-multiway-pots-in-poker', 'image-74.png'): (
        '멀티웨이에서 블로커(Blocker) 효과의 증폭 현상',
        '멀티웨이에서 블로커 효과의 증폭 현상'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-15.jpg'): (
        '캡(Capped)된 레인지의 익스플로잇 방지 전략',
        '캡된 레인지의 익스플로잇 방지 전략'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-16.jpg'): (
        '멀티웨이 턴/리버 팟 사이즈 조절 및 오버폴드 유도',
        '멀티웨이 턴/리버 팟 사이즈 조절 및 오버폴드 유도'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-17.jpg'): (
        '다자간 올인 상황에서의 에퀴티 배분',
        '다자간 올인 상황에서의 에퀴티 배분'
    ),
    ('10-tips-multiway-pots-in-poker', 'gto-wizard-multiway-mechanics-image-18.jpg'): (
        '멀티웨이 최종 복습: 10가지 핵심 전술 요약 차트',
        '멀티웨이 최종 복습: 10가지 핵심 전술 요약 차트'
    ),

    # 8. what-is-the-bubble-factor-in-poker-tournaments
    ('what-is-the-bubble-factor-in-poker-tournaments', 'gto-wizard-what-is-the-bubble-factor-in-tournaments-blog-image-5.jpg'): (
        '버블 팩터 1.18 적용 시 필요 승률: 1.18 / (1.18 + 1) = 54% (리스크 프리미엄 반영)',
        '버블 팩터 1.18 적용 시 필요 승률 공식'
    ),

    # 9. the-theory-of-progressive-knockout-tournaments
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image4.jpg'): (
        'PKO 스타팅 바운티 풀 계산: 시작 스택 바운티 – ($50 × 탈락자 수)',
        'PKO 스타팅 바운티 풀 계산 공식'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image5.jpg'): (
        '바운티 획득 가치가 팟 오즈에 미치는 칩 환산 효과',
        '바운티 획득 가치가 팟 오즈에 미치는 칩 환산 효과'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image9.jpg'): (
        'PKO 버블 팩터 계산: 콜에 필요한 최소 에퀴티 = 12 / (27.5 + 9.55) = 32.4%',
        'PKO 버블 팩터 계산 공식'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image10.jpg'): (
        '바운티 크기에 따른 프리플랍 올인/콜 레인지 확장 분석',
        '바운티 크기에 따른 프리플랍 올인/콜 레인지 확장 분석'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image11.jpg'): (
        '빅스택 vs 숏스택 바운티 헌팅 레인지 비교',
        '빅스택 vs 숏스택 바운티 헌팅 레인지 비교'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image12.jpg'): (
        'PKO 후반부 ICM 압박과 바운티 기대값의 상호작용',
        'PKO 후반부 ICM 압박과 바운티 기대값의 상호작용'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image13.jpg'): (
        '파이널 테이블 직전 PKO 칩 가치 변동 그래프',
        '파이널 테이블 직전 PKO 칩 가치 변동 그래프'
    ),
    ('the-theory-of-progressive-knockout-tournaments', 'gto-wizard-progressive-knockout-tournaments-image15.jpg'): (
        'PKO 토너먼트 최적 밸류 벳 및 바운티 방어 전략',
        'PKO 토너먼트 최적 밸류 벳 및 바운티 방어 전략'
    ),

    # 10. how-solvers-work
    ('how-solvers-work', 'gto-wizard-how-solvers-work-btn-vs-bb-srp.jpg'): (
        '기댓값(EV) 산출 공식: E[X] = Σ xᵢ · p(xᵢ)',
        '기댓값(EV) 산출 공식'
    ),
    ('how-solvers-work', 'gto-wizard-how-solvers-work-regret-table.png'): (
        '후회 최소화(CFR) 계산: (⅓ × 0) + (⅓ × 7 BB) + (⅓ × 5 BB) = 4 BB (평균 기댓값)',
        '후회 최소화(CFR) 계산 공식'
    ),
    ('how-solvers-work', 'gto-wizard-how-solvers-work-regret-table-new-strategy.png'): (
        '새로운 전략 업데이트: 액션 후회도(Regret) / 양의 후회도 총합',
        '새로운 전략 업데이트 공식'
    ),
    ('how-solvers-work', 'gto-wizard-how-solvers-work-convex-payoff-space-grapf.jpg'): (
        '게임 이론의 볼록한 보수 공간(Convex Payoff Space)과 내쉬 균형 수렴 그래프',
        '게임 이론의 볼록한 보수 공간과 내쉬 균형 수렴 그래프'
    ),

    # 11. equity-realization
    ('equity-realization', 'gto-wizard-equity-realization-out-of-position-eqr.jpg'): (
        '에퀴티 실현 공식: 에퀴티(승률) × EQR(실현율) × 팟 크기 = 기댓값(EV)',
        '에퀴티 실현 공식'
    ),
    ('equity-realization', 'gto-wizard-equity-realization-out-of-position-eqr-2.jpg'): (
        '아웃오브포지션(OOP)에서의 에퀴티 실현 난이도 및 삭감률 분석',
        '아웃오브포지션(OOP)에서의 에퀴티 실현 난이도 분석'
    ),
    ('equity-realization', 'equity-realization-image-4.jpg'): (
        '포지션별(IP vs OOP) 핸드 카테고리별 EQR 비교 차트',
        '포지션별 핸드 카테고리별 EQR 비교 차트'
    ),

    # 12. variance-and-bankroll-management
    ('variance-and-bankroll-management', 'image-117.png'): (
        '포커 베리언스(분산)의 정규 분포도 및 표준편차 곡선',
        '포커 베리언스의 정규 분포도'
    ),
    ('variance-and-bankroll-management', 'image-118.png'): (
        '10만 핸드 시뮬레이션에 따른 실제 누적 수익 편차',
        '10만 핸드 시뮬레이션에 따른 실제 누적 수익 편차'
    ),
    ('variance-and-bankroll-management', 'image-119.png'): (
        '동일 실력 플레이어 간의 단기 다운스윙 발생 확률 분포',
        '동일 실력 플레이어 간의 단기 다운스윙 발생 확률 분포'
    ),
    ('variance-and-bankroll-management', 'image-120.png'): (
        '승률 및 신뢰구간: 2.5 ± 3.16 BB/100 (Winrate ± 1σ)',
        '승률 및 신뢰구간 공식'
    ),
    ('variance-and-bankroll-management', 'image-121.png'): (
        '파산 위험(RoR) 1% 미만을 유지하기 위한 권장 바이인(BI) 가이드',
        '파산 위험 1% 미만 유지를 위한 뱅크롤 권장 가이드'
    ),
    ('variance-and-bankroll-management', 'image-122.png'): (
        '켈리 기준(Kelly Criterion)을 응용한 최적 뱅크롤 투자 비율',
        '켈리 기준 응용 뱅크롤 투자 비율'
    ),
    ('variance-and-bankroll-management', 'image-123.png'): (
        '하프 켈리(Half-Kelly) 적용 시 변동성 완화 효과',
        '하프 켈리 적용 시 변동성 완화 효과'
    ),
    ('variance-and-bankroll-management', 'image-124.png'): (
        '스테이크 승급 및 강등 기준선(Shot-taking & Move-down Rules)',
        '스테이크 승급 및 강등 기준선'
    ),
    ('variance-and-bankroll-management', 'image-125.png'): (
        '캐시게임 vs 토너먼트 뱅크롤 규모 비교 차트',
        '캐시게임 vs 토너먼트 뱅크롤 규모 비교 차트'
    ),
    ('variance-and-bankroll-management', 'image-126.png'): (
        '장기 기대 승률(True Winrate) 수렴 핸드 수 분석',
        '장기 기대 승률 수렴 핸드 수 분석'
    ),

    # 13. icm-basics
    ('icm-basics', 'image-168.png'): (
        'ICM 칩 가치 비선형성 및 팟 요구 에퀴티 산출 공식',
        'ICM 칩 가치 비선형성 및 팟 요구 에퀴티 산출 공식'
    ),
    ('icm-basics', 'icm-basics-image-13.png'): (
        '칩 EV와 상금 EV 차이에 따른 추가 요구 에퀴티(Risk Premium)',
        '추가 요구 에퀴티(Risk Premium) 분석'
    ),

    # 14. what-is-equity-in-poker
    ('what-is-equity-in-poker', 'image-172.png'): (
        '에퀴티 실현 공식: EQR = 팟 점유율(%) / 핸드 에퀴티(%)',
        '에퀴티 실현 공식'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-6.png'): (
        '실전 플랍에서 핸드별 에퀴티 실현율(EQR) 차이 비교',
        '실전 플랍에서 핸드별 에퀴티 실현율 비교'
    ),
    ('what-is-equity-in-poker', 'image-173.png'): (
        '핸드 에퀴티와 실제 기대 수익(EV)의 상관관계 분석',
        '핸드 에퀴티와 실제 기대 수익의 상관관계 분석'
    ),
    ('what-is-equity-in-poker', 'image-174.png'): (
        '스트리트 진행에 따른 에퀴티 분포도(Equity Distribution) 변화',
        '스트리트 진행에 따른 에퀴티 분포도 변화'
    ),
    ('what-is-equity-in-poker', 'image-175.png'): (
        '핸드 강도별 에퀴티 버킷(Equity Buckets: 넛, 강한 핸드, 마지널, 에어)',
        '핸드 강도별 에퀴티 버킷 분류'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-10.png'): (
        '레인지 구성비에 따른 에퀴티 버킷 시각화',
        '레인지 구성비에 따른 에퀴티 버킷 시각화'
    ),
    ('what-is-equity-in-poker', 'image-176.png'): (
        '플랍 텍스처별 양 플레이어의 에퀴티 버킷 점유율',
        '플랍 텍스처별 양 플레이어의 에퀴티 버킷 점유율'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-12.png'): (
        '핸드 승률 그래프(Equity Graph)와 레인지 우위 비교',
        '핸드 승률 그래프와 레인지 우위 비교'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-13.png'): (
        '넛 어드밴티지(Nut Advantage)의 발생 원리와 베팅 사이즈 결정',
        '넛 어드밴티지 발생 원리 분석'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-14.png'): (
        '최상위 넛 핸드 비중 차이가 가져오는 오버벳 빈도',
        '최상위 넛 핸드 비중 차이가 가져오는 오버벳 빈도'
    ),
    ('what-is-equity-in-poker', 'what-is-equity-in-poker-image-15.png'): (
        '전체 레인지 어드밴티지(Range Advantage)와 하이 프리퀀시 C-bet 전략',
        '전체 레인지 어드밴티지와 하이 프리퀀시 C-bet 전략'
    )
}

def clean_tags(text):
    if not text:
        return text
    # Clean up {{center}} and {{/center}}
    text = re.sub(r'\{\{/?center\}\}', '', text)
    # Clean up {{color[^}]*}} and {{/color}}
    text = re.sub(r'\{\{/?color[^}]*\}\}', '', text)
    # Clean up [[!TODO! ... ]]
    text = re.sub(r'\[\[!TODO![^\]]*\]\]', '', text)
    # Clean up TODO : Clickable ...
    text = re.sub(r'TODO\s*:\s*Clickable[^\n<"]*', '', text)
    return text.strip()

with open('data/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

updated_count = 0

for a in articles:
    aid = a['id']
    content = a.get('content_html', '')
    original_content = content
    
    # 1. First, apply specific mappings to chart wrappers
    def replace_wrapper(match):
        wrapper_html = match.group(0)
        img_m = re.search(r'src="([^"]+)"', wrapper_html)
        if not img_m:
            return wrapper_html
        src_url = img_m.group(1)
        filename = src_url.split('/')[-1]
        
        # Check mapping
        key = (aid, filename)
        if key in CAPTION_MAPPINGS:
            cap_text, alt_text = CAPTION_MAPPINGS[key]
            # Replace alt
            wrapper_html = re.sub(r'alt="[^"]*"', f'alt="{alt_text}"', wrapper_html)
            # Replace caption
            wrapper_html = re.sub(
                r'(<div class="article-(?:chart|img)-caption"[^>]*>)([\s\S]*?)(</div>)',
                rf'\g<1>📊 {cap_text}\g<3>',
                wrapper_html
            )
            return wrapper_html
        return wrapper_html

    content = re.sub(r'<div class="article-chart-wrapper"[^>]*>[\s\S]*?</div>\s*</div>', replace_wrapper, content)
    
    # 2. General cleanup for any remaining {{center}}, {{color}}, etc. in all captions and alts
    def clean_caption_block(match):
        open_tag = match.group(1)
        cap_inner = match.group(2)
        close_tag = match.group(3)
        cleaned_inner = clean_tags(cap_inner)
        if not cleaned_inner.startswith('📊'):
            cleaned_inner = f'📊 {cleaned_inner}'
        return f'{open_tag}{cleaned_inner}{close_tag}'

    content = re.sub(r'(<div class="article-(?:chart|img)-caption"[^>]*>)([\s\S]*?)(</div>)', clean_caption_block, content)
    
    # Clean any remaining tags in alt attributes
    def clean_alt_attr(match):
        alt_val = match.group(1)
        cleaned_alt = clean_tags(alt_val)
        return f'alt="{cleaned_alt}"'
    content = re.sub(r'alt="([^"]*)"', clean_alt_attr, content)
    
    # 3. Clean any remaining {{...}} tags anywhere in the body HTML
    content = clean_tags(content)

    if content != original_content:
        a['content_html'] = content
        updated_count += 1

print(f"Updated articles count: {updated_count}")

with open('data/articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("Saved updated data/articles.json successfully!")
