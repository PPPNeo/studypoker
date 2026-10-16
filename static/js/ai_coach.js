/**
 * AI Poker Coach Chat Assistant
 */

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

  async sendMessage() {
    if (!this.inputEl) this.init();
    const text = this.inputEl.value.trim();
    if (!text) return;

    this.inputEl.value = '';

    // Append User Message
    this.appendMessage('user', text);
    this.scrollToBottom();

    // Append Loading indicator
    const loadingId = 'loading-' + Date.now();
    this.appendMessage('coach', '코치가 포커 솔버 데이터를 분석 중입니다... 🧠', loadingId);
    this.scrollToBottom();

    try {
      const resp = await fetch('/api/ai/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text })
      });
      const data = await resp.json();

      // Replace loading message with answer
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.innerHTML = data.answer.replace(/\n/g, '<br>');
      }
      this.scrollToBottom();
      app.playAudioEffect('click');
    } catch (e) {
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.innerText = '답변을 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
      }
    }
  },

  appendMessage(role, text, id = null) {
    const div = document.createElement('div');
    div.className = `ai-msg ${role}`;
    if (id) div.id = id;
    div.innerHTML = text.replace(/\n/g, '<br>');
    this.messagesArea.appendChild(div);
  },

  scrollToBottom() {
    this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
  }
};
