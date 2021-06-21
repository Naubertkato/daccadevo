
import os
import sys
import submitDACCAD
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import nnls
import scipy.linalg
from numpy.linalg import svd, matrix_rank

class Reservoir:
    def __init__(self, ind, nNodes, result, inSize=1, outSize=1, delay=1, trainLen=1000, testLen=2000, initLen=200) -> None:
        """
        Load the data.
        Args:
            ind: array
                reaction network
            nNodes: integer
                the number of nodes
            inSize: integer
                input size
            outSize: integer
                output size
            delay: integer
        """
        self.ind = ind
        self.nNodes = nNodes
        self.result=result
        self.inSize = inSize
        self.outSize = outSize
        self.delay = delay
        self.trainLen = trainLen
        self.testLen = testLen
        self.initLen = initLen

    def get_data_for_mc(self):
        """
        Prepare the input data for memory capacity.
        Return:
            data: numpy.array
                input data for calculating memory capacity (= target data)
        """
        input_arr = [float(line) for line in self.result.split('\n')[2:3002]]
        input_f = pd.DataFrame(input_arr, columns=['target'])
        data = input_f['target'].values
        
        return data
    
    def get_data_for_kr(self):
        """
        Generate the input data for kernel rank.
        For the kernel rank, one chooses input streams that differ
        strongly with respect to the target function (e.g., streams that belong to
        different target classes).
        Intuitively, this rank measures how well the reservoir represents
        different input streams.
        Args:
        Return:
            ui: numpy.array
                input data for calculating kernel rank (= target data)
        """
        bestDist = 0
        for i in range(1000):
            ui = (20 * np.random.rand(self.trainLen + self.testLen + self.initLen) - 10) / 10
            dist = np.std(ui)
            if dist > bestDist:
                bestDist = dist
                bestUi = ui
        ui = bestUi

        #print("ui_kr: ", ui)
        return ui
    
    def get_data_for_gr(self):
        """
        Generate the input data for generalization rank.
        For the generalization rank, one chooses similar input streams.
        Intuitively, the generalization rank measures how strongly the
        reservoir state at time t is sensitive to inputs old time steps.
        Args:
        Return:
            ui: numpy.array
                input data for calculating generalization rank (= target data)
        """

        ui_1 = (10*np.random.rand())/10
        ui = np.tile(ui_1,(self.trainLen + self.testLen + self.initLen,))+(1*np.random.rand(self.trainLen+self.testLen+self.initLen)-0.5)/10
        ui[0] = ui_1
        #print("ui_gr: ", ui)
        return ui

    def run(self, data):
        """
        Implementing reservoir computing.
        Args:
            data: numpy.array
                input data (= target data)
                
        """
        arr = [[float(a) for a in line.split(',')] for line in self.result.split('\n')[3003:-1]]
        f = pd.DataFrame(arr)

        # Non-negative constraint
        # A: X(t) b: Y~(t) target function
        # x : W out
        s = f.iloc[:, 0:2]
        X = s.values.T
        #print("X: ", X[0], X[1])

            # train the output
        Y_target = data[self.initLen-self.delay:self.trainLen-self.delay]
        (W_out, rnorm) = nnls(X.T[self.initLen:self.trainLen, :], Y_target)

        #print("W_out = ", W_out)

        Y = np.zeros((self.outSize, self.testLen))
        for t in range(self.testLen):
            y = np.dot(W_out, X[:, self.trainLen+t])
            Y[:,t] = y
        #print("Y : ", Y)

        return X, Y

    def get_MCk(self, data, Y, mcLen=1000):
        """
        Calculate memory capacity when the delay is equal to k.(MC_k)
        Args:
            data: numpy.array
                The target output data
                
            Y: numpy.array
                The predicted output data
                
            mcLen: integer
                the range for calculating MC_k
        Return:
            mc_k: float
                memory capacity with delay = k
        """
        mc_k = np.corrcoef(data[self.trainLen-self.delay:self.trainLen+mcLen-self.delay], Y[0, :mcLen])[0][1] ** 2
        # print("mc_k = ", mc_k)

        return mc_k
    
    def get_KR_or_GR(self, X):
        """
        Calculate kernel rank and generalization rank.
        Args:
            X: numpy.array
                the states of a reservoir
        Return:
            KGrank: integer
                kernel rank or generalization rank            
        """
        u, s, vh = svd(X)
        tmp_rank_sum = 0
        full_rank_sum = 0
        e_rank = 0
        for i in range(len(s)):
            full_rank_sum += s[i]
            while tmp_rank_sum < full_rank_sum * 0.99:
                tmp_rank_sum += s[e_rank]
                e_rank += 1
        KGrank = e_rank - 1
        # print("KGrank = ", KGrank)
        return KGrank
