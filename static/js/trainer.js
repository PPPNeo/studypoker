/**
 * Spot Quiz & Poker Table Simulator Controller
 * Renders poker cards, table felt, handles interactive scenario choices & EV feedback.
 */

const trainer = {
  quizzes: [],
  currentIndex: 0,
  isAnswered: false,

  async init() {
    if (!this.quizzes.length) {
      try {
        const resp = await fetch('/api/quizzes');
        this.quizzes = await resp.json();
      } catch (e) {
        console.error('Failed to load quizzes:', e);
        return;
      }
    }
    this.renderCurrentQuiz();
  },

  renderCurrentQuiz() {
    if (!this.quizzes.length) return;
    const q = this.quizzes[this.currentIndex];
    this.isAnswered = false;

    // Counter
    document.getElementById('quiz-counter').innerText = `${this.currentIndex + 1} / ${this.quizzes.length}`;

    // Table Pot
    document.getElementById('trainer-pot-display').innerText = q.pot;

    // Render Board Cards
    const boardEl = document.getElementById('trainer-board-cards');
    if (!q.board || q.board.length === 0) {
      boardEl.innerHTML = `<div style="color: #64748b; font-size: 0.9rem; font-style: italic;">[Preflop - 보드 카드 없음]</div>`;
    } else {
      boardEl.innerHTML = q.board.map(c => this.createCardHtml(c)).join('');
    }

    // Render Hero Cards
    const heroEl = document.getElementById('trainer-hero-cards');
    heroEl.innerHTML = q.hero_hand.map(c => this.createCardHtml(c)).join('');

    // Hero Position & Stack
    document.getElementById('trainer-hero-label').innerText = 
      `HERO (${q.hero_position}) • Effective Stack: ${q.effective_stack}`;

    // Question & Situation
    document.getElementById('trainer-situation-desc').innerText = q.situation;
    document.getElementById('trainer-question-text').innerText = q.question;

    // Reset Feedback Box
    const feedbackBox = document.getElementById('trainer-feedback-box');
    feedbackBox.style.display = 'none';

    // Render Options
    const optGrid = document.getElementById('trainer-options-grid');
    optGrid.innerHTML = q.options.map((opt, i) => `
      <button class="quiz-opt-btn" id="quiz-btn-${i}" onclick="trainer.selectOption(${i})">
        <span>${opt.label}</span>
        <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500;">선택</span>
      </button>
    `).join('');
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

  async selectOption(optIndex) {
    if (this.isAnswered) return;
    this.isAnswered = true;
    const q = this.quizzes[this.currentIndex];

    try {
      const resp = await fetch('/api/quizzes/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quiz_id: q.id,
          selected_option_index: optIndex
        })
      });
      const res = await resp.json();

      // Highlight options with GTO freq and correctness
      q.options.forEach((opt, i) => {
        const btn = document.getElementById(`quiz-btn-${i}`);
        btn.disabled = true;
        btn.innerHTML = `
          <span>${opt.label}</span>
          <span style="font-size: 0.85rem; font-weight: 800; color: ${opt.is_correct ? '#34d399' : '#94a3b8'};">
            GTO: ${opt.gto_freq} (EV: ${opt.ev})
          </span>
        `;
        if (i === optIndex) {
          btn.classList.add(res.is_correct ? 'correct' : 'wrong');
        } else if (opt.is_correct) {
          btn.classList.add('correct');
        }
      });

      // Show Feedback Box
      const feedbackBox = document.getElementById('trainer-feedback-box');
      const statusTitle = document.getElementById('feedback-status-title');
      const conceptTag = document.getElementById('feedback-concept-tag');
      const explanationText = document.getElementById('feedback-explanation-text');

      statusTitle.className = `feedback-status ${res.is_correct ? 'correct' : 'wrong'}`;
      statusTitle.innerText = res.is_correct ? `✅ 정답입니다! (+${res.xp_gained} XP)` : `❌ 아쉽네요! (+${res.xp_gained} XP)`;
      conceptTag.innerText = `핵심 원리: ${res.key_concept}`;
      explanationText.innerText = res.explanation;
      feedbackBox.style.display = 'block';

      app.addXP(res.xp_gained);
      app.playAudioEffect(res.is_correct ? 'correct' : 'wrong');
    } catch (e) {
      console.error(e);
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
