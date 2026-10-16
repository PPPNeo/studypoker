"""
GTO Playbook KR - Interactive Poker Study Platform Backend
FastAPI server providing GTO articles, glossary, spot quizzes, AI coach, and range matrix
"""

import os
import json
import re
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="GTO Playbook KR",
    description="Interactive Poker Theory & GTO Wizard Study Platform for Korean Players",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")

def load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# In-memory storage / caches
articles_db = load_json("articles.json")
glossary_db = load_json("glossary.json")
quizzes_db = load_json("quizzes.json")
roadmap_db = load_json("roadmap.json")
ranges_db = load_json("ranges.json")

# In-memory User Session state (persists during server lifetime)
user_state = {
    "name": "포커신동",
    "avatar": "🦈",
    "playstyle": "TAG",
    "xp": 0,
    "level": 1,
    "streak": 1,
    "completed_articles": [],
    "completed_quizzes": [],
    "recent_answers": [],
    "promotions_passed": [],
    "ai_queries_count": 0
}

class QuizSubmission(BaseModel):
    quiz_id: str
    selected_option_index: int

class AIQuestion(BaseModel):
    question: str
    context: Optional[str] = None
    article_id: Optional[str] = None

class SyncSaveRequest(BaseModel):
    nickname: str
    pin: str
    state: Dict[str, Any]

class SyncLoadRequest(BaseModel):
    nickname: str
    pin: str

# ----------------- API ROUTES -----------------

@app.post("/api/sync/save")
def sync_save(req: SyncSaveRequest):
    users_file = os.path.join(DATA_DIR, "users_cloud.json")
    users = {}
    if os.path.exists(users_file):
        try:
            with open(users_file, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = {}
    
    key = req.nickname.strip().lower()
    if key in users and users[key].get("pin") != req.pin:
        raise HTTPException(status_code=403, detail="PIN 번호가 일치하지 않습니다.")
    
    users[key] = {
        "nickname": req.nickname.strip(),
        "pin": req.pin,
        "state": req.state
    }
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return {"success": True, "message": "클라우드 저장 완료"}

@app.post("/api/sync/load")
def sync_load(req: SyncLoadRequest):
    users_file = os.path.join(DATA_DIR, "users_cloud.json")
    if not os.path.exists(users_file):
        raise HTTPException(status_code=404, detail="해당 닉네임의 저장 기록을 찾을 수 없습니다.")
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="데이터베이스 읽기 실패")

    key = req.nickname.strip().lower()
    if key not in users:
        raise HTTPException(status_code=404, detail="해당 닉네임의 저장 기록을 찾을 수 없습니다.")
    if users[key].get("pin") != req.pin:
        raise HTTPException(status_code=403, detail="PIN 번호가 일치하지 않습니다.")
    return {"success": True, "state": users[key]["state"]}

@app.get("/api/articles")
def get_articles(category: Optional[str] = None, level: Optional[str] = None):
    results = []
    for art in articles_db:
        if category and category != "all" and art.get("category") != category:
            continue
        if level and level != "all" and level not in art.get("level", ""):
            continue
        # omit large content_html for summary list
        item = {k: v for k, v in art.items() if k != "content_html"}
        item["is_completed"] = art["id"] in user_state["completed_articles"]
        results.append(item)
    return results

@app.get("/api/articles/{article_id}")
def get_article(article_id: str):
    for art in articles_db:
        if art["id"] == article_id or art.get("slug") == article_id:
            article_copy = dict(art)
            article_copy["is_completed"] = art["id"] in user_state["completed_articles"]
            # find related quiz
            related_quizzes = [q for q in quizzes_db if q.get("article_id") == art["id"]]
            article_copy["related_quizzes"] = related_quizzes
            return article_copy
    raise HTTPException(status_code=404, detail="Article not found")

@app.post("/api/articles/{article_id}/complete")
def complete_article(article_id: str):
    if article_id not in user_state["completed_articles"]:
        user_state["completed_articles"].append(article_id)
        user_state["xp"] += 50
        check_level_up()
    return {"success": True, "xp": user_state["xp"], "level": user_state["level"]}

@app.get("/api/glossary")
def get_glossary(q: Optional[str] = None, category: Optional[str] = None):
    results = {}
    for key, item in glossary_db.items():
        if category and category != "all" and item.get("category") != category:
            continue
        if q:
            query = q.lower()
            text_pool = f"{key} {item.get('term', '')} {item.get('korean_term', '')} {item.get('short_desc', '')}".lower()
            if query not in text_pool:
                continue
        results[key] = item
    return results

@app.get("/api/glossary/{term_key}")
def get_term(term_key: str):
    key = term_key.lower().strip()
    if key in glossary_db:
        return glossary_db[key]
    raise HTTPException(status_code=404, detail="Term not found")

@app.get("/api/quizzes")
def get_quizzes():
    return quizzes_db

@app.post("/api/quizzes/submit")
def submit_quiz(sub: QuizSubmission):
    quiz = next((q for q in quizzes_db if q["id"] == sub.quiz_id), None)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    correct_idx = quiz["correct_index"]
    is_correct = (sub.selected_option_index == correct_idx)
    selected_opt = quiz["options"][sub.selected_option_index]
    
    xp_gained = 50 if is_correct else 10
    user_state["xp"] += xp_gained
    check_level_up()
    
    if is_correct and quiz["id"] not in user_state["completed_quizzes"]:
        user_state["completed_quizzes"].append(quiz["id"])
        
    return {
        "is_correct": is_correct,
        "selected_option": selected_opt,
        "correct_option": quiz["options"][correct_idx],
        "key_concept": quiz.get("key_concept", ""),
        "explanation": quiz["explanation"],
        "xp_gained": xp_gained,
        "current_xp": user_state["xp"],
        "level": user_state["level"]
    }

@app.get("/api/roadmap")
def get_roadmap():
    roadmap_copy = json.loads(json.dumps(roadmap_db))
    # Update unlocked status based on user level and XP
    for lvl in roadmap_copy["levels"]:
        lvl["is_unlocked"] = (user_state["xp"] >= lvl["required_xp"])
        for node in lvl["nodes"]:
            node["is_completed"] = node["article_id"] in user_state["completed_articles"]
    return {
        "user_state": user_state,
        "roadmap": roadmap_copy
    }

@app.get("/api/ranges")
def get_ranges():
    return ranges_db

@app.post("/api/ai/ask")
def ask_ai_coach(query: AIQuestion):
    """
    Intelligent Poker AI Coach providing localized answers based on GTO articles & theory
    """
    q = query.question.strip()
    q_lower = q.lower()
    
    # 1. Match against poker glossary & core strategy concepts
    matched_terms = []
    for k, v in glossary_db.items():
        if k in q_lower or v["korean_term"].lower() in q_lower or v["term"].lower() in q_lower:
            matched_terms.append(v)
            
    # Formulate rich conversational Korean poker response
    if "a72" in q_lower or "a-7-2" in q_lower or "작은 벳" in q_lower or "스몰 벳" in q_lower or "1/3" in q_lower or "c-bet" in q_lower or "c벳" in q_lower:
        answer = (
            "**[코치 Ivan의 GTO 해설]**\n\n"
            "A-7-2r이나 K-8-3r 같은 **드라이한 A/K-high 보드**에서 1/3팟의 작은 C-bet을 전체 레인지(80~100%)로 구사하는 이유는 명확합니다:\n\n"
            "1. **압도적인 레인지 우위 (Range Advantage)**: 프리플랍 레이저(IP)는 AA, AK, AQ을 모두 쥐고 있는 반면, BB는 보통 AA, AK을 3벳으로 뺐기 때문에 레인지가 캡(Capped)되어 있습니다.\n"
            "2. **낮은 에퀴티 저항선**: A가 깔린 보드에서는 상대방의 99, 88 같은 포켓페어나 언더카드가 턴에서 역전할 확률이 5장 이하(약 10~15%)로 매우 낮습니다.\n"
            "3. **효율적 칩 보존**: 굳이 팟을 크게 키우지 않아도 상대의 에어(Air) 핸드와 약한 콤보들을 1/3 팟만으로 즉시 폴드시킬 수 있기 때문입니다!"
        )
    elif "블로커" in q_lower or "언블로커" in q_lower or "blocker" in q_lower:
        answer = (
            "**[코치 Tombos의 GTO 해설]**\n\n"
            "블로커는 콤보 수학의 마법입니다. 핵심 원칙을 요약해 드릴게요:\n\n"
            "1. **리버 블러프를 칠 때**: 상대의 **'콜할 최강 핸드'**를 블락해야 합니다! (예: 상대의 스트레이트 완성 카드인 T이나 너트 플러시 카드인 A♠를 내가 쥐고 있어야 상대가 콜을 못 합니다.)\n"
            "2. **언블로커의 중요성**: 반대로 상대가 미스해서 폴드해야 할 카드(Busted Draw)는 내가 **쥐고 있지 않아야(Unblock)** 합니다. 내가 그 카드를 들고 있으면 상대가 폴드할 꽝 핸드가 사라지기 때문입니다.\n"
            "3. **블러프 캐칭(콜)할 때**: 상대의 블러프 카드를 블락하지 말고, 순수하게 언블락 상태여야 상대가 블러프를 시도했을 확률이 높아집니다."
        )
    elif "mdf" in q_lower or "최소 방어" in q_lower:
        answer = (
            "**[GTO Wizard 이론팀 해설]**\n\n"
            "**MDF (Minimum Defense Frequency)**는 상대가 아무 카드로나 블러프를 쳐서 '자동 수익(공짜 돈)'을 내지 못하도록 방어해야 하는 이론적 하한선입니다.\n\n"
            "- 공식: `MDF = 팟 사이즈 / (팟 사이즈 + 베팅 금액)`\n"
            "- 예시: 100칩 팟에 상대가 50칩(하프팟)을 베팅하면 `100 / (100 + 50) = 66.7%`를 최소한 콜 또는 레이스로 방어해야 합니다.\n"
            "- ⚠️ **주의사항**: 보드에 상대의 너트 우위가 극심할 때는 MDF를 문자 그대로 지키려다 스택이 털릴 수 있습니다. 실전 솔버는 텍스처에 따라 오버폴드(Overfold)를 자주 지시합니다."
        )
    elif "icm" in q_lower or "토너먼트" in q_lower:
        answer = (
            "**[토너먼트 스페셜리스트 조언]**\n\n"
            "토너먼트 파이널 테이블이나 버블에서는 **ChipEV(칩 기대값)**로 생각하면 패망합니다. 반드시 **$EV(실제 상금 가치)**로 접근해야 합니다:\n\n"
            "- **칩의 비대칭성**: 칩을 딸 때 얻는 가치보다 칩을 잃을 때 날아가는 상금 가치가 훨씬 큽니다.\n"
            "- **리스크 프리미엄**: 칩리더를 상대로는 AKs나 QQ 같은 프리미엄 핸드조차 뒤의 숏스택 탈락을 기다리기 위해 눈물을 머금고 폴드해야 하는 순간이 있습니다."
        )
    elif matched_terms:
        term = matched_terms[0]
        answer = (
            f"**[{term['term']} ({term['korean_term']}) 핵심 정리]**\n\n"
            f"📌 **정의**: {term['short_desc']}\n\n"
            f"💡 **실전 비유**: {term['analogy']}\n\n"
            f"⚡ **GTO 프로 팁**: {term['pro_tip']}"
        )
    else:
        answer = (
            f"**[AI 포커 코치 답변]**\n\n"
            f"질문해 주신 '{q}'에 대한 GTO 전략 관점의 조언입니다:\n\n"
            "포커 의사결정의 핵심은 언제나 **[레인지 vs 레인지의 상호작용]**입니다. "
            "단 한 장의 내 카드가 아닌, 상대의 전체 레인지와 내 전체 레인지가 현재 보드 텍스처에서 어떤 에퀴티 분포를 가지는지를 먼저 파악하세요.\n\n"
            "- 내가 **너트 우위**를 가지면? 👉 큰 벳(75%+)이나 오버벳으로 압박\n"
            "- 내가 **레인지 우위**만 가지면? 👉 작은 벳(25~33%)으로 넓은 빈도 공격\n"
            "- 상대가 너트 우위를 점하면? 👉 첵백 빈도를 높여 팟 컨트롤"
        )
        
    return {
        "question": q,
        "answer": answer,
        "matched_terms": [t["term"] for t in matched_terms]
    }

def get_level_threshold(lvl: int) -> int:
    if lvl <= 1:
        return 0
    return int(68 * (lvl ** 1.55))

def check_level_up():
    xp = user_state["xp"]
    promotions = user_state.get("promotions_passed", [])
    raw_lvl = 1
    for l in range(1, 101):
        if xp >= get_level_threshold(l):
            raw_lvl = l
        else:
            break
            
    # Gateways for 6 promotions (Lv.10, 25, 45, 65, 85, 100)
    effective_lvl = raw_lvl
    gateways = [(1, 10), (2, 25), (3, 45), (4, 65), (5, 85), (6, 100)]
    for tier, req in gateways:
        if raw_lvl >= req and tier not in promotions:
            effective_lvl = req
            break
            
    user_state["level"] = effective_lvl

@app.get("/api/ranking")
def get_ranking():
    """
    Returns global leaderboard sorted by Level (DESC) then XP (DESC)
    """
    rivals = [
        {"name": "LinusLove", "avatar": "🦁", "style": "GTO", "level": 98, "xp": 82400, "articles": 340, "tier": "🦁 하이롤러 위저드"},
        {"name": "Phil_Ivey", "avatar": "👑", "style": "EXPLOIT", "level": 96, "xp": 78900, "articles": 325, "tier": "🦁 하이롤러 위저드"},
        {"name": "폴푸아 (Master)", "avatar": "🦈", "style": "TAG", "level": 94, "xp": 75100, "articles": 369, "tier": "🦁 하이롤러 위저드"},
        {"name": "Daniel_Negreanu", "avatar": "🦊", "style": "EXPLOIT", "level": 91, "xp": 71200, "articles": 290, "tier": "🦁 하이롤러 위저드"},
        {"name": "Fedor_Holz", "avatar": "🧠", "style": "GTO", "level": 88, "xp": 68400, "articles": 260, "tier": "🦁 하이롤러 위저드"},
        {"name": "압구정샤크", "avatar": "🦈", "style": "TAG", "level": 82, "xp": 60200, "articles": 210, "tier": "🦊 미드스테이크 프로"},
        {"name": "마카오레귤러", "avatar": "🦁", "style": "LAG", "level": 78, "xp": 55400, "articles": 185, "tier": "🦊 미드스테이크 프로"},
        {"name": "GTO솔버러", "avatar": "🤖", "style": "GTO", "level": 73, "xp": 49800, "articles": 160, "tier": "🦊 미드스테이크 프로"},
        {"name": "체크레이즈달인", "avatar": "🥷", "style": "LAG", "level": 68, "xp": 44200, "articles": 135, "tier": "🦊 미드스테이크 프로"},
        {"name": "홍대펍지배자", "avatar": "⚔️", "style": "TAG", "level": 62, "xp": 38600, "articles": 110, "tier": "🔥 로우스테이크 크러셔"},
        {"name": "온라인그라인더99", "avatar": "⚙️", "style": "TAG", "level": 56, "xp": 33100, "articles": 95, "tier": "🔥 로우스테이크 크러셔"},
        {"name": "강남너트장인", "avatar": "🦊", "style": "EXPLOIT", "level": 50, "xp": 27900, "articles": 80, "tier": "🔥 로우스테이크 크러셔"},
        {"name": "리버원샷", "avatar": "🦉", "style": "HUNTER", "level": 46, "xp": 24500, "articles": 65, "tier": "🔥 로우스테이크 크러셔"},
        {"name": "스몰블라인드킬러", "avatar": "🥷", "style": "LAG", "level": 41, "xp": 20800, "articles": 55, "tier": "⚙️ 마이크로 그라인더"},
        {"name": "팟스틸러", "avatar": "🦊", "style": "LAG", "level": 36, "xp": 17200, "articles": 45, "tier": "⚙️ 마이크로 그라인더"},
        {"name": "3벳마니아", "avatar": "🦁", "style": "LAG", "level": 31, "xp": 13900, "articles": 38, "tier": "⚙️ 마이크로 그라인더"},
        {"name": "에퀴티계산기", "avatar": "🤖", "style": "GTO", "level": 27, "xp": 10800, "articles": 30, "tier": "⚙️ 마이크로 그라인더"},
        {"name": "홀덤꿈나무", "avatar": "🐣", "style": "TAG", "level": 23, "xp": 8500, "articles": 24, "tier": "⚔️ 펍 레귤러"},
        {"name": "펍루키007", "avatar": "⚔️", "style": "HUNTER", "level": 19, "xp": 6200, "articles": 18, "tier": "⚔️ 펍 레귤러"},
        {"name": "포커새싹", "avatar": "🌱", "style": "TAG", "level": 14, "xp": 3900, "articles": 12, "tier": "⚔️ 펍 레귤러"},
        {"name": "마이크로도전자", "avatar": "⚙️", "style": "TAG", "level": 11, "xp": 2600, "articles": 9, "tier": "⚔️ 펍 레귤러"},
        {"name": "초보홀덤러", "avatar": "🐟", "style": "HUNTER", "level": 7, "xp": 1200, "articles": 5, "tier": "🐣 동네 피쉬"},
        {"name": "스타팅핸드공부중", "avatar": "🐣", "style": "TAG", "level": 4, "xp": 500, "articles": 2, "tier": "🐣 동네 피쉬"},
        {"name": "입문자A", "avatar": "🐟", "style": "TAG", "level": 2, "xp": 150, "articles": 1, "tier": "🐣 동네 피쉬"}
    ]
    
    # Calculate user tier title
    tier_map = {
        0: "🐣 동네 피쉬",
        1: "⚔️ 펍 레귤러",
        2: "⚙️ 마이크로 그라인더",
        3: "🔥 로우스테이크 크러셔",
        4: "🦊 미드스테이크 프로",
        5: "🦁 하이롤러 위저드",
        6: "👑 WSOP 레전드 챔피언"
    }
    highest_promo = max([0] + user_state.get("promotions_passed", []))
    my_tier = tier_map.get(highest_promo, "🐣 동네 피쉬")
    
    me = {
        "name": user_state.get("name", "포커신동"),
        "avatar": user_state.get("avatar", "🦈"),
        "style": user_state.get("playstyle", "TAG"),
        "level": user_state["level"],
        "xp": user_state["xp"],
        "articles": len(user_state.get("completed_articles", [])),
        "tier": my_tier,
        "is_me": True
    }
    
    all_players = rivals + [me]
    # Sort: 1) Level DESC, 2) XP DESC
    all_players.sort(key=lambda p: (p["level"], p["xp"]), reverse=True)
    
    for idx, p in enumerate(all_players, start=1):
        p["rank"] = idx
        
    return {
        "players": all_players,
        "my_rank": next((p["rank"] for p in all_players if p.get("is_me")), 1)
    }

# ----------------- STATIC ASSETS & SPA ROUTE -----------------

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
@app.get("/index.html")
def serve_index():
    root_index = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(root_index):
        return FileResponse(root_index)
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Also support routes without /api prefix in case serverless strips it
@app.get("/articles")
def get_articles_alias(category: Optional[str] = None, level: Optional[str] = None):
    return get_articles(category=category, level=level)

@app.get("/quizzes")
def get_quizzes_alias():
    return get_quizzes()

@app.get("/glossary")
def get_glossary_alias(q: Optional[str] = None, category: Optional[str] = None):
    return get_glossary(q=q, category=category)

@app.get("/roadmap")
def get_roadmap_alias():
    return get_roadmap()

@app.get("/ranges")
def get_ranges_alias():
    return get_ranges()

@app.post("/ai/ask")
def ask_ai_alias(query: AIQuestion):
    return ask_ai_coach(query)

@app.post("/quizzes/submit")
def submit_quiz_alias(sub: QuizSubmission):
    return submit_quiz(sub)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
