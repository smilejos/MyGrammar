"""Build dependency-free, GitHub Pages-compatible teaching pages."""
from pathlib import Path
from html import escape as esc
import json, shutil, os, hashlib, re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
UNITS=json.loads((ROOT/'content/units.json').read_text())
CURRICULUM=json.loads((ROOT/'content/curriculum.json').read_text())
BY_ID={u['id']:u for u in UNITS}
DISCLAIMER='本課程為自主編排。G1–G2 參考使用者提供的教材目錄；G3–G6 為延伸設計，非康橋或 MyGrammar 官方課綱。'

def e(x): return esc(str(x),quote=True)
def href(current,target): return os.path.relpath(target,Path(current).parent).replace(os.sep,'/')
def route(u): return f'grades/g{u["grade"]}/term-{u["term"]}/u{u["number"]:02}-{u["slug"]}/index.html'
def asset(path,name):
    digest=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()[:10]
    return href(path,name)+"?v="+digest

def sibling(u,name): return str(Path(route(u)).with_name(name))
def link(path,target,label,cls=''): return f'<a class="{cls}" href="{href(path,target)}">{label}</a>'
def write(path,html):
    dest=OUT/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(html)
def header(path,active=''):
    return f'''<a class="skip" href="#main">跳到主要內容</a><header class="site-header"><div class="header-inner">
    {link(path,'index.html','<span class="brand-mark" aria-hidden="true">g.</span><span>Grammar Journey<small>英文文法學習室</small></span>','brand')}
    <nav aria-label="主要導覽">{link(path,'index.html','開始學習','nav-link '+('active' if active=='home' else ''))}{link(path,'curriculum/index.html','六年課程地圖','nav-link '+('active' if active=='map' else ''))}{link(path,'guide/index.html','使用指南','nav-link '+('active' if active=='guide' else ''))}</nav>
    <span class="preview-label">G1–G3 課程</span></div></header>'''
def shell(path,title,body,active='',color='blue',printpage=False,description='Grade 1–3 共 36 個英文文法單元，含情境例句、互動練習、寫作與可列印學習單。'):
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · Grammar Journey</title><meta name="description" content="{e(description)}"><meta name="robots" content="noindex,follow"><link rel="icon" type="image/svg+xml" href="{href(path,'assets/favicon.svg')}"><link rel="stylesheet" href="{asset(path,'assets/style.css')}"><link rel="stylesheet" media="print" href="{asset(path,'assets/print.css')}"><script defer src="{asset(path,'assets/app.js')}"></script></head><body class="theme-{color}{' print-page' if printpage else ''}">{header(path,active)}{body}<footer class="site-footer"><div><span class="footer-brand">Grammar Journey</span><p>{DISCLAIMER}</p><p class="fine">教材 v1.0 · 2026.09　<span>G1–G3 共 36 課已開放；G5 保留 1 課示範。自主編寫教材待教師審閱。</span></p></div>{link(path,'guide/index.html#privacy','資料與隱私說明')}</footer></body></html>'''
def crumb(path,items):
    parts=[link(path,'index.html','首頁')]
    for target,label in items:
        item=link(path,target,e(label)) if target else '<span aria-current="page">'+e(label)+'</span>'
        parts.append('<span aria-hidden="true">/</span>'+item)
    return '<nav class="breadcrumbs" aria-label="麵包屑">'+''.join(parts)+'</nav>'
def art(u):
    if u['id']=='g1-u06':
        return '<div class="sentence-art"><span>I</span><strong>am</strong><span>happy.</span><div class="art-caption">主詞 <span>＋</span> be <span>＋</span> 感受</div></div>'
    if u['id']=='g3-u09':
        return '<div class="comparison-art"><div><span>Bag A</span><strong>1 <small>kg</small></strong><i style="width:33%"></i></div><div><span>Bag B</span><strong>3 <small>kg</small></strong><i></i></div><p>lighter <span>↔</span> heavier</p></div>'
    if u['id']!='g5-u03':
        return f'<div class="lesson-card-art"><span>GRAMMAR IN CONTEXT</span><p lang="en">{e(u["usage_groups"][0]["cases"][0]["example"])}</p></div>'
    return '<div class="time-art"><div><span>THEN · 過去</span><span>NOW · 現在</span></div><div class="time-line"></div><strong>I have lived here</strong><p>since 2022.</p></div>'
def cards(path,units=UNITS):
    out='<div class="course-grid">'
    for u in units:
        out+=f'''<article class="course-card theme-{u['color']}"><div class="card-top"><span class="grade-label">GRADE {u['grade']}</span><span class="unit-label">UNIT {u['number']:02}</span></div>{art(u)}<div class="card-content"><p class="eyebrow">{u['tag']}</p><h2>{e(u['topic'])}</h2><p>{u['short']}</p><div class="card-meta"><span>4 個學習小節</span><span>練習＋寫作</span></div>{link(path,route(u),'進入單元 <span aria-hidden="true">↗</span>','button full')}</div></article>'''
    return out+'</div>'
def grade_cards(path):
    subtitles={1:('從詞語到完整句','名詞、代名詞、be、形容詞、位置與四種句型。'),2:('把日常與時間說清楚','複數、受格、現在式、過去式與未來計畫。'),3:('把句子寫得更豐富','所有格、進行式、副詞、比較與句子連接。')}
    output='<div class="course-grid">'
    for g,(title,desc) in subtitles.items():
        output+=f'<article class="grade-card theme-{ {1:"blue",2:"violet",3:"teal"}[g]}"><p class="eyebrow">GRADE {g}</p><h2>{title}</h2><p>{desc}</p><p class="fine">2 個 Term · 12 個 Unit · 2 次學期複習</p>{link(path,f"grades/g{g}/index.html","查看課程與開始學習 →","button full")}</article>'
    return output+'</div>'
def home():
    path='index.html'
    body=f'''<main id="main" tabindex="-1" class="home-main"><section class="home-heading"><div><p class="eyebrow">LEARN IT. USE IT.</p><h1>從一句話開始，<br>一步一步學會表達。</h1><p class="intro">Grade 1–3 的 36 個完整單元，循序閱讀、練習，再寫出自己的句子。</p></div><div class="edition"><strong>36</strong><span>課程單元<br>開放學習</span></div></section>{grade_cards(path)}<section class="learning-strip" aria-labelledby="flow-title"><div><p class="eyebrow">YOUR LEARNING PATH</p><h2 id="flow-title">每一課，都有一個小進步。</h2></div><ol><li><b>01</b>看例子</li><li><b>02</b>懂用法</li><li><b>03</b>試一試</li><li><b>04</b>寫出來</li></ol></section><section class="featured-lessons"><h2>也可以從熟悉的主題開始</h2><p>每個教學重點至少五個情境例句；先做暖身，確認先備能力。</p>{cards(path,[BY_ID['g1-u06'],BY_ID['g2-u06'],BY_ID['g3-u09']])}</section><section class="home-bottom"><div><h2>看見整條學習路線</h2><p>G1–G3 已完成；G4–G6 保留規劃方向與 G5 示範課。</p>{link(path,'curriculum/index.html','查看六年課程地圖 →','text-link')}</div><div><h2>一起陪孩子學習</h2><p>每課附解析、寫作判準與可列印學習單。</p>{link(path,'guide/index.html','閱讀家長與教師指南 →','text-link')}</div></section></main>'''
    write(path,shell(path,'Grade 1–3 英文文法課程',body,'home'))

def prerequisite_links(path,u):
    ids=u.get('prerequisites',[])
    if not ids:return '<p class="fine">起步單元：可先由成人朗讀，口頭回答。</p>' if u['grade']==1 else ''
    return '<div class="prerequisite-links"><b>先備與複習：</b>'+ '、'.join(link(path,route(BY_ID[i]),e(i.upper()+' '+BY_ID[i]['topic'])) for i in ids)+'</div>'
def course_navigation(path,u):
    peers=sorted([x for x in UNITS if x['grade']==u['grade']],key=lambda x:x['number'])
    pos=peers.index(u)
    links=[]
    if pos:links.append(link(path,route(peers[pos-1]),f'← 上一課 U{peers[pos-1]["number"]:02}'))
    links.append(link(path,f'grades/g{u["grade"]}/index.html','年級課程目錄'))
    if u['grade']<=3 and u['number'] in [6,12]:
        links.append(link(path,f'grades/g{u["grade"]}/term-{u["term"]}/review.html','學期複習與作品檢核 →'))
    if pos+1<len(peers):links.append(link(path,route(peers[pos+1]),f'下一課 U{peers[pos+1]["number"]:02} →'))
    elif u['grade'] in [1,2]:links.append(link(path,f'grades/g{u["grade"]+1}/index.html',f'前往 Grade {u["grade"]+1} →'))
    return '<nav class="course-navigation" aria-label="單元前後導覽">'+' '.join(links)+'</nav>'

def option_label(text):
    return f'<span lang="en">{e(text)}</span>' if text.isascii() else f'<span>{e(text)}</span>'

def question_block(q,i):
    return f'''<fieldset class="question" data-answer="{q['answer']}"><legend><span class="q-number">{i:02}</span> {e(q['prompt'])}</legend><div class="options">'''+''.join(f'<label class="option"><input type="radio" name="{q["id"]}" value="{j}">{option_label(opt)}</label>' for j,opt in enumerate(q['options']))+f'''</div><p class="feedback" hidden data-feedback></p><details class="answer-reveal"><summary>查看答案與原因</summary><p><strong>答案：{e(q['options'][q['answer']])}</strong></p><p class="why">{e(q['why'])}</p></details></fieldset>'''
def quiz(qs,name,start=1):
    return f'<form class="quiz" data-quiz="{e(name)}"><div class="question-list">'+''.join(question_block(q,i) for i,q in enumerate(qs,start))+f'''</div><div class="quiz-actions js-only" hidden><button type="submit" class="button">檢查答案</button><button type="reset" class="button secondary">重新練習</button><p class="quiz-result" role="status" aria-live="polite"></p></div></form>'''
def open_tasks(u):
    return '<div class="open-tasks">'+''.join(f'''<article class="open-task"><p><span class="q-number">{i+10:02}</span> {e(t['prompt'])}</p><details><summary>對照參考答案</summary><p lang="en" class="english">{e(t['sample'])}</p><p>{e(t['why'])}</p></details></article>''' for i,t in enumerate(u['open']))+'</div>'
def section_head(n,k,title): return f'<header class="section-heading"><span class="step-num">{n}</span><div><p class="eyebrow">{k}</p><h2>{title}</h2></div></header>'
def highlighted_example(case):
    # Match a complete form: highlighting "is" must not mark the end of "This".
    pattern=(r'(?<!\w)' if case['focus'][0].isalnum() else '')+re.escape(case['focus'])+(r'(?!\w)' if case['focus'][-1].isalnum() else '')
    match=re.search(pattern,case['example'])
    if not match: raise ValueError(f"Target form not found: {case}")
    return e(case['example'][:match.start()])+f'<strong class="grammar-highlight">{e(match.group())}</strong>'+e(case['example'][match.end():])

def usage_library(u):
    nav='<nav class="usage-nav" aria-label="例句與用法分組">'+''.join(
        f'<a href="#usage-{e(g["id"])}">{e(g["title"].split("：")[0])} <span>{len(g["cases"])} 組</span></a>'
        for g in u['usage_groups'])+'</nav>'
    groups=''
    for group in u['usage_groups']:
        cases=''.join(
            f'<li class="usage-case"><div class="usage-case-label"><span class="usage-number">{i:02}</span><h5>{e(case["context"])}</h5></div>'
            f'<p class="usage-when"><b>什麼時候用？</b>{e(case["use"])}</p>'
            f'<p class="usage-example" lang="en">{highlighted_example(case)}</p>'
            f'<p class="usage-translation">{e(case["translation"])}</p></li>'
            for i,case in enumerate(group['cases'],1))
        groups+=f'<section class="usage-group" id="usage-{e(group["id"])}" aria-labelledby="usage-title-{e(group["id"])}">'
        groups+=f'<header><h4 id="usage-title-{e(group["id"])}">{e(group["title"])}</h4><span class="pill">{len(group["cases"])} 個例句 · {len(group["cases"])} 種情境</span></header>'
        groups+=f'<p class="usage-form">{e(group["form"])}</p><p class="usage-note">{e(group["note"])}</p><ol class="usage-list">{cases}</ol></section>'
    return f'<div class="usage-library"><h3>從五種情境，看懂每一種文法</h3><p class="muted">{e(u["usage_intro"])}</p>{nav}{groups}</div>'

def lesson(u):
    path=route(u); write_task=u['write']
    toc=[('start','開始前','暖身與學習目標'),('notice','01 看例子','觀察情境'),('understand','02 懂用法','情境、例句與對照'),('practice','03 試一試','練習與回饋'),('write','04 寫出來','完成小作品'),('check','帶走一個進步','課末檢核')]
    pre=f'''<section id="start" class="lesson-section"><div class="section-topline"><h2>這一課，我可以…</h2><span class="pill">核心學習</span></div><ul class="goals">{''.join(f'<li>{e(g)}</li>' for g in u['goals'])}</ul>{prerequisite_links(path,u)}<details class="support"><summary>先備小補充 · 展開快速回顧</summary><p>{u['prereq_text']}</p>{''.join(f'<h3>{e(t)}</h3><p>{e(d)}</p>' for t,d in u['support'])}</details><h3>先暖身，不計分</h3>{quiz(u['pre'],'先備暖身')}</section>'''
    scene=f'''<section id="notice" class="lesson-section">{section_head('01','NOTICE',u['scene_title'])}<p>{u['scene_intro']}</p><div class="scene {'data-scene' if u['grade']==3 else ''}">{''.join(f'<div class="scene-line"><span class="speaker">{e(who)}</span><p lang="en">{e(line)}</p></div>' for who,line in u['scene'])}</div><div class="notice-questions">{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in u['notice'])}</div><details class="vocab"><summary>本課小字典</summary><dl>{''.join(f'<div><dt lang="en">{e(w)}</dt><dd>{e(d)}</dd></div>' for w,d in u['vocab'])}</dl></details></section>'''
    rules=f'''<section id="understand" class="lesson-section">{section_head('02','UNDERSTAND','抓住用法，就能舉一反三')}<div class="rules">{''.join(f'<article class="rule"><span>{n}</span><div><h3>{e(t)}</h3><p>{e(d)}</p><p class="rule-example" lang="en">{e(ex)}</p></div></article>' for n,t,d,ex in u['rules'])}</div>{usage_library(u)}<h3>五組對照，看看差在哪裡</h3>{''.join(f'<div class="contrast"><p lang="en">{e(a)}</p><p lang="en">{e(b)}</p><p>{e(d)}</p></div>' for a,b,d in u['contrasts'])}<h3>容易卡住的地方</h3>{''.join(f'<div class="mistake"><p><span class="error-label">需修改</span><span lang="en">{e(a)}</span></p><p><span class="correct-label">修改後</span><span lang="en">{e(b)}</span></p><p>{e(d)}</p></div>' for a,b,d in u['mistakes'])}</section>'''
    practice=f'''<section id="practice" class="lesson-section">{section_head('03','PRACTICE','換你試一試')}<p>先自己想，再檢查答案。答錯時，讀一讀原因後再試一次。</p><noscript><p class="note">互動檢查未啟用。你仍可逐題展開答案，或使用列印學習單。</p></noscript>{''.join(f'<h3 class="practice-heading">{i+1}. {e(name)}</h3>{quiz(qs,name,i*3+1)}' for i,(name,qs) in enumerate(u['groups']))}<h3 class="practice-heading">4. 改一改，自己寫一句</h3><p class="muted">請在紙上或自己的筆記中作答。這三題使用參考答案自評。</p>{open_tasks(u)}</section>'''
    writing=f'''<section id="write" class="lesson-section">{section_head('04','WRITE',write_task['title'])}<p>{e(write_task['prompt'])}</p><div class="writing-paper"><p class="eyebrow">START WITH A SENTENCE</p>{''.join(f'<p lang="en">{e(x)}</p>' for x in write_task['frames'])}<p class="paper-note">寫在紙上，或列印這份學習單。</p></div><details class="sample"><summary>寫完後，再看一份示例</summary><p lang="en" class="english">{e(write_task['sample'])}</p><p>這是其中一種寫法。你的內容可以不同。</p></details><h3>讀一遍，幫自己檢查</h3><div class="checklist">{''.join(f'<label><input type="checkbox"><span>{e(c)}</span></label>' for c in write_task['checklist'])}</div><p class="fine">勾選只供這次閱讀使用，不會儲存。</p><p class="note">{e(write_task['rubric'])}</p></section>'''
    end=f'''<section id="check" class="lesson-section">{section_head('✓','QUICK CHECK','把今天學的，帶到新句子裡')}<p>用三題看看自己哪些地方已經熟悉。這是學習提示，不是程度認證。</p>{quiz(u['exit'],'課末檢核')}<div class="next-note"><h3>還不確定？這樣複習</h3><p>主詞或基本形式卡住，回到<a href="#start">先備小補充</a>；選擇意思時猶豫，回看<a href="#notice">情境</a>；形式不穩定，再看<a href="#understand">用法與錯誤對照</a>。</p><p>{e(u['next_note'])}</p>{course_navigation(path,u)}</div></section><section class="lesson-section adult-section"><details><summary>給家長與教師的教學提示</summary><p>{e(u['adult'])}</p><p>建議分四個 35–40 分鐘時段教學；家庭學習可拆成 10–20 分鐘，依孩子實際需要調整。先備與課末題不列入本課 12 道核心練習。</p><p>{e(u['origin'])}。教材待教師審閱。</p></details></section>'''
    body=f'''<main id="main" tabindex="-1" class="lesson-main">{crumb(path,[(f'grades/g{u["grade"]}/index.html',f'Grade {u["grade"]}'),(None,f'Unit {u["number"]:02}')])}<div class="lesson-layout"><aside class="lesson-sidebar"><div class="side-title"><span class="grade-label">GRADE {u['grade']}</span><p>Term {u['term']} · Unit {u['number']:02}</p><h2>{e(u['topic'])}</h2></div><nav aria-label="本課目錄">{''.join(f'<a href="#{a}"><b>{b}</b><small>{c}</small></a>' for a,b,c in toc)}</nav><div class="sidebar-resources">{link(path,sibling(u,'worksheet.html'),'列印學習單 ↗')}{link(path,sibling(u,'answers.html'),'答案與解析 ↗')}</div></aside><div class="lesson-content"><header class="lesson-hero"><p class="eyebrow">{e(u['en'])}</p><h1>{e(u['title'])}</h1><div class="lesson-meta"><span>4 個學習小節</span><span>12 道核心練習</span><span>1 個寫作任務</span></div><a href="#notice" class="button">開始看例子 <span aria-hidden="true">↓</span></a></header>{pre}{scene}{rules}{practice}{writing}{end}</div></div></main>'''
    write(path,shell(path,f'G{u["grade"]} U{u["number"]:02} {u["topic"]}',body,color=u['color'],description=u['short']))

def printable(u,answers=False):
    path=sibling(u,'answers.html' if answers else 'worksheet.html')
    allgroups=[('先備暖身',u['pre'],1)]+[(name,qs,i*3+1) for i,(name,qs) in enumerate(u['groups'])]+[('課末檢核',u['exit'],1)]
    content=''
    deferred=''
    for name,qs,start in allgroups:
        begin=len(content)
        content+=f'<section class="print-section"><h2>{e(name)}</h2>'
        for i,q in enumerate(qs,start):
            content+=f'<div class="print-question"><p><b>{i}. {e(q["prompt"])}</b></p><p>'+('　'.join(f'{chr(65+j)}. {e(v)}' for j,v in enumerate(q['options'])))+'</p>'
            if answers: content+=f'<p class="printed-answer">答案：{chr(65+q["answer"])}. {e(q["options"][q["answer"]])}</p><p>{e(q["why"])}</p>'
            else: content+='<p class="answer-line">答案：____________</p>'
            content+='</div>'
        content+='</section>'
        if name=='課末檢核':
            deferred=content[begin:]
            content=content[:begin]
    content+='<section class="print-section"><h2>改一改，自己寫一句</h2>'
    for i,t in enumerate(u['open'],10):
        content+=f'<div class="print-question"><p><b>{i}. {e(t["prompt"])}</b></p>'+(f'<p lang="en">{e(t["sample"])}</p><p>{e(t["why"])}</p>' if answers else '<div class="writing-lines short-lines"></div>')+'</div>'
    content+='</section>'
    wt=u['write']
    content+=f'<section class="print-section"><h2>Writing · {e(wt["title"])}</h2><p>{e(wt["prompt"])}</p><p lang="en">'+ '<br>'.join(e(f) for f in wt['frames'])+'</p>'
    content+=(f'<h3>參考作品</h3><p lang="en">{e(wt["sample"])}</p><p>{e(wt["rubric"])}</p>' if answers else '<div class="writing-lines"></div>')
    content+='<ul>'+''.join(f'<li>□ {e(c)}</li>' for c in wt['checklist'])+'</ul></section>'
    content+=deferred
    body=f'''<main id="main" tabindex="-1" class="print-main"><div class="print-toolbar">{link(path,route(u),'← 回到教學單元')}<button class="button js-only" hidden data-print>列印 / 另存 PDF</button></div><header class="print-heading"><p>GRAMMAR JOURNEY · G{u['grade']} / T{u['term']} / U{u['number']:02} · v1.0</p><h1>{e(u['topic'])}</h1><h2>{'答案與教學參考' if answers else '學生學習單'}</h2>{'' if answers else '<p>姓名：________________　日期：________________</p>'}<p>{'開放題的示例並非唯一答案，請依判準給予回饋。' if answers else '不需要電腦也能練習。可用瀏覽器的列印功能直接列印。'}</p></header><section class="print-section"><h2>情境資料</h2><p>{e(u['scene_intro'])}</p>{''.join(f'<p><b>{e(w)}</b> <span lang="en">{e(s)}</span></p>' for w,s in u['scene'])}</section>{content}</main>'''
    write(path,shell(path,u['topic']+(' 答案' if answers else ' 學習單'),body,color=u['color'],printpage=True))

def term_outline(path,data):
    text=f'<section class="term-outline" id="term-{data["term"]}"><p class="eyebrow">TERM {data["term"]}</p><h2>{e(data["title"])}</h2><ol class="unit-list">'
    for uid in data['units']:
        u=BY_ID[uid]
        text+=f'<li><span class="unit-index">U{u["number"]:02}</span><div><h3>{link(path,route(u),e(u["title"]))}</h3><p class="unit-topic" lang="en">{e(u["topic"])}</p><p>{e(u["goals"][-1])}</p><details><summary>學習重點、句型與先備</summary><ul>'+''.join(f'<li>{e(g)}</li>' for g in u['goals'])+f'</ul><p lang="en">{e(u["usage_groups"][0]["cases"][0]["example"])}</p>{prerequisite_links(path,u)}</details></div>{link(path,route(u),"開始學習 →","button secondary")}</li>'
    first=BY_ID[data['units'][0]]
    review_path=f"grades/g{first['grade']}/term-{data['term']}/review.html"
    return text+f'</ol><div class="term-review-link"><h3>把這六課連起來</h3><p>六道跨課檢核＋一份寫作作品。答錯可以直接回到對應單元，再練一次。</p>{link(path,review_path,"進入學期複習 →","button")}</div></section>'
def overview(grade=None):
    labels={1:('Words → Sentences','開始寫完整句子','名詞、代名詞、be 與動作動詞、描述與基本句型。'),2:('Sentences → Time','說清楚日常與過去','名詞系統、現在式問句與否定、過去式、未來計畫。'),3:('Expand & Connect','把句子寫得更豐富','所有格、進行式、副詞、比較級與最高級、句子連接與提問。'),4:('Time & Clauses','連起事件與原因','過去進行式深化、情態、原因與時間子句。'),5:('Precision & Perspective','表達經驗與細節','現在完成式、被動語態、關係子句與段落連貫。'),6:('Grammar for Writing','讓段落更清楚','整合時態、句型變化、指代與寫作修訂。')}
    path=f'grades/g{grade}/index.html' if grade else 'curriculum/index.html'
    if grade:
        en,title,desc=labels[grade]
        inner=f'<p class="eyebrow">GRADE {grade} · {en}</p><h1>{title}</h1><p class="intro">{desc}</p>'
        if grade<=3:
            data=next(x for x in CURRICULUM if x['grade']==grade)
            inner+='<p class="note">全年 12 個 Unit，分為兩個 Term。每課分四個學習小節；建議每 Term 用 12–15 週完成單元，另留 3–5 週複習與寫作回饋，可依先備能力調整。</p><nav class="term-tabs" aria-label="學期導覽"><a href="#term-1">Term 1 · U01–U06</a><a href="#term-2">Term 2 · U07–U12</a></nav>'
            inner+=''.join(term_outline(path,t) for t in data['terms'])
        else:
            available=[u for u in UNITS if u['grade']==grade]
            inner+='<div class="empty-state"><h2>完整年級課程尚在規劃</h2><p>目前 G1–G3 已全部開放；G5 保留一個示範單元。下方僅列已完成的教材。</p></div>'
            if available:inner+=cards(path,available)
            inner+=link(path,'index.html','前往 G1–G3 課程','button')
    else:
        inner='<p class="eyebrow">THE BIG PICTURE</p><h1>六年，一步一步累積。</h1><p class="intro">從詞語到段落。年級是建議起點，先備能力更重要；G1–G3 共 36 課已開放。</p><div class="grade-map">'
        for g,(en,title,desc) in labels.items():
            status='12 課＋2 次學期複習' if g<=3 else ('1 個示範單元' if g==5 else '課程規劃中')
            inner+=f'<article class="map-row"><strong class="map-grade">{g:02}</strong><div><p class="eyebrow">GRADE {g} · {en}</p><h2>{title}</h2><p>{desc}</p></div><div><span class="pill">{status}</span>{link(path,f"grades/g{g}/index.html","查看年級 →","text-link")}</div></article>'
        inner+='</div><p class="note">原規劃每年級 12 課，G1–G3 完成 36 課，另有 G5 示範 1 課。G1/G2 的主題參考教材目錄重新編排；網站單元編號不等同原書，G3–G6 為自主延伸，非官方課綱。</p>'+link(path,'curriculum/grade-1-3.md','下載 G1–G3 課程編排文件（Markdown）','button secondary')
    body=f'<main id="main" tabindex="-1" class="overview-main">{crumb(path,[(None,f"Grade {grade}" if grade else "六年課程地圖")])}{inner}</main>'
    write(path,shell(path,f'Grade {grade}' if grade else '六年課程地圖',body,'map'))

def term_review(grade,data):
    path=f'grades/g{grade}/term-{data["term"]}/review.html'
    content=''
    for offset in [0,3]:
        content+=quiz(data['review'][offset:offset+3],f'學期複習 {offset//3+1}',offset+1)
    wt=data['project']
    sources=list(dict.fromkeys(q['source'] for q in data['review']))
    breadcrumbs=crumb(path,[(f'grades/g{grade}/index.html',f'Grade {grade}'),(None,f"Term {data['term']} 複習")])
    body=f'<main id="main" tabindex="-1" class="guide-main term-review">{breadcrumbs}<p class="eyebrow">RETRIEVE · CONNECT · WRITE</p><h1>Term {data["term"]}：把學過的連起來</h1><p>先不看課文，試做六題，再讀解析。這是跨課抽樣檢核，不是完整程度測驗。可列印本頁；列印會包含已展開的解析。</p>{content}<section><h2>錯了，就回到這裡</h2><ul>'+''.join(f'<li>{link(path,route(BY_ID[uid]),e(uid.upper()+" "+BY_ID[uid]["topic"]))}</li>' for uid in sources)+f'</ul><p>形式錯：回到用法與對照；意思不清楚：回到情境卡；寫不出來：先口述，再用句框寫，最後拿掉句框重寫。</p></section><section><h2>整合作品：{e(wt["title"])}</h2><p>{e(wt["prompt"])}</p><p>再從本 Term 其他兩課各選一個已學重點加入作品。隔一週不看示例重寫一次，保留兩次作品比較。</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in wt['checklist'])+f'</ul><details><summary>參考作品（可自行增加本學期的細節）</summary><p lang="en">{e(wt["sample"])}</p></details><p class="note">作品檢核：意思清楚、目標形式合宜、句子完整、修訂有進步。每項記「可獨立完成／需要提示／先複習」，不用單一分數代表全部能力。</p></section>{link(path,f"grades/g{grade}/index.html","回年級課程目錄 →","button")}</main>'
    write(path,shell(path,f'G{grade} Term {data["term"]} 複習',body,'map'))

def curriculum_document():
    lines=['# Grade 1–3 英文文法課程編排 v1.0','', '更新：2026-09-19。每年級兩個 Term、每 Term 六個 Unit，共 36 課。G5-U03 另保留示範。', '', '## 來源與編排原則', '', 'G1/G2 參考使用者提供的三張教材目錄照片，重新組織成網站單元；編號不是原書頁碼或單元的一對一複製。G3 為自主延伸設計，非康橋或 MyGrammar 官方課綱。所有教材例句與練習皆自主撰寫。', '', '依辨認、理解、產出、寫作四層教學。每個用法分組至少五個不同情境例句，每句包含使用情境、英文、中文與目標形式。五種情境不等於五種不同的文法意義。', '', '每課包含兩題先備檢核、三組各三題核心選擇題、三題改寫／開放題、寫作與三題課末檢核；另附學生學習單及獨立答案。每 Term 六題跨課檢核與作品回顧。', '', '每課四個 35–40 分鐘小節，可拆為家庭短時段；每 Term 單元約 12–15 週，另保留 3–5 週複習、作品與補強。不是每個學生都需要相同課時。', '', '## 與原始目錄／對話的對應', '', '- G1 名詞、普通／專有、代名詞與 I/me、動作、簡單現在、主詞／述語、形容詞／冠詞、位置、四類句型均涵蓋；增加 be 專課與完整句修訂，延續已公開 U06。', '- G2 句子／標點、主詞／述語、規則與不規則複數、集合名詞、簡單現在、過去／未來與不規則動詞均涵蓋；補上受格、問句否定與片語以串接寫作。', '- G3 對話列出的詞性回顧、所有格、助動詞、現在／過去進行、現在式對照、副詞、比較／最高級、連接詞／複合句、Wh-、there is/are、可數／不可數均整併為 12 課。U01 較多，分四小節教：詞性與名詞、數量、some/any、存在句；助動詞 have 的完成式只辨認，不納入評量。', '', '## 螺旋與教學邊界', '', '- 名詞：G1 辨認與基本單複數 → G2 完整常用複數／集合 → G3 數量與所有關係。', '- 動詞：G1 be／動作與第三人稱初步接觸 → G2 現在、過去、未來 → G3 現在／過去進行與使用對照。', '- 句子：G1 主詞述語與四種句型 → G2 片語擴充 → G3 副詞、比較、連接與提問。', '- G1 可口述代替大量抄寫；G2 寫 3–5 句；G3 寫 4–6 句並加入修訂。術語服務於表達，不只考圈字。', '- 不把 a/an 教成只看字母；不把所有 f/fe 或 y 一律套用；不把 now 當進行式唯一判據；區分 be/do 問句及 did/does 後原形。', '- 集合名詞以美式團體整體用法示範，說明英式用法可不同；不把變體當全球唯一正解。', '- 不用性別姓名刻板假定評分；題幹需要時明確指定代名詞語境。', '- 暖身回取先備課程；課末更換情境檢核；一日後針對錯誤再練，一週後重寫作品。', '', '## Scope & sequence', '']
    for grade in CURRICULUM:
        lines+= [f'### Grade {grade["grade"]}','']
        for term in grade['terms']:
            lines += [f'#### Term {term["term"]} — {term["title"]}','']
            for uid in term['units']:
                u=BY_ID[uid]
                lines += [f'##### {uid.upper()} · {u["topic"]}', '', '- 學習目標：'+'；'.join(u['goals']),'- 先備：'+('、'.join(u['prerequisites']) or '口語辨認生活事物'),'- 教學重點：'+'；'.join(g['title'] for g in u['usage_groups']),'- 目標句：'+u['usage_groups'][0]['cases'][0]['example'],'- 寫作：'+u['write']['prompt'],f'- 教材：{route(u)}', '']
            lines += ['學期末：六題跨課抽樣檢核＋整合作品，依解析連回對應課程。','']
    lines += ['## 編輯與驗收', '', '教材單一來源為 content/units.json，學期順序與複習題為 content/curriculum.json。維持既有網址不改名。執行 python3 scripts/build.py、python3 tests/validate.py、node --check assets/app.js。', '', '驗收包含 G1–G3 各 12 課且順序連續、先備存在且不倒置、每個用法分組至少五種情境、選項不重複且答案有效、全部頁面及錨點可達、學習單與答案分離、所有學期複習可回到來源課程。', '', '教材尚待教師審閱，不以自動檢查替代語意與教學成效評估。G4/G6 尚無完整教材，G5 僅一個示範；不標成六年全部完成。', '']
    write('curriculum/grade-1-3.md','\n'.join(lines))
def guide():
    path='guide/index.html'
    body=f'''<main id="main" tabindex="-1" class="guide-main">{crumb(path,[(None,'使用指南')])}<p class="eyebrow">FOR LEARNERS & GROWN-UPS</p><h1>讓每一次練習，都接近真正的表達。</h1><p class="intro">可以和孩子一起讀，也可以讓孩子依自己的步調試一試。</p><section><h2>從哪一課開始？</h2><p>G1 從名詞與句子開始；G2 建立現在、過去與未來表達；G3 擴充進行式、比較與句子連接。G5 示範假設已接觸現在完成式。每課都附暖身題與先備小補充，年級不代表固定程度。</p></section><section><h2>一課怎麼進行？</h2><ol><li>讀目標，做兩題暖身。</li><li>看情境，先談意思，再找形式。</li><li>分段練習，查看答案與原因。</li><li>在紙上完成小作品，依檢核表修改。</li><li>用三題課末檢核決定要複習哪一段。</li></ol><p>每單元建議四個 35–40 分鐘學習時段；在家可拆成更短的段落。答得快不代表一定學會，能用在新句子裡更重要。</p></section><section><h2>給回饋時，先看意思</h2><p>選擇題可以即時檢查。改寫與寫作有多種合理答案，請依參考答案及判準自評，不以唯一字串判定。初學者可先口述，成人協助記錄，不把書寫速度當文法能力。</p></section><section><h2>列印與離線閱讀</h2><p>每課側欄有「列印學習單」與「答案與解析」。學習單不含答案；答案另頁列印。你也可以使用瀏覽器的列印功能另存 PDF。即使關閉 JavaScript，教材、連結與答案仍可使用。</p></section><section id="privacy"><h2>資料與隱私</h2><p>這個網站不要求登入，也不收集姓名或上傳答案。作答選擇與檢核勾選不會持久儲存；頁面重新載入或離開後，請勿期待保留。網站沒有分析追蹤或外部字型。網站由 GitHub Pages 提供服務，主機可能依其服務政策記錄連線資訊。</p></section><section><h2>教材來源與目前範圍</h2><p>{DISCLAIMER}</p><p>G1–G3 各 12 課，共 36 課完整教學內容，另有每年級兩次學期複習。G5 保留 U03 示範，其餘 G4–G6 仍為規劃方向。每課都有例句、練習、解析、寫作與學習單。教材待教師審閱，請依實際學習反應調整。</p></section>{link(path,'index.html','選擇年級，開始學習','button')}</main>'''
    write(path,shell(path,'使用指南',body,'guide'))

def main():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    curriculum_document()
    home(); overview(); guide()
    for grade in CURRICULUM:
        for term in grade['terms']: term_review(grade['grade'],term)
    for g in range(1,7): overview(g)
    for u in UNITS: lesson(u); printable(u); printable(u,True)
    write('404.html',shell('404.html','找不到這個頁面','<main id="main" tabindex="-1" class="overview-main"><h1>這個頁面不在課程裡。</h1><p>請由上一頁或網站首頁重新選擇單元。</p><a href="./index.html">返回首頁</a></main>'))
    write('.nojekyll','')
    write('robots.txt','User-agent: *\nAllow: /\n')
    print(f'Built {len(list(OUT.rglob("*.html")))} HTML pages in {OUT}')
if __name__=='__main__': main()
