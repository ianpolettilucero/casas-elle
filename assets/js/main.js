/* ==========================================================================
   CASASILVIAWEB · main.js
   - Medición de publicidad y conversiones (GTM / GA4 / Google Ads / Meta Pixel)
   - Tracking de clics de WhatsApp por fuente (conversión principal)
   - Popup de WhatsApp (esquina inferior derecha)
   - Menú móvil, animaciones de scroll, año del footer
   ========================================================================== */
(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     1) CONFIGURACIÓN DE MEDICIÓN
     Completá los IDs cuando los tengas. Si quedan vacíos, no se carga nada
     (la web sigue funcionando y los eventos se encolan en dataLayer igual).
     ---------------------------------------------------------------------- */
  var CONFIG = Object.assign(
    {
      gtmId: "",                      // "GTM-XXXXXXX"  (recomendado: gestiona todo desde GTM)
      ga4Id: "",                      // "G-XXXXXXXXXX" (Google Analytics 4)
      googleAdsId: "",                // "AW-XXXXXXXXX" (Google Ads)
      googleAdsConversionLabel: "",   // "AbC-D_efGh" (etiqueta de conversión de Google Ads)
      metaPixelId: "",                // "123456789012345" (Facebook/Instagram Pixel)
      whatsappNumber: "541166034047", // sin +, espacios ni guiones
      leadValue: 0,                   // valor estimado por lead (para Ads/Pixel), opcional
      currency: "ARS"
    },
    window.CSW_CONFIG || {}
  );

  // dataLayer SIEMPRE disponible (GTM/GA lo consumen cuando cargan)
  window.dataLayer = window.dataLayer || [];
  function dl(obj) { window.dataLayer.push(obj); }
  function gtag() { window.dataLayer.push(arguments); }

  /* ----------------------------------------------------------------------
     2) CARGA DE ETIQUETAS (solo si hay IDs)
     ---------------------------------------------------------------------- */
  function loadScript(src, attrs) {
    var s = document.createElement("script");
    s.async = true; s.src = src;
    if (attrs) Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
    return s;
  }

  // Google Tag Manager
  if (CONFIG.gtmId) {
    dl({ "gtm.start": Date.now(), event: "gtm.js" });
    loadScript("https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(CONFIG.gtmId));
  }

  // gtag.js (GA4 + Google Ads) — útil si no se gestiona desde GTM
  var gtagId = CONFIG.ga4Id || CONFIG.googleAdsId;
  if (!CONFIG.gtmId && gtagId) {
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(gtagId));
    gtag("js", new Date());
    if (CONFIG.ga4Id) gtag("config", CONFIG.ga4Id);
    if (CONFIG.googleAdsId) gtag("config", CONFIG.googleAdsId);
  }
  window.gtag = window.gtag || gtag;

  // Meta (Facebook/Instagram) Pixel
  if (CONFIG.metaPixelId) {
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", CONFIG.metaPixelId);
    window.fbq("track", "PageView");
  }

  /* ----------------------------------------------------------------------
     3) EVENTOS PERSONALIZADOS / CONVERSIONES
     La conversión principal es el clic a WhatsApp. Cada botón lleva
     data-wa="origen" (hero, popup, categoria, lista-precios, etc.)
     ---------------------------------------------------------------------- */
  function trackLead(source, label) {
    var payload = {
      event: "whatsapp_click",
      lead_source: source || "desconocido",
      lead_label: label || "",
      conversion_channel: "whatsapp"
    };
    dl(payload);
    // GA4: evento recomendado de generación de lead
    dl({ event: "generate_lead", currency: CONFIG.currency, value: CONFIG.leadValue, method: "whatsapp", lead_source: source });

    // Google Ads (conversión) vía gtag, si está configurado sin GTM
    if (!CONFIG.gtmId && window.gtag && CONFIG.googleAdsId && CONFIG.googleAdsConversionLabel) {
      window.gtag("event", "conversion", {
        send_to: CONFIG.googleAdsId + "/" + CONFIG.googleAdsConversionLabel,
        value: CONFIG.leadValue, currency: CONFIG.currency
      });
    }
    // Meta Pixel
    if (window.fbq) {
      window.fbq("track", "Contact", { content_name: label || source });
      window.fbq("track", "Lead", { value: CONFIG.leadValue, currency: CONFIG.currency });
    }
  }

  function trackEvent(name, params) { dl(Object.assign({ event: name }, params || {})); }

  // Delegación: cualquier elemento con [data-wa] dispara el lead
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-wa]");
    if (!el) return;
    trackLead(el.getAttribute("data-wa"), el.getAttribute("data-wa-label") || el.textContent.trim());
  });

  /* ----------------------------------------------------------------------
     4) UI: menú móvil
     ---------------------------------------------------------------------- */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("is-open"); navToggle.setAttribute("aria-expanded", "false"); }
    });
  }

  /* ----------------------------------------------------------------------
     5) UI: popup de WhatsApp (esquina inferior derecha)
     ---------------------------------------------------------------------- */
  var pop = document.getElementById("wa-pop");
  var waBtn = document.getElementById("wa-btn");
  var popClose = document.getElementById("wa-pop-close");
  var STORAGE_KEY = "csw_wa_pop_closed";

  function openPop() {
    if (!pop) return;
    pop.hidden = false;
    requestAnimationFrame(function () { pop.classList.remove("is-hidden"); });
    trackEvent("whatsapp_popup_open");
    var badge = document.getElementById("wa-badge");
    if (badge) badge.style.display = "none";
  }
  function closePop(remember) {
    if (!pop) return;
    pop.classList.add("is-hidden");
    setTimeout(function () { pop.hidden = true; }, 250);
    if (remember) { try { localStorage.setItem(STORAGE_KEY, "1"); } catch (_) {} }
  }

  if (waBtn && pop) {
    waBtn.addEventListener("click", function () {
      if (pop.hidden) openPop(); else closePop(false);
    });
  }
  if (popClose) popClose.addEventListener("click", function () { closePop(true); });

  // Auto-apertura una sola vez por visitante, salvo que ya lo haya cerrado
  var alreadyClosed = false;
  try { alreadyClosed = localStorage.getItem(STORAGE_KEY) === "1"; } catch (_) {}
  if (pop && !alreadyClosed) {
    setTimeout(openPop, 3500);
  }

  /* ----------------------------------------------------------------------
     6) UI: animaciones al hacer scroll
     ---------------------------------------------------------------------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ----------------------------------------------------------------------
     7) Misc
     ---------------------------------------------------------------------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // Marca de page_view enriquecida (por si se mide desde GTM)
  trackEvent("page_view_enriched", { page_type: "home", business: "casasilviaweb" });
})();
