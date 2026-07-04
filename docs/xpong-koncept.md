# xpong — koncept i razvoj

**Autor:** Flavio (sa Claudeom)
**Status:** Živi dokument — koncept portala i metode njegovog nastanka
**Verzija:** v1

> *Ovaj dokument objašnjava šta je xpong kao ideja i kao web prezentacija, i kako nastaje. Nije README (koji drži samo trenutno tehničko stanje) niti hronologija (koja je u `docs/sessions/`) — on stoji između njih: zašto portal izgleda i raste baš ovako. Namenjen je čitaocu koji dolazi spolja i želi da razume celinu.*

---

## 1. Šta je xpong

xpong je edukativni, višejezični web portal koji uči pojmove reinforcement learning-a (RL) kroz interaktivne demonstracije klasične igre Pong. To je treći pokušaj naslednika ranijeg projekta Pong — a razlika u odnosu na pretke nije u tome šta se demonstrira, nego kako se prezentuje: xpong nije jedna aplikacija s mnogo dugmadi, nego **niz stranica gde je svaka prozor u jednu fazu razvoja veštačke inteligencije koja uči da igra**.

Motivacija nije produkcijski AI. Motivacija je učenje kroz praksu, učinjeno vidljivim. Posetilac ne dobija gotov rezultat i objašnjenje „veruj mi da radi"; dobija stranicu na kojoj vidi agenta kako se ponaša, sloj telemetrije koji pokazuje šta se dešava, i Key Concept kartice koje povezuju ono što gleda sa širim pojmovima (uz Wikipediju). Svaka stranica je jedan korak u priči: od agenta koji uopšte ne uči, preko agenta koji uči, ka složenijim tehnikama.

## 2. Vodeći stav — X-Ray

xpong je izgrađen iz jednog stava, koji projekat nasleđuje iz šireg X-Ray pamfleta: **vredi gledati unutra u sistem čak i kad spolja sve izgleda u redu — naročito tada.** Zapadna tradicija pita „kako ovo izgleda?"; X-Ray pita „šta ovo zapravo jeste?". Primenjeno na portal, to znači da nije dovoljno prikazati da agent igra — treba otvoriti prozor u to kako igra i, kasnije, kako misli.

Otuda telemetrija kao središnji motiv: heatmap, trajektorija loptice, kasnije vizualizacija procene vrednosti akcija. Inspiracija je telemetrija prenosa Formule 1 — isti sport gledan spolja i iznutra su dve različite stvari. X-Ray nije feature jedne stranice; to je stav nad celim projektom. (Zato je stranica koja nosi telemetriju svesno nazvana „Telemetrija", a ne „X-Ray" — imenovati jednu stranicu X-Ray degradiralo bi stav u puku funkciju i impliciralo da ostale stranice to nisu.)

## 3. Zašto baš višestranični portal

Ovo je najvažnija koncepcijska odluka i zaslužuje da bude eksplicitna, jer iz nje sledi skoro sve ostalo.

Pojam u učenju ima granicu. Ono što je pojmovno ili istorijski odvojeno mora i u prezentaciji biti odvojeno prikazano — inače se granica gubi. Ključno je da se **forma odvajanja bira prema publici, ne prema nama koji gradimo.** Za posetioca van struke, novi „switch" na postojećoj stranici percipira se kao još jedan feature; pojmovna granica se izgubi. Nova stranica, naprotiv, tera novost da se opazi: došao sam na drugo mesto, dakle ovo je druga stvar.

Zato pojmovi s pedagoškom težinom — random baseline, Q-learning, DQN — dobijaju svaki svoju stranicu. Posledica koja najbolje ilustruje pravilo: „agent koji ne uči" i „agent koji uči" nisu dva stanja jedne stranice s prekidačem između njih, nego **dve zasebne stranice**. Njihova pojmovna razlika je prevelika da bi je nosio switch.

Ponavljanje zajedničkog konteksta među stranicama je pritom namerno, ne lenjost: zajednička pozadina je ono naspram čega se ističe ono što je na datoj stranici novo. Stranice dele izgled i ponašanje (isti sidebar, iste kontrole telemetrije) upravo da bi razlika koja nosi pojam bila jedina stvar koja se menja i time se sama istakne.

Switch nije zabranjen i nije drugorazredan — kad razlika koju nosi nije pojmovna granica (npr. uključi/isključi sloj telemetrije), switch je tačno pravo sredstvo, i vizuelno je ravnopravan stranici jer porodica stranica deli stil pa switch reciklira umesto da duplira. Ali kad switch ipak mora da nosi pojmovnu granicu, mora biti eksplicitno uokviren — s naslovom i objašnjenjem — inače tu granicu briše.

## 4. Anatomija stranice

Stranice pripadaju „porodici" — dele šablon da bi posetilac na svakoj novoj odmah prepoznao gde šta stoji, i da bi jedina razlika bila pojam koji stranica uvodi. Tipična stranica nosi:

- **Interaktivni prikaz** — živi Pong na canvasu, kojim se može upravljati (tastatura/touch), sa agentom čije ponašanje stranica demonstrira.
- **Sloj telemetrije** — prekidači koji pale/gase prozore ka unutra: trajektorija loptice („zrak"), heatmap događaja. Telemetrija ima svoj vizuelni jezik: kad je sloj uključen ali još nema podataka, to se vidi (prazni okviri, prsten na loptici) — „živ sam, samo čekam", da uključivanje uvek da trenutni vizuelni odgovor.
- **Infoboxi** — kratka objašnjenja: šta ova stranica uvodi, šta telemetrija znači, kako se upravlja.
- **Key Concepts** — kartice koje povezuju prikaz sa imenovanim pojmovima i vode na Wikipediju; generišu se automatski po stranici iz jednog kuriranog JSON-a.

Važna granica koja se pokazala kroz razvoj: **telemetrija sveta nije telemetrija uma.** Zrak i heatmap čitaju svet — putanju loptice, mesta golova — i rade bez obzira na to ko vodi reket. Oni pripadaju svakoj stranici, uključujući onu s agentom koji uopšte ne misli. Telemetrija uma (procene vrednosti akcija, ono što agent „misli") je zaseban sloj i uvodi se tek sa stranicom na kojoj agent zaista uči. Ne meša se jedno s drugim.

## 5. Kako projekat raste — mapa faza

Razvoj ide u milestone-ima, gde svaki dodaje jedan prozor razumevanja:

- **M0** — landing i skelet portala.
- **M1** — klasičan Pong: sama igra, za dva igrača, temelj nad kojim sve ostalo stoji.
- **M2** — telemetrija: prvi X-Ray sloj nad igrom (zrak + heatmap), bez ikakve inteligencije — čista senka onoga što se dešava.
- **M3** — RL faze, jedna stranica po pojmu. Otvorena je prvom stranicom: random-walker agent, koji igra ali *ne uči* — istorijski arhetip nulte osnovice svake simulacije. Sledi agent koji uči (Q-learning), pa složenije tehnike.

Odluka da prva RL stranica bude baš „random walker" a ne „Q-agent bez učenja" sažima celo pravilo granularnosti: random walk je pojam s vlastitim imenom, istorijom i mestom u literaturi — zaslužuje stranicu. „Q bez update-a" je implementaciona faza prerušena u pojam — ne zaslužuje. Stranica se zove po pojmu koji uvodi, ne po tome gde je u nizu građenja.

Unutar jedne stranice, koraci gradnje („cigle" — skelet, pa agent, pa telemetrija, pa i18n, pa Key Concepts) nisu pojmovi i ne dobijaju svoje stranice; oni su faze rada, ne prozori razumevanja.

## 6. Prezentacija: jezik, pristupačnost, identitet

**Višejezičnost** je od početka ugrađena, ne naknadna: engleski kao baza, uz nemački, italijanski, hrvatski i srpski (ćirilica, sa strukturom koja dozvoljava da se latinica doda aditivno). Ovo nije kozmetika — u duhu šireg stava da znanje zaključano u jednom jeziku za druge ne postoji, portal se od prvog dana gradi kao višejezičan.

**Pristupačnost** se projektuje unapred, ne dodaje na kraju: visok kontrast i čitljiva tipografija su zahtev, ne opcija. Kad čitljivost i tematska doslednost dođu u sukob, čitljivost pobeđuje — vizuelne odluke (npr. boja broja na heatmap traci) donose se tako da broj bude čitljiv u obe teme, a biraju se gledanjem stvarnih varijanti u pravim bojama, ne nagađanjem.

**Tehnički identitet vs vidljivo ime** je naučena disciplina: ime fajla, interni identifikator stranice i i18n prefiks postavljaju se jednom i ostaju stabilni; vidljivo ime stranice sme slobodno da evoluira. Stranica čiji su fajlovi `xray.*` u međuvremenu se zove „Telemetrija" — jer preimenovanje fajlova lomi linkove bez ikakve dobiti, dok je vidljivo ime stvar prezentacije. Identitet je adresa; ime je natpis na vratima.

**Look & feel** je namerno pozajmljen iz srodnog projekta (Buchenberg) — deljena estetika i konvencije znače da porodica stranica izgleda kao celina, i da nova stranica počinje od proverenog šablona umesto od nule.

## 7. Metoda rada

xpong nastaje kroz saradnju čoveka i AI-ja po dokumentovanoj metodi (detaljno u zasebnom METHOD dokumentu). Suština relevantna za ovaj koncept:

- **Podela po komparativnoj prednosti.** Flavio drži strateški pravac, konačne odluke, domensko znanje i infrastrukturu; Claude implementaciju, verifikaciju i kontinuitet kroz mnoge sesije. Nijedna strana ne popušta naslepo — neslaganje se iznosi i rešava u dijalogu, odluka je čovekova.
- **Prikaži → OK → izvrši.** Svaka komanda se vidi u celosti pre nego što se pokrene. Ništa se ne dešava iznutra što nije prvo bilo vidljivo — isti X-Ray stav okrenut ka samom procesu izgradnje.
- **Server je izvor istine, ne pamćenje.** Svaka sesija počinje snimkom stvarnog stanja repozitorijuma i živog sajta; pamćenje (ljudsko ili AI) sme da bude zastarelo, kod ne.
- **Fiksni ritam sesije.** Svaka se otvara istim onboarding redom (pročitaj kanonske dokumente, pa poslednje zapise, pa snimak zdravlja) i zatvara istim ritualom (zapis sesije, ažuriranje kanonskih dokumenata ako se nešto trajno promenilo, verzija, commit i push). Ritam, a ne ničije sećanje, nosi projekat kroz mnoge sesije.
- **Iterativno, verifikovano u pregledaču.** Deploy → pogledaj uživo → javi → podesi. Odluke se često menjaju tek kad se rezultat vidi — i to je tretirano kao vrednost saradnje, ne kao neodlučnost.

Dokumentacija je razdvojena po ulozi: **README** drži samo trenutno kanonsko stanje i prepisuje se; **session zapisi** su nepromenljiv hronološki trag „kako smo došli dovde"; a ovaj **koncept-dokument** stoji iznad oba i objašnjava „zašto ovako". Svaka trajna lekcija iz razvoja upisuje se tamo gde će je sledeća sesija naći — što je i samo primena X-Ray stava na saradnju: proces koji beleži sam sebe može se pregledati i popraviti.

## 8. Šta xpong nastoji da bude

Kad bude zreliji, xpong treba da bude mesto na koje neko dođe bez pretpostavke o predznanju iz AI-ja i, prolazeći kroz stranice redom, stekne ne samo „znam da ovo radi" nego „vidim kako i zašto radi". Portal koji ne skriva unutrašnjost iza glatke fasade, nego je otvara sloj po sloj — jedan pojam, jedna stranica, jedan prozor u isto vreme.

To je X-Ray pretvoren u web prezentaciju: ne gledati samo izlaz, nego graditi prozore ka unutra — i pozvati posetioca da pogleda kroz njih.

---

*Flavio & Claude · xpong-koncept · v1 · 2026*
