---
name: nstc-conference-recommendation
description: |
  國科會「補助國內研究生出席國際學術會議」指導教授推薦信自動生成工具。
  使用已驗證的 DOCX 範本（NTU 信頭、標楷體+Times New Roman），透過 unpack→編輯XML→repack 流程產生格式完美的推薦信。
  當使用者提到「推薦信」、「出席國際學術會議」、「研究生出國補助」、「conference travel grant」、「recommendation letter」時觸發此技能。
  也適用於使用者說「幫某某學生寫推薦信去 CVPR/NeurIPS/ICML/ICLR/AAAI」、「國科會出國補助推薦信」、「寫推薦信讓學生出國開會」等情境。
  注意：此技能專用於「補助國內研究生出席國際學術會議」推薦信，不適用於獎學金推薦信或入學推薦信。
---

# 國科會研究生出席國際學術會議 — 指導教授推薦信

## 概述

本技能用於快速產生國科會「補助國內研究生出席國際學術會議」的指導教授推薦信。
推薦信以 NTU CSIE Prof. Chun-Yi Lee 的信紙格式為基礎，使用 unpack→edit XML→repack 工作流程確保格式零損壞。

## 資訊收集

在開始之前，需要以下資訊（通常可從使用者提供的 CV、論文、自傳中提取）：

### 必要資訊
| 項目 | 說明 | 範例 |
|------|------|------|
| 學生英文名 | Full name | Yan-Ting Chen |
| 學生中文名 | 中文全名 | 陳彥廷 |
| 會議名稱 | 全名 + 縮寫 | IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) |
| 會議年份 | | 2026 |
| 會議地點 | 城市, 州/國家 | Nashville, Tennessee, USA |
| 會議月份 | | June 2026 |
| 論文標題 | 被接受的論文 | Landscape-Awareness for Geometric View Diffusion Model |
| 作者身份 | 第一作者/共同作者 | first author |

### 從 CV/自傳/論文提取
| 項目 | 說明 |
|------|------|
| 學歷 | 大學校系、畢業名次/榮譽 |
| 重要獎項 | 如梅貽琦獎章等（會標紅色粗體） |
| 課外活動 | 競賽、社團、國際經驗 |
| 研究方向 | 加入實驗室後的研究主題 |
| 先前發表 | 已發表的其他論文（標題、會議、地點、日期） |
| 技術能力 | 程式語言、框架、專長 |
| 論文技術貢獻 | 從論文 PDF 提取核心貢獻摘要 |

## 工作流程

### Step 1: 讀取範本並解壓

```bash
# 複製範本到工作目錄
cp <skill-path>/assets/template.docx <workdir>/base.docx

# 解壓
python <docx-skill-path>/scripts/office/unpack.py <workdir>/base.docx <workdir>/unpacked/
```

其中 `<docx-skill-path>` 是 docx skill 的路徑（通常在 `mnt/.skills/skills/docx`）。

### Step 2: 讀取並理解 XML 結構

```bash
# 讀取 document.xml
cat <workdir>/unpacked/word/document.xml
```

理解範本中的段落結構。參考 `references/example_陳彥廷.txt` 了解 9 段式推薦信結構。

### Step 3: 寫 Python 編輯腳本

撰寫一個 Python 腳本（如 `edit_letter.py`）來修改 `document.xml`。腳本應做以下替換：

#### 3a. 簡單文字替換（直接 string replace）
- 日期：`Feb. 22` → 新日期（月.日）, `, 2026` → `, YYYY`
- 序數後綴：`>nd<` → `>st<` 或 `>rd<` 或 `>th<`（視日期而定）
- 學生英文名：`Yan-Ting Chen` → 新名字（注意所有出現位置）
- 學生中文名：`陳彥廷` → 新中文名
- 名字暱稱：`Yan-Ting` → 新名字的 first name（出現非常多次，要全部替換）
- Grant 名稱不需改（都是 "NSTC Graduate Student International Conference Travel Grant"）

#### 3b. 需要理解上下文的替換
- 會議名稱：所有 `CVPR 2026` → 新會議名稱+年份
- 會議全名：`IEEE/CVF Conference on Computer Vision and Pattern Recognition` → 新會議全名
- 會議地點：`Nashville, Tennessee, USA, in June 2026` → 新地點+月份
- 研究領域描述：`computer vision and diffusion models` → 新領域
- 大學背景：整段需要根據學生資料重寫
- 獎項：紅色粗體部分需要替換為新學生的獎項
- 先前發表：論文標題、會議名稱、技術描述全部重寫
- 主要論文段落：技術貢獻描述需要根據新論文重寫
- 個人特質段落：根據新學生的特點調整

#### 3c. 整段重寫的處理方式

對於需要整段重寫的段落（如學術背景、研究成果、論文技術貢獻），在 Python 腳本中用 `content.replace(old_text, new_text)` 替換**整個 `<w:t>` 元素的文字內容**。

重要：不要試圖修改 XML 標籤結構，只替換 `<w:t>` 和 `</w:t>` 之間的文字。這樣可以保留所有格式屬性。

#### 3d. 插入新的紅色粗體文字

如果需要在原本不是紅色的文字中插入紅色粗體的會議名稱，需要：
1. 將原本的長 `<w:t>` 文字拆成三段
2. 中間插入紅色粗體的 `<w:r>` 區塊

參考 `references/xml_formatting.md` 中的 XML 模板。

### Step 4: 執行編輯腳本

```bash
python edit_letter.py
```

### Step 5: 驗證

```bash
# 檢查是否有殘留的舊內容
grep -c "Yan-Ting\|陳彥廷\|CVPR 2026" <workdir>/unpacked/word/document.xml

# 應該全部是 0（除非新學生也是這些內容）
```

### Step 6: 重新打包

```bash
python <docx-skill-path>/scripts/office/pack.py \
  <workdir>/unpacked/ \
  "<output-path>/推薦信.docx" \
  --original <workdir>/base.docx
```

### Step 7: 轉 PDF 驗證

```bash
python <docx-skill-path>/scripts/office/soffice.py \
  --headless --convert-to pdf \
  "<output-path>/推薦信.docx" \
  --outdir <workdir>/

pdftoppm -jpeg -r 150 "<workdir>/推薦信.pdf" <workdir>/verify
```

然後用 Read tool 讀取每一頁 JPG 圖片，仔細檢查：
- 格式是否正確（信頭、字體、間距）
- 所有學生姓名是否已替換
- 會議名稱是否為紅色粗體
- 關鍵獎項是否為紅色粗體
- 日期是否正確（含序數後綴）
- 所有句子結尾是否有句號
- 無殘留的範例學生資料

## 推薦信寫作風格指南

### Prof. Lee 的寫作特點
- 正式學術英文，語調溫暖但專業
- 大量使用具體細節（數字、排名、具體成果）
- 每段有明確的主題句
- 重要成就用粗體或紅色粗體強調
- 論文技術描述要夠深入，展現教授對學生研究的理解
- 結尾語氣堅定："without any reservation"

### 紅色粗體（#941100）使用規則
以下項目應為紅色粗體：
- 會議名稱 + 年份（如 CVPR 2026）— 每次出現都要
- 論文標題（在引號內）
- 重要獎項名稱（如梅貽琦獎章）

### 一般粗體使用規則
以下項目應為一般粗體（黑色）：
- Grant 名稱（"the NSTC Graduate Student International Conference Travel Grant"）
- 會議 venue 名稱（如 "the 19th International Conference on Machine Vision Applications (MVA)"）
- 研究方向描述（如 "diffusion models and their applications to computer vision problems"）

### 避免的常見錯誤
1. 句號遺漏：尤其是粗體文字後面容易漏掉句號
2. "the" 的使用：Grant 名稱前要加 "the"
3. 重複句子：不同段落不要出現幾乎相同的句子
4. "research works" 是錯誤用法，應為 "research"
5. 日期序數：22nd（不是 22th），1st, 2nd, 3rd, 4th...
6. 同一短語不要在相鄰段落重複出現（如 "cutting-edge research"）

## 實驗室資訊（可用於推薦信內容）

- 教授：李濬屹 (Chun-Yi Lee)
- 職稱：Professor of Computer Science and Information Engineering, National Taiwan University
- 系所：Department of Computer Science and Information Engineering, NTU
- 地址：No. 1, Sec. 4, Roosevelt Rd., Taipei 106319, Taiwan
- 電話：(02) 33664888 ext. 510
- Email: cylee@csie.ntu.edu.tw
- 研究方向：Computer Vision, Machine Learning, Deep Learning, Diffusion Models, Embodied AI

## 檔案結構

```
nstc-conference-recommendation/
├── SKILL.md                              # 本文件
├── assets/
│   └── template.docx                     # 黃金範本（陳彥廷版本，已驗證格式正確）
└── references/
    ├── example_陳彥廷.txt                  # 範例推薦信結構分析
    └── xml_formatting.md                  # XML 格式模板（紅字、粗體、中文等）
```
