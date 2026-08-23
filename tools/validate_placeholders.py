#!/usr/bin/env python3
"""Validate that every translation preserves its source placeholders.

Covers all three platforms:
  ios/Localizable.xcstrings          (Apple String Catalog, keyed by English)
  android/values-<lang>/strings.xml  (compared against android/values/strings.xml)
  desktop/values-<lang>/strings.xml  (compared against desktop/values/strings.xml)

Placeholders are compared by conversion TYPE and COUNT, ignoring the position
index. That means "%@ %@" and "%1$@ %2$@" are treated as equal (both are two
'@' arguments), which is allowed and encouraged for reordering languages, but
a dropped, added, or type-changed placeholder is reported as an error.

Exit code is non-zero if any mismatch is found.
"""
import json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# %[position$][flags][width][.prec](conversion)
PH = re.compile(r'%(?:(\d+)\$)?[-+ 0#]?\d*(?:\.\d+)?(ll|l|h|hh|z|j|t|L)?([@dioumxXeEfFgGaAcspn%])')

def types(s):
    """Multiset of placeholder types, position-independent. '%%' is ignored."""
    out = []
    for m in PH.finditer(s):
        conv = m.group(3)
        if conv == '%':      # literal percent
            continue
        length = m.group(2) or ''
        out.append(length + conv)
    return sorted(out)

errors = []

# ---------- iOS ----------
ios = os.path.join(ROOT, 'ios', 'Localizable.xcstrings')
if os.path.exists(ios):
    cat = json.load(open(ios, encoding='utf-8'))
    for key, entry in cat.get('strings', {}).items():
        if not isinstance(entry, dict):
            continue
        loc = entry.get('localizations', {})
        # source placeholders come from the English key (or an en override)
        src = key
        en = loc.get('en')
        if en and 'stringUnit' in en:
            src = en['stringUnit']['value']
        want = types(src)
        for lang, unit in loc.items():
            if lang == 'en':
                continue
            vals = []
            if 'stringUnit' in unit:
                vals.append(unit['stringUnit']['value'])
            elif 'variations' in unit:
                for cat_name, u in unit['variations'].get('plural', {}).items():
                    vals.append(u['stringUnit']['value'])
            for v in vals:
                if types(v) != want:
                    errors.append(f'iOS [{lang}] {key!r}: source {want} != {types(v)}')

# ---------- Android / Desktop ----------
def load_xml(path):
    out = {}
    tree = ET.parse(path)
    for node in tree.getroot():
        if node.tag == 'string' and node.get('name'):
            out[node.get('name')] = ''.join(node.itertext())
        elif node.tag == 'plurals' and node.get('name'):
            for item in node:
                out[(node.get('name'), item.get('quantity'))] = ''.join(item.itertext())
    return out

for platform in ('android', 'desktop'):
    base = os.path.join(ROOT, platform, 'values', 'strings.xml')
    if not os.path.exists(base):
        continue
    src_map = load_xml(base)
    pdir = os.path.join(ROOT, platform)
    for d in sorted(os.listdir(pdir)):
        if not d.startswith('values-'):
            continue
        f = os.path.join(pdir, d, 'strings.xml')
        if not os.path.exists(f):
            continue
        lang = d[len('values-'):]
        tr = load_xml(f)
        for name, val in tr.items():
            base_name = name[0] if isinstance(name, tuple) else name
            if base_name not in src_map and name not in src_map:
                continue  # extra key; not our job here
            src = src_map.get(name, src_map.get(base_name, ''))
            # Accepted placeholder sets for this value. Normally just the matching
            # source form. For a PLURAL item we also accept the canonical 'other'
            # form's placeholders: per GLOSSARY.md, a language's 'one'/'few'/'many'
            # form must still carry the count placeholder even when English hard-
            # codes the number (English "One key needs regenerating" has none, but
            # Russian's 'one' category covers 1, 21, 31 ... and must show "%1$d").
            allowed = {tuple(types(src))}
            if isinstance(name, tuple):
                other = src_map.get((base_name, 'other'))
                if other is not None:
                    allowed.add(tuple(types(other)))
            if tuple(types(val)) not in allowed:
                exp = ' or '.join(str(list(a)) for a in sorted(allowed))
                errors.append(f'{platform} [{lang}] {name!r}: source {exp} != {types(val)}')

if errors:
    print(f'PLACEHOLDER ERRORS: {len(errors)}')
    for e in errors:
        print('  ' + e)
    sys.exit(1)
print('OK: all placeholders match their source.')
