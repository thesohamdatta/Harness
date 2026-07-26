document.addEventListener('DOMContentLoaded', () => {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const strategies = [
    {
      name: 'about',
      match: (path, ds) => path.includes('about') || ds.page === 'about',
      fallback() {
        document.querySelectorAll('section:not(:first-of-type)').forEach(el => {
          el.classList.remove('opacity-0', 'translate-y-4');
          el.classList.add('opacity-100');
        });
      },
      setup() {
        const els = document.querySelectorAll('section:not(:first-of-type)');
        const obs = new IntersectionObserver(entries => {
          entries.forEach(e => {
            if (e.isIntersecting) {
              e.target.classList.add('opacity-100');
              e.target.classList.remove('opacity-0', 'translate-y-4');
            }
          });
        }, { threshold: 0.1 });
        els.forEach(el => {
          el.classList.add('opacity-0', 'translate-y-4');
          obs.observe(el);
        });
      }
    },
    {
      name: 'ai',
      match: (path, ds) => path.includes('ai') || ds.page === 'ai',
      fallback() {
        document.querySelectorAll('section > div').forEach(el => {
          el.classList.remove('opacity-0', 'translate-y-10');
          el.classList.add('opacity-100');
        });
      },
      setup() {
        const els = document.querySelectorAll('section > div');
        const obs = new IntersectionObserver(entries => {
          entries.forEach(e => {
            if (e.isIntersecting) {
              e.target.classList.add('opacity-100');
              e.target.classList.remove('opacity-0', 'translate-y-10');
            }
          });
        }, { threshold: 0.1 });
        els.forEach(el => {
          el.classList.add('opacity-0', 'translate-y-10');
          obs.observe(el);
        });
      }
    },
    {
      name: 'manifesto',
      match: (path, ds) => path.includes('manifesto') || ds.page === 'manifesto',
      fallback() {
        document.querySelectorAll('article p').forEach(p => {
          p.style.opacity = '1';
          p.style.transform = 'translateY(0)';
        });
      },
      setup() {
        const obs = new IntersectionObserver(entries => {
          entries.forEach(e => {
            if (e.isIntersecting) {
              e.target.style.opacity = '1';
              e.target.style.transform = 'translateY(0)';
            }
          });
        }, { threshold: 0.1 });
        document.querySelectorAll('article p').forEach(p => {
          p.style.opacity = '0';
          p.style.transform = 'translateY(10px)';
          p.style.transition = 'opacity 1s ease-out, transform 1s ease-out';
          obs.observe(p);
        });
      }
    },
    {
      name: 'index',
      match: (path, ds) => {
        const isOther = path.includes('about') || path.includes('ai') || path.includes('manifesto');
        return path.includes('index') || path.endsWith('/') || path === '' || ds.page === 'index' || (!isOther && document.getElementById('app-demo-section'));
      },
      fallback() {},
      setup() {
        const section = document.getElementById('app-demo-section');
        if (!section) return;
        const phoneImg = document.getElementById('demoPhoneImage');
        const captionLabel = document.getElementById('demoCaptionLabel');
        const captionBody = document.getElementById('demoCaptionBody');
        const obs = new IntersectionObserver((entries, inst) => {
          entries.forEach(e => {
            if (e.isIntersecting) {
              if (phoneImg) phoneImg.classList.add('animate-in');
              setTimeout(() => { if (captionLabel) captionLabel.classList.add('animate-in'); }, 300);
              setTimeout(() => { if (captionBody) captionBody.classList.add('animate-in'); }, 500);
              inst.unobserve(e.target);
            }
          });
        }, { threshold: 0.2 });
        obs.observe(section);
      }
    }
  ];

  const path = window.location.pathname.toLowerCase();
  const ds = document.body.dataset;

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    strategies.forEach(s => { if (s.match(path, ds)) s.fallback(); });
    return;
  }

  const matched = strategies.find(s => s.match(path, ds));
  if (matched) matched.setup();
});
