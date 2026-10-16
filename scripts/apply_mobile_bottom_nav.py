# -*- coding: utf-8 -*-
"""
apply_mobile_bottom_nav.py
Solves the mobile navigation overflow issue by:
1. Moving main menu tabs to a native-app-style Mobile Bottom Navigation Bar (Dock)
2. Slimming down the top header on mobile (logo on left, avatar + theme + AI coach on right)
3. Keeping active states synced across desktop and mobile navs
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_head.html')
TAIL_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_tail.js')

MOBILE_CSS = """
/* ==========================================================================
   Mobile Optimization: App-Style Bottom Dock & Header Slimming
   ========================================================================== */

/* Bottom Nav Bar (Hidden by default on Desktop) */
.mobile-bottom-nav {
  display: none;
}

@media (max-width: 860px) {
  /* 1. Top Header Slimming for Mobile */
  header {
    position: sticky;
    top: 0;
    z-index: 990;
  }

  .header-container {
    padding: 0.5rem 0.85rem;
    gap: 0.5rem;
    overflow-x: visible !important;
  }

  /* Hide the 5 nav buttons from top header (they move to the bottom dock) */
  header .main-nav {
    display: none !important;
  }

  /* Compact Brand */
  .brand {
    gap: 0.45rem;
  }
  .brand-icon {
    width: 32px;
    height: 32px;
    font-size: 1.15rem;
  }
  .brand-title {
    font-size: 1.05rem;
  }
  .brand-badge {
    display: none !important;
  }

  /* Compact User Bar */
  .user-bar {
    gap: 0.4rem;
  }
  .user-bar .xp-container {
    display: none !important;
  }
  .user-bar .streak-pill {
    display: none !important;
  }

  .char-header-pill {
    height: 34px;
    padding: 0.15rem 0.5rem 0.15rem 0.25rem;
    gap: 0.35rem;
  }
  .char-avatar-icon {
    width: 24px;
    height: 24px;
    font-size: 1.15rem;
  }
  .char-header-name {
    font-size: 0.78rem;
    max-width: 65px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .char-header-tag {
    display: none !important;
  }

  .theme-toggle-btn {
    height: 34px;
    padding: 0.3rem 0.55rem;
    font-size: 0.78rem;
  }
  #theme-text {
    display: none !important;
  }

  .ai-coach-btn {
    height: 34px;
    padding: 0.3rem 0.65rem;
    font-size: 0.78rem;
    gap: 0.25rem;
  }

  /* 2. Main content bottom padding to prevent bottom dock overlap */
  main {
    margin: 0.75rem auto;
    padding: 0 0.85rem 85px !important;
  }

  /* 3. Native App Style Mobile Bottom Navigation Bar */
  .mobile-bottom-nav {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 58px;
    background: rgba(19, 27, 46, 0.94);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-top: 1px solid var(--border-color);
    z-index: 1000;
    justify-content: space-around;
    align-items: center;
    padding: 0 0.25rem calc(env(safe-area-inset-bottom, 0px));
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.4);
  }

  body.theme-light .mobile-bottom-nav {
    background: rgba(255, 255, 255, 0.95);
    border-top-color: #cbd5e1;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.08);
  }

  .mobile-nav-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 6px 0;
    gap: 3px;
    transition: all 0.2s ease;
    -webkit-tap-highlight-color: transparent;
  }

  .mobile-nav-icon {
    font-size: 1.35rem;
    line-height: 1;
    transition: transform 0.2s ease;
  }

  .mobile-nav-label {
    font-size: 0.68rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.3px;
  }

  .mobile-nav-btn.active {
    color: #3b82f6;
  }
  .mobile-nav-btn.active .mobile-nav-icon {
    transform: scale(1.15) translateY(-2px);
  }
  .mobile-nav-btn.active .mobile-nav-label {
    color: #3b82f6;
    font-weight: 800;
  }

  body.theme-light .mobile-nav-btn.active {
    color: #2563eb;
  }
  body.theme-light .mobile-nav-btn.active .mobile-nav-label {
    color: #2563eb;
  }

  /* Mobile Dashboard Enhancements */
  .char-hero-card {
    padding: 1.25rem 1rem;
    gap: 1rem;
  }
  .char-avatar-display {
    width: 68px;
    height: 68px;
    font-size: 2.4rem;
  }
  .char-name-title {
    font-size: 1.3rem;
  }
}
"""

MOBILE_BOTTOM_NAV_HTML = """
  <!-- Mobile Bottom Navigation Bar (App-Style Dock) -->
  <nav class="mobile-bottom-nav">
    <button class="mobile-nav-btn active" data-target="roadmap" onclick="app.navigate('roadmap')">
      <span class="mobile-nav-icon">🗺️</span>
      <span class="mobile-nav-label">로드맵</span>
    </button>
    <button class="mobile-nav-btn" data-target="articles" onclick="app.navigate('articles')">
      <span class="mobile-nav-icon">📚</span>
      <span class="mobile-nav-label">도서관</span>
    </button>
    <button class="mobile-nav-btn" data-target="trainer" onclick="app.navigate('trainer')">
      <span class="mobile-nav-icon">🎯</span>
      <span class="mobile-nav-label">스팟퀴즈</span>
    </button>
    <button class="mobile-nav-btn" data-target="matrix" onclick="app.navigate('matrix')">
      <span class="mobile-nav-icon">📊</span>
      <span class="mobile-nav-label">매트릭스</span>
    </button>
    <button class="mobile-nav-btn" data-target="glossary" onclick="app.navigate('glossary')">
      <span class="mobile-nav-icon">📖</span>
      <span class="mobile-nav-label">용어사전</span>
    </button>
  </nav>
"""

def update_head():
    with open(HEAD_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert MOBILE_CSS right before </style>
    if 'Mobile Optimization: App-Style Bottom Dock' not in html:
        html = html.replace('</style>', MOBILE_CSS + '\n</style>', 1)

    # 2. Insert MOBILE_BOTTOM_NAV_HTML right after </main>
    if 'class="mobile-bottom-nav"' not in html:
        html = html.replace('</main>', '</main>\n' + MOBILE_BOTTOM_NAV_HTML, 1)

    with open(HEAD_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated bundle_head.html with mobile bottom nav!")


def update_tail():
    with open(TAIL_PATH, 'r', encoding='utf-8') as f:
        tail = f.read()

    # In app.navigate, also update mobile-nav-btn active state
    old_nav_code = """    document.querySelectorAll('.nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });"""

    new_nav_code = """    document.querySelectorAll('.nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
      if (btn.dataset.target === viewId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });"""

    if '.mobile-nav-btn' not in tail:
        tail = tail.replace(old_nav_code, new_nav_code)

    with open(TAIL_PATH, 'w', encoding='utf-8') as f:
        f.write(tail)
    print("Updated bundle_tail.js with mobile nav syncing!")


if __name__ == '__main__':
    update_head()
    update_tail()
