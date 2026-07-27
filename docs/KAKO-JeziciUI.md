# KAKO-JeziciUI.md — Kako se menja, dodaje i briše tekst u višejezičnom UI-u xponga

Konsolidovana referenca za xpong, izvedena iz Buchenberg recepta
(`KAKO-JeziciUI.md`) i proverena protiv stvarnog `app.js` (sesija 21).
Arhitektura je pojednostavljena u odnosu na Buchenberg — razlike su
navedene eksplicitno jer menjaju gde greška može nastati.

**Nastalo:** sesija 21, 27. jul 2026.

---

## 1. Arhitektura — izvor istine

Tekst prikazan na stranici NIJE ono što piše u HTML hardkodu. Izvor istine
je promenljiva `T` u `/var/www/xpong/app.js`.

- Pet jezičkih blokova: `T.en`, `T.de`, `T.it`, `T.hr`, `T.sr`.
- **SR je ugnežden pod `.cyr`**: `T.sr.cyr` — namerno pripremljeno da se
  `T.sr.lat` doda aditivno kasnije, bez lomljenja postojeće strukture. SR
  blok koristi 8-razmaknu indentaciju (nested), svi ostali jezici
  6-razmaknu.
- Ključevi su prefiksovani po stranici: `nav_*`, `g_*` (game), `x_*`
  (xray/Telemetrija — tehnički identitet zadržan iako se stranica ZOVE
  Telemetrija), `r1_*` (rl1), `r2_*` (rl2), `ab_*` (about).
- `dict(lang)` bira ceo jezički objekat: `sr` → `T.sr.cyr`, ostali →
  `T[lang]` ili `T.en` kao fallback ako jezik ne postoji.
- `t(key, lang)`: `dict(lang)[key]`, ako ne postoji → `T.en[key]`, ako ni
  to ne postoji → **vraća sâm `key`** (string ključa, bez ikakve provere
  ili upozorenja — vidi §2).

## 2. Ključna razlika od Buchenberga: data-i18n atributi, ne apply-linije

Buchenberg: rečnik + apply-linija po stranici
(`const x = t('kljuc'); if (x && x !== 'kljuc') getElementById(id)...`) —
tri dodirne tačke po tekstu (ključ, apply-linija, HTML id).

xpong: rečnik + `data-i18n="ključ"` (ili `data-i18n-html="ključ"` za HTML
sadržaj) atribut direktno na HTML elementu. Jedna centralna funkcija
`applyI18n()` automatski hvata SVE elemente sa tim atributima — nema
apply-linija po elementu.

    function applyI18n() {
      var lang = getLang();
      document.documentElement.setAttribute('lang', lang);
      document.querySelectorAll('[data-i18n]').forEach(function (el) {
        el.textContent = t(el.getAttribute('data-i18n'), lang);
      });
      document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
        el.innerHTML = t(el.getAttribute('data-i18n-html'), lang);
      });
    }

Posledice, jedna dobra i jedna loša:
- **Dobra:** ceo razred Buchenberg bagova ("apply-linija zaboravljena/
  pogrešan id") strukturno ne postoji — nema apply-linije koju bi trebalo
  zaboraviti.
- **Loša:** Buchenbergova apply-linija je pisala preko HTML-a SAMO ako je
  `t()` vratio pravi prevod, ne sâm ključ. xpongov `applyI18n()` tu
  proveru NEMA — piše bezuslovno. Ako `data-i18n` atribut postoji a ključ
  ne postoji nigde, `t()` vraća ime ključa i ono se vidi sirovo na ekranu,
  na SVIM jezicima.

**Ova razlika je poznata i namerno neuklonjena za sada** (razmatrano u
sesiji 21) — videti §10.

## 3. Kako DODATI novi ključ / novi tekst

1. Dodaj ključ u SVIH 5 jezičkih blokova (`T.en`, `T.de`, `T.it`, `T.hr`,
   `T.sr.cyr`) — svaki na svom jeziku, ne kopija engleskog.
2. Dodaj `data-i18n="ključ"` (čist tekst) ili `data-i18n-html="ključ"`
   (sadrži HTML) atribut na HTML element.
3. **Koraci 1 i 2 moraju ući ISTOVREMENO** — nema zaštite kao u Buchenbergu
   (§2). Ako atribut uđe pre ključa (ili obrnuto), sâmo ime ključa se vidi
   na ekranu, tiho, bez greške u konzoli.

## 4. Kako IZMENITI postojeći tekst

1. `grep -n "ključ:" app.js` — pronađi tačan ključ za jezik koji menjaš.
2. **Pročitaj doslovan sadržaj pre zamene.** Escape oblici u `app.js` su
   MEŠANI, čak i unutar istog bloka: `\uXXXX`, `\xNN`, sirov UTF-8
   koegzistiraju. Pre sidrenja: `grep -n "target" app.js | cat -A`.
3. `str.replace` + `assert count==1`, ponovi za svih 5 jezika ako izmena
   treba biti dosledna.

## 5. Kako OBRISATI ključ ("mrtvi ključevi")

1. `grep -n 'data-i18n="ključ"\|data-i18n-html="ključ"'` na SVIM `.html`
   stranicama — potvrdi da se STVARNO ne poziva nigde.
2. Ako potvrđeno mrtav — obriši iz svih 5 jezičkih blokova.
3. Ne brisati "za svaki slučaj" bez grep potvrde.

## 6. Kako dodati i18n na sasvim novu stranicu

1. Za svaki vidljiv tekstualni element odluči prefiks ključa (`<page>_*`).
2. Ubaci ključeve u svih 5 blokova.
3. HTML: element dobija `data-i18n` ili `data-i18n-html` atribut — nema
   potrebe za apply-funkcijom po stranici, `applyI18n()` je već centralna.
4. Testiraj JEDAN jezik potpuno pre nego pređeš na svih pet.

## 7. Tehnička metoda izmene

Isti obrazac kao kod `concepts.json`: Python heredoc, NE `sed`.

    cd /var/www/xpong && python3 - << 'PYEOF'
    f = "app.js"
    s = open(f, encoding="utf-8").read()

    old = '<TAČAN POSTOJEĆI TEKST — anchor, proveren sed-om PRE konstrukcije>'
    new = '<NOVI TEKST>'

    assert s.count(old) == 1, f"anchor count = {s.count(old)}"
    s = s.replace(old, new)
    open(f, "w", encoding="utf-8").write(s)
    print("OK")
    PYEOF

Pravila za anchor:
- Uvek prvo pročitati stvaran sadržaj (`sed -n 'LINE,LINEp' app.js`) pre
  konstruisanja anchor-a.
- Ćirilica (SR): koristiti literalni ćirilični string direktno u heredocu
  (`<<'PYEOF'` čuva UTF-8), ne rekonstruisati preko Unicode escape sekvenci.
- `assert s.count(old) == 1` pre svakog pisanja — zaštita, ne formalnost.

## 8. Verifikacija

Nema `node` na serveru — dvoslojna verifikacija:
1. Strukturna (pre browser testa): broj vitičastih zagrada balansiran
   (paziti na `T.sr.cyr` ugnežđenje — jedna dodatna `{`/`}` para u odnosu
   na ostale jezike), `grep -c "ključ:" app.js` potvrđuje tačan broj
   pojavljivanja.
2. Funkcionalna (JEDINA prava potvrda): browser test na svih 5 UI jezika.
   Claude ovo ne može uraditi sam — Flavio potvrđuje, Claude priprema i
   predlaže šta tačno proveriti.

## 9. Poznati bagovi — ledger

| Bag | Sesija | Uzrok | Napomena |
|---|---|---|---|
| Sirovo ime ključa vidljivo na ekranu | s20 (opšta lekcija) | `data-i18n` atribut i ključ u `app.js` nisu ušli istovremeno; `applyI18n()` nema proveru postojanja | Videti §2 — poznata razlika od Buchenberga, za sada neuklonjena |
| Slomljen `concepts.json` obara i Key Concepts (susedni sistem) | s20 (bag B4) | Isti `.catch` obrazac tihog gutanja greške | Videti KAKO-KeyConcepts.md §10 |

## 10. Otvorena stavka (kandidat, nije odlučeno)

Predlog razmatran u sesiji 21: uvesti u `applyI18n()` istu proveru koju
Buchenberg ima u apply-liniji (piši samo ako `t()` nije pao na sâm ključ)
— zadržalo bi se pojednostavljenje (atribut umesto apply-linije po
elementu) uz uvoz jedine dokazano korisne zaštite iz starog rešenja.
Flavio je za sada odlučio da NE menja — dokumentovano radi buduće odluke,
ne kao TODO.

## 11. Poreklo

Recept izveden iz Buchenberg `KAKO-JeziciUI.md` (sesije 61, 77–82, 108,
114, 115) i prilagođen stvarnom xpong kodu (sesija 21). Arhitekturna
razlika (atributi umesto apply-linija) potiče iz same inicijalne izgradnje
xponga, ne iz jedne izolovane odluke.

---

*Flavio & Claude · xpong · KAKO-JeziciUI.md · 27. jul 2026.*
