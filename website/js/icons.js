(function () {
  function refreshIcons() {
    if (typeof lucide === 'undefined') return;
    lucide.createIcons({
      attrs: {
        'stroke-width': 1.5,
      },
    });
  }

  window.AuraIcons = {
    refresh: refreshIcons,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refreshIcons);
  } else {
    refreshIcons();
  }
})();
