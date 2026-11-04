from qdpy.base import registry
from qdpy.phenotype import ScoresDict

from daccadevo.core import evaluate_timeseries, get_standard_metrics

import numpy as np



## Bistable evaluation
@registry.register
def bistable_eval_fn(daccadIndiv, config = None, high_conc = 10.0, low_conc=0.1, stability_length = 50, **kwargs):
	if daccadIndiv.nb_nodes > 1:
		initConc1 = [low_conc for _ in range(daccadIndiv.nb_nodes)]
		initConc2 = [low_conc for _ in range(daccadIndiv.nb_nodes)]
		initConc1[0] = high_conc
		initConc2[1] = high_conc
		y1 = evaluate_timeseries(daccadIndiv, config = config, initConc=initConc1, **kwargs)[-stability_length:,:2]
		y2 = evaluate_timeseries(daccadIndiv, config = config, initConc=initConc2, **kwargs)[-stability_length:,:2]

		stab1 = np.abs(np.average(np.diff(y1[:,0]))/max(np.max(y1[:,0]),1e-5))
		stab2 = np.abs(np.average(np.diff(y2[:,1]))/max(np.max(y2[:,1]),1e-5))

		diff1 = (y1[-1,0]-y1[-1,1])/max(low_conc,y1[-1,0])
		diff2 = (y2[-1,1]-y2[-1,0])/max(low_conc,y2[-1,1])
	else:
		stab1=1.0
		stab2=1.0
		diff1=0.0
		diff2=0.0
    
	stab_eval = (stab1+stab2)/2
	diff_eval = (diff1+diff2)/2
	scores = {"stab": stab_eval, "difference": diff_eval,
				"overall":diff_eval-stab_eval,
				**get_standard_metrics(daccadIndiv)}

	daccadIndiv.scores = ScoresDict(scores)
	daccadIndiv.fitness.weights = (1.0,)
	daccadIndiv.fitness.values = [scores[config['fitness_type']]]
	daccadIndiv.features.values = [scores[x] for x in config["features_list"]]
	return daccadIndiv