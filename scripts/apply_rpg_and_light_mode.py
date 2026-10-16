# -*- coding: utf-8 -*-
"""
apply_rpg_and_light_mode.py
Updates templates/bundle_head.html and templates/bundle_tail.js to implement:
1. Default Light Mode
2. Roadmap as Primary First View
3. RPG Character Creation and Growth System
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_head.html')
TAIL_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_tail.js')

# --- 1. RPG CSS ---
RPG_CSS = """
/* ==========================================================================
   RPG Character Persona & Growth System Styles
   ========================================================================== */

/* Header Character Pill */
.char-header-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-surface);
  border: 1.5px solid var(--border-color);
  border-radius: 24px;
  padding: 0.2rem 0.85rem 0.2rem 0.35rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-main);
  height: 38px;
  white-space: nowrap;
}
.char-header-pill:hover {
  border-color: #3b82f6;
  background: var(--bg-card-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}
.char-avatar-icon {
  font-size: 1.35rem;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.15);
  border-radius: 50%;
}
.char-header-info {
  display: flex;
  flex-direction: column;
  text-align: left;
  line-height: 1.15;
}
.char-header-name {
  font-size: 0.82rem;
  font-weight: 800;
  color: var(--text-main);
}
.char-header-tag {
  font-size: 0.68rem;
  color: #3b82f6;
  font-weight: 700;
}

/* Character Dashboard Card */
.character-dashboard {
  margin-bottom: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.char-hero-card {
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.75rem 2rem;
  display: flex;
  align-items: center;
  gap: 1.75rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  transition: all 0.25s ease;
}

.char-hero-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #10b981, #f59e0b, #ec4899);
}

.char-avatar-wrapper {
  position: relative;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}
.char-avatar-wrapper:hover {
  transform: scale(1.06);
}
.char-avatar-display {
  width: 86px;
  height: 86px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(16, 185, 129, 0.2));
  border: 3px solid #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.2rem;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
  user-select: none;
}
.char-avatar-edit-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  background: #3b82f6;
  color: #ffffff;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 12px;
  border: 1.5px solid var(--bg-card);
  white-space: nowrap;
}

.char-main-info {
  flex: 1;
  min-width: 0;
}
.char-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.char-name-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.char-name-title {
  font-size: 1.65rem;
  font-weight: 900;
  color: var(--text-main);
  letter-spacing: -0.5px;
  margin: 0;
}
.char-style-tag {
  font-size: 0.8rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 14px;
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}
.char-tier-badge {
  font-size: 0.82rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 14px;
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.35);
}
.btn-character-edit {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 0.45rem 0.95rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s ease;
}
.btn-character-edit:hover {
  border-color: #3b82f6;
  background: var(--bg-card-hover);
  color: #3b82f6;
}

.char-bio-text {
  font-size: 0.92rem;
  color: var(--text-muted);
  margin-bottom: 1.15rem;
  line-height: 1.5;
}

.char-level-progress-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.75rem 1rem;
}
.char-xp-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  font-weight: 700;
  margin-bottom: 0.45rem;
}
.char-xp-current {
  color: #3b82f6;
}
.char-xp-remaining {
  color: var(--text-dim);
}
.char-progress-track {
  height: 10px;
  background: var(--bg-card);
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}
.char-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #10b981, #06b6d4);
  border-radius: 6px;
  transition: width 0.5s ease;
}

/* 4 Core RPG Stats Panel */
.char-stats-panel {
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}
.panel-subtitle {
  font-size: 1.15rem;
  font-weight: 800;
  margin-bottom: 1.15rem;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 520px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  transition: transform 0.2s ease, border-color 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
  border-color: #3b82f6;
}
.stat-icon-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.stat-emoji {
  font-size: 1.6rem;
}
.stat-name {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
}
.stat-desc {
  font-size: 0.72rem;
  color: var(--text-dim);
}
.stat-grade {
  font-size: 1rem;
  font-weight: 900;
  padding: 2px 9px;
  border-radius: 8px;
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border: 1.5px solid #3b82f6;
}
.stat-grade.grade-SS { background: rgba(236, 72, 153, 0.2); color: #ec4899; border-color: #ec4899; }
.stat-grade.grade-S { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border-color: #f59e0b; }
.stat-grade.grade-A { background: rgba(16, 185, 129, 0.2); color: #10b981; border-color: #10b981; }
.stat-grade.grade-B { background: rgba(59, 130, 246, 0.2); color: #3b82f6; border-color: #3b82f6; }
.stat-grade.grade-C { background: rgba(100, 116, 139, 0.2); color: #94a3b8; border-color: #94a3b8; }
.stat-grade.grade-D { background: rgba(148, 163, 184, 0.15); color: #64748b; border-color: #64748b; }

.stat-bar-track {
  height: 8px;
  background: var(--bg-card);
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}
.stat-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}
.stat-bar-fill.theory { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.stat-bar-fill.decision { background: linear-gradient(90deg, #10b981, #34d399); }
.stat-bar-fill.ranges { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.stat-bar-fill.mental { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.stat-val-text {
  font-size: 0.78rem;
  color: var(--text-dim);
  text-align: right;
  font-weight: 700;
}

/* Fast Action Quests Box */
.char-quests-box {
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}
.quest-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.quest-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.quest-item {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.9rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}
.quest-item:hover {
  border-color: #3b82f6;
  background: var(--bg-card-hover);
}
.quest-info {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.quest-check {
  font-size: 1.4rem;
}
.quest-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-main);
}
.quest-reward {
  font-size: 0.78rem;
  color: #fbbf24;
  font-weight: 700;
}

/* Character Creation / Edit Modal */
.char-create-modal {
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-lg);
  width: 92%;
  max-width: 680px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
  animation: modalScaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
}
@keyframes modalScaleUp {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.char-modal-header {
  padding: 1.25rem 1.75rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: var(--bg-card);
  z-index: 10;
}
.char-modal-body {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.char-modal-footer {
  padding: 1rem 1.75rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  background: var(--bg-card);
  position: sticky;
  bottom: 0;
  z-index: 10;
}

.char-form-group {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}
.char-form-label {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
}

.avatar-select-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}
@media (max-width: 500px) {
  .avatar-select-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
.avatar-option {
  background: var(--bg-surface);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  padding: 0.75rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.avatar-option:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}
.avatar-option.active {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.12);
  box-shadow: 0 0 14px rgba(59, 130, 246, 0.3);
}
.avatar-emoji {
  font-size: 2.2rem;
}
.avatar-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-main);
}

.char-input {
  flex: 1;
  background: var(--bg-surface);
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  padding: 0.65rem 1rem;
  color: var(--text-main);
  font-size: 0.95rem;
  outline: none;
  font-weight: 700;
}
.char-input:focus {
  border-color: #3b82f6;
}

.nickname-chips {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}
.chip-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  font-weight: 600;
}
.name-chip {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  border-radius: 14px;
  padding: 3px 10px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}
.name-chip:hover {
  background: #3b82f6;
  color: #ffffff;
  border-color: #3b82f6;
}

.style-select-grid {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}
.style-card {
  background: var(--bg-surface);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.style-card:hover {
  border-color: #3b82f6;
}
.style-card.active {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
}
.style-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.2rem;
}
.style-desc {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.4;
}

/* Toast Notifications */
.poker-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #1e293b;
  color: #ffffff;
  border: 1.5px solid #3b82f6;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
  font-weight: 700;
  font-size: 0.95rem;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  animation: toastSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes toastSlideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
body.theme-light .poker-toast {
  background: #ffffff;
  color: #0f172a;
  border-color: #3b82f6;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

/* Light Mode Overrides for RPG System */
body.theme-light .char-hero-card {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}
body.theme-light .char-stats-panel {
  background: #ffffff;
  border-color: #cbd5e1;
}
body.theme-light .stat-card {
  background: #f8fafc;
  border-color: #e2e8f0;
}
body.theme-light .char-quests-box {
  background: #ffffff;
  border-color: #cbd5e1;
}
body.theme-light .quest-item {
  background: #f8fafc;
  border-color: #e2e8f0;
}
body.theme-light .char-create-modal {
  background: #ffffff;
  border-color: #cbd5e1;
}
body.theme-light .char-modal-header,
body.theme-light .char-modal-footer {
  background: #ffffff;
  border-color: #e2e8f0;
}
body.theme-light .avatar-option {
  background: #f8fafc;
  border-color: #e2e8f0;
}
body.theme-light .avatar-option.active {
  background: #eff6ff;
  border-color: #3b82f6;
}
body.theme-light .style-card {
  background: #f8fafc;
  border-color: #e2e8f0;
}
body.theme-light .style-card.active {
  background: #eff6ff;
  border-color: #3b82f6;
}
body.theme-light .char-input {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #0f172a;
}
"""

# --- 2. Character Dashboard HTML ---
CHARACTER_DASHBOARD_HTML = """
        <!-- RPG Character Persona & Growth Dashboard -->
        <div class="character-dashboard" id="character-dashboard-card">
          <div class="char-hero-card">
            <div class="char-avatar-wrapper" onclick="characterManager.openModal()" title="캐릭터 아바타 변경/커스텀">
              <div class="char-avatar-display" id="dash-char-avatar">🦈</div>
              <span class="char-avatar-edit-badge">✏️ 커스텀</span>
            </div>
            <div class="char-main-info">
              <div class="char-header-row">
                <div class="char-name-group">
                  <h2 class="char-name-title" id="dash-char-name">포커신동</h2>
                  <span class="char-style-tag" id="dash-char-style">⚡ TAG 스타일</span>
                  <span class="char-tier-badge" id="dash-char-tier">Lv.1 동네 피쉬 탈출기 🐟</span>
                </div>
                <button class="btn-character-edit" onclick="characterManager.openModal()">
                  <span>🎭</span> 캐릭터 설정
                </button>
              </div>
              <p class="char-bio-text" id="dash-char-bio">
                "엄선된 프리미엄 핸드로 강력하게 주도권을 잡는 정석적인 승리 공식"
              </p>
              
              <!-- XP Bar with Level progress -->
              <div class="char-level-progress-box">
                <div class="char-xp-stats">
                  <span class="char-xp-current" id="dash-xp-text">120 / 200 XP</span>
                  <span class="char-xp-remaining" id="dash-xp-needed">다음 승급까지 80 XP 남음</span>
                </div>
                <div class="char-progress-track">
                  <div class="char-progress-fill" id="dash-xp-fill" style="width: 60%;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 4 Core RPG Poker Stats Grid -->
          <div class="char-stats-panel">
            <h3 class="panel-subtitle">📊 포커 RPG 4대 핵심 능력치</h3>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon-title">
                  <span class="stat-emoji">📚</span>
                  <div>
                    <div class="stat-name">GTO 이론력</div>
                    <div class="stat-desc">아티클 완독 시 상승</div>
                  </div>
                  <span class="stat-grade grade-C" id="stat-grade-theory">C</span>
                </div>
                <div class="stat-bar-track">
                  <div class="stat-bar-fill theory" id="stat-bar-theory" style="width: 35%;"></div>
                </div>
                <div class="stat-val-text"><span id="stat-val-theory">35</span> / 100 PTS</div>
              </div>

              <div class="stat-card">
                <div class="stat-icon-title">
                  <span class="stat-emoji">🎯</span>
                  <div>
                    <div class="stat-name">스팟 결단력</div>
                    <div class="stat-desc">퀴즈 정답 시 상승</div>
                  </div>
                  <span class="stat-grade grade-B" id="stat-grade-decision">B</span>
                </div>
                <div class="stat-bar-track">
                  <div class="stat-bar-fill decision" id="stat-bar-decision" style="width: 40%;"></div>
                </div>
                <div class="stat-val-text"><span id="stat-val-decision">40</span> / 100 PTS</div>
              </div>

              <div class="stat-card">
                <div class="stat-icon-title">
                  <span class="stat-emoji">📊</span>
                  <div>
                    <div class="stat-name">레인지 이해도</div>
                    <div class="stat-desc">매트릭스 탐색 시 상승</div>
                  </div>
                  <span class="stat-grade grade-C" id="stat-grade-ranges">C</span>
                </div>
                <div class="stat-bar-track">
                  <div class="stat-bar-fill ranges" id="stat-bar-ranges" style="width: 25%;"></div>
                </div>
                <div class="stat-val-text"><span id="stat-val-ranges">25</span> / 100 PTS</div>
              </div>

              <div class="stat-card">
                <div class="stat-icon-title">
                  <span class="stat-emoji">🧠</span>
                  <div>
                    <div class="stat-name">멘탈 & 뱅크롤</div>
                    <div class="stat-desc">연속 출석 시 상승</div>
                  </div>
                  <span class="stat-grade grade-B" id="stat-grade-mental">B</span>
                </div>
                <div class="stat-bar-track">
                  <div class="stat-bar-fill mental" id="stat-bar-mental" style="width: 50%;"></div>
                </div>
                <div class="stat-val-text"><span id="stat-val-mental">50</span> / 100 PTS</div>
              </div>
            </div>
          </div>

          <!-- Fast Action Quest Quick Links -->
          <div class="char-quests-box">
            <div class="quest-title-row">
              <span style="font-size: 1.1rem; font-weight: 800; color: var(--text-main);">⚡ 오늘의 캐릭터 고속 육성 퀘스트</span>
              <span style="font-size: 0.8rem; color: var(--text-dim);">매일 훈련하여 레벨업 달성</span>
            </div>
            <div class="quest-items-list">
              <div class="quest-item">
                <div class="quest-info">
                  <span class="quest-check" id="quest-check-article">📖</span>
                  <div>
                    <div class="quest-name">GTO 아티클 1편 정독하고 완독 버튼 누르기</div>
                    <div class="quest-reward">+50 XP • GTO 이론력 +10</div>
                  </div>
                </div>
                <button class="btn-primary" style="padding: 0.45rem 1rem; font-size: 0.85rem;" onclick="app.navigate('articles')">도서관 가기 ↗</button>
              </div>

              <div class="quest-item">
                <div class="quest-info">
                  <span class="quest-check" id="quest-check-quiz">🎯</span>
                  <div>
                    <div class="quest-name">GTO 실전 스팟 퀴즈 풀고 정답 맞히기</div>
                    <div class="quest-reward">+50 XP • 스팟 결단력 +15</div>
                  </div>
                </div>
                <button class="btn-primary" style="padding: 0.45rem 1rem; font-size: 0.85rem;" onclick="app.navigate('trainer')">퀴즈 풀기 ↗</button>
              </div>

              <div class="quest-item">
                <div class="quest-info">
                  <span class="quest-check" id="quest-check-matrix">📊</span>
                  <div>
                    <div class="quest-name">13x13 레인지 매트릭스 프리셋 탐색하기</div>
                    <div class="quest-reward">+20 XP • 레인지 이해도 +10</div>
                  </div>
                </div>
                <button class="btn-primary" style="padding: 0.45rem 1rem; font-size: 0.85rem;" onclick="app.navigate('matrix')">매트릭스 보기 ↗</button>
              </div>
            </div>
          </div>
        </div>
"""

# --- 3. Character Modal HTML ---
CHARACTER_MODAL_HTML = """
  <!-- Character Creation / Customization Modal -->
  <div class="ai-modal-overlay" id="char-modal-overlay" style="display: none;" onclick="if(event.target === this) characterManager.closeModal()">
    <div class="char-create-modal">
      <div class="char-modal-header">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
          <span style="font-size: 1.5rem;">🎭</span>
          <div>
            <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--text-main); margin: 0;">포커 페르소나 캐릭터 생성 / 커스텀</h3>
            <p style="font-size: 0.8rem; color: var(--text-dim); margin: 0;">나만의 포커 플레이어 캐릭터를 만들고 GTO 마스터로 육성하세요.</p>
          </div>
        </div>
        <button onclick="characterManager.closeModal()" style="background: none; border: none; color: #94a3b8; font-size: 1.3rem; cursor: pointer;">✕</button>
      </div>

      <div class="char-modal-body">
        <!-- 1. Avatar Picker -->
        <div class="char-form-group">
          <label class="char-form-label">1. 캐릭터 아바타 선택</label>
          <div class="avatar-select-grid" id="avatar-picker-grid">
            <div class="avatar-option active" data-avatar="🦈" onclick="characterManager.selectAvatar('🦈')">
              <span class="avatar-emoji">🦈</span>
              <span class="avatar-name">샤크</span>
            </div>
            <div class="avatar-option" data-avatar="🦊" onclick="characterManager.selectAvatar('🦊')">
              <span class="avatar-emoji">🦊</span>
              <span class="avatar-name">여우</span>
            </div>
            <div class="avatar-option" data-avatar="🦁" onclick="characterManager.selectAvatar('🦁')">
              <span class="avatar-emoji">🦁</span>
              <span class="avatar-name">사자</span>
            </div>
            <div class="avatar-option" data-avatar="🦉" onclick="characterManager.selectAvatar('🦉')">
              <span class="avatar-emoji">🦉</span>
              <span class="avatar-name">부엉이</span>
            </div>
            <div class="avatar-option" data-avatar="👑" onclick="characterManager.selectAvatar('👑')">
              <span class="avatar-emoji">👑</span>
              <span class="avatar-name">황제</span>
            </div>
            <div class="avatar-option" data-avatar="🥷" onclick="characterManager.selectAvatar('🥷')">
              <span class="avatar-emoji">🥷</span>
              <span class="avatar-name">닌자</span>
            </div>
            <div class="avatar-option" data-avatar="🤖" onclick="characterManager.selectAvatar('🤖')">
              <span class="avatar-emoji">🤖</span>
              <span class="avatar-name">사이보그</span>
            </div>
            <div class="avatar-option" data-avatar="🐟" onclick="characterManager.selectAvatar('🐟')">
              <span class="avatar-emoji">🐟</span>
              <span class="avatar-name">피쉬</span>
            </div>
          </div>
        </div>

        <!-- 2. Nickname Input -->
        <div class="char-form-group">
          <label class="char-form-label">2. 플레이어 닉네임 설정</label>
          <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
            <input type="text" id="char-name-input" maxlength="12" placeholder="닉네임 입력 (최대 12자)" class="char-input" value="포커신동">
            <button class="btn-secondary" style="white-space: nowrap;" onclick="characterManager.randomizeName()">🎲 추천 닉네임</button>
          </div>
          <div class="nickname-chips">
            <span class="chip-label">추천:</span>
            <button class="name-chip" onclick="characterManager.setName('강남샤크')">강남샤크</button>
            <button class="name-chip" onclick="characterManager.setName('GTO마법사')">GTO마법사</button>
            <button class="name-chip" onclick="characterManager.setName('체크레이즈달인')">체크레이즈달인</button>
            <button class="name-chip" onclick="characterManager.setName('리버원샷')">리버원샷</button>
            <button class="name-chip" onclick="characterManager.setName('폴푸아수제자')">폴푸아수제자</button>
          </div>
        </div>

        <!-- 3. Playstyle Selection -->
        <div class="char-form-group">
          <label class="char-form-label">3. 선호 플레이 스타일</label>
          <div class="style-select-grid" id="style-picker-grid">
            <div class="style-card active" data-style="TAG" onclick="characterManager.selectStyle('TAG')">
              <div class="style-title">⚡ TAG (타이트 어그레시브)</div>
              <div class="style-desc">엄선된 프리미엄 핸드로 강력하게 주도권을 잡는 정석적인 승리 공식</div>
            </div>
            <div class="style-card" data-style="LAG" onclick="characterManager.selectStyle('LAG')">
              <div class="style-title">🔥 LAG (루즈 어그레시브)</div>
              <div class="style-desc">넓은 레인지와 포스트플랍 공격성으로 상대에게 끊임없는 압박 부여</div>
            </div>
            <div class="style-card" data-style="GTO" onclick="characterManager.selectStyle('GTO')">
              <div class="style-title">🧠 GTO Solved (솔버 밸런스)</div>
              <div class="style-desc">수학적 균형과 빈도 밸런싱으로 상대의 익스플로잇을 완벽 차단</div>
            </div>
            <div class="style-card" data-style="EXPLOIT" onclick="characterManager.selectStyle('EXPLOIT')">
              <div class="style-title">🎯 Exploitative (익스플로잇)</div>
              <div class="style-desc">상대의 성향적 약점과 릭(Leak)을 파악하여 최대 EV를 추출</div>
            </div>
            <div class="style-card" data-style="HUNTER" onclick="characterManager.selectStyle('HUNTER')">
              <div class="style-title">🦈 Fish Hunter (피쉬 헌터)</div>
              <div class="style-desc">불필요한 블러프를 배제하고 탄탄한 밸류 벳으로 스택을 빨아들이는 스타일</div>
            </div>
          </div>
        </div>
      </div>

      <div class="char-modal-footer">
        <button class="btn-secondary" onclick="characterManager.closeModal()">취소</button>
        <button class="btn-primary" style="padding: 0.65rem 1.8rem; font-weight: 800;" onclick="characterManager.saveCharacter()">
          ✨ 캐릭터 저장 및 육성 시작
        </button>
      </div>
    </div>
  </div>
"""

def patch_head():
    with open(HEAD_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert RPG CSS right before </style>
    if 'RPG Character Persona & Growth System Styles' not in html:
        html = html.replace('</style>', RPG_CSS + '\n</style>', 1)

    # 2. Set default body class to theme-light
    html = re.sub(r'<body(?:\s+class="[^"]*")?>', '<body class="theme-light">', html, count=1)

    # 3. Header updates:
    # 3a. Brand click to roadmap
    html = html.replace('<div class="brand" onclick="app.navigate(\'articles\')">', '<div class="brand" onclick="app.navigate(\'roadmap\')">')

    # 3b. Nav buttons order: Roadmap first and active
    old_nav = """      <nav class="main-nav">
        <button class="nav-btn active" data-target="articles" onclick="app.navigate('articles')">
          <span>📚</span> 아티클 도서관 (369)
        </button>
        <button class="nav-btn" data-target="trainer" onclick="app.navigate('trainer')">
          <span>🎯</span> 스팟 퀴즈 (25)
        </button>
        <button class="nav-btn" data-target="matrix" onclick="app.navigate('matrix')">
          <span>📊</span> 레인지 매트릭스
        </button>
        <button class="nav-btn" data-target="roadmap" onclick="app.navigate('roadmap')">
          <span>🗺️</span> 로드맵
        </button>
        <button class="nav-btn" data-target="glossary" onclick="app.navigate('glossary')">
          <span>📖</span> 용어 사전
        </button>
      </nav>"""

    new_nav = """      <nav class="main-nav">
        <button class="nav-btn active" data-target="roadmap" onclick="app.navigate('roadmap')">
          <span>🗺️</span> 성장 로드맵
        </button>
        <button class="nav-btn" data-target="articles" onclick="app.navigate('articles')">
          <span>📚</span> 아티클 도서관 (369)
        </button>
        <button class="nav-btn" data-target="trainer" onclick="app.navigate('trainer')">
          <span>🎯</span> 스팟 퀴즈 (25)
        </button>
        <button class="nav-btn" data-target="matrix" onclick="app.navigate('matrix')">
          <span>📊</span> 레인지 매트릭스
        </button>
        <button class="nav-btn" data-target="glossary" onclick="app.navigate('glossary')">
          <span>📖</span> 용어 사전
        </button>
      </nav>"""
    html = html.replace(old_nav, new_nav)

    # 3c. User bar: Light mode button text initially '다크 모드' (since light mode is default), add Character Pill
    old_user_bar_start = """      <div class="user-bar">
        <button class="theme-toggle-btn" id="theme-toggle-btn" onclick="themeManager.toggle()" title="화면 테마 변경">
          <span id="theme-icon">☀️</span> <span id="theme-text">라이트 모드</span>
        </button>

        <div class="streak-pill">
          <span>🔥</span> <span id="user-streak">3</span>일 연속
        </div>"""

    new_user_bar_start = """      <div class="user-bar">
        <button class="theme-toggle-btn" id="theme-toggle-btn" onclick="themeManager.toggle()" title="화면 테마 변경">
          <span id="theme-icon">🌙</span> <span id="theme-text">다크 모드</span>
        </button>

        <!-- Clickable Character Persona Header Pill -->
        <button class="char-header-pill" id="char-header-pill" onclick="characterManager.openModal()" title="내 포커 캐릭터 프로필 및 커스텀">
          <span class="char-avatar-icon" id="header-char-avatar">🦈</span>
          <div class="char-header-info">
            <span class="char-header-name" id="header-char-name">포커신동</span>
            <span class="char-header-tag" id="header-char-style">TAG</span>
          </div>
        </button>

        <div class="streak-pill" title="연속 출석 스트릭">
          <span>🔥</span> <span id="user-streak">3</span>일 연속
        </div>"""
    html = html.replace(old_user_bar_start, new_user_bar_start)

    # 4. Extract view-roadmap and move it as the FIRST section under <main>, with character dashboard!
    # Let's locate view-roadmap
    roadmap_pattern = r'(<!-- 5\. Roadmap & Skill Tree View -->\s*<section id="view-roadmap" class="view-section">.*?</section>)'
    roadmap_match = re.search(roadmap_pattern, html, flags=re.DOTALL)
    if roadmap_match:
        roadmap_block = roadmap_match.group(1)
        # Remove it from old location
        html = html.replace(roadmap_block, '')

        # Modify roadmap_block to be active and have character dashboard
        roadmap_block = roadmap_block.replace('class="view-section"', 'class="view-section active"')
        roadmap_block = roadmap_block.replace(
            '<div class="roadmap-container">',
            '<div class="roadmap-container">\n' + CHARACTER_DASHBOARD_HTML
        )

        # In view-articles, remove class="view-section active" -> class="view-section"
        html = html.replace('<section id="view-articles" class="view-section active">', '<section id="view-articles" class="view-section">')

        # Insert roadmap right after <main>
        html = html.replace('<main>', '<main>\n\n    ' + roadmap_block)

    # 5. Insert Character Modal right before <script>
    if 'id="char-modal-overlay"' not in html:
        html = html.replace('<script>', CHARACTER_MODAL_HTML + '\n  <script>')

    with open(HEAD_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched bundle_head.html successfully!")


def patch_tail():
    with open(TAIL_PATH, 'r', encoding='utf-8') as f:
        tail = f.read()

    # 1. Update themeManager default to light
    tail = tail.replace(
        "theme: localStorage.getItem('studypoker_theme') || 'dark'",
        "theme: localStorage.getItem('studypoker_theme') || 'light'"
    )

    # 2. Update storage.get() with character attributes
    old_storage = """    return {
      xp: 120,
      level: 1,
      streak: 3,
      completed_articles: ['what-is-expected-value-in-poker'],
      completed_quizzes: []
    };"""

    new_storage = """    return {
      name: '포커신동',
      avatar: '🦈',
      playstyle: 'TAG',
      xp: 120,
      level: 1,
      streak: 3,
      stats: {
        theory: 35,
        decision: 40,
        ranges: 25,
        mental: 50
      },
      completed_articles: ['what-is-expected-value-in-poker'],
      completed_quizzes: []
    };"""

    # Also handle saved parsing to inject defaults if missing
    old_saved_parsing = """    if (saved) {
      try { return JSON.parse(saved); } catch(e) {}
    }"""
    new_saved_parsing = """    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (!parsed.name) parsed.name = '포커신동';
        if (!parsed.avatar) parsed.avatar = '🦈';
        if (!parsed.playstyle) parsed.playstyle = 'TAG';
        if (!parsed.stats) parsed.stats = { theory: 35, decision: 40, ranges: 25, mental: 50 };
        return parsed;
      } catch(e) {}
    }"""
    tail = tail.replace(old_saved_parsing, new_saved_parsing)
    tail = tail.replace(old_storage, new_storage)

    # 3. Add constants and characterManager before `const app = {`
    character_js = """
// 6-Tier RPG Level System
const LEVEL_TIERS = [
  { level: 1, title: "Lv.1 동네 피쉬 탈출기 🐟", badge: "🐣 피쉬 탈출", minXp: 0, maxXp: 200, tierName: "동네 피쉬" },
  { level: 2, title: "Lv.2 홀덤펍 로컬 레귤러 ⚔️", badge: "⚔️ 펍 레귤러", minXp: 200, maxXp: 500, tierName: "로컬 레귤러" },
  { level: 3, title: "Lv.3 마이크로 그라인더 🔥", badge: "🔥 온라인 그라인더", minXp: 500, maxXp: 1000, tierName: "마이크로 그라인더" },
  { level: 4, title: "Lv.4 온라인 세미프로 🦊", badge: "🦊 세미프로", minXp: 1000, maxXp: 2000, tierName: "온라인 세미프로" },
  { level: 5, title: "Lv.5 하이롤러 토너 크러셔 🦁", badge: "🦁 하이롤러", minXp: 2000, maxXp: 4000, tierName: "토너 크러셔" },
  { level: 6, title: "Lv.6 WSOP 챔피언 👑", badge: "👑 WSOP 챔피언", minXp: 4000, maxXp: 9999, tierName: "세계 챔피언" }
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
  },

  openModal() {
    const u = app.userState;
    this.selectedAvatar = u.avatar || '🦈';
    this.selectedStyle = u.playstyle || 'TAG';

    const nameInput = document.getElementById('char-name-input');
    if (nameInput) nameInput.value = u.name || '포커신동';

    this.updateModalSelections();
    const modal = document.getElementById('char-modal-overlay');
    if (modal) modal.style.display = 'flex';
  },

  closeModal() {
    const modal = document.getElementById('char-modal-overlay');
    if (modal) modal.style.display = 'none';
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

  saveCharacter() {
    const nameInput = document.getElementById('char-name-input');
    const newName = (nameInput && nameInput.value.trim()) ? nameInput.value.trim() : '포커신동';

    app.userState.name = newName;
    app.userState.avatar = this.selectedAvatar;
    app.userState.playstyle = this.selectedStyle;

    storage.save(app.userState);
    this.renderHeader();
    this.renderDashboard();
    this.closeModal();

    if (window.app && app.playAudioEffect) app.playAudioEffect('correct');
    this.showToast(`🎉 캐릭터 [${newName}] 설정이 저장되었습니다!`);
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
    const stats = u.stats || { theory: 35, decision: 40, ranges: 25, mental: 50 };
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
"""

    if 'const characterManager =' not in tail:
        tail = tail.replace('const app = {', character_js + '\nconst app = {', 1)

    # 4. Update app object
    # Default view changed to 'roadmap'
    tail = tail.replace("currentView: 'articles'", "currentView: 'roadmap'")

    # In app.init(): default view roadmap and characterManager.init()
    old_app_init = """  init() {
    themeManager.init();
    this.updateUserBar();
    reader.loadArticles();
    matrix.init();
    roadmap.load();
    glossary.load();

    const hash = window.location.hash.replace('#', '');
    if (hash && ['articles', 'trainer', 'matrix', 'roadmap', 'glossary'].includes(hash)) {
      this.navigate(hash);
    }
  },"""

    new_app_init = """  init() {
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
  },"""
    tail = tail.replace(old_app_init, new_app_init)

    # Add getLevelInfo method and update updateUserBar & addXP
    old_user_bar_func = """  updateUserBar() {
    const xp = this.userState.xp;
    let levelTitle = "Lv.1 피쉬 탈출";
    let nextThreshold = 200;
    let prevThreshold = 0;

    if (xp >= 800) {
      levelTitle = "Lv.4 GTO 마스터 👑";
      prevThreshold = 800;
      nextThreshold = 1500;
    } else if (xp >= 500) {
      levelTitle = "Lv.3 온라인 그라인더 🔥";
      prevThreshold = 500;
      nextThreshold = 800;
    } else if (xp >= 200) {
      levelTitle = "Lv.2 펍 레귤러 ⚔️";
      prevThreshold = 200;
      nextThreshold = 500;
    }

    const currentLevelXp = xp - prevThreshold;
    const requiredLevelXp = nextThreshold - prevThreshold;
    const pct = Math.min(100, Math.round((currentLevelXp / requiredLevelXp) * 100));

    document.getElementById('user-level-badge').innerText = levelTitle;
    document.getElementById('user-xp-text').innerText = `${xp} / ${nextThreshold} XP`;
    document.getElementById('user-xp-bar').style.width = `${pct}%`;
    document.getElementById('user-streak').innerText = this.userState.streak;
    storage.save(this.userState);
  },

  addXP(amount) {
    this.userState.xp += amount;
    this.updateUserBar();
    this.playAudioEffect('xp');
  },"""

    new_user_bar_func = """  getLevelInfo(xp) {
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
    return { level: 1, title: "Lv.1 동네 피쉬 탈출기 🐟", badge: "🐣 피쉬 탈출", minXp: 0, maxXp: 200, progressPct: 0, remainingXp: 200, tierName: "동네 피쉬" };
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
    storage.save(this.userState);
  },

  addXP(amount, type = 'general') {
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
  },"""
    tail = tail.replace(old_user_bar_func, new_user_bar_func)

    # 5. Connect XP triggers
    # In reader.markCompleted()
    tail = tail.replace("app.addXP(50);", "app.addXP(50, 'article');")

    # In trainer.submitAnswer()
    tail = tail.replace("app.addXP(50);", "app.addXP(50, 'quiz');")

    with open(TAIL_PATH, 'w', encoding='utf-8') as f:
        f.write(tail)
    print("Patched bundle_tail.js successfully!")


if __name__ == '__main__':
    patch_head()
    patch_tail()
