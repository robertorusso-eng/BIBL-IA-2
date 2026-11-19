# Riscrivere le lezioni di BIBL-IA 2 (testi nostri, MAI testo dei libri)

Ogni lotto (`lotti/lotto_N.json`) è una lista di lezioni: `indice`, `materia`, `tema`, `numero`, `titolo` (spesso
brutto, fatto in automatico) e `domande` (le domande guida: dicono quali concetti tratta la lezione).

Per OGNI lezione scrivi, con parole tue e conoscenze corrette (NON copiare né parafrasare frase per frase testi di
libri; nessun nome di libro, autore o pagina), una voce in `lotto_N_lezioni.json` (oggetto: "<indice>" → voce):

```json
"12": {
  "titolo": "titolo chiaro e breve della lezione (3-8 parole), per esempio «Acidi forti e basi forti: NaOH, H₂SO₄, NaCl»",
  "introduzione": "2-3 frasi: di che cosa parla la lezione e perché è importante",
  "paragrafi": [{"titolo": "...", "testo": "un paragrafo di 5-9 frasi, chiaro e rigoroso, con esempi concreti"}],
  "punti_chiave": ["4-7 frasi brevi da ricordare"],
  "esempio": "un esempio svolto o un caso concreto (per esempio un esercizio risolto, un caso clinico semplice, un'applicazione)",
  "termini": [{"termine": "parola chiave", "definizione": "definizione in una frase"}]
}
```
- 3-6 paragrafi che coprano TUTTI i concetti delle domande guida, in un ordine logico (dal semplice al complesso).
- 4-8 termini (servono anche per i giochi di abbinamento: definizioni chiare, senza ripetere il termine).
- Livello: studente che prepara il test di ammissione o il primo anno di università (per «Medicina» livello universitario
  di base). Italiano corretto, simboli Unicode (H₂O, ², →, ⇌), niente frasi vuote.
- Lavora a blocchi di 6-8 lezioni: per ogni blocco carica il file (se esiste), aggiungi e riscrivi con uno script Python
  (json.dump ensure_ascii=False indent=1). Usa per gli script una TUA sottocartella dello scratchpad.
- Alla fine controlla con uno script che ogni indice del lotto abbia una voce con tutti i campi non vuoti.
