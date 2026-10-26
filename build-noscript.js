// Generates <noscript> fallback lists for the JS-built grids on index.html and work.html.
// Run after editing the cases/projects arrays: node build-noscript.js
const fs = require('fs');
const dir = process.argv[2] || __dirname;

function extract(html, decl) {
  const start = html.indexOf(decl);
  const open = html.indexOf('[', start);
  let depth = 0, i = open;
  for (; i < html.length; i++) {
    if (html[i] === '[') depth++;
    else if (html[i] === ']' && --depth === 0) break;
  }
  return eval(html.slice(open, i + 1));
}

const sentence = s => {
  s = String(s).replace(/<br\s*\/?>/g, ', ').replace(/•\s*/g, '').replace(/\s+/g, ' ').trim();
  return /[.!?]$/.test(s) ? s : s + '.';
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function inject(file, decl, anchor, render, indent) {
  const path = `${dir}/${file}`;
  let html = fs.readFileSync(path, 'utf8');
  html = html.replace(/\n\s*<noscript class="grid-fallback">[\s\S]*?<\/noscript>/, '');
  const items = extract(html, decl).filter(p => p.link);
  const lis = items.map(p => `${indent}  <li>${render(p)}</li>`).join('\n');
  const block = `${indent}<noscript class="grid-fallback">\n${indent}<ul>\n${lis}\n${indent}</ul>\n${indent}</noscript>`;
  if (!html.includes(anchor)) throw new Error(`anchor missing in ${file}`);
  html = html.replace(anchor, `${anchor}\n${block}`);
  fs.writeFileSync(path, html);
  console.log(file, items.length);
}

inject('index.html', 'const cases = [', '<div class="cases-grid" id="cases"></div>',
  c => `<a href="${c.link}">${esc(c.b)}</a>. ${esc(sentence(c.desc))} ${esc(c.tag)}${c.year ? `, ${esc(c.year)}` : ''}.`, '    ');
inject('work.html', 'const projects = [', '<div class="work-grid" id="work-grid"></div>',
  p => `<a href="${p.link}">${esc(p.b)}</a>. ${esc(p.t)}.`, '  ');
