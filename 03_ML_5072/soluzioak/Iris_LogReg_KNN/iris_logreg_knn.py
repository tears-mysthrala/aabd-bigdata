#!/usr/bin/env python3
"""Ikaskuntza Gainbegiratua (Iris): LogReg vs KNN, decision boundaries.

Enuntziatua: ../../materialak/ikaskuntza_gainbegiratua_ikaslea.ipynb
Exekutatu karpeta honetan: python iris_logreg_knn.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

# 1. Iris: sepal length + width (lehenengo 2 zutabeak).
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
print("X:", X.shape, "| klaseak:", list(iris.target_names))


def plot_decision_boundaries(clf, X, y, ax, title):
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors="k", cmap=plt.cm.RdYlBu)
    ax.set_xlabel("sepal length")
    ax.set_ylabel("sepal width")
    ax.set_title(title)


# 3. LogReg lineal (max_iter=200) eta 4. KNN (k=3).
logreg = LogisticRegression(max_iter=200)
logreg.fit(X, y)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

acc_lr = accuracy_score(y, logreg.predict(X))
acc_knn = accuracy_score(y, knn.predict(X))
print(f"LogReg accuracy: {acc_lr:.4f} | KNN(3) accuracy: {acc_knn:.4f}")

# 5. Side-by-side.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plot_decision_boundaries(logreg, X, y, ax1, "Erregresio Logistikoa (lineala)")
plot_decision_boundaries(knn, X, y, ax2, "KNN k=3 (ez-lineala)")
fig.tight_layout()
fig.savefig("erabaki_mugak.png", dpi=150)
print("erabaki_mugak.png gorde da")
