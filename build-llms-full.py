"""Writes llms-full.txt: the readable text of every public page in one
Markdown file, so an agent can read the whole practice in one request.
Run after editing page copy: python3 build-llms-full.py"""
import html, json, os, re, sys
from html.parser import HTMLParser

DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
B = 'https://frederikfrede.com/'
SKIP_TAGS = {'script', 'style', 'noscript', 'svg', 'nav', 'footer', 'form', 'button', 'video', 'iframe', 'template'}
BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'dt', 'dd', 'figcaption', 'div', 'section', 'header'}
HEAD = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'h4': '#### '}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.buf, self.skip, self.inmain, self.prefix = [], [], 0, 0, ''

    def flush(self):
        t = re.sub(r'\s+', ' ', ''.join(self.buf)).strip()
        if t:
            self.out.append(self.prefix + t)
        self.buf, self.prefix = [], ''

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.inmain += 1
        if not self.inmain:
            return
        if tag in SKIP_TAGS:
            self.skip += 1
        elif not self.skip and tag in BLOCK | {'br'}:
            self.flush()
            if tag in HEAD:
                self.prefix = HEAD[tag]
            elif tag == 'li':
                self.prefix = '- '

    def handle_endtag(self, tag):
        if tag == 'main':
            self.flush()
            self.inmain = max(0, self.inmain - 1)
        if not self.inmain:
            return
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and tag in BLOCK:
            self.flush()
        elif not self.skip and tag == 'span':
            self.buf.append(' ')  # keep inline labels apart, e.g. client and year

    def handle_data(self, data):
        if self.inmain and not self.skip:
            self.buf.append(data)


def page_text(src):
    p = Text()
    p.feed(src)
    p.flush()
    lines, seen, label = [], set(), None
    for line in p.out:
        key = line.lstrip('#- ').strip()
        if len(key) <= 1 or key in ('—', '–', '-', 'View all', 'More Work', 'View all work'):
            continue  # section letters and empty credit values
        if line.startswith('# '):
            continue  # the page h1 repeats the title used as this section's heading
        if line.startswith('#') and key in seen:
            continue
        seen.add(key)
        lines.append('##' + line if line.startswith('#') else line)
    # credits: "Year" followed by "2019" reads better as "Year: 2019"
    labels = ('Live site', 'Year', 'Collaborators', 'Press', 'Photography', 'Director', 'Co-founders', 'Typefaces')
    out = []
    for line in lines:
        if out and out[-1] in labels and line not in labels and not line.startswith('#'):
            out[-1] = out[-1] + ': ' + line
        else:
            out.append(line)
    out = [l for l in out if l not in labels]  # labels left without a value
    return '\n\n'.join(out)


def meta(src, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % name, src)
    return html.unescape(m.group(1)) if m else ''


def main():
    sm = open(os.path.join(DIR, 'sitemap.xml'), encoding='utf-8').read()
    urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    files = ['index.html' if u == B else u.replace(B, '') for u in urls]
    first = ['index.html', 'about.html', 'work.html', 'ai-consulting.html', 'hospitality.html', 'real-estate.html', 'space-making.html']
    order = [f for f in first if f in files] + sorted(f for f in files if f not in first)
    head = open(os.path.join(DIR, 'llms.txt'), encoding='utf-8').read().split('\n## ')[0].strip()
    parts = [head, 'This file holds the text of every page on frederikfrede.com. A shorter index is at https://frederikfrede.com/llms.txt.']
    for f in order:
        src = open(os.path.join(DIR, f), encoding='utf-8').read()
        title = html.unescape(re.search(r'<title>([^<]*)</title>', src).group(1)).strip()
        url = B if f == 'index.html' else B + f
        body = page_text(src)
        parts.append('---\n\n## %s\n\nURL: %s\n\n%s\n\n%s' % (title, url, meta(src, 'description'), body))
    out = '\n\n'.join(parts).strip() + '\n'
    open(os.path.join(DIR, 'llms-full.txt'), 'w', encoding='utf-8').write(out)
    print('pages:', len(order), '| size: %d KB' % (len(out.encode()) // 1024))


main()
