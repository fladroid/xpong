# xpong

Treći pokušaj naslednika projekta **Pong** — browser-based platforma za
treniranje AI agenata (self-play, DQN, genetski algoritmi, X-Ray overlay).
Počinje od nule.

> Kanonski README: drži SAMO trenutno stanje. Uvek čitaj poslednju verziju.
> Hronologija je u `docs/sessions/`.

## Trenutno stanje
- **Faza:** Day-0 bootstrap završen. Još nema koda.
- **Stack:** nije odlučen.
- **Sledeće:** odluka o stacku i prvom milestone-u.

## Infrastruktura
- **Server:** `foxuno.dynu.net` (Ubuntu), user `balsam`. Sudo kod Flavija
  (root komande: Claude priprema, Flavio izvršava).
- **Repo:** `git@github.com:fladroid/xpong.git`, grana `main`.
- **Home:** `/home/balsam/xpong`.
- **Baza / drugi server:** ne koristi se.
- **Alat:** `foxuno:run_command` za sve na foxuno.

## Metoda
Radimo po METHOD dokumentu (project knowledge): show → OK → execute na svakoj
komandi; sirovi izlaz prvo; fiksno otvaranje/zatvaranje sesije; server/repo je
izvor istine, ne pamćenje.

## Struktura
    xpong/
    ├── README.md            # ovaj fajl — kanonsko stanje
    └── docs/
        └── sessions/        # hronološki zapisi sesija (session_NN.md)
