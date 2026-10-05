from Orange.classification import SVMLearner
# Los preprocesadores del learner se ajustan dentro de cada fold.
out_learner = SVMLearner(C=1.0, kernel="rbf", gamma=0.25,
                         probability=True, tol=0.001, max_iter=-1)
# Semilla de la calibración interna de probabilidades sklearn/libsvm.
out_learner.params["random_state"] = 42
out_learner.name = "SVM Iris (RBF, C=1, gamma=0.25)"
# Modelo completo solo para inspección; no es la evaluación CV.
out_classifier = out_learner(in_data) if in_data is not None else None
out_data = in_data
