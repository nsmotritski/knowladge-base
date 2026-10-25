#!/usr/bin/env python3
"""Build a dependency-free bilingual static guide; content lives in content/*.json."""
import json, shutil, pathlib, html, argparse
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=pathlib.Path(__file__).resolve().parent
E=html.escape
ids=json.loads((ROOT/'content/order.json').read_text())
assert len(ids)==len(set(ids)), 'Duplicate chapter IDs'
pages=[json.loads((ROOT/'content'/f'{i}.json').read_text()) for i in ids]
assert all(p['id']==i for p,i in zip(pages,ids))
out=ROOT/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir(); shutil.copytree(ROOT/'assets',out/'assets')
labels={'en':['CONTENTS','Chapter','Previous','Next','Sources & scope','Knowledge Base','Independent study notes · v0.1'],'ru':['СОДЕРЖАНИЕ','Глава','Назад','Далее','Источники и границы','База знаний','Независимое пособие · v0.1']}
for lang in labels:
 (out/'anthropic'/lang).mkdir(parents=True)
 for n,p in enumerate(pages):
  d=p[lang]; lab=labels[lang]; other='ru' if lang=='en' else 'en'
  nav=''.join(f'<a href="{q["id"]}.html" class="{"active" if q==p else ""}" {"aria-current=page" if q==p else ""}><span>{k:02}</span>{E(q[lang]["title"])}</a>' for k,q in enumerate(pages,1))
  sections=''.join(f'<section><h2>{E(h)}</h2><p>{E(b)}</p></section>' for h,b in d['sections'])
  diagrams=''.join(f'<figure class="illustration detail-diagram"><figcaption class="figuretitle">{E(g["title"])}</figcaption><a href="../../assets/diagrams/{E(g["file"],quote=True)}" target="_blank" rel="noopener"><img src="../../assets/diagrams/{E(g["file"],quote=True)}" alt="{E(g["caption"],quote=True)}" width="1000" height="850"></a><p class="caption">{E(g["caption"])}</p></figure>' for g in d.get('diagrams',[]))
  flow='<span class="arrow" aria-hidden="true">→</span>'.join(f'<div class="flowbox">{E(x)}</div>' for x in d['flow'])
  sources='''<a href="https://www.anthropic.com/engineering/multi-agent-research-system">Anthropic · How we built our multi-agent research system</a><br><a href="https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them">Anthropic · When to use multi-agent systems</a>'''
  pager=''
  for k,label in [(n-1,lab[2]),(n+1,lab[3])]:
   if 0<=k<len(pages):
    q=pages[k];pager+=f'<a href="{q["id"]}.html"><small>{label}</small>{E(q[lang]["title"])}</a>'
  content=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(d['lead'],quote=True)}"><title>{E(d['title'])} · Cloud Architect Field Guide</title><link rel="stylesheet" href="../../assets/style.css"><script src="../../assets/app.js" defer></script></head><body><a class="skip" href="#main">{'Skip to content' if lang=='en' else 'К содержанию'}</a><aside id="sidebar"><a class="brand" href="../../catalog.html"><span class="logo">kb<span>↗</span></span><strong>Knowledge Base<small>CLOUD ARCHITECT</small></strong></a><div class="edition">Foundations · EN / RU</div><label class="navlabel" for="search">{lab[0]}</label><input id="search" type="search" placeholder="{'Find a topic' if lang=='en' else 'Найти тему'}" aria-label="{'Find a topic' if lang=='en' else 'Найти тему'}"><nav>{nav}</nav><div class="asidebottom"><span class="dot"></span>{lab[6]}<p>{'Study, connect, revisit.' if lang=='en' else 'Изучайте, связывайте, повторяйте.'}</p></div></aside><div class="shell"><header><button id="menu" aria-controls="sidebar" aria-expanded="false" aria-label="{'Toggle contents' if lang=='en' else 'Открыть оглавление'}">☰</button><div>{lab[5]} / Anthropic / {n+1:02}</div><div class="languages"><a class="active" aria-current="true" href="{p['id']}.html">{lang.upper()}</a><a href="../{other}/{p['id']}.html" lang="{other}">{other.upper()}</a></div></header><main id="main"><div class="eyebrow"><span>{lab[1]} {n+1:02} / {len(pages):02}</span><span class="tag">ARCHITECTURE</span></div><h1>{E(d['heading'])}</h1><p class="lead">{E(d['lead'])}</p><figure class="illustration"><figcaption class="figuretitle">{'THE PATTERN' if lang=='en' else 'СХЕМА'}</figcaption><div class="flow">{flow}</div></figure>{diagrams}{sections}<details class="further"><summary>{'Practice' if lang=='en' else 'Проверьте себя'}</summary><p>{'What input is missing? Who owns the next action? What evidence must survive? Explain the failure before choosing a component.' if lang=='en' else 'Какого входа не хватает? Кто отвечает за следующий шаг? Какие доказательства нужно сохранить? Объясните причину ошибки до выбора компонента.'}</p></details><section class="source"><h2>{lab[4]}</h2>{sources}<p>{'Independent learning guide · Reviewed 25 October 2026.' if lang=='en' else 'Независимое учебное пособие · Проверено 25 октября 2026.'}</p></section><div class="pager">{pager}</div></main><footer><span>CLOUD ARCHITECT / FIELD NOTES</span><span>{n+1:02} — {len(pages):02}</span></footer></div></body></html>'''
  (out/'anthropic'/lang/f'{p["id"]}.html').write_text(content)
(out/'catalog.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Knowledge Base</title><link rel="stylesheet" href="assets/style.css"></head><body><main><div class="eyebrow">KNOWLEDGE BASE · FIELD GUIDES</div><h1>A place to<br><em>connect ideas.</em></h1><p class="lead">Расширяемый каталог знаний / An expanding collection of learning guides.</p><article class="illustration"><h2>Cloud Architect</h2><p>Agents, context, tools & evidence · Агенты, контекст, инструменты и доказательства</p><a href="anthropic/en/overview.html">Read in English →</a> · <a href="anthropic/ru/overview.html">Читать по-русски →</a></article></main></body></html>''')
# Relative redirect works at both localhost / and GitHub Pages /knowladge-base/.
(out/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=anthropic/en/overview.html"><title>Cloud Architect · Knowledge Base</title></head><body><p><a href="anthropic/en/overview.html">Continue to the English guide →</a></p><p><a href="anthropic/ru/overview.html" lang="ru">Читать по-русски</a> · <a href="catalog.html">Knowledge Base catalog</a></p></body></html>''')
(out/'.nojekyll').touch()
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,val in attrs:
   if key in ('href','src') and val and not urlsplit(val).scheme and not val.startswith('#'):
    target=(self.file.parent/unquote(urlsplit(val).path)).resolve()
    assert target.is_relative_to(out.resolve()) and target.is_file(), f'Broken local link: {self.file}: {val}'
for f in out.rglob('*.html'):
 parser=Links();parser.file=f;parser.feed(f.read_text())
print(f'Built {len(list(out.rglob("*.html")))} HTML pages; all local links and assets verified.')
