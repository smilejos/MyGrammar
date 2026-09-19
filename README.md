# Grammar Journey — 英文文法學習室

[正式網站](https://smilejos.github.io/MyGrammar/) · [G1–G3 課程編排](dist/curriculum/grade-1-3.md) · [G4–G6 課程編排](dist/curriculum/grade-4-6.md) · [六年完整編排](dist/curriculum/grade-1-6.md)

Grade 1–6 各 12 個完整單元，分為兩個 Term，共 72 課。以原生 HTML、CSS、JavaScript 製作，由 GitHub Pages 提供服務，無第三方前端套件、資料庫或執行期 API。

## 已完成內容

| 年級 | 編排方向 | 單元 | 情境例句 |
|---|---|---:|---:|
| G1 | 詞性、主詞述語、be、描述與四種句型 | 12 | 162 |
| G2 | 複數、受格、現在式、過去式、未來與片語 | 12 | 138 |
| G3 | 所有格、進行式、副詞、比較、連接與提問 | 12 | 164 |
| G4 | 時態深化、情態、動詞搭配、受詞與子句 | 12 | 120 |
| G5 | 完成式、被動、關係子句、條件與合句 | 12 | 130 |
| G6 | 假設、轉述、句型變化、段落與修訂 | 12 | 120 |

- G1–G6 共 72 課、834 組情境例句；每個用法分組至少五個不同情境、英文例句、中文與目標形式標示。
- 每課：兩題先備暖身、九題核心選擇、三題改寫／開放題、寫作任務、三題課末檢核、五組差異對照與常見錯誤。
- 十二次學期複習各六題，附來源課程連結與整合作品檢核。全站共 1,080 道選擇題呈現（含暖身回取與學期複習，不是 1,080 道不重複題目）。
- 72 份學生學習單與 72 份獨立答案頁；全站共 238 頁 HTML。
- 依年級、Term、Unit 顯示順序，單元提供先備連結、上一課／下一課與學期複習入口。
- G4–G6 共 36 課、370 組情境例句；保留原 G5-U03 網址，現在由 U01 的形式與 U02 的意義先鋪陳，再進入時態對照。
- 完成進行式、非限定關係子句、compound-complex 從理解與仿寫入手；G6 最終作品為 8–10 句，保留初稿、修訂稿與修改理由。

G1/G2 參考使用者提供的目錄主題重新編排，網站編號不等同原書。G3–G6 為自主延伸設計，非康橋或 MyGrammar 官方課綱。教材仍待教師審閱；自動檢查不能取代教學判斷。

## 本機預覽與修改

教材的單一來源是 `content/units.json`；年級／學期順序、複習題與整合作品是 `content/curriculum.json`。`scripts/build.py` 共用模板產生網站與 Markdown 課程編排，`assets/` 保存樣式與互動。不要只修改 `dist/`，重建會覆蓋生成檔。

```sh
python3 scripts/build.py
python3 tests/validate.py
node --check assets/app.js
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

開啟 `http://127.0.0.1:4173/`；也可直接開啟 `dist/index.html` 離線閱讀。建置／檢查使用 Python 3.10+ 標準函式庫，Node 僅作 JavaScript 語法檢查。

每次修改課末檢核或寫作任務時，也應更新 `curriculum.json` 中對應的學期複習副本與作品；新增先備必須指向已完成且較早的課程。維持已發布的單元 slug，避免舊連結失效。

## GitHub Pages

[儲存庫](https://github.com/smilejos/MyGrammar) 已啟用 GitHub Actions 發布。推送 `main` 後，`.github/workflows/pages.yml` 會建置、驗證連結與資料、檢查 JS，再發布 `dist/`。相對網址支援 `/MyGrammar/` 子路徑。

目前保留 `noindex,follow`，供教材評閱，不產生正式 canonical/sitemap。未來完成內容審閱並決定開放搜尋後再處理；列印副本與答案可繼續 noindex。

## 學習方式與限制

選擇題可檢查答對、答錯、未答與原因，也可重設。所有教材、答案和連結在 HTML 中；JavaScript 關閉時仍可閱讀及展開答案。改寫與寫作依判準自評，沒有字串比對或 AI 自動批改。

作答與勾選不持久儲存，沒有登入、追蹤分析或資料上傳。學生可在紙上作答，學習單不含答案。教學頁與學期複習頁列印時會展開解析；需要無答案版本時請選單元的「列印學習單」。

驗證記錄見 [QA.md](QA.md)。完整課程數量、先備順序、固定網址、情境數量、答案範圍、全部頁面／錨點與學習單答案分離都會自動檢查。
