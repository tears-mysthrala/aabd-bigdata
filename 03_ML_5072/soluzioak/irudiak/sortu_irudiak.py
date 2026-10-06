"""Render Heart Disease figures from recorded out-of-fold predictions."""
import csv
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score

BASE = Path(__file__).resolve().parent
DATA = BASE.parent / 'datos' / 'heart_disease'
report = json.loads((DATA / 'resultados_cv.json').read_text())
assert hashlib.sha256((DATA / 'predicciones_cv.csv').read_bytes()).hexdigest() == report['predictions_sha256']
with (DATA / 'predicciones_cv.csv').open() as f:
    rows = list(csv.DictReader(f))
models = report['models']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
COLORS = ['#2980B9', '#27AE60', '#E67E22', '#8E44AD']


def save(fig, name):
    fig.tight_layout()
    fig.savefig(BASE / name, dpi=300)
    plt.close(fig)
    print(BASE / name)


# Conceptual API pipeline, not a claimed GUI screenshot.
fig, ax = plt.subplots(figsize=(11, 4))
ax.axis('off')
boxes = [(0.12, 0.66, 'Heart Disease\n303 rows / 13 predictors'),
         (0.45, 0.66, 'Stratified CV\n10 folds / seed 42'),
         (0.8, 0.66, 'Each training fold\nImpute + model preprocessing'),
         (0.8, 0.23, 'Four learners\nLR / RF / Tree / k-NN'),
         (0.45, 0.23, 'Held-out predictions\nCSV + JSON'),
         (0.12, 0.23, 'Metrics / ROC / matrices\nFigures + PDF')]
for x, y, label in boxes:
    ax.text(x, y, label, transform=ax.transAxes, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.9', fc='#e8eff7', ec='#2980B9'), fontsize=9)
for a, b in zip(boxes, boxes[1:]):
    ax.annotate('', xy=(b[0], b[1]), xytext=(a[0], a[1]), xycoords='axes fraction',
                arrowprops=dict(arrowstyle='->', shrinkA=42 if a[0] == b[0] else 72, shrinkB=42 if a[0] == b[0] else 72, color='#444'))
ax.set_title('Orange Python API: preprocessing inside training folds', pad=18)
save(fig, 'orange_workflow.png')

keys = ['AUC', 'CA', 'F1', 'Precision', 'Recall']
fig, ax = plt.subplots(figsize=(11, 5))
x = np.arange(len(models))
for j, key in enumerate(keys):
    bars = ax.bar(x + (j-2)*0.15, [m['metrics'][key] for m in models], width=0.15, label=key)
    ax.bar_label(bars, fmt='%.3f', rotation=60, fontsize=7, padding=3)
ax.set_xticks(x, [m['name'] for m in models])
ax.set_ylim(0, 1.09)
ax.set_ylabel('Score')
ax.set_title('Pooled out-of-fold metrics / class 1 positive / 10-fold CV')
ax.legend(ncols=5, loc='lower center')
ax.grid(axis='y', alpha=0.2)
save(fig, 'metrics_comparison.png')

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
figroc, axroc = plt.subplots(figsize=(8, 6))
for m, ax, color in zip(models, axes.flat, COLORS):
    selected = [r for r in rows if r['model'] == m['name']]
    assert len(selected) == report['dataset']['n']
    y = np.array([int(r['actual']) for r in selected])
    pred = np.array([int(r['predicted']) for r in selected])
    probability = np.array([float(r['probability_1']) for r in selected])
    cm = confusion_matrix(y, pred, labels=[0, 1])
    assert np.array_equal(cm, m['confusion_matrix'])
    ax.imshow(cm, cmap='Blues', vmin=0, vmax=164)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', fontsize=18,
                    color='white' if cm[i, j] > 80 else '#222')
    ax.set_xticks([0, 1], ['0', '1'])
    ax.set_yticks([0, 1], ['0', '1'])
    ax.set_xlabel('Predicted class')
    ax.set_ylabel('Actual class')
    ax.set_title(f"{m['name']} / CA={m['metrics']['CA']:.3f}")
    fpr, tpr, _ = roc_curve(y, probability)
    auc = roc_auc_score(y, probability)
    assert np.isclose(auc, m['metrics']['AUC'])
    axroc.step(fpr, tpr, where='post', color=color, lw=2, label=f"{m['name']} (AUC={auc:.3f})")
fig.suptitle('Out-of-fold confusion matrices / positive class 1')
save(fig, 'confusion_matrices.png')
axroc.plot([0, 1], [0, 1], '--', color='gray', label='Chance baseline')
axroc.set(xlim=(0, 1), ylim=(0, 1.02), xlabel='False positive rate', ylabel='True positive rate',
          title='Empirical ROC from held-out probabilities / class 1')
axroc.legend(loc='lower right')
axroc.grid(alpha=0.2)
save(figroc, 'roc_curves.png')

fig, ax = plt.subplots(figsize=(11, 6.8))
ax.axis('off')
counts = report['display_tree']['root_counts']
text = f"Root counts [class 0 / class 1]: {counts}\n" + report['display_tree']['text']
ax.text(0.02, 0.96, text, transform=ax.transAxes, ha='left', va='top',
        family='DejaVu Sans Mono', fontsize=11, linespacing=1.2)
ax.set_title('Actual Orange tree rules / max_depth=3 / fitted on all rows\nIllustration only; CV evaluates max_depth=5', pad=14)
save(fig, 'decision_tree_vis.png')

# Bind the rendered images to the exact result artifact for the PDF builder.
manifest = dict(results_sha256=hashlib.sha256((DATA / 'resultados_cv.json').read_bytes()).hexdigest(),
                figures={name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
                         for name in ['orange_workflow.png', 'metrics_comparison.png',
                                      'confusion_matrices.png', 'roc_curves.png', 'decision_tree_vis.png']})
(DATA / 'figuras_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
