---
name: nstc-c804
description: |
  國科會大專生研究計畫 指導教授初評意見表（C804表）自動生成工具。
  使用已驗證格式的 DOCX 範本，透過 unpack→填入→repack 流程快速產生格式正確的 C804 表。
  當使用者提到「C804」、「初評意見表」、「大專生研究計畫」、「指導教授意見」、「推薦信」時觸發此技能。
  也適用於使用者說「幫某某學生寫 C804」、「大專生計畫的教授評語」等情境。
---

# 國科會大專生研究計畫 指導教授初評意見表（C804）

## 概述

這個 Skill 用來快速產生格式正確的國科會大專生研究計畫 C804 指導教授初評意見表。與差旅報告不同，C804 的內容高度客製化（每個學生完全不同），因此本 Skill 的重點是：
1. 保留已驗證的 DOCX 格式範本
2. 提供過去成功案例作為寫作參考
3. 指引 Claude 如何撰寫各段內容

## 檔案結構

```
nstc-c804/
├── SKILL.md                              ← 你正在讀的這份
├── assets/
│   └── template.docx                     ← 黃金範本（含 {{佔位符}}）
└── references/
    └── example_鄭又齊.txt                ← 過去成功案例（完整文字）
```

## 使用流程

### 第一步：收集學生資訊

向使用者收集以下資訊：

**必要資訊：**
| 資訊 | 說明 |
|------|------|
| 學生姓名（中英文） | 如：鄭又齊 / Yu-Chi Cheng |
| 性別 | 決定英文代名詞 he/she/they |
| 系所年級 | 如：資訊工程學系三年級 |
| 研究計畫名稱（中英文） | 如：Research on Bimanual Robotic Dexterous Manipulations |
| 修過的課程及成績 | 特別是與指導教授的課 |
| GPA 及排名 | |
| 研究經歷 | 實習、比賽、專案等 |
| 研究方向及計畫內容摘要 | 計畫要做什麼、怎麼做、預期成果 |
| 預期投稿會議 | 如 CVPR 2027、ICML 2027 等 |
| 實驗室資源 | 可提供的設備、計算資源等 |

**可選：**
- 學生的 CV 或自傳（可從中擷取成就和經歷）
- 學生的研究計畫書（用來撰寫第二節）
- 過去的 C804 範例（用來參考風格）

### 第二步：撰寫各段內容

撰寫前，先讀取 `references/example_鄭又齊.txt` 作為風格和結構的參考。

#### 第一節：學生潛力評估（英文推薦信）

**語言**：全英文
**長度**：約 5 段，約 500-700 字
**風格**：正式學術推薦信，第一人稱，語氣熱情但專業

**段落結構（對應範本佔位符）：**
- `{{SEC1_PARA1}}`：開頭介紹 + 與學生的關係 + 課程表現 + 研究領域概述 + 團隊中的角色定位。開頭用 "I am glad to have this opportunity to write this letter in support of [Mr./Ms.] [English Name] ([中文名]) application to the undergraduate research project supported by the National Science and Technology Council (國科會大專生研究計畫)."
- `{{SEC1_BOLD1}}`：承接前段的粗體強調文字（如 "key member in our research team"），在範本中這是一個粗體 run。
- `{{SEC1_PARA2}}`：學業表現（GPA、排名、修課成績）
- `{{SEC1_PARA3}}`：課外經歷（實習、比賽、獲獎）
- `{{SEC1_PARA4}}`：推薦結語（為什麼這個學生適合、未來展望）
- `{{SEC1_PARA5}}`：結尾重申推薦 + 聯絡方式。結尾用 "To conclude, I would like to restate my strong recommendation for [Name]..."

**注意事項：**
- 多強調 "undergraduate research project supported by the National Science and Technology Council" 或 "NSTC" 而非只說 "研究計畫"
- 粗體標示重要成就（如 NSTC bold 強調的機構名稱）
- 具體列舉成績和排名數據
- 寫出 "Based on my experience, I would rank him/her among the top X% of students I have ever encountered"

#### 第二節：對學生所提研究計畫內容之評述（中文）

**語言**：中文
**結構**：3 個子段，各有粗體小標題

**子段 1：資源提供與經驗指導**
- `{{SEC2_SUB1_TITLE}}`：「[學生姓名]同學之大專生研究計畫之資源提供與經驗指導」
- `{{SEC2_SUB1_CONTENT}}`：
  - 計畫名稱和討論過程
  - 實驗室的研究資源和經驗（列舉研究領域）
  - 過往獲獎紀錄
  - 研究團隊的國際發表紀錄（列舉頂尖會議和期刊名稱）
  - 可提供的硬體和計算資源
  - 預期成果投稿目標

**子段 2：研究計畫背景概述**
- `{{SEC2_SUB2_TITLE}}`：「[學生姓名]同學之大專生研究計畫背景概述」
- `{{SEC2_SUB2_CONTENT}}`：
  - 學生基本資訊
  - 研究主題的背景和挑戰
  - 為什麼這個研究重要
  - 研究動機

**子段 3：預期目標**
- `{{SEC2_SUB3_TITLE}}`：「[學生姓名]同學之大專生研究計畫之預期目標」
- `{{SEC2_SUB3_CONTENT}}`：
  - 具體的研究方法和技術框架
  - 分階段的實驗計畫
  - 預期投稿的會議

#### 第三節：指導方式（中文）

- `{{SEC3_CONTENT}}`：描述指導方式（每週 meeting、論文閱讀、專家指導等）
- `{{SEC3_ITEM1}}` 至 `{{SEC3_ITEM5}}`：預期指導項目的條列式項目

#### 第四節（固定文字，不需修改）

「本人同意指導學生瞭解並遵守執行計畫須符合學術倫理及研究倫理規範。」

- `{{簽名日期}}`：格式為「YYYY 年  M 月  DD 日」（注意年月日之間用兩個空格）

### 第三步：填入範本並輸出

```bash
# 1. 複製範本
cp assets/template.docx working.docx

# 2. Unpack
python <docx-skill>/scripts/office/unpack.py working.docx unpacked/

# 3. 編輯 XML —— 替換佔位符
#    在 unpacked/word/document.xml 中替換 {{佔位符}}

# 4. Repack
python <docx-skill>/scripts/office/pack.py unpacked/ output.docx --original working.docx

# 5. 轉 PDF 驗證
python <docx-skill>/scripts/office/soffice.py --headless --convert-to pdf output.docx --outdir .
```

## 範本佔位符一覽

| 佔位符 | 說明 | 語言 |
|--------|------|------|
| `{{SEC1_PARA1}}` | 英文推薦信第一段：開頭介紹 | EN |
| `{{SEC1_BOLD1}}` | 粗體強調文字 | EN |
| `{{SEC1_PARA2}}` | 英文推薦信第二段：學業表現 | EN |
| `{{SEC1_PARA3}}` | 英文推薦信第三段：課外經歷 | EN |
| `{{SEC1_PARA4}}` | 英文推薦信第四段：推薦結語 | EN |
| `{{SEC1_PARA5}}` | 英文推薦信第五段：結尾 | EN |
| `{{SEC2_SUB1_TITLE}}` | 子段1標題 | ZH |
| `{{SEC2_SUB1_CONTENT}}` | 資源提供與經驗指導 | ZH |
| `{{SEC2_SUB2_TITLE}}` | 子段2標題 | ZH |
| `{{SEC2_SUB2_CONTENT}}` | 研究計畫背景概述 | ZH |
| `{{SEC2_SUB3_TITLE}}` | 子段3標題 | ZH |
| `{{SEC2_SUB3_CONTENT}}` | 預期目標 | ZH |
| `{{SEC3_CONTENT}}` | 指導方式正文 | ZH |
| `{{SEC3_ITEM1}}` ~ `{{SEC3_ITEM5}}` | 指導項目（5項） | ZH |
| `{{簽名日期}}` | 簽名日期 | — |

## 技術注意事項

- 使用 unpack→edit→repack 流程，不要從頭生成 DOCX
- 新增段落時 paraId 必須 < 0x80000000
- 英文字體為 Times New Roman 12pt，中文字體為標楷體
- 內文段落有首行縮排 `firstLine="480"` 和兩端對齊 `jc="both"`
- 英文推薦信中提到 NSTC 和重要機構名稱時可用粗體
- 條列項目使用 bullet list 格式（範本已含格式設定）

## 李教授實驗室常用資訊（供參考）

以下是李濬屹教授實驗室的常用資訊，可在撰寫第二節時引用：

**研究領域：**
1. 機器學習與電腦視覺 (Machine Learning and Computer Vision)
2. 深度增強式學習 (Deep Reinforcement Learning)
3. 數位孿生 (Digital Twins)
4. 平行計算與平行處理系統 (Parallel Computing and Parallel Processing Systems)
5. 智慧型機器人 (Intelligent Robotics)

**國際發表紀錄（頂尖會議/期刊）：**
NeurIPS、ICLR、ICML、AAMAS、CVPR、ECCV、BMVC、WACV、IJCAI、CoRL、ICRA、IROS、ICCD、DAC、ASP-DAC、GTC、ACM TELO、IEEE TPAMI、JMLR、IEEE TCAD

**獲獎紀錄（可選用）：**
- 2024 The Third Place at AMD Pervasive AI Developer Contest: Robotics AI Track
- 2024 Best Solution Award (1st Place) at Small Object Detection Challenge for Spotting Birds held by MVA 2023
- 2020 NVIDIA AI at the Edge Challenge 世界第二名
- 2018 NVIDIA Jetson Robotics Challenge 世界冠軍
- 2018 ECCV Person In Context Challenge 世界第二名
- 2016 NVIDIA Embedded Intelligent Robotics Challenge 全國冠軍
