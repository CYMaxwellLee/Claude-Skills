#!/usr/bin/env python3
"""
台灣用語檢查與修正工具
Check and fix China-specific terminology → Taiwan/ROC terminology.
For use in 國科會 (NSTC) official reports.
"""

# China term → Taiwan term mapping
TERM_MAP = {
    '信息': '資訊',
    '人工智能': '人工智慧',
    '視頻': '影片',
    '軟件': '軟體',
    '硬件': '硬體',
    '網絡': '網路',
    '激光': '雷射',
    '打印': '列印',
    '程序': '程式',  # context-dependent, but usually correct
    '算法': '演算法',
    '服務器': '伺服器',
    '數據庫': '資料庫',
    '數據集': '資料集',
    '數據': '資料',   # careful: 數據 is sometimes OK in Taiwan for "data"
    '存儲': '儲存',
    '內存': '記憶體',
    '芯片': '晶片',
    '優化': '最佳化',  # context-dependent
    '自回歸': '自迴歸',
    '增長': '成長',   # in data context
    '博客': '部落格',
    '上傳': '上傳',   # same in Taiwan, no change needed
    '下載': '下載',   # same in Taiwan, no change needed
}

# Terms that are fine in Taiwan (no change needed) - for reference
TAIWAN_OK = ['回饋', '部署', '社群', '下載', '上傳', '存取']

# Terms that need careful context checking
CONTEXT_SENSITIVE = {
    '數據': '資料',     # Sometimes 數據 is OK in scientific context
    '優化': '最佳化',   # 優化 is actually commonly used in Taiwan too
    '程序': '程式',     # 程序 can mean "procedure" which is OK
}

# Safe replacements (always replace these)
SAFE_REPLACEMENTS = {
    '信息': '資訊',
    '人工智能': '人工智慧',
    '視頻': '影片',
    '軟件': '軟體',
    '硬件': '硬體',
    '激光': '雷射',
    '打印': '列印',
    '算法': '演算法',
    '服務器': '伺服器',
    '數據庫': '資料庫',
    '數據集': '資料集',
    '存儲': '儲存',
    '內存': '記憶體',
    '芯片': '晶片',
    '自回歸': '自迴歸',
    '博客': '部落格',
}


def check_and_fix(text, auto_fix=True):
    """
    Check text for China-specific terms and optionally fix them.

    Args:
        text: The text to check
        auto_fix: If True, automatically replace safe terms

    Returns:
        tuple: (fixed_text, list_of_changes, list_of_warnings)
    """
    changes = []
    warnings = []

    # Auto-fix safe replacements
    if auto_fix:
        for china_term, taiwan_term in SAFE_REPLACEMENTS.items():
            count = text.count(china_term)
            if count > 0:
                text = text.replace(china_term, taiwan_term)
                changes.append(f"'{china_term}' → '{taiwan_term}' ({count}處)")

    # Warn about context-sensitive terms
    for china_term, taiwan_term in CONTEXT_SENSITIVE.items():
        count = text.count(china_term)
        if count > 0:
            warnings.append(
                f"發現 '{china_term}' {count}處 (建議替換為 '{taiwan_term}'，但需確認上下文)"
            )

    return text, changes, warnings


def check_xml_file(xml_path, auto_fix=True):
    """Check and fix a DOCX XML file for China-specific terms."""
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content, changes, warnings = check_and_fix(content, auto_fix)

    if auto_fix and changes:
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes, warnings


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python taiwan_terms.py <xml_path> [--check-only]")
        sys.exit(1)

    xml_path = sys.argv[1]
    auto_fix = '--check-only' not in sys.argv

    changes, warnings = check_xml_file(xml_path, auto_fix)

    if changes:
        print("已修正：")
        for c in changes:
            print(f"  ✓ {c}")
    else:
        print("✓ 未發現需要修正的中國用語")

    if warnings:
        print("\n需確認（可能需要依上下文判斷）：")
        for w in warnings:
            print(f"  ⚠ {w}")
