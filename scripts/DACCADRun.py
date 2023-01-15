import qdpy
from qdpy.base import *
from qdpy.experiment import QDExperiment
import submitDACCAD
import evolver
from scipy import signal
import numpy as np
from numpy import linalg as LA
from datetime import datetime
import os
from statistics import mean
from ReservoirRun import Reservoir
from jacobian import get_jacobian
from predict_mc import get_predict_mc, get_predict_mc_daccadIndiv, get_predict_mc_eigenvalue
from predict_kr import get_predict_kr_daccadIndiv


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
    k_max = 1 # the maximum delay length

    # memory capacity
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_mc']
                                             ).decode('ascii')
    
    ### TODO: calculate standard error of multiple runs
    mc = 0
    for k in range(1, k_max + 1):
        Reservoir_mc = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
        data = Reservoir_mc.get_data()
        X, Y = Reservoir_mc.run(data)
        mc_k = Reservoir_mc.get_MCk(data, Y)
        mc += mc_k

    # kernel rank
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_kr']
                                             ).decode('ascii')

    Reservoir_kr = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
    data_for_kr = Reservoir_kr.get_data()
    X_kr, Y_kr = Reservoir_kr.run(data_for_kr)
    kernel_rank = Reservoir_kr.get_KR_or_GR(X_kr, "kernel")
    
    # generalization rank
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_gr']
                                             ).decode('ascii')

    Reservoir_gr = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
    data_for_gr = Reservoir_gr.get_data()
    X_gr, Y_gr = Reservoir_gr.run(data_for_gr)
    gene_rank = Reservoir_gr.get_KR_or_GR(X_gr, "gene")

    print("[ {}:size, {}: mc, {}: kr, {}: gr ]".format(nNodes, mc, kernel_rank, gene_rank))
    return [mc], [kernel_rank, gene_rank]

def reservoir_jacobian_eval_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    # produce several sizes of reservoir
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    k_max = 100 # the maximum delay length # 100
    ave_mc = 0
    for _ in range(10):
        # memory capacity
        jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                                configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                                jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                                configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_mc']
                                                ).decode('ascii')

        ### TODO: calculate standard error of multiple runs
        mc = 0
    
        for k in range(1, k_max + 1):
            Reservoir_mc = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
            data = Reservoir_mc.get_data()
            X, Y = Reservoir_mc.run(data)
            mc_k = Reservoir_mc.get_MCk(data, Y)
            mc += mc_k
        ave_mc += mc
    ave_mc = ave_mc / 10 # average of mc

    # nb_templates = len([i for i in myarray[2:6] if i != 0 ])
    stability = mean(daccadIndiv.stabilities) 
    j_matrix = get_jacobian(daccadIndiv, myarray, jikeiretu)
    w, v = LA.eig(j_matrix)
    eigenvalue = np.mean([np.linalg.norm(val) for val in w])

    print("data : {}, {}, {}, {}, {}".format(nNodes, ave_mc, stability, eigenvalue, myarray))
    return [mc], [nNodes, stability]

def reservoir_eval_5_kernel_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    # only produce size 5 of reservoir
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    k = 1

    # kernel rank
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_kr']
                                             ).decode('ascii')

    Reservoir_kr = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
    data_for_kr = Reservoir_kr.get_data()
    X_kr, Y_kr = Reservoir_kr.run(data_for_kr)
    kernel_rank = Reservoir_kr.get_KR_or_GR(X_kr, "kernel")

    stability = mean(daccadIndiv.stabilities)

    nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])

    print("data : {}, {}, {}, {}".format(nTemplates, kernel_rank, stability, myarray))
    return [kernel_rank], [nTemplates, stability]

def reservoir_jacobian_eval_5_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    # only produce size 5 of reservoir
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    k_max = 100 # the maximum delay length # 100
    ave_mc = 0
    for _ in range(5):
        # memory capacity
        jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                                configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                                jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                                configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_mc']
                                                ).decode('ascii')

        ### TODO: calculate standard error of multiple runs
        mc = 0
    
        for k in range(1, k_max + 1):
            Reservoir_mc = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
            data = Reservoir_mc.get_data()
            X, Y = Reservoir_mc.run(data)
            mc_k = Reservoir_mc.get_MCk(data, Y)
            mc += mc_k
        ave_mc += mc
    ave_mc = ave_mc / 5 # average of mc

    stability = mean(daccadIndiv.stabilities) 
    j_matrix = get_jacobian(daccadIndiv, myarray, jikeiretu)
    w, v = LA.eig(j_matrix)
    eigenvalue = np.mean([np.linalg.norm(val) for val in w])

    nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])

    print("data : {}, {}, {}, {}, {}".format(nTemplates, ave_mc, stability, eigenvalue, myarray))
    return [ave_mc], [nTemplates, stability]

def reservoir_jacobian_surrogate_eval_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    k_max = 100 # the maximum delay length # 100

    # memory capacity
    '''
    jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], 
                                             jsonFileName=os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json",
                                             configFile_input = os.path.abspath(os.getcwd()) +"/"+config['daccad']['config_file_input_for_mc']
                                             ).decode('ascii')

    '''
    stability = mean(daccadIndiv.stabilities) 
    # j_matrix = get_jacobian(daccadIndiv, myarray, jikeiretu)
    # w, v = LA.eig(j_matrix)
    # eigenvalue = np.mean([np.linalg.norm(val) for val in w])
    
    nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])
    
    # get the prediction of memory capacity
    # mc_prediction = get_predict_mc_eigenvalue(myarray, eigenvalue)

    mc_prediction = get_predict_mc_daccadIndiv(daccadIndiv)

    # print("data : {}, {}, {}, {}, {}".format(nTemplates, mc_prediction, stability, eigenvalue, myarray))
    print("data : {}, {}, {}, {}".format(nTemplates, mc_prediction, stability, myarray))
    return [mc_prediction], [nTemplates, stability]

def reservoir_surrogate_kernel_eval_fn(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0], npeaks = 1):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)

    k_max = 100 # the maximum delay length # 100

    # kernel rank
    
    stability = mean(daccadIndiv.stabilities) 
    
    nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])

    kr_prediction = get_predict_kr_daccadIndiv(daccadIndiv)

    print("data : {}, {}, {}, {}".format(nTemplates, kr_prediction, stability, myarray))
    return [kr_prediction], [nTemplates, stability]

class DACCADExperiment(QDExperiment):
    def __init__(self, config_filename, **kwargs):
        super().__init__(config_filename, **kwargs)
        if 'eval' in self.config:
            if self.config["eval"] == "reservoir":
                self._eval_fn = reservoir_eval_fn
            elif self.config["eval"] == "reservoir_jacobian":
                self._eval_fn = reservoir_jacobian_eval_fn
            elif self.config["eval"] == "reservoir_jacobian_5":
                self._eval_fn = reservoir_jacobian_eval_5_fn
            elif self.config["eval"] == "reservoir_jacobian_5_with_inhib":
                self._eval_fn = reservoir_jacobian_eval_5_fn
            elif self.config["eval"] == "reservoir_5_kernel":
                self._eval_fn = reservoir_eval_5_kernel_fn
            elif self.config["eval"] == "reservoir_jacobian_surrogate":
                self._eval_fn = reservoir_jacobian_surrogate_eval_fn
            elif self.config["eval"] == "reservoir_surrogate_kernel":
                self._eval_fn = reservoir_surrogate_kernel_eval_fn
            elif self.config["eval"] == "reservoir_jacobian_2step":
                self._eval_fn = reservoir_jacobian_eval_5_fn
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
