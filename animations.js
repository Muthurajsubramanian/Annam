// ===== Shared site animations =====

// 1) Scroll-reveal: fade/slide up elements and groups as they enter the viewport
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal, .reveal-group').forEach(el => revealObserver.observe(el));

// 2) Count-up animation for stat numbers (About page)
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.dataset.target, 10) || 0;
    const suffix = el.dataset.suffix || '';
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
    countObserver.unobserve(el);
  });
}, { threshold: 0.4 });

document.querySelectorAll('.stat-number[data-target]').forEach(el => countObserver.observe(el));

// 3) Smooth scroll for same-page anchor links (pure hash links only, not cross-page)
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const id = link.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// 4) Page transitions: fade the page out before navigating to another page in the site
document.body.classList.add('page-transition');

document.querySelectorAll('a[href]').forEach(link => {
  const href = link.getAttribute('href');
  if (!href || !href.includes('.html') || href.startsWith('http') || link.target === '_blank') return;

  link.addEventListener('click', (e) => {
    e.preventDefault();
    document.body.classList.remove('page-transition');
    document.body.classList.add('page-fade-out');
    setTimeout(() => { window.location.href = href; }, 320);
  });
});
