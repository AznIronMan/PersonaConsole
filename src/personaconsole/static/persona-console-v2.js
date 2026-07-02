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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      scrollThreads();
      installFilters();
    });
  } else {
    scrollThreads();
    installFilters();
  }
})();
