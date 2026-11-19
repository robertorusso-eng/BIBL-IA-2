"""Reazioni in più per il Laboratorio di BIBL-IA 2 («cosa succede se sommo…?»).

Stesso formato di chimica_v2.REAZIONI: reagenti con le stesse etichette «Formula (nome)», prodotti, equazione
bilanciata (gas ↑, precipitati ↓), tipo, condizioni (quando servono), che cosa si allontana o si vede, e una
spiegazione con i numeri di ossidazione e gli usi nella vita reale, in medicina e nell'industria.
Nessuna coppia di reagenti ripete quelle già presenti in chimica_v2.REAZIONI.
"""


def _r(reagenti, prodotti, equazione, tipo, allontana, spiegazione, condizioni=None):
    voce = {"reagenti": reagenti, "prodotti": prodotti, "equazione": equazione, "tipo": tipo}
    if condizioni:
        voce["condizioni"] = condizioni
    voce["allontana"] = allontana
    voce["spiegazione"] = spiegazione
    return voce


REAZIONI_EXTRA = [
    # --- Elemento + elemento (sintesi) ------------------------------------------------------------------
    _r(["Na (sodio)", "Cl₂ (cloro)"], ["NaCl (cloruro di sodio)"],
       "2 Na + Cl₂ → 2 NaCl", "Sintesi (ossidoriduzione tra elementi)",
       "Niente si libera: il sodio brucia nel gas verde-giallo con una fiamma gialla intensa e resta una polvere "
       "bianca di sale. Si libera molto calore.",
       "Il sodio si ossida (da 0 a +1) cedendo il suo unico elettrone esterno, il cloro si riduce (da 0 a −1) "
       "acquistandolo: nasce il legame ionico Na⁺Cl⁻. Da un metallo tenero e reattivo e da un gas tossico si ottiene "
       "il comune sale da cucina. È molto esotermica (ΔH ≈ −411 kJ per mole di NaCl) ed è l'esempio classico di "
       "formazione di un composto ionico.",
       "basta un piccolo riscaldamento iniziale"),
    _r(["Fe (ferro)", "S (zolfo)"], ["FeS (solfuro di ferro)"],
       "Fe + S → FeS", "Sintesi (ossidoriduzione tra elementi)",
       "Niente gas: la miscela grigio-gialla diventa incandescente e resta un solido grigio-nero di solfuro di "
       "ferro(II), che la calamita non attira più.",
       "Il ferro si ossida (da 0 a +2) e lo zolfo si riduce (da 0 a −2). È l'esperimento classico che distingue un "
       "miscuglio da un composto: prima il ferro si separa con la calamita, dopo non più, perché si è formata una "
       "sostanza nuova con proprietà diverse. Una volta avviata va avanti da sola, perché è esotermica.",
       "riscaldare la miscela di polveri finché si innesca"),
    _r(["H₂ (idrogeno)", "Cl₂ (cloro)"], ["HCl (cloruro di idrogeno)"],
       "H₂ + Cl₂ → 2 HCl", "Sintesi (reazione a catena)",
       "Si forma cloruro di idrogeno, un gas incolore che all'aria umida fa fumi bianchi; il colore verde-giallo del "
       "cloro scompare. Con luce forte la miscela esplode.",
       "L'idrogeno si ossida (da 0 a +1) e il cloro si riduce (da 0 a −1). La luce rompe le molecole di Cl₂ in "
       "radicali che avviano una reazione a catena velocissima. Sciogliendo il gas HCl in acqua si ottiene l'acido "
       "cloridrico: è anche così che lo si produce industrialmente.",
       "luce (ultravioletta) o una scintilla"),
    _r(["N₂ (azoto)", "O₂ (ossigeno)"], ["NO (monossido di azoto)"],
       "N₂ + O₂ ⇌ 2 NO", "Sintesi (ad alta temperatura)",
       "Si forma monossido di azoto, gas incolore che all'aria diventa subito biossido di azoto rosso-bruno.",
       "L'azoto si ossida (da 0 a +2) e l'ossigeno si riduce (da 0 a −2). La reazione è endotermica (ΔH ≈ +180 kJ) "
       "e il triplo legame di N₂ è fortissimo, quindi avviene solo a temperature altissime: nei fulmini, nei motori e "
       "nelle centrali. Così nascono gli ossidi di azoto (NOx) dello smog e delle piogge acide, che le marmitte "
       "catalitiche riportano ad azoto.",
       "oltre 2000 °C (fulmini, camere di combustione dei motori)"),
    _r(["C (carbonio)", "O₂ (ossigeno)"], ["CO₂ (anidride carbonica)"],
       "C + O₂ → CO₂", "Combustione (completa)",
       "Si libera anidride carbonica, un gas incolore; il carbone brucia con brace rossa e molto calore "
       "(ΔH ≈ −394 kJ/mol).",
       "Con ossigeno abbondante il carbonio si ossida fino al numero di ossidazione massimo (da 0 a +4), mentre "
       "l'ossigeno si riduce (da 0 a −2). È la reazione del carbone nelle centrali termoelettriche e nella brace del "
       "barbecue, e una delle principali fonti di CO₂ che aumentano l'effetto serra.",
       "accensione, ossigeno in eccesso"),
    _r(["C (carbonio)", "O₂ (ossigeno)"], ["CO (monossido di carbonio)"],
       "2 C + O₂ → 2 CO", "Combustione (incompleta)",
       "Si libera monossido di carbonio, un gas incolore, inodore e molto tossico.",
       "Con poco ossigeno il carbonio si ossida solo fino a +2. Il CO si lega all'emoglobina circa 200-250 volte più "
       "dell'ossigeno e impedisce il trasporto di O₂: è l'avvelenamento da stufe, bracieri e caldaie che funzionano "
       "male in ambienti chiusi (per questo esistono i rilevatori di CO). Nell'altoforno, invece, il CO è utile: è "
       "il riducente che trasforma il minerale in ferro.",
       "poco ossigeno (combustione in ambiente chiuso o mal ventilato)"),
    _r(["S (zolfo)", "O₂ (ossigeno)"], ["SO₂ (anidride solforosa)"],
       "S + O₂ → SO₂", "Combustione (sintesi di un ossido acido)",
       "Si libera anidride solforosa, un gas incolore dall'odore pungente (quello dei fiammiferi); lo zolfo fonde e "
       "brucia con una fiamma azzurra.",
       "Lo zolfo si ossida (da 0 a +4) e l'ossigeno si riduce (da 0 a −2). L'SO₂ è la materia prima dell'acido "
       "solforico e si usa come conservante nel vino (i «solfiti»); bruciando carbone e petrolio contenenti zolfo "
       "finisce nell'aria e provoca le piogge acide.",
       "accensione"),
    _r(["Al (alluminio)", "O₂ (ossigeno)"], ["Al₂O₃ (ossido di alluminio)"],
       "4 Al + 3 O₂ → 2 Al₂O₃", "Sintesi (ossidazione di un metallo)",
       "Niente: all'aria si forma subito uno strato sottilissimo e trasparente di ossido. La polvere di alluminio, "
       "invece, brucia con una luce bianca abbagliante.",
       "L'alluminio si ossida (da 0 a +3) e l'ossigeno si riduce (da 0 a −2). Lo strato di Al₂O₃ è compatto e "
       "aderente e protegge il metallo sottostante (passivazione): per questo l'alluminio non arrugginisce, e "
       "l'anodizzazione rende lo strato più spesso. La polvere di alluminio si usa nei fuochi d'artificio e nei "
       "propellenti solidi dei razzi.",
       "a temperatura ambiente (strato protettivo) o accendendo la polvere"),
    _r(["Cu (rame)", "O₂ (ossigeno)"], ["CuO (ossido di rame)"],
       "2 Cu + O₂ → 2 CuO", "Sintesi (ossidazione di un metallo)",
       "Niente gas: il rame rosso, scaldato nella fiamma, si ricopre di uno strato nero di ossido di rame(II).",
       "Il rame si ossida (da 0 a +2) e l'ossigeno si riduce (da 0 a −2). A temperatura ambiente il rame si ossida "
       "lentissimamente; in anni, con CO₂ e umidità, forma invece la patina verde (carbonato basico di rame) dei "
       "tetti e delle statue, come la Statua della Libertà.",
       "riscaldamento nella fiamma"),
    _r(["Ca (calcio)", "O₂ (ossigeno)"], ["CaO (ossido di calcio, calce viva)"],
       "2 Ca + O₂ → 2 CaO", "Sintesi (ossidazione di un metallo)",
       "Niente gas: il calcio brucia con una fiamma rosso-arancio e resta una polvere bianca di calce viva.",
       "Il calcio si ossida (da 0 a +2) e l'ossigeno si riduce (da 0 a −2). Il colore rosso-arancio della fiamma "
       "è il «saggio alla fiamma» del calcio, usato per riconoscerlo. Industrialmente la calce viva non si fa così "
       "(il calcio metallico costa troppo) ma scaldando il calcare.",
       "accensione"),
    _r(["Li (litio)", "H₂O (acqua)"], ["LiOH (idrossido di litio)", "H₂ ↑"],
       "2 Li + 2 H₂O → 2 LiOH + H₂↑", "Ossidoriduzione (metallo alcalino + acqua)",
       "Si libera idrogeno: il litio galleggia e frizza con calma, senza infiammarsi; con la fenolftaleina l'acqua "
       "diventa fucsia.",
       "Il litio si ossida (da 0 a +1) e l'idrogeno dell'acqua si riduce (da +1 a 0); la soluzione diventa basica "
       "per l'LiOH. Fra i metalli alcalini è quello che reagisce più lentamente, ma reagisce comunque: per questo le "
       "batterie al litio non vanno forate, bagnate o schiacciate.",
       None),
    _r(["K (potassio)", "H₂O (acqua)"], ["KOH (idrossido di potassio)", "H₂ ↑"],
       "2 K + 2 H₂O → 2 KOH + H₂↑", "Ossidoriduzione (metallo alcalino + acqua)",
       "Si libera idrogeno che si incendia subito con una fiamma lilla; il potassio sfreccia sull'acqua e può "
       "scoppiettare. Reazione violenta.",
       "Il potassio si ossida (da 0 a +1) e l'idrogeno dell'acqua si riduce (da +1 a 0). È più violento del sodio "
       "perché il suo elettrone esterno è più lontano dal nucleo (raggio atomico maggiore, energia di ionizzazione "
       "minore): scendendo nel gruppo i metalli alcalini diventano più reattivi. Il colore lilla è il saggio alla "
       "fiamma del potassio.",
       None),
    _r(["Zn (zinco)", "S (zolfo)"], ["ZnS (solfuro di zinco)"],
       "Zn + S → ZnS", "Sintesi (ossidoriduzione tra elementi)",
       "Niente gas: la miscela di polveri reagisce in modo vivacissimo, con un lampo, fiamma e fumo; resta solfuro "
       "di zinco bianco-giallastro.",
       "Lo zinco si ossida (da 0 a +2) e lo zolfo si riduce (da 0 a −2). È così esotermica che è stata usata come "
       "propellente per piccoli razzi dimostrativi. Lo ZnS è un pigmento bianco e un materiale fosforescente (vecchi "
       "schermi a tubo catodico e lancette luminose).",
       "innesco con una fiamma (solo all'aperto o sotto cappa)"),
    _r(["P₄ (fosforo bianco)", "O₂ (ossigeno)"], ["P₄O₁₀ (decaossido di tetrafosforo)"],
       "P₄ + 5 O₂ → P₄O₁₀", "Combustione (sintesi di un ossido acido)",
       "Si forma un fumo bianco e denso di ossido di fosforo; al buio il fosforo bianco brilla di luce verdastra "
       "(chemiluminescenza).",
       "Il fosforo si ossida (da 0 a +5) e l'ossigeno si riduce (da 0 a −2). Il fosforo bianco si accende da solo "
       "all'aria già verso 30 °C, per questo si conserva sott'acqua; il fosforo rosso, molto più stabile, è sulla "
       "striscia delle scatole di fiammiferi. Il P₄O₁₀ è un disidratante potentissimo e con l'acqua dà acido "
       "fosforico.",
       "si accende spontaneamente all'aria (≈ 30 °C)"),
    _r(["Al (alluminio)", "Cl₂ (cloro)"], ["AlCl₃ (cloruro di alluminio)"],
       "2 Al + 3 Cl₂ → 2 AlCl₃", "Sintesi (ossidoriduzione tra elementi)",
       "Niente gas: l'alluminio si incendia nel cloro con scintille; resta cloruro di alluminio, un solido "
       "bianco-giallastro che fuma all'aria umida.",
       "L'alluminio si ossida (da 0 a +3) e il cloro si riduce (da 0 a −1): servono 3 Cl₂ per ogni 2 Al per "
       "scambiare 6 elettroni. Il cloruro di alluminio anidro è un acido di Lewis usato come catalizzatore nelle "
       "reazioni di Friedel-Crafts (per esempio per produrre detergenti e plastiche).",
       "foglio o polvere di alluminio, leggero riscaldamento"),
    _r(["Fe (ferro)", "Cl₂ (cloro)"], ["FeCl₃ (cloruro ferrico)"],
       "2 Fe + 3 Cl₂ → 2 FeCl₃", "Sintesi (ossidoriduzione tra elementi)",
       "Si formano fumi bruni di cloruro ferrico, che si depositano come solido bruno-nero.",
       "Il ferro si ossida (da 0 a +3) e il cloro si riduce (da 0 a −1). Il cloro è un ossidante forte e porta "
       "il ferro direttamente a +3, mentre l'acido cloridrico (H⁺ è un ossidante debole) lo porta solo a +2. "
       "Il FeCl₃ si usa come coagulante nella depurazione delle acque e per incidere i circuiti stampati.",
       "lana di ferro riscaldata"),
    _r(["Mg (magnesio)", "N₂ (azoto)"], ["Mg₃N₂ (nitruro di magnesio)"],
       "3 Mg + N₂ → Mg₃N₂", "Sintesi (ossidoriduzione tra elementi)",
       "Niente gas: si forma un solido giallo-verdastro di nitruro di magnesio (quando il magnesio brucia all'aria "
       "si forma insieme all'ossido bianco).",
       "Il magnesio si ossida (da 0 a +2) e l'azoto si riduce (da 0 a −3). L'azoto è di solito pochissimo reattivo "
       "per il suo triplo legame, ma il magnesio che brucia raggiunge temperature così alte da riuscire a romperlo. "
       "Il nitruro con l'acqua libera ammoniaca, e da quell'odore si riconosce.",
       "magnesio acceso in atmosfera di azoto"),
    _r(["Cu (rame)", "S (zolfo)"], ["Cu₂S (solfuro di rame(I))"],
       "2 Cu + S → Cu₂S", "Sintesi (ossidoriduzione tra elementi)",
       "Niente gas: il filo di rame immerso nei vapori di zolfo diventa nero e fragile, ricoperto di solfuro di "
       "rame(I).",
       "Il rame si ossida (da 0 a +1) e lo zolfo si riduce (da 0 a −2). Il Cu₂S è la calcocite, uno dei minerali "
       "da cui si estrae il rame. Un processo simile fa annerire l'argenteria, che reagisce con i composti dello "
       "zolfo presenti nell'aria e nei cibi (uova) formando Ag₂S nero.",
       "riscaldamento (vapori di zolfo)"),
    _r(["H₂ (idrogeno)", "S (zolfo)"], ["H₂S (acido solfidrico)"],
       "H₂ + S → H₂S", "Sintesi (ossidoriduzione tra elementi)",
       "Si forma acido solfidrico, gas incolore, tossico, con il tipico odore di uova marce.",
       "Qui lo zolfo fa da ossidante: si riduce da 0 a −2, mentre l'idrogeno si ossida da 0 a +1. L'H₂S si trova "
       "nei gas vulcanici e nelle acque termali sulfuree; ad alte concentrazioni è tossico quanto il cianuro e "
       "paralizza l'olfatto, quindi non ci si può fidare del naso.",
       "zolfo fuso, ≈ 400 °C"),
    _r(["Cl₂ (cloro)", "H₂O (acqua)"], ["HCl (acido cloridrico)", "HClO (acido ipocloroso)"],
       "Cl₂ + H₂O ⇌ HCl + HClO", "Disproporzione (ossidoriduzione)",
       "Niente gas: si forma «acqua di cloro», giallo-verdina, che sbianca e disinfetta.",
       "Il cloro (0) in parte si riduce a −1 (HCl) e in parte si ossida a +1 (HClO): è una disproporzione. "
       "L'acido ipocloroso uccide batteri e virus: è il principio della clorazione dell'acqua potabile e delle "
       "piscine.",
       None),
    _r(["Cl₂ (cloro)", "NaOH (idrossido di sodio)"], ["NaCl", "NaClO (ipoclorito di sodio)", "H₂O"],
       "Cl₂ + 2 NaOH → NaCl + NaClO + H₂O", "Disproporzione (ossidoriduzione)",
       "Niente gas: il cloro viene assorbito dalla soda e si forma la candeggina (soluzione di ipoclorito).",
       "Il cloro (0) si riduce a −1 nel cloruro e si ossida a +1 nell'ipoclorito. È così che si produce la "
       "varechina per la casa; a caldo, invece, si forma clorato (NaClO₃). Spiega anche perché candeggina e acidi "
       "non vanno mescolati: la reazione si inverte e torna a liberare cloro.",
       "a freddo, soluzione diluita"),
    _r(["Cl₂ (cloro)", "KI (ioduro di potassio)"], ["KCl (cloruro di potassio)", "I₂ (iodio)"],
       "Cl₂ + 2 KI → 2 KCl + I₂", "Ossidoriduzione (alogeni)",
       "Si forma iodio: la soluzione incolore diventa giallo-bruna (blu-nera se c'è amido).",
       "Il cloro si riduce (da 0 a −1) e lo ioduro si ossida (da −1 a 0): il cloro è un ossidante più forte "
       "dello iodio e lo «sposta» dai suoi sali. Le cartine all'amido-ioduro usano proprio questa reazione per "
       "rivelare il cloro e gli altri ossidanti: diventano blu.",
       None),
    _r(["Br₂ (bromo)", "KI (ioduro di potassio)"], ["KBr (bromuro di potassio)", "I₂ (iodio)"],
       "Br₂ + 2 KI → 2 KBr + I₂", "Ossidoriduzione (alogeni)",
       "La soluzione arancione del bromo diventa bruna per lo iodio; agitando con un po' di esano lo iodio passa "
       "nello strato organico, che si colora di viola.",
       "Il bromo si riduce (da 0 a −1) e lo ioduro si ossida (da −1 a 0). Conferma la scala del potere ossidante "
       "degli alogeni, F₂ > Cl₂ > Br₂ > I₂, che diminuisce scendendo nel gruppo: al contrario, lo iodio non reagisce "
       "con il bromuro.",
       None),
    # --- Metalli + acidi, acqua, basi e sali (serie di attività) --------------------------------------------
    _r(["Al (alluminio)", "HCl (acido cloridrico)"], ["AlCl₃ (cloruro di alluminio)", "H₂ ↑"],
       "2 Al + 6 HCl → 2 AlCl₃ + 3 H₂↑", "Ossidoriduzione (metallo + acido)",
       "Si libera idrogeno: dopo un attimo di ritardo l'effervescenza diventa vivace e la provetta si scalda.",
       "L'alluminio si ossida (da 0 a +3) e l'H⁺ si riduce (da +1 a 0). Il ritardo iniziale è dovuto allo strato "
       "protettivo di ossido, che l'acido deve prima sciogliere. Per lo stesso motivo non conviene conservare cibi "
       "acidi e salati (pomodoro, limone) nei contenitori di alluminio.",
       None),
    _r(["Fe (ferro)", "HCl (acido cloridrico)"], ["FeCl₂ (cloruro ferroso)", "H₂ ↑"],
       "Fe + 2 HCl → FeCl₂ + H₂↑", "Ossidoriduzione (metallo + acido)",
       "Si libera idrogeno (bollicine); la soluzione diventa verde pallido per gli ioni Fe²⁺.",
       "Il ferro si ossida (da 0 a +2) e l'H⁺ si riduce (da +1 a 0). L'H⁺ è un ossidante debole e porta il ferro "
       "solo a +2. Nell'industria l'acido cloridrico si usa per il «decapaggio» dell'acciaio: toglie ruggine e "
       "ossidi prima della zincatura o della verniciatura.",
       None),
    _r(["Zn (zinco)", "H₂SO₄ (acido solforico diluito)"], ["ZnSO₄ (solfato di zinco)", "H₂ ↑"],
       "Zn + H₂SO₄ → ZnSO₄ + H₂↑", "Ossidoriduzione (metallo + acido)",
       "Si libera idrogeno; lo zinco si consuma e la soluzione resta incolore.",
       "Lo zinco si ossida (da 0 a +2) e l'H⁺ si riduce (da +1 a 0). È il metodo classico di laboratorio per "
       "preparare idrogeno (apparecchio di Kipp). Una goccia di solfato di rame la accelera molto, perché sullo "
       "zinco si deposita rame e si formano tante micro-pile.",
       None),
    _r(["Mg (magnesio)", "CH₃COOH (acido acetico)"], ["(CH₃COO)₂Mg (acetato di magnesio)", "H₂ ↑"],
       "Mg + 2 CH₃COOH → (CH₃COO)₂Mg + H₂↑", "Ossidoriduzione (metallo + acido debole)",
       "Si libera idrogeno, ma le bollicine sono più lente che con l'acido cloridrico.",
       "Il magnesio si ossida (da 0 a +2) e l'H⁺ si riduce (da +1 a 0). L'acido acetico è debole: a parità di "
       "concentrazione ha molti meno H⁺ liberi, quindi la reazione è più lenta, anche se alla fine (a parità di moli "
       "di acido) si libera la stessa quantità di idrogeno. È l'esperimento tipico per confrontare acidi forti e "
       "deboli.",
       None),
    _r(["Cu (rame)", "HNO₃ (acido nitrico diluito)"], ["Cu(NO₃)₂ (nitrato di rame)", "NO ↑", "H₂O"],
       "3 Cu + 8 HNO₃ → 3 Cu(NO₃)₂ + 2 NO↑ + 4 H₂O", "Ossidoriduzione (metallo + acido ossidante)",
       "Si libera monossido di azoto, gas incolore che all'aria diventa subito rosso-bruno (NO₂); la soluzione "
       "diventa azzurra per gli ioni Cu²⁺.",
       "Il rame si ossida (da 0 a +2) e l'azoto si riduce (da +5 a +2). Con l'acido diluito l'azoto si riduce di "
       "più (fino a NO) che con l'acido concentrato (fino a NO₂). Degli 8 HNO₃ solo 2 si riducono; gli altri 6 "
       "restano come ioni nitrato nel sale.",
       None),
    _r(["Cu (rame)", "H₂SO₄ (acido solforico concentrato)"], ["CuSO₄ (solfato di rame)", "SO₂ ↑", "H₂O"],
       "Cu + 2 H₂SO₄ → CuSO₄ + SO₂↑ + 2 H₂O", "Ossidoriduzione (metallo + acido ossidante)",
       "Si libera anidride solforosa, gas dall'odore pungente; diluendo con acqua la soluzione diventa azzurra.",
       "Il rame si ossida (da 0 a +2) e lo zolfo si riduce (da +6 a +4). Il rame non reagisce con gli H⁺ "
       "(sta dopo l'idrogeno nella serie di attività), per cui l'acido solforico diluito non lo attacca: lo "
       "attacca solo quello concentrato e caldo, che ossida tramite lo zolfo.",
       "acido concentrato e caldo"),
    _r(["Mg (magnesio)", "H₂O (acqua)"], ["Mg(OH)₂ (idrossido di magnesio)", "H₂ ↑"],
       "Mg + 2 H₂O → Mg(OH)₂ + H₂↑", "Ossidoriduzione (metallo + acqua)",
       "Poche bollicine di idrogeno; con la fenolftaleina l'acqua diventa rosa.",
       "Il magnesio si ossida (da 0 a +2) e l'idrogeno dell'acqua si riduce (da +1 a 0). A freddo è lentissima "
       "perché l'idrossido, poco solubile, ricopre il metallo; con il vapore e il magnesio caldo diventa violenta. "
       "Per questo gli incendi di magnesio non si spengono con l'acqua.",
       "acqua calda (a freddo quasi non si vede)"),
    _r(["Fe (ferro)", "H₂O (vapore)"], ["Fe₃O₄ (magnetite)", "H₂ ↑"],
       "3 Fe + 4 H₂O ⇌ Fe₃O₄ + 4 H₂↑", "Ossidoriduzione (metallo + vapore)",
       "Si libera idrogeno; il ferro si ricopre di un ossido nero e magnetico (magnetite).",
       "Il ferro si ossida (nella magnetite ci sono insieme Fe²⁺ e Fe³⁺) e l'idrogeno dell'acqua si riduce (da +1 "
       "a 0). Lavoisier usò questa reazione, facendo passare vapore in una canna di fucile rovente, per dimostrare "
       "che l'acqua non è un elemento ma un composto di idrogeno e ossigeno.",
       "ferro rovente, ≈ 500-800 °C"),
    _r(["Cu (rame)", "AgNO₃ (nitrato d'argento)"], ["Cu(NO₃)₂ (nitrato di rame)", "Ag ↓"],
       "Cu + 2 AgNO₃ → Cu(NO₃)₂ + 2 Ag", "Ossidoriduzione (spostamento)",
       "Sul filo di rame crescono cristalli lucenti d'argento («albero di Diana»); la soluzione incolore diventa "
       "azzurra.",
       "Il rame si ossida (da 0 a +2) e l'argento si riduce (da +1 a 0): ogni atomo di rame cede 2 elettroni a "
       "2 ioni Ag⁺. Avviene perché il rame è più riducente dell'argento (E° Cu²⁺/Cu = +0,34 V, Ag⁺/Ag = +0,80 V). "
       "È un esempio classico della serie elettrochimica.",
       None),
    _r(["Mg (magnesio)", "CuSO₄ (solfato di rame)"], ["MgSO₄ (solfato di magnesio)", "Cu ↓"],
       "Mg + CuSO₄ → MgSO₄ + Cu", "Ossidoriduzione (spostamento)",
       "Il magnesio si ricopre di rame rosso-bruno, la soluzione azzurra si schiarisce e si scalda.",
       "Il magnesio si ossida (da 0 a +2) e il rame si riduce (da +2 a 0). La differenza di potenziale è "
       "grandissima (E° Mg²⁺/Mg = −2,37 V contro +0,34 V del rame), quindi la reazione è rapida ed esotermica. "
       "Il magnesio si usa come «anodo sacrificale» per proteggere scafi e tubature d'acciaio.",
       None),
    _r(["Zn (zinco)", "Pb(NO₃)₂ (nitrato di piombo)"], ["Zn(NO₃)₂ (nitrato di zinco)", "Pb ↓"],
       "Zn + Pb(NO₃)₂ → Zn(NO₃)₂ + Pb", "Ossidoriduzione (spostamento)",
       "Sullo zinco crescono foglioline grigie e luccicanti di piombo («albero di Saturno»).",
       "Lo zinco si ossida (da 0 a +2) e il piombo si riduce (da +2 a 0): lo zinco precede il piombo nella serie "
       "di attività. Il nome viene dagli alchimisti, che associavano il piombo al pianeta Saturno.",
       None),
    _r(["Al (alluminio)", "CuCl₂ (cloruro rameico)"], ["AlCl₃ (cloruro di alluminio)", "Cu ↓"],
       "2 Al + 3 CuCl₂ → 2 AlCl₃ + 3 Cu", "Ossidoriduzione (spostamento)",
       "Sul foglio di alluminio si deposita rame rosso-bruno spugnoso, la soluzione verde-azzurra si scolora, si "
       "sviluppa molto calore e qualche bollicina di idrogeno.",
       "L'alluminio si ossida (da 0 a +3) e il rame si riduce (da +2 a 0): 2 Al cedono 6 elettroni, che 3 Cu²⁺ "
       "acquistano. Con il cloruro la reazione è rapida perché gli ioni Cl⁻ rompono lo strato protettivo di ossido; "
       "con il solfato di rame, invece, l'alluminio reagisce lentissimamente.",
       None),
    _r(["Al (alluminio)", "NaOH (idrossido di sodio)"], ["Na[Al(OH)₄] (alluminato di sodio)", "H₂ ↑"],
       "2 Al + 2 NaOH + 6 H₂O → 2 Na[Al(OH)₄] + 3 H₂↑", "Ossidoriduzione (metallo anfotero + base)",
       "Si libera idrogeno con effervescenza abbondante e molto calore; l'alluminio si scioglie.",
       "L'alluminio si ossida (da 0 a +3) e l'idrogeno dell'acqua si riduce (da +1 a 0). L'alluminio è anfotero: "
       "la base scioglie lo strato di ossido e poi il metallo reagisce con l'acqua. È il principio dei disgorganti "
       "per tubi (soda caustica con granuli di alluminio) e il motivo per cui le pentole di alluminio non vanno "
       "lavate con prodotti fortemente basici.",
       "soluzione acquosa di soda"),
    _r(["Mg (magnesio)", "CO₂ (anidride carbonica)"], ["MgO (ossido di magnesio)", "C (carbonio)"],
       "2 Mg + CO₂ → 2 MgO + C", "Ossidoriduzione (metallo + ossido)",
       "Il magnesio continua a bruciare dentro la CO₂ con luce bianca; restano polvere bianca (MgO) e puntini neri "
       "di carbonio.",
       "Il magnesio si ossida (da 0 a +2) e il carbonio si riduce (da +4 a 0). Il magnesio è così riducente da "
       "strappare l'ossigeno perfino all'anidride carbonica: per questo gli estintori a CO₂ non spengono gli "
       "incendi di metalli, che richiedono estintori di classe D o sabbia secca.",
       "magnesio già acceso"),
    # --- Ossidi + acqua, ossidi + acidi e basi ------------------------------------------------------------
    _r(["K₂O (ossido di potassio)", "H₂O (acqua)"], ["KOH (idrossido di potassio)"],
       "K₂O + H₂O → 2 KOH", "Ossido basico + acqua → idrossido",
       "Niente gas: si libera calore e la soluzione diventa fortemente basica.",
       "Lo ione ossido O²⁻ è una base fortissima: strappa un H⁺ all'acqua e si formano due ioni OH⁻. Nessun "
       "numero di ossidazione cambia (non è una ossidoriduzione). Il KOH è la potassa caustica, usata per i saponi "
       "molli e come elettrolita nelle pile alcaline.",
       None),
    _r(["P₄O₁₀ (decaossido di tetrafosforo)", "H₂O (acqua)"], ["H₃PO₄ (acido fosforico)"],
       "P₄O₁₀ + 6 H₂O → 4 H₃PO₄", "Ossido acido (anidride) + acqua → ossiacido",
       "Niente gas: la reazione è violenta, sibila e libera molto calore.",
       "Un ossido di non metallo con l'acqua dà un ossiacido; il fosforo resta +5. La grande avidità per l'acqua "
       "fa del P₄O₁₀ uno dei disidratanti più potenti, usato negli essiccatori. L'acido fosforico si trova nelle "
       "bibite tipo cola, nei fertilizzanti e nei prodotti antiruggine.",
       None),
    _r(["CO₂ (anidride carbonica)", "NaOH (idrossido di sodio)"], ["Na₂CO₃ (carbonato di sodio)", "H₂O"],
       "CO₂ + 2 NaOH → Na₂CO₃ + H₂O", "Acido-base (ossido acido + base)",
       "Niente gas: la CO₂ viene assorbita e si forma acqua.",
       "L'anidride carbonica si comporta da acido: con l'acqua darebbe acido carbonico, che la base neutralizza. "
       "Con CO₂ in eccesso si forma invece bicarbonato (NaHCO₃). È il modo in cui si cattura la CO₂ in laboratorio, "
       "nei sottomarini e nelle capsule spaziali (lì con calce sodata o idrossido di litio).",
       None),
    _r(["SO₂ (anidride solforosa)", "Ca(OH)₂ (idrossido di calcio)"], ["CaSO₃ ↓ (solfito di calcio)", "H₂O"],
       "SO₂ + Ca(OH)₂ → CaSO₃↓ + H₂O", "Acido-base (ossido acido + base)",
       "Precipita solfito di calcio, un solido bianco; si forma acqua.",
       "L'anidride solforosa, ossido acido, viene neutralizzata dalla calce; lo zolfo resta +4. È la "
       "desolforazione dei fumi delle centrali a carbone: il solfito viene poi ossidato a gesso (CaSO₄·2H₂O), "
       "usato in edilizia. Così si riducono molto le piogge acide.",
       None),
    _r(["CaO (ossido di calcio, calce viva)", "CO₂ (anidride carbonica)"], ["CaCO₃ (carbonato di calcio)"],
       "CaO + CO₂ → CaCO₃", "Sintesi (ossido basico + ossido acido)",
       "Niente: la CO₂ viene fissata come carbonato di calcio, solido bianco.",
       "Un ossido basico e un ossido acido si uniscono e formano un sale; nessun elemento cambia numero di "
       "ossidazione. È la reazione inversa della calcinazione del calcare e viene studiata per catturare la CO₂ "
       "dai fumi industriali («calcium looping»).",
       None),
    _r(["CaO (ossido di calcio, calce viva)", "SiO₂ (silice, sabbia)"], ["CaSiO₃ (silicato di calcio, scoria)"],
       "CaO + SiO₂ → CaSiO₃", "Sintesi (ossido basico + ossido acido)",
       "Si forma una scoria fusa di silicato di calcio, che galleggia sopra la ghisa liquida.",
       "La calce (basica) si combina con la silice (acida) e forma un sale; nessun numero di ossidazione cambia. "
       "Nell'altoforno il calcare aggiunto (il «fondente») elimina così le impurezze di sabbia del minerale di "
       "ferro; la scoria raffreddata si usa per il cemento e le massicciate stradali.",
       "≈ 1500 °C (altoforno)"),
    _r(["CuO (ossido di rame)", "H₂SO₄ (acido solforico)"], ["CuSO₄ (solfato di rame)", "H₂O"],
       "CuO + H₂SO₄ → CuSO₄ + H₂O", "Acido-base (ossido basico + acido)",
       "Si forma acqua; la polvere nera scompare e la soluzione diventa azzurra.",
       "Lo ione ossido prende due H⁺ e forma acqua; il rame resta +2 (non è una ossidoriduzione). È il metodo di "
       "laboratorio per preparare i cristalli blu di solfato di rame pentaidrato, usato anche in agricoltura "
       "(poltiglia bordolese contro la peronospora della vite).",
       "acido diluito e tiepido"),
    _r(["Fe₂O₃ (ossido ferrico, ruggine)", "HCl (acido cloridrico)"], ["FeCl₃ (cloruro ferrico)", "H₂O"],
       "Fe₂O₃ + 6 HCl → 2 FeCl₃ + 3 H₂O", "Acido-base (ossido basico + acido)",
       "Si forma acqua; la ruggine si scioglie e la soluzione diventa giallo-arancio per gli ioni Fe³⁺.",
       "Gli ossidi dei metalli reagiscono con gli acidi come basi: ogni O²⁻ prende due H⁺ e diventa acqua; il ferro "
       "resta +3. È ciò che fanno i prodotti antiruggine e il decapaggio industriale, che puliscono l'acciaio prima "
       "di verniciarlo o zincarlo.",
       None),
    _r(["Al₂O₃ (ossido di alluminio)", "NaOH (idrossido di sodio)"], ["Na[Al(OH)₄] (alluminato di sodio)"],
       "Al₂O₃ + 2 NaOH + 3 H₂O → 2 Na[Al(OH)₄]", "Acido-base (ossido anfotero + base)",
       "Niente gas: l'ossido bianco si scioglie e la soluzione resta limpida.",
       "L'ossido di alluminio è anfotero: con gli acidi si comporta da base, con le basi forti da acido e forma "
       "lo ione alluminato; l'alluminio resta +3. È il cuore del processo Bayer, che purifica la bauxite separando "
       "l'allumina dagli ossidi di ferro prima dell'elettrolisi.",
       "soda concentrata e calda, sotto pressione"),
    _r(["CaCO₃ (carbonato di calcio)", "CO₂ (anidride carbonica)"], ["Ca(HCO₃)₂ (bicarbonato di calcio)"],
       "CaCO₃ + CO₂ + H₂O ⇌ Ca(HCO₃)₂", "Acido-base (dissoluzione del calcare, carsismo)",
       "Niente: il calcare insolubile diventa bicarbonato di calcio, solubile, e si scioglie nell'acqua.",
       "L'acqua piovana con la CO₂ sciolta (acido carbonico) scioglie lentamente le rocce calcaree e scava grotte "
       "e doline. La reazione inversa, quando l'acqua perde CO₂, forma stalattiti e stalagmiti e il calcare nei "
       "bollitori e nelle lavatrici (a caldo la CO₂ se ne va).",
       "in presenza di acqua"),
    # --- Acidi e basi ------------------------------------------------------------------------------------
    _r(["H₃PO₄ (acido fosforico)", "NaOH (idrossido di sodio)"], ["Na₃PO₄ (fosfato di sodio)", "H₂O"],
       "H₃PO₄ + 3 NaOH → Na₃PO₄ + 3 H₂O", "Acido-base (neutralizzazione di un acido triprotico)",
       "Si formano 3 molecole d'acqua; il sale resta sciolto.",
       "L'acido fosforico cede i suoi 3 H⁺ uno alla volta (tre punti di equivalenza nella titolazione), quindi "
       "servono 3 NaOH. Le coppie intermedie H₂PO₄⁻/HPO₄²⁻ formano il tampone fosfato, che mantiene il pH dentro le "
       "cellule e nelle urine.",
       None),
    _r(["H₂SO₄ (acido solforico)", "Ca(OH)₂ (idrossido di calcio)"], ["CaSO₄ ↓ (solfato di calcio, gesso)", "H₂O"],
       "H₂SO₄ + Ca(OH)₂ → CaSO₄↓ + 2 H₂O", "Acido-base (neutralizzazione)",
       "Si forma acqua e la soluzione diventa torbida per il solfato di calcio, poco solubile.",
       "Due H⁺ e due OH⁻ formano due molecole d'acqua. La calce è la base più economica: si usa per neutralizzare "
       "le acque acide delle miniere e degli scarichi industriali e per correggere i terreni troppo acidi.",
       None),
    _r(["HCl (acido cloridrico)", "Al(OH)₃ (idrossido di alluminio)"], ["AlCl₃ (cloruro di alluminio)", "H₂O"],
       "3 HCl + Al(OH)₃ → AlCl₃ + 3 H₂O", "Acido-base (neutralizzazione, antiacido)",
       "Si formano 3 molecole d'acqua; il solido bianco si scioglie.",
       "Ogni idrossido di alluminio neutralizza tre H⁺. È uno dei principi attivi degli antiacidi per il bruciore "
       "di stomaco (spesso insieme a Mg(OH)₂, perché l'alluminio rallenta l'intestino e il magnesio lo accelera).",
       None),
    _r(["H₂SO₄ (acido solforico)", "NH₃ (ammoniaca)"], ["(NH₄)₂SO₄ (solfato di ammonio)"],
       "H₂SO₄ + 2 NH₃ → (NH₄)₂SO₄", "Acido-base (secondo Brønsted)",
       "Niente: si forma solfato di ammonio, un sale bianco.",
       "Ogni molecola di ammoniaca accetta un H⁺ dall'acido e diventa ione ammonio NH₄⁺; l'acido diprotico ne "
       "neutralizza due. Il solfato di ammonio è un fertilizzante azotato molto diffuso.",
       None),
    _r(["HNO₃ (acido nitrico)", "NH₃ (ammoniaca)"], ["NH₄NO₃ (nitrato di ammonio)"],
       "HNO₃ + NH₃ → NH₄NO₃", "Acido-base (secondo Brønsted)",
       "Niente: si forma nitrato di ammonio, un sale bianco; si libera calore.",
       "L'ammoniaca accetta l'H⁺ dell'acido nitrico. Il nitrato di ammonio è il fertilizzante azotato più usato al "
       "mondo (contiene azoto sia ammoniacale sia nitrico), ma è anche un ossidante pericoloso: grandi depositi "
       "mal conservati sono esplosi, come a Beirut nel 2020.",
       None),
    _r(["NH₄Cl (cloruro di ammonio)", "NaOH (idrossido di sodio)"], ["NaCl", "NH₃ ↑", "H₂O"],
       "NH₄Cl + NaOH → NaCl + NH₃↑ + H₂O", "Acido-base (una base forte sposta una base debole)",
       "Si libera ammoniaca: odore pungente, e una cartina al tornasole rossa e bagnata diventa blu.",
       "L'OH⁻ della base forte strappa un H⁺ allo ione ammonio, che torna ammoniaca; il gas se ne va scaldando. "
       "È il saggio per riconoscere i sali di ammonio e il modo più semplice per preparare ammoniaca in "
       "laboratorio.",
       "leggero riscaldamento"),
    _r(["H₂SO₄ (acido solforico)", "NaHCO₃ (bicarbonato di sodio)"], ["Na₂SO₄", "H₂O", "CO₂ ↑"],
       "H₂SO₄ + 2 NaHCO₃ → Na₂SO₄ + 2 H₂O + 2 CO₂↑", "Acido + carbonato",
       "Si libera anidride carbonica con forte effervescenza.",
       "Ogni bicarbonato accetta un H⁺ e diventa acido carbonico, che si decompone in acqua e CO₂; l'acido "
       "solforico, diprotico, ne consuma due. I vecchi estintori «soda-acido» funzionavano così: rovesciandoli "
       "l'acido cadeva nel bicarbonato e la CO₂ spingeva fuori l'acqua.",
       None),
    _r(["CH₃COOH (acido acetico)", "CaCO₃ (carbonato di calcio)"], ["(CH₃COO)₂Ca (acetato di calcio)", "H₂O", "CO₂ ↑"],
       "2 CH₃COOH + CaCO₃ → (CH₃COO)₂Ca + H₂O + CO₂↑", "Acido + carbonato",
       "Si libera anidride carbonica (bollicine) e il calcare si scioglie.",
       "Anche un acido debole come l'aceto riesce a trasformare il carbonato in acido carbonico, che si decompone. "
       "È il motivo per cui l'aceto (o l'acido citrico) toglie il calcare da rubinetti, bollitori e ferri da stiro. "
       "Un guscio d'uovo lasciato nell'aceto perde il guscio duro e resta solo la membrana.",
       None),
    _r(["C₆H₈O₇ (acido citrico)", "NaHCO₃ (bicarbonato di sodio)"], ["Na₃C₆H₅O₇ (citrato di sodio)", "H₂O", "CO₂ ↑"],
       "C₆H₈O₇ + 3 NaHCO₃ → Na₃C₆H₅O₇ + 3 H₂O + 3 CO₂↑", "Acido + carbonato",
       "Si libera anidride carbonica con vivace effervescenza (appena si aggiunge acqua).",
       "L'acido citrico è triprotico: cede 3 H⁺ a 3 bicarbonati, che diventano acqua e CO₂. Da secche le due "
       "polveri non reagiscono, perché servono ioni in soluzione: è il principio delle compresse effervescenti "
       "(vitamina C, aspirina effervescente) e delle bombe da bagno.",
       "in acqua"),
    _r(["FeS (solfuro di ferro)", "HCl (acido cloridrico)"], ["FeCl₂ (cloruro ferroso)", "H₂S ↑"],
       "FeS + 2 HCl → FeCl₂ + H₂S↑", "Acido-base (un acido forte sposta un acido debole)",
       "Si libera acido solfidrico, gas tossico con odore di uova marce.",
       "L'acido forte cede H⁺ allo ione solfuro S²⁻ e libera l'acido debole H₂S, che essendo un gas se ne va; "
       "nessun numero di ossidazione cambia. Era il modo classico di preparare H₂S nell'analisi qualitativa "
       "(apparecchio di Kipp); oggi si evita per la sua tossicità.",
       "sotto cappa"),
    _r(["NaCl (cloruro di sodio)", "H₂SO₄ (acido solforico concentrato)"], ["NaHSO₄ (solfato acido di sodio)", "HCl ↑"],
       "NaCl + H₂SO₄ → NaHSO₄ + HCl↑", "Acido-base (un acido non volatile sposta un acido volatile)",
       "Si libera cloruro di idrogeno, gas che fa fumi bianchi all'aria umida.",
       "L'acido solforico cede un H⁺ al cloruro; l'HCl gassoso, volatile, se ne va e sposta l'equilibrio verso "
       "destra. È il vecchio metodo (processo Leblanc) per produrre acido cloridrico.",
       "acido concentrato, riscaldamento moderato"),
    _r(["NH₃ (ammoniaca)", "H₂O (acqua)"], ["NH₄⁺ (ione ammonio)", "OH⁻ (ione idrossido)"],
       "NH₃ + H₂O ⇌ NH₄⁺ + OH⁻", "Acido-base (secondo Brønsted, base debole)",
       "Niente: l'ammoniaca si scioglie moltissimo e la soluzione diventa basica (pH ≈ 11).",
       "L'ammoniaca accetta un H⁺ dall'acqua, che fa da acido; l'equilibrio è molto spostato a sinistra "
       "(Kb ≈ 1,8·10⁻⁵), quindi è una base debole. L'ammoniaca per la casa è questa soluzione.",
       None),
    _r(["HCO₃⁻ (ione bicarbonato)", "H⁺ (ione idrogeno)"], ["H₂O", "CO₂ ↑"],
       "HCO₃⁻ + H⁺ ⇌ H₂O + CO₂", "Acido-base (tampone bicarbonato del sangue)",
       "Si forma CO₂, che nel corpo viene eliminata con il respiro.",
       "Il bicarbonato cattura gli H⁺ in eccesso e diventa acido carbonico, che si scinde in acqua e CO₂ "
       "(reazione accelerata dall'anidrasi carbonica). È il principale tampone del sangue: mantiene il pH tra 7,35 "
       "e 7,45, e polmoni (CO₂) e reni (HCO₃⁻) regolano i due lati dell'equilibrio.",
       None),
    _r(["Ba(OH)₂·8H₂O (idrossido di bario ottaidrato)", "NH₄Cl (cloruro di ammonio)"], ["BaCl₂", "NH₃ ↑", "H₂O"],
       "Ba(OH)₂·8H₂O + 2 NH₄Cl → BaCl₂ + 2 NH₃↑ + 10 H₂O", "Acido-base (reazione endotermica spontanea)",
       "Si libera ammoniaca e si forma acqua liquida da due solidi; la temperatura scende sotto 0 °C, tanto che il "
       "recipiente posato su una tavoletta bagnata resta incollato dal ghiaccio.",
       "È endotermica (assorbe calore) eppure avviene da sola, perché il disordine aumenta molto: da due solidi si "
       "passa a un liquido e a un gas. Quindi ΔG = ΔH − TΔS è negativo grazie al grande ΔS: è l'esempio classico "
       "per spiegare l'entropia. Principio simile al ghiaccio istantaneo (lì con nitrato di ammonio e acqua).",
       "agitando insieme i due solidi"),
    _r(["CaC₂ (carburo di calcio)", "H₂O (acqua)"], ["Ca(OH)₂", "C₂H₂ ↑ (acetilene)"],
       "CaC₂ + 2 H₂O → Ca(OH)₂ + C₂H₂↑", "Idrolisi (carburo di calcio)",
       "Si libera acetilene, gas che brucia con una fiamma molto luminosa (odore agliaceo dovuto alle impurezze).",
       "Lo ione acetiluro C₂²⁻ è una base fortissima: strappa due H⁺ all'acqua e diventa acetilene. Era la luce "
       "delle lampade a carburo di minatori e speleologi, e così si produce ancora acetilene per la saldatura.",
       None),
    _r(["Mg₃N₂ (nitruro di magnesio)", "H₂O (acqua)"], ["Mg(OH)₂", "NH₃ ↑"],
       "Mg₃N₂ + 6 H₂O → 3 Mg(OH)₂ + 2 NH₃↑", "Idrolisi (nitruro)",
       "Si libera ammoniaca (odore pungente) e resta idrossido di magnesio bianco.",
       "Lo ione nitruro N³⁻ è una base fortissima e prende tre H⁺ dall'acqua diventando ammoniaca; nessun numero "
       "di ossidazione cambia. È il modo per dimostrare che, bruciando all'aria, il magnesio ha reagito anche con "
       "l'azoto.",
       None),
    # --- Precipitazioni ---------------------------------------------------------------------------------
    _r(["AgNO₃ (nitrato d'argento)", "KBr (bromuro di potassio)"], ["AgBr ↓ (bromuro d'argento)", "KNO₃"],
       "AgNO₃ + KBr → AgBr↓ + KNO₃", "Precipitazione (doppio scambio)",
       "Precipita bromuro d'argento, color crema (giallo pallido), che alla luce scurisce.",
       "Ag⁺ + Br⁻ → AgBr, molto poco solubile: è il saggio dei bromuri. Il bromuro d'argento è sensibile alla "
       "luce (si decompone liberando argento nero): era la base delle pellicole fotografiche e delle lastre "
       "radiografiche.",
       None),
    _r(["AgNO₃ (nitrato d'argento)", "KI (ioduro di potassio)"], ["AgI ↓ (ioduro d'argento)", "KNO₃"],
       "AgNO₃ + KI → AgI↓ + KNO₃", "Precipitazione (doppio scambio)",
       "Precipita ioduro d'argento, giallo.",
       "Ag⁺ + I⁻ → AgI, il meno solubile degli alogenuri d'argento. Si distingue da AgCl perché non si scioglie "
       "in ammoniaca. Lo ioduro d'argento si disperde nelle nubi per far cadere pioggia o neve (inseminazione "
       "delle nuvole), perché i suoi cristalli somigliano a quelli del ghiaccio.",
       None),
    _r(["BaCl₂ (cloruro di bario)", "H₂SO₄ (acido solforico)"], ["BaSO₄ ↓ (solfato di bario)", "HCl"],
       "BaCl₂ + H₂SO₄ → BaSO₄↓ + 2 HCl", "Precipitazione (doppio scambio)",
       "Precipita solfato di bario, bianco e finissimo; resta acido cloridrico in soluzione.",
       "Ba²⁺ + SO₄²⁻ → BaSO₄, praticamente insolubile anche in acido. Gli ioni bario sono tossici, ma il solfato è "
       "così insolubile da non essere assorbito: per questo si beve come «pasto baritato», mezzo di contrasto per "
       "le radiografie di esofago, stomaco e intestino.",
       None),
    _r(["Pb(NO₃)₂ (nitrato di piombo)", "NaCl (cloruro di sodio)"], ["PbCl₂ ↓ (cloruro di piombo)", "NaNO₃"],
       "Pb(NO₃)₂ + 2 NaCl → PbCl₂↓ + 2 NaNO₃", "Precipitazione (doppio scambio)",
       "Precipita cloruro di piombo, bianco; scaldando si scioglie e raffreddando ricristallizza in aghi lucenti.",
       "Pb²⁺ + 2 Cl⁻ → PbCl₂. La sua solubilità cresce molto con la temperatura, e nell'analisi qualitativa questo "
       "permette di separarlo da AgCl, che resta insolubile anche a caldo.",
       None),
    _r(["AgNO₃ (nitrato d'argento)", "K₂CrO₄ (cromato di potassio)"], ["Ag₂CrO₄ ↓ (cromato d'argento)", "KNO₃"],
       "2 AgNO₃ + K₂CrO₄ → Ag₂CrO₄↓ + 2 KNO₃", "Precipitazione (doppio scambio)",
       "Precipita cromato d'argento, rosso mattone.",
       "2 Ag⁺ + CrO₄²⁻ → Ag₂CrO₄. Nel metodo di Mohr (titolazione dei cloruri, per esempio nell'acqua o nel "
       "sangue) il cromato fa da indicatore: precipita rosso solo quando tutto il cloruro è già precipitato come "
       "AgCl bianco.",
       None),
    _r(["FeSO₄ (solfato ferroso)", "NaOH (idrossido di sodio)"], ["Fe(OH)₂ ↓ (idrossido ferroso)", "Na₂SO₄"],
       "FeSO₄ + 2 NaOH → Fe(OH)₂↓ + Na₂SO₄", "Precipitazione",
       "Precipita idrossido ferroso, verde sporco, che all'aria diventa lentamente rosso-bruno.",
       "Fe²⁺ + 2 OH⁻ → Fe(OH)₂. All'aria l'ossigeno ossida il ferro da +2 a +3 e si forma Fe(OH)₃ rosso-bruno. "
       "Il colore del precipitato permette di distinguere i sali ferrosi (verde) da quelli ferrici (bruno).",
       None),
    _r(["MgCl₂ (cloruro di magnesio)", "NaOH (idrossido di sodio)"], ["Mg(OH)₂ ↓ (idrossido di magnesio)", "NaCl"],
       "MgCl₂ + 2 NaOH → Mg(OH)₂↓ + 2 NaCl", "Precipitazione",
       "Precipita idrossido di magnesio, bianco.",
       "Mg²⁺ + 2 OH⁻ → Mg(OH)₂, poco solubile. È la prima tappa per estrarre il magnesio dall'acqua di mare "
       "(industrialmente con la calce, più economica); lo stesso idrossido è il «latte di magnesia», antiacido e "
       "lassativo.",
       None),
    _r(["AlCl₃ (cloruro di alluminio)", "NaOH (idrossido di sodio)"], ["Al(OH)₃ ↓ (idrossido di alluminio)", "NaCl"],
       "AlCl₃ + 3 NaOH → Al(OH)₃↓ + 3 NaCl", "Precipitazione",
       "Precipita idrossido di alluminio, bianco e gelatinoso, che si ridiscioglie se si aggiunge altra soda.",
       "Al³⁺ + 3 OH⁻ → Al(OH)₃. In eccesso di base il precipitato si scioglie perché l'idrossido è anfotero e "
       "forma lo ione alluminato. Il precipitato gelatinoso intrappola le particelle sospese: i sali di alluminio "
       "si usano per chiarificare l'acqua potabile.",
       None),
    _r(["CaCl₂ (cloruro di calcio)", "Na₃PO₄ (fosfato di sodio)"], ["Ca₃(PO₄)₂ ↓ (fosfato di calcio)", "NaCl"],
       "3 CaCl₂ + 2 Na₃PO₄ → Ca₃(PO₄)₂↓ + 6 NaCl", "Precipitazione",
       "Precipita fosfato di calcio, bianco.",
       "3 Ca²⁺ + 2 PO₄³⁻ → Ca₃(PO₄)₂, insolubile. I fosfati di calcio (idrossiapatite) sono il minerale di ossa e "
       "denti; i fosfati nei detersivi servivano a togliere il calcio dell'acqua dura, ma sono stati limitati "
       "perché causano l'eutrofizzazione di laghi e fiumi.",
       None),
    _r(["Ca(OH)₂ (idrossido di calcio)", "Na₂CO₃ (carbonato di sodio)"], ["CaCO₃ ↓", "NaOH (idrossido di sodio)"],
       "Ca(OH)₂ + Na₂CO₃ → CaCO₃↓ + 2 NaOH", "Precipitazione (caustificazione)",
       "Precipita carbonato di calcio, bianco; in soluzione resta soda caustica.",
       "Ca²⁺ + CO₃²⁻ → CaCO₃: il carbonato insolubile si separa e lascia NaOH. Questa «caustificazione» è stata per "
       "secoli il modo di produrre soda caustica e si usa ancora nelle cartiere per recuperare la soda.",
       None),
    # --- Decomposizioni ---------------------------------------------------------------------------------
    _r(["KClO₃ (clorato di potassio, riscaldato)"], ["KCl (cloruro di potassio)", "O₂ ↑"],
       "2 KClO₃ → 2 KCl + 3 O₂↑", "Decomposizione termica (ossidoriduzione interna)",
       "Si libera ossigeno: una scheggia di legno con la brace si riaccende.",
       "Nello stesso composto il cloro si riduce (da +5 a −1) e l'ossigeno si ossida (da −2 a 0). È un metodo "
       "classico per preparare ossigeno in laboratorio; il biossido di manganese fa da catalizzatore e abbassa la "
       "temperatura necessaria. Il clorato è anche nella capocchia dei fiammiferi.",
       "riscaldamento, catalizzatore MnO₂"),
    _r(["NaHCO₃ (bicarbonato di sodio, riscaldato)"], ["Na₂CO₃ (carbonato di sodio)", "H₂O", "CO₂ ↑"],
       "2 NaHCO₃ → Na₂CO₃ + H₂O + CO₂↑", "Decomposizione termica",
       "Si liberano anidride carbonica e vapore acqueo.",
       "Scaldando, due ioni bicarbonato si scambiano un H⁺: uno diventa carbonato, l'altro acido carbonico che si "
       "decompone; nessun numero di ossidazione cambia. È la CO₂ che fa gonfiare i dolci con il bicarbonato in "
       "forno, ed è il principio degli estintori a polvere.",
       "sopra ≈ 80 °C"),
    _r(["HgO (ossido di mercurio, riscaldato)"], ["Hg (mercurio)", "O₂ ↑"],
       "2 HgO → 2 Hg + O₂↑", "Decomposizione termica (ossidoriduzione interna)",
       "Si libera ossigeno; la polvere rossa scompare e sulle pareti fredde si condensano goccioline di mercurio.",
       "Il mercurio si riduce (da +2 a 0) e l'ossigeno si ossida (da −2 a 0). Con questa reazione Priestley "
       "scoprì l'ossigeno nel 1774 e Lavoisier ne capì il ruolo nelle combustioni. Oggi non si fa più a scuola "
       "perché i vapori di mercurio sono tossici.",
       "riscaldamento sopra ≈ 450 °C"),
    _r(["Cu(OH)₂ (idrossido di rame, riscaldato)"], ["CuO (ossido di rame)", "H₂O"],
       "Cu(OH)₂ → CuO + H₂O", "Decomposizione termica (disidratazione)",
       "Si libera vapore acqueo; il precipitato azzurro diventa nero.",
       "L'idrossido perde una molecola d'acqua e diventa ossido; il rame resta +2. Il cambio di colore da azzurro "
       "a nero si vede anche scaldando la provetta del saggio del rame con la soda.",
       "riscaldamento (anche solo a bagnomaria)"),
    _r(["NH₄NO₃ (nitrato di ammonio, riscaldato)"], ["N₂O ↑ (protossido di azoto)", "H₂O"],
       "NH₄NO₃ → N₂O↑ + 2 H₂O", "Decomposizione termica (ossidoriduzione interna)",
       "Si libera protossido di azoto, gas incolore dall'odore dolciastro, e vapore acqueo.",
       "Nello stesso sale l'azoto dello ione ammonio si ossida (da −3 a +1) e quello del nitrato si riduce (da +5 "
       "a +1): è una comproporzione. Il protossido di azoto è il «gas esilarante», usato come anestetico in "
       "odontoiatria e come propellente della panna spray. Scaldando troppo il nitrato può esplodere.",
       "riscaldamento cauto, ≈ 200-250 °C"),
    _r(["(NH₄)₂Cr₂O₇ (dicromato di ammonio, riscaldato)"], ["Cr₂O₃ (ossido di cromo)", "N₂ ↑", "H₂O"],
       "(NH₄)₂Cr₂O₇ → Cr₂O₃ + N₂↑ + 4 H₂O", "Decomposizione termica (ossidoriduzione interna)",
       "Si liberano azoto e vapore acqueo con scintille; i cristalli arancioni diventano una «cenere» verde "
       "voluminosa: è il «vulcano chimico».",
       "L'azoto si ossida (da −3 a 0) e il cromo si riduce (da +6 a +3) nello stesso composto. Il dicromato è "
       "tossico e cancerogeno: l'esperimento si fa solo sotto cappa. L'ossido di cromo verde è un pigmento "
       "molto stabile (verde delle banconote e delle vernici).",
       "innesco con una fiamma"),
    _r(["CuSO₄·5H₂O (solfato di rame pentaidrato, riscaldato)"], ["CuSO₄ (solfato di rame anidro)", "H₂O ↑"],
       "CuSO₄·5H₂O → CuSO₄ + 5 H₂O", "Decomposizione (disidratazione di un idrato)",
       "Si libera vapore acqueo; i cristalli blu diventano una polvere bianca.",
       "L'acqua di cristallizzazione, legata agli ioni rame, se ne va scaldando; il blu è dovuto proprio all'acqua "
       "legata al Cu²⁺. Aggiungendo acqua alla polvere bianca torna il blu e si scalda: è un test per riconoscere "
       "l'acqua.",
       "riscaldamento sopra ≈ 150 °C"),
    _r(["H₂O₂ (acqua ossigenata)", "KI (ioduro di potassio)"], ["H₂O", "O₂ ↑"],
       "2 H₂O₂ → 2 H₂O + O₂↑", "Decomposizione catalitica («dentifricio dell'elefante»)",
       "Si libera ossigeno velocissimamente; con un po' di detersivo si forma una colonna di schiuma calda, gialla "
       "per un po' di iodio.",
       "L'ossigeno dell'acqua ossigenata (−1) in parte si ossida a 0 e in parte si riduce a −2 (disproporzione). "
       "Lo ioduro è un catalizzatore: reagisce con H₂O₂ e si riforma, quindi non si consuma e non compare "
       "nell'equazione. È lo stesso lavoro che fa l'enzima catalasi nelle cellule.",
       "KI come catalizzatore, acqua ossigenata concentrata, detersivo per la schiuma"),
    # --- Combustioni ------------------------------------------------------------------------------------
    _r(["C₂H₆ (etano)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "2 C₂H₆ + 7 O₂ → 4 CO₂ + 6 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo; molto calore.",
       "Il carbonio si ossida (da −3 a +4) e l'ossigeno si riduce (da 0 a −2). Per bilanciare si parte da C e H; "
       "l'ossigeno viene 7/2, quindi si raddoppia tutto per avere coefficienti interi. L'etano è il secondo "
       "componente del gas naturale.",
       "accensione"),
    _r(["C₄H₁₀ (butano)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "2 C₄H₁₀ + 13 O₂ → 8 CO₂ + 10 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo; fiamma azzurra se l'aria è sufficiente, gialla e fumosa se manca.",
       "Il carbonio si ossida (da una media di −2,5 a +4) e l'ossigeno si riduce. Il butano è il gas degli "
       "accendini e delle bombole da campeggio (GPL insieme al propano). Con poca aria si forma anche CO, per "
       "questo le stufe a gas vanno usate in ambienti ventilati.",
       "accensione"),
    _r(["C₈H₁₈ (ottano)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "2 C₈H₁₈ + 25 O₂ → 16 CO₂ + 18 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo che escono dal tubo di scappamento; molto calore.",
       "Il carbonio si ossida (da una media di −2,25 a +4) e l'ossigeno si riduce. L'ottano rappresenta la "
       "benzina: il «numero di ottano» misura quanto un carburante resiste all'autoaccensione (battito in testa) "
       "nel motore. Ogni litro di benzina bruciato produce più di 2 kg di CO₂.",
       "scintilla della candela nel motore"),
    _r(["CH₃OH (metanolo)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "2 CH₃OH + 3 O₂ → 2 CO₂ + 4 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo; la fiamma è azzurra e quasi invisibile alla luce del giorno.",
       "Il carbonio si ossida (da −2 a +4) e l'ossigeno si riduce. Il metanolo si usa come combustibile per "
       "modellini e nelle celle a combustibile a metanolo. Attenzione: bevuto è molto tossico (può causare "
       "cecità), per questo si distingue dall'etanolo.",
       "accensione"),
    _r(["Saccarosio", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "C₁₂H₂₂O₁₁ + 12 O₂ → 12 CO₂ + 11 H₂O", "Combustione (di uno zucchero)",
       "Anidride carbonica e vapore acqueo; lo zucchero fonde, caramella, annerisce e brucia.",
       "Il carbonio si ossida (da 0 a +4) e l'ossigeno si riduce (da 0 a −2). Le cellule ottengono lo stesso "
       "risultato complessivo con la respirazione cellulare, ma a piccoli passi e immagazzinando l'energia "
       "nell'ATP invece di disperderla come calore. Con la combustione nella bomba calorimetrica si misurano le "
       "calorie degli alimenti (circa 4 kcal per grammo di zucchero).",
       "accensione (con un po' di cenere come catalizzatore)"),
    _r(["C₂H₂ (acetilene)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "2 C₂H₂ + 5 O₂ → 4 CO₂ + 2 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo; fiamma bianchissima che con ossigeno puro supera i 3000 °C.",
       "Il carbonio si ossida (da −1 a +4) e l'ossigeno si riduce. Il cannello ossiacetilenico usa questa "
       "fiamma per saldare e tagliare l'acciaio. Con poca aria brucia con fiamma fuligginosa, perché l'acetilene "
       "contiene molto carbonio.",
       "accensione; con ossigeno puro nel cannello"),
    _r(["CO (monossido di carbonio)", "O₂ (ossigeno)"], ["CO₂ ↑"],
       "2 CO + O₂ → 2 CO₂", "Combustione (ossidazione catalitica)",
       "Si forma anidride carbonica; il CO brucia con una fiamma azzurra.",
       "Il carbonio si ossida (da +2 a +4) e l'ossigeno si riduce. È una delle reazioni della marmitta catalitica "
       "(platino, palladio): trasforma il CO tossico in CO₂. La fiamma azzurra sopra le braci è proprio CO che "
       "brucia.",
       "accensione, oppure catalizzatore Pt/Pd nella marmitta"),
    _r(["C₂₅H₅₂ (paraffina, cera di candela)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "C₂₅H₅₂ + 38 O₂ → 25 CO₂ + 26 H₂O", "Combustione",
       "Anidride carbonica e vapore acqueo (su un vetro freddo sopra la fiamma si appanna); la parte gialla della "
       "fiamma è fuliggine incandescente.",
       "Il carbonio si ossida e l'ossigeno si riduce. Non brucia la cera solida: il calore la fonde, lo stoppino "
       "la fa risalire e la vaporizza, ed è il vapore a bruciare. Coprendo la candela con un bicchiere la fiamma "
       "si spegne quando l'ossigeno finisce.",
       "stoppino acceso"),
    _r(["C₁₆H₃₂O₂ (acido palmitico)", "O₂ (ossigeno)"], ["CO₂ ↑", "H₂O"],
       "C₁₆H₃₂O₂ + 23 O₂ → 16 CO₂ + 16 H₂O", "Combustione (ossidazione completa di un acido grasso)",
       "Anidride carbonica e acqua; nelle cellule l'energia va nell'ATP (circa 106 ATP per molecola).",
       "Nel corpo avviene a tappe: β-ossidazione nei mitocondri (che stacca 2 carboni alla volta come acetil-CoA), "
       "poi ciclo di Krebs e catena respiratoria. I grassi rendono circa 9 kcal per grammo, più del doppio degli "
       "zuccheri, perché i loro carboni sono più ridotti e possono cedere più elettroni.",
       "nelle cellule: enzimi mitocondriali"),
    _r(["NO (monossido di azoto)", "O₂ (ossigeno)"], ["NO₂ (biossido di azoto)"],
       "2 NO + O₂ → 2 NO₂", "Sintesi (ossidazione)",
       "Niente si libera: il gas incolore diventa rosso-bruno.",
       "L'azoto si ossida (da +2 a +4) e l'ossigeno si riduce (da 0 a −2). Avviene spontaneamente all'aria: per "
       "questo i gas di scarico e lo smog urbano hanno una sfumatura bruna. È anche una tappa del processo Ostwald "
       "per l'acido nitrico.",
       None),
    _r(["O₂ (ossigeno, con raggi UV o scariche elettriche)"], ["O₃ (ozono)"],
       "3 O₂ → 2 O₃", "Sintesi (formazione dell'ozono)",
       "Niente si libera: si forma ozono, un gas dall'odore pungente (quello che si sente dopo i temporali o "
       "vicino alle fotocopiatrici).",
       "I raggi UV o le scariche spezzano O₂ in atomi di ossigeno, che si uniscono ad altre molecole di O₂; non "
       "c'è variazione del numero di ossidazione (è una allotropia). Nella stratosfera lo strato di ozono assorbe "
       "gli UV pericolosi; vicino al suolo, invece, l'ozono è un inquinante irritante.",
       "raggi ultravioletti o scariche elettriche"),
    _r(["CO₂ (anidride carbonica)", "C (carbonio)"], ["CO (monossido di carbonio)"],
       "CO₂ + C ⇌ 2 CO", "Ossidoriduzione (comproporzione, equilibrio di Boudouard)",
       "Niente: si forma monossido di carbonio, gas tossico.",
       "Il carbonio elementare si ossida (da 0 a +2) e quello della CO₂ si riduce (da +4 a +2): entrambi arrivano "
       "a +2. È endotermica, quindi favorita ad alta temperatura: nell'altoforno rigenera il CO che riduce il "
       "minerale di ferro.",
       "sopra ≈ 700-1000 °C (carbone incandescente)"),
    _r(["C (carbonio)", "H₂O (vapore)"], ["CO (monossido di carbonio)", "H₂ (idrogeno)"],
       "C + H₂O ⇌ CO + H₂", "Ossidoriduzione (gas d'acqua)",
       "Niente si allontana: si forma una miscela combustibile di CO e H₂ (gas d'acqua).",
       "Il carbonio si ossida (da 0 a +2) e l'idrogeno si riduce (da +1 a 0). È endotermica: soffiando vapore sul "
       "carbone rovente quest'ultimo si raffredda. Prima del metano si produceva così il «gas di città» per le "
       "cucine; oggi la gassificazione del carbone fornisce gas di sintesi per l'industria.",
       "carbone incandescente, ≈ 1000 °C"),
    _r(["CO (monossido di carbonio)", "H₂ (idrogeno)"], ["CH₃OH (metanolo)"],
       "CO + 2 H₂ ⇌ CH₃OH", "Sintesi (equilibrio, produzione del metanolo)",
       "Niente: il metanolo si separa condensandolo.",
       "Il carbonio si riduce (da +2 a −2) e l'idrogeno si ossida (da 0 a +1). Come la sintesi dell'ammoniaca è "
       "esotermica e diminuisce le moli di gas (3 → 1): la pressione alta sposta l'equilibrio verso il metanolo. "
       "Il metanolo è una materia prima chimica (formaldeide, plastiche) e un possibile combustibile.",
       "≈ 250 °C, 50-100 bar, catalizzatore Cu/ZnO/Al₂O₃"),
    _r(["NH₃ (ammoniaca)", "CO₂ (anidride carbonica)"], ["CO(NH₂)₂ (urea)", "H₂O"],
       "2 NH₃ + CO₂ → CO(NH₂)₂ + H₂O", "Sintesi (urea, processo Bosch-Meiser)",
       "Si forma acqua; l'urea si ottiene come solido bianco.",
       "Prima si forma carbammato di ammonio, che poi perde acqua; non c'è ossidoriduzione. L'urea è il "
       "fertilizzante azotato più prodotto al mondo e si usa nell'AdBlue dei motori diesel. Nel 1828 Wöhler la "
       "sintetizzò da sostanze inorganiche, dimostrando che le molecole «degli esseri viventi» si possono fare in "
       "laboratorio.",
       "≈ 180-190 °C, ≈ 150 bar"),
    # --- Ossidoriduzioni famose ---------------------------------------------------------------------------
    _r(["KMnO₄ (permanganato di potassio)", "FeSO₄ (solfato ferroso)"],
       ["K₂SO₄", "MnSO₄ (solfato di manganese)", "Fe₂(SO₄)₃ (solfato ferrico)", "H₂O"],
       "2 KMnO₄ + 10 FeSO₄ + 8 H₂SO₄ → K₂SO₄ + 2 MnSO₄ + 5 Fe₂(SO₄)₃ + 8 H₂O", "Ossidoriduzione (in ambiente acido)",
       "Niente gas: il viola del permanganato scompare goccia dopo goccia; quando tutto il ferro(II) è ossidato la "
       "prima goccia in più resta rosa.",
       "Il manganese si riduce (da +7 a +2, acquista 5 elettroni) e il ferro si ossida (da +2 a +3, ne cede 1): "
       "per questo un MnO₄⁻ ossida 5 Fe²⁺. È la permanganometria, titolazione che non ha bisogno di indicatore "
       "perché il permanganato si colora da solo; si usa per dosare il ferro, per esempio negli integratori.",
       "ambiente acido per acido solforico"),
    _r(["KMnO₄ (permanganato di potassio)", "H₂O₂ (acqua ossigenata)"],
       ["K₂SO₄", "MnSO₄ (solfato di manganese)", "O₂ ↑", "H₂O"],
       "2 KMnO₄ + 5 H₂O₂ + 3 H₂SO₄ → K₂SO₄ + 2 MnSO₄ + 5 O₂↑ + 8 H₂O", "Ossidoriduzione (in ambiente acido)",
       "Si libera ossigeno (bollicine) e la soluzione viola si decolora.",
       "Il manganese si riduce (da +7 a +2) e l'ossigeno dell'acqua ossigenata si ossida (da −1 a 0): qui H₂O₂ fa "
       "da riducente. 2 MnO₄⁻ acquistano 10 elettroni, che 5 H₂O₂ cedono. Si usa per misurare la concentrazione "
       "dell'acqua ossigenata, per esempio quella venduta in farmacia.",
       "ambiente acido per acido solforico"),
    _r(["KMnO₄ (permanganato di potassio)", "HCl (acido cloridrico)"],
       ["KCl", "MnCl₂ (cloruro di manganese)", "Cl₂ ↑", "H₂O"],
       "2 KMnO₄ + 16 HCl → 2 KCl + 2 MnCl₂ + 5 Cl₂↑ + 8 H₂O", "Ossidoriduzione",
       "Si libera cloro, gas verde-giallo dall'odore soffocante; il viola scompare.",
       "Il manganese si riduce (da +7 a +2) e il cloro si ossida (da −1 a 0). Dei 16 HCl solo 10 si ossidano a "
       "Cl₂; gli altri 6 forniscono i cloruri dei sali e l'ambiente acido. È un metodo di laboratorio per "
       "preparare piccole quantità di cloro, sotto cappa.",
       "acido concentrato, sotto cappa"),
    _r(["K₂Cr₂O₇ (dicromato di potassio)", "C₂H₅OH (etanolo)"],
       ["K₂SO₄", "Cr₂(SO₄)₃ (solfato di cromo)", "CH₃COOH (acido acetico)", "H₂O"],
       "2 K₂Cr₂O₇ + 3 C₂H₅OH + 8 H₂SO₄ → 2 K₂SO₄ + 2 Cr₂(SO₄)₃ + 3 CH₃COOH + 11 H₂O",
       "Ossidoriduzione (ossidazione di un alcol, etilometro)",
       "Niente gas: la soluzione arancione diventa verde.",
       "Il cromo si riduce (da +6 a +3) e il carbonio dell'alcol si ossida (da −1 a +3): l'etanolo diventa acido "
       "acetico. Il cambio di colore da arancione (Cr₂O₇²⁻) a verde (Cr³⁺) era il principio dei vecchi "
       "etilometri a fialetta; oggi si usano sensori elettrochimici o all'infrarosso.",
       "ambiente acido per acido solforico"),
    _r(["Al (alluminio)", "Fe₂O₃ (ossido ferrico, ruggine)"], ["Al₂O₃ (ossido di alluminio)", "Fe (ferro fuso)"],
       "2 Al + Fe₂O₃ → Al₂O₃ + 2 Fe", "Ossidoriduzione (alluminotermia, termite)",
       "Niente gas: pioggia di scintille e luce accecante; cola ferro fuso, oltre 2500 °C.",
       "L'alluminio si ossida (da 0 a +3) e il ferro si riduce (da +3 a 0). L'alluminio ha una affinità per "
       "l'ossigeno molto maggiore del ferro, e la reazione libera un calore enorme (ΔH ≈ −850 kJ). Si usa per "
       "saldare le rotaie dei binari sul posto e, in passato, nelle bombe incendiarie.",
       "innesco con un nastro di magnesio acceso"),
    _r(["Fe₂O₃ (ossido ferrico, ruggine)", "CO (monossido di carbonio)"], ["Fe (ferro)", "CO₂ ↑"],
       "Fe₂O₃ + 3 CO → 2 Fe + 3 CO₂↑", "Ossidoriduzione (altoforno)",
       "Esce anidride carbonica con i gas dell'altoforno; il ferro fuso (ghisa) cola sul fondo.",
       "Il ferro si riduce (da +3 a 0) e il carbonio si ossida (da +2 a +4). Il CO viene dal coke che brucia con "
       "poca aria nel fondo dell'altoforno. È la reazione principale della siderurgia: produce la ghisa, che poi "
       "diventa acciaio togliendo parte del carbonio.",
       "altoforno, ≈ 800-1500 °C"),
    _r(["CuO (ossido di rame)", "H₂ (idrogeno)"], ["Cu (rame)", "H₂O"],
       "CuO + H₂ → Cu + H₂O", "Ossidoriduzione (riduzione di un ossido)",
       "Si forma vapore acqueo, che si condensa in goccioline; la polvere nera diventa rame rosso lucente.",
       "Il rame si riduce (da +2 a 0) e l'idrogeno si ossida (da 0 a +1). È l'esperimento classico per mostrare "
       "che l'idrogeno è un riducente e per trovare la formula dell'ossido pesando prima e dopo. Molti metalli "
       "puri si ottengono riducendo gli ossidi con idrogeno o carbonio.",
       "riscaldamento in corrente di idrogeno"),
    _r(["SO₂ (anidride solforosa)", "H₂S (acido solfidrico)"], ["S ↓ (zolfo)", "H₂O"],
       "SO₂ + 2 H₂S → 3 S↓ + 2 H₂O", "Ossidoriduzione (comproporzione, processo Claus)",
       "Si deposita zolfo giallo e si forma acqua.",
       "Lo zolfo dell'SO₂ si riduce (da +4 a 0) e quello dell'H₂S si ossida (da −2 a 0): due stati diversi dello "
       "stesso elemento arrivano allo stesso valore (comproporzione). Il processo Claus toglie l'H₂S dal gas "
       "naturale e dal petrolio, e oggi è la principale fonte di zolfo; avviene anche nei vulcani.",
       "≈ 200-300 °C, catalizzatore di allumina"),
    _r(["FeCl₃ (cloruro ferrico)", "KI (ioduro di potassio)"], ["FeCl₂ (cloruro ferroso)", "I₂ (iodio)", "KCl"],
       "2 FeCl₃ + 2 KI → 2 FeCl₂ + I₂ + 2 KCl", "Ossidoriduzione",
       "Niente gas: la soluzione diventa bruna per lo iodio che si forma (blu-nera con l'amido).",
       "Il ferro si riduce (da +3 a +2) e lo ioduro si ossida (da −1 a 0). Avviene perché la coppia Fe³⁺/Fe²⁺ "
       "(+0,77 V) è più ossidante della coppia I₂/I⁻ (+0,54 V). Mostra che uno ione metallico può fare da "
       "ossidante.",
       None),
    _r(["Na₂S₂O₃ (tiosolfato di sodio)", "I₂ (iodio)"], ["Na₂S₄O₆ (tetrationato di sodio)", "NaI (ioduro di sodio)"],
       "2 Na₂S₂O₃ + I₂ → Na₂S₄O₆ + 2 NaI", "Ossidoriduzione (iodometria)",
       "Niente gas: il colore bruno dello iodio scompare; con l'amido il blu scuro diventa incolore di colpo.",
       "Lo iodio si riduce (da 0 a −1) e lo zolfo si ossida (da +2 a +2,5 in media nel tetrationato). È la "
       "reazione dell'iodometria, usata per dosare il cloro attivo nella candeggina, la vitamina C e l'ossigeno "
       "disciolto nell'acqua. Il tiosolfato serve anche a togliere il cloro dall'acqua degli acquari.",
       None),
    _r(["MnO₂ (biossido di manganese)", "HCl (acido cloridrico)"], ["MnCl₂ (cloruro di manganese)", "Cl₂ ↑", "H₂O"],
       "MnO₂ + 4 HCl → MnCl₂ + Cl₂↑ + 2 H₂O", "Ossidoriduzione",
       "Si libera cloro, gas verde-giallo soffocante.",
       "Il manganese si riduce (da +4 a +2) e metà del cloro si ossida (da −1 a 0); l'altra metà resta come "
       "cloruro. Con questa reazione Scheele scoprì il cloro nel 1774, e per un secolo fu il modo di produrlo per "
       "sbiancare i tessuti.",
       "acido concentrato e caldo, sotto cappa"),
    _r(["Cu (rame)", "FeCl₃ (cloruro ferrico)"], ["CuCl₂ (cloruro rameico)", "FeCl₂ (cloruro ferroso)"],
       "Cu + 2 FeCl₃ → CuCl₂ + 2 FeCl₂", "Ossidoriduzione",
       "Niente gas: il rame si scioglie e la soluzione bruna diventa verde scura.",
       "Il rame si ossida (da 0 a +2) e il ferro si riduce (da +3 a +2). Il rame non reagisce con gli acidi non "
       "ossidanti, ma Fe³⁺ è un ossidante abbastanza forte. È così che si incidono i circuiti stampati: le piste "
       "sono protette da una vernice, il rame scoperto si scioglie.",
       None),
    _r(["NaClO (ipoclorito di sodio, candeggina)", "HCl (acido cloridrico)"], ["NaCl", "Cl₂ ↑", "H₂O"],
       "NaClO + 2 HCl → NaCl + Cl₂↑ + H₂O", "Ossidoriduzione (comproporzione)",
       "Si libera cloro, gas verde-giallo tossico che irrita occhi e polmoni.",
       "Il cloro dell'ipoclorito si riduce (da +1 a 0) e quello dell'acido si ossida (da −1 a 0). È il motivo per "
       "cui la candeggina non va MAI mescolata con prodotti acidi (anticalcare, acido muriatico, alcuni "
       "detersivi per il WC): in casa si possono liberare quantità pericolose di cloro.",
       None),
    _r(["NaCl (fuso, elettrolisi)"], ["Na (sodio)", "Cl₂ ↑"],
       "2 NaCl → 2 Na + Cl₂↑", "Elettrolisi (cella di Downs)",
       "Cloro gassoso all'anodo; sodio metallico fuso al catodo, che galleggia e si raccoglie.",
       "Catodo: Na⁺ + e⁻ → Na (riduzione). Anodo: 2 Cl⁻ → Cl₂ + 2 e⁻ (ossidazione). Serve il sale fuso e non "
       "sciolto in acqua: in soluzione al catodo si riduce l'acqua e si forma idrogeno invece di sodio. Si aggiunge "
       "CaCl₂ per abbassare la temperatura di fusione.",
       "NaCl fuso, ≈ 600 °C, corrente continua"),
    _r(["Al₂O₃ (ossido di alluminio)", "C (carbonio)"], ["Al (alluminio)", "CO₂ ↑"],
       "2 Al₂O₃ + 3 C → 4 Al + 3 CO₂↑", "Elettrolisi (processo Hall-Héroult)",
       "Anidride carbonica all'anodo di carbonio, che si consuma; l'alluminio fuso si raccoglie sul fondo.",
       "L'alluminio si riduce (da +3 a 0) al catodo, mentre all'anodo l'ossigeno si ossida e brucia il carbonio "
       "dell'elettrodo. L'allumina è sciolta nella criolite fusa, che abbassa la temperatura di fusione da oltre "
       "2000 °C a circa 950 °C. Consuma moltissima elettricità: per questo riciclare l'alluminio fa risparmiare "
       "circa il 95% dell'energia.",
       "≈ 950-980 °C, allumina sciolta in criolite fusa, corrente continua"),
    # --- Chimica organica --------------------------------------------------------------------------------
    _r(["CH₄ (metano)", "Cl₂ (cloro)"], ["CH₃Cl (clorometano)", "HCl ↑"],
       "CH₄ + Cl₂ → CH₃Cl + HCl", "Sostituzione radicalica (alogenazione degli alcani)",
       "Si forma cloruro di idrogeno gassoso; il colore verde-giallo del cloro sparisce.",
       "La luce rompe Cl₂ in due radicali Cl·, che strappano un H al metano e avviano una reazione a catena; un "
       "atomo di H viene sostituito da un Cl. Con più cloro la sostituzione continua (CH₂Cl₂, CHCl₃, CCl₄). Gli "
       "alcani, poco reattivi, reagiscono così, e non per addizione come gli alcheni.",
       "luce ultravioletta"),
    _r(["C₂H₄ (etilene)", "Cl₂ (cloro)"], ["C₂H₄Cl₂ (1,2-dicloroetano)"],
       "C₂H₄ + Cl₂ → CH₂Cl-CH₂Cl", "Addizione elettrofila (alogenazione)",
       "Niente: il colore del cloro scompare e si forma un liquido oleoso.",
       "Il doppio legame si apre e ogni carbonio lega un atomo di cloro. L'1,2-dicloroetano si trasforma in "
       "cloruro di vinile, da cui si fa il PVC (tubi, infissi, cavi): è una delle reazioni più importanti "
       "dell'industria chimica.",
       "catalizzatore FeCl₃, a temperatura moderata"),
    _r(["C₃H₆ (propene)", "HBr (acido bromidrico)"], ["CH₃CHBrCH₃ (2-bromopropano)"],
       "C₃H₆ + HBr → CH₃CHBrCH₃", "Addizione elettrofila (regola di Markovnikov)",
       "Niente gas: si forma un solo prodotto principale.",
       "L'H⁺ si lega al carbonio del doppio legame che ha già più idrogeni e il Br⁻ va sull'altro (regola di "
       "Markovnikov), perché così si forma il carbocatione più stabile, quello secondario. Si ottiene quindi "
       "2-bromopropano e non 1-bromopropano.",
       None),
    _r(["C₃H₆ (propene)", "H₂O (acqua)"], ["CH₃CH(OH)CH₃ (2-propanolo, alcol isopropilico)"],
       "C₃H₆ + H₂O → CH₃CH(OH)CH₃", "Addizione (idratazione, regola di Markovnikov)",
       "Niente: si forma alcol isopropilico.",
       "Il doppio legame si apre: l'H va sul carbonio terminale e l'OH su quello centrale (Markovnikov). "
       "L'alcol isopropilico è il disinfettante delle salviette e dei gel per le mani e si usa per pulire "
       "schermi ed elettronica.",
       "catalizzatore acido (H₂SO₄ o H₃PO₄)"),
    _r(["C₆H₆ (benzene)", "Br₂ (bromo)"], ["C₆H₅Br (bromobenzene)", "HBr ↑"],
       "C₆H₆ + Br₂ → C₆H₅Br + HBr", "Sostituzione elettrofila aromatica",
       "Si libera bromuro di idrogeno gassoso (fumi all'aria umida); il colore del bromo sparisce lentamente.",
       "A differenza degli alcheni, il benzene non decolora il bromo da solo: l'anello aromatico è molto stabile e "
       "preferisce sostituire un H piuttosto che rompere la delocalizzazione degli elettroni. Serve un "
       "catalizzatore (FeBr₃) che renda il bromo un elettrofilo più forte.",
       "catalizzatore FeBr₃ (o limatura di ferro)"),
    _r(["C₆H₆ (benzene)", "HNO₃ (acido nitrico)"], ["C₆H₅NO₂ (nitrobenzene)", "H₂O"],
       "C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O", "Sostituzione elettrofila aromatica (nitrazione)",
       "Si forma acqua; il nitrobenzene è un liquido giallo pallido con odore di mandorle amare.",
       "L'acido solforico trasforma l'acido nitrico nello ione nitronio NO₂⁺, l'elettrofilo che sostituisce un H "
       "sull'anello. Il nitrobenzene ridotto dà l'anilina, base dei coloranti e di molti farmaci (come il "
       "paracetamolo); con più gruppi nitro si arriva a esplosivi come il tritolo (TNT, partendo dal toluene).",
       "miscela solfonitrica (HNO₃ + H₂SO₄ concentrati), ≈ 50 °C"),
    _r(["CH₃COOH (acido acetico)", "CH₃OH (metanolo)"], ["CH₃COOCH₃ (acetato di metile)", "H₂O"],
       "CH₃COOH + CH₃OH ⇌ CH₃COOCH₃ + H₂O", "Esterificazione (condensazione)",
       "Si forma una molecola d'acqua; l'estere ha un odore dolciastro, simile a quello della colla.",
       "L'OH dell'acido e l'H dell'alcol escono come acqua e resta il legame estere. È un equilibrio (esterificazione "
       "di Fischer): con un eccesso di alcol o togliendo l'acqua si aumenta la resa. L'acetato di metile è un "
       "solvente di colle e vernici.",
       "acido solforico come catalizzatore, calore"),
    _r(["CH₃COOH (acido acetico)", "C₅H₁₁OH (alcol isoamilico)"], ["CH₃COOC₅H₁₁ (acetato di isoamile)", "H₂O"],
       "CH₃COOH + C₅H₁₁OH ⇌ CH₃COOC₅H₁₁ + H₂O", "Esterificazione (condensazione)",
       "Si forma una molecola d'acqua; l'estere ha un intenso profumo di banana.",
       "Come tutte le esterificazioni, l'acido e l'alcol si legano perdendo acqua. Molti profumi della frutta sono "
       "esteri: l'acetato di isoamile è l'aroma di banana (usato nelle caramelle), il butanoato di etile quello di "
       "ananas. È anche un feromone d'allarme delle api.",
       "acido solforico come catalizzatore, calore"),
    _r(["C₇H₆O₃ (acido salicilico)", "(CH₃CO)₂O (anidride acetica)"],
       ["C₉H₈O₄ (acido acetilsalicilico, aspirina)", "CH₃COOH (acido acetico)"],
       "C₇H₆O₃ + C₄H₆O₃ → C₉H₈O₄ + CH₃COOH", "Esterificazione (acetilazione, sintesi dell'aspirina)",
       "Si forma acido acetico (odore di aceto); l'aspirina cristallizza raffreddando con acqua.",
       "Il gruppo OH dell'acido salicilico reagisce con l'anidride acetica e diventa un estere; si stacca acido "
       "acetico invece dell'acqua. L'acido salicilico, estratto dal salice, era un antidolorifico che irritava lo "
       "stomaco; acetilato (Bayer, 1897) diventò l'aspirina, ancora oggi usata contro dolore, febbre e per "
       "prevenire i trombi.",
       "acido solforico o fosforico come catalizzatore, ≈ 80 °C"),
    _r(["Glicerolo", "HNO₃ (acido nitrico)"], ["C₃H₅N₃O₉ (nitroglicerina)", "H₂O"],
       "C₃H₈O₃ + 3 HNO₃ → C₃H₅N₃O₉ + 3 H₂O", "Esterificazione (nitrazione del glicerolo)",
       "Si formano 3 molecole d'acqua; la nitroglicerina è un liquido oleoso ed estremamente instabile.",
       "Ognuno dei tre OH del glicerolo forma un estere nitrico. La nitroglicerina esplode con un urto: Nobel la "
       "stabilizzò assorbendola nella dinamite. In medicina, in dosi minime sotto la lingua, libera monossido di "
       "azoto che dilata i vasi coronarici e allevia il dolore dell'angina.",
       "miscela solfonitrica, a freddo (sotto i 10 °C)"),
    _r(["CH₃OH (metanolo)", "CuO (ossido di rame)"], ["HCHO (formaldeide)", "Cu (rame)", "H₂O"],
       "CH₃OH + CuO → HCHO + Cu + H₂O", "Ossidoriduzione (ossidazione di un alcol primario ad aldeide)",
       "Si forma vapore acqueo; il filo di rame annerito torna rosso lucente; odore pungente di formaldeide.",
       "Il carbonio dell'alcol si ossida (da −2 a 0) e il rame si riduce (da +2 a 0). Un alcol primario si ossida "
       "ad aldeide (e poi ad acido), uno secondario a chetone, uno terziario non si ossida. La formaldeide in acqua "
       "è la formalina, usata per conservare i preparati anatomici e nelle resine.",
       "filo di rame arroventato e immerso nei vapori"),
    _r(["C₂H₅OH (etanolo, con Acetobacter)", "O₂ (ossigeno)"], ["CH₃COOH (acido acetico)", "H₂O"],
       "C₂H₅OH + O₂ → CH₃COOH + H₂O", "Fermentazione acetica (ossidazione)",
       "Niente gas: il vino diventa aceto; in superficie si forma una pellicola gelatinosa (la «madre» dell'aceto).",
       "Il carbonio dell'alcol si ossida (da −1 a +3) e l'ossigeno si riduce (da 0 a −2), grazie ai batteri "
       "Acetobacter che hanno bisogno di aria. È il motivo per cui una bottiglia di vino aperta inacidisce, ed è "
       "il modo tradizionale di produrre l'aceto.",
       "batteri Acetobacter, aria, ≈ 25-30 °C"),
    _r(["CH₃CHO (acetaldeide)", "AgNO₃ (nitrato d'argento)"], ["CH₃COONH₄ (acetato di ammonio)", "Ag ↓", "NH₄NO₃"],
       "CH₃CHO + 2 AgNO₃ + 3 NH₃ + H₂O → CH₃COONH₄ + 2 Ag↓ + 2 NH₄NO₃", "Ossidoriduzione (saggio di Tollens)",
       "Sulle pareti della provetta si deposita uno specchio d'argento lucente.",
       "L'aldeide si ossida ad acido (il carbonio passa da +1 a +3) e l'argento si riduce (da +1 a 0). I chetoni "
       "non reagiscono: è il saggio per distinguere aldeidi e chetoni (e gli zuccheri riducenti come il glucosio). "
       "Con lo stesso principio si argentavano gli specchi e le palline dell'albero di Natale.",
       "reattivo di Tollens (nitrato d'argento in ammoniaca), bagnomaria tiepido"),
    _r(["C₅₇H₁₁₀O₆ (tristearina)", "KOH (idrossido di potassio)"],
       ["C₃H₈O₃ (glicerolo)", "C₁₇H₃₅COOK (stearato di potassio, sapone)"],
       "C₅₇H₁₁₀O₆ + 3 KOH → C₃H₈O₃ + 3 C₁₇H₃₅COOK", "Saponificazione (idrolisi basica)",
       "Niente gas: si forma un sapone molle e il glicerolo resta sciolto.",
       "La base rompe i tre legami estere del grasso: si liberano il glicerolo e tre molecole di sapone. Con la "
       "potassa (KOH) i saponi sono molli o liquidi, con la soda (NaOH) sono duri. Il sapone ha una testa ionica "
       "che ama l'acqua e una coda lunga che ama i grassi: così forma micelle che portano via lo sporco.",
       "a caldo"),
    _r(["CH₃COOC₂H₅ (acetato di etile)", "NaOH (idrossido di sodio)"], ["CH₃COONa (acetato di sodio)", "C₂H₅OH (etanolo)"],
       "CH₃COOC₂H₅ + NaOH → CH₃COONa + C₂H₅OH", "Saponificazione (idrolisi basica di un estere)",
       "Niente gas: l'odore fruttato dell'estere sparisce.",
       "L'OH⁻ attacca il carbonio del gruppo estere e lo spezza in un sale dell'acido e in alcol. A differenza "
       "dell'idrolisi acida, non è un equilibrio: l'acido carbossilico diventa subito ione acetato e non può più "
       "riformare l'estere. È la stessa reazione che fa il sapone dai grassi.",
       "a caldo"),
    _r(["Saccarosio", "H₂SO₄ (acido solforico concentrato)"], ["C (carbonio)", "H₂O ↑"],
       "C₁₂H₂₂O₁₁ → 12 C + 11 H₂O", "Eliminazione (disidratazione dello zucchero)",
       "Esce vapore acqueo con odore di caramello bruciato; lo zucchero diventa una colonna nera e spugnosa di "
       "carbone che sale dal bicchiere.",
       "L'acido solforico concentrato è un disidratante fortissimo: strappa a ogni molecola di zucchero 11 "
       "molecole d'acqua e lascia il carbonio. È molto esotermica. L'acido non compare nell'equazione perché trattiene "
       "l'acqua senza trasformarsi; spiega perché l'acido solforico concentrato provoca ustioni così gravi sulla pelle.",
       "acido solforico concentrato, sotto cappa"),
    # --- Biomolecole e biochimica ------------------------------------------------------------------------
    _r(["C₂H₅NO₂ (glicina)", "C₂H₅NO₂ (glicina)"], ["C₄H₈N₂O₃ (glicilglicina)", "H₂O"],
       "2 C₂H₅NO₂ → C₄H₈N₂O₃ + H₂O", "Condensazione (legame peptidico)",
       "Si libera una molecola d'acqua.",
       "Il gruppo carbossilico (−COOH) di una glicina si lega al gruppo amminico (−NH₂) dell'altra e si forma il "
       "legame peptidico −CO−NH−. La glicina è l'amminoacido più semplice (la catena laterale è un solo H) ed è "
       "abbondantissima nel collagene.",
       "nella cellula: ribosomi ed energia del GTP/ATP"),
    _r(["C₂H₅NO₂ (glicina)", "C₃H₇NO₂ (alanina)"], ["C₅H₁₀N₂O₃ (glicilalanina)", "H₂O"],
       "C₂H₅NO₂ + C₃H₇NO₂ → C₅H₁₀N₂O₃ + H₂O", "Condensazione (legame peptidico)",
       "Si libera una molecola d'acqua.",
       "Il −COOH della glicina e il −NH₂ dell'alanina formano il legame peptidico. Lo stesso due amminoacidi possono "
       "dare due dipeptidi diversi (Gly-Ala e Ala-Gly), a seconda di quale gruppo reagisce: per questo in una "
       "proteina conta l'ordine (sequenza) degli amminoacidi.",
       "nella cellula: ribosomi"),
    _r(["Dipeptide", "H₂O (acqua)"], ["C₂H₅NO₂ (glicina)", "C₃H₇NO₂ (alanina)"],
       "C₅H₁₀N₂O₃ + H₂O → C₂H₅NO₂ + C₃H₇NO₂", "Idrolisi (del legame peptidico)",
       "Niente si libera: entra una molecola d'acqua e il dipeptide (qui glicilalanina) si spezza.",
       "L'acqua rompe il legame peptidico e restituisce i due amminoacidi: è il contrario della condensazione. "
       "Nella digestione lo fanno gli enzimi proteasi (pepsina nello stomaco, tripsina nell'intestino), così gli "
       "amminoacidi vengono assorbiti.",
       "enzimi proteasi (o acido forte e calore)"),
    _r(["Lattosio", "H₂O (acqua)"], ["Glucosio", "Galattosio"],
       "C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆", "Idrolisi (del legame glicosidico)",
       "Niente si libera: entra una molecola d'acqua.",
       "La lattasi rompe il legame β-1,4 tra galattosio e glucosio, che vengono assorbiti dall'intestino. Chi produce "
       "poca lattasi (intolleranza al lattosio) lascia il lattosio ai batteri del colon, che lo fermentano con gas "
       "e gonfiore: il latte «senza lattosio» è già stato idrolizzato con la lattasi.",
       "enzima lattasi (intestino tenue)"),
    _r(["Maltosio", "H₂O (acqua)"], ["Glucosio"],
       "C₁₂H₂₂O₁₁ + H₂O → 2 C₆H₁₂O₆", "Idrolisi (del legame glicosidico)",
       "Niente si libera: entra una molecola d'acqua.",
       "La maltasi rompe il legame α-1,4 e libera due molecole di glucosio. Il maltosio viene dalla digestione "
       "dell'amido e dal malto dell'orzo germinato: nella birra il lievito lo usa, dopo l'idrolisi, per la "
       "fermentazione.",
       "enzima maltasi"),
    _r(["Amido", "H₂O (acqua)"], ["Glucosio"],
       "(C₆H₁₀O₅)ₙ + n H₂O → n C₆H₁₂O₆", "Idrolisi (dell'amido)",
       "Niente si libera: entrano n molecole d'acqua; con lo iodio il blu dell'amido scompare man mano.",
       "Ogni legame glicosidico dell'amido viene rotto da una molecola d'acqua, fino al glucosio (passando per "
       "destrine e maltosio). Nel corpo inizia in bocca con l'amilasi della saliva (il pane masticato a lungo "
       "diventa dolce) e continua nell'intestino con l'amilasi del pancreas.",
       "enzimi amilasi (saliva, pancreas) o acido e calore"),
    _r(["C₆H₁₂O₆ (glucosio, nei muscoli senza ossigeno)"], ["C₃H₆O₃ (acido lattico)"],
       "C₆H₁₂O₆ → 2 C₃H₆O₃", "Fermentazione lattica",
       "Niente gas (a differenza della fermentazione alcolica): si forma acido lattico.",
       "Dopo la glicolisi il piruvato viene ridotto a lattato dal NADH, che così torna NAD⁺ e permette alla "
       "glicolisi di continuare senza ossigeno; rende solo 2 ATP per glucosio. Avviene nei muscoli sotto sforzo "
       "intenso e nei globuli rossi; i batteri lattici la usano per fare yogurt, formaggi e crauti.",
       "assenza di ossigeno (muscoli sotto sforzo, batteri lattici)"),
    _r(["Glucosio", "ATP"], ["Glucosio-6-fosfato", "ADP"],
       "C₆H₁₂O₆ + C₁₀H₁₆N₅O₁₃P₃ → C₆H₁₃O₉P + C₁₀H₁₅N₅O₁₀P₂", "Fosforilazione (prima tappa della glicolisi)",
       "Niente si libera: un gruppo fosfato passa dall'ATP al glucosio.",
       "L'esochinasi trasferisce il fosfato terminale dell'ATP al carbonio 6 del glucosio. Il glucosio-6-fosfato, "
       "carico negativamente, non può più uscire dalla cellula: resta «intrappolato» per la glicolisi o per fare "
       "glicogeno. È una tappa che consuma energia (si «investe» un ATP).",
       "enzima esochinasi (glucochinasi nel fegato), ioni Mg²⁺"),
    _r(["Fosfocreatina", "ADP"], ["Creatina", "ATP"],
       "C₄H₁₀N₃O₅P + C₁₀H₁₅N₅O₁₀P₂ → C₄H₉N₃O₂ + C₁₀H₁₆N₅O₁₃P₃", "Trasferimento di fosfato (riserva rapida del muscolo)",
       "Niente si libera: il fosfato passa dalla fosfocreatina all'ADP e si riforma ATP.",
       "La creatina chinasi ricarica l'ADP in pochi millisecondi: è la riserva di energia dei primi 10 secondi di "
       "uno sforzo massimo (scatto, sollevamento pesi). Per questo alcuni sportivi assumono creatina; la creatina "
       "chinasi nel sangue è anche un indice di danno muscolare o cardiaco.",
       "enzima creatina chinasi, nei muscoli"),
    _r(["CO(NH₂)₂ (urea)", "H₂O (acqua)"], ["CO₂ ↑", "NH₃ ↑"],
       "CO(NH₂)₂ + H₂O → CO₂↑ + 2 NH₃↑", "Idrolisi (enzima ureasi)",
       "Si liberano anidride carbonica e ammoniaca (odore pungente, per esempio nelle lettiere e nei pannolini).",
       "L'ureasi scinde l'urea; il pH sale per l'ammoniaca. Il batterio Helicobacter pylori, che causa gastrite e "
       "ulcera, produce ureasi per proteggersi dall'acido dello stomaco: il «breath test» fa bere urea marcata e "
       "cerca nel respiro la CO₂ marcata che si libera.",
       "enzima ureasi (batteri, semi di soia)"),
]
