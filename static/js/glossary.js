/**
 * GTO Poker Glossary Controller
 * Searchable dictionary with easy analogies and formulas.
 */

const glossary = {
  terms: {},

  async load() {
    try {
      const resp = await fetch('/api/glossary');
      this.terms = await resp.json();
      this.render();
    } catch (e) {
      console.error('Failed to load glossary:', e);
    }
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
          <p class="subtitle-en" style="font-weight: 700; color: #ffffff; margin-bottom: 0.75rem;">${item.korean_term}</p>
          <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 1rem; line-height: 1.5;">${item.short_desc}</p>
          
          <div style="background: rgba(0,0,0,0.3); border-left: 3px solid #f59e0b; padding: 0.65rem 0.85rem; font-size: 0.85rem; color: #e2e8f0; border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
            💡 <strong>비유:</strong> ${item.analogy}
          </div>
        </div>

        <div style="padding-top: 0.75rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: #34d399;">
          ⚡ <strong>Pro Tip:</strong> ${item.pro_tip}
        </div>
      </div>
    `).join('');
  },

  render() {
    this.filterTerms('');
  }
};
