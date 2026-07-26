document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  function updateScrollState() {
    if (window.scrollY >= 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  if (navbar.classList.contains('bg-transparent')) {
    window.addEventListener('scroll', updateScrollState, { passive: true });
    updateScrollState();
  }

  const links = document.querySelectorAll('#navbar .nav-link');
  links.forEach(link => {
    const href = link.getAttribute('href');
    const isMatch = window.AuraSite
      ? window.AuraSite.isHrefActive(href)
      : link.classList.contains('active');

    if (isMatch) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    } else {
      link.classList.remove('active');
      link.removeAttribute('aria-current');
    }
  });

  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  let menuIcon = document.getElementById('menuIcon');
  if (menuToggle && mobileMenu) {
    const setMenuIcon = (name) => {
      if (!menuIcon || !menuIcon.parentNode) return;
      var newIcon = document.createElement('i');
      newIcon.id = 'menuIcon';
      newIcon.setAttribute('data-lucide', name);
      menuIcon.parentNode.replaceChild(newIcon, menuIcon);
      menuIcon = newIcon;
      if (window.AuraIcons) window.AuraIcons.refresh();
    };
    const closeMenu = () => {
      menuToggle.setAttribute('aria-expanded', 'false');
      mobileMenu.classList.remove('flex', 'menu-open');
      mobileMenu.classList.add('hidden');
      setMenuIcon('menu');
    };
    const openMenu = () => {
      menuToggle.setAttribute('aria-expanded', 'true');
      mobileMenu.classList.remove('hidden');
      mobileMenu.classList.add('flex', 'menu-open');
      setMenuIcon('close');
    };
    menuToggle.addEventListener('click', () => {
      const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
      isExpanded ? closeMenu() : openMenu();
    });
    document.addEventListener('click', (e) => {
      if (menuToggle.getAttribute('aria-expanded') === 'true' &&
          !mobileMenu.contains(e.target) &&
          !menuToggle.contains(e.target)) {
        closeMenu();
      }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menuToggle.focus();
      }
    });
  }
});
