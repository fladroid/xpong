# Session 06 — About stranica: istorijsko-filozofski esej + sidebar, 5 jezika

**Datum:** 25 Jun 2026
**Fokus:** nova About stranica — esej „od dve crte do milijardu parametara"
(Pong 1972 → if-then → Q-learning → DQN → LLM, zajednička nit: ne vidi se kako
softver radi iznutra), sidebar s tri boxa, Key Concepts i na About, pun i18n
(en + de/it/hr + sr-ćirilica). Bez M1.

## Otvaranje (health snapshot)
- xpong @ `2e1e549` (s05), čisto, u sinhronu.
- xpongweb @ `1cd607b` (s05), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s05'`.
- `health_check.py`: i dalje ne postoji (ručni snapshot).
- Nastavak u istoj sesiji (s05 odmah pre) — onboarding skraćen uz Flaviovu
  saglasnost; izvor istine ostaje server/repo.

## Šta je urađeno
1. **about.html** (nov) — naš obrazac (`data-i18n` / `data-i18n-html`, NE
   buchenbergovi id-jevi). `data-page="about"` → `renderConcepts()` automatski
   ubacuje Key Concepts grid. Layout `#about-layout` grid 1fr/280px (prose +
   sidebar), responsive 1-kolona već postojala.
2. **Esej (7 sekcija)** — istorijska linija Ponga kao ulaz u X-Ray stav:
   1972 logika u kolima → čitljiva if-then pravila → Q-learning (naš stari
   Pong, self-play, tabela vrednosti) → DQN + emergencija (zamke, ćoškovi) →
   LLM/transformer → zajednička nit „crna kutija". Tekst Flaviova ideja,
   Claude artikulacija; oba imena u Authorship boxu.
3. **Sidebar — 3 boxa:** Project info (bez Database reda; M0, stack, repoi,
   web), „Provera, ne mašta" (NOVI box — Flaviova ideja: Wikipedia linkovi kao
   epistemološko sidro, X-Ray stav okrenut tekstu; jednina/prvo lice),
   Authorship & Collaboration (verbatim buchenberg ton, samo xpong + „this
   very page", bez broja sesija — Flavio izričito tražio da se ne dira registar).
4. **Key Concepts na About** — `data/concepts.json` ključ `about` = kopija
   home (6 koncepata, uključujući 2 X-Ray linka).
5. **Nav** — `about` stavka (živa, posle home), `nav_about` u svih 5 lokala.
6. **Footer** — uklonjen `· Flavio &amp; Claude` u svih 5 lokala (sad je u
   Authorship boxu, kao buchenberg).
7. **i18n** — ~31 ključ × 5 jezika. EN baza; de/it/hr latinica; sr ćirilica.
8. **Verzija** — s06 (datum 25 Jun ostaje).

## Lekcije / ledger
- **Ampersand: textContent vs innerHTML.** `ab_side_auth` (naslov) ide kroz
  `data-i18n` (textContent) → `&amp;` se NE dekodira, prikazuje se bukvalno.
  Fiks: goli `&`. Ali `_text` ključevi idu kroz `data-i18n-html` (innerHTML)
  gde `&amp;` (npr. „Flavio &amp; Claude") JESTE ispravno. Pravilo: entitet
  samo u innerHTML kontekstu.
- **dict + apply obrazac za prevode.** Tekst (Python dict, čist, `\u` escape)
  odvojen od logike (apply skripta generiše JS). exec() učita dict → ako
  Python ne pukne, escaping je čist. Ponovo upotrebljiv za svaku buduću
  stranicu. Provera `assert '"' not in v` pre upisa (JS string u dvostrukim
  navodnicima, tekst pun apostrofa l'agente/čovjek).
- **sr uvlaka = 8 razmaka** (ugnežden pod `cyr:`), ostali 6. Provereno pre
  upisa; sidrište footer string svakog jezika (`assert count==1`).
- **Ćirilica iz prve.** Najbolja sr implementacija dosad — `\u` escape kroz
  heredoc (ne sirovi bajtovi), backup pre upisa, provera strukture. Nagomilani
  ledger ranijih grešaka (s03 truncation) isplatio se.
- **Latinica/ćirilica pravilo (sr):** ćirilica = pismo teksta; Понг/Атари
  transkribovano; xpong + tehnički termini (Q-learning, DQN, transformer,
  self-play, LLM, X-Ray) + lična imena (Joe Strummer) latinično. Flavio
  delegirao odluku (čita ćirilicu lako, piše teško).

## Odluke za budućnost
- **Key Concepts = ponavljajući proces.** Pri svakoj promeni/aktivaciji
  stranice: proći tekst, izvući nove pojmove u grid. ODLOŽENO za sledeću
  sesiju: dublja analiza About teksta za proširenje (kandidati: crna kutija,
  emergencija, neuronska mreža, transformer arhitektura, hyperparametri…).
- Key Concepts ostaje i na Home (ulaz/orijentir) i na About (potvrda priče) —
  različite uloge, ne duplikat.

## Završno stanje
- About kompletan na `https://xpong.opik.net/about.html` (s06): esej 7 sekcija,
  sidebar 3 boxa, Key Concepts 6 kartica, svih 5 jezika (en/de/it/hr/sr-ćir).
  Potvrđeno u brauzeru za sve jezike (dve provere: latinica + ćirilica).
- xpongweb dirnuto: `about.html` (nov), `app.js`, `xpong.css`,
  `data/concepts.json`.
- Igra i dalje neimplementirana (M1 otvoren).

## Sledeće
- (kandidat) Proširenje Key Concepts iz About teksta — vidi „Odluke za budućnost".
- M1: klasičan Pong (`game.html` — canvas, reketi, lopta, gol L/D, tastatura +
  touch); ukloniti `soon` s nav „The Game".
