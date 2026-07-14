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
import os
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
<symbol id="i-cart" viewBox="0 0 24 24"><path d="M3 4h2.4l2.2 11.2a1.6 1.6 0 0 0 1.6 1.3h8.7a1.6 1.6 0 0 0 1.6-1.2L21.5 8H6.1"/><circle cx="9.8" cy="20.4" r="1.5" fill="currentColor" stroke="none"/><circle cx="17.6" cy="20.4" r="1.5" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-trash" viewBox="0 0 24 24"><path d="M4 7h16M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M6.5 7l.9 12a1.6 1.6 0 0 0 1.6 1.5h6a1.6 1.6 0 0 0 1.6-1.5l.9-12"/><path d="M10 11v6M14 11v6"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/></symbol>
<symbol id="i-minus" viewBox="0 0 24 24"><path d="M5 12h14"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8-5.4 2.8 1-6L3.3 9.4l6-.9z" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-wrench" viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2l-6 6 2.2 2.2 6-6a4 4 0 0 0 5.2-5.4l-2.5 2.5-2-2 2.5-2.5z"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/></symbol>
<symbol id="i-ig" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-fb" viewBox="0 0 24 24"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z" fill="currentColor" stroke="none"/></symbol>
<symbol id="p-screw-hex" viewBox="0 0 24 24"><path d="M8 3h8l1.6 3H6.4zM6.6 6h10.8M10.3 6v10.8M13.7 6v10.8M10.3 16.8 12 21l1.7-4.2M10.3 9.2h3.4M10.3 12h3.4M10.3 14.8h3.4"/></symbol>
<symbol id="p-screw" viewBox="0 0 24 24"><path d="M7 3h10M7 3l3.2 3.2M17 3l-3.2 3.2M10.2 6.2v10.6M13.8 6.2v10.6M10.2 16.8 12 21l1.8-4.2M10.2 9.2h3.6M10.2 12h3.6M10.2 14.8h3.6"/></symbol>
<symbol id="p-screw-drywall" viewBox="0 0 24 24"><path d="M6.5 3h11M6.5 3c1.2 2.6 3.1 3.4 5.5 3.4s4.3-.8 5.5-3.4M10.3 6.4v10.4M13.7 6.4v10.4M10.3 16.8 12 21l1.7-4.2M10.3 9.4h3.4M10.3 12.1h3.4M10.3 14.8h3.4"/></symbol>
<symbol id="p-screw-pan" viewBox="0 0 24 24"><rect x="8" y="3" width="8" height="3" rx="1.4"/><path d="M7.5 6h9M10.3 6v10.8M13.7 6v10.8M10.3 16.8 12 21l1.7-4.2M10.3 9.2h3.4M10.3 12h3.4M10.3 14.8h3.4"/></symbol>
<symbol id="p-lag" viewBox="0 0 24 24"><path d="M8.2 3h7.6l1.4 2.6H6.8zM10 5.6v11M14 5.6v11M10 8.4l4 1.2M10 11.2l4 1.2M10 14l4 1.2M10 16.6 12 21l2-4.4"/></symbol>
<symbol id="p-nut" viewBox="0 0 24 24"><path d="M12 3l7.2 4.2v9.6L12 21l-7.2-4.2V7.2z"/><circle cx="12" cy="12" r="3.4"/></symbol>
<symbol id="p-washer" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.4"/></symbol>
<symbol id="p-plug" viewBox="0 0 24 24"><path d="M8.5 3h7M9 3v10.5l1.2 6.7a1.9 1.9 0 0 0 3.6 0l1.2-6.7V3M9 6.2h6M9 9h6M9 11.8h6M12 14.5v3.5"/></symbol>
<symbol id="p-clamp" viewBox="0 0 24 24"><path d="M4.5 18.5h4.9l-1.3-2.6a5.6 5.6 0 1 1 7.8 0l-1.3 2.6h4.9"/></symbol>
<symbol id="p-staple" viewBox="0 0 24 24"><path d="M6.2 20.5V9.8a5.8 5.8 0 0 1 11.6 0v10.7"/></symbol>
<symbol id="p-hook" viewBox="0 0 24 24"><path d="M11.6 3h6M14.6 3v9.4a4.3 4.3 0 0 1-8.6 0v-1.2"/></symbol>
<symbol id="p-turnbuckle" viewBox="0 0 24 24"><ellipse cx="12" cy="12" rx="6" ry="3.4"/><path d="M2.5 12H6M18 12h3.5M8.5 12h7"/></symbol>
<symbol id="p-nail" viewBox="0 0 24 24"><path d="M8 3.4h8M12 3.4V17M10.3 17 12 21l1.7-4"/></symbol>
<symbol id="p-wire" viewBox="0 0 24 24"><ellipse cx="11.5" cy="12" rx="8" ry="6.6"/><ellipse cx="11.5" cy="12" rx="5" ry="4"/><path d="M18.8 14.6c1.4.8 2.4 1.9 2.7 3.4"/></symbol>
<symbol id="p-barbed" viewBox="0 0 24 24"><path d="M2 12h20M5.8 9.6l4.8 4.8M10.6 9.6l-4.8 4.8M13.4 9.6l4.8 4.8M18.2 9.6l-4.8 4.8"/></symbol>
<symbol id="p-mesh" viewBox="0 0 24 24"><path d="M12 3l9 9-9 9-9-9zM7.5 7.5l9 9M16.5 7.5l-9 9"/></symbol>
<symbol id="p-rebar" viewBox="0 0 24 24"><path d="M3.5 17.5 17.5 3.5M6.5 20.5 20.5 6.5M7.6 11.6l1.8 1.8M11.6 7.6l1.8 1.8M15.6 3.6l1.8 1.8"/></symbol>
<symbol id="p-weld" viewBox="0 0 24 24"><path d="M4 20l7.5-7.5M11.9 12.1l2.3-2.3M16.5 7.5 19 5M17.7 10.6l3-.6M13.4 6.3l.6-3"/></symbol>
<symbol id="p-paint" viewBox="0 0 24 24"><path d="M5.5 8.5h13l-1.2 10.6a1.8 1.8 0 0 1-1.8 1.6H8.5a1.8 1.8 0 0 1-1.8-1.6zM7 8.5a5 3.1 0 0 1 10 0M6.6 12h10.8"/></symbol>
<symbol id="p-can" viewBox="0 0 24 24"><ellipse cx="12" cy="5.3" rx="6" ry="2.3"/><path d="M6 5.3v13.2c0 1.3 2.7 2.3 6 2.3s6-1 6-2.3V5.3M6 10.3c0 1.3 2.7 2.3 6 2.3s6-1 6-2.3"/></symbol>
<symbol id="p-bag" viewBox="0 0 24 24"><path d="M7.2 8.5l1.8-4h6l1.8 4M6.5 8.5h11l-.8 10.2a2 2 0 0 1-2 1.8H9.3a2 2 0 0 1-2-1.8z"/><circle cx="12" cy="14" r="2.4"/></symbol>
<symbol id="p-jerrican" viewBox="0 0 24 24"><path d="M9 3.5h6V6l2.5 2v10.5a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2V8L9 6zM9.6 11.5l4.8 4.8M14.4 11.5l-4.8 4.8"/></symbol>
<symbol id="p-flask" viewBox="0 0 24 24"><path d="M9.8 3.5h4.4M10.5 3.5v5L5.6 18a1.9 1.9 0 0 0 1.8 2.5h9.2a1.9 1.9 0 0 0 1.8-2.5l-4.9-9.5v-5M7.6 14.5h8.8"/></symbol>
<symbol id="p-pigment" viewBox="0 0 24 24"><path d="M3.5 17.5c2-3.4 4.6-4 6.5-3.2 1.2.5 2.8.5 4 0 1.9-.8 4.5-.2 6.5 3.2zM3 20.5h18M9.5 8.5 12 6l2.5 2.5L12 11z"/></symbol>
<symbol id="p-roll" viewBox="0 0 24 24"><circle cx="8" cy="9.5" r="4.8"/><circle cx="8" cy="9.5" r="1.6"/><path d="M8 14.3h12.5v-4.8h-7.7"/></symbol>
<symbol id="p-tape" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7.5"/><circle cx="11" cy="11" r="3"/><path d="M16.3 15.6 21 20.3h-6.8"/></symbol>
<symbol id="p-roller" viewBox="0 0 24 24"><rect x="4" y="4" width="12.5" height="6" rx="2"/><path d="M16.5 7H20v4.5h-7.5v3"/><rect x="11" y="14.5" width="3" height="6" rx="1"/></symbol>
</defs></svg>"""

CONFIG_SCRIPT = """  <script>
    window.CSW_CONFIG = {
      gtmId: "",                    // "GTM-XXXXXXX"
      ga4Id: "G-PWKB7N27M1",        // Google Analytics 4
      googleAdsId: "",              // "AW-XXXXXXXXX"
      googleAdsConversionLabel: "", // etiqueta de conversión de Google Ads
      metaPixelId: "",              // Pixel de Facebook/Instagram
      whatsappNumber: \"""" + WA + """"
    };
  </script>"""

# --------------------------------------------------------------------------- head
def head(title, desc, path, og_image="assets/img/og-image.png", preload=None, jsonld=None, noindex=False):
    canonical = f"{SITE}/{path}" if path else f"{SITE}/"
    og_img_url = f"{SITE}/{og_image}"
    og_type = "image/png" if og_image.lower().endswith(".png") else "image/jpeg"
    preload_tag = f'\n  <link rel="preload" as="image" href="{preload}">' if preload else ""
    robots = "noindex, nofollow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
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
  <meta name="robots" content="{robots}">
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
  <meta property="og:image:type" content="{og_type}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="CASASILVIAWEB — Mayorista de fijaciones y aceros">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_img_url}">
  <meta name="theme-color" content="#d21e28">
  <link rel="icon" href="assets/img/logo.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/icon-192.png">
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
        <a class="nav__pedido" href="pedido.html">Armá tu pedido</a>
        <a href="nosotros.html">Nosotros</a>
        <a href="como-comprar.html">Cómo comprar</a>
        <a href="{sec}#contacto">Contacto</a>
      </nav>
      <div class="header__cta">
        {wa_btn("Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.", "header", "Header — Lista de precios", "btn btn--wa", inner='<span class="cta-text">Lista de precios</span>')}
        <button class="cart-btn" id="cart-open" type="button" aria-label="Ver tu pedido" title="Tu pedido">
          <svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg>
          <span class="cart-btn__badge" id="cart-badge" hidden>0</span>
        </button>
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
            <a href="pedido.html">Armá tu pedido</a>
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
""" + WA_FLOAT + CART_DRAWER + """
  <script src="assets/js/main.js" defer></script>
  <script src="assets/js/carrito.js" defer></script>
</body>
</html>"""

CART_DRAWER = """  <div class="cart-layer" id="cart-layer" hidden>
    <div class="cart-layer__backdrop" id="cart-backdrop"></div>
    <aside class="cart-drawer" role="dialog" aria-modal="true" aria-label="Tu pedido">
      <header class="cart-drawer__head">
        <span class="cart-drawer__ic"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg></span>
        <div><b>Tu pedido</b><span id="cart-count-label">Sin productos</span></div>
        <button class="cart-drawer__close" id="cart-close" type="button" aria-label="Cerrar carrito"><svg class="line" aria-hidden="true"><use href="#i-close"></use></svg></button>
      </header>
      <div class="cart-drawer__body" id="cart-body">
        <div class="cart-empty" id="cart-empty">
          <svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg>
          <p><b>Todavía no agregaste productos.</b></p>
          <p>Buscá en el catálogo con precios y armá tu pedido: lo enviás por WhatsApp y te confirmamos descuentos y entrega.</p>
          <a class="btn btn--wa" href="pedido.html" style="--btn-bg:var(--red)">Ver catálogo con precios</a>
        </div>
        <ul class="cart-items" id="cart-items"></ul>
      </div>
      <footer class="cart-drawer__foot" id="cart-foot" hidden>
        <div class="cart-minimo" id="cart-minimo" hidden>Pedido mínimo mayorista: <b>$300.000</b>. Te falta <b id="cart-minimo-falta"></b> para llegar.</div>
        <div class="cart-total"><span>Total estimado</span><b id="cart-total">$0</b></div>
        <p class="cart-disclaimer">Precios de lista sujetos a confirmación. Los descuentos por volumen se aplican al confirmar por WhatsApp.</p>
        <a class="btn btn--wa btn--lg btn--block" id="cart-send" href="#" target="_blank" rel="noopener" data-wa="carrito" data-wa-label="Carrito — Enviar pedido"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg>Enviar pedido por WhatsApp</a>
        <a class="cart-drawer__more" href="pedido.html">Seguir agregando productos →</a>
      </footer>
    </aside>
  </div>"""

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

DEPOT_PHOTOS = [
  ("deposito-almacen.webp", "Pallets de pintura y productos de obra apilados en altura en el depósito de CASASILVIAWEB"),
  ("deposito-hierros.webp", "Hierro aletado en barras apilado en profundidad en el depósito de CASASILVIAWEB"),
  ("deposito-mallas.webp", "Gran volumen de mallas electrosoldadas apiladas en el depósito de CASASILVIAWEB"),
  ("deposito-logistica.webp", "Autoelevador cargando mercadería palletizada para despacho"),
]

def _figs(photos):
    return "\n".join(
      f'          <figure class="gallery__item"><img src="assets/img/{p}" alt="{a}" width="800" height="600" loading="lazy" decoding="async"></figure>'
      for p, a in photos)

def gallery_section(soft=False):
    cls = "section section--soft" if soft else "section"
    return f"""    <section class="{cls}" id="deposito" aria-label="Nuestro depósito">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">Nuestro depósito</span><h2>Mercadería lista para entregar</h2><p>Stock propio y respaldo de fábrica para responder a cualquier pedido, grande o chico. <a class="link-wa" href="{wa_href('Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.')}" target="_blank" rel="noopener" data-wa="deposito" data-wa-label="Depósito — Lista de precios">Pedí la lista por WhatsApp</a>.</p></div>
        <div class="gallery reveal">
{_figs(DEPOT_PHOTOS)}
        </div>
      </div>
    </section>"""

def cat_gallery(c, soft=True):
    """Galería de fotos propia de cada categoría (cae a la del depósito si no tiene)."""
    photos = c.get("photos")
    if not photos:
        return gallery_section(soft=soft)
    cls = "section section--soft" if soft else "section"
    return f"""    <section class="{cls}" aria-label="{c['name']} en el depósito">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">En nuestro depósito</span><h2>{c['name']} en stock</h2><p>Mercadería propia, lista para entregar. <a class="link-wa" href="{wa_href(c['wa_text'])}" target="_blank" rel="noopener" data-wa="cat-{c['slug']}-galeria" data-wa-label="Galería — {c['name']}">Pedí la lista de precios por WhatsApp</a>.</p></div>
        <div class="gallery gallery--fit reveal">
{_figs(photos)}
        </div>
      </div>
    </section>"""

# --------------------------------------------------------------------------- DATOS DEL CATÁLOGO
CATS = [
  {
    "slug":"tornillos-autoperforantes", "name":"Tornillos Autoperforantes", "kicker":"Línea 01",
    "img":"cat-tornillos.webp", "img_alt":"Caja de tornillos autoperforantes cincados en el depósito de CASASILVIAWEB",
    "photos":[
      ("tornillos-stock.webp","Pallets de tornillos autoperforantes en stock en el depósito de CASASILVIAWEB"),
      ("tornillos-tipos.webp","Cajas de tornillos autoperforantes por tipo y medida en estantería"),
    ],
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
    "photos":[
      ("clavos-coils.webp","Rollos de alambre en pallets, gran volumen en stock"),
      ("clavos-deposito.webp","Stock de alambre y autoelevador en el depósito de CASASILVIAWEB"),
    ],
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
    "photos":[
      ("tirafondos-stock.webp","Tornillos y fijaciones junto a pallets de mercadería en el depósito"),
      ("tirafondos-tuercas.webp","Tuercas hexagonales cincadas, bulonería en stock"),
    ],
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
    "photos":[
      ("deposito-hierros.webp","Hierro aletado en barras apilado en profundidad en el depósito"),
      ("calidad-stock.webp","Operario moviendo barras de hierro aletado en el depósito de CASASILVIAWEB"),
    ],
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
    "photos":[
      ("pinturas-stock.webp","Pallets de pintura de obra de distintos colores en stock"),
      ("deposito-logistica.webp","Autoelevador con mezcla adhesiva palletizada para despacho"),
    ],
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
              <a class="cat__link" href="{c['slug']}.html" aria-label="Ver línea {c['name']}">Ver línea <svg class="line" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
            </div>
          </article>"""

# --------------------------------------------------------------------------- página de categoría
def precios_por_linea(c):
    """Links a las páginas de precios por línea de la categoría (SEO interno)."""
    gs = GRUPOS_BY_CAT.get(c["slug"])
    if not gs:
        return ""
    links = "\n".join(
        f'          <a class="linea-link" href="{grupo_url(g)}"><b>{g["grupo"]}</b>'
        f'<span>{len(g["items"])} {"producto" if len(g["items"]) == 1 else "productos"} con precio</span></a>'
        for g in gs)
    return f"""    <section class="section">
      <div class="container">
        <div class="section-head reveal"><span class="eyebrow">Listas de precios</span><h2>Precios de {c['name'].lower()} por línea</h2><p>Precios de lista actualizados 2026. Entrá a la línea que buscás o <a href="pedido.html?cat={c['slug']}">armá tu pedido online</a>.</p></div>
        <div class="lineas-grid reveal">
{links}
        </div>
      </div>
    </section>"""

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
              <a class="btn btn--ghost-dark btn--lg" href="pedido.html?cat={c['slug']}"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg> Armá tu pedido con precios</a>
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
{cat_gallery(c)}
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
{precios_por_linea(c)}
{faq_block(c['faq'], center=True, heading='Sobre '+c['name'].lower())}
{price_cta(heading='Pedí la lista de '+c['name'].lower(), wa_text=c['wa_text'], source='cat-'+c['slug']+'-cta', label='CTA '+c['name'])}
    <section class="section">
      <div class="container">
        <div class="section-head center reveal"><span class="eyebrow">Más líneas</span><h2>Seguí viendo el catálogo</h2></div>
        <p class="related reveal">{rel_links}</p>
      </div>
    </section>"""
    # Producto: sin precio (cotización por WhatsApp), marca Gerdau solo donde corresponde (acero)
    product = {"@type":"Product","name":c["name"],"image":f"{SITE}/assets/img/{c['img']}",
               "description":c["desc"],"category":"Fijaciones y aceros",
               "url":f"{SITE}/{c['slug']}.html"}
    if c["slug"] in ("hierros-y-mallas","soldadura"):
        product["brand"] = {"@type":"Brand","name":"Gerdau"}
    # JSON-LD
    jsonld = {"@context":"https://schema.org","@graph":[
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":"Productos","item":f"{SITE}/#productos"},
        {"@type":"ListItem","position":3,"name":c["name"],"item":f"{SITE}/{c['slug']}.html"},
      ]},
      product,
      {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faq"]]},
    ]}
    # Imagen para compartir (Open Graph): PNG/JPG por categoría (WhatsApp/FB no leen WebP)
    og_img = f"assets/img/og-{c['slug']}.jpg"
    if not os.path.exists(og_img):
        og_img = "assets/img/og-image.png"
    html = (head(c["title"], c["desc"], f"{c['slug']}.html", og_image=og_img,
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
          <a class="btn btn--ghost btn--lg" href="pedido.html"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg> Armá tu pedido online</a>
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

# --------------------------------------------------------------------------- pedido (catálogo con precios + carrito)
def catalogo_estatico():
    """Contenido indexable de pedido.html: el catálogo real lo dibuja carrito.js,
    pero los buscadores (y quien navegue sin JS) ven este índice de líneas con
    links a las páginas de precios estáticas."""
    blocks = []
    for c in CATS:
        gs = GRUPOS_BY_CAT.get(c["slug"])
        if not gs:
            continue
        lis = "\n".join(
            f'              <li><a href="{grupo_url(g)}">{g["grupo"]}</a> — '
            f'{len(g["items"])} {"producto con precio" if len(g["items"]) == 1 else "productos con precio"}</li>'
            for g in gs)
        blocks.append(f"""          <section>
            <h2><a href="{c['slug']}.html">{c['name']}</a></h2>
            <ul>
{lis}
            </ul>
          </section>""")
    return ('        <nav class="catalogo-estatico" aria-label="Listas de precios por línea">\n'
            + "\n".join(blocks) + "\n        </nav>")

def render_pedido():
    crumb = breadcrumb([("Inicio","index.html"),("Armá tu pedido",None)])
    sections = f"""    <section class="section section--soft pedido-hero">
      <div class="container">
        {crumb}
        <div class="section-head reveal">
          <span class="eyebrow">Catálogo con precios</span>
          <h1>Armá tu pedido online</h1>
          <p class="lead-big">Buscá los productos, agregalos al carrito y mirá el total en tiempo real. Cuando termines, lo enviás por WhatsApp y te confirmamos <strong>descuentos por volumen</strong> y entrega. <strong>Abonás al recibir.</strong></p>
          <ul class="pedido-meta">
            <li><svg class="line" aria-hidden="true"><use href="#i-tag"></use></svg> Listas vigentes 2026</li>
            <li><svg class="line" aria-hidden="true"><use href="#i-box"></use></svg> <span id="pedido-total-productos">—</span> productos</li>
            <li><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg> Pedido mínimo $300.000 · Entrega CABA y GBA</li>
          </ul>
        </div>
      </div>
    </section>
    <section class="section pedido-catalogo" id="catalogo">
      <div class="container">
        <div class="pedido-toolbar" id="pedido-toolbar">
          <label class="pedido-search" for="buscador">
            <svg class="line" aria-hidden="true"><use href="#i-search"></use></svg>
            <input type="search" id="buscador" placeholder="Buscá por producto, medida o código (ej: fix 4.5, tirafondo 1/4, N001066)" autocomplete="off">
          </label>
          <div class="pedido-chips" id="pedido-chips" role="tablist" aria-label="Filtrar por categoría"></div>
          <select id="pedido-grupo" aria-label="Filtrar por línea"><option value="">Todas las líneas</option></select>
        </div>
        <p class="pedido-result" id="pedido-result" aria-live="polite"></p>
        <section class="destacados" id="destacados-wrap" hidden aria-label="Los más pedidos">
          <div class="destacados__head">
            <span class="destacados__star"><svg class="fill" aria-hidden="true"><use href="#i-star"></use></svg></span>
            <div><h2>Los más pedidos</h2><p>Lo que más nos compran ferreterías y corralones, listo para agregar.</p></div>
          </div>
          <div class="destacados__row" id="destacados"></div>
        </section>
        <div class="prod-list" id="prod-list" aria-live="polite">
{catalogo_estatico()}
        </div>
        <div class="pedido-mas-wrap"><button class="btn btn--ghost-dark" id="pedido-mas" type="button" hidden>Mostrar más productos</button></div>
        <p class="cart-disclaimer center">Precios de lista (sin descuentos aplicados), sujetos a confirmación por WhatsApp. Las presentaciones son por caja, sobre o estuche según el producto.</p>
      </div>
    </section>
{price_cta(heading="¿Preferís que te armemos el pedido?",
           text="Escribinos por WhatsApp con lo que necesitás y te pasamos precios, descuentos por volumen y entrega. <strong>Abonás al recibir.</strong>",
           source="pedido-ayuda", label="Pedido — Ayuda por WhatsApp")}"""
    jsonld = {"@context":"https://schema.org","@graph":[
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":"Armá tu pedido","item":f"{SITE}/pedido.html"}]},
      {"@type":"CollectionPage","name":"Armá tu pedido online","url":f"{SITE}/pedido.html",
       "description":"Catálogo mayorista con precios: armá tu carrito y envialo por WhatsApp."},
      {"@type":"ItemList","name":"Listas de precios por línea","numberOfItems":len(GRUPOS),
       "itemListElement":[{"@type":"ListItem","position":i+1,"name":g["grupo"],
                           "url":f"{SITE}/{grupo_url(g)}"} for i, g in enumerate(GRUPOS)]}]}
    return (head("Catálogo con precios | Armá tu pedido online | CASASILVIAWEB",
                 "Catálogo mayorista con precios de lista: tornillos, clavos, alambres, tirafondos y más. Armá tu carrito online, mirá el total en tiempo real y envialo por WhatsApp.",
                 "pedido.html", jsonld=jsonld)
            + header() + sections + footer())

# --------------------------------------------------------------------------- datos de productos (para SEO)
import re as _re
import unicodedata as _ud

INDEXNOW_KEY = "b5a1c835135653201064af094dfac54c"  # clave IndexNow (Bing/Yandex/Naver)

def slugify(s):
    s = _ud.normalize("NFD", s)
    s = "".join(ch for ch in s if _ud.category(ch) != "Mn")
    return _re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def precio_ar(v):
    s = f"{v:,.2f}"
    return "$" + s.replace(",", "X").replace(".", ",").replace("X", ".")

with open("assets/data/productos.json", encoding="utf-8") as _f:
    _PROD_DATA = json.load(_f)
PRODUCTOS = _PROD_DATA["items"]

GRUPOS = []   # [{grupo, cat, items:[...]}] en orden de lista
_gidx = {}
for _p in PRODUCTOS:
    _k = (_p["grupo"], _p["cat"])
    if _k not in _gidx:
        _gidx[_k] = {"grupo": _p["grupo"], "cat": _p["cat"], "items": []}
        GRUPOS.append(_gidx[_k])
    _gidx[_k]["items"].append(_p)
GRUPOS_BY_CAT = {}
for _g in GRUPOS:
    GRUPOS_BY_CAT.setdefault(_g["cat"], []).append(_g)

def grupo_url(g):
    return f"precios-{slugify(g['grupo'])}.html"

def _pres_txt(i):
    return " · ".join(x for x in ((i["pack"] + " u.") if i["pack"] else "", i["pres"]) if x)

# --------------------------------------------------------------------------- páginas de precios por línea (SEO)
def render_grupo(g):
    grupo, cat, items = g["grupo"], g["cat"], g["items"]
    catname = CAT_BY_SLUG[cat]["name"]
    n = len(items)
    url = grupo_url(g)
    crumb = breadcrumb([("Inicio", "index.html"), ("Armá tu pedido", "pedido.html"), (grupo, None)])
    rows = "\n".join(
        f'              <tr><td class="cod">{i["cod"]}</td><td>{i["desc"]}'
        + (' <em class="sinstock">(sin stock, consultá)</em>' if i["sinStock"] else "")
        + f'</td><td>{_pres_txt(i)}</td>'
        + f'<td class="num">{precio_ar(i["precio"]) if i["precio"] is not None else "Consultar"}</td></tr>'
        for i in items)
    related = [x for x in GRUPOS_BY_CAT[cat] if x["grupo"] != grupo]
    rel_links = " · ".join(f'<a href="{grupo_url(r)}">{r["grupo"]}</a>' for r in related[:12])
    otras = f"""    <section class="section section--soft">
      <div class="container">
        <div class="section-head reveal"><span class="eyebrow">Más líneas de {catname}</span><h2>Otras listas de precios</h2></div>
        <p class="related reveal">{rel_links} · <a href="{cat}.html">Ver la línea completa</a></p>
      </div>
    </section>""" if related else ""
    wa_text = f"Hola CASASILVIAWEB! Me interesa {grupo} ({catname}). ¿Me pasan precios y descuentos por volumen?"
    sections = f"""    <section class="section section--soft">
      <div class="container">
        {crumb}
        <div class="section-head reveal">
          <span class="eyebrow">{catname} · Lista mayorista</span>
          <h1>{grupo}: precios por mayor</h1>
          <p>Lista de precios mayorista de <strong>{grupo.lower()}</strong> con {n} {"producto" if n == 1 else "productos"}, actualizada 2026.
          Comprá por caja, sobre o granel con <strong>descuentos por volumen</strong> y <strong>abonás al recibir</strong> en CABA y GBA. Pedido mínimo $300.000.</p>
          <div class="cat-intro__actions">
            <a class="btn btn--red btn--lg" href="pedido.html?grupo={slugify(grupo)}"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg> Agregar al pedido online</a>
            {wa_btn(wa_text, 'grupo-' + slugify(grupo), 'Línea ' + grupo, 'btn btn--wa btn--lg', inner='Consultar por WhatsApp')}
          </div>
        </div>
        <div class="table-wrap reveal">
          <table class="ptable">
            <thead><tr><th>Código</th><th>Producto</th><th>Presentación</th><th>Precio de lista</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="cart-disclaimer">Precios de lista en pesos argentinos, sin descuentos aplicados y sujetos a confirmación por WhatsApp. Los descuentos por volumen se definen según el monto del pedido.</p>
      </div>
    </section>
{trust_strip()}
{otras}
{price_cta(heading='Pedí ' + grupo.lower() + ' al por mayor', wa_text=wa_text, source='grupo-' + slugify(grupo) + '-cta', label='CTA ' + grupo)}"""
    products_ld = []
    for i in items[:30]:
        if i["precio"] is None:
            continue
        products_ld.append({"@type": "ListItem", "position": len(products_ld) + 1, "item": {
            "@type": "Product", "name": (i["desc"] + (" " + i["pres"] if i["pres"] else "")).strip(),
            "sku": i["cod"], "category": catname, "url": f"{SITE}/{url}",
            "offers": {"@type": "Offer", "price": round(i["precio"], 2), "priceCurrency": "ARS",
                       "availability": "https://schema.org/" + ("OutOfStock" if i["sinStock"] else "InStock"),
                       "priceValidUntil": f"{date.today().year}-12-31",
                       "seller": {"@id": f"{SITE}/#business"}}}})
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Armá tu pedido", "item": f"{SITE}/pedido.html"},
            {"@type": "ListItem", "position": 3, "name": grupo, "item": f"{SITE}/{url}"}]},
        {"@type": "ItemList", "name": f"{grupo} — precios mayoristas", "numberOfItems": len(products_ld),
         "itemListElement": products_ld}]}
    title = f"{grupo}: precios por mayor 2026 | CASASILVIAWEB"
    desc = (f"Lista de precios mayorista de {grupo.lower()} ({catname.lower()}): {n} productos actualizados. "
            "Descuentos por volumen, abonás al recibir, envíos a CABA y GBA.")
    return head(title, desc, url, jsonld=jsonld) + header() + sections + footer()

# --------------------------------------------------------------------------- páginas de gracias (conversiones Ads/GA4)
def render_gracias_pedido():
    """Página a la que llega el cliente después de enviar el pedido por WhatsApp.
    carrito.js marca acá la conversión `purchase` (GA4) y la de Google Ads.
    Para Google Ads también sirve como conversión por destino: /gracias-pedido.html"""
    sections = f"""    <section class="section gracias" id="gracias-pedido">
      <div class="container gracias__inner">
        <span class="gracias__ic"><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg></span>
        <span class="eyebrow">Pedido enviado</span>
        <h1>¡Gracias! Tu pedido ya está en WhatsApp</h1>
        <p class="lead-big">Se abrió una conversación de WhatsApp con tu pedido cargado. Si todavía no lo enviaste, tocá <b>enviar</b> en WhatsApp y te respondemos enseguida para confirmar <strong>precios, descuentos por volumen y entrega</strong>. Recordá: <strong>abonás al recibir</strong>.</p>
        <div class="gracias__acciones">
          <a class="btn btn--wa btn--lg" id="gracias-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-wa="gracias-pedido" data-wa-label="Gracias — Reabrir WhatsApp"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg>¿No se abrió? Reabrir WhatsApp</a>
          <a class="btn btn--ghost-dark btn--lg" href="pedido.html">Seguir comprando</a>
        </div>
        <div class="gracias-resumen" id="gracias-resumen" hidden>
          <h2>Resumen de lo que enviaste</h2>
          <table><tbody></tbody><tfoot><tr><td>Total estimado</td><td id="gracias-total"></td></tr></tfoot></table>
          <p class="cart-disclaimer">Precios de lista sujetos a confirmación. Te pasamos los descuentos por volumen por WhatsApp.</p>
          <button class="gracias__vaciar" id="gracias-vaciar" type="button">Ya lo envié, vaciar el carrito</button>
        </div>
        <ol class="steps reveal gracias__pasos">
          <li class="step"><span class="step__num">1</span><span class="step__ic"><svg class="fill" aria-hidden="true"><use href="#i-wa"></use></svg></span><h3>Te confirmamos</h3><p>Revisamos tu pedido y te confirmamos precios y descuentos.</p></li>
          <li class="step"><span class="step__num">2</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-truck"></use></svg></span><h3>Coordinamos la entrega</h3><p>Envío a CABA y GBA, o retiro en Tuyutí 1025, Tapiales.</p></li>
          <li class="step"><span class="step__num">3</span><span class="step__ic"><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg></span><h3>Abonás al recibir</h3><p>Efectivo o transferencia cuando te llega el pedido.</p></li>
        </ol>
      </div>
    </section>"""
    return (head("Pedido enviado | CASASILVIAWEB", "Tu pedido se envió por WhatsApp. Te confirmamos precios, descuentos y entrega enseguida.",
                 "gracias-pedido.html", noindex=True)
            + header() + sections + footer())

def render_gracias():
    """Página de gracias genérica (leads): destino para campañas de Google Ads."""
    sections = f"""    <section class="section gracias" id="gracias-contacto">
      <div class="container gracias__inner">
        <span class="gracias__ic"><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg></span>
        <span class="eyebrow">Mensaje recibido</span>
        <h1>¡Gracias por contactarnos!</h1>
        <p class="lead-big">Te respondemos por WhatsApp a la brevedad con la <strong>lista de precios</strong> y las bonificaciones vigentes. Mientras tanto, podés ir armando tu pedido online con precios.</p>
        <div class="gracias__acciones">
          <a class="btn btn--red btn--lg" href="pedido.html"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg> Armá tu pedido online</a>
          {wa_btn("Hola CASASILVIAWEB! Quiero solicitar la lista de precios mayorista.", "gracias-contacto", "Gracias — WhatsApp", "btn btn--wa btn--lg", inner="Escribinos por WhatsApp")}
        </div>
      </div>
    </section>
{trust_strip()}"""
    return (head("¡Gracias por contactarnos! | CASASILVIAWEB", "Recibimos tu consulta. Te respondemos por WhatsApp con la lista de precios mayorista.",
                 "gracias.html", noindex=True)
            + header() + sections + footer())

# --------------------------------------------------------------------------- sitemap
def render_sitemap():
    urls = ([("", "1.0"), ("pedido.html", "0.9")]
            + [(f"{c['slug']}.html", "0.8") for c in CATS]
            + [(grupo_url(g), "0.7") for g in GRUPOS]
            + [("nosotros.html", "0.6"), ("como-comprar.html", "0.6")])
    body = "\n".join(
      f'  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>'
      for p, pr in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'

# --------------------------------------------------------------------------- llms.txt
LLMS_INTRO = (
  "Mayorista de fijaciones y aceros en Tapiales, Buenos Aires (Argentina): tornillos "
  "autoperforantes, clavos, alambres, tirafondos, hierros y mallas, soldadura y pinturas. "
  "Venta al por mayor con descuentos por volumen, respaldo de fábrica (Gerdau, calidad "
  "certificada ISO 9001 / IRAM) y pago contra entrega (\"abonás al recibir\") en CABA y "
  f"Gran Buenos Aires. Pedido mínimo $300.000. Pedidos y lista de precios por WhatsApp ({WA_DISPLAY})."
)

def render_llms():
    prods = "\n".join(
        f"- [{c['name']}]({SITE}/{c['slug']}.html): " + ", ".join(c["tags"]).lower() + "."
        for c in CATS)
    return f"""# CASASILVIAWEB

> {LLMS_INTRO}

## Productos

{prods}

## Precios

- [Armá tu pedido]({SITE}/pedido.html): catálogo online con {len(PRODUCTOS)} productos y precios de lista; el carrito se envía por WhatsApp.
{chr(10).join(f"- [{g['grupo']} — precios]({SITE}/{grupo_url(g)})" for g in GRUPOS)}

## Empresa

- [Nosotros]({SITE}/nosotros.html): mayorista que abastece a ferreterías, corralones, zingueros, madereras, distribuidores y constructoras.
- [Cómo comprar]({SITE}/como-comprar.html): pedido mínimo, envíos, formas de pago y descuentos por volumen.

## Contacto

- [WhatsApp](https://wa.me/{WA}): {WA_DISPLAY} — pedidos y lista de precios al instante.
- Dirección: Tuyutí 1025, Tapiales (B1770), Zona Oeste, Gran Buenos Aires, Argentina.
- [Sitio web]({SITE}/)

## Información útil

- Modalidad: venta mayorista. Pedido mínimo $300.000 (pedidos habituales de $300.000 a $4.000.000).
- Pago: abonás al recibir el pedido (efectivo o transferencia), también en pedidos grandes.
- Envíos: CABA y todo el Gran Buenos Aires; los pedidos grandes se despachan directo desde la acería con flete.
- Descuentos: bonificaciones por volumen de compra.
- Calidad: respaldo de fábrica (Gerdau), una de las principales marcas de acero del país, con norma ISO 9001 otorgada por IRAM.
- Idioma de atención: español (Argentina).

## Recursos

- [Versión completa para IA]({SITE}/llms-full.txt)
"""

def render_llms_full():
    blocks = []
    for c in CATS:
        subs = "\n".join(f"- {n}: {d}" for n, d in c["subcats"])
        faqs = "\n".join(f"- {q} {a}" for q, a in c["faq"])
        blocks.append(
            f"### {c['name']}\n"
            f"URL: {SITE}/{c['slug']}.html\n\n"
            f"{c['lead']}\n\n"
            f"Tipos y líneas:\n{subs}\n\n"
            f"Medidas y presentaciones: {c['measures']}\n\n"
            f"Preguntas frecuentes:\n{faqs}\n")
    catalog = "\n".join(blocks)
    # lista de precios completa, por línea, para consumo de LLMs
    price_blocks = []
    for g in GRUPOS:
        lines = "\n".join(
            f"- {i['cod']} · {i['desc']}"
            + (f" ({_pres_txt(i)})" if _pres_txt(i) else "")
            + ": " + (precio_ar(i["precio"]) if i["precio"] is not None else "consultar")
            + (" [SIN STOCK]" if i["sinStock"] else "")
            for i in g["items"])
        price_blocks.append(f"### {g['grupo']} ({CAT_BY_SLUG[g['cat']]['name']})\n"
                            f"URL: {SITE}/{grupo_url(g)}\n{lines}\n")
    precios_full = "\n".join(price_blocks)
    return f"""# CASASILVIAWEB — Información completa para IA

> {LLMS_INTRO}

## La empresa

CASASILVIAWEB es un mayorista de fijaciones y aceros ubicado en Tuyutí 1025, Tapiales (B1770),
Zona Oeste del Gran Buenos Aires, Argentina. Abastece a ferreterías, corralones, zingueros,
madereras, distribuidores y constructoras. Trabaja con respaldo de fábrica (Gerdau, una de las
principales marcas de acero del país, con norma ISO 9001 otorgada por IRAM). Toda la atención,
la lista de precios y los pedidos se gestionan por WhatsApp ({WA_DISPLAY}).

## Cómo comprar

1. Escribís por WhatsApp ({WA_DISPLAY}) y pedís la lista de precios.
2. Armás el pedido: te pasan precios y descuentos por volumen y coordinan la entrega.
3. Abonás al recibir (efectivo o transferencia), también en pedidos grandes.

- Pedido mínimo: $300.000 (pedidos habituales de $300.000 a $4.000.000).
- Envíos: CABA y todo el Gran Buenos Aires. Los pedidos grandes se despachan directo desde la acería con flete.
- Descuentos por volumen de compra.

## Catálogo

{catalog}
## Lista de precios completa (precios de lista 2026, ARS, sin descuentos)

Los precios son de lista, sujetos a confirmación por WhatsApp; los descuentos por
volumen se definen según el monto del pedido. Pedido online: {SITE}/pedido.html

{precios_full}
## Contacto y ubicación

- WhatsApp: {WA_DISPLAY} — https://wa.me/{WA}
- Dirección: Tuyutí 1025, Tapiales (B1770), Zona Oeste, Gran Buenos Aires, Argentina.
- Cobertura de entrega: CABA y Gran Buenos Aires.
- Sitio web: {SITE}/
"""

# --------------------------------------------------------------------------- main
def main():
    import os
    out = {}
    out["index.html"] = render_home()
    out["pedido.html"] = render_pedido()
    out["gracias-pedido.html"] = render_gracias_pedido()
    out["gracias.html"] = render_gracias()
    for g in GRUPOS:
        out[grupo_url(g)] = render_grupo(g)
    out[f"{INDEXNOW_KEY}.txt"] = INDEXNOW_KEY
    out["nosotros.html"] = render_nosotros()
    out["como-comprar.html"] = render_como_comprar()
    for c in CATS:
        out[f"{c['slug']}.html"] = render_category(c)
    out["sitemap.xml"] = render_sitemap()
    out["llms.txt"] = render_llms()
    _full = render_llms_full()
    out["llms-full.txt"] = _full
    out["llms_full.txt"] = _full
    for fn, content in out.items():
        with open(fn, "w", encoding="utf-8") as f:
            f.write(content)
        print("escrito:", fn, f"({len(content)//1024} KB)")
    print(f"\nOK — {len(out)} archivos generados.")

if __name__ == "__main__":
    main()

