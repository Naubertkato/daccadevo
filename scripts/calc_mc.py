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

def get_mc(file_name, num):
    with open("../results/reservoir_jacobian_surrogate/final_" + str(file_name) + ".p", "rb") as f:
            data = pickle.load(f)

    ave_mc_lst = []
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
        mc_lst = np.zeros(10)

        for i in range(10):
            # memory capacity
            jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                                            configFile = os.path.abspath(os.getcwd())+"/" + '../daccadConf.conf', 
                                                            jsonFileName=os.path.abspath(os.getcwd())+"/"+"."+"/"+datetime.now().isoformat(timespec='microseconds')+".json",
                                                            configFile_input = os.path.abspath(os.getcwd())+"/" + "../config_mc.json"
                                                            ).decode('ascii')

            mc = 0
            k_max = 100 # the maximum delay length # 100
            for k in range(1, k_max + 1):
                Reservoir_mc = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
                data = Reservoir_mc.get_data()
                X, Y = Reservoir_mc.run(data)
                mc_k = Reservoir_mc.get_MCk(data, Y)
                mc += mc_k
            mc_lst[i] = mc

        ave_mc = np.mean(mc_lst)
        std_mc = np.std(mc_lst)
        ave_mc_lst.append(ave_mc)
        print("ave_mc : ", ave_mc)
        print("std_mc : ", std_mc)
        print()

    mc_file_name = "mc_" + str(num) + "_" + str(file_name) + ".txt"
    ave_mc_lst_str = [str(n) for n in ave_mc_lst]
    with open(mc_file_name, mode='w') as f:
        f.write('\n'.join(ave_mc_lst_str))

if __name__ == "__main__":
    file_name_lst = [20221202065807, 20221202070049, 20221202070444, 20221202074639, 20221202074809, 
    20221202075003, 20221202075130, 20221202075303, 20221202080329, 20221202080502, 
    20221202080700, 20221202080839, 20221202081010, 20221202081155, 20221202081341]
    num = 46
    for file_name in file_name_lst:
        get_mc(file_name, num)
        num += 1