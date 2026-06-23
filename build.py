#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador estático de CASASILVIAWEB.
Genera el sitio multipágina (home + categorías + nosotros + cómo comprar + sitemap)
a partir de los datos del catálogo. Salida: archivos .html en la raíz (estáticos,
sirven en GitHub Pages / Cloudflare Pages sin build del lado del host).

Uso:  python3 build.py
"""
import json
import urllib.parse
from datetime import date

SITE = "https://www.casasilviaweb.com.ar"
WA = "541166034047"
WA_DISPLAY = "+54 11 6603-4047"
TODAY = date.today().isoformat()

# --------------------------------------------------------------------------- utils
def wa_href(text):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(text, safe="")

def wa_btn(text, source, label, classes="btn btn--wa", inner=None, icon=True):
    ic = '<svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg>' if icon else ""
    inner = inner or "Pedir lista de precios"
    return (f'<a class="{classes}" href="{wa_href(text)}" target="_blank" rel="noopener" '
            f'data-wa="{source}" data-wa-label="{label}">{ic}{inner}</a>')

# --------------------------------------------------------------------------- sprite
SPRITE = r"""<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-wa" viewBox="0 0 32 32"><path d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.55 4.17 1.6 5.98L4 29l8.18-1.55a12 12 0 0 0 3.86.64h.01C22.7 28.08 28.1 22.68 28.1 16.04 28.1 8.4 22.7 3 16.04 3Zm0 21.9c-1.2 0-2.38-.2-3.5-.6l-.25-.1-4.86.92.92-4.73-.16-.25a9.9 9.9 0 0 1-1.52-5.04c0-5.46 4.46-9.9 9.93-9.9 2.65 0 5.14 1.03 7.01 2.9a9.83 9.83 0 0 1 2.9 7.01c0 5.47-4.46 9.9-9.92 9.9Zm5.45-7.4c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49 0 1.47 1.07 2.89 1.22 3.09.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35Z"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></symbol>
<symbol id="i-tag" viewBox="0 0 24 24"><path d="M3 12V5a2 2 0 0 1 2-2h7l9 9-9 9-9-9z"/><circle cx="7.5" cy="7.5" r="1.4" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24"><path d="M3 6h11v9H3zM14 9h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></symbol>
<symbol id="i-headset" viewBox="0 0 24 24"><path d="M4 13v-1a8 8 0 0 1 16 0v1"/><path d="M20 16v1a3 3 0 0 1-3 3h-3"/><rect x="2.5" y="13" width="3.5" height="6" rx="1.2"/><rect x="18" y="13" width="3.5" height="6" rx="1.2"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-box" viewBox="0 0 24 24"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8-5.4 2.8 1-6L3.3 9.4l6-.9z" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-wrench" viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2l-6 6 2.2 2.2 6-6a4 4 0 0 0 5.2-5.4l-2.5 2.5-2-2 2.5-2.5z"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/></symbol>
<symbol id="i-ig" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-fb" viewBox="0 0 24 24"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z" fill="currentColor" stroke="none"/></symbol>
</defs></svg>"""

CONFIG_SCRIPT = """  <script>
    window.CSW_CONFIG = {
      gtmId: "",                    // "GTM-XXXXXXX"
      ga4Id: "",                    // "G-XXXXXXXXXX"
      googleAdsId: "",              // "AW-XXXXXXXXX"
      googleAdsConversionLabel: "", // etiqueta de conversión de Google Ads
      metaPixelId: "",              // Pixel de Facebook/Instagram
      whatsappNumber: \"""" + WA + """"
    };
  </script>"""

# --------------------------------------------------------------------------- head
def head(title, desc, path, og_image="assets/img/og-image.png", preload=None, jsonld=None):
    canonical = f"{SITE}/{path}" if path else f"{SITE}/"
    og_img_url = f"{SITE}/{og_image}"
    preload_tag = f'\n  <link rel="preload" as="image" href="{preload}">' if preload else ""
    ld = ""
    if jsonld:
        ld = '\n  <script type="application/ld+json">\n' + json.dumps(jsonld, ensure_ascii=False, indent=2) + "\n  </script>"
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.classList.add('js')</script>
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="CASASILVIAWEB">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="geo.region" content="AR-B">
  <meta name="geo.placename" content="Tapiales, Buenos Aires">
  <meta name="geo.position" content="-34.695779;-58.512789">
  <meta name="ICBM" content="-34.695779, -58.512789">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="es-AR" href="{canonical}">
  <link rel="alternate" hreflang="x-default" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="CASASILVIAWEB">
  <meta property="og:locale" content="es_AR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_img_url}">
  <meta property="og:image:alt" content="CASASILVIAWEB — Mayorista de fijaciones y aceros">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_img_url}">
  <meta name="theme-color" content="#d21e28">
  <link rel="icon" href="assets/img/logo.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/logo.png">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">{preload_tag}
  <link rel="stylesheet" href="assets/css/styles.css">{ld}
{CONFIG_SCRIPT}
</head>
<body>"""

# --------------------------------------------------------------------------- header / footer
NAV_CATS = [
    ("tornillos-autoperforantes.html", "Tornillos Autoperforantes"),
    ("clavos-y-alambres.html", "Clavos y Alambres"),
    ("tirafondos-y-fijaciones.html", "Tirafondos y Fijaciones"),
    ("hierros-y-mallas.html", "Hierros y Mallas"),
    ("soldadura.html", "Soldadura"),
    ("pinturas-y-quimicos.html", "Pinturas y Químicos"),
]

def header(on_home=False):
    sec = "" if on_home else "index.html"
    home_link = "#inicio" if on_home else "index.html"
    dd = "\n".join(
        f'            <a href="{u}">{n}</a>' for u, n in NAV_CATS
    )
    return f"""  <a class="skip-link" href="#contenido">Saltar al contenido</a>
{SPRITE}
  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="{home_link}" aria-label="CASASILVIAWEB — inicio">
        <img class="brand__logo" src="assets/img/logo.png" alt="Logo de CASASILVIAWEB" width="42" height="42">
        <span class="brand__name"><b>CASASILVIAWEB</b><span>Mayorista</span></span>
      </a>
      <nav class="nav" id="primary-nav" aria-label="Navegación principal">
        <div class="nav__dd">
          <a class="nav__dd-toggle" href="{sec}#productos">Productos <svg class="line" aria-hidden="true"><use href="#i-chev"></use></svg></a>
          <div class="nav__dd-menu">
{dd}
          </div>
        </div>
        <a href="nosotros.html">Nosotros</a>
        <a href="como-comprar.html">Cómo comprar</a>
        <a href="{sec}#contacto">Contacto</a>
      </nav>
      <div class="header__cta">
        {wa_btn("Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.", "header", "Header — Lista de precios", "btn btn--wa", inner='<span class="cta-text">Lista de precios</span>')}
        <button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="primary-nav">
          <svg class="line" aria-hidden="true"><use href="#i-menu"></use></svg>
        </button>
      </div>
    </div>
  </header>
  <main id="contenido">"""

def footer(on_home=False):
    sec = "" if on_home else "index.html"
    prod_links = "\n".join(
        f'            <a href="{u}">{n}</a>' for u, n in NAV_CATS
    )
    return f"""  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="brand" href="{'#inicio' if on_home else 'index.html'}" aria-label="CASASILVIAWEB — inicio">
            <img class="brand__logo" src="assets/img/logo.png" alt="Logo de CASASILVIAWEB" width="42" height="42">
            <span class="brand__name"><b>CASASILVIAWEB</b><span>Mayorista</span></span>
          </a>
          <p>Mayorista de tornillos autoperforantes, clavos, alambres, tirafondos, hierros y mallas, soldadura y pinturas. Respaldo Gerdau, descuentos por volumen y abonás al recibir en Tapiales, Buenos Aires.</p>
          <div class="socials">
            <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp" data-wa="footer-social" data-wa-label="Footer — WhatsApp"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg></a>
            <a href="https://www.instagram.com/casasilviaweb" target="_blank" rel="noopener" aria-label="Instagram"><svg class="line" aria-hidden="true"><use href="#i-ig"></use></svg></a>
            <a href="https://www.facebook.com/casasilviaweb" target="_blank" rel="noopener" aria-label="Facebook"><svg class="fill" aria-hidden="true"><use href="#i-fb"></use></svg></a>
          </div>
        </div>
        <div>
          <h4>Productos</h4>
          <nav class="footer__links" aria-label="Productos">
{prod_links}
          </nav>
        </div>
        <div>
          <h4>Empresa</h4>
          <nav class="footer__links" aria-label="Empresa">
            <a href="nosotros.html">Nosotros</a>
            <a href="como-comprar.html">Cómo comprar</a>
            <a href="{sec}#contacto">Contacto y ubicación</a>
            <a href="{sec}#faq">Preguntas frecuentes</a>
          </nav>
        </div>
        <div>
          <h4>Contacto</h4>
          <nav class="footer__links" aria-label="Contacto">
            <a href="{wa_href('Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.')}" target="_blank" rel="noopener" data-wa="footer" data-wa-label="Footer — WhatsApp">WhatsApp: {WA_DISPLAY}</a>
            <a href="{sec}#contacto">Tuyutí 1025, Tapiales</a>
            <a href="{sec}#contacto">CABA y Gran Buenos Aires</a>
          </nav>
        </div>
      </div>
      <div class="footer__bottom">
        <span>© <span id="year">{date.today().year}</span> CASASILVIAWEB · Mayorista de fijaciones y aceros · Tapiales, Buenos Aires</span>
      </div>
    </div>
  </footer>
""" + WA_FLOAT + """
  <script src="assets/js/main.js" defer></script>
</body>
</html>"""

WA_FLOAT = f"""  <div class="wa-float">
    <div class="wa-pop is-hidden" id="wa-pop" hidden role="dialog" aria-label="Chat de WhatsApp con CASASILVIAWEB">
      <div class="wa-pop__head">
        <span class="wa-pop__avatar"><img src="assets/img/logo.png" alt="CASASILVIAWEB"></span>
        <div><b>CASASILVIAWEB</b><span>En línea</span></div>
        <button class="wa-pop__close" id="wa-pop-close" type="button" aria-label="Cerrar"><svg class="line" aria-hidden="true"><use href="#i-close"></use></svg></button>
      </div>
      <div class="wa-pop__body">
        <div class="wa-pop__msg">¡Hola! 👋 Somos <b>CASASILVIAWEB</b>, mayorista de tornillos, clavos y aceros.<br>¿Te paso la <b>lista de precios</b>?<span class="wa-pop__time">Ahora</span></div>
        {wa_btn("Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.", "popup", "Popup — Lista de precios", "btn btn--wa btn--block", inner="Solicitar lista de precios")}
      </div>
    </div>
    <button class="wa-btn" id="wa-btn" type="button" aria-label="Abrir chat de WhatsApp">
      <span class="wa-badge" id="wa-badge">1</span>
      <svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg>
    </button>
  </div>"""

# --------------------------------------------------------------------------- breadcrumb
def breadcrumb(items):
    # items: list of (name, url|None)
    lis = []
    for i, (name, url) in enumerate(items):
        if url:
            lis.append(f'<li><a href="{url}">{name}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{name}</li>')
    return '<nav class="crumb" aria-label="Migas de pan"><ol>' + "".join(lis) + "</ol></nav>"

# --------------------------------------------------------------------------- componentes
def trust_strip():
    items = [
        ("i-shield", "Calidad Gerdau", "Acero líder del mercado argentino"),
        ("i-box", "Stock y respaldo", "Cualquier cantidad, directo de fábrica"),
        ("i-truck", "Abonás al recibir", "Entrega en CABA y GBA"),
        ("i-tag", "Descuentos por volumen", "Precios mayoristas reales"),
    ]
    cells = "\n".join(
        f'          <div class="trust__item"><span class="trust__icon"><svg class="line" aria-hidden="true"><use href="#{ic}"></use></svg></span>'
        f'<span><b>{t}</b><span>{s}</span></span></div>' for ic, t, s in items)
    return f"""    <section class="trust" aria-label="Por qué elegirnos">
      <div class="container"><div class="trust__grid">
{cells}
      </div></div>
    </section>"""

def faq_block(faqs, center=True, title="Preguntas frecuentes", heading="Lo que más nos consultan"):
    rows = "\n".join(
        f'          <details><summary>{q} <span class="chev"><svg class="line" aria-hidden="true"><use href="#i-plus"></use></svg></span></summary>'
        f'<div class="faq__a">{a}</div></details>' for q, a in faqs)
    cls = "section-head center reveal" if center else "section-head reveal"
    return f"""    <section class="section" id="faq">
      <div class="container">
        <div class="{cls}"><span class="eyebrow">{title}</span><h2>{heading}</h2></div>
        <div class="faq reveal">
{rows}
        </div>
      </div>
    </section>"""

def price_cta(heading="Pedí tu lista de precios mayorista",
              text="Te enviamos la lista actualizada al instante. <strong>Descuentos por volumen</strong>, entrega en CABA y GBA y <strong>abonás al recibir</strong>, también en pedidos grandes.",
              wa_text="Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.",
              source="lista-precios", label="Banner — Lista de precios"):
    return f"""    <section class="section price-cta" id="precios">
      <div class="price-cta__bg" aria-hidden="true"></div>
      <div class="container price-cta__inner">
        <div class="reveal">
          <span class="eyebrow" style="color:#ffe0e2">Lista de precios</span>
          <h2>{heading}</h2>
          <p>{text}</p>
        </div>
        <div class="price-cta__actions reveal">
          {wa_btn(wa_text, source, label, "btn btn--wa btn--lg btn--block", inner="Solicitar lista por WhatsApp")}
          <span class="price-cta__note">{WA_DISPLAY} · Atención directa por WhatsApp</span>
        </div>
      </div>
    </section>"""

def gallery_section(soft=False):
    photos = [
      ("deposito-almacen.webp", "Pallets de pintura y productos de obra apilados en altura en el depósito de CASASILVIAWEB"),
      ("deposito-hierros.webp", "Hierro aletado en barras apilado en profundidad en el depósito de CASASILVIAWEB"),
      ("deposito-mallas.webp", "Gran volumen de mallas electrosoldadas apiladas en el depósito de CASASILVIAWEB"),
      ("deposito-logistica.webp", "Autoelevador cargando mercadería palletizada para despacho"),
    ]
    figs = "\n".join(
      f'          <figure class="gallery__item"><img src="assets/img/{p}" alt="{a}" width="800" height="600" loading="lazy" decoding="async"></figure>'
      for p, a in photos)
    cls = "section section--soft" if soft else "section"
    return f"""    <section class="{cls}" id="deposito" aria-label="Nuestro depósito">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">Nuestro depósito</span><h2>Mercadería lista para entregar</h2><p>Stock propio y respaldo de fábrica para responder a cualquier pedido, grande o chico.</p></div>
        <div class="gallery reveal">
{figs}
        </div>
      </div>
    </section>"""

# --------------------------------------------------------------------------- DATOS DEL CATÁLOGO
CATS = [
  {
    "slug":"tornillos-autoperforantes", "name":"Tornillos Autoperforantes", "kicker":"Línea 01",
    "img":"cat-tornillos.webp", "img_alt":"Caja de tornillos autoperforantes cincados en el depósito de CASASILVIAWEB",
    "core":True,
    "tags":["Hexagonal mecha/aguja","FIX","Drywall metal","Drywall madera","Durlock","Punta con alas","Ensamblador","Deck T25","Hormigón T30","KREG"],
    "title":"Tornillos autoperforantes mayorista | Tipos y medidas | CASASILVIAWEB",
    "desc":"Tornillos autoperforantes al por mayor: hexagonal mecha/aguja, FIX, drywall metal y madera, durlock, ensamblador, deck T25, hormigón T30 y KREG. Todas las medidas. Pedí la lista por WhatsApp.",
    "lead":"Toda la línea de tornillos autoperforantes para chapa, madera, metal, hormigón y construcción en seco. Punta mecha y aguja, en todas las medidas y presentaciones por caja, millar o granel.",
    "subcats":[
      ("Hexagonal punta mecha","Para fijar chapa sobre estructura metálica (perfilería gruesa). Con o sin arandela, EPDM o vulcanizada. Ideal para techos y zinguería."),
      ("Hexagonal punta aguja / ranurada","Para chapa sobre madera o perfil liviano. Cabeza hexagonal para ajustar con tubo o atornillador."),
      ("FIX","Tornillo rápido de fijación liviana (línea amarilla), en medidas chicas para alta producción."),
      ("Drywall para metal","Punta mecha, cabeza trompeta, para placa de durlock sobre perfil de acero (construcción en seco)."),
      ("Drywall para madera","Punta aguja tipo #17, para placa sobre estructura de madera, sin pretaladro."),
      ("Punta mecha con alas","Para fijar maderas o placas gruesas sobre metal: las alas escarian y evitan el desplazamiento."),
      ("Ensamblador","Para muebles y aglomerado, con buen agarre y cabeza avellanada."),
      ("Deck T25","Para deck de madera, con torx T25 y tratamiento para intemperie."),
      ("Hormigón T30","Fijación directa a hormigón y mampostería, torx T30, sin tarugo."),
      ("KREG / Pan framing","Uniones de carpintería (pocket hole) y steel framing."),
    ],
    "measures":"Diámetros del #6 al #14 y largos desde 1/2\" hasta 6\". Presentaciones por caja, millar o granel. Cincados, negros, con arandela EPDM o vulcanizada según la línea.",
    "apps":[
      ("i-home","Techos y zinguería","Chapa sobre estructura metálica o de madera, con arandela de estanqueidad."),
      ("i-box","Construcción en seco","Durlock y steel framing: drywall metal/madera y pan framing."),
      ("i-wrench","Carpintería y muebles","Ensambladores, KREG y tornillos para aglomerado."),
      ("i-shield","Hormigón y deck","Fijación a hormigón (T30) y deck de exterior (T25)."),
    ],
    "faq":[
      ("¿Qué tornillo uso para durlock sobre perfil metálico?","El drywall punta mecha (rosca fina), cabeza trompeta. Para estructura de madera, el drywall punta aguja."),
      ("¿Tienen autoperforantes para chapa de techo?","Sí: hexagonal punta mecha o aguja, con arandela EPDM o vulcanizada para sellar."),
      ("¿Venden por millar o por caja?","Ambos, y a granel según la medida. Consultá presentaciones y descuentos por volumen por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesan los Tornillos Autoperforantes. ¿Me pasan la lista de precios?",
  },
  {
    "slug":"clavos-y-alambres", "name":"Clavos y Alambres", "kicker":"Línea 02",
    "img":"cat-clavos-alambres.webp", "img_alt":"Rollos de alambre galvanizado en stock",
    "core":True,
    "tags":["Punta París","Espiralados","Cabeza de plomo","Electrosoldados","Alambre galvanizado","Alambre de fardo","Púas / Concertina","Alambre MIG"],
    "title":"Clavos y alambres mayorista | Punta París, fardo Nº16 | CASASILVIAWEB",
    "desc":"Clavos y alambres al por mayor: clavo punta París, espiralados, cabeza de plomo, electrosoldados; alambre galvanizado, de fardo Nº16, púas y concertina. Pedí la lista por WhatsApp.",
    "lead":"Clavería y alambres para construcción, encofrados, techos, cercos y embalaje. Dos de nuestros productos más pedidos: el clavo Punta París 2½\" y el alambre de fardo Nº16.",
    "subcats":[
      ("Clavo Punta París","El clásico de obra y carpintería. Todas las medidas, de 1\" a 6\". ★ El 2½\" es uno de los más vendidos."),
      ("Clavos espiralados","Mayor agarre, ideales para encofrados y maderas duras."),
      ("Clavos cabeza de plomo","Nacionales e importados, para fijación de chapa y techos."),
      ("Clavos electrosoldados","En tira para clavadora neumática, alta producción."),
      ("Clavos cabeza chata / perdida / cajonero","Para cajonería, embalaje y terminación."),
      ("Clavos paragua","Cabeza ancha para fijación de chapa y membranas."),
      ("Alambre galvanizado","Línea Acindar, para atado, cercos y construcción. Varios números."),
      ("Alambre de fardo / recocido Nº16","Para encofrados y atado de hierros en obra. Nacional e importado. ★ Muy pedido."),
      ("Alambre de púas y concertina","Seguridad perimetral y cercos."),
      ("Alambre tejido","Cerco romboidal."),
      ("Alambre para soldar / MIG","Para soldadura semiautomática."),
    ],
    "measures":"Clavos de 1\" a 6\". Alambres del Nº8 al Nº18 según la línea, en rollos por kilo o granel. Galvanizado, recocido (fardo) y para soldar.",
    "apps":[
      ("i-box","Construcción y encofrados","Clavos espiralados/París y alambre de fardo Nº16 para armado y atado de hierros."),
      ("i-home","Techos y zinguería","Clavos cabeza de plomo y paragua para chapa."),
      ("i-shield","Cercos y seguridad","Alambre galvanizado, de púas, concertina y tejido."),
      ("i-wrench","Embalaje y carpintería","Clavos cabeza chata, perdida y cajonero."),
    ],
    "faq":[
      ("¿Tienen el clavo Punta París 2½\"?","Sí, es uno de los más vendidos. También todas las demás medidas, por kilo o por bulto."),
      ("¿Qué alambre se usa para encofrados?","El alambre de fardo (recocido) Nº16, para atar armaduras. Lo tenemos nacional e importado."),
      ("¿Venden alambre galvanizado por rollo?","Sí, en rollos y a granel, en distintos números. Consultá medidas por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesan los Clavos y Alambres. ¿Me pasan la lista de precios?",
  },
  {
    "slug":"tirafondos-y-fijaciones", "name":"Tirafondos y Fijaciones", "kicker":"Línea 03",
    "img":"cat-tirafondos.webp", "img_alt":"Tirafondos y bulones de acero cincado",
    "core":True,
    "tags":["Tirafondos hexagonales","Tarugos","Tuercas","Arandelas","Grampas","Gancho J","Torniquetes","Mariposas"],
    "title":"Tirafondos, tarugos y fijaciones mayorista | CASASILVIAWEB",
    "desc":"Tirafondos cabeza hexagonal (DIN 571), tarugos, tuercas, arandelas, grampas, ganchos y torniquetes al por mayor. Todas las medidas. Pedí la lista por WhatsApp.",
    "lead":"Fijaciones de alta resistencia y todos los accesorios de bulonería para sujetar soportes pesados, instalaciones y estructuras.",
    "subcats":[
      ("Tirafondos cabeza hexagonal (DIN 571)","Para madera y mampostería (con tarugo). Para soportes pesados: aires, toldos, soportes de TV, antenas."),
      ("Tarugos","De nylon, en todas las medidas, para fijar en pared y hormigón."),
      ("Tuercas hexagonales","Bulonería general, distintas medidas y calidades."),
      ("Arandelas","Planas y de presión."),
      ("Grampas / Grampas Omega","Para fijación de caños y conductos."),
      ("Gancho J","Para sujeción de chapa y tirantes."),
      ("Torniquetes","Para tensado de alambre y cables."),
      ("Mariposas","Fijación en placas huecas (durlock)."),
    ],
    "measures":"Tirafondos de 3/16\" a 3/8\" de diámetro y largos de 1\" a 8\". Tarugos, tuercas y arandelas en todas las medidas. Cincados.",
    "apps":[
      ("i-shield","Soportes pesados","Aires acondicionados, toldos, soportes de TV y antenas, con tarugo."),
      ("i-wrench","Instalaciones","Grampas y ganchos para caños, conductos y chapa."),
      ("i-box","Estructuras y cercos","Torniquetes para tensado; bulonería general."),
      ("i-home","Construcción en seco","Mariposas y tarugos para placas y mampostería."),
    ],
    "faq":[
      ("¿Qué necesito para colgar algo pesado en la pared?","Tirafondo hexagonal + tarugo del diámetro correspondiente. Te asesoramos según el peso y el material."),
      ("¿Tienen tarugos en todas las medidas?","Sí, de nylon en distintos diámetros, junto con tirafondos, tuercas y arandelas."),
      ("¿Venden bulonería suelta o por caja?","Por caja y a granel según la medida. Consultá por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesan los Tirafondos y fijaciones. ¿Me pasan la lista de precios?",
  },
  {
    "slug":"hierros-y-mallas", "name":"Hierros y Mallas", "kicker":"Línea 04",
    "img":"cat-hierros-mallas.webp", "img_alt":"Mallas electrosoldadas apiladas en el depósito",
    "core":True,
    "tags":["Hierro aletado","Hierro dulce","Varilla","Mallas electrosoldadas","Estribos","Línea Gerdau"],
    "title":"Hierros y mallas mayorista | Gerdau, Sima | CASASILVIAWEB",
    "desc":"Hierro aletado y dulce, varillas, mallas electrosoldadas (Sima) y estribos al por mayor, línea Gerdau. Para losas, columnas y contrapisos. Pedí la lista por WhatsApp.",
    "lead":"Acero para estructura de hormigón armado: hierro aletado y dulce, mallas electrosoldadas y estribos, con respaldo de Gerdau. Para pedidos grandes despachamos directo desde la acería.",
    "subcats":[
      ("Hierro aletado (nervado)","Para hormigón armado: columnas, vigas y losas. Diámetros según proyecto."),
      ("Hierro dulce / liso","Para estribos, herrería y usos generales."),
      ("Varillas","Barras de 12 m para construcción."),
      ("Mallas electrosoldadas (Sima)","Para losas, pisos y contrapisos. Distintas separaciones y diámetros (ej. 15x25, 18x18)."),
      ("Estribos","Armados para columnas y vigas."),
      ("Línea Gerdau","Acero con calidad certificada de una de las marcas líderes del país."),
    ],
    "measures":"Hierro aletado de Ø4,2 a Ø25 mm; varillas de 12 m. Mallas electrosoldadas en distintas medidas y diámetros. Consultá medidas y armados por WhatsApp.",
    "apps":[
      ("i-box","Hormigón armado","Columnas, vigas y losas con hierro aletado y estribos."),
      ("i-home","Pisos y contrapisos","Mallas electrosoldadas para losas y solados."),
      ("i-wrench","Herrería","Hierro dulce y liso para trabajos de taller."),
      ("i-truck","Pedidos grandes","Despacho directo desde la acería, con flete, y abonás al recibir."),
    ],
    "faq":[
      ("¿Trabajan con Gerdau?","Sí. Gerdau es una de las principales marcas de acero del país, con calidad certificada."),
      ("¿Hacen entregas grandes de hierro?","Sí. En pedidos grandes despachamos directo desde la acería con flete, y abonás al recibir."),
      ("¿Qué malla uso para un contrapiso?","Depende de la luz y la carga. Te orientamos con la separación y el diámetro por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesan los Hierros y Mallas. ¿Me pasan la lista de precios?",
  },
  {
    "slug":"soldadura", "name":"Soldadura", "kicker":"Línea 05",
    "img":"cat-soldadura.webp", "img_alt":"Productos de soldadura: electrodos y alambre MIG",
    "core":False,
    "tags":["Electrodos Gerdau","E-6013","Alambre MIG","Accesorios"],
    "title":"Electrodos y alambre MIG mayorista | Soldadura | CASASILVIAWEB",
    "desc":"Electrodos Gerdau (E-6013) y alambre MIG al por mayor para soldadura al arco y semiautomática. Pedí la lista por WhatsApp.",
    "lead":"Insumos de soldadura para herrería, estructuras metálicas y reparaciones.",
    "subcats":[
      ("Electrodos Gerdau E-6013","Para soldadura al arco, uso general. Distintos diámetros (2,0 / 2,5 / 3,25 mm)."),
      ("Alambre MIG","Para soldadura semiautomática, en rollos (0,8 / 0,9 mm)."),
      ("Accesorios","Consultá disponibilidad de insumos y accesorios de soldadura."),
    ],
    "measures":"Electrodos por kilo y por caja; alambre MIG en rollos. Consultá diámetros y marcas por WhatsApp.",
    "apps":[
      ("i-wrench","Herrería","Electrodos para uso general y reparaciones."),
      ("i-box","Estructuras metálicas","Soldadura de perfiles y armados."),
    ],
    "faq":[
      ("¿Tienen electrodos Gerdau?","Sí, E-6013 en distintos diámetros, por kilo y por caja."),
      ("¿Venden alambre MIG?","Sí, en rollos de 0,8 y 0,9 mm. Consultá stock por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesa la línea de Soldadura (electrodos / MIG). ¿Me pasan la lista de precios?",
  },
  {
    "slug":"pinturas-y-quimicos", "name":"Pinturas y Químicos", "kicker":"Línea 06",
    "img":"cat-pinturas.webp", "img_alt":"Pallets de pintura y productos de obra en el depósito",
    "core":False,
    "tags":["Pinturas de obra","Impermeabilizantes","Mezcla adhesiva","Químicos para construcción"],
    "title":"Pinturas y químicos para obra mayorista | CASASILVIAWEB",
    "desc":"Pinturas de obra, impermeabilizantes y mezcla adhesiva al por mayor para construcción y terminaciones. Pedí la lista por WhatsApp.",
    "lead":"Complementamos la obra con pinturas y químicos para construcción y terminaciones.",
    "subcats":[
      ("Pinturas de obra","Líneas para interior y exterior. Consultá marcas y medidas disponibles."),
      ("Impermeabilizantes","Para techos y superficies expuestas."),
      ("Mezcla adhesiva","Para colocación y pegado en obra."),
    ],
    "measures":"Distintas presentaciones y marcas. Consultá disponibilidad y precios por WhatsApp.",
    "apps":[
      ("i-home","Terminaciones","Pinturas para interior y exterior."),
      ("i-shield","Impermeabilización","Productos para techos y superficies expuestas."),
    ],
    "faq":[
      ("¿Qué marcas de pintura manejan?","Trabajamos distintas líneas de obra. Consultá disponibilidad y precios por WhatsApp."),
      ("¿Tienen impermeabilizantes y adhesivos?","Sí, productos químicos para construcción. Consultá stock por WhatsApp."),
    ],
    "wa_text":"Hola CASASILVIAWEB! Me interesa la línea de Pinturas y químicos. ¿Me pasan la lista de precios?",
  },
]
CAT_BY_SLUG = {c["slug"]: c for c in CATS}

# --------------------------------------------------------------------------- render helpers
def sub_grid(subcats):
    cards = "\n".join(
        f'          <div class="sub-card"><h3>{n}</h3><p>{d}</p></div>' for n, d in subcats)
    return f'        <div class="sub-grid">\n{cards}\n        </div>'

def apps_list(apps):
    rows = "\n".join(
        f'            <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#{ic}"></use></svg></span>'
        f'<div><b>{t}</b><p>{x}</p></div></div>' for ic, t, x in apps)
    return f'          <div class="feature-list">\n{rows}\n          </div>'

def cat_card(c):
    tags = "".join(f"<li>{t}</li>" for t in c["tags"][:8])
    return f"""          <article class="cat reveal" id="{c['slug']}">
            <span class="cat__corner" aria-hidden="true"></span>
            <div class="cat__img"><img src="assets/img/{c['img']}" alt="{c['img_alt']}" width="900" height="650" loading="lazy" decoding="async"></div>
            <div class="cat__body">
              <span class="cat__kicker">{c['kicker']}</span>
              <h3>{c['name']}</h3>
              <ul class="cat__tags">{tags}</ul>
              <a class="cat__link" href="{c['slug']}.html">Ver línea <svg class="line" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
            </div>
          </article>"""

# --------------------------------------------------------------------------- página de categoría
def render_category(c):
    crumb = breadcrumb([("Inicio","index.html"),("Productos","index.html#productos"),(c["name"],None)])
    related = [x for x in CATS if x["slug"] != c["slug"]][:5]
    rel_links = " · ".join(f'<a href="{r["slug"]}.html">{r["name"]}</a>' for r in related)
    sections = f"""    <section class="section section--soft">
      <div class="container">
        {crumb}
        <div class="split cat-intro">
          <div class="reveal">
            <span class="eyebrow">{c['kicker']} · Mayorista</span>
            <h1>{c['name']}</h1>
            <p class="lead-big">{c['lead']}</p>
            <div class="cat-intro__actions">
              {wa_btn(c['wa_text'], 'cat-'+c['slug'], 'Categoría '+c['name'], 'btn btn--wa btn--lg', inner='Pedir lista de precios')}
              <a class="btn btn--ghost-dark btn--lg" href="como-comprar.html">Cómo comprar</a>
            </div>
          </div>
          <div class="split__media reveal">
            <img src="assets/img/{c['img']}" alt="{c['img_alt']}" width="900" height="650" loading="eager" fetchpriority="high">
          </div>
        </div>
      </div>
    </section>
{trust_strip()}
    <section class="section">
      <div class="container">
        <div class="section-head reveal"><span class="eyebrow">Tipos y líneas</span><h2>Qué tenemos en {c['name'].lower()}</h2><p>Todas las medidas y presentaciones, por caja, millar o granel. Pedí la lista de precios por WhatsApp.</p></div>
        <div class="reveal">
{sub_grid(c['subcats'])}
        </div>
      </div>
    </section>
    <section class="section section--soft">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Aplicaciones</span>
            <h2>Para qué se usa</h2>
{apps_list(c['apps'])}
          </div>
          <div class="reveal">
            <div class="measures-box">
              <span class="measures-box__label"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg> Medidas y presentaciones</span>
              <p>{c['measures']}</p>
              {wa_btn(c['wa_text'], 'cat-'+c['slug']+'-medidas', 'Categoría '+c['name']+' — Medidas', 'btn btn--wa btn--block', inner='Consultar medidas y precios')}
            </div>
          </div>
        </div>
      </div>
    </section>
{faq_block(c['faq'], center=True, heading='Sobre '+c['name'].lower())}
{price_cta(heading='Pedí la lista de '+c['name'].lower(), wa_text=c['wa_text'], source='cat-'+c['slug']+'-cta', label='CTA '+c['name'])}
    <section class="section">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">Más líneas</span><h2>Seguí viendo el catálogo</h2></div>
        <p class="related reveal">{rel_links}</p>
      </div>
    </section>"""
    # JSON-LD
    jsonld = {"@context":"https://schema.org","@graph":[
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":"Productos","item":f"{SITE}/#productos"},
        {"@type":"ListItem","position":3,"name":c["name"],"item":f"{SITE}/{c['slug']}.html"},
      ]},
      {"@type":"Product","name":c["name"],"image":f"{SITE}/assets/img/{c['img']}",
       "description":c["desc"],"category":"Fijaciones y aceros",
       "brand":{"@type":"Brand","name":"Gerdau"},
       "offers":{"@type":"AggregateOffer","priceCurrency":"ARS","availability":"https://schema.org/InStock",
                 "seller":{"@id":f"{SITE}/#business"}}},
      {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faq"]]},
    ]}
    html = (head(c["title"], c["desc"], f"{c['slug']}.html", og_image=f"assets/img/{c['img']}",
                 preload=f"assets/img/{c['img']}", jsonld=jsonld)
            + header(on_home=False) + sections + footer(on_home=False))
    return html

# --------------------------------------------------------------------------- HOME
def render_home():
    core = [c for c in CATS if c.get("core")]
    extra = [c for c in CATS if not c.get("core")]
    cards = "\n".join(cat_card(c) for c in core)
    extra_links = " · ".join(f'<a href="{c["slug"]}.html">{c["name"]}</a>' for c in extra)
    home_faq = [
      ("¿Cuál es el pedido mínimo? ¿A quién le venden?","Somos mayoristas: el pedido mínimo es de $300.000 y los pedidos suelen ir de $300.000 a $4.000.000. Atendemos ferreterías, corralones, zingueros, madereras, distribuidores y constructoras."),
      ("¿Cómo pido la lista de precios?","Escribinos por WhatsApp al "+WA_DISPLAY+" y te enviamos la lista actualizada con las bonificaciones vigentes."),
      ("¿Qué productos tienen?","Tornillos autoperforantes, clavos, alambres, tirafondos, hierros y mallas. También soldadura, pinturas y accesorios (tarugos, tuercas, arandelas, grampas)."),
      ("¿Hacen envíos y cómo es el pago?","Entregamos en CABA y GBA y abonás al recibir, también en pedidos grandes (que salen directo desde la acería). Coordinás todo por WhatsApp."),
      ("¿Hacen descuentos por volumen?","Sí. Trabajamos con descuentos por volumen de compra. Pedí tu escala por WhatsApp junto con la lista de precios."),
      ("¿Dónde están ubicados?","Estamos en Tuyutí 1025, Tapiales, Zona Oeste del Gran Buenos Aires. Mirá el mapa más abajo."),
    ]
    sections = f"""    <section class="hero" id="inicio">
      <div class="hero__bg"><img src="assets/img/hero-deposito.webp" alt="" aria-hidden="true" fetchpriority="high"></div>
      <div class="container hero__inner">
        <span class="eyebrow">Mayorista de fijaciones y aceros</span>
        <h1>Tornillos, clavos y aceros <span class="accent">al por mayor</span></h1>
        <p class="hero__lead">Somos mayoristas de fijaciones y aceros con <strong>respaldo de fábrica (Gerdau)</strong>: tornillos, clavos, alambres, tirafondos, hierros y mallas. Entregamos en CABA y GBA y <strong>abonás al recibir</strong>, con descuentos por volumen.</p>
        <div class="hero__actions">
          {wa_btn("Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.", "hero", "Hero — Lista de precios", "btn btn--wa btn--lg", inner="Pedir lista de precios")}
          <a class="btn btn--ghost btn--lg" href="#productos">Ver productos</a>
        </div>
        <div class="hero__stats">
          <div class="hero__stat"><b>Respaldo Gerdau</b><span>Acero líder, primera calidad</span></div>
          <div class="hero__stat"><b>Abonás al recibir</b><span>Incluso en pedidos grandes</span></div>
          <div class="hero__stat"><b>Envío CABA y GBA</b><span>Descuentos por volumen</span></div>
        </div>
      </div>
    </section>
{trust_strip()}
    <section class="section" id="productos">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Nuestro catálogo</span>
          <h2>Todo en fijaciones y aceros</h2>
          <p>Seis líneas de producto, en todas las medidas y para cada trabajo. Entrá a la categoría que necesites o pedí la lista por WhatsApp.</p>
        </div>
        <div class="cats">
{cards}
        </div>
        <p class="more-lines reveal">También trabajamos: {extra_links}</p>
      </div>
    </section>
    <section class="section section--soft" id="calidad">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Calidad y respaldo</span>
            <h2>Respaldo de fábrica, precios de mayorista</h2>
            <p>Trabajamos con <strong>Gerdau</strong>, una de las principales marcas de acero del país, con Sistema de Gestión de Calidad certificado según <strong>norma ISO 9001 otorgada por IRAM</strong>. Tenemos stock propio y entregamos <strong>cualquier cantidad</strong>: los pedidos grandes se despachan directo desde la acería.</p>
            <div class="feature-list">
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-shield"></use></svg></span><div><b>Calidad Gerdau</b><p>Acero de primera, una de las marcas líderes del mercado argentino.</p></div></div>
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-box"></use></svg></span><div><b>Stock y respaldo de fábrica</b><p>Entregamos cualquier cantidad; los pedidos grandes salen directo de la acería.</p></div></div>
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg></span><div><b>Comprás tranquilo</b><p>Abonás al recibir, también en pedidos grandes, con descuentos por volumen.</p></div></div>
            </div>
            <div class="certs" aria-label="Calidad y certificaciones">
              <span class="cert">Gerdau</span><span class="cert">ISO 9001 · IRAM</span><span class="cert">Gestión Ambiental</span><span class="cert">Gestión SySO</span><span class="cert">Acero sustentable</span>
            </div>
          </div>
          <div class="split__media reveal">
            <img src="assets/img/calidad-stock.webp" alt="Hierros y acero en stock en el depósito de CASASILVIAWEB" width="1000" height="750" loading="lazy" decoding="async">
            <div class="badge"><span class="trust__icon" style="background:var(--red-tint)"><svg class="line" aria-hidden="true" style="color:var(--red)"><use href="#i-shield"></use></svg></span><div><b>Calidad certificada</b><span>ISO 9001 · IRAM</span></div></div>
          </div>
        </div>
      </div>
    </section>
{gallery_section()}
    <section class="section section--soft" id="como-comprar" aria-label="Cómo comprar">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">Cómo comprar</span><h2>Comprás en 3 pasos</h2><p>Nos escribís por WhatsApp, te pasamos la lista y coordinamos la entrega.</p></div>
        <ol class="steps reveal">
          <li class="step"><span class="step__num">1</span><span class="step__ic"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg></span><h3>Escribinos por WhatsApp</h3><p>Pedinos la lista de precios y contanos qué necesitás.</p></li>
          <li class="step"><span class="step__num">2</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg></span><h3>Armás tu pedido</h3><p>Te pasamos precios y descuentos por volumen, y coordinamos la entrega.</p></li>
          <li class="step"><span class="step__num">3</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><h3>Abonás al recibir</h3><p>Te llevamos el pedido a CABA o GBA y pagás cuando lo recibís.</p></li>
        </ol>
        <p class="center-cta reveal"><a class="btn btn--ghost-dark" href="como-comprar.html">Ver envíos, pagos y mínimos →</a></p>
      </div>
    </section>
{price_cta()}
{faq_block(home_faq)}
{location_section()}"""
    jsonld = {"@context":"https://schema.org","@graph":[ BUSINESS_LD, WEBSITE_LD,
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in home_faq]} ]}
    return head("Tornillos, clavos y aceros al por mayor | CASASILVIAWEB",
                "Mayorista de fijaciones y aceros con respaldo Gerdau: tornillos, clavos, alambres, tirafondos, hierros y mallas. Entrega en CABA y GBA y abonás al recibir. Pedí la lista por WhatsApp.",
                "", preload="assets/img/hero-deposito.webp", jsonld=jsonld) + header(on_home=True) + sections + footer(on_home=True)

def location_section():
    return f"""    <section class="section" id="contacto">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">¿Dónde estamos?</span>
          <h2>Visitanos o coordiná tu pedido</h2>
          <p>Estamos en <strong>Tuyutí 1025, Tapiales</strong> (La Matanza). Entregamos en <strong>CABA y todo el Gran Buenos Aires</strong> y abonás al recibir; los pedidos grandes salen directo desde la acería. Coordinás envío o retiro por WhatsApp.</p>
        </div>
        <div class="loc">
          <div class="loc__card reveal">
            <div class="loc__list">
              <div class="loc__row"><span class="ic"><svg class="line" aria-hidden="true"><use href="#i-pin"></use></svg></span><div><b>Dirección</b><span>Tuyutí 1025, Tapiales (B1770)<br>Zona Oeste · Gran Buenos Aires</span></div></div>
              <div class="loc__row"><span class="ic"><svg class="fill" aria-hidden="true"><use href="#i-phone"></use></svg></span><div><b>WhatsApp</b><a href="{wa_href('Hola CASASILVIAWEB! Quiero coordinar un pedido.')}" target="_blank" rel="noopener" data-wa="ubicacion" data-wa-label="Ubicación — WhatsApp">{WA_DISPLAY}</a></div></div>
              <div class="loc__row"><span class="ic"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg></span><div><b>Modalidad</b><span>Venta mayorista · Abonás al recibir</span></div></div>
              <div class="loc__row"><span class="ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><div><b>Cobertura</b><span>CABA y Gran Buenos Aires · Envío o retiro</span></div></div>
            </div>
            {wa_btn("Hola CASASILVIAWEB! Quiero coordinar un pedido.", "ubicacion-cta", "Ubicación — Escribinos", "btn btn--wa btn--block", inner="Escribinos por WhatsApp")}
            <a class="btn btn--block" style="--btn-bg:var(--ink-900);margin-top:10px" href="https://www.google.com/maps/search/?api=1&query=Tuyut%C3%AD%201025%2C%20Tapiales%2C%20Buenos%20Aires" target="_blank" rel="noopener"><svg class="line" aria-hidden="true"><use href="#i-pin"></use></svg> Cómo llegar</a>
          </div>
          <div class="loc__map reveal">
            <iframe title="Ubicación de CASASILVIAWEB en Tuyutí 1025, Tapiales" src="https://www.google.com/maps?q=Tuyut%C3%AD%201025,%20Tapiales,%20Buenos%20Aires,%20Argentina&z=16&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </section>"""

# JSON-LD reutilizable
BUSINESS_LD = {
  "@type":["Organization","HardwareStore"],"@id":f"{SITE}/#business","name":"CASASILVIAWEB",
  "alternateName":"Casa Silvia Web","slogan":"Mayorista de fijaciones y aceros. Abonás al recibir.",
  "knowsAbout":["Tornillos autoperforantes","Clavos","Alambres","Tirafondos","Hierros","Mallas electrosoldadas","Soldadura","Pinturas","Fijaciones","Acero Gerdau","Venta mayorista"],
  "description":"Mayorista de tornillos autoperforantes, clavos, alambres, tirafondos, hierros y mallas en Tapiales, Buenos Aires.",
  "url":f"{SITE}/","logo":f"{SITE}/assets/img/logo.png","image":f"{SITE}/assets/img/og-image.png",
  "telephone":"+541166034047","priceRange":"$$","currenciesAccepted":"ARS","paymentAccepted":"Efectivo, Transferencia",
  "areaServed":["Tapiales","San Justo","Ramos Mejía","Lomas del Mirador","Villa Madero","Ciudad Evita","Isidro Casanova","González Catán","La Matanza","Zona Oeste","Gran Buenos Aires","CABA","Argentina"],
  "address":{"@type":"PostalAddress","streetAddress":"Tuyutí 1025","addressLocality":"Tapiales","addressRegion":"Buenos Aires","postalCode":"B1770","addressCountry":"AR"},
  "geo":{"@type":"GeoCoordinates","latitude":-34.695779,"longitude":-58.512789},
  "hasMap":"https://www.google.com/maps?q=-34.695779,-58.512789",
  "contactPoint":{"@type":"ContactPoint","telephone":"+541166034047","contactType":"sales","availableLanguage":["Spanish"]},
  "sameAs":["https://wa.me/541166034047","https://www.instagram.com/casasilviaweb","https://www.facebook.com/casasilviaweb"],
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Catálogo mayorista","itemListElement":[
    {"@type":"Offer","itemOffered":{"@type":"Product","image":f"{SITE}/assets/img/{c['img']}","name":c["name"],"url":f"{SITE}/{c['slug']}.html","description":c["desc"]}} for c in CATS]},
}
WEBSITE_LD = {"@type":"WebSite","@id":f"{SITE}/#website","url":f"{SITE}/","name":"CASASILVIAWEB","inLanguage":"es-AR","publisher":{"@id":f"{SITE}/#business"}}

# --------------------------------------------------------------------------- páginas simples
def render_nosotros():
    crumb = breadcrumb([("Inicio","index.html"),("Nosotros",None)])
    sections = f"""    <section class="section section--soft">
      <div class="container">
        {crumb}
        <div class="section-head reveal"><span class="eyebrow">Nosotros</span><h1>Mayoristas de fijaciones y aceros</h1>
          <p>En <strong>CASASILVIAWEB</strong> abastecemos a ferreterías, corralones, zingueros, madereras, distribuidores y constructoras con tornillos, clavos, alambres, tirafondos, hierros, mallas, soldadura y pinturas. Trabajamos al por mayor, con precios reales y atención directa por WhatsApp.</p>
        </div>
        <div class="reveal">
          <div class="feature-list feature-list--2col">
            <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-shield"></use></svg></span><div><b>Respaldo Gerdau</b><p>Trabajamos con una de las principales marcas de acero del país, con calidad certificada (ISO 9001 / IRAM).</p></div></div>
            <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-box"></use></svg></span><div><b>Stock y respaldo de fábrica</b><p>Stock propio y, con el respaldo de nuestros proveedores, entregamos cualquier cantidad en 24 h. Los pedidos grandes salen directo de la acería.</p></div></div>
            <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><div><b>Abonás al recibir</b><p>Entregamos en CABA y todo el Gran Buenos Aires y pagás cuando recibís el pedido, también en compras grandes.</p></div></div>
            <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg></span><div><b>Precios mayoristas</b><p>Descuentos por volumen y bonificaciones. Pedí tu escala junto con la lista de precios.</p></div></div>
          </div>
        </div>
      </div>
    </section>
{trust_strip()}
{gallery_section()}
{price_cta(heading="¿Querés trabajar con nosotros?", text="Pedí la lista de precios mayorista por WhatsApp. Te respondemos al instante.")}
{location_section()}"""
    jsonld = {"@context":"https://schema.org","@graph":[BUSINESS_LD,
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":"Nosotros","item":f"{SITE}/nosotros.html"}]}]}
    return head("Nosotros | Mayorista de fijaciones y aceros | CASASILVIAWEB",
                "CASASILVIAWEB, mayorista de tornillos, clavos, alambres, tirafondos, hierros y mallas en Tapiales. Respaldo Gerdau, stock, descuentos por volumen y abonás al recibir.",
                "nosotros.html", jsonld=jsonld) + header() + sections + footer()

def render_como_comprar():
    crumb = breadcrumb([("Inicio","index.html"),("Cómo comprar",None)])
    faqs = [
      ("¿Cuál es el pedido mínimo?","El pedido mínimo es de $300.000. Los pedidos suelen ir de $300.000 a $4.000.000."),
      ("¿Qué formas de pago aceptan?","Efectivo y transferencia. Lo más cómodo: abonás al recibir el pedido."),
      ("¿A qué zonas entregan?","CABA y todo el Gran Buenos Aires. Los pedidos grandes se despachan directo desde la acería con flete."),
      ("¿Hacen descuentos por volumen?","Sí, tenemos escalas de descuento según el monto de compra. Pedí la tuya por WhatsApp."),
    ]
    sections = f"""    <section class="section section--soft">
      <div class="container">
        {crumb}
        <div class="section-head center reveal"><span class="eyebrow">Cómo comprar</span><h1>Comprar es simple</h1><p>Todo se coordina por WhatsApp. Te pasamos la lista, armás el pedido y <strong>abonás al recibir</strong>.</p></div>
        <ol class="steps reveal">
          <li class="step"><span class="step__num">1</span><span class="step__ic"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg></span><h3>Escribinos por WhatsApp</h3><p>Pedinos la lista de precios y contanos qué necesitás.</p></li>
          <li class="step"><span class="step__num">2</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg></span><h3>Armás tu pedido</h3><p>Te pasamos precios y descuentos por volumen, y coordinamos la entrega.</p></li>
          <li class="step"><span class="step__num">3</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><h3>Abonás al recibir</h3><p>Te llevamos el pedido a CABA o GBA y pagás cuando lo recibís.</p></li>
        </ol>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Condiciones</span><h2>Envíos, pagos y mínimos</h2>
            <div class="feature-list">
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg></span><div><b>Pedido mínimo</b><p>Desde $300.000. Pedidos habituales de $300.000 a $4.000.000.</p></div></div>
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><div><b>Envíos</b><p>CABA y Gran Buenos Aires. Pedidos grandes directo desde la acería con flete.</p></div></div>
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg></span><div><b>Pago</b><p>Abonás al recibir (efectivo o transferencia), también en pedidos grandes.</p></div></div>
              <div class="feature"><span class="feature__ic"><svg class="line" aria-hidden="true"><use href="#i-box"></use></svg></span><div><b>Descuentos por volumen</b><p>Escalas según el monto de compra. Pedí la tuya por WhatsApp.</p></div></div>
            </div>
          </div>
          <div class="split__media reveal"><img src="assets/img/calidad-stock.webp" alt="Depósito de CASASILVIAWEB con stock para entrega" width="1000" height="750" loading="lazy" decoding="async"></div>
        </div>
      </div>
    </section>
{faq_block(faqs, heading='Sobre la compra')}
{price_cta()}"""
    jsonld = {"@context":"https://schema.org","@graph":[
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":"Cómo comprar","item":f"{SITE}/como-comprar.html"}]},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]}
    return head("Cómo comprar | Envíos, pagos y mínimos | CASASILVIAWEB",
                "Cómo comprar al por mayor en CASASILVIAWEB: pedís por WhatsApp, te pasamos la lista, coordinás y abonás al recibir. Envíos a CABA y GBA, descuentos por volumen.",
                "como-comprar.html", jsonld=jsonld) + header() + sections + footer()

# --------------------------------------------------------------------------- sitemap
def render_sitemap():
    urls = [("", "1.0")] + [(f"{c['slug']}.html","0.8") for c in CATS] + [("nosotros.html","0.6"),("como-comprar.html","0.6")]
    body = "\n".join(
      f'  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>'
      for p, pr in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'

# --------------------------------------------------------------------------- main
def main():
    import os
    out = {}
    out["index.html"] = render_home()
    out["nosotros.html"] = render_nosotros()
    out["como-comprar.html"] = render_como_comprar()
    for c in CATS:
        out[f"{c['slug']}.html"] = render_category(c)
    out["sitemap.xml"] = render_sitemap()
    for fn, content in out.items():
        with open(fn, "w", encoding="utf-8") as f:
            f.write(content)
        print("escrito:", fn, f"({len(content)//1024} KB)")
    print(f"\nOK — {len(out)} archivos generados.")

if __name__ == "__main__":
    main()

