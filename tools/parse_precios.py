#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte la lista de precios (texto extraído del PDF con `pdftotext -layout`)
en assets/data/productos.json, que consume el carrito de la web.

Uso:
  pdftotext -layout LISTA_DE_PRECIOS.pdf tools/lista-precios-AAAA-MM.txt
  python3 tools/parse_precios.py tools/lista-precios-AAAA-MM.txt

Cada producto queda como:
  { "id": "...", "cod": "...", "desc": "...", "pack": "x2000" | "",
    "pres": "Granel" | "Sobre" | "Estuche" | "", "precio": 123456.78 | null,
    "grupo": "Hexagonal punta mecha", "cat": "tornillos-autoperforantes",
    "sinStock": true|false }
"""
import json
import re
import sys
import unicodedata

# Encabezados de sección del PDF -> (nombre de grupo, slug de categoría del sitio)
SECTIONS = {
    "HEXAGONAL PUNTA RANURA/AGUJA": ("Hexagonal punta ranurada/aguja", "tornillos-autoperforantes"),
    "HEXAGONAL PUNTA MECHA":        ("Hexagonal punta mecha", "tornillos-autoperforantes"),
    "FIX":                          ("FIX", "tornillos-autoperforantes"),
    "DECK T25":                     ("Deck T25", "tornillos-autoperforantes"),
    "HORMIGÓN T30":                 ("Hormigón T30", "tornillos-autoperforantes"),
    "DRYWALL MADERA":               ("Drywall madera", "tornillos-autoperforantes"),
    "TANQUE AGUJA":                 ("Tanque aguja", "tornillos-autoperforantes"),
    "TANQUE MECHA":                 ("Tanque mecha", "tornillos-autoperforantes"),
    "DRYWALL METAL PUNTA AGUJA":    ("Drywall metal punta aguja", "tornillos-autoperforantes"),
    "DRYWALL METAL PUNTA MECHA":    ("Drywall metal punta mecha", "tornillos-autoperforantes"),
    "ENSAMBLADOR":                  ("Ensamblador", "tornillos-autoperforantes"),
    "PAN FRAMING":                  ("Pan framing", "tornillos-autoperforantes"),
    "TIPO KRG":                     ("Tipo KREG (oculto)", "tornillos-autoperforantes"),
    "PUNTA MECHA CON ALAS":         ("Punta mecha con alas", "tornillos-autoperforantes"),
    "PARKER AGUJA":                 ("Parker aguja", "tornillos-autoperforantes"),
    "PARKER MECHA":                 ("Parker mecha", "tornillos-autoperforantes"),
    "TANQUE P/TUERCA":              ("Tanque p/tuerca", "tornillos-autoperforantes"),
    "TIRAFONDOS":                   ("Tirafondos", "tirafondos-y-fijaciones"),
    "TUERCA HEXAGONAL":             ("Tuercas hexagonales", "tirafondos-y-fijaciones"),
    "ARANDELAS":                    ("Arandelas planas", "tirafondos-y-fijaciones"),
    "PLANAS":                       ("Arandelas planas", "tirafondos-y-fijaciones"),
    "CHAPISTA":                     ("Arandelas chapista", "tirafondos-y-fijaciones"),
    "TARUGOS":                      ("Tarugos comunes", "tirafondos-y-fijaciones"),
    "COMÚN SIN TOPE":               ("Tarugos comunes sin tope", "tirafondos-y-fijaciones"),
    "COMÚN CON TOPE":               ("Tarugos comunes con tope", "tirafondos-y-fijaciones"),
    "UNIVERSAL SIN TOPE":           ("Tarugos universales sin tope", "tirafondos-y-fijaciones"),
    "UNIVERSAL CON TOPE":           ("Tarugos universales con tope", "tirafondos-y-fijaciones"),
    "FX (HUECO)":                   ("Tarugos FX (hueco)", "tirafondos-y-fijaciones"),
    "YESO - DURLOCK":               ("Tarugos yeso/durlock", "tirafondos-y-fijaciones"),
    "MARIPOSA":                     ("Tarugos mariposa", "tirafondos-y-fijaciones"),
    "GRAMPAS OMEGA - MEDIA":        ("Grampas Omega", "tirafondos-y-fijaciones"),
    "GANCHO J":                     ("Ganchos J", "tirafondos-y-fijaciones"),
    "TORNIQUETES":                  ("Torniquetes", "tirafondos-y-fijaciones"),
    "CLAVOS":                       ("Clavos punta París", "clavos-y-alambres"),
    "PUNTA PARIS":                  ("Clavos punta París", "clavos-y-alambres"),
    "ESPIRALADOS":                  ("Clavos espiralados", "clavos-y-alambres"),
    "CABEZA DE PLOMO - NACIONALES": ("Clavos cabeza de plomo (nacionales)", "clavos-y-alambres"),
    "CABEZA DE PLOMO - IMPORTADOS": ("Clavos cabeza de plomo (importados)", "clavos-y-alambres"),
    "CAJONERO ESPIRALADO":          ("Clavos cajonero espiralado", "clavos-y-alambres"),
    "ALAMBRE GALVANIZADO":          ("Alambre galvanizado", "clavos-y-alambres"),
    "ALAMBRE NEGRO RECOCIDO":       ("Alambre negro recocido", "clavos-y-alambres"),
    "ALAMBRE PARA SOLDAR":          ("Alambre para soldar (MIG)", "soldadura"),
    "CABEZA CHATA/PERDIDA/CAJONERO": ("Clavos cabeza chata/perdida", "clavos-y-alambres"),
    "CONCERTINA":                   ("Concertina", "clavos-y-alambres"),
    "ALAMBRE DE PÚAS":              ("Alambre de púas", "clavos-y-alambres"),
    "ELECTRODOS":                   ("Electrodos", "soldadura"),
    "CLAVOS PARAGUA":               ("Clavos paragua", "clavos-y-alambres"),
    "HIERRO DULCE":                 ("Hierro dulce", "hierros-y-mallas"),
    "CLAVOS ELECTROSOLDADOS":       ("Clavos electrosoldados", "clavos-y-alambres"),
    "GRAMPAS":                      ("Grampas", "tirafondos-y-fijaciones"),
    "CLAVOS TIPIN (F)":             ("Clavos tipín (F)", "clavos-y-alambres"),
    "ALAMBRE TEJIDO":               ("Alambre tejido", "clavos-y-alambres"),
}

# Encabezados "contenedores" que solo agrupan (no cambian el grupo activo útil)
IGNORE_HEADS = {"TORNILLOS AUTOPERFORANTES", "GRANEL", "COD", "DESCRIPCIÓN", "LISTA", "LISTA A", "S/IVA"}

ROW = re.compile(r"^\s*([A-Za-z]+[\w-]*\d+)\s{2,}(.+?)(?:\s+\$\s*([\d.,]+|-))?\s*$")


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def parse_price(raw):
    if not raw or raw == "-":
        return None
    # formato es-AR: 100.568,30
    return float(raw.replace(".", "").replace(",", "."))


def clean_desc(desc):
    """Limpia marcadores del PDF y separa pack/presentación."""
    d = norm_ws(desc)
    sin_stock = "SIN STOCK" in d
    d = d.replace("- SIN STOCK", "").replace("SIN STOCK", "")
    # marcadores internos de la lista ('<' y '*')
    d = re.sub(r"\s[<*]\s", " ", d + " ").strip()
    d = re.sub(r"\s[<*]$", "", d).strip()
    pack = ""
    m = re.match(r"^[Xx](\d[\d.]*)\s+(.*)$", d)
    if m:
        pack = "x" + m.group(1)
        d = m.group(2)
    pres = ""
    m = re.search(r"\s(GRANEL|SOBRE|ESTUCHE)$", d)
    if m:
        pres = m.group(1).capitalize()
        d = d[: m.start()].strip()
    d = re.sub(r"\sTARUGO$", "", d)  # redundante: el grupo ya dice "Tarugos"
    d = norm_ws(d.strip(" -"))
    return d, pack, pres, sin_stock


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    grupo, cat = None, None
    items, seen_ids = [], set()
    for line in lines:
        s = norm_ws(line)
        if not s:
            continue
        # ¿es un encabezado de sección?
        up = s.upper()
        if up in SECTIONS:
            grupo, cat = SECTIONS[up]
            continue
        if up in IGNORE_HEADS or up.startswith("COD "):
            continue
        m = ROW.match(line)
        if not m or grupo is None:
            continue
        cod, rawdesc, rawprice = m.group(1), m.group(2), m.group(3)
        desc, pack, pres, sin_stock = clean_desc(rawdesc)
        if not desc:
            continue
        pid = cod
        n = 2
        while pid in seen_ids:  # hay códigos repetidos en el PDF (ALA05, CON03)
            pid = f"{cod}-{n}"
            n += 1
        seen_ids.add(pid)
        items.append({
            "id": pid, "cod": cod, "desc": desc, "pack": pack, "pres": pres,
            "precio": parse_price(rawprice), "grupo": grupo, "cat": cat,
            "sinStock": sin_stock,
        })

    # Pinturas y químicos: lista aparte en formato matriz, transcripta a mano
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pinturas
    items.extend(pinturas.items())

    out = {"actualizado": {"fijaciones": "2026-05", "pinturas": pinturas.ACTUALIZADO},
           "moneda": "ARS", "items": items}
    dest = "assets/data/productos.json"
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK — {len(items)} productos -> {dest}")
    # resumen por categoría
    from collections import Counter
    for k, v in Counter(i["cat"] for i in items).most_common():
        print(f"  {k}: {v}")
    nulos = [i["cod"] for i in items if i["precio"] is None]
    if nulos:
        print("  sin precio (a consultar):", ", ".join(nulos))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tools/lista-precios-2026-05.txt")
