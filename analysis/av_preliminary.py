"""PRELIMINARY audio/video analysis (H1, H3, H6 and descriptive H2, H4, H5, and training).

Status: runs on unverified extraction (data/av_extraction.csv), before the
verification pass and before missing numbers were recovered. The results are
provisional and are not the registered confirmatory results.

Model (preregistration.md): three-level random-effects meta-regression
(groups nested in papers), REML, t-tests with k - p df.
"""
import csv, re, json, math
import numpy as np
from scipy import optimize, stats

D = 'data/'
rows = list(csv.DictReader(open(D + 'av_extraction.csv')))
gen = {r['row_id']: r for r in csv.DictReader(open(D + 'generator_coding.csv'))}
DROP = {r['target'] for r in csv.DictReader(open(D + 'verification_log.csv')) if r['status'] == 'drop'}
rec = {r['record_id']: r for r in csv.DictReader(open('search/records.csv'))}

def num(x):
    try: return float(str(x).replace('%', '').replace(',', '').strip())
    except Exception: return None

def year_run(r):
    m = re.findall(r'(20[12]\d)', r['data_collection'])
    if m:
        ys = sorted(set(int(y) for y in m))
        return (ys[0] + ys[-1]) / 2 + 0.5
    pubs = [num(rec[x]['year']) for x in r['record_ids'].split(';') if x in rec]
    pubs = [p for p in pubs if p]
    return (min(pubs) - 0.5) if pubs else None   # publication year minus 0.5

def effort(r):
    c = r['curation'].lower(); p = r['post_processing'].lower()
    hides = any(k in p for k in ['codec', 'gsm', 'volte', 'voip', 'telephone', 'whatsapp', 'noise', 'compress', 'beautification'])
    if 'adversarial' in c or hides: return 2
    if 'curated' in c: return 1
    return 0

def expertise(r):
    t = r['participant_type'].lower()
    if 'generative' in t: return 2
    if any(k in t for k in ['professional', 'expert', 'police', 'forensic', 'researcher']) and 'general public' not in t[:15]:
        return 1
    return 0

def training(r):
    return 1 if r['training_feedback'].strip().startswith('1') else 0

data = []
for r in rows:
    g = gen[r['row_id']]
    if g['coding_status'] != 'coded' or not r['accuracy_pct']: continue
    if r['study_id'] in DROP or r['row_id'] in DROP: continue
    if r['minors_included'].strip().startswith('1'): continue
    acc = num(r['accuracy_pct']); n = num(r['n_participants'])
    if acc is None or not n: continue
    ch = num(r['chance']) or 0.5
    p = acc / 100
    sd = num(r['accuracy_sd']); tr = num(r['trials_per_participant'])
    if sd is not None and sd > 0:
        v = (sd / 100) ** 2 / n; approx = 0
    elif tr:
        v = p * (1 - p) / (n * tr); approx = 1
    else:
        v = p * (1 - p) / n; approx = 1
    mod = r['modality']
    data.append(dict(row=r['row_id'], study=r['study_id'], dep=r['dependence_id'] or r['row_id'],
                     modality='audio' if mod == 'audio' else 'video',  # audiovisual analysed with video
                     y=p - ch, v=max(v, 1e-6), approx=approx, gendate=float(g['release_decimal']),
                     family=g['family'], effort=effort(r), expert=expertise(r), train=training(r),
                     yrun=year_run(r), comps=g['components'], n=n, conf=r['extraction_confidence']))

# family reset: earliest included generator within family and modality
for m in ['audio', 'video']:
    first = {}
    for d in data:
        if d['modality'] != m or 'dataset' in d['family']: continue
        first[d['family']] = min(first.get(d['family'], 9e9), d['gendate'])
    for d in data:
        if d['modality'] == m:
            d['reset'] = 0 if 'dataset' in d['family'] else int(abs(d['gendate'] - first.get(d['family'], -1)) < 1e-9)

def fit3(sub, cols, center=2020.0):
    y = np.array([d['y'] for d in sub]); v = np.array([d['v'] for d in sub])
    X = np.column_stack([np.ones(len(sub))] + [np.array([d[c] for d in sub], float) - (center if c in ('gendate', 'yrun') else 0) for c in cols])
    # drop constant columns
    keep = [0] + [j for j in range(1, X.shape[1]) if np.ptp(X[:, j]) > 0]
    names = ['intercept'] + [cols[j - 1] for j in keep[1:]]
    X = X[:, keep]
    studies = sorted(set(d['study'] for d in sub)); si = np.array([studies.index(d['study']) for d in sub])
    Z = (si[:, None] == np.arange(len(studies))[None, :]).astype(float)
    k, p = X.shape
    def V(t):
        s2u, s2e = np.exp(t)
        return np.diag(v + s2e) + s2u * Z @ Z.T
    def nll(t):
        Vm = V(t); Vi = np.linalg.inv(Vm)
        XtViX = X.T @ Vi @ X
        b = np.linalg.solve(XtViX, X.T @ Vi @ y); r = y - X @ b
        return 0.5 * (np.linalg.slogdet(Vm)[1] + np.linalg.slogdet(XtViX)[1] + r @ Vi @ r)
    best = min((optimize.minimize(nll, np.log([a, b]), method='Nelder-Mead') for a in (1e-3, 1e-2) for b in (1e-3, 1e-2)), key=lambda o: o.fun)
    Vi = np.linalg.inv(V(best.x)); cov = np.linalg.inv(X.T @ Vi @ X); b = cov @ X.T @ Vi @ y
    se = np.sqrt(np.diag(cov)); df = max(k - p, 1); t = b / se
    out = {}
    for j, nm in enumerate(names):
        out[nm] = dict(b=float(b[j]), se=float(se[j]), t=float(t[j]), df=df,
                       p_two=float(2 * stats.t.sf(abs(t[j]), df)),
                       ci=[float(b[j] - stats.t.ppf(.975, df) * se[j]), float(b[j] + stats.t.ppf(.975, df) * se[j])])
    return dict(k=k, papers=len(studies), sigma2=[float(x) for x in np.exp(best.x)], coef=out)

res = {}
cov_full = ['gendate', 'reset', 'effort', 'expert', 'yrun', 'train']
for m in ['audio', 'video']:
    sub = [d for d in data if d['modality'] == m and d['yrun']]
    res[m] = dict(full=fit3(sub, cov_full), gendate_only=fit3(sub, ['gendate']),
                  untrained_general=fit3([d for d in sub if d['train'] == 0 and d['expert'] == 0], ['gendate']))
    # H3: fixed generator -> within-generator year-run slope (generator fixed effects)
    gens = sorted(set(d['comps'] for d in sub if d['train'] == 0 and d['expert'] == 0))
    multi = [c for c in gens if len({d['study'] for d in sub if d['comps'] == c}) >= 2]
    hs = [dict(d, **{f'g{i}': int(d['comps'] == c) for i, c in enumerate(multi[1:])}) for d in sub if d['comps'] in multi and d['train'] == 0 and d['expert'] == 0]
    res[m]['H3_fixed_generator'] = fit3(hs, ['yrun'] + [f'g{i}' for i in range(len(multi) - 1)]) if len(hs) >= 4 else None
    res[m]['H3_generators'] = multi
# H6 pooled with interaction
for d in data: d['is_video'] = int(d['modality'] == 'video'); d['gd_x_video'] = (d['gendate'] - 2020) * d['is_video']
res['pooled_H6'] = fit3([d for d in data if d['yrun']], ['gendate', 'is_video', 'gd_x_video'])
res['n_rows'] = {m: sum(d['modality'] == m for d in data) for m in ['audio', 'video']}
res['n_papers'] = {m: len({d['study'] for d in data if d['modality'] == m}) for m in ['audio', 'video']}
json.dump(res, open('output/av_preliminary.json', 'w'), indent=1)
w = csv.DictWriter(open('output/av_analysis_rows.csv', 'w', newline=''), fieldnames=list(data[0].keys()))
w.writeheader(); w.writerows(data)

def show(title, f):
    print(f'\n== {title}  (k={f["k"]}, papers={f["papers"]}, tau2 paper/group={f["sigma2"][0]:.4f}/{f["sigma2"][1]:.4f})')
    for nm, c in f['coef'].items():
        print(f'  {nm:10s} b={c["b"]*100:+7.2f} pts  95% CI [{c["ci"][0]*100:+.2f}, {c["ci"][1]*100:+.2f}]  p(2-sided)={c["p_two"]:.3f}')
for m in ['audio', 'video']:
    print(f'\n######## {m.upper()}: rows={res["n_rows"][m]}, papers={res["n_papers"][m]}')
    show('GenDate only', res[m]['gendate_only'])
    show('Untrained general public, GenDate only', res[m]['untrained_general'])
    show('Full registered model', res[m]['full'])
    if res[m]['H3_fixed_generator']: show('H3 year-run slope with generator fixed effects: ' + ' | '.join(res[m]['H3_generators']), res[m]['H3_fixed_generator'])
show('Pooled H6 (gd_x_video = video minus audio slope)', res['pooled_H6'])
