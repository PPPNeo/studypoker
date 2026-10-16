"""
Builds the complete expanded library of 15 GTO Wizard articles with Korean localization,
summary cards, interactive term tags, and original GTO Wizard URLs.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

articles = [
  # ==================== LEVEL 1: FUNDAMENTALS (3편) ====================
  {
    "id": "what-is-expected-value-in-poker",
    "slug": "what-is-expected-value-in-poker",
    "title_ko": "기대값(EV)이란 무엇인가? 포커 수학의 절대 원칙",
    "title_en": "What Is Expected Value in Poker?",
    "level": "Level 1 (입문)",
    "category": "수학/기초",
    "read_time": "5분",
    "author": "GTO Wizard Team & Coach Matt",
    "original_url": "https://blog.gtowizard.com/what-is-expected-value-in-poker/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "단기 결과는 노이즈다",
        "text": "단 한 판의 팟 승패(운)는 잊으세요. 포커에서 실력이란 오직 '장기적 기대값(+EV)이 높은 결정을 몇 번 내렸는가'로 측정됩니다."
      },
      {
        "badge": "핵심 2",
        "title": "EV 공식의 직관적 이해",
        "text": "EV = (이겼을 때 얻는 팟 × 승률) - (졌을 때 잃는 베팅 × 패배율). 0보다 크면 무조건 장기적으로 돈을 버는 결정입니다."
      },
      {
        "badge": "핵심 3",
        "title": "폴드(Fold)의 EV는 항상 0이다",
        "text": "모든 콜, 레이스, 베팅 결정은 '폴드했을 때의 기준선(0 EV)'보다 더 높은 EV를 창출할 수 있는지를 비교하는 것입니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커를 취미로 즐기는 유저와 프로 플레이어를 가르는 단 하나의 차이는 바로 <strong><span class="gto-term" data-term="ev">기대값(Expected Value, EV)</span></strong>에 대한 태도입니다. 피쉬는 "이번 판에 이겼는가 졌는가"를 보지만, 프로는 "이 선택이 장기적으로 얼마의 EV를 남겼는가"만을 계산합니다.
      </div>

      <h2>1. EV의 직관적인 개념: 동전 던지기 비유</h2>
      <p>친구가 당신에게 이런 내기를 제안했다고 상상해 봅시다.</p>
      <div class="quote-box">
        <em>"동전을 던져서 앞면이 나오면 내가 너한테 2,000원을 주고, 뒷면이 나오면 네가 나한테 1,000원만 줘."</em>
      </div>
      <p>동전 앞뒤 확률은 각각 50%입니다. 당신의 1회 시행 기대값은 다음과 같습니다.</p>
      <ul>
        <li>앞면 (50%): +2,000원 × 0.5 = +1,000원</li>
        <li>뒷면 (50%): -1,000원 × 0.5 = -500원</li>
        <li><strong>최종 EV = +1,000원 - 500원 = +500원</strong></li>
      </ul>
      <p>만약 첫 판에 뒷면이 나와서 1,000원을 잃었다고 해서 당신이 잘못된 결정을 내린 것일까요? <strong>절대 아닙니다.</strong> 1,000번 반복하면 당신은 약 50만 원의 순이익을 얻습니다. 포커의 모든 스트리트 선택은 정확히 이 공식의 연속입니다.</p>

      <h2>2. 팟 오즈(Pot Odds)와 EV의 상관관계</h2>
      <p>실전 테이블에서 상대가 팟 100칩에 50칩을 베팅했다고 가정합시다. 총 팟은 150칩이 되었고, 당신은 50칩을 콜해야 합니다.</p>
      <p>이때 당신이 요구받는 <strong>팟 오즈</strong>는 <code>50 / (150 + 50) = 25%</code>입니다. 즉, 내 핸드의 <span class="gto-term" data-term="eqr">에퀴티(승률)</span>가 25%를 넘는다면 이 콜은 무조건 <strong>+EV</strong>가 됩니다!</p>

      <div class="callout-card tip">
        <h4>💡 솔버 마인드셋 체크포인트</h4>
        <p>상대의 벳을 맞닥뜨렸을 때 '감'으로 콜하지 마세요. <strong>[필요 승률(Pot Odds)]</strong>과 <strong>[내 핸드의 에퀴티]</strong>를 비교하여 EV가 플러스인지 마이너스인지만 냉정하게 판단하세요.</p>
      </div>

      <h2>3. 왜 폴드(Fold)의 EV는 0인가?</h2>
      <p>이미 팟에 들어간 블라인드나 이전 스트리트의 칩은 <strong>'매몰 비용(Sunk Cost)'</strong>입니다. 지금 이 순간 당신이 카드를 던지면(Fold), 미래의 손익은 정확히 0입니다.</p>
      <p>따라서 당신이 콜이나 레이스를 고려할 때 유일한 질문은 이것이어야 합니다: <em>"이 행동의 EV가 0보다 큰가?"</em> 만약 콜의 EV가 -0.2 BB라면 아무리 팟이 커도 폴드하는 것이 가장 수학적으로 우월한 선택입니다.</p>
    """
  },
  {
    "id": "equity-realization",
    "slug": "equity-realization",
    "title_ko": "에퀴티 실현(EQR): 왜 50% 승률이 50% 팟을 의미하지 않는가?",
    "title_en": "Equity Realization in Poker",
    "level": "Level 1 (입문)",
    "category": "수학/기초",
    "read_time": "6분",
    "author": "GTO Wizard Strategy Team",
    "original_url": "https://blog.gtowizard.com/equity-realization/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "Raw Equity vs Realized Equity",
        "text": "에퀴티 계산기에서 나오는 50%는 쇼다운까지 무사히 갔을 때의 승률일 뿐, 실전에서는 상대 벳에 폴드당해 팟을 못 챙깁니다."
      },
      {
        "badge": "핵심 2",
        "title": "포지션(IP)의 EQR 부스터",
        "text": "인포지션(IP)은 항상 쇼다운을 공짜로 보거나 블러프로 팟을 뺏을 수 있어 원본 승률 대비 110%~130%의 에퀴티를 실현합니다."
      },
      {
        "badge": "핵심 3",
        "title": "수티드 & 연결성의 마법",
        "text": "핸드의 연결성(Connectors)과 수티드는 백도어 드로우를 만들어 상대의 배럴을 견디고 팟을 실현(EQR)하게 해줍니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        많은 초보자들이 에퀴티 계산기를 돌려보고 충격을 받습니다. <em>"BB에서 K2o가 BTN 레인지 상대로 35%나 승률이 나오는데 왜 폴드해야 하나요?"</em> 답은 바로 <strong><span class="gto-term" data-term="eqr">에퀴티 실현율(EQR)</span></strong> 때문입니다.
      </div>

      <h2>1. 원본 에퀴티(Raw Equity)의 환상</h2>
      <p>포커 카드는 플랍, 턴, 리버 3번의 베팅 라운드를 거쳐야 쇼다운에 도달합니다. 내가 원본 승률 40%를 가지고 있더라도, 상대가 플랍에서 벳하고 턴에서 또 벳할 때 내 핸드가 견디지 못하고 폴드해 버린다면? <strong>실제 획득하는 팟은 0%가 됩니다.</strong></p>
      <p>즉, <strong>실현된 팟 = 순수 에퀴티 × EQR(%)</strong> 공식이 성립합니다.</p>

      <h2>2. EQR을 결정하는 4대 요소</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <h4>1. 포지션 (Position)</h4>
          <p>IP는 상대의 액션을 먼저 보고 마지막에 결정하므로 쇼다운 밸류를 온전히 보전합니다. BB(OOP)는 평균 EQR 70~80%에 불과하지만, BTN(IP)은 110~130%를 실현합니다.</p>
        </div>
        <div class="feature-item">
          <h4>2. 플레이어빌리티 (Playability)</h4>
          <p>수티드(Suited) 핸드나 89s 같은 커넥터는 플랍에서 콤보 드로우나 백도어를 띄워 턴 카드를 계속 볼 수 있게 해줍니다.</p>
        </div>
        <div class="feature-item">
          <h4>3. <span class="gto-term" data-term="spr">SPR (스택 대 팟 비율)</span></h4>
          <p>스택이 깊을수록(Deep Stack) 불리한 포지션의 저주가 심해져 OOP의 EQR이 급격히 추락합니다.</p>
        </div>
        <div class="feature-item">
          <h4>4. 상대의 스킬 수준</h4>
          <p>상대가 공격적인 턴/리버 배럴러라면 방어하기 힘든 핸드들의 EQR은 바닥을 칩니다.</p>
        </div>
      </div>

      <h2>3. 실전 적용: 프리플랍 수비 레인지의 비밀</h2>
      <p>이제 왜 솔버가 <strong>K9o</strong>는 폴드하면서 <strong>65s</strong>나 <strong>54s</strong>는 방어하는지 이해할 수 있습니다. 65s는 원본 승률은 낮지만, 강한 핸드로 발전했을 때 큰 팟을 먹고, 보드를 놓쳤을 때 깔끔하게 포기할 수 있어 EQR이 압도적으로 높기 때문입니다.</p>
    """
  },
  {
    "id": "how-stack-sizes-change-your-range",
    "slug": "how-stack-sizes-change-your-range",
    "title_ko": "스택 크기가 레인지를 어떻게 바꾸는가? 딥스택 vs 숏스택",
    "title_en": "How Stack Sizes Change Your Range",
    "level": "Level 1 (입문)",
    "category": "수학/기초",
    "read_time": "6분",
    "author": "GTO Wizard Team",
    "original_url": "https://blog.gtowizard.com/how-stack-sizes-change-your-range/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "스택이 얕을수록 (Short Stack)",
        "text": "20~30BB 숏스택에서는 포지션의 중요성이 줄어들고, A-high나 하이카드 핸드의 '순수 원본 에퀴티'가 최우선 순위가 됩니다."
      },
      {
        "badge": "핵심 2",
        "title": "스택이 깊을수록 (Deep Stack)",
        "text": "150~200BB 딥스택에서는 수티드 커넥터와 스몰 포켓이 넛(Nut)을 만들어 역대급 임플라이드 오즈를 누릴 수 있습니다."
      },
      {
        "badge": "핵심 3",
        "title": "역임플라이드 오즈의 공포",
        "text": "딥스택에서 약한 키커의 원페어(예: A2o, K9o)는 탑페어를 맞추고도 스택 전체를 잃는 재앙을 부르므로 레인지에서 제외됩니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        토너먼트 초반 100BB 딥스택과 후반 25BB 숏스택에서 똑같은 핸드 레인지를 쓰고 계신가요? 그것은 엄청난 누수(Leak)입니다. <strong>스택 깊이(Stack Depth)</strong>는 레인지의 구성을 근본부터 뒤흔듭니다.
      </div>

      <h2>1. 숏스택 (15 ~ 30 BB): 원본 에퀴티가 왕이다</h2>
      <p>스택이 얕으면 플랍이나 턴에서 거의 모든 스택이 팟에 들어가며 <span class="gto-term" data-term="spr">SPR</span>이 극도로 낮아집니다. 복잡한 3스트리트 마누버링을 할 여유가 없습니다.</p>
      <ul>
        <li><strong>가치 상승</strong>: A-T 오프수트, K-J 오프수트, 88~TT 포켓페어. (원페어 쇼다운으로 즉시 승리 가능)</li>
        <li><strong>가치 하락</strong>: 6-5 수티드, 5-4 수티드. (드로우가 뜰 때까지 팟을 키울 스택이 없음)</li>
      </ul>

      <h2>2. 딥스택 (150 ~ 200 BB): 너트 잠재력(Implied Odds)</h2>
      <p>반대로 딥스택에서는 한 판에 수백 BB가 오갑니다. 여기서 원페어로 200BB 올인에 콜하는 사람은 없습니다.</p>
      <p>따라서 셋(Set), 스트레이트, 넛 플러시를 만들 수 있는 <strong>수티드 커넥터와 스몰 포켓페어의 가치가 폭등</strong>합니다.</p>
    """
  },

  # ==================== LEVEL 2: FLOP STRATEGY (4편) ====================
  {
    "id": "the-right-way-to-think-about-protection",
    "slug": "the-right-way-to-think-about-protection",
    "title_ko": "'프로텍션 벳'의 진실: 상대를 폴드시킨다는 것",
    "title_en": "The Right Way To Think About Protection",
    "level": "Level 2 (초급)",
    "category": "플랍 전략",
    "read_time": "7분",
    "author": "Tombos21 (GTO Wizard Lead Theorist)",
    "original_url": "https://blog.gtowizard.com/the-right-way-to-think-about-protection/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "공짜 에퀴티를 박탈하라",
        "text": "프로텍션의 본질은 내 패를 보호하는 게 아니라 상대의 6아웃츠(25% 승률) 오버카드들이 공짜 턴을 보는 것을 '디나이얼(Denial)'하는 것입니다."
      },
      {
        "badge": "핵심 2",
        "title": "폴드시키거나, 나쁜 가격을 주거나",
        "text": "상대가 폴드하면 팟을 즉시 회수해서 이득이고, 상대가 불리한 팟 오즈로 콜하면 밸류를 뜯어내서 이득입니다."
      },
      {
        "badge": "핵심 3",
        "title": "드라이 보드 vs 웻 보드",
        "text": "상대 에퀴티가 분산된 웻 보드일수록 큰 사이징(60%~75%)으로 프로텍션 베팅을 강하게 날려야 합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커 펍에서 흔히 듣는 말: <em>"플랍에 드로우 깔려서 내 탑페어 보호하려고 올인 박았어!"</em> 하지만 솔버는 프로텍션을 전혀 다른 관점으로 정의합니다.
      </div>

      <h2>1. 프로텍션은 독립된 베팅 카테고리가 아니다</h2>
      <p>포커의 베팅 목적은 전통적으로 2가지로 나뉩니다: <strong>밸류 베팅(더 안 좋은 패의 콜 유도)</strong>과 <strong>블러프 베팅(더 좋은 패의 폴드 유도)</strong>.</p>
      <p>프로텍션은 별개의 3번째 목적이 아니라, <strong>밸류 베팅에 수반되는 '에퀴티 디나이얼(Equity Denial)' 보너스 효과</strong>입니다.</p>

      <h2>2. 수학으로 보는 에퀴티 디나이얼</h2>
      <p>보드가 <strong>T♠ 8♦ 3♣</strong>이고, 당신이 <strong>J♠ J♥</strong>를 쥐고 있습니다. 팟은 100칩입니다.</p>
      <p>상대방이 <strong>A♥ K♦</strong>(오버카드 6아웃츠 = 약 25% 승률)를 쥐고 있다고 해봅시다. 만약 당신이 여기서 체크하면, 상대는 100칩 팟의 25%에 해당하는 <strong>25칩의 공짜 가치</strong>를 얻게 됩니다.</p>
      <ul>
        <li>당신이 50칩을 베팅하고 상대가 <strong>폴드</strong>하면? 👉 상대가 가질 뻔했던 25칩의 지분을 즉시 강탈(Denial)합니다.</li>
        <li>상대가 억지로 50칩을 <strong>콜</strong>하면? 👉 25% 승률 핸드가 33% 팟 오즈 벳을 콜했으므로, 매 콜마다 상대는 수학적 실수를 저지릅니다.</li>
      </ul>
    """
  },
  {
    "id": "c-betting-ip-in-3-bet-pots",
    "slug": "c-betting-ip-in-3-bet-pots",
    "title_ko": "3벳 팟 인포지션(IP) C-bet 전략 완벽 가이드",
    "title_en": "C-Betting IP in 3-Bet Pots",
    "level": "Level 2 (초급)",
    "category": "3벳 팟",
    "read_time": "8분",
    "author": "GTO Wizard Coach Ivan",
    "original_url": "https://blog.gtowizard.com/c-betting-ip-in-3-bet-pots/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "낮은 SPR의 심리학",
        "text": "3벳 팟은 프리플랍 팟이 이미 크기 때문에 SPR이 보통 3~4로 매우 낮습니다. 탑페어만 맞아도 올인 스택을 감당할 수 있습니다."
      },
      {
        "badge": "핵심 2",
        "title": "A-high / K-high 보드의 1/3 C-bet",
        "text": "3베터는 프리플랍에서 AA, KK, AK을 모두 쥐고 있으므로 하이카드 보드에서 75% 이상의 높은 빈도로 스몰 벳(33%)을 구사합니다."
      },
      {
        "badge": "핵심 3",
        "title": "로우 커넥티드 보드의 브레이크",
        "text": "7-6-5나 8-7-6 보드에서는 콜러가 세트와 투페어, 스트레이트 넛 우위를 가지므로 C-bet을 멈추고 첵백 빈도를 높여야 합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커에서 가장 큰 돈이 오가는 격전지가 바로 <strong>3벳 팟(3-Bet Pot)</strong>입니다. 싱글 레이즈드 팟(SRP)과 달리 3벳 팟은 플랍이 열리는 순간 이미 팟이 거대해져 있어 한 번의 사이징 실수로 스택 전체가 날아갈 수 있습니다.
      </div>

      <h2>1. 3벳 팟의 황금 열쇠: <span class="gto-term" data-term="spr">SPR</span></h2>
      <p>100 BB 딥스택 기준으로, CO 오픈(2.5bb) ➔ BTN 3벳(7.5bb) ➔ CO 콜이 나오면 플랍 팟은 약 16.5 BB, 남은 스택은 92.5 BB가 됩니다. 이때 <strong>SPR은 약 5.6</strong>입니다.</p>
      <p>SPR이 5 안팎이면 <strong>'기하학적 팟 사이징' 2~3번이면 리버에 무조건 올인이 들어간다는 뜻</strong>입니다. 따라서 플랍에서 무리하게 큰 벳을 칠 필요가 전혀 없습니다.</p>
    """
  },
  {
    "id": "maximizing-value-on-monotone-flops",
    "slug": "maximizing-value-on-monotone-flops",
    "title_ko": "모노톤 플랍(Monotone Flop)에서의 밸류 극대화 전략",
    "title_en": "Maximizing Value on Monotone Flops",
    "level": "Level 2 (초급)",
    "category": "플랍 전략",
    "read_time": "7분",
    "author": "GTO Wizard Strategy Team",
    "original_url": "https://blog.gtowizard.com/maximizing-value-on-monotone-flops/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "같은 무늬 3장의 공포",
        "text": "K♠ 8♠ 3♠처럼 플랍에 3장의 무늬가 같으면 플러시 완성자가 이미 존재할 수 있어 C-bet 빈도가 전체적으로 급감합니다."
      },
      {
        "badge": "핵심 2",
        "title": "스몰 벳(25%~33%) 사이징",
        "text": "솔버는 모노톤 플랍에서 베팅할 때 대부분 25%~33%의 아주 작은 사이징을 선호합니다. 큰 벳은 상대의 플러시/너트 드로우에게만 액션을 받기 때문입니다."
      },
      {
        "badge": "핵심 3",
        "title": "A♠ 블로커의 압도적 위력",
        "text": "내가 넛 플러시 블로커(A♠)를 한 장 쥐고 있다면, 탑페어나 아무것도 없는 핸드로도 상대에게 엄청난 압박 블러프를 날릴 수 있습니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        플랍에 같은 무늬 3장이 깔리는 <strong>모노톤 보드(Monotone Flop)</strong>는 많은 플레이어들을 공포에 떨게 만듭니다. 플러시가 이미 완성되었을지도 모른다는 두려움 때문입니다.
      </div>

      <h2>1. 모노톤 플랍에서 C-bet 빈도가 떨어지는 이유</h2>
      <p>일반적인 레인보우 보드에서는 프리플랍 어그레서가 70~80% 빈도로 C-bet을 칠 수 있지만, 모노톤 보드에서는 <strong>C-bet 빈도가 35~45%로 절반 가까이 추락</strong>합니다.</p>
      <p>이유는 상대방(BB)의 넓은 방어 레인지에 수많은 수티드 콤보와 원스페이드 드로우 핸드가 걸려있기 때문입니다.</p>

      <h2>2. 25%~33% 스몰 벳의 마법</h2>
      <p>모노톤 보드에서 팟의 75% 같은 큰 벳을 치면, 상대방은 오직 메이드 플러시나 넛 플러시 드로우(A♠x)로만 콜하고 나머지는 다 폴드합니다. 이는 내 밸류 핸드를 고립시키는 최악의 플레이입니다.</p>
      <p>1/4~1/3팟의 스몰 벳을 쳐야만 상대의 미디엄 페어, 페어 없는 넛 드로우들로부터 저렴하게 밸류를 뜯어낼 수 있습니다.</p>
    """
  },
  {
    "id": "small-blind-big-problems-when-to-size-up-from-oop-bvb",
    "slug": "small-blind-big-problems-when-to-size-up-from-oop-bvb",
    "title_ko": "블라인드 대 블라인드(BvB): 언제 OOP에서 큰 벳을 쳐야 하는가?",
    "title_en": "Small Blind, Big Problems: When to Size Up From OOP BvB",
    "level": "Level 2 (초급)",
    "category": "플랍 전략",
    "read_time": "8분",
    "author": "GTO Wizard Coach Ivan",
    "original_url": "https://blog.gtowizard.com/small-blind-big-problems-when-to-size-up-from-oop-bvb/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "BvB의 특수성: 와이드 레인지",
        "text": "SB vs BB는 포커에서 양쪽의 레인지가 가장 넓게 부딪히는 전장입니다. 마지널 핸드의 비중이 극도로 높습니다."
      },
      {
        "badge": "핵심 2",
        "title": "아웃포지션(OOP)의 고통",
        "text": "SB는 3스트리트 내내 먼저 액션해야 하는 최악의 포지션 불리함을 안고 싸워야 합니다."
      },
      {
        "badge": "핵심 3",
        "title": "언제 66%~75%로 사이즈업하는가?",
        "text": "하이카드 드라이 보드나 탑페어 넛 어드밴티지가 확실할 때 큰 사이징으로 IP의 포지션 이점을 무력화해야 합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커에서 가장 플레이하기 까다롭고 누수가 심하게 발생하는 스팟이 바로 <strong>SB vs BB (BvB)</strong>입니다.
      </div>

      <h2>1. 넓은 레인지의 충돌</h2>
      <p>SB 오픈에 대해 BB는 무려 50% 이상의 핸드로 콜이나 3벳을 합니다. 서로의 레인지에 에어(Air)와 약한 핸드가 가득 차 있습니다.</p>

      <h2>2. 언제 스몰 벳(33%)을 치고, 언제 빅 벳(75%)을 치는가?</h2>
      <p><strong>A-x-x나 K-x-x 레인보우 보드</strong>: SB가 강력한 탑페어 너트 우위를 점하므로 1/3 팟으로 넓게 C-bet합니다.</p>
      <p><strong>T-8-6이나 9-7-5 같은 미들 커넥티드 보드</strong>: BB에게 투페어와 스트레이트 너트 우위가 넘어가므로 SB는 대부분의 레인지를 체크로 방어해야 합니다.</p>
    """
  },

  # ==================== LEVEL 3: TURN & RIVER (4편) ====================
  {
    "id": "understanding-blockers-in-poker",
    "slug": "understanding-blockers-in-poker",
    "title_ko": "블로커(Blockers) 완벽 마스터: 최상의 블러프와 콜",
    "title_en": "Understanding Blockers in Poker",
    "level": "Level 3 (중급)",
    "category": "고급 이론",
    "read_time": "9분",
    "author": "GTO Wizard Theory Team",
    "original_url": "https://blog.gtowizard.com/understanding-blockers-in-poker/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "콤보 수학의 파괴력",
        "text": "내 손에 특정 카드 1장만 있어도, 상대가 가질 수 있는 투페어/셋 콤보는 50%, 특정 수티드 콤보는 100% 차단됩니다."
      },
      {
        "badge": "핵심 2",
        "title": "리버 블러프의 황금 룰",
        "text": "상대의 '콜할 핸드(너트/탑페어)'는 블락하고, 상대의 '폴드할 핸드(미스된 드로우)'는 언블락하는 핸드가 신이 내린 블러프 핸드입니다."
      },
      {
        "badge": "핵심 3",
        "title": "블러프 캐칭(콜)의 역발상",
        "text": "상대 올인에 콜할 때는 상대의 블러프 카드(미스된 플러시 카드)를 내가 쥐고 있으면 안 됩니다!"
      }
    ],
    "content_html": """
      <div class="article-lead">
        리버에서 팟은 100BB, 상대가 올인을 박았습니다. 내 손에는 마지널한 페어가 있습니다. <em>"콜해야 할까, 폴드해야 할까?"</em> 이 극한의 순간 승패를 가르는 디테일이 바로 <strong><span class="gto-term" data-term="blocker">블로커</span></strong>입니다.
      </div>

      <h2>1. 블로커란 무엇인가?</h2>
      <p>포커 덱에는 52장의 카드만 존재합니다. 내가 특정 카드를 쥐는 순간, 상대가 그 카드를 가지고 있을 확률은 0이 됩니다.</p>
      <ul>
        <li><strong>미페어 핸드 (예: AK)</strong>: 보드에 A나 K가 없을 때 16가지 조합이 존재합니다. 하지만 내가 A 한 장을 들고 있으면 상대의 AK 콤보는 <strong>8가지로 50% 급감</strong>합니다.</li>
        <li><strong>포켓페어 (예: AA)</strong>: 원래 6가지 조합이지만, 내가 A 한 장을 쥐면 <strong>3가지로 50% 감소</strong>합니다.</li>
      </ul>
    """
  },
  {
    "id": "when-is-bluffing-profitable-the-key-factors-you-need-to-know",
    "slug": "when-is-bluffing-profitable-the-key-factors-you-need-to-know",
    "title_ko": "블러프는 언제 수익이 나는가? 핵심 팩터 5가지",
    "title_en": "When Is Bluffing Profitable? The Key Factors You Need to Know",
    "level": "Level 3 (중급)",
    "category": "고급 이론",
    "read_time": "8분",
    "author": "GTO Wizard Coach Ivan",
    "original_url": "https://blog.gtowizard.com/when-is-bluffing-profitable-the-key-factors-you-need-to-know/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "폴드 에퀴티(Fold Equity)의 원천",
        "text": "블러프가 +EV가 되려면 상대방의 폴드 빈도가 내 베팅 사이즈에 따른 손익분기점(Alpha)을 초과해야 합니다."
      },
      {
        "badge": "핵심 2",
        "title": "쇼다운 밸류의 유무",
        "text": "쇼다운 밸류가 있는 마지널 핸드로 블러프를 치는 것은 자살행위입니다. 이길 수 있는 상대 패를 다 폴드시켜버리기 때문입니다."
      },
      {
        "badge": "핵심 3",
        "title": "런아웃(Runout)과 스토리텔링",
        "text": "프리플랍부터 리버까지 내 액션과 보드 런아웃이 강한 핸드를 대표(Represent)하고 있어야 상대가 믿고 폴드합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커에서 가장 짜릿한 순간은 에어(Air) 핸드로 상대의 탑페어를 폴드시킬 때입니다. 하지만 아무 때나 치는 블러프는 칩을 태워버리는 화형식에 불과합니다.
      </div>

      <h2>1. 블러프 성공의 5대 기둥</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <h4>1. 레인지 어드밴티지</h4>
          <p>내 레인지에 넛이 존재하고, 상대 레인지는 캡(Capped)되어 있을 때 블러프 성공률이 가장 높습니다.</p>
        </div>
        <div class="feature-item">
          <h4>2. <span class="gto-term" data-term="blocker">블로커 효과</span></h4>
          <p>상대의 밸류콜 카드를 블락하고, 폴드할 핸드를 언블락하는 완벽한 카드를 골라야 합니다.</p>
        </div>
        <div class="feature-item">
          <h4>3. 사이징 레버리지</h4>
          <p>오버벳(125~150%)이나 올인은 상대의 원페어 블러프 캐처를 극한의 고통에 빠뜨립니다.</p>
        </div>
        <div class="feature-item">
          <h4>4. 상대의 플레이어 성향</h4>
          <p>상대가 절대로 탑페어를 못 접는 '콜링 스테이션'이라면 GTO 블러프도 멈춰야 합니다.</p>
        </div>
      </div>
    """
  },
  {
    "id": "the-art-of-bluff-catching-2",
    "slug": "the-art-of-bluff-catching-2",
    "title_ko": "블러프 캐칭(Bluff Catching)의 예술: 리버 콜의 수학",
    "title_en": "The Art of Bluff Catching",
    "level": "Level 3 (중급)",
    "category": "고급 이론",
    "read_time": "8분",
    "author": "GTO Wizard Theory Team",
    "original_url": "https://blog.gtowizard.com/the-art-of-bluff-catching-2/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "블러프 캐처의 정의",
        "text": "상대의 모든 밸류 베팅에는 무조건 지고, 상대의 순수 블러프에게만 이길 수 있는 마지널한 핸드를 뜻합니다."
      },
      {
        "badge": "핵심 2",
        "title": "상대 블러프 빈도 vs 팟 오즈",
        "text": "상대가 팟 100칩에 50칩을 베팅했을 때, 상대 레인지에 블러프가 25% 이상만 섞여 있다면 콜은 수학적 +EV입니다."
      },
      {
        "badge": "핵심 3",
        "title": "미스된 드로우를 언블락하라",
        "text": "플러시 드로우가 완성되지 않은 보드에서 내가 플러시 카드를 안 들고 있어야 상대가 그 꽝 핸드로 블러프를 쳤을 확률이 올라갑니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        리버에서 상대가 큰 벳을 날렸을 때, 내 손에 세컨페어나 서드페어가 있다면 이것은 전형적인 <strong>블러프 캐처(Bluff Catcher)</strong>입니다.
      </div>

      <h2>1. 블러프 캐칭의 유일한 질문</h2>
      <p>내가 세컨페어를 가졌든 에이스 하이를 가졌든 상관없습니다. 어차피 상대의 밸류 벳(탑페어 이상)에는 다 집니다.</p>
      <p>따라서 질문은 오직 하나입니다: <em>"상대가 이 라인에서 자신의 패를 블러프로 돌릴 확률이 나의 팟 오즈(Pot Odds)보다 높은가?"</em></p>
    """
  },
  {
    "id": "mdf-alpha",
    "slug": "mdf-alpha",
    "title_ko": "MDF와 Alpha: 방어와 공격의 수학적 균형",
    "title_en": "MDF & Alpha: The Foundations of Game Theory",
    "level": "Level 3 (중급)",
    "category": "수학/기초",
    "read_time": "9분",
    "author": "Tombos21",
    "original_url": "https://blog.gtowizard.com/mdf-alpha/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "MDF (최소 방어 빈도)",
        "text": "상대의 블러프가 자동 수익(Auto-profit)을 내지 못하도록 내가 최소한 방어해야 하는 레인지의 비율입니다."
      },
      {
        "badge": "핵심 2",
        "title": "Alpha (손익분기 블러프 성공률)",
        "text": "내 블러프가 즉각적으로 이득을 보기 위해 상대방이 폴드해야 하는 최소한의 빈도입니다."
      },
      {
        "badge": "핵심 3",
        "title": "MDF + Alpha = 100%",
        "text": "두 개념은 동전의 양면과 같습니다. 하프팟 벳에서 Alpha가 33.3%라면 MDF는 66.7%입니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        GTO의 핵심 수학 공식 중 가장 유명하면서도 가장 많이 오해되는 두 개념이 바로 <strong><span class="gto-term" data-term="mdf">MDF</span></strong>와 <strong><span class="gto-term" data-term="alpha">Alpha</span></strong>입니다.
      </div>

      <h2>1. MDF (Minimum Defense Frequency)</h2>
      <p>공식: <code>MDF = 팟 사이즈 / (팟 사이즈 + 베팅 금액)</code></p>
      <p>상대가 100칩 팟에 50칩을 베팅했을 때, MDF는 <code>100 / 150 = 66.7%</code>입니다. 내가 66.7% 이상 방어하지 않으면 상대는 쌩에어 핸드로도 무조건 돈을 복사하게 됩니다.</p>

      <h2>2. Alpha (손익분기점)</h2>
      <p>공식: <code>Alpha = 베팅 금액 / (팟 사이즈 + 베팅 금액)</code></p>
      <p>내가 100칩 팟에 50칩 블러프를 칠 때, 상대가 33.3% 이상 폴드해 준다면 내 블러프는 즉각적인 +EV입니다.</p>
    """
  },

  # ==================== LEVEL 4: SOLVER & EXPLOIT (4편) ====================
  {
    "id": "icm-basics",
    "slug": "icm-basics",
    "title_ko": "토너먼트의 심장, ICM 기초와 리스크 프리미엄",
    "title_en": "ICM Basics: Independent Chip Model",
    "level": "Level 4 (고급)",
    "category": "토너먼트",
    "read_time": "10분",
    "author": "GTO Wizard Tournament Specialists",
    "original_url": "https://blog.gtowizard.com/icm-basics/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "ChipEV ≠ $EV",
        "text": "캐시게임에서는 칩 1개가 곧 1원의 가치를 갖지만, 토너먼트에서는 상금 풀 구조 때문에 '칩 손실의 아픔'이 '칩 획득의 기쁨'보다 항상 더 큽니다."
      },
      {
        "badge": "핵심 2",
        "title": "리스크 프리미엄(Risk Premium)",
        "text": "ICM 압박 상황에서는 평소 50% 승률로 들어갈 수 있던 스팟도 60~65% 이상의 압도적 승률이 보장되어야만 콜할 수 있습니다."
      },
      {
        "badge": "핵심 3",
        "title": "빅스택의 횡포와 미들스택의 생존",
        "text": "숏스택이 탈락 대기 중일 때, 칩리더는 미들스택을 상대로 거의 100% 레인지로 올인 압박을 가할 수 있는 절대 권력을 쥡니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        캐시게임에서는 전설적인 플레이어가 토너먼트 파이널 테이블에만 오르면 어이없이 탈락하는 이유가 무엇일까요? 바로 <strong><span class="gto-term" data-term="icm">ICM (독립 칩 모델)</span></strong>의 역학을 무시하고 ChipEV로만 플레이하기 때문입니다.
      </div>

      <h2>1. 토너먼트 칩의 한계효용 체감</h2>
      <p>10명이 참가하여 1등 50%, 2등 30%, 3등 20%의 상금을 받는 토너먼트가 있습니다.</p>
      <p>내가 모든 칩(100,000칩)을 다 따서 1등을 해도 전체 상금의 <strong>50%</strong>만 가져갑니다. 즉, 칩이 늘어날수록 칩 1개당 실제 현금 가치는 줄어듭니다.</p>

      <h2>2. 리스크 프리미엄(Risk Premium)</h2>
      <p>머니인 버블이나 파이널 테이블에서 빅스택과 맞붙을 때, 당신이 칩을 잃으면 상금을 한 푼도 못 받고 탈락하지만, 이기더라도 상금이 2배가 되지 않습니다.</p>
      <p>이 손실 비대칭성을 메우기 위해 필요한 추가 승률을 <strong>리스크 프리미엄</strong>이라고 부릅니다.</p>
    """
  },
  {
    "id": "punish_the_unstudied_capped_ranges_and_bluffing_imbalances",
    "slug": "punish_the_unstudied_capped_ranges_and_bluffing_imbalances",
    "title_ko": "캡된(Capped) 레인지 응징하기: 상대의 릭(Leak)을 박살내는 법",
    "title_en": "Punish the Unstudied: Capped Ranges & Bluffing Imbalances",
    "level": "Level 4 (고급)",
    "category": "익스플로잇",
    "read_time": "9분",
    "author": "GTO Wizard Exploit Specialists",
    "original_url": "https://blog.gtowizard.com/punish_the_unstudied_capped_ranges_and_bluffing_imbalances/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "캡된(Capped) 레인지란?",
        "text": "특정 액션(체크나 플랍 콜)을 거치면서 레인지에서 최상위 너트 핸드(셋, 투페어, 오버페어)가 논리적으로 배제된 상태입니다."
      },
      {
        "badge": "핵심 2",
        "title": "오버벳(Overbet) 폭격",
        "text": "상대 레인지가 캡되어 있다는 확신이 서면, 턴이나 리버에서 125%~150%의 거대한 오버벳으로 상대의 마지널 핸드를 질식시킵니다."
      },
      {
        "badge": "핵심 3",
        "title": "인간의 불균형(Imbalance)",
        "text": "대부분의 인간 플레이어는 턴에서 체크하면 강한 패가 없습니다. 솔버는 이 릭을 발견했을 때 100% 빈도로 블러프를 날리라고 지시합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커에서 가장 돈을 많이 버는 익스플로잇(Exploit) 기회는 바로 상대방이 <strong>캡된(Capped) 레인지</strong>를 가졌을 때 발생합니다.
      </div>

      <h2>1. 레인지가 캡(Capped)된다는 것의 의미</h2>
      <p>플랍에서 상대방이 첵-레이스를 칠 수 있었는데도 그냥 <strong>체크-콜</strong>만 했다고 가정해 봅시다.</p>
      <p>보통 상대의 최고 너트(세트, 투페어)는 첵-레이스를 쳤을 것이므로, 상대의 콜 레인지에는 원페어나 중간 페어 같은 '미디엄 핸드'들만 압축(Condensed)되어 캡이 씌워집니다.</p>

      <h2>2. 응징의 기술: 기하학적 오버벳</h2>
      <p>상대방이 캡되어 있다면 당신은 리버에서 아무런 두려움 없이 <strong>팟의 150% 오버벳 올인</strong>을 날릴 수 있습니다. 상대는 기껏해야 원페어 블러프 캐처로 목숨을 걸어야 하기 때문에 대부분 눈물을 머금고 폴드하게 됩니다.</p>
    """
  },
  {
    "id": "adjusting-on-later-streets-after-exploiting-flop",
    "slug": "adjusting-on-later-streets-after-exploiting-flop",
    "title_ko": "플랍 익스플로잇 후 턴과 리버에서의 전략 조정",
    "title_en": "Adjusting on Later Streets After Exploiting Flop",
    "level": "Level 4 (고급)",
    "category": "익스플로잇",
    "read_time": "9분",
    "author": "GTO Wizard Strategy Team",
    "original_url": "https://blog.gtowizard.com/adjusting-on-later-streets-after-exploiting-flop/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "플랍 익스플로잇의 부작용",
        "text": "플랍에서 상대가 자주 폴드한다고 100% C-bet을 남발하면, 상대가 콜하고 들어온 턴에서는 상대 레인지가 상상 이상으로 강력해집니다."
      },
      {
        "badge": "핵심 2",
        "title": "턴에서의 급격한 브레이크",
        "text": "플랍에서 너무 넓은 레인지로 공격했다면, 턴에서는 무리한 블러프를 멈추고 첵백(Check-back)으로 레인지를 정돈해야 합니다."
      },
      {
        "badge": "핵심 3",
        "title": "선택적 리버 트리플 배럴",
        "text": "상대 콜러의 레인지가 극도로 타이트해진 리버에서는 완벽한 너트 블로커를 쥔 핸드로만 블러프를 제한해야 자폭을 피할 수 있습니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        많은 플레이어들이 플랍에서 상대의 릭을 보고 익스플로잇을 시도하다가, 턴과 리버에서 겉잡을 수 없이 스택을 털립니다. 왜일까요?
      </div>

      <h2>1. 상대 레인지의 급격한 정제 (Filtration)</h2>
      <p>플랍에서 당신이 가벼운 벳을 쳤을 때 상대가 콜을 했다면, 상대는 이미 쓰레기 패들을 다 버리고 <strong>상위 20~30%의 진짜 패들만 손에 쥐고 턴에 도착</strong>했습니다.</p>
      <p>그런데도 플랍에서의 기세를 몰아 턴에서 또 쌩블러프를 치는 것은, 이미 단단해진 바위에 계란을 던지는 것과 같습니다.</p>

      <h2>2. 노드 간의 연쇄 반응</h2>
      <p>플랍에서 레인지 외적인 익스플로잇을 감행했다면, 턴에서는 반대 방향으로 신중하게 전략을 조정(Counter-adjust)해야 전체 EV가 플러스로 유지됩니다.</p>
    """
  },
  {
    "id": "node-locking-exploit-guide",
    "slug": "node-locking-exploit-guide",
    "title_ko": "노드락(Node Locking) 실전 가이드: 솔버로 인간 플레이어 파훼하기",
    "title_en": "Node Locking: How to Exploit Humans Using Solvers",
    "level": "Level 4 (고급)",
    "category": "익스플로잇",
    "read_time": "10분",
    "author": "GTO Wizard Research Lab",
    "original_url": "https://blog.gtowizard.com/",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "GTO는 시작점일 뿐이다",
        "text": "GTO 솔루션은 양쪽 모두가 완벽한 신(God)처럼 플레이할 때의 내시 균형입니다. 인간은 결코 GTO대로 치지 않습니다."
      },
      {
        "badge": "핵심 2",
        "title": "노드락(Node Locking)이란?",
        "text": "솔버에서 특정 분기점(예: 상대가 C-bet에 80% 폴드함)을 강제로 고정한 뒤, 그 실수를 최대한 털어먹는 '최대 익스플로잇(Max Exploit)'을 계산하는 도구입니다."
      },
      {
        "badge": "핵심 3",
        "title": "진짜 고수가 돈을 버는 원리",
        "text": "GTO를 방패로 삼아 내 약점을 지키고, 상대의 실수를 노드락으로 간파하여 창으로 찌르는 것이 현대 포커의 최정상 메타입니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        <em>"상대가 GTO대로 안 치는데 왜 GTO를 공부해야 하죠?"</em> 이 질문에 대한 솔버 엔지니어들의 해답이 바로 <strong><span class="gto-term" data-term="nodelock">노드락(Node Locking)</span></strong>입니다.
      </div>

      <h2>1. 인간의 가장 흔한 3대 릭(Leak)</h2>
      <ul>
        <li><strong>오버폴딩 (Overfolding)</strong>: 턴/리버 큰 벳에 겁을 먹고 이론적 MDF보다 훨씬 많이 폴드함.</li>
        <li><strong>블러프 부족 (Underbluffing)</strong>: 리버 첵-레이스나 트리플 배럴 라인에서 블러프 빈도가 거의 0%에 수렴함.</li>
        <li><strong>콜링 스테이션 (Calling Station)</strong>: 탑페어나 플러시 드로우를 잡으면 상대 벳 크기와 상관없이 절대로 안 죽음.</li>
      </ul>

      <h2>2. 노드락의 실전 적용</h2>
      <p>상대가 리버 블러프를 전혀 안 친다면(Underbluffing), 솔버의 상대 블러프 노드를 0%로 잠급니다(Lock). 그러면 솔버는 놀랍게도 <strong>내 모든 블러프 캐처들을 100% 폴드</strong>하라는 전략을 도출해 냅니다!</p>
      <p>이것이 바로 솔버를 진정으로 마스터하여 필드를 파괴하는 비결입니다.</p>
    """
  }
]

# Write to data/articles.json
with open(os.path.join(BASE_DIR, 'data', 'articles.json'), 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(articles)} comprehensive articles in data/articles.json!")
