# Session 08 — About dopune: Filozofija sidebar box + Claude Key Concept + status M0→M1

**Datum:** 27 Jun 2026
**Fokus:** tri male About dopune po buchenberg obrascu — novi sidebar box
„Filozofija" (5 jezika, jednina, potpis „— Flavio"), Claude Key Concept kartica
u gridu, i popravka zastarelog statusa M0→M1. Bez M2.

## Otvaranje (health snapshot)
- xpong @ `1d4b9de` (s07), čisto, u sinhronu.
- xpongweb @ `f8493be` (s07), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s07'` (živo) — README, session docs i kod složni.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Odluka: zašto Filozofija box SAD a ne u s06
U s06 je box svesno izostavljen uz obrazloženje „cela About stranica je
filozofija" — esej od 7 sekcija JESTE X-Ray stav, pa bi box ponavljao stranicu.
Sad dodat jer buchenbergov drugi pasus nosi **meta-izjavu koju esej ne kaže
eksplicitno**: da je xpong *praktična implementacija* X-Ray stava, ne samo priča
o njemu. To je posao koji esej ne pokriva → box nije duplikat.

Tekst (Flaviova ideja, modifikacija buchenberg pasusa):
> Put je važniji od cilja. Stav koji gradim je generičan i primenjiv daleko šire
> od igre Ponga. xpong je praktična implementacija mog X-Ray stava: odbijanje da
> se mašinsko učenje tretira kao crna kutija, i gradnja prozora u njega — potez
> po potez, sloj po sloj. — Flavio

Tri svesne izmene od buchenberg originala:
- **„pipeline" → „stav"** — xpong NEMA pipeline (buchenberg ima, to mu je jezgro);
  xpong je sajt-prozor. Reći „pipeline" lagalo bi o tome šta xpong jeste —
  suprotno X-Ray stavu.
- **„strojnog prevođenja" → „mašinsko učenje"** — naša crna kutija (tema eseja),
  ne buchenbergova.
- **„sloj po sloj, score po score" → „potez po potez, sloj po sloj"** — „potez"
  = Pong (vidljiv u M2 overlay-u), „sloj" = neuronska mreža + esejsko „sloj po
  sloj gradim razumevanje". Buchenbergov „score" je tamo doslovan (sudija ocenjuje
  prevod brojem); kod nas bi značio drugo.
- **Jednina** (gradim, ne gradimo) — isti glas kao „Provera, ne mašta" box i
  potpis „— Flavio". Dva susedna boxa pod istim potpisom moraju isti glas.

## Šta je urađeno
1. **Filozofija box** — `ab_side_phil` + `ab_side_phil_text` × 5 jezika u app.js
   (EN baza, DE/IT/HR latinica, SR ćirilica). Naslov kroz `data-i18n`
   (textContent), telo kroz `data-i18n-html` (innerHTML: `<br><br>` + `<em>—
   Flavio</em>`). HTML `<div class="xp-infobox">` ubačen u about.html **između
   Verify i Auth** (Auth ostaje poslednji).
2. **Claude Key Concept kartica** — `concepts.json` ključ `about`, dodata 7.
   kartica: ✨ Claude, opis „Anthropic's AI assistant — the working partner across
   xpong's documented sessions.", wiki `Claude_(AI)`. Samo na About (ne Home) —
   paralela Authorship boxu, kao buchenberg. Home ostaje 6, About 7.
3. **Status M0→M1** — `ab_side_status_v` × 5 jezika: „M0 — landing" →
   „M1 — classic Pong / klassisches Pong / Pong classico / klasični Pong /
   класичан Понг". Bilo zastarelo od s06.
4. **Verzija** — s07 → s08; datum → 27 Jun 2026.

## Lekcije / ledger
- **Heredoc kroz MCP kanal ima granicu dužine.** Pun base64 skripte (~11.7k
  znakova) isekao se u jednom `cat > … << EOF` — heredoc primio samo početak,
  ostatak izgubljen. Otkriveno pre štete (krnji b64 obrisan, nije dekodiran).
  Novi transport obrazac za velike skripte: `split -b 3900` → više `cat >>`
  (append) → `tr -d '\n' | base64 -d` → **md5 + `ast.parse` verifikacija pre
  pokretanja**. md5 originala iz sandboxa poredi se s md5 na serveru; poklapanje
  garantuje bajt-veran prenos.
- **`grep -c` vraća exit 1 kad je rezultat 0.** U `&&` lancu to prekida ostatak
  komande (provera „M0 pojava: 0" zaustavila lanac iako je 0 baš ono što želimo).
  Za provere koje smeju legitimno vratiti 0, koristi `;` umesto `&&`.
- **Ne prepisuj tuđu grešku iz reference.** Buchenbergova Claude kartica u
  prosleđenom tekstu imala „Buchenberg's" (Flavio ručno ispravio na „xpong's") i
  slug `Claude_(language_model)` na disku — Flavio dao `Claude_(AI)`. Išli s
  Flaviovom direktnom instrukcijom (Wikipedia preimenovala članak), ne s grep
  nalazom. Ista disciplina kao node/window.xpong iz s07: proveri, ne pretpostavi.
- **Atomska multi-fajl izmena (potvrđen obrazac).** Jedna Python skripta u /tmp,
  van repoa: čita app.js + about.html + concepts.json → `assert count==1` po
  svakom sidrištu (5 auth redova jedinstveno po vrednosti naslova) → JSON
  re-parse i provera da slug nije duplikat → bekap `*.s08bak` → piše tek kad sve
  asercije prođu.

## Završno stanje
- About dopunjen na `https://xpong.opik.net/about.html` (s08): sidebar 4 boxa
  (Project info → Provera, ne mašta → **Filozofija** → Authorship), Key Concepts
  grid 7 kartica (zadnja ✨ Claude), Status „M1 — klasičan Pong". Svih 5 jezika.
  Potvrđeno u brauzeru (hard refresh, footer „s08", ćirilica + latinica).
- xpongweb dirnuto: `app.js`, `about.html`, `data/concepts.json`.
- Bekapi `*.s08bak` ostaju na serveru (mogu se obrisati po želji).

## Sledeće
- **M2 — X-Ray overlay** (predviđena putanja lopte s odbijanjima, na zasebnoj
  stranici, ne na klasičnoj igri); settings panel s podesivim parametrima
  (config→start disciplina, konstante već izdvojene u game.js).
- (kandidat, i dalje otvoren) Proširenje Key Concepts iz About teksta: crna
  kutija, emergencija, neuronska mreža, transformer arhitektura.
- (kandidat) health_check.py kao strukturni čeker kad struktura poraste.
