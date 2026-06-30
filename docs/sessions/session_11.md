# Session 11 — M2 cigla 2 (deo 2): heatmap dugme→switch, kontrole u dva reda, bočne kutije + Navigacija box

**Datum:** 30 Jun 2026
**Fokus:** dovršetak ožičenja heatmapa i preuređenje kontrola/legendi po Buchenberg
identitetu. Urađeno: heatmap dugme + i18n (pa pretvoreno u SWITCH zajedno s X-Ray),
kontrole u dva reda, bočne kutije skraćene na tastere, novi Navigacija infobox,
X-Ray box proširen heatmap pomenom, x_intro "dugme→switch". Heatmap mehanika je
bila gotova iz s10; sada je i UI zatvoren.

## Otvaranje (health snapshot)
- xpong (docs) @ `21f12c8` (s11), čisto, u sinhronu.
- xpongweb (web) @ `d8ec06d` (s11), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s11'` (živo) — README, session docs, kod složni.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Šta je urađeno (XP_VERSION s12)

### (a) Heatmap dugme + i18n — pa SWITCH (cigla 2 ožičenje zatvoreno)
- Prvo: dodato dugme `#xp-btn-heat` + `x_heat_on/off` x5 u app.js (ključevi su se
  već koristili u `updateHUD` preko `gt` s EN fallbackom — dotad padali na fallback).
- Usput uočen i uklonjen **mrtav `data-i18n="x_ray_btn"`** na ray dugmetu: ključ ne
  postoji u app.js, a `t()` za nepostojeći ključ vraća SAM KLJUČ kao string → na svaku
  promenu jezika `applyI18n` bi postavio dugme na tekst "x_ray_btn", dok ga `updateHUD`
  ne vrati. Latentan bug (na load `updateHUD` istrči posle pa maskira). Skinut atribut.
- Zatim (Flaviov zahtev): četiri stavke u jednom redu su se razvlačile. Odluka —
  razdvojiti po PRIRODI: Start/Reset su AKCIJE (dugmad), X-Ray/Heatmap su STANJA
  (switchevi). Kontrole u dva reda; X-Ray i Heatmap pretvoreni u `.xp-toggle` switcheve.
- `.xp-toggle` switch komponenta je VEĆ postojala u xpong.css (verbatim port Buchenberg
  `bb-toggle`, neiskorišćena) — samo upotrebljena, nije dodavan CSS za switch.

### (b) xray.js: dugmad → switchevi (checkbox = izvor istine)
- `elBtnRay/elBtnHeat` → `elTglRay/elTglHeat` (checkbox inputi) + `elLblRay/elLblHeat`
  (span za tekst).
- Bind: `change` umesto `click`; handler čita `el.checked` i POSTAVLJA stanje
  (`rayOn = elTglRay.checked`), ne flipuje — switch je izvor istine.
- `updateHUD`: postavlja `el.checked = stanje` + tekst u label span (umesto textContent
  + classList na dugmetu).
- Tasteri `x`/`h` (`toggleRay/toggleHeat`) NETAKNUTI: flipuju stanje, `updateHUD`
  sinhronizuje checkbox. Klik na switch i taster daju isto stanje (nema duple inverzije).

### (c) Bočne kutije (legende) skraćene; novi Navigacija infobox
- Bočne kutije `Levi/Desni igrač`: uklonjeni `g_up/g_down/g_touch_left/right` iz HTML-a;
  ostaje naslov + krupno bold `W / S` (levo) i `O / L` (desno) u novom `.xp-keys` divu
  (18px, bold, letter-spacing). CSS `.xp-keys` dodat posle `.xp-game-legend-side`.
  (Ključevi g_up/g_down/g_touch ostaju u app.js — neiskorišćeni, bezopasni.)
- Novi infobox **Navigacija** (`x_nav_title`/`x_nav_text` x5) ispod X-Ray boxa: cela
  priča o kretanju na jednom mestu (levi W/S, desni O/L, touch po svojoj polovini).
  Odluka ZAJEDNO (jedan box, ne dva pola-boxa) — ista misao se ne cepa.
- Princip: bočne kutije = brza referenca (šta pritisnuti), Navigacija box = objašnjenje
  (kako radi). Isto razdvajanje akcija/objašnjenje kao kod kontrola.

### (d) X-Ray box proširen + x_intro "dugme→switch"
- `x_intro` x5: terminologija "dugme/button/Taste/pulsante/gumb" → "switch/prekidač/
  Schalter/interruttore" (tekst je zaostao za UI pošto smo prešli na switcheve).
- Dodata rečenica o heatmapu: "Heatmap switch (ili taster h) boji zid gde su golovi
  padali" x5. (PUN opis heatmapa — granularnost, senka/metapodaci okvir — ostaje za
  kasnije, kad Flavio odluči granularnost gledajući golove uživo.)

### (e) Dva infoboxa: ista širina + razmak (CSS)
- `.xray-side` (dotad bez CSS) → `display:flex; flex-direction:column; gap:16px` —
  stretch daje istu širinu, gap daje razmak.
- `.xray-side .xp-infobox { width:auto; margin:0; float:none }` — Navigacija box je
  imao `float:right; width:220px` pa bio uži/prilepljen; sad prati X-Ray box.
- X-Ray box (`.xp-xray-box`) netaknut (zadržava sticky).

## Lekcije / ledger
- **`t()` za nepostojeći ključ vraća sam ključ kao string** (`return ... : key`). Zato
  je `data-i18n` na nepostojeći ključ tih bug: `applyI18n` ga upiše kao tekst. Toggle
  dugmad/labele vođene iz JS-a NE treba da nose `data-i18n` (sukob applyI18n↔updateHUD).
- **Pre kopiranja obrasca, proveri da nije polomljen.** Ray dugme je imalo mrtav
  data-i18n; da sam ga "verno preslikao" na heat, preslikao bih bug. Proveri original.
- **Switch (stanje) vs dugme (akcija).** X-Ray/Heatmap su stanja → switch, i semantički
  i vizuelno (Buchenberg). Checkbox = izvor istine; ručni toggle (taster) samo flipuje
  pa sinhronizuje, ne drži paralelno stanje.
- **i18n vrednosti u app.js su `\u`-escaped ASCII.** Novi tekstovi generisani preko
  `s.encode('ascii','backslashreplace')` da daju isti `\u` oblik (ćirilica, dijakritike,
  IT apostrof `'`=U+2019→`\u2019`, bezbedan u JS single-quote stringu).

## Završno stanje
- `https://xpong.opik.net/xray.html` (s12): kontrole u dva reda (akcije / switchevi);
  X-Ray i Heatmap kao Buchenberg switchevi (checkbox izvor istine, tasteri x/h
  sinhronizuju); bočne kutije = bold W/S, O/L; dva infoboxa iste širine s razmakom —
  X-Ray (pominje heatmap+h) i Navigacija. 5 jezika/pisama prate. Potvrđeno u browseru.
- xpongweb dirnuto: `app.js` (x_heat/x_nav i18n, x_intro switch+heatmap, XP_VERSION s12),
  `xray.html` (dva reda, switchevi, kutije, nav box), `xray.js` (toggle→switch ožičenje),
  `xpong.css` (.xp-controls-row, .xp-keys, .xray-side flex).
- XP_VERSION s12. Bekapi obrisani.

## Sledeće
- **Heatmap objašnjenje (cigla 2 deo 2, pun opis)**: za sada samo jedna rečenica u X-Ray
  boxu. Pun opis (senka/metapodaci okvir, granularnost) — kad Flavio odluči granularnost
  gledajući golove uživo. Time je cigla 2 suštinski gotova (mehanika+kontrole+i18n).
- (kandidat) granularnost heatmapa — zasad gruba (4 trake), možda ostaje.
- (odloženo) Key Concept kartica za xray stranicu.
- (kandidat) Key Concepts iz About eseja: crna kutija, emergencija, neuronska mreža,
  transformer.
- (kandidat) health_check.py kao strukturni čeker.
- (anticipiran) sr.lat aditivno.
