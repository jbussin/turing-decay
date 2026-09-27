import numpy as np, pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

REL = {  # generator public release (decimal year)
    "MixedGAN": 2018.5, "StyleGAN": 2018.95, "StyleGAN2": 2019.95,
    "StyleGAN3": 2021.47, "Diffusion": 2022.5, "StableDiffusion": 2022.64,
    "GPT4o": 2025.23,
}
df = pd.read_csv(DATA / "faces_pilot.csv")
df["y"] = df.acc - df.chance                      # distance above chance
df["v"] = df.sd**2 / df.n                         # sampling variance
df["gen_date"] = df.generator.map(REL)
df["t2i"] = df.generator.isin(["Diffusion", "StableDiffusion", "GPT4o"]).astype(int)
df["run_year"] = df.pub_year - 0.5                # rough: studies run ~6mo before pub

def metareg(d, cols, label):
    d = d.dropna(subset=cols)
    y, v = d.y.values, d.v.values
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
    k, p = X.shape
    W = np.diag(1 / v)
    XtWX_inv = np.linalg.inv(X.T @ W @ X)
    b = XtWX_inv @ X.T @ W @ y
    Q = float((y - X @ b) @ W @ (y - X @ b))
    P = W - W @ X @ XtWX_inv @ X.T @ W
    tau2 = max(0.0, (Q - (k - p)) / np.trace(P))   # DerSimonian-Laird
    Ws = np.diag(1 / (v + tau2))
    cov = np.linalg.inv(X.T @ Ws @ X)
    b = cov @ X.T @ Ws @ y
    # Knapp-Hartung adjustment
    r = y - X @ b
    s2 = float(r @ Ws @ r) / (k - p)
    se = np.sqrt(np.diag(cov) * max(s2, 1))
    from scipy import stats
    t = b / se
    pv = 2 * stats.t.sf(np.abs(t), k - p)
    print(f"\n== {label}  (k={k}, tau={np.sqrt(tau2):.3f})")
    for name, bi, si, pi in zip(["intercept"] + cols, b, se, pv):
        print(f"  {name:12s} {bi:+.4f}  se {si:.4f}  p={pi:.3f}")
    return b

d = df.copy()
gan = d[d.generator.isin(["MixedGAN", "StyleGAN", "StyleGAN2", "StyleGAN3"])]
sg2 = d[d.generator == "StyleGAN2"]

metareg(d, ["pub_year", "intervention"], "Naive: publication year only (replicates paper's direction)")
metareg(gan, ["gen_date", "run_year", "intervention"], "Two-clock, GAN family only")
metareg(sg2, ["run_year", "intervention"], "Observer clock alone: StyleGAN2 studies only")
metareg(d, ["gen_date", "run_year", "intervention", "t2i"], "Two-clock, all generators + text-to-image flag")

# Generator-level pooled means, untrained participants, GAN lineage
base = gan[(gan.intervention == 0) & gan.generator.isin(["StyleGAN", "StyleGAN2", "StyleGAN3", "MixedGAN"])]
print("\n== Pooled accuracy by generator (untrained, inverse-variance + tau)")
rows = []
for g, sub in d[d.intervention == 0].groupby("generator"):
    y, v = sub.y.values, sub.v.values
    w = 1 / v; mu = (w * y).sum() / w.sum()
    Q = (w * (y - mu) ** 2).sum()
    tau2 = max(0, (Q - (len(y) - 1)) / (w.sum() - (w**2).sum() / w.sum())) if len(y) > 1 else 0
    ws = 1 / (v + tau2); mu = (ws * y).sum() / ws.sum(); se = np.sqrt(1 / ws.sum())
    rows.append((g, REL.get(g), len(y), 0.5 + mu, se))
    print(f"  {g:22s} rel {REL.get(g)}  k={len(y):2d}  acc={0.5+mu:.3f} ± {1.96*se:.3f}")
pd.DataFrame(rows, columns=["generator", "release", "k", "acc", "se"]).to_csv(OUT / "generator_means.csv", index=False)
d.to_csv(OUT / "faces_pilot_coded.csv", index=False)
