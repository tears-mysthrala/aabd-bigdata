"""Heart Disease: reproducible Orange CV and traceable report inputs.

Run with an Orange 3.40 environment. Paths are relative to this script, not cwd.
Preprocessors are fitted by each learner on each training fold, never globally.
"""
import csv
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import Orange
import sklearn
from Orange.classification import TreeLearner, LogisticRegressionLearner, RandomForestLearner, KNNLearner
from Orange.evaluation import CrossValidation
from Orange.preprocess import Continuize, Impute, Normalize
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'datos' / 'heart_disease'
SEED = 42


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Freeze the installed Orange sample so subsequent runs use the same bytes.
    source = OUTPUT / 'heart_disease.tab'
    if not source.exists():
        installed = Orange.data.Table('heart_disease')
        source.write_bytes(Path(installed.__file__).read_bytes())
    data = Orange.data.Table(str(source))
    assert data.domain.class_var.values == ('0', '1')
    assert np.isfinite(data.Y).all(), 'Missing target values require an explicit population policy'
    learners = [
        LogisticRegressionLearner(C=1, penalty='l2', max_iter=1000, random_state=SEED,
                                  preprocessors=[Continuize(), Impute(), Normalize()]),
        RandomForestLearner(n_estimators=100, random_state=SEED,
                            preprocessors=[Continuize(), Impute()]),
        TreeLearner(max_depth=5, preprocessors=[Impute()]),
        KNNLearner(n_neighbors=5, preprocessors=[Continuize(), Impute(), Normalize()]),
    ]
    names = ['Logistic Regression', 'Random Forest', 'Decision Tree', 'k-NN (k=5)']
    settings = [
        {'C': 1, 'penalty': 'l2', 'max_iter': 1000, 'random_state': SEED},
        {'n_estimators': 100, 'random_state': SEED, 'max_depth': None, 'max_features': 'sqrt'},
        {'max_depth': 5, 'min_samples_leaf': 1, 'min_samples_split': 2, 'sufficient_majority': 0.95},
        {'n_neighbors': 5, 'metric': 'euclidean', 'weights': 'uniform'},
    ]
    cv = CrossValidation(k=10, stratified=True, random_state=SEED, store_models=False)
    result = cv(data, learners)
    if any(result.failed):
        raise RuntimeError(f'Failed learners: {result.failed}')
    fold_by_row = {}
    for fold, (_, test) in enumerate(cv.get_indices(data), 1):
        for row in test:
            fold_by_row[int(row)] = fold
    records = []
    models = []
    y = result.actual.astype(int)
    for i, name in enumerate(names):
        pred = result.predicted[i].astype(int)
        prob = result.probabilities[i, :, 1]
        assert len(set(result.row_indices)) == len(data)
        assert np.isfinite(prob).all() and ((0 <= prob) & (prob <= 1)).all()
        fpr, tpr, thresholds = roc_curve(y, prob)
        metrics = dict(AUC=float(roc_auc_score(y, prob)), CA=float(accuracy_score(y, pred)),
                       F1=float(f1_score(y, pred, pos_label=1, zero_division=0)),
                       Precision=float(precision_score(y, pred, pos_label=1, zero_division=0)),
                       Recall=float(recall_score(y, pred, pos_label=1, zero_division=0)))
        models.append(dict(name=name, learner=type(learners[i]).__name__, settings=settings[i],
                           preprocessors=[repr(p) for p in learners[i].preprocessors], metrics=metrics,
                           confusion_matrix=confusion_matrix(y, pred, labels=[0, 1]).tolist(),
                           roc=dict(fpr=fpr.tolist(), tpr=tpr.tolist(),
                                    thresholds=[float(t) if np.isfinite(t) else None for t in thresholds])))
        for row, actual, predicted, probability in zip(result.row_indices, y, pred, prob):
            records.append(dict(row_index=int(row), fold=fold_by_row[int(row)], model=name,
                                actual=int(actual), predicted=int(predicted), probability_1=float(probability)))
        print(name, metrics, models[-1]['confusion_matrix'])
    # Display model is explicitly separate from the evaluated depth-5 model.
    display_tree = TreeLearner(max_depth=3, preprocessors=[Impute()])(data)
    report = dict(dataset=dict(file='heart_disease.tab', sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                              n=len(data), predictors=len(data.domain.attributes), target=data.domain.class_var.name,
                              class_values=list(data.domain.class_var.values), class_counts=np.bincount(data.Y.astype(int)).tolist(),
                              positive_class='1', missing_predictor_cells=int(np.isnan(data.X).sum()),
                              attributes=[dict(name=a.name, type='categorical' if a.is_discrete else 'continuous') for a in data.domain.attributes]),
                  evaluation=dict(k=10, stratified=True, shuffle=True, random_state=SEED,
                                  aggregation='pooled out-of-fold predictions; binary F1/Precision/Recall for class 1',
                                  predictions='learner class decision; ROC uses probability for class 1',
                                  preprocessing='fitted within each training fold by the learner'),
                  versions=dict(python=platform.python_version(), Orange=Orange.__version__, sklearn=sklearn.__version__, numpy=np.__version__),
                  models=models, display_tree=dict(max_depth=3, fitted_on='all rows; illustration only, not CV performance',
                                                    root_counts=display_tree.root.value.tolist(), text=display_tree.print_tree()))
    records.sort(key=lambda r: (names.index(r['model']), r['row_index']))
    csv_path = OUTPUT / 'predicciones_cv.csv'
    with csv_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    report['predictions_sha256'] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    (OUTPUT / 'resultados_cv.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    print('Saved:', OUTPUT)


if __name__ == '__main__':
    main()
