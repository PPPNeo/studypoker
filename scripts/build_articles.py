import json

articles = [
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
    "thumbnail": "https://blog.gtowizard.com/content/2026/04/expected-value.jpg",
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
    "level": "Level 1 (기초)",
    "category": "레인지 수학",
    "read_time": "6분",
    "author": "GTO Wizard Strategy Team",
    "original_url": "https://blog.gtowizard.com/equity-realization/",
    "thumbnail": "https://blog.gtowizard.com/content/2026/04/equity-realization.jpg",
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
    "id": "the-right-way-to-think-about-protection",
    "slug": "the-right-way-to-think-about-protection",
    "title_ko": "'프로텍션 벳'의 진실: 상대를 폴드시키는 진짜 이유",
    "title_en": "The Right Way To Think About Protection",
    "level": "Level 2 (초급)",
    "category": "플랍 전략",
    "read_time": "7분",
    "author": "Tombos21 (GTO Wizard Lead Theorist)",
    "original_url": "https://blog.gtowizard.com/the-right-way-to-think-about-protection/",
    "thumbnail": "https://blog.gtowizard.com/content/2026/03/protection-bet.jpg",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "공짜 에퀴티를 박탈하라",
        "text": "프로텍션의 본질은 '내 패를 보호하는 것'이 아니라 상대의 6아웃츠(25% 승률) 오버카드들이 공짜 턴 카드를 보는 것을 '디나이얼(Denial)'하는 것입니다."
      },
      {
        "badge": "핵심 2",
        "title": "폴드시키거나, 나쁜 가격을 강요하거나",
        "text": "상대가 폴드하면 팟을 즉시 회수해서 이득이고, 상대가 불리한 팟 오즈로 콜하면 밸류를 뜯어내서 이득입니다. 둘 다 윈-윈입니다."
      },
      {
        "badge": "핵심 3",
        "title": "드라이 보드 vs 웻 보드의 사이징",
        "text": "상대 에퀴티가 분산된 웻 보드일수록 큰 사이징(60%~75%)으로 프로텍션 베팅을 강하게 날려야 합니다."
      }
    ],
    "content_html": """
      <div class="article-lead">
        포커 펍에서 흔히 듣는 말: <em>"플랍에 드로우 깔려서 내 탑페어 보호(Protect)하려고 올인 박았어!"</em> 하지만 솔버는 프로텍션을 전혀 다른 관점으로 정의합니다.
      </div>

      <h2>1. 프로텍션은 독립된 베팅 카테고리가 아니다</h2>
      <p>포커의 베팅 목적은 전통적으로 2가지로 나뉩니다: <strong>밸류 베팅(더 안 좋은 패의 콜을 유도)</strong>과 <strong>블러프 베팅(더 좋은 패의 폴드를 유도)</strong>.</p>
      <p>그렇다면 '프로텍션 벳'은 무엇일까요? 프로텍션은 별개의 3번째 목적이 아니라, <strong>밸류 베팅에 수반되는 '에퀴티 디나이얼(Equity Denial)' 보너스 효과</strong>입니다.</p>

      <h2>2. 수학으로 보는 에퀴티 디나이얼</h2>
      <p>보드가 <strong>T♠ 8♦ 3♣</strong>이고, 당신이 <strong>J♠ J♥</strong>를 쥐고 있습니다. 팟은 100칩입니다.</p>
      <p>상대방이 <strong>A♥ K♦</strong>(오버카드 6아웃츠 = 약 25% 승률)를 쥐고 있다고 해봅시다. 만약 당신이 여기서 체크하면, 상대는 100칩 팟의 25%에 해당하는 <strong>25칩의 공짜 가치</strong>를 얻게 됩니다.</p>
      <ul>
        <li>당신이 50칩을 베팅하고 상대가 <strong>폴드</strong>하면? 👉 당신은 상대가 가질 뻔했던 25칩의 지분을 즉시 강탈(Denial)합니다.</li>
        <li>상대가 억지로 50칩을 <strong>콜</strong>하면? 👉 25% 승률 핸드가 33% 팟 오즈를 요구하는 벳을 콜했으므로, 매 콜마다 상대는 수학적 실수를 저지릅니다.</li>
      </ul>

      <h2>3. 웻 보드에서 작은 벳(1/3 팟)이 금기시되는 이유</h2>
      <p>드라이한 K-7-2 레인보우 보드에서는 상대의 에퀴티가 거의 없으므로 1/3 팟의 스몰 벳으로 충분합니다. 하지만 T-9-7 투수티드 같은 다이내믹 보드에서는 상대 레인지의 70%가 8아웃츠 이상의 강력한 드로우를 갖습니다.</p>
      <p>여기서 1/3 팟을 치는 것은 상대에게 공짜 점심을 떠먹여 주는 것과 같습니다. <strong>강력한 프로텍션과 밸류를 위해 66%~80%의 헤비한 벳 사이즈를 선택해야 합니다.</strong></p>
    """
  },
  {
    "id": "c-betting-ip-in-3-bet-pots",
    "slug": "c-betting-ip-in-3-bet-pots",
    "title_ko": "3벳 팟 인포지션(IP) C-bet 전략 완벽 가이드",
    "title_en": "C-Betting IP in 3-Bet Pots",
    "level": "Level 2 (중급)",
    "category": "3벳 팟",
    "read_time": "8분",
    "author": "GTO Wizard Coach Ivan",
    "original_url": "https://blog.gtowizard.com/c-betting-ip-in-3-bet-pots/",
    "thumbnail": "https://blog.gtowizard.com/content/2026/03/cbet-3bet-pots.jpg",
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

      <h2>1. 3벳 팟의 황금 열쇠: <span class="gto-term" data-term="spr">SPR (Stack-to-Pot Ratio)</span></h2>
      <p>100 BB 딥스택 기준으로, CO 오픈(2.5bb) ➔ BTN 3벳(7.5bb) ➔ CO 콜이 나오면 플랍 팟은 약 16.5 BB, 남은 스택은 92.5 BB가 됩니다. 이때 <strong>SPR은 약 5.6</strong>입니다.</p>
      <p>SRP에서의 SPR이 15 이상인 것과 비교하면 매우 낮습니다. 이것이 의미하는 바는 무엇일까요? <strong>'기하학적 팟 사이징' 2~3번이면 리버에 무조건 올인이 들어간다는 뜻</strong>입니다. 따라서 플랍에서 무리하게 큰 벳을 칠 필요가 전혀 없습니다.</p>

      <h2>2. 보드 텍스처별 C-bet 솔루션 비교</h2>
      <table class="poker-table-data">
        <thead>
          <tr>
            <th>보드 유형</th>
            <th>대표 예시</th>
            <th>권장 C-bet 빈도</th>
            <th>추천 사이징</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>A-High 드라이</strong></td>
            <td>A♠ 8♦ 2♣</td>
            <td><strong>85% ~ 95% (매우 높음)</strong></td>
            <td>25% ~ 33% 팟</td>
          </tr>
          <tr>
            <td><strong>브로드웨이 하이</strong></td>
            <td>K♦ Q♠ 4♣</td>
            <td><strong>70% ~ 80% (높음)</strong></td>
            <td>33% 팟</td>
          </tr>
          <tr>
            <td><strong>미들 커넥티드</strong></td>
            <td>8♠ 7♠ 5♦</td>
            <td><strong>25% ~ 35% (매우 낮음)</strong></td>
            <td>50% ~ 66% 팟</td>
          </tr>
          <tr>
            <td><strong>페어 보드</strong></td>
            <td>K♠ K♦ 6♣</td>
            <td><strong>65% ~ 75%</strong></td>
            <td>25% 팟</td>
          </tr>
        </tbody>
      </table>

      <h2>3. 33% 스몰 C-bet이 GTO의 표준인 이유</h2>
      <p>상대방(OOP)은 3벳 팟에서 프리플랍 콜러였기 때문에 포지션이 없고, 레인지에 AA, KK 같은 최상위 너트가 제한(Capped)되어 있습니다. 33%의 작은 베팅만으로도 상대의 99, TT, 미스된 브로드웨이 핸드들을 엄청난 곤경에 빠뜨릴 수 있습니다.</p>
    """
  },
  {
    "id": "understanding-blockers-in-poker",
    "slug": "understanding-blockers-in-poker",
    "title_ko": "블로커(Blockers) 완벽 마스터: 최상의 블러프와 콜",
    "title_en": "Understanding Blockers in Poker",
    "level": "Level 3 (중·고급)",
    "category": "고급 이론",
    "read_time": "9분",
    "author": "GTO Wizard Theory Team",
    "original_url": "https://blog.gtowizard.com/understanding-blockers-in-poker/",
    "thumbnail": "https://blog.gtowizard.com/content/2026/03/gto-wizard-understanding-blockers-in-poker-image-1.jpg",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "콤보 수학의 파괴력",
        "text": "내 손에 특정 카드 1장만 있어도, 상대가 가질 수 있는 투페어/셋 콤보는 50%, 포켓페어는 50%, 특정 수티드 콤보는 100% 차단됩니다."
      },
      {
        "badge": "핵심 2",
        "title": "리버 블러프의 황금 룰",
        "text": "상대의 '콜할 핸드(너트/탑페어)'는 블락하고, 상대의 '폴드할 핸드(미스된 드로우)'는 언블락하는 핸드가 신이 내린 블러프 핸드입니다."
      },
      {
        "badge": "핵심 3",
        "title": "블러프 캐칭(콜)의 역발상",
        "text": "상대 올인에 콜할 때는 상대의 블러프 카드(미스된 플러시 카드)를 내가 쥐고 있으면 안 됩니다! (그걸 쥐면 상대가 블러프를 못 칩니다)"
      }
    ],
    "content_html": """
      <div class="article-lead">
        리버에서 팟은 100BB, 상대가 올인을 박았습니다. 내 손에는 마지널한 페어가 있습니다. <em>"콜해야 할까, 폴드해야 할까?"</em> 이 극한의 순간 승패를 가르는 0.1%의 디테일이 바로 <strong><span class="gto-term" data-term="blocker">블로커(Blocker)</span></strong>와 <strong><span class="gto-term" data-term="unblocker">언블로커(Unblocker)</span></strong>입니다.
      </div>

      <h2>1. 블로커란 무엇인가? 콤보의 물리적 차단</h2>
      <p>포커 덱에는 52장의 카드만 존재합니다. 내가 특정 카드를 손에 쥐는 순간, 상대가 그 카드를 가지고 있을 확률은 0이 됩니다.</p>
      <ul>
        <li><strong>미페어 핸드 (예: AK)</strong>: 보드에 A나 K가 없을 때 16가지 조합이 존재합니다. 하지만 내가 A 한 장을 들고 있으면 상대의 AK 콤보는 <strong>8가지로 50% 급감</strong>합니다.</li>
        <li><strong>포켓페어 (예: AA)</strong>: 원래 6가지 조합이지만, 내가 A 한 장을 쥐면 <strong>3가지로 50% 감소</strong>합니다.</li>
      </ul>

      <h2>2. 예술적인 리버 블러프 핸드 고르기</h2>
      <p>보드가 <strong>K♠ J♦ 9♣ 4♥ 2♦</strong>로 끝났습니다. 당신은 쇼다운 밸류가 없는 꽝 핸드로 올인 블러프를 시도하려 합니다. 다음 두 핸드 중 솔버는 무엇을 100% 블러프로 선택할까요?</p>
      <ol>
        <li>핸드 A: <strong>A♠ Q♣</strong> (Q로 T 스트레이트를 블락, A로 투페어/AK 블락)</li>
        <li>핸드 B: <strong>6♠ 5♠</strong> (아무것도 블락하지 못하는 쌩에어)</li>
      </ol>
      <p>정답은 압도적으로 <strong>A♠ Q♣</strong>입니다! AQ을 쥐고 있으면 상대가 콜할 수 있는 최강 핸드(QT 스트레이트, AK, KQ)의 조합 수가 대폭 줄어들어 상대의 폴드 확률이 수학적으로 급상승합니다.</p>

      <h2>3. 블러프 캐칭: 언블로커의 역학</h2>
      <div class="callout-card warning">
        <h4>⚠️ 초보자들이 가장 많이 저지르는 블러프 캐치 실수</h4>
        <p>플러시 드로우가 말라붙은 리버에서, <strong>"내가 플러시 무늬 카드를 쥐고 있으니까 콜해야지!"</strong>라고 생각하시나요? 정반대입니다!</p>
        <p>당신이 그 무늬를 쥐고 있다면, 상대방이 플러시를 노리다 미스해서 블러프를 치고 있을 확률을 당신 스스로 지워버린 것입니다. 블러프 캐치를 할 때는 상대의 블러프 콤보를 <strong>언블락(Unblock)</strong>하고 있어야 안전합니다.</p>
      </div>
    """
  },
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
    "thumbnail": "https://blog.gtowizard.com/content/2026/04/icm-basics.jpg",
    "summary_cards": [
      {
        "badge": "핵심 1",
        "title": "ChipEV ≠ $EV",
        "text": "캐시게임에서는 칩 1개가 곧 1원의 가치를 갖지만, 토너먼트에서는 상금 풀 구조 때문에 '칩을 잃을 때의 손실'이 '칩을 딸 때의 이득'보다 항상 더 큽니다."
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

      <h2>1. 토너먼트 칩의 '한계효용 체감의 법칙'</h2>
      <p>10명이 참가하여 1등 50%, 2등 30%, 3등 20%의 상금을 받는 토너먼트가 있습니다. 각자 10,000칩을 갖고 시작합니다.</p>
      <ul>
        <li>시작 시점: 10,000칩의 가치 = 전체 상금의 10%</li>
        <li>내가 모든 칩(100,000칩)을 다 따서 1등을 하면? = 전체 상금의 <strong>50%</strong>만 가져갑니다!</li>
      </ul>
      <p>칩은 10배로 늘어났는데 상금은 5배밖에 못 받습니다. 즉, <strong>'내가 새롭게 얻는 칩의 가치는 내가 이미 가지고 있는 칩의 가치보다 항상 작다'</strong>는 냉혹한 진실이 성립합니다.</p>

      <h2>2. 리스크 프리미엄(Risk Premium)이란?</h2>
      <p>머니인 버블이나 파이널 테이블에서 빅스택과 맞붙을 때, 당신이 칩을 잃으면 상금을 한 푼도 못 받고 탈락(0원)하지만, 이기더라도 상금이 2배가 되지 않습니다.</p>
      <p>이 손실 비대칭성을 메우기 위해 필요한 추가 승률을 <strong>리스크 프리미엄</strong>이라고 부릅니다. 상황에 따라 평소 필요 승률(예: 35%)에 15~25%의 리스크 프리미엄이 붙어 <strong>최소 55% 이상의 승률</strong>이 없으면 올인 콜을 할 수 없게 됩니다.</p>

      <h2>3. 파이널 테이블 전략의 정석: 누구를 공격할 것인가?</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <h4>👑 칩리더 (Big Stack)</h4>
          <p>탈락 위험이 전혀 없으므로 미들스택들의 숨통을 조이는 광기 어린 어그레션을 행사합니다.</p>
        </div>
        <div class="feature-item">
          <h4>😰 미들스택 (Middle Stack)</h4>
          <p>가장 고통받는 포지션입니다. 뒤에 있는 숏스택이 먼저 죽어주면 상금이 오르므로, 빅스택의 레이스에 극도로 타이트하게 오버폴드해야 합니다.</p>
        </div>
        <div class="feature-item">
          <h4>⚡ 숏스택 (Short Stack)</h4>
          <p>어차피 블라인드에 말라 죽기 직전이므로, 리스크 프리미엄이 거의 0에 수렴하여 수학적 칩EV대로 시원하게 올인 셔브를 감행해야 합니다.</p>
        </div>
      </div>
    """
  }
]

with open("data/articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("Successfully written valid data/articles.json! Total articles:", len(articles))
