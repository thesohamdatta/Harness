/* eslint-disable */
// @ts-nocheck
/*!
 * footer.js — single source of truth for the site footer.
 *
 * Mounts into <div id="footer-mount"></div> at the end of <body>.
 * Apple HIG: footer is parchment, narrow columns, no decorative chrome.
 *
 * Note: this file is intended for browser <script> loading only.
 * It is intentionally written as plain ES5 so it runs without a build step.
 */
(function () {
  var mount = document.getElementById("footer-mount");
  if (!mount) return;

  function link(href, label) {
    if (href === "#") {
      return (
        '<span class="footer-disabled-link" aria-disabled="true">' +
        label +
        "</span>"
      );
    }
    return '<a href="' + href + '">' + label + "</a>";
  }

  function col(title, items) {
    var html = '<div class="footer-col">';
    html += '<h3 class="footer-col-title">' + title + "</h3>";
    html += "<ul>";
    for (var i = 0; i < items.length; i++) {
      html += "<li>" + link(items[i][0], items[i][1]) + "</li>";
    }
    html += "</ul></div>";
    return html;
  }

  var buildCol = col("Build", [
    ["docs.html#hardware", "Build yours"],
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

  html += '<nav class="footer-nav" aria-label="Site">';
  html += '<div class="footer-col footer-col-brand">';
  html += '<div class="footer-wordmark">Aura</div>';
  html += '<p class="footer-tagline">Open-source, screenless, voice-first.</p>';
  html += "</div>";
  html += buildCol;
  html += learnCol;
  html += communityCol;
  html += projectCol;
  html += "</nav>";

  html += '<div class="footer-secondary">';
  html += "More ways to build: ";
  html += link("https://github.com/thesohamdatta/aura", "Fork the GitHub repo");
  html += " or ";
  html += link("docs.html", "read our assembly guides");
  html += ". Need help? Contact ";
  html += link("mailto:thesohamdatta@gmail.com", "thesohamdatta@gmail.com");
  html += ".";
  html += "</div>";

  html += '<div class="footer-meta">';
  html +=
    '<p class="footer-copy">\u00A9 2026 Aura. Open source under MIT License.</p>';
  html += '<div class="footer-meta-links">';
  html += link("#", "MIT License");
  html += link("#", "Privacy");
  html += link("https://github.com/thesohamdatta/aura", "GitHub");
  html += "</div>";
  html += '<span class="footer-locale">Pune, India</span>';
  html += "</div>";

  html += "</div>";
  html += "</footer>";

  mount.innerHTML = html;
})();
