(function() {
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
      <span class="cookie-text">This site uses analytics. <a href="/imprint.html">Imprint</a></span>
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
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: isMobile ? 0.05 : 0.15, rootMargin: isMobile ? '0px 0px -10% 0px' : '0px 0px -40px 0px' });
    targets.forEach(el => observer.observe(el));
  }
  window.addEventListener('load', () => setTimeout(initReveal, 50));

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
