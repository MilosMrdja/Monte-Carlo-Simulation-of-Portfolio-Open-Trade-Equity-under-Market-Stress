# 📈 Monte-Carlo-Simulation-of-Portfolio-Open-Trade-Equity-under-Market-Stress

## 0. Trading domen

### 0.1. Kontekst: Finansijska tržišta i inženjering

Domen finansijskog trgovanja (engl. Trading) postaje sve više dostupan široj populacijia, naročito među mladim biznismenima, među kojima se nalaze institucionalni investitori, individualni korisnici i poslovni subjekti. Ovde ključnu ulogu imaju **brokerske platforme** koji su posrednici između korisnika i **berze** (engl. Exchange), gde se vrše transkacije putem **finansijskih instrumenata** (engl. Assets). Instrumenti mogu biti bilo šta čime se trguje kao što su akcije, obveznice, valute, derivati.
korisnik, nakon verifikacije, alocira kapital za kupovinu određenog instrumenta po trenutnoj ceni, berza diktira cenu. (engl. Entry price). Kroz vreme tržišna cena (engl. Market price) je fluktuira konstantno, što direktno utiče na vrednost investicije instrumenata.

### 0.2. Definisanje problema i metrika OTE

Glavni izazov brokera jeste da blagovremeno i precizno kvantitifikuje finansijski položaj korisnikovog portfolija. S obzirom na to da ozbiljni investitori drže milione jedinica (engl. Position size) različitih instrumenata tokom dužeg vremena (meseci, godine), a tržište se menja u realnom vremenu, kompleksnost proračuna eksponencijalno raste.
Ključna metrika koja definiše stanje portfolija je **Open Trade Equity (OTE)**.

OTE je nerealizovani profit/gubitak portfolija u datom vremenu _t_. On se računa kao razlika između trenutne tržišne vrednosti pozicije i njene ulazne cene:

$\text{OTE}_t = (\text{Tržišna Cena}_t - \text{Ulazna Cena}) \times \text{Količina Instrumenta}$

Centralni problem je u računarskoj složenosti (engl. Computational complexity), potreba za konstantim izračunavanjem OTE-a za milione pozicije koje se tiču hiljade klijenata u situacijama gde je nepohodno modelovati **rizične scenarije** (engl. Stress testing) koji zahteva masovnu paralelizaciju (engl. High-Performance computing) i optimizaciju, koja bi se inače izvršavala predugo u realnom vremenu(engl. Ex-Post Risk Analysis). Ako platforma nema mogućnost izveštavanje potencijalnih ishoda i predikcija (engl. Ex-Ante Risk Analysis), postaje skoro neupotrebljiva, odnosno zastarela, mnogim preduzetnicima nije dovljno izveštavanje o trenutnom stanju.

### 0.3. Metodologija: Monte Carlo simulacija pod tržišnim stresom

Da bismo pomoću OTE-a izračunali budući rizik koristićemo **Monte Carlo simulaciju**

- Model: Kretanje cene instrumenata modelovano je korišćenjem Geometrijskog Braunovog Kretanja (GBM), stohastičkog procesa koji uključuje drift ($\mu$) (očekivani prinos) i volatilnost ($\sigma$) (meru neizvesnosti).
- Stres Testing: U model je implementiran uslovni mehanizam tržišnog stresa, gde nagli pad cene privremeno povećava volatilnost, simulirajući realne fenomene panike i tržišnih krahova.

## 1. Uvod i Definicija Problema (HPC Tema)

Ovaj projekat se bavi problemom iz oblasti **Računarstva visokih performansi (HPC)** radjena na predmetu "napredne tehnike programiranja" na 4. godini osnovnih akademskih studija. Izabrana tema je **Monte Carlo Simulacija Evolucije Portfolio Open Trade Equity (OTE) pod uslovima tržišnog stresa**.

### 1.1. OTE i Tržišni Stres

**Open Trade Equity (OTE)** predstavlja nerealizovani profit ili gubitak portfolija u datom trenutku. Da bi se kvantifikovao rizik i potencijal, neophodno je simulirati hiljade (ili milione) mogućih budućih scenarija kretanja cene imovine.

- **Modeliranje Cene:** Koristi se **Geometrijsko Braunovo Kretanje (Geometric Brownian Motion - GBM)** kao stohastički proces za simulaciju kretanja cene:
  $$S_{t+1} = S_t \cdot \exp\left( (\mu - \frac{\sigma^2}{2})\Delta t + \sigma \sqrt{\Delta t} Z \right)$$
  Gde je prvi sabirak deterministički deo očekivani prinos (engl. Drift), a drugi stohastički deo slučajni šok.
- **Stres Mehanizam:** Da bi simulacija bila realistična, uvodi se mehanizam **tržišnog stresa**. Ako stopa prinosa padne ispod definisanog praga (npr. -2% dnevno), volatilnost (standardna devijacija prihoda) ($\sigma$) se privremeno multiplikuje (npr. $\sigma \times 3$), simulirajući paniku na tržištu i povećanu neizvesnost.
- **Iterativna Priroda:** Problem je iterativne prirode, jer cena u trenutku $t+1$ zavisi od cene u trenutku $t$, što čini rešenje pogodnim za praćenje promena stanja sistema po koracima (danima).

### 1.2. HPC I Strukturna Paralelizacija

Ova tema spada u kategoriju **"Embarrassingly Parallel"** problema. Svaka pojedinačna Monte Carlo putanja (simulacija) je nezavisna od ostalih putanja. Ovo omogućava minimalnu komunikaciju između procesa/niti, što obećava izuzetno visoko ubrzanje i efikasno skaliranje, što je idealno za demonstraciju Amdalovog i Gustafsonovog zakona.

---

## 2. Arhitektura Rešenja i Sistematika

Rešenje je implementirano u dva jezika (Python i Rust) sa sekvencijalnom i paralelnom verzijom, prateći striktne zahteve zadatka.

### 2.1. Implementacija u Pythonu (25 poena)

| Verzija            | Tehnologija                            | Izlaz (Stanje Sistema)                                |
| :----------------- | :------------------------------------- | :---------------------------------------------------- |
| **Sekvencijalna**  | Standardni Python + `numpy` biblioteka | `python_seq_results.csv` (Statistika OTE-a po danima) |
| **Paralelizovana** | `multiprocessing` biblioteka           | `python_par_results.csv` (Statistika OTE-a po danima) |

- **Stanje Sistema:** Datoteke beleže promene stanja sistema na nivou dnevnih agregata (srednja vrednost, percentili, min/max OTE vrednosti) iz svih $N$ simulacija, čime se izbegava I/O usko grlo pri zapisivanju celih miliona putanja.

### 2.2. Implementacija u Rustu (26 poena)

| Verzija            | Tehnologija                                        | Izlaz (Stanje Sistema)                              |
| :----------------- | :------------------------------------------------- | :-------------------------------------------------- |
| **Sekvencijalna**  | Standardni Rust, Cargo                             | `rust_seq_results.csv` (Statistika OTE-a po danima) |
| **Paralelizovana** | Niti (`std::thread` / `std::sync` / `rayon` crate) | `rust_par_results.csv` (Statistika OTE-a po danima) |

- **Fokus:** Rust implementacija koristi nativne niti i fokusira se na efikasno korišćenje memorije i minimalan _runtime_ trošak, očekujući značajno veće realno ubrzanje u odnosu na Python implementaciju.

### 2.3. Paralelni i serijski pristup

#### A. Struktura Podataka (Matrica Stanja Sistema)

Za obe implementacije, stanje modelovanog sistema se čuva u **dvodimenzionalnoj strukturi** (nizu (nizova/vektora)) / matrici), gde je:

- **Redovi:** Predstavljaju vremenske korake (npr. dani \( t = 1, 2, ..., 252 \)).
- **Kolone:** Predstavljaju pojedinačne Monte Carlo putanje (simulacije \( N_1, N_2, ..., N_k \)).

Svaki element matrice na poziciji \( (t, N) \) predstavlja **OTE vrednost** na dan \( t \) za simulaciju \( N \).

---

#### B. Serijski (Sekvencijalni) Pristup

- Serijski pristup izvršava sve \( N \) simulacija **redom**, jednu za drugom, na **jednom procesorskom jezgru**.

Algoritam sekvencijalno prolazi kroz **kolone matrice** (Monte Carlo simulacije) i za svaku simulaciju izračunava kompletan niz vremenskih koraka (redova) pre prelaska na sledeću simulaciju.

- **Simulacija \( N_1 \):**  
  Izračunava se OTE za \( t = 1, 2, ..., 252 \)

- **Simulacija \( N_2 \):**  
  Izračunava se OTE za \( t = 1, 2, ..., 252 \)

- ...

- **Simulacija \( N_k \):**  
  Izračunava se OTE za \( t = 1, 2, ..., 252 \)

---

#### C. Paralelni Pristup (Strategija Raspodele Posla)

Paralelna implementacija koristi strategiju **dekompozicije podataka** (engl. Data Decomposition) i
ovo je model koji se može lako pralelizovati (engl. Embarrassingly Parallel)

Ukupan broj simulacija _N_ deli se empirijski (ravnomerna podela) na _P_ dostupnih procesorskih jezgara ili niti.

- Posao \( Posao*i \) za jezgro \_i* predstavlja izračunavanje  
  _N_ / _P_  
  nezavisnih Monte Carlo putanja.

##### Raspodela po jezgrima

- **Jezgro 1:** računa putanje od 1 do _N_ / _P_
- **Jezgro 2:** računa putanje od (_N_ / _P_) + 1 do _2N_ / _P_
- ...
- **Jezgro P:** računa preostale putanje

---

## 3. Eksperimenti Skaliranja (9 + 10 poena)

### 3.1. Amdalov Zakon (Jako Skaliranje)

Veličina problema je fiksna, i postavlja se pitanje koliko brzo se može uraditi posao. Vreme izvršavanja je ogrnaičeno delom koda koji mora da se izvršava serijski.

- **Definicija:** Fiksira se **ukupan obim posla** ($N$ simulacija), a povećava se **broj procesorskih jezgara** ($P$).
- **Merenje:** Upoređuje se vreme izvršavanja $T(1)$ sa $T(P)$ (Vreme izvršavanje na jednom jezgru i na P jezgara).
- **Grafici:** Jako skaliranje u pyton-u i rust-u

### 3.2. Gustafsonov Zakon (Slabo Skaliranje)

Vreme izvršavanje je fiksno, suština je da za isto vreme uradimo što više posla. Veličina problema raste zajedno sa brojem jezgara.

- **Definicija:** Fiksira se **obim posla po jezgru** ($N/P$), a istovremeno se povećava **broj jezgara** ($P$) i **ukupan obim posla** ($N$).
- **Manipulacija Poslom:** Konstanta opterećenja po jezgru se postiže dinamičkim podešavanjem broja simulacija: $N_{ukupno} = P \times N_{bazno}$.
- **Grafici:** Slabo skaliranje u pyton-u i rust-u

## 4. Vizualizacija Rešenja (10 poena)

Vizualizacija je urađena korišćenjem **Rust okruženja** i biblioteke **Plotters**.

- **Cilj:** Vizuelna reprezentacija rizika i potencijala.
- **Tip Grafika:** **Konus Neizvesnosti (Cone of Uncertainty)**.
- **Elementi:**
  1.  Prosečna OTE putanja (**Mean**) - linija koja prolazi tačno kroz sredinu svih mogućih scenarija.
  2.  Oblast senčenja koja predstavlja **90% Interval Poverenja** (između 5. i 95. percentila) – ovo vizuelno prikazuje rizik, dok je donja linija na grafiku najbintija jer prikazije najgori mogući slučaj.

---

- **NAPOMENA** Tokom rada moguća mala izmena navedenih biblioteka ili pristupa rešenju ukoliko bude bilo potrebno

---
