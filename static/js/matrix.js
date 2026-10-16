/**
 * 13x13 GTO Poker Range Matrix Component
 * Generates the full 169 starting hands grid with hover inspector & preset switcher.
 */

const matrix = {
  ranks: ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'],
  rangesData: null,
  currentPreset: null,

  async init() {
    try {
      const resp = await fetch('/api/ranges');
      this.rangesData = await resp.json();
      this.loadPreset('btn_open');
    } catch (e) {
      console.error('Failed to load ranges:', e);
    }
  },

  loadPreset(presetId) {
    if (!this.rangesData) return;
    const preset = this.rangesData.presets.find(p => p.id === presetId);
    if (!preset) return;

    this.currentPreset = preset;
    document.getElementById('matrix-preset-desc').innerText = preset.description;

    // Render Legend
    const legendEl = document.getElementById('matrix-legend-container');
    legendEl.innerHTML = preset.legend.map(l => `
      <div class="legend-item">
        <div class="legend-color-box" style="background: ${l.color};"></div>
        <span style="font-weight: 600;">${l.label}</span>
      </div>
    `).join('');

    // Render 13x13 Matrix
    this.renderGrid();
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
        let bgStyle = '';

        if (actionData) {
          const actionName = actionData.action.toLowerCase();
          if (actionName.includes('raise')) {
            actionClass = 'action-raise';
          } else if (actionName.includes('3-bet')) {
            actionClass = 'action-3bet';
          } else if (actionName.includes('call')) {
            actionClass = 'action-call';
          }
        }

        const cell = document.createElement('div');
        cell.className = `matrix-cell ${actionClass}`;
        cell.innerText = handName;

        // Hover inspector event
        cell.addEventListener('mouseenter', () => {
          this.inspectHand(handName, handType, actionData);
        });

        gridEl.appendChild(cell);
      }
    }
  },

  inspectHand(handName, handType, actionData) {
    document.getElementById('inspect-hand-name').innerText = handName;
    document.getElementById('inspect-combos').innerText = handType;

    const actionDescEl = document.getElementById('inspect-action-desc');
    if (!actionData) {
      actionDescEl.innerHTML = `<span style="color: #64748b;">Fold (100%)</span>`;
    } else {
      let color = '#ef4444';
      if (actionData.action.toLowerCase().includes('call')) color = '#10b981';
      else if (actionData.action.toLowerCase().includes('3-bet')) color = '#f59e0b';

      actionDescEl.innerHTML = `
        <span style="color: ${color};">
          ${actionData.action} (${actionData.freq}%)
        </span>
      `;
    }
  }
};
