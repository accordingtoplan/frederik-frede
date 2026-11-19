(function() {
  /* ─── NAV INJECTION ──────────────────────────────────── */
  /* Synchronous — runs immediately when script parses at bottom of body.
     nav-mount div already exists in DOM at that point. */
  const NAV_HTML = `<a class="skip-link" href="#main">Skip to content</a>
<nav class="nav" aria-label="Main">
  <div class="nav-left">
    <a class="nav-logo" href="/">Frederik</a>
    <a class="nav-studio" href="/">&nbsp;Frede</a>
  </div>
  <div class="nav-center">
    <div class="swatches" role="group" aria-label="Colour theme">
      <button type="button" class="swatch" style="background:#fff" aria-label="White theme" onclick="setTheme('white',this)"></button>
      <button type="button" class="swatch" style="background:#111" aria-label="Black theme" onclick="setTheme('black',this)"></button>
      <button type="button" class="swatch" style="background:#e63222" aria-label="Red theme" onclick="setTheme('signal',this)"></button>
    </div>
  </div>
  <div class="nav-right" id="navLinks">
    <button type="button" class="nav-close" aria-label="Close menu">×</button>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/work.html">Work</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/about.html#contact">Contact</a></li>
    </ul>
  </div>
  <button type="button" class="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><span></span><span></span></button>
</nav>`;
  const navMount = document.getElementById('nav-mount');
  if (navMount) {
    navMount.innerHTML = NAV_HTML;
    const navLinks = navMount.querySelector('#navLinks');
    const burger = navMount.querySelector('.hamburger');
    const setMenu = function(open) {
      navLinks.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    burger.addEventListener('click', function() { setMenu(!navLinks.classList.contains('open')); });
    navMount.querySelector('.nav-close').addEventListener('click', function() { setMenu(false); });
    navLinks.querySelectorAll('a').forEach(function(a) { a.addEventListener('click', function() { setMenu(false); }); });
    const path = window.location.pathname;
    navMount.querySelectorAll('#navLinks a').forEach(function(a) {
      const href = a.getAttribute('href');
      if (href === '/' && (path === '/' || path === '/index.html' || path.endsWith('/index.html'))) {
        a.classList.add('active');
      } else if (href === '/work.html' && path.indexOf('/work') !== -1) {
        a.classList.add('active');
      } else if (href === '/about.html' && path.indexOf('/about') !== -1) {
        a.classList.add('active');
      }
    });
  }


  /* ─── THEME ───────────────────────────────────────────
     Pages may define their own setTheme(); this is the shared fallback.
     The choice is stored and re-applied on every page. The matching CSS
     variables live in style.css under html[data-theme], and a one-line
     script in each page head sets data-theme before first paint. */
  const THEMES = {
    white:  { bg:'#fff',    card:'#f5f3f1', fg:'#4a4540', mid:'#706b66',                light:'#7a7470',                border:'#c8c3be' },
    black:  { bg:'#111',    card:'#1a1a1a', fg:'#fff',    mid:'rgba(255,255,255,0.62)', light:'rgba(255,255,255,0.52)', border:'rgba(255,255,255,0.12)' },
    signal: { bg:'#e63222', card:'#cc2b1d', fg:'#000',    mid:'rgba(0,0,0,0.55)',       light:'rgba(0,0,0,0.48)',       border:'transparent' }
  };
  const swatchFor = function(name) { return document.querySelector('.swatch[onclick*="\'' + name + '\'"]'); };
  function applyTheme(name, el) {
    const t = THEMES[name]; if (!t) return;
    const r = document.documentElement.style;
    r.setProperty('--bg', t.bg);          r.setProperty('--bg-card', t.card);
    r.setProperty('--fg', t.fg);          r.setProperty('--fg-mid', t.mid);
    r.setProperty('--fg-light', t.light); r.setProperty('--border', t.border);
    r.setProperty('--grey-dark', t.fg);   r.setProperty('--grey-mid', t.mid);
    r.setProperty('--grey-light', t.light);
    document.documentElement.setAttribute('data-theme', name);
    document.querySelectorAll('.swatch').forEach(function(s) { s.classList.remove('active'); });
    if (el) el.classList.add('active');
  }
  if (typeof window.setTheme !== 'function') window.setTheme = applyTheme;
  document.addEventListener('DOMContentLoaded', function() {
    const base = window.setTheme;
    window.setTheme = function(name, el) {
      base(name, el || swatchFor(name));
      try { localStorage.setItem('ff-theme', name); } catch (e) {}
    };
    let saved = null;
    try { saved = localStorage.getItem('ff-theme'); } catch (e) {}
    const current = document.documentElement.getAttribute('data-theme') || 'white';
    const name = THEMES[saved] ? saved : current;
    base(name, swatchFor(name));
  });

  /* ─── NAV SCROLL BEHAVIOUR ────────────────────────────
     Hide nav on scroll-down, reveal on scroll-up or stop */
  (function() {
    var nav = document.querySelector('.nav');
    if (!nav) return;
    var lastY = window.scrollY;
    var ticking = false;
    var hideTimer;
    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          var y = window.scrollY;
          // Always show nav within 60px of top
          if (y < 60) {
            nav.classList.remove('nav--hidden');
          } else if (y > lastY + 8) {
            // Scrolling down — hide
            nav.classList.add('nav--hidden');
          } else if (y < lastY - 4) {
            // Scrolling up — show
            nav.classList.remove('nav--hidden');
          }
          lastY = y;
          ticking = false;
          // Also show after scroll stops (300ms)
          clearTimeout(hideTimer);
          hideTimer = setTimeout(function() {
            nav.classList.remove('nav--hidden');
          }, 300);
        });
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  })();

  const FOOTER_HTML = `<div class="footer-bar">
      <div class="footer-top-row">
        <div class="footer-logo-row">
          <img src="/frede-logo.webp" width="52" height="80" alt="FREDE" class="footer-logo">
          <svg class="footer-marker" viewBox="0 0 210 65" xmlns="http://www.w3.org/2000/svg" aria-label="vibecoded. with a lot of prompts.">
            <defs>
              <filter id="ink-footer">
                <feTurbulence type="fractalNoise" baseFrequency="0.055" numOctaves="3" result="n"/>
                <feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/>
              </filter>
            </defs>
            <g filter="url(#ink-footer)" transform="rotate(-3.5, 0, 0)">
              <text font-family="'Permanent Marker', cursive" font-size="18" fill="#c01719" letter-spacing="0.2">
                <tspan x="0" y="22">vibecoded.</tspan>
                <tspan x="0" dy="24">with a lot of prompts.</tspan>
              </text>
            </g>
          </svg>
        </div>
      </div>
      <div class="footer-bottom-row">
        <span class="footer-copy">© 2026 <span class="footer-frak">Frede</span> · <a href="/imprint.html" class="footer-copy-link">Imprint</a> · <button class="footer-copy-link footer-cookie-btn" onclick="resetConsent()">Cookie settings</button></span>
        <div class="footer-links">
          <a href="https://instagram.com/frederikfrede" target="_blank" rel="noopener">Instagram</a>
          <a href="https://linkedin.com/in/frede" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://substack.com/@frederikfrede" target="_blank" rel="noopener">Substack</a>
        </div>
        <form class="footer-subscribe" action="https://substack.com/api/v1/free" method="get" target="_blank">
          <input type="email" name="email" placeholder="your@email.com" class="subscribe-input" required>
          <button type="submit" class="subscribe-btn">Subscribe</button>
        </form>
      </div>
    </div>
    <div class="cookie-consent" id="cookieConsent">
      <span class="cookie-text">Uses analytics.</span>
      <div class="cookie-actions">
        <button id="cookieDecline">Decline</button>
        <button id="cookieAccept">Accept</button>
      </div>
    </div>`;

  const mount = document.getElementById('footer-mount');
  if (mount) mount.innerHTML = FOOTER_HTML;

  /* ─── SCROLL REVEAL ───────────────────────────────────── */
  function initReveal() {
    const targets = document.querySelectorAll('.case, .cs-media-full, .cs-grid > *, .cs-grid-3 > *');
    if (!targets.length) return;
    const isMobile = window.innerWidth <= 640;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          entry.target.style.transitionDelay = (i % 2) * 90 + 'ms';
          entry.target.classList.add('in-view');
          // Autoplay alone can leave a video paused on its first frame (looks
          // like a stuck poster). Explicitly play any video as it reveals —
          // covers plain-src videos that aren't wired to the lazy-loader.
          entry.target.querySelectorAll('video').forEach(v => {
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: isMobile ? 0.05 : 0.15, rootMargin: isMobile ? '0px 0px -10% 0px' : '0px 0px -40px 0px' });
    targets.forEach(el => observer.observe(el));
    // Safety net: if anything ALREADY IN/near the viewport is still hidden a
    // moment after load (observer raced, errored, or never fired), reveal +
    // play it. Scoped to the visible region so below-fold content keeps its
    // staggered scroll-reveal instead of all popping in at once.
    setTimeout(() => {
      targets.forEach(el => {
        if (el.classList.contains('in-view')) return;
        const r = el.getBoundingClientRect();
        const near = r.top < window.innerHeight + 200 && r.bottom > -200;
        if (near) {
          el.classList.add('in-view');
          el.querySelectorAll('video').forEach(v => {
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
          });
        }
      });
    }, 2500);
  }
  window.addEventListener('load', () => setTimeout(initReveal, 50));

  /* ─── VIDEO LAZY-LOAD ─────────────────────────────────── */
  /* Loads <video data-lazy> sources only when near the viewport.
     Source URLs live in data-src; swapped to src on intersection.
     Videos using a plain src= keep working untouched. */
  function initVideoLazy() {
    const vids = document.querySelectorAll('video[data-lazy]');
    if (!vids.length) return;
    const load = (video) => {
      if (video.dataset.loaded) return;
      video.dataset.loaded = '1';
      video.querySelectorAll('source[data-src]').forEach(s => {
        s.src = s.dataset.src;
      });
      // iOS Safari only autoplays when muted is set as a property, not just the attribute
      if (video.hasAttribute('muted')) { video.muted = true; video.defaultMuted = true; }
      video.playsInline = true;
      video.load();
      // autoplay videos resume once buffered; ignore promise rejection
      const p = video.play();
      if (p && p.catch) p.catch(() => {});
    };
    if (!('IntersectionObserver' in window)) { vids.forEach(load); return; }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          load(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '600px 0px' });
    vids.forEach(v => observer.observe(v));
  }
  window.addEventListener('load', () => setTimeout(initVideoLazy, 50));

  /* ─── COOKIE CONSENT + GA ───────────────────────────────── */
  const GA_ID = 'G-QGPYRWBXZ9';
  function loadGA() {
    if (window.gaLoaded) return;
    window.gaLoaded = true;
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag(){ dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID);
  }
  function resetConsent() {
    localStorage.removeItem('cookie-consent');
    const banner = document.getElementById('cookieConsent');
    if (banner) {
      banner.classList.add('visible');
      document.getElementById('cookieAccept').onclick = () => {
        localStorage.setItem('cookie-consent', 'accepted');
        banner.classList.remove('visible');
        loadGA();
      };
      document.getElementById('cookieDecline').onclick = () => {
        localStorage.setItem('cookie-consent', 'declined');
        banner.classList.remove('visible');
      };
    }
  }
  window.resetConsent = resetConsent;

  const consent = localStorage.getItem('cookie-consent');
  if (consent === 'accepted') {
    loadGA();
  } else if (consent !== 'declined') {
    const banner = document.getElementById('cookieConsent');
    if (banner) {
      requestAnimationFrame(() => banner.classList.add('visible'));
      document.getElementById('cookieAccept').addEventListener('click', () => {
        localStorage.setItem('cookie-consent', 'accepted');
        banner.classList.remove('visible');
        loadGA();
      });
      document.getElementById('cookieDecline').addEventListener('click', () => {
        localStorage.setItem('cookie-consent', 'declined');
        banner.classList.remove('visible');
      });
    }
  }
})();
