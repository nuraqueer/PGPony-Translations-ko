# Glossary and translation rules

These rules apply to **every** language in this repository. They exist so that
translations stay consistent and, above all, so the apps do not crash or show
broken text at runtime.

## Hard rules (never break these)

1. **Placeholders must be copied exactly.** Keep every placeholder character
   for character, in a valid order, with the same count as the source.
   - iOS: `%@`, `%lld`, `%d`, and positional forms `%1$@`, `%2$@`, `%1$lld`, etc.
   - Android: `%s`, `%d`, `%1$s`, `%2$d`, etc.
   - Never translate, drop, add, or renumber a placeholder. If your language
     needs a different word order, use the **positional** form (`%1$@`, `%2$@`)
     so the arguments still line up.

2. **Do not translate product and brand names.** Keep them in Latin script:
   PGPony, AgePony, BurnPony, CarrierPony, NorseHorse, Token2, ObjectivePGP,
   YubiKey, Yubico.

3. **Do not translate crypto / protocol terms.** Keep verbatim:
   Ed25519, Curve25519, Cv25519, X25519, ML-KEM-768, RSA, DSA, ECDH, ECDSA,
   EdDSA, KDF, AES-256, AES, AEAD, OCB, EAX, GCM, CFB, MDC, SEIPD, RFC 9580,
   RFC 4880, OpenPGP, GnuPG, GPG, LibrePGP, PGP, WKD, SOCKS, SOCKS5, Tor, Orbot,
   Signal, TLS, SSH, NFC, USB-C, USB, PIN, PW1, PW3, PUK, OTP, URL, URI, JSON,
   UUID, SHA-256, SHA-512, Base64.

4. **Keep file extensions verbatim:** `.gpg`, `.pgp`, `.asc`, `.sig`, `.txt`, etc.

5. **Keep PGP armor markers verbatim**, e.g. `-----BEGIN PGP MESSAGE-----`.

6. **Keep CLI commands verbatim**, e.g. `ykman config usb --disable OTP`.

7. **Legal / license text stays in English.** Do not translate BSD/MIT license
   bodies or copyright lines.

## Tone

UI strings are terse. Keep translations short. Use the imperative for buttons
and actions unless the source is clearly a title or noun. Match the source's
punctuation (do not add a trailing period the English lacks).

## Plurals

Some languages need more plural categories than English (English uses only
`one` / `other`). Provide every category your language's CLDR rules require.
For example Russian needs `one`, `few`, `many`, `other`; Polish and Czech are
similar. Each plural form must still contain the count placeholder (`%lld` on
iOS, `%d` on Android) even when English hard-codes the number "1".

---

## Reference: Russian term choices

The Russian translation already in this repo uses these choices. New languages
should build their own equivalent table and add it below.

| English | Russian |
| --- | --- |
| passphrase | парольная фраза |
| password | пароль |
| keyring | связка (ключей) |
| fingerprint | отпечаток |
| hardware key | аппаратный ключ |
| software key | программный ключ |
| public key | открытый ключ |
| private / secret key | закрытый ключ |
| subkey | подключ |
| armored / ASCII armor | ASCII-броня |
| sign / signature | подписать / подпись |
| verify | проверить |
| encrypt / decrypt | зашифровать / расшифровать |
| revoke / revocation | отозвать / отзыв |
| attachment | вложение |
| attempts remaining | осталось попыток |
| reset code | код сброса |
| admin PIN | PIN администратора |
| Bundle | Комплект |

Russian uses guillemets « » for quotes and for iOS Settings paths, e.g.
«Настройки» › «PGPony».
