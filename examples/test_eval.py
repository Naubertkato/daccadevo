from qdpy.base import registry
from daccadevo.DACCADRun import get_standard_metrics
from qdpy.phenotype import ScoresDict

@registry.register
def test_eval_fn(daccadIndiv, config={"fitness_type": "dissociation_avg", "features_list": ["nb_nodes", 'activations_nb']}):
	daccadIndiv.scores = ScoresDict(get_standard_metrics(daccadIndiv))
	daccadIndiv.fitness.weights = (1.0,) 
	daccadIndiv.fitness.values = [daccadIndiv.scores[config['fitness_type']]]
	daccadIndiv.features.values = [daccadIndiv.scores[x] for x in config["features_list"]]
	return daccadIndiv
