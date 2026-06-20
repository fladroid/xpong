# Session 01 — Upoznavanje (Day-0 / bootstrap)

**Datum:** 2026-06-20
**Tip:** Day-0 bootstrap — prva sesija projekta xpong.

## Fokus
Uspostaviti supstrat i metodu za xpong (treći pokušaj naslednika Ponga,
od nule). Bez koda — samo postavka.

## Snimak zdravlja (verifikovano komandama, ne pamćenjem)
- Server: foxuno (host `vnic-foxuno`, alias `foxuno.dynu.net`), user `balsam`,
  sudo kod Flavija.
- Home: `/home/balsam/xpong` — kloniran repo, bio prazan.
- Git: origin = `git@github.com:fladroid/xpong.git` (fetch+push), grana `main`,
  bez commita do ovog.
- GitHub SSH s foxuno: radi (`fladroid` autentifikovan).
- Baza / drugi server: ne koristi se.

## Šta je urađeno
- Pročitan project knowledge: METHOD (SR/EN), X-Ray v3b (SR/EN).
- Verifikovan supstrat s 3 read-only komande (identitet, stanje dira, GitHub SSH).
- Kloniran `xpong` repo u `/home/balsam/xpong`.
- Potvrđeno ožičavanje repoa (origin, grana main, čisto).
- Položen minimalni skelet: README v0 + ovaj zapis.

## Lekcije / ledger
- Default cwd konektora `foxuno:run_command` je `/home/balsam/mcp_foxuno`,
  NE projekat → uvek apsolutne putanje ili eksplicitan `cd /home/balsam/xpong`.
- `balsam` je i username na foxuno i ime zasebnog servera (`balsam.dynu.net`).
  Ne mešati; za xpong se balsam server ne koristi.

## Završno stanje
Supstrat postavljen i verifikovan. Repo ožičen. Skelet na mestu.
Projekat prazan — još nijedna linija koda.

## Sledeći koraci
- Odlučiti STACK (Python backend + JS/HTML frontend? čisto browser JS? drugo?)
  i PRVI MILESTONE.
- Tek po tome: `.gitignore`, `src/` raspored, prvi health_check ekvivalent.
- Eventualno povući sažetak prethodna dva pokušaja Ponga u project knowledge.
