# Session 12 — M2 cigla 2 zatvorena; stranica X-Ray → Telemetrija; Key Concepts x4

**Datum:** 02 Jul 2026
**Fokus:** dovršetak cigle 2 (pun opis heatmapa) + konceptualno preimenovanje
stranice (X-Ray je stav, ne stranica) + Key Concepts kartice. Pet verzija
(s12.1–s12.5), sve potvrđene u browseru odmah po deployu.

## Otvaranje (health snapshot)
- xpong (docs) @ `fff99e7` (s12), čisto, u sinhronu.
- xpongweb (web) @ `c7b6989` (s12), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s12'` (živo) — README, session docs, kod složni.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Šta je urađeno

### s12.1 — switch preimenovan: X-Ray → Zrak (zagrevanje, Flaviov predlog)
Switch kontroliše samo zrak, ne ceo X-Ray sadržaj stranice — ime je bilo šire
od funkcije. `x_ray_on/off` x5: Beam/Strahl/Raggio/Zraka (uklj./isklj. ž. rod
uz HR "zraka")/Зрак; `x_intro` rečenica "X-Ray switch" → "Beam switch" x5.
`x_box_title` tada još netaknut (stigao u s12.4).

### s12.2 — heatmap okviri traka + zrak bleđi van igre (Flaviov predlog)
- Switch mora dati vizuelni odgovor odmah, ne tek posle prvog gola: tanki
  okviri (strokeRect 1px, alpha 0.25, +0.5 pomak za oštrinu) svih traka uz oba
  zida crtaju se čim je heatmap uključen; ispune rastu unutar njih. Prazan
  heatmap = "senka bez podataka", ne "ništa".
- Zrak: `dim = running ? 1 : 0.55` množi alfu segmenata i kontakt markera —
  bleđi pre starta / u pauzi / posle seta, pun tokom žive igre.

### s12.3 — Heatmap infobox: pun opis (cigla 2 ZATVORENA)
- Novi infobox "Heatmap" između X-Ray i Navigacija boxa (`x_heat_box_title/text`
  x5). Okvir iz manifesta: senka/metapodaci — "The heatmap is a shadow, not a
  mind…". Granularnost potvrđena: ostaje 4 trake; tekst ne pominje broj (ne
  zastareva).
- Heatmap rečenica UKLONJENA iz `x_intro` x5 — X-Ray box postao čist opis zraka.
- HTML fallback "laser" → "beam" (zaostao iz pre-s10). Cigla 2 time kompletna:
  mehanika (s10) + kontrole (s11) + okviri (s12.2) + pun opis (s12.3).

### s12.4 — stranica X-Ray → Telemetrija (Flaviova inicijativa, ključna odluka)
Obrazloženje: X-Ray je stav nad SVIM projektima/stranicama ("nije naziv
projekta ni metodologije — to je stav", manifest). Imenovati jednu stranicu
X-Ray degradira stav u feature i implicira da ostale stranice to nisu.
- Ime: "Telemetrija" (Claudeov predlog, Flavio prihvatio) — pokriva OBA sloja
  (zrak + heatmap) i buduće; rodoslov u manifestu (F1 broadcast telemetrija).
  "Telemetrija 1" odbačeno: stranice prirodno nasleđuju slojeve, numerisanje
  suvišno.
- `nav_xray` + `x_title` x5: Telemetry/Telemetrie/Telemetria/Telemetrija/
  Телеметрија; `x_title` bez podnaslova (ne zastareva).
- `x_box_title` x5: Beam/Strahl/Raggio/Zraka/Зрак — box posle s12.3 opisuje
  isključivo zrak.
- `x_intro` + završna rečenica x5: "Built in the X-Ray attitude — see About."
  (upućivanje imenom About stavke u tom jeziku) — stav vidljiv, s pravim mestom.
- HTML: `<title>Telemetry — xpong</title>`, h1 i box fallback usklađeni.
- Fajlovi OSTAJU `xray.html`/`xray.js` + `data-page="xray"` + i18n prefiks
  `x_`: URL/interni ID je tehnički identitet, preimenovanje lomi linkove bez
  dobiti (odluka, ne propust).

### s12.5 — Key Concepts x4 za telemetrija stranicu
`concepts.json` + sekcija `"xray"`: Pong (ponovljen sa game), Telemetry (📡),
Light beam (🔦, `Light_beam`), Heat map (🌡️, `Heat_map`) — EN opisi + EN
Wikipedia, postojeća konvencija. `data-page="xray"` je već postojao na body,
renderConcepts pokupio automatski — zahvat samo JSON + verzija.

## Lekcije / ledger
- **Mešani escape oblici i UNUTAR ISTOG i18n bloka.** SR: `x_intro` je
  `\u`-escaped, `x_ray_on/off` i nav linija sirov UTF-8; DE: `Schl\u00e4ger` i
  `f\xe4rbt` u ISTOJ liniji. Nikad ne pretpostavljaj konvenciju po bloku —
  `cat -A`/grep za SVAKO sidro posebno. (s12.4 assert pukao na SR nav sidru
  jer sam pretpostavio `\u`; fajl netaknut, assert pre upisa.)
- **`endswith` sidro mora računati završni newline.** concepts.json se
  završava `}\n`, ne `}` — s12.5 assert pukao, `tail -c | cat -A` dijagnoza,
  fajl netaknut. Rep-sidra uvek proveriti `tail -c`.
- **JSON izmene: `json.loads` validacija PRE upisa** + strukturni assert
  (skup ključeva, dužina niza) — sintaksna greška obara skript pre štete.
- **Identična vrednost u više i18n blokova → sidro preko jedinstvenog suseda.**
  `x_box_title: 'X-Ray'` x5 i `nav_xray: 'X-Ray'` x5 sidreni preko `x_ray_on`
  odnosno `nav_game` (jedinstveni po jeziku).
- **Dva assert-FAIL-a ove sesije = obrazac radi.** Oba puta nula štete, jasna
  dijagnoza, popravka u jednom potezu.

## Završno stanje
- `https://xpong.opik.net/xray.html` (s13): stranica **Telemetrija** — naslov,
  nav x5; tri infoboxa (Zrak/Beam / Heatmap / Navigacija); heatmap okviri traka
  odmah vidljivi, zrak bleđi van žive igre; X-Ray stav pomenut u intro s uputom
  na About; Key Concepts x4. Sve potvrđeno u browseru po koracima
  (s12.1→s12.5).
- xpongweb dirnuto: `app.js` (i18n zrak/telemetrija/heat box, XP_VERSION),
  `xray.js` (okviri, dim), `xray.html` (heat box, title/fallback),
  `data/concepts.json` (xray sekcija).
- M2: cigla 1 ✅, cigla 2 ✅ (kompletna). XP_VERSION s13. Bekapi u /tmp/
  (brišu se posle commita).

## Sledeće
- M2 cigla 3+ ili prelaz na M3 (RL faze) — Flaviova odluka pravca.
- (kandidat) Key Concepts iz About eseja: crna kutija, emergencija, neuronska
  mreža, transformer.
- (kandidat) health_check.py kao strukturni čeker.
- (anticipiran) sr.lat aditivno.
