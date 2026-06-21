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
| `hero-deposito.webp`            | Fondo de la portada (oscuro)         | 1600×1000, horizontal  |
| `og-image.png`                  | Vista previa al compartir (redes)    | 1200×630 (PNG/JPG, no WebP) |
| `cat-tornillos.webp`            | Tarjeta "Tornillos Autoperforantes"  | 900×650                |
| `cat-clavos-alambres.webp`      | Tarjeta "Clavos y Alambres"          | 900×650                |
| `cat-tirafondos.webp`           | Tarjeta "Tirafondos y fijaciones"    | 900×650                |
| `cat-hierros-mallas.webp`       | Tarjeta "Hierros y Mallas"           | 900×650                |
| `calidad-stock.webp`            | Sección "Calidad y respaldo"         | 1000×750               |

> Las fotos van en **WebP** (más livianas). Para convertir: Squoosh.app o
> `convert foto.jpg -quality 80 foto.webp`. La de compartir (`og-image`) dejala en PNG/JPG
> porque WhatsApp/Facebook no leen bien WebP en la vista previa.

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

## 🌐 Publicar / previsualizar

### Vista previa ahora (sin dominio) — GitHub Pages
1. *Settings → Pages → Source: **Deploy from a branch**.*
2. Branch: `claude/sweet-knuth-lxcsii` · carpeta `/ (root)` → **Save**.
3. En ~1 minuto queda online en: `https://ianpolettilucero.github.io/casas-elle/`

> No incluimos el archivo `CNAME` todavía, así la vista previa funciona en la URL de
> github.io. Las etiquetas `canonical` / Open Graph siguen apuntando al dominio final
> (`www.casasilviaweb.com.ar`), que es lo correcto para SEO.

### Cuando tengas acceso al dominio casasilviaweb.com.ar
1. Creá en la raíz un archivo llamado **`CNAME`** con una sola línea: `www.casasilviaweb.com.ar`
2. En tu proveedor de DNS: registro `CNAME` de `www` → `ianpolettilucero.github.io`
   (y registros `A` del apex hacia las IPs de GitHub Pages si lo querés sin `www`).
3. En *Settings → Pages → Custom domain* confirmá el dominio y activá **Enforce HTTPS**.

> Nada de esto afecta al sitio actual hasta que cambies el DNS: el original sigue
> funcionando en el dominio hasta el momento exacto del switch.

### Otras opciones
**Netlify** o **Vercel**: importás el repo y te dan una URL al instante, sin tocar DNS.

---

## ✅ Pendientes (para completar)

- [ ] Reemplazar las imágenes por las versiones definitivas (ver tabla de arriba).
- [ ] Confirmar/actualizar los enlaces de **Instagram** y **Facebook** en el footer
      (hoy apuntan a `instagram.com/casasilviaweb` y `facebook.com/casasilviaweb` como tentativos).
- [ ] Cargar los IDs de medición (GTM / GA4 / Google Ads / Meta Pixel) en `CSW_CONFIG`.
- [ ] (Opcional) Agregar íconos cuadrados 192×192 y 512×512 para la PWA.
- [ ] Verificar el horario de atención si se quiere mostrar.
