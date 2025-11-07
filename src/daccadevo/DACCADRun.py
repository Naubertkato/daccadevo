from qdpy.base import registry
from qdpy.phenotype import ScoresDict
from qdpy.experiment import QDExperiment
import daccadevo.submitDACCAD as sd

import numpy as np
from scipy import signal
import warnings 

def evaluate_timeseries(daccadIndiv, config = None, scales = [1000.0,200.0], default_enzymes = {"pol" : 1.0, "nick" : 1.0, "exo" : 1.0}, **kwargs):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)
    enzymes = daccadIndiv.enzymes if hasattr(daccadIndiv, "enzymes") else default_enzymes
    dataResult = sd.submitPENSystem(myarray, nNodes = nNodes, config = config, enzymes=enzymes, **kwargs)
    return dataResult

def get_standard_metrics(daccadIndiv):
    def _helper(array, base_name):
        values = array[np.nonzero(array)]
        values_dict = {}
        values_dict[base_name+"_nb"] = len(values)
        values_dict[base_name+"_avg"] = np.mean(values) if len(values) > 0 else 0
        values_dict[base_name+"_std"] = np.std(values) if len(values) > 0 else 0
        return values_dict
    metrics = {}
    metrics["dissociation_avg"] = np.mean(daccadIndiv.stabilities)
    metrics["dissociation_std"] = np.std(daccadIndiv.stabilities)
    metrics["nb_nodes"] = daccadIndiv.nb_nodes
    metrics = {**metrics, **_helper(daccadIndiv.activations,"activations")}
    metrics = {**metrics, **_helper(daccadIndiv.inhibitions,"inhibitions")}
    return metrics

## Base oscillator test function
def oscill_eval_fn(daccadIndiv, config = None, npeaks = 1, **kwargs):
    y = evaluate_timeseries(daccadIndiv, config = config, **kwargs)[:,0]
    
    maxVal = np.max(y)
    peaks, properties = signal.find_peaks(y/maxVal, prominence=0.01)
    res = 0
    feature2 = 0.0
    period = 0.0
    std = 0.0
    
    if len(peaks) > npeaks:
        res = 1- np.diff(y[peaks]).mean()/maxVal
        res *= min(len(peaks) / 10, 1)
        res *= properties["prominences"].mean()
        feature2 = y[peaks[-1]]/maxVal
        peak_dist = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
        # Food for thoughts: period cannot realistically reach 1 
        # (would put a peak at 0 and one at the end). Using period wastes
        # about half the container space
        period = np.average(peak_dist)/len(y) 
        if len(peak_dist) > 1:
            std = np.std(peak_dist)/(0.6*len(y)) # Normalized

    scores = {"oscillations": res, "peaksNumber": min(len(peaks)/25.0,1.0), 
              "peaksLastValue": feature2, "averagePeriod": period, 
              "periodStd": std, "valueStd": np.std(y)/maxVal, 
              **get_standard_metrics(daccadIndiv)}

    # add the actual normalized values of the system
    if "use_timeseries_points" in config and int(config["use_timeseries_points"]) > 0:
        offset = int(config["timeseries_offset"]) if "timeseries_offset" in config else 0
        for i in range(int(config["use_evals"])):
            scores[f"eval{i}"] = y[i+offset]/maxVal

    daccadIndiv.scores = ScoresDict(scores)
    daccadIndiv.fitness.weights = (1.0,) 
    daccadIndiv.fitness.values = [scores[config['fitness_type']]]
    daccadIndiv.features.values = [scores[x] for x in config["features_list"]]
    return daccadIndiv

class DACCADExperiment(QDExperiment):
    def __init__(self, config_filename, **kwargs):
        super().__init__(config_filename, **kwargs)
        if 'eval_fn' in self.config:
            self._eval_fn = registry[self.config["eval_fn"]]          
        else:
            self._eval_fn = oscill_eval_fn
        
    def reinit(self):
        super().reinit()
        self.env_name = self.config['daccad']['env_name']
        
    def eval_fn(self, ind):
        return self._eval_fn(ind, config = self.config)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configFilename', type=str, default='configs/test.yaml', help = "Path of configuration file")
    parser.add_argument('-e', '--evaluation', type=str, default=None, help = "Path to the python file providing the implementation of the evaluation function")
    parser.add_argument('-o', '--resultsBaseDir', type=str, default='results/', help = "Path of results files")
    parser.add_argument('-p', '--parallelismType', type=str, default='concurrent', help = "Type of parallelism to use")
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-r','--repeats', type=int, default=1, help="Number of repeats for evaluations")
    return parser.parse_args()

def create_base_config(args):
    base_config = {}
    if len(args.resultsBaseDir) > 0:
        base_config['resultsBaseDir'] = args.resultsBaseDir
    return base_config


def create_experiment(args, base_config):
    exp = DACCADExperiment(args.configFilename, parallelism_type =args.parallelismType, seed=args.seed, base_config=base_config)
    print("INFO: Using configuration file '%s'. Instance name: '%s'" % (args.configFilename, exp.instance_name))
    return exp

if __name__ == "__main__":
    import traceback
    args = parse_args()
    base_config = create_base_config(args)
    if args.evaluation is not None:
        from pathlib import Path
        import importlib.util
        import sys
        p = Path(args.evaluation)
        name = p.stem
        module_name = ".".join(p.parent.parts)+"."+name
        spec = importlib.util.spec_from_file_location(module_name, p)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    for _ in range(args.repeats):
        try:
            exp = create_experiment(args, base_config)
            exp.run()
        except Exception as e:
            warnings.warn(f"Run failed: {str(e)}")
            traceback.print_exc()
