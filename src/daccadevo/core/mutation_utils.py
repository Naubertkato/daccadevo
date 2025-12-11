import math
import random

import numpy as np
from qdpy import hdsobol

"""
Convenience functions used for individual generation and mutation.
Inspired by QDpy
"""

def generateUniform(dimension, indBounds, nb):
    res = []
    for i in range(nb):
        res.append(np.random.uniform(indBounds[0], indBounds[1], dimension))
    return res

def generateSparseUniform(dimension, indBounds, nb, sparsity):
    res = []
    for i in range(nb):
        base = np.random.uniform(indBounds[0], indBounds[1], dimension)
        mask = np.random.uniform(0., 1., dimension)
        base[mask < sparsity] = 0.
        res.append(base)
    return res


def generateSparseUniformDomain(dimension, indBounds, nb, sparsityDomain):
    res = []
    for i in range(nb):
        ind = np.full(dimension, indBounds[0])
        sparsity = np.random.randint(sparsityDomain[0], sparsityDomain[1])
        while sum(ind > 0.) < sparsity:
            ind[np.random.randint(len(ind))] = np.random.uniform(indBounds[0], indBounds[1])
        res.append(ind)
    return res


def generateSobol(dimension, indBounds, nb):
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = res * (indBounds[1] - indBounds[0]) + indBounds[0]
    return res

def generateBinarySobol(dimension, indBounds, nb, cutoff = 0.50):
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = np.unique((res > cutoff).astype(int), axis=0)
    return res

def generateSobolConnectionsWithUniformValues(dimension, indBounds, nb, cutoff = 0.50, nbValueSets = 1):
    base = generateBinarySobol(dimension, (0., 1.), nb // nbValueSets, cutoff)
    mask = base >= 0.5
    res = []
    nbMasked = len(base[mask])
    for i in range(nbValueSets):
        m = base.astype(float)
        m[mask] = np.random.uniform(indBounds[0], indBounds[1], nbMasked)
        res.append(m)
    return np.concatenate(res)

def random_log_scale_1000():
    while True:
        res = math.exp(0. + random.random() * math.log(1000.)) / 1000.
        if res >= 10. / 1000.:
            return res

def random_log_scale():
    while True:
        res = math.exp(0. + random.random() * math.log(200.)) / 200.
        if res >= 1. / 200.:
            return res
