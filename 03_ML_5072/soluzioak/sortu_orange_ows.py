import base64
import pickle
import orangecanvas.scheme.readwrite as rw
from pathlib import Path
from orangewidget.utils.filedialogs import RecentPath

ows_content = """<?xml version='1.0' encoding='utf-8'?>
<scheme version="2.0" title="Bihotzeko Gaixotasunen Sailkapena - 5072 ML" description="Orange Data Mining lan-fluxua: Heart Disease datu-multzoa, aurreprozesamendua, ereduak (Logistic Regression, Random Forest, Decision Tree, k-NN), 10-Fold Cross-Validation ebaluazioa, Confusion Matrix, ROC analisia eta Tree Viewer.">
	<nodes>
		<node id="0" name="File" qualified_name="Orange.widgets.data.owfile.OWFile" project_name="Orange3" version="" title="File (Heart Disease)" position="(80.0, 220.0)" />
		<node id="1" name="Data Table" qualified_name="Orange.widgets.data.owtable.OWTable" project_name="Orange3" version="" title="Data Table" position="(260.0, 90.0)" />
		<node id="2" name="Preprocess" qualified_name="Orange.widgets.data.owpreprocess.OWPreprocess" project_name="Orange3" version="" title="Preprocess" position="(260.0, 220.0)" />
		<node id="3" name="Logistic Regression" qualified_name="Orange.widgets.model.owlogisticregression.OWLogisticRegression" project_name="Orange3" version="" title="Logistic Regression" position="(450.0, 140.0)" />
		<node id="4" name="Random Forest" qualified_name="Orange.widgets.model.owrandomforest.OWRandomForest" project_name="Orange3" version="" title="Random Forest" position="(450.0, 230.0)" />
		<node id="5" name="Tree" qualified_name="Orange.widgets.model.owtree.OWTreeLearner" project_name="Orange3" version="" title="Decision Tree" position="(450.0, 320.0)" />
		<node id="6" name="k-NN" qualified_name="Orange.widgets.model.owknn.OWKNNLearner" project_name="Orange3" version="" title="k-NN (k=5)" position="(450.0, 410.0)" />
		<node id="7" name="Test and Score" qualified_name="Orange.widgets.evaluate.owtestandscore.OWTestAndScore" project_name="Orange3" version="" title="Test &amp; Score" position="(670.0, 260.0)" />
		<node id="8" name="Confusion Matrix" qualified_name="Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix" project_name="Orange3" version="" title="Confusion Matrix" position="(870.0, 190.0)" />
		<node id="9" name="ROC Analysis" qualified_name="Orange.widgets.evaluate.owrocanalysis.OWROCAnalysis" project_name="Orange3" version="" title="ROC Analysis" position="(870.0, 320.0)" />
		<node id="10" name="Tree Viewer" qualified_name="Orange.widgets.visualize.owtreeviewer.OWTreeGraph" project_name="Orange3" version="" title="Tree Viewer" position="(670.0, 430.0)" />
	</nodes>
	<links>
		<link id="0" source_node_id="0" sink_node_id="1" source_channel="Data" sink_channel="Data" enabled="true" source_channel_id="data" sink_channel_id="data" />
		<link id="1" source_node_id="0" sink_node_id="2" source_channel="Data" sink_channel="Data" enabled="true" source_channel_id="data" sink_channel_id="data" />
		<link id="2" source_node_id="0" sink_node_id="7" source_channel="Data" sink_channel="Data" enabled="true" source_channel_id="data" sink_channel_id="train_data" />
		<link id="3" source_node_id="3" sink_node_id="7" source_channel="Learner" sink_channel="Learner" enabled="true" source_channel_id="learner" sink_channel_id="learner" />
		<link id="4" source_node_id="4" sink_node_id="7" source_channel="Learner" sink_channel="Learner" enabled="true" source_channel_id="learner" sink_channel_id="learner" />
		<link id="5" source_node_id="5" sink_node_id="7" source_channel="Learner" sink_channel="Learner" enabled="true" source_channel_id="learner" sink_channel_id="learner" />
		<link id="6" source_node_id="6" sink_node_id="7" source_channel="Learner" sink_channel="Learner" enabled="true" source_channel_id="learner" sink_channel_id="learner" />
		<link id="7" source_node_id="7" sink_node_id="8" source_channel="Evaluation Results" sink_channel="Evaluation Results" enabled="true" source_channel_id="evaluations_results" sink_channel_id="evaluation_results" />
		<link id="8" source_node_id="7" sink_node_id="9" source_channel="Evaluation Results" sink_channel="Evaluation Results" enabled="true" source_channel_id="evaluations_results" sink_channel_id="evaluation_results" />
		<link id="9" source_node_id="2" sink_node_id="5" source_channel="Preprocessed Data" sink_channel="Data" enabled="true" source_channel_id="preprocessed_data" sink_channel_id="data" />
		<link id="10" source_node_id="5" sink_node_id="10" source_channel="Model" sink_channel="Tree" enabled="true" source_channel_id="model" sink_channel_id="tree" />
		<link id="11" source_node_id="2" sink_node_id="7" source_channel="Preprocessor" sink_channel="Preprocessor" enabled="true" source_channel_id="preprocessor" sink_channel_id="preprocessor" />
	</links>
	<annotations>
		<text id="0" type="text/plain" rect="(40.0, 140.0, 180.0, 60.0)" font-family="Helvetica" font-size="12">1. Bihotzeko gaixotasunen datu-multzoa (heart_disease.tab)</text>
		<text id="1" type="text/plain" rect="(240.0, 300.0, 160.0, 50.0)" font-family="Helvetica" font-size="12">2. Missing values inputazioa eta normalizazioa</text>
		<text id="2" type="text/plain" rect="(430.0, 70.0, 180.0, 50.0)" font-family="Helvetica" font-size="12">3. Sailkapen ereduak: LR, RF, Tree, k-NN</text>
		<text id="3" type="text/plain" rect="(630.0, 190.0, 170.0, 50.0)" font-family="Helvetica" font-size="12">4. 10-Fold Stratified Cross-Validation</text>
		<text id="4" type="text/plain" rect="(830.0, 120.0, 180.0, 50.0)" font-family="Helvetica" font-size="12">5. Ebaluazioa: Confusion Matrix eta ROC</text>
	</annotations>
	<thumbnail />
	<node_properties>
		<properties node_id="0" format="pickle">{file_settings}</properties>
		<properties node_id="2" format="literal">{'storedsettings': {'name': '', 'preprocessors': [('orange.preprocess.impute', {'method': 2}), ('orange.preprocess.scale', {'method': 2})]}, 'autocommit': True, '__version__': 2}</properties>
		<properties node_id="3" format="literal">{'C_index': 61, 'auto_apply': True, 'class_weight': False, 'controlAreaVisible': True, 'learner_name': 'Logistic Regression', 'penalty_type': 1, 'savedWidgetGeometry': None, '__version__': 2}</properties>
		<properties node_id="4" format="literal">{'auto_apply': True, 'class_weight': False, 'controlAreaVisible': True, 'index_output': 0, 'learner_name': 'Random Forest', 'max_depth': 5, 'max_features': 5, 'min_samples_split': 5, 'n_estimators': 100, 'savedWidgetGeometry': None, 'use_max_depth': True, 'use_max_features': False, 'use_min_samples_split': True, 'use_random_state': True, 'random_state': 42, '__version__': 1}</properties>
		<properties node_id="5" format="literal">{'auto_apply': True, 'binarize': False, 'controlAreaVisible': True, 'filter_nodes': True, 'limit_depth': True, 'limit_min_leaf': True, 'limit_min_parent': True, 'max_depth': 5, 'min_internal': 5, 'min_leaf': 2, 'savedWidgetGeometry': None, '__version__': 1}</properties>
		<properties node_id="6" format="literal">{'auto_apply': True, 'controlAreaVisible': True, 'metrics_idx': 0, 'n_neighbors': 5, 'weights_idx': 0, '__version__': 1}</properties>
		<properties node_id="7" format="literal">{'controlAreaVisible': True, 'resampling': 0, 'n_folds': 3, 'cv_stratified': True, '__version__': 1}</properties>
	</node_properties>
</scheme>
"""

file_settings = base64.b64encode(pickle.dumps({
    "controlAreaVisible": True,
    "recent_paths": [RecentPath("", "sample-datasets", "heart_disease.tab")],
    "recent_urls": [], "savedWidgetGeometry": None, "sheet_names": {},
    "source": 0, "url": "", "domain_editor": {}, "__version__": 1,
    "context_settings": [],
}, protocol=4)).decode("ascii")
ows_content = ows_content.replace("{file_settings}", file_settings)

out_path = Path(__file__).with_name("Orange_Bihotza_Ereduak.ows")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(ows_content)

print(f"Workflow saved to: {out_path}")

# Validate with parse_ows_stream
with open(out_path, "rb") as f:
    parsed = rw.parse_ows_stream(f)
    print("Validation successful!")
    print(f"Title: {parsed.title}")
    print(f"Nodes ({len(parsed.nodes)}): {[n.title for n in parsed.nodes]}")
    print(f"Links ({len(parsed.links)}): {[(l.source_node_id, l.sink_node_id) for l in parsed.links]}")
