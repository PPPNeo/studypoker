# -*- coding: utf-8 -*-
"""
Streaming verification script that doesn't load large JSON files into RAM all at once.
"""

# Check index.html by streaming lines
found = {
    'level-lock-modal-overlay': False,
    'quiz-locked-shield': False,
    'matrix-locked-shield': False,
    'filter-unlocked-btn': False,
    'quiz-level-filter-chips': False
}

with open('index.html', 'r', encoding='utf-8') as f:
    for line in f:
        for k in found:
            if k in line:
                found[k] = True

for k, v in found.items():
    assert v, f"Target '{k}' not found in index.html"

print("STREAMING VERIFICATION: ALL 5 TARGETS CONFIRMED IN index.html!")
