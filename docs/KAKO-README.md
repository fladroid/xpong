# KAKO-README.md — Kako se ažurira README.md u xpongu

Meta-recept za README (za razliku od `KAKO-Session.md` za session dokumente)
— iste korene deli sa njim (isti closing ritual, isti `&&` rizik), ali README
ima sopstvenu mehaniku jer se PREPISUJE, ne dodaje kao dnevnik.

**Nastalo:** sesija 21, 27. jul 2026.

---

## 1. Svrha

README je **kanonsko trenutno stanje** — "gde smo sad", ne "kako smo došli
dovde" (to je posao session dokumenta). Prepisuje se pri svakoj trajnoj
promeni; samo poslednja verzija je istinita. Detaljno u METHOD §4.

## 2. Mehanika izmene — ciljani str.replace, ne prepisivanje celog fajla

README je 12.108 znakova (27. jul 2026) — predaleko iznad ~3.900-znakovnog
praga za bezbedan jednokratni heredoc upis (videti `KAKO-Session.md` §2).
**Standardni obrazac za README nije heredoc prepisivanja celog fajla, nego
Python `str.replace` sa `assert count==1`, po izmeni:**

    cp README.md /tmp/README.md.bak-sNN
    python3 - << 'PYEOF'
    f = "/home/balsam/xpong/README.md"
    s = open(f, encoding="utf-8").read()

    old = '<TAČAN POSTOJEĆI FRAGMENT>'
    new = '<NOVI FRAGMENT>'
    assert s.count(old) == 1, f"count = {s.count(old)}"
    s = s.replace(old, new)

    open(f, "w", encoding="utf-8").write(s)
    print("OK")
    PYEOF

Više nezavisnih izmena u istoj sesiji mogu ići u istom skriptu, kao niz
`assert`-ovanih zamena — svaka mora proći svoj `assert` PRE nego što se bilo
šta upiše na disk (isti obrazac kao `concepts.json` i `app.js`).

## 3. Numerisane liste — rizik pri dodavanju/uklanjanju stavke

README sadrži nekoliko ručno numerisanih lista (npr. "Otvorene stavke po
prioritetu"). Brojevi NISU automatski — uklanjanje ili dodavanje stavke iz
sredine zahteva ručno renumerisanje svega posle nje. Konkretan primer (ova
ista sesija, s21): uklanjanje zatvorene stavke (5) iz šestočlane liste
zahtevalo je da se bivša (6) preimenuje u (5).

**Pravilo:** posle svake izmene numerisane liste, pročitaj celu listu i
potvrdi da brojevi idu uzastopno bez rupe ili duplikata — ne pretpostaviti
da je `str.replace` sam po sebi dovoljna provera, jer on menja SAMO tekst
koji je naveden kao anchor, ne susedne brojeve.

## 4. Zajednički rizici sa session dokumentima

README deli dva rizika detaljno opisana u `KAKO-Session.md`:
- **§4 (`&&` lanac)** — posebno važno kod README jer se `diff` pre/posle
  često koristi baš za proveru README izmena, i baš `diff` je taj koji je
  već jednom prekinuo lanac pre commit/push-a (s17).
- **§5 (re-otkrivanje već dokumentovane činjenice)** — README je često
  UPRAVO to mesto gde je činjenica već zapisana; pre nego što se predloži
  nova odluka ili istraživanje, proveriti da README (i `KAKO-*.md` recepti)
  već ne sadrže odgovor.

## 5. Verifikacija

`diff /tmp/README.md.bak-sNN README.md` da se vidi TAČNO šta se promenilo —
ali kao ODVOJENA komanda od `git add`/`commit`/`push` (§4/KAKO-Session §4).
Vizuelna provera da nova sekcija/red čita prirodno u kontekstu okolnog
teksta — `assert count==1` garantuje da je zamena izvršena, ne da rezultat
ima smisla.

## 6. Redosled

README se ažurira KAO DEO zatvaranja sesije, posle pisanja session
dokumenta — videti `KAKO-Session.md` §7 za pun checklist. Redosled komandi
kad se README menja: bekap → `str.replace` skript(a) → `diff` provera
(odvojeno) → `git add`/`commit`/`push` (odvojeno) → brisanje bekapa.

---

*Flavio & Claude · xpong · KAKO-README.md · 27. jul 2026.*
