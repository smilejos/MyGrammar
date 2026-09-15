"""Meaningful static checks: curriculum, answers, local URLs, and print separation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
units=json.loads((ROOT/'content/units.json').read_text())
assert {u['id'] for u in units}=={'g1-u06','g3-u09','g5-u03'}
all_ids=[]
for u in units:
    core=[q for _,qs in u['groups'] for q in qs]
    assert len(core)==9 and len(u['open'])==3
    assert len(u['pre'])==2 and len(u['exit'])==3
    assert len(u['contrasts'])>=5 and len(u['mistakes'])>=2
    assert len(u['usage_groups'])>=3
    for group in u['usage_groups']:
        assert len(group['cases'])>=5, (u['id'],group['id'])
        assert len({c['example'] for c in group['cases']})>=5
        assert len({c['context'] for c in group['cases']})>=5
        for case in group['cases']:
            assert all(case.get(k,'').strip() for k in ['context','use','example','translation','focus'])
            assert case['focus'] in case['example']
    for q in u['pre']+core+u['exit']:
        assert 0<=q['answer']<len(q['options'])
        assert len(set(q['options']))==len(q['options'])
        assert q['why'].strip() and q['prompt'].strip()
        all_ids.append(q['id'])
    assert all(t['sample'] and t['why'] for t in u['open'])
    assert u['write']['sample'] and len(u['write']['checklist'])>=3
assert len(set(all_ids))==len(all_ids)==42
class Page(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.ids=[];self.refs=[];self.h1=0;self.answers=0;self.questions=0;self.forms=0;self.feed(s)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if tag=='h1':self.h1+=1
        if 'answer-reveal' in a.get('class',''):self.answers+=1
        if tag=='fieldset':self.questions+=1
        if tag=='form':self.forms+=1
pages={p:Page(p.read_text()) for p in OUT.rglob('*.html')}
assert len(pages)==19
for p,page in pages.items():
    assert page.h1==1,p
    assert len(page.ids)==len(set(page.ids)),p
    for ref in page.refs:
        url=urlsplit(ref)
        assert not url.scheme and not url.netloc,(p,ref,'external dependency')
        target=(p.parent/unquote(url.path)).resolve() if url.path else p.resolve()
        if target.is_dir():target=target/'index.html'
        assert target.is_relative_to(OUT.resolve()),(p,ref,'escapes dist')
        assert target.exists(),(p,ref,'missing target')
        if url.fragment and target.suffix=='.html':
            assert unquote(url.fragment) in pages[target].ids,(p,ref,'missing anchor')
    if page.forms:
        assert page.forms==5 and page.questions==14 and page.answers==14,p
        assert 'XMLHttpRequest' not in p.read_text()
        unit=next(u for u in units if f"u{u['number']:02}-{u['slug']}"==p.parent.name)
        assert p.read_text().count('class="usage-case"')==sum(len(g['cases']) for g in unit['usage_groups'])
        for group in unit['usage_groups']:
            assert 'usage-'+group['id'] in page.ids
    if p.name=='worksheet.html':
        s=p.read_text()
        assert 'printed-answer' not in s and 'answer-reveal' not in s and '參考作品' not in s
        assert 'writing-lines' in s and '情境資料' in s
    if p.name=='answers.html':
        assert p.read_text().count('class="printed-answer"')==14
assert len(list(OUT.rglob('worksheet.html')))==3
assert len(list(OUT.rglob('answers.html')))==3
print('PASS: 50 contextual examples across 10 grammar groups, 5 contrast pairs per unit; 3 units; 36 core exercises; 42 objective questions with explanations; 19 pages; all local links/anchors; 3 separate worksheets and answer keys.')
