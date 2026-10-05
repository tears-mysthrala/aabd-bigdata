from Orange.classification import RandomForestLearner
out_learner = RandomForestLearner(n_estimators=100, random_state=42,
    max_features="sqrt", max_depth=None, min_samples_split=5,
    min_samples_leaf=1, bootstrap=True, class_weight=None)
out_learner.name = "Random Forest Iris (100, semilla 42)"
# Modelo completo solo para inspección; no es la evaluación CV.
out_classifier = out_learner(in_data) if in_data is not None else None
out_data = in_data
