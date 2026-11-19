"""Il riepilogo di tutte le prove con gli studenti virtuali: legge le cartelle sulla Scrivania e scrive
«RIEPILOGO.md» con la tabella dei risultati, i problemi trovati e le correzioni fatte."""
import re
from pathlib import Path

CARTELLA = Path.home() / "Desktop" / "Prove studenti BIBL-IA"

CORREZIONI = """## Problemi trovati con le prove e correzioni fatte nell'app

1. **Gli studenti deboli restavano bloccati sulla prima lezione** (serviva il 100% al quiz da 20 domande: con il 25% di
   risposte giuste è impossibile). → Ora: l'obiettivo resta il 100%, ma dal 3° tentativo basta l'80% e l'argomento
   resta «da consolidare» con due verifiche di memoria (3 e 7 giorni); dal 5° tentativo c'è «Vai avanti», che mette
   l'argomento nel recupero con una Flash Review; dopo 2 tentativi compaiono gli aiuti (spiegazione semplice, video,
   tutor). Risultato: Marco (25%) è passato da 16 a 46 sessioni fatte e dal 27% al 39% di preparazione.
2. **Anche i bravissimi rifacevano la stessa lezione fino a 9 volte** (con il 90% di giuste fare 20/20 riesce 1 volta
   su 8). → Risolto con la stessa soglia.
3. **Il recupero intelligente proponeva ripassi inutili** (Flash Review su argomenti al 97%). → Ora solo sotto l'80%.
4. **Piano finito = «Crea il tuo piano»**: chi finiva il piano vedeva l'invito a crearne uno. → Ora «🎉 Piano completato»
   con «Nuovo piano di consolidamento» (sulle percentuali di oggi) e «Fai una simulazione completa».
5. **La dashboard diventava lentissima con tanti errori** (8 secondi per due riquadri con 577 errori salvati).
   → Ora 0,2 secondi: le spiegazioni restano in memoria invece di essere ricopiate per ogni domanda.
6. **Nel piano le Flash Review sembravano lezioni** (stesso nome e stessa icona). → Ora «⚡ Flash Review» con il motivo.
7. **Il calendario metteva tutte le verifiche arretrate oggi** (250 minuti in un giorno) e partiva da lunedì.
   → Al massimo 2 verifiche al giorno; il calendario parte da oggi.
8. **«Quiz completati» si fermava a 30** (le attività ne tengono 30). → Ora conta il totale vero.
9. **Agli studenti delle superiori l'obiettivo del mese chiedeva 4 simulazioni** (che per la maturità non ci sono).
   → Per loro: 4 verifiche.
10. **L'obiettivo «nessun errore arretrato» era impossibile per i deboli** (centinaia di errori). → Ora «ripasso degli
    errori di oggi» (al massimo 30 al giorno).

11. **Il piano non teneva conto della data dell'esame** (esame fra 10 giorni → piano di 8 settimane, 67 sessioni).
    → Ora il piano sta nei giorni e nelle ore di studio che restano: si tengono le sessioni più importanti, con più
    spazio alle materie più deboli, e il piano lo dice («L'esame è fra 10 giorni: tenute 19 sessioni, tolte 8»).
12. **«Piano completato» mancava nella pagina del piano.** → Aggiunto, con nuovo piano di consolidamento.

13. **La prima lezione del piano andava in errore** per chi non aveva ancora scelto il formato (mappe/lezione/
    paragrafi): succedeva a ogni studente nuovo. → Corretto (si parte dalla lezione).
14. **Alcune lezioni di Chimica andavano in errore** (la stessa reazione mostrata due volte). → Corretto.
15. **In inglese molte scritte della dashboard e del piano restavano in italiano** o mezze tradotte («0% di answers
    giuste»). → Aggiunte le traduzioni.
16. **Titoli dei paragrafi tagliati a metà parola.** → Ora si tagliano tra una parola e l'altra, con «…».
18. **Per chi frequenta già l'università il piano restava vuoto** nei corsi aggiunti di recente (Scienze biologiche,
    Chimica, Fisica, Matematica, Informatica, Economia, Psicologia…): gli esami erano salvati con l'anno scritto come
    testo e l'app non li trovava (anche nell'elenco degli esami di «Quiz ed esercitazioni»). → Corretto: ora tutti i
    corsi hanno gli esami di ogni anno.
19. **Gli esami universitari non usavano le 18 materie nuove**. → Ora ogni esame prende anche i capitoli della materia
    che gli corrisponde (Fisiologia → Anatomia e fisiologia umana, Ecologia → Ecologia e scienze ambientali, Analisi
    matematica 1 → Analisi matematica…), con le loro domande spiegate.
20. **Sul telefono il logo in alto si sovrapponeva al testo** scorrendo. → La barra in alto ha uno sfondo.
17. **Nuova prova automatica**: per ogni studente virtuale si aprono tutte le 14 pagine principali
    (prove/prova_pagine_studenti.py). Ultimo risultato: 46 studenti × 14 pagine, 0 errori.

## Fatti dopo le prove (16/11)

21. **Test di livello da 36 domande** (prima 24, circa 45 minuti): il livello dato è più vicino a quello vero.
22. **Prima tappa per chi è lontano dalla soglia**: la previsione propone prima un obiettivo intermedio (per esempio
    il 60%: «🪜 Prima tappa: 60% → 37 domande al giorno» invece di 80 per l'85%) e il pulsante porta l'obiettivo del
    giorno a quella tappa.
23. **Chi studia poco ogni giorno**: con meno di un'ora il ripasso di oggi è di 10 errori e 1 sola verifica di memoria
    al giorno (con un'ora: 20 errori e 1 verifica; da un'ora e mezza: 30 e 2), così resta tempo per la sessione del
    piano. Anche il calendario segue questa regola.
24. **Simulazione per la scuola e la maturità**: in «Simulazioni d'esame» chi va alle superiori sceglie «Per la scuola»:
    prova a tempo (2 minuti a domanda) sulle sue materie al livello della sua classe; per la maturità le materie della
    seconda prova valgono metà delle domande. Voto in decimi e, per la maturità, in ventesimi. È a scelta multipla:
    misura quanto si conoscono gli argomenti, non sostituisce i problemi scritti della seconda prova.

25. **Con l'esame già passato «Impostazioni» andava in errore** (trovato perché stanotte è cambiato il giorno: l'esame
    di uno studente virtuale era «ieri»). → Ora il campo data resta vuoto e si sceglie la nuova data.
26. **Dashboard semplice** (nuova, ora quella predefinita): stesso stile e tre colonne, ma solo «Come stai»,
    «Cosa fare adesso» con un pulsante, le materie con «Quiz» e «Oggi» con le cose da fare. Le altre versioni si
    scelgono in ⚙️ Impostazioni.

## Migliorie del 16/11 (pomeriggio)

27. **Nomi dei libri**: 170 spiegazioni nate da domande costruite sui libri entravano nella ricerca della Biblioteca
    AI (e in tre casi nominavano l'autore). → Escluse, più un filtro sui nomi dei libri e degli autori.
28. **Ricerca della Biblioteca e del tutor**: «che cos'è la mitosi?» portava a «Telofase ed endometriosi». → Ora
    vengono prima i testi che definiscono proprio il concetto («La mitosi è…»); 18 domande di prova tutte giuste.
29. **Errori da rifare**: si contavano anche le domande già rifatte giuste (Marco 558 invece di 351). → Ora solo
    quelle ancora sbagliate, prima quelle sbagliate più spesso; con tanti errori il pulsante propone i 20 più importanti.
30. **AI più veloce**: il modello resta caricato 30 minuti e si carica all'avvio; nel tutor la risposta compare
    mentre viene scritta.
31. **Inglese**: 130 scritte nuove tradotte.
32. **3D**: organi e grandi molecole (tRNA, DNA, emoglobina…) si guardano nel capitolo stesso.
33. **Maturità**: «✍️ Problemi scritti» come la seconda prova; il risultato lo controlla il programma, il metodo l'AI.
34. **Menu più corto**: 16 voci invece di 24 (gli strumenti sono in «Tutti gli strumenti»).
35. **«Questa lezione era chiara?»** sotto ogni lezione; i pareri sono nell'Area docenti.
36. **Solo sul Mac**: BIBL-IA 2 non si apre più dagli altri computer della rete Wi-Fi.

## Ancora da tenere d'occhio

- I **libri su GitHub**: 12 PDF (6 protetti da diritto d'autore) e indice.json con il testo delle pagine sono nel
  repository privato. Toglierli anche dalla cronologia si può fare solo con il sì dell'utente.
"""


def numero(testo, schema, predefinito="—"):
    m = re.search(schema, testo)
    return m.group(1) if m else predefinito


def main():
    righe = ["# Prove di BIBL-IA 2 con gli studenti virtuali", "",
             "Ogni studente ha una bravura (quante risposte giuste dà), studia per 3-4 settimane con le vere funzioni "
             "dell'app (test di livello, piano, lezioni con quiz, ripasso, Flash Review, verifiche, «Rifai gli errori», "
             "simulazioni) e la bravura cresce quando studia un argomento. In ogni cartella: **piano.md** (il piano "
             "iniziale e come è andato), **diario.md** (giorno per giorno), **resoconto.md** e le foto dell'app.", "",
             "| # | Studente | Bravura | Test | Livello dato | Preparazione (inizio → fine) | Sessioni fatte | Simulazioni |",
             "|---|---|---|---|---|---|---|---|"]
    for d in sorted(p for p in CARTELLA.iterdir() if p.is_dir() and p.name[:2].isdigit()):
        r = (d / "resoconto.md").read_text(encoding="utf-8") if (d / "resoconto.md").exists() else ""
        piano = (d / "piano.md").read_text(encoding="utf-8") if (d / "piano.md").exists() else ""
        test = numero(piano, r"test: \*\*(.+?)\*\*")
        livello = numero(piano, r"livello \*\*(\w+)\*\*")
        prep = numero(r, r"Preparazione: dal test di livello (\d+%) → \*\*(\d+%)\*\*")
        prep2 = numero(r, r"→ \*\*(\d+%)\*\*")
        sessioni = numero(r, r"Sessioni del piano fatte: \*\*(\d+/\d+)\*\*")
        sim = numero(r, r"Simulazioni: (.+)")
        ultima = sim.split(", ")[-1] if sim not in ("—", "nessuna") else "nessuna"
        nome, _, resto = d.name[3:].partition(" - ")
        righe.append(f"| {d.name[:2]} | {nome} | {resto} | {test} | {livello} | {prep} → {prep2} | {sessioni} | {ultima} |")
    righe += ["", CORREZIONI]
    (CARTELLA / "RIEPILOGO.md").write_text("\n".join(righe), encoding="utf-8")
    print("\n".join(righe[:40]))


if __name__ == "__main__":
    main()
