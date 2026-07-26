(function () {
  var pages = [
    { id: 'index', href: 'index.html', label: 'Overview' },
    { id: 'manifesto', href: 'manifesto.html', label: 'Manifesto' },
    { id: 'docs', href: 'docs.html', label: 'Docs' }
  ];

  function copyPage(page) {
    return { id: page.id, href: page.href, label: page.label };
  }

  function findPageById(id) {
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].id === id) return pages[i];
    }
    return null;
  }

  function findPageByHref(href) {
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].href === href) return pages[i];
    }
    return null;
  }

  function filenameFromPath(pathname) {
    var path = (pathname || '').toLowerCase();
    if (path === '' || path === '/' || path.endsWith('/')) return 'index.html';
    return path.split('/').pop() || 'index.html';
  }

  function resolvePageId(pathname, datasetPage) {
    if (datasetPage && findPageById(datasetPage)) return datasetPage;
    var page = findPageByHref(filenameFromPath(pathname));
    return page ? page.id : 'index';
  }

  function getPages() {
    var result = [];
    for (var i = 0; i < pages.length; i++) {
      result.push(copyPage(pages[i]));
    }
    return result;
  }

  function getActivePage(pathname, datasetPage) {
    if (typeof pathname === 'undefined') {
      pathname = window.location.pathname;
    }
    if (typeof datasetPage === 'undefined' && document.body) {
      datasetPage = document.body.dataset.page;
    }
    return resolvePageId(pathname, datasetPage);
  }

  function getPageLabel(id) {
    var page = findPageById(id);
    return page ? page.label : 'Overview';
  }

  function isHrefActive(href, pathname, datasetPage) {
    var activePage = findPageById(getActivePage(pathname, datasetPage));
    return Boolean(activePage && activePage.href === href);
  }

  window.AuraSite = {
    getPages: getPages,
    getActivePage: getActivePage,
    getPageLabel: getPageLabel,
    isHrefActive: isHrefActive
  };
})();
