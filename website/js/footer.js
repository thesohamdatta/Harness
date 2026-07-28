/* eslint-disable */
// @ts-nocheck
/*!
 * footer.js — single source of truth for the site footer.
 *
 * Mounts into <div id="footer-mount"></div> at the end of <body>.
 * Apple HIG: footer is parchment, narrow columns, no decorative chrome.
 * Reads the current page from location.pathname to label the breadcrumb.
 *
 * Note: this file is intended for browser <script> loading only.
 * It is intentionally written as plain ES5 so it runs without a build step.
 */
(function () {
  var mount = document.getElementById("footer-mount");
  if (!mount) return;

  var raw = window.location.pathname.split("/").pop() || "index.html";
  var path = raw.replace(/\.html$/, "");
  var labels = {
    index: "Overview",
    manifesto: "Manifesto",
    docs: "Documentation",
    404: "Not Found",
  };
  var crumb = labels[path] || path;

  var c = function (tag, attrs, children) {
    var open = "<" + tag;
    for (var k in attrs) open += " " + k + '="' + attrs[k] + '"';
    open += ">";
    var close = "<" + "/" + tag + ">";
    return open + (children || "") + close;
  };

  function link(href, label, cls) {
    var extra = cls ? ' class="' + cls + '"' : "";
    if (href === "#") {
      extra = ' class="footer-disabled-link" aria-disabled="true"';
    }
    return '<a href="' + href + '"' + extra + ">" + label + "<" + "/" + "a>";
  }

  function col(title, items) {
    var html = c("div", { class: "footer-col" }, "");
    html += c("span", { class: "footer-col-title" }, title);
    html += "<ul>";
    for (var i = 0; i < items.length; i++) {
      html +=
        "<li>" +
        link(items[i][0], items[i][1], items[i][2]) +
        "<" +
        "/" +
        "li>";
    }
    html += "<" + "/" + "ul>";
    html += "<" + "/" + "div>";
    return html;
  }

  var buildCol = col("Build", [
    ["docs.html#hardware", "Build Yours"],
    ["docs.html#firmware", "Firmware"],
    ["docs.html#backend", "SDK"],
  ]);
  var learnCol = col("Learn", [
    ["docs.html#how-it-works", "How It Works"],
    ["manifesto.html", "Manifesto"],
    ["docs.html", "Docs"],
  ]);
  var communityCol = col("Community", [
    ["https://github.com/thesohamdatta/aura", "GitHub"],
    ["#", "Discord"],
    ["#", "Ethics"],
  ]);
  var projectCol = col("Project", [
    ["index.html", "Overview"],
    ["manifesto.html", "Manifesto"],
    ["docs.html", "Docs"],
  ]);

  var html = "";
  html += '<footer class="site-footer">';
  html += '<div class="footer-inner">';

  html += '<nav class="footer-breadcrumb" aria-label="Breadcrumb">';
  html += link("index.html", "Aura", "footer-breadcrumb-link");
  html += '<span class="footer-breadcrumb-sep" aria-hidden="true">›</span>';
  html += "<span>" + crumb + "</span>";
  html += "<" + "/" + "nav>";

  html += '<div class="footer-grid">';
  html +=
    '<div class="footer-brand"><div class="footer-wordmark">Aura</div><' +
    "/" +
    "div>";
  html += buildCol;
  html += learnCol;
  html += communityCol;
  html += projectCol;
  html += "<" + "/" + "div>";

  html += '<div class="footer-secondary">';
  html += "More ways to build: ";
  html += link(
    "https://github.com/thesohamdatta/aura",
    "Fork the GitHub repo",
    "footer-inline-link"
  );
  html += " or ";
  html += link("docs.html", "read our assembly guides", "footer-inline-link");
  html += ". Need help? Contact ";
  html += link(
    "mailto:thesohamdatta@gmail.com",
    "thesohamdatta@gmail.com",
    "footer-inline-link"
  );
  html += ".";
  html += "<" + "/" + "div>";

  html += '<div class="footer-meta">';
  html += '<p class="footer-copy">© 2026 Aura Project. MIT Licensed.</p>';
  html += '<div class="footer-meta-links">';
  html += link("#", "MIT License");
  html += link("#", "Privacy");
  html += link(
    "https://github.com/thesohamdatta/aura",
    "GitHub",
    "footer-legal-link"
  );
  html += "<" + "/" + "div>";
  html += '<span class="footer-locale">Pune, India</span>';
  html += "<" + "/" + "div>";

  html += "<" + "/" + "div>";
  html += "<" + "/" + "footer>";

  mount.innerHTML = html;
})();
