/**
 * Skill Tree Roadmap & Achievements Controller
 */

const roadmap = {
  data: null,

  async load() {
    try {
      const resp = await fetch('/api/roadmap');
      this.data = await resp.json();
      this.render();
    } catch (e) {
      console.error('Failed to load roadmap:', e);
    }
  },

  render() {
    if (!this.data) return;
    const { user_state, roadmap: rm } = this.data;

    // Render Levels
    const levelsContainer = document.getElementById('roadmap-levels-container');
    levelsContainer.innerHTML = rm.levels.map(lvl => {
      const isLocked = !lvl.is_unlocked;
      return `
        <div class="roadmap-level-card ${isLocked ? 'locked' : ''}">
          <div class="level-badge-header">
            <div>
              <h3 style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">${lvl.title}</h3>
              <p style="font-size: 0.85rem; color: var(--text-dim);">${lvl.subtitle}</p>
            </div>
            <span class="level-badge">${lvl.badge}</span>
          </div>

          <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1rem;">
            ${lvl.description}
          </p>

          ${isLocked ? `
            <div style="background: rgba(0,0,0,0.4); padding: 0.75rem; border-radius: 8px; font-size: 0.85rem; color: #f59e0b; font-weight: 700;">
              🔒 해금 조건: ${lvl.required_xp} XP 달성 필요 (현재: ${user_state.xp} XP)
            </div>
          ` : `
            <div class="nodes-list">
              ${lvl.nodes.map(n => `
                <div class="node-item ${n.is_completed ? 'completed' : ''}" onclick="reader.openArticle('${n.article_id}')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.2rem;">${n.is_completed ? '✅' : '📖'}</span>
                    <div>
                      <div style="font-weight: 700; font-size: 0.95rem; color: #ffffff;">${n.title}</div>
                      <span style="font-size: 0.75rem; color: #94a3b8;">${n.category}</span>
                    </div>
                  </div>
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 0.8rem; color: #fbbf24; font-weight: 700;">+${n.xp} XP</span>
                    <button class="btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">
                      ${n.is_completed ? '다시 읽기' : '학습 시작'}
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          `}
        </div>
      `;
    }).join('');

    // Render Achievements
    const achContainer = document.getElementById('roadmap-achievements-container');
    achContainer.innerHTML = rm.achievements.map(a => `
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
};
