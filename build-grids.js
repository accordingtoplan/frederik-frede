// Writes the project grids on index.html and work.html into the HTML, so
// crawlers and readers without JavaScript see every card, image and link.
// The pages' own render code is run here against a tiny stand-in DOM, so
// the baked markup is exactly what the browser would build.
// index.html keeps the baked cards; work.html still reshuffles on load.
// Run after editing the cases/projects arrays: node build-grids.js
const fs = require('fs');
const dir = process.argv[2] || __dirname;

function arrayDecl(src, decl) {
  const start = src.indexOf(decl);
  if (start < 0) throw new Error('missing ' + decl);
  let i = src.indexOf('[', start), depth = 0;
  for (; i < src.length; i++) {
    if (src[i] === '[') depth++;
    else if (src[i] === ']' && --depth === 0) break;
  }
  return src.slice(start, i + 1) + ';';
}
function between(src, from, to) {
  const a = src.indexOf(from), b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error('missing code block: ' + from);
  return src.slice(a, b);
}

const esc = v => String(v).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
class El {
  constructor(tag) { this.tagName = tag; this.className = ''; this.innerHTML = ''; this.children = []; this.style = { cssText: '' }; }
  appendChild(c) { this.children.push(c); return c; }
  get outerHTML() {
    const attrs = [['href', this.href], ['class', this.className], ['style', this.style.cssText], ['target', this.target], ['rel', this.rel]]
      .filter(([, v]) => v).map(([k, v]) => ` ${k}="${esc(v)}"`).join('');
    return `<${this.tagName}${attrs}>${this.innerHTML}</${this.tagName}>`;
  }
}
const fakeDocument = grid => ({ createElement: t => new El(t), getElementById: () => grid });

function bake(file, anchorRe, cardsHtml) {
  const path = `${dir}/${file}`;
  let html = fs.readFileSync(path, 'utf8');
  html = html.replace(/\n\s*<noscript class="grid-fallback">[\s\S]*?<\/noscript>/, '');
  const m = html.match(anchorRe);
  if (!m) throw new Error('grid container missing in ' + file);
  html = html.replace(anchorRe, `${m[1]}<!--grid:start-->${cardsHtml}<!--grid:end--></div>`);
  fs.writeFileSync(path, html);
}

// index.html
{
  const src = fs.readFileSync(`${dir}/index.html`, 'utf8');
  const code = arrayDecl(src, 'const cases = [') + '\n' +
    between(src, "const grid = document.getElementById('cases');", '// Lazy-load below-fold');
  const grid = new El('div');
  new Function('document', code.replace(/if \(!grid\.children\.length\) /, ''))(fakeDocument(grid));
  bake('index.html', /(<div class="cases-grid" id="cases">)(?:<!--grid:start-->[\s\S]*?<!--grid:end-->)?<\/div>/,
    grid.children.map(c => c.outerHTML).join(''));
  console.log('index.html cards:', grid.children.length);
}

// work.html
{
  const src = fs.readFileSync(`${dir}/work.html`, 'utf8');
  const code = arrayDecl(src, 'const projects = [') + '\n' + arrayDecl(src, 'const VITRA = [') + '\n' +
    between(src, 'function makeCard(', 'function buildGrid(') + '\nreturn projects.map(makeCard);';
  const cards = new Function('document', code)(fakeDocument(null));
  bake('work.html', /(<div class="work-grid" id="work-grid">)(?:<!--grid:start-->[\s\S]*?<!--grid:end-->)?<\/div>/,
    cards.map(c => c.outerHTML).join(''));
  console.log('work.html cards:', cards.length);
}
