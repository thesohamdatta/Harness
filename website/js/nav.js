(function () {
  var nav = document.getElementById("navbar");
  if (!nav) return;

  /* Apple-style nav: text-only, no button pill in the chrome.
   * Primary CTAs live inside the page (hero / closing CTA), never in the nav. */
  var actions = nav.querySelector(".nav-actions");
  if (actions) {
    var cta = actions.querySelector(".nav-cta");
    if (cta) cta.parentNode.removeChild(cta);
  }

  /* Defensive: re-apply aria-current on the active link in case the HTML
   * author forgot. The static nav block already sets .active on each page. */
  var path = (
    window.location.pathname.split("/").pop() || "index.html"
  ).replace(/\.html$/, "");
  var aliases = { "": "index" };
  var activeKey = aliases[path] || path;
  document.querySelectorAll(".nav-link").forEach(function (link) {
    var href = (link.getAttribute("href") || "")
      .replace(/^.*\//, "")
      .replace(/\.html$/, "");
    if (href === activeKey) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });

  // Transparent nav scroll behavior
  if (nav.classList.contains("nav-transparent")) {
    var ticking = false;
    var onScroll = function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          nav.classList.toggle("scrolled", window.scrollY > 60);
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Mobile menu toggle
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var expanded =
        toggle.getAttribute("aria-expanded") === "true" ? false : true;
      toggle.setAttribute("aria-expanded", expanded);
      menu.classList.toggle("open");
      document.body.style.overflow = expanded ? "hidden" : "";
    });

    document.addEventListener("click", function (e) {
      if (
        toggle.getAttribute("aria-expanded") === "true" &&
        !menu.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        toggle.setAttribute("aria-expanded", "false");
        menu.classList.remove("open");
        document.body.style.overflow = "";
      }
    });

    document.addEventListener("keydown", function (e) {
      if (
        e.key === "Escape" &&
        toggle.getAttribute("aria-expanded") === "true"
      ) {
        toggle.setAttribute("aria-expanded", "false");
        menu.classList.remove("open");
        document.body.style.overflow = "";
        toggle.focus();
      }
    });
  }

  // Smooth anchor scroll
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        var navHeight = nav ? nav.offsetHeight : 0;
        var targetPos =
          target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({ top: targetPos, behavior: "smooth" });
      }
    });
  });
})();
