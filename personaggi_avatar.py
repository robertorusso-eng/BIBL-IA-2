"""I personaggi per l'avatar degli studenti di BIBL-IA 2: disegni originali in stile cartone (SVG), fatti con il
codice, senza immagini scaricate. Ogni personaggio è una combinazione di pelle, capelli, occhi, vestiti e accessori."""

PELLE = {"chiara": ("#FAD9BE", "#E8B897"), "rosata": ("#F3C6A5", "#DDA27F"), "olivastra": ("#E0AC78", "#C38F5C"),
         "ambrata": ("#C68642", "#A66C30"), "scura": ("#8D5524", "#6E401A"), "molto scura": ("#5C3A21", "#452A16")}
CAPELLI = {"neri": "#2B2118", "castani": "#6B4226", "biondi": "#E1B85C", "rossi": "#B5502B", "grigi": "#B8B8B8",
           "blu": "#3B5BDB", "rosa": "#E86AA6", "viola": "#7C4DDB"}


def _capelli_dietro(stile, c):
    return {
        "lunghi": f'<path d="M25 46 Q23 17 50 17 Q77 17 75 46 L77 86 Q66 90 61 76 L39 76 Q34 90 23 86 Z" fill="{c}"/>',
        "caschetto": f'<path d="M24 48 Q22 16 50 16 Q78 16 76 48 L76 66 Q71 69 66 66 L34 66 Q29 69 24 66 Z" fill="{c}"/>',
        "coda": f'<path d="M70 36 Q88 44 82 74 Q78 62 70 52 Z" fill="{c}"/>',
        "chignon": f'<circle cx="50" cy="15" r="9" fill="{c}"/>',
        "ricci": "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{c}"/>' for x, y in
                         [(28, 44), (72, 44), (26, 56), (74, 56), (30, 66), (70, 66)]),
        "velo": f'<path d="M22 52 Q20 14 50 14 Q80 14 78 52 L82 92 L18 92 Z" fill="{c}"/>',
    }.get(stile, "")


def _capelli_davanti(stile, c):
    corti = f'<path d="M28 45 Q27 19 50 19 Q73 19 72 45 Q69 31 59 29 Q50 34 40 29 Q31 32 28 45 Z" fill="{c}"/>'
    riga = f'<path d="M28 46 Q27 18 50 18 Q73 18 72 46 Q68 30 54 27 Q40 30 28 46 Z" fill="{c}"/>'
    return {
        "corti": corti,
        "ciuffo": f'<path d="M28 45 Q26 17 52 16 Q70 15 73 34 Q76 44 72 45 Q68 30 58 28 Q46 34 36 30 Q30 36 28 45 Z" fill="{c}"/>'
                  f'<path d="M44 20 Q52 6 66 14 Q56 14 52 22 Z" fill="{c}"/>',
        "rasati": f'<path d="M29 41 Q30 21 50 21 Q70 21 71 41 Q61 30 50 30 Q39 30 29 41 Z" fill="{c}" opacity=".85"/>',
        "lunghi": riga, "caschetto": f'<path d="M28 46 Q27 18 50 18 Q73 18 72 46 Q66 32 50 32 Q34 32 28 46 Z" fill="{c}"/>',
        "coda": riga, "chignon": f'<path d="M28 44 Q27 21 50 21 Q73 21 72 44 Q64 29 50 29 Q36 29 28 44 Z" fill="{c}"/>',
        "ricci": "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{c}"/>' for x, y in
                         [(31, 34), (39, 26), (50, 23), (61, 26), (69, 34), (44, 31), (56, 31)]),
        "velo": f'<path d="M26 50 Q26 20 50 20 Q74 20 74 50 Q70 30 50 29 Q30 30 26 50 Z" fill="{c}"/>',
    }.get(stile, corti)


def svg_personaggio(x):
    """Il disegno SVG (100×100) di un personaggio."""
    pelle, ombra = PELLE[x["pelle"]]
    capelli = CAPELLI[x["capelli"]]
    velo = x["stile"] == "velo"
    vestito = x.get("vestito", "#2563EB")
    parti = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><clipPath id="t"><circle cx="50" cy="50" r="50"/>'
             f'</clipPath></defs><g clip-path="url(#t)"><rect width="100" height="100" fill="{x.get("sfondo", "#DBE4FF")}"/>',
             _capelli_dietro(x["stile"], x.get("colore_velo", capelli) if velo else capelli)]
    # Il corpo: maglietta o camice da laboratorio.
    parti.append(f'<rect x="43" y="62" width="14" height="13" fill="{ombra}"/>')
    if x.get("camice"):
        parti.append(f'<path d="M12 100 Q14 75 50 73 Q86 75 88 100 Z" fill="#FFFFFF" stroke="#D5DBE5" stroke-width="1"/>'
                     f'<path d="M42 74 L50 90 L58 74 Q54 73 50 73 Q46 73 42 74 Z" fill="{vestito}"/>'
                     f'<path d="M42 74 L47 100 M58 74 L53 100" stroke="#D5DBE5" stroke-width="1.2"/>'
                     f'<rect x="62" y="84" width="9" height="6" rx="1.5" fill="none" stroke="#C3CAD6" stroke-width="1"/>')
    else:
        parti.append(f'<path d="M12 100 Q14 75 50 73 Q86 75 88 100 Z" fill="{vestito}"/>'
                     f'<path d="M42 74 Q50 81 58 74" fill="none" stroke="{ombra}" stroke-width="2"/>')
    if not velo:
        parti.append(f'<circle cx="28.5" cy="49" r="4.5" fill="{pelle}"/><circle cx="71.5" cy="49" r="4.5" fill="{pelle}"/>')
    parti.append(f'<ellipse cx="50" cy="46" rx="21.5" ry="24.5" fill="{pelle}"/>')
    parti.append(_capelli_davanti(x["stile"], x.get("colore_velo", capelli) if velo else capelli))
    # Il viso: sopracciglia, occhi grandi con il riflesso, guance, naso e sorriso.
    sopracciglia = x.get("sopracciglia", capelli if not velo else "#3A2A20")
    parti.append(f'<path d="M37 39.5 Q42 36.5 47 39" stroke="{sopracciglia}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
                 f'<path d="M53 39 Q58 36.5 63 39.5" stroke="{sopracciglia}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    for cx in (42, 58):
        parti.append(f'<ellipse cx="{cx}" cy="47" rx="3.6" ry="4.3" fill="#2B2B2B"/><circle cx="{cx + 1.2}" cy="45.4" r="1.3" fill="#fff"/>')
    parti.append('<circle cx="35" cy="55" r="3.6" fill="#F28B82" opacity=".35"/><circle cx="65" cy="55" r="3.6" fill="#F28B82" opacity=".35"/>')
    parti.append(f'<path d="M50 49 Q48 54 50.8 54.4" stroke="{ombra}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    if x.get("sorriso") == "aperto":
        parti.append('<path d="M42 58 Q50 67 58 58 Z" fill="#FFFFFF" stroke="#8A3B3B" stroke-width="1.6" stroke-linejoin="round"/>')
    else:
        parti.append('<path d="M43 58.5 Q50 64 57 58.5" stroke="#8A3B3B" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if x.get("barba"):
        parti.append(f'<path d="M30 50 Q31 73 50 74 Q69 73 70 50 Q66 64 58 63 Q50 61 42 63 Q34 64 30 50 Z" fill="{capelli}"/>'
                     '<path d="M43 59 Q50 63.5 57 59" stroke="#8A3B3B" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if x.get("occhiali"):
        parti.append(f'<g fill="none" stroke="{x.get("occhiali")}" stroke-width="1.8"><circle cx="42" cy="47" r="6.5"/>'
                     '<circle cx="58" cy="47" r="6.5"/><path d="M48.5 47 Q50 45.5 51.5 47"/></g>')
    if x.get("cuffie"):
        parti.append(f'<path d="M25 48 Q25 15 50 15 Q75 15 75 48" fill="none" stroke="{x["cuffie"]}" stroke-width="4"/>'
                     f'<rect x="20" y="42" width="9" height="15" rx="4" fill="{x["cuffie"]}"/>'
                     f'<rect x="71" y="42" width="9" height="15" rx="4" fill="{x["cuffie"]}"/>')
    parti.append("</g></svg>")
    return "".join(parti)


# I personaggi già pronti tra cui scegliere.
PERSONAGGI = {
    "p01": {"pelle": "chiara", "capelli": "castani", "stile": "corti", "vestito": "#2563EB", "sfondo": "#DBE4FF", "sorriso": "aperto"},
    "p02": {"pelle": "rosata", "capelli": "biondi", "stile": "lunghi", "vestito": "#E64980", "sfondo": "#FFE3EC"},
    "p03": {"pelle": "ambrata", "capelli": "neri", "stile": "ricci", "vestito": "#16A34A", "sfondo": "#D3F9D8", "sorriso": "aperto"},
    "p04": {"pelle": "scura", "capelli": "neri", "stile": "rasati", "vestito": "#F59F00", "sfondo": "#FFF3BF", "barba": True},
    "p05": {"pelle": "olivastra", "capelli": "castani", "stile": "coda", "vestito": "#7C3AED", "sfondo": "#E5DBFF", "occhiali": "#343A40"},
    "p06": {"pelle": "chiara", "capelli": "rossi", "stile": "caschetto", "vestito": "#0CA678", "sfondo": "#C3FAE8", "sorriso": "aperto"},
    "p07": {"pelle": "molto scura", "capelli": "neri", "stile": "ricci", "vestito": "#E03131", "sfondo": "#FFE3E3"},
    "p08": {"pelle": "rosata", "capelli": "neri", "stile": "ciuffo", "vestito": "#1C7ED6", "sfondo": "#D0EBFF", "cuffie": "#212529"},
    "p09": {"pelle": "olivastra", "capelli": "neri", "stile": "velo", "colore_velo": "#5F3DC4", "vestito": "#5F3DC4", "sfondo": "#F3F0FF", "sorriso": "aperto"},
    "p10": {"pelle": "chiara", "capelli": "biondi", "stile": "ciuffo", "vestito": "#FFFFFF", "camice": True, "sfondo": "#E7F5FF", "occhiali": "#1971C2"},
    "p11": {"pelle": "ambrata", "capelli": "castani", "stile": "chignon", "vestito": "#2563EB", "camice": True, "sfondo": "#EDF2FF"},
    "p12": {"pelle": "chiara", "capelli": "grigi", "stile": "corti", "vestito": "#495057", "sfondo": "#F1F3F5", "occhiali": "#495057", "barba": True},
    "p13": {"pelle": "rosata", "capelli": "rosa", "stile": "caschetto", "vestito": "#AE3EC9", "sfondo": "#F8F0FC", "sorriso": "aperto"},
    "p14": {"pelle": "scura", "capelli": "blu", "stile": "ciuffo", "vestito": "#0B7285", "sfondo": "#C5F6FA", "sorriso": "aperto"},
    "p15": {"pelle": "olivastra", "capelli": "castani", "stile": "corti", "vestito": "#E8590C", "sfondo": "#FFE8CC", "occhiali": "#862E9C"},
    "p16": {"pelle": "molto scura", "capelli": "neri", "stile": "chignon", "vestito": "#C2255C", "sfondo": "#FFDEEB", "sorriso": "aperto"},
    "p17": {"pelle": "chiara", "capelli": "neri", "stile": "lunghi", "vestito": "#37B24D", "sfondo": "#EBFBEE", "cuffie": "#E64980"},
    "p18": {"pelle": "ambrata", "capelli": "neri", "stile": "corti", "vestito": "#1864AB", "camice": True, "sfondo": "#E7F5FF", "barba": True},
    "p19": {"pelle": "rosata", "capelli": "viola", "stile": "coda", "vestito": "#3B5BDB", "sfondo": "#EDF2FF", "sorriso": "aperto"},
    "p20": {"pelle": "scura", "capelli": "castani", "stile": "lunghi", "vestito": "#F08C00", "sfondo": "#FFF9DB", "occhiali": "#212529"},
}
