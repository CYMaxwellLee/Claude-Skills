---
name: nstc-travel-report
description: |
  國科會（NSTC）出國差旅報告 / 出席國際學術會議心得報告自動生成工具。
  使用預先建立的黃金範本 DOCX，透過 unpack→填入→repack 流程快速產生格式完美的報告。
  內建台灣用語檢查，自動修正中國用語為中華民國台灣正式用語。
  當使用者提到「差旅報告」、「出國報告」、「國科會報告」、「會議心得報告」、「NSTC travel report」時觸發此技能。
  也適用於使用者說「幫我寫 CVPR/NeurIPS/ICML/ICLR/AAAI 報告」等情境。
---

# 國科會出席國際學術會議心得報告

## 概述

這個 Skill 用來快速產生格式正確的國科會（NSTC）出席國際學術會議心得報告。核心做法是用一份已驗證格式的黃金範本 DOCX，透過 XML 佔位符替換來填入會議資訊，完全跳過 from scratch 生成文件的各種格式問題。

## 檔案結構

```
nstc-travel-report/
├── SKILL.md                          ← 你正在讀的這份
├── scripts/
│   ├── fill_template.py              ← 主要流程腳本（unpack→替換→repack）
│   └── taiwan_terms.py               ← 台灣用語檢查/修正工具
├── assets/
│   └── template.docx                 ← 黃金範本（含 {{佔位符}}）
└── references/
    └── xml_gotchas.md                ← DOCX XML 編輯的踩坑筆記
```

## 使用流程

### 第一步：收集必要資訊

向使用者收集以下資訊（可透過對話、上傳檔案、或截圖取得）：

**必填欄位（表格資訊）：**
| 欄位 | 範例 | 說明 |
|------|------|------|
| 計畫編號 | NSTC 113-2634-F-002-008 | 國科會計畫編號 |
| 計畫名稱 | 解決在地化需求之生成式AI關鍵技術研究 | |
| 出國人員姓名 | 李濬屹 | |
| 服務機構及職稱 | 國立臺灣大學 資訊工程學系 教授 | |
| 會議起始日 | 113年12月10日 | 用民國年（西元年 - 1911） |
| 會議結束日 | 113年12月15日 | |
| 會議地點 | Vancouver Convention Centre, Vancouver, BC, Canada | |
| 會議中文名稱 | 2024神經資訊處理系統大會 | |
| 會議英文名稱 | The Thirty-Eighth Annual Conference on Neural Information Processing Systems | |
| 會議簡稱 | NeurIPS 2024 | |
| 論文中文題目 | 基於能量正規化流的最大熵強化學習 | |
| 論文英文題目 | Maximum Entropy Reinforcement Learning via Energy-Based Normalizing Flow | |
| 報告日期 | 115年2月22日 | 繳交報告的日期 |

**需要生成的內文（由 Claude 撰寫）：**
- 第一節：參加會議經過（Tutorial、主會議、Workshop 分日描述）
- 第二節：與會心得（含重要論文介紹 3-4 篇）
- 第三節：發表論文全文或摘要（作者、Abstract）
- 第四節：建議（4-5 點）
- 第五節：攜回資料名稱及內容

**可選：**
- 使用者的論文 PDF（用來擷取作者名單和 Abstract）
- 會議行程表（用來確認日期和活動安排）
- 照片說明文字（用於海報展示照片的圖說）

### 第二步：生成內文並填入範本

有兩種方式：

#### 方式 A：使用 fill_template.py 腳本（推薦用於完全自動化）

1. 建立 config.json，包含所有表格欄位和內文
2. 執行腳本：
```bash
python scripts/fill_template.py config.json assets/template.docx output.docx
```

#### 方式 B：手動 unpack + 編輯（推薦用於需要微調的情況）

這是這次經過驗證的做法，更靈活：

```bash
# 1. 複製範本
cp assets/template.docx working.docx

# 2. Unpack
python <docx-skill>/scripts/office/unpack.py working.docx unpacked/

# 3. 編輯 XML —— 替換佔位符
#    在 unpacked/word/document.xml 中搜尋 {{佔位符}} 並替換為實際值
#    可以用 Python 腳本或直接用 Edit 工具

# 4. 執行台灣用語檢查
python scripts/taiwan_terms.py unpacked/word/document.xml

# 5. Repack
python <docx-skill>/scripts/office/pack.py unpacked/ output.docx --original working.docx

# 6. 驗證
python <docx-skill>/scripts/office/soffice.py --headless --convert-to pdf output.docx --outdir .
pdftoppm -jpeg -r 150 output.pdf verify
# 然後用 Read 工具查看 verify-*.jpg
```

### 第三步：驗證

1. 轉 PDF 並轉圖片做視覺確認
2. 用 pandoc 擷取純文字，grep 檢查是否有遺漏的中國用語
3. 確認所有 `{{佔位符}}` 都已被替換

## 範本中的佔位符一覽

### 表格欄位
`{{報告日期}}` `{{計畫編號}}` `{{計畫名稱}}` `{{出國人員姓名}}` `{{服務機構及職稱}}`
`{{會議起始日}}` `{{會議結束日}}` `{{會議地點}}` `{{會議中文名稱}}` `{{會議英文名稱}}`
`{{會議簡稱}}` `{{論文中文題目}}` `{{論文英文題目}}`

### 第一節：參加會議經過
`{{SEC1_會議簡介}}` — 會議整體介紹（名稱、日期、地點、投稿/接受數量等）
`{{SEC1_TUTORIAL日期標題}}` — 如「12月10日：參加Tutorials」
`{{SEC1_TUTORIAL內容}}` — Tutorial 活動描述
`{{SEC1_主會議日期標題}}` — 如「12月11日至12月13日」
`{{SEC1_主會議內容}}` — 主會議描述（Best Paper、自己的論文展示等）
`{{SEC1_WORKSHOP日期標題}}` — 如「12月14日至12月15日」
`{{SEC1_WORKSHOP內容}}` — Workshop 活動描述

### 第二節：與會心得
`{{SEC2_心得段落1}}` 至 `{{SEC2_心得段落6}}` — 6 段心得
`{{SEC2_重要論文標題}}` — 如「NeurIPS 2024重要論文與個人觀察」
`{{SEC2_重要論文引言}}` — 引言段落
`{{SEC2_論文1}}` 至 `{{SEC2_論文4}}` — 4 篇重要論文介紹

### 第三節：發表論文
`{{論文作者與摘要}}` — 作者名單 + Abstract

### 第四節：建議
`{{SEC4_建議1}}` 至 `{{SEC4_建議5}}` — 5 點建議
`{{SEC4_建議4標題}}` — 第 4 點建議的小標題

### 第五節：攜回資料
`{{SEC5_攜回資料1}}` `{{SEC5_攜回資料2}}` — 攜回資料描述

### 其他
`{{照片說明}}` — 海報照片的圖說

## 撰寫內文的注意事項

### 用語規範
- **嚴禁使用中國用語**，這是國科會正式報告，必須使用中華民國台灣用語
- 撰寫完成後務必執行 `taiwan_terms.py` 做最終檢查
- 常見易錯：信息→資訊、算法→演算法、自回歸→自迴歸
- 詳細對照表見 `references/xml_gotchas.md`

### 內文風格
- 以學術正式語氣撰寫
- 第一節描述事實（日期、活動、論文數量）
- 第二節表達個人觀察與反思，連結自身研究方向
- 重要論文介紹：每篇約 80-120 字，說明研究內容 + 對自身研究的啟發
- 第四節建議要具體可行，與台灣學術環境相關
- 全文使用正體中文，專有名詞保留英文

### 民國年換算
西元年 - 1911 = 民國年。2024年 = 民國113年。

## 技術注意事項

在編輯 XML 之前，務必先閱讀 `references/xml_gotchas.md`。重點摘要：

1. **絕對不要用 docx-js 從頭生成** — 格式會全壞，必須用 unpack→edit→repack
2. **文字可能被拆散到多個 XML run** — 用佔位符替換可避免此問題
3. **新增段落的 paraId 必須 < 0x80000000** — 否則 pack 驗證失敗
4. **LibreOffice 要用 soffice.py wrapper** — 不能直接呼叫 soffice
5. **台灣用語檢查** — 用 taiwan_terms.py 自動檢查修正

## 範例 config.json

```json
{
  "報告日期": "115年2月22日",
  "計畫編號": "NSTC 113-2634-F-002-008",
  "計畫名稱": "解決在地化需求之生成式AI關鍵技術研究",
  "出國人員姓名": "李濬屹",
  "服務機構及職稱": "國立臺灣大學 資訊工程學系 教授",
  "會議起始日": "113年12月10日",
  "會議結束日": "113年12月15日",
  "會議地點": "Vancouver Convention Centre, Vancouver, BC, Canada",
  "會議中文名稱": "2024神經資訊處理系統大會",
  "會議英文名稱": "The Thirty-Eighth Annual Conference on Neural Information Processing Systems",
  "會議簡稱": "NeurIPS 2024",
  "論文中文題目": "基於能量正規化流的最大熵強化學習",
  "論文英文題目": "Maximum Entropy Reinforcement Learning via Energy-Based Normalizing Flow",
  "論文作者與摘要": "Chen-Hao Chao, ... Chun-Yi Lee\n\nAbstract: ...",
  "照片說明": "圖一、本人於NeurIPS 2024主會議海報展示現場",
  "body": {
    "參加會議經過": {
      "會議簡介": "...",
      "tutorial日期標題": "12月10日：參加Tutorials",
      "tutorial內容": "...",
      "主會議日期標題": "12月11日至12月13日",
      "主會議內容": "...",
      "workshop日期標題": "12月14日至12月15日",
      "workshop內容": "..."
    },
    "與會心得": {
      "心得段落1": "...",
      "心得段落2": "...",
      "心得段落3": "...",
      "心得段落4": "...",
      "心得段落5": "...",
      "心得段落6": "...",
      "重要論文標題": "NeurIPS 2024重要論文與個人觀察",
      "重要論文引言": "以下列舉本次會議中我認為最具影響力的幾篇論文...",
      "論文1": "1. Visual Autoregressive Modeling（Best Paper）：...",
      "論文2": "2. Diffusion Models Are Evolutionary Algorithms（Oral）：...",
      "論文3": "3. Large Language Monkeys（Spotlight）：...",
      "論文4": "4. LLM-QAT（Oral）：..."
    },
    "建議": {
      "建議1": "...",
      "建議2": "...",
      "建議3": "...",
      "建議4標題": "建立產學合作的AI研發平台",
      "建議4": "...",
      "建議5": "..."
    },
    "攜回資料": {
      "攜回資料1": "...",
      "攜回資料2": "..."
    }
  }
}
```
