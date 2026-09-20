from pathlib import Path
import re, html

root=Path('/mnt/data/v4work')
article_re=re.compile(r'(<article\s+class=["\']product["\'][^>]*>)(.*?)(</article>)', re.I|re.S)
h3_re=re.compile(r'(<h3\b[^>]*>)(.*?)(</h3>)', re.I|re.S)
img_re=re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', re.I|re.S)
changed=[]

def title_from_src(src):
    if not src.startswith('images/'):
        return None
    name=src.rsplit('/',1)[-1].lower()
    m=re.search(r'(?<!\d)(\d{4})(?:[-_])', name)
    if not m:
        return None
    year=m.group(1)
    if re.search(r'[-_]retro[-_]', name) or re.search(r'[-_]retro[._]', name):
        return f'{year} Retro'
    if re.search(r'[-_](?:player|jogador)[-_]', name) or re.search(r'[-_](?:player|jogador)[._]', name):
        return f'{year} Jogador'
    return year

for p in root.glob('*.html'):
    text=p.read_text(encoding='utf-8', errors='ignore')
    def repl(m):
        body=m.group(2)
        img=img_re.search(body)
        if not img: return m.group(0)
        title=title_from_src(html.unescape(img.group(1)))
        if not title: return m.group(0)
        hm=h3_re.search(body)
        if not hm: return m.group(0)
        old=re.sub(r'<[^>]+>','',hm.group(2)).strip()
        if old==title: return m.group(0)
        newbody=body[:hm.start(2)] + title + body[hm.end(2):]
        changed.append((p.name,old,title,img.group(1)))
        return m.group(1)+newbody+m.group(3)
    newtext=article_re.sub(repl,text)
    if newtext!=text:
        p.write_text(newtext,encoding='utf-8')
print('CHANGED',len(changed))
for x in changed: print(*x,sep=' | ')
