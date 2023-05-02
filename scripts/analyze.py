import qdpy
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import submitDACCAD


def get_data(path):
    res = None
    with open(path, "rb") as f:
        res = pickle.load(f)
    return res

def get_bests(container, n=5):
    return sorted(container, key= lambda indiv: indiv.fitness, reverse=True)[:n]
    
def evaluate_timeseries(daccadIndiv, config = {'daccad': {'path':'../../daccad'}}, scales = [1000.0,200.0]):
    nNodes = daccadIndiv.nb_nodes
    scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
    myarray = np.array(scaling)*np.array(daccadIndiv)
    tmpfilepath = os.path.abspath(os.getcwd())+"/"+config['dataDir']+"/"+config['daccad']['env_name']+datetime.now().isoformat(timespec='microseconds')+".json"
    jikeiretu = submitDACCAD.submitPENSystem(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                             configFile = os.path.abspath(os.getcwd())+"/"+config['daccad']['config_file'], jsonFileName=tmpfilepath).decode('ascii')
    dataResult = [[float(j) for j in i.split(',')[:-1]] for i in jikeiretu.split('\n')[1:-1]]
    y = np.array(dataResult)[:,0]
        
    if "keepTemporaryFiles" not in config or not config['keepTemporaryFiles']:
        os.remove(tmpfilepath)
    return y

if __name__ == "__main__":
    import sys
    dt = get_data(sys.argv[1])
    indiv_list = get_bests(dt["container"], n=10)
    config = dt["config"]
    config["keepTemporaryFiles"] = False
    all_timeseries = []
    for i in indiv_list:
        print(i.fitness)
        y = evaluate_timeseries(i, config = config)
        all_timeseries.append(y)
    plt.plot(np.array(all_timeseries).T)
    plt.show()
