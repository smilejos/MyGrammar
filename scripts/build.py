"""Build dependency-free, GitHub Pages-compatible teaching pages."""
from pathlib import Path
from html import escape as esc
import json, shutil, os, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
UNITS=json.loads((ROOT/'content/units.json').read_text())
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
    <nav aria-label="主要導覽">{link(path,'index.html','示範課程','nav-link '+('active' if active=='home' else ''))}{link(path,'curriculum/index.html','六年課程地圖','nav-link '+('active' if active=='map' else ''))}{link(path,'guide/index.html','使用指南','nav-link '+('active' if active=='guide' else ''))}</nav>
    <span class="preview-label">教學預覽版</span></div></header>'''
def shell(path,title,body,active='',color='blue',printpage=False,description='三個英文文法示範單元，從理解例句、練習到寫作。'):
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · Grammar Journey</title><meta name="description" content="{e(description)}"><meta name="robots" content="noindex,follow"><link rel="icon" type="image/svg+xml" href="{href(path,'assets/favicon.svg')}"><link rel="stylesheet" href="{asset(path,'assets/style.css')}"><link rel="stylesheet" media="print" href="{asset(path,'assets/print.css')}"><script defer src="{asset(path,'assets/app.js')}"></script></head><body class="theme-{color}{' print-page' if printpage else ''}">{header(path,active)}{body}<footer class="site-footer"><div><span class="footer-brand">Grammar Journey</span><p>{DISCLAIMER}</p><p class="fine">示範教材 · v0.2 · 2026.09　<span>3 個單元開放試用，其餘課程尚未製作。教材待教師審閱。</span></p></div>{link(path,'guide/index.html#privacy','資料與隱私說明')}</footer></body></html>'''
def crumb(path,items):
    return '<nav class="breadcrumbs" aria-label="麵包屑">'+link(path,'index.html','首頁')+''.join(f'<span aria-hidden="true">/</span>{link(path,t,l) if t else f"<span aria-current=\"page\">{e(l)}</span>"}' for t,l in items)+'</nav>'
def art(u):
    if u['grade']==1:
        return '<div class="sentence-art"><span>I</span><strong>am</strong><span>happy.</span><div class="art-caption">主詞 <span>＋</span> be <span>＋</span> 感受</div></div>'
    if u['grade']==3:
        return '<div class="comparison-art"><div><span>Bag A</span><strong>1 <small>kg</small></strong><i style="width:33%"></i></div><div><span>Bag B</span><strong>3 <small>kg</small></strong><i></i></div><p>lighter <span>↔</span> heavier</p></div>'
    return '<div class="time-art"><div><span>THEN · 過去</span><span>NOW · 現在</span></div><div class="time-line"></div><strong>I have lived here</strong><p>since 2022.</p></div>'
def cards(path,units=UNITS):
    out='<div class="course-grid">'
    for u in units:
        out+=f'''<article class="course-card theme-{u['color']}"><div class="card-top"><span class="grade-label">GRADE {u['grade']}</span><span class="unit-label">UNIT {u['number']:02}</span></div>{art(u)}<div class="card-content"><p class="eyebrow">{u['tag']}</p><h2>{e(u['topic'])}</h2><p>{u['short']}</p><div class="card-meta"><span>4 個學習小節</span><span>練習＋寫作</span></div>{link(path,route(u),'進入單元 <span aria-hidden="true">↗</span>','button full')}</div></article>'''
    return out+'</div>'
def home():
    path='index.html'
    body=f'''<main id="main" tabindex="-1" class="home-main"><section class="home-heading"><div><p class="eyebrow">LEARN IT. USE IT.</p><h1>今天，想練習<br class="mobile-break">哪一種表達？</h1><p class="intro">從一句話開始，讓文法成為你表達的工具。</p></div><div class="edition"><strong>03</strong><span>示範單元<br>現在開始學習</span></div></section>{cards(path)}<section class="learning-strip" aria-labelledby="flow-title"><div><p class="eyebrow">YOUR LEARNING PATH</p><h2 id="flow-title">每一課，都有一個小進步。</h2></div><ol><li><b>01</b>看例子</li><li><b>02</b>懂用法</li><li><b>03</b>試一試</li><li><b>04</b>寫出來</li></ol></section><section class="home-bottom"><div><h2>從 Grade 1，走到 Grade 6</h2><p>查看六年的學習方向。這次先試用 G1、G3、G5 各一課。</p>{link(path,'curriculum/index.html','查看完整學習路線 →','text-link')}</div><div><h2>一起陪孩子學習</h2><p>每課附有教學提示、答案解析與可列印學習單。</p>{link(path,'guide/index.html','閱讀家長與教師指南 →','text-link')}</div></section></main>'''
    write(path,shell(path,'示範課程',body,'home'))
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
    before, focus, after = case['example'].partition(case['focus'])
    return e(before)+f'<strong class="grammar-highlight">{e(focus)}</strong>'+e(after)

def usage_library(u):
    nav='<nav class="usage-nav" aria-label="例句與用法分組">'+''.join(
        f'<a href="#usage-{e(g["id"])}">{e(g["title"].split("：")[0])} <span>5 組</span></a>'
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
        groups+=f'<header><h4 id="usage-title-{e(group["id"])}">{e(group["title"])}</h4><span class="pill">5 個例句 · 5 種情境</span></header>'
        groups+=f'<p class="usage-form">{e(group["form"])}</p><p class="usage-note">{e(group["note"])}</p><ol class="usage-list">{cases}</ol></section>'
    return f'<div class="usage-library"><h3>從五種情境，看懂每一種文法</h3><p class="muted">{e(u["usage_intro"])}</p>{nav}{groups}</div>'

def lesson(u):
    path=route(u); write_task=u['write']
    toc=[('start','開始前','暖身與學習目標'),('notice','01 看例子','觀察情境'),('understand','02 懂用法','情境、例句與對照'),('practice','03 試一試','練習與回饋'),('write','04 寫出來','完成小作品'),('check','帶走一個進步','課末檢核')]
    pre=f'''<section id="start" class="lesson-section"><div class="section-topline"><h2>這一課，我可以…</h2><span class="pill">核心學習</span></div><ul class="goals">{''.join(f'<li>{e(g)}</li>' for g in u['goals'])}</ul><details class="support"><summary>先備小補充 · 展開快速回顧</summary><p>{u['prereq_text']}</p>{''.join(f'<h3>{e(t)}</h3><p>{e(d)}</p>' for t,d in u['support'])}</details><h3>先暖身，不計分</h3>{quiz(u['pre'],'先備暖身')}</section>'''
    scene=f'''<section id="notice" class="lesson-section">{section_head('01','NOTICE',u['scene_title'])}<p>{u['scene_intro']}</p><div class="scene {'data-scene' if u['grade']==3 else ''}">{''.join(f'<div class="scene-line"><span class="speaker">{e(who)}</span><p lang="en">{e(line)}</p></div>' for who,line in u['scene'])}</div><div class="notice-questions">{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in u['notice'])}</div><details class="vocab"><summary>本課小字典</summary><dl>{''.join(f'<div><dt lang="en">{e(w)}</dt><dd>{e(d)}</dd></div>' for w,d in u['vocab'])}</dl></details></section>'''
    rules=f'''<section id="understand" class="lesson-section">{section_head('02','UNDERSTAND','抓住用法，就能舉一反三')}<div class="rules">{''.join(f'<article class="rule"><span>{n}</span><div><h3>{e(t)}</h3><p>{e(d)}</p><p class="rule-example" lang="en">{e(ex)}</p></div></article>' for n,t,d,ex in u['rules'])}</div>{usage_library(u)}<h3>五組對照，看看差在哪裡</h3>{''.join(f'<div class="contrast"><p lang="en">{e(a)}</p><p lang="en">{e(b)}</p><p>{e(d)}</p></div>' for a,b,d in u['contrasts'])}<h3>容易卡住的地方</h3>{''.join(f'<div class="mistake"><p><span class="error-label">需修改</span><span lang="en">{e(a)}</span></p><p><span class="correct-label">修改後</span><span lang="en">{e(b)}</span></p><p>{e(d)}</p></div>' for a,b,d in u['mistakes'])}</section>'''
    practice=f'''<section id="practice" class="lesson-section">{section_head('03','PRACTICE','換你試一試')}<p>先自己想，再檢查答案。答錯時，讀一讀原因後再試一次。</p><noscript><p class="note">互動檢查未啟用。你仍可逐題展開答案，或使用列印學習單。</p></noscript>{''.join(f'<h3 class="practice-heading">{i+1}. {e(name)}</h3>{quiz(qs,name,i*3+1)}' for i,(name,qs) in enumerate(u['groups']))}<h3 class="practice-heading">4. 改一改，自己寫一句</h3><p class="muted">請在紙上或自己的筆記中作答。這三題使用參考答案自評。</p>{open_tasks(u)}</section>'''
    writing=f'''<section id="write" class="lesson-section">{section_head('04','WRITE',write_task['title'])}<p>{e(write_task['prompt'])}</p><div class="writing-paper"><p class="eyebrow">START WITH A SENTENCE</p>{''.join(f'<p lang="en">{e(x)}</p>' for x in write_task['frames'])}<p class="paper-note">寫在紙上，或列印這份學習單。</p></div><details class="sample"><summary>寫完後，再看一份示例</summary><p lang="en" class="english">{e(write_task['sample'])}</p><p>這是其中一種寫法。你的內容可以不同。</p></details><h3>讀一遍，幫自己檢查</h3><div class="checklist">{''.join(f'<label><input type="checkbox"><span>{e(c)}</span></label>' for c in write_task['checklist'])}</div><p class="fine">勾選只供這次閱讀使用，不會儲存。</p><p class="note">{e(write_task['rubric'])}</p></section>'''
    end=f'''<section id="check" class="lesson-section">{section_head('✓','QUICK CHECK','把今天學的，帶到新句子裡')}<p>用三題看看自己哪些地方已經熟悉。這是學習提示，不是程度認證。</p>{quiz(u['exit'],'課末檢核')}<div class="next-note"><h3>還不確定？這樣複習</h3><p>主詞或基本形式卡住，回到<a href="#start">先備小補充</a>；選擇意思時猶豫，回看<a href="#notice">情境</a>；形式不穩定，再看<a href="#understand">用法與錯誤對照</a>。</p><p>{e(u['next_note'])}</p>{link(path,'index.html','回到三個示範單元 →','text-link')}</div></section><section class="lesson-section adult-section"><details><summary>給家長與教師的教學提示</summary><p>{e(u['adult'])}</p><p>建議分四個 35–40 分鐘時段教學；家庭學習可拆成 10–20 分鐘，依孩子實際需要調整。先備與課末題不列入本課 12 道核心練習。</p><p>{e(u['origin'])}。示範教材待教師審閱。</p></details></section>'''
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
    body=f'''<main id="main" tabindex="-1" class="print-main"><div class="print-toolbar">{link(path,route(u),'← 回到教學單元')}<button class="button js-only" hidden data-print>列印 / 另存 PDF</button></div><header class="print-heading"><p>GRAMMAR JOURNEY · G{u['grade']} / T{u['term']} / U{u['number']:02} · v0.2</p><h1>{e(u['topic'])}</h1><h2>{'答案與教學參考' if answers else '學生學習單'}</h2>{'' if answers else '<p>姓名：________________　日期：________________</p>'}<p>{'開放題的示例並非唯一答案，請依判準給予回饋。' if answers else '不需要電腦也能練習。可用瀏覽器的列印功能直接列印。'}</p></header><section class="print-section"><h2>情境資料</h2><p>{e(u['scene_intro'])}</p>{''.join(f'<p><b>{e(w)}</b> <span lang="en">{e(s)}</span></p>' for w,s in u['scene'])}</section>{content}</main>'''
    write(path,shell(path,u['topic']+(' 答案' if answers else ' 學習單'),body,color=u['color'],printpage=True))

def overview(grade=None):
    labels={1:('Words → Sentences','開始寫完整句子','名詞、代名詞、be 與動作動詞、基本句型。'),2:('Sentences → Time','說清楚日常與過去','現在式問句與否定、常見過去式、未來計畫。'),3:('Expand & Connect','把句子寫得更豐富','所有格、進行式、比較級與最高級、句子連接。'),4:('Time & Clauses','連起事件與原因','過去進行式、情態、原因與時間子句。'),5:('Precision & Perspective','表達經驗與細節','現在完成式、被動語態、關係子句與段落連貫。'),6:('Grammar for Writing','讓段落更清楚','整合時態、句型變化、指代與寫作修訂。')}
    path=f'grades/g{grade}/index.html' if grade else 'curriculum/index.html'
    selected=[u for u in UNITS if u['grade']==grade] if grade else []
    if grade:
        en,title,desc=labels[grade]
        inner=f'<p class="eyebrow">GRADE {grade} · {en}</p><h1>{title}</h1><p class="intro">{desc}</p>'
        if selected: inner+='<h2 class="subhead">現在可以試學</h2>'+cards(path,selected)
        else: inner+='<div class="empty-state"><h2>這個年級還在規劃中</h2><p>本次示範先開放 Grade 1、3、5 各一個單元。這裡提供學習方向，尚無可上課的教材。</p>'+link(path,'index.html','先看看三個示範單元','button')+'</div>'
        inner+='<p class="note">完整規劃為每年級 2 個 Term、12 個 Unit；本次只開放明確標示的示範課程。</p>'
    else:
        inner='<p class="eyebrow">THE BIG PICTURE</p><h1>六年，一步一步累積。</h1><p class="intro">從認識詞語，到寫出清楚的段落。年級是建議起點，先備能力更重要。</p><div class="grade-map">'
        for g,(en,title,desc) in labels.items():
            available=next((u for u in UNITS if u['grade']==g),None)
            inner+=f'<article class="map-row"><strong class="map-grade">{g:02}</strong><div><p class="eyebrow">GRADE {g} · {en}</p><h2>{title}</h2><p>{desc}</p></div><div><span class="pill">{"1 個示範單元" if available else "課程規劃中"}</span>{link(path,f"grades/g{g}/index.html","查看年級 →","text-link")}</div></article>'
        inner+='</div><p class="note">全課程規劃為 72 個單元，目前完成 3 個示範。G3–G6 為自主延伸設計，非學校官方課綱。</p>'
    body=f'<main id="main" tabindex="-1" class="overview-main">{crumb(path,[(None,f"Grade {grade}" if grade else "六年課程地圖")])}{inner}</main>'
    write(path,shell(path,f'Grade {grade}' if grade else '六年課程地圖',body,'map'))
def guide():
    path='guide/index.html'
    body=f'''<main id="main" tabindex="-1" class="guide-main">{crumb(path,[(None,'使用指南')])}<p class="eyebrow">FOR LEARNERS & GROWN-UPS</p><h1>讓每一次練習，都接近真正的表達。</h1><p class="intro">可以和孩子一起讀，也可以讓孩子依自己的步調試一試。</p><section><h2>從哪一課開始？</h2><p>G1 適合剛開始寫英文句子的孩子；G3 適合已會用形容詞與 be 描述物品的孩子；G5 假設已接觸現在完成式。每課都附暖身題與先備小補充，年級不代表固定程度。</p></section><section><h2>一課怎麼進行？</h2><ol><li>讀目標，做兩題暖身。</li><li>看情境，先談意思，再找形式。</li><li>分段練習，查看答案與原因。</li><li>在紙上完成小作品，依檢核表修改。</li><li>用三題課末檢核決定要複習哪一段。</li></ol><p>每單元建議四個 35–40 分鐘學習時段；在家可拆成更短的段落。答得快不代表一定學會，能用在新句子裡更重要。</p></section><section><h2>給回饋時，先看意思</h2><p>選擇題可以即時檢查。改寫與寫作有多種合理答案，請依參考答案及判準自評，不以唯一字串判定。初學者可先口述，成人協助記錄，不把書寫速度當文法能力。</p></section><section><h2>列印與離線閱讀</h2><p>每課側欄有「列印學習單」與「答案與解析」。學習單不含答案；答案另頁列印。你也可以使用瀏覽器的列印功能另存 PDF。即使關閉 JavaScript，教材、連結與答案仍可使用。</p></section><section id="privacy"><h2>資料與隱私</h2><p>這個示範站不要求登入，也不收集姓名或上傳答案。作答選擇與檢核勾選不會持久儲存；頁面重新載入或離開後，請勿期待保留。網站沒有分析追蹤或外部字型。若之後發布到 GitHub Pages，主機可能依其服務政策記錄連線資訊。</p></section><section><h2>教材來源與目前範圍</h2><p>{DISCLAIMER}</p><p>本次完成 G1-U06、G3-U09、G5-U03 的示範內容，包含練習、解析與寫作。其他年級頁目前只說明方向，不表示完整教材已完成。所有例句及題目為自主撰寫；示範版待教師審閱，歡迎以實際學習反應調整。</p></section>{link(path,'index.html','選一個示範單元，開始試學','button')}</main>'''
    write(path,shell(path,'使用指南',body,'guide'))

def main():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    home(); overview(); guide()
    for g in range(1,7): overview(g)
    for u in UNITS: lesson(u); printable(u); printable(u,True)
    write('404.html',shell('404.html','找不到這個頁面','<main id="main" tabindex="-1" class="overview-main"><h1>這個頁面不在課程裡。</h1><p>請由上一頁或網站首頁重新選擇單元。</p><a href="./index.html">返回首頁</a></main>'))
    write('.nojekyll','')
    write('robots.txt','User-agent: *\nAllow: /\n')
    print(f'Built {len(list(OUT.rglob("*.html")))} HTML pages in {OUT}')
if __name__=='__main__': main()
