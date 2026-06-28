# Session 09 — M2 cigla 1: X-Ray trajektorni zrak (+ pong-core refaktor, game deck layout)

**Datum:** 28 Jun 2026
**Fokus:** otvaranje M2. Tri koraka: (0) izdvajanje fizike u deljeni
`pong-core.js` bez promene ponašanja, (layout) podizanje legendi u liniju sa
status/dugmadima na game stranici, (1) X-Ray stranica sa trajektornim zrakom —
„cigla 1" od M2. Cigle 2 (heatmap) i parametri nisu rađene ove sesije.

## Otvaranje (health snapshot)
- xpong @ `1534fab` (s08), čisto, u sinhronu.
- xpongweb @ `0579469` (s08), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s08'` (živo) — README, session docs i kod složni.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Odluka: opseg M2 (zaključano kroz razgovor)
M2 = X-Ray overlay stranica, **bez inteligencije ikad**. Nema učenika → nema
uma za rendgenisanje; pravi agent pripada budućim RL stranicama. Tri cigle
zamišljene: (1) trajektorni zrak, (2) heatmap golova po kvadrantima,
(3) parametri — ali **parametri ispali iz M2** na Flaviov zahtev (konstante
ostaju izolovane u pong-core za kasnije). Okvir: zrak = pravila učinjena
vidljivim, heatmap = senka/metapodaci.

**Ograničenje iskrenosti zraka:** zrak baca lopticu unapred čistom fizikom do
PRVE prepreke (zid/reket/gol), pa bledi. Nikad ne predviđa odboj ni nečiji
potez — staje gde prestaje izvesnost. Poklapa se s fizikom: nema `Math.random`
u zoni odbijanja od zida (random samo na servisu `resetBall` i u uglu odbijanja
od reketa koji je determinističan po mestu udara). Zrak je tačan bez ikakvog
seed/sync mehanizma.

## Šta je urađeno

### Cigla 0 — refaktor fizike (commit `e7a3b6b`)
Izabran „put C": čista fizika izdvojena u nov `pong-core.js` (bez DOM-a),
izlaže `window.xpong.PongCore`: `C` (konstante W800/H500, PADDLE_*, BALL_R,
brzine, WIN_SCORE 11), `newState()`, `resetBall(state,dir)`, `clampPaddle(p)`,
`bounce(ball,paddle)`, `stepBall(state)` (vraća tip kolizije
`wall|paddleL|paddleR|goalL|goalR|null`), i `castRay(state,maxSteps)` (klonira
samo lopticu, čita reketе po referenci na trenutnoj poziciji, ide do prve
prepreke, vraća `{points:[...], stop}`). `game.js` stanjen na input/render/HUD,
zove `Core.*`. `game.html` učitava pong-core.js pre game.js. M1 potvrđen
nepromenjen u brauzeru.

### Layout — game deck (commit `2e638e8`)
Legende podignute u `.xp-game-deck` flex red: [leva legenda | status+Start/Reset
| desna legenda], legende na fizičkoj strani svog reketa (W/S levo, O/L desno).
Mobilni media kolaps u kolonu (centar prvi). Dirnuto game.html + xpong.css.

### Cigla 1 — X-Ray zrak (commit `4df58f1`)
- `xray.js` — standalone PongCore consumer, isti input/render skelet kao game.js
  PLUS `drawRay()`: isprekidana linija u akcent boji preko `castRay`, bledi ka
  kraju (alpha po segmentu), marker kruga na kontaktu SAMO za zid/reket (ne gol).
- `xray.html` — iz game.html šablona, sidebar layout.
- Nav: `xray` stavka već postojala sa `soon:true` — samo skinut `soon`.
- **Sidebar layout** (opcija A, na Flaviov zahtev posle gledanja): `#xray-layout`
  grid `1fr 280px`, uvodni tekst u `.xp-infobox.xp-xray-box` (sticky, override
  float). Igra levo, infobox desno; uzak ekran → 1 kolona, box pod igrom.
- **Dugme-prekidač**: tekst „X-Ray: on/off" prati stanje, okvir (akcent klasa)
  prati stanje. Zrak **isključen na startu** (`rayOn=false`), off-dugme bez
  okvira. Taster `x` radi isto.
- **Manji marker**: `BALL_R-2` (6px), linija 1.5px (prvobitno BALL_R+3/2px).
- **i18n x5**: `x_title`, `x_intro`, `x_box_title`, `x_ray_on`, `x_ray_off`
  (EN/DE/IT/HR latinica, SR ćirilica). Verzija s08 → s09.2.

## Lekcije / ledger
- **Footer u app.js je sirov UTF-8, ne `\u` escape.** Sidrišta za zamenu
  `x_ray_btn`→on/off prvo asertovala na `\u00b7` i `\u`-ćirilici za footer →
  `assert count==1` pukao (count 0), ništa upisano. `cat -A` pokazao `M-BM-7`
  (sirov · U+00B7) i sirovu ćirilicu. Popravka: sidrišta sa sirovim znakovima u
  UTF-8 Python izvoru. Pouka: pre sidrenja na susednu liniju, proveri njen
  *stvarni* bajt-oblik (`cat -A` / `grep`), ne pretpostavljaj escape konvenciju.
- **`cut -c` podela čistija od `fold | tr` za heredoc transport.** s08 obrazac
  (`fold -w3900 | tr -d '\n`) jednom dao krnji prenos (md5 promašaj uhvatio).
  Čistije: `base64 -w0 > full.b64`, pa `cut -c1-3400`/`cut -c3401-` (ili
  `split -b 3400`) → spoj plain `cat` bez `tr`. Manje fajlova, bez `\n` koji se
  mora skidati. md5 i dalje obavezan pre dekodiranja/pokretanja.
- **md5 + „OK" izlaz hvataju obe vrste kvara.** md5 promašaj = krnji transport
  (ništa upisano jer dekodiranje/ast padne). md5 pogodak ali nema „OK" = assert
  pukao u skripti (sidrište ne valja) → backup se pravi tek pred upis, pa
  original netaknut. Oba puta: nula štete, jasna dijagnoza.
- **xray.js se deli na 5 b64 komada** (~14.3k b64), ne 3-4. `split -b 3400` dao
  pouzdano; lokalna rekonstrukcija + md5 pre slanja potvrdila broj komada.

## Završno stanje
- `https://xpong.opik.net/xray.html` (s09.2): X-Ray stranica radi — sidebar
  infobox desno, trajektorni zrak (off na startu, dugme-prekidač on/off +
  okvir, taster x), manji marker, sve 5 jezika sa ćirilicom, teme prate.
  Potvrđeno u brauzeru kroz tri iteracije (s09.1 sidebar+prekidač-bez-teksta,
  s09.2 on/off tekst + off-na-startu).
- M1 game stranica: legende podignute u liniju (game deck), nepromenjeno
  ponašanje igre.
- pong-core.js: deljena čista fizika, izvor za game.js i xray.js.
- xpongweb @ `4df58f1`, čisto, push-ovano (3 commita: refaktor, layout, cigla 1).
- Bekapi obrisani sa servera.

## Sledeće
- **M2 cigla 2 — heatmap golova** po kvadrantima (granularnost odložena: odluči
  gledajući žive golove). Okvir: senka/metapodaci, ne um.
- (odloženo) Key Concept kartica za xray stranicu.
- (kandidat, otvoren) Proširenje Key Concepts iz About teksta: crna kutija,
  emergencija, neuronska mreža, transformer arhitektura.
- (kandidat) health_check.py kao strukturni čeker kad struktura poraste.
- (arhitektonski anticipiran) `sr.lat` — `sr.cyr` podstruktura dozvoljava
  aditivno dodavanje bez refaktora.
