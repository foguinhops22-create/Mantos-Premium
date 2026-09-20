from pathlib import Path
import zipfile,re,html
base=Path('/mnt/data/buildv3'); imgroot=base/'images'; new=Path('/mnt/data/newimgs')
with zipfile.ZipFile('/mnt/data/Mantos_Premium_V2_backup.zip') as z:
 base_files=set(z.namelist())
# map each new source to output name

def outname(src):
 rel=src.relative_to(new); normal='images/'+str(rel.with_suffix('.webp')).replace('\\','/')
 if normal not in base_files: return str(rel.with_suffix('.webp')).replace('\\','/')
 # choose first novo name that exists
 stem=Path(normal).stem; folder=imgroot/Path(normal).parent.relative_to('images')
 i=2
 while True:
  candidate=f'{stem}-novo{i}.webp'
  if (folder/candidate).exists(): return str(Path(normal).parent/candidate).replace('\\','/')
  i+=1
names={'flamengo':'Flamengo','gremio':'Grêmio','internacional':'Internacional','inter-de-milao':'Inter de Milão','liverpool':'Liverpool','manchester-city':'Manchester City','manchester-united':'Manchester United','milan':'Milan','newcastle':'Newcastle','psg':'PSG','real-madrid':'Real Madrid','roma':'Roma','sevilla':'Sevilla','valencia':'Valencia'}
cat={k:('br' if k in ('flamengo','gremio','internacional') else 'eu') for k in names}

def products(team):
 d=new/team; rows=[]
 for src in sorted(d.glob('*frente*')):
  if src.suffix.lower() not in ('.jpg','.jpeg','.png'): continue
  v=next((x for x in d.iterdir() if x.stem==src.stem.replace('frente','verso')),None)
  if not v: continue
  fpath=outname(src); vpath=outname(v)
  title=src.stem.replace('-frente','').replace('_frente','').replace('frente','')
  title=title.replace('-retro',' Retro').replace('_retro',' Retro').replace('-libertadores',' Libertadores').replace('-player',' Jogador').replace('_player',' Jogador')
  title=re.sub(r'[-_]',' ',title); title=re.sub(r'\s+',' ',title).strip(); label='Camisa '+title
  tag='CLUBES BRASILEIROS' if cat[team]=='br' else 'CLUBES EUROPEUS'
  rows.append(f'''<article class="product"><div class="photo club-carousel" data-carousel="{team}-novo-{len(rows)}"><div class="carousel-track"><img class="carousel-slide is-active" src="{fpath}" alt="{html.escape(label)} - frente"><img class="carousel-slide" src="{vpath}" alt="{html.escape(label)} - verso"></div><button class="carousel-arrow carousel-prev" type="button" aria-label="Ver foto anterior">‹</button><button class="carousel-arrow carousel-next" type="button" aria-label="Ver próxima foto">›</button><div class="carousel-dots" aria-hidden="true"><span class="carousel-dot is-active"></span><span class="carousel-dot"></span></div></div><div class="info"><span class="tag">{tag}</span><h3>{html.escape(label)}</h3><p>Camisa Tailandesa</p><strong>R$ 129</strong><button onclick="buy('{html.escape(names[team])} - {html.escape(label)}')">Comprar Pelo WhatsApp</button></div></article>''')
 return '\n'.join(rows)
for team in names:
 block=products(team); page=base/f'{team}.html'
 if not block: continue
 if page.exists():
  txt=page.read_text(encoding='utf-8')
  txt=txt.replace('</div></div></main>',block+'\n</div></div></main>',1)
 else:
  catfile='brasileiros.html' if cat[team]=='br' else 'europeus.html'; catname='Clubes Brasileiros' if cat[team]=='br' else 'Clubes Europeus'
  txt=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Camisas {names[team]} | Mantos Premium</title><link rel="stylesheet" href="style.css?v=7"></head><body><header class="top"><div class="container nav"><a class="brand" href="index.html"><img src="assets/logo.jpg"><span>MANTOS <b>PREMIUM</b></span></a><nav class="links"><a href="brasileiros.html">Clubes Brasileiros</a><a href="europeus.html">Clubes Europeus</a><a href="selecoes.html">Seleções</a><a href="infantis.html">Infantis</a><a href="lancamentos.html">Lançamentos</a></nav></div></header><section class="hero team-page"><div class="container"><a class="team-back" href="{catfile}">← Voltar para {catname}</a><span class="crumb">MANTOS PREMIUM</span><h1>{names[team]}</h1><p>Aqui aparecem somente as camisas de {names[team]} disponíveis na Mantos Premium.</p></div></section><main class="content"><div class="container"><div class="notice">👕 <b>{names[team]}</b> • 📏 Tamanhos P, M, G e GG • 📦 Enviamos para todo o Brasil</div><div class="product-grid">{block}</div></div></main><section class="social"><div class="container social-inner"><div><span class="crumb">MANTOS PREMIUM</span><h2>Fale com a gente</h2><p>Escolha onde quer continuar:</p></div><div class="social-buttons"><a class="social-btn whatsapp" href="https://wa.me/5511911321494?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Mantos%20Premium." target="_blank">📲 WhatsApp</a><a class="social-btn group" href="https://chat.whatsapp.com/HgAmfUZx5NPD6XtovopAYB" target="_blank">👥 Grupo Oficial</a><a class="social-btn instagram" href="https://www.instagram.com/mantospremium_/" target="_blank">📸 Instagram</a></div></div></section><footer class="footer"><div class="container"><strong>MANTOS PREMIUM</strong><p>📍 Itatiba-SP • 📲 11 91132-1494 • <a href="https://www.instagram.com/mantospremium_/" target="_blank">📸 @mantospremium_</a></p></div></footer><a class="floating" href="https://wa.me/5511911321494?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Mantos%20Premium." target="_blank">💬</a><script src="script.js"></script></body></html>'''
  page.write_text(txt,encoding='utf-8')
# category cards
cards={'gremio':('Grêmio','https://media.api-sports.io/football/teams/130.png','br'),'internacional':('Internacional','https://media.api-sports.io/football/teams/119.png','br'),'inter-de-milao':('Inter de Milão','https://media.api-sports.io/football/teams/505.png','eu'),'milan':('Milan','https://media.api-sports.io/football/teams/489.png','eu'),'newcastle':('Newcastle','https://media.api-sports.io/football/teams/34.png','eu'),'roma':('Roma','https://media.api-sports.io/football/teams/497.png','eu'),'sevilla':('Sevilla','https://media.api-sports.io/football/teams/536.png','eu'),'valencia':('Valencia','https://media.api-sports.io/football/teams/532.png','eu')}
for file,typ in [('brasileiros.html','br'),('europeus.html','eu')]:
 p=base/file; txt=p.read_text(encoding='utf-8'); add=''
 for slug,(nm,logo,t) in cards.items():
  if t==typ and f'href="{slug}.html"' not in txt: add+=f'<a class="team-card" href="{slug}.html"><div class="team-info"><img alt="Escudo {nm}" class="team-crest" src="{logo}"/><h3>{nm}</h3></div></a>'
 if add: txt=txt.replace('</div></div></main>',add+'</div></div></main>',1)
 p.write_text(txt,encoding='utf-8')
# requested crest corrections: use official/current sources rather than old API crest
p=base/'brasileiros.html'; txt=p.read_text(encoding='utf-8')
txt=re.sub(r'(<a class="team-card" href="bragantino\.html">.*?<img[^>]+src=")[^"]+(")',r'\1https://www.redbullbragantino.com/midia_imagens/4d484538b5d74d1e9bbff910d0cad2a4.png\2',txt,flags=re.S)
txt=re.sub(r'(<a class="team-card" href="cruzeiro\.html">.*?<img[^>]+src=")[^"]+(")',r'\1https://commons.wikimedia.org/wiki/Special:Redirect/file/Escudo%20Cruzeiro%20BH.png\2',txt,flags=re.S)
p.write_text(txt,encoding='utf-8')
# remove admin
for p in base.glob('admin*'):
 if p.is_file(): p.unlink()
