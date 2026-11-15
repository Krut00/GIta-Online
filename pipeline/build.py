"""Rebuild the Gita Pathshala site from base.html + explanation batches.

Run from anywhere:  python3 -I pipeline/build.py
Reads : pipeline/base.html, pipeline/batches/b*.json, pipeline/original-exp/ch{1-9}.json
Writes: index.html and exp/ch1..ch18.json (repo root)
"""
import json, glob, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = ROOT
os.makedirs(os.path.join(SITE, 'exp'), exist_ok=True)
html = open(os.path.join(HERE, 'base.html'), encoding='utf8').read()
V = json.loads(re.search(r'id="VDATA">(.*?)</script>', html, re.S).group(1))
valid = {f"{x['c']}.{x['v']}" for x in V}
F = ['wm','tr','simple','deep','ctx','ex','apply','mis','interp','rq','take']
new = {}
for f in sorted(glob.glob(os.path.join(HERE, 'batches', 'b*.json'))):
    for k, e in json.load(open(f, encoding='utf8')).items():
        assert k in valid, k
        n = len(e['w'])
        for lg in ('en', 'hi', 'gu'):
            assert list(e[lg].keys()) == F, (k, lg)
            assert len(e[lg]['wm']) == n, (k, lg, 'wm')
            assert len(e[lg]['ex']) == 2 and 1 <= len(e[lg]['interp']) <= 4, (k, lg)
            assert all(isinstance(i, list) and len(i) == 2 for i in e[lg]['interp']), (k, lg)
        new[k] = e
total = 0
for c in range(1, 19):
    p = os.path.join(HERE, 'original-exp', f'ch{c}.json')
    d = json.load(open(p, encoding='utf8')) if os.path.exists(p) else {}
    d.update({k: e for k, e in new.items() if int(k.split('.')[0]) == c})
    total += len(d)
    json.dump(d, open(os.path.join(SITE, 'exp', f'ch{c}.json'), 'w', encoding='utf8'),
              ensure_ascii=False, separators=(',', ':'))
m = re.search(r'"expKeys":(\[.*?\])', html)
keys = json.loads(m.group(1))
keys += [k for k in new if k not in keys]
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf8').write(
    html.replace(m.group(0), '"expKeys":' + json.dumps(keys), 1))
print(f'batch entries: {len(new)} | explained verses: {total}/{len(valid)} | expKeys: {len(keys)}')
