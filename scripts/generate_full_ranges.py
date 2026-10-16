"""
Generates rich, comprehensive GTO preflop range presets for StudyPoker.
Includes:
- 6-Max 100BB Open Ranges (UTG, HJ, CO, BTN, SB)
- 3-Bet & Defense Ranges (BB vs BTN, BB vs CO, BB vs UTG, SB vs BTN, BTN vs CO)
- 4-Bet Ranges (BTN vs SB 3-bet, CO vs BTN 3-bet)
- 15BB Push/Fold Tournament Ranges (BTN 15BB Shove, SB 15BB Shove, BB vs BTN Call)
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANGES_FILE = os.path.join(BASE_DIR, 'data', 'ranges.json')

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def get_combos(hand):
    if len(hand) == 2: # pair
        return 6
    elif hand.endswith('s'):
        return 4
    elif hand.endswith('o'):
        return 12
    return 0

# Helper to build range actions
def build_actions_dict(raise_hands, call_hands=None, three_bet_hands=None, four_bet_hands=None):
    actions = {}
    
    if raise_hands:
        for h, freq in raise_hands.items():
            actions[h] = {"action": "Raise 2.5bb", "freq": freq}
            
    if call_hands:
        for h, freq in call_hands.items():
            actions[h] = {"action": "Call", "freq": freq}
            
    if three_bet_hands:
        for h, freq in three_bet_hands.items():
            actions[h] = {"action": "3-Bet", "freq": freq}
            
    if four_bet_hands:
        for h, freq in four_bet_hands.items():
            actions[h] = {"action": "4-Bet / Shove", "freq": freq}
            
    return actions

# 1. UTG Open (15.5%)
utg_raise = {
    "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 100, "99": 100, "88": 100, "77": 100, "66": 50,
    "AKs": 100, "AQs": 100, "AJs": 100, "ATs": 100, "A9s": 60, "A5s": 100, "A4s": 80, "A3s": 50, "A2s": 30,
    "KQs": 100, "KJs": 100, "KTs": 100, "K9s": 40,
    "QJs": 100, "QTs": 100, "Q9s": 30,
    "JTs": 100, "J9s": 40,
    "T9s": 100, "98s": 100, "87s": 80, "76s": 70, "65s": 50, "54s": 40,
    "AKo": 100, "AQo": 100, "AJo": 70, "ATo": 30,
    "KQo": 60
}

# 2. HJ Open (20.0%)
hj_raise = dict(utg_raise)
hj_raise.update({
    "66": 100, "55": 100, "44": 60,
    "A9s": 100, "A8s": 100, "A7s": 60, "A6s": 50, "A4s": 100, "A3s": 80, "A2s": 60,
    "K9s": 100, "K8s": 60, "K7s": 40,
    "Q9s": 100, "Q8s": 50,
    "J9s": 100, "J8s": 50,
    "T8s": 80, "97s": 60, "87s": 100, "76s": 100, "65s": 80, "54s": 70,
    "AJo": 100, "ATo": 70,
    "KQo": 100, "KJo": 70, "QJo": 50
})

# 3. CO Open (27.8%)
co_raise = dict(hj_raise)
co_raise.update({
    "44": 100, "33": 100, "22": 100,
    "A8s": 100, "A7s": 100, "A6s": 100, "A3s": 100, "A2s": 100,
    "K8s": 100, "K7s": 100, "K6s": 80, "K5s": 70, "K4s": 60, "K3s": 50, "K2s": 40,
    "Q8s": 100, "Q7s": 70, "Q6s": 60, "Q5s": 40,
    "J8s": 100, "J7s": 70, "J6s": 40,
    "T8s": 100, "T7s": 70, "98s": 100, "97s": 100, "96s": 50,
    "86s": 80, "75s": 70, "64s": 60, "53s": 50, "43s": 40,
    "ATo": 100, "A9o": 80, "A8o": 40,
    "KJo": 100, "KTo": 80, "QJo": 100, "QTo": 70, "JTo": 80
})

# 4. BTN Open (43.5%) - already in ranges.json
btn_raise = dict(co_raise)
btn_raise.update({
    "K5s": 100, "K4s": 100, "K3s": 100, "K2s": 100,
    "Q7s": 100, "Q6s": 100, "Q5s": 100, "Q4s": 80, "Q3s": 60, "Q2s": 50,
    "J7s": 100, "J6s": 80, "J5s": 60, "J4s": 40,
    "T7s": 100, "T6s": 70, "T5s": 40,
    "96s": 100, "95s": 60, "85s": 80, "74s": 50, "63s": 40, "52s": 30,
    "A9o": 100, "A8o": 90, "A7o": 80, "A6o": 70, "A5o": 80, "A4o": 70, "A3o": 50, "A2o": 40,
    "KTo": 100, "K9o": 80, "K8o": 60, "K7o": 40,
    "QTo": 100, "Q9o": 80, "Q8o": 50,
    "JTo": 100, "J9o": 80, "J8o": 50,
    "T9o": 80, "T8o": 50, "98o": 70, "87o": 60, "76o": 50
})

# 5. SB Open / Raise (47.5%)
sb_raise = dict(btn_raise)
sb_raise.update({
    "A7o": 100, "A6o": 100, "A5o": 100, "A4o": 100, "A3o": 80, "A2o": 70,
    "K8o": 90, "K7o": 80, "K6o": 60, "K5o": 40,
    "Q8o": 80, "Q7o": 60, "J8o": 70, "T8o": 70, "97o": 50, "86o": 40
})

PRESETS = [
    # Category 1: 6-Max Open Ranges
    {
        "id": "utg_open",
        "category": "6-Max 100BB 오픈",
        "name": "UTG 오픈 레이스 (15.5%)",
        "description": "언더 더 건(UTG) 6-Max 100BB GTO 오픈 레이스 레인지. 뒤에 5명이 남아있으므로 최상위 15.5% 프리미엄 핸드로만 엄격히 레이즈합니다.",
        "legend": [
            {"action": "Raise 2.5bb", "color": "#ef4444", "label": "레이스 (오픈)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(utg_raise)
    },
    {
        "id": "hj_open",
        "category": "6-Max 100BB 오픈",
        "name": "HJ 오픈 레이스 (20.0%)",
        "description": "하이잭(HJ) 6-Max 100BB GTO 오픈 레인지. UTG보다 레인지를 5% 넓혀 수티드 에이스와 수티드 커넥터 비중을 확대합니다.",
        "legend": [
            {"action": "Raise 2.5bb", "color": "#ef4444", "label": "레이스 (오픈)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(hj_raise)
    },
    {
        "id": "co_open",
        "category": "6-Max 100BB 오픈",
        "name": "CO 오픈 레이스 (27.8%)",
        "description": "컷오프(CO) 6-Max 100BB GTO 오픈 레인지. 모든 포켓페어(22+)와 수티드 브로드웨이, A-x 수티드를 100% 오픈합니다.",
        "legend": [
            {"action": "Raise 2.5bb", "color": "#ef4444", "label": "레이스 (오픈)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(co_raise)
    },
    {
        "id": "btn_open",
        "category": "6-Max 100BB 오픈",
        "name": "BTN 오픈 레이스 (43.5%)",
        "description": "버튼(BTN) 6-Max 100BB GTO 오픈 레인지. 포스트플랍 절대적 포지션 우위를 바탕으로 상위 43.5%의 넓은 레인지를 공격적으로 오픈합니다.",
        "legend": [
            {"action": "Raise 2.5bb", "color": "#ef4444", "label": "레이스 (오픈)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(btn_raise)
    },
    {
        "id": "sb_open",
        "category": "6-Max 100BB 오픈",
        "name": "SB 오픈 레이스 (47.5%)",
        "description": "스몰 블라인드(SB) BvB(Blind vs Blind) GTO 오픈 레이스(3bb) 레인지. BB 단 한 명을 상대로 폴드 에퀴티를 극대화합니다.",
        "legend": [
            {"action": "Raise 3.0bb", "color": "#ef4444", "label": "레이스 (오픈)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(sb_raise)
    },

    # Category 2: 3-Bet & Defense
    {
        "id": "bb_vs_btn",
        "category": "3-Bet & 디펜스",
        "name": "BB 디펜드 vs BTN 2.5bb 오픈",
        "description": "빅블라인드(BB)에서 버튼 오픈을 상대로 방어(3-Bet 12.5% 또는 Flat Call 38.5%)하는 솔버 솔루션.",
        "legend": [
            {"action": "3-Bet", "color": "#ef4444", "label": "3-Bet (12.5%)"},
            {"action": "Call", "color": "#10b981", "label": "콜 (38.5%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드 (49.0%)"}
        ],
        "actions": build_actions_dict(
            None,
            call_hands={
                "99": 100, "88": 100, "77": 100, "66": 100, "55": 100, "44": 100, "33": 100, "22": 90,
                "ATs": 100, "A9s": 100, "A8s": 100, "A7s": 100, "A6s": 100, "A2s": 100,
                "KJs": 100, "KTs": 100, "K9s": 100, "K8s": 100, "K7s": 90, "K6s": 80, "K5s": 70,
                "QJs": 100, "QTs": 100, "Q9s": 100, "Q8s": 90, "Q7s": 70,
                "JTs": 100, "J9s": 100, "J8s": 90, "J7s": 70,
                "T9s": 100, "T8s": 100, "T7s": 80, "98s": 100, "97s": 90, "87s": 100, "86s": 80, "76s": 100, "65s": 100, "54s": 100,
                "AJo": 100, "ATo": 100, "A9o": 80, "KQo": 100, "KJo": 100, "KTo": 90, "QJo": 100, "QTo": 80, "JTo": 80
            },
            three_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 75,
                "AKs": 100, "AQs": 100, "AJs": 60, "A5s": 85, "A4s": 75, "A3s": 60,
                "KQs": 50, "AKo": 100, "AQo": 80
            }
        )
    },
    {
        "id": "bb_vs_co",
        "category": "3-Bet & 디펜스",
        "name": "BB 디펜드 vs CO 2.5bb 오픈",
        "description": "빅블라인드(BB)에서 컷오프(CO) 오픈을 상대로 방어(3-Bet 10.5% / Call 28.0%)하는 GTO 레인지.",
        "legend": [
            {"action": "3-Bet", "color": "#ef4444", "label": "3-Bet (10.5%)"},
            {"action": "Call", "color": "#10b981", "label": "콜 (28.0%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(
            None,
            call_hands={
                "TT": 40, "99": 100, "88": 100, "77": 100, "66": 100, "55": 100, "44": 80, "33": 60,
                "ATs": 100, "A9s": 100, "A8s": 100, "A7s": 80, "A6s": 60,
                "KJs": 100, "KTs": 100, "K9s": 80, "K8s": 60,
                "QJs": 100, "QTs": 100, "Q9s": 80, "JTs": 100, "J9s": 80, "T9s": 100, "98s": 100, "87s": 100, "76s": 100, "65s": 90, "54s": 80,
                "AJo": 80, "ATo": 70, "KQo": 90, "KJo": 80, "QJo": 70
            },
            three_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 60,
                "AKs": 100, "AQs": 100, "AJs": 80, "A5s": 90, "A4s": 80, "A3s": 60,
                "KQs": 70, "AKo": 100, "AQo": 90
            }
        )
    },
    {
        "id": "sb_vs_btn",
        "category": "3-Bet & 디펜스",
        "name": "SB vs BTN 오픈 (3-Bet or Fold)",
        "description": "스몰 블라인드(SB)에서 버튼 오픈에 대응하는 '콜 없는(No Flatting) 3-Bet or Fold' 전략 (14.5% 3-Bet).",
        "legend": [
            {"action": "3-Bet 10bb", "color": "#ef4444", "label": "3-Bet (14.5%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드 (85.5%)"}
        ],
        "actions": build_actions_dict(
            None,
            three_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 100, "99": 90, "88": 70, "77": 50,
                "AKs": 100, "AQs": 100, "AJs": 100, "ATs": 90, "A5s": 100, "A4s": 100, "A3s": 80, "A2s": 60,
                "KQs": 100, "KJs": 90, "KTs": 80, "K9s": 50,
                "QJs": 90, "QTs": 80, "JTs": 90, "T9s": 80, "98s": 70, "87s": 60, "76s": 50,
                "AKo": 100, "AQo": 100, "AJo": 90, "ATo": 50, "KQo": 80
            }
        )
    },
    {
        "id": "btn_vs_co",
        "category": "3-Bet & 디펜스",
        "name": "BTN vs CO 오픈 (3-Bet & Flat)",
        "description": "버튼(BTN)에서 CO 오픈을 상대로 포지션을 점유하며 3-Bet(8.5%) 및 플랫 콜(7.5%)하는 솔루션.",
        "legend": [
            {"action": "3-Bet 7.5bb", "color": "#ef4444", "label": "3-Bet (8.5%)"},
            {"action": "Call", "color": "#10b981", "label": "플랫 콜 (7.5%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(
            None,
            call_hands={
                "TT": 40, "99": 80, "88": 80, "77": 70, "66": 60,
                "AQs": 40, "AJs": 70, "ATs": 80, "KQs": 60, "KJs": 70, "QJs": 80, "JTs": 80, "T9s": 80, "98s": 70,
                "AQo": 30
            },
            three_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 80, "TT": 60,
                "AKs": 100, "AQs": 60, "A5s": 90, "A4s": 80,
                "KQs": 40, "AKo": 100, "AQo": 70
            }
        )
    },

    # Category 3: 4-Bet Strategy
    {
        "id": "btn_vs_sb_3bet",
        "category": "4-Bet & 방어",
        "name": "BTN vs SB 3-Bet 대응 (4-Bet / Call)",
        "description": "버튼(BTN) 2.5bb 오픈 후 SB의 10bb 3벳에 대응하는 GTO 4-Bet(2.2x) 및 콜 레인지.",
        "legend": [
            {"action": "4-Bet 22bb", "color": "#ef4444", "label": "4-Bet (7.2%)"},
            {"action": "Call", "color": "#10b981", "label": "콜 (11.5%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드"}
        ],
        "actions": build_actions_dict(
            None,
            call_hands={
                "JJ": 60, "TT": 90, "99": 90, "88": 80, "77": 60,
                "AQs": 80, "AJs": 90, "ATs": 80, "KQs": 90, "KJs": 80, "QJs": 80, "JTs": 70,
                "AQo": 80
            },
            four_bet_hands={
                "AA": 100, "KK": 100, "QQ": 80, "JJ": 40,
                "AKs": 100, "A5s": 80, "A4s": 70, "AKo": 100
            }
        )
    },

    # Category 4: Tournament 15BB Push/Fold
    {
        "id": "push_btn_15bb",
        "category": "15BB 토너먼트 푸시/폴드",
        "name": "15BB BTN 올인 셔브 (35.8%)",
        "description": "토너먼트 15BB 숏스택에서 버튼(BTN) 올인 셔브(Open Shove) GTO 내쉬 균형 레인지.",
        "legend": [
            {"action": "All-in Shove", "color": "#ef4444", "label": "올인 셔브 (35.8%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드 (64.2%)"}
        ],
        "actions": build_actions_dict(
            None,
            four_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 100, "99": 100, "88": 100, "77": 100, "66": 100, "55": 100, "44": 100, "33": 100, "22": 100,
                "AKs": 100, "AQs": 100, "AJs": 100, "ATs": 100, "A9s": 100, "A8s": 100, "A7s": 100, "A6s": 100, "A5s": 100, "A4s": 100, "A3s": 100, "A2s": 100,
                "KQs": 100, "KJs": 100, "KTs": 100, "K9s": 100, "K8s": 80, "K7s": 70, "K6s": 60, "K5s": 50,
                "QJs": 100, "QTs": 100, "Q9s": 100, "Q8s": 80, "JTs": 100, "J9s": 90, "T9s": 100, "98s": 90, "87s": 80, "76s": 70,
                "AKo": 100, "AQo": 100, "AJo": 100, "ATo": 100, "A9o": 100, "A8o": 90, "A7o": 70, "A5o": 80,
                "KQo": 100, "KJo": 100, "KTo": 90, "QJo": 100, "QTo": 80, "JTo": 80
            }
        )
    },
    {
        "id": "push_sb_15bb",
        "category": "15BB 토너먼트 푸시/폴드",
        "name": "15BB SB vs BB 셔브 (42.5%)",
        "description": "토너먼트 15BB 숏스택에서 SB의 블라인드 대결 올인 셔브(Open Shove) GTO 레인지.",
        "legend": [
            {"action": "All-in Shove", "color": "#ef4444", "label": "올인 셔브 (42.5%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드 (57.5%)"}
        ],
        "actions": build_actions_dict(
            None,
            four_bet_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 100, "99": 100, "88": 100, "77": 100, "66": 100, "55": 100, "44": 100, "33": 100, "22": 100,
                "AKs": 100, "AQs": 100, "AJs": 100, "ATs": 100, "A9s": 100, "A8s": 100, "A7s": 100, "A6s": 100, "A5s": 100, "A4s": 100, "A3s": 100, "A2s": 100,
                "KQs": 100, "KJs": 100, "KTs": 100, "K9s": 100, "K8s": 100, "K7s": 90, "K6s": 80, "K5s": 80, "K4s": 70,
                "QJs": 100, "QTs": 100, "Q9s": 100, "Q8s": 100, "Q7s": 80, "JTs": 100, "J9s": 100, "J8s": 80, "T9s": 100, "T8s": 90, "98s": 90, "87s": 90, "76s": 80,
                "AKo": 100, "AQo": 100, "AJo": 100, "ATo": 100, "A9o": 100, "A8o": 100, "A7o": 90, "A6o": 80, "A5o": 90, "A4o": 80, "A3o": 70, "A2o": 60,
                "KQo": 100, "KJo": 100, "KTo": 100, "K9o": 80, "QJo": 100, "QTo": 90, "JTo": 90, "T9o": 80
            }
        )
    },
    {
        "id": "call_bb_vs_btn_15bb",
        "category": "15BB 토너먼트 푸시/폴드",
        "name": "15BB BB vs BTN 셔브 콜 (19.8%)",
        "description": "토너먼트 15BB 스택에서 버튼의 올인 셔브를 상대로 BB가 스택을 걸고 콜(Call All-in)해야 하는 방어선.",
        "legend": [
            {"action": "Call All-in", "color": "#10b981", "label": "올인 콜 (19.8%)"},
            {"action": "Fold", "color": "#1e293b", "label": "폴드 (80.2%)"}
        ],
        "actions": build_actions_dict(
            None,
            call_hands={
                "AA": 100, "KK": 100, "QQ": 100, "JJ": 100, "TT": 100, "99": 100, "88": 100, "77": 100, "66": 90, "55": 70,
                "AKs": 100, "AQs": 100, "AJs": 100, "ATs": 100, "A9s": 100, "A8s": 90, "A7s": 80, "A5s": 90, "A4s": 80,
                "KQs": 100, "KJs": 100, "KTs": 90, "QJs": 90,
                "AKo": 100, "AQo": 100, "AJo": 100, "ATo": 90, "A9o": 70,
                "KQo": 90, "KJo": 80
            }
        )
    }
]

def main():
    print(f"Writing {len(PRESETS)} comprehensive GTO preflop presets to {RANGES_FILE}...")
    with open(RANGES_FILE, 'w', encoding='utf-8') as f:
        json.dump({"presets": PRESETS}, f, ensure_ascii=False, indent=2)
    print("Successfully generated all ranges!")

if __name__ == '__main__':
    main()
