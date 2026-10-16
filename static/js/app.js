/**
 * Main Application Controller
 * Handles SPA navigation, audio synthesis, user state, and XP updates.
 */

const app = {
  currentView: 'articles',
  userState: {
    xp: 120,
    level: 1,
    streak: 3
  },

  init() {
    this.setupNavigation();
    this.updateUserBar();
    reader.loadArticles();
    matrix.init();
    
    // Check hash route if any
    const hash = window.location.hash.replace('#', '');
    if (hash && ['articles', 'trainer', 'matrix', 'roadmap', 'glossary'].includes(hash)) {
      this.navigate(hash);
    }
  },

  navigate(viewId) {
    this.currentView = viewId;
    window.location.hash = viewId;
    
    // Hide all view sections
    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.remove('active');
    });

    // Show target section
    const targetSection = document.getElementById(`view-${viewId}`);
    if (targetSection) {
      targetSection.classList.add('active');
    }

    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // View specific activations
    if (viewId === 'trainer') {
      trainer.init();
    } else if (viewId === 'roadmap') {
      roadmap.load();
    } else if (viewId === 'glossary') {
      glossary.load();
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  setupNavigation() {
    window.addEventListener('popstate', () => {
      const hash = window.location.hash.replace('#', '') || 'articles';
      this.navigate(hash);
    });
  },

  updateUserBar() {
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
  },

  addXP(amount) {
    this.userState.xp += amount;
    this.updateUserBar();
    this.playAudioEffect('xp');
  },

  // Web Audio API Sound Effects (zero external dependencies)
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
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }
};

window.addEventListener('DOMContentLoaded', () => {
  app.init();
});
