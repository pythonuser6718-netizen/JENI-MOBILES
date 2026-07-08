(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Page loader ---------- */
  window.addEventListener('load', function () {
    var loader = document.getElementById('pageLoader');
    if (loader) {
      setTimeout(function () { loader.classList.add('is-hidden'); }, 250);
    }
  });

  /* ---------- Sticky header shrink ---------- */
  var header = document.getElementById('siteHeader');
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 24) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  }
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav toggle ---------- */
  var navToggle = document.getElementById('navToggle');
  var mainNav = document.getElementById('mainNav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      var open = mainNav.classList.toggle('is-open');
      mainNav.style.display = open ? 'flex' : '';
      if (open) {
        mainNav.style.position = 'absolute';
        mainNav.style.top = '76px';
        mainNav.style.left = '0';
        mainNav.style.right = '0';
        mainNav.style.flexDirection = 'column';
        mainNav.style.background = 'rgba(11,13,18,0.98)';
        mainNav.style.padding = '20px 32px';
        mainNav.style.borderBottom = '1px solid #262B37';
      }
    });
  }

  /* ---------- Scroll reveal via IntersectionObserver ---------- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && revealEls.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var delay = parseInt(el.dataset.revealDelay || '0', 10);
          delay = Math.min(delay, 6);
          el.style.transitionDelay = (delay * 70) + 'ms';
          el.classList.add('in-view');
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in-view'); });
  }

  /* ---------- Animated stat counters ---------- */
  var statEls = document.querySelectorAll('.stat__num[data-count]');
  if (statEls.length) {
    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseInt(el.dataset.count, 10);
        var start = null;
        var duration = 1200;
        function step(ts) {
          if (!start) start = ts;
          var progress = Math.min((ts - start) / duration, 1);
          var eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.round(eased * target);
          if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        countObserver.unobserve(el);
      });
    }, { threshold: 0.5 });
    statEls.forEach(function (el) { countObserver.observe(el); });
  }

  /* ---------- 3D tilt: hero phone follows cursor within stage ---------- */
  function attachTilt(stageEl, targetEl, intensity) {
    if (!stageEl || !targetEl || reduceMotion) return;
    stageEl.addEventListener('mousemove', function (e) {
      var rect = stageEl.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5;
      var y = (e.clientY - rect.top) / rect.height - 0.5;
      targetEl.style.transform =
        'rotateY(' + (x * intensity) + 'deg) rotateX(' + (-y * intensity) + 'deg)';
    });
    stageEl.addEventListener('mouseleave', function () {
      targetEl.style.transform = 'rotateY(0deg) rotateX(0deg)';
    });
  }
  attachTilt(document.getElementById('heroStage'), document.getElementById('tiltPhone'), 16);
  attachTilt(document.getElementById('detailStage'), document.getElementById('tiltPhoneDetail'), 14);

  /* ---------- Magnetic tilt for product cards ---------- */
  if (!reduceMotion) {
    document.querySelectorAll('.tilt-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform =
          'perspective(700px) rotateY(' + (x * 8) + 'deg) rotateX(' + (-y * 8) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = 'perspective(700px) rotateY(0deg) rotateX(0deg) translateY(0)';
      });
    });
  }

  /* ---------- Cart badge bump when count changes ---------- */
  var cartBadge = document.getElementById('cartBadge');
  if (cartBadge) {
    var lastCount = sessionStorage.getItem('orbitCartCount');
    var currentCount = cartBadge.textContent.trim();
    if (lastCount !== null && lastCount !== currentCount) {
      cartBadge.classList.add('is-bumped');
      setTimeout(function () { cartBadge.classList.remove('is-bumped'); }, 500);
    }
    sessionStorage.setItem('orbitCartCount', currentCount);
  }

  /* ---------- Auto-dismiss toasts ---------- */
  var toastStack = document.getElementById('toastStack');
  if (toastStack) {
    setTimeout(function () { toastStack.style.display = 'none'; }, 3800);
  }
})();
