#!/usr/bin/env python3
"""Generate a 4-column review/translation sheet for one language.

Usage:
    python3 tools/make_review_tsv.py <platform> <lang> [out.tsv]

    platform : ios | android | desktop
    lang     : language code as used in this repo
               (ios: ru, de, ja, zh-Hans ... ; android/desktop: de, es, pt-rBR ...)

Columns (tab-separated): English  Translation  Context  Changes

  English      the source string (do not edit)
  Translation  the current translation, or blank if none exists yet
  Context      a hint about where/how the string is used
  Changes      LEFT BLANK for the translator: put corrections or notes here

Fill in "Translation" for empty rows, or write a fix in "Changes" for rows that
already have a translation. Send the finished sheet back and a maintainer merges
it. Open the file in any spreadsheet app (Numbers, Excel, LibreOffice, Sheets)
and keep the tab-separated format when you save.
"""
import csv, json, os, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rows_ios(lang):
    cat = json.load(open(os.path.join(ROOT, 'ios', 'Localizable.xcstrings'), encoding='utf-8'))
    out = []
    for key, entry in cat.get('strings', {}).items():
        if not isinstance(entry, dict):
            continue
        loc = entry.get('localizations', {})
        en = key
        if 'en' in loc and 'stringUnit' in loc['en']:
            en = loc['en']['stringUnit']['value']
        ctx = entry.get('comment', '')
        unit = loc.get(lang)
        if not unit:
            out.append([en, '', ctx, ''])
        elif 'stringUnit' in unit:
            out.append([en, unit['stringUnit']['value'], ctx, ''])
        elif 'variations' in unit:
            for cat_name, u in unit['variations'].get('plural', {}).items():
                out.append([f'{en}  [{cat_name}]', u['stringUnit']['value'],
                            (ctx or 'plural'), ''])
    return out

def load_xml(path):
    out = {}
    for node in ET.parse(path).getroot():
        if node.tag == 'string' and node.get('name'):
            out[node.get('name')] = ''.join(node.itertext())
    return out

def rows_androidlike(platform, lang):
    base = load_xml(os.path.join(ROOT, platform, 'values', 'strings.xml'))
    tr_path = os.path.join(ROOT, platform, f'values-{lang}', 'strings.xml')
    tr = load_xml(tr_path) if os.path.exists(tr_path) else {}
    out = []
    for name, en in base.items():
        cur = tr.get(name, '')
        if cur == en:
            cur = ''  # same as English means untranslated
        out.append([en, cur, name, ''])
    return out

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    platform, lang = sys.argv[1], sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else f'PGPony_{platform}_{lang}_review.tsv'
    if platform == 'ios':
        rows = rows_ios(lang)
    elif platform in ('android', 'desktop'):
        rows = rows_androidlike(platform, lang)
    else:
        print(f'unknown platform: {platform}')
        sys.exit(1)
    rows = [r for r in rows if r[0].strip()]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['English', 'Translation', 'Context', 'Changes'])
        w.writerows(rows)
    print(f'wrote {out_path}  ({len(rows)} rows)')

if __name__ == '__main__':
    main()
