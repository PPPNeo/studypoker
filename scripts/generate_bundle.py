import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'articles.json'), encoding='utf-8') as f:
    articles = json.load(f)
with open(os.path.join(BASE_DIR, 'data', 'glossary.json'), encoding='utf-8') as f:
    glossary = json.load(f)
with open(os.path.join(BASE_DIR, 'data', 'quizzes.json'), encoding='utf-8') as f:
    quizzes = json.load(f)
with open(os.path.join(BASE_DIR, 'data', 'ranges.json'), encoding='utf-8') as f:
    ranges = json.load(f)
with open(os.path.join(BASE_DIR, 'data', 'roadmap.json'), encoding='utf-8') as f:
    roadmap = json.load(f)

with open(os.path.join(BASE_DIR, 'static', 'css', 'style.css'), encoding='utf-8') as f:
    css_content = f.read()

# Read the HTML template from static/index.html
with open(os.path.join(BASE_DIR, 'static', 'index.html'), encoding='utf-8') as f:
    html_content = f.read()

# Replace stylesheet link with inline CSS for total self-containment
html_content = html_content.replace(
    '<link rel="stylesheet" href="/static/css/style.css" />',
    f'<style>\n{css_content}\n</style>'
)

# Inline client-side database and complete standalone JS
js_bundle = f"""
<script>
const DB = {{
  articles: {json.dumps(articles, ensure_ascii=False)},
  glossary: {json.dumps(glossary, ensure_ascii=False)},
  quizzes: {json.dumps(quizzes, ensure_ascii=False)},
  ranges: {json.dumps(ranges, ensure_ascii=False)},
  roadmap: {json.dumps(roadmap, ensure_ascii=False)}
}};

// User Session state with localStorage persistence
const storage = {{
  get() {{
    const saved = localStorage.getItem('studypoker_user');
    if (saved) {{
      try {{ return JSON.parse(saved); }} catch(e) {{}}
    }}
    return {{
      xp: 120,
      level: 1,
      streak: 3,
      completed_articles: ['what-is-expected-value-in-poker'],
      completed_quizzes: []
    }};
  }},
  save(state) {{
    localStorage.setItem('studypoker_user', JSON.stringify(state));
  }}
}};

const app = {{
  userState: storage.get(),
  currentView: 'articles',

  init() {{
    this.updateUserBar();
    reader.loadArticles();
    matrix.init();
    roadmap.load();
    glossary.load();

    const hash = window.location.hash.replace('#', '');
    if (hash && ['articles', 'trainer', 'matrix', 'roadmap', 'glossary'].includes(hash)) {{
      this.navigate(hash);
    }}
  }},

  navigate(viewId) {{
    this.currentView = viewId;
    window.location.hash = viewId;

    document.querySelectorAll('.view-section').forEach(sec => {{
      sec.classList.remove('active');
    }});

    const targetSection = document.getElementById(`view-${{viewId}}`);
    if (targetSection) {{
      targetSection.classList.add('active');
    }}

    document.querySelectorAll('.nav-btn').forEach(btn => {{
      if (btn.dataset.target === viewId) {{
        btn.classList.add('active');
      }} else {{
        btn.classList.remove('active');
      }}
    }});

    if (viewId === 'trainer') {{
      trainer.init();
    }} else if (viewId === 'roadmap') {{
      roadmap.load();
    }} else if (viewId === 'glossary') {{
      glossary.load();
    }}

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }},

  updateUserBar() {{
    const xp = this.userState.xp;
    let levelTitle = "Lv.1 피쉬 탈출";
    let nextThreshold = 200;
    let prevThreshold = 0;

    if (xp >= 800) {{
      levelTitle = "Lv.4 GTO 마스터 👑";
      prevThreshold = 800;
      nextThreshold = 1500;
    }} else if (xp >= 500) {{
      levelTitle = "Lv.3 온라인 그라인더 🔥";
      prevThreshold = 500;
      nextThreshold = 800;
    }} else if (xp >= 200) {{
      levelTitle = "Lv.2 펍 레귤러 ⚔️";
      prevThreshold = 200;
      nextThreshold = 500;
    }}

    const currentLevelXp = xp - prevThreshold;
    const requiredLevelXp = nextThreshold - prevThreshold;
    const pct = Math.min(100, Math.round((currentLevelXp / requiredLevelXp) * 100));

    document.getElementById('user-level-badge').innerText = levelTitle;
    document.getElementById('user-xp-text').innerText = `${{xp}} / ${{nextThreshold}} XP`;
    document.getElementById('user-xp-bar').style.width = `${{pct}}%`;
    document.getElementById('user-streak').innerText = this.userState.streak;
    storage.save(this.userState);
  }},

  addXP(amount) {{
    this.userState.xp += amount;
    this.updateUserBar();
    this.playAudioEffect('xp');
  }},

  playAudioEffect(type) {{
    try {{
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();

      if (type === 'click') {{
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
      }} else if (type === 'correct') {{
        const now = ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {{
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
        }});
      }} else if (type === 'wrong') {{
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
      }} else if (type === 'xp') {{
        const now = ctx.currentTime;
        [659.25, 880, 1174.66].forEach((freq, i) => {{
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
        }});
      }}
    }} catch (e) {{}}
  }}
}};

const reader = {{
  articles: DB.articles,
  currentArticle: null,
  activeCategory: 'all',

  loadArticles() {{
    this.renderArticleCards();
  }},

  filterCategory(cat) {{
    this.activeCategory = cat;
    document.querySelectorAll('#article-category-filters .filter-pill').forEach(pill => {{
      if (pill.innerText.includes(cat) || (cat === 'all' && pill.innerText.includes('전체'))) {{
        pill.classList.add('active');
      }} else {{
        pill.classList.remove('active');
      }}
    }});
    this.renderArticleCards();
  }},

  renderArticleCards() {{
    const container = document.getElementById('articles-grid-container');
    const filtered = this.articles.filter(a => {{
      if (this.activeCategory === 'all') return true;
      return a.category === this.activeCategory;
    }});

    document.getElementById('article-count-label').innerText = `총 ${{filtered.length}}편의 프리미엄 가이드`;

    container.innerHTML = filtered.map(a => {{
      const isCompleted = app.userState.completed_articles.includes(a.id);
      return `
        <div class="article-card" onclick="reader.openArticle('${{a.id}}')">
          <div>
            <div class="article-card-header">
              <span class="badge-level">${{a.level}}</span>
              <span class="read-time">⏱️ ${{a.read_time}}</span>
            </div>
            <h3>${{a.title_ko}}</h3>
            <p class="subtitle-en">${{a.title_en}}</p>
          </div>
          
          <div class="article-card-footer">
            <div class="author-info">✍️ ${{a.author}}</div>
            ${{isCompleted ? `<span class="completed-check" title="학습 완료">✓</span>` : `<span style="font-size: 0.8rem; color: #3b82f6; font-weight: 700;">학습하기 →</span>`}}
          </div>
        </div>
      `;
    }}).join('');
  }},

  openArticle(articleId) {{
    app.playAudioEffect('click');
    const data = this.articles.find(a => a.id === articleId || a.slug === articleId);
    if (!data) return;
    this.currentArticle = data;

    document.getElementById('reader-title-ko').innerText = data.title_ko;
    document.getElementById('reader-title-en').innerText = data.title_en;
    document.getElementById('reader-level').innerText = data.level;
    document.getElementById('reader-time').innerText = `⏱️ ${{data.read_time}} 소요`;
    document.getElementById('reader-author').innerText = `✍️ ${{data.author}}`;

    const isCompleted = app.userState.completed_articles.includes(data.id);
    const btnComplete = document.getElementById('btn-complete-article');
    if (isCompleted) {{
      btnComplete.innerText = '✓ 학습 완료됨';
      btnComplete.disabled = true;
      btnComplete.style.opacity = '0.6';
    }} else {{
      btnComplete.innerText = '✓ 완독 완료 (+50 XP)';
      btnComplete.disabled = false;
      btnComplete.style.opacity = '1';
    }}

    const tldrGrid = document.getElementById('reader-tldr-grid');
    tldrGrid.innerHTML = data.summary_cards.map(c => `
      <div class="tldr-card">
        <div class="tldr-badge">${{c.badge}}</div>
        <div class="tldr-title">${{c.title}}</div>
        <div class="tldr-text">${{c.text}}</div>
      </div>
    `).join('');

    const bodyEl = document.getElementById('reader-body');
    bodyEl.innerHTML = data.content_html;

    this.generateTOC(bodyEl);
    this.attachTermListeners(bodyEl);

    const relatedQuizzes = DB.quizzes.filter(q => q.article_id === data.id);
    this.renderEmbeddedQuiz(relatedQuizzes);

    app.navigate('reader');
  }},

  generateTOC(bodyEl) {{
    const tocList = document.getElementById('reader-toc-list');
    const headings = bodyEl.querySelectorAll('h2');
    if (!headings.length) {{
      tocList.innerHTML = `<li style="color: var(--text-dim); font-size: 0.85rem;">소제목이 없습니다.</li>`;
      return;
    }}

    tocList.innerHTML = Array.from(headings).map((h, i) => {{
      const id = `heading-${{i}}`;
      h.id = id;
      return `<li><a href="#${{id}}" onclick="event.preventDefault(); document.getElementById('${{id}}').scrollIntoView({{behavior: 'smooth'}})">${{h.innerText}}</a></li>`;
    }}).join('');
  }},

  attachTermListeners(container) {{
    const termTags = container.querySelectorAll('.gto-term');
    termTags.forEach(tag => {{
      const termKey = tag.dataset.term;
      tag.addEventListener('mouseenter', (e) => {{
        termPopover.show(termKey, e);
      }});
      tag.addEventListener('click', (e) => {{
        e.stopPropagation();
        termPopover.show(termKey, e);
      }});
    }});
  }},

  renderEmbeddedQuiz(relatedQuizzes) {{
    const quizContainer = document.getElementById('reader-quiz-container');
    if (!relatedQuizzes || !relatedQuizzes.length) {{
      quizContainer.style.display = 'none';
      return;
    }}

    const q = relatedQuizzes[0];
    quizContainer.style.display = 'block';
    quizContainer.innerHTML = `
      <div style="background: var(--bg-surface); border: 1px solid #3b82f6; border-radius: 12px; padding: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
          <span style="font-size: 1.3rem;">🎯</span>
          <h3 style="font-size: 1.15rem; font-weight: 800; color: #93c5fd;">아티클 체크업 퀴즈</h3>
        </div>
        <p style="font-size: 0.95rem; margin-bottom: 1rem; color: #cbd5e1;">${{q.situation}}</p>
        <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 1rem; color: #ffffff;">${{q.question}}</div>
        
        <div class="quiz-options-grid" id="embedded-quiz-options">
          ${{q.options.map((opt, i) => `
            <button class="quiz-opt-btn" onclick="reader.handleEmbeddedAnswer('${{q.id}}', ${{i}})">
              <span>${{opt.label}}</span>
            </button>
          `).join('')}}
        </div>
        <div id="embedded-quiz-feedback" style="display: none; margin-top: 1rem; padding: 1rem; background: #0f172a; border-radius: 8px;"></div>
      </div>
    `;
  }},

  handleEmbeddedAnswer(quizId, selectedIdx) {{
    const q = DB.quizzes.find(item => item.id === quizId);
    if (!q) return;

    const isCorrect = (selectedIdx === q.correct_index);
    const xpGained = isCorrect ? 50 : 10;

    const buttons = document.querySelectorAll('#embedded-quiz-options .quiz-opt-btn');
    buttons.forEach((b, i) => {{
      b.disabled = true;
      if (i === selectedIdx) {{
        b.classList.add(isCorrect ? 'correct' : 'wrong');
      }} else if (i === q.correct_index) {{
        b.classList.add('correct');
      }}
    }});

    const feedbackEl = document.getElementById('embedded-quiz-feedback');
    feedbackEl.style.display = 'block';
    feedbackEl.innerHTML = `
      <div style="font-weight: 800; color: ${{isCorrect ? '#34d399' : '#f87171'}}; margin-bottom: 0.5rem;">
        ${{isCorrect ? '🎉 정답입니다!' : '❌ 오답입니다.'}} (+${{xpGained}} XP)
      </div>
      <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">${{q.explanation}}</div>
    `;

    app.addXP(xpGained);
    app.playAudioEffect(isCorrect ? 'correct' : 'wrong');
  }},

  markCompleted() {{
    if (!this.currentArticle) return;
    if (!app.userState.completed_articles.includes(this.currentArticle.id)) {{
      app.userState.completed_articles.push(this.currentArticle.id);
      app.addXP(50);
    }}
    
    const btn = document.getElementById('btn-complete-article');
    btn.innerText = '✓ 학습 완료됨 (+50 XP 획득!)';
    btn.disabled = true;
    btn.style.opacity = '0.7';

    this.renderArticleCards();
  }}
}};

const termPopover = {{
  el: null,

  init() {{
    this.el = document.getElementById('term-popover');
    document.addEventListener('click', (e) => {{
      if (this.el && !this.el.contains(e.target) && !e.target.classList.contains('gto-term')) {{
        this.hide();
      }}
    }});
  }},

  show(termKey, event) {{
    if (!this.el) this.init();
    const data = DB.glossary[termKey.toLowerCase().trim()];
    if (!data) return;

    document.getElementById('pop-category').innerText = data.category;
    document.getElementById('pop-title').innerText = `${{data.term}} (${{data.korean_term}})`;
    document.getElementById('pop-desc').innerText = data.short_desc;
    document.getElementById('pop-analogy').innerText = `💡 ${{data.analogy}}`;
    document.getElementById('pop-tip').innerText = `⚡ ${{data.pro_tip}}`;

    const rect = event.target.getBoundingClientRect();
    const popoverWidth = 340;
    let left = rect.left;
    if (left + popoverWidth > window.innerWidth - 20) {{
      left = window.innerWidth - popoverWidth - 20;
    }}
    let top = rect.bottom + 8;
    if (top + 260 > window.innerHeight) {{
      top = rect.top - 270;
    }}

    this.el.style.left = `${{Math.max(10, left)}}px`;
    this.el.style.top = `${{Math.max(10, top)}}px`;
    this.el.style.display = 'block';
  }},

  hide() {{
    if (this.el) {{
      this.el.style.display = 'none';
    }}
  }}
}};

const trainer = {{
  quizzes: DB.quizzes,
  currentIndex: 0,
  isAnswered: false,

  init() {{
    this.renderCurrentQuiz();
  }},

  renderCurrentQuiz() {{
    if (!this.quizzes.length) return;
    const q = this.quizzes[this.currentIndex];
    this.isAnswered = false;

    document.getElementById('quiz-counter').innerText = `${{this.currentIndex + 1}} / ${{this.quizzes.length}}`;
    document.getElementById('trainer-pot-display').innerText = q.pot;

    const boardEl = document.getElementById('trainer-board-cards');
    if (!q.board || q.board.length === 0) {{
      boardEl.innerHTML = `<div style="color: #64748b; font-size: 0.9rem; font-style: italic;">[Preflop - 보드 카드 없음]</div>`;
    }} else {{
      boardEl.innerHTML = q.board.map(c => this.createCardHtml(c)).join('');
    }}

    const heroEl = document.getElementById('trainer-hero-cards');
    heroEl.innerHTML = q.hero_hand.map(c => this.createCardHtml(c)).join('');

    document.getElementById('trainer-hero-label').innerText = 
      `HERO (${{q.hero_position}}) • Effective Stack: ${{q.effective_stack}}`;

    document.getElementById('trainer-situation-desc').innerText = q.situation;
    document.getElementById('trainer-question-text').innerText = q.question;

    const feedbackBox = document.getElementById('trainer-feedback-box');
    feedbackBox.style.display = 'none';

    const optGrid = document.getElementById('trainer-options-grid');
    optGrid.innerHTML = q.options.map((opt, i) => `
      <button class="quiz-opt-btn" id="quiz-btn-${{i}}" onclick="trainer.selectOption(${{i}})">
        <span>${{opt.label}}</span>
        <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500;">선택</span>
      </button>
    `).join('');
  }},

  createCardHtml(cardStr) {{
    if (!cardStr) return '';
    const rank = cardStr.slice(0, -1);
    const suit = cardStr.slice(-1);
    
    let suitClass = 'card-suit-spade';
    if (suit === '♥' || suit === '♦') {{
      suitClass = (suit === '♥') ? 'card-suit-heart' : 'card-suit-diamond';
    }} else if (suit === '♣') {{
      suitClass = 'card-suit-club';
    }}

    return `
      <div class="poker-card ${{suitClass}}">
        <div class="card-top">
          <span class="card-rank">${{rank}}</span>
          <span style="font-size: 0.8rem;">${{suit}}</span>
        </div>
        <div class="card-center-suit">${{suit}}</div>
        <div class="card-bottom">
          <span class="card-rank">${{rank}}</span>
          <span style="font-size: 0.8rem;">${{suit}}</span>
        </div>
      </div>
    `;
  }},

  selectOption(optIndex) {{
    if (this.isAnswered) return;
    this.isAnswered = true;
    const q = this.quizzes[this.currentIndex];

    const isCorrect = (optIndex === q.correct_index);
    const xpGained = isCorrect ? 50 : 10;

    q.options.forEach((opt, i) => {{
      const btn = document.getElementById(`quiz-btn-${{i}}`);
      btn.disabled = true;
      btn.innerHTML = `
        <span>${{opt.label}}</span>
        <span style="font-size: 0.85rem; font-weight: 800; color: ${{opt.is_correct ? '#34d399' : '#94a3b8'}};">
          GTO: ${{opt.gto_freq}} (EV: ${{opt.ev}})
        </span>
      `;
      if (i === optIndex) {{
        btn.classList.add(isCorrect ? 'correct' : 'wrong');
      }} else if (opt.is_correct) {{
        btn.classList.add('correct');
      }}
    }});

    const feedbackBox = document.getElementById('trainer-feedback-box');
    const statusTitle = document.getElementById('feedback-status-title');
    const conceptTag = document.getElementById('feedback-concept-tag');
    const explanationText = document.getElementById('feedback-explanation-text');

    statusTitle.className = `feedback-status ${{isCorrect ? 'correct' : 'wrong'}}`;
    statusTitle.innerText = isCorrect ? `✅ 정답입니다! (+${{xpGained}} XP)` : `❌ 아쉽네요! (+${{xpGained}} XP)`;
    conceptTag.innerText = `핵심 원리: ${{q.key_concept}}`;
    explanationText.innerText = q.explanation;
    feedbackBox.style.display = 'block';

    app.addXP(xpGained);
    app.playAudioEffect(isCorrect ? 'correct' : 'wrong');
  }},

  nextQuiz() {{
    app.playAudioEffect('click');
    if (this.currentIndex < this.quizzes.length - 1) {{
      this.currentIndex++;
      this.renderCurrentQuiz();
    }}
  }},

  prevQuiz() {{
    app.playAudioEffect('click');
    if (this.currentIndex > 0) {{
      this.currentIndex--;
      this.renderCurrentQuiz();
    }}
  }}
}};

const matrix = {{
  ranks: ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'],
  rangesData: DB.ranges,
  currentPreset: null,

  init() {{
    this.loadPreset('btn_open');
  }},

  loadPreset(presetId) {{
    const preset = this.rangesData.presets.find(p => p.id === presetId);
    if (!preset) return;

    this.currentPreset = preset;
    document.getElementById('matrix-preset-desc').innerText = preset.description;

    const legendEl = document.getElementById('matrix-legend-container');
    legendEl.innerHTML = preset.legend.map(l => `
      <div class="legend-item">
        <div class="legend-color-box" style="background: ${{l.color}};"></div>
        <span style="font-weight: 600;">${{l.label}}</span>
      </div>
    `).join('');

    this.renderGrid();
  }},

  renderGrid() {{
    const gridEl = document.getElementById('poker-matrix-grid');
    gridEl.innerHTML = '';

    for (let r = 0; r < 13; r++) {{
      for (let c = 0; c < 13; c++) {{
        let handName = '';
        let combos = 0;
        let handType = '';

        if (r === c) {{
          handName = this.ranks[r] + this.ranks[c];
          combos = 6;
          handType = '포켓 페어 (6 combos)';
        }} else if (r < c) {{
          handName = this.ranks[r] + this.ranks[c] + 's';
          combos = 4;
          handType = '수티드 (4 combos)';
        }} else {{
          handName = this.ranks[c] + this.ranks[r] + 'o';
          combos = 12;
          handType = '오프수트 (12 combos)';
        }}

        const actionData = this.currentPreset.actions[handName];
        let actionClass = 'action-fold';

        if (actionData) {{
          const actionName = actionData.action.toLowerCase();
          if (actionName.includes('raise')) {{
            actionClass = 'action-raise';
          }} else if (actionName.includes('3-bet')) {{
            actionClass = 'action-3bet';
          }} else if (actionName.includes('call')) {{
            actionClass = 'action-call';
          }}
        }}

        const cell = document.createElement('div');
        cell.className = `matrix-cell ${{actionClass}}`;
        cell.innerText = handName;

        cell.addEventListener('mouseenter', () => {{
          this.inspectHand(handName, handType, actionData);
        }});

        gridEl.appendChild(cell);
      }}
    }}
  }},

  inspectHand(handName, handType, actionData) {{
    document.getElementById('inspect-hand-name').innerText = handName;
    document.getElementById('inspect-combos').innerText = handType;

    const actionDescEl = document.getElementById('inspect-action-desc');
    if (!actionData) {{
      actionDescEl.innerHTML = `<span style="color: #64748b;">Fold (100%)</span>`;
    }} else {{
      let color = '#ef4444';
      if (actionData.action.toLowerCase().includes('call')) color = '#10b981';
      else if (actionData.action.toLowerCase().includes('3-bet')) color = '#f59e0b';

      actionDescEl.innerHTML = `
        <span style="color: ${{color}};">
          ${{actionData.action}} (${{actionData.freq}}%)
        </span>
      `;
    }}
  }}
}};

const roadmap = {{
  data: DB.roadmap,

  load() {{
    const rm = this.data;
    const userState = app.userState;

    const levelsContainer = document.getElementById('roadmap-levels-container');
    levelsContainer.innerHTML = rm.levels.map(lvl => {{
      const isLocked = (userState.xp < lvl.required_xp);
      return `
        <div class="roadmap-level-card ${{isLocked ? 'locked' : ''}}">
          <div class="level-badge-header">
            <div>
              <h3 style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">${{lvl.title}}</h3>
              <p style="font-size: 0.85rem; color: var(--text-dim);">${{lvl.subtitle}}</p>
            </div>
            <span class="level-badge">${{lvl.badge}}</span>
          </div>

          <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1rem;">
            ${{lvl.description}}
          </p>

          ${{isLocked ? `
            <div style="background: rgba(0,0,0,0.4); padding: 0.75rem; border-radius: 8px; font-size: 0.85rem; color: #f59e0b; font-weight: 700;">
              🔒 해금 조건: ${{lvl.required_xp}} XP 달성 필요 (현재: ${{userState.xp}} XP)
            </div>
          ` : `
            <div class="nodes-list">
              ${{lvl.nodes.map(n => {{
                const isCompleted = userState.completed_articles.includes(n.article_id);
                return `
                  <div class="node-item ${{isCompleted ? 'completed' : ''}}" onclick="reader.openArticle('${{n.article_id}}')">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                      <span style="font-size: 1.2rem;">${{isCompleted ? '✅' : '📖'}}</span>
                      <div>
                        <div style="font-weight: 700; font-size: 0.95rem; color: #ffffff;">${{n.title}}</div>
                        <span style="font-size: 0.75rem; color: #94a3b8;">${{n.category}}</span>
                      </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                      <span style="font-size: 0.8rem; color: #fbbf24; font-weight: 700;">+${{n.xp}} XP</span>
                      <button class="btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">
                        ${{isCompleted ? '다시 읽기' : '학습 시작'}}
                      </button>
                    </div>
                  </div>
                `;
              }}).join('')}}
            </div>
          `}}
        </div>
      `;
    }}).join('');

    const achContainer = document.getElementById('roadmap-achievements-container');
    achContainer.innerHTML = rm.achievements.map(a => `
      <div class="feature-item" style="opacity: ${{a.unlocked ? '1' : '0.45'}};">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">${{a.icon}}</div>
        <h4 style="font-size: 1.05rem; margin-bottom: 0.25rem;">${{a.title}}</h4>
        <p style="font-size: 0.85rem; color: var(--text-muted);">${{a.desc}}</p>
        <div style="margin-top: 0.75rem; font-size: 0.75rem; font-weight: 700; color: ${{a.unlocked ? '#34d399' : '#64748b'}};">
          ${{a.unlocked ? '🏆 달성 완료' : '미달성'}}
        </div>
      </div>
    `).join('');
  }}
}};

const glossary = {{
  terms: DB.glossary,

  load() {{
    this.filterTerms('');
  }},

  filterTerms(query) {{
    const q = query.toLowerCase().trim();
    const container = document.getElementById('glossary-grid-container');

    const filtered = Object.entries(this.terms).filter(([k, item]) => {{
      if (!q) return true;
      const pool = `${{k}} ${{item.term}} ${{item.korean_term}} ${{item.short_desc}} ${{item.analogy}}`.toLowerCase();
      return pool.includes(q);
    }});

    if (!filtered.length) {{
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-dim); padding: 3rem;">검색 결과가 없습니다.</div>`;
      return;
    }}

    container.innerHTML = filtered.map(([k, item]) => `
      <div class="article-card" style="cursor: default;">
        <div>
          <div class="article-card-header">
            <span class="badge-level">${{item.category}}</span>
          </div>
          <h3 style="color: #60a5fa;">${{item.term}}</h3>
          <p class="subtitle-en" style="font-weight: 700; color: #ffffff; margin-bottom: 0.75rem;">${{item.korean_term}}</p>
          <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 1rem; line-height: 1.5;">${{item.short_desc}}</p>
          
          <div style="background: rgba(0,0,0,0.3); border-left: 3px solid #f59e0b; padding: 0.65rem 0.85rem; font-size: 0.85rem; color: #e2e8f0; border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
            💡 <strong>비유:</strong> ${{item.analogy}}
          </div>
        </div>

        <div style="padding-top: 0.75rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: #34d399;">
          ⚡ <strong>Pro Tip:</strong> ${{item.pro_tip}}
        </div>
      </div>
    `).join('');
  }}
}};

const aiCoach = {{
  overlay: null,
  messagesArea: null,
  inputEl: null,

  init() {{
    this.overlay = document.getElementById('ai-modal-overlay');
    this.messagesArea = document.getElementById('ai-messages-area');
    this.inputEl = document.getElementById('ai-user-input');
  }},

  open() {{
    if (!this.overlay) this.init();
    this.overlay.style.display = 'flex';
    this.inputEl.focus();
    app.playAudioEffect('click');
  }},

  close() {{
    if (!this.overlay) this.init();
    this.overlay.style.display = 'none';
  }},

  sendPreset(text) {{
    if (!this.inputEl) this.init();
    this.inputEl.value = text;
    this.sendMessage();
  }},

  sendMessage() {{
    if (!this.inputEl) this.init();
    const text = this.inputEl.value.trim();
    if (!text) return;

    this.inputEl.value = '';
    this.appendMessage('user', text);
    this.scrollToBottom();

    const loadingId = 'loading-' + Date.now();
    this.appendMessage('coach', '코치가 포커 솔버 데이터를 분석 중입니다... 🧠', loadingId);
    this.scrollToBottom();

    setTimeout(() => {{
      const answer = this.generateAnswer(text);
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {{
        loadingEl.innerHTML = answer.replace(/\\n/g, '<br>');
      }}
      this.scrollToBottom();
      app.playAudioEffect('click');
    }}, 400);
  }},

  generateAnswer(q) {{
    const qLower = q.toLowerCase();
    if (qLower.includes('a72') || qLower.includes('a-7-2') || qLower.includes('작은 벳') || qLower.includes('1/3') || qLower.includes('c-bet') || qLower.includes('c벳')) {{
      return `**[코치 Ivan의 GTO 해설]**\\n\\nA-7-2r이나 K-8-3r 같은 **드라이한 A/K-high 보드**에서 1/3팟의 작은 C-bet을 전체 레인지(80~100%)로 구사하는 이유는 명확합니다:\\n\\n1. **압도적인 레인지 우위 (Range Advantage)**: 프리플랍 레이저(IP)는 AA, AK, AQ을 모두 쥐고 있는 반면, BB는 보통 AA, AK을 3벳으로 뺐기 때문에 레인지가 캡(Capped)되어 있습니다.\\n2. **낮은 에퀴티 저항선**: A가 깔린 보드에서는 상대방의 99, 88 같은 포켓페어나 언더카드가 턴에서 역전할 확률이 5장 이하(약 10~15%)로 매우 낮습니다.\\n3. **효율적 칩 보존**: 굳이 팟을 크게 키우지 않아도 상대의 에어(Air) 핸드와 약한 콤보들을 1/3 팟만으로 즉시 폴드시킬 수 있기 때문입니다!`;
    }} else if (qLower.includes('블로커') || qLower.includes('언블로커') || qLower.includes('blocker')) {{
      return `**[코치 Tombos의 GTO 해설]**\\n\\n블로커는 콤보 수학의 마법입니다. 핵심 원칙을 요약해 드릴게요:\\n\\n1. **리버 블러프를 칠 때**: 상대의 **'콜할 최강 핸드'**를 블락해야 합니다! (예: 상대의 스트레이트 완성 카드인 T이나 너트 플러시 카드인 A♠를 내가 쥐고 있어야 상대가 콜을 못 합니다.)\\n2. **언블로커의 중요성**: 반대로 상대가 미스해서 폴드해야 할 카드(Busted Draw)는 내가 **쥐고 있지 않아야(Unblock)** 합니다. 내가 그 카드를 들고 있으면 상대가 폴드할 꽝 핸드가 사라지기 때문입니다.\\n3. **블러프 캐칭(콜)할 때**: 상대의 블러프 카드를 블락하지 말고, 순수하게 언블락 상태여야 상대가 블러프를 시도했을 확률이 높아집니다.`;
    }} else if (qLower.includes('mdf') || qLower.includes('최소 방어')) {{
      return `**[GTO Wizard 이론팀 해설]**\\n\\n**MDF (Minimum Defense Frequency)**는 상대가 아무 카드로나 블러프를 쳐서 '자동 수익(공짜 돈)'을 내지 못하도록 방어해야 하는 이론적 하한선입니다.\\n\\n- 공식: MDF = 팟 사이즈 / (팟 사이즈 + 베팅 금액)\\n- 예시: 100칩 팟에 상대가 50칩(하프팟)을 베팅하면 100 / (100 + 50) = 66.7%를 최소한 콜 또는 레이스로 방어해야 합니다.\\n- ⚠️ **주의사항**: 보드에 상대의 너트 우위가 극심할 때는 MDF를 문자 그대로 지키려다 스택이 털릴 수 있습니다. 실전 솔버는 텍스처에 따라 오버폴드(Overfold)를 자주 지시합니다.`;
    }} else if (qLower.includes('icm') || qLower.includes('토너먼트')) {{
      return `**[토너먼트 스페셜리스트 조언]**\\n\\n토너먼트 파이널 테이블이나 버블에서는 **ChipEV(칩 기대값)**로 생각하면 패망합니다. 반드시 **$EV(실제 상금 가치)**로 접근해야 합니다:\\n\\n- **칩의 비대칭성**: 칩을 딸 때 얻는 가치보다 칩을 잃을 때 날아가는 상금 가치가 훨씬 큽니다.\\n- **리스크 프리미엄**: 칩리더를 상대로는 AKs나 QQ 같은 프리미엄 핸드조차 뒤의 숏스택 탈락을 기다리기 위해 눈물을 머금고 폴드해야 하는 순간이 있습니다.`;
    }} else {{
      return `**[AI 포커 코치 조언]**\\n\\n질문해 주신 '${{q}}'에 대한 GTO 전략 관점의 조언입니다:\\n\\n포커 의사결정의 핵심은 언제나 **[레인지 vs 레인지의 상호작용]**입니다. 단 한 장의 내 카드가 아닌, 상대의 전체 레인지와 내 전체 레인지가 현재 보드 텍스처에서 어떤 에퀴티 분포를 가지는지를 먼저 파악하세요.\\n\\n- 내가 **너트 우위**를 가지면? 👉 큰 벳(75%+)이나 오버벳으로 압박\\n- 내가 **레인지 우위**만 가지면? 👉 작은 벳(25~33%)으로 넓은 빈도 공격\\n- 상대가 너트 우위를 점하면? 👉 첵백 빈도를 높여 팟 컨트롤`;
    }}
  }},

  appendMessage(role, text, id = null) {{
    const div = document.createElement('div');
    div.className = `ai-msg ${{role}}`;
    if (id) div.id = id;
    div.innerHTML = text.replace(/\\n/g, '<br>');
    this.messagesArea.appendChild(div);
  }},

  scrollToBottom() {{
    this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
  }}
}};

window.addEventListener('DOMContentLoaded', () => {{
  app.init();
}});
</script>
"""

# Remove the separate external script tags at the bottom
script_tags = """  <script src="/static/js/app.js"></script>
  <script src="/static/js/reader.js"></script>
  <script src="/static/js/trainer.js"></script>
  <script src="/static/js/matrix.js"></script>
  <script src="/static/js/roadmap.js"></script>
  <script src="/static/js/glossary.js"></script>
  <script src="/static/js/ai_coach.js"></script>"""

html_content = html_content.replace(script_tags, js_bundle)

# Save as root index.html
output_path = os.path.join(BASE_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated standalone root index.html! Length: {len(html_content)} bytes")
