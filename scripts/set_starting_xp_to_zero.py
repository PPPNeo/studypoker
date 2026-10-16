# -*- coding: utf-8 -*-
"""
set_starting_xp_to_zero.py
Ensures new characters and fresh sessions start strictly at 0 XP,
with 0 completed articles, 0 stats (Grade D), and 0% progress bars.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_head.html')
TAIL_PATH = os.path.join(BASE_DIR, 'templates', 'bundle_tail.js')

def update_head():
    with open(HEAD_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update header user bar initial state
    html = html.replace(
        '<span id="user-streak">3</span>일 연속',
        '<span id="user-streak">1</span>일 연속'
    )
    html = html.replace(
        '<span id="user-xp-text">120 / 200 XP</span>',
        '<span id="user-xp-text">0 / 200 XP</span>'
    )
    html = html.replace(
        '<div class="xp-progress" id="user-xp-bar" style="width: 60%;"></div>',
        '<div class="xp-progress" id="user-xp-bar" style="width: 0%;"></div>'
    )

    # 2. Update dashboard hero card initial state
    html = html.replace(
        '<span class="char-xp-current" id="dash-xp-text">120 / 200 XP</span>',
        '<span class="char-xp-current" id="dash-xp-text">0 / 200 XP</span>'
    )
    html = html.replace(
        '<span class="char-xp-remaining" id="dash-xp-needed">다음 승급까지 80 XP 남음</span>',
        '<span class="char-xp-remaining" id="dash-xp-needed">다음 승급까지 200 XP 남음</span>'
    )
    html = html.replace(
        '<div class="char-progress-fill" id="dash-xp-fill" style="width: 60%;"></div>',
        '<div class="char-progress-fill" id="dash-xp-fill" style="width: 0%;"></div>'
    )

    # 3. Update initial stat cards to 0 PTS and Grade D
    html = html.replace(
        '<span class="stat-grade grade-C" id="stat-grade-theory">C</span>',
        '<span class="stat-grade grade-D" id="stat-grade-theory">D</span>'
    )
    html = html.replace(
        '<div class="stat-bar-fill theory" id="stat-bar-theory" style="width: 35%;"></div>',
        '<div class="stat-bar-fill theory" id="stat-bar-theory" style="width: 0%;"></div>'
    )
    html = html.replace(
        '<div class="stat-val-text"><span id="stat-val-theory">35</span> / 100 PTS</div>',
        '<div class="stat-val-text"><span id="stat-val-theory">0</span> / 100 PTS</div>'
    )

    html = html.replace(
        '<span class="stat-grade grade-B" id="stat-grade-decision">B</span>',
        '<span class="stat-grade grade-D" id="stat-grade-decision">D</span>'
    )
    html = html.replace(
        '<div class="stat-bar-fill decision" id="stat-bar-decision" style="width: 40%;"></div>',
        '<div class="stat-bar-fill decision" id="stat-bar-decision" style="width: 0%;"></div>'
    )
    html = html.replace(
        '<div class="stat-val-text"><span id="stat-val-decision">40</span> / 100 PTS</div>',
        '<div class="stat-val-text"><span id="stat-val-decision">0</span> / 100 PTS</div>'
    )

    html = html.replace(
        '<span class="stat-grade grade-C" id="stat-grade-ranges">C</span>',
        '<span class="stat-grade grade-D" id="stat-grade-ranges">D</span>'
    )
    html = html.replace(
        '<div class="stat-bar-fill ranges" id="stat-bar-ranges" style="width: 25%;"></div>',
        '<div class="stat-bar-fill ranges" id="stat-bar-ranges" style="width: 0%;"></div>'
    )
    html = html.replace(
        '<div class="stat-val-text"><span id="stat-val-ranges">25</span> / 100 PTS</div>',
        '<div class="stat-val-text"><span id="stat-val-ranges">0</span> / 100 PTS</div>'
    )

    html = html.replace(
        '<span class="stat-grade grade-B" id="stat-grade-mental">B</span>',
        '<span class="stat-grade grade-D" id="stat-grade-mental">D</span>'
    )
    html = html.replace(
        '<div class="stat-bar-fill mental" id="stat-bar-mental" style="width: 50%;"></div>',
        '<div class="stat-bar-fill mental" id="stat-bar-mental" style="width: 0%;"></div>'
    )
    html = html.replace(
        '<div class="stat-val-text"><span id="stat-val-mental">50</span> / 100 PTS</div>',
        '<div class="stat-val-text"><span id="stat-val-mental">0</span> / 100 PTS</div>'
    )

    with open(HEAD_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated bundle_head.html to 0 XP starting state!")


def update_tail():
    with open(TAIL_PATH, 'r', encoding='utf-8') as f:
        tail = f.read()

    # 1. Update storage.get() default state
    old_storage = """    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (!parsed.name) parsed.name = '포커신동';
        if (!parsed.avatar) parsed.avatar = '🦈';
        if (!parsed.playstyle) parsed.playstyle = 'TAG';
        if (!parsed.stats) parsed.stats = { theory: 35, decision: 40, ranges: 25, mental: 50 };
        return parsed;
      } catch(e) {}
    }
    return {
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

    new_storage = """    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (!parsed.name) parsed.name = '포커신동';
        if (!parsed.avatar) parsed.avatar = '🦈';
        if (!parsed.playstyle) parsed.playstyle = 'TAG';
        if (!parsed.stats) parsed.stats = { theory: 0, decision: 0, ranges: 0, mental: 0 };
        if (parsed.xp === undefined) parsed.xp = 0;
        if (!parsed.completed_articles) parsed.completed_articles = [];
        if (!parsed.completed_quizzes) parsed.completed_quizzes = [];
        return parsed;
      } catch(e) {}
    }
    return {
      name: '포커신동',
      avatar: '🦈',
      playstyle: 'TAG',
      xp: 0,
      level: 1,
      streak: 1,
      stats: {
        theory: 0,
        decision: 0,
        ranges: 0,
        mental: 0
      },
      completed_articles: [],
      completed_quizzes: []
    };"""
    tail = tail.replace(old_storage, new_storage)

    # 2. Update characterManager.saveCharacter() to ensure 0 XP on initial creation
    old_save_char = """    app.userState.name = newName;
    app.userState.avatar = this.selectedAvatar;
    app.userState.playstyle = this.selectedStyle;

    localStorage.setItem('studypoker_char_created', 'true');
    storage.save(app.userState);
    this.renderHeader();
    this.renderDashboard();
    this.closeModal();

    if (window.app && app.playAudioEffect) app.playAudioEffect('correct');
    this.showToast(`🎉 <strong>[${newName}]</strong> 님, 환영합니다! Lv.1 피쉬 탈출 퀘스트를 시작하세요.`);"""

    new_save_char = """    const isFirstTime = !localStorage.getItem('studypoker_char_created');

    app.userState.name = newName;
    app.userState.avatar = this.selectedAvatar;
    app.userState.playstyle = this.selectedStyle;

    if (isFirstTime) {
      app.userState.xp = 0;
      app.userState.level = 1;
      app.userState.streak = 1;
      app.userState.stats = { theory: 0, decision: 0, ranges: 0, mental: 0 };
      app.userState.completed_articles = [];
      app.userState.completed_quizzes = [];
    }

    localStorage.setItem('studypoker_char_created', 'true');
    storage.save(app.userState);
    app.updateUserBar();
    this.renderHeader();
    this.renderDashboard();
    this.closeModal();

    if (window.app && app.playAudioEffect) app.playAudioEffect('correct');
    this.showToast(`🎉 <strong>[${newName}]</strong> 님, 환영합니다! 0 XP에서 시작하여 Lv.1 피쉬 탈출 퀘스트를 완수해보세요!`);"""
    tail = tail.replace(old_save_char, new_save_char)

    # 3. Update characterManager.renderDashboard() default stats
    tail = tail.replace(
        "const stats = u.stats || { theory: 35, decision: 40, ranges: 25, mental: 50 };",
        "const stats = u.stats || { theory: 0, decision: 0, ranges: 0, mental: 0 };"
    )

    # 4. Make roadmap.load() achievements dynamically tied to real userState
    old_achievements_render = """    const achContainer = document.getElementById('roadmap-achievements-container');
    achContainer.innerHTML = rm.achievements.map(a => `
      <div class="feature-item" style="opacity: ${a.unlocked ? '1' : '0.45'};">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">${a.icon}</div>
        <h4 style="font-size: 1.05rem; margin-bottom: 0.25rem;">${a.title}</h4>
        <p style="font-size: 0.85rem; color: var(--text-muted);">${a.desc}</p>
        <div style="margin-top: 0.75rem; font-size: 0.75rem; font-weight: 700; color: ${a.unlocked ? '#34d399' : '#64748b'};">
          ${a.unlocked ? '🏆 달성 완료' : '미달성'}
        </div>
      </div>
    `).join('');"""

    new_achievements_render = """    const dynamicAchievements = [
      {
        id: "char_created",
        title: "모험의 시작",
        desc: "나만의 포커 캐릭터 생성 및 첫 발걸음",
        icon: userState.avatar || "🦈",
        unlocked: !!localStorage.getItem('studypoker_char_created')
      },
      {
        id: "first_read",
        title: "첫 페이지를 넘기다",
        desc: "첫 번째 GTO 아티클 완독 (+50 XP)",
        icon: "📖",
        unlocked: (userState.completed_articles && userState.completed_articles.length > 0)
      },
      {
        id: "quiz_ace",
        title: "솔버적 뇌지컬",
        desc: "스팟 퀴즈 정답 맞히기 (+50 XP)",
        icon: "🎯",
        unlocked: (userState.completed_quizzes && userState.completed_quizzes.length > 0)
      },
      {
        id: "streak_3",
        title: "3일 연속 그라인딩",
        desc: "3일 연속 학습 스트릭 유지",
        icon: "🔥",
        unlocked: ((userState.streak || 0) >= 3)
      },
      {
        id: "level_up",
        title: "로컬 레귤러 달성",
        desc: "200 XP 달성 및 Lv.2 진화",
        icon: "⚔️",
        unlocked: ((userState.xp || 0) >= 200)
      },
      {
        id: "matrix_explorer",
        title: "레인지의 지배자",
        desc: "13x13 매트릭스 5개 이상 포지션 탐색",
        icon: "📊",
        unlocked: (matrix._explored && Object.keys(matrix._explored).length >= 5)
      }
    ];

    const achContainer = document.getElementById('roadmap-achievements-container');
    if (achContainer) {
      achContainer.innerHTML = dynamicAchievements.map(a => `
        <div class="feature-item" style="opacity: ${a.unlocked ? '1' : '0.45'};">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">${a.icon}</div>
          <h4 style="font-size: 1.05rem; margin-bottom: 0.25rem;">${a.title}</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted);">${a.desc}</p>
          <div style="margin-top: 0.75rem; font-size: 0.75rem; font-weight: 700; color: ${a.unlocked ? '#34d399' : '#64748b'};">
            ${a.unlocked ? '🏆 달성 완료' : '미달성'}
          </div>
        </div>
      `).join('');
    }"""
    tail = tail.replace(old_achievements_render, new_achievements_render)

    with open(TAIL_PATH, 'w', encoding='utf-8') as f:
        f.write(tail)
    print("Updated bundle_tail.js to 0 XP starting state!")

if __name__ == '__main__':
    update_head()
    update_tail()
