# -*- coding: utf-8 -*-
"""
Lista de precios de PINTURAS Y QUÍMICOS — Julio 2026 ("LISTA DE PRECIOS
FERRETERO - JULIO 2026"). Transcripta a mano del PDF porque su formato es una
matriz producto × presentación (no parseable de forma confiable con pdftotext).

Cada producto: (descripción, [(presentación, precio), ...]).
Precio None o presentación ausente = no viene en esa medida.

La consume tools/parse_precios.py, que genera assets/data/productos.json.
"""

ACTUALIZADO = "2026-07"

# (grupo, [(desc, [(pres, precio)...]), ...])
PINTURAS = [
  ("Látex Símbolo-Tex", [
    ("LATEX INTERIOR PROFESIONAL", [("1 L", 6037.46), ("4 L", 15657.07), ("10 L", 33549.23), ("20 L", 62628.28)]),
    ("LATEX PARA CIELORRASO", [("1 L", 6635.20), ("4 L", 21450.00)]),
    ("LATEX INT-EXT PROFESIONAL", [("1 L", 6885.45), ("4 L", 18793.06), ("10 L", 42502.46), ("20 L", 80560.48)]),
    ("ENDUIDO INT-EXT", [("1 L", 6485.05), ("4 L", 15862.99), ("10 L", 32536.79), ("20 L", 61630.14)]),
    ("FIJADOR INT-EXT", [("1 L", 6267.69), ("4 L", 17480.32), ("10 L", 37405.94), ("20 L", 71996.21)]),
    ("MEMBRANA LIQUIDA - BLANCA/ROJA/VERDE", [("1 L", 9390.81), ("4 L", 31311.28), ("10 L", 68742.96), ("20 L", 128159.46)]),
    ("HIDROFUGO MINERAL EN PASTA", [("1 L", 3452.02), ("4 L", 13206.05), ("10 L", 26060.32), ("20 L", 46825.35)]),
    ("ADHESIVO PLASTICO", [("1 L", 6236.23), ("4 L", 17480.32), ("10 L", 37277.24), ("20 L", 71994.78)]),
    ("MASILLA PARA PLACA DE YESO INT-EXT", [("1 L", 7830.68), ("4 L", 20280.26), ("10 L", 43770.87), ("20 L", 65458.25)]),
  ]),
  ("Sintéticos 3 en 1", [
    ("SINTETICO 3 EN 1 GRUPO 1 (Negro brill/mate/satin, Verde inglés, Marrón, Azul, Gris)",
     [("1/4 L", 7383.09), ("1/2 L", 8529.95), ("1 L", 14042.60), ("4 L", 48534.20)]),
    ("SINTETICO 3 EN 1 GRUPO 2 (Blanco brill/mate/satin, Bermellón, Amarillo, Naranja)",
     [("1/4 L", 8840.26), ("1/2 L", 9685.39), ("1 L", 16998.41), ("4 L", 61398.48)]),
    ("BARNIZ", [("1/4 L", 6134.70), ("1/2 L", 9210.63), ("1 L", 13982.54), ("4 L", 45376.76)]),
    ("BARNIZ MARINO", [("1/4 L", 7684.82), ("1/2 L", 10140.13), ("1 L", 15365.35), ("4 L", 49774.01)]),
  ]),
  ("Polvos y morteros", [
    ("MEZCLA REFORZADA", [("2 kg", 1261.26), ("5 kg", 2696.98), ("10 kg", 5232.37), ("30 kg", 15514.07)]),
    ("MEZCLA ADHESIVA", [("2 kg", 1667.38), ("5 kg", 3702.27), ("10 kg", 6698.12), ("30 kg", 16904.03)]),
    ("FINO A LA CAL", [("5 kg", 3104.53), ("10 kg", 5312.45), ("30 kg", 13719.42)]),
    ("ARENA CLASIFICADA", [("5 kg", 1970.54), ("10 kg", 3361.93), ("30 kg", 9000.42)]),
    ("YESO TIPO PARIS", [("1 kg", 1328.47), ("2 kg", 2492.49), ("5 kg", 5485.48), ("10 kg", 10134.41), ("30 kg", 19109.09)]),
    ("CEMENTO COMUN LOMA NEGRA", [("1 kg", 1168.31), ("2 kg", 1937.65), ("5 kg", 4248.53), ("10 kg", 8029.45)]),
    ("CEMENTO RAPIDO GRIS", [("1 kg", 1265.55), ("2 kg", 2365.22), ("5 kg", 5245.24), ("10 kg", 9751.17)]),
    ("CEMENTO RAPIDO BLANCO", [("1 kg", 2260.83), ("2 kg", 4154.15), ("5 kg", 8997.56), ("10 kg", 18125.25)]),
    ("CEMENTO BLANCO", [("1 kg", 2173.60), ("2 kg", 4006.86), ("5 kg", 8694.40), ("10 kg", 17601.87)]),
    ("TIZA MOLIDA", [("1 kg", 1116.83), ("2 kg", 2213.64), ("5 kg", 4869.15)]),
    ("CONCRETO", [("2 kg", 1225.51), ("5 kg", 2625.48), ("10 kg", 5089.37), ("30 kg", 13921.05)]),
    ("CEMENTO BLANCO SUPER WHITE", [("25 kg", 74492.99)]),
    ("CAL STA ELENA", [("20 kg", 11787.49)]),
    ("PASTINA BLANCA Y COLOR (Rojo, Negro, Crema, Gris, Cuero, Beige, Amarillo, Arena, Ocre, Verde, Azul, Marrón)", [("1 kg", 2807.09)]),
  ]),
  ("Pinturas al agua y cal", [
    ("PINTURA AL AGUA BLANCA", [("4 kg", 4723.29)]),
    ("PINTURA AL AGUA COLOR (Celeste, Gris, Tabaco, Verde, Azul, Rosa, Marfil, Durazno, Crema)", [("4 kg", 5727.15)]),
    ("CAL PARA BLANQUEO", [("4 kg", 4723.29)]),
    ("LECHE DE TUNA - FIJADOR P/ CAL", [("1/4 kg", 1372.80)]),
  ]),
  ("Polvos para colorear", [
    ("FERRITE ROJO / AMARILLO", [("1 kg", 5077.93), ("25 kg", 107650.40)]),
    ("FERRITE NEGRO", [("1 kg", 5571.28), ("25 kg", 118416.87)]),
    ("FERRITE AZUL / VERDE", [("1 kg", 7663.37), ("25 kg", 175179.29)]),
  ]),
  ("Combustibles y diluyentes", [
    ("PRESERVADOR PARA MADERA", [("1 L", 4620.33), ("5 L", 19821.23), ("10 L", 38627.16), ("20 L", 87556.04)]),
    ("DILURRAS", [("1/2 L", 2323.75), ("1 L", 4212.78), ("5 L", 18088.07), ("10 L", 35266.66), ("20 L", 79924.13)]),
    ("SIMBOLORRAS", [("1/2 L", 3000.14), ("1 L", 5835.83), ("5 L", 27344.46), ("10 L", 49648.17), ("20 L", 98386.86)]),
    ("THINNER", [("1/2 L", 3906.76), ("1 L", 7347.34), ("5 L", 34151.26), ("10 L", 68301.09), ("20 L", 136642.22)]),
    ("REMOVEDOR", [("1 L", 5312.45), ("5 L", 9987.12)]),
    ("REMOVEDOR GEL TRIMAS", [("1 L", 26407.81)]),
    ("KEROSENE", [("1 L", 7504.64), ("5 L", 35651.33)]),
    ("CLORO", [("1 L", 2080.65), ("5 L", 9249.24), ("10 L", 19406.53), ("20 L", 42859.96)]),
    ("ACEITE BOMBEADOR", [("1 L", 4417.27)]),
    ("ACEITE P/ MADERA", [("1 L", 4365.79), ("5 L", 20258.81), ("10 L", 40243.06)]),
  ]),
  ("Asfaltos", [
    ("PINTURA ASFALTICA", [("1 kg", 7470.32), ("4 kg", 23526.36), ("10 kg", 56303.39), ("18 kg", 98153.77)]),
  ]),
  ("Químicos Símbolo-Tex", [
    ("MASILLA PARA VIDRIOS Y SANITARIOS", [("1/2 kg", 1535.82), ("1 kg", 2428.14)]),
    ("GRASA ROJA (LITIO)", [("1/4 kg", 3281.85), ("1/2 kg", 6127.55)]),
    ("SOLUCION CAUSTICA", [("1/2 kg", 2197.91), ("1 kg", 4197.05)]),
    ("AM/00", [("1 kg", 2862.86), ("5 L", 13087.36), ("10 L", 24224.20)]),
    ("DESOXIDANTE", [("1 kg", 7230.08), ("5 L", 35624.16)]),
    ("ACELERANTE DE FRAGUE", [("1 kg", 2120.69), ("5 L", 9965.67)]),
    ("QUITA SARRO", [("1/2 kg", 2309.45), ("1 kg", 4388.67)]),
    ("DESTAPA CAÑERIAS", [("1 kg", 2631.20)]),
    ("SAL DE LIMÓN", [("1/4 kg", 2132.13), ("1/2 kg", 4112.68)]),
  ]),
  ("Vendas y mantas sintéticas", [
    ("COBERTOR PLASTICO", [("1,10 x 2,20 m", 2340.91)]),
    ("VENDA DE FIBRA SINTETICA ANCHA", [("0,20 x 25 m", 4144.14)]),
    ("VENDA DE FIBRA SINTETICA ANGOSTA", [("0,10 x 25 m", 2166.45)]),
    ("MANTA DE FIBRA SINTETICA", [("1 x 25 m", 19572.41)]),
    ("MANTA GEO TEXTIL MAGIPLAST", [("Manta", 121550.00)]),
  ]),
  ("Accesorios y varios", [
    ("LIJAS AL AGUA Nº 60 A 500 (60/80/100/120/150/180/220/240/280/320/400/500)", [("Pack completo", 67659.02)]),
    ("CINTA ENMASCARAR 12X50", [("Unidad", 3054.48)]),
    ("CINTA ENMASCARAR 18X50", [("Unidad", 4006.86)]),
    ("CINTA ENMASCARAR 24X50", [("Unidad", 5369.65)]),
    ("CINTA ENMASCARAR 36X50", [("Unidad", 7999.42)]),
    ("CINTA ENMASCARAR 48X50", [("Unidad", 10427.56)]),
    ("RECUMIX", [("1,250 kg", 9738.30)]),
    ("PASTA DE PULIR FINA", [("Unidad", 12980.11)]),
    ("LUBRICANTE PENETRIT 10 FUNCIONES", [("155 g / 216 cm³", 6023.16)]),
    ("MASILLA TRI-MAS TRADICIONAL (línea automotor)", [("1/4 kg", 10531.95), ("1/2 kg", 12225.07), ("1 kg", 16496.48)]),
  ]),
  ("Cibel / Casablanca / Tintas", [
    ("LATEX ECO CIBEL - PAREDES BLANCAS", [("20 L", 57200.00)]),
    ("ENTONADORES BY CIBEL (Varios colores)", [("120 cc", 3289.00)]),
    ("ENTONADORES BY CASABLANCA (Varios colores)", [("120 cc", 4533.10)]),
    ("TINTAS PARA BARNIZ BY SINTEPLAST (Varios tonos)", [("60 cc", 3832.40)]),
  ]),
  ("Rodillos y pinceles El Galgo", [
    ("RODILLO ANTIGOTA", [("Nº 17", 10397.53), ("Nº 22", 10756.46)]),
    ("MINI RODILLO ANTIGOTA", [("5 cm", 2571.14), ("8 cm", 2779.92), ("11 cm", 3257.54)]),
    ("RODILLO ESPUMA", [("Nº 10", 5995.99), ("Nº 17", 6357.78), ("Nº 22", 7629.05)]),
    ("RODILLO LANA NATURAL LINEA HOGAR", [("Nº 17", 10248.81), ("Nº 22", 14227.07)]),
    ("RODILLO CUBREMAS", [("Nº 17", 8947.51), ("Nº 22", 10662.08)]),
    ("MINI RODILLO FORRADO", [("5 cm", 2522.52), ("8 cm", 2439.58), ("11 cm", 3364.79)]),
    ("PINCEL Nº7 SIMBOLO-TEX", [("Unidad", 2313.74)]),
    ("PINCEL Nº10 SIMBOLO-TEX", [("Unidad", 2798.51)]),
    ("PINCEL Nº15 SIMBOLO-TEX", [("Unidad", 3444.87)]),
    ("PINCEL Nº20 SIMBOLO-TEX", [("Unidad", 4894.89)]),
    ("PINCEL Nº25 SIMBOLO-TEX", [("Unidad", 5762.90)]),
    ("PINCEL Nº30 SIMBOLO-TEX", [("Unidad", 7124.26)]),
    ("PINCELETA SIMBOLO-TEX", [("Unidad", 8189.61)]),
  ]),
  ("Cetol / Brik-Col (nuevos ingresos)", [
    ("CETOL CLASSIC BRILLANTE (Cristal/Natural/Cedro/Roble/Caoba/Nogal)", [("1 L", 26779.61), ("4 L", 92339.39)]),
    ("CETOL CLASSIC SATINADO (Cristal/Natural/Cedro/Roble/Caoba/Nogal)", [("1 L", 20600.58), ("4 L", 71030.96)]),
    ("BRIK-COL LADRILLO (Incoloro/Cerámico/Natural)", [("1 L", 28381.21), ("4 L", 92242.15)]),
  ]),
]


def items():
    """Aplana la matriz a la misma estructura de productos.json."""
    out = []
    n = 0
    for grupo, prods in PINTURAS:
        for desc, presentaciones in prods:
            for pres, precio in presentaciones:
                if precio is None:
                    continue
                n += 1
                out.append({
                    "id": f"PIN{n:03d}", "cod": f"PIN{n:03d}",
                    "desc": desc, "pack": "", "pres": pres,
                    "precio": precio, "grupo": grupo,
                    "cat": "pinturas-y-quimicos", "sinStock": False,
                })
    return out
