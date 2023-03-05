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

def get_gr(file_name, num):
    with open("../results/reservoir_surrogate_gene/final_" + str(file_name) + ".p", "rb") as f:
            data = pickle.load(f)

    gr_lst = []
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

        # generalization rank
        jikeiretu = submitDACCAD.submitPENSystem_input(myarray, nNodes = nNodes, executablePath=config['daccad']['path'],
                                                configFile = os.path.abspath(os.getcwd())+"/" + '../daccadConf.conf', 
                                                jsonFileName=os.path.abspath(os.getcwd())+"/"+"."+"/"+datetime.now().isoformat(timespec='microseconds')+".json",
                                                configFile_input = os.path.abspath(os.getcwd())+"/" + "../config_gr.json"
                                                ).decode('ascii')

        Reservoir_gr = Reservoir(nNodes=nNodes, result=jikeiretu, delay=k)
        data_for_gr = Reservoir_gr.get_data()
        X_gr, Y_gr = Reservoir_gr.run(data_for_gr)
        generalization_rank = Reservoir_gr.get_KR_or_GR(X_gr, "generalization")
        gr_lst.append(generalization_rank)

        print("generalization rank : ", generalization_rank)
        print()

    gr_file_name = "gr_" + str(num) + "_" + str(file_name) + ".txt"
    gr_lst_str = [str(n) for n in gr_lst]
    with open(gr_file_name, mode='w') as f:
        f.write('\n'.join(gr_lst_str))

if __name__ == "__main__":
    file_name_lst = [20230305045929,20230305050203,20230305051139,20230305055625,20230305055758,
    20230305055928,20230305060158,20230305060213,20230305060341,20230305060401,
    20230305063156,20230305063203,20230305063555,20230305063532,20230305070423,
    20230305070512,20230305070545,20230305070923,20230305070919,20230305072730]
    num = 0
    for file_name in file_name_lst:
        get_gr(file_name, num)
        num += 1