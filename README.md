# Gestione Ingrosso per Ristoranti e Fornitori

Questo programma è progettato per gestire le interazioni tra ristoranti e fornitori, consentendo una gestione efficiente degli ordini e dei prodotti.

## Funzionalità Principali

### Registrazione e Accesso
- **Registrazione**: Gli utenti possono registrarsi tramite email, username e password, scegliendo il tipo di account (fornitore o cliente).
- **Accesso**: Dopo la registrazione, è possibile accedere al sistema. Gli utenti possono recuperare la password dimenticata tramite un link inviato alla loro email. Durante l'accesso, devono specificare il tipo di utente.

### Funzionalità per Clienti
- **Homepage**: I clienti vedono una lista di prodotti suddivisi in categorie. È possibile filtrare i prodotti per:
  - Categoria
  - Sottocategoria
  - Fornitore
  - Nome del prodotto
- **Carrello**: Gli utenti possono:
  - Aggiungere prodotti al carrello
  - Specificare la quantità desiderata
  - Rimuovere prodotti dal carrello
  - Effettuare l'ordine di tutti i prodotti nel carrello, con conseguente pulizia del carrello
- **Storico Ordini**: I clienti possono visualizzare lo storico degli ordini, con dettagli su:
  - Data e ora dell'ordine
  - Stato dell'ordine (In sospeso o Completato)
  - Dettagli dell'ordine, con possibilità di annullarlo se ci sono prodotti in sospeso
- **Gestione Account**: I clienti possono:
  - Modificare email e username dopo aver reinserito la password
  - Cancellare il proprio account se non hanno ordini in sospeso

### Funzionalità per Fornitori
- **Homepage**: I fornitori vedono una lista dei propri prodotti in magazzino, suddivisi in categorie e filtrabili come per i clienti.
- **Gestione Prodotti**: I fornitori possono:
  - Eliminare prodotti dal magazzino, rimuovendoli anche dai carrelli e dagli ordini dei clienti
  - Modificare i dati dei prodotti
- **Inserimento Nuovo Prodotto**: I fornitori possono aggiungere nuovi prodotti specificando tutti i dettagli necessari.
- **Ordini Ricevuti**: I fornitori possono visualizzare una lista degli ordini ricevuti, con dettagli su:
  - Data e ora dell'ordine
  - Stato dei prodotti nell'ordine
  - Cliente che ha effettuato l'ordine
  - Possibilità di accettare o rifiutare singoli prodotti o interi ordini
- **Gestione Account**: I fornitori possono:
  - Modificare email e username
  - Cancellare il proprio account con le stesse modalità dei clienti

## Navigazione e Operazioni
- **Menu a Tendina**: Sia per i clienti che per i fornitori, è disponibile un menu a tendina per accedere a diverse funzioni come:
  - Controllo del carrello
  - Storico degli ordini
  - Gestione dell'account
  - Cancellazione dell'account
- **Log Out**: Gli utenti possono effettuare il log out dalla homepage.

## Considerazioni Finali
Questo programma offre una soluzione completa per la gestione degli ordini e dei prodotti tra ristoranti e fornitori, garantendo un'interfaccia user-friendly e funzionalità avanzate per entrambe le tipologie di utenti.
