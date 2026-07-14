/* ==========================================================================
   CASASILVIAWEB · carrito.js
   - Carrito mayorista persistido en localStorage (sobrevive entre visitas)
   - Badge en el header + drawer lateral en todas las páginas
   - Catálogo tipo vidriera en pedido.html: "Los más pedidos", secciones por
     línea con imagen, tarjetas con variantes de presentación (1L/4L/10L/20L)
   - Checkout: mensaje de WhatsApp formateado + redirección a gracias-pedido
     (conversión "purchase" para GA4 / Google Ads)
   ========================================================================== */
(function () {
  "use strict";

  var CFG = window.CSW_CONFIG || {};
  var CART_KEY = "csw_carrito_v1";
  var ORDER_KEY = "csw_last_order";
  var WA_NUMBER = CFG.whatsappNumber || "541166034047";
  var MINIMO = 300000;
  var PAGE_SIZE = 48;   // resultados de búsqueda por tanda
  var PREVIEW_N = 6;    // tarjetas visibles por línea antes de "ver todos"

  /* ------------------------------------------------------------------ utils */
  function $(id) { return document.getElementById(id); }
  function dl(obj) { (window.dataLayer = window.dataLayer || []).push(obj); }

  // GA4: sin GTM los push de objetos al dataLayer no llegan; hay que usar gtag()
  var USE_GTM = !!CFG.gtmId;
  function track(name, params) {
    if (USE_GTM) dl(Object.assign({ event: name }, params || {}));
    else if (window.gtag) window.gtag("event", name, params || {});
  }
  function gaItems(lines) {
    return lines.map(function (i) {
      return { item_id: i.cod, item_name: i.desc + (i.pres ? " " + i.pres : ""), price: i.precio, quantity: i.qty };
    });
  }

  function fmt(n) {
    return "$" + Number(n).toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function fmt0(n) {
    return "$" + Number(n).toLocaleString("es-AR", { maximumFractionDigits: 0 });
  }
  function normalize(s) {
    return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* ------------------------------------------------------------------ estado del carrito */
  // items: [{id, cod, desc, pack, pres, precio, qty}]
  function loadCart() {
    try {
      var raw = localStorage.getItem(CART_KEY);
      if (!raw) return [];
      var data = JSON.parse(raw);
      return Array.isArray(data.items) ? data.items : [];
    } catch (_) { return []; }
  }
  function saveCart() {
    try { localStorage.setItem(CART_KEY, JSON.stringify({ items: cart, ts: Date.now() })); } catch (_) {}
  }

  var cart = loadCart();

  function cartCount() { return cart.reduce(function (a, i) { return a + i.qty; }, 0); }
  function cartTotal() { return cart.reduce(function (a, i) { return a + (i.precio || 0) * i.qty; }, 0); }
  function findLine(id) {
    for (var i = 0; i < cart.length; i++) if (cart[i].id === id) return cart[i];
    return null;
  }

  function addToCart(prod, qty) {
    var line = findLine(prod.id);
    if (line) { line.qty += qty; }
    else {
      cart.push({ id: prod.id, cod: prod.cod, desc: prod.desc, pack: prod.pack, pres: prod.pres, precio: prod.precio, qty: qty });
    }
    saveCart(); renderCart();
    track("add_to_cart", { currency: "ARS", value: (prod.precio || 0) * qty, items: gaItems([{ cod: prod.cod, desc: prod.desc, pres: prod.pres, precio: prod.precio, qty: qty }]) });
  }

  function setQty(id, qty) {
    var line = findLine(id);
    if (!line) return;
    if (qty <= 0) { cart = cart.filter(function (i) { return i.id !== id; }); }
    else { line.qty = qty; }
    saveCart(); renderCart();
  }

  function emptyCart() { cart = []; saveCart(); renderCart(); }

  /* ------------------------------------------------------------------ WhatsApp */
  function buildMessage() {
    var lines = ["Hola CASASILVIAWEB! Quiero hacer este pedido:", ""];
    cart.forEach(function (i, idx) {
      var pres = [i.pack, i.pres].filter(Boolean).join(" ");
      lines.push((idx + 1) + ") " + i.qty + " x " + i.desc + (pres ? " (" + pres + ")" : ""));
      lines.push("    Cod. " + i.cod + " - " + fmt(i.precio || 0) + " c/u = *" + fmt((i.precio || 0) * i.qty) + "*");
    });
    lines.push("");
    lines.push("*TOTAL: " + fmt(cartTotal()) + "* (" + cartCount() + (cartCount() === 1 ? " bulto" : " bultos") + ")");
    lines.push("");
    lines.push("Enviado desde casasilviaweb.com.ar");
    return lines.join("\n");
  }
  function waLink(msg) {
    return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg);
  }
  function updateSendLink() {
    var send = $("cart-send");
    if (send) send.href = waLink(buildMessage());
  }

  /* ------------------------------------------------------------------ drawer */
  var layer = $("cart-layer");

  function openCart() {
    if (!layer) return;
    layer.hidden = false;
    requestAnimationFrame(function () { layer.classList.add("is-open"); });
    document.documentElement.classList.add("cart-lock");
    track("view_cart", { currency: "ARS", value: cartTotal(), items: gaItems(cart) });
  }
  function closeCart() {
    if (!layer) return;
    layer.classList.remove("is-open");
    document.documentElement.classList.remove("cart-lock");
    setTimeout(function () { layer.hidden = true; }, 280);
  }

  function renderCart() {
    var badge = $("cart-badge"), items = $("cart-items"), empty = $("cart-empty"),
        foot = $("cart-foot"), total = $("cart-total"), label = $("cart-count-label"),
        minimo = $("cart-minimo"), falta = $("cart-minimo-falta");
    var n = cartCount(), t = cartTotal();

    if (badge) {
      badge.hidden = n === 0;
      badge.textContent = n > 99 ? "99+" : String(n);
    }
    if (label) label.textContent = n === 0 ? "Sin productos" : (n + (n === 1 ? " bulto" : " bultos") + " · " + cart.length + (cart.length === 1 ? " producto" : " productos"));
    if (empty) empty.hidden = cart.length > 0;
    if (foot) foot.hidden = cart.length === 0;

    if (items) {
      items.innerHTML = cart.map(function (i) {
        var pres = [i.pack, i.pres].filter(Boolean).join(" · ");
        return '<li class="cart-item" data-id="' + esc(i.id) + '">' +
          '<div class="cart-item__info">' +
            '<b>' + esc(i.desc) + '</b>' +
            '<span class="cart-item__meta">' + (pres ? esc(pres) + " · " : "") + 'Cód. ' + esc(i.cod) + '</span>' +
            '<span class="cart-item__price">' + fmt(i.precio || 0) + ' c/u</span>' +
          '</div>' +
          '<div class="cart-item__side">' +
            '<div class="qty"><button type="button" class="qty__btn" data-cart-menos aria-label="Restar uno"><svg class="line" aria-hidden="true"><use href="#i-minus"></use></svg></button>' +
            '<input class="qty__num" type="number" min="0" inputmode="numeric" value="' + i.qty + '" data-cart-qty aria-label="Cantidad">' +
            '<button type="button" class="qty__btn" data-cart-mas aria-label="Sumar uno"><svg class="line" aria-hidden="true"><use href="#i-plus"></use></svg></button></div>' +
            '<b class="cart-item__sub">' + fmt((i.precio || 0) * i.qty) + '</b>' +
            '<button type="button" class="cart-item__del" data-cart-del aria-label="Quitar del pedido"><svg class="line" aria-hidden="true"><use href="#i-trash"></use></svg></button>' +
          '</div></li>';
      }).join("");
    }
    if (total) total.textContent = fmt(t);
    if (minimo) {
      var debajo = cart.length > 0 && t < MINIMO;
      minimo.hidden = !debajo;
      if (debajo && falta) falta.textContent = fmt0(MINIMO - t);
    }
    updateSendLink();
    renderStickyBar();
    syncCatalogButtons();
  }

  // eventos del drawer
  if (layer) {
    var openBtn = $("cart-open"), closeBtn = $("cart-close"), backdrop = $("cart-backdrop");
    if (openBtn) openBtn.addEventListener("click", openCart);
    if (closeBtn) closeBtn.addEventListener("click", closeCart);
    if (backdrop) backdrop.addEventListener("click", closeCart);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !layer.hidden) closeCart(); });

    layer.addEventListener("click", function (e) {
      var li = e.target.closest(".cart-item");
      if (!li) return;
      var id = li.getAttribute("data-id"), line = findLine(id);
      if (!line) return;
      if (e.target.closest("[data-cart-mas]")) setQty(id, line.qty + 1);
      else if (e.target.closest("[data-cart-menos]")) setQty(id, line.qty - 1);
      else if (e.target.closest("[data-cart-del]")) setQty(id, 0);
    });
    layer.addEventListener("change", function (e) {
      if (!e.target.matches("[data-cart-qty]")) return;
      var li = e.target.closest(".cart-item");
      var q = parseInt(e.target.value, 10);
      setQty(li.getAttribute("data-id"), isNaN(q) ? 1 : q);
    });

    // Checkout: guarda el pedido, abre WhatsApp (target=_blank) y lleva esta
    // pestaña a la página de gracias (ahí se marca la conversión "purchase").
    var sendBtn = $("cart-send");
    if (sendBtn) sendBtn.addEventListener("click", function () {
      var order = { items: cart.slice(), total: cartTotal(), count: cartCount(), ts: Date.now(), msg: buildMessage() };
      try { localStorage.setItem(ORDER_KEY, JSON.stringify(order)); } catch (_) {}
      track("begin_checkout", { currency: "ARS", value: order.total, items: gaItems(cart) });
      setTimeout(function () { location.href = "gracias-pedido.html"; }, 900);
    });
  }

  /* ------------------------------------------------------------------ catálogo (pedido.html) */
  var listEl = $("prod-list");

  var CAT_NAMES = {
    "tornillos-autoperforantes": "Tornillos",
    "clavos-y-alambres": "Clavos y Alambres",
    "tirafondos-y-fijaciones": "Tirafondos y Fijaciones",
    "hierros-y-mallas": "Hierros",
    "soldadura": "Soldadura",
    "pinturas-y-quimicos": "Pinturas y Químicos"
  };
  // Pictogramas por línea (símbolos p-* del sprite). Nada de fotos genéricas:
  // cada línea muestra un ícono representativo del producto real.
  var CAT_ICON = {
    "tornillos-autoperforantes": "p-screw-hex",
    "clavos-y-alambres": "p-nail",
    "tirafondos-y-fijaciones": "p-lag",
    "hierros-y-mallas": "p-rebar",
    "soldadura": "p-weld",
    "pinturas-y-quimicos": "p-paint"
  };
  var GRUPO_ICON = {
    "Hexagonal punta ranurada/aguja": "p-screw-hex",
    "Hexagonal punta mecha": "p-screw-hex",
    "FIX": "p-screw",
    "Deck T25": "p-screw",
    "Hormigón T30": "p-screw",
    "Drywall madera": "p-screw-drywall",
    "Drywall metal punta aguja": "p-screw-drywall",
    "Drywall metal punta mecha": "p-screw-drywall",
    "Tanque aguja": "p-screw-pan",
    "Tanque mecha": "p-screw-pan",
    "Tanque p/tuerca": "p-screw-pan",
    "Parker aguja": "p-screw-pan",
    "Parker mecha": "p-screw-pan",
    "Pan framing": "p-screw-pan",
    "Ensamblador": "p-screw",
    "Tipo KREG (oculto)": "p-screw",
    "Punta mecha con alas": "p-screw",
    "Tirafondos": "p-lag",
    "Tuercas hexagonales": "p-nut",
    "Arandelas planas": "p-washer",
    "Arandelas chapista": "p-washer",
    "Tarugos comunes sin tope": "p-plug",
    "Tarugos comunes con tope": "p-plug",
    "Tarugos universales sin tope": "p-plug",
    "Tarugos universales con tope": "p-plug",
    "Tarugos FX (hueco)": "p-plug",
    "Tarugos yeso/durlock": "p-plug",
    "Tarugos mariposa": "p-plug",
    "Grampas Omega": "p-clamp",
    "Grampas": "p-staple",
    "Ganchos J": "p-hook",
    "Torniquetes": "p-turnbuckle",
    "Alambre galvanizado": "p-wire",
    "Alambre negro recocido": "p-wire",
    "Alambre para soldar (MIG)": "p-weld",
    "Alambre de púas": "p-barbed",
    "Concertina": "p-barbed",
    "Alambre tejido": "p-mesh",
    "Hierro dulce": "p-rebar",
    "Electrodos": "p-weld",
    "Látex Símbolo-Tex": "p-paint",
    "Sintéticos 3 en 1": "p-can",
    "Polvos y morteros": "p-bag",
    "Pinturas al agua y cal": "p-paint",
    "Polvos para colorear": "p-pigment",
    "Combustibles y diluyentes": "p-jerrican",
    "Asfaltos": "p-paint",
    "Químicos Símbolo-Tex": "p-flask",
    "Vendas y mantas sintéticas": "p-roll",
    "Accesorios y varios": "p-tape",
    "Cibel / Casablanca / Tintas": "p-can",
    "Rodillos y pinceles El Galgo": "p-roller",
    "Cetol / Brik-Col (nuevos ingresos)": "p-can"
  };
  function grupoIcon(grupo, cat) {
    return GRUPO_ICON[grupo] || CAT_ICON[cat] || "p-screw";
  }
  function iconSvg(grupo, cat) {
    return '<svg class="line" aria-hidden="true"><use href="#' + grupoIcon(grupo, cat) + '"></use></svg>';
  }

  // Los más pedidos (por id; el orden es el de la vidriera)
  var DESTACADOS = ["CLA04", "ALA06", "PIN007", "N001066", "PIN019", "i001074", "N001035", "i001489"];

  var ITEMS = [];      // productos crudos del JSON
  var CARDS = [];      // tarjetas: variantes agrupadas por (cat, grupo, desc)
  var CARD_BY_VID = {}; // id de variante -> tarjeta
  var GRUPOS = [];     // [{grupo, cat, cards:[...]}] en orden de lista
  var expanded = {};   // grupo -> true (ver todos)
  var state = { q: "", cat: "", grupo: "" };
  var shownFlat = 0, flatCards = [];

  function buildCards() {
    var byKey = {}, order = [];
    ITEMS.forEach(function (p) {
      var key = p.cat + "|" + p.grupo + "|" + p.desc;
      if (!byKey[key]) {
        byKey[key] = { key: key, desc: p.desc, grupo: p.grupo, cat: p.cat, variants: [] };
        order.push(byKey[key]);
      }
      byKey[key].variants.push(p);
    });
    CARDS = order;
    CARDS.forEach(function (c) {
      c.variants.forEach(function (v) { CARD_BY_VID[v.id] = c; });
    });
    var gid = {};
    GRUPOS = [];
    CARDS.forEach(function (c) {
      var k = c.cat + "|" + c.grupo;
      if (!gid[k]) { gid[k] = { grupo: c.grupo, cat: c.cat, cards: [] }; GRUPOS.push(gid[k]); }
      gid[k].cards.push(c);
    });
  }

  function cardMatches(c) {
    if (state.cat && c.cat !== state.cat) return false;
    if (state.grupo && c.grupo !== state.grupo) return false;
    var q = normalize(state.q).split(/\s+/).filter(Boolean);
    if (!q.length) return true;
    var hay = normalize(c.desc + " " + c.grupo + " " + c.variants.map(function (v) { return v.cod + " " + v.pres + " " + v.pack; }).join(" "));
    return q.every(function (t) { return hay.indexOf(t) !== -1; });
  }

  /* ---------------- tarjeta de producto (con variantes de presentación) */
  function pillLabels(variants) {
    // etiqueta que distinga cada variante: presentación, si no alcanza el
    // pack (caja x5000 vs x5500), y como último recurso el código
    function dup(l) {
      var seen = {};
      for (var i = 0; i < l.length; i++) { if (seen[l[i]]) return true; seen[l[i]] = 1; }
      return false;
    }
    var l = variants.map(function (v) { return v.pres || v.pack || v.cod; });
    if (dup(l)) l = variants.map(function (v) { return v.pack || v.pres || v.cod; });
    if (dup(l)) l = variants.map(function (v) { return [v.pack, v.pres].filter(Boolean).join(" ") || v.cod; });
    if (dup(l)) l = variants.map(function (v) { return v.cod; });
    return l;
  }

  // Marcas conocidas dentro de las descripciones -> chip destacado
  var BRANDS = [
    ["LOMA NEGRA", "Loma Negra"], ["SIMBOLO-TEX", "Símbolo-Tex"], ["SÍMBOLO-TEX", "Símbolo-Tex"],
    ["SIMBOLOTEX", "Símbolo-Tex"], ["CIBEL", "Cibel"], ["CASABLANCA", "Casablanca"],
    ["SINTEPLAST", "Sinteplast"], ["EL GALGO", "El Galgo"], ["CETOL", "Cetol"],
    ["BRIK-COL", "Brik-Col"], ["TRI-MAS", "Tri-Mas"], ["TRIMAS", "Tri-Mas"],
    ["PENETRIT", "Penetrit"], ["STA ELENA", "Sta. Elena"], ["MAGIPLAST", "Magiplast"],
    ["GERDAU", "Gerdau"], ["KRG", "Tipo KREG"], ["KREG", "Tipo KREG"]
  ];
  function brandOf(desc, grupo) {
    var hay = (desc + " " + grupo).toUpperCase();
    for (var i = 0; i < BRANDS.length; i++) if (hay.indexOf(BRANDS[i][0]) !== -1) return BRANDS[i][1];
    return null;
  }
  function packLabel(pack) { return pack ? pack + " u." : ""; }

  function cardHTML(c, opts) {
    opts = opts || {};
    var sel = 0;
    if (opts.preferId) c.variants.forEach(function (v, i) { if (v.id === opts.preferId) sel = i; });
    var v0 = c.variants[sel];
    var multi = c.variants.length > 1;
    var pills = "", labels = null;
    if (multi) {
      labels = pillLabels(c.variants);
      pills = '<div class="prod__pills" role="group" aria-label="Presentaciones">' + c.variants.map(function (v, i) {
        return '<button type="button" class="pill' + (i === sel ? " is-active" : "") + '" data-vid="' + esc(v.id) + '">' + esc(labels[i]) + '</button>';
      }).join("") + '</div>';
    }

    // Chips visuales: marca + cantidad por bulto (x2000 u.) + presentación (Granel)
    var pillsUsePres = multi && labels[sel] === (v0.pres || "");
    var tags = [];
    var brand = brandOf(c.desc, c.grupo);
    if (brand) tags.push('<span class="tagchip tagchip--brand">' + esc(brand) + '</span>');
    tags.push('<span class="tagchip tagchip--pack" data-chip-pack' + (v0.pack ? "" : " hidden") + '>' + esc(packLabel(v0.pack)) + '</span>');
    tags.push('<span class="tagchip tagchip--pres" data-chip-pres' + (v0.pres && !pillsUsePres ? "" : " hidden") + '>' + esc(v0.pres || "") + '</span>');
    var tagsHtml = '<div class="prod__tags">' + tags.join("") + '</div>';

    var meta = [];
    meta.push('Cód. <span class="prod__cod">' + esc(v0.cod) + '</span>');
    if (v0.sinStock) meta.push('<span class="prod__stock">Sin stock — consultá</span>');

    var precio = v0.precio == null
      ? '<a class="prod__consultar" href="' + waLink("Hola CASASILVIAWEB! Quiero consultar el precio de: " + c.desc + " (Cód. " + v0.cod + ")") + '" target="_blank" rel="noopener" data-wa="pedido-consulta" data-wa-label="Consulta precio ' + esc(v0.cod) + '">Consultar precio</a>'
      : '<b class="prod__precio">' + fmt(v0.precio) + '</b>';
    var controls = v0.precio == null ? "" :
      '<div class="prod__acciones">' +
        '<div class="qty"><button type="button" class="qty__btn" data-menos aria-label="Restar uno"><svg class="line" aria-hidden="true"><use href="#i-minus"></use></svg></button>' +
        '<input class="qty__num" type="number" min="1" inputmode="numeric" value="1" aria-label="Cantidad">' +
        '<button type="button" class="qty__btn" data-mas aria-label="Sumar uno"><svg class="line" aria-hidden="true"><use href="#i-plus"></use></svg></button></div>' +
        '<button type="button" class="btn btn--add" data-agregar><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg><span>Agregar</span></button>' +
      '</div>';

    var img = opts.img ? '<div class="prod__hero">' + iconSvg(c.grupo, c.cat) +
      '<span class="prod__badge"><svg class="fill" aria-hidden="true"><use href="#i-star"></use></svg> Más pedido</span></div>' : "";

    return '<article class="prod' + (opts.img ? " prod--star" : "") + (v0.sinStock ? " prod--sinstock" : "") + '" data-key="' + esc(c.key) + '" data-sel="' + esc(v0.id) + '">' +
      img +
      '<div class="prod__main">' +
        '<h3 class="prod__nombre">' + esc(c.desc) + '</h3>' +
        tagsHtml +
        '<div class="prod__meta">' + meta.map(function (m) { return "<span>" + m + "</span>"; }).join("") + '</div>' +
        pills +
        '<span class="prod__encart" hidden><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg> <b>0</b> en tu pedido</span>' +
      '</div>' +
      '<div class="prod__buy">' + precio + controls + '</div>' +
    '</article>';
  }

  function findCardByKey(key) {
    for (var i = 0; i < CARDS.length; i++) if (CARDS[i].key === key) return CARDS[i];
    return null;
  }
  function findItem(id) {
    for (var i = 0; i < ITEMS.length; i++) if (ITEMS[i].id === id) return ITEMS[i];
    return null;
  }

  /* ---------------- render principal */
  function renderCatalog() {
    var res = $("pedido-result");
    var moreBtn = $("pedido-mas");
    var destacadosWrap = $("destacados-wrap");
    var matched = CARDS.filter(cardMatches);
    var searching = !!(state.q || state.grupo);

    if (destacadosWrap) destacadosWrap.hidden = searching;

    if (searching) {
      flatCards = matched;
      shownFlat = 0;
      listEl.innerHTML = "";
      if (res) res.textContent = matched.length + (matched.length === 1 ? " producto encontrado" : " productos encontrados");
      renderFlatMore();
      if (!matched.length) {
        listEl.innerHTML = '<div class="prod-vacio"><p><b>No encontramos productos con esa búsqueda.</b></p>' +
          '<p>Probá con menos palabras (ej: "fix 4.5", "latex 20" o "tirafondo 1/4") o <a href="' + waLink("Hola CASASILVIAWEB! Estoy buscando: " + state.q) + '" target="_blank" rel="noopener" data-wa="pedido-sin-resultado" data-wa-label="Búsqueda sin resultado">consultanos por WhatsApp</a>.</p></div>';
        if (moreBtn) moreBtn.hidden = true;
      }
    } else {
      if (res) res.textContent = "";
      if (moreBtn) moreBtn.hidden = true;
      renderDestacados();
      renderGrouped(matched);
    }
    syncCatalogButtons();
  }

  function renderFlatMore() {
    var next = flatCards.slice(shownFlat, shownFlat + PAGE_SIZE);
    if (shownFlat === 0) listEl.innerHTML = '<div class="prod-grid"></div>';
    listEl.querySelector(".prod-grid").insertAdjacentHTML("beforeend", next.map(function (c) { return cardHTML(c); }).join(""));
    shownFlat += next.length;
    var more = $("pedido-mas");
    if (more) {
      more.hidden = shownFlat >= flatCards.length;
      more.textContent = "Mostrar más productos (" + (flatCards.length - shownFlat) + " restantes)";
    }
    syncCatalogButtons();
  }

  function renderDestacados() {
    var row = $("destacados");
    if (!row) return;
    var html = DESTACADOS.map(function (id) {
      var c = CARD_BY_VID[id];
      if (!c) return "";
      if (state.cat && c.cat !== state.cat) return "";
      return cardHTML(c, { img: true, preferId: id });
    }).join("");
    row.innerHTML = html;
    var wrap = $("destacados-wrap");
    if (wrap) wrap.hidden = !html;
  }

  function renderGrouped(matchedCards) {
    var matchedKeys = {};
    matchedCards.forEach(function (c) { matchedKeys[c.key] = true; });
    var html = "", lastCat = null;
    GRUPOS.forEach(function (g) {
      var cards = g.cards.filter(function (c) { return matchedKeys[c.key]; });
      if (!cards.length) return;
      if (g.cat !== lastCat) {
        lastCat = g.cat;
        html += '<div class="cat-divider"><h2>' + esc(CAT_NAMES[g.cat] || g.cat) + '</h2><span></span></div>';
      }
      var isOpen = !!expanded[g.grupo];
      var visible = isOpen ? cards : cards.slice(0, PREVIEW_N);
      var totalSkus = cards.reduce(function (a, c) { return a + c.variants.length; }, 0);
      html += '<section class="grupo" data-grupo="' + esc(g.grupo) + '">' +
        '<header class="grupo__head">' +
          '<span class="grupo__ic">' + iconSvg(g.grupo, g.cat) + '</span>' +
          '<div><h3>' + esc(g.grupo) + '</h3><span>' + totalSkus + (totalSkus === 1 ? " producto" : " productos") + ' · ' + esc(CAT_NAMES[g.cat] || "") + '</span></div>' +
        '</header>' +
        '<div class="prod-grid">' + visible.map(function (c) { return cardHTML(c); }).join("") + '</div>' +
        (cards.length > PREVIEW_N
          ? '<button type="button" class="grupo__mas" data-grupo-mas>' + (isOpen ? "Ver menos" : "Ver los " + cards.length + " productos de esta línea") + "</button>"
          : "") +
      '</section>';
    });
    listEl.innerHTML = html;
    syncCatalogButtons();
  }

  /* ---------------- sincronización de estado en las tarjetas */
  function renderStickyBar() {
    var bar = $("pedido-sticky");
    if (!bar) return;
    var n = cartCount();
    bar.hidden = n === 0;
    if (n > 0) {
      $("pedido-sticky-n").textContent = n + (n === 1 ? " bulto" : " bultos");
      $("pedido-sticky-total").textContent = fmt(cartTotal());
    }
  }

  function syncCatalogButtons() {
    if (!listEl) return;
    document.querySelectorAll(".prod[data-key]").forEach(function (card) {
      var c = findCardByKey(card.getAttribute("data-key"));
      if (!c) return;
      var total = c.variants.reduce(function (a, v) { var l = findLine(v.id); return a + (l ? l.qty : 0); }, 0);
      var flag = card.querySelector(".prod__encart");
      if (flag) {
        flag.hidden = total === 0;
        if (total) flag.querySelector("b").textContent = String(total);
      }
    });
  }

  /* ---------------- filtros */
  function buildFilters() {
    var chips = $("pedido-chips");
    var cats = [];
    ITEMS.forEach(function (p) { if (cats.indexOf(p.cat) === -1) cats.push(p.cat); });
    chips.innerHTML = '<button type="button" class="chip is-active" data-cat="">Todo</button>' +
      cats.map(function (c) {
        return '<button type="button" class="chip" data-cat="' + esc(c) + '">' + esc(CAT_NAMES[c] || c) + '</button>';
      }).join("");
    chips.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      state.cat = b.getAttribute("data-cat");
      chips.querySelectorAll(".chip").forEach(function (x) { x.classList.toggle("is-active", x === b); });
      state.grupo = "";
      buildGrupoSelect();
      $("pedido-grupo").value = "";
      renderCatalog();
    });

    var sel = $("pedido-grupo");
    sel.addEventListener("change", function () { state.grupo = sel.value; renderCatalog(); });
    buildGrupoSelect();

    var input = $("buscador"), t = null;
    input.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        state.q = input.value.trim();
        renderCatalog();
        if (state.q.length >= 3) track("search", { search_term: state.q });
      }, 160);
    });

    // ?cat= desde las páginas de categoría
    var m = location.search.match(/[?&]cat=([\w-]+)/);
    if (m) {
      var target = chips.querySelector('[data-cat="' + m[1] + '"]');
      if (target) target.click();
    }
  }

  function buildGrupoSelect() {
    var sel = $("pedido-grupo");
    var grupos = [];
    ITEMS.forEach(function (p) {
      if (state.cat && p.cat !== state.cat) return;
      if (grupos.indexOf(p.grupo) === -1) grupos.push(p.grupo);
    });
    sel.innerHTML = '<option value="">Todas las líneas</option>' +
      grupos.map(function (g) { return '<option>' + esc(g) + "</option>"; }).join("");
  }

  /* ---------------- arranque del catálogo */
  function initCatalog() {
    fetch("assets/data/productos.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        ITEMS = data.items;
        buildCards();
        var tot = $("pedido-total-productos");
        if (tot) tot.textContent = String(ITEMS.length);
        buildFilters();
        renderCatalog();
      })
      .catch(function () {
        listEl.innerHTML = '<div class="prod-vacio"><p><b>No pudimos cargar el catálogo.</b></p>' +
          '<p>Recargá la página o <a href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener">pedinos la lista por WhatsApp</a>.</p></div>';
      });

    var moreBtn = $("pedido-mas");
    if (moreBtn) moreBtn.addEventListener("click", renderFlatMore);

    // interacción con las tarjetas (delegado en todo el documento: los
    // destacados viven fuera de #prod-list)
    document.addEventListener("click", function (e) {
      var card = e.target.closest(".prod[data-key]");
      if (!card) {
        var gm = e.target.closest("[data-grupo-mas]");
        if (gm) {
          var sec = gm.closest(".grupo");
          var grupo = sec.getAttribute("data-grupo");
          expanded[grupo] = !expanded[grupo];
          renderCatalog();
          if (!expanded[grupo]) sec = document.querySelector('.grupo[data-grupo="' + grupo.replace(/"/g, '\\"') + '"]');
        }
        return;
      }
      var qtyInput = card.querySelector(".qty__num");

      // cambiar presentación (pill)
      var pill = e.target.closest(".pill[data-vid]");
      if (pill) {
        var vid = pill.getAttribute("data-vid");
        var item = findItem(vid);
        if (!item) return;
        card.setAttribute("data-sel", vid);
        card.querySelectorAll(".pill").forEach(function (x) { x.classList.toggle("is-active", x === pill); });
        var priceEl = card.querySelector(".prod__precio");
        if (priceEl) priceEl.textContent = fmt(item.precio);
        var codEl = card.querySelector(".prod__cod");
        if (codEl) codEl.textContent = item.cod;
        // chips de bulto/presentación de la variante elegida
        var packChip = card.querySelector("[data-chip-pack]");
        if (packChip) {
          packChip.hidden = !item.pack;
          packChip.textContent = packLabel(item.pack);
        }
        var presChip = card.querySelector("[data-chip-pres]");
        if (presChip) {
          var dupPill = pill.textContent === (item.pres || "");
          presChip.hidden = !item.pres || dupPill;
          presChip.textContent = item.pres || "";
        }
        return;
      }

      if (e.target.closest("[data-mas]") && qtyInput) qtyInput.value = String((parseInt(qtyInput.value, 10) || 1) + 1);
      else if (e.target.closest("[data-menos]") && qtyInput) qtyInput.value = String(Math.max(1, (parseInt(qtyInput.value, 10) || 1) - 1));
      else if (e.target.closest("[data-agregar]")) {
        var prod = findItem(card.getAttribute("data-sel"));
        if (!prod) return;
        var q = Math.max(1, parseInt(qtyInput.value, 10) || 1);
        addToCart(prod, q);
        qtyInput.value = "1";
        var btn = e.target.closest("[data-agregar]");
        btn.classList.add("is-added");
        var span = btn.querySelector("span");
        span.textContent = "¡Agregado!";
        setTimeout(function () { btn.classList.remove("is-added"); span.textContent = "Agregar"; }, 1200);
      }
    });

    // barra inferior fija con total en tiempo real
    var sticky = document.createElement("div");
    sticky.className = "pedido-sticky";
    sticky.id = "pedido-sticky";
    sticky.hidden = true;
    sticky.innerHTML = '<div class="pedido-sticky__info"><span id="pedido-sticky-n"></span><b id="pedido-sticky-total"></b></div>' +
      '<button type="button" class="btn btn--wa" id="pedido-sticky-ver"><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg>Ver pedido</button>';
    document.body.appendChild(sticky);
    $("pedido-sticky-ver").addEventListener("click", openCart);
  }

  if (listEl) initCatalog();

  /* ------------------------------------------------------------------ página de gracias (conversión) */
  var graciasPedido = $("gracias-pedido");
  if (graciasPedido) {
    var order = null;
    try { order = JSON.parse(localStorage.getItem(ORDER_KEY) || "null"); } catch (_) {}
    if (order && order.items && order.items.length) {
      // conversión "purchase" (una sola vez por pedido)
      var fired = null;
      try { fired = localStorage.getItem("csw_purchase_fired"); } catch (_) {}
      if (String(order.ts) !== fired) {
        track("purchase", {
          transaction_id: "wa-" + order.ts, currency: "ARS", value: order.total,
          items: gaItems(order.items)
        });
        // conversión de Google Ads (si está configurada y no se gestiona por GTM)
        if (!USE_GTM && window.gtag && CFG.googleAdsId && CFG.googleAdsConversionLabel) {
          window.gtag("event", "conversion", {
            send_to: CFG.googleAdsId + "/" + CFG.googleAdsConversionLabel,
            value: order.total, currency: "ARS", transaction_id: "wa-" + order.ts
          });
        }
        try { localStorage.setItem("csw_purchase_fired", String(order.ts)); } catch (_) {}
      }

      // resumen del pedido en pantalla
      var resumen = $("gracias-resumen");
      if (resumen) {
        resumen.hidden = false;
        resumen.querySelector("tbody").innerHTML = order.items.map(function (i) {
          var pres = [i.pack, i.pres].filter(Boolean).join(" ");
          return "<tr><td>" + i.qty + " × " + esc(i.desc) + (pres ? " <small>(" + esc(pres) + ")</small>" : "") + "</td><td>" + fmt((i.precio || 0) * i.qty) + "</td></tr>";
        }).join("");
        $("gracias-total").textContent = fmt(order.total);
      }
      var waAgain = $("gracias-wa");
      if (waAgain) waAgain.href = waLink(order.msg || buildMessage());
    }
    var vaciar = $("gracias-vaciar");
    if (vaciar) vaciar.addEventListener("click", function () {
      emptyCart();
      vaciar.textContent = "Carrito vaciado ✓";
      vaciar.disabled = true;
    });
  }

  if ($("gracias-contacto")) {
    track("lead_gracias_page", { method: "whatsapp" });
  }

  /* ------------------------------------------------------------------ arranque */
  renderCart();
})();
