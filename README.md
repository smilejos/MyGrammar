# Grammar Journey — 英文文法學習室

三個可實際試用的示範單元，採原生 HTML、CSS、JavaScript，適合 GitHub Pages。沒有第三方前端套件、資料庫、遠端字型或執行期 API。

**正式網站：[Grammar Journey](https://smilejos.github.io/MyGrammar/)**

已於 2026-09-16 發布。推送到 `main` 後，GitHub Actions 會自動檢查、建置並更新網站。

## 已完成範圍

- G1-U06：am / is / are 介紹自己。
- G3-U09：比較級，用重量與價格說明選擇。
- G5-U03：現在完成式與簡單過去式，含 for / since。
- 每課兩題暖身、依文法形式分組的情境例句、五組差異對照、九道單選＋三道開放核心練習、寫作任務、三題課末檢核。
- 三份學生學習單、三份獨立答案頁、年級方向與使用指南。
- 所有答案與教材都在 HTML 裡；JavaScript 僅提供選擇題檢查、重設與頁內導覽提示。

其他年級與單元只呈現規劃方向，不代表完整 72 課已完成。示範教材為自主編排、待教師審閱；G1 的 be verbs 為補充設計，G3–G6 為延伸設計，非康橋或 MyGrammar 官方課綱。

## 例句與用法標準（v0.2）

每個文法形式至少五個不同例句與五種使用情境；每組包含情境、何時使用、英文例句、中文意思與目標形式標示。這裡的「五種用法」是五種情境應用，不將同一規則硬拆成五種文法意義。

- G1：am、is、are，各五組，共 15 組。
- G3：-er、more、good → better，各五組，共 15 組。
- G5：簡單過去、現在完成、for、since，各五組，共 20 組。
- 每課另附五組對照，說明形式、語意與上下文的差異。
- 編輯來源為 `content/units.json` 的 `usage_groups`；不要把只換人名的句子當作不同情境。
- 學生學習單仍只含作答所需資訊，完整情境例句收在教學頁，可用瀏覽器列印該頁。

## 在本機查看

直接開啟 `dist/index.html` 即可。也可以在專案目錄執行：

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

然後開啟 `http://127.0.0.1:4173/`。

## 修改內容與重建

`content/units.json` 是教材單一來源；`scripts/build.py` 是共用頁面模板；`assets/` 保存樣式與選擇題互動。請勿只改 `dist/` 裡的教材，重建會覆蓋已生成頁面。

```sh
python3 scripts/build.py
python3 tests/validate.py
node --check assets/app.js
```

需要 Python 3.10 或以上執行建置與檢查；瀏覽網站不需要 Python。Node 只用於語法檢查，不是建置或瀏覽必需條件。

## 發布到 GitHub Pages

儲存庫：[smilejos/MyGrammar](https://github.com/smilejos/MyGrammar)。已附 `.github/workflows/pages.yml`，GitHub Pages 發布來源設定為 GitHub Actions。正式網址與目前發布結果可從儲存庫的 Pages 設定或 Actions 執行結果查看。

1. 將專案放入選定的 GitHub repository，預設分支使用 `main`；若不同，修改 workflow 分支名稱。
2. 在 repository 的 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。
3. 推送到 `main` 或手動執行 workflow，完成後使用部署結果所顯示的 Pages 網址。

流程會先建置與檢查，再只發布 `dist/`，不會把內容編輯檔與開發用資料一起作為網站根目錄。相對連結支援 repository 子路徑。沒有假造帳號、網址或已完成部署的狀態。

此示範版所有頁面暫設 `noindex,follow`，方便評估，尚未產生正式 canonical/sitemap。若要讓正式教材被搜尋到，請在確定正式網址且完成教材審閱後，調整 `scripts/build.py` 的 robots 設定，另生成主頁與課文的 canonical/sitemap，學生列印副本與答案頁仍可保留 noindex。

Workflow 的部署步驟參考 [GitHub 官方 static Pages workflow](https://github.com/actions/starter-workflows/blob/main/pages/static.yml)（2026-09-15 查閱）。發布流程會檢查課程資料、連結與 JavaScript，僅將 `dist/` 上傳為網站。

## 使用方式

選擇題「檢查答案」會標示未答、答對或需要再想一想，並解釋原因。答案可直接展開，這是學習材料，不是保密考試。改寫與寫作以判準自評，不使用字串比對或 AI 假裝批改。

作答與勾選不持久保存。學生可在紙上寫作；列印學習單不含答案，答案另頁。沒有登入、跨裝置進度或作答資料上傳。

## 驗證與限制

靜態檢查涵蓋全部 19 頁的連結／錨點、題目數量與答案範圍、學生／答案分離。瀏覽器檢查記錄見 `QA.md`。

自動與瀏覽器檢查不能取代英文教師的內容審閱。這是可操作的教材示範版，尚未聲稱全面符合 WCAG 或通過正式教學成效驗證。
