(function () {
  function scrollThreads() {
    document.querySelectorAll("[data-pcv2-scroll-bottom]").forEach(function (node) {
      node.scrollTop = node.scrollHeight;
    });
  }

  function installFilters() {
    document.querySelectorAll("[data-pcv2-filter]").forEach(function (input) {
      input.addEventListener("input", function () {
        var section = input.closest(".pcv2-section");
        var query = String(input.value || "").trim().toLowerCase();
        if (!section) return;
        section.querySelectorAll(".pcv2-table tbody tr, .pcv2-feed-item, .pcv2-panel, .pcv2-card, .pcv2-media-tile").forEach(function (row) {
          var text = String(row.textContent || "").toLowerCase();
          row.hidden = Boolean(query && text.indexOf(query) === -1);
        });
      });
    });
  }

  function installActionMethods() {
    document.querySelectorAll("a[data-method]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        var method = String(link.getAttribute("data-method") || "").trim().toLowerCase();
        if (!method || method === "get") return;
        event.preventDefault();
        if (link.classList.contains("is-disabled") || link.getAttribute("aria-disabled") === "true") return;
        var href = link.getAttribute("href") || "";
        if (!href || href === "#") return;
        var message = link.getAttribute("data-confirm");
        if (message && !window.confirm(message)) return;
        var form = document.createElement("form");
        form.hidden = true;
        form.method = method === "post" ? "post" : "post";
        form.action = href;
        if (method !== "post") {
          var methodInput = document.createElement("input");
          methodInput.type = "hidden";
          methodInput.name = "_method";
          methodInput.value = method.toUpperCase();
          form.appendChild(methodInput);
        }
        document.body.appendChild(form);
        form.submit();
      });
    });
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function installHoverCards() {
    var sources = Array.prototype.slice.call(document.querySelectorAll("[data-pcv2-hover-source]"));
    if (!sources.length) return;
    var layer = document.createElement("div");
    layer.className = "pcv2-hover-card-layer";
    layer.hidden = true;
    document.body.appendChild(layer);

    function templateFor(source) {
      return source.querySelector("[data-pcv2-hover-template]");
    }

    function positionLayer(event, source) {
      var width = layer.offsetWidth || 340;
      var height = layer.offsetHeight || 220;
      var x = 0;
      var y = 0;
      if (event && typeof event.clientX === "number") {
        x = event.clientX + 16;
        y = event.clientY + 16;
      } else {
        var rect = source.getBoundingClientRect();
        x = rect.left + Math.min(rect.width, 220) + 12;
        y = rect.top + 8;
      }
      layer.style.left = clamp(x, 12, window.innerWidth - width - 12) + "px";
      layer.style.top = clamp(y, 12, window.innerHeight - height - 12) + "px";
    }

    function show(source, event) {
      var template = templateFor(source);
      if (!template) return;
      layer.innerHTML = template.innerHTML;
      layer.hidden = false;
      positionLayer(event, source);
      source.setAttribute("aria-expanded", "true");
    }

    function hide(source) {
      layer.hidden = true;
      layer.innerHTML = "";
      if (source) source.setAttribute("aria-expanded", "false");
    }

    sources.forEach(function (source) {
      source.setAttribute("aria-haspopup", "dialog");
      source.setAttribute("aria-expanded", "false");
      source.addEventListener("mouseenter", function (event) { show(source, event); });
      source.addEventListener("mousemove", function (event) { if (!layer.hidden) positionLayer(event, source); });
      source.addEventListener("mouseleave", function () { hide(source); });
      source.addEventListener("focusin", function () { show(source); });
      source.addEventListener("focusout", function () { hide(source); });
      source.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
          hide(source);
          source.blur();
        }
      });
    });

    window.addEventListener("scroll", function () { hide(); }, true);
    window.addEventListener("resize", function () { hide(); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      scrollThreads();
      installFilters();
      installActionMethods();
      installHoverCards();
    });
  } else {
    scrollThreads();
    installFilters();
    installActionMethods();
    installHoverCards();
  }
})();
