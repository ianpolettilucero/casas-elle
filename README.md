# CASASILVIAWEB — Sitio web

Sitio institucional y de catálogo para **CASASILVIAWEB**, mayorista de tornillos
autoperforantes, clavos, alambres, tirafondos, hierros y mallas (Tapiales, Buenos Aires).

Hecho como **sitio estático** (HTML + CSS + JS, sin build ni dependencias): rápido,
fácil de hostear y óptimo para SEO. Toda la comunicación con el cliente es por **WhatsApp**.

---

## 🚀 Cómo verlo localmente

No requiere instalación. Desde la raíz del proyecto:

```bash
python3 -m http.server 8080
# abrir http://localhost:8080
```

(O cualquier servidor estático: `npx serve`, la extensión *Live Server* de VS Code, etc.)

---

## 📁 Estructura

```
.
├── index.html                # Página principal (todas las secciones)
├── 404.html                  # Página de error
├── robots.txt                # SEO: rastreo + sitemap + bots de IA
├── sitemap.xml               # SEO: mapa del sitio
├── manifest.webmanifest      # PWA / icono
├── llms.txt                  # Resumen para LLMs (estándar llmstxt.org)
├── llms-full.txt             # Versión completa para LLMs
├── llms_full.txt             # Copia (nombre con guión bajo)
├── CNAME                     # Dominio para GitHub Pages
├── .nojekyll                 # Sirve los archivos tal cual en GitHub Pages
└── assets/
    ├── css/styles.css        # Estilos (diseño industrial rojo/negro)
    ├── js/main.js            # Medición, popup de WhatsApp, UI
    └── img/
        ├── logo.png, hero.png, og-image.png
        ├── cat-*.png/.jpg    # Imágenes de cada categoría
        ├── detail-*.png
        └── originales/       # Imágenes originales del sitio (referencia)
```

---

## 🖼️ Cambiar las imágenes (cuando lleguen las definitivas)

Las imágenes actuales son las del sitio original (sirven de placeholder).
Para reemplazarlas, **mantené el mismo nombre de archivo** y pisá el que está en `assets/img/`:

| Archivo                         | Dónde se usa                         | Tamaño sugerido        |
|---------------------------------|--------------------------------------|------------------------|
| `logo.png`                      | Header, footer, favicon, popup       | PNG con fondo transparente, ~512px |
| `hero.png`                      | Fondo de la portada (oscuro)         | 1920×1080, horizontal  |
| `og-image.png`                  | Vista previa al compartir (redes)    | 1200×630               |
| `cat-autoperforantes.jpg`       | Tarjeta "Tornillos Autoperforantes"  | 800×600                |
| `cat-clavos-alambres.png`       | Tarjeta "Clavos y Alambres"          | 800×600                |
| `cat-tirafondos.png`            | Tarjeta "Tirafondos"                 | 800×600                |
| `cat-hierros-mallas.png`        | Tarjeta "Hierros y Mallas"           | 800×600                |
| `detail-macro.png`              | Sección "Garantía de calidad"        | 800×600                |

> Tip: optimizá los pesos (TinyPNG / Squoosh) antes de subirlas para que cargue rápido.

---

## 📊 Medición de publicidad y conversiones

Todo se configura en **un solo lugar**: el objeto `CSW_CONFIG` dentro de `index.html`
(`<head>`). Completá los IDs que tengas y se cargan solos. Si quedan vacíos, **no se
carga nada** y el sitio funciona igual.

```js
window.CSW_CONFIG = {
  gtmId: "GTM-XXXXXXX",          // Google Tag Manager (recomendado)
  ga4Id: "G-XXXXXXXXXX",         // Google Analytics 4
  googleAdsId: "AW-XXXXXXXXX",   // Google Ads
  googleAdsConversionLabel: "",  // Etiqueta de conversión de Google Ads
  metaPixelId: "",               // Pixel de Facebook/Instagram
  whatsappNumber: "541166034047"
};
```

> Si usás **GTM**, acordate de descomentar y completar también el `<noscript>` que está
> al inicio del `<body>`.

### Eventos personalizados (custom tags)

Cada clic a WhatsApp es la **conversión principal**. El sitio empuja estos eventos al
`dataLayer` (listos para mapear en GTM / GA4 / Ads / Meta):

| Evento (`dataLayer`)   | Cuándo ocurre                          | Datos útiles                          |
|------------------------|----------------------------------------|---------------------------------------|
| `whatsapp_click`       | Clic en cualquier botón de WhatsApp    | `lead_source`, `lead_label`           |
| `generate_lead`        | Junto al clic (evento GA4 recomendado) | `method`, `lead_source`, `value`      |
| `whatsapp_popup_open`  | Se abre el popup de la esquina         | —                                     |
| `page_view_enriched`   | Carga de página                        | `page_type`, `business`               |

El valor de `lead_source` identifica **desde dónde** convirtió cada visitante:
`hero`, `header`, `lista-precios`, `popup`, `footer`, `ubicacion`, `404`, y por categoría
(`cat-autoperforantes`, `cat-clavos-alambres`, `cat-tirafondos`, `cat-hierros-mallas`).
Así podés medir qué sección y qué campaña traen más pedidos.

> Cada botón lleva los atributos `data-wa="origen"` y `data-wa-label="..."`. Para sumar
> un botón nuevo medible, basta con agregarle `data-wa`.

---

## 📞 WhatsApp

Número: **+54 11 6603-4047** → todos los enlaces apuntan a `https://wa.me/541166034047`
con un mensaje prearmado distinto según la sección (lista de precios, categoría, etc.).
Para cambiar el número, reemplazá `541166034047` en `index.html` (y en `whatsappNumber`).

---

## 🔎 SEO incluido

- HTML semántico, un solo `<h1>`, jerarquía de encabezados y `alt` descriptivos.
- Meta `title`/`description`, **Open Graph** y **Twitter Cards**.
- **Datos estructurados (JSON-LD)**: `HardwareStore`/`Organization`, `WebSite` y `FAQPage`.
- `sitemap.xml`, `robots.txt`, `canonical`, etiquetas `geo` y favicon/manifest.
- `llms.txt` y `llms-full.txt` para buscadores e IAs.
- Rendimiento: preconnect de fuentes, preload del hero, `loading="lazy"` e imágenes con medidas.

---

## 🌐 Deploy en GitHub Pages

1. *Settings → Pages → Build and deployment → Source: Deploy from a branch.*
2. Elegí la rama y carpeta `/ (root)`.
3. El archivo **`CNAME`** ya apunta a `www.casasilviaweb.com.ar`. En tu proveedor de
   dominio, creá un `CNAME` de `www` hacia `<usuario>.github.io` (y los `A` del apex si
   querés `casasilviaweb.com.ar` sin `www`).
4. Si hosteás en otro lado (Netlify, Vercel, hosting propio), podés borrar `CNAME`.

---

## ✅ Pendientes (para completar)

- [ ] Reemplazar las imágenes por las versiones definitivas (ver tabla de arriba).
- [ ] Confirmar/actualizar los enlaces de **Instagram** y **Facebook** en el footer
      (hoy apuntan a `instagram.com/casasilviaweb` y `facebook.com/casasilviaweb` como tentativos).
- [ ] Cargar los IDs de medición (GTM / GA4 / Google Ads / Meta Pixel) en `CSW_CONFIG`.
- [ ] (Opcional) Agregar íconos cuadrados 192×192 y 512×512 para la PWA.
- [ ] Verificar el horario de atención si se quiere mostrar.
