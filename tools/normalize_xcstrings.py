#!/usr/bin/env python3
"""Canonicalize an Xcode String Catalog (.xcstrings) so git stores it in a
stable key order regardless of how Xcode happened to serialize it.

Xcode re-serializes Localizable.xcstrings on almost every save and does not
guarantee a stable key order, which produces enormous, meaningless diffs
(tens of thousands of moved lines) that bury the actual translation changes
and turn every merge into a conflict.

This script parses the catalog and re-emits it with keys sorted, using the
exact byte formatting Xcode itself uses (2-space indent, " : " separators,
raw UTF-8, no trailing newline, empty objects rendered across three lines).
Because the output matches Xcode's formatting in every respect except order,
the only thing this ever changes is line ORDER, and once every commit is
sorted the same way, diffs collapse down to real content changes.

Usage
  Clean filter (reads stdin, writes stdout) -- this is what git calls:
      python3 tools/normalize_xcstrings.py -

  Normalize a file in place:
      python3 tools/normalize_xcstrings.py ios/Localizable.xcstrings

  Check only (exit 1 if the file is not already canonical), no write:
      python3 tools/normalize_xcstrings.py --check ios/Localizable.xcstrings
"""

import json
import re
import sys

# Xcode writes an empty JSON object as:  {\n\n<indent>}  (blank line, close
# brace aligned with the key's indent). Python's json emits "{}", so expand it.
_EMPTY_OBJ = re.compile(r'^(?P<indent> *)(?P<key>".*") : \{\}(?P<comma>,?)$', re.M)


def normalize(text: str) -> str:
    data = json.loads(text)
    out = json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", " : "),
    )
    out = _EMPTY_OBJ.sub(
        lambda m: f'{m.group("indent")}{m.group("key")} : {{\n\n{m.group("indent")}}}{m.group("comma")}',
        out,
    )
    return out


def main(argv):
    args = argv[1:]

    if not args:
        sys.stderr.write(__doc__)
        return 2

    if args[0] == "-":
        sys.stdout.write(normalize(sys.stdin.read()))
        return 0

    check = False
    if args[0] == "--check":
        check = True
        args = args[1:]

    if len(args) != 1:
        sys.stderr.write("expected exactly one file path\n")
        return 2

    path = args[0]
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
    result = normalize(original)

    if check:
        return 0 if original == result else 1

    if original != result:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
