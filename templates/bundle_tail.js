// Global Auth Manager reference
var authManager;

// Theme Manager
const themeManager = {
  theme: localStorage.getItem('studypoker_theme') || 'light',

  init() {
    this.apply(this.theme);
  },

  toggle() {
    this.theme = (this.theme === 'dark') ? 'light' : 'dark';
    this.apply(this.theme);
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  apply(t) {
    this.theme = t;
    if (t === 'light') {
      document.body.classList.add('theme-light');
    } else {
      document.body.classList.remove('theme-light');
    }
    localStorage.setItem('studypoker_theme', t);

    const icon = document.getElementById('theme-icon');
    const text = document.getElementById('theme-text');
    if (icon && text) {
      if (t === 'light') {
        icon.innerText = '🌙';
        text.innerText = '다크 모드';
      } else {
        icon.innerText = '☀️';
        text.innerText = '라이트 모드';
      }
    }
  }
};

// Storage with one-time fair-play patch migration (Global 0 XP reset for this update)
const FAIR_PLAY_PATCH_VERSION = 'v2026_fair_play_reset_v1';

const storage = {
  get() {
    const patchApplied = localStorage.getItem('studypoker_patch_version');
    const saved = localStorage.getItem('studypoker_user');
    
    // One-time global XP reset for this update
    if (patchApplied !== FAIR_PLAY_PATCH_VERSION) {
      localStorage.setItem('studypoker_patch_version', FAIR_PLAY_PATCH_VERSION);
      let preservedName = '포커신동';
      let preservedAvatar = '🦈';
      let preservedStyle = 'TAG';
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          if (parsed.name) preservedName = parsed.name;
          if (parsed.avatar) preservedAvatar = parsed.avatar;
          if (parsed.playstyle) preservedStyle = parsed.playstyle;
        } catch(e) {}
      }
      const resetState = {
        name: preservedName,
        avatar: preservedAvatar,
        playstyle: preservedStyle,
        xp: 0,
        level: 1,
        streak: 1,
        stats: { theory: 0, decision: 0, ranges: 0, mental: 0 },
        completed_articles: [],
        completed_quizzes: [],
        explored_ranges: [],
        promotions_passed: [],
        ai_queries_count: 0
      };
      this.save(resetState);
      setTimeout(() => {
        if (window.characterManager && characterManager.showToast) {
          characterManager.showToast('🛡️ 공정 밸런스 패치 적용: 퀴즈/레인지 무한 파밍 방지 및 모든 유저 0 XP 초기화가 완료되었습니다.');
        }
      }, 1000);
      return resetState;
    }

    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (!parsed.name) parsed.name = '포커신동';
        if (!parsed.avatar) parsed.avatar = '🦈';
        if (!parsed.playstyle) parsed.playstyle = 'TAG';
        if (!parsed.stats) parsed.stats = { theory: 0, decision: 0, ranges: 0, mental: 0 };
        if (parsed.xp === undefined) parsed.xp = 0;
        if (!parsed.completed_articles) parsed.completed_articles = [];
        if (!parsed.completed_quizzes) parsed.completed_quizzes = [];
        if (!parsed.explored_ranges) parsed.explored_ranges = [];
        if (!parsed.promotions_passed) parsed.promotions_passed = [];
        if (parsed.ai_queries_count === undefined) parsed.ai_queries_count = 0;
        return parsed;
      } catch(e) {}
    }
    return {
      name: '포커신동',
      avatar: '🦈',
      playstyle: 'TAG',
      xp: 0,
      level: 1,
      streak: 1,
      stats: {
        theory: 0,
        decision: 0,
        ranges: 0,
        mental: 0
      },
      completed_articles: [],
      completed_quizzes: [],
      explored_ranges: [],
      promotions_passed: [],
      ai_queries_count: 0
    };
  },
  save(state) {
    localStorage.setItem('studypoker_user', JSON.stringify(state));
    if (window.authManager && authManager.isLoggedIn && authManager.isLoggedIn()) {
      authManager.syncToCloud();
    }
  }
};

// 🌟 6개 전직 구간 시스템 (Lv.1 ~ Lv.100)
const PROMOTION_TIERS = [
  {
    tier: 0,
    targetLevel: 0,
    name: "동네 피쉬",
    title: "동네 피쉬 🐟",
    badge: "🐣 동네 피쉬",
    icon: "🐟",
    desc: "기본 족보와 팟오즈를 배우는 포커 입문 단계",
    color: "#94a3b8",
    badgeClass: "rank-badge-0",
    reqArticles: 3,
    reqQuizzes: 3,
    bonusXP: 0
  },
  {
    tier: 1,
    targetLevel: 10,
    name: "홀덤펍 레귤러",
    title: "홀덤펍 레귤러 ⚔️",
    badge: "⚔️ 펍 레귤러",
    icon: "⚔️",
    desc: "포지션과 프리플랍 레인지의 힘을 깨달은 로컬 강자",
    examTitle: "1차 전직 심사: 프리플랍 포지션 & 팟오즈 기초",
    color: "#34d399",
    badgeClass: "rank-badge-1",
    reqArticles: 8,
    reqQuizzes: 8,
    bonusXP: 500
  },
  {
    tier: 2,
    targetLevel: 25,
    name: "마이크로 그라인더",
    title: "마이크로 그라인더 ⚙️",
    badge: "⚙️ 마이크로 그라인더",
    icon: "⚙️",
    desc: "플랍 텍스처와 C-bet 빈도를 솔버 기반으로 다루는 그라인더",
    examTitle: "2차 전직 심사: 플랍 C-bet & 보드 텍스처 분석",
    color: "#60a5fa",
    badgeClass: "rank-badge-2",
    reqArticles: 20,
    reqQuizzes: 15,
    bonusXP: 1000
  },
  {
    tier: 3,
    targetLevel: 45,
    name: "로우스테이크 크러셔",
    title: "로우스테이크 크러셔 🔥",
    badge: "🔥 로우스테이크 크러셔",
    icon: "🔥",
    desc: "턴 더블배럴과 MDF 방어선으로 상대를 압살하는 크러셔",
    examTitle: "3차 전직 심사: 턴 배럴링 & MDF 수학 공식",
    color: "#f87171",
    badgeClass: "rank-badge-3",
    reqArticles: 45,
    reqQuizzes: 20,
    bonusXP: 1500
  },
  {
    tier: 4,
    targetLevel: 65,
    name: "미드스테이크 프로",
    title: "미드스테이크 프로 🦊",
    badge: "🦊 미드스테이크 프로",
    icon: "🦊",
    desc: "블로커/언블로커 콤보와 리버 블러프 캐칭의 고수",
    examTitle: "4차 전직 심사: 블로커 콤보 & 리버 블러프 캐치",
    color: "#a78bfa",
    badgeClass: "rank-badge-4",
    reqArticles: 75,
    reqQuizzes: 25,
    bonusXP: 2000
  },
  {
    tier: 5,
    targetLevel: 85,
    name: "하이롤러 위저드",
    title: "하이롤러 위저드 🦁",
    badge: "🦁 하이롤러 위저드",
    icon: "🦁",
    desc: "지오메트릭 사이징과 폴라라이즈드 레인지를 자유자재로 구사",
    examTitle: "5차 전직 심사: 지오메트릭 사이징 & 믹스드 솔루션",
    color: "#fbbf24",
    badgeClass: "rank-badge-5",
    reqArticles: 110,
    reqQuizzes: 25,
    bonusXP: 3000
  },
  {
    tier: 6,
    targetLevel: 100,
    name: "WSOP 레전드 챔피언",
    title: "WSOP 레전드 챔피언 👑",
    badge: "👑 WSOP 레전드 챔피언",
    icon: "👑",
    desc: "ICM 토너먼트의 극한과 헤즈업 GTO를 완성한 불멸의 챔피언",
    examTitle: "최종 6차 승급 심사: 극강의 ICM 토너먼트 & WSOP 파이널",
    color: "#fef08a",
    badgeClass: "rank-badge-6",
    reqArticles: 150,
    reqQuizzes: 25,
    bonusXP: 5000
  }
];

// 1~100 레벨 경험치 공식 (Lv.1: 0 XP, Lv.10: 2,308 XP, Lv.25: 9,600 XP, Lv.45: 23,800 XP, Lv.65: 42,600 XP, Lv.85: 65,500 XP, Lv.100: 85,200 XP)
function getLevelThreshold(lvl) {
  if (lvl <= 1) return 0;
  return Math.floor(68 * Math.pow(lvl, 1.55));
}

// 레거시 호환용 LEVEL_TIERS 매핑
const LEVEL_TIERS = PROMOTION_TIERS.map(pt => ({
  level: pt.tier === 0 ? 1 : pt.targetLevel,
  title: pt.title,
  badge: pt.badge,
  minXp: getLevelThreshold(pt.tier === 0 ? 1 : pt.targetLevel),
  maxXp: getLevelThreshold(pt.tier === 6 ? 100 : PROMOTION_TIERS[pt.tier + 1].targetLevel),
  tierName: pt.name
}));

const PLAYSTYLES = {
  TAG: { title: "⚡ TAG (타이트 어그레시브)", tag: "TAG", bio: "엄선된 프리미엄 핸드로 강력하게 주도권을 잡는 정석적인 승리 공식" },
  LAG: { title: "🔥 LAG (루즈 어그레시브)", tag: "LAG", bio: "넓은 레인지와 포스트플랍 공격성으로 상대에게 끊임없는 압박 부여" },
  GTO: { title: "🧠 GTO Solved (솔버 밸런스)", tag: "GTO", bio: "수학적 균형과 빈도 밸런싱으로 상대의 익스플로잇을 완벽 차단" },
  EXPLOIT: { title: "🎯 Exploitative (익스플로잇)", tag: "익스플로잇", bio: "상대의 성향적 약점과 릭(Leak)을 파악하여 최대 EV를 추출" },
  HUNTER: { title: "🦈 Fish Hunter (피쉬 헌터)", tag: "피쉬헌터", bio: "불필요한 블러프를 배제하고 탄탄한 밸류 벳으로 스택을 빨아들이는 스타일" }
};

// RPG Character Manager
const characterManager = {
  selectedAvatar: '🦈',
  selectedStyle: 'TAG',
  _toastTimer: null,

  init() {
    const u = app.userState;
    this.selectedAvatar = u.avatar || '🦈';
    this.selectedStyle = u.playstyle || 'TAG';
    this.renderHeader();
    this.renderDashboard();

    // If new user visiting for the first time and logged in, auto-open character setup popup!
    const hasConfigured = localStorage.getItem('studypoker_char_created');
    if (!hasConfigured && window.authManager && authManager.isLoggedIn()) {
      setTimeout(() => {
        this.openModal(true); // isFirstTime = true
      }, 400);
    }
  },

  openModal(isFirstTime = false) {
    const u = app.userState;
    this.selectedAvatar = u.avatar || '🦈';
    this.selectedStyle = u.playstyle || 'TAG';

    const nameInput = document.getElementById('char-name-input');
    if (nameInput) nameInput.value = u.name || '포커신동';

    const titleEl = document.getElementById('char-modal-title');
    const subEl = document.getElementById('char-modal-subtitle');
    const saveBtn = document.getElementById('btn-save-character');

    if (isFirstTime) {
      if (titleEl) titleEl.innerText = '🃏 폴푸아의 GTO Playbook에 오신 것을 환영합니다!';
      if (subEl) subEl.innerText = '나만의 포커 페르소나 캐릭터를 설정하고 Lv.1 피쉬 탈출기부터 시작하세요!';
      if (saveBtn) saveBtn.innerText = '🚀 캐릭터 생성 완료하고 모험 시작하기';
    } else {
      if (titleEl) titleEl.innerText = '🎭 포커 페르소나 캐릭터 커스텀';
      if (subEl) subEl.innerText = '플레이 스타일과 닉네임, 아바타를 언제든 변경할 수 있습니다.';
      if (saveBtn) saveBtn.innerText = '✨ 캐릭터 설정 저장';
    }

    this.updateModalSelections();
    const modal = document.getElementById('char-modal-overlay');
    if (modal) modal.style.display = 'flex';
  },

  closeModal() {
    const modal = document.getElementById('char-modal-overlay');
    if (modal) modal.style.display = 'none';
  },

  toggleStats() {
    const panel = document.getElementById('char-stats-panel');
    const arrow = document.getElementById('stats-toggle-arrow');
    const btn = document.getElementById('btn-toggle-stats');
    if (!panel) return;
    const isHidden = (panel.style.display === 'none' || getComputedStyle(panel).display === 'none');
    if (isHidden) {
      panel.style.display = 'block';
      if (arrow) arrow.innerText = '▲';
      if (btn) btn.classList.add('active');
    } else {
      panel.style.display = 'none';
      if (arrow) arrow.innerText = '▼';
      if (btn) btn.classList.remove('active');
    }
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  resetCharacter() {
    const ok = confirm("⚠️ 캐릭터 초기화 확인\n\n정말로 모든 학습 기록(경험치, 레벨, 완독 아티클, 퀴즈 기록, 4대 능력치)을 초기화하시겠습니까?\n\n초기화 시 0 XP (Lv.1 동네 피쉬)로 완전히 새로 시작합니다.");
    if (!ok) return;

    localStorage.removeItem('studypoker_user');
    localStorage.removeItem('studypoker_char_created');

    app.userState = {
      name: '포커신동',
      avatar: '🦈',
      playstyle: 'TAG',
      xp: 0,
      level: 1,
      streak: 1,
      stats: {
        theory: 0,
        decision: 0,
        ranges: 0,
        mental: 0
      },
      completed_articles: [],
      completed_quizzes: [],
      explored_ranges: []
    };
    storage.save(app.userState);

    this.selectedAvatar = '🦈';
    this.selectedStyle = 'TAG';

    this.closeModal();
    app.updateUserBar();
    this.renderHeader();
    this.renderDashboard();
    if (window.roadmap && roadmap.load) roadmap.load();
    if (window.reader && reader.renderArticleCards) reader.renderArticleCards();
    if (window.trainer && trainer.renderCurrentQuiz) trainer.renderCurrentQuiz();

    this.showToast("🔄 모든 학습 데이터가 0 XP(초기 상태)로 깨끗하게 초기화되었습니다.");
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');

    setTimeout(() => {
      this.openModal(true);
    }, 500);
  },

  selectAvatar(emoji) {
    this.selectedAvatar = emoji;
    this.updateModalSelections();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  selectStyle(styleKey) {
    this.selectedStyle = styleKey;
    this.updateModalSelections();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  setName(name) {
    const nameInput = document.getElementById('char-name-input');
    if (nameInput) {
      nameInput.value = name;
      nameInput.focus();
    }
  },

  randomizeName() {
    const names = [
      '강남샤크', 'GTO마법사', '체크레이즈달인', '리버원샷', '필아이비후계자',
      '폴푸아수제자', '마카오크러셔', '넛츠빌런', '블라인드도둑', '팟스틸러',
      '하이롤러지망생', '솔버장인', '에퀴티괴물'
    ];
    const pick = names[Math.floor(Math.random() * names.length)];
    this.setName(pick);
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  updateModalSelections() {
    document.querySelectorAll('#avatar-picker-grid .avatar-option').forEach(el => {
      if (el.dataset.avatar === this.selectedAvatar) el.classList.add('active');
      else el.classList.remove('active');
    });
    document.querySelectorAll('#style-picker-grid .style-card').forEach(el => {
      if (el.dataset.style === this.selectedStyle) el.classList.add('active');
      else el.classList.remove('active');
    });
  },

  
  showLevelLockModal(item) {
    const u = app.userState;
    const userLvl = app.getLevelInfo(u.xp).level;
    const reqLvl = item.required_level || 1;
    const reqInfo = LEVEL_TIERS[reqLvl - 1] || LEVEL_TIERS[0];
    const userLvlInfo = app.getLevelInfo(u.xp);
    const xpNeeded = Math.max(0, reqInfo.minXp - u.xp);

    const contentEl = document.getElementById('lock-modal-content');
    if (!contentEl) return;

    contentEl.innerHTML = `
      <div class="lock-detail-box">
        <div>
          <span style="font-size: 0.8rem; color: #f59e0b; font-weight: 800; display: block; margin-bottom: 2px;">
            🔒 [${reqInfo.title}] 이상 열람 가능
          </span>
          <h4 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-bottom: 4px;">
            ${item.title_ko || item.name || item.title || '고급 전략 콘텐츠'}
          </h4>
          <span style="font-size: 0.78rem; color: var(--text-dim);">${item.category || item.level || '심화 포커 이론'}</span>
        </div>

        <div class="lock-tier-row">
          <div>
            <span style="font-size: 0.75rem; color: var(--text-dim); display: block;">현재 내 캐릭터</span>
            <strong style="color: var(--text-main); font-size: 0.92rem;">${userLvlInfo.title} (${u.xp} XP)</strong>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 0.75rem; color: var(--text-dim); display: block;">해금 필요 레벨</span>
            <strong style="color: #f59e0b; font-size: 0.92rem;">${reqInfo.title} (${reqInfo.minXp} XP)</strong>
          </div>
        </div>

        <div style="background: rgba(245, 158, 11, 0.1); border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.82rem; color: #f59e0b; font-weight: 700;">
          ⚡ 앞으로 <strong>${xpNeeded} XP</strong>를 더 획득하면 즉시 해금됩니다!
        </div>

        <div class="lock-tip-quote">
          💡 <strong>프로 코치의 조언:</strong><br>
          기대값(EV), 팟 오즈, 에퀴티 실현 같은 기초 원리가 체화되지 않은 상태에서 턴/리버 오버벳이나 4벳 같은 고급 과정을 먼저 공부하면 실전에서 심각한 릭(Leak)이 발생합니다. 현재 해금된 기초 아티클과 스팟 퀴즈를 먼저 마스터하세요!
        </div>
      </div>
    `;

    const modal = document.getElementById('level-lock-modal-overlay');
    if (modal) modal.style.display = 'flex';
    if (window.app && app.playAudioEffect) app.playAudioEffect('wrong');
  },

  closeLevelLockModal() {
    const modal = document.getElementById('level-lock-modal-overlay');
    if (modal) modal.style.display = 'none';
  },

  handleLockAction() {
    this.closeLevelLockModal();
    reader.toggleUnlockedOnly(true);
    app.navigate('articles');
  },

  saveCharacter() {
    const nameInput = document.getElementById('char-name-input');
    const newName = (nameInput && nameInput.value.trim()) ? nameInput.value.trim() : '포커신동';

    const isFirstTime = !localStorage.getItem('studypoker_char_created');

    app.userState.name = newName;
    app.userState.avatar = this.selectedAvatar;
    app.userState.playstyle = this.selectedStyle;

    if (isFirstTime) {
      app.userState.xp = 0;
      app.userState.level = 1;
      app.userState.streak = 1;
      app.userState.stats = { theory: 0, decision: 0, ranges: 0, mental: 0 };
      app.userState.completed_articles = [];
      app.userState.completed_quizzes = [];
      app.userState.explored_ranges = [];
    }

    localStorage.setItem('studypoker_char_created', 'true');
    storage.save(app.userState);
    app.updateUserBar();
    this.renderHeader();
    this.renderDashboard();
    this.closeModal();

    if (window.app && app.playAudioEffect) app.playAudioEffect('correct');
    this.showToast(`🎉 <strong>[${newName}]</strong> 님, 환영합니다! 0 XP에서 시작하여 Lv.1 피쉬 탈출 퀘스트를 완수해보세요!`);
  },

  renderHeader() {
    const u = app.userState;
    const av = document.getElementById('header-char-avatar');
    const nm = document.getElementById('header-char-name');
    const st = document.getElementById('header-char-style');
    if (av) av.innerText = u.avatar || '🦈';
    if (nm) nm.innerText = u.name || '포커신동';
    if (st) st.innerText = u.playstyle || 'TAG';
  },

  renderDashboard() {
    const u = app.userState;
    const lvlInfo = app.getLevelInfo(u.xp);

    const dAv = document.getElementById('dash-char-avatar');
    const dNm = document.getElementById('dash-char-name');
    const dSt = document.getElementById('dash-char-style');
    const dTr = document.getElementById('dash-char-tier');
    const dBio = document.getElementById('dash-char-bio');
    const dXpText = document.getElementById('dash-xp-text');
    const dXpNeed = document.getElementById('dash-xp-needed');
    const dXpFill = document.getElementById('dash-xp-fill');

    if (dAv) dAv.innerText = u.avatar || '🦈';
    if (dNm) dNm.innerText = u.name || '포커신동';

    const dKakao = document.getElementById('dash-kakao-tag');
    if (dKakao) {
      if (u.kakao_name) {
        dKakao.innerText = `💬 카톡: ${u.kakao_name}`;
        dKakao.style.display = 'inline-flex';
      } else {
        dKakao.innerText = `💬 카톡: 미연동`;
      }
    }

    const dAuthBtn = document.getElementById('dash-auth-btn');
    if (dAuthBtn && window.authManager) {
      const isAuth = authManager.isLoggedIn();
      dAuthBtn.innerHTML = isAuth ? '<span>⚙️</span> 내 계정' : '<span>👤</span> 회원가입/로그인';
    }
    
    const styleInfo = PLAYSTYLES[u.playstyle] || PLAYSTYLES.TAG;
    if (dSt) dSt.innerText = styleInfo.title;
    if (dTr) dTr.innerText = lvlInfo.title;
    if (dBio) dBio.innerText = `"${styleInfo.bio}"`;

    if (dXpText) dXpText.innerText = `${u.xp} / ${lvlInfo.maxXp} XP`;
    if (dXpNeed) {
      if (lvlInfo.remainingXp > 0) {
        dXpNeed.innerText = `다음 승급까지 ${lvlInfo.remainingXp} XP 남음`;
      } else {
        dXpNeed.innerText = `최고 레벨 WSOP 챔피언 등극! 👑`;
      }
    }
    if (dXpFill) dXpFill.style.width = `${lvlInfo.progressPct}%`;

    // 4 Core RPG Stats
    const stats = u.stats || { theory: 0, decision: 0, ranges: 0, mental: 0 };
    this.updateStatCard('theory', stats.theory);
    this.updateStatCard('decision', stats.decision);
    this.updateStatCard('ranges', stats.ranges);
    this.updateStatCard('mental', stats.mental);

    // Promotion Alert Banner Update
    const promoBanner = document.getElementById('promotion-alert-banner');
    if (promoBanner) {
      if (lvlInfo.needsExam) {
        promoBanner.style.display = 'flex';
        const pTitle = document.getElementById('promo-banner-title');
        const pDesc = document.getElementById('promo-banner-desc');
        const tier = PROMOTION_TIERS[lvlInfo.needsExam];
        if (pTitle) pTitle.innerText = `⚡ ${tier.examTitle} 응시 가능!`;
        if (pDesc) pDesc.innerText = `Lv.${tier.targetLevel} 달성! 5문제 중 4문제 이상 정답 시 [${tier.name}] 칭호 및 +${tier.bonusXP} XP 획득!`;
      } else {
        promoBanner.style.display = 'none';
      }
    }
  },

  updateStatCard(statKey, score) {
    const clamped = Math.min(100, Math.max(0, score || 0));
    const grade = this.calcGrade(clamped);

    const gradeEl = document.getElementById(`stat-grade-${statKey}`);
    const barEl = document.getElementById(`stat-bar-${statKey}`);
    const valEl = document.getElementById(`stat-val-${statKey}`);

    if (gradeEl) {
      gradeEl.innerText = grade;
      gradeEl.className = `stat-grade grade-${grade}`;
    }
    if (barEl) barEl.style.width = `${clamped}%`;
    if (valEl) valEl.innerText = clamped;
  },

  calcGrade(score) {
    if (score >= 90) return 'SS';
    if (score >= 80) return 'S';
    if (score >= 70) return 'A';
    if (score >= 50) return 'B';
    if (score >= 30) return 'C';
    return 'D';
  },

  showToast(msg) {
    let toast = document.getElementById('poker-live-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'poker-live-toast';
      toast.className = 'poker-toast';
      document.body.appendChild(toast);
    }
    toast.innerHTML = msg;
    toast.style.display = 'flex';
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => {
      if (toast) toast.style.display = 'none';
    }, 3800);
  }
};

const app = {
  userState: storage.get(),
  currentView: 'roadmap',

  init() {
    window.authManager = authManager;
    authManager.init();

    // 🔒 비로그인 상태일 때는 절대 게임 및 프로필을 초기화/표시하지 않음
    if (!authManager.isLoggedIn()) {
      return;
    }

    this.startAuthenticatedApp();
  },

  startAuthenticatedApp() {
    this.userState = storage.get();
    themeManager.init();
    characterManager.init();
    this.updateUserBar();
    roadmap.load();
    reader.loadArticles();
    matrix.init();
    glossary.load();
    if (window.rankingManager && rankingManager.fetchCloudPlayers) {
      rankingManager.fetchCloudPlayers();
    }

    const hash = window.location.hash.replace('#', '');
    if (hash && ['articles', 'trainer', 'matrix', 'roadmap', 'glossary', 'ranking'].includes(hash)) {
      this.navigate(hash);
    } else {
      this.navigate('roadmap');
    }
  },

  navigate(viewId) {
    if (window.authManager && !authManager.isLoggedIn()) {
      authManager.showGate('login');
      return;
    }
    if (viewId !== 'reader' && window.reader && reader.readTimer) {
      clearInterval(reader.readTimer);
      reader.readTimer = null;
      reader.secondsRemaining = 45;
    }

    this.currentView = viewId;
    window.location.hash = viewId;

    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.remove('active');
    });

    const targetSection = document.getElementById(`view-${viewId}`);
    if (targetSection) {
      targetSection.classList.add('active');
    }

    document.querySelectorAll('.nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    if (viewId === 'trainer') {
      trainer.init();
    } else if (viewId === 'roadmap') {
      roadmap.load();
    } else if (viewId === 'glossary') {
      glossary.load();
    } else if (viewId === 'ranking') {
      if (window.rankingManager) {
        if (rankingManager.fetchCloudPlayers) rankingManager.fetchCloudPlayers();
        rankingManager.render();
      }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },


  // 📚 레벨별 지정 필수 학습 커리큘럼 (아티클 & 퀴즈 순차 지정)
  getCurriculumForLevel(lvl) {
    lvl = Math.max(1, Math.min(100, parseInt(lvl, 10) || 1));
    const allArticles = (window.DB && DB.articles) ? DB.articles : [];
    const allQuizzes = (window.DB && DB.quizzes) ? DB.quizzes : [];

    // Lv.1 ~ Lv.9: 기초 입문 구간 정밀 큐레이션 트랙
    const curatedTracks = {
      1: {
        articleIds: ['what-is-expected-value-in-poker', 'equity-realization', 'common_poker_sayings_that_ruin_your_winrate'],
        quizIds: ['quiz-16', 'quiz-17'],
        title: '포커 기초 수학: 기대값(EV) & 에퀴티 실현의 정석'
      },
      2: {
        articleIds: ['what-are-pot-odds-in-poker', 'the-trouble-with-implied-odds', 'what-is-equity-in-poker'],
        quizIds: ['quiz-20', 'quiz-7'],
        title: '팟오즈 & 임플라이드 오즈 계산법 완성'
      },
      3: {
        articleIds: ['understanding_domination_the_hidden_logic_behind_every_bet', 'the_3_biggest_leaks_killing_your_winrate', 'a-beginners-guide-to-poker-combinatorics'],
        quizIds: ['quiz-22'],
        title: '도미네이션과 치명적 릭(Leak) 차단'
      },
      4: {
        articleIds: ['mdf-alpha', 'protect-equity-and-prosper', 'visualizing-implied-odds'],
        quizIds: ['quiz-16', 'quiz-7'],
        title: '최소 방어 빈도(MDF)와 에퀴티 프로텍션'
      },
      5: {
        articleIds: ['what-is-leverage-in-poker', 'what-is-valor-in-poker', 'the-magic-of-equity-buckets'],
        quizIds: ['quiz-17', 'quiz-20'],
        title: '레버리지와 에퀴티 버킷 분류법'
      },
      6: {
        articleIds: ['what-is-gto-in-poker', 'what-does-gto-aim-to-achieve', 'interpreting-equity-distributions'],
        quizIds: ['quiz-22', 'quiz-16'],
        title: 'GTO의 진정한 목적과 에퀴티 분포 곡선'
      },
      7: {
        articleIds: ['understanding-which-mistakes-cost-you-the-most-money', 'mathematical-misconceptions-in-poker', 'the-value-of-fold-equity-experiment'],
        quizIds: ['quiz-7', 'quiz-17'],
        title: '치명적 수학 실수와 폴드 에퀴티 실험'
      },
      8: {
        articleIds: ['top-5-mistakes-in-spin-gos', 'fixing-a-poker-leak-part-1-spotting-and-correcting-errors', 'fixing-a-poker-leak-part-2-the-mental-game'],
        quizIds: ['quiz-20', 'quiz-22'],
        title: '에러 교정과 멘탈 게임 강화'
      },
      9: {
        articleIds: ['how_pros_use_solvers_to_crush_pool_leaks', 'how-to-leverage-gto-wizards-ev-comparison-tool', 'plo-just-changed-forever'],
        quizIds: ['quiz-16', 'quiz-17'],
        title: '1차 전직 대비: 솔버 활용 및 필드 공략'
      }
    };

    let track = curatedTracks[lvl];

    if (!track) {
      // Lv.10 이상 구간별 자동 순환 트랙
      const tierNum = lvl >= 85 ? 6 : lvl >= 65 ? 5 : lvl >= 45 ? 4 : lvl >= 25 ? 3 : 2;
      const tierArticles = allArticles.filter(a => {
        if (tierNum === 2) return a.level && a.level.includes('Lv.10~24');
        if (tierNum === 3) return a.level && a.level.includes('Lv.25~44');
        if (tierNum === 4) return a.level && a.level.includes('Lv.45~64');
        if (tierNum === 5) return a.level && a.level.includes('Lv.65~84');
        if (tierNum === 6) return a.level && a.level.includes('Lv.85~100');
        return true;
      });
      const tierQuizzes = allQuizzes.filter(q => (q.tier_num || 1) === tierNum);

      const aPool = tierArticles.length ? tierArticles : allArticles;
      const qPool = tierQuizzes.length ? tierQuizzes : allQuizzes;

      const artStart = ((lvl - 10) * 2) % Math.max(1, aPool.length - 2);
      const qStart = (lvl - 10) % qPool.length;

      const artSlice = aPool.slice(artStart, artStart + 3);
      const qSlice = [qPool[qStart], qPool[(qStart + 1) % qPool.length]].filter(Boolean);

      track = {
        articleIds: artSlice.map(a => a.id || a.slug),
        quizIds: qSlice.map(q => q.id),
        title: `Lv.${lvl} 실전 고급 이론과 스팟 분석`
      };
    }

    // 메타데이터 보강
    const requiredArticles = track.articleIds.map(id => {
      const found = allArticles.find(a => a.id === id || a.slug === id);
      return found || { id: id, slug: id, title_ko: id, category: '이론 학습', read_time: '5분' };
    });

    const requiredQuizzes = track.quizIds.map(qid => {
      const found = allQuizzes.find(q => q.id === qid);
      return found || { id: qid, title: qid, category: '실전 스팟', situation: '의사결정' };
    });

    return {
      level: lvl,
      title: track.title,
      requiredArticles: requiredArticles,
      requiredQuizzes: requiredQuizzes
    };
  },

  getLevelInfo(xp) {
    const passed = (this.userState && this.userState.promotions_passed) || [];
    const completedArts = (this.userState && this.userState.completed_articles) || [];
    const completedQs = (this.userState && this.userState.completed_quizzes) || [];

    // 1~100 레벨 계산 (순수 XP 기준)
    let rawLevel = 1;
    for (let l = 1; l <= 100; l++) {
      if (xp >= getLevelThreshold(l)) {
        rawLevel = l;
      } else {
        break;
      }
    }

    // 🔒 지정 필수 미션(아티클/퀴즈) 순차 클리어 검증 (미완료 시 레벨업 캡)
    let effectiveLevel = 1;
    let missionBlocked = false;
    let blockedReason = null;

    for (let l = 1; l < rawLevel; l++) {
      const curMissions = this.getCurriculumForLevel(l);
      const artsDone = curMissions.requiredArticles.every(a => completedArts.includes(a.id || a.slug));
      const qsDone = curMissions.requiredQuizzes.every(q => completedQs.includes(q.id));

      if (!artsDone || !qsDone) {
        effectiveLevel = l;
        missionBlocked = true;
        blockedReason = `Lv.${l} 필수 지정 미션 미완료`;
        break;
      }
      effectiveLevel = l + 1;
    }

    // 6구간 전직 게이트웨이 체크 (Lv.10, Lv.25, Lv.45, Lv.65, Lv.85, Lv.100)
    let needsExam = null;
    const gateways = [
      { tier: 1, reqLevel: 10 },
      { tier: 2, reqLevel: 25 },
      { tier: 3, reqLevel: 45 },
      { tier: 4, reqLevel: 65 },
      { tier: 5, reqLevel: 85 },
      { tier: 6, reqLevel: 100 }
    ];

    for (const g of gateways) {
      if (effectiveLevel >= g.reqLevel && !passed.includes(g.tier)) {
        effectiveLevel = g.reqLevel;
        needsExam = g.tier;
        break;
      }
    }

    // 현재 유저의 최고 전직 티어 결정
    let currentTierNum = 0;
    for (let t = 6; t >= 1; t--) {
      if (passed.includes(t)) {
        currentTierNum = t;
        break;
      }
    }
    const currentTier = PROMOTION_TIERS[currentTierNum];

    // 현재 레벨 내 XP 진행도 계산
    const curLvlMinXp = getLevelThreshold(effectiveLevel);
    const nextLvlXp = (effectiveLevel >= 100) ? curLvlMinXp : getLevelThreshold(effectiveLevel + 1);
    const curXpInLevel = Math.max(0, xp - curLvlMinXp);
    const neededForNext = Math.max(1, nextLvlXp - curLvlMinXp);
    const progressPct = (effectiveLevel >= 100) ? 100 : Math.min(100, Math.round((curXpInLevel / neededForNext) * 100));

    return {
      level: effectiveLevel,
      rawLevel: rawLevel,
      tier: currentTier,
      tierNum: currentTierNum,
      title: `Lv.${effectiveLevel} ${currentTier.title}`,
      badge: currentTier.badge,
      minXp: curLvlMinXp,
      maxXp: nextLvlXp,
      progressPct: progressPct,
      remainingXp: (effectiveLevel >= 100) ? 0 : Math.max(0, nextLvlXp - xp),
      needsExam: needsExam,
      passedPromotions: passed,
      missionBlocked: missionBlocked,
      blockedReason: blockedReason
    };
  },

  updateUserBar() {
    const xp = this.userState.xp;
    const info = this.getLevelInfo(xp);

    const badgeEl = document.getElementById('user-level-badge');
    const xpTextEl = document.getElementById('user-xp-text');
    const xpBarEl = document.getElementById('user-xp-bar');
    const streakEl = document.getElementById('user-streak');

    if (badgeEl) badgeEl.innerText = info.title;
    if (xpTextEl) xpTextEl.innerText = `${xp} / ${info.maxXp} XP`;
    if (xpBarEl) xpBarEl.style.width = `${info.progressPct}%`;
    if (streakEl) streakEl.innerText = this.userState.streak;

    characterManager.renderHeader();
    characterManager.renderDashboard();
    if (window.reader && reader.updateFilterPillsUI) {
      reader.updateFilterPillsUI();
      reader.renderArticleCards();
    }
    if (window.trainer && trainer.updateLevelChips) {
      trainer.updateLevelChips();
    }
    if (window.roadmap && roadmap.load) {
      roadmap.load();
    }
    storage.save(this.userState);
  },

  addXP(amount, type = 'general') {
    if (!amount || amount <= 0) return;
    const prevLvl = this.getLevelInfo(this.userState.xp).level;
    this.userState.xp += amount;

    // Stat boosts
    if (!this.userState.stats) {
      this.userState.stats = { theory: 35, decision: 40, ranges: 25, mental: 50 };
    }
    if (type === 'article') {
      this.userState.stats.theory = Math.min(100, (this.userState.stats.theory || 0) + 10);
    } else if (type === 'quiz') {
      this.userState.stats.decision = Math.min(100, (this.userState.stats.decision || 0) + 15);
    } else if (type === 'range') {
      this.userState.stats.ranges = Math.min(100, (this.userState.stats.ranges || 0) + 10);
    }

    const newLvlInfo = this.getLevelInfo(this.userState.xp);
    if (newLvlInfo.needsExam && (!prevLvl || newLvlInfo.level > prevLvl)) {
      const tier = PROMOTION_TIERS[newLvlInfo.needsExam];
      characterManager.showToast(`⚡ 축하합니다! <strong>[${tier.examTitle}]</strong> 자격을 획득하셨습니다! 시험을 통과하고 전직하세요!`);
      this.playAudioEffect('correct');
    } else if (newLvlInfo.level > prevLvl) {
      characterManager.showToast(`🎉 레벨업! <strong>Lv.${newLvlInfo.level}</strong> 달성!`);
      this.playAudioEffect('correct');
    } else {
      this.playAudioEffect('xp');
    }

    this.updateUserBar();
  },

  playAudioEffect(type) {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();

      if (type === 'click') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.05);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.05);
      } else if (type === 'correct') {
        const now = ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + i * 0.07);
          gain.gain.setValueAtTime(0.2, now + i * 0.07);
          gain.gain.exponentialRampToValueAtTime(0.001, now + (i + 1) * 0.07 + 0.15);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + i * 0.07);
          osc.stop(now + (i + 1) * 0.07 + 0.15);
        });
      } else if (type === 'wrong') {
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.linearRampToValueAtTime(160, now + 0.2);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === 'xp') {
        const now = ctx.currentTime;
        [659.25, 880, 1174.66].forEach((freq, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + i * 0.06);
          gain.gain.setValueAtTime(0.15, now + i * 0.06);
          gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.2);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + i * 0.06);
          osc.stop(now + i * 0.06 + 0.2);
        });
      }
    } catch (e) {}
  }
};

const reader = {
  articles: DB.articles,
  currentArticle: null,
  activeCategory: 'all',
  activeLevel: 'all',
  searchQuery: '',
  displayLimit: 24,
  unlockedOnly: false,
  readTimer: null,
  secondsRemaining: 45,

  loadArticles() {
    this.updateFilterPillsUI();
    this.renderArticleCards();
  },

  searchArticles(q) {
    this.searchQuery = q.toLowerCase().trim();
    this.displayLimit = 24;
    this.updateFilterPillsUI();
    this.renderArticleCards();
  },

  filterCategory(cat) {
    this.activeCategory = cat;
    this.displayLimit = 24;

    // Smart adjustment: if currently selected level has 0 items in this category, reset level to all
    if (this.activeLevel !== 'all') {
      const matchWithLevel = this.articles.filter(a =>
        (cat === 'all' || a.category === cat) && a.level.startsWith(this.activeLevel)
      );
      if (matchWithLevel.length === 0) {
        this.activeLevel = 'all';
      }
    }

    this.updateFilterPillsUI();
    this.renderArticleCards();
  },

  filterLevel(lvl) {
    this.activeLevel = lvl;
    this.displayLimit = 24;

    // Smart adjustment: if currently selected category has 0 items in this level, reset category to all!
    if (this.activeCategory !== 'all') {
      const matchWithCategory = this.articles.filter(a =>
        a.category === this.activeCategory && (lvl === 'all' || a.level.startsWith(lvl))
      );
      if (matchWithCategory.length === 0) {
        this.activeCategory = 'all';
      }
    }

    this.updateFilterPillsUI();
    this.renderArticleCards();
  },

  resetFilters() {
    this.activeCategory = 'all';
    this.activeLevel = 'all';
    this.searchQuery = '';
    const input = document.getElementById('article-search-input');
    if (input) input.value = '';
    this.displayLimit = 24;
    this.updateFilterPillsUI();
    this.renderArticleCards();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  updateFilterPillsUI() {
    // 1. Update active class on Category pills
    document.querySelectorAll('#article-category-filters .filter-pill').forEach(pill => {
      const c = pill.dataset.cat;
      if (c === this.activeCategory || (this.activeCategory === 'all' && c === 'all')) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });

    // 2. Update active class on Level pills
    document.querySelectorAll('#article-level-filters .filter-pill').forEach(pill => {
      const l = pill.dataset.lvl;
      if (l === this.activeLevel || (this.activeLevel === 'all' && l === 'all')) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });

    // 3. Dynamically update Level pill counts and Lock badges based on active category & user level
    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const levelMeta = {
      'Level 1': { title: '[입문] 동네 피쉬 (Lv.1~9)', req: 1, tierNum: 1 },
      'Level 2': { title: '[1차 전직] 펍 레귤러 (Lv.10~24)', req: 10, tierNum: 2 },
      'Level 3': { title: '[2차 전직] 마이크로 그라인더 (Lv.25~44)', req: 25, tierNum: 3 },
      'Level 4': { title: '[3차 전직] 로우스테이크 크러셔 (Lv.45~64)', req: 45, tierNum: 4 },
      'Level 5': { title: '[4차 전직] 미드스테이크 프로 (Lv.65~84)', req: 65, tierNum: 5 },
      'Level 6': { title: '[5차 전직/최종] 하이롤러 & 챔피언 (Lv.85~100)', req: 85, tierNum: 6 }
    };

    document.querySelectorAll('#article-level-filters .filter-pill').forEach(pill => {
      const l = pill.dataset.lvl;
      if (l === 'all') {
        const cnt = this.articles.filter(a => this.activeCategory === 'all' || a.category === this.activeCategory).length;
        pill.innerText = `전체 난이도 (${cnt})`;
        pill.style.opacity = '1';
      } else if (levelMeta[l]) {
        const meta = levelMeta[l];
        const isLocked = meta.req > userLvl;
        const cnt = this.articles.filter(a => 
          (this.activeCategory === 'all' || a.category === this.activeCategory) &&
          (a.tier_num === meta.tierNum || a.tier_category === l || a.level.startsWith(l))
        ).length;
        pill.innerText = `${isLocked ? '🔒 ' : '🔓 '}${meta.title} (${cnt})`;
        pill.style.opacity = (cnt === 0) ? '0.45' : '1';
      }
    });
  },

  loadMore() {
    this.displayLimit += 24;
    this.renderArticleCards();
    app.playAudioEffect('click');
  },

  renderArticleCards() {
    const container = document.getElementById('articles-grid-container');
    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const filtered = this.articles.filter(a => {
      if (this.activeCategory !== 'all' && a.category !== this.activeCategory) return false;
      if (this.activeLevel !== 'all') {
        const meta = { 'Level 1': 1, 'Level 2': 2, 'Level 3': 3, 'Level 4': 4, 'Level 5': 5, 'Level 6': 6 }[this.activeLevel];
        const matchesLevel = a.tier_num === meta || a.tier_category === this.activeLevel || a.level.startsWith(this.activeLevel);
        if (!matchesLevel) return false;
      }
      if (this.unlockedOnly && (a.required_level || 1) > userLvl) return false;
      if (this.searchQuery) {
        const pool = `${a.title_ko} ${a.title_en} ${a.category} ${a.level} ${a.slug}`.toLowerCase();
        if (!pool.includes(this.searchQuery)) return false;
      }
      return true;
    });

    const totalCount = filtered.length;
    const slice = filtered.slice(0, this.displayLimit);

    document.getElementById('article-count-label').innerText = `총 369편 중 ${totalCount}편 일치 (${slice.length}편 표시 중)`;

    if (totalCount === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3.5rem 1.5rem; background: var(--bg-card); border: 1.5px dashed var(--border-color); border-radius: 14px; margin: 1rem 0;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔍</div>
          <h3 style="font-size: 1.2rem; color: var(--text-main); margin-bottom: 0.5rem; font-weight: 700;">조건에 일치하는 아티클이 없습니다</h3>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem;">선택하신 카테고리와 난이도 조합에 해당하는 글이 없습니다.</p>
          <button class="btn-primary" onclick="reader.resetFilters()" style="padding: 0.65rem 1.75rem; font-size: 0.95rem; border-radius: 25px;">
            🔄 필터 초기화하고 전체 아티클 보기
          </button>
        </div>
      `;
      const loadMoreContainer = document.getElementById('articles-load-more-container');
      if (loadMoreContainer) loadMoreContainer.style.display = 'none';
      return;
    }

    container.innerHTML = slice.map(a => {
      const isCompleted = app.userState.completed_articles.includes(a.id);
      const isLocked = (a.required_level || 1) > userLvl;

      return `
        <div class="article-card ${isLocked ? 'locked' : ''}" onclick="reader.openArticle('${a.id}')" title="${isLocked ? `🔒 Lv.${a.required_level} 달성 시 열람 가능 (클릭하여 조건 확인)` : ''}">
          <div>
            <div class="article-card-header">
              ${isLocked ? `
                <span class="badge-lock">🔒 Lv.${a.required_level} 해금 필요</span>
              ` : `
                <span class="badge-level">${a.level}</span>
              `}
              <span style="font-size: 0.75rem; background: var(--bg-surface); padding: 2px 7px; border-radius: 4px; color: var(--text-muted); font-weight: 600;">${a.category}</span>
              <span class="read-time" style="margin-left: auto;">⏱️ ${a.read_time}</span>
            </div>
            <h3 style="${isLocked ? 'color: var(--text-muted);' : ''}">${a.title_ko}</h3>
            <p class="subtitle-en">${a.title_en}</p>
          </div>
          
          <div class="article-card-footer">
            <div class="author-info">✍️ ${a.author}</div>
            <div style="display: flex; gap: 0.6rem; align-items: center;">
              ${a.original_url ? `<a href="${a.original_url}" target="_blank" onclick="event.stopPropagation()" class="btn-original-link" style="padding: 2px 6px; font-size: 0.75rem;" title="GTO Wizard 공식 원문 열기">🌐 원문 ↗</a>` : ''}
              ${isLocked ? `
                <span style="font-size: 0.8rem; color: #f59e0b; font-weight: 800;">🔒 잠김</span>
              ` : isCompleted ? `
                <span class="completed-check" title="학습 완료">✓</span>
              ` : `
                <span style="font-size: 0.8rem; color: #3b82f6; font-weight: 700;">학습하기 →</span>
              `}
            </div>
          </div>
        </div>
      `;
    }).join('');

    const loadMoreContainer = document.getElementById('articles-load-more-container');
    if (loadMoreContainer) {
      if (slice.length < totalCount) {
        loadMoreContainer.style.display = 'block';
        document.getElementById('btn-load-more-count').innerText = `남은 ${totalCount - slice.length}개 더 보기 (+24)`;
      } else {
        loadMoreContainer.style.display = 'none';
      }
    }
  },

  updateCompletionUI(isCompleted, secondsRemaining) {
    const btnSidebar = document.getElementById('btn-complete-article');
    const btnBottom = document.getElementById('btn-bottom-complete-article');
    const bottomDesc = document.getElementById('bottom-complete-desc');
    const bottomIcon = document.getElementById('bottom-complete-icon');

    if (isCompleted) {
      if (btnSidebar) {
        btnSidebar.innerText = '✓ 이미 완독 완료한 아티클';
        btnSidebar.disabled = true;
        btnSidebar.style.opacity = '0.6';
        btnSidebar.style.cursor = 'not-allowed';
      }
      if (btnBottom) {
        btnBottom.innerText = '✓ 이미 완독 완료한 아티클 (+50 XP 획득 완료)';
        btnBottom.disabled = true;
        btnBottom.style.opacity = '0.6';
        btnBottom.style.cursor = 'not-allowed';
      }
      if (bottomIcon) bottomIcon.innerText = '✅';
      if (bottomDesc) bottomDesc.innerHTML = '이미 정독을 완료하여 경험치(50 XP)를 획득한 아티클입니다.';
    } else if (secondsRemaining > 0) {
      if (btnSidebar) {
        btnSidebar.innerText = `⏱️ 정독 중... (${secondsRemaining}초)`;
        btnSidebar.disabled = true;
        btnSidebar.style.opacity = '0.7';
        btnSidebar.style.cursor = 'wait';
      }
      if (btnBottom) {
        btnBottom.innerText = `⏱️ 아티클 정독 중... (${secondsRemaining}초 후 완독 가능)`;
        btnBottom.disabled = true;
        btnBottom.style.opacity = '0.7';
        btnBottom.style.cursor = 'wait';
      }
      if (bottomIcon) bottomIcon.innerText = '📖';
      if (bottomDesc) bottomDesc.innerHTML = `본문을 최소 45초 이상 꼼꼼히 정독하고 아래 완료 버튼을 직접 눌러야 정독이 인정되며 <strong>+50 XP</strong>를 획득합니다. (남은 시간: ${secondsRemaining}초)`;
    } else {
      if (btnSidebar) {
        btnSidebar.innerText = '✓ 정독 완료 (+50 XP)';
        btnSidebar.disabled = false;
        btnSidebar.style.opacity = '1';
        btnSidebar.style.cursor = 'pointer';
      }
      if (btnBottom) {
        btnBottom.innerText = '✓ 정독 완료! (+50 XP 획득하기)';
        btnBottom.disabled = false;
        btnBottom.style.opacity = '1';
        btnBottom.style.cursor = 'pointer';
      }
      if (bottomIcon) bottomIcon.innerText = '🎉';
      if (bottomDesc) bottomDesc.innerHTML = '🎉 <strong>45초 정독 시간 충족!</strong> 아래 버튼을 직접 클릭해야 정독이 완료되고 경험치가 지급됩니다.';
    }
  },

  openArticle(articleId) {
    const data = this.articles.find(a => a.id === articleId || a.slug === articleId);
    if (!data) return;

    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const isLocked = (data.required_level || 1) > userLvl;

    if (isLocked) {
      characterManager.showLevelLockModal(data);
      return;
    }

    app.playAudioEffect('click');
    this.currentArticle = data;

    document.getElementById('reader-title-ko').innerText = data.title_ko;
    document.getElementById('reader-title-en').innerText = data.title_en;
    document.getElementById('reader-level').innerText = data.level;
    document.getElementById('reader-time').innerText = `⏱️ ${data.read_time} 소요`;

    const origLink = document.getElementById('reader-original-link');
    const origFooterLink = document.getElementById('reader-footer-original-link');
    if (origLink && data.original_url) {
      origLink.href = data.original_url;
      origLink.style.display = 'inline-flex';
    }
    if (origFooterLink && data.original_url) {
      origFooterLink.href = data.original_url;
      origFooterLink.style.display = 'inline-flex';
    }

    if (this.readTimer) {
      clearInterval(this.readTimer);
      this.readTimer = null;
    }

    this.hasScrolledBottom = false;

    // Attach scroll listener to check bottom reach
    if (!this._scrollListenerAttached) {
      this._scrollListenerAttached = true;
      window.addEventListener('scroll', () => {
        if (app.currentView !== 'reader' || !this.currentArticle) return;
        const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (totalHeight <= 0 || (window.scrollY / totalHeight) >= 0.75) {
          this.hasScrolledBottom = true;
        }
      }, { passive: true });
    }

    const isCompleted = app.userState.completed_articles.includes(data.id);
    if (isCompleted) {
      this.secondsRemaining = 0;
      this.hasScrolledBottom = true;
      this.updateCompletionUI(true, 0);
    } else {
      this.secondsRemaining = 35; // 정독 필수 35초
      this.updateCompletionUI(false, 35);

      this.readTimer = setInterval(() => {
        // 편법 방지: 화면이 비활성화(다른 탭 등)되어 있으면 타이머 일시정지
        if (document.hidden || document.visibilityState !== 'visible') {
          return;
        }

        this.secondsRemaining--;
        if (this.secondsRemaining > 0) {
          this.updateCompletionUI(false, this.secondsRemaining);
        } else {
          clearInterval(this.readTimer);
          this.readTimer = null;
          this.updateCompletionUI(false, 0);
          if (window.app && app.playAudioEffect) app.playAudioEffect('xp');
        }
      }, 1000);
    }

    const tldrGrid = document.getElementById('reader-tldr-grid');
    tldrGrid.innerHTML = data.summary_cards.map(c => `
      <div class="tldr-card">
        <div class="tldr-badge">${c.badge}</div>
        <div class="tldr-title">${c.title}</div>
        <div class="tldr-text">${c.text}</div>
      </div>
    `).join('');

    const bodyEl = document.getElementById('reader-body');
    bodyEl.innerHTML = data.content_html;

    this.generateTOC(bodyEl);
    this.attachTermListeners(bodyEl);

    const relatedQuizzes = DB.quizzes.filter(q => q.article_id === data.id);
    this.renderEmbeddedQuiz(relatedQuizzes);

    app.navigate('reader');
  },

  generateTOC(bodyEl) {
    const tocList = document.getElementById('reader-toc-list');
    const headings = bodyEl.querySelectorAll('h2');
    if (!headings.length) {
      tocList.innerHTML = `<li style="color: var(--text-dim); font-size: 0.85rem;">소제목이 없습니다.</li>`;
      return;
    }

    tocList.innerHTML = Array.from(headings).map((h, i) => {
      const id = `heading-${i}`;
      h.id = id;
      return `<li><a href="#${id}" onclick="event.preventDefault(); document.getElementById('${id}').scrollIntoView({behavior: 'smooth'})">${h.innerText}</a></li>`;
    }).join('');
  },

  attachTermListeners(container) {
    const termTags = container.querySelectorAll('.gto-term');
    termTags.forEach(tag => {
      const termKey = tag.dataset.term;
      tag.addEventListener('mouseenter', (e) => {
        termPopover.show(termKey, e);
      });
      tag.addEventListener('click', (e) => {
        e.stopPropagation();
        termPopover.show(termKey, e);
      });
    });
  },

  renderEmbeddedQuiz(relatedQuizzes) {
    const quizContainer = document.getElementById('reader-quiz-container');
    if (!relatedQuizzes || !relatedQuizzes.length) {
      quizContainer.style.display = 'none';
      return;
    }

    const q = relatedQuizzes[0];
    quizContainer.style.display = 'block';
    quizContainer.innerHTML = `
      <div style="background: var(--bg-surface); border: 1px solid #3b82f6; border-radius: 12px; padding: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
          <span style="font-size: 1.3rem;">🎯</span>
          <h3 style="font-size: 1.15rem; font-weight: 800; color: #93c5fd;">아티클 체크업 퀴즈</h3>
        </div>
        <p style="font-size: 0.95rem; margin-bottom: 1rem; color: var(--text-main);">${q.situation}</p>
        <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 1rem; color: var(--text-main);">${q.question}</div>
        
        <div class="quiz-options-grid" id="embedded-quiz-options">
          ${q.options.map((opt, i) => `
            <button class="quiz-opt-btn" onclick="reader.handleEmbeddedAnswer('${q.id}', ${i})">
              <span>${opt.label}</span>
            </button>
          `).join('')}
        </div>
        <div id="embedded-quiz-feedback" style="display: none; margin-top: 1rem; padding: 1rem; background: var(--bg-surface); border-radius: 8px;"></div>
      </div>
    `;
  },

  handleEmbeddedAnswer(quizId, selectedIdx) {
    const q = DB.quizzes.find(item => item.id === quizId);
    if (!q) return;

    const isCorrect = (selectedIdx === q.correct_index);
    const alreadyCompleted = app.userState.completed_quizzes && app.userState.completed_quizzes.includes(q.id);
    const xpGained = (isCorrect && !alreadyCompleted) ? 50 : 0;

    const buttons = document.querySelectorAll('#embedded-quiz-options .quiz-opt-btn');
    buttons.forEach((b, i) => {
      b.disabled = true;
      if (i === selectedIdx) {
        b.classList.add(isCorrect ? 'correct' : 'wrong');
      } else if (i === q.correct_index) {
        b.classList.add('correct');
      }
    });

    const feedbackEl = document.getElementById('embedded-quiz-feedback');
    feedbackEl.style.display = 'block';

    let feedbackTitle = '';
    if (isCorrect) {
      feedbackTitle = alreadyCompleted
        ? '🎉 정답입니다! (이미 해결한 퀴즈 복습 • +0 XP)'
        : `🎉 정답입니다! (+${xpGained} XP)`;
    } else {
      feedbackTitle = '❌ 오답입니다 (+0 XP) — 솔버 해설을 정독하세요';
    }

    feedbackEl.innerHTML = `
      <div style="font-weight: 800; color: ${isCorrect ? '#34d399' : '#f87171'}; margin-bottom: 0.5rem;">
        ${feedbackTitle}
      </div>
      <div style="font-size: 0.9rem; color: var(--text-main); line-height: 1.5;">${q.explanation}</div>
    `;

    if (isCorrect) {
      if (!alreadyCompleted) {
        if (!app.userState.completed_quizzes) app.userState.completed_quizzes = [];
        app.userState.completed_quizzes.push(q.id);
        app.addXP(xpGained, 'quiz');
        characterManager.showToast('🎯 체크업 퀴즈 첫 정답 달성! (+50 XP 획득)');
      }
      app.playAudioEffect('correct');
    } else {
      app.playAudioEffect('wrong');
    }
  },

  markCompleted() {
    if (!this.currentArticle) return;

    // 편법 방지: 스크롤 및 체류 시간 검증
    if (!app.userState.completed_articles.includes(this.currentArticle.id)) {
      if (this.secondsRemaining > 0 && !this.hasScrolledBottom) {
        characterManager.showToast(`📜 본문을 끝까지 스크롤하여 정독하고, 타이머(${this.secondsRemaining}초)를 채워주세요!`);
        if (window.app && app.playAudioEffect) app.playAudioEffect('wrong');
        return;
      }
      if (this.secondsRemaining > 0) {
        characterManager.showToast(`⏱️ 아티클을 깊이 있게 정독해주세요! (${this.secondsRemaining}초 남음)`);
        if (window.app && app.playAudioEffect) app.playAudioEffect('wrong');
        return;
      }
      if (!this.hasScrolledBottom) {
        characterManager.showToast(`📜 아티클 본문을 끝까지 스크롤하여 읽어주세요! (체크업 퀴즈와 결론 확인 필수)`);
        if (window.app && app.playAudioEffect) app.playAudioEffect('wrong');
        return;
      }
    }

    if (this.readTimer) {
      clearInterval(this.readTimer);
      this.readTimer = null;
    }

    if (!app.userState.completed_articles.includes(this.currentArticle.id)) {
      app.userState.completed_articles.push(this.currentArticle.id);
      app.addXP(50, 'article');
      characterManager.showToast('📖 아티클 정독 완료! (+50 XP 획득)');
    }
    
    this.updateCompletionUI(true, 0);

    this.renderArticleCards();
  }
};

const termPopover = {
  el: null,

  init() {
    this.el = document.getElementById('term-popover');
    document.addEventListener('click', (e) => {
      if (this.el && !this.el.contains(e.target) && !e.target.classList.contains('gto-term')) {
        this.hide();
      }
    });
  },

  show(termKey, event) {
    if (!this.el) this.init();
    const data = DB.glossary[termKey.toLowerCase().trim()];
    if (!data) return;

    document.getElementById('pop-category').innerText = data.category;
    document.getElementById('pop-title').innerText = `${data.term} (${data.korean_term})`;
    document.getElementById('pop-desc').innerText = data.short_desc;
    document.getElementById('pop-analogy').innerText = `💡 ${data.analogy}`;
    document.getElementById('pop-tip').innerText = `⚡ ${data.pro_tip}`;

    const rect = event.target.getBoundingClientRect();
    const popoverWidth = 340;
    let left = rect.left;
    if (left + popoverWidth > window.innerWidth - 20) {
      left = window.innerWidth - popoverWidth - 20;
    }
    let top = rect.bottom + 8;
    if (top + 260 > window.innerHeight) {
      top = rect.top - 270;
    }

    this.el.style.left = `${Math.max(10, left)}px`;
    this.el.style.top = `${Math.max(10, top)}px`;
    this.el.style.display = 'block';
  },

  hide() {
    if (this.el) {
      this.el.style.display = 'none';
    }
  }
};

const trainer = {
  quizzes: DB.quizzes,
  currentIndex: 0,
  isAnswered: false,

  init() {
    this.renderCurrentQuiz();
  },

  jumpToLevel(lvl) {
    const qLevelReqs = { 1: 1, 2: 10, 3: 25, 4: 45, 5: 65, 6: 85 };
    const targetReq = qLevelReqs[lvl] || lvl;
    const idx = this.quizzes.findIndex(q => (q.tier_num || 1) === lvl || (q.required_level || 1) === targetReq);
    if (idx !== -1) {
      this.currentIndex = idx;
      this.renderCurrentQuiz();
      app.playAudioEffect('click');
    }
  },

  openQuizById(quizId) {
    if (window.authManager && !authManager.isLoggedIn()) {
      authManager.showGate('login');
      return;
    }
    const idx = this.quizzes.findIndex(q => q.id === quizId);
    if (idx !== -1) {
      this.currentIndex = idx;
    }
    app.navigate('trainer');
    this.renderCurrentQuiz();
  },

  jumpToFirstUnlocked() {
    this.currentIndex = 0;
    this.renderCurrentQuiz();
    app.playAudioEffect('click');
  },

  updateLevelChips() {
    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const curQ = this.quizzes[this.currentIndex];
    const curTier = curQ ? (curQ.tier_num || (curQ.required_level >= 85 ? 6 : curQ.required_level >= 65 ? 5 : curQ.required_level >= 45 ? 4 : curQ.required_level >= 25 ? 3 : curQ.required_level >= 10 ? 2 : 1)) : 1;

    const qLevelReqs = { 1: 1, 2: 10, 3: 25, 4: 45, 5: 65, 6: 85 };
    const labels = {
      1: '[입문] 동네 피쉬 (Lv.1~9)',
      2: '[1차 전직] 펍 레귤러 (Lv.10~24)',
      3: '[2차 전직] 마이크로 그라인더 (Lv.25~44)',
      4: '[3차 전직] 로우스테이크 크러셔 (Lv.45~64)',
      5: '[4차 전직] 미드스테이크 프로 (Lv.65~84)',
      6: '[5차 전직/최종] 하이롤러 & 챔피언 (Lv.85~100)'
    };

    document.querySelectorAll('#quiz-level-filter-chips .filter-pill').forEach(btn => {
      const qlvl = parseInt(btn.dataset.qlvl, 10);
      const reqLvl = qLevelReqs[qlvl] || 1;
      const isLocked = reqLvl > userLvl;
      const isActive = (qlvl === curTier);

      if (isActive) btn.classList.add('active');
      else btn.classList.remove('active');

      btn.innerText = `${isLocked ? '🔒 ' : '🔓 '}${labels[qlvl] || `Tier ${qlvl}`}`;
    });
  },

  renderCurrentQuiz() {
    if (!this.quizzes.length) return;
    const q = this.quizzes[this.currentIndex];
    this.isAnswered = false;

    const userLvlInfo = app.getLevelInfo(app.userState.xp);
    const userLvl = userLvlInfo.level;
    const isLocked = (q.required_level || 1) > userLvl;

    this.updateLevelChips();

    document.getElementById('quiz-counter').innerText = `${this.currentIndex + 1} / ${this.quizzes.length} [${q.level || `Lv.${q.required_level}`}]`;
    document.getElementById('trainer-pot-display').innerText = q.pot;

    const boardEl = document.getElementById('trainer-board-cards');
    if (!q.board || q.board.length === 0) {
      boardEl.innerHTML = `<div style="color: #64748b; font-size: 0.9rem; font-style: italic;">[Preflop - 보드 카드 없음]</div>`;
    } else {
      boardEl.innerHTML = q.board.map(c => this.createCardHtml(c)).join('');
    }

    const heroEl = document.getElementById('trainer-hero-cards');
    heroEl.innerHTML = q.hero_hand.map(c => this.createCardHtml(c)).join('');

    document.getElementById('trainer-hero-label').innerText = 
      `HERO (${q.hero_position}) • Effective Stack: ${q.effective_stack}`;

    document.getElementById('trainer-situation-desc').innerText = q.situation;

    const feedbackBox = document.getElementById('trainer-feedback-box');
    feedbackBox.style.display = 'none';

    const questionEl = document.getElementById('trainer-question-text');
    const optGrid = document.getElementById('trainer-options-grid');

    if (isLocked) {
      questionEl.innerHTML = `<span style="color: #f59e0b; font-weight: 800;">🔒 [${q.level}] 달성 시 도전 가능한 고급 스팟입니다.</span>`;
      optGrid.innerHTML = `
        <div class="quiz-locked-shield" style="grid-column: 1 / -1;">
          <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">🔒</div>
          <h3>${q.level} 이상 도전 가능</h3>
          <p>
            현재 회원님의 레벨은 <strong>${userLvlInfo.title}</strong>입니다.<br>
            기초 레벨 퀴즈와 아티클을 먼저 마스터하여 XP를 획득하고 승급하세요!
          </p>
          <button class="btn-primary" onclick="trainer.jumpToFirstUnlocked()">
            🔓 해금된 퀴즈 풀기 (1번으로 이동)
          </button>
        </div>
      `;
    } else {
      questionEl.innerText = q.question;
      optGrid.innerHTML = q.options.map((opt, i) => `
        <button class="quiz-opt-btn" id="quiz-btn-${i}" onclick="trainer.selectOption(${i})">
          <span>${opt.label}</span>
          <span style="font-size: 0.85rem; color: var(--text-dim); font-weight: 500;">선택</span>
        </button>
      `).join('');
    }
  },

  createCardHtml(cardStr) {
    if (!cardStr) return '';
    const rank = cardStr.slice(0, -1);
    const suit = cardStr.slice(-1);
    
    let suitClass = 'card-suit-spade';
    if (suit === '♥' || suit === '♦') {
      suitClass = (suit === '♥') ? 'card-suit-heart' : 'card-suit-diamond';
    } else if (suit === '♣') {
      suitClass = 'card-suit-club';
    }

    return `
      <div class="poker-card ${suitClass}">
        <div class="card-top">
          <span class="card-rank">${rank}</span>
          <span style="font-size: 0.8rem;">${suit}</span>
        </div>
        <div class="card-center-suit">${suit}</div>
        <div class="card-bottom">
          <span class="card-rank">${rank}</span>
          <span style="font-size: 0.8rem;">${suit}</span>
        </div>
      </div>
    `;
  },

  selectOption(optIndex) {
    if (this.isAnswered) return;
    this.isAnswered = true;
    const q = this.quizzes[this.currentIndex];

    const isCorrect = (optIndex === q.correct_index);
    const alreadyCompleted = app.userState.completed_quizzes && app.userState.completed_quizzes.includes(q.id);
    const xpGained = (isCorrect && !alreadyCompleted) ? 50 : 0;

    q.options.forEach((opt, i) => {
      const btn = document.getElementById(`quiz-btn-${i}`);
      btn.disabled = true;
      btn.innerHTML = `
        <span>${opt.label}</span>
        <span style="font-size: 0.85rem; font-weight: 800; color: ${opt.is_correct ? '#34d399' : 'var(--text-dim)'};">
          GTO: ${opt.gto_freq} (EV: ${opt.ev})
        </span>
      `;
      if (i === optIndex) {
        btn.classList.add(isCorrect ? 'correct' : 'wrong');
      } else if (opt.is_correct) {
        btn.classList.add('correct');
      }
    });

    const feedbackBox = document.getElementById('trainer-feedback-box');
    const statusTitle = document.getElementById('feedback-status-title');
    const conceptTag = document.getElementById('feedback-concept-tag');
    const explanationText = document.getElementById('feedback-explanation-text');

    statusTitle.className = `feedback-status ${isCorrect ? 'correct' : 'wrong'}`;
    if (isCorrect) {
      if (alreadyCompleted) {
        statusTitle.innerText = `✅ 정답입니다! (이미 클리어한 퀴즈 • 복습 완료 / +0 XP)`;
      } else {
        statusTitle.innerText = `✅ 정답입니다! (+${xpGained} XP)`;
      }
    } else {
      statusTitle.innerText = `❌ 오답입니다 (+0 XP) — 아래 솔버 해설을 정독하세요!`;
    }
    conceptTag.innerText = `핵심 원리: ${q.key_concept}`;
    explanationText.innerText = q.explanation;
    feedbackBox.style.display = 'block';

    if (isCorrect) {
      if (!alreadyCompleted) {
        if (!app.userState.completed_quizzes) app.userState.completed_quizzes = [];
        app.userState.completed_quizzes.push(q.id);
        app.addXP(xpGained, 'quiz');
        characterManager.showToast('🎯 스팟 퀴즈 첫 정답 달성! (+50 XP 획득)');
      }
      app.playAudioEffect('correct');
    } else {
      app.playAudioEffect('wrong');
      characterManager.showToast('❌ 오답입니다. 솔버 해설을 꼼꼼히 확인하고 복습하세요!');
    }
  },

  nextQuiz() {
    app.playAudioEffect('click');
    if (this.currentIndex < this.quizzes.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuiz();
    }
  },

  prevQuiz() {
    app.playAudioEffect('click');
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuiz();
    }
  }
};

const matrix = {
  ranks: ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'],
  rangesData: DB.ranges,
  currentPreset: null,
  _explored: {},
  _initialized: false,

  init() {
    this._initialized = false;
    this.loadPreset('btn_open');
    this._initialized = true;
  },

  loadPreset(presetId) {
    const preset = this.rangesData.presets.find(p => p.id === presetId);
    if (!preset) return;

    const userLvlInfo = app.getLevelInfo(app.userState.xp);
    const userLvl = userLvlInfo.level;
    const isLocked = (preset.required_level || 1) > userLvl;

    if (!app.userState.explored_ranges) {
      app.userState.explored_ranges = [];
    }

    // Award XP ONLY once per unlocked preset, persisted in storage (anti-cheat)
    if (this._initialized && !isLocked && !app.userState.explored_ranges.includes(presetId)) {
      app.userState.explored_ranges.push(presetId);
      if (window.app && app.addXP) {
        app.addXP(20, 'range');
        characterManager.showToast(`📊 새로운 레인지 [${preset.name}] 첫 탐색! (+20 XP)`);
      }
    }

    this.currentPreset = preset;

    // Sync select dropdown
    const selectEl = document.getElementById('matrix-preset-select');
    if (selectEl && selectEl.value !== presetId) {
      selectEl.value = presetId;
    }

    // Sync quick-chips active state and lock indicators
    document.querySelectorAll('#matrix-quick-chips button').forEach(btn => {
      const pid = btn.dataset.pid;
      const targetP = this.rangesData.presets.find(p => p.id === pid);
      const pReqLvl = targetP ? (targetP.required_level || 1) : 1;
      const pLocked = pReqLvl > userLvl;

      if (btn.dataset.pid === presetId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }

      // Add lock icon if locked
      if (pLocked && !btn.innerText.startsWith('🔒')) {
        btn.innerText = `🔒 ${btn.innerText.replace('🔒 ', '')}`;
      } else if (!pLocked && btn.innerText.startsWith('🔒')) {
        btn.innerText = btn.innerText.replace('🔒 ', '');
      }
    });

    const descEl = document.getElementById('matrix-preset-desc');
    const gridEl = document.getElementById('poker-matrix-grid');
    const legendEl = document.getElementById('matrix-legend-container');
    const hoverEl = document.getElementById('matrix-hover-inspector');

    if (isLocked) {
      descEl.innerHTML = `<span style="color: #f59e0b; font-weight: 800;">🔒 [Lv.${preset.required_level} ${preset.required_level_title}] 달성 시 열람 가능한 고급 솔버 레인지입니다.</span>`;
      
      gridEl.innerHTML = `
        <div class="matrix-locked-shield">
          <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🔒</div>
          <h3>${preset.required_level_title} 전용 GTO 솔루션</h3>
          <p>
            현재 회원님의 레벨은 <strong>${userLvlInfo.title}</strong>입니다.<br>
            기초 오픈 레인지를 먼저 실전에 체화하고 레벨업하여 3-Bet 및 15BB 셔브 솔루션을 해금하세요!
          </p>
          <button class="btn-primary" onclick="matrix.loadPreset('btn_open')">
            🔓 기본 해금 레인지 (BTN 오픈) 보기
          </button>
        </div>
      `;

      legendEl.innerHTML = `<div style="color: var(--text-dim); font-size: 0.85rem; padding: 0.5rem;">🔒 레벨 달성 후 범례가 해금됩니다.</div>`;
      if (hoverEl) {
        hoverEl.innerHTML = `<div style="color: var(--text-dim); text-align: center; padding: 2rem 0;">🔒 레벨 해금 후 핸드 인스펙터가 작동합니다.</div>`;
      }
      document.getElementById('matrix-stats-combos').innerText = '잠김 (Lv.' + preset.required_level + ' 필요)';
      document.getElementById('matrix-stats-bar').innerHTML = '';
      return;
    }

    descEl.innerText = preset.description;

    legendEl.innerHTML = preset.legend.map(l => `
      <div class="legend-item">
        <div class="legend-color-box" style="background: ${l.color};"></div>
        <span style="font-weight: 600;">${l.label}</span>
      </div>
    `).join('');

    this.calculateRangeStats();
    this.renderGrid();
  },

  calculateRangeStats() {
    if (!this.currentPreset) return;
    let totalCombos = 0;
    const actionCounts = {};

    for (let r = 0; r < 13; r++) {
      for (let c = 0; c < 13; c++) {
        let handName = '';
        let combos = 0;
        if (r === c) {
          handName = this.ranks[r] + this.ranks[c];
          combos = 6;
        } else if (r < c) {
          handName = this.ranks[r] + this.ranks[c] + 's';
          combos = 4;
        } else {
          handName = this.ranks[c] + this.ranks[r] + 'o';
          combos = 12;
        }

        const data = this.currentPreset.actions[handName];
        if (data) {
          const effective = combos * (data.freq / 100);
          totalCombos += effective;
          const act = data.action;
          actionCounts[act] = (actionCounts[act] || 0) + effective;
        }
      }
    }

    const pct = ((totalCombos / 1326) * 100).toFixed(1);
    const combosEl = document.getElementById('matrix-stats-combos');
    if (combosEl) {
      combosEl.innerText = `${Math.round(totalCombos)} 콤보 (${pct}%)`;
    }

    const barEl = document.getElementById('matrix-stats-bar');
    if (barEl) {
      barEl.innerHTML = Object.entries(actionCounts).map(([act, cnt]) => {
        const actPct = ((cnt / 1326) * 100).toFixed(1);
        let color = '#ef4444';
        if (act.toLowerCase().includes('call')) color = '#10b981';
        else if (act.toLowerCase().includes('3-bet')) color = '#f59e0b';
        else if (act.toLowerCase().includes('shove') || act.toLowerCase().includes('4-bet')) color = '#8b5cf6';
        return `<span style="color: ${color};">${act}: ${Math.round(cnt)}개 (${actPct}%)</span>`;
      }).join(' • ');
    }
  },

  renderGrid() {
    const gridEl = document.getElementById('poker-matrix-grid');
    gridEl.innerHTML = '';

    for (let r = 0; r < 13; r++) {
      for (let c = 0; c < 13; c++) {
        let handName = '';
        let combos = 0;
        let handType = '';

        if (r === c) {
          handName = this.ranks[r] + this.ranks[c];
          combos = 6;
          handType = '포켓 페어 (6 combos)';
        } else if (r < c) {
          handName = this.ranks[r] + this.ranks[c] + 's';
          combos = 4;
          handType = '수티드 (4 combos)';
        } else {
          handName = this.ranks[c] + this.ranks[r] + 'o';
          combos = 12;
          handType = '오프수트 (12 combos)';
        }

        const actionData = this.currentPreset.actions[handName];
        let actionClass = 'action-fold';

        if (actionData) {
          const actionName = actionData.action.toLowerCase();
          if (actionName.includes('shove') || actionName.includes('4-bet')) {
            actionClass = 'action-shove';
          } else if (actionName.includes('3-bet')) {
            actionClass = 'action-3bet';
          } else if (actionName.includes('call')) {
            actionClass = 'action-call';
          } else if (actionName.includes('raise')) {
            actionClass = 'action-raise';
          }
        }

        const cell = document.createElement('div');
        cell.className = `matrix-cell ${actionClass}`;
        cell.innerText = handName;

        cell.addEventListener('mouseenter', () => {
          this.inspectHand(handName, handType, actionData);
        });
        cell.addEventListener('click', () => {
          this.inspectHand(handName, handType, actionData);
          app.playAudioEffect('click');
        });

        gridEl.appendChild(cell);
      }
    }
  },

  inspectHand(handName, handType, actionData) {
    document.getElementById('inspect-hand-name').innerText = handName;
    document.getElementById('inspect-combos').innerText = handType;

    const actionDescEl = document.getElementById('inspect-action-desc');
    const tipEl = document.getElementById('inspect-tip');

    if (!actionData) {
      actionDescEl.innerHTML = `<span style="color: #64748b;">Fold (100%)</span>`;
      if (tipEl) {
        tipEl.innerHTML = `❌ <strong>GTO 솔버 폴드 권장</strong>: 기대값(EV)이 마이너스이거나 역임플라이드 오즈가 심각하여 깔끔하게 폴드합니다.`;
      }
    } else {
      let color = '#ef4444';
      if (actionData.action.toLowerCase().includes('call')) color = '#10b981';
      else if (actionData.action.toLowerCase().includes('3-bet')) color = '#f59e0b';
      else if (actionData.action.toLowerCase().includes('shove') || actionData.action.toLowerCase().includes('4-bet')) color = '#8b5cf6';

      actionDescEl.innerHTML = `
        <span style="color: ${color};">
          ${actionData.action} (${actionData.freq}%)
        </span>
      `;

      if (tipEl) {
        let tipText = `⚡ 솔버 핵심 핸드: 현재 포지션에서 적극적인 참여가 요구되는 핵심 레인지입니다.`;
        if (['AA', 'KK', 'QQ', 'AKs'].includes(handName)) {
          tipText = `🔥 <strong>최상위 프리미엄 너츠 핸드</strong>: 100% 빈도로 강력한 밸류 팟 빌딩을 감행합니다.`;
        } else if (['JJ', 'TT', '99', 'AQs', 'AKo'].includes(handName)) {
          tipText = `⚔️ <strong>강력한 브로드웨이/하이페어</strong>: 높은 밸류를 바탕으로 3벳 및 오픈의 핵심 축을 담당합니다.`;
        } else if (['A5s', 'A4s', 'A3s', 'A2s'].includes(handName)) {
          tipText = `🎯 <strong>A-블로커 + 휠 스트레이트</strong>: 상대의 AA/AK을 차단하며 최고의 3벳/4벳 세미 블러프로 기능합니다.`;
        } else if (['T9s', '98s', '87s', '76s', '65s', '54s'].includes(handName)) {
          tipText = `🌊 <strong>최고의 수티드 커넥터</strong>: 높은 에퀴티 실현력(EQR)과 넛 플러시/스트레이트 잠재력으로 멀티웨이 및 플랫에 탁월합니다.`;
        } else if (['88', '77', '66', '55', '44', '33', '22'].includes(handName)) {
          tipText = `🧱 <strong>포켓 페어</strong>: 셋 마이닝(Set Mining) 밸류와 상대 블러프를 낚아채는 안정적인 쇼다운 밸류를 가집니다.`;
        } else if (actionData.action.toLowerCase().includes('call')) {
          tipText = `🛡️ <strong>플랫 콜 디펜스</strong>: 포지션 혹은 좋은 팟 오즈를 바탕으로 포스트플랍 에퀴티를 실현하는 방어 핸드입니다.`;
        }
        tipEl.innerHTML = tipText;
      }
    }
  }
};

const roadmap = {
  data: DB.roadmap,

  load() {
    const rm = this.data;
    const userState = app.userState;

    const levelsContainer = document.getElementById('roadmap-levels-container');
    levelsContainer.innerHTML = rm.levels.map(lvl => {
      const isLocked = (userState.xp < lvl.required_xp);
      return `
        <div class="roadmap-level-card ${isLocked ? 'locked' : ''}">
          <div class="level-badge-header">
            <div>
              <h3 style="font-size: 1.35rem; font-weight: 800; color: var(--text-main);">${lvl.title}</h3>
              <p style="font-size: 0.85rem; color: var(--text-dim);">${lvl.subtitle}</p>
            </div>
            <span class="level-badge">${lvl.badge}</span>
          </div>

          <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1rem;">
            ${lvl.description}
          </p>

          ${isLocked ? `
            <div style="background: rgba(0,0,0,0.2); padding: 0.75rem; border-radius: 8px; font-size: 0.85rem; color: #f59e0b; font-weight: 700;">
              🔒 해금 조건: ${lvl.required_xp} XP 달성 필요 (현재: ${userState.xp} XP)
            </div>
          ` : `
            <div class="nodes-list">
              ${lvl.nodes.map((n, idx) => {
                const isCompleted = userState.completed_articles.includes(n.article_id);
                const isFirstPending = !isCompleted && lvl.nodes.slice(0, idx).every(prev => userState.completed_articles.includes(prev.article_id));
                return `
                  <div class="node-item ${isCompleted ? 'completed' : ''}" onclick="reader.openArticle('${n.article_id}')" style="${isFirstPending ? 'border: 1.5px solid #3b82f6; background: rgba(59, 130, 246, 0.05);' : ''}">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                      <span style="font-size: 1.2rem;">${isCompleted ? '✅' : (isFirstPending ? '👉' : '📖')}</span>
                      <div>
                        <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
                          <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-main);">${n.title}</div>
                          ${isFirstPending ? '<span style="font-size: 0.68rem; background: #3b82f6; color: #fff; padding: 1px 6px; border-radius: 10px; font-weight: 800;">추천 다음 스팟</span>' : ''}
                        </div>
                        <span style="font-size: 0.75rem; color: var(--text-dim);">${n.category}</span>
                      </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                      <span style="font-size: 0.8rem; color: #fbbf24; font-weight: 700;">+${n.xp} XP</span>
                      <button class="${isFirstPending ? 'btn-primary' : 'btn-secondary'}" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">
                        ${isCompleted ? '다시 읽기' : (isFirstPending ? '지금 학습 시작 →' : '학습 시작')}
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          `}
        </div>
      `;
    }).join('');

    const dynamicAchievements = [
      {
        id: "char_created",
        title: "모험의 시작",
        desc: "나만의 포커 캐릭터 생성 및 첫 발걸음",
        icon: userState.avatar || "🦈",
        unlocked: !!localStorage.getItem('studypoker_char_created')
      },
      {
        id: "first_read",
        title: "첫 페이지를 넘기다",
        desc: "첫 번째 GTO 아티클 완독 (+50 XP)",
        icon: "📖",
        unlocked: (userState.completed_articles && userState.completed_articles.length > 0)
      },
      {
        id: "quiz_ace",
        title: "솔버적 뇌지컬",
        desc: "스팟 퀴즈 정답 맞히기 (+50 XP)",
        icon: "🎯",
        unlocked: (userState.completed_quizzes && userState.completed_quizzes.length > 0)
      },
      {
        id: "streak_3",
        title: "3일 연속 그라인딩",
        desc: "3일 연속 학습 스트릭 유지",
        icon: "🔥",
        unlocked: ((userState.streak || 0) >= 3)
      },
      {
        id: "level_up",
        title: "1차 전직 달성",
        desc: "600 XP 달성 및 1차 전직 심사 해금",
        icon: "⚔️",
        unlocked: ((userState.xp || 0) >= 600)
      },
      {
        id: "matrix_explorer",
        title: "레인지의 지배자",
        desc: "13x13 매트릭스 5개 이상 포지션 탐색",
        icon: "📊",
        unlocked: (userState.explored_ranges && userState.explored_ranges.length >= 5)
      }
    ];

    const achContainer = document.getElementById('roadmap-achievements-container');
    if (achContainer) {
      achContainer.innerHTML = dynamicAchievements.map(a => `
        <div class="feature-item" style="opacity: ${a.unlocked ? '1' : '0.45'};">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">${a.icon}</div>
          <h4 style="font-size: 1.05rem; margin-bottom: 0.25rem;">${a.title}</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted);">${a.desc}</p>
          <div style="margin-top: 0.75rem; font-size: 0.75rem; font-weight: 700; color: ${a.unlocked ? '#34d399' : '#64748b'};">
            ${a.unlocked ? '🏆 달성 완료' : '미달성'}
          </div>
        </div>
      `).join('');
    }
  }
};

const glossary = {
  terms: DB.glossary,

  load() {
    this.filterTerms('');
  },

  filterTerms(query) {
    const q = query.toLowerCase().trim();
    const container = document.getElementById('glossary-grid-container');

    const filtered = Object.entries(this.terms).filter(([k, item]) => {
      if (!q) return true;
      const pool = `${k} ${item.term} ${item.korean_term} ${item.short_desc} ${item.analogy}`.toLowerCase();
      return pool.includes(q);
    });

    if (!filtered.length) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-dim); padding: 3rem;">검색 결과가 없습니다.</div>`;
      return;
    }

    container.innerHTML = filtered.map(([k, item]) => `
      <div class="article-card" style="cursor: default;">
        <div>
          <div class="article-card-header">
            <span class="badge-level">${item.category}</span>
          </div>
          <h3 style="color: #60a5fa;">${item.term}</h3>
          <p class="subtitle-en" style="font-weight: 700; color: var(--text-main); margin-bottom: 0.75rem;">${item.korean_term}</p>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.5;">${item.short_desc}</p>
          
          <div style="background: rgba(0,0,0,0.06); border-left: 3px solid #f59e0b; padding: 0.65rem 0.85rem; font-size: 0.85rem; color: var(--text-main); border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
            💡 <strong>비유:</strong> ${item.analogy}
          </div>
        </div>

        <div style="padding-top: 0.75rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: #34d399;">
          ⚡ <strong>Pro Tip:</strong> ${item.pro_tip}
        </div>
      </div>
    `).join('');
  }
};

const aiCoach = {
  overlay: null,
  messagesArea: null,
  inputEl: null,

  init() {
    this.overlay = document.getElementById('ai-modal-overlay');
    this.messagesArea = document.getElementById('ai-messages-area');
    this.inputEl = document.getElementById('ai-user-input');
  },

  open() {
    if (!this.overlay) this.init();
    this.overlay.style.display = 'flex';
    this.inputEl.focus();
    app.playAudioEffect('click');
  },

  close() {
    if (!this.overlay) this.init();
    this.overlay.style.display = 'none';
  },

  sendPreset(text) {
    if (!this.inputEl) this.init();
    this.inputEl.value = text;
    this.sendMessage();
  },

  sendMessage() {
    if (!this.inputEl) this.init();
    const text = this.inputEl.value.trim();
    if (!text) return;

    this.inputEl.value = '';
    this.appendMessage('user', text);
    this.scrollToBottom();

    app.userState.ai_queries_count = (app.userState.ai_queries_count || 0) + 1;
    storage.save(app.userState);

    const loadingId = 'loading-' + Date.now();
    this.appendMessage('coach', '코치가 369개 포커 솔버 데이터를 분석 중입니다... 🧠', loadingId);
    this.scrollToBottom();

    setTimeout(() => {
      const answer = this.generateAnswer(text);
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.innerHTML = answer.replace(/\\n/g, '<br>');
      }
      this.scrollToBottom();
      app.playAudioEffect('click');
    }, 400);
  },

  generateAnswer(q) {
    const qLower = q.toLowerCase();
    if (qLower.includes('a72') || qLower.includes('a-7-2') || qLower.includes('작은 벳') || qLower.includes('1/3') || qLower.includes('c-bet') || qLower.includes('c벳')) {
      return `**[코치 Ivan의 GTO 해설]**\\n\\nA-7-2r이나 K-8-3r 같은 **드라이한 A/K-high 보드**에서 1/3팟의 작은 C-bet을 전체 레인지(80~100%)로 구사하는 이유는 명확합니다:\\n\\n1. **압도적인 레인지 우위 (Range Advantage)**: 프리플랍 레이저(IP)는 AA, AK, AQ을 모두 쥐고 있는 반면, BB는 보통 AA, AK을 3벳으로 뺐기 때문에 레인지가 캡(Capped)되어 있습니다.\\n2. **낮은 에퀴티 저항선**: A가 깔린 보드에서는 상대방의 99, 88 같은 포켓페어나 언더카드가 턴에서 역전할 확률이 5장 이하(약 10~15%)로 매우 낮습니다.\\n3. **효율적 칩 보존**: 굳이 팟을 크게 키우지 않아도 상대의 에어(Air) 핸드와 약한 콤보들을 1/3 팟만으로 즉시 폴드시킬 수 있기 때문입니다!`;
    } else if (qLower.includes('블로커') || qLower.includes('언블로커') || qLower.includes('blocker')) {
      return `**[코치 Tombos의 GTO 해설]**\\n\\n블로커는 콤보 수학의 마법입니다. 핵심 원칙을 요약해 드릴게요:\\n\\n1. **리버 블러프를 칠 때**: 상대의 **'콜할 최강 핸드'**를 블락해야 합니다! (예: 상대의 스트레이트 완성 카드인 T이나 너트 플러시 카드인 A♠를 내가 쥐고 있어야 상대가 콜을 못 합니다.)\\n2. **언블로커의 중요성**: 반대로 상대가 미스해서 폴드해야 할 카드(Busted Draw)는 내가 **쥐고 있지 않아야(Unblock)** 합니다. 내가 그 카드를 들고 있으면 상대가 폴드할 꽝 핸드가 사라지기 때문입니다.\\n3. **블러프 캐칭(콜)할 때**: 상대의 블러프 카드를 블락하지 말고, 순수하게 언블락 상태여야 상대가 블러프를 시도했을 확률이 높아집니다.`;
    } else if (qLower.includes('mdf') || qLower.includes('최소 방어')) {
      return `**[GTO Wizard 이론팀 해설]**\\n\\n**MDF (Minimum Defense Frequency)**는 상대가 아무 카드로나 블러프를 쳐서 '자동 수익(공짜 돈)'을 내지 못하도록 방어해야 하는 이론적 하한선입니다.\\n\\n- 공식: MDF = 팟 사이즈 / (팟 사이즈 + 베팅 금액)\\n- 예시: 100칩 팟에 상대가 50칩(하프팟)을 베팅하면 100 / (100 + 50) = 66.7%를 최소한 콜 또는 레이스로 방어해야 합니다.\\n- ⚠️ **주의사항**: 보드에 상대의 너트 우위가 극심할 때는 MDF를 문자 그대로 지키려다 스택이 털릴 수 있습니다. 실전 솔버는 텍스처에 따라 오버폴드(Overfold)를 자주 지시합니다.`;
    } else if (qLower.includes('icm') || qLower.includes('토너먼트')) {
      return `**[토너먼트 스페셜리스트 조언]**\\n\\n토너먼트 파이널 테이블이나 버블에서는 **ChipEV(칩 기대값)**로 생각하면 패망합니다. 반드시 **$EV(실제 상금 가치)**로 접근해야 합니다:\\n\\n- **칩의 비대칭성**: 칩을 딸 때 얻는 가치보다 칩을 잃을 때 날아가는 상금 가치가 훨씬 큽니다.\\n- **리스크 프리미엄**: 칩리더를 상대로는 AKs나 QQ 같은 프리미엄 핸드조차 뒤의 숏스택 탈락을 기다리기 위해 눈물을 머금고 폴드해야 하는 순간이 있습니다.`;
    } else {
      return `**[AI 포커 코치 조언]**\\n\\n질문해 주신 '${q}'에 대한 GTO 전략 관점의 조언입니다:\\n\\n포커 의사결정의 핵심은 언제나 **[레인지 vs 레인지의 상호작용]**입니다. 단 한 장의 내 카드가 아닌, 상대의 전체 레인지와 내 전체 레인지가 현재 보드 텍스처에서 어떤 에퀴티 분포를 가지는지를 먼저 파악하세요.\\n\\n- 내가 **너트 우위**를 가지면? 👉 큰 벳(75%+)이나 오버벳으로 압박\\n- 내가 **레인지 우위**만 가지면? 👉 작은 벳(25~33%)으로 넓은 빈도 공격\\n- 상대가 너트 우위를 점하면? 👉 첵백 빈도를 높여 팟 컨트롤`;
    }
  },

  appendMessage(role, text, id = null) {
    const div = document.createElement('div');
    div.className = `ai-msg ${role}`;
    if (id) div.id = id;
    div.innerHTML = text.replace(/\\n/g, '<br>');
    this.messagesArea.appendChild(div);
  },

  scrollToBottom() {
    this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
  }
};

// ==========================================
// 📝 6개 차수 전직 심사 시험 문제 데이터베이스 (총 30문항)
// ==========================================
const EXAM_DATABASE = {
  1: [ // 1차 전직: 홀덤펍 레귤러 (프리플랍 포지션 & 팟오즈)
    {
      question: "6-Max 캐시게임에서 장기적으로 가장 많은 수익을 창출하는 '절대적인 인포지션(IP)' 포지션은?",
      context: "6-Max 테이블: UTG - MP - CO - BTN - SB - BB",
      options: ["UTG (언더더건)", "MP (미들포지션)", "BTN (버튼)", "SB (스몰블라인드)"],
      correct: 2,
      explanation: "버튼(BTN)은 플랍, 턴, 리버의 모든 스트리트에서 가장 마지막으로 액션하므로 정보 우위를 극대화할 수 있는 최고의 자리입니다."
    },
    {
      question: "현재 팟에 100칩이 있고, 상대가 50칩을 베팅했습니다. 콜(50칩)하기 위해 필요한 최소한의 승률(팟 오즈)은 얼마인가요?",
      context: "팟: 100 | 상대 베팅: 50 | 내 콜 필요액: 50",
      options: ["20.0%", "25.0%", "33.3%", "50.0%"],
      correct: 1,
      explanation: "팟 오즈 = 콜 금액 / (최종 팟 총합) = 50 / (100 + 50 + 50) = 50 / 200 = 25%입니다. 즉 4번 중 1번 이상 승리하면 본전 이상의 콜입니다."
    },
    {
      question: "UTG에서 포켓 에이스(AA)를 받았습니다. 현대 GTO 전략에서 가장 권장되는 기본 오픈 액션은 무엇인가요?",
      context: "핸드: A♠ A♦ | 포지션: UTG | 스택: 100bb",
      options: ["상대를 속이기 위해 1bb로 림프(체크)한다.", "표준 사이즈인 2~2.5bb로 정상 오픈 레이즈한다.", "팟의 10배로 거대하게 레이즈하여 팟을 즉시 먹는다.", "프리플랍 100bb 올인을 박는다."],
      correct: 1,
      explanation: "솔버는 림프를 거의 사용하지 않습니다. AA와 같은 몬스터 핸드도 다른 오픈 레인지와 밸런스를 맞추어 표준 사이징(2~2.5bb)으로 오픈하여 팟을 빌딩합니다."
    },
    {
      question: "앞선 루즈한 플레이어 2명이 1bb씩 림프(Limp)하고 지나갔습니다. BTN에서 강력한 핸드로 취해야 할 정석 플레이는?",
      context: "상황: UTG 림프, MP 림프 | 내 포지션: BTN | 핸드: A♠ Q♣",
      options: ["나도 1bb만 내고 편안하게 같이 림프한다.", "약한 림퍼들을 격리(Isolation)하기 위해 4~5bb로 레이즈한다.", "림프가 나왔으므로 안전하게 폴드한다.", "상대의 패를 보고 결정한다."],
      correct: 1,
      explanation: "림퍼들의 캡된 약한 레인지를 상대로 인포지션에서 주도권을 잡고 팟을 독점하기 위해 3bb + (림퍼당 1bb) = 약 5bb 수준의 아이솔레이션 레이즈가 필수입니다."
    },
    {
      question: "플랍에서 넛 플러시 드로우(스페이드 4장 완성 대기)가 있습니다. 턴이나 리버에서 플러시를 완성시킬 수 있는 아웃츠(Outs)는 몇 장인가요?",
      context: "보드: K♠ 7♠ 2♦ | 내 핸드: A♠ 5♠",
      options: ["4장", "8장", "9장", "11장"],
      correct: 2,
      explanation: "한 무늬는 총 13장이며, 내 손의 2장과 플랍의 2장을 제외한 덱 속 9장의 스페이드가 플러시 아웃츠가 됩니다."
    }
  ],
  2: [ // 2차 전직: 마이크로 그라인더 (플랍 C-bet & 보드 텍스처)
    {
      question: "A♠ 7♦ 2♣ 드라이(Dry) 보드에서 BTN 오픈 레이저가 BB를 상대로 가장 선호하는 GTO C-bet 전략은?",
      context: "보드: A♠ 7♦ 2♣ (레인보우) | BTN 오픈 vs BB 디펜스",
      options: ["전체 레인지로 첵백한다.", "1/3팟의 작은 사이징으로 레인지 전체(80~100%) 고빈도 C-bet을 한다.", "팟의 200% 오버벳을 감행한다.", "상대가 체크했으므로 무조건 팟사이즈 벳을 한다."],
      correct: 1,
      explanation: "드라이한 A-high 보드는 프리플랍 레이저(PFR)에게 압도적인 레인지 우위가 있습니다. 1/3팟 작은 베팅만으로도 상대의 수많은 에어 핸드를 효율적으로 폴드시킬 수 있습니다."
    },
    {
      question: "T♠ 9♠ 8♦ 처럼 스트레이트와 플러시 드로우가 가득한 웻(Wet) 보드에서 PFR이 체크백 빈도를 높여야 하는 주된 이유는?",
      context: "보드: T♠ 9♠ 8♦ | 프리플랍 레이저 vs BB 콜러",
      options: ["레이크가 높아서 팟을 줄이려고", "BB의 디펜스 레인지가 보드와 강력하게 맞물려 너트 우위를 위협하기 때문에", "웻 보드에서는 블러프를 절대 칠 수 없어서", "상대가 플랍에 무조건 올인하기 때문에"],
      correct: 1,
      explanation: "수티드 커넥터와 미들 콤보가 많은 BB의 콜링 레인지가 웻 보드에서 스트레이트, 투페어, 강한 드로우를 대거 완성하므로, PFR은 첵백으로 팟을 컨트롤해야 합니다."
    },
    {
      question: "'레인지 우위(Range Advantage)'와 '너트 우위(Nut Advantage)'의 올바른 설명은?",
      context: "GTO 핵심 보드 분석 이론",
      options: ["두 개념은 사실상 동일한 포커 용어이다.", "레인지 우위는 전체 에퀴티(평균 승률)의 우세이고, 너트 우위는 최상위 몬스터 핸드 콤보의 우세이다.", "너트 우위가 있으면 무조건 작은 벳만 해야 한다.", "레인지 우위는 칩 스택이 많은 사람이 가진다."],
      correct: 1,
      explanation: "레인지 우위는 작은 벳을 자주 칠 수 있는 근거가 되며, 너트 우위는 큰 벳이나 오버벳을 감행할 수 있는 이론적 기반이 됩니다."
    },
    {
      question: "플랍 C-bet에 직면했을 때, 첵-콜(Check-Call) 라인을 타는 플레이어의 레인지는 일반적으로 어떻게 평가되나요?",
      context: "포스트플랍 레인지 구조 분석",
      options: ["절대적으로 무적의 너트만 있는 레인지", "몬스터 핸드가 상당수 배제된 '캡(Capped)된 미디엄 스트렝스' 레인지", "100% 아무것도 없는 순수 블러프 에어 핸드", "아무런 규칙성이 없는 랜덤 레인지"],
      correct: 1,
      explanation: "플랍에서 레이즈를 하지 않고 첵콜만 했다는 것은 강한 핸드(투페어, 셋)를 뺐을 확률이 높아 레인지의 상한선이 제한(Capped)되었다고 봅니다."
    },
    {
      question: "BB에서 플랍 1/3 C-bet을 맞았을 때, 언더페어(예: 88 on K-7-3r)나 백도어 드로우가 있는 핸드로 올바른 대처는?",
      context: "보드: K♦ 7♣ 3♠ | 상대 베팅: 1/3팟 | 내 핸드: 8♠ 8♥",
      options: ["즉시 올인으로 상대를 밀어낸다.", "좋은 팟오즈(1:4)와 쇼다운 밸류를 고려해 콜로 디펜스하며 턴을 본다.", "K이 깔렸으므로 1초의 망설임도 없이 폴드한다.", "딜러에게 카드를 바꿔달라고 요청한다."],
      correct: 1,
      explanation: "1/3팟 베팅에는 80% 이상의 MDF 방어가 필요하며, 상대의 플랍 블러프를 이기고 있는 포켓 페어는 안정적인 콜 디펜스 핸드입니다."
    }
  ],
  3: [ // 3차 전직: 로우스테이크 크러셔 (턴 배럴링 & MDF 공식)
    {
      question: "MDF(Minimum Defense Frequency, 최소 방어 빈도)의 올바른 수학 공식은?",
      context: "게임 이론적 최적 방어 수식",
      options: ["베팅 금액 / 팟 사이즈", "팟 사이즈 / (팟 사이즈 + 베팅 금액)", "베팅 금액 / (팟 사이즈 + 베팅 금액)", "(팟 사이즈 - 베팅 금액) / 팟 사이즈"],
      correct: 1,
      explanation: "MDF = Pot / (Pot + Bet) 입니다. 상대가 아무 카드로나 블러프를 쳐서 즉각적인 무위험 수익을 내지 못하도록 차단하는 최소 방어 빈도입니다."
    },
    {
      question: "팟이 100칩인 상황에서 상대가 50칩(하프 팟)을 베팅했습니다. 이론상 내가 방어(콜 또는 레이즈)해야 하는 최소 빈도(MDF)는?",
      context: "팟: 100 | 베팅: 50 | MDF 계산",
      options: ["50.0%", "66.7%", "75.0%", "80.0%"],
      correct: 1,
      explanation: "MDF = 100 / (100 + 50) = 100 / 150 = 약 66.7%입니다. 최소 66.7%의 핸드로 방어해야 상대의 100% 빈도 블러프를 차단합니다."
    },
    {
      question: "플랍 C-bet 이후, 턴에서 더블 배럴 블러프를 날리기에 가장 이상적인 스케어 카드는?",
      context: "플랍: J♠ 8♦ 3♣ | 턴 카드 출현",
      options: ["상대의 미들페어와 투페어를 완성시켜주는 8 무늬", "PFR의 레인지를 강력하게 강화하는 A♠ 또는 K♦", "아무 영향이 없는 블랭크 2♥", "상대방의 셋을 만드는 3♦"],
      correct: 1,
      explanation: "A나 K 같은 하이 오버카드는 프리플랍 레이저의 오픈 레인지에 압도적으로 많이 포함되어 있어, 상대방의 플랍 첵콜 레인지(J, 8 페어)를 강하게 얼어붙게 만듭니다."
    },
    {
      question: "플랍에 첵백한 뒤 턴에서 상대가 다시 체크했을 때, 인포지션에서 베팅하는 전략을 무엇이라 부르나요?",
      context: "포스트플랍 턴 전략 용어",
      options: ["슬로우 플레이 (Slow Play)", "딜레이드 C-bet (Delayed C-bet)", "동크 벳 (Donk Bet)", "스퀴즈 (Squeeze)"],
      correct: 1,
      explanation: "플랍 첵백 후 턴에서 베팅하는 것을 Delayed C-bet이라고 하며, 상대의 패시브함을 공략하고 마지널 핸드의 밸류를 추출하는 강력한 무기입니다."
    },
    {
      question: "턴 보드에 서드 플러시나 4스트레이트가 완성되었습니다. 탑페어 위크키커를 쥔 인포지션 플레이어의 올바른 행동은?",
      context: "보드: Q♠ J♠ T♦ 9♣ | 내 핸드: Q♥ 6♥",
      options: ["팟 전체 올인을 친다.", "첵백으로 팟을 컨트롤하며 쇼다운 밸류를 보존한다.", "무조건 즉시 카드를 오픈하고 포기한다.", "상대에게 칩을 레이즈한다."],
      correct: 1,
      explanation: "보드가 극단적으로 웻해져 수많은 핸드에게 역전당했을 때는 팟을 키우지 않고 첵백으로 저렴하게 쇼다운을 보는 팟 컨트롤이 필수입니다."
    }
  ],
  4: [ // 4차 전직: 미드스테이크 프로 (블로커/언블로커 & 블러프 캐칭)
    {
      question: "리버에서 트리플 배럴 블러프를 시도할 때, 가장 이상적인 핸드의 블로커 조합은?",
      context: "리버 블러프 콤보 선정 원리",
      options: ["상대가 콜할 최강 핸드를 블락하고, 상대가 실패해서 폴드할 드로우 카드는 언블락(Unblock)함", "상대가 미스해서 무조건 폴드할 꽝 카드를 내가 잔뜩 쥐고 있음", "상대의 너트 플러시 카드를 전혀 블락하지 않음", "아무 무늬나 상관없이 가장 낮은 카드"],
      correct: 0,
      explanation: "상대가 폴드해야 할 카드(Busted Draw)를 내가 들고 있으면 상대가 폴드할 콤보가 사라집니다. 따라서 상대 콜링 레인지를 블락하고 폴드 레인지를 언블락해야 성공률이 극대화됩니다."
    },
    {
      question: "리버에서 상대의 팟 사이즈 베팅을 상대로 블러프 캐칭(콜)할 때 가장 좋은 카드는?",
      context: "블러프 캐쳐 핸드 인스펙션",
      options: ["상대의 밸류 핸드(스트레이트/플러시)를 블락하고, 상대의 실패한 드로우를 언블락한 핸드", "상대의 미스한 드로우 카드를 내가 두 장 다 쥐고 있는 핸드", "보드에 없는 무늬의 2와 3", "상대의 에어 핸드만 블락한 핸드"],
      correct: 0,
      explanation: "상대가 밸류로 베팅할 조합을 내가 차단(Block)해야 상대가 블러프를 쳤을 확률이 통계적으로 높아지므로, 밸류 블락 + 드로우 언블락이 최적의 캐쳐입니다."
    },
    {
      question: "리버에서 팟 사이즈(100% 팟) 베팅을 할 때, GTO 균형을 달성하기 위한 밸류 핸드와 블러프 핸드의 최적 비율은?",
      context: "리버 내시 균형 벳 레인지 비율",
      options: ["밸류 50% : 블러프 50% (1:1)", "밸류 67% : 블러프 33% (2:1)", "밸류 90% : 블러프 10% (9:1)", "블러프 75% : 밸류 25%"],
      correct: 1,
      explanation: "상대에게 100을 따기 위해 100을 콜해야 하는 2:1의 팟오즈(필요 승률 33.3%)를 줄 때, 내 레인지에 블러프가 정확히 33.3% 섞여 있어야 상대의 콜과 폴드 EV가 0으로 균형을 이룹니다."
    },
    {
      question: "'씬 밸류 벳(Thin Value Bet)'을 감행할 수 있는 이론적 타당성의 기준은?",
      context: "리버 밸류 베팅 마진",
      options: ["상대가 100% 무조건 콜해줄 때만", "상대가 내 베팅에 '콜을 주는 레인지'에 대해 내가 50% 이상 이기고 있을 때", "상대가 폴드할 확률이 95% 이상일 때", "내 스택이 팟보다 적을 때"],
      correct: 1,
      explanation: "상대가 폴드하는 패는 고려하지 않고, '콜을 주는 레인지'를 상대로 50%를 초과하는 에퀴티가 있다면 첵백보다 베팅하는 것이 장기적으로 +EV입니다."
    },
    {
      question: "BB의 캡된(Capped) 레인지를 상대로 인포지션 프로가 구사하는 가장 파괴적인 전술은?",
      context: "레인지 비대칭성을 이용한 공격",
      options: ["상대와 똑같이 첵-체크로 넘어간다.", "상대가 가질 수 없는 너트 우위를 바탕으로 턴과 리버에 걸쳐 큰 사이징과 오버벳으로 압박한다.", "무조건 스몰 벳(10%)만 친다.", "안전하게 쇼다운을 본다."],
      correct: 1,
      explanation: "상대의 레인지 상한선이 제한되어 몬스터 핸드가 없을 때, 공격자는 오버벳을 통해 상대의 미디엄 콤보들에게 극심한 인디퍼런트 고통을 강요할 수 있습니다."
    }
  ],
  5: [ // 5차 전직: 하이롤러 위저드 (지오메트릭 사이징 & 믹스드 솔루션)
    {
      question: "플랍, 턴, 리버에 걸쳐 스택을 고른 팟 비율로 배분하여 리버 올인을 완성하는 수학적 사이징을 무엇이라 하나요?",
      context: "스택-투-팟 비율(SPR) 최적화 이론",
      options: ["아리스메틱(산술) 사이징", "지오메트릭(Geometric, 기하학적) 벳 사이징", "마틴게일 사이징", "하프팟 고정 사이징"],
      correct: 1,
      explanation: "지오메트릭 사이징은 각 스트리트마다 동일한 비율(예: 70% - 70% - 70%)로 팟을 키워 정확히 리버에 모든 스택을 투입하는 솔버의 대표적인 스택 소진 기법입니다."
    },
    {
      question: "솔버 출력 결과에서 특정 핸드가 'Call 55%, Raise 45%'처럼 믹스드(혼합) 빈도를 보일 때의 정확한 이론적 의미는?",
      context: "게임 이론 내시 균형(Nash Equilibrium)",
      options: ["솔버가 어떤 패를 낼지 몰라 혼란에 빠졌다는 뜻이다.", "Call과 Raise 두 액션의 기대값(EV)이 정확하게 동일하다는 뜻이다.", "무조건 레이스가 유리하다는 뜻이다.", "카드의 무늬가 마음에 들지 않는다는 뜻이다."],
      correct: 1,
      explanation: "내시 균형에서 두 전략의 EV가 완전히 같을 때(Indifferent), 상대방이 한쪽으로 착취(Exploit)하지 못하도록 특정 빈도로 섞어서 플레이합니다."
    },
    {
      question: "솔버가 플랍이나 턴에서 200% 이상의 극단적 오버벳(Overbet)을 감행하는 보드 조건은?",
      context: "오버벳 노드 발생 원리",
      options: ["내 레인지에 압도적인 '너트 우위(Nut Advantage)'가 있고 상대는 캡되어 있을 때", "양쪽 모두 강한 패가 전혀 없을 때", "보드에 A가 깔리지 않았을 때", "블라인드가 상승했을 때"],
      correct: 0,
      explanation: "오버벳은 내가 최강 너트 콤보를 독점하고 상대는 결코 너트를 가질 수 없을 때 발생하며, 상대의 블러프 캐쳐들에게 최대의 수학적 압박을 가합니다."
    },
    {
      question: "포커 솔버에서 '노드 락킹(Node Locking)' 기능의 주요 용도는 무엇인가요?",
      context: "GTO 솔버 심화 익스플로잇 기법",
      options: ["솔버의 CPU 사용량을 100%로 고정하는 기능", "특정 상대의 릭(과도한 폴드, 부족한 블러프 등)을 고정하고 그에 대한 완벽한 극대화 착취(Exploit) 전략을 산출하는 기능", "포커 테이블 좌석을 예약하는 기능", "프리플랍 레인지를 잠그는 기능"],
      correct: 1,
      explanation: "완전한 GTO 대 GTO가 아닌, 실전 상대의 편향된 실수(Leak)를 한 노드에 고정하여 최대의 이익을 뽑아내는 실전 프로들의 필수 연구 도구입니다."
    },
    {
      question: "플레이어 3명 이상이 참여한 멀티웨이(Multiway) 팟에서 솔버의 전반적인 전략 변화는?",
      context: "Multiway GTO 전략 특성",
      options: ["헤즈업보다 훨씬 공격적으로 변하며 블러프 빈도가 3배로 증가한다.", "에퀴티 실현의 방해와 블러프 성공률 급락으로 인해 베팅 빈도가 대폭 감소하고 패시브해진다.", "무조건 오버벳 올인을 날린다.", "헤즈업 솔루션과 100% 동일하게 진행한다."],
      correct: 1,
      explanation: "플레이어가 많아질수록 누군가 몬스터 핸드를 쥐었을 확률이 극적으로 높아지므로, 멀티웨이에서는 블러프가 줄어들고 퓨어한 밸류 위주로 정직하게 전환됩니다."
    }
  ],
  6: [ // 6차 전직: WSOP 레전드 챔피언 (극강의 ICM & 토너먼트 마스터리)
    {
      question: "토너먼트 ICM에서 '버블 팩터(Bubble Factor)'의 근본적인 의미는 무엇인가요?",
      context: "ICM(Independent Chip Model) 수학",
      options: ["칩 스택이 거품처럼 늘어나는 비율", "칩을 획득할 때 증가하는 달러($EV) 가치 대비, 칩을 잃을 때 감소하는 달러($EV) 손실의 위험 배율", "토너먼트 토탈 참가자 수의 변동치", "파이널 테이블의 테이블 매너 지수"],
      correct: 1,
      explanation: "상금 계단과 탈락 리스크 때문에 토너먼트에서는 1칩을 딸 때의 상금 가치보다 1칩을 잃을 때 날아가는 상금 가치가 훨씬 큽니다. 이 비대칭 배율이 버블 팩터입니다."
    },
    {
      question: "파이널 테이블 버블 상황에서 빅스택(칩리더)이 취해야 할 가장 지배적인 ICM 전략은?",
      context: "WSOP 파이널 테이블 칩리더 전략",
      options: ["탈락이 두려워 조용히 폴드만 한다.", "탈락 위험으로 인해 극도로 위축된 미들스택들을 상대로 무자비한 오픈과 3벳으로 블라인드를 난타 착취(Abuse)한다.", "숏스택에게 칩을 기부하여 버블을 길게 끈다.", "매 핸드마다 100% 올인을 박는다."],
      correct: 1,
      explanation: "미들스택은 뒤에 숏스택 탈락을 기다려 상금 점프를 노려야 하므로 빅스택에게 무조건 폴드해야 하는 극심한 ICM 족쇄에 묶여 있습니다. 빅스택은 이를 무자비하게 착취합니다."
    },
    {
      question: "토너먼트 숏스택(10~12bb) 상황에서 '내시 균형 푸시/폴드(Push/Fold)' 차트의 핵심 목표는?",
      context: "숏스택 수학적 생존 전략",
      options: ["포스트플랍 복잡한 승부를 피하고, 폴드 에퀴티와 데드머니(블라인드+앤티)를 즉시 회수하여 상금 EV를 극대화함", "모든 승부를 순수 운에 맡김", "상대에게 유리한 팟오즈를 선물함", "토너먼트를 빨리 끝내기 위함"],
      correct: 0,
      explanation: "숏스택에서는 플랍 이후 마진이 없으므로, 프리플랍 올인을 통해 상대의 폴드를 이끌어내고 테이블의 데드머니를 회수하는 것이 유일한 수학적 최적해입니다."
    },
    {
      question: "토너먼트 헤즈업(Heads-up)에서 BTN/SB 포지션의 이상적인 프리플랍 참여 빈도는?",
      context: "헤즈업 GTO 마스터리",
      options: ["타이트하게 상위 25% 핸드로만 참여한다.", "75~85% 이상의 광범위한 핸드로 미니레이즈와 림프를 믹싱하여 팟을 주도한다.", "100% 무조건 올인만 선택한다.", "BB에게 항상 양보한다."],
      correct: 1,
      explanation: "헤즈업에서는 버튼이 포스트플랍 절대적 인포지션을 가지므로, 80% 안팎의 극도로 넓은 레인지로 공격적으로 참여하는 것이 표준입니다."
    },
    {
      question: "WSOP 파이널 3인 상황: 숏스택이 2bb로 다음 핸드 탈락 직전인데, 미들스택인 내가 빅스택의 올인을 상대로 AKs를 쥐었습니다. 올바른 ICM 판단은?",
      context: "전설적인 WSOP ICM 수어사이드 방지 스팟",
      options: ["AKs는 최강 핸드이므로 1초의 고민도 없이 스냅 콜한다.", "순수 칩으로는 콜이지만, 숏스택 탈락 시 확정되는 수억 원의 2위 보장 상금($EV)을 위해 눈물을 머금고 폴드할 수 있어야 한다.", "동전을 던져 결정한다.", "타임아웃으로 자동 폴드되길 기다린다."],
      correct: 1,
      explanation: "ChipEV로는 이길 확률이 높더라도, 콜해서 탈락하면 3위 상금에 그치지만 폴드하면 숏스택 탈락으로 확정 상금 점프가 보장되는 전형적인 ICM 스팟에서는 극단적 오버폴드가 정답입니다."
    }
  ]
};

// ==========================================
// 📜 퀘스트 매니저 (성장 미션 & 6구간 전직 현황)
// ==========================================
const questManager = {
  openModal() {
    this.render();
    const modal = document.getElementById('quest-modal-overlay');
    if (modal) modal.style.display = 'flex';
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  closeModal() {
    const modal = document.getElementById('quest-modal-overlay');
    if (modal) modal.style.display = 'none';
  },

  render() {
    const u = app.userState;
    const lvlInfo = app.getLevelInfo(u.xp);
    const body = document.getElementById('quest-modal-body');
    if (!body) return;

    const curLvl = lvlInfo.level;
    const nextLvl = Math.min(100, curLvl + 1);
    const curXp = u.xp;

    // 지정 필수 미션 트랙 조회
    const missions = app.getCurriculumForLevel(curLvl);
    const reqArticles = missions.requiredArticles;
    const reqQuizzes = missions.requiredQuizzes;

    const completedArtsCount = reqArticles.filter(a => (u.completed_articles || []).includes(a.id || a.slug)).length;
    const completedQsCount = reqQuizzes.filter(q => (u.completed_quizzes || []).includes(q.id)).length;
    const allMissionsComplete = (completedArtsCount === reqArticles.length) && (completedQsCount === reqQuizzes.length);

    const targetRanges = Math.min(15, Math.max(2, Math.ceil(curLvl * 0.2)));
    const exploredRangesCount = (u.explored_ranges || []).length;
    const rangePct = Math.min(100, Math.round((exploredRangesCount / targetRanges) * 100));

    const needsExam = lvlInfo.needsExam;

    let promoBannerHtml = '';
    if (needsExam) {
      const examTier = PROMOTION_TIERS[needsExam];
      promoBannerHtml = `
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(234, 88, 12, 0.25)); border: 2px solid #f59e0b; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: center; box-shadow: 0 8px 20px rgba(245, 158, 11, 0.25);">
          <div style="font-size: 2.2rem; margin-bottom: 0.25rem; animation: pulseGlow 1.5s infinite ease-in-out;">⚡</div>
          <h3 style="font-size: 1.25rem; font-weight: 800; color: #fbbf24; margin-bottom: 0.4rem;">
            ${examTier.examTitle} 자격 획득!
          </h3>
          <p style="font-size: 0.88rem; color: var(--text-main); margin-bottom: 1rem; line-height: 1.5;">
            Lv.${examTier.targetLevel}에 도달하셨습니다! 5문항의 실전 스팟 테스트 중 4문항 이상 통과 시 <strong>[${examTier.name}]</strong> 칭호 승급 및 <strong>+${examTier.bonusXP} XP</strong> 특전을 획득합니다!
          </p>
          <button onclick="questManager.closeModal(); promotionManager.openExamModal(${needsExam})" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: 800; font-size: 0.95rem; border: none; padding: 0.75rem 2rem; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);">
            📝 지금 전직 심사 시험 응시하기 ➔
          </button>
        </div>
      `;
    }

    body.innerHTML = `
      <!-- User Current Status Card -->
      <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 0.75rem;">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 2.2rem;">${u.avatar || '🦈'}</div>
            <div>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <strong style="font-size: 1.15rem; color: var(--text-main);">${u.name || '포커신동'}</strong>
                <span class="rank-badge ${lvlInfo.tier.badgeClass}">${lvlInfo.tier.badge}</span>
              </div>
              <span style="font-size: 0.85rem; color: #60a5fa; font-weight: 700;">Lv.${curLvl} / 100</span>
            </div>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 0.8rem; color: var(--text-dim); display: block;">누적 경험치</span>
            <strong style="font-size: 1.1rem; color: #fbbf24;">${curXp} XP</strong>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.35rem;">
          <span>Lv.${curLvl} 진행도</span>
          <span>${lvlInfo.remainingXp > 0 ? `다음 레벨까지 ${lvlInfo.remainingXp} XP 남음` : '만렙 달성 👑'}</span>
        </div>
        <div style="width: 100%; height: 8px; background: rgba(0,0,0,0.3); border-radius: 4px; overflow: hidden;">
          <div style="width: ${lvlInfo.progressPct}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #38bdf8); border-radius: 4px;"></div>
        </div>
      </div>

      ${promoBannerHtml}

      <!-- Quest Requirements Section -->
      <div style="margin-bottom: 1.75rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.85rem;">
          <div>
            <h4 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin: 0 0 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
              <span>🎯</span> Lv.${curLvl} ➔ Lv.${nextLvl} 레벨업 필수 지정 미션
            </h4>
            <p style="font-size: 0.82rem; color: #60a5fa; margin: 0; font-weight: 700;">
              ✨ ${missions.title}
            </p>
          </div>
          <div>
            ${allMissionsComplete ? `
              <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 12px; border-radius: 14px; font-size: 0.82rem; font-weight: 800;">
                🎉 필수 미션 모두 완료!
              </span>
            ` : `
              <span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 4px 12px; border-radius: 14px; font-size: 0.82rem; font-weight: 800;">
                ⏳ 미션 진행 중 (${completedArtsCount}/${reqArticles.length} 아티클, ${completedQsCount}/${reqQuizzes.length} 퀴즈)
              </span>
            `}
          </div>
        </div>

        <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1.15rem; font-size: 0.82rem; color: #93c5fd; line-height: 1.5;">
          💡 <strong>순차 레벨업 규칙</strong>: 레벨업을 위해서는 경험치(XP)뿐만 아니라, 현재 레벨에 <strong>지정된 필수 아티클과 스팟 퀴즈를 모두 완료</strong>해야 다음 레벨로 승급합니다.
        </div>

        <!-- Mission 1: Specific Required Articles -->
        <div style="background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 14px; padding: 1.15rem; margin-bottom: 1.15rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.65rem;">
            <div style="display: flex; align-items: center; gap: 0.45rem;">
              <span style="font-size: 1.3rem;">📖</span>
              <strong style="font-size: 0.96rem; color: var(--text-main);">지정 필수 GTO 아티클</strong>
            </div>
            <span style="font-size: 0.82rem; font-weight: 800; color: ${completedArtsCount === reqArticles.length ? '#34d399' : '#fbbf24'};">
              ${completedArtsCount} / ${reqArticles.length} 완독
            </span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.65rem;">
            ${reqArticles.map(a => {
              const isDone = (u.completed_articles || []).includes(a.id || a.slug);
              return `
                <div style="background: ${isDone ? 'rgba(16, 185, 129, 0.06)' : 'rgba(0,0,0,0.12)'}; border: 1px solid ${isDone ? 'rgba(16, 185, 129, 0.35)' : 'var(--border-color)'}; border-radius: 10px; padding: 0.75rem 0.9rem; display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                  <div style="flex: 1; min-width: 220px;">
                    <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.25rem;">
                      <span style="font-size: 0.95rem;">${isDone ? '✅' : '⏳'}</span>
                      <span style="font-size: 0.72rem; color: var(--text-dim); background: rgba(59, 130, 246, 0.12); padding: 1px 6px; border-radius: 6px;">${a.category || '이론'}</span>
                      <span style="font-size: 0.72rem; color: #fbbf24; font-weight: 700;">+50 XP</span>
                    </div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: var(--text-main); line-height: 1.4;">${a.title_ko || a.title}</div>
                  </div>
                  <div>
                    ${isDone ? `
                      <button onclick="questManager.closeModal(); reader.openArticle('${a.id || a.slug}')" class="btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 700;">
                        다시 읽기
                      </button>
                    ` : `
                      <button onclick="questManager.closeModal(); reader.openArticle('${a.id || a.slug}')" class="btn-primary" style="padding: 0.45rem 1rem; font-size: 0.82rem; font-weight: 800; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);">
                        📖 지금 읽기 ➔
                      </button>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Mission 2: Specific Required Spot Quizzes -->
        <div style="background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 14px; padding: 1.15rem; margin-bottom: 1.15rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.65rem;">
            <div style="display: flex; align-items: center; gap: 0.45rem;">
              <span style="font-size: 1.3rem;">🎯</span>
              <strong style="font-size: 0.96rem; color: var(--text-main);">지정 필수 실전 스팟 퀴즈</strong>
            </div>
            <span style="font-size: 0.82rem; font-weight: 800; color: ${completedQsCount === reqQuizzes.length ? '#34d399' : '#fbbf24'};">
              ${completedQsCount} / ${reqQuizzes.length} 정답
            </span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.65rem;">
            ${reqQuizzes.map(q => {
              const isDone = (u.completed_quizzes || []).includes(q.id);
              return `
                <div style="background: ${isDone ? 'rgba(16, 185, 129, 0.06)' : 'rgba(0,0,0,0.12)'}; border: 1px solid ${isDone ? 'rgba(16, 185, 129, 0.35)' : 'var(--border-color)'}; border-radius: 10px; padding: 0.75rem 0.9rem; display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                  <div style="flex: 1; min-width: 220px;">
                    <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.25rem;">
                      <span style="font-size: 0.95rem;">${isDone ? '✅' : '⏳'}</span>
                      <span style="font-size: 0.72rem; color: var(--text-dim); background: rgba(245, 158, 11, 0.12); padding: 1px 6px; border-radius: 6px;">${q.street || 'Preflop'} • ${q.category || '스팟'}</span>
                      <span style="font-size: 0.72rem; color: #fbbf24; font-weight: 700;">+50 XP</span>
                    </div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: var(--text-main); line-height: 1.4;">${q.title}</div>
                  </div>
                  <div>
                    ${isDone ? `
                      <button onclick="questManager.closeModal(); trainer.openQuizById('${q.id}')" class="btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 700;">
                        다시 풀기
                      </button>
                    ` : `
                      <button onclick="questManager.closeModal(); trainer.openQuizById('${q.id}')" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; padding: 0.45rem 1rem; font-size: 0.82rem; font-weight: 800; border-radius: 8px; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);">
                        🎯 퀴즈 풀기 ➔
                      </button>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Mission 3: Matrix Exploration -->
        <div style="background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 14px; padding: 1rem 1.15rem; display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.3rem;">📊</span>
            <div>
              <strong style="font-size: 0.92rem; color: var(--text-main); display: block;">13x13 매트릭스 레인지 탐색</strong>
              <span style="font-size: 0.78rem; color: var(--text-dim);">포지션별 프리플랍/3벳 레인지 프리셋 인스펙션 (+20 XP)</span>
            </div>
          </div>
          <button onclick="questManager.closeModal(); app.navigate('matrix')" class="btn-secondary" style="padding: 0.4rem 0.85rem; font-size: 0.8rem; font-weight: 700; white-space: nowrap;">
            매트릭스 보기 ➔
          </button>
        </div>
      </div>

      <!-- 6-Stage Promotion Career Overview -->
      <div>
        <h4 style="font-size: 1.05rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.85rem; display: flex; align-items: center; gap: 0.4rem;">
          <span>⚔️</span> 6구간 전직 로드맵 현황
        </h4>

        <div class="promotion-step-grid">
          ${PROMOTION_TIERS.slice(1).map(pt => {
            const isPassed = (u.promotions_passed || []).includes(pt.tier);
            const isTarget = (needsExam === pt.tier);
            const isLocked = !isPassed && !isTarget;

            return `
              <div class="promo-step-card ${isPassed ? 'unlocked' : ''} ${isTarget ? 'active-target' : ''}">
                <div style="font-size: 1.8rem; margin-bottom: 0.35rem;">${pt.icon}</div>
                <div style="font-size: 0.9rem; font-weight: 800; color: ${pt.color}; margin-bottom: 0.2rem;">
                  ${pt.name}
                </div>
                <span style="font-size: 0.72rem; color: var(--text-dim); display: block; margin-bottom: 0.4rem;">
                  목표: Lv.${pt.targetLevel}
                </span>
                <div style="font-size: 0.78rem; font-weight: 700; color: ${isPassed ? '#34d399' : (isTarget ? '#fbbf24' : '#64748b')};">
                  ${isPassed ? '✅ 전직 완료' : (isTarget ? '⚡ 시험 응시 가능!' : '🔒 레벨 미달')}
                </div>
                ${isTarget ? `
                  <button onclick="questManager.closeModal(); promotionManager.openExamModal(${pt.tier})" style="margin-top: 0.5rem; width: 100%; background: #f59e0b; color: #000; font-weight: 800; font-size: 0.75rem; border: none; padding: 0.35rem 0.5rem; border-radius: 6px; cursor: pointer;">
                    응시하기 ➔
                  </button>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }
};

// ==========================================
// ⚡ 전직 심사 시험 매니저 (Promotion Test Engine)
// ==========================================
const promotionManager = {
  currentTier: null,
  currentQuestionIndex: 0,
  score: 0,
  selectedIdx: null,

  openExamModal(tierNumber) {
    if (!tierNumber) {
      const info = app.getLevelInfo(app.userState.xp);
      tierNumber = info.needsExam || 1;
    }
    this.currentTier = tierNumber;
    this.currentQuestionIndex = 0;
    this.score = 0;
    this.selectedIdx = null;

    const modal = document.getElementById('promotion-modal-overlay');
    if (modal) modal.style.display = 'flex';
    this.renderQuestion();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  closeModal() {
    const modal = document.getElementById('promotion-modal-overlay');
    if (modal) modal.style.display = 'none';
  },

  getQuestions(tier) {
    return EXAM_DATABASE[tier] || EXAM_DATABASE[1];
  },

  renderQuestion() {
    const tierInfo = PROMOTION_TIERS[this.currentTier];
    const questions = this.getQuestions(this.currentTier);
    const q = questions[this.currentQuestionIndex];
    this.selectedIdx = null;

    const titleEl = document.getElementById('promo-modal-title');
    const subEl = document.getElementById('promo-modal-subtitle');
    const body = document.getElementById('promo-modal-body');

    if (titleEl) titleEl.innerText = `⚡ ${tierInfo.examTitle}`;
    if (subEl) subEl.innerText = `문제 ${this.currentQuestionIndex + 1} / ${questions.length} (4문제 이상 정답 시 전직 성공)`;

    body.innerHTML = `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
          <span style="font-size: 0.8rem; font-weight: 800; color: #f59e0b; background: rgba(245, 158, 11, 0.15); padding: 2px 8px; border-radius: 6px;">
            QUESTION ${this.currentQuestionIndex + 1} of 5
          </span>
          <span style="font-size: 0.8rem; color: var(--text-dim); font-weight: 700;">
            현재 점수: ${this.score} / ${this.currentQuestionIndex}
          </span>
        </div>

        <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.75rem; line-height: 1.45;">
          ${q.question}
        </h3>

        ${q.context ? `
          <div style="background: rgba(13, 56, 36, 0.4); border: 1px solid rgba(5, 150, 105, 0.3); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.9rem; color: #6ee7b7; font-family: monospace;">
            🃏 ${q.context}
          </div>
        ` : ''}

        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1rem;" id="exam-options-container">
          ${q.options.map((opt, i) => `
            <button class="exam-option-btn" onclick="promotionManager.selectAnswer(${i})">
              <span style="font-weight: 800; color: var(--text-dim); width: 20px;">${i + 1}.</span>
              <span>${opt}</span>
            </button>
          `).join('')}
        </div>

        <div id="exam-feedback-box" style="display: none; margin-top: 1.25rem; padding: 1rem; border-radius: 8px;"></div>
      </div>
    `;
  },

  selectAnswer(index) {
    if (this.selectedIdx !== null) return;
    this.selectedIdx = index;

    const questions = this.getQuestions(this.currentTier);
    const q = questions[this.currentQuestionIndex];
    const isCorrect = (index === q.correct);
    if (isCorrect) this.score++;

    const buttons = document.querySelectorAll('#exam-options-container .exam-option-btn');
    buttons.forEach((btn, i) => {
      btn.disabled = true;
      if (i === index) {
        btn.classList.add(isCorrect ? 'correct' : 'wrong');
      } else if (i === q.correct) {
        btn.classList.add('correct');
      }
    });

    const feedbackBox = document.getElementById('exam-feedback-box');
    if (feedbackBox) {
      feedbackBox.style.display = 'block';
      feedbackBox.style.background = isCorrect ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
      feedbackBox.style.border = isCorrect ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(239, 68, 68, 0.4)';
      feedbackBox.innerHTML = `
        <div style="font-weight: 800; font-size: 0.95rem; color: ${isCorrect ? '#34d399' : '#f87171'}; margin-bottom: 0.4rem;">
          ${isCorrect ? '🎉 정답입니다!' : '❌ 오답입니다.'}
        </div>
        <div style="font-size: 0.88rem; color: var(--text-main); line-height: 1.5; margin-bottom: 0.75rem;">
          💡 <strong>해설:</strong> ${q.explanation}
        </div>
        <div style="text-align: right;">
          <button onclick="promotionManager.nextQuestion()" class="btn-primary" style="padding: 0.5rem 1.25rem; font-weight: 800; font-size: 0.88rem;">
            ${this.currentQuestionIndex < 4 ? '다음 문제 풀기 ➔' : '최종 심사 결과 보기 ➔'}
          </button>
        </div>
      `;
    }

    if (window.app && app.playAudioEffect) {
      app.playAudioEffect(isCorrect ? 'correct' : 'wrong');
    }
  },

  nextQuestion() {
    this.currentQuestionIndex++;
    if (this.currentQuestionIndex < 5) {
      this.renderQuestion();
    } else {
      this.showResult();
    }
  },

  showResult() {
    const tierInfo = PROMOTION_TIERS[this.currentTier];
    const isPassed = (this.score >= 4);
    const body = document.getElementById('promo-modal-body');
    const u = app.userState;

    if (isPassed) {
      if (!u.promotions_passed) u.promotions_passed = [];
      if (!u.promotions_passed.includes(this.currentTier)) {
        u.promotions_passed.push(this.currentTier);
        app.addXP(tierInfo.bonusXP, 'general');
      }
      storage.save(u);
      app.updateUserBar();
      if (window.rankingManager && rankingManager.render) rankingManager.render();
      if (window.characterManager && characterManager.showToast) {
        characterManager.showToast(`👑 축하합니다! [${tierInfo.name}] 전직에 성공하셨습니다! (+${tierInfo.bonusXP} XP)`);
      }
      if (window.app && app.playAudioEffect) app.playAudioEffect('correct');
    }

    body.innerHTML = `
      <div style="text-align: center; padding: 2rem 1rem;">
        <div style="font-size: 4rem; margin-bottom: 0.75rem;">
          ${isPassed ? '🏆' : '📚'}
        </div>
        <h2 style="font-size: 1.6rem; font-weight: 800; color: ${isPassed ? '#fbbf24' : '#f87171'}; margin-bottom: 0.5rem;">
          ${isPassed ? `🎉 [${tierInfo.name}] 전직 심사 통과!` : '아쉽습니다! 불합격'}
        </h2>
        <p style="font-size: 1rem; color: var(--text-main); margin-bottom: 1.5rem;">
          최종 결과: 5문항 중 <strong>${this.score}문항</strong> 정답 (${Math.round((this.score / 5) * 100)}%)
        </p>

        ${isPassed ? `
          <div style="background: rgba(245, 158, 11, 0.12); border: 1.5px solid #f59e0b; border-radius: 12px; padding: 1.25rem; max-width: 480px; margin: 0 auto 1.5rem; text-align: left;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
              <span style="font-size: 1.6rem;">${tierInfo.icon}</span>
              <div>
                <strong style="color: ${tierInfo.color}; font-size: 1.1rem;">${tierInfo.title}</strong>
                <div style="font-size: 0.8rem; color: var(--text-dim);">${tierInfo.desc}</div>
              </div>
            </div>
            <div style="font-size: 0.85rem; color: #34d399; font-weight: 700; border-top: 1px solid rgba(245, 158, 11, 0.2); padding-top: 0.5rem; margin-top: 0.5rem;">
              ✨ 전직 특전: 칭호 해금 & 보너스 +${tierInfo.bonusXP} XP 즉시 지급 완료!
            </div>
          </div>
          <button onclick="promotionManager.closeModal(); questManager.openModal()" class="btn-primary" style="padding: 0.75rem 2.2rem; font-weight: 800; font-size: 1rem;">
            성장 퀘스트 현황 확인하기 ➔
          </button>
        ` : `
          <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.25rem; max-width: 480px; margin: 0 auto 1.5rem; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5;">
            승급을 위해서는 5문항 중 4문항 이상 정답을 맞혀야 합니다. 아티클과 스팟 퀴즈를 복습한 후 언제든 다시 도전하세요!
          </div>
          <div style="display: flex; gap: 0.75rem; justify-content: center;">
            <button onclick="promotionManager.openExamModal(${this.currentTier})" class="btn-primary" style="padding: 0.65rem 1.75rem; font-weight: 800;">
              🔄 시험 다시 응시하기
            </button>
            <button onclick="promotionManager.closeModal()" class="btn-secondary" style="padding: 0.65rem 1.25rem;">
              닫기
            </button>
          </div>
        `}
      </div>
    `;
  }
};

// ==========================================
// 🏆 실시간 전체 이용자 랭킹보드 매니저 (Leaderboard)
// ==========================================
const rankingManager = {
  currentFilter: 'all', // 'all', 'top10', 'near'
  cloudPlayers: [],

  async fetchCloudPlayers() {
    try {
      if (!window.SUPABASE_CONFIG) return;
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/poker_users?select=id,game_nickname,kakao_nickname,avatar,playstyle,level,xp,completed_articles,completed_quizzes,promotions_passed&order=level.desc,xp.desc&limit=100`, {
        headers: {
          'apikey': SUPABASE_CONFIG.key,
          'Authorization': 'Bearer ' + SUPABASE_CONFIG.key
        }
      });
      if (res.ok) {
        const data = await res.json();
        this.cloudPlayers = data || [];
        this.render();
      }
    } catch (e) {
      console.warn("Failed to fetch cloud ranking players:", e);
    }
  },

  // 실존 포커 전설 및 가상 랭커 데이터 (내 계정과 함께 실시간 경쟁)
  rivals: [
    { name: "LinusLove", avatar: "🦁", style: "GTO", level: 98, xp: 82400, articles: 340, tierNum: 5 },
    { name: "Phil_Ivey", avatar: "👑", style: "EXPLOIT", level: 96, xp: 78900, articles: 325, tierNum: 5 },
    { name: "폴푸아 (Master)", avatar: "🦈", style: "TAG", level: 94, xp: 75100, articles: 369, tierNum: 5 },
    { name: "Daniel_Negreanu", avatar: "🦊", style: "EXPLOIT", level: 91, xp: 71200, articles: 290, tierNum: 5 },
    { name: "Fedor_Holz", avatar: "🧠", style: "GTO", level: 88, xp: 68400, articles: 260, tierNum: 5 },
    { name: "압구정샤크", avatar: "🦈", style: "TAG", level: 82, xp: 60200, articles: 210, tierNum: 4 },
    { name: "마카오레귤러", avatar: "🦁", style: "LAG", level: 78, xp: 55400, articles: 185, tierNum: 4 },
    { name: "GTO솔버러", avatar: "🤖", style: "GTO", level: 73, xp: 49800, articles: 160, tierNum: 4 },
    { name: "체크레이즈달인", avatar: "🎭", style: "LAG", level: 68, xp: 44200, articles: 135, tierNum: 4 },
    { name: "홍대펍지배자", avatar: "⚔️", style: "TAG", level: 62, xp: 38600, articles: 110, tierNum: 3 },
    { name: "온라인그라인더99", avatar: "⚙️", style: "TAG", level: 56, xp: 33100, articles: 95, tierNum: 3 },
    { name: "강남너트장인", avatar: "🦊", style: "EXPLOIT", level: 50, xp: 27900, articles: 80, tierNum: 3 },
    { name: "리버원샷", avatar: "🦉", style: "HUNTER", level: 46, xp: 24500, articles: 65, tierNum: 3 },
    { name: "스몰블라인드킬러", avatar: "🗡️", style: "LAG", level: 41, xp: 20800, articles: 55, tierNum: 2 },
    { name: "팟스틸러", avatar: "🦊", style: "LAG", level: 36, xp: 17200, articles: 45, tierNum: 2 },
    { name: "3벳마니아", avatar: "🦁", style: "LAG", level: 31, xp: 13900, articles: 38, tierNum: 2 },
    { name: "에퀴티계산기", avatar: "🤖", style: "GTO", level: 27, xp: 10800, articles: 30, tierNum: 2 },
    { name: "홀덤꿈나무", avatar: "🐣", style: "TAG", level: 23, xp: 8500, articles: 24, tierNum: 1 },
    { name: "펍루키007", avatar: "⚔️", style: "HUNTER", level: 19, xp: 6200, articles: 18, tierNum: 1 },
    { name: "포커새싹", avatar: "🌱", style: "TAG", level: 14, xp: 3900, articles: 12, tierNum: 1 },
    { name: "마이크로도전자", avatar: "⚙️", style: "TAG", level: 11, xp: 2600, articles: 9, tierNum: 1 },
    { name: "초보홀덤러", avatar: "🐟", style: "HUNTER", level: 7, xp: 1200, articles: 5, tierNum: 0 },
    { name: "스타팅핸드공부중", avatar: "🐣", style: "TAG", level: 4, xp: 500, articles: 2, tierNum: 0 },
    { name: "입문자A", avatar: "🐟", style: "TAG", level: 2, xp: 150, articles: 1, tierNum: 0 }
  ],

  setFilter(filter) {
    this.currentFilter = filter;
    document.querySelectorAll('#view-ranking .filter-pill').forEach(btn => {
      if (btn.id === `rank-filter-${filter}`) btn.classList.add('active');
      else btn.classList.remove('active');
    });
    this.render();
  },

  getAllPlayers() {
    const u = app.userState;
    const lvlInfo = app.getLevelInfo(u.xp);
    const auth = (window.authManager && authManager.isLoggedIn()) ? authManager.getAuthUser() : null;
    const isMeAuth = !!auth;
    const myKakao = (auth && auth.kakao_nickname) ? auth.kakao_nickname : (u.kakao_name || '');

    // 내 캐릭터 객체 생성 (실시간 반영)
    const me = {
      isMe: true,
      name: u.name || "포커신동",
      kakao_nickname: myKakao,
      isCertified: isMeAuth,
      avatar: u.avatar || "🦈",
      style: u.playstyle || "TAG",
      level: lvlInfo.level,
      xp: u.xp,
      articles: (u.completed_articles || []).length,
      quizzes: (u.completed_quizzes || []).length,
      tierNum: lvlInfo.tierNum,
      tierBadge: lvlInfo.tier.badge,
      badgeClass: lvlInfo.tier.badgeClass
    };

    // 실시간 클라우드 회원 목록 변환
    const cloudMembers = (this.cloudPlayers || [])
      .filter(p => {
        if (auth && p.id === auth.id) return false;
        if (p.game_nickname === me.name) return false;
        return true;
      })
      .map(p => {
        let tNum = 0;
        const pLevel = p.level || 1;
        for (let i = PROMOTION_TIERS.length - 1; i >= 0; i--) {
          if (pLevel >= PROMOTION_TIERS[i].minLevel) {
            tNum = i;
            break;
          }
        }
        const tierObj = PROMOTION_TIERS[tNum] || PROMOTION_TIERS[0];
        return {
          isMe: false,
          name: p.game_nickname,
          kakao_nickname: p.kakao_nickname || '',
          isCertified: true,
          avatar: p.avatar || '🦈',
          style: p.playstyle || 'TAG',
          level: pLevel,
          xp: p.xp || 0,
          articles: Array.isArray(p.completed_articles) ? p.completed_articles.length : 0,
          quizzes: Array.isArray(p.completed_quizzes) ? p.completed_quizzes.length : 0,
          tierNum: tNum,
          tierBadge: tierObj.badge,
          badgeClass: tierObj.badgeClass
        };
      });

    // 라이벌 봇들 (이름 중복 방지)
    const takenNames = new Set([me.name, ...cloudMembers.map(c => c.name)]);
    const botList = this.rivals
      .filter(r => !takenNames.has(r.name))
      .map(r => {
        const tierObj = PROMOTION_TIERS[r.tierNum] || PROMOTION_TIERS[0];
        return {
          ...r,
          isMe: false,
          kakao_nickname: '',
          isCertified: false,
          tierBadge: tierObj.badge,
          badgeClass: tierObj.badgeClass,
          quizzes: Math.floor(r.articles * 0.4)
        };
      });

    const list = [me, ...cloudMembers, ...botList];

    // 🏆 핵심 정렬 로직:
    // 1순위: 레벨이 높은 순 (level DESC)
    // 2순위: 레벨이 같으면 경험치가 높은 순 (xp DESC)
    list.sort((a, b) => {
      if (b.level !== a.level) {
        return b.level - a.level;
      }
      return b.xp - a.xp;
    });

    // 랭킹 부여 (1-indexed)
    list.forEach((p, idx) => {
      p.rank = idx + 1;
    });

    return list;
  },

  render() {
    const all = this.getAllPlayers();
    const me = all.find(p => p.isMe);
    const myRank = me ? me.rank : 1;
    const totalCount = all.length;
    const topPct = Math.max(1, Math.round((myRank / totalCount) * 100));

    // 1. 내 랭킹 요약 카드 렌더링
    const summaryCard = document.getElementById('my-ranking-summary-card');
    if (summaryCard && me) {
      const nextRival = all[myRank - 2]; // 내 바로 위 순위자
      const xpToOvertake = nextRival ? Math.max(0, nextRival.xp - me.xp + 10) : 0;

      summaryCard.innerHTML = `
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="font-size: 2.8rem; background: var(--bg-surface); width: 68px; height: 68px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #3b82f6;">
            ${me.avatar}
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
              <span style="font-size: 1.4rem; font-weight: 800; color: #fbbf24;">현재 나의 순위: #${myRank}위</span>
              <span style="font-size: 0.78rem; background: rgba(59, 130, 246, 0.25); color: #93c5fd; padding: 2px 8px; border-radius: 12px; font-weight: 800;">
                상위 ${topPct}%
              </span>
            </div>
            <div style="font-size: 0.95rem; color: var(--text-main); margin-top: 0.25rem; display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
              <strong>${me.name}</strong>
              ${me.kakao_nickname ? `<span style="font-size: 0.75rem; color: #f59e0b; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 4px; padding: 1px 6px; font-weight: 700;">💬 카톡: ${me.kakao_nickname}</span>` : ''}
              ${me.isCertified ? `<span style="font-size: 0.68rem; background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 1px 5px; border-radius: 4px; font-weight: 800;">⭐ 인증회원</span>` : ''}
              • <span class="rank-badge ${me.badgeClass}">${me.tierBadge}</span> • <span style="color: #60a5fa; font-weight: 700;">Lv.${me.level}</span>
            </div>
          </div>
        </div>

        <div style="text-align: right;">
          <div style="font-size: 0.8rem; color: var(--text-dim);">누적 경험치</div>
          <div style="font-size: 1.3rem; font-weight: 800; color: #fbbf24;">${me.xp.toLocaleString()} XP</div>
          ${nextRival ? `
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.25rem;">
              #${nextRival.rank}위(${nextRival.name}) 역전까지: <strong style="color: #38bdf8;">+${xpToOvertake} XP</strong>
            </div>
          ` : `
            <div style="font-size: 0.78rem; color: #34d399; font-weight: 700; margin-top: 0.25rem;">
              👑 전체 1위 독주 중!
            </div>
          `}
        </div>
      `;
    }

    // 2. TOP 3 포디움 렌더링
    const podiumShowcase = document.getElementById('ranking-podium-showcase');
    if (podiumShowcase) {
      const top3 = all.slice(0, 3);
      // 순서: 2위(은), 1위(금), 3위(동)
      const order = [top3[1] || top3[0], top3[0], top3[2] || top3[0]];
      const ranks = [2, 1, 3];

      podiumShowcase.innerHTML = order.map((p, i) => {
        const r = ranks[i];
        const isGold = (r === 1);
        const medal = r === 1 ? '🥇 1위' : (r === 2 ? '🥈 2위' : '🥉 3위');
        const cardClass = r === 1 ? 'podium-rank-1' : (r === 2 ? 'podium-rank-2' : 'podium-rank-3');

        return `
          <div class="podium-card ${cardClass}" style="${isGold ? 'order: 2;' : (r === 2 ? 'order: 1;' : 'order: 3;')}">
            ${isGold ? '<div class="podium-crown">👑</div>' : ''}
            <div class="podium-avatar">${p.avatar}</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: ${isGold ? '#fbbf24' : 'var(--text-main)'}; margin-bottom: 0.2rem;">
              ${medal}
            </div>
            <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.2rem; display: flex; align-items: center; justify-content: center; gap: 0.3rem; flex-wrap: wrap;">
              <span>${p.name}</span>
              ${p.isMe ? '<span style="color: #3b82f6; font-size: 0.75rem;">(나)</span>' : ''}
              ${p.isCertified ? '<span style="color: #34d399; font-size: 0.72rem;" title="클라우드 정회원">⭐</span>' : ''}
            </div>
            ${p.kakao_nickname ? `<div style="font-size: 0.72rem; color: #f59e0b; margin-bottom: 0.35rem; font-weight: 600;">💬 ${p.kakao_nickname}</div>` : ''}
            <span class="rank-badge ${p.badgeClass}" style="margin-bottom: 0.5rem;">${p.tierBadge}</span>
            <div style="font-size: 0.85rem; font-weight: 800; color: #60a5fa;">
              Lv.${p.level} • ${p.xp.toLocaleString()} XP
            </div>
          </div>
        `;
      }).join('');
    }

    // 3. 필터 적용 및 테이블 렌더링
    let displayList = all;
    if (this.currentFilter === 'top10') {
      displayList = all.slice(0, 10);
    } else if (this.currentFilter === 'near') {
      const start = Math.max(0, myRank - 6);
      const end = Math.min(all.length, myRank + 5);
      displayList = all.slice(start, end);
    }

    const tableBody = document.getElementById('ranking-table-body');
    if (tableBody) {
      tableBody.innerHTML = displayList.map(p => {
        let rankBadge = `${p.rank}`;
        if (p.rank === 1) rankBadge = '🥇 1';
        else if (p.rank === 2) rankBadge = '🥈 2';
        else if (p.rank === 3) rankBadge = '🥉 3';

        return `
          <tr class="${p.isMe ? 'ranking-row-me' : ''}" style="border-bottom: 1px solid var(--border-color); transition: background 0.15s ease;">
            <td style="padding: 1rem 1.25rem; text-align: center; font-weight: 800; color: ${p.rank <= 3 ? '#fbbf24' : 'var(--text-dim)'}; font-size: 1.05rem;">
              ${rankBadge}
            </td>
            <td style="padding: 1rem 1.25rem;">
              <div style="display: flex; align-items: center; gap: 0.65rem;">
                <span style="font-size: 1.5rem;">${p.avatar}</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
                    <strong style="color: var(--text-main); font-size: 0.95rem;">${p.name}</strong>
                    ${p.kakao_nickname ? `<span style="font-size: 0.72rem; color: #f59e0b; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 4px; padding: 1px 5px; font-weight: 600;">💬 카톡: ${p.kakao_nickname}</span>` : ''}
                    ${p.isCertified ? `<span style="font-size: 0.68rem; background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 1px 5px; border-radius: 4px; font-weight: 800;">⭐ 인증회원</span>` : ''}
                    ${p.isMe ? '<span style="background: #3b82f6; color: #fff; font-size: 0.68rem; font-weight: 800; padding: 1px 5px; border-radius: 4px;">나</span>' : ''}
                  </div>
                  <span style="font-size: 0.75rem; color: var(--text-dim);">${p.style} 스타일</span>
                </div>
              </div>
            </td>
            <td style="padding: 1rem 1.25rem;">
              <span class="rank-badge ${p.badgeClass}">${p.tierBadge}</span>
            </td>
            <td style="padding: 1rem 1.25rem; text-align: center;">
              <strong style="color: #60a5fa; font-size: 1rem;">Lv.${p.level}</strong>
            </td>
            <td style="padding: 1rem 1.25rem; text-align: right; font-weight: 800; color: #fbbf24; font-size: 0.95rem;">
              ${p.xp.toLocaleString()} XP
            </td>
            <td style="padding: 1rem 1.25rem; text-align: center; font-size: 0.8rem; color: var(--text-muted);">
              📖 ${p.articles}편 완독
            </td>
          </tr>
        `;
      }).join('');
    }
  }
};

// ==========================================
// 📖 Game System & Promotion Guidebook Manager
// ==========================================
const guidebookManager = {
  currentTab: 'tiers',

  openModal(tab = 'tiers') {
    this.currentTab = tab;
    this.render();
    const el = document.getElementById('guidebook-modal-overlay');
    if (el) el.style.display = 'flex';
    app.playAudioEffect('click');
  },

  closeModal() {
    const el = document.getElementById('guidebook-modal-overlay');
    if (el) el.style.display = 'none';
  },

  switchTab(tab) {
    this.currentTab = tab;
    this.render();
    app.playAudioEffect('click');
  },

  render() {
    const body = document.getElementById('guidebook-modal-body');
    if (!body) return;

    const tabs = [
      { id: 'tiers', label: '⚔️ 6개 전직 구간 & 칭호', icon: '⚔️' },
      { id: 'levelup', label: '📈 레벨업 & XP 획득 공식', icon: '📈' },
      { id: 'exam', label: '🎓 전직 심사 시험 안내', icon: '🎓' },
      { id: 'anticheat', label: '⚖️ 공정 학습 가드', icon: '⚖️' },
      { id: 'ranking', label: '🏆 랭킹보드 산정 기준', icon: '🏆' }
    ];

    let contentHtml = '';

    if (this.currentTab === 'tiers') {
      contentHtml = `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 1.1rem; font-weight: 800; color: #60a5fa; margin-bottom: 0.4rem;">
            🌟 Lv.1 동네 피쉬에서 Lv.100 WSOP 전설까지의 6단계 여정
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin: 0;">
            스터디포커는 포커 실력의 발달 단계를 6개 전직 구간으로 구현했습니다. 일정 레벨에 도달하면 자동으로 '전직 심사 시험' 자격이 부여되며, 시험을 합격해야만 다음 레벨 구간으로 진입할 수 있습니다.
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.85rem;">
          ${PROMOTION_TIERS.map(pt => {
            const isEntry = pt.tier === 0;
            const lvlSpan = isEntry ? 'Lv.1 ~ Lv.9' : pt.tier === 1 ? 'Lv.10 ~ Lv.24' : pt.tier === 2 ? 'Lv.25 ~ Lv.44' : pt.tier === 3 ? 'Lv.45 ~ Lv.64' : pt.tier === 4 ? 'Lv.65 ~ Lv.84' : pt.tier === 5 ? 'Lv.85 ~ Lv.99' : 'Lv.100 (만렙)';
            const tierPrefix = isEntry ? '[입문]' : pt.tier === 6 ? '[최종 6차]' : `[${pt.tier}차 전직]`;

            return `
              <div style="background: var(--bg-card); border: 1.5px solid ${pt.color}55; border-radius: 12px; padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.85rem;">
                  <span style="font-size: 2.2rem; filter: drop-shadow(0 2px 8px ${pt.color}44);">${pt.icon}</span>
                  <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                      <span style="font-weight: 800; font-size: 1.05rem; color: ${pt.color};">${tierPrefix} ${pt.name}</span>
                      <span style="background: ${pt.color}22; color: ${pt.color}; font-size: 0.78rem; font-weight: 800; padding: 2px 8px; border-radius: 12px; border: 1px solid ${pt.color}44;">(${lvlSpan})</span>
                    </div>
                    <p style="font-size: 0.83rem; color: var(--text-muted); margin: 0.25rem 0 0; line-height: 1.5;">${pt.desc}</p>
                  </div>
                </div>
                <div style="text-align: right; min-width: 140px;">
                  <span style="font-size: 0.75rem; color: var(--text-dim); display: block;">심사 자격 레벨</span>
                  <strong style="color: #fbbf24; font-size: 0.95rem;">${isEntry ? '기본 입문' : `Lv.${pt.targetLevel} 도달 시`}</strong>
                  ${pt.bonusXP > 0 ? `<div style="font-size: 0.75rem; color: #34d399; font-weight: 700; margin-top: 2px;">🎁 전직 보너스 +${pt.bonusXP.toLocaleString()} XP</div>` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    } else if (this.currentTab === 'levelup') {
      contentHtml = `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 1.1rem; font-weight: 800; color: #34d399; margin-bottom: 0.4rem;">
            📈 실전 학습으로 획득하는 공정한 경험치(XP) 규칙
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin: 0;">
            모든 경험치 획득은 실제 학습 시간을 검증하여 공정하게 부여됩니다. 아래의 5가지 활동을 통해 XP를 획득하고 레벨을 올리세요!
          </p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.85rem;">
          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 800; color: #60a5fa; font-size: 0.95rem;">📖 아티클 정독</span>
              <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px;">+50 XP</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0;">
              369편의 GTO 솔버 아티클을 <strong>최소 35초 이상 집중 열람</strong>하고 본문의 <strong>75% 이상을 스크롤</strong>하면 완독 및 +50 XP가 지급됩니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 800; color: #34d399; font-size: 0.95rem;">🎯 스팟 퀴즈 풀기</span>
              <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px;">+30 XP / +10 XP</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0;">
              실전 핸드 스팟 문제 정답 시 <strong>+30 XP</strong>, 오답 시에도 해설을 복습하면 <strong>+10 XP</strong>를 학습 보상으로 획득합니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 800; color: #a78bfa; font-size: 0.95rem;">🧮 프리플랍 매트릭스 탐색</span>
              <span style="background: rgba(167, 139, 250, 0.2); color: #a78bfa; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px;">+15 XP</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0;">
              169개 핸드 그리드에서 포지션별(UTG~BB) 오픈, 3벳 방어 솔루션 빈도를 탐구하면 경험치가 누적됩니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 800; color: #f59e0b; font-size: 0.95rem;">🤖 AI 코치 심층 질의</span>
              <span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px;">+20 XP</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0;">
              실전에서 헷갈렸던 스팟이나 GTO 이론을 AI 코치에게 질문하고 심층 피드백을 받으면 질문 보너스를 획득합니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 1.15rem; grid-column: 1 / -1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 800; color: #fbbf24; font-size: 0.95rem;">🎓 전직 심사 시험 통과 보너스</span>
              <span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px;">+500 ~ +5,000 XP</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0;">
              각 전직 심사 시험(1차~6차)을 통과할 때마다 대량의 승급 축하 보너스 경험치를 즉시 획득합니다!
            </p>
          </div>
        </div>
      `;
    } else if (this.currentTab === 'exam') {
      contentHtml = `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 1.1rem; font-weight: 800; color: #f59e0b; margin-bottom: 0.4rem;">
            🎓 6구간 전직 심사 시험(Promotion Exam) 시스템
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin: 0;">
            레벨만 높다고 전직할 수 없습니다! 해당 레벨에 도달하면 실제 솔버 지식을 검증하는 5문항의 실전 심사 시험을 치르게 됩니다.
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem;">
            <strong style="color: #60a5fa; font-size: 0.95rem;">🔒 전직 게이트웨이 락 (Level Gate)</strong>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0.35rem 0 0; line-height: 1.5;">
              전직 시험을 통과하지 못하면 해당 레벨(Lv.10, Lv.25, Lv.45 등)에서 레벨업이 잠기며, 상위 티어 콘텐츠가 해금되지 않습니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem;">
            <strong style="color: #34d399; font-size: 0.95rem;">⏱️ 불합격 시 무제한 재도전 가능</strong>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0.35rem 0 0; line-height: 1.5;">
              시험에서 탈락하더라도 경험치나 레벨이 깎이지 않으며, 아티클을 더 복습한 후 언제든지 다시 도전할 수 있습니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem;">
            <strong style="color: #fbbf24; font-size: 0.95rem;">🏆 통과 기준</strong>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0.35rem 0 0; line-height: 1.5;">
              엄선된 실전 핸드 5문항 중 <strong>4문항 이상 정답 시 즉시 합격</strong> 처리되며, 칭호 변경 + 상위 레벨 해금 + 대량의 보너스 XP가 지급됩니다.
            </p>
          </div>
        </div>
      `;
    } else if (this.currentTab === 'anticheat') {
      contentHtml = `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 1.1rem; font-weight: 800; color: #ef4444; margin-bottom: 0.4rem;">
            ⚖️ 공정 학습 및 부정행위 방지 시스템 (Anti-Cheat Fair Guard)
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin: 0;">
            랭킹보드의 공정성과 학습의 진정성을 위해 편법으로 완독 버튼을 누르는 행위를 완벽하게 차단합니다.
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0; padding: 1rem 1.25rem;">
            <strong style="color: #f87171; font-size: 0.95rem;">⏱️ 35초 활성 독서 타이머</strong>
            <p style="font-size: 0.82rem; color: var(--text-main); margin: 0.35rem 0 0; line-height: 1.5;">
              글을 연 후 35초가 경과해야만 완독 버튼이 활성화됩니다.
            </p>
          </div>

          <div style="background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; border-radius: 0 8px 8px 0; padding: 1rem 1.25rem;">
            <strong style="color: #fbbf24; font-size: 0.95rem;">👁️ 백그라운드 탭 자동 일시정지</strong>
            <p style="font-size: 0.82rem; color: var(--text-main); margin: 0.35rem 0 0; line-height: 1.5;">
              다른 인터넷 탭으로 넘어가거나 화면을 가리면 타이머가 즉시 일시정지되어, 켜두기만 하는 방치형 어뷰징을 방지합니다.
            </p>
          </div>

          <div style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 1rem 1.25rem;">
            <strong style="color: #60a5fa; font-size: 0.95rem;">📜 최소 75% 스크롤 검증</strong>
            <p style="font-size: 0.82rem; color: var(--text-main); margin: 0.35rem 0 0; line-height: 1.5;">
              글의 서론만 보고 끝내지 않고 본문의 솔버 차트와 핵심 전략까지 실제로 스크롤을 내려야만 학습 완료로 인증됩니다.
            </p>
          </div>
        </div>
      `;
    } else if (this.currentTab === 'ranking') {
      contentHtml = `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 1.1rem; font-weight: 800; color: #fbbf24; margin-bottom: 0.4rem;">
            🏆 전체 이용자 랭킹보드 순위 산정 기준
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin: 0;">
            모든 이용자의 학습 성과는 실시간으로 집계되어 랭킹보드에 반영됩니다. 순위는 아래의 엄격한 원칙으로 결정됩니다:
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="background: var(--bg-card); border: 1.5px solid #fbbf24; border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
              <span style="font-size: 1.3rem;">🥇</span>
              <strong style="color: #fbbf24; font-size: 1rem;">1순위: 현재 레벨 (Level)</strong>
            </div>
            <p style="font-size: 0.83rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
              레벨이 높은 이용자가 무조건 더 높은 순위를 차지합니다. (예: Lv.25 유저는 Lv.24 유저보다 무조건 상위)
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1.5px solid #60a5fa; border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
              <span style="font-size: 1.3rem;">🥈</span>
              <strong style="color: #60a5fa; font-size: 1rem;">2순위: 동일 레벨일 경우 누적 경험치 (Total XP)</strong>
            </div>
            <p style="font-size: 0.83rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
              동일한 레벨(예: 둘 다 Lv.15)인 경우, 누적 획득 경험치(XP)가 더 많은 유저가 상위 순위로 산정됩니다.
            </p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.15rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
              <span style="font-size: 1.3rem;">🥉</span>
              <strong style="color: var(--text-main); font-size: 1rem;">3순위: 완독 아티클 수</strong>
            </div>
            <p style="font-size: 0.83rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
              레벨과 경험치가 모두 완벽히 동일할 경우, 완독한 아티클 편수가 더 많은 플레이어가 우선순위를 갖습니다.
            </p>
          </div>
        </div>
      `;
    }

    body.innerHTML = `
      <div style="display: flex; gap: 0.4rem; margin-bottom: 1.25rem; overflow-x: auto; padding-bottom: 4px;">
        ${tabs.map(t => `
          <button onclick="guidebookManager.switchTab('${t.id}')" style="
            background: ${this.currentTab === t.id ? '#3b82f6' : 'var(--bg-card)'};
            color: ${this.currentTab === t.id ? '#fff' : 'var(--text-muted)'};
            border: 1px solid ${this.currentTab === t.id ? '#3b82f6' : 'var(--border-color)'};
            padding: 0.5rem 0.9rem;
            border-radius: 8px;
            font-size: 0.83rem;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
          ">
            ${t.label}
          </button>
        `).join('')}
      </div>

      <div style="animation: fadeIn 0.2s ease;">
        ${contentHtml}
      </div>
    `;
  }
};

// ==========================================
// 🔐 Supabase Cloud Authentication & Multi-Device Sync Manager
// ==========================================
const SUPABASE_CONFIG = {
  url: 'https://fjlxlvozbrtigsmlbury.supabase.co',
  key: 'sb_publishable_Wd1XDhi2nWMYib7M_2tS0A_Fxt-FtO_'
};

authManager = window.authManager = {
  gateMode: 'login', // 'login', 'signup', 'forgot'
  currentMode: 'profile', // modal mode: 'profile'
  _syncDebounceTimer: null,
  _isSyncing: false,

  init() {
    if (!this.isLoggedIn()) {
      document.body.classList.remove('authenticated');
      document.body.classList.add('not-authenticated');
      this.showGate('login');
    } else {
      document.body.classList.remove('not-authenticated');
      document.body.classList.add('authenticated');
      this.hideGate();
      this.renderAuthButton();
      this.syncFromCloudSilently();
    }
  },

  // 🛡️ 1차 클라이언트 암호화 (SHA-256 솔트 해싱 - 평문 비밀번호 전송 원천 차단)
  async hashPin(pin) {
    const raw = `spkr_salt_2026_security_${String(pin).trim()}`;
    const msgBuffer = new TextEncoder().encode(raw);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
  },

  isLoggedIn() {
    try {
      const s = localStorage.getItem('studypoker_auth');
      if (!s) return false;
      const parsed = JSON.parse(s);
      return !!(parsed && parsed.id && parsed.auth_token && parsed.game_nickname);
    } catch (e) {
      return false;
    }
  },

  getAuthUser() {
    try {
      const s = localStorage.getItem('studypoker_auth');
      return s ? JSON.parse(s) : null;
    } catch (e) {
      return null;
    }
  },

  showGate(mode = 'login') {
    this.gateMode = mode;
    document.body.classList.remove('authenticated');
    document.body.classList.add('not-authenticated');
    const gate = document.getElementById('auth-gate-screen');
    if (gate) gate.style.display = 'flex';

    const header = document.getElementById('app-header') || document.querySelector('header');
    const main = document.querySelector('main');
    const mobileNav = document.querySelector('.mobile-bottom-nav');

    if (header) header.style.display = 'none';
    if (main) main.style.display = 'none';
    if (mobileNav) mobileNav.style.display = 'none';

    this.renderGate();
  },

  hideGate() {
    document.body.classList.remove('not-authenticated');
    document.body.classList.add('authenticated');
    const gate = document.getElementById('auth-gate-screen');
    if (gate) gate.style.display = 'none';

    const header = document.getElementById('app-header') || document.querySelector('header');
    const main = document.querySelector('main');
    const mobileNav = document.querySelector('.mobile-bottom-nav');

    if (header) header.style.display = '';
    if (main) main.style.display = '';
    if (mobileNav) mobileNav.style.display = '';
  },

  switchGateMode(mode) {
    this.gateMode = mode;
    this.renderGate();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  renderGate() {
    const bodyEl = document.getElementById('auth-gate-body');
    if (!bodyEl) return;

    if (this.gateMode === 'login') {
      bodyEl.innerHTML = `
        <div style="padding: 0.25rem 0;">
          <!-- Tab Navigation -->
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">
            <button onclick="authManager.switchGateMode('login')" style="flex: 1; padding: 0.65rem; border-radius: 8px; font-size: 0.95rem; font-weight: 800; background: #3b82f6; color: #fff; border: none; cursor: pointer;">
              🔑 로그인
            </button>
            <button onclick="authManager.switchGateMode('signup')" style="flex: 1; padding: 0.65rem; border-radius: 8px; font-size: 0.95rem; font-weight: 700; background: var(--bg-surface); color: var(--text-muted); border: 1px solid var(--border-color); cursor: pointer;">
              ✨ 30초 회원가입
            </button>
          </div>

          <form onsubmit="event.preventDefault(); authManager.handleGateLoginSubmit();" style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.4rem;">
                아이디 (게임 닉네임 또는 가입 이메일)
              </label>
              <input type="text" id="gate-login-id" required placeholder="게임 닉네임 입력 (또는 등록된 이메일)" autocomplete="username" style="width: 100%; padding: 0.75rem 0.9rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.95rem; box-sizing: border-box;">
            </div>

            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-main);">
                  비밀번호
                </label>
                <a href="javascript:void(0)" onclick="authManager.switchGateMode('forgot')" style="font-size: 0.78rem; color: #60a5fa; text-decoration: none;">
                  비밀번호 찾기
                </a>
              </div>
              <input type="password" id="gate-login-pin" required placeholder="비밀번호 입력" autocomplete="current-password" style="width: 100%; padding: 0.75rem 0.9rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.95rem; box-sizing: border-box;">
            </div>

            <div id="gate-login-status" style="display: none; padding: 0.6rem; border-radius: 6px; font-size: 0.83rem; text-align: center;"></div>

            <button type="submit" id="gate-login-submit-btn" class="btn-primary" style="width: 100%; padding: 0.85rem; font-size: 1rem; font-weight: 800; border-radius: 8px; margin-top: 0.35rem;">
              🔑 로그인하고 게임 시작하기
            </button>
          </form>

          <div style="text-align: center; margin-top: 1.25rem; font-size: 0.85rem; color: var(--text-muted);">
            처음 오셨나요? <a href="javascript:void(0)" onclick="authManager.switchGateMode('signup')" style="color: #fbbf24; font-weight: 800; text-decoration: underline;">간편 회원가입 (이메일 없이 10초 완료)</a>
          </div>
        </div>
      `;
    } else if (this.gateMode === 'signup') {
      bodyEl.innerHTML = `
        <div style="padding: 0.25rem 0;">
          <!-- Tab Navigation -->
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">
            <button onclick="authManager.switchGateMode('login')" style="flex: 1; padding: 0.65rem; border-radius: 8px; font-size: 0.95rem; font-weight: 700; background: var(--bg-surface); color: var(--text-muted); border: 1px solid var(--border-color); cursor: pointer;">
              🔑 로그인
            </button>
            <button onclick="authManager.switchGateMode('signup')" style="flex: 1; padding: 0.65rem; border-radius: 8px; font-size: 0.95rem; font-weight: 800; background: #3b82f6; color: #fff; border: none; cursor: pointer;">
              ✨ 30초 회원가입
            </button>
          </div>

          <form onsubmit="event.preventDefault(); authManager.handleGateSignUpSubmit();" style="display: flex; flex-direction: column; gap: 0.85rem;">
            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
                1. 게임 닉네임 <span style="color: #ef4444;">*</span> <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 400;">(캐릭터명 & 로그인 아이디)</span>
              </label>
              <input type="text" id="gate-reg-game-nick" required minlength="2" maxlength="16" placeholder="예: 압구정포커신 (2~16자)" autocomplete="nickname" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
            </div>

            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
                2. 카카오톡 단톡방 닉네임 <span style="color: #ef4444;">*</span> <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 400;">(단톡방 랭킹 표시용)</span>
              </label>
              <input type="text" id="gate-reg-kakao-nick" required minlength="1" maxlength="20" placeholder="예: 홍길동/오픈채팅방닉네임" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem;">
              <div>
                <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
                  3. 비밀번호 <span style="color: #ef4444;">*</span> <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">(자유 입력, 4자 이상)</span>
                </label>
                <input type="password" id="gate-reg-pin" required minlength="4" placeholder="비밀번호 입력 (자유)" autocomplete="new-password" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
              </div>
              <div>
                <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
                  비밀번호 확인 <span style="color: #ef4444;">*</span>
                </label>
                <input type="password" id="gate-reg-pin-confirm" required minlength="4" placeholder="비밀번호 재입력" autocomplete="new-password" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
              </div>
            </div>

            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
                4. 이메일 주소 <span style="font-size: 0.75rem; color: #10b981; font-weight: 700;">(선택사항)</span>
              </label>
              <input type="email" id="gate-reg-email" placeholder="이메일 입력 (입력 안 해도 가입 가능)" autocomplete="email" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
              <div style="font-size: 0.74rem; color: #f59e0b; margin-top: 4px; line-height: 1.4;">
                ⚠️ <strong>선택사항 안내</strong>: 이메일을 적지 않아도 10초 만에 가입하여 바로 플레이할 수 있습니다. 단, 비밀번호 분실 시 재설정이 불가능하므로 기억하기 쉬운 비밀번호를 설정해주세요.
              </div>
            </div>

            <div id="gate-reg-status" style="display: none; padding: 0.6rem; border-radius: 6px; font-size: 0.83rem; text-align: center;"></div>

            <button type="submit" id="gate-reg-submit-btn" class="btn-primary" style="width: 100%; padding: 0.85rem; font-size: 1rem; font-weight: 800; border-radius: 8px; margin-top: 0.35rem; background: linear-gradient(135deg, #10b981, #059669);">
              ✨ 가입하고 게임 시작하기
            </button>
          </form>

          <div style="text-align: center; margin-top: 1rem; font-size: 0.85rem; color: var(--text-muted);">
            이미 계정이 있으신가요? <a href="javascript:void(0)" onclick="authManager.switchGateMode('login')" style="color: #60a5fa; font-weight: 800; text-decoration: underline;">로그인하기</a>
          </div>
        </div>
      `;
    } else if (this.gateMode === 'forgot') {
      bodyEl.innerHTML = `
        <div style="padding: 0.25rem 0;">
          <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 1.25rem; font-size: 0.82rem; color: #93c5fd; line-height: 1.5;">
            🔍 <strong>비밀번호 재설정</strong>: 가입 시 <strong>이메일을 등록한 회원</strong>에 한하여 새 비밀번호로 즉시 변경됩니다.
          </div>

          <form onsubmit="event.preventDefault(); authManager.handleGateForgotSubmit();" style="display: flex; flex-direction: column; gap: 0.9rem;">
            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">가입 이메일 주소</label>
              <input type="email" id="gate-forgot-email" required placeholder="가입 시 입력했던 이메일" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
            </div>

            <div>
              <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">게임 닉네임</label>
              <input type="text" id="gate-forgot-nick" required placeholder="가입한 게임 닉네임" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem;">
              <div>
                <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">새 비밀번호</label>
                <input type="password" id="gate-forgot-pin" required minlength="4" placeholder="새 비밀번호 입력 (4자 이상)" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
              </div>
              <div>
                <label style="display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">새 비밀번호 확인</label>
                <input type="password" id="gate-forgot-pin-confirm" required minlength="4" placeholder="새 비밀번호 재입력" style="width: 100%; padding: 0.7rem 0.85rem; background: var(--bg-surface); border: 1.5px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.92rem; box-sizing: border-box;">
              </div>
            </div>

            <div id="gate-forgot-status" style="display: none; padding: 0.6rem; border-radius: 6px; font-size: 0.83rem; text-align: center;"></div>

            <button type="submit" id="gate-forgot-submit-btn" class="btn-primary" style="width: 100%; padding: 0.85rem; font-size: 1rem; font-weight: 800; border-radius: 8px; margin-top: 0.35rem;">
              🔑 새 비밀번호로 변경하기
            </button>
          </form>

          <div style="text-align: center; margin-top: 1rem; font-size: 0.85rem;">
            <a href="javascript:void(0)" onclick="authManager.switchGateMode('login')" style="color: #60a5fa; font-weight: 800; text-decoration: underline;">
              ← 로그인 화면으로 돌아가기
            </a>
          </div>
        </div>
      `;
    }
  },

  async handleGateLoginSubmit() {
    const loginId = (document.getElementById('gate-login-id')?.value || '').trim();
    const pin = (document.getElementById('gate-login-pin')?.value || '').trim();
    const submitBtn = document.getElementById('gate-login-submit-btn');

    if (!loginId) {
      this.showStatus('gate-login-status', '아이디(게임 닉네임 또는 이메일)를 입력해주세요.', true);
      return;
    }
    if (!pin || pin.length < 4) {
      this.showStatus('gate-login-status', '비밀번호를 입력해주세요 (최소 4자 이상).', true);
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerText = '🔒 보안 검증 중...';
    }

    try {
      const pinHash = await this.hashPin(pin);
      const url = `${SUPABASE_CONFIG.url}/rest/v1/rpc/poker_login`;
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.key,
          'Authorization': 'Bearer ' + SUPABASE_CONFIG.key,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          p_login_id: loginId,
          p_pin_hash: pinHash
        })
      });

      if (!res.ok) throw new Error(`서버 응답 오류 (${res.status})`);

      const result = await res.json();
      if (!result || result.success === false) {
        let errMsg = result.error || '일치하는 계정을 찾을 수 없습니다.';
        if (errMsg.includes('일치하지') || errMsg.includes('비밀번호')) {
          errMsg = '비밀번호가 일치하지 않습니다. 다시 확인해주세요.';
        }
        this.showStatus('gate-login-status', errMsg, true);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = '🔑 로그인하고 게임 시작하기';
        }
        return;
      }

      // 로그인 성공! 세션 저장
      localStorage.setItem('studypoker_auth', JSON.stringify({
        id: result.user_id,
        game_nickname: result.game_nickname,
        kakao_nickname: result.kakao_nickname,
        auth_token: result.auth_token
      }));

      // 유저 상태 수화
      const u = app.userState;
      u.name = result.game_nickname;
      u.kakao_name = result.kakao_nickname;
      u.avatar = result.avatar || '🦈';
      u.playstyle = result.playstyle || 'TAG';
      u.xp = result.xp || 0;
      u.completed_articles = result.completed_articles || [];
      u.completed_quizzes = result.completed_quizzes || [];
      u.promotions_passed = result.promotions_passed || [0];
      u.stats = result.stats || {};

      storage.save(u);

      this.hideGate();
      this.renderAuthButton();
      app.startAuthenticatedApp();

      characterManager.showToast(`🎉 반갑습니다, ${result.game_nickname}님! 게임이 시작되었습니다.`);
    } catch (e) {
      console.error("Gate login error:", e);
      this.showStatus('gate-login-status', `로그인 실패: ${e.message}`, true);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = '🔑 로그인하고 게임 시작하기';
      }
    }
  },

  async handleGateSignUpSubmit() {
    const gameNick = (document.getElementById('gate-reg-game-nick')?.value || '').trim();
    const kakaoNick = (document.getElementById('gate-reg-kakao-nick')?.value || '').trim();
    const email = (document.getElementById('gate-reg-email')?.value || '').trim();
    const pin = (document.getElementById('gate-reg-pin')?.value || '').trim();
    const pinConfirm = (document.getElementById('gate-reg-pin-confirm')?.value || '').trim();
    const submitBtn = document.getElementById('gate-reg-submit-btn');

    if (!gameNick || gameNick.length < 2) {
      this.showStatus('gate-reg-status', '게임 닉네임은 최소 2글자 이상이어야 합니다.', true);
      return;
    }
    if (!kakaoNick || kakaoNick.length < 1) {
      this.showStatus('gate-reg-status', '카카오톡 오픈채팅방 닉네임을 입력해주세요.', true);
      return;
    }
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      this.showStatus('gate-reg-status', '올바른 이메일 형식을 입력해주세요.', true);
      return;
    }
    if (!pin || pin.length < 4) {
      this.showStatus('gate-reg-status', '비밀번호는 최소 4자 이상이어야 합니다.', true);
      return;
    }
    if (pin !== pinConfirm) {
      this.showStatus('gate-reg-status', '비밀번호와 비밀번호 확인이 일치하지 않습니다.', true);
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerText = '🔒 3중 보안 가입 처리 중...';
    }

    try {
      const pinHash = await this.hashPin(pin);
      const u = app.userState;
      const lvlInfo = app.getLevelInfo(u.xp || 0);

      const signupUrl = `${SUPABASE_CONFIG.url}/rest/v1/rpc/poker_signup`;
      const res = await fetch(signupUrl, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.key,
          'Authorization': 'Bearer ' + SUPABASE_CONFIG.key,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          p_game_nickname: gameNick,
          p_kakao_nickname: kakaoNick,
          p_email: email, // Optional, can be empty string
          p_pin_hash: pinHash,
          p_level: 1,
          p_xp: 0,
          p_streak: 1,
          p_avatar: '🦈',
          p_playstyle: 'TAG',
          p_completed_articles: [],
          p_completed_quizzes: [],
          p_promotions_passed: [0],
          p_stats: {}
        })
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`회원 등록 통신 실패 (${res.status}): ${errText}`);
      }

      const result = await res.json();
      if (!result || result.success === false) {
        this.showStatus('gate-reg-status', result.error || '회원 등록에 실패했습니다.', true);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = '✨ 가입하고 게임 시작하기';
        }
        return;
      }

      localStorage.setItem('studypoker_auth', JSON.stringify({
        id: result.user_id,
        game_nickname: result.game_nickname,
        kakao_nickname: result.kakao_nickname,
        auth_token: result.auth_token
      }));

      u.name = gameNick;
      u.kakao_name = kakaoNick;
      u.xp = 0;
      u.completed_articles = [];
      u.completed_quizzes = [];
      u.promotions_passed = [0];
      storage.save(u);

      this.hideGate();
      this.renderAuthButton();
      app.startAuthenticatedApp();

      characterManager.showToast(`🎉 ${gameNick}님, 환영합니다! 스터디포커가 시작되었습니다.`);
    } catch (e) {
      console.error("Gate signup error:", e);
      this.showStatus('gate-reg-status', `가입 실패: ${e.message}`, true);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = '✨ 가입하고 게임 시작하기';
      }
    }
  },

  async handleGateForgotSubmit() {
    const email = (document.getElementById('gate-forgot-email')?.value || '').trim();
    const gameNick = (document.getElementById('gate-forgot-nick')?.value || '').trim();
    const pin = (document.getElementById('gate-forgot-pin')?.value || '').trim();
    const pinConfirm = (document.getElementById('gate-forgot-pin-confirm')?.value || '').trim();
    const submitBtn = document.getElementById('gate-forgot-submit-btn');

    if (!email || !gameNick) {
      this.showStatus('gate-forgot-status', '가입 이메일과 게임 닉네임을 모두 입력해주세요.', true);
      return;
    }
    if (!pin || pin.length < 4) {
      this.showStatus('gate-forgot-status', '새 비밀번호는 최소 4자 이상이어야 합니다.', true);
      return;
    }
    if (pin !== pinConfirm) {
      this.showStatus('gate-forgot-status', '비밀번호 확인이 일치하지 않습니다.', true);
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerText = '🔒 보안 재설정 중...';
    }

    try {
      const pinHash = await this.hashPin(pin);
      const url = `${SUPABASE_CONFIG.url}/rest/v1/rpc/poker_reset_pin`;
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.key,
          'Authorization': 'Bearer ' + SUPABASE_CONFIG.key,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          p_email: email,
          p_game_nickname: gameNick,
          p_new_pin_hash: pinHash
        })
      });

      if (!res.ok) throw new Error("서버 확인 실패");

      const result = await res.json();
      if (!result || result.success === false) {
        this.showStatus('gate-forgot-status', result.error || '일치하는 가입 회원 정보를 찾을 수 없습니다.', true);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = '🔑 새 비밀번호로 변경하기';
        }
        return;
      }

      characterManager.showToast("✅ 비밀번호가 성공적으로 재설정되었습니다! 새 비밀번호로 로그인해주세요.");
      this.switchGateMode('login');
    } catch (e) {
      console.error("Gate forgot error:", e);
      this.showStatus('gate-forgot-status', `재설정 실패: ${e.message}`, true);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = '🔑 새 비밀번호로 변경하기';
      }
    }
  },

  openModal(mode = 'profile') {
    if (!this.isLoggedIn()) {
      this.showGate('login');
      return;
    }
    this.currentMode = mode;
    this.renderModal();
    const overlay = document.getElementById('auth-modal-overlay');
    if (overlay) overlay.style.display = 'flex';
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },

  closeModal() {
    const overlay = document.getElementById('auth-modal-overlay');
    if (overlay) overlay.style.display = 'none';
  },

  renderAuthButton() {
    const container = document.getElementById('header-auth-container');
    const isAuth = this.isLoggedIn();
    const auth = this.getAuthUser();

    if (container) {
      if (isAuth && auth) {
        container.innerHTML = `
          <button class="header-action-btn" onclick="authManager.openModal('profile')" title="내 계정 정보 및 클라우드 동기화" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.3)); border: 1.5px solid #10b981; color: #34d399; padding: 0.45rem 0.85rem; border-radius: 20px; font-weight: 800; cursor: pointer; font-size: 0.82rem; display: inline-flex; align-items: center; gap: 0.45rem; transition: all 0.2s ease;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 6px #34d399;"></span>
            <span>${this.escapeHtml(auth.game_nickname)}</span>
          </button>
        `;
      } else {
        container.innerHTML = `
          <button class="header-action-btn" onclick="authManager.showGate('login')" title="클라우드 로그인" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.3)); border: 1.5px solid #f59e0b; color: #fbbf24; padding: 0.45rem 0.85rem; border-radius: 20px; font-weight: 800; cursor: pointer; font-size: 0.82rem; display: inline-flex; align-items: center; gap: 0.4rem; transition: all 0.2s ease;">
            <span>👤</span> 로그인
          </button>
        `;
      }
    }

    const dAuthBtn = document.getElementById('dash-auth-btn');
    if (dAuthBtn) {
      dAuthBtn.innerHTML = isAuth ? '<span>⚙️</span> 내 계정 관리' : '<span>👤</span> 로그인';
      dAuthBtn.onclick = () => {
        if (isAuth) authManager.openModal('profile');
        else authManager.showGate('login');
      };
    }

    const dKakao = document.getElementById('dash-kakao-tag');
    if (dKakao) {
      if (isAuth && auth && auth.kakao_nickname) {
        dKakao.innerText = `💬 단톡방: ${auth.kakao_nickname}`;
        dKakao.style.display = 'inline-flex';
      } else if (app.userState.kakao_name) {
        dKakao.innerText = `💬 단톡방: ${app.userState.kakao_name}`;
        dKakao.style.display = 'inline-flex';
      } else {
        dKakao.innerText = `💬 단톡방 닉네임: 미등록`;
      }
    }
  },

  escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[m]));
  },

  renderModal() {
    const titleEl = document.getElementById('auth-modal-title');
    const descEl = document.getElementById('auth-modal-desc');
    const iconEl = document.getElementById('auth-modal-icon');
    const bodyEl = document.getElementById('auth-modal-body');

    if (!bodyEl) return;
    const auth = this.getAuthUser();
    const u = app.userState;
    const lvlInfo = app.getLevelInfo(u.xp || 0);

    if (titleEl) titleEl.innerText = '내 계정 및 클라우드 연동 상태';
    if (descEl) descEl.innerText = '현재 로그인된 계정 정보와 클라우드 실시간 동기화 상태입니다.';
    if (iconEl) iconEl.innerText = '👤';

    bodyEl.innerHTML = `
      <div style="padding: 0.25rem 0;">
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15)); border: 1.5px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span style="font-size: 2.2rem;">${u.avatar || '🦈'}</span>
              <div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-main);">
                  ${this.escapeHtml(auth ? auth.game_nickname : u.name)}
                </div>
                <div style="font-size: 0.82rem; color: #34d399; font-weight: 700; display: flex; align-items: center; gap: 0.35rem; margin-top: 2px;">
                  <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 6px #34d399;"></span>
                  3중 철통 보안 연동 중
                </div>
              </div>
            </div>
            <span class="rank-badge ${lvlInfo.tier.badgeClass}">${lvlInfo.tier.badge}</span>
          </div>

          <div style="border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 0.85rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; font-size: 0.85rem;">
            <div>
              <span style="color: var(--text-muted); display: block; font-size: 0.75rem;">💬 카카오톡 단톡방 닉네임</span>
              <strong style="color: #f59e0b;">${this.escapeHtml((auth && auth.kakao_nickname) ? auth.kakao_nickname : (u.kakao_name || '미설정'))}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); display: block; font-size: 0.75rem;">🔒 가입 정보 보호</span>
              <strong style="color: #34d399; font-size: 0.8rem;">비공개 금고 격리됨</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); display: block; font-size: 0.75rem;">⭐ 현재 레벨 & 경험치</span>
              <strong style="color: #60a5fa;">Lv.${lvlInfo.level} (${(u.xp || 0).toLocaleString()} XP)</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); display: block; font-size: 0.75rem;">📖 완독한 아티클</span>
              <strong style="color: #a78bfa;">${(u.completed_articles || []).length}편</strong>
            </div>
          </div>
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem; margin-bottom: 1.25rem;">
          <div style="font-weight: 700; color: var(--text-main); font-size: 0.9rem; margin-bottom: 0.35rem;">
            📱 모바일 ↔ PC 어디서든 이어하는 방법
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
            스마트폰이나 다른 컴퓨터 브라우저에서 <strong>https://studypoker.vercel.app</strong> 접속 후,
            게임 닉네임(<strong>${this.escapeHtml(auth ? auth.game_nickname : u.name)}</strong>)과 비밀번호로 로그인하시면 모든 공부 기록이 즉시 동기화됩니다!
          </p>
        </div>

        <div id="auth-profile-status" style="display: none; padding: 0.6rem; border-radius: 6px; font-size: 0.83rem; text-align: center; margin-bottom: 0.75rem;"></div>

        <div style="display: flex; gap: 0.75rem;">
          <button onclick="authManager.forcePushToCloud()" class="btn-primary" style="flex: 1; padding: 0.75rem; font-size: 0.9rem; font-weight: 800; border-radius: 8px;">
            🔄 지금 즉시 클라우드 백업
          </button>
          <button onclick="authManager.handleSignOut()" class="btn-secondary" style="flex: 1; padding: 0.75rem; font-size: 0.9rem; font-weight: 800; border-radius: 8px; border-color: #ef444455; color: #f87171;">
            🚪 로그아웃
          </button>
        </div>
      </div>
    `;
  },

  showStatus(elementId, message, isError = false) {
    const el = document.getElementById(elementId);
    if (!el) return;
    let cleanMsg = String(message || '');
    cleanMsg = cleanMsg.replace(/\(숫자\s*6자리\)/g, '').replace(/숫자\s*6자리/g, '').trim();
    if (cleanMsg.includes('일치하지') && cleanMsg.includes('비밀번호')) {
      cleanMsg = '비밀번호가 일치하지 않습니다. 다시 확인해주세요.';
    }
    el.style.display = 'block';
    el.style.background = isError ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)';
    el.style.color = isError ? '#fca5a5' : '#6ee7b7';
    el.style.border = isError ? '1px solid rgba(239, 68, 68, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)';
    el.innerText = cleanMsg;
  },

  handleSignOut() {
    if (!confirm("정말 로그아웃 하시겠습니까?")) {
      return;
    }
    localStorage.removeItem('studypoker_auth');
    localStorage.removeItem('studypoker_user');
    app.userState = {
      name: '',
      avatar: '🦈',
      playstyle: 'TAG',
      xp: 0,
      completed_articles: [],
      completed_quizzes: [],
      promotions_passed: [],
      ai_queries_count: 0
    };
    this.closeModal();
    this.showGate('login');
    characterManager.showToast("🚪 로그아웃 되었습니다.");
  },

  async syncFromCloudSilently() {
    const auth = this.getAuthUser();
    if (!auth || !auth.id) return;

    try {
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/poker_users?id=eq.${auth.id}&select=*`, {
        headers: {
          'apikey': SUPABASE_CONFIG.key,
          'Authorization': 'Bearer ' + SUPABASE_CONFIG.key
        }
      });

      if (!res.ok) return;
      const list = await res.json();
      if (!list || list.length === 0) return;

      const cloud = list[0];
      const u = app.userState;

      let changed = false;
      const cloudXp = cloud.xp || 0;
      if (cloudXp > (u.xp || 0)) {
        u.xp = cloudXp;
        changed = true;
      }

      const mergedArticles = Array.from(new Set([...(u.completed_articles || []), ...(cloud.completed_articles || [])]));
      if (mergedArticles.length !== (u.completed_articles || []).length) {
        u.completed_articles = mergedArticles;
        changed = true;
      }

      const mergedQuizzes = Array.from(new Set([...(u.completed_quizzes || []), ...(cloud.completed_quizzes || [])]));
      if (mergedQuizzes.length !== (u.completed_quizzes || []).length) {
        u.completed_quizzes = mergedQuizzes;
        changed = true;
      }

      const mergedPromotions = Array.from(new Set([...(u.promotions_passed || [0]), ...(cloud.promotions_passed || [0])]));
      if (mergedPromotions.length !== (u.promotions_passed || [0]).length) {
        u.promotions_passed = mergedPromotions;
        changed = true;
      }

      if (cloud.game_nickname && cloud.game_nickname !== u.name) {
        u.name = cloud.game_nickname;
        changed = true;
      }
      if (cloud.kakao_nickname && cloud.kakao_nickname !== u.kakao_name) {
        u.kakao_name = cloud.kakao_nickname;
        changed = true;
      }

      if (changed) {
        localStorage.setItem('studypoker_user', JSON.stringify(u));
        characterManager.renderDashboard();
        characterManager.renderHeader();
        app.updateUserBar();
        roadmap.load();
        if (window.rankingManager && rankingManager.render) {
          rankingManager.render();
        }
      } else if ((u.xp || 0) > cloudXp) {
        this.syncToCloud(true);
      }
    } catch (e) {
      console.warn("Silent cloud pull error:", e);
    }
  },

  syncToCloud(immediate = false) {
    if (!this.isLoggedIn()) return;
    if (this._syncDebounceTimer) clearTimeout(this._syncDebounceTimer);

    const doPush = async () => {
      try {
        const auth = this.getAuthUser();
        if (!auth || !auth.id || !auth.auth_token) return;
        const u = app.userState;
        const lvlInfo = app.getLevelInfo(u.xp || 0);

        await fetch(`${SUPABASE_CONFIG.url}/rest/v1/rpc/poker_sync_progress`, {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_CONFIG.key,
            'Authorization': 'Bearer ' + SUPABASE_CONFIG.key,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            p_user_id: auth.id,
            p_auth_token: auth.auth_token,
            p_level: lvlInfo.level,
            p_xp: u.xp || 0,
            p_streak: u.streak || 1,
            p_avatar: u.avatar || '🦈',
            p_playstyle: u.playstyle || 'TAG',
            p_completed_articles: u.completed_articles || [],
            p_completed_quizzes: u.completed_quizzes || [],
            p_promotions_passed: u.promotions_passed || [0],
            p_stats: u.stats || {}
          })
        });
      } catch (e) {
        console.warn("Cloud sync push error:", e);
      }
    };

    if (immediate) {
      doPush();
    } else {
      this._syncDebounceTimer = setTimeout(doPush, 1500);
    }
  },

  async forcePushToCloud() {
    const statusEl = document.getElementById('auth-profile-status');
    if (statusEl) {
      statusEl.style.display = 'block';
      statusEl.style.background = 'rgba(59, 130, 246, 0.15)';
      statusEl.style.color = '#93c5fd';
      statusEl.innerText = '🔒 보안 검증 후 클라우드 저장 중...';
    }

    try {
      await this.syncToCloud(true);
      if (statusEl) {
        statusEl.style.background = 'rgba(16, 185, 129, 0.15)';
        statusEl.style.color = '#6ee7b7';
        statusEl.innerText = `✅ 클라우드 동기화 완료! (${new Date().toLocaleTimeString('ko-KR')})`;
      }
      characterManager.showToast("☁️ 최신 캐릭터 상태가 클라우드에 안전하게 백업되었습니다.");
    } catch (e) {
      if (statusEl) {
        statusEl.style.background = 'rgba(239, 68, 68, 0.15)';
        statusEl.style.color = '#fca5a5';
        statusEl.innerText = `동기화 실패: ${e.message}`;
      }
    }
  }
};


window.addEventListener('DOMContentLoaded', () => {
  app.init();
});
  </script>
</body>
</html>
