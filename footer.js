(function() {
  /* ─── NAV INJECTION ──────────────────────────────────── */
  /* Synchronous — runs immediately when script parses at bottom of body.
     nav-mount div already exists in DOM at that point. */
  const NAV_HTML = `<nav class="nav">
  <div class="nav-left">
    <a class="nav-logo" href="/">Frederik</a>
    <a class="nav-studio" href="/">&nbsp;Frede</a>
  </div>
  <div class="nav-center">
    <div class="swatches">
      <div class="swatch" style="background:#fff" onclick="setTheme('white',this)"></div>
      <div class="swatch" style="background:#111" onclick="setTheme('black',this)"></div>
      <div class="swatch" style="background:#e63222" onclick="setTheme('signal',this)"></div>
    </div>
  </div>
  <div class="nav-right" id="navLinks">
    <ul>
      <button class="nav-close" aria-label="Close menu" onclick="document.getElementById('navLinks').classList.remove('open')">×</button>
      <li><a href="/" onclick="document.getElementById('navLinks').classList.remove('open')">Home</a></li>
      <li><a href="/work.html" onclick="document.getElementById('navLinks').classList.remove('open')">Work</a></li>
      <li><a href="/about.html" onclick="document.getElementById('navLinks').classList.remove('open')">About</a></li>
      <li><a href="/about.html#contact" onclick="document.getElementById('navLinks').classList.remove('open')">Contact</a></li>
    </ul>
  </div>
  <button class="hamburger" aria-label="Menu" onclick="document.getElementById('navLinks').classList.toggle('open')"><span></span><span></span></button>
</nav>`;
  const navMount = document.getElementById('nav-mount');
  if (navMount) {
    navMount.innerHTML = NAV_HTML;
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

  const FOOTER_HTML = `<div class="footer-bar">
      <div class="footer-top-row">
        <div class="footer-logo-row">
          <img src="/frede-logo.png" alt="FREDE" class="footer-logo">
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
        <span class="footer-copy">© 2026 <span class="footer-frak">Frede</span> · <a href="/imprint.html" class="footer-copy-link">Imprint</a></span>
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
