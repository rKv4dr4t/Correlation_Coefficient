# getCorrelation
Lo script permette di ottenere il coefficiente di correlazione tra differenti indici estrapolati da Yahoo Finance.
Una volta eseguito lo script verrà generato un file Excel che mostrerà i risultati ottenuti.

## Setup
- Installare [Python](https://www.python.org/downloads/), quando si aprirà la schermata di setup di Python spuntare la casella 'Add Python to PATH', poi premere 'Install now'
- Successivamente installare le dipendenze aprendo il file `setup.bat` e attendere fino alla chiusura automatica della finestra

## Opzioni
All'interno del file `config.yml` (da aprire con il blocco note) si possono configurare diverse opzioni (i testi preceduti da `#` sono dei commenti e non vengono analizzati dal codice. Tutto il resto viene gestito dal codice, perciò, per evitare errori, è importante rispettare la corretta sintassi quando si modificano le impostazioni):
- `dateOn`: stampa la data del giorno odierno all'interno del nome del file Excel. I due valori validi sono `False` o `True`
- `period_timeframe` e `interval_timeframe`: sono due valori connessi tra loro. Il primo indica il periodo di tempo entro il quale vengono estrapolate le chiusure degli indici, il secondo indica l'intervallo di ripetizione che all'interno del periodo di tempo i dati devono essere estrapolati. I periodi di 15, 30, 90 e 120 giorni, di default, hanno come intervallo un giorno. Fa eccezione il periodo di un giorno che come intervallo ha un'ora. I valori del periodo di un giorno, in base all'orario in cui vengono visualizzati, possono restituire valori del giorno odierno o del giorno precedente, in caso i dati del giorno odierno non siano ancora disponibili.
- `comparisons_symbols`: rappresenta i due valori all'interno delle colonne della tabella
- `symbols`: rappresenta i valori all'interno delle righe della tabella

## Avvio
Una volta completato il setup e modificato (opzionalmente) il file `config.yml`, si può procedere ad avviare lo script tramite il file `start.bat`, il quale, dopo un caricamento di circa 2 o 3 minuti, genererà il file Excel.

## Note
La API di Yahoo Finance è una tecnologia gratuita e come tale dispone di blocchi verso qualunque tipo di spam. Per evitare blocchi temporanei quindi è importante non avviare lo script troppe volte nel giro di pochi minuti.