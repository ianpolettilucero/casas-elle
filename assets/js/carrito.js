/* ==========================================================================
   CASASILVIAWEB · carrito.js
   - Carrito mayorista persistido en localStorage (sobrevive entre visitas)
   - Badge en el header + drawer lateral en todas las páginas
   - Catálogo con buscador y filtros en pedido.html (assets/data/productos.json)
   - Checkout: arma el mensaje de WhatsApp con cantidades, precios y total
   ========================================================================== */
(function () {
  "use strict";

  var CART_KEY = "csw_carrito_v1";
  var WA_NUMBER = (window.CSW_CONFIG && window.CSW_CONFIG.whatsappNumber) || "541166034047";
  var MINIMO = 300000;
  var PAGE_SIZE = 60;

  /* ------------------------------------------------------------------ utils */
  function $(id) { return document.getElementById(id); }
  function dl(obj) { (window.dataLayer = window.dataLayer || []).push(obj); }

  function fmt(n) {
    return "$" + Number(n).toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function fmt0(n) {
    return "$" + Number(n).toLocaleString("es-AR", { maximumFractionDigits: 0 });
  }

  function normalize(s) {
    return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  /* ------------------------------------------------------------------ estado */
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
    dl({ event: "add_to_cart", currency: "ARS", value: (prod.precio || 0) * qty,
         items: [{ item_id: prod.cod, item_name: prod.desc, price: prod.precio, quantity: qty }] });
  }

  function setQty(id, qty) {
    var line = findLine(id);
    if (!line) return;
    if (qty <= 0) { cart = cart.filter(function (i) { return i.id !== id; }); }
    else { line.qty = qty; }
    saveCart(); renderCart();
  }

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

  function updateSendLink() {
    var send = $("cart-send");
    if (!send) return;
    send.href = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(buildMessage());
  }

  /* ------------------------------------------------------------------ drawer */
  var layer = $("cart-layer");

  function openCart() {
    if (!layer) return;
    layer.hidden = false;
    requestAnimationFrame(function () { layer.classList.add("is-open"); });
    document.documentElement.classList.add("cart-lock");
    dl({ event: "view_cart", currency: "ARS", value: cartTotal() });
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
        return '<li class="cart-item" data-id="' + i.id + '">' +
          '<div class="cart-item__info">' +
            '<b>' + i.desc + '</b>' +
            '<span class="cart-item__meta">' + (pres ? pres + " · " : "") + 'Cód. ' + i.cod + '</span>' +
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
    var sendBtn = $("cart-send");
    if (sendBtn) sendBtn.addEventListener("click", function () {
      dl({ event: "begin_checkout", currency: "ARS", value: cartTotal(),
           items: cart.map(function (i) { return { item_id: i.cod, item_name: i.desc, price: i.precio, quantity: i.qty }; }) });
    });
  }

  /* ------------------------------------------------------------------ catálogo (pedido.html) */
  var listEl = $("prod-list");
  var PRODUCTS = [], FILTERED = [], shown = 0;
  var CAT_NAMES = {
    "tornillos-autoperforantes": "Tornillos",
    "clavos-y-alambres": "Clavos y Alambres",
    "tirafondos-y-fijaciones": "Tirafondos y Fijaciones",
    "hierros-y-mallas": "Hierros",
    "soldadura": "Soldadura"
  };
  var state = { q: "", cat: "", grupo: "" };

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
    listEl.querySelectorAll(".prod").forEach(function (card) {
      var line = findLine(card.getAttribute("data-id"));
      var flag = card.querySelector(".prod__encart");
      if (flag) {
        flag.hidden = !line;
        if (line) flag.querySelector("b").textContent = String(line.qty);
      }
    });
  }

  function prodCard(p) {
    var pres = [p.pack, p.pres].filter(Boolean).join(" · ");
    var precio = p.precio == null
      ? '<a class="prod__consultar" href="https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hola CASASILVIAWEB! Quiero consultar el precio de: " + p.desc + " (Cód. " + p.cod + ")") + '" target="_blank" rel="noopener" data-wa="pedido-consulta" data-wa-label="Consulta precio ' + p.cod + '">Consultar precio</a>'
      : '<b class="prod__precio">' + fmt(p.precio) + '</b>';
    var controls = p.precio == null ? "" :
      '<div class="prod__acciones">' +
        '<div class="qty"><button type="button" class="qty__btn" data-menos aria-label="Restar uno"><svg class="line" aria-hidden="true"><use href="#i-minus"></use></svg></button>' +
        '<input class="qty__num" type="number" min="1" inputmode="numeric" value="1" aria-label="Cantidad">' +
        '<button type="button" class="qty__btn" data-mas aria-label="Sumar uno"><svg class="line" aria-hidden="true"><use href="#i-plus"></use></svg></button></div>' +
        '<button type="button" class="btn btn--add" data-agregar><svg class="line" aria-hidden="true"><use href="#i-cart"></use></svg><span>Agregar</span></button>' +
      '</div>';
    return '<article class="prod' + (p.sinStock ? " prod--sinstock" : "") + '" data-id="' + p.id + '">' +
      '<div class="prod__main">' +
        '<h3 class="prod__nombre">' + p.desc + '</h3>' +
        '<div class="prod__meta">' +
          '<span class="prod__grupo">' + p.grupo + '</span>' +
          (pres ? '<span>' + pres + '</span>' : "") +
          '<span class="prod__cod">Cód. ' + p.cod + '</span>' +
          (p.sinStock ? '<span class="prod__stock">Sin stock — consultá</span>' : "") +
        '</div>' +
        '<span class="prod__encart" hidden><svg class="line" aria-hidden="true"><use href="#i-check"></use></svg> <b>0</b> en tu pedido</span>' +
      '</div>' +
      '<div class="prod__compra">' + precio + controls + '</div>' +
    '</article>';
  }

  function applyFilter() {
    var q = normalize(state.q).split(/\s+/).filter(Boolean);
    FILTERED = PRODUCTS.filter(function (p) {
      if (state.cat && p.cat !== state.cat) return false;
      if (state.grupo && p.grupo !== state.grupo) return false;
      if (!q.length) return true;
      var hay = normalize(p.desc + " " + p.grupo + " " + p.cod);
      return q.every(function (term) { return hay.indexOf(term) !== -1; });
    });
    shown = 0;
    listEl.innerHTML = "";
    renderMore();
    var res = $("pedido-result");
    if (res) res.textContent = FILTERED.length === PRODUCTS.length
      ? ""
      : FILTERED.length + (FILTERED.length === 1 ? " producto encontrado" : " productos encontrados");
  }

  function renderMore() {
    var next = FILTERED.slice(shown, shown + PAGE_SIZE);
    listEl.insertAdjacentHTML("beforeend", next.map(prodCard).join(""));
    shown += next.length;
    var more = $("pedido-mas");
    if (more) {
      more.hidden = shown >= FILTERED.length;
      more.textContent = "Mostrar más productos (" + (FILTERED.length - shown) + " restantes)";
    }
    if (!FILTERED.length) {
      listEl.innerHTML = '<div class="prod-vacio"><p><b>No encontramos productos con esa búsqueda.</b></p>' +
        '<p>Probá con menos palabras (ej: “fix 4.5” o “tirafondo 1/4”) o <a href="https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hola CASASILVIAWEB! Estoy buscando: " + state.q) + '" target="_blank" rel="noopener" data-wa="pedido-sin-resultado" data-wa-label="Búsqueda sin resultado">consultanos por WhatsApp</a>.</p></div>';
    }
    syncCatalogButtons();
  }

  function buildFilters() {
    // chips de categoría
    var chips = $("pedido-chips");
    var cats = [];
    PRODUCTS.forEach(function (p) { if (cats.indexOf(p.cat) === -1) cats.push(p.cat); });
    chips.innerHTML = '<button type="button" class="chip is-active" data-cat="">Todo</button>' +
      cats.map(function (c) {
        return '<button type="button" class="chip" data-cat="' + c + '">' + (CAT_NAMES[c] || c) + '</button>';
      }).join("");
    chips.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      state.cat = b.getAttribute("data-cat");
      chips.querySelectorAll(".chip").forEach(function (x) { x.classList.toggle("is-active", x === b); });
      buildGrupoSelect();
      state.grupo = "";
      $("pedido-grupo").value = "";
      applyFilter();
    });

    var sel = $("pedido-grupo");
    sel.addEventListener("change", function () { state.grupo = sel.value; applyFilter(); });
    buildGrupoSelect();

    var input = $("buscador"), t = null;
    input.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        state.q = input.value;
        applyFilter();
        if (state.q.length >= 3) dl({ event: "search", search_term: state.q });
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
    PRODUCTS.forEach(function (p) {
      if (state.cat && p.cat !== state.cat) return;
      if (grupos.indexOf(p.grupo) === -1) grupos.push(p.grupo);
    });
    sel.innerHTML = '<option value="">Todas las líneas</option>' +
      grupos.map(function (g) { return '<option>' + g + "</option>"; }).join("");
  }

  function initCatalog() {
    fetch("assets/data/productos.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        PRODUCTS = data.items;
        var tot = $("pedido-total-productos");
        if (tot) tot.textContent = String(PRODUCTS.length);
        buildFilters();
        applyFilter();
      })
      .catch(function () {
        listEl.innerHTML = '<div class="prod-vacio"><p><b>No pudimos cargar el catálogo.</b></p>' +
          '<p>Recargá la página o <a href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener">pedinos la lista por WhatsApp</a>.</p></div>';
      });

    // interacción con las cards
    listEl.addEventListener("click", function (e) {
      var card = e.target.closest(".prod");
      if (!card) return;
      var qtyInput = card.querySelector(".qty__num");
      if (e.target.closest("[data-mas]")) qtyInput.value = String((parseInt(qtyInput.value, 10) || 1) + 1);
      else if (e.target.closest("[data-menos]")) qtyInput.value = String(Math.max(1, (parseInt(qtyInput.value, 10) || 1) - 1));
      else if (e.target.closest("[data-agregar]")) {
        var id = card.getAttribute("data-id");
        var prod = null;
        for (var i = 0; i < PRODUCTS.length; i++) if (PRODUCTS[i].id === id) { prod = PRODUCTS[i]; break; }
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

    // barra inferior fija (mobile) con total + abrir carrito
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

  /* ------------------------------------------------------------------ arranque */
  renderCart();
})();
