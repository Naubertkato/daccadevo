import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import re
import statistics
import pickle
import csv
import os 
import sys
from datetime import datetime

from individual import DaccadIndividual

from ReservoirRun import Reservoir
import submitDACCAD

def get_kr(file_name, num):
    with open("../results/reservoir_surrogate_kernel/final_" + str(file_name) + ".p", "rb") as f:
            data = pickle.load(f)

    kr_lst = []
    config = {'daccad': {'path':'../../daccad'}}
    scales = [1000.0,200.0]
    npeaks = 1
    ave_mc = 0
    len_ind = len(data["container"])

    for i, daccadIndiv in enumerate(data["container"]):
        print("***** " + str(i+1) + "/" + str(len_ind) + " *****")
        print(daccadIndiv)
        nNodes = daccadIndiv.nb_nodes
        scaling = [scales[0]]*nNodes+[scales[1]]*(nNodes*nNodes*(nNodes+1))
        myarray = np.array(scaling)*np.array(daccadIndiv)
        nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])
        print("nTemplates : ", nTemplates)
        
        k = 1

        # kernel rank
        jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                                configFile = os.path.abspath(os.getcwd())+"/" + '../daccadConf.conf', 
                                                jsonFileName=os.path.abspath(os.getcwd())+"/"+"."+"/"+datetime.now().isoformat(timespec='microseconds')+".json",
                                                configFile_input = os.path.abspath(os.getcwd())+"/" + "../config_kr.json"
                                                ).decode('ascii')

        Reservoir_kr = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
        data_for_kr = Reservoir_kr.get_data()
        X_kr, Y_kr = Reservoir_kr.run(data_for_kr)
        kernel_rank = Reservoir_kr.get_KR_or_GR(X_kr, "kernel")
        kr_lst.append(kernel_rank)

        print("kernel rank : ", kernel_rank)
        print()

    kr_file_name = "kr_" + str(num) + "_" + str(file_name) + ".txt"
    kr_lst_str = [str(n) for n in kr_lst]
    with open(kr_file_name, mode='w') as f:
        f.write('\n'.join(kr_lst_str))

if __name__ == "__main__":
    file_name_lst = [20230117144059, 20230117144914, 20230117145401, 20230117145751, 
    20230117150120, 20230117150510, 20230118033602, 20230118034123, 20230118043917, 20230118051429, 20230118063432, 20230118134707, 
    20230118140753, 20230118144557, 20230118145540, 20230118150419, 20230118151036]
    num = 0
    for file_name in file_name_lst:
        get_kr(file_name, num)
        num += 1