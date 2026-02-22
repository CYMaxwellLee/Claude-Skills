#!/usr/bin/env python3
"""
國科會出國差旅報告生成腳本
Fill the golden template DOCX with conference-specific content.

Usage:
    python fill_template.py <config.json> <template.docx> <output.docx>

The config.json should contain all the placeholder values.
See SKILL.md for the full config schema.
"""

import json
import sys
import os
import re
import shutil
import subprocess
import tempfile


def find_docx_tools():
    """Find the docx unpack/pack tools."""
    # Look for the docx skill's pack/unpack scripts
    candidates = [
        '/sessions/great-affectionate-johnson/mnt/.skills/skills/docx/scripts/office',
        os.path.expanduser('~/.skills/skills/docx/scripts/office'),
    ]
    for path in candidates:
        if os.path.exists(os.path.join(path, 'pack.py')):
            return path
    return None


def unpack_docx(docx_path, unpack_dir, tools_dir):
    """Unpack a DOCX file to a directory."""
    result = subprocess.run(
        ['python', os.path.join(tools_dir, 'unpack.py'), docx_path, unpack_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR unpacking: {result.stderr}")
        sys.exit(1)
    print(f"Unpacked: {result.stdout.strip()}")


def pack_docx(unpack_dir, output_path, original_path, tools_dir):
    """Pack an unpacked directory back to DOCX."""
    result = subprocess.run(
        ['python', os.path.join(tools_dir, 'pack.py'),
         unpack_dir, output_path, '--original', original_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR packing: {result.stderr}")
        sys.exit(1)
    print(f"Packed: {result.stdout.strip()}")


def fill_placeholders(xml_content, config):
    """Replace {{PLACEHOLDER}} markers with actual values from config."""
    replacements = {
        '{{報告日期}}': config.get('報告日期', ''),
        '{{計畫編號}}': config.get('計畫編號', ''),
        '{{計畫名稱}}': config.get('計畫名稱', ''),
        '{{出國人員姓名}}': config.get('出國人員姓名', ''),
        '{{服務機構及職稱}}': config.get('服務機構及職稱', ''),
        '{{會議起始日}}': config.get('會議起始日', ''),
        '{{會議結束日}}': config.get('會議結束日', ''),
        '{{會議地點}}': config.get('會議地點', ''),
        '{{會議中文名稱}}': config.get('會議中文名稱', ''),
        '{{會議英文名稱}}': config.get('會議英文名稱', ''),
        '{{會議簡稱}}': config.get('會議簡稱', ''),
        '{{論文中文題目}}': config.get('論文中文題目', ''),
        '{{論文英文題目}}': config.get('論文英文題目', ''),
        '{{論文作者與摘要}}': config.get('論文作者與摘要', ''),
        '{{照片說明}}': config.get('照片說明', ''),
    }

    # Body section placeholders
    body = config.get('body', {})

    sec1 = body.get('參加會議經過', {})
    replacements.update({
        '{{SEC1_會議簡介}}': sec1.get('會議簡介', ''),
        '{{SEC1_TUTORIAL日期標題}}': sec1.get('tutorial日期標題', ''),
        '{{SEC1_TUTORIAL內容}}': sec1.get('tutorial內容', ''),
        '{{SEC1_主會議日期標題}}': sec1.get('主會議日期標題', ''),
        '{{SEC1_主會議內容}}': sec1.get('主會議內容', ''),
        '{{SEC1_WORKSHOP日期標題}}': sec1.get('workshop日期標題', ''),
        '{{SEC1_WORKSHOP標題}}': sec1.get('workshop標題', '參加Workshops'),
        '{{SEC1_WORKSHOP內容}}': sec1.get('workshop內容', ''),
    })

    sec2 = body.get('與會心得', {})
    for i in range(1, 7):
        key = f'心得段落{i}'
        replacements[f'{{{{SEC2_心得段落{i}}}}}'] = sec2.get(key, '')

    replacements['{{SEC2_重要論文標題}}'] = sec2.get('重要論文標題', '')
    replacements['{{SEC2_重要論文引言}}'] = sec2.get('重要論文引言', '')
    for i in range(1, 5):
        key = f'論文{i}'
        replacements[f'{{{{SEC2_論文{i}}}}}'] = sec2.get(key, '')

    sec4 = body.get('建議', {})
    for i in range(1, 6):
        key = f'建議{i}'
        replacements[f'{{{{SEC4_建議{i}}}}}'] = sec4.get(key, '')
    replacements['{{SEC4_建議4標題}}'] = sec4.get('建議4標題', '')

    sec5 = body.get('攜回資料', {})
    replacements['{{SEC5_攜回資料1}}'] = sec5.get('攜回資料1', '')
    replacements['{{SEC5_攜回資料2}}'] = sec5.get('攜回資料2', '')

    # Do the replacements
    filled_count = 0
    missing = []
    for placeholder, value in replacements.items():
        if placeholder in xml_content:
            if value:
                xml_content = xml_content.replace(placeholder, value)
                filled_count += 1
            else:
                missing.append(placeholder)

    print(f"Filled {filled_count} placeholders")
    if missing:
        print(f"WARNING: {len(missing)} placeholders still empty: {', '.join(missing)}")

    return xml_content


def main():
    if len(sys.argv) < 4:
        print("Usage: python fill_template.py <config.json> <template.docx> <output.docx>")
        sys.exit(1)

    config_path = sys.argv[1]
    template_path = sys.argv[2]
    output_path = sys.argv[3]

    # Load config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Find tools
    tools_dir = find_docx_tools()
    if not tools_dir:
        print("ERROR: Cannot find docx pack/unpack tools")
        sys.exit(1)

    # Create working directory
    work_dir = tempfile.mkdtemp(prefix='nstc_report_')
    unpack_dir = os.path.join(work_dir, 'unpacked')

    try:
        # Unpack template
        unpack_docx(template_path, unpack_dir, tools_dir)

        # Read XML
        xml_path = os.path.join(unpack_dir, 'word', 'document.xml')
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fill placeholders
        content = fill_placeholders(content, config)

        # Run Taiwan terminology check
        script_dir = os.path.dirname(os.path.abspath(__file__))
        taiwan_terms_path = os.path.join(script_dir, 'taiwan_terms.py')
        if os.path.exists(taiwan_terms_path):
            # Import and use directly
            sys.path.insert(0, script_dir)
            from taiwan_terms import check_and_fix
            content, changes, warnings = check_and_fix(content)
            if changes:
                print("台灣用語修正:")
                for c in changes:
                    print(f"  ✓ {c}")
            if warnings:
                for w in warnings:
                    print(f"  ⚠ {w}")

        # Write back
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Pack
        pack_docx(unpack_dir, output_path, template_path, tools_dir)
        print(f"\n✓ Report generated: {output_path}")

    finally:
        # Cleanup
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
