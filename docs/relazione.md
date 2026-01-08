# Sviluppo e confronto di euristiche per il TSP simmetrico

---

## Introduzione

Il *Problema del Commesso Viaggiatore* (*Traveling Salesman Problem*, TSP) è uno dei problemi di ottimizzazione combinatoria più studiati in letteratura.  
Dato un insieme di città e le distanze tra ogni coppia di esse, l’obiettivo è determinare il tour di costo minimo che visita ogni città esattamente una volta e ritorna alla città di partenza.

Nel caso *simmetrico*, considerato in questo progetto, la distanza tra due città è la stessa in entrambe le direzioni.  
Il TSP simmetrico è un problema **NP-difficile**, per cui il tempo richiesto per trovare la soluzione ottima cresce esponenzialmente con la dimensione dell’istanza.

---

## Motivazioni del lavoro

Nonostante l’esistenza di modelli esatti basati sulla *Programmazione Lineare Intera* (PLI), come quelli risolvibili tramite solver commerciali (ad esempio Gurobi), tali approcci risultano impraticabili per istanze di dimensione medio-grande a causa dell’elevato costo computazionale.

Per questo motivo, in applicazioni reali si ricorre frequentemente a:

- **euristiche deterministiche**, rapide ma approssimate;
- **euristiche randomizzate**, in grado di esplorare lo spazio delle soluzioni in modo più efficace;
- **modelli esatti**, utilizzati come riferimento per valutare la qualità delle soluzioni euristiche su istanze di piccole dimensioni.

---

## Obiettivi del progetto

L’obiettivo principale di questo progetto è sviluppare, implementare e confrontare diverse strategie di risoluzione del TSP simmetrico, valutandone l’efficacia in termini di **qualità della soluzione** e **tempo di calcolo**.

In particolare, vengono considerate:

- una euristica deterministica costruttiva (*Greedy – Nearest Neighbor*);
- una euristica di miglioramento locale basata su mosse *2-opt*;
- una euristica randomizzata (*Simulated Annealing*);
- un modello esatto di Programmazione Lineare Intera basato sulla formulazione *MTZ*, risolto tramite il solver Gurobi.

---

## Contributi principali

Il progetto fornisce:

- un’implementazione modulare e riproducibile degli algoritmi;
- un confronto sperimentale su istanze TSPLIB di diversa dimensione;
- un’analisi quantitativa basata su:
  - costo del tour;
  - tempo di esecuzione;
  - gap percentuale rispetto alla soluzione ottima;
- una valutazione del *trade-off* tra qualità della soluzione e costo computazionale.

---

## Struttura della relazione

La relazione è organizzata come segue:

- **Sezione 2**: metodologia e descrizione degli algoritmi utilizzati;
- **Sezione 3**: impostazione sperimentale e dataset;
- **Sezione 4**: risultati sperimentali e analisi comparativa;
- **Sezione 5**: conclusioni e possibili sviluppi futuri.

---

## Metodologia

### Definizione del problema

Dato un insieme di `n` città e una matrice delle distanze simmetriche `d_ij`, il problema del TSP consiste nel determinare una permutazione delle città tale da minimizzare il costo totale del tour, visitando ciascuna città esattamente una volta e ritornando alla città di partenza.

---

### Euristica Greedy (Nearest Neighbor)

La prima strategia considerata è un’euristica deterministica costruttiva basata sull’approccio *Nearest Neighbor*.  
A partire da una città iniziale fissata, l’algoritmo seleziona iterativamente la città non ancora visitata più vicina alla città corrente.

Questo metodo è estremamente veloce, con complessità computazionale `O(n²)`, ma soffre di un comportamento miope che può portare a soluzioni di bassa qualità, soprattutto per istanze di dimensione maggiore.

---

### Local Search con 2-opt

Per migliorare la soluzione iniziale ottenuta con l’euristica Greedy, viene applicata una procedura di *local search* basata sulla mossa *2-opt*.  
Questa tecnica consiste nel rimuovere due archi dal tour e riconnettere i segmenti risultanti invertendo una sottosequenza del percorso.

La scelta della mossa 2-opt, invece della più complessa 4-opt, è motivata dal buon compromesso tra:

- qualità delle soluzioni ottenute;
- semplicità di implementazione;
- costo computazionale contenuto.

Il 4-opt introduce un vicinato molto più ampio e costoso da esplorare, non giustificato rispetto agli obiettivi comparativi del progetto.

L’algoritmo 2-opt viene iterato fino al raggiungimento di un ottimo locale, producendo un significativo miglioramento rispetto alla soluzione Greedy iniziale.

---

### Simulated Annealing

Per evitare il rischio di rimanere intrappolati in ottimi locali, è stata implementata una euristica randomizzata basata sul *Simulated Annealing* (SA).

L’algoritmo parte da una soluzione iniziale (in questo caso la soluzione migliorata da 2-opt) e, a ogni iterazione, genera una soluzione vicina mediante una mossa 2-opt casuale.  
Le soluzioni peggiorative possono essere accettate con una probabilità che dipende da una temperatura `T`, che decresce progressivamente secondo una legge di raffreddamento.

Per diverse istanze (`eil51`, `berlin52`, `st70`, `pr76`, `rat99`) il Simulated Annealing non migliora ulteriormente la soluzione 2-opt, producendo soluzioni di costo identico.  
Su istanze più complesse (ad esempio `kroA100`), invece, riesce a ottenere soluzioni migliori, confermando la maggiore robustezza delle metaeuristiche randomizzate.

---

### Modello esatto: formulazione MTZ

Come riferimento per la valutazione delle soluzioni euristiche, è stato implementato un modello esatto di Programmazione Lineare Intera basato sulla formulazione di Miller–Tucker–Zemlin (MTZ).

Il modello utilizza:

- variabili binarie `x_ij` che indicano se l’arco `(i,j)` è incluso nel tour;
- variabili ausiliarie `u_i` per eliminare i sottocicli.

Il modello è stato risolto tramite il solver Gurobi, imponendo un limite massimo di tempo per evitare tempi di esecuzione eccessivi.

---

## Ambiente sperimentale e risultati

### Confronto dei costi delle euristiche

Vedere su  
`/Users/lucacapone/PycharmProjects/AMODproject/results/figures/confronto_costi.png`

---

### Miglioramento percentuale rispetto a Greedy

Vedere su  
`/Users/lucacapone/PycharmProjects/AMODproject/results/figures/miglioramento_percentuale.png`

---

### Riduzione assoluta del costo

Vedere su  
`/Users/lucacapone/PycharmProjects/AMODproject/results/figures/riduzione_assoluta.png`

---

### Gap percentuale rispetto alla soluzione ottima

Vedere su  
`/Users/lucacapone/PycharmProjects/AMODproject/results/figures/gap_vs_mtz.png`

---

### Tempi di esecuzione

Vedere su  
`/Users/lucacapone/PycharmProjects/AMODproject/results/figures/tempi_confronto.png`

---

## Conclusioni

Il confronto sperimentale mostra che le euristiche di miglioramento locale rappresentano una soluzione estremamente efficace per il TSP di dimensione medio-grande.  
Il modello MTZ garantisce l’ottimo ma risulta poco scalabile, mentre 2-opt e Simulated Annealing offrono soluzioni di alta qualità in tempi trascurabili.

---

### Sviluppi futuri

Possibili estensioni includono:

- metaeuristiche avanzate (Tabu Search, Algoritmi Genetici);
- formulazioni PLI più forti (DFJ con generazione di tagli);
- estensione al TSP asimmetrico o a varianti reali del problema.
