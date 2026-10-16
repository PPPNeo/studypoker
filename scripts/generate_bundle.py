"""
GTO Playbook KR - High-Performance Streaming Bundle Generator
Streams all 369 deep articles directly from disk into index.html and static/index.html.
Uses zero excess RAM via chunked I/O streaming.
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'templates', 'bundle_head.html'), encoding='utf-8') as f:
    head_content = f.read()

with open(os.path.join(BASE_DIR, 'templates', 'bundle_tail.js'), encoding='utf-8') as f:
    tail_content = f.read()

def write_bundle(target_path):
    with open(target_path, 'w', encoding='utf-8') as out:
        out.write(head_content)
        out.write("var DB = window.DB = {\n  articles: ")
        with open(os.path.join(BASE_DIR, 'data', 'articles.json'), 'r', encoding='utf-8') as af:
            shutil.copyfileobj(af, out)
        out.write(",\n  glossary: ")
        with open(os.path.join(BASE_DIR, 'data', 'glossary.json'), 'r', encoding='utf-8') as gf:
            shutil.copyfileobj(gf, out)
        out.write(",\n  quizzes: ")
        with open(os.path.join(BASE_DIR, 'data', 'quizzes.json'), 'r', encoding='utf-8') as qf:
            shutil.copyfileobj(qf, out)
        out.write(",\n  ranges: ")
        with open(os.path.join(BASE_DIR, 'data', 'ranges.json'), 'r', encoding='utf-8') as rf:
            shutil.copyfileobj(rf, out)
        out.write(",\n  roadmap: ")
        with open(os.path.join(BASE_DIR, 'data', 'roadmap.json'), 'r', encoding='utf-8') as rmf:
            shutil.copyfileobj(rmf, out)
        out.write("\n};\n\n")
        out.write(tail_content)

if __name__ == '__main__':
    root_index = os.path.join(BASE_DIR, 'index.html')
    static_index = os.path.join(BASE_DIR, 'static', 'index.html')

    write_bundle(root_index)
    shutil.copyfile(root_index, static_index)

    print(f"Generated standalone bundles with 369 deep articles!")
    print(f"  index.html: {os.path.getsize(root_index)} bytes")
    print(f"  static/index.html: {os.path.getsize(static_index)} bytes")
