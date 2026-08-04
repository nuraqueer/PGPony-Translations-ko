#!/usr/bin/env python3
"""Report translation coverage per language for all three platforms.

For iOS, counts how many source strings lack a translation for each language.
For Android/desktop, counts how many keys in the English base file are missing
(or identical to English) in each language file.
"""
import json, os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_xml(path):
    out = {}
    for node in ET.parse(path).getroot():
        if node.tag == 'string' and node.get('name'):
            out[node.get('name')] = ''.join(node.itertext())
    return out

print('=== iOS (ios/Localizable.xcstrings) ===')
ios = os.path.join(ROOT, 'ios', 'Localizable.xcstrings')
if os.path.exists(ios):
    cat = json.load(open(ios, encoding='utf-8'))
    strings = cat.get('strings', {})
    langs = set()
    for e in strings.values():
        if isinstance(e, dict):
            langs.update(e.get('localizations', {}))
    langs.discard('en')
    total = len(strings)
    for lang in sorted(langs):
        have = sum(1 for e in strings.values()
                   if isinstance(e, dict) and lang in e.get('localizations', {}))
        print(f'  {lang:8} {have}/{total}   missing {total-have}')

for platform in ('android', 'desktop'):
    base = os.path.join(ROOT, platform, 'values', 'strings.xml')
    if not os.path.exists(base):
        continue
    print(f'=== {platform} ({platform}/values-<lang>/strings.xml) ===')
    src = load_xml(base)
    total = len(src)
    pdir = os.path.join(ROOT, platform)
    for d in sorted(os.listdir(pdir)):
        if not d.startswith('values-'):
            continue
        f = os.path.join(pdir, d, 'strings.xml')
        if not os.path.exists(f):
            continue
        lang = d[len('values-'):]
        tr = load_xml(f)
        missing = sum(1 for k, v in src.items() if k not in tr or tr[k] == v)
        print(f'  {lang:8} {total-missing}/{total}   missing/untranslated {missing}')
