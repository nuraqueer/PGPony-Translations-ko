# Contributing

Thank you for helping translate PGPony. Please read `GLOSSARY.md` first, then
follow the steps for the platform you are editing.

Before you open a pull request, run the checks in `tools/` (see the bottom of
this file). They catch the most common breakage: a missing or altered
placeholder.

---

## Editing an existing language

### iOS (`ios/Localizable.xcstrings`)

This is a single JSON file (Apple's "String Catalog"). Every entry is keyed by
its English text. A single entry looks like this:

```json
"Incorrect PIN." : {
  "localizations" : {
    "ru" : {
      "stringUnit" : { "state" : "translated", "value" : "Неверный PIN." }
    }
  }
}
```

To fix a translation, find the English key and edit the `value` for your
language code. To translate a string that has no entry for your language yet,
add a `"xx"` block (with your language code) next to the others under
`localizations`. Set `"state"` to `"translated"`.

You can edit the JSON in any text editor. If you have a Mac with Xcode, opening
the file there gives you a friendlier side-by-side table.

### Android and Desktop (`android/` and `desktop/`, `values-<lang>/strings.xml`)

The Android app and the Desktop app both use this same XML format, in their own
top-level folders (`android/` and `desktop/`). They have different keys, so
treat them as two separate jobs. Everything below applies to both.

Each language has its own folder, so you only touch your language's file. Keys
are symbolic names shared across languages:

```xml
<string name="common_button_cancel">Отмена</string>
```

Edit the text between the tags. Do not change the `name`. Keep Android escaping
rules: an apostrophe is `\'`, and `%` placeholders stay exactly as in the
English file (`android/values/strings.xml`).

---

## Adding a brand new language

Pick the correct language code first (e.g. `it` for Italian, `ko` for Korean,
`pt-BR` for Brazilian Portuguese).

### iOS

For each English entry you translate, add a block under `localizations` using
your language code, exactly like the `ru` example above. You do not have to
translate everything at once; untranslated strings fall back to English.

A maintainer also has to register the new language in the Xcode project
(`knownRegions`) and in `CFBundleLocalizations` for it to appear in the app.
Note in your pull request that the language is new so this gets done.

### Android

1. Copy the whole `android/values/` folder to `android/values-<code>/`
   (Android uses `values-pt-rBR` style region codes, e.g. `values-it`,
   `values-ko`).
2. Translate the text in the new file, leaving each `name` unchanged.

---

## Checks before you submit

From the repository root:

```
python3 tools/validate_placeholders.py
python3 tools/status.py
```

`validate_placeholders.py` fails if any translation's placeholders do not match
its English source. `status.py` prints how many strings each language still has
untranslated. Please make sure the validator passes before opening a pull
request.

## Prefer not to touch code or GitHub?

Email **norsehorse@norsehor.se** with the language you want to work on. You will
receive a four-column spreadsheet (English, Translation, Context, Changes),
generated with `tools/make_review_tsv.py`. Fill in the blank translations, or
write a fix in the **Changes** column for rows that already have one, and send
it back. A maintainer applies it to the app. No GitHub account needed.

Maintainers: generate a sheet for any language and platform with

```
python3 tools/make_review_tsv.py ios ru
python3 tools/make_review_tsv.py android de
python3 tools/make_review_tsv.py desktop fr
```

## Review

Every change is reviewed by a maintainer (and, where possible, a native
speaker) before it ships in a release. Translations may be edited for
consistency with the glossary.
