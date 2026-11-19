# Revisione etica – BIBL-IA 2

BIBL-IA 2 è usato da studenti, spesso minorenni, e da professori. Per ognuna delle quattro dimensioni: il rischio concreto che abbiamo visto e la scelta di progetto con cui lo affrontiamo.

## 1. Privacy

**Rischio.** Un agente di studio raccoglie molto su uno studente: che cosa non sa, quanto studia, i voti dei quiz, le domande che fa (a volte anche sulla propria salute, nella sezione Sintomi e cure). Mandare tutto questo a un servizio di AI esterno vorrebbe dire affidare dati di minorenni a terzi, spesso all'estero.

**Scelte di progetto.**
- L'AI gira sul computer (Ollama, `gemma3:4b`): le domande e le risposte non escono dal computer.
- Per le ricerche scientifiche a Europe PMC si inviano solo le parole dell'argomento (per esempio «cell division»), mai il nome dello studente o la sua domanda intera.
- Profili, classi, account e domande fatte sono in file locali esclusi da Git: nel repository ci sono solo profili finti per i test.
- Le password sono salvate con PBKDF2 e un sale diverso per ognuna; le password del Pannello di gestione si scelgono con uno script che non le mostra mentre si scrivono.
- Chi usa BIBL-IA e i suoi dati li vede solo il proprietario seduto davanti al computer: chi arriva dalla rete o attraverso un tunnel non viene mai trattato come proprietario.

## 2. Bias e correttezza

**Rischio.** Un modello piccolo può sbagliare o semplificare troppo, e lo fa con lo stesso tono sicuro di quando ha ragione. Inoltre le ricerche scientifiche più citate vengono quasi tutte da paesi e università ricche, e un sistema che premia solo quelle mostra una scienza parziale. Infine un'app pensata per chi fa Medicina rischia di trascurare chi studia in un istituto tecnico o professionale.

**Scelte di progetto.**
- L'AI deve usare prima di tutto testi controllati di BIBL-IA e non inventare numeri; le risposte hanno una struttura fissa, più facile da controllare.
- Le ricerche passano un filtro di pertinenza e mostrano sempre l'ente che le ha fatte, così lo studente vede da dove arrivano.
- Il percorso si adatta al livello (test iniziale, argomenti deboli) e copre licei, tecnici e professionali, non solo l'università; l'app è in italiano e in inglese.
- Abbiamo misurato gli errori invece di nasconderli: nel README sono scritti i limiti noti, compreso un errore vero del modello.

## 3. Trasparenza

**Rischio.** Uno studente può prendere una frase scritta dall'AI per una verità controllata da un professore, o una scheda di salute per un consiglio medico.

**Scelte di progetto.**
- Ogni testo scritto dall'AI lo dice («🤖 Scritto dall'AI del Mac…»); le mappe dicono se sono controllate o fatte dall'AI; le risposte già pronte lo dicono («⚡ Risposta già preparata»).
- Le ricerche scientifiche hanno il titolo originale, l'ente e il link all'articolo; la sintesi in italiano è indicata come scritta dall'AI partendo dal riassunto.
- Sintomi e cure ripete in ogni scheda che «serve per studiare, non è un consulto medico» e indica le fonti ufficiali (ISS, Ministero della Salute, OMS, Manuale MSD).
- Il codice è leggibile e i criteri di scelta (soglie di somiglianza, filtri) sono scritti nei commenti.

## 4. Responsabilità

**Rischio.** Se una risposta è sbagliata, qualcuno deve poterlo vedere e correggerla; se un professore o un estraneo abusa dell'app (per esempio inserendo testo o link nascosti in un compito), gli studenti non devono pagarne le conseguenze.

**Scelte di progetto.**
- Gli studenti votano le risposte con le stelle e possono segnalarle; una risposta con 1-2 stelle viene tolta dalla banca e rifatta.
- I professori si attivano da soli solo con l'email di una scuola statale o di un'università vera; tutte le altre richieste le approva il proprietario. Il testo scritto dai professori viene ripulito da immagini, link e HTML.
- Il Pannello di gestione chiede più password insieme; ci sono limiti ai tentativi di accesso e alle richieste.
- I test automatici (prove su 10 studenti finti, prove di sicurezza su professori e classi) si rilanciano prima di ogni modifica, e un responsabile umano (il proprietario dell'installazione) decide gli aggiornamenti.
