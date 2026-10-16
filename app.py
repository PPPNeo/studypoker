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
    "xp": 120,
    "level": 1,
    "streak": 3,
    "completed_articles": ["what-is-expected-value-in-poker"],
    "completed_quizzes": [],
    "recent_answers": []
}

class QuizSubmission(BaseModel):
    quiz_id: str
    selected_option_index: int

class AIQuestion(BaseModel):
    question: str
    context: Optional[str] = None
    article_id: Optional[str] = None

# ----------------- API ROUTES -----------------

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

def check_level_up():
    xp = user_state["xp"]
    new_lvl = 1
    if xp >= 800:
        new_lvl = 4
    elif xp >= 500:
        new_lvl = 3
    elif xp >= 200:
        new_lvl = 2
    user_state["level"] = new_lvl

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
