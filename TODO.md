# TO DO — SEO, conversión y confianza (CASASILVIAWEB)

> Objetivo de todo lo que sigue: **que nos encuentren fácil (SEO)**, **que generemos
> tranquilidad y seguridad (confianza)** y **que la consulta se transforme en venta
> (conversión)**. Canal de venta: **WhatsApp** (no e-commerce, no carrito).

Etiquetas: 🔍 SEO · 💬 Conversión · 🛡️ Confianza · Prioridad: 🔴 Alta · 🟡 Media · 🟢 Baja

---

## 0) Investigación: por qué rankean los primeros

Busqué como lo haría nuestro público (ferreterías, corralones, instaladores de durlock/steel
framing, herreros, constructores y consumidor final) y entré a los que aparecen primeros.
Patrones que se repiten:

1. **MercadoLibre copa lo transaccional** por autoridad de dominio + fichas con precio,
   **reseñas, ventas realizadas, preguntas/respuestas, envío y medios de pago**. No competimos
   de igual a igual, pero nos marca **qué espera ver el comprador para confiar**.
2. **Páginas dedicadas que calzan con la búsqueda**: los orgánicos que rankean tienen una página
   por producto/categoría/uso, con el H1 y la URL iguales a lo que la gente busca
   (ej. "Tornillo T1/T2/T3/T4", "Tornillos para Durlock – Drywall para Madera",
   "Tirafondo para Madera Cabeza Hexagonal DIN 571"). **Una sola landing no alcanza** para rankear
   en todas esas consultas.
3. **Contenido que informa (guías)** rankea para "qué/cómo/cuál" y **da confianza**
   (Bulonera Da Silva: "qué tornillo usar para durlock"; TEL: pestaña "Usos"; guías de tirafondos).
4. **Profundidad técnica** = más keywords y menos dudas: descripción + medidas + usos + presentación
   + normas (IRAM/DIN) + esquemas. (TEL es el mejor ejemplo.)
5. **SEO local** para "zona oeste / La Matanza": ganan las casas con **trayectoria y ubicación clara**
   (Catley "50 años", Bulonera Oeste "desde 1979", + ficha de Google y directorios).
6. **Señales de legitimidad** muy argentinas: normas IRAM/DIN, "100% argentino", logo de AFIP,
   marcas/clientes, años de trayectoria, mapa de distribuidores.

### Ideas tomadas de cada uno

| Competidor | Qué hace bien | Idea para nosotros |
|---|---|---|
| **TEL** (autoperforantestel.com) | Ficha con pestañas: Descripción/Medidas/Usos/Presentación/360° + tabla comparativa T1-T4 + ISO/IRAM | Fichas de categoría con secciones (descripción, medidas, usos, presentación) y **tabla de medidas** |
| **Tornillos Mitto** (tornillosmitto.com) | **Catálogo PDF descargable**, CTAs segmentados (mayorista/minorista), "líneas" de producto, blog "Anatomía del tornillo" | Catálogo PDF como imán de contacto + guía educativa |
| **MercadoLibre** | Reseñas con estrellas, ventas, **preguntas y respuestas**, envío y medios de pago claros | **Testimonios**, FAQ por categoría, "cómo compro / cómo entrego / cómo pago" claro |
| **Curia / BULJAC / CMP** | **WhatsApp pre-formateado con el producto**, breadcrumbs, listado de medidas, badges (envío/seguro) | Ya tenemos WhatsApp con mensaje; sumar breadcrumbs + listado de medidas + badges |
| **Catley / Bulonera Oeste** (local) | Trayectoria ("50 años", "desde 1979"), zona, cantidad de artículos | Sección **Nosotros** con trayectoria real + foco Zona Oeste |
| **Guías** (durlock.com, industriapedia) | Explican usos, medidas y normas (DIN/IRAM) | Notas/guía: "qué fijación usar según material" |

Fuentes: tornillosmitto.com · autoperforantestel.com · buljac.com.ar · comercialcmp.com.ar ·
curia.com.ar · buloneradasilva.com.ar · maferbul.com.ar · mercadolibre.com.ar · catley.com.ar ·
buloneraoeste.com.ar · durlock.com · industriapedia.com

---

## 1) Arquitectura de contenido — el cambio más importante 🔴

> De "una página que dice lo que hacemos" → a "un sitio que **informa y da confianza**".
> Esto es lo que pediste y, además, es el gap #1 de SEO.

- [ ] 🔴 🔍💬🛡️ **Crear una página por categoría** (4 hoy: Autoperforantes, Clavos y Alambres,
  Tirafondos, Hierros y Mallas). Cada una con esta estructura (estilo catálogo, como la competencia):
  1. Título + intro corta con keyword (ej. "Tornillos autoperforantes mayorista").
  2. **Descripción del producto** (qué es, para qué sirve).
  3. **Información adicional / especificaciones** (tipos, puntas, cabezas, tratamientos, normas).
  4. **Medidas disponibles** (tabla o listado: diámetro × largo, presentación por caja/millar).
  5. **Casos de uso / aplicaciones** (chapa, madera, metal, durlock, steel framing, hormigón…).
  6. **Imágenes** del producto y de aplicación.
  7. **Preguntas frecuentes** de esa categoría (al final).
  8. **CTA de WhatsApp** con mensaje pre-armado de esa categoría + "pedí la lista de precios".
- [ ] 🔴 🔍 **URLs y H1 que calcen con la búsqueda**: `/tornillos-autoperforantes/`,
  `/clavos-y-alambres/`, `/tirafondos/`, `/hierros-y-mallas/` (y a futuro por producto).
- [ ] 🔴 🔍 **Breadcrumbs** (Inicio › Productos › Categoría) + datos estructurados `BreadcrumbList`.
- [ ] 🟡 🔍 **Datos estructurados `Product`** por categoría/producto (ya hay base en la home).
- [ ] 🟡 💬 Enlazar la home con cada categoría (las tarjetas actuales abren la página, no solo WhatsApp).

### ⚠️ Catálogo abierto / escalable (porque vas a sumar productos)
- [ ] 🔴 🔍 **Diseñar el catálogo "data-driven"**: los productos/medidas en un archivo
  (`productos.json` o markdown) + una plantilla que genera las páginas. Así sumar un producto
  o categoría nuevo es **agregar un registro**, no programar una página.
  → Mantiene el sitio simple de mantener y listo para crecer.
- [ ] 🟡 🔍 Dejar preparada la jerarquía **categoría → producto** para cuando cierres el catálogo
  (hoy páginas por categoría; mañana subpáginas por producto, ej. "Tornillo T2 punta aguja 6×1").

---

## 2) Contenido que informa y rankea (guías) 🟡

> Captura búsquedas "qué/cómo/cuál" (público que todavía no sabe qué comprar) y **da confianza**.

- [ ] 🟡 🔍🛡️ Sección **"Guías / Consejos"** (o notas) con artículos cortos y útiles:
  - "¿Qué tornillo autoperforante usar según el material? (chapa, madera, metal, durlock)"
  - "Tipos de clavos y para qué sirve cada uno (París, espiralado, cabeza de plomo…)"
  - "Tirafondos: medidas, usos y norma DIN 571"
  - "Malla electrosoldada e hierro: cómo elegir para tu obra"
- [ ] 🟡 🔍 Cada guía enlaza a la **categoría correspondiente** (del lector informado → a la consulta).
- [ ] 🟢 🔍 Tabla orientativa "qué medida/tornillo para cada uso" (muy buscado y compartible).

---

## 3) Señales de confianza (tranquilidad y seguridad) 🔴

> Es lo que convierte "una web que vende" en "una web en la que confío".

- [ ] 🔴 🛡️ Sección **"Nosotros"**: trayectoria (años en el rubro), que es **mayorista**,
  foco en Zona Oeste/GBA, valores (stock, calidad, atención). *(Necesito datos reales tuyos.)*
- [ ] 🔴 🛡️💬 **Testimonios / opiniones** de clientes (aunque sean 4-6 para empezar).
  Es el equivalente a las reseñas de MercadoLibre que tanto pesan. *(Necesito que me pases algunos.)*
- [ ] 🟡 🛡️ **Marcas que trabajan** (Gerdau, etc.) y/o logos de clientes (corralones, ferreterías).
- [ ] 🟡 🛡️ Reforzar **normas y calidad** (IRAM / DIN / ISO de los fabricantes) en cada categoría.
- [ ] 🟡 🛡️ **Datos de legitimidad**: razón social, CUIT, "Responsable Inscripto/Monotributo"
  en el footer (muy valorado en compras B2B en Argentina). *(Necesito el dato.)*
- [ ] 🟢 🛡️ Foto real del local / depósito / equipo (humaniza y da seguridad).

---

## 4) Conversión — transformar la consulta en venta 💬

- [ ] 🔴 💬 **WhatsApp pre-formateado por producto** (no solo por categoría): que el mensaje
  incluya el producto/medida que estaba mirando. (La competencia lo usa y reduce fricción.)
- [ ] 🟡 💬 **Catálogo / lista de precios en PDF descargable** como imán de contacto
  (pide WhatsApp para enviarlo, o descarga directa). Mitto lo usa muy bien.
- [ ] 🟡 💬 Bloque claro **"Cómo comprar"**: 1) Consultás por WhatsApp → 2) Te pasamos la lista →
  3) Coordinás → 4) **Abonás al recibir**. Da seguridad sobre el proceso.
- [ ] 🟡 💬 **Medios de pago y envíos** explícitos (transferencia/efectivo, zonas, mínimos).
  *(Necesito condiciones reales.)*
- [ ] 🟢 💬 Medir conversión por categoría (ya está el tracking por `data-wa`): ver qué línea
  consulta más y optimizar.

---

## 5) SEO técnico y local 🟡

- [ ] 🔴 🔍🛡️ **Crear/optimizar la ficha de Google Business Profile** (Google Maps):
  para "tornillos zona oeste / La Matanza", el negocio con ficha + reseñas gana. *(Lo hacés vos
  con la cuenta del negocio; te guío.)*
- [ ] 🟡 🔍 **Sitemap**: agregar las nuevas páginas (categorías y guías) cuando existan.
- [ ] 🟡 🔍 Mantener **Core Web Vitals**: reemplazar imágenes por versiones optimizadas
  (WebP, comprimidas) cuando lleguen las definitivas.
- [ ] 🟡 🔍 **Datos estructurados** por página (Product / FAQ / Breadcrumb).
- [ ] 🟢 🔍 Páginas/landing por **localidad** clave (San Justo, Ramos Mejía, etc.) si se quiere
  empujar lo local (sin exagerar, para no sonar repetitivo).
- [ ] 🟢 🔍 Conseguir menciones/enlaces en **directorios** del rubro (elferretero, guías locales).

---

## 6) Necesito que me pases (para llenar lo de arriba sin inventar)

- [ ] Años de trayectoria / desde cuándo trabajan.
- [ ] Datos fiscales (razón social, CUIT, condición IVA) para el footer.
- [ ] Condiciones reales: zonas de envío, mínimos de compra, medios de pago.
- [ ] 4-6 testimonios de clientes (nombre/comercio + frase).
- [ ] Marcas que distribuyen y/o clientes para mostrar.
- [ ] Links reales de **Instagram** y **Facebook**.
- [ ] Fotos del local/depósito/productos (las "imágenes bien hechas").
- [ ] El catálogo cuando lo cierres (o por partes) para armar las páginas/medidas.

---

## Orden sugerido (fases, para no romper lo simple)

- **Fase 1 (ahora):** páginas por categoría (sección 1) + Nosotros + testimonios + "Cómo comprar".
- **Fase 2:** guías/notas (sección 2) + catálogo PDF + Google Business Profile.
- **Fase 3:** subpáginas por producto cuando cierres el catálogo + landings locales + optimización fina.
