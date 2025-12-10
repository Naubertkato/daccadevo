import pytest
import numpy as np
import pandas as pd
from daccadevo.optimization import DaccadBioneatMut
from qdpy.containers import Grid
from qdpy.algorithms.logging import default_algorithm_logger
from daccadevo.optimization import get_bests, get_metric_over_time, default_analysis
import matplotlib.pyplot as plt

@pytest.fixture(scope="module")
def fake_evals():
	rng = np.random.default_rng()
	return rng.random((1000,3))

@pytest.fixture(scope="module")
def fake_evaluation_function(fake_evals):
	def generator():
		for evaluation in fake_evals:
			yield (evaluation[0], ), (evaluation[1], evaluation[2])
	gen = generator()
	def func(individual):
		return next(gen)
	return func

@pytest.fixture(scope="module")
def fake_run(fake_evaluation_function):
	batch_size = 100
	grid = Grid(shape=(25,25), max_items_per_bin=1, fitness_domain=((0., 1.),), features_domain=((0., 1.), (0., 1.)))
	evo = DaccadBioneatMut(grid, 1000, [0.0,200.0], optimisation_task="max", batch_size=batch_size)
	log = default_algorithm_logger
	log.monitor([evo])
	log.config={'main_algorithm_name': "test", "algorithms": {"test": {"batch_size": batch_size}}, 
	    'daccad':{'env_name': "test", 'path':'../daccad', 'config_file': "daccad_configs/short.conf"}}
	evo.optimise(fake_evaluation_function, batch_mode=True)
	return log

def test_get_bests(fake_evals, fake_run):
	algo = fake_run.algorithms[0]
	container = algo.container
	n_bests = 5
	bests = get_bests(container, n=n_bests)
	real_bests = sorted(fake_evals, key=lambda x: x[0], reverse=True)
	for i in range(n_bests):
		assert bests[i].fitness[0] == real_bests[i][0]
		assert bests[i].features[0] == real_bests[i][1]
		assert bests[i].features[1] == real_bests[i][2]
	
def test_metric_over_time(fake_evals, fake_run):
	batch_size = 100
	for metric in ["max", "qd_score"]:
		fig1, ax1 = get_metric_over_time(pd.DataFrame(fake_run._iterations_data), batch_size= batch_size, metric=metric)
		x= ax1.get_lines()[0]._x
		#y= ax1.get_lines()[0]._y
		for i, v in enumerate(x):
			assert v == i*batch_size
	fig2, ax2 = get_metric_over_time(pd.DataFrame(fake_run._iterations_data), metric="ft_min")
	for ax in ax2:
		x= ax.get_lines()[0]._x
		#y= ax.get_lines()[0]._y
		for i, v in enumerate(x):
			assert v == i*batch_size

def test_default_plots(fake_evals, fake_run, monkeypatch, tmp_path):
	fake_run.config['dataDir'] = str(tmp_path)
	dest_dir = tmp_path / fake_run.config['daccad']['env_name']
	dest_dir.mkdir()
	with plt.ion():
		# We only need to check that there's no run error
		default_analysis([fake_run.__get_saved_state__()])
		