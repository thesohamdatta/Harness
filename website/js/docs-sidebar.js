/* eslint-disable */
// @ts-nocheck
/*!
 * docs-sidebar.js — sticky sidebar + scroll-spy for the docs page.
 *
 * - Highlights the sidebar link matching the section currently in view
 * - Toggles the mobile drawer behind a scrim
 * - Closes the drawer on link click
 *
 * Plain ES5 — no build step required.
 */
(function () {
  var sidebar = document.getElementById("docs-sidebar");
  if (!sidebar) return;

  var tocBtn = document.getElementById("toc-mobile-btn");
  var links = Array.prototype.slice.call(
    sidebar.querySelectorAll(".docs-sidebar-link")
  );

  function sectionIdFromHref(href) {
    var idx = href.indexOf("#");
    return idx >= 0 ? href.slice(idx + 1) : null;
  }

  /* Scroll-spy: pick the section closest to the top of the viewport. */
  var sections = links
    .map(function (link) {
      var id = sectionIdFromHref(link.getAttribute("href") || "");
      if (!id) return null;
      var el = document.getElementById(id);
      return el ? { id: id, el: el, link: link } : null;
    })
    .filter(function (x) {
      return !!x;
    });

  function setActive(activeId) {
    for (var i = 0; i < sections.length; i++) {
      var s = sections[i];
      if (s.id === activeId) {
        s.link.classList.add("is-active");
      } else {
        s.link.classList.remove("is-active");
      }
    }
  }

  function onScroll() {
    if (!sections.length) return;
    var offset = 100; /* nav height + breathing room */
    var current = sections[0].id;
    for (var i = 0; i < sections.length; i++) {
      var rect = sections[i].el.getBoundingClientRect();
      if (rect.top - offset <= 0) current = sections[i].id;
    }
    /* If the user is at the very bottom, force the last link active. */
    var scrolledToBottom =
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 8;
    if (scrolledToBottom) current = sections[sections.length - 1].id;
    setActive(current);
  }

  var ticking = false;
  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          onScroll();
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );
  onScroll();

  /* Mobile drawer. */
  if (tocBtn) {
    /* Inject scrim once. */
    var scrim = document.createElement("div");
    scrim.className = "docs-drawer-scrim";
    document.body.appendChild(scrim);

    function openDrawer() {
      sidebar.classList.add("is-drawer", "open");
      scrim.classList.add("open");
      document.body.style.overflow = "hidden";
      tocBtn.setAttribute("aria-expanded", "true");
    }
    function closeDrawer() {
      sidebar.classList.remove("open");
      scrim.classList.remove("open");
      document.body.style.overflow = "";
      tocBtn.setAttribute("aria-expanded", "false");
    }
    function toggleDrawer() {
      if (sidebar.classList.contains("open")) closeDrawer();
      else openDrawer();
    }
    tocBtn.addEventListener("click", toggleDrawer);
    scrim.addEventListener("click", closeDrawer);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && sidebar.classList.contains("open"))
        closeDrawer();
    });
    /* Close after clicking any sidebar link on mobile. */
    for (var j = 0; j < links.length; j++) {
      links[j].addEventListener("click", function () {
        if (window.innerWidth < 834) closeDrawer();
      });
    }
  }
})();
