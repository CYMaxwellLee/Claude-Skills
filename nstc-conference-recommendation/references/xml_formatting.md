# DOCX XML Formatting Reference for Recommendation Letters

## Red Bold Text (for conference names, paper titles, key awards)

To make text red bold (color #941100), use this run format:
```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Times Roman" w:hAnsi="Times Roman"/>
    <w:b w:val="1"/>
    <w:bCs w:val="1"/>
    <w:outline w:val="0"/>
    <w:color w:val="941100"/>
    <w:sz w:val="22"/>
    <w:szCs w:val="22"/>
    <w:rtl w:val="0"/>
    <w14:textFill>
      <w14:solidFill>
        <w14:srgbClr w14:val="941100"/>
      </w14:solidFill>
    </w14:textFill>
  </w:rPr>
  <w:t>TEXT HERE</w:t>
</w:r>
```

## Regular Bold Text (for grant names, venue names)

```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Times Roman" w:hAnsi="Times Roman"/>
    <w:b w:val="1"/>
    <w:bCs w:val="1"/>
    <w:sz w:val="22"/>
    <w:szCs w:val="22"/>
    <w:rtl w:val="0"/>
    <w:lang w:val="en-US"/>
  </w:rPr>
  <w:t>TEXT HERE</w:t>
</w:r>
```

## Chinese Text (for student Chinese name, award Chinese name)

```xml
<w:r>
  <w:rPr>
    <w:rFonts w:eastAsia="標楷體-繁" w:hint="eastAsia"/>
    <w:sz w:val="22"/>
    <w:szCs w:val="22"/>
    <w:rtl w:val="0"/>
    <w:lang w:val="zh-TW" w:eastAsia="zh-TW"/>
  </w:rPr>
  <w:t>中文內容</w:t>
</w:r>
```

## Regular English Text

```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Times Roman" w:hAnsi="Times Roman"/>
    <w:sz w:val="22"/>
    <w:szCs w:val="22"/>
    <w:rtl w:val="0"/>
    <w:lang w:val="en-US"/>
  </w:rPr>
  <w:t>TEXT HERE</w:t>
</w:r>
```

## Date Format (right-aligned, with superscript ordinal)

The date line has three runs:
1. Month + day number (e.g., "Feb. 22")
2. Ordinal suffix in superscript (e.g., "nd") — uses `<w:vertAlign w:val="superscript"/>`
3. Year (e.g., ", 2026")

Ordinal rules: 1st, 2nd, 3rd, 4th-20th, 21st, 22nd, 23rd, 24th-30th, 31st

## Known XML Pitfalls

1. **paraId validation**: Any new paragraphs must have paraId < 0x80000000. Use values like "1A000001", "1B000002", etc.

2. **Run splitting**: Text that appears continuous in Word may be split across multiple `<w:r>` runs in XML. When replacing text, always check the XML structure first — don't assume text is in a single run.

3. **xml:space="preserve"**: Any `<w:t>` with leading/trailing spaces MUST have `xml:space="preserve"` attribute, or the spaces will be stripped.

4. **Smart quotes**: Left quote = `&#x201C;`, right quote = `&#x201D;`. These are in separate runs from the quoted text.

5. **Color consistency**: Always use both `<w:color w:val="941100"/>` AND `<w14:textFill><w14:solidFill><w14:srgbClr w14:val="941100"/></w14:solidFill></w14:textFill>` for red text. Missing either can cause inconsistent rendering.

6. **Font names**: Body text uses "Times Roman" (not "Times New Roman"). Header/footer uses "Times New Roman". These are different fonts in the DOCX.
