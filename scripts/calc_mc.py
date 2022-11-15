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


with open("../results/reservoir_jacobian_surrogate/final_20221115054543.p", "rb") as f:
        data = pickle.load(f)

mc_lst = []
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

    print("ave_mc : ", ave_mc)
    print("std_mc : ", std_mc)
    print()
