// Tells Bing, Yandex and other IndexNow engines which pages changed, so
// they recrawl within minutes. Run after a push has deployed:
//   node ping-indexnow.js            pages changed in the last commit
//   node ping-indexnow.js HEAD~3     pages changed since that commit
//   node ping-indexnow.js --all      every URL in sitemap.xml
// The key is the name of the <32 hex chars>.txt file in the site root.
const fs = require('fs');
const https = require('https');
const { execFileSync } = require('child_process');
const dir = __dirname;
const HOST = 'frederikfrede.com';
const B = `https://${HOST}/`;

const keyFile = fs.readdirSync(dir).find(f => /^[0-9a-f]{32}\.txt$/.test(f));
if (!keyFile) throw new Error('IndexNow key file missing');
const key = keyFile.slice(0, -4);

const sitemap = fs.readFileSync(`${dir}/sitemap.xml`, 'utf8');
const all = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
let urls;
if (process.argv[2] === '--all') {
  urls = all;
} else {
  const since = process.argv[2] || 'HEAD~1';
  const changed = execFileSync('git', ['-C', dir, 'diff', '--name-only', since, 'HEAD'], { encoding: 'utf8' })
    .split('\n').filter(Boolean);
  urls = changed.map(f => (f === 'index.html' ? B : B + f)).filter(u => all.includes(u));
}
if (!urls.length) { console.log('No sitemap pages changed.'); process.exit(0); }

const body = JSON.stringify({ host: HOST, key, keyLocation: `${B}${keyFile}`, urlList: urls });
const req = https.request('https://api.indexnow.org/indexnow',
  { method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) } },
  res => console.log(`IndexNow: HTTP ${res.statusCode} for ${urls.length} URL(s)`));
req.on('error', e => console.error('IndexNow failed:', e.message));
req.end(body);
