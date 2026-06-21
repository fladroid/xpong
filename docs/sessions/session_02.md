# Session 02 — Web prezentacija + TLS

**Datum:** 2026-06-21
**Tip:** Web infrastruktura — apache2 vhost + Let's Encrypt HTTPS za xpong.

## Fokus
Postaviti web prezentaciju za xpong na foxuno, po proverenom buchenberg
obrascu: poseban web repo, docroot pod /var/www, apache vhost, HTTPS preko
certbota. Bez aplikacijskog koda — i dalje samo infrastruktura + placeholder.

## Snimak zdravlja (verifikovano komandama, ne pamćenjem)
- Foxuno javni IP: 130.61.37.60 (lokalni 10.0.0.175).
- Domen: xpong.opik.net → 130.61.37.60 preko javnih resolvera (8.8.8.8, 1.1.1.1).
  Lokalni resolver na foxuno vraća prazno (stari negativni keš) — bezopasno za LE.
- Docroot: /var/www/xpong, vlasnik balsam:balsam (git bez sudo).
- Web repo: git@github.com:fladroid/xpongweb.git, grana main, commit cd20c9e.
- Apache 2.4.58 (aktivan), certbot 2.9.0.

## Šta je urađeno
- Read-only verifikacija web sloja: DNS, fajl-sistem, buchenberg apache šablon, certbot.
- Klon praznog xpongweb u /var/www/xpong; dodati placeholder index.html i
  .gitignore (*.bak*); repo-scoped identitet fladroid / fladroid@gmail.com;
  commit cd20c9e push-ovan na GitHub.
- Port-80 vhost /etc/apache2/sites-available/xpong.opik.net.conf (šablon
  buchenberg, BEZ redirecta) → a2ensite, configtest Syntax OK, reload.
- certbot --apache -d xpong.opik.net --redirect → cert izdat, napravljen
  xpong.opik.net-le-ssl.conf, dodat HTTP→HTTPS redirect, auto-renewal zakazan.
- Verifikacija spolja (--resolve): HTTPS 200, HTTP 301→https,
  cert CN=xpong.opik.net (Let's Encrypt), važi do 2026-09-19.

## Lekcije / ledger
- dynu propagacija ume da kasni; DNS verifikuj preko više javnih resolvera
  (8.8.8.8, 1.1.1.1), ne preko lokalnog — negativni keš može vraćati prazno
  iako je javno već zeleno.
- Sa foxuno lokalni resolver ne razrešava xpong.opik.net; za proveru koristi
  curl --resolve host:port:130.61.37.60.
- certbot --apache sam dodaje HTTP→HTTPS redirect (RewriteRule u :80 vhostu) i
  pravi -le-ssl.conf → početni :80 vhost piši BEZ redirecta.
- .gitignore se preslikava po obrascu, ne verbatim (buchenberg-ov je sadržajno
  specifičan: data/, books/, BBOLD/).
- Root komande (apache, certbot): Claude priprema, Flavio izvršava (connector
  balsam nema sudo).

## Završno stanje
- https://xpong.opik.net je živ: servira placeholder, HTTP→HTTPS redirect,
  valjan LE cert, automatska obnova.
- Dva repoa za xpong: xpong (backend/docs, /home/balsam/xpong) i xpongweb
  (web, /var/www/xpong) — oba pod fladroid na GitHubu.
- Aplikacijskog koda i dalje nema; web je placeholder.

## Sledeći koraci
- (otvoreno iz s01) odluka o STACK-u i prvom milestone-u za samu xpong aplikaciju.
- Zameniti web placeholder pravom prezentacijom kad bude sadržaja.
