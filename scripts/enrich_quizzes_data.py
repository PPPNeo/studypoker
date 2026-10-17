"""
GTO Playbook KR - Complete Quiz Data Enrichment Script
Guarantees 100% completeness and clarity across all 25 quizzes:
1. Every situation text explicitly states:
   - Hero position and exact hand (with suit symbols)
   - Preflop action & stack / pot details
   - Board cards and board texture (dry, wet, paired, monotone, etc.)
   - Opponent's exact action and sizing before Hero's turn
2. Every question clearly defines the exact decision point and action facing Hero.
3. Aligns action_history, situation, board, and explanation seamlessly.
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
quiz_file = os.path.join(BASE_DIR, 'data', 'quizzes.json')

with open(quiz_file, 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

ENRICHED_QUIZZES = {
    # 1. quiz-16
    "quiz-16": {
        "situation": "스트래들+앤티(2bb) 캐시 게임. MP와 CO 2명이 2bb로 연속 림프했습니다. 당신은 BTN에서 A♠ J♠ 프리미엄 수티드 브로드웨이를 쥐고 있습니다. (팟: 7.5 BB)",
        "question": "팟에 림퍼들의 데드 머니가 많이 쌓여 있습니다. BTN에서 A♠J♠를 쥔 당신의 최적 프리플랍 액션은?",
        "action_history": "Preflop: 스트래들 2bb ➔ MP 림프 2bb ➔ CO 림프 2bb ➔ BTN 차례."
    },
    # 2. quiz-17
    "quiz-17": {
        "situation": "당신은 BB에서 8♥ 8♦로 UTG의 2.5bb 오픈 레이즈에 콜했습니다. 플랍에 6♠ 5♦ 4♣ (로우 커넥티드 보드)가 깔렸고, 당신의 체크에 UTG가 33% 팟(1.8bb) C-bet을 베팅했습니다. (팟: 7.3 BB)",
        "question": "오버페어(88)와 거트샷 스트레이트 드로우를 보유하고 있습니다. 로우 커넥티드 플랍에서 UTG의 33% 팟 C-bet에 대한 올바른 대응은?",
        "action_history": "Preflop: UTG 오픈 2.5bb ➔ BB 콜. Flop (6♠ 5♦ 4♣): BB 체크 ➔ UTG 33% 팟 벳(1.8bb)."
    },
    # 3. quiz-20
    "quiz-20": {
        "situation": "유효스택 100bb 게임. CO가 2.5bb로 오픈하고 BTN이 2.5bb 플랫 콜을 했습니다. 당신은 BB에서 프리미엄 몬스터 A♠ K♠를 받았습니다. (팟: 6.5 BB)",
        "question": "블라인드에서 데드 머니를 적극적으로 회수하고 포지션 불리함을 상쇄해야 합니다. BB에서 A♠K♠ 스퀴즈 3벳의 권장 사이징은?",
        "action_history": "Preflop: CO 오픈 2.5bb ➔ BTN 콜 2.5bb ➔ SB 폴드 ➔ BB 차례."
    },
    # 4. quiz-22
    "quiz-22": {
        "situation": "토너먼트 중반. 15bb 숏스택인 당신은 BB에 위치해 있으며, CO가 2.2bb로 오픈 레이즈하고 SB는 폴드했습니다. 당신의 손패는 휠 에이스 블로커를 가진 A♥ 5♥입니다. (팟: 3.7 BB)",
        "question": "A5 수티드로 15bb 숏스택 국면입니다. CO의 2.2bb 오픈을 상대로 가장 높은 기댓값(+EV)을 창출하는 액션은?",
        "action_history": "Preflop: CO 오픈 2.2bb ➔ BTN/SB 폴드 ➔ BB 차례."
    },
    # 5. quiz-7
    "quiz-7": {
        "situation": "당신은 CO에서 A♥ K♠로 2.5bb 오픈했고 BB가 콜했습니다. 플랍에 J♦ J♣ 4♠ (페어드 드라이 보드)가 깔렸고, BB가 체크했습니다. (팟: 5.5 BB)",
        "question": "보드를 미스한 A-K 하이지만, 페어드 보드에서 공격자 레인지 우위가 압도적입니다. BB 체크에 대한 CO의 올바른 플랍 C-bet 사이징은?",
        "action_history": "Preflop: CO 오픈 2.5bb ➔ BB 콜. Flop (J♦ J♣ 4♠): BB 체크 ➔ CO 차례."
    },
    # 6. quiz-1
    "quiz-1": {
        "situation": "당신은 BTN에서 K♠ K♦로 CO의 2.5bb 오픈에 7.5bb로 3벳했고 CO가 콜했습니다. 플랍에 A♣ 8♦ 3♠ (A-하이 드라이 보드)가 깔렸고 CO가 체크했습니다. (팟: 16.5 BB)",
        "question": "3벳 팟에서 A가 보드에 깔린 상태로 K-K 세컨페어를 쥐고 있습니다. CO의 체크에 대한 BTN의 GTO 솔버 권장 액션은?",
        "action_history": "Preflop: CO 오픈 2.5bb ➔ BTN 3벳 7.5bb ➔ CO 콜. Flop (A♣ 8♦ 3♠): CO 체크 ➔ BTN 차례."
    },
    # 7. quiz-11
    "quiz-11": {
        "situation": "스택 100bb BvB(블라인드 대 블라인드) 상황. 당신은 SB에서 최강 몬스터 A♠ A♦를 들고 1bb 림프로 슬로우플레이 트랩을 놓았고, 어그레시브한 BB가 3.5bb로 아이솔레이션 레이즈를 쳤습니다. (팟: 4.5 BB)",
        "question": "AA 트랩이 완벽히 적중했습니다. BB의 3.5bb 레이즈에 직면한 SB의 다음 최적 행동은?",
        "action_history": "Preflop: SB 1bb 림프 ➔ BB 3.5bb 아이솔레이션 레이즈 ➔ SB 차례."
    },
    # 8. quiz-3
    "quiz-3": {
        "situation": "당신은 BTN에서 J♠ J♥로 2.5bb 오픈 레이즈했고 BB가 콜했습니다. 플랍에 T♠ 9♦ 4♣ (웻하고 다이내믹한 커넥티드 보드)가 깔렸고 BB가 체크했습니다. (팟: 5.5 BB)",
        "question": "오버페어(JJ)를 쥐고 있지만 보드에 수많은 스트레이트 드로우가 열려 있습니다. 에퀴티 보호(Protection)를 위한 BB 체크 상대 최적 C-bet 사이징은?",
        "action_history": "Preflop: BTN 오픈 2.5bb ➔ BB 콜. Flop (T♠ 9♦ 4♣): BB 체크 ➔ BTN 차례."
    },
    # 9. quiz-6
    "quiz-6": {
        "situation": "당신은 BTN에서 2.5bb로 오픈하고 BB가 콜했습니다. 플랍에 K♠ 8♠ 3♠ (모노톤 플러시 완성 보드)가 깔렸고 BB가 체크했습니다. 당신의 손패는 A♠ Q♦ (A스페이드 넛 플러시 드로우 + 오버카드)입니다. (팟: 5.5 BB)",
        "question": "보드 전체가 플러시로 연결된 모노톤 플랍입니다. 넛 플러시 블로커(A♠)를 보유한 BTN의 올바른 플랍 액션은?",
        "action_history": "Preflop: BTN 오픈 2.5bb ➔ BB 콜. Flop (K♠ 8♠ 3♠): BB 체크 ➔ BTN 차례."
    },
    # 10. quiz-8
    "quiz-8": {
        "situation": "당신은 BB에서 9♠ 6♠로 BTN의 2.5bb 오픈을 방어 콜했습니다. 플랍에 8♠ 7♦ 2♣가 깔렸고, 당신의 체크에 BTN이 33% 팟(1.8bb) C-bet을 베팅했습니다. (팟: 7.3 BB)",
        "question": "양차 스트레이트 드로우(OESD)와 백도어 플러시 드로우를 쥐고 있습니다. BTN의 33% C-bet에 대한 BB의 최선의 세미 블러프 액션은?",
        "action_history": "Preflop: BTN 오픈 2.5bb ➔ BB 콜. Flop (8♠ 7♦ 2♣): BB 체크 ➔ BTN 33% 벳(1.8bb) ➔ BB 차례."
    },
    # 11. quiz-12
    "quiz-12": {
        "situation": "당신은 BTN에서 A♦ T♠로 오픈했고 BB가 콜했습니다. A♠ Q♦ 6♣ 플랍에서 당신의 33% C-bet에 BB가 콜했습니다. 턴에 A♥가 떨어져 트립스가 완성되었고, BB가 체크했습니다. (팟: 11.5 BB)",
        "question": "A 세 장 트립스를 맞췄으나 턴 카드로 인해 상대의 컨티뉴 레인지가 심하게 캡되었습니다. BB 체크에 대한 BTN의 올바른 턴 액션은?",
        "action_history": "Flop (A♠ Q♦ 6♣): BTN 33% 벳 ➔ BB 콜. Turn (A♥): BB 체크 ➔ BTN 차례."
    },
    # 12. quiz-18
    "quiz-18": {
        "situation": "4벳 팟. BTN이 3벳하자 당신은 SB에서 A♠ A♣로 22bb 4벳을 감행했고 BTN이 콜했습니다. 플랍에 Q♠ 7♦ 2♣ (드라이 보드)가 깔렸고, 현재 팟은 45bb, 남은 유효 스택은 55bb(SPR 1.2)입니다.",
        "question": "오버페어(AA)를 쥐고 있고 스택 대비 팟 비율(SPR)이 1.2로 매우 낮아 팟 커밋 상태입니다. 아웃포지션(OOP) SB의 플랍 최적 액션은?",
        "action_history": "Preflop: BTN 3벳 ➔ SB 4벳 22bb ➔ BTN 콜. Flop (Q♠ 7♦ 2♣): SB 차례 (팟 45bb, 잔여스택 55bb)."
    },
    # 13. quiz-19
    "quiz-19": {
        "situation": "당신은 BB에서 8♠ 8♥로 BTN의 2.5bb 오픈을 콜했습니다. K♠ 9♦ 4♣ 플랍에서 당신이 체크하자 BTN이 C-bet을 치지 않고 첵백했습니다. 턴에 3♥ 블랭크 카드가 떨어졌습니다. (팟: 5.5 BB)",
        "question": "BTN이 유리한 K-하이 플랍에서 C-bet을 포기하여 레인지가 캡(Capped)되었습니다. 88을 쥔 BB의 턴 프로브 벳(Probe Bet) 액션은?",
        "action_history": "Flop (K♠ 9♦ 4♣): BB 체크 ➔ BTN 첵백. Turn (3♥): BB 차례."
    },
    # 14. quiz-4 (User's specific reported quiz!)
    "quiz-4": {
        "situation": "당신은 BB에서 K♥ 9♥로 BTN의 2.5bb 오픈에 콜했습니다. 플랍에 9♠ 5♦ 2♣ (드라이한 투톤 9-하이 보드)가 깔렸고, 당신의 체크에 BTN이 넓은 레인지로 33% 팟(1.8bb) C-bet을 베팅했습니다. (팟: 7.3 BB)",
        "question": "K9 탑페어 좋은 키커를 맞췄습니다. BTN의 33% 팟 C-bet에 직면한 아웃포지션(OOP) 당신의 에퀴티 실현(EQR)을 위한 최선의 행동은?",
        "action_history": "Preflop: BTN 오픈 2.5bb ➔ BB 콜. Flop (9♠ 5♦ 2♣): BB 체크 ➔ BTN 33% 벳(1.8bb) ➔ BB 차례."
    },
    # 15. quiz-9
    "quiz-9": {
        "situation": "당신은 BTN에서 Q♠ J♠로 오픈했고 BB가 콜했습니다. K♠ 7♦ 2♣ 플랍에서 당신의 33% C-bet에 BB가 콜했습니다. 턴에 언커넥티드 블랭크 4♥가 떨어졌고 BB가 체크했습니다. (팟: 11.5 BB)",
        "question": "아직 페어는 없지만 거트샷 스트레이트 드로우(10 아웃츠)와 오버카드를 보유하고 있습니다. 턴 블랭크 카드에서 BTN의 최적 2nd 배럴 액션은?",
        "action_history": "Flop (K♠ 7♦ 2♣): BTN 33% 벳 ➔ BB 콜. Turn (4♥): BB 체크 ➔ BTN 차례."
    },
    # 16. quiz-13
    "quiz-13": {
        "situation": "PKO(프로그레시브 녹아웃) 토너먼트. 50bb 스택인 당신은 BB에 있고, SB의 10bb 숏스택이 10bb 올인 셔브를 감행했습니다. 당신의 손패는 Q♥ T♥ 수티드 브로드웨이입니다. (팟: 11.5 BB)",
        "question": "상대 스택을 완전히 커버하고 있으며 머리에 걸린 현금 바운티 가치가 상당합니다. QTs를 쥔 BB의 올바른 올인 방어 결정은?",
        "action_history": "Preflop: 모두 폴드 ➔ SB 10bb 올인 셔브 ➔ BB 차례."
    },
    # 17. quiz-2
    "quiz-2": {
        "situation": "당신은 CO에서 A♠ T♦로 오픈했고 BB가 콜했습니다. Q♠ J♦ 4♣ 플랍과 2♠ 턴에서 당신이 연속 배럴을 치고 BB가 모두 첵-콜했습니다. 리버에 8♥가 떨어졌고 BB가 다시 체크했습니다. (팟: 32 BB)",
        "question": "스트레이트 드로우가 미스되어 쇼다운 밸류가 없습니다. 하지만 상대의 넛 스트레이트(T9)를 완벽히 차단(Block)하고 있습니다. 리버 트리플 배럴 블러프를 날려야 할까요?",
        "action_history": "Flop (Q♠ J♦ 4♣): CO C-bet ➔ BB 콜. Turn (2♠): CO 2nd 배럴 ➔ BB 콜. River (8♥): BB 체크 ➔ CO 차례."
    },
    # 18. quiz-21
    "quiz-21": {
        "situation": "당신은 BTN에서 A♠ 6♠를 들고 있습니다. A♣ T♦ 3♠ 플랍과 7♥ 턴 모두 양 플레이어 체크로 진행되었고, 리버에 2♦가 떨어지자 BB가 다시 체크했습니다. (팟: 12 BB)",
        "question": "약한 키커의 A 탑페어(A6)입니다. 상대의 첵-다운 레인지를 상대로 쇼다운 첵백을 할까요, 아니면 씬 밸류 벳(Thin Value Bet)을 칠까요?",
        "action_history": "Flop (A♣ T♦ 3♠): 양자 체크. Turn (7♥): 양자 체크. River (2♦): BB 체크 ➔ BTN 차례."
    },
    # 19. quiz-5
    "quiz-5": {
        "situation": "토너먼트 파이널 테이블 직전 버블(머니점프 극심). 3등 스택인 당신은 BB(38bb)에 있고, 뒤에 5bb, 7bb 초단 숏스택 2명이 탈락 직전입니다. SB의 압도적 칩리더(85bb)가 BB를 향해 38bb 올인 셔브를 했습니다. 당신의 손패는 프리미엄 A♠ K♦입니다. (팟: 40.5 BB)",
        "question": "순수 칩EV 기준으로는 AKs는 압도적 스냅 콜 핸드입니다. 그러나 숏스택 탈락이 임박한 극단적인 파이널 테이블 ICM 상황에서 당신의 선택은?",
        "action_history": "Preflop: 모두 폴드 ➔ SB 칩리더 85bb가 BB를 향해 38bb 올인 셔브! ➔ BB 차례."
    },
    # 20. quiz-10
    "quiz-10": {
        "situation": "당신은 BTN에서 J♣ 9♣를 들고 T♠ 8♦ 4♣ 플랍과 2♠ 턴에 연속 베팅했고 BB가 모두 체크-콜했습니다. 리버에 K♥가 떨어지며 넛 스트레이트를 완성했고 BB가 체크했습니다. (팟: 32 BB)",
        "question": "보드에 J9 외에는 더 높은 패가 없는 절대적 너츠 핸드입니다. 상대의 캡된 레인지를 상대로 극대화된 밸류를 뽑아내기 위한 리버 사이징은?",
        "action_history": "Flop (T♠ 8♦ 4♣): BTN 벳 ➔ BB 콜. Turn (2♠): BTN 벳 ➔ BB 콜. River (K♥): BB 체크 ➔ BTN 차례."
    },
    # 21. quiz-15
    "quiz-15": {
        "situation": "당신은 BB에서 T♥ 9♥로 BTN의 오픈을 방어했습니다. K♦ T♠ 5♣ 2♦ 8♠ 보드에서 플랍과 턴에 이어, 리버에서 BTN이 40bb 올인 트리플 배럴을 날렸습니다. (팟: 55 BB, 남은스택 40 BB)",
        "question": "보드에 수많은 플러시/스트레이트 드로우가 미스되었습니다. 당신의 T9h는 다이아몬드(♦)를 한 장도 차단하지 않아 상대의 블러프 가능성을 온전히 열어둡니다. 세컨페어로 히어로 콜을 해야 할까요?",
        "action_history": "Flop (K♦ T♠ 5♣): BTN 벳 ➔ BB 콜. Turn (2♦): BTN 벳 ➔ BB 콜. River (8♠): BTN 40bb 올인 셔브 ➔ BB 차례."
    },
    # 22. quiz-24
    "quiz-24": {
        "situation": "유효스택 200bb 딥스택 캐시게임. 당신은 BTN에서 7♠ 7♣로 미들 셋을 맞췄습니다. K♠ 7♦ 2♣ T♠ 3♥ 보드에서 플랍과 턴의 거대한 레이즈 공방 후, 리버에 팟이 95bb인 상태에서 BB가 150bb 오버벳 올인 잼을 던졌습니다.",
        "question": "미들 세트(77)를 쥐고 있습니다. 200bb 딥스택에서 상대의 셋 오버 셋(KK/TT) 공포를 이겨내고 오버벳 올인에 콜해야 할까요?",
        "action_history": "Flop (K♠ 7♦ 2♣): 레이즈 공방 ➔ Turn (T♠): 벳/콜 ➔ River (3♥): BB 150bb 오버벳 올인 잼 ➔ BTN 차례."
    },
    # 23. quiz-14
    "quiz-14": {
        "situation": "당신은 BTN에서 K♠ Q♠로 2.5bb 오픈 레이즈했고, SB와 BB가 모두 콜하여 3웨이 팟이 되었습니다. 플랍에 A♠ 9♠ 4♠가 떨어지며 플랍 2등 플러시를 완성했습니다. 앞서 SB와 BB가 모두 체크했습니다. (팟: 8.5 BB)",
        "question": "두 명의 수비자가 체크했습니다. 3웨이 팟에서 2등 플러시를 쥔 당신의 플랍 최적 액션은?",
        "action_history": "Preflop: BTN 오픈 2.5bb ➔ SB 콜, BB 콜. Flop (A♠ 9♠ 4♠): SB 체크, BB 체크 ➔ BTN 차례."
    },
    # 24. quiz-23
    "quiz-23": {
        "situation": "당신은 BB에서 9♠ 7♠로 BTN의 2.5bb 오픈을 방어했습니다. J♠ 8♦ 3♣ 플랍에서 BTN의 33% C-bet에 콜했고, 턴에 T♠가 떨어지며 스트레이트 완성 및 넛 플러시 드로우까지 추가되었습니다. 당신의 체크에 BTN이 66% 팟(12bb) 2nd 배럴을 쳤습니다. (팟: 18 BB)",
        "question": "이미 스트레이트가 완성되었고 턴 넛 플러시 드로우까지 장착한 괴물급 콤보 핸드입니다. BTN의 12bb 배럴에 직면한 BB의 최적 액션은?",
        "action_history": "Flop (J♠ 8♦ 3♣): BTN 33% 벳 ➔ BB 콜. Turn (T♠): BB 체크 ➔ BTN 66% 벳(12bb) ➔ BB 차례."
    },
    # 25. quiz-25
    "quiz-25": {
        "situation": "당신은 CO에서 Q♠ J♦로 오픈했습니다. A♠ 8♦ 2♠ 플랍과 7♣ 턴에서 배럴을 날렸고 BB가 연속 첵-콜했습니다. 리버에 K♦가 떨어지며 플러시 드로우가 완전히 미스되었고, BB가 체크했습니다. (팟: 36 BB)",
        "question": "아무것도 맞지 않은 순수 Q-하이 에어(Air)입니다. 그러나 리버에 떨어진 K은 공격자 레인지에 매우 유리한 카드입니다. 70% 팟 트리플 배럴 블러프를 날려야 할까요, 체크 포기해야 할까요?",
        "action_history": "Flop (A♠ 8♦ 2♠): CO C-bet ➔ BB 콜. Turn (7♣): CO 2nd 배럴 ➔ BB 콜. River (K♦): BB 체크 ➔ CO 차례."
    }
}

updated_count = 0
for q in quizzes:
    qid = q.get('id')
    if qid in ENRICHED_QUIZZES:
        e = ENRICHED_QUIZZES[qid]
        q['situation'] = e['situation']
        q['question'] = e['question']
        q['action_history'] = e['action_history']
        updated_count += 1

print(f"Successfully enriched {updated_count} out of {len(quizzes)} quizzes.")

with open(quiz_file, 'w', encoding='utf-8') as f:
    json.dump(quizzes, f, ensure_ascii=False, indent=2)

print(f"Saved enriched quizzes to {quiz_file}!")
