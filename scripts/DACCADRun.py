import qdpy
from qdpy.base import *
from qdpy.experiment import QDExperiment
import submitDACCAD
import evolver
from scipy import signal
import numpy as np
from datetime import datetime
import os
from ReservoirRun import Reservoir



## Base oscillator test function
def oscill_eval_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    jikeiretu = submitDACCAD.submitPENSystem(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json").decode('ascii')
    dataResult = [[float(j) for j in i.split(',')[:-1]] for i in jikeiretu.split('\n')[1:-1]]
    y = np.array(dataResult)[:,0]
    
    maxVal = np.max(y)
    peaks, properties = signal.find_peaks(y/maxVal, prominence=0.01)
    res = 0
    feature2 = 0.0
    
    if len(peaks) > npeaks:
        res = 1- np.diff(y[peaks]).mean()/maxVal
        res *= min(len(peaks) / 10, 1)
        res *= properties["prominences"].mean()
        feature2 = y[peaks[-1]]/maxVal
    return [res], [min(len(peaks)/25.0,1.0), feature2]


def reservoir_eval_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    # memory capacity
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input']
                                             ).decode('ascii')

    Reservoir_ = Reservoir(ind=myarray, nNodes=nNodes, result=jikeiretu, inSize=1, outSize=1, delay=1, trainLen=1000, testLen=2000, initLen=200)
    data = Reservoir_.get_data_for_mc()
    X, Y = Reservoir_.run(data)
    mc_k = Reservoir_.get_MCk(data, Y)

    # kernel rank
    data_for_kr = Reservoir_.get_data_for_kr()
    data_for_kr = (np.repeat(data_for_kr, 50)+1) * 50
    X_kr, Y_kr = Reservoir_.run(data_for_kr)
    kernel_rank = Reservoir_.get_KR_or_GR(X_kr)
    
    # generalization rank
    data_for_gr = Reservoir_.get_data_for_gr()
    data_for_gr = (np.repeat(data_for_gr, 50)+1) * 50
    X_gr, Y_gr = Reservoir_.run(data_for_gr)
    gene_rank = Reservoir_.get_KR_or_GR(X_gr)

    return [mc_k], [kernel_rank, gene_rank]

class DACCADExperiment(QDExperiment):
    def __init__(self, config_filename, **kwargs):
        super().__init__(config_filename, **kwargs)
        if 'eval' in self.config:
            if self.config["eval"] == "reservoir":
                self._eval_fn = reservoir_eval_fn
            else:
                factory = Factory()
                self._eval_fn = factory[self.config["eval"]]
        else:
            self._eval_fn = oscill_eval_fn
        
    def reinit(self):
        super().reinit()
        self.env_name = self.config['daccad']['env_name']
        
    def eval_fn(self, ind):
        # submitDACCAD
        return self._eval_fn(ind, config = self.config)




def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    parser.add_argument('-o', '--resultsBaseDir', type=str, default='results/', help = "Path of results files")
    parser.add_argument('-p', '--parallelismType', type=str, default='concurrent', help = "Type of parallelism to use")
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    return parser.parse_args()

def create_base_config(args):
    base_config = {}
    if len(args.resultsBaseDir) > 0:
        base_config['resultsBaseDir'] = args.resultsBaseDir
    return base_config


def create_experiment(args, base_config):
    exp = DACCADExperiment(args.configFilename, parallelism_type =args.parallelismType, seed=args.seed, base_config=base_config)
    print("Using configuration file '%s'. Instance name: '%s'" % (args.configFilename, exp.instance_name))
    return exp

if __name__ == "__main__":
    import traceback
    args = parse_args()
    base_config = create_base_config(args)
    try:
        exp = create_experiment(args, base_config)
        exp.run()
    except Exception as e:
        warnings.warn(f"Run failed: {str(e)}")
        traceback.print_exc()
