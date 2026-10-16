/**
 * Smart Reader Controller
 * Manages article browsing, rich reading experience, term popovers, and completion.
 */

const reader = {
  articles: [],
  currentArticle: null,
  activeCategory: 'all',

  async loadArticles() {
    try {
      const resp = await fetch('/api/articles');
      this.articles = await resp.json();
      this.renderArticleCards();
    } catch (err) {
      console.error('Failed to load articles:', err);
    }
  },

  filterCategory(cat) {
    this.activeCategory = cat;
    document.querySelectorAll('#article-category-filters .filter-pill').forEach(pill => {
      if (pill.innerText.includes(cat) || (cat === 'all' && pill.innerText.includes('전체'))) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });
    this.renderArticleCards();
  },

  renderArticleCards() {
    const container = document.getElementById('articles-grid-container');
    const filtered = this.articles.filter(a => {
      if (this.activeCategory === 'all') return true;
      return a.category === this.activeCategory;
    });

    document.getElementById('article-count-label').innerText = `총 ${filtered.length}편의 프리미엄 가이드`;

    container.innerHTML = filtered.map(a => `
      <div class="article-card" onclick="reader.openArticle('${a.id}')">
        <div>
          <div class="article-card-header">
            <span class="badge-level">${a.level}</span>
            <span class="read-time">⏱️ ${a.read_time}</span>
          </div>
          <h3>${a.title_ko}</h3>
          <p class="subtitle-en">${a.title_en}</p>
        </div>
        
        <div class="article-card-footer">
          <div class="author-info">✍️ ${a.author}</div>
          ${a.is_completed ? `<span class="completed-check" title="학습 완료">✓</span>` : `<span style="font-size: 0.8rem; color: #3b82f6; font-weight: 700;">학습하기 →</span>`}
        </div>
      </div>
    `).join('');
  },

  async openArticle(articleId) {
    app.playAudioEffect('click');
    try {
      const resp = await fetch(`/api/articles/${articleId}`);
      const data = await resp.json();
      this.currentArticle = data;

      document.getElementById('reader-title-ko').innerText = data.title_ko;
      document.getElementById('reader-title-en').innerText = data.title_en;
      document.getElementById('reader-level').innerText = data.level;
      document.getElementById('reader-time').innerText = `⏱️ ${data.read_time} 소요`;
      document.getElementById('reader-author').innerText = `✍️ ${data.author}`;

      // Complete button state
      const btnComplete = document.getElementById('btn-complete-article');
      if (data.is_completed) {
        btnComplete.innerText = '✓ 학습 완료됨';
        btnComplete.disabled = true;
        btnComplete.style.opacity = '0.6';
      } else {
        btnComplete.innerText = '✓ 완독 완료 (+50 XP)';
        btnComplete.disabled = false;
        btnComplete.style.opacity = '1';
      }

      // Render 3-Point Summary Cards
      const tldrGrid = document.getElementById('reader-tldr-grid');
      tldrGrid.innerHTML = data.summary_cards.map(c => `
        <div class="tldr-card">
          <div class="tldr-badge">${c.badge}</div>
          <div class="tldr-title">${c.title}</div>
          <div class="tldr-text">${c.text}</div>
        </div>
      `).join('');

      // Render Body HTML
      const bodyEl = document.getElementById('reader-body');
      bodyEl.innerHTML = data.content_html;

      // Extract TOC from H2
      this.generateTOC(bodyEl);

      // Attach Term Popovers
      this.attachTermListeners(bodyEl);

      // Render Embedded Quiz if available
      this.renderEmbeddedQuiz(data.related_quizzes);

      // Switch view
      app.navigate('reader');
    } catch (err) {
      console.error('Failed to load article:', err);
    }
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
        <p style="font-size: 0.95rem; margin-bottom: 1rem; color: #cbd5e1;">${q.situation}</p>
        <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 1rem; color: #ffffff;">${q.question}</div>
        
        <div class="quiz-options-grid" id="embedded-quiz-options">
          ${q.options.map((opt, i) => `
            <button class="quiz-opt-btn" onclick="reader.handleEmbeddedAnswer('${q.id}', ${i})">
              <span>${opt.label}</span>
            </button>
          `).join('')}
        </div>
        <div id="embedded-quiz-feedback" style="display: none; margin-top: 1rem; padding: 1rem; background: #0f172a; border-radius: 8px;"></div>
      </div>
    `;
  },

  async handleEmbeddedAnswer(quizId, selectedIdx) {
    try {
      const resp = await fetch('/api/quizzes/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quiz_id: quizId, selected_option_index: selectedIdx })
      });
      const res = await resp.json();
      
      const buttons = document.querySelectorAll('#embedded-quiz-options .quiz-opt-btn');
      buttons.forEach((b, i) => {
        b.disabled = true;
        if (i === selectedIdx) {
          b.classList.add(res.is_correct ? 'correct' : 'wrong');
        }
      });

      const feedbackEl = document.getElementById('embedded-quiz-feedback');
      feedbackEl.style.display = 'block';
      feedbackEl.innerHTML = `
        <div style="font-weight: 800; color: ${res.is_correct ? '#34d399' : '#f87171'}; margin-bottom: 0.5rem;">
          ${res.is_correct ? '🎉 정답입니다!' : '❌ 오답입니다.'} (+${res.xp_gained} XP)
        </div>
        <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">${res.explanation}</div>
      `;

      app.addXP(res.xp_gained);
      app.playAudioEffect(res.is_correct ? 'correct' : 'wrong');
    } catch (e) {
      console.error(e);
    }
  },

  async markCompleted() {
    if (!this.currentArticle) return;
    try {
      const resp = await fetch(`/api/articles/${this.currentArticle.id}/complete`, { method: 'POST' });
      const data = await resp.json();
      app.addXP(50);
      
      const btn = document.getElementById('btn-complete-article');
      btn.innerText = '✓ 학습 완료됨 (+50 XP 획득!)';
      btn.disabled = true;
      btn.style.opacity = '0.7';

      this.loadArticles(); // refresh list badge
    } catch (e) {
      console.error(e);
    }
  }
};

/**
 * Interactive Term Popover Controller
 */
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

  async show(termKey, event) {
    if (!this.el) this.init();
    try {
      const resp = await fetch(`/api/glossary/${termKey}`);
      if (!resp.ok) return;
      const data = await resp.json();

      document.getElementById('pop-category').innerText = data.category;
      document.getElementById('pop-title').innerText = `${data.term} (${data.korean_term})`;
      document.getElementById('pop-desc').innerText = data.short_desc;
      document.getElementById('pop-analogy').innerText = `💡 ${data.analogy}`;
      document.getElementById('pop-tip').innerText = `⚡ ${data.pro_tip}`;

      // Calculate position
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
    } catch (e) {
      console.error(e);
    }
  },

  hide() {
    if (this.el) {
      this.el.style.display = 'none';
    }
  }
};
