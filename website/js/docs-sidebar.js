/* eslint-disable */
// @ts-nocheck
/*!
 * docs-sidebar.js — docs page behaviors: sticky sidebar + scroll-spy,
 * section filter, mobile drawer as a proper dialog, and code-block copy.
 *
 * - Highlights the sidebar link matching the section currently in view
 * - Filters sidebar links as the visitor types in the search input
 * - Opens the mobile drawer as a dialog: focus trapped while open,
 *   focus returned to the toggle on close, scrim click closes
 * - Copies code-block text with visible success feedback
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

  /* Immediate active state on click — before smooth scroll completes. */
  for (var k = 0; k < links.length; k++) {
    links[k].addEventListener("click", function (e) {
      var id = sectionIdFromHref(this.getAttribute("href") || "");
      if (id) setActive(id);
    });
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

    /* Focusables inside the drawer, for the focus trap. */
    var FOCUSABLE_SELECTOR =
      'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])';

    function drawerFocusables() {
      return Array.prototype.slice.call(
        sidebar.querySelectorAll(FOCUSABLE_SELECTOR)
      );
    }

    function openDrawer() {
      sidebar.classList.add("is-drawer", "open");
      sidebar.setAttribute("role", "dialog");
      sidebar.setAttribute("aria-modal", "true");
      scrim.classList.add("open");
      document.body.style.overflow = "hidden";
      tocBtn.setAttribute("aria-expanded", "true");
      /* Move focus into the dialog. */
      var focusable = drawerFocusables();
      if (focusable.length) focusable[0].focus();
    }
    function closeDrawer() {
      sidebar.classList.remove("open");
      sidebar.removeAttribute("role");
      sidebar.removeAttribute("aria-modal");
      scrim.classList.remove("open");
      document.body.style.overflow = "";
      tocBtn.setAttribute("aria-expanded", "false");
      tocBtn.focus(); /* restore focus to the toggle */
    }
    function toggleDrawer() {
      if (sidebar.classList.contains("open")) closeDrawer();
      else openDrawer();
    }
    tocBtn.addEventListener("click", toggleDrawer);
    scrim.addEventListener("click", closeDrawer);
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" || !sidebar.classList.contains("open")) return;
      closeDrawer();
      e.preventDefault();
    });
    /* Focus trap while the drawer is open. */
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || !sidebar.classList.contains("open")) return;
      var focusable = drawerFocusables();
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        last.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    });
    /* Close after clicking any sidebar link on mobile. */
    for (var j = 0; j < links.length; j++) {
      links[j].addEventListener("click", function () {
        if (window.innerWidth < 834) closeDrawer();
      });
    }
  }

  /* Section filter: hide links that do not match the query. */
  var search = document.getElementById("docs-search");
  if (search) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var sections = Array.prototype.slice.call(
        sidebar.querySelectorAll(".docs-sidebar-section")
      );
      for (var i = 0; i < sections.length; i++) {
        var visible = false;
        var sectionLinks = Array.prototype.slice.call(
          sections[i].querySelectorAll(".docs-sidebar-link")
        );
        for (var m = 0; m < sectionLinks.length; m++) {
          var matches =
            !q || sectionLinks[m].textContent.toLowerCase().indexOf(q) >= 0;
          sectionLinks[m].style.display = matches ? "" : "none";
          if (matches) visible = true;
        }
        sections[i].style.display = visible ? "" : "none";
      }
    });
  }

  /* Code-block copy buttons with success feedback. */
  var copyButtons = Array.prototype.slice.call(
    document.querySelectorAll(".docs-copy-btn")
  );
  for (var c = 0; c < copyButtons.length; c++) {
    var btn = copyButtons[c];
    btn.setAttribute("aria-label", "Copy code to clipboard");
    btn.addEventListener("click", function () {
      var block = this.closest(".docs-code-block");
      if (!block) return;
      var text = block.querySelector("pre").textContent;
      var self = this;
      var original = self.textContent;
      var showResult = function (success) {
        self.textContent = success ? "Copied" : "Failed";
        self.classList.add(success ? "is-copied" : "is-failed");
        setTimeout(
          function () {
            self.textContent = original;
            self.classList.remove("is-copied", "is-failed");
          }.bind(self),
          1600
        );
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(text)
          .then(function () {
            showResult(true);
          })
          .catch(function () {
            fallbackCopy(text, self, showResult);
          });
      } else {
        fallbackCopy(text, self, showResult);
      }
    });
  }

  function fallbackCopy(text, btn, showResult) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    var success = false;
    try {
      success = document.execCommand("copy");
    } catch (err) {
      success = false;
    }
    document.body.removeChild(ta);
    showResult(success);
  }
})();
