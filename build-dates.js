// Sets dateModified in each page's JSON-LD and <lastmod> in sitemap.xml
// from git: the last commit that touched the file, or today if the file
// has uncommitted changes. Run just before committing: node build-dates.js
const fs = require('fs');
const { execFileSync } = require('child_process');
const dir = process.argv[2] || __dirname;
const git = (...a) => execFileSync('git', ['-C', dir, ...a], { encoding: 'utf8' }).trim();
const today = new Date().toISOString().slice(0, 10);
// A file counts as changed only if it differs from the last commit in
// more than the dates this script writes, so running it twice is safe.
const strip = t => t.replace(/,?\s*"dateModified": "[^"]*"/g, '').replace(/\s+/g, ' ');
function changed(f) {
  let head;
  try { head = execFileSync('git', ['-C', dir, 'show', `HEAD:${f}`], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); }
  catch (e) { return true; }
  return strip(head) !== strip(fs.readFileSync(`${dir}/${f}`, 'utf8'));
}
const dateOf = f => (changed(f) ? today : git('log', '-1', '--format=%cs', '--', f)) || today;
const MAIN = ['CreativeWork', 'CollectionPage', 'ProfilePage', 'WebSite'];
const B = 'https://frederikfrede.com/';

const dates = {};
let pages = 0;
for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
  const path = `${dir}/${file}`;
  let html = fs.readFileSync(path, 'utf8');
  const re = /(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/;
  const m = html.match(re);
  if (!m) continue;
  const date = dateOf(file);
  dates[file] = date;
  const data = JSON.parse(m[2]);
  const nodes = data['@graph'] || [data];
  const main = nodes.find(n => MAIN.includes(n['@type']));
  if (!main || main.dateModified === date) continue;
  main.dateModified = date;
  html = html.replace(re, (_, a, __, c) => `${a}\n${JSON.stringify(data, null, 2)}\n${c}`);
  fs.writeFileSync(path, html);
  pages++;
}

let sm = fs.readFileSync(`${dir}/sitemap.xml`, 'utf8');
let urls = 0;
sm = sm.replace(/<url>\s*<loc>([^<]+)<\/loc>\s*<lastmod>[^<]*<\/lastmod>/g, (block, loc) => {
  const file = loc === B ? 'index.html' : loc.replace(B, '');
  const date = dates[file] || (fs.existsSync(`${dir}/${file}`) ? dateOf(file) : today);
  urls++;
  return block.replace(/<lastmod>[^<]*<\/lastmod>/, `<lastmod>${date}</lastmod>`);
});
fs.writeFileSync(`${dir}/sitemap.xml`, sm);
console.log('pages with new dateModified:', pages, '| sitemap urls:', urls);
