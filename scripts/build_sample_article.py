import json
import re

with open('data/raw_ghost_full.json', encoding='utf-8') as f:
    posts = json.load(f)

# Find first post
post = posts[0]

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    return text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('’', "'").replace('“', '"').replace('”', '"').strip()

def build_rich_korean_article(p):
    title_en = p['title']
    html = p.get('html', '')
    
    # Extract sections
    normalized = re.sub(r'<h3[^>]*>', '<h2>', html)
    normalized = re.sub(r'</h3>', '</h2>', normalized)
    parts = re.split(r'<h2[^>]*>', normalized)
    
    # Intro
    intro_paras = [clean_html(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', parts[0], re.DOTALL) if clean_html(x)]
    intro_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', parts[0])
    
    content_parts = []
    
    # Lead paragraph
    intro_lead = intro_paras[0] if intro_paras else p.get('custom_excerpt', '')
    content_parts.append(f"""
      <div class="article-lead">
        <strong>{title_en}</strong>: {intro_lead}
      </div>
    """)
    
    # Intro details
    if len(intro_paras) > 1:
        content_parts.append("<h2>1. 핵심 개요 및 배경 (Overview & Strategic Background)</h2>")
        for para in intro_paras[1:]:
            content_parts.append(f"<p>{para}</p>")
        if intro_imgs:
            for img in intro_imgs[:2]:
                content_parts.append(f"""
                  <div class="article-chart-wrapper" style="margin: 1.5rem 0; text-align: center;">
                    <img src="{img}" alt="GTO Solver Analysis" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 16px rgba(0,0,0,0.3);" loading="lazy">
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">📊 GTO Wizard 솔버 분석 차트</div>
                  </div>
                """)
    
    # Iterate through remaining sections
    sec_idx = 2 if len(intro_paras) > 1 else 1
    for part in parts[1:]:
        m = re.match(r'^(.*?)</h2>(.*)', part, re.DOTALL)
        if not m:
            continue
        raw_h = clean_html(m.group(1))
        body = m.group(2)
        paras = [clean_html(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL) if clean_html(x)]
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', body)
        
        if not paras and not imgs:
            continue
            
        content_parts.append(f"<h2>{sec_idx}. {raw_h}</h2>")
        sec_idx += 1
        
        # Add paragraphs
        for para in paras:
            content_parts.append(f"<p>{para}</p>")
            
        # Add chart images
        for img in imgs:
            content_parts.append(f"""
              <div class="article-chart-wrapper" style="margin: 1.5rem 0; text-align: center;">
                <img src="{img}" alt="{raw_h} 차트" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 16px rgba(0,0,0,0.3);" loading="lazy">
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">📊 {raw_h} - GTO Wizard 솔버 시뮬레이션</div>
              </div>
            """)
            
    # Add final conclusion and original link
    original_url = f"https://blog.gtowizard.com/{p['slug']}/"
    content_parts.append(f"""
      <div class="callout-card tip" style="margin-top: 2rem;">
        <h4>💡 핵심 솔버 테이크어웨이</h4>
        <p>GTO 솔버 분석 결과, 이 스팟에서는 단일 핸드의 절대적 밸류보다 <strong>포지션 이점, 스프레드, 팟 오즈 및 레인지 밸런스</strong>를 엄격하게 지키는 것이 장기적인 EV를 극대화하는 핵심 열쇠입니다.</p>
      </div>

      <div style="margin: 2rem 0; padding: 1.5rem; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; text-align: center;">
        <h3 style="margin-bottom: 0.5rem; font-size: 1.1rem; color: var(--text-main);">📖 원문 전체 보기 및 인터랙티브 솔버</h3>
        <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.25rem;">GTO Wizard 공식 블로그에서 전체 시뮬레이션 트리와 핸드 히스토리를 직접 조작해보세요.</p>
        <a href="{original_url}" target="_blank" rel="noopener noreferrer" class="btn-primary" style="display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none; padding: 0.75rem 1.75rem; border-radius: 25px;">
          <span>🌐</span> GTO Wizard 공식 원문 열기 (English) ↗
        </a>
      </div>
    """)
    
    return "\n".join(content_parts)

sample_html = build_rich_korean_article(post)
with open('scripts/sample_output.html', 'w', encoding='utf-8') as f:
    f.write(sample_html)

print(f"Generated sample article! Length: {len(sample_html)} bytes")
