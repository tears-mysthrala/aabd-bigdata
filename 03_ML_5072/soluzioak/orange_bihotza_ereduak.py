"""
5072 Ikasketa Automatikoa — Orange Data Mining praktika (Python API bidez).
Dataset: Heart Disease (Orange-n integratua)
Modeloak: Decision Tree, Logistic Regression, Random Forest, k-NN
Ebaluazioa: 10-Fold Cross-Validation, Nahasketa Matrizea, Zuhaitzaren Arauak

Exekuzioa:
    /home/tears/.local/share/uv/tools/orange3/bin/python 03_ML_5072/soluzioak/orange_bihotza_ereduak.py
"""

import Orange
from Orange.evaluation import CrossValidation, CA, AUC, F1, Precision, Recall
from Orange.classification import (
    TreeLearner,
    LogisticRegressionLearner,
    RandomForestLearner,
    KNNLearner,
)
from sklearn.metrics import confusion_matrix

def main():
    print("=" * 65)
    print("ORANGE DATA MINING — BIHOTZEKO GAIXOTASUNEN SAILKAPENA")
    print("=" * 65)

    # 1. Datuak kargatu
    data = Orange.data.Table("heart_disease")
    n = len(data)
    p = len(data.domain.attributes)
    print(f"\n[1] DATUAK KARGATUTA:")
    print(f"  - Instantziak (pazienteak): {n}")
    print(f"  - Ezaugarriak: {p}")
    print(f"  - Helburu-aldagaia: {data.domain.class_var.name} ({list(data.domain.class_var.values)})")

    # 2. Ereduak definitu
    tree = TreeLearner(max_depth=5)
    tree.name = "Decision Tree"

    lr = LogisticRegressionLearner()
    lr.name = "Logistic Regression"

    rf = RandomForestLearner(n_estimators=100)
    rf.name = "Random Forest"

    knn = KNNLearner(n_neighbors=5)
    knn.name = "k-NN (k=5)"

    learners = [lr, rf, tree, knn]

    # 3. 10-Fold Cross-Validation bidez ebaluatu
    print("\n[2] MODELOAK ENTRENATZEN ETA EBALUATZEN (10-Fold CV)...")
    cv = CrossValidation(k=10, random_state=42)
    res = cv(data, learners)

    auc = AUC(res)
    ca = CA(res)
    f1 = F1(res)
    prec = Precision(res)
    rec = Recall(res)

    print("\n[3] EBALUAZIO METRIKAK:")
    print("-" * 65)
    print(f"{'Eredua':<22} | {'AUC':<6} | {'CA (Acc)':<8} | {'F1':<6} | {'Prec':<6} | {'Recall':<6}")
    print("-" * 65)
    for i, l in enumerate(learners):
        print(f"{l.name:<22} | {auc[i]:.3f}  | {ca[i]:.3f}    | {f1[i]:.3f} | {prec[i]:.3f}  | {rec[i]:.3f}")
    print("-" * 65)

    # 4. Nahasketa Matrizeak
    print("\n[4] NAHASKETA MATRIZEAK (Errenkadak: Benetakoa, Zutabeak: Iragarria):")
    for i, l in enumerate(learners):
        cm = confusion_matrix(res.actual, res.predicted[i])
        print(f"\n--- {l.name} ---")
        print("                Iragarria: 0    Iragarria: 1")
        print(f"Benetan: 0 (Osasuntsu)   {cm[0, 0]:<14}  {cm[0, 1]:<14} (FP={cm[0, 1]})")
        print(f"Benetan: 1 (Gaixo)       {cm[1, 0]:<14}  {cm[1, 1]:<14} (FN={cm[1, 0]})")

    # 5. Erabaki-Zuhaitzaren Arau Nagusiak
    print("\n[5] EREDUAREN ARAUAK (demo akademikoa; ez dira gomendio klinikoak):")
    tree_model = TreeLearner(max_depth=3)(data)
    print(tree_model.print_tree())

    print("=" * 65)
    print("Exekuzioa ondo burutu da.")
    print("=" * 65)

if __name__ == "__main__":
    main()
