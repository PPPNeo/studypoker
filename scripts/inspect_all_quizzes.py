# -*- coding: utf-8 -*-
import json

with open('data/quizzes.json', 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

for i, q in enumerate(quizzes):
    print(f"{i+1}. id={q['id']} title={q['title']} category={q.get('category')} level={q.get('level')}")
