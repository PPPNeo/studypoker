# -*- coding: utf-8 -*-
"""
apply_progressive_unlock_system.py
Implements progressive level-based gating for:
- Articles Library (369 articles across 6 levels, lock badge, lock modal, unlocked-only toggle)
- Spot Quizzes (25 quizzes across 6 levels, lock shields, level jump chips)
- Range Matrix (13 presets across 6 levels, lock indicators, lock matrix shield)
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_head.html')
TAIL_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_tail.js')

# --- 1. Additional CSS for Gating & Locks ---
LOCK_CSS = """
/* ==========================================================================
   Progressive Level Gating & Lock Styles
   ========================================================================== */

/* Locked Article Card */
.article-card.locked {
  position: relative;
  border-color: rgba(245, 158, 11, 0.35);
  background: var(--bg-card);
  transition: all 0.2s ease;
}
.article-card.locked:hover {
  border-color: #f59e0b;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
}
.article-card.locked::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #f59e0b, #ef4444);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.badge-lock {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 12px;
  background: rgba(245, 158, 11, 0.18);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.4);
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
body.theme-light .badge-lock {
  background: #fef3c7;
  color: #b45309;
  border-color: #fde68a;
}
body.theme-light .article-card.locked {
  border-color: #cbd5e1;
}

/* Quiz Lock Shield */
.quiz-locked-shield {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2.5rem 1.5rem;
  background: var(--bg-surface);
  border: 1.5px dashed rgba(245, 158, 11, 0.5);
  border-radius: 12px;
  margin: 1rem 0;
}
.quiz-locked-shield h3 {
  font-size: 1.3rem;
  font-weight: 800;
  color: #fbbf24;
  margin-bottom: 0.5rem;
}
.quiz-locked-shield p {
  font-size: 0.92rem;
  color: var(--text-muted);
  max-width: 500px;
  line-height: 1.55;
  margin-bottom: 1.25rem;
}

/* Matrix Lock Shield */
.matrix-locked-shield {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 1.5rem;
  background: var(--bg-surface);
  border: 2px dashed rgba(245, 158, 11, 0.5);
  border-radius: 14px;
  margin: 0.5rem 0;
}
.matrix-locked-shield h3 {
  font-size: 1.4rem;
  font-weight: 800;
  color: #fbbf24;
  margin-bottom: 0.5rem;
}
.matrix-locked-shield p {
  font-size: 0.95rem;
  color: var(--text-muted);
  max-width: 480px;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

/* Level Lock Detail Box in Modal */
.lock-detail-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.lock-tier-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px dashed var(--border-color);
  padding-bottom: 0.75rem;
}
.lock-tip-quote {
  font-size: 0.88rem;
  color: var(--text-main);
  background: var(--bg-card);
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border-left: 3.5px solid #f59e0b;
  line-height: 1.55;
}
"""

LEVEL_LOCK_MODAL_HTML = """
  <!-- Level Lock Informational Modal -->
  <div class="ai-modal-overlay" id="level-lock-modal-overlay" style="display: none;" onclick="if(event.target === this) characterManager.closeLevelLockModal()">
    <div class="char-create-modal" style="max-width: 540px;">
      <div class="char-modal-header" style="background: rgba(245, 158, 11, 0.1); border-bottom-color: rgba(245, 158, 11, 0.3);">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
          <span style="font-size: 1.6rem;">🔒</span>
          <div>
            <h3 style="font-size: 1.15rem; font-weight: 800; color: #fbbf24; margin: 0;">레벨 제한 콘텐츠 안내</h3>
            <span style="font-size: 0.78rem; color: var(--text-dim);">단계별 포커 실력 향상 & 커리큘럼 잠금</span>
          </div>
        </div>
        <button onclick="characterManager.closeLevelLockModal()" style="background: none; border: none; color: #94a3b8; font-size: 1.3rem; cursor: pointer;">✕</button>
      </div>
      <div class="char-modal-body" style="padding: 1.5rem;">
        <div id="lock-modal-content"></div>
      </div>
      <div class="char-modal-footer">
        <button class="btn-secondary" onclick="characterManager.closeLevelLockModal()">닫기</button>
        <button class="btn-primary" id="lock-modal-action-btn" onclick="characterManager.handleLockAction()">
          🔓 해금된 기초 아티클 보기
        </button>
      </div>
    </div>
  </div>
"""

def update_head():
    with open(HEAD_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add LOCK_CSS right before </style>
    if 'Progressive Level Gating & Lock Styles' not in html:
        html = html.replace('</style>', LOCK_CSS + '\n</style>', 1)

    # 2. Update Level Filter Bar in view-articles to 6 tiers + Unlocked Only toggle button
    old_level_bar = """      <!-- Level Filter Bar -->
      <div class="filter-bar" style="margin-bottom: 1.5rem; justify-content: space-between;">
        <div class="filter-pills" id="article-level-filters">
          <span style="font-size: 0.85rem; color: var(--text-muted); align-self: center; margin-right: 0.4rem; font-weight: 600;">난이도:</span>
          <button class="filter-pill active" data-lvl="all" onclick="reader.filterLevel('all')">전체 난이도 (369)</button>
          <button class="filter-pill" data-lvl="Level 1" onclick="reader.filterLevel('Level 1')">Lv.1 입문 (21)</button>
          <button class="filter-pill" data-lvl="Level 2" onclick="reader.filterLevel('Level 2')">Lv.2 초급 (248)</button>
          <button class="filter-pill" data-lvl="Level 3" onclick="reader.filterLevel('Level 3')">Lv.3 중급 (68)</button>
          <button class="filter-pill" data-lvl="Level 4" onclick="reader.filterLevel('Level 4')">Lv.4 고급 (32)</button>
        </div>
        <div class="article-count-label" id="article-count-label" style="color: var(--text-dim); font-size: 0.9rem;">
          총 369편
        </div>
      </div>"""

    new_level_bar = """      <!-- Level Filter Bar (6 Progressive RPG Tiers) -->
      <div class="filter-bar" style="margin-bottom: 1.5rem; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;">
        <div class="filter-pills" id="article-level-filters">
          <span style="font-size: 0.85rem; color: var(--text-muted); align-self: center; margin-right: 0.4rem; font-weight: 600;">난이도:</span>
          <button class="filter-pill active" data-lvl="all" onclick="reader.filterLevel('all')">전체 난이도 (369)</button>
          <button class="filter-pill" data-lvl="Level 1" onclick="reader.filterLevel('Level 1')">Lv.1 입문 (33)</button>
          <button class="filter-pill" data-lvl="Level 2" onclick="reader.filterLevel('Level 2')">Lv.2 초급 (201)</button>
          <button class="filter-pill" data-lvl="Level 3" onclick="reader.filterLevel('Level 3')">Lv.3 중급 (47)</button>
          <button class="filter-pill" data-lvl="Level 4" onclick="reader.filterLevel('Level 4')">Lv.4 고급 (65)</button>
          <button class="filter-pill" data-lvl="Level 5" onclick="reader.filterLevel('Level 5')">Lv.5 심화 (15)</button>
          <button class="filter-pill" data-lvl="Level 6" onclick="reader.filterLevel('Level 6')">Lv.6 마스터 (8)</button>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <button class="filter-pill" id="filter-unlocked-btn" onclick="reader.toggleUnlockedOnly()" style="border: 1.5px solid #3b82f6; font-weight: 700; white-space: nowrap;">
            <span id="unlocked-only-icon">🔓</span> <span id="unlocked-only-text">내 레벨 해금 글만 보기</span>
          </button>
          <div class="article-count-label" id="article-count-label" style="color: var(--text-dim); font-size: 0.9rem; white-space: nowrap;">
            총 369편
          </div>
        </div>
      </div>"""
    html = html.replace(old_level_bar, new_level_bar)

    # 3. Add Quiz Level Filter Chips in view-trainer
    old_trainer_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <div>
            <h2 style="font-size: 1.6rem; font-weight: 800;">🎯 GTO 스팟 트레이너</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem;">실전 스팟에서 GTO 솔루션의 의사결정을 훈련하고 해설을 확인하세요.</p>
          </div>
          <div style="display: flex; gap: 0.5rem;" id="quiz-nav-controls">
            <button class="btn-secondary" onclick="trainer.prevQuiz()">◀ 이전</button>
            <span id="quiz-counter" style="padding: 0.6rem 1rem; background: var(--bg-card); border-radius: 8px; font-weight: 700;">1 / 25</span>
            <button class="btn-secondary" onclick="trainer.nextQuiz()">다음 ▶</button>
          </div>
        </div>"""

    new_trainer_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;">
          <div>
            <h2 style="font-size: 1.6rem; font-weight: 800;">🎯 GTO 스팟 트레이너 (25스팟)</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem;">실전 스팟에서 GTO 솔루션의 의사결정을 훈련하고 해설을 확인하세요. (레벨별 순차 해금)</p>
          </div>
          <div style="display: flex; gap: 0.5rem;" id="quiz-nav-controls">
            <button class="btn-secondary" onclick="trainer.prevQuiz()">◀ 이전</button>
            <span id="quiz-counter" style="padding: 0.6rem 1rem; background: var(--bg-card); border-radius: 8px; font-weight: 700;">1 / 25</span>
            <button class="btn-secondary" onclick="trainer.nextQuiz()">다음 ▶</button>
          </div>
        </div>

        <!-- Quiz Level Jump Selector -->
        <div style="display: flex; gap: 0.35rem; margin-bottom: 1.25rem; flex-wrap: wrap;" id="quiz-level-filter-chips">
          <button class="filter-pill active" data-qlvl="1" onclick="trainer.jumpToLevel(1)">Lv.1 입문 (1~5)</button>
          <button class="filter-pill" data-qlvl="2" onclick="trainer.jumpToLevel(2)">Lv.2 초급 (6~10)</button>
          <button class="filter-pill" data-qlvl="3" onclick="trainer.jumpToLevel(3)">Lv.3 중급 (11~15)</button>
          <button class="filter-pill" data-qlvl="4" onclick="trainer.jumpToLevel(4)">Lv.4 고급 (16~19)</button>
          <button class="filter-pill" data-qlvl="5" onclick="trainer.jumpToLevel(5)">Lv.5 심화 (20~22)</button>
          <button class="filter-pill" data-qlvl="6" onclick="trainer.jumpToLevel(6)">Lv.6 마스터 (23~25)</button>
        </div>"""
    html = html.replace(old_trainer_header, new_trainer_header)

    # 4. Insert Level Lock Modal right before <script>
    if 'id="level-lock-modal-overlay"' not in html:
        html = html.replace('<script>', LEVEL_LOCK_MODAL_HTML + '\n  <script>')

    with open(HEAD_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched bundle_head.html with progressive gating successfully!")


def update_tail():
    with open(TAIL_PATH, 'r', encoding='utf-8') as f:
        tail = f.read()

    # 1. Update characterManager with Level Lock Modal methods
    char_lock_methods = """
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
"""

    if 'showLevelLockModal' not in tail:
        tail = tail.replace('saveCharacter() {', char_lock_methods + '\n  saveCharacter() {')

    # 2. Update reader with progressive gating logic
    # Add unlockedOnly flag
    tail = tail.replace(
        "searchQuery: '',\n  displayLimit: 24,",
        "searchQuery: '',\n  displayLimit: 24,\n  unlockedOnly: false,"
    )

    # Add toggleUnlockedOnly method
    toggle_method = """  toggleUnlockedOnly(forceState = null) {
    if (forceState !== null) {
      this.unlockedOnly = forceState;
    } else {
      this.unlockedOnly = !this.unlockedOnly;
    }

    const btn = document.getElementById('filter-unlocked-btn');
    const icon = document.getElementById('unlocked-only-icon');
    const text = document.getElementById('unlocked-only-text');
    if (btn) {
      if (this.unlockedOnly) {
        btn.classList.add('active');
        if (icon) icon.innerText = '🔒';
        if (text) text.innerText = '전체 아티클 보기';
      } else {
        btn.classList.remove('active');
        if (icon) icon.innerText = '🔓';
        if (text) text.innerText = '내 레벨 해금 글만 보기';
      }
    }

    this.displayLimit = 24;
    this.renderArticleCards();
    if (window.app && app.playAudioEffect) app.playAudioEffect('click');
  },
"""
    if 'toggleUnlockedOnly' not in tail:
        tail = tail.replace('loadArticles() {', toggle_method + '\n  loadArticles() {')

    # Update reader.updateFilterPillsUI() to handle 6 levels and display lock icons
    old_update_pills = """    // 3. Dynamically update Level pill counts based on active category
    const levelLabels = {
      'Level 1': 'Lv.1 입문',
      'Level 2': 'Lv.2 초급',
      'Level 3': 'Lv.3 중급',
      'Level 4': 'Lv.4 고급'
    };

    document.querySelectorAll('#article-level-filters .filter-pill').forEach(pill => {
      const l = pill.dataset.lvl;
      if (l === 'all') {
        const cnt = this.articles.filter(a => this.activeCategory === 'all' || a.category === this.activeCategory).length;
        pill.innerText = `전체 난이도 (${cnt})`;
        pill.style.opacity = '1';
      } else {
        const cnt = this.articles.filter(a => 
          (this.activeCategory === 'all' || a.category === this.activeCategory) && a.level.startsWith(l)
        ).length;
        pill.innerText = `${levelLabels[l] || l} (${cnt})`;
        pill.style.opacity = (cnt === 0) ? '0.45' : '1';
      }
    });"""

    new_update_pills = """    // 3. Dynamically update Level pill counts and Lock badges based on active category & user level
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
    });"""
    tail = tail.replace(old_update_pills, new_update_pills)

    # Update reader.renderArticleCards() to respect unlockedOnly, render lock cards, and handle lock modal clicks
    old_card_filter = """    const filtered = this.articles.filter(a => {
      if (this.activeCategory !== 'all' && a.category !== this.activeCategory) return false;
      if (this.activeLevel !== 'all' && !a.level.startsWith(this.activeLevel)) return false;
      if (this.searchQuery) {
        const pool = `${a.title_ko} ${a.title_en} ${a.category} ${a.level} ${a.slug}`.toLowerCase();
        if (!pool.includes(this.searchQuery)) return false;
      }
      return true;
    });"""

    new_card_filter = """    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const filtered = this.articles.filter(a => {
      if (this.activeCategory !== 'all' && a.category !== this.activeCategory) return false;
      if (this.activeLevel !== 'all' && !a.level.startsWith(this.activeLevel)) return false;
      if (this.unlockedOnly && (a.required_level || 1) > userLvl) return false;
      if (this.searchQuery) {
        const pool = `${a.title_ko} ${a.title_en} ${a.category} ${a.level} ${a.slug}`.toLowerCase();
        if (!pool.includes(this.searchQuery)) return false;
      }
      return true;
    });"""
    tail = tail.replace(old_card_filter, new_card_filter)

    old_card_render = """    container.innerHTML = slice.map(a => {
      const isCompleted = app.userState.completed_articles.includes(a.id);
      return `
        <div class="article-card" onclick="reader.openArticle('${a.id}')">
          <div>
            <div class="article-card-header">
              <span class="badge-level">${a.level}</span>
              <span style="font-size: 0.75rem; background: var(--bg-surface); padding: 2px 7px; border-radius: 4px; color: var(--text-muted); font-weight: 600;">${a.category}</span>
              <span class="read-time" style="margin-left: auto;">⏱️ ${a.read_time}</span>
            </div>
            <h3>${a.title_ko}</h3>
            <p class="subtitle-en">${a.title_en}</p>
          </div>
          
          <div class="article-card-footer">
            <div class="author-info">✍️ ${a.author}</div>
            <div style="display: flex; gap: 0.6rem; align-items: center;">
              ${a.original_url ? `<a href="${a.original_url}" target="_blank" onclick="event.stopPropagation()" class="btn-original-link" style="padding: 2px 6px; font-size: 0.75rem;" title="GTO Wizard 공식 원문 열기">🌐 원문 ↗</a>` : ''}
              ${isCompleted ? `<span class="completed-check" title="학습 완료">✓</span>` : `<span style="font-size: 0.8rem; color: #3b82f6; font-weight: 700;">학습하기 →</span>`}
            </div>
          </div>
        </div>
      `;
    }).join('');"""

    new_card_render = """    container.innerHTML = slice.map(a => {
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
    }).join('');"""
    tail = tail.replace(old_card_render, new_card_render)

    # In reader.openArticle, check lock status and show modal if locked
    old_open_article = """  openArticle(articleId) {
    app.playAudioEffect('click');
    const data = this.articles.find(a => a.id === articleId || a.slug === articleId);
    if (!data) return;
    this.currentArticle = data;"""

    new_open_article = """  openArticle(articleId) {
    const data = this.articles.find(a => a.id === articleId || a.slug === articleId);
    if (!data) return;

    const userLvl = app.getLevelInfo(app.userState.xp).level;
    const isLocked = (data.required_level || 1) > userLvl;

    if (isLocked) {
      characterManager.showLevelLockModal(data);
      return;
    }

    app.playAudioEffect('click');
    this.currentArticle = data;"""
    tail = tail.replace(old_open_article, new_open_article)

    # 3. Update trainer with level chips and locked quiz shield
    old_trainer_render = """  renderCurrentQuiz() {
    if (!this.quizzes.length) return;
    const q = this.quizzes[this.currentIndex];
    this.isAnswered = false;

    document.getElementById('quiz-counter').innerText = `${this.currentIndex + 1} / ${this.quizzes.length}`;
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
    document.getElementById('trainer-question-text').innerText = q.question;

    const feedbackBox = document.getElementById('trainer-feedback-box');
    feedbackBox.style.display = 'none';

    const optGrid = document.getElementById('trainer-options-grid');
    optGrid.innerHTML = q.options.map((opt, i) => `
      <button class="quiz-opt-btn" id="quiz-btn-${i}" onclick="trainer.selectOption(${i})">
        <span>${opt.label}</span>
        <span style="font-size: 0.85rem; color: var(--text-dim); font-weight: 500;">선택</span>
      </button>
    `).join('');
  },"""

    new_trainer_render = """  jumpToLevel(lvl) {
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
  },"""
    tail = tail.replace(old_trainer_render, new_trainer_render)

    # 4. Update matrix with progressive gating logic
    old_matrix_load = """    this.currentPreset = preset;

    // Sync select dropdown
    const selectEl = document.getElementById('matrix-preset-select');
    if (selectEl && selectEl.value !== presetId) {
      selectEl.value = presetId;
    }

    // Sync quick-chips active state
    document.querySelectorAll('#matrix-quick-chips button').forEach(btn => {
      if (btn.dataset.pid === presetId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    document.getElementById('matrix-preset-desc').innerText = preset.description;

    const legendEl = document.getElementById('matrix-legend-container');
    legendEl.innerHTML = preset.legend.map(l => `
      <div class="legend-item">
        <div class="legend-color-box" style="background: ${l.color};"></div>
        <span style="font-weight: 600;">${l.label}</span>
      </div>
    `).join('');

    this.calculateRangeStats();
    this.renderGrid();"""

    new_matrix_load = """    const userLvlInfo = app.getLevelInfo(app.userState.xp);
    const userLvl = userLvlInfo.level;
    const isLocked = (preset.required_level || 1) > userLvl;

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
    this.renderGrid();"""
    tail = tail.replace(old_matrix_load, new_matrix_load)

    with open(TAIL_PATH, 'w', encoding='utf-8') as f:
        f.write(tail)
    print("Patched bundle_tail.js with progressive gating successfully!")


if __name__ == '__main__':
    update_head()
    update_tail()
