"""Meaningful static checks: curriculum, answers, local URLs, and print separation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json, re, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from build import route, highlighted_example
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
units=json.loads((ROOT/'content/units.json').read_text())
expected={f'g{g}-u{n:02}' for g in [1,2,3] for n in range(1,13)}|{'g5-u03'}
assert {u['id'] for u in units}==expected
assert len(units)==len(expected)
by_id={u['id']:u for u in units}
curriculum=json.loads((ROOT/'content/curriculum.json').read_text())
assert [g['grade'] for g in curriculum]==[1,2,3]
for grade in curriculum:
    assert [t['term'] for t in grade['terms']]==[1,2]
    for term in grade['terms']:
        start=1 if term['term']==1 else 7
        assert term['units']==[f'g{grade["grade"]}-u{n:02}' for n in range(start,start+6)]
        assert len(term['review'])==6
        assert term['project']==by_id[term['units'][-1]]['write']
        assert len({q['source'] for q in term['review']})>=3
        for q in term['review']:
            assert q['source'] in term['units']
            assert any(all(q[k]==source[k] for k in ['prompt','options','answer','why']) for source in by_id[q['source']]['exit']), q['id']
            assert 0<=q['answer']<len(q['options']) and q['why'].strip()
for u in units:
    assert u['term']==(1 if u['number']<=6 else 2)
    assert u['id']==f'g{u["grade"]}-u{u["number"]:02}'
    for prior in u.get('prerequisites',[]):
        assert prior in by_id
        p=by_id[prior]
        assert (p['grade'],p['number'])<(u['grade'],u['number']), (u['id'],prior)
# Keep previously published lesson URLs stable.
assert route(by_id['g1-u06'])=='grades/g1/term-1/u06-be-verbs/index.html'
assert route(by_id['g3-u09'])=='grades/g3/term-2/u09-comparatives/index.html'
assert route(by_id['g5-u03'])=='grades/g5/term-1/u03-present-perfect/index.html'
assert highlighted_example({'example':'This is red.','focus':'is'})=='This <strong class="grammar-highlight">is</strong> red.'
all_ids=[]
for u in units:
    core=[q for _,qs in u['groups'] for q in qs]
    assert len(core)==9 and len(u['open'])==3
    assert len(u['pre'])==2 and len(u['exit'])==3
    assert len(u['contrasts'])>=5 and len(u['mistakes'])>=2
    assert len(u['usage_groups'])>=2
    assert len({g['id'] for g in u['usage_groups']})==len(u['usage_groups'])
    for group in u['usage_groups']:
        assert len(group['cases'])>=5, (u['id'],group['id'])
        assert len({c['example'] for c in group['cases']})>=5
        assert len({c['context'] for c in group['cases']})>=5
        for case in group['cases']:
            assert all(case.get(k,'').strip() for k in ['context','use','example','translation','focus'])
            assert case['focus'] in case['example']
            assert 'grammar-highlight' in highlighted_example(case)
    for q in u['pre']+core+u['exit']:
        assert 0<=q['answer']<len(q['options'])
        assert len(set(q['options']))==len(q['options'])
        assert q['why'].strip() and q['prompt'].strip()
        all_ids.append(q['id'])
    assert all(t['sample'] and t['why'] for t in u['open'])
    assert u['write']['sample'] and len(u['write']['checklist'])>=3
assert len(set(all_ids))==len(all_ids)==14*len(units)
review_ids=[q['id'] for g in curriculum for t in g['terms'] for q in t['review']]
assert len(set(all_ids+review_ids))==len(all_ids)+36
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
assert len(pages)==10+3*len(units)+6
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
    if p.name=='review.html':
        assert page.forms==2 and page.questions==6 and page.answers==6,p
    elif page.forms:
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
assert len(list(OUT.rglob('worksheet.html')))==len(units)
assert len(list(OUT.rglob('answers.html')))==len(units)
# Every lesson must be reachable from its grade page, with sequential navigation.
for u in units:
    path=OUT/route(u)
    grade_page=OUT/f'grades/g{u["grade"]}/index.html'
    resolved={(grade_page.parent/urlsplit(r).path).resolve() for r in pages[grade_page].refs if urlsplit(r).path}
    assert path.resolve() in resolved,u['id']
    if u['grade']<=3:
        text=path.read_text()
        assert '單元前後導覽' in text
        if u['number']<12:assert f'下一課 U{u["number"]+1:02}' in text
        if u['number']>1:assert f'上一課 U{u["number"]-1:02}' in text
assert (OUT/'curriculum/grade-1-3.md').read_text().count('##### G')==36
assert not any(term in (OUT/'index.html').read_text() for term in ['3 個單元開放試用','回到三個示範'])
examples=sum(len(g['cases']) for u in units for g in u['usage_groups'])
print(f'PASS: G1–G3 36 units + G5 demo; {examples} contextual examples; {len(all_ids)} lesson questions + 36 term review questions; {len(pages)} pages; prerequisites/order/navigation; all links/anchors; {len(units)} worksheets and separate answer keys.')
