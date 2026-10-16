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
        explored_ranges: []
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
      explored_ranges: []
    };
  },
  save(state) {
    localStorage.setItem('studypoker_user', JSON.stringify(state));
  }
};


// 6-Tier RPG Level System (Deep Long-Term Mastery Curve)
const LEVEL_TIERS = [
  { level: 1, title: "Lv.1 동네 피쉬 탈출기 🐟", badge: "🐣 피쉬 탈출", minXp: 0, maxXp: 600, tierName: "동네 피쉬" },
  { level: 2, title: "Lv.2 홀덤펍 로컬 레귤러 ⚔️", badge: "⚔️ 펍 레귤러", minXp: 600, maxXp: 2000, tierName: "로컬 레귤러" },
  { level: 3, title: "Lv.3 마이크로 그라인더 🔥", badge: "🔥 온라인 그라인더", minXp: 2000, maxXp: 5000, tierName: "마이크로 그라인더" },
  { level: 4, title: "Lv.4 온라인 세미프로 🦊", badge: "🦊 세미프로", minXp: 5000, maxXp: 10000, tierName: "온라인 세미프로" },
  { level: 5, title: "Lv.5 하이롤러 토너 크러셔 🦁", badge: "🦁 하이롤러", minXp: 10000, maxXp: 18000, tierName: "토너 크러셔" },
  { level: 6, title: "Lv.6 WSOP 챔피언 👑", badge: "👑 WSOP 챔피언", minXp: 18000, maxXp: 99999, tierName: "세계 챔피언" }
];

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

    // If new user visiting for the first time, auto-open character setup popup!
    const hasConfigured = localStorage.getItem('studypoker_char_created');
    if (!hasConfigured) {
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
    themeManager.init();
    characterManager.init();
    this.updateUserBar();
    roadmap.load();
    reader.loadArticles();
    matrix.init();
    glossary.load();

    const hash = window.location.hash.replace('#', '');
    if (hash && ['articles', 'trainer', 'matrix', 'roadmap', 'glossary'].includes(hash)) {
      this.navigate(hash);
    } else {
      this.navigate('roadmap');
    }
  },

  navigate(viewId) {
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
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  getLevelInfo(xp) {
    for (let i = LEVEL_TIERS.length - 1; i >= 0; i--) {
      if (xp >= LEVEL_TIERS[i].minXp) {
        const cur = LEVEL_TIERS[i];
        const curXpInLevel = xp - cur.minXp;
        const neededForNext = cur.maxXp - cur.minXp;
        const pct = Math.min(100, Math.round((curXpInLevel / neededForNext) * 100));
        return {
          ...cur,
          progressPct: pct,
          remainingXp: Math.max(0, cur.maxXp - xp)
        };
      }
    }
    return { level: 1, title: "Lv.1 동네 피쉬 탈출기 🐟", badge: "🐣 피쉬 탈출", minXp: 0, maxXp: 600, progressPct: 0, remainingXp: 600, tierName: "동네 피쉬" };
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
    if (newLvlInfo.level > prevLvl) {
      characterManager.showToast(`🎉 축하합니다! <strong>${newLvlInfo.title}</strong> 등급으로 승급하셨습니다!`);
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
      'Level 1': { title: 'Lv.1 입문', req: 1 },
      'Level 2': { title: 'Lv.2 초급', req: 2 },
      'Level 3': { title: 'Lv.3 중급', req: 3 },
      'Level 4': { title: 'Lv.4 고급', req: 4 },
      'Level 5': { title: 'Lv.5 심화', req: 5 },
      'Level 6': { title: 'Lv.6 마스터', req: 6 }
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
          (this.activeCategory === 'all' || a.category === this.activeCategory) && a.level.startsWith(l)
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
      if (this.activeLevel !== 'all' && !a.level.startsWith(this.activeLevel)) return false;
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

    const isCompleted = app.userState.completed_articles.includes(data.id);
    if (isCompleted) {
      this.secondsRemaining = 0;
      this.updateCompletionUI(true, 0);
    } else {
      this.secondsRemaining = 45;
      this.updateCompletionUI(false, 45);

      this.readTimer = setInterval(() => {
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
    if (this.secondsRemaining > 0 && !app.userState.completed_articles.includes(this.currentArticle.id)) {
      characterManager.showToast(`⏱️ 아티클을 깊이 있게 정독해주세요! (${this.secondsRemaining}초 남음)`);
      return;
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
    const idx = this.quizzes.findIndex(q => (q.required_level || 1) === lvl);
    if (idx !== -1) {
      this.currentIndex = idx;
      this.renderCurrentQuiz();
      app.playAudioEffect('click');
    }
  },

  jumpToFirstUnlocked() {
    this.currentIndex = 0;
    this.renderCurrentQuiz();
    app.playAudioEffect('click');
  },

  updateLevelChips() {
    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const curQ = this.quizzes[this.currentIndex];
    const curLvl = curQ ? (curQ.required_level || 1) : 1;

    document.querySelectorAll('#quiz-level-filter-chips .filter-pill').forEach(btn => {
      const lvl = parseInt(btn.dataset.qlvl, 10);
      const isLocked = lvl > userLvl;
      const isActive = (lvl === curLvl);

      if (isActive) btn.classList.add('active');
      else btn.classList.remove('active');

      const labels = { 1: 'Lv.1 입문', 2: 'Lv.2 초급', 3: 'Lv.3 중급', 4: 'Lv.4 고급', 5: 'Lv.5 심화', 6: 'Lv.6 마스터' };
      btn.innerText = `${isLocked ? '🔒 ' : '🔓 '}${labels[lvl] || `Lv.${lvl}`}`;
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
        title: "로컬 레귤러 달성",
        desc: "600 XP 달성 및 Lv.2 진화",
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

window.addEventListener('DOMContentLoaded', () => {
  app.init();
});
  </script>
</body>
</html>
