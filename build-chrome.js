// Writes the nav and footer from footer.js into every page as static HTML,
// so crawlers and readers without JavaScript get the name, the navigation
// and the footer links. footer.js stays the single source and still
// re-renders both at runtime.
// Run after editing NAV_HTML or FOOTER_HTML: node build-chrome.js
const fs = require('fs');
const dir = process.argv[2] || __dirname;
const js = fs.readFileSync(`${dir}/footer.js`, 'utf8');

function tpl(name) {
  const m = js.match(new RegExp('const ' + name + ' = `([\\s\\S]*?)`;'));
  if (!m) throw new Error(name + ' not found in footer.js');
  if (m[1].includes('${')) throw new Error(name + ' contains an interpolation');
  return m[1].trim();
}

const parts = { nav: tpl('NAV_HTML'), footer: tpl('FOOTER_HTML') };
let count = 0;
for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
  const path = `${dir}/${file}`;
  const before = fs.readFileSync(path, 'utf8');
  let html = before;
  for (const [key, body] of Object.entries(parts)) {
    const re = new RegExp(`<div id="${key}-mount">(?:<!--${key}:start-->[\\s\\S]*?<!--${key}:end-->)?</div>`);
    html = html.replace(re, () => `<div id="${key}-mount"><!--${key}:start-->${body}<!--${key}:end--></div>`);
  }
  if (html !== before) { fs.writeFileSync(path, html); count++; }
}
console.log('pages updated:', count);
