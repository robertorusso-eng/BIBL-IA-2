"""Il laboratorio di BIBL-IA 2: reazioni controllate («cosa succede se sommo…?») e impianti chimici.

Ogni reazione è scritta a mano con l'equazione bilanciata, che cosa si allontana (gas ↑, precipitato ↓, acqua),
il tipo e le condizioni. Gli impianti sono gli schemi dei processi industriali classici studiati in
ingegneria chimica, con le condizioni operative tipiche dei manuali.
"""

# allontana: che cosa «se ne va» o si separa (gas che si libera ↑, solido che precipita ↓, acqua che si forma)
REAZIONI = [
    # --- Acidi e basi ---------------------------------------------------------------------------------
    {"reagenti": ["HCl (acido cloridrico)", "NaOH (idrossido di sodio)"], "prodotti": ["NaCl (cloruro di sodio)", "H₂O"],
     "equazione": "HCl + NaOH → NaCl + H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si forma acqua; il sale resta sciolto. Nessun gas.",
     "spiegazione": "L'H⁺ dell'acido e l'OH⁻ della base si uniscono e formano acqua: la soluzione diventa neutra "
                    "(pH 7 se le moli sono uguali). La reazione libera calore (esotermica)."},
    {"reagenti": ["H₂SO₄ (acido solforico)", "NaOH (idrossido di sodio)"], "prodotti": ["Na₂SO₄ (solfato di sodio)", "H₂O"],
     "equazione": "H₂SO₄ + 2 NaOH → Na₂SO₄ + 2 H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si formano 2 molecole d'acqua.",
     "spiegazione": "L'acido solforico è diprotico: cede 2 H⁺, quindi servono 2 NaOH per neutralizzarlo."},
    {"reagenti": ["HNO₃ (acido nitrico)", "KOH (idrossido di potassio)"], "prodotti": ["KNO₃ (nitrato di potassio)", "H₂O"],
     "equazione": "HNO₃ + KOH → KNO₃ + H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si forma acqua.", "spiegazione": "Acido forte + base forte: sale neutro e acqua."},
    {"reagenti": ["HCl (acido cloridrico)", "Ca(OH)₂ (idrossido di calcio)"], "prodotti": ["CaCl₂ (cloruro di calcio)", "H₂O"],
     "equazione": "2 HCl + Ca(OH)₂ → CaCl₂ + 2 H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si formano 2 molecole d'acqua.", "spiegazione": "Ca(OH)₂ ha due OH⁻: servono 2 HCl."},
    {"reagenti": ["HCl (acido cloridrico)", "Mg(OH)₂ (idrossido di magnesio)"], "prodotti": ["MgCl₂ (cloruro di magnesio)", "H₂O"],
     "equazione": "2 HCl + Mg(OH)₂ → MgCl₂ + 2 H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si forma acqua.",
     "spiegazione": "È come agisce un antiacido: l'idrossido di magnesio neutralizza l'acido dello stomaco."},
    {"reagenti": ["HCl (acido cloridrico)", "NH₃ (ammoniaca)"], "prodotti": ["NH₄Cl (cloruro di ammonio)"],
     "equazione": "HCl + NH₃ → NH₄Cl", "tipo": "Acido-base (secondo Brønsted)",
     "allontana": "Niente: se i due gas si incontrano si forma un fumo bianco di cloruro di ammonio solido.",
     "spiegazione": "L'ammoniaca accetta l'H⁺ (base di Brønsted) e diventa ione ammonio NH₄⁺."},
    {"reagenti": ["CH₃COOH (acido acetico)", "NaOH (idrossido di sodio)"], "prodotti": ["CH₃COONa (acetato di sodio)", "H₂O"],
     "equazione": "CH₃COOH + NaOH → CH₃COONa + H₂O", "tipo": "Acido-base (neutralizzazione)",
     "allontana": "Si forma acqua.",
     "spiegazione": "Acido debole + base forte: al punto di equivalenza la soluzione è leggermente basica (pH > 7), "
                    "perché lo ione acetato è una base debole."},
    # --- Carbonati e bicarbonati: si libera CO₂ ---------------------------------------------------------
    {"reagenti": ["HCl (acido cloridrico)", "NaHCO₃ (bicarbonato di sodio)"], "prodotti": ["NaCl", "H₂O", "CO₂ ↑"],
     "equazione": "HCl + NaHCO₃ → NaCl + H₂O + CO₂↑", "tipo": "Acido + carbonato",
     "allontana": "Si libera anidride carbonica (CO₂ gassosa): si vedono le bollicine (effervescenza).",
     "spiegazione": "Si forma acido carbonico H₂CO₃, instabile, che si decompone subito in acqua e CO₂."},
    {"reagenti": ["HCl (acido cloridrico)", "CaCO₃ (carbonato di calcio)"], "prodotti": ["CaCl₂", "H₂O", "CO₂ ↑"],
     "equazione": "2 HCl + CaCO₃ → CaCl₂ + H₂O + CO₂↑", "tipo": "Acido + carbonato",
     "allontana": "CO₂ gassosa (effervescenza): il calcare «frigge» e si scioglie.",
     "spiegazione": "È il test del calcare (e il motivo per cui gli acidi rovinano il marmo)."},
    {"reagenti": ["HCl (acido cloridrico)", "Na₂CO₃ (carbonato di sodio)"], "prodotti": ["NaCl", "H₂O", "CO₂ ↑"],
     "equazione": "2 HCl + Na₂CO₃ → 2 NaCl + H₂O + CO₂↑", "tipo": "Acido + carbonato",
     "allontana": "CO₂ gassosa.", "spiegazione": "Il carbonato accetta 2 H⁺ e diventa acido carbonico, che si decompone."},
    {"reagenti": ["CH₃COOH (acido acetico)", "NaHCO₃ (bicarbonato di sodio)"], "prodotti": ["CH₃COONa", "H₂O", "CO₂ ↑"],
     "equazione": "CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂↑", "tipo": "Acido + carbonato",
     "allontana": "CO₂ gassosa: è il «vulcano» di aceto e bicarbonato.",
     "spiegazione": "Anche un acido debole come l'acido acetico sposta l'acido carbonico, che si decompone."},
    # --- Metalli ---------------------------------------------------------------------------------------
    {"reagenti": ["Zn (zinco)", "HCl (acido cloridrico)"], "prodotti": ["ZnCl₂ (cloruro di zinco)", "H₂ ↑"],
     "equazione": "Zn + 2 HCl → ZnCl₂ + H₂↑", "tipo": "Ossidoriduzione (metallo + acido)",
     "allontana": "Si libera idrogeno gassoso (H₂).",
     "spiegazione": "Lo zinco si ossida (Zn → Zn²⁺) e l'H⁺ si riduce a H₂: lo zinco è più riducente dell'idrogeno."},
    {"reagenti": ["Mg (magnesio)", "HCl (acido cloridrico)"], "prodotti": ["MgCl₂", "H₂ ↑"],
     "equazione": "Mg + 2 HCl → MgCl₂ + H₂↑", "tipo": "Ossidoriduzione (metallo + acido)",
     "allontana": "Idrogeno gassoso (H₂).", "spiegazione": "Mg → Mg²⁺ + 2e⁻; 2H⁺ + 2e⁻ → H₂."},
    {"reagenti": ["Fe (ferro)", "H₂SO₄ (acido solforico diluito)"], "prodotti": ["FeSO₄ (solfato ferroso)", "H₂ ↑"],
     "equazione": "Fe + H₂SO₄ → FeSO₄ + H₂↑", "tipo": "Ossidoriduzione (metallo + acido)",
     "allontana": "Idrogeno gassoso (H₂).", "spiegazione": "Con l'acido diluito il ferro diventa Fe²⁺."},
    {"reagenti": ["Na (sodio)", "H₂O (acqua)"], "prodotti": ["NaOH", "H₂ ↑"],
     "equazione": "2 Na + 2 H₂O → 2 NaOH + H₂↑", "tipo": "Ossidoriduzione (metallo alcalino + acqua)",
     "allontana": "Idrogeno gassoso, con molto calore (può prendere fuoco): reazione violenta.",
     "spiegazione": "I metalli alcalini cedono facilmente l'elettrone esterno; la soluzione diventa basica."},
    {"reagenti": ["Ca (calcio)", "H₂O (acqua)"], "prodotti": ["Ca(OH)₂", "H₂ ↑"],
     "equazione": "Ca + 2 H₂O → Ca(OH)₂ + H₂↑", "tipo": "Ossidoriduzione (metallo + acqua)",
     "allontana": "Idrogeno gassoso.", "spiegazione": "Meno violenta del sodio: il calcio è un alcalino-terroso."},
    {"reagenti": ["Cu (rame)", "HNO₃ (acido nitrico concentrato)"], "prodotti": ["Cu(NO₃)₂", "NO₂ ↑", "H₂O"],
     "equazione": "Cu + 4 HNO₃ → Cu(NO₃)₂ + 2 NO₂↑ + 2 H₂O", "tipo": "Ossidoriduzione",
     "allontana": "Biossido di azoto (NO₂), un gas rosso-bruno e tossico.",
     "spiegazione": "Il rame non reagisce con HCl, ma l'acido nitrico è un ossidante forte: è lui che si riduce "
                    "(N da +5 a +4), non l'H⁺."},
    {"reagenti": ["Zn (zinco)", "CuSO₄ (solfato di rame)"], "prodotti": ["ZnSO₄", "Cu ↓"],
     "equazione": "Zn + CuSO₄ → ZnSO₄ + Cu", "tipo": "Ossidoriduzione (spostamento)",
     "allontana": "Il rame si deposita come metallo rosso; la soluzione da azzurra diventa incolore.",
     "spiegazione": "Lo zinco è più riducente del rame (serie elettrochimica): cede elettroni a Cu²⁺. È il principio "
                    "della pila Daniell."},
    {"reagenti": ["Fe (ferro)", "CuSO₄ (solfato di rame)"], "prodotti": ["FeSO₄", "Cu ↓"],
     "equazione": "Fe + CuSO₄ → FeSO₄ + Cu", "tipo": "Ossidoriduzione (spostamento)",
     "allontana": "Il chiodo di ferro si ricopre di rame rosso.", "spiegazione": "Fe è più riducente di Cu."},
    {"reagenti": ["Cl₂ (cloro)", "NaBr (bromuro di sodio)"], "prodotti": ["NaCl", "Br₂"],
     "equazione": "Cl₂ + 2 NaBr → 2 NaCl + Br₂", "tipo": "Ossidoriduzione (alogeni)",
     "allontana": "Si forma bromo (la soluzione diventa arancione).",
     "spiegazione": "Il cloro è un ossidante più forte del bromo e lo sposta dai suoi sali."},
    # --- Precipitazioni ---------------------------------------------------------------------------------
    {"reagenti": ["AgNO₃ (nitrato d'argento)", "NaCl (cloruro di sodio)"], "prodotti": ["AgCl ↓", "NaNO₃"],
     "equazione": "AgNO₃ + NaCl → AgCl↓ + NaNO₃", "tipo": "Precipitazione (doppio scambio)",
     "allontana": "Precipita cloruro d'argento, un solido bianco che non si scioglie.",
     "spiegazione": "È il saggio dei cloruri: Ag⁺ + Cl⁻ → AgCl (molto poco solubile)."},
    {"reagenti": ["BaCl₂ (cloruro di bario)", "Na₂SO₄ (solfato di sodio)"], "prodotti": ["BaSO₄ ↓", "NaCl"],
     "equazione": "BaCl₂ + Na₂SO₄ → BaSO₄↓ + 2 NaCl", "tipo": "Precipitazione (doppio scambio)",
     "allontana": "Precipita solfato di bario, bianco.", "spiegazione": "È il saggio dei solfati."},
    {"reagenti": ["Pb(NO₃)₂ (nitrato di piombo)", "KI (ioduro di potassio)"], "prodotti": ["PbI₂ ↓", "KNO₃"],
     "equazione": "Pb(NO₃)₂ + 2 KI → PbI₂↓ + 2 KNO₃", "tipo": "Precipitazione (doppio scambio)",
     "allontana": "Precipita ioduro di piombo, giallo brillante («pioggia d'oro»).", "spiegazione": "Pb²⁺ + 2I⁻ → PbI₂."},
    {"reagenti": ["CuSO₄ (solfato di rame)", "NaOH (idrossido di sodio)"], "prodotti": ["Cu(OH)₂ ↓", "Na₂SO₄"],
     "equazione": "CuSO₄ + 2 NaOH → Cu(OH)₂↓ + Na₂SO₄", "tipo": "Precipitazione",
     "allontana": "Precipita idrossido di rame, azzurro e gelatinoso.", "spiegazione": "Cu²⁺ + 2OH⁻ → Cu(OH)₂."},
    {"reagenti": ["FeCl₃ (cloruro ferrico)", "NaOH (idrossido di sodio)"], "prodotti": ["Fe(OH)₃ ↓", "NaCl"],
     "equazione": "FeCl₃ + 3 NaOH → Fe(OH)₃↓ + 3 NaCl", "tipo": "Precipitazione",
     "allontana": "Precipita idrossido ferrico, rosso-bruno.", "spiegazione": "Fe³⁺ + 3OH⁻ → Fe(OH)₃."},
    {"reagenti": ["CaCl₂ (cloruro di calcio)", "Na₂CO₃ (carbonato di sodio)"], "prodotti": ["CaCO₃ ↓", "NaCl"],
     "equazione": "CaCl₂ + Na₂CO₃ → CaCO₃↓ + 2 NaCl", "tipo": "Precipitazione",
     "allontana": "Precipita carbonato di calcio (calcare), bianco.", "spiegazione": "È come si «addolcisce» l'acqua dura."},
    {"reagenti": ["Ca(OH)₂ (acqua di calce)", "CO₂ (anidride carbonica)"], "prodotti": ["CaCO₃ ↓", "H₂O"],
     "equazione": "Ca(OH)₂ + CO₂ → CaCO₃↓ + H₂O", "tipo": "Precipitazione (riconoscimento della CO₂)",
     "allontana": "L'acqua di calce diventa torbida: precipita carbonato di calcio.",
     "spiegazione": "È il test per riconoscere la CO₂ (per esempio nell'aria espirata)."},
    # --- Ossidi e acqua ----------------------------------------------------------------------------------
    {"reagenti": ["CaO (ossido di calcio, calce viva)", "H₂O (acqua)"], "prodotti": ["Ca(OH)₂ (calce spenta)"],
     "equazione": "CaO + H₂O → Ca(OH)₂", "tipo": "Ossido basico + acqua → idrossido",
     "allontana": "Niente, ma si libera molto calore.", "spiegazione": "Gli ossidi dei metalli con l'acqua danno idrossidi."},
    {"reagenti": ["Na₂O (ossido di sodio)", "H₂O (acqua)"], "prodotti": ["NaOH"],
     "equazione": "Na₂O + H₂O → 2 NaOH", "tipo": "Ossido basico + acqua → idrossido",
     "allontana": "Niente.", "spiegazione": "Ossido basico: la soluzione diventa basica."},
    {"reagenti": ["CO₂ (anidride carbonica)", "H₂O (acqua)"], "prodotti": ["H₂CO₃ (acido carbonico)"],
     "equazione": "CO₂ + H₂O ⇌ H₂CO₃", "tipo": "Ossido acido (anidride) + acqua → ossiacido",
     "allontana": "Niente: è un equilibrio, gran parte della CO₂ resta sciolta come tale.",
     "spiegazione": "Per questo l'acqua gassata e la pioggia sono leggermente acide. Nel sangue la reazione è "
                    "accelerata dall'anidrasi carbonica."},
    {"reagenti": ["SO₃ (anidride solforica)", "H₂O (acqua)"], "prodotti": ["H₂SO₄ (acido solforico)"],
     "equazione": "SO₃ + H₂O → H₂SO₄", "tipo": "Ossido acido (anidride) + acqua → ossiacido",
     "allontana": "Niente, molto calore.", "spiegazione": "Gli ossidi dei non metalli con l'acqua danno ossiacidi (piogge acide)."},
    {"reagenti": ["SO₂ (anidride solforosa)", "H₂O (acqua)"], "prodotti": ["H₂SO₃ (acido solforoso)"],
     "equazione": "SO₂ + H₂O ⇌ H₂SO₃", "tipo": "Ossido acido (anidride) + acqua → ossiacido",
     "allontana": "Niente.", "spiegazione": "Acido debole: equilibrio."},
    {"reagenti": ["NO₂ (biossido di azoto)", "H₂O (acqua)"], "prodotti": ["HNO₃", "NO ↑"],
     "equazione": "3 NO₂ + H₂O → 2 HNO₃ + NO↑", "tipo": "Disproporzione (ossidoriduzione)",
     "allontana": "Monossido di azoto (NO), gas.",
     "spiegazione": "L'azoto (+4) in parte si ossida a +5 (HNO₃) e in parte si riduce a +2 (NO). È l'ultima tappa del "
                    "processo Ostwald."},
    # --- Combustioni e sintesi --------------------------------------------------------------------------
    {"reagenti": ["CH₄ (metano)", "O₂ (ossigeno)"], "prodotti": ["CO₂ ↑", "H₂O"],
     "equazione": "CH₄ + 2 O₂ → CO₂ + 2 H₂O", "tipo": "Combustione",
     "allontana": "Anidride carbonica e vapore acqueo; si libera molto calore (ΔH ≈ −890 kJ/mol).",
     "spiegazione": "Combustione completa. Con poco ossigeno si forma anche monossido di carbonio (CO), tossico."},
    {"reagenti": ["C₃H₈ (propano)", "O₂ (ossigeno)"], "prodotti": ["CO₂ ↑", "H₂O"],
     "equazione": "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", "tipo": "Combustione",
     "allontana": "CO₂ e vapore acqueo, calore.", "spiegazione": "Si bilanciano prima C, poi H, poi O."},
    {"reagenti": ["C₂H₅OH (etanolo)", "O₂ (ossigeno)"], "prodotti": ["CO₂ ↑", "H₂O"],
     "equazione": "C₂H₅OH + 3 O₂ → 2 CO₂ + 3 H₂O", "tipo": "Combustione",
     "allontana": "CO₂ e vapore acqueo.", "spiegazione": "L'alcol brucia con fiamma azzurra quasi invisibile."},
    {"reagenti": ["H₂ (idrogeno)", "O₂ (ossigeno)"], "prodotti": ["H₂O"],
     "equazione": "2 H₂ + O₂ → 2 H₂O", "tipo": "Sintesi (combustione dell'idrogeno)",
     "allontana": "Solo vapore acqueo e molto calore (può essere esplosiva).",
     "spiegazione": "È la reazione delle celle a combustibile, che la usano per produrre elettricità."},
    {"reagenti": ["Mg (magnesio)", "O₂ (ossigeno)"], "prodotti": ["MgO (ossido di magnesio)"],
     "equazione": "2 Mg + O₂ → 2 MgO", "tipo": "Sintesi (ossidazione di un metallo)",
     "allontana": "Una luce bianca intensissima; resta una polvere bianca.", "spiegazione": "Mg → Mg²⁺: il metallo si ossida."},
    {"reagenti": ["Fe (ferro)", "O₂ (ossigeno)"], "prodotti": ["Fe₂O₃ (ossido ferrico, ruggine)"],
     "equazione": "4 Fe + 3 O₂ → 2 Fe₂O₃", "tipo": "Ossidazione (corrosione)",
     "allontana": "Niente: si forma lentamente la ruggine (con l'acqua è un ossido idrato).",
     "spiegazione": "La corrosione è un'ossidoriduzione lenta, favorita dall'acqua e dai sali."},
    {"reagenti": ["N₂ (azoto)", "H₂ (idrogeno)"], "prodotti": ["NH₃ (ammoniaca)"],
     "equazione": "N₂ + 3 H₂ ⇌ 2 NH₃ (ΔH = −92 kJ/mol)", "tipo": "Sintesi (equilibrio, processo Haber-Bosch)",
     "allontana": "Niente: l'ammoniaca si separa raffreddando e condensando.",
     "condizioni": "400-500 °C, 150-300 bar, catalizzatore di ferro",
     "spiegazione": "Esotermica e con diminuzione delle moli di gas (4 → 2): la pressione alta sposta l'equilibrio verso "
                    "NH₃ (Le Châtelier); la temperatura è un compromesso tra resa e velocità."},
    {"reagenti": ["SO₂ (anidride solforosa)", "O₂ (ossigeno)"], "prodotti": ["SO₃ (anidride solforica)"],
     "equazione": "2 SO₂ + O₂ ⇌ 2 SO₃ (ΔH ≈ −198 kJ)", "tipo": "Ossidazione catalitica (processo a contatto)",
     "allontana": "Niente.", "condizioni": "400-450 °C, catalizzatore V₂O₅",
     "spiegazione": "Tappa chiave della produzione di acido solforico."},
    {"reagenti": ["NH₃ (ammoniaca)", "O₂ (ossigeno)"], "prodotti": ["NO", "H₂O"],
     "equazione": "4 NH₃ + 5 O₂ → 4 NO + 6 H₂O", "tipo": "Ossidazione catalitica (processo Ostwald)",
     "allontana": "Vapore acqueo.", "condizioni": "≈ 850-900 °C, retina di platino-rodio",
     "spiegazione": "Prima tappa della produzione di acido nitrico."},
    {"reagenti": ["CH₄ (metano)", "H₂O (vapore)"], "prodotti": ["CO", "H₂"],
     "equazione": "CH₄ + H₂O ⇌ CO + 3 H₂ (ΔH ≈ +206 kJ/mol)", "tipo": "Steam reforming (produzione di idrogeno)",
     "allontana": "Niente: il gas di sintesi (CO + H₂) va alle tappe successive.",
     "condizioni": "800-900 °C, 20-30 bar, catalizzatore di nichel", "spiegazione": "Endotermica: serve calore."},
    {"reagenti": ["CO (monossido di carbonio)", "H₂O (vapore)"], "prodotti": ["CO₂", "H₂"],
     "equazione": "CO + H₂O ⇌ CO₂ + H₂ (ΔH ≈ −41 kJ/mol)", "tipo": "Water-gas shift",
     "allontana": "La CO₂ viene poi tolta (assorbimento) per avere idrogeno puro.",
     "spiegazione": "Aumenta l'idrogeno e toglie il CO."},
    {"reagenti": ["NaCl (salamoia)", "H₂O (elettrolisi)"], "prodotti": ["NaOH", "H₂ ↑", "Cl₂ ↑"],
     "equazione": "2 NaCl + 2 H₂O → 2 NaOH + H₂↑ + Cl₂↑", "tipo": "Elettrolisi (processo cloro-soda)",
     "allontana": "Cloro gassoso all'anodo e idrogeno gassoso al catodo.",
     "spiegazione": "Anodo: 2Cl⁻ → Cl₂ + 2e⁻ (ossidazione). Catodo: 2H₂O + 2e⁻ → H₂ + 2OH⁻ (riduzione)."},
    {"reagenti": ["H₂O (elettrolisi)"], "prodotti": ["H₂ ↑", "O₂ ↑"],
     "equazione": "2 H₂O → 2 H₂↑ + O₂↑", "tipo": "Elettrolisi dell'acqua",
     "allontana": "Idrogeno al catodo e ossigeno all'anodo (in volume 2 : 1).",
     "spiegazione": "Serve energia elettrica: è il contrario della combustione dell'idrogeno."},
    {"reagenti": ["CaCO₃ (carbonato di calcio, riscaldato)"], "prodotti": ["CaO", "CO₂ ↑"],
     "equazione": "CaCO₃ → CaO + CO₂↑", "tipo": "Decomposizione termica (calcinazione)",
     "allontana": "Anidride carbonica.", "condizioni": "≈ 900 °C", "spiegazione": "È come si produce la calce viva."},
    {"reagenti": ["H₂O₂ (acqua ossigenata)"], "prodotti": ["H₂O", "O₂ ↑"],
     "equazione": "2 H₂O₂ → 2 H₂O + O₂↑", "tipo": "Decomposizione (disproporzione)",
     "allontana": "Ossigeno gassoso: la schiuma bianca sulla ferita.",
     "condizioni": "catalizzata dalla catalasi (nel sangue) o dal biossido di manganese",
     "spiegazione": "L'ossigeno (−1) in parte si ossida a 0 (O₂) e in parte si riduce a −2 (H₂O)."},
    # --- Chimica organica e biomolecole -----------------------------------------------------------------
    {"reagenti": ["CH₃COOH (acido acetico)", "C₂H₅OH (etanolo)"], "prodotti": ["CH₃COOC₂H₅ (acetato di etile)", "H₂O"],
     "equazione": "CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O", "tipo": "Esterificazione (condensazione)",
     "allontana": "Una molecola d'acqua.", "condizioni": "acido solforico come catalizzatore, calore",
     "spiegazione": "L'OH dell'acido e l'H dell'alcol escono come acqua; resta il legame estere. È un equilibrio: "
                    "togliendo l'acqua si aumenta la resa."},
    {"reagenti": ["C₂H₄ (etilene)", "H₂ (idrogeno)"], "prodotti": ["C₂H₆ (etano)"],
     "equazione": "C₂H₄ + H₂ → C₂H₆", "tipo": "Addizione (idrogenazione)",
     "allontana": "Niente.", "condizioni": "catalizzatore di nichel, platino o palladio",
     "spiegazione": "Il doppio legame si apre e ogni carbonio prende un idrogeno (così si induriscono gli oli)."},
    {"reagenti": ["C₂H₄ (etilene)", "Br₂ (bromo)"], "prodotti": ["C₂H₄Br₂ (1,2-dibromoetano)"],
     "equazione": "C₂H₄ + Br₂ → CH₂Br-CH₂Br", "tipo": "Addizione elettrofila",
     "allontana": "Niente, ma l'acqua di bromo da arancione diventa incolore.",
     "spiegazione": "È il saggio dei doppi legami: gli alcheni decolorano il bromo, gli alcani no."},
    {"reagenti": ["C₂H₄ (etilene)", "H₂O (acqua)"], "prodotti": ["C₂H₅OH (etanolo)"],
     "equazione": "C₂H₄ + H₂O → C₂H₅OH", "tipo": "Addizione (idratazione)",
     "allontana": "Niente.", "condizioni": "acido fosforico come catalizzatore, ≈ 300 °C, 60-70 bar",
     "spiegazione": "È così che si produce l'etanolo industriale (non alimentare)."},
    {"reagenti": ["C₂H₅OH (etanolo, con H₂SO₄ a caldo)"], "prodotti": ["C₂H₄ (etilene)", "H₂O"],
     "equazione": "C₂H₅OH → C₂H₄ + H₂O", "tipo": "Eliminazione (disidratazione)",
     "allontana": "Una molecola d'acqua.", "condizioni": "acido solforico concentrato, ≈ 170 °C",
     "spiegazione": "Il contrario dell'idratazione: si forma il doppio legame."},
    {"reagenti": ["C₆H₁₂O₆ (glucosio, con lievito)"], "prodotti": ["C₂H₅OH (etanolo)", "CO₂ ↑"],
     "equazione": "C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂↑", "tipo": "Fermentazione alcolica",
     "allontana": "Anidride carbonica (le bollicine del vino e della birra, il pane che lievita).",
     "condizioni": "lieviti (Saccharomyces cerevisiae), senza ossigeno, ≈ 30 °C",
     "spiegazione": "Dopo la glicolisi, il piruvato perde CO₂ e diventa acetaldeide, ridotta a etanolo dal NADH."},
    {"reagenti": ["C₆H₁₂O₆ (glucosio)", "O₂ (ossigeno)"], "prodotti": ["CO₂ ↑", "H₂O"],
     "equazione": "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O (ΔG ≈ −2870 kJ/mol)", "tipo": "Respirazione cellulare",
     "allontana": "CO₂, che si elimina con il respiro, e acqua; l'energia va nell'ATP (circa 30-32 per glucosio).",
     "spiegazione": "Glicolisi, ciclo di Krebs e fosforilazione ossidativa: i percorsi passo per passo sono nelle mappe."},
    {"reagenti": ["CO₂ (anidride carbonica)", "H₂O (acqua, con la luce)"], "prodotti": ["C₆H₁₂O₆ (glucosio)", "O₂ ↑"],
     "equazione": "6 CO₂ + 6 H₂O → C₆H₁₂O₆ + 6 O₂", "tipo": "Fotosintesi",
     "allontana": "Ossigeno, che esce dalle foglie.", "condizioni": "luce, clorofilla (cloroplasti)",
     "spiegazione": "Il contrario della respirazione: l'ossigeno liberato viene dall'acqua."},
    {"reagenti": ["Glucosio", "Glucosio"], "prodotti": ["Maltosio (C₁₂H₂₂O₁₁)", "H₂O"],
     "equazione": "C₆H₁₂O₆ + C₆H₁₂O₆ → C₁₂H₂₂O₁₁ + H₂O", "tipo": "Condensazione (legame glicosidico α-1,4)",
     "allontana": "Una molecola d'acqua.", "spiegazione": "Due monosaccaridi formano un disaccaride perdendo acqua."},
    {"reagenti": ["Glucosio", "Fruttosio"], "prodotti": ["Saccarosio (C₁₂H₂₂O₁₁)", "H₂O"],
     "equazione": "C₆H₁₂O₆ + C₆H₁₂O₆ → C₁₂H₂₂O₁₁ + H₂O", "tipo": "Condensazione (legame glicosidico α-1,β-2)",
     "allontana": "Una molecola d'acqua.", "spiegazione": "Il saccarosio è lo zucchero da tavola."},
    {"reagenti": ["Glucosio", "Galattosio"], "prodotti": ["Lattosio (C₁₂H₂₂O₁₁)", "H₂O"],
     "equazione": "C₆H₁₂O₆ + C₆H₁₂O₆ → C₁₂H₂₂O₁₁ + H₂O", "tipo": "Condensazione (legame glicosidico β-1,4)",
     "allontana": "Una molecola d'acqua.", "spiegazione": "Il lattosio è lo zucchero del latte; la lattasi lo idrolizza."},
    {"reagenti": ["Saccarosio", "H₂O (acqua)"], "prodotti": ["Glucosio", "Fruttosio"],
     "equazione": "C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆", "tipo": "Idrolisi",
     "allontana": "Niente: entra una molecola d'acqua.", "condizioni": "enzima saccarasi (invertasi) o acido",
     "spiegazione": "L'idrolisi è il contrario della condensazione: l'acqua rompe il legame."},
    {"reagenti": ["Amminoacido", "Amminoacido"], "prodotti": ["Dipeptide", "H₂O"],
     "equazione": "H₂N-CHR-COOH + H₂N-CHR'-COOH → H₂N-CHR-CO-NH-CHR'-COOH + H₂O", "tipo": "Condensazione (legame peptidico)",
     "allontana": "Una molecola d'acqua.",
     "spiegazione": "Il gruppo carbossilico di un amminoacido si lega al gruppo amminico dell'altro: nasce il legame "
                    "peptidico (nei ribosomi)."},
    {"reagenti": ["Glicerolo", "Acidi grassi (3)"], "prodotti": ["Trigliceride", "H₂O"],
     "equazione": "glicerolo + 3 acidi grassi → trigliceride + 3 H₂O", "tipo": "Esterificazione (condensazione)",
     "allontana": "Tre molecole d'acqua.", "spiegazione": "Ogni OH del glicerolo forma un estere con un acido grasso."},
    {"reagenti": ["Trigliceride", "NaOH (idrossido di sodio)"], "prodotti": ["Glicerolo", "Saponi (sali sodici degli acidi grassi)"],
     "equazione": "trigliceride + 3 NaOH → glicerolo + 3 R-COO⁻Na⁺", "tipo": "Saponificazione (idrolisi basica)",
     "allontana": "Niente: si separano il sapone e il glicerolo.", "spiegazione": "È così che si fa il sapone."},
    {"reagenti": ["ATP", "H₂O (acqua)"], "prodotti": ["ADP", "Pi (fosfato)"],
     "equazione": "ATP + H₂O → ADP + Pi (ΔG°' ≈ −30,5 kJ/mol)", "tipo": "Idrolisi (energia della cellula)",
     "allontana": "Si libera un fosfato inorganico e l'energia che la cellula usa.",
     "spiegazione": "È la «moneta» dell'energia: muscoli, pompe, sintesi."},
]


def tutti_i_reagenti():
    return sorted({r for x in REAZIONI for r in x["reagenti"]}, key=str.lower)


def cerca(a, b=None):
    """Le reazioni che hanno A (e B) tra i reagenti."""
    trovate = []
    for x in REAZIONI:
        if a in x["reagenti"] and (not b or b == "—" or (b in x["reagenti"] and (a != b or x["reagenti"].count(a) == 2))):
            trovate.append(x)
    return trovate


# Le reazioni utili per ogni argomento di chimica del programma.
TIPI_ARGOMENTO = {
    "Acidi, basi, pH e tamponi": ["Acido-base", "Acido + carbonato"],
    "Ossidoriduzioni ed elettrochimica": ["Ossidoriduzione", "Elettrolisi", "Disproporzione"],
    "Nomenclatura e reazioni inorganiche": ["Precipitazione", "Ossido", "Acido + carbonato", "Acido-base"],
    "Stechiometria, moli e reazioni": ["Combustione", "Sintesi", "Decomposizione"],
    "Termodinamica, cinetica ed equilibrio": ["Sintesi (equilibrio", "Steam reforming", "Water-gas", "Ossidazione catalitica"],
    "Chimica organica e biomolecole": ["Esterificazione", "Addizione", "Eliminazione", "Condensazione", "Idrolisi",
                                       "Saponificazione", "Fermentazione"],
    "Metabolismo ed energia": ["Respirazione", "Fotosintesi", "Fermentazione", "Idrolisi (energia"],
    "Carboidrati": ["Condensazione (legame glicosidico", "Idrolisi", "Fermentazione"],
    "Chimica generale": ["Acido-base", "Ossidoriduzione", "Precipitazione", "Combustione", "Sintesi"],
    "Chimica organica": ["Esterificazione", "Addizione", "Eliminazione", "Saponificazione"],
}


def reazioni_argomento(argomento):
    tipi = TIPI_ARGOMENTO.get(argomento, [])
    return [x for x in REAZIONI if any(x["tipo"].startswith(t) for t in tipi)]


# --- Impianti chimici -------------------------------------------------------------------------------
# unita: (nome, tipo) — il tipo decide la forma nel disegno; correnti: (da, a, cosa passa)
TIPI_UNITA = {"Alimentazione": "invhouse", "Serbatoio": "cylinder", "Pompa": "ellipse", "Compressore": "trapezium",
              "Scambiatore di calore": "hexagon", "Forno": "house", "Reattore": "box3d", "Colonna di distillazione": "cds",
              "Assorbitore": "cds", "Separatore": "diamond", "Condensatore": "hexagon", "Filtro": "invtrapezium",
              "Fermentatore": "box3d", "Cella elettrolitica": "box3d", "Vasca": "box", "Prodotto": "doubleoctagon",
              "Spurgo": "octagon", "Miscelatore": "triangle", "Valvola": "point"}

IMPIANTI = {
    "Sintesi dell'ammoniaca (Haber-Bosch)": {
        "reazione": "N₂ + 3 H₂ ⇌ 2 NH₃ (ΔH = −92 kJ/mol)",
        "condizioni": "400-500 °C, 150-300 bar, catalizzatore di ferro con promotori (K₂O, Al₂O₃)",
        "descrizione": [
            "Le materie prime sono l'azoto dell'aria e l'idrogeno, ottenuto quasi sempre dal metano con lo steam "
            "reforming; vengono mescolati nel rapporto 1 : 3.",
            "Il gas viene compresso a 150-300 bar e preriscaldato scambiando calore con il gas caldo che esce dal "
            "reattore (recupero di calore).",
            "Nel reattore catalitico, a più letti di catalizzatore di ferro raffreddati tra un letto e l'altro, solo il "
            "15-25% del gas si trasforma in ammoniaca a ogni passaggio.",
            "Il gas che esce viene raffreddato: l'ammoniaca condensa ed è separata come liquido.",
            "Il gas che non ha reagito torna al reattore (riciclo) con un compressore; una piccola parte viene spurgata "
            "per non accumulare gli inerti (argon e metano).",
        ],
        "perche": "La reazione è esotermica e riduce le moli di gas: la pressione alta sposta l'equilibrio verso NH₃; la "
                  "temperatura è un compromesso, perché a bassa temperatura la resa sarebbe più alta ma la reazione "
                  "troppo lenta. Il riciclo porta la conversione complessiva oltre il 95%.",
        "unita": [("N₂ + H₂ (1 : 3)", "Alimentazione"), ("Compressore", "Compressore"),
                  ("Scambiatore (preriscaldo)", "Scambiatore di calore"), ("Reattore catalitico (Fe)", "Reattore"),
                  ("Condensatore", "Condensatore"), ("Separatore gas-liquido", "Separatore"),
                  ("Ammoniaca liquida", "Prodotto"), ("Compressore di riciclo", "Compressore"), ("Spurgo inerti", "Spurgo")],
        "correnti": [("N₂ + H₂ (1 : 3)", "Compressore", "gas fresco"), ("Compressore", "Scambiatore (preriscaldo)", "150-300 bar"),
                     ("Scambiatore (preriscaldo)", "Reattore catalitico (Fe)", "≈ 400 °C"),
                     ("Reattore catalitico (Fe)", "Condensatore", "NH₃ 15-25% + gas"),
                     ("Condensatore", "Separatore gas-liquido", "raffreddato"),
                     ("Separatore gas-liquido", "Ammoniaca liquida", "NH₃ liquida"),
                     ("Separatore gas-liquido", "Compressore di riciclo", "N₂ + H₂ non reagiti"),
                     ("Compressore di riciclo", "Scambiatore (preriscaldo)", "riciclo"),
                     ("Separatore gas-liquido", "Spurgo inerti", "Ar, CH₄")],
        "parole": ["azoto", "idrogeno", "compress", "pressione", "catalizzatore", "ferro", "reattore", "riciclo",
                   "condens", "spurgo", "esotermic", "equilibrio", "temperatura"],
    },
    "Acido solforico (processo a contatto)": {
        "reazione": "S + O₂ → SO₂;  2 SO₂ + O₂ ⇌ 2 SO₃;  SO₃ + H₂O → H₂SO₄ (tramite oleum)",
        "condizioni": "convertitore a 400-450 °C con catalizzatore V₂O₅, 4 letti con raffreddamento intermedio",
        "descrizione": [
            "Lo zolfo fuso brucia in un forno con aria secca e dà anidride solforosa (SO₂).",
            "Il gas, raffreddato in una caldaia a recupero (che produce vapore), entra nel convertitore: su letti di "
            "pentossido di vanadio (V₂O₅) la SO₂ si ossida a SO₃.",
            "La reazione è esotermica: tra un letto e l'altro il gas viene raffreddato per tenere alta la resa.",
            "La SO₃ non si assorbe in acqua (formerebbe una nebbia acida): si assorbe in acido solforico al 98% in una "
            "torre di assorbimento, ottenendo oleum, poi diluito con acqua.",
            "Con il doppio assorbimento (una torre a metà conversione e una alla fine) si supera il 99,7% di conversione e "
            "si riducono le emissioni di SO₂.",
        ],
        "perche": "Le Châtelier: la reazione è esotermica, quindi si raffredda tra i letti; il catalizzatore rende "
                  "abbastanza veloce la reazione a temperature in cui la resa resta alta.",
        "unita": [("Zolfo + aria secca", "Alimentazione"), ("Forno a zolfo", "Forno"), ("Caldaia a recupero", "Scambiatore di calore"),
                  ("Convertitore (V₂O₅, 4 letti)", "Reattore"), ("Torre di assorbimento", "Assorbitore"),
                  ("Diluizione", "Miscelatore"), ("H₂SO₄ 98%", "Prodotto"), ("Camino (gas depurati)", "Spurgo")],
        "correnti": [("Zolfo + aria secca", "Forno a zolfo", ""), ("Forno a zolfo", "Caldaia a recupero", "SO₂ caldo"),
                     ("Caldaia a recupero", "Convertitore (V₂O₅, 4 letti)", "≈ 420 °C"),
                     ("Convertitore (V₂O₅, 4 letti)", "Torre di assorbimento", "SO₃"),
                     ("Torre di assorbimento", "Diluizione", "oleum"), ("Diluizione", "H₂SO₄ 98%", ""),
                     ("Torre di assorbimento", "Camino (gas depurati)", "gas residui")],
        "parole": ["zolfo", "forno", "so2", "so₂", "convertitore", "vanadio", "v2o5", "v₂o₅", "assorbimento", "oleum",
                   "raffredd", "esotermic", "doppio"],
    },
    "Acido nitrico (processo Ostwald)": {
        "reazione": "4 NH₃ + 5 O₂ → 4 NO + 6 H₂O;  2 NO + O₂ → 2 NO₂;  3 NO₂ + H₂O → 2 HNO₃ + NO",
        "condizioni": "ossidazione dell'ammoniaca su retine di platino-rodio a ≈ 850-900 °C, tempi di contatto brevissimi",
        "descrizione": [
            "Ammoniaca e aria in eccesso passano su retine di platino-rodio: l'ammoniaca si ossida a monossido di azoto "
            "(NO) con resa superiore al 95%.",
            "Il gas viene raffreddato (recuperando calore): l'NO reagisce con altro ossigeno e diventa NO₂.",
            "Nella torre di assorbimento l'NO₂ incontra acqua in controcorrente e forma acido nitrico; l'NO che si "
            "riforma viene riossidato e riassorbito.",
            "Si ottiene acido nitrico al 60-68%; i gas di coda vengono depurati dagli ossidi di azoto.",
        ],
        "perche": "Il catalizzatore e il tempo di contatto brevissimo favoriscono NO invece di N₂; l'assorbimento "
                  "in controcorrente massimizza la resa.",
        "unita": [("NH₃ + aria", "Alimentazione"), ("Reattore a retine Pt-Rh", "Reattore"),
                  ("Raffreddamento (NO → NO₂)", "Scambiatore di calore"), ("Torre di assorbimento", "Assorbitore"),
                  ("HNO₃ 60-68%", "Prodotto"), ("Depurazione gas di coda", "Spurgo")],
        "correnti": [("NH₃ + aria", "Reattore a retine Pt-Rh", ""), ("Reattore a retine Pt-Rh", "Raffreddamento (NO → NO₂)", "NO"),
                     ("Raffreddamento (NO → NO₂)", "Torre di assorbimento", "NO₂"),
                     ("Torre di assorbimento", "HNO₃ 60-68%", ""), ("Torre di assorbimento", "Depurazione gas di coda", "NOx")],
        "parole": ["ammoniaca", "platino", "rodio", "ossid", "no2", "no₂", "assorbimento", "acqua", "controcorrente",
                   "raffredd"],
    },
    "Idrogeno dal metano (steam reforming)": {
        "reazione": "CH₄ + H₂O ⇌ CO + 3 H₂ (endotermica);  CO + H₂O ⇌ CO₂ + H₂ (shift)",
        "condizioni": "reformer a 800-900 °C e 20-30 bar con catalizzatore di nichel; shift ad alta e bassa temperatura",
        "descrizione": [
            "Il metano viene desolforato (lo zolfo avvelena il catalizzatore) e mescolato con vapore.",
            "Nel reformer, tubi pieni di catalizzatore di nichel scaldati da bruciatori, si forma il gas di sintesi "
            "(CO + H₂): la reazione è fortemente endotermica.",
            "Nei reattori di shift il CO reagisce con altro vapore e diventa CO₂, producendo altro idrogeno.",
            "La CO₂ viene tolta per assorbimento (con ammine) o con il PSA (adsorbimento a pressione alternata), che dà "
            "idrogeno purissimo.",
        ],
        "perche": "Alta temperatura per una reazione endotermica; lo shift sposta il CO verso altro H₂; la separazione "
                  "finale toglie la CO₂ (che è anche il problema ambientale di questo processo).",
        "unita": [("Metano", "Alimentazione"), ("Desolforazione", "Filtro"), ("Miscelatore con vapore", "Miscelatore"),
                  ("Reformer (Ni, 850 °C)", "Forno"), ("Reattori di shift", "Reattore"), ("Rimozione CO₂ (ammine/PSA)", "Assorbitore"),
                  ("Idrogeno", "Prodotto"), ("CO₂", "Spurgo")],
        "correnti": [("Metano", "Desolforazione", ""), ("Desolforazione", "Miscelatore con vapore", ""),
                     ("Miscelatore con vapore", "Reformer (Ni, 850 °C)", "CH₄ + H₂O"),
                     ("Reformer (Ni, 850 °C)", "Reattori di shift", "CO + H₂"),
                     ("Reattori di shift", "Rimozione CO₂ (ammine/PSA)", "CO₂ + H₂"),
                     ("Rimozione CO₂ (ammine/PSA)", "Idrogeno", "H₂"), ("Rimozione CO₂ (ammine/PSA)", "CO₂", "")],
        "parole": ["metano", "vapore", "nichel", "reformer", "endotermic", "shift", "co2", "co₂", "psa", "ammine",
                   "desolfor"],
    },
    "Distillazione del petrolio (topping)": {
        "reazione": "Nessuna reazione: è una separazione fisica in base alla temperatura di ebollizione",
        "condizioni": "forno a ≈ 350-400 °C, colonna a pressione atmosferica con piatti; residuo in colonna sotto vuoto",
        "descrizione": [
            "Il greggio viene dissalato e scaldato in un forno fino a vaporizzarne gran parte.",
            "Entra nella colonna di distillazione: i vapori salgono attraverso i piatti e si raffreddano; ogni frazione "
            "condensa all'altezza in cui la temperatura è uguale alla sua temperatura di ebollizione.",
            "Dall'alto al basso escono: gas (GPL), benzina, cherosene, gasolio; dal fondo il residuo.",
            "Il residuo viene distillato in una seconda colonna sotto vuoto (a pressione bassa le sostanze bollono a "
            "temperatura più bassa e non si decompongono): lubrificanti e bitume.",
        ],
        "perche": "Le frazioni hanno temperature di ebollizione diverse; il riflusso in testa e i piatti rendono la "
                  "separazione più netta.",
        "unita": [("Greggio", "Alimentazione"), ("Forno", "Forno"), ("Colonna atmosferica", "Colonna di distillazione"),
                  ("GPL", "Prodotto"), ("Benzina", "Prodotto"), ("Cherosene", "Prodotto"), ("Gasolio", "Prodotto"),
                  ("Colonna sotto vuoto", "Colonna di distillazione"), ("Lubrificanti e bitume", "Prodotto")],
        "correnti": [("Greggio", "Forno", ""), ("Forno", "Colonna atmosferica", "≈ 370 °C"), ("Colonna atmosferica", "GPL", "testa"),
                     ("Colonna atmosferica", "Benzina", ""), ("Colonna atmosferica", "Cherosene", ""),
                     ("Colonna atmosferica", "Gasolio", ""), ("Colonna atmosferica", "Colonna sotto vuoto", "residuo"),
                     ("Colonna sotto vuoto", "Lubrificanti e bitume", "")],
        "parole": ["forno", "colonna", "piatti", "ebollizione", "frazion", "benzina", "gasolio", "residuo", "vuoto",
                   "riflusso", "condens"],
    },
    "Cloro e soda (elettrolisi a membrana)": {
        "reazione": "2 NaCl + 2 H₂O → 2 NaOH + H₂ + Cl₂",
        "condizioni": "celle elettrolitiche con membrana a scambio cationico, salamoia satura purificata",
        "descrizione": [
            "Il sale viene sciolto in acqua (salamoia) e purificato da calcio e magnesio, che rovinerebbero la membrana.",
            "Nella cella, all'anodo il cloruro si ossida a cloro gassoso; al catodo l'acqua si riduce a idrogeno e ioni OH⁻.",
            "La membrana lascia passare solo gli ioni Na⁺ dall'anodo al catodo: lì si forma soda caustica (NaOH) al "
            "30-35% senza contaminazione di cloruro.",
            "Cloro e idrogeno vengono raffreddati, essiccati e compressi; la salamoia impoverita torna a sciogliere sale.",
        ],
        "perche": "La membrana separa i prodotti (il cloro non deve incontrare la soda né l'idrogeno) ed evita il mercurio "
                  "dei vecchi impianti.",
        "unita": [("Sale + acqua", "Alimentazione"), ("Purificazione salamoia", "Filtro"), ("Cella a membrana", "Cella elettrolitica"),
                  ("Cloro (anodo)", "Prodotto"), ("Idrogeno (catodo)", "Prodotto"), ("Soda caustica 30-35%", "Prodotto")],
        "correnti": [("Sale + acqua", "Purificazione salamoia", "salamoia"), ("Purificazione salamoia", "Cella a membrana", ""),
                     ("Cella a membrana", "Cloro (anodo)", "Cl₂"), ("Cella a membrana", "Idrogeno (catodo)", "H₂"),
                     ("Cella a membrana", "Soda caustica 30-35%", "NaOH"),
                     ("Cella a membrana", "Purificazione salamoia", "salamoia impoverita")],
        "parole": ["salamoia", "anodo", "catodo", "membrana", "cloro", "idrogeno", "soda", "naoh", "ossid", "riduz",
                   "elettrolisi"],
    },
    "Bioetanolo (fermentazione)": {
        "reazione": "C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂",
        "condizioni": "lieviti Saccharomyces cerevisiae, 30-35 °C, senza ossigeno; distillazione fino all'azeotropo (≈ 95,6%)",
        "descrizione": [
            "La materia prima (canna da zucchero, mais, scarti) viene macinata; se contiene amido, enzimi (amilasi) lo "
            "trasformano in glucosio.",
            "Nel fermentatore i lieviti trasformano il glucosio in etanolo e anidride carbonica.",
            "Il «vino» ottenuto (8-12% di etanolo) viene distillato: non si supera il 95,6% perché si forma un azeotropo "
            "con l'acqua.",
            "Con i setacci molecolari si toglie l'ultima acqua e si ottiene etanolo anidro (per carburanti).",
        ],
        "perche": "Senza ossigeno i lieviti fermentano invece di respirare; la distillazione separa l'etanolo che bolle "
                  "a 78 °C, ma l'azeotropo obbliga a una disidratazione finale.",
        "unita": [("Biomassa", "Alimentazione"), ("Idrolisi enzimatica", "Reattore"), ("Fermentatore (lieviti)", "Fermentatore"),
                  ("Colonna di distillazione", "Colonna di distillazione"), ("Setacci molecolari", "Filtro"),
                  ("Etanolo anidro", "Prodotto"), ("CO₂", "Spurgo")],
        "correnti": [("Biomassa", "Idrolisi enzimatica", ""), ("Idrolisi enzimatica", "Fermentatore (lieviti)", "glucosio"),
                     ("Fermentatore (lieviti)", "Colonna di distillazione", "etanolo 8-12%"), ("Fermentatore (lieviti)", "CO₂", ""),
                     ("Colonna di distillazione", "Setacci molecolari", "95,6%"), ("Setacci molecolari", "Etanolo anidro", "")],
        "parole": ["lievit", "fermenta", "glucosio", "amido", "enzim", "distill", "azeotrop", "anidro", "co2", "co₂"],
    },
    "Depurazione delle acque reflue": {
        "reazione": "Ossidazione biologica della sostanza organica da parte dei batteri (fanghi attivi)",
        "condizioni": "vasca di ossidazione aerata; sedimentatori; digestione anaerobica dei fanghi (biogas)",
        "descrizione": [
            "Pretrattamenti: grigliatura (oggetti grossi), dissabbiatura e disoleatura.",
            "Sedimentazione primaria: le particelle sospese si depositano sul fondo.",
            "Trattamento biologico: nella vasca a fanghi attivi i batteri, con l'aria insufflata, consumano la sostanza "
            "organica (e con la nitrificazione-denitrificazione tolgono l'azoto).",
            "Sedimentazione secondaria: i fanghi si separano dall'acqua; una parte torna in vasca (ricircolo).",
            "Disinfezione (raggi UV, cloro o acido peracetico) e scarico; i fanghi vengono ispessiti e digeriti senza "
            "ossigeno, producendo biogas.",
        ],
        "perche": "Si separa prima ciò che è fisico (grigliatura, sedimentazione), poi i batteri tolgono ciò che è "
                  "disciolto; il ricircolo mantiene alta la quantità di batteri.",
        "unita": [("Acque reflue", "Alimentazione"), ("Grigliatura e dissabbiatura", "Filtro"), ("Sedimentatore primario", "Vasca"),
                  ("Vasca a fanghi attivi (aria)", "Reattore"), ("Sedimentatore secondario", "Vasca"),
                  ("Disinfezione", "Vasca"), ("Acqua depurata", "Prodotto"), ("Digestore fanghi (biogas)", "Reattore")],
        "correnti": [("Acque reflue", "Grigliatura e dissabbiatura", ""), ("Grigliatura e dissabbiatura", "Sedimentatore primario", ""),
                     ("Sedimentatore primario", "Vasca a fanghi attivi (aria)", ""),
                     ("Vasca a fanghi attivi (aria)", "Sedimentatore secondario", ""),
                     ("Sedimentatore secondario", "Vasca a fanghi attivi (aria)", "ricircolo fanghi"),
                     ("Sedimentatore secondario", "Disinfezione", ""), ("Disinfezione", "Acqua depurata", ""),
                     ("Sedimentatore primario", "Digestore fanghi (biogas)", "fanghi"),
                     ("Sedimentatore secondario", "Digestore fanghi (biogas)", "fanghi in eccesso")],
        "parole": ["grigli", "sediment", "fanghi", "batteri", "aria", "ossid", "ricircolo", "disinfez", "biogas",
                   "digest", "azoto"],
    },
}


# Parole che fanno riconoscere un impianto in una richiesta («come si fa l'ammoniaca»).
PAROLE_IMPIANTO = {
    "Sintesi dell'ammoniaca (Haber-Bosch)": ["ammoniaca", "haber"],
    "Acido solforico (processo a contatto)": ["acido solforico", "processo a contatto"],
    "Acido nitrico (processo Ostwald)": ["acido nitrico", "ostwald"],
    "Idrogeno dal metano (steam reforming)": ["steam reforming", "idrogeno dal metano", "produrre idrogeno",
                                              "produzione di idrogeno", "gas di sintesi"],
    "Distillazione del petrolio (topping)": ["petrolio", "raffineria", "topping"],
    "Cloro e soda (elettrolisi a membrana)": ["cloro-soda", "cloro soda", "soda caustica", "elettrolisi del sale",
                                              "elettrolisi della salamoia"],
    "Bioetanolo (fermentazione)": ["bioetanolo", "etanolo dalla fermentazione", "produzione di etanolo"],
    "Depurazione delle acque reflue": ["depurazione", "depuratore", "acque reflue", "fanghi attivi"],
}

# Nomi comuni → nomi chimici (per capire «aceto e bicarbonato», «brucio il metano»…).
NOMI_COMUNI = {"aceto": "acido acetico", "bicarbonato": "bicarbonato di sodio NaHCO₃", "calcare": "carbonato di calcio",
               "marmo": "carbonato di calcio", "sale da cucina": "cloruro di sodio", "soda caustica": "idrossido di sodio",
               "candeggina": "ipoclorito", "ruggine": "ferro ossigeno ossido ferrico", "brucio": "combustione con ossigeno",
               "bruciare": "combustione con ossigeno", "bruciando": "combustione con ossigeno",
               "acqua ossigenata": "perossido di idrogeno H₂O₂", "calce": "ossido di calcio", "zucchero": "glucosio",
               "alcol": "etanolo", "sapone": "saponificazione trigliceride"}


# --- Impianti delle operazioni unitarie (distillazione, assorbimento, estrazione, evaporazione…) ---------
# Stanno in impianti_operazioni.py; qui si uniscono a quelli di processo, dopo di loro (così «petrolio»
# porta ancora al topping prima che «distillazione» porti alla distillazione binaria).
import impianti_operazioni as _operazioni  # noqa: E402

TIPI_UNITA.update(_operazioni.TIPI_UNITA_EXTRA)
IMPIANTI.update(_operazioni.IMPIANTI_OPERAZIONI)
PAROLE_IMPIANTO.update(_operazioni.PAROLE_IMPIANTO_OPERAZIONI)

# --- Altre 137 reazioni («cosa succede se sommo…?»): elementi tra loro, metalli, precipitazioni, combustioni,
# ossidoriduzioni, organica e biochimica. Stanno in reazioni_extra.py, bilanciate e controllate atomo per atomo.
import reazioni_extra as _extra  # noqa: E402

REAZIONI.extend(_extra.REAZIONI_EXTRA)
TIPI_ARGOMENTO["Chimica organica e biomolecole"] += ["Sostituzione"]
TIPI_ARGOMENTO["Chimica organica"] += ["Sostituzione"]
TIPI_ARGOMENTO["Metabolismo ed energia"] += ["Fosforilazione", "Trasferimento di fosfato"]
TIPI_ARGOMENTO["Stechiometria, moli e reazioni"] += ["Ossido"]
