# DOCX XML 編輯踩坑筆記

這份文件記錄了在編輯國科會差旅報告 DOCX 時遇到的所有問題和解法。

## 核心原則：絕對不要用 docx-js 從頭生成

用 JavaScript 的 docx-js 套件從頭生成 DOCX 會導致字型、排版、行距全壞。正確做法是：
1. 以一份格式正確的範本 DOCX 為基底
2. Unpack → 編輯 XML → Repack
3. 這樣可以完美保留原本的格式設定

## 文字被拆散到多個 XML run

DOCX 的 XML 裡，一段看似連續的文字常常被拆成多個 `<w:r>` (run) 元素。例如：
```xml
<w:r><w:t>NeurIPS 20</w:t></w:r>
<w:r><w:t>25</w:t></w:r>
```
**解法**：
- 不能用簡單的 `str.replace()`，要用 regex 匹配 `<w:t>` 標籤內的文字前綴
- 或者在 unpack 時使用 `--merge-runs` 選項（docx skill 的 unpack.py 會自動合併）
- 最佳解法：使用預先設計好的佔位符（如 `{{計畫編號}}`），這些短標記不會被拆散

## paraId 必須小於 0x80000000

新增段落時給的 `w14:paraId` 值必須小於 `0x80000000`，否則 pack.py 驗證會失敗。
- ❌ `paraId="AA000001"` (A > 7)
- ✓ `paraId="1A000001"` (1 < 8)

## LibreOffice 轉 PDF 的正確方式

不能直接呼叫 `soffice --headless`，要用 docx skill 提供的 wrapper：
```bash
python mnt/.skills/skills/docx/scripts/office/soffice.py --headless --convert-to pdf file.docx --outdir /output/
```

## 報告格式的 XML 結構

### 字型設定
```xml
<w:rFonts w:eastAsia="標楷體-繁"/>
<w:szCs w:val="22"/>
```

### 內文段落（兩端對齊 + 首行縮排）
```xml
<w:pPr>
  <w:ind w:firstLineChars="200" w:firstLine="480"/>
  <w:jc w:val="both"/>
</w:pPr>
```

### 粗體子標題
```xml
<w:rPr>
  <w:rFonts w:eastAsia="標楷體-繁"/>
  <w:b/>
  <w:szCs w:val="22"/>
</w:rPr>
```

### 章節標題（帶編號）
使用 `<w:numPr>` 搭配 `numId="9"`

### 表格欄寬
四欄：1620, 2770, 1701, 4457 DXA，部分儲存格跨三欄

## 民國年轉換

| 西元年 | 民國年 |
|--------|--------|
| 2024   | 113年  |
| 2025   | 114年  |
| 2026   | 115年  |

公式：民國年 = 西元年 - 1911

## 中國用語 vs 台灣用語（常見對照）

| 中國用語 | 台灣用語 |
|----------|----------|
| 信息     | 資訊     |
| 人工智能 | 人工智慧 |
| 視頻     | 影片     |
| 軟件     | 軟體     |
| 硬件     | 硬體     |
| 算法     | 演算法   |
| 自回歸   | 自迴歸   |
| 數據集   | 資料集   |
| 服務器   | 伺服器   |
| 芯片     | 晶片     |
| 存儲     | 儲存     |
| 內存     | 記憶體   |

注意：「數據」在台灣學術文章中有時可用，但「資料」更正式。「優化」在台灣也常用，不一定要改成「最佳化」。

## 完整工作流程

```
1. 複製 template.docx
2. python unpack.py template.docx unpacked/
3. 編輯 unpacked/word/document.xml
   - 替換 {{佔位符}} → 實際值
   - 執行 taiwan_terms.py 檢查用語
4. python pack.py unpacked/ output.docx --original template.docx
5. 用 soffice.py 轉 PDF 驗證
6. 用 pdftoppm 轉圖片做視覺確認
```
