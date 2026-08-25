#!/usr/bin/env sh
# Run once after cloning. Enables the .xcstrings clean filter so Xcode's
# re-serialization noise never lands in commits. Git will not run a repo's
# clean filters until you opt in like this, so every fresh clone needs it.
set -e
cd "$(git rev-parse --show-toplevel)"
git config filter.xcstrings-normalize.clean "python3 tools/normalize_xcstrings.py -"
echo "xcstrings clean filter enabled."
