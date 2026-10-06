from Orange.classification import TreeLearner
out_learner = TreeLearner(max_depth=3, min_samples_leaf=2,
                          min_samples_split=5, binarize=True,
                          sufficient_majority=0.95)
out_learner.name = "Árbol Iris (profundidad 3)"
# Modelo completo solo para inspección; no es la evaluación CV.
out_classifier = out_learner(in_data) if in_data is not None else None
out_data = in_data
