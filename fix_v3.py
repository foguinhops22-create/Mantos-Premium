from pathlib import Path
from bs4 import BeautifulSoup
import shutil, re, zipfile, os

root=Path('/mnt/data/v3work')
clubs={
'liverpool':'Liverpool','psg':'PSG','manchester-united':'Manchester United','manchester-city':'Manchester City','real-madrid':'Real Madrid'
}

def pair_images(d):
    files=sorted([p for p in (root/'images'/d).glob('*.webp')])
    fronts=[p for p in files if '-frente' in p.name]
    pairs=[]
    for front in fronts:
        # same basename stem, replacing frente with verso
        verso_name=front.name.replace('-frente','-verso')
        verso=front.with_name(verso_name)
        if not verso.exists():
            # no exact pair; skip
            continue
        pairs.append((front,verso))
    return pairs

for slug, name in clubs.items():
    path=root/f'{slug}.html'
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    grid=soup.select_one('.product-grid')
    if not grid: raise RuntimeError(f'grid missing {path}')
    grid.clear()
    for i,(front,verso) in enumerate(pair_images(slug),1):
        art=soup.new_tag('article', attrs={'class':'product'})
        photo=soup.new_tag('div', attrs={'class':'photo club-carousel', 'data-carousel':f'{slug}-{i-1}'})
        track=soup.new_tag('div', attrs={'class':'carousel-track'})
        for j,p in enumerate((front,verso)):
            img=soup.new_tag('img', attrs={'class':'carousel-slide'+(' is-active' if j==0 else ''), 'src':f'images/{slug}/{p.name}', 'alt':f'{name} - {p.stem}'})
            track.append(img)
        photo.append(track)
        prev=soup.new_tag('button', attrs={'class':'carousel-arrow carousel-prev','type':'button','aria-label':'Ver foto anterior'}); prev.string='‹'
        nxt=soup.new_tag('button', attrs={'class':'carousel-arrow carousel-next','type':'button','aria-label':'Ver próxima foto'}); nxt.string='›'
        dots=soup.new_tag('div', attrs={'class':'carousel-dots','aria-hidden':'true'})
        for j in range(2): dots.append(soup.new_tag('span', attrs={'class':'carousel-dot'+(' is-active' if j==0 else '')}))
        photo.extend([prev,nxt,dots])
        info=soup.new_tag('div', attrs={'class':'info'})
        tag=soup.new_tag('span', attrs={'class':'tag'}); tag.string='CLUBES EUROPEUS'
        h3=soup.new_tag('h3')
        label=front.stem.replace('-frente','').replace('-',' ').title()
        h3.string=f'Camisa {label}'
        p=soup.new_tag('p'); p.string='Camisa Tailandesa'
        strong=soup.new_tag('strong'); strong.string='R$ 129'
        btn=soup.new_tag('button', attrs={'onclick':f"buy('{name} - Camisa {label}')"}); btn.string='Comprar Pelo WhatsApp'
        info.extend([tag,h3,p,strong,btn])
        art.extend([photo,info]); grid.append(art)
    path.write_text(str(soup),encoding='utf-8')

# Replace Bragantino crest URL with the user-provided image saved locally.
crest_src=Path('/mnt/data/a8bf71e7-9501-496e-8557-fcfa35ad7d74.png')
assets=root/'assets'; assets.mkdir(exist_ok=True)
shutil.copy2(crest_src, assets/'bragantino-escudo.png')
bra=root/'brasileiros.html'
text=bra.read_text(encoding='utf-8')
text=text.replace('https://www.redbullbragantino.com/midia_imagens/4d484538b5d74d1e9bbff910d0cad2a4.png','assets/bragantino-escudo.png')
bra.write_text(text,encoding='utf-8')

# Add a short manifest for verification.
manifest=[]
for slug,name in clubs.items(): manifest.append(f'{name}: {len(pair_images(slug))} produtos, {len(pair_images(slug))*2} imagens')
(root/'INTEGRACAO_CAMISAS_V3.txt').write_text('Atualização V3\n'+'\n'.join(manifest)+'\nBragantino: escudo substituído pela imagem fornecida pelo usuário.\n',encoding='utf-8')
