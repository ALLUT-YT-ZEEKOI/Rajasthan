(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Blog category filters */
  var filters = document.querySelectorAll('.blog-filter');
  var cards = document.querySelectorAll('[data-category]');
  if (filters.length && cards.length) {
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-filter');
        filters.forEach(function (b) { b.classList.toggle('active', b === btn); });
        cards.forEach(function (card) {
          var show = cat === 'all' || card.getAttribute('data-category') === cat;
          card.style.display = show ? '' : 'none';
          if (show) card.classList.add('in');
        });
      });
    });
  }

  /* Contact store selector */
  var stores = document.querySelectorAll('.contact-store');
  var mapFrame = document.getElementById('contactMapFrame');
  if (stores.length && mapFrame) {
    stores.forEach(function (store) {
      store.addEventListener('click', function () {
        stores.forEach(function (s) { s.classList.remove('active'); });
        store.classList.add('active');
        var src = store.getAttribute('data-map');
        if (src) mapFrame.src = src;
      });
    });
  }

  /* Stat counters on about page */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduce) {
    var counted = false;
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting || counted) return;
        counted = true;
        counters.forEach(function (el) {
          var target = parseInt(el.getAttribute('data-count'), 10) || 0;
          var suffix = el.getAttribute('data-suffix') || '';
          var start = 0;
          var dur = 1400;
          var t0 = performance.now();
          function tick(now) {
            var p = Math.min((now - t0) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.floor(start + (target - start) * eased) + suffix;
            if (p < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        });
      });
    }, { threshold: 0.35 });
    var statsBlock = document.querySelector('.page-stats');
    if (statsBlock) co.observe(statsBlock);
  }

  /* Stagger reveal for page cards */
  var staggerItems = document.querySelectorAll('.blog-card, .about-value, .contact-store');
  if (staggerItems.length && 'IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    staggerItems.forEach(function (el, i) {
      el.classList.add('rise');
      el.style.transitionDelay = (i % 6) * 0.08 + 's';
      io.observe(el);
    });
  }
})();
