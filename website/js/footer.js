(function () {
  function renderFooter() {
    var mount = document.getElementById('footer-mount');
    if (!mount || !window.AuraSite) return;

    var activePage = window.AuraSite.getActivePage();
    var breadcrumb = window.AuraSite.getPageLabel(activePage);

    var html = ''
      + '<footer class="site-footer border-t border-[#d2d2d7]/50" style="padding: 64px 0 0 0;">\n'
      + '  <div class="max-w-[var(--content-max)] mx-auto px-6">\n'
      + '\n'
      + '    <!-- Breadcrumb row -->\n'
      + '    <div class="flex items-center text-[12px] text-[#86868b] pb-4 mb-6 border-b border-[#d2d2d7]/35 flex-wrap gap-y-2">\n'
      + '      <a href="index.html" class="hover:text-[#1d1d1f] transition-colors">Aura</a>\n'
      + '      <span class="mx-2 text-[10px] text-[#86868b]">&rsaquo;</span>\n'
      + '      <span class="text-[#1d1d1f]">' + breadcrumb + '</span>\n'
      + '    </div>\n'
      + '\n'
      + '    <!-- Main grid -->\n'
      + '    <div class="grid grid-cols-2 md:grid-cols-[1.5fr_1fr_1fr_1fr_1fr] gap-8 md:gap-6">\n'
      + '      \n'
      + '      <!-- Brand column -->\n'
      + '      <div class="col-span-2 md:col-span-1 mb-10 md:mb-0">\n'
      + '        <div class="font-display text-[21px] font-semibold text-[#1d1d1f] mb-2">Aura</div>\n'
      + '      </div>\n'
      + '\n'
      + '      <!-- Build column -->\n'
      + '      <div class="col-span-1">\n'
      + '        <span class="font-body text-[11px] font-medium text-[#1d1d1f]/60 mb-4 block">Build</span>\n'
      + '        <ul class="space-y-0 flex flex-col">\n'
      + '          <li><a href="docs.html#hardware" class="footer-link-item">Build Yours</a></li>\n'
      + '          <li><a href="docs.html#firmware" class="footer-link-item">Firmware</a></li>\n'
      + '          <li><a href="docs.html#backend" class="footer-link-item">SDK</a></li>\n'
      + '        </ul>\n'
      + '      </div>\n'
      + '\n'
      + '      <!-- Learn column -->\n'
      + '      <div class="col-span-1">\n'
      + '        <span class="font-body text-[11px] font-medium text-[#1d1d1f]/60 mb-4 block">Learn</span>\n'
      + '        <ul class="space-y-0 flex flex-col">\n'
      + '          <li><a href="docs.html#how-it-works" class="footer-link-item">How It Works</a></li>\n'
      + '          <li><a href="manifesto.html" class="footer-link-item">Manifesto</a></li>\n'
      + '          <li><a href="docs.html" class="footer-link-item">Docs</a></li>\n'
      + '        </ul>\n'
      + '      </div>\n'
      + '\n'
      + '      <!-- Community column -->\n'
      + '      <div class="col-span-1">\n'
      + '        <span class="font-body text-[11px] font-medium text-[#1d1d1f]/60 mb-4 block">Community</span>\n'
      + '        <ul class="space-y-0 flex flex-col">\n'
      + '          <li><a href="https://github.com/thesohamdatta/aura" target="_blank" class="footer-link-item">GitHub</a></li>\n'
      + '          <li><a href="#" aria-disabled="true" class="footer-disabled-link">Discord</a></li>\n'
      + '          <li><a href="#" aria-disabled="true" class="footer-disabled-link">Ethics</a></li>\n'
      + '        </ul>\n'
      + '      </div>\n'
      + '\n'
      + '      <!-- Project column -->\n'
      + '      <div class="col-span-1">\n'
      + '        <span class="font-body text-[11px] font-medium text-[#1d1d1f]/60 mb-4 block">Project</span>\n'
      + '        <ul class="space-y-0 flex flex-col">\n'
      + '          <li><a href="index.html" class="footer-link-item">Overview</a></li>\n'
      + '          <li><a href="manifesto.html" class="footer-link-item">Manifesto</a></li>\n'
      + '          <li><a href="docs.html" class="footer-link-item">Docs</a></li>\n'
      + '        </ul>\n'
      + '      </div>\n'
      + '\n'
      + '    </div>\n'
      + '\n'
      + '    <!-- Retailer/Footnote row -->\n'
      + '    <div class="pt-6 pb-4 border-t border-[#d2d2d7]/35 mt-8 text-[12px] text-[#86868b] leading-relaxed">\n'
      + '      More ways to build: <a href="https://github.com/thesohamdatta/aura" target="_blank" class="text-[#0066cc] hover:underline">Fork the GitHub repo</a> or <a href="docs.html" class="text-[#0066cc] hover:underline">read our assembly guides</a>. Need help? Contact <a href="mailto:thesohamdatta@gmail.com" class="text-[#0066cc] hover:underline">thesohamdatta@gmail.com</a>.\n'
      + '    </div>\n'
      + '\n'
      + '    <!-- Bottom bar -->\n'
      + '    <div class="border-t border-[#d2d2d7]/35 py-5 flex flex-col md:flex-row justify-between items-center gap-4 text-center md:text-left">\n'
      + '      <p class="font-body text-[12px] text-[#86868b]">&copy; 2026 Aura Project. MIT Licensed.</p>\n'
      + '      <div class="flex gap-6 flex-row">\n'
      + '        <a href="#" aria-disabled="true" class="footer-legal-disabled">MIT License</a>\n'
      + '        <a href="#" aria-disabled="true" class="footer-legal-disabled">Privacy</a>\n'
      + '        <a href="https://github.com/thesohamdatta/aura" target="_blank" class="footer-legal-link">GitHub</a>\n'
      + '      </div>\n'
      + '      <span class="font-body text-[12px] text-[#86868b]">Pune, India</span>\n'
      + '    </div>\n'
      + '\n'
      + '  </div>\n'
      + '</footer>\n';

    mount.insertAdjacentHTML('beforebegin', html);
    mount.remove();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderFooter);
  } else {
    renderFooter();
  }
})();
