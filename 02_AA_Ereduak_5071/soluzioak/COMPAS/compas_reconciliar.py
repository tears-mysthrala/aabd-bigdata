"""Reconcile COMPAS threshold metrics; persist only aggregated academic outputs.

The pinned identifiable source is cached outside the repository with mode 0600.
No row-level data, names, dates, IDs or individual predictions are exported.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import urllib.request

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'resultados'
COMMIT = 'c062fbb5fa84f6c99d82f432c46b405f3a0ca5ec'
SHA256 = 'c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d'
URL = f'https://raw.githubusercontent.com/propublica/compas-analysis/{COMMIT}/compas-scores-two-years.csv'
GROUPS = ['African-American', 'Caucasian']
COLUMNS = ['race', 'days_b_screening_arrest', 'is_recid', 'c_charge_degree',
           'score_text', 'decile_score', 'two_year_recid']


def source_path():
    """Fetch fixed bytes only if absent; never cache within the checkout."""
    cache = Path.home() / '.cache' / 'aabd-compas'
    repo = BASE.parents[2]
    if cache.resolve().is_relative_to(repo):
        raise ValueError('The source cache must remain outside the repository')
    cache.mkdir(mode=0o700, parents=True, exist_ok=True)
    cache.chmod(0o700)
    target = cache / f'{SHA256}.csv'
    if not target.exists():
        with urllib.request.urlopen(URL, timeout=60) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != SHA256:
            raise ValueError('Remote source hash mismatch')
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(content)
    if hashlib.sha256(target.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Cached source hash mismatch')
    target.chmod(0o600)
    return target


def wilson_interval(positive, n, z=1.959963984540054):
    """95% Wilson binomial intervals; descriptive, not equivalence tests."""
    if n == 0:
        return float('nan'), float('nan')
    p = positive / n
    denominator = 1 + z*z/n
    center = (p + z*z/(2*n))/denominator
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/denominator
    return center-half, center+half


def prepare_data():
    # Only analysis fields enter memory; no identifying columns are read.
    data = pd.read_csv(source_path(), usecols=COLUMNS, keep_default_na=False)
    assert len(data) == 7214
    numeric = ['days_b_screening_arrest', 'is_recid', 'decile_score', 'two_year_recid']
    for name in numeric:
        data[name] = pd.to_numeric(data[name], errors='coerce')
    filters = [
        ('days_b_screening_arrest between -30 and 30 inclusive', data.days_b_screening_arrest.between(-30, 30)),
        ('is_recid != -1', data.is_recid.ne(-1) & data.is_recid.notna()),
        ('c_charge_degree != O', data.c_charge_degree.ne('O')),
        ('score_text != N/A', data.score_text.ne('N/A')),
    ]
    selected = pd.Series(True, index=data.index)
    counts = [dict(step='raw source', n=len(data))]
    for description, mask in filters:
        selected &= mask
        counts.append(dict(step=description, n=int(selected.sum())))
    clean = data[selected].copy()
    assert len(clean) == 6172
    counts.append(dict(step='race in African-American, Caucasian', n=int(clean.race.isin(GROUPS).sum())))
    clean = clean[clean.race.isin(GROUPS)].copy()
    assert len(clean) == 5278
    assert clean[['decile_score', 'two_year_recid']].notna().all().all()
    assert clean.decile_score.between(1, 10).all()
    assert clean.decile_score.mod(1).eq(0).all()
    assert clean.two_year_recid.isin([0, 1]).all()
    assert clean.decile_score.ge(5).equals(clean.score_text.ne('Low'))
    return clean, counts


def aggregate_metrics(data):
    rows = []
    for threshold in [7, 5]:
        for group in GROUPS:
            subset = data[data.race.eq(group)]
            actual = subset.two_year_recid.eq(1)
            predicted = subset.decile_score.ge(threshold)
            tn = int((~actual & ~predicted).sum())
            fp = int((~actual & predicted).sum())
            fn = int((actual & ~predicted).sum())
            tp = int((actual & predicted).sum())
            n = len(subset)
            assert tn+fp+fn+tp == n and tn+fp > 0 and tp+fn > 0
            rows.append(dict(threshold=threshold, group=group, n=n, TN=tn, FP=fp, FN=fn, TP=tp,
                             negatives=tn+fp, positives=tp+fn, predicted_positives=tp+fp,
                             base_rate=(tp+fn)/n, FPR=fp/(fp+tn), FNR=fn/(fn+tp), TPR=tp/(tp+fn),
                             PPV=tp/(tp+fp), accuracy=(tp+tn)/n))
    return pd.DataFrame(rows)


def aggregate_scores(data):
    scores = data.groupby(['race', 'decile_score']).two_year_recid.agg(['sum', 'count']).reset_index()
    scores = scores.rename(columns={'race':'group', 'decile_score':'score', 'sum':'positives', 'count':'n'})
    scores['observed_rate'] = scores.positives / scores.n
    intervals = [wilson_interval(int(v.positives), int(v.n)) for v in scores.itertuples()]
    scores['lower_95'] = [v[0] for v in intervals]
    scores['upper_95'] = [v[1] for v in intervals]
    assert len(scores) == 20 and int(scores.n.sum()) == len(data)
    return scores


def render_figures(metrics, scores):
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11})
    colors = {'African-American':'#235a91', 'Caucasian':'#bd630b'}
    markers = {'African-American':'o', 'Caucasian':'s'}
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, threshold in zip(axes, [7, 5]):
        keys = ['FPR', 'FNR', 'TPR', 'base_rate']
        x = np.arange(len(keys))
        for i, group in enumerate(GROUPS):
            row = metrics[(metrics.threshold.eq(threshold)) & metrics.group.eq(group)].iloc[0]
            bars = ax.bar(x + (i-.5)*.34, [row[k]*100 for k in keys], width=.34,
                          label=f'{group} (n={row.n})', color=colors[group], hatch='' if i == 0 else '//')
            ax.bar_label(bars, fmt='%.1f%%', fontsize=8, padding=3)
        ax.set_xticks(x, ['FPR', 'FNR', 'TPR', 'Base rate'])
        ax.set_title(f"Score >= {threshold}" + (' / material threshold' if threshold == 7 else ' / separate comparison'))
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=.15)
        ax.legend(fontsize=9)
    axes[0].set_ylabel('Percent / denominator defined in metric table')
    fig.suptitle('COMPAS observed two-year label / same filtered population (n=5,278)')
    fig.tight_layout()
    fig.savefig(OUTPUT/'tasas_por_umbral.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios':[2,1]})
    for group in GROUPS:
        subset = scores[scores.group.eq(group)].sort_values('score')
        y = subset.observed_rate.to_numpy()
        errors = np.vstack([y-subset.lower_95.to_numpy(), subset.upper_95.to_numpy()-y])
        axes[0].errorbar(subset.score, y*100, yerr=errors*100, marker=markers[group],
                         color=colors[group], label=group, capsize=3)
        axes[1].plot(subset.score, subset.n, marker=markers[group], color=colors[group], label=group)
    axes[0].set(ylabel='Observed two-year label rate (%)', ylim=(0, 100),
                title='Observed rates by decile / 95% Wilson intervals / same filtered population')
    axes[0].legend()
    axes[1].set(xlabel='COMPAS decile_score (ordinal category; not a probability)', ylabel='Records per score', xticks=range(1,11))
    axes[1].set_ylim(bottom=0)
    for ax in axes:
        ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(OUTPUT/'tasas_por_score.png', dpi=180)
    plt.close(fig)


def run_analysis():
    OUTPUT.mkdir(exist_ok=True)
    data, counts = prepare_data()
    metrics = aggregate_metrics(data)
    scores = aggregate_scores(data)
    # Export only grouped counts/rates, never source rows.
    metrics.to_csv(OUTPUT/'metricas_umbral.csv', index=False)
    scores.to_csv(OUTPUT/'tasas_score.csv', index=False)
    render_figures(metrics, scores)
    source = dict(url=URL, commit=COMMIT, sha256=SHA256,
                  source_rows=7214, filtered_all_groups=6172, analysed_rows=5278,
                  groups=GROUPS, positive_label='two_year_recid = 1', primary_threshold=7,
                  comparison_threshold=5, filter_counts=counts,
                  unit='one source record; no new cohort or trained model',
                  stored_outputs='aggregate counts/rates and figures only; source is outside repository',
                  versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','matplotlib','nbformat','nbclient','ipykernel']},
                  python=platform.python_version())
    source['outputs_sha256'] = {name:hashlib.sha256((OUTPUT/name).read_bytes()).hexdigest()
                               for name in ['metricas_umbral.csv','tasas_score.csv','tasas_por_umbral.png','tasas_por_score.png']}
    (OUTPUT/'proveniencia.json').write_text(json.dumps(source, indent=2, ensure_ascii=False)+'\n')
    return metrics, scores, source


if __name__ == '__main__':
    metrics, scores, source = run_analysis()
    print(metrics.to_string(index=False))
    print('Population:', source['source_rows'], '->', source['filtered_all_groups'], '->', source['analysed_rows'])
    print('SHA256:', source['sha256'])
