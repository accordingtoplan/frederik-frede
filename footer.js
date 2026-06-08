(function() {
  const FOOTER_HTML = `<div class="footer-bar">
      <div class="footer-left">
        <div class="footer-logo-row">
          <img src="/frede-studio/frede-logo.png" alt="FREDE" class="footer-logo">
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
        <span class="footer-copy">© 2026 <span class="footer-frak">Frede</span> · <a href="/frede-studio/imprint.html" class="footer-copy-link">Imprint</a></span>
      </div>
      <div class="footer-links">
        <a href="https://instagram.com/frederikfrede" target="_blank" rel="noopener">Instagram</a>
        <a href="https://linkedin.com/in/frede" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://substack.com/@frederikfrede" target="_blank" rel="noopener">Substack</a>
      </div>
      <form class="footer-subscribe" action="https://substack.com/api/v1/free" method="get" target="_blank">
        <input type="email" name="email" placeholder="your@email.com" class="subscribe-input" required>
        <button type="submit" class="subscribe-btn">Subscribe</button>
      </form>
    </div>`;

  const mount = document.getElementById('footer-mount');
  if (mount) mount.innerHTML = FOOTER_HTML;
})();
