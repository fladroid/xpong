# KAKO-Cache.md — Kako prepoznati i rešiti keš problem u xpongu (PC i tablet)

Praktičan vodič, prvenstveno za Flavija — za razliku od `KAKO-Session.md` i
`KAKO-README.md` (procesni recepti za Claudeovo pisanje), ovaj dokument je
dijagnostički alat za trenutak kad nešto na sajtu izgleda staro ili čudno.
Sastavljen na osnovu istorije problema kroz ceo projekat (sesija 21,
27. jul 2026).

**Nastalo:** sesija 21, 27. jul 2026.

---

## 1. Istorija — ovo nije nov problem

Keš/verzija zabuna prati projekat od početka, i prethodni projekat isto:

- **Pong (prethodni projekat):** *"GitHub Pages cache: dupli `Ctrl+Shift+R`
  je očekivano ponašanje, nije deployment greška."* (`PongPregledProjekta.md`)
- **s02:** DNS negativni keš na lokalnom resolveru foxuno — rešeno
  korišćenjem `@8.8.8.8`/`@1.1.1.1` direktno.
- **s03:** uveden `XP_VERSION` u footeru kao self-dijagnostika.
- **s04:** uveden verzioni sufiks (`sNN.M`, npr. `s04.1→.4`) da se tokom
  sesije razluči tvrdoglav keš od stvarnog kvara u kodu.
- **s20:** **tri ručna čišćenja keša u jednoj sesiji** — uzrok je rupa u
  pokrivenosti, videti §3.

Zaključak: ovo nije nešto što treba "jednom rešiti i zaboraviti". To je
stalna karakteristika statičkih sajtova iza kešujućeg servera/browsera —
protokol i alati u nastavku postoje da diagnoza bude brza, ne da problem
nestane.

## 2. PC i tablet su različiti problemi

**Na PC-u:** `Ctrl+Shift+R` (hard refresh) pouzdano rešava keš. Glavni
rizik nije tehnički nego navičajni — zaboravi se da se uradi pre nego što
se zaključi "nešto ne radi".

**Na tabletu:** nema `Ctrl+Shift+R`. Pull-to-refresh gest ("potezanje")
nije pouzdan ekvivalent — može osvežiti prikaz a da ne prisili browser na
stvaran novi fetch resursa, zavisno od OS-a/browsera. Ovo je razlog zašto
se na tabletu problem oseća kao da "zeza" nasumično, dok je na PC-u
predvidljiv (samo zaboravljen refresh).

## 3. Postojeći alat i njegova poznata rupa

`XP_VERSION` footer (+ `sNN.M` sufiks tokom sesije) postoji tačno zato da
se ne mora nagađati — uporedi broj u footeru sa onim što Claude javlja da
je upisao.

**Poznata rupa (uzrok s20 incidenta):** `XP_VERSION` pokriva SAMO `app.js`.
`xpong.css` i `<page>.js` (npr. `rl2.js`) nemaju sopstvenu oznaku verzije —
footer može reći "sve sveže" dok su CSS ili stranični JS i dalje stari iz
keša. Ovo je razlog zašto footer sam po sebi ponekad nije dovoljan dokaz.

## 4. Predlog tehničkog rešenja — PRIO 1 (već u README-u, podsetnik)

Cache-busting query string `?v=sNN` na `<link>`/`<script>` tagovima u
svakoj stranici, bumpuje se zajedno sa `XP_VERSION`. Rešava tačno rupu iz
§3 — browser tretira `xpong.css?v=s21` kao potpuno nov resurs čim se
`sNN` promeni, nezavisno od keš politike servera. Infrastrukturno, radi se
jednom po stranici, ne ponavlja se.

## 5. Predlog tehničkog rešenja — PRIO 2 (nov, ova sesija)

PRIO 1 rešava "novi deploy → nov URL za resurse". NE rešava situaciju koju
si opisao: korisnik (ti) već ima stranicu otvorenu na tabletu, i sam gest
osvežavanja je nepouzdan — nema garancije da će se ijedan fetch, sa novim
ili starim URL-om, uopšte desiti dok se ne zatvori i ponovo otvori stranica.

**Predlog:** aktivna provera verzije iznutra, ne oslanjanje na gest.
- Mali `version.json` sa trenutnim `XP_VERSION` (menja se pri svakom bumpu).
- `app.js` ga proverava periodično (npr. na `visibilitychange` — kad se
  tab/app vrati u fokus, što pokriva i "vratio sam se na tablet posle
  pauze") i fetch nosi sopstveni cache-busting (`?t=Date.now()`, isti
  obrazac kao `concepts.json`).
- Ako se live verzija razlikuje od učitane: nenametljiv baner "Nova verzija
  dostupna — pritisni da osvežiš" sa dugmetom (`location.reload()`).
- Radi identično na PC-u i tabletu, jer je to **klik/tap na dugme**, ne
  gest i ne kombinacija tastera — ne zavisi od toga da li OS ispravno
  tumači pull-to-refresh.

Ovo ide u red posle PRIO 1 — nadograđuje se na njega (isti `XP_VERSION`
kao izvor istine), ne zamenjuje ga.

## 6. Brzi vodič dok se PRIO 1/2 ne implementiraju

- **PC:** ako nešto izgleda staro — `Ctrl+Shift+R` PRE javljanja da nešto
  ne radi. Uporedi footer broj sa očekivanim.
- **Tablet:** pull-to-refresh nije pouzdan test. Pouzdanije: zatvori
  tab/app potpuno i ponovo otvori, nego povlačenje nadole.
- Ako je footer već tačan broj a ponašanje i dalje staro — to je § 3 rupa
  (CSS/page-JS), ne stvaran bag u logici; reci to Claudeu direktno, štedi
  vreme dijagnoze.

---

*Flavio & Claude · xpong · KAKO-Cache.md · 27. jul 2026.*
