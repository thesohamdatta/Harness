/* scroll-orchestrator.js — declarative scroll enhancement, no dependencies.
 * Parses Apple-style keyframe DSL: "top 85%", "bottom 15%", "a0t - 100vh", "a0b"
 * Sets --scroll-progress (global), --section-progress (per-element), --stagger-index
 * Respects prefers-reduced-motion. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = [];
  var ticking = false;

  /* Parse Apple-style keyframe expressions into document scroll offsets.
   *
   * Expressions reference the ANCHOR element (data-anim-anchor):
   * - "top 85%": trigger when anchor.top reaches 85% down from viewport top
   * - "bottom 15%": trigger when anchor.bottom reaches 15% up from viewport bottom
   * - "a0t": anchor top edge
   * - "a0b": anchor bottom edge
   * - "a0t - 100vh": 100vh above anchor top
   * - "a0b + 50px": 50px below anchor bottom
   *
   * Formula: "top X%" → scroll = anchor.documentTop - X% * viewport
   *          "bottom X%" → scroll = anchor.documentBottom - (100-X)% * viewport */
  function point(expression, anchorRect, scroll, viewport) {
    var value = (expression || "a0t").toLowerCase().replace(/\s+/g, " ").trim();
    var match;

    /* "top 85%" or "bottom 15%" - viewport-relative anchor position triggers */
    match = /^(top|bottom)\s+([\d.]+)(%|vh|px)$/.exec(value);
    if (match) {
      var amount = parseFloat(match[2]);
      var unit = match[3];
      var offset = unit === "px" ? amount : (amount / 100) * viewport;
      if (match[1] === "top") {
        /* anchor.top - scroll = offset → scroll = anchor.top - offset */
        return anchorRect.top + scroll - offset;
      } else {
        /* anchor.bottom - scroll = viewport - offset → scroll = anchor.bottom - viewport + offset */
        return anchorRect.bottom + scroll - viewport + offset;
      }
    }

    /* "a0t - 100vh" or "a0b + 50px" - anchor-relative with offset */
    match = /^(a0t|a0b)\s*([+-])\s*([\d.]+)(%|vh|px)$/.exec(value);
    if (match) {
      var anchorBase = match[1] === "a0t" ? anchorRect.top : anchorRect.bottom;
      var amount = parseFloat(match[3]);
      var unit = match[4];
      if (unit === "px") amount = amount;
      else amount = (amount / 100) * viewport;
      return scroll + anchorBase + (match[2] === "+" ? amount : -amount);
    }

    /* Simple anchor references */
    if (value === "a0t") return scroll + anchorRect.top;
    if (value === "a0b") return scroll + anchorRect.bottom;

    /* Viewport references (no anchor) */
    if (value === "top") return scroll;
    if (value === "bottom") return scroll + viewport;

    return scroll + anchorRect.top;
  }

  function refresh() {
    var scroll = window.pageYOffset || root.scrollTop || 0;
    var height = Math.max(1, root.scrollHeight - window.innerHeight);
    root.style.setProperty(
      "--scroll-progress",
      Math.max(0, Math.min(1, scroll / height)).toFixed(4)
    );

    items.forEach(function (item) {
      var rect = item.anchor.getBoundingClientRect();
      var start = point(item.startExpr, rect, scroll, window.innerHeight);
      var end = point(item.endExpr, rect, scroll, window.innerHeight);
      var progress =
        end === start
          ? scroll >= end
            ? 1
            : 0
          : (scroll - start) / (end - start);
      progress = Math.max(0, Math.min(1, progress));
      item.el.style.setProperty("--section-progress", progress.toFixed(4));
      if (item.visible && (reduced || progress > 0)) reveal(item);
    });
    ticking = false;
  }

  function requestRefresh() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(refresh);
    }
  }

  function reveal(item) {
    if (item.waiting) return;
    item.el.classList.add("is-revealed");
    if (item.stagger) {
      Array.prototype.forEach.call(item.el.children, function (child, index) {
        child.style.setProperty("--stagger-index", index);
        child.classList.add("is-revealed");
      });
    }
  }

  function waitForImages(item) {
    var images =
      item.el.tagName === "IMG" ? [item.el] : item.el.querySelectorAll("img");
    var pending = images.length;
    if (!pending) return;
    item.waiting = true;
    Array.prototype.forEach.call(images, function (image) {
      function done() {
        image.removeEventListener("load", done);
        image.removeEventListener("error", done);
        if (!--pending) {
          item.waiting = false;
          requestRefresh();
        }
      }
      if (image.complete) done();
      else {
        image.addEventListener("load", done);
        image.addEventListener("error", done);
      }
    });
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-anim-trigger]"),
    function (el) {
      var anchorSelector = el.getAttribute("data-anim-anchor");
      var anchor = anchorSelector && document.querySelector(anchorSelector);
      var trigger = el.getAttribute("data-anim-trigger") || "";
      var startExpr = el.getAttribute("data-anim-start") || "a0t - 100vh";
      var endExpr = el.getAttribute("data-anim-end") || "a0b";
      var item = {
        el: el,
        anchor: anchor || el.closest("section") || el,
        startExpr: startExpr,
        endExpr: endExpr,
        stagger: trigger === "stagger",
        visible: reduced,
      };
      if (trigger === "image" || trigger === "load") waitForImages(item);
      items.push(item);
    }
  );

  var observer =
    window.IntersectionObserver &&
    new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          entry.target.__auraAnimation.visible = entry.isIntersecting;
        });
        requestRefresh();
      },
      { rootMargin: "0px 0px -10%", threshold: 0 }
    );

  items.forEach(function (item) {
    item.el.__auraAnimation = item;
    if (observer) observer.observe(item.el);
    else item.visible = true;
  });

  window.addEventListener("scroll", requestRefresh, { passive: true });
  window.addEventListener("resize", requestRefresh, { passive: true });
  requestRefresh();

  /* FAQ Accordion — one open at a time */
  document.addEventListener("DOMContentLoaded", function () {
    var faqQuestions = document.querySelectorAll(".faq-question");
    Array.prototype.forEach.call(faqQuestions, function (btn) {
      btn.addEventListener("click", function () {
        var item = btn.closest(".faq-item");
        var isOpen = item.hasAttribute("open");
        document
          .querySelectorAll(".faq-item[open]")
          .forEach(function (openItem) {
            if (openItem !== item) openItem.removeAttribute("open");
          });
        if (!isOpen) item.setAttribute("open", "");
        else item.removeAttribute("open");
      });
    });
  });
})();
