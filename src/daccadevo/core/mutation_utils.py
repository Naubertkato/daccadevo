import math
import random

import numpy as np
from qdpy import hdsobol

"""
Convenience functions used for individual generation and mutation.
Inspired by QDpy
"""

def generateUniform(dimension, indBounds, nb):
    """
    Wrapper around the random uniform function of Numpy to generate 
    multiple evaluations in a given range.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values.
    nb: int
        Number of independent generations.

    Returns
    -------
    res: array
        (nb,dimension) array of random values.
    """
    res = []
    for i in range(nb):
        res.append(np.random.uniform(indBounds[0], indBounds[1], dimension))
    return res

def generateSparseUniform(dimension, indBounds, nb, sparsity):
    """
    Wrapper around the random uniform function of Numpy to generate 
    multiple evaluations in a given range. For each independent
    evaluation, a sparcity mask is also generated, setting values
    not selected to 0. Note that the returned data type is not
    sparse on its own.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values.
    nb: int
        Number of independent generations.
    sparsity:
        Target sparcity fraction. For each independent run, a random
        mask is generated using random values between 0 and 1. Values
        below sparsity force the corresponding index to be set to 0
        in the generated array.
    Returns
    -------
    res: array
        (nb,dimension) array of random values.
    """
    res = []
    for i in range(nb):
        base = np.random.uniform(indBounds[0], indBounds[1], dimension)
        mask = np.random.uniform(0., 1., dimension)
        base[mask < sparsity] = 0.
        res.append(base)
    return res


def generateSparseUniformDomain(dimension, indBounds, nb, sparsityDomain):
    """
    Generate multiple independent arrays where values are set to the minimum 
    value of `indBounds`, and randomly replaced to a uniform value in
    `indBounds` until the sum matches a 'sparcity' target.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values. Only the minimum value is used
    nb: int
        Number of independent generations.
    sparsityDomain:
        Target sparcity range. For each independent run, a random sparcity
        value in the range is selected. Values at random position in the array 
        are replaced by a new random uniform value until the total of positive
        values overcomes the sparcity value.
    Returns
    -------
    res: array
        (nb,dimension) array of random values.
    """
    res = []
    for i in range(nb):
        ind = np.full(dimension, indBounds[0])
        sparsity = np.random.randint(sparsityDomain[0], sparsityDomain[1])
        while sum(ind > 0.) < sparsity:
            ind[np.random.randint(len(ind))] = np.random.uniform(indBounds[0], indBounds[1])
        res.append(ind)
    return res


def generateSobol(dimension, indBounds, nb):
    """
    Wrapper around the hdsobol Sobol pseudo-random generator.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values.
    nb: int
        Number of independent generations.

    Returns
    -------
    res: array
        (nb,dimension) array of random values.
    """
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = res * (indBounds[1] - indBounds[0]) + indBounds[0]
    return res

def generateBinarySobol(dimension, indBounds, nb, cutoff = 0.50):
    """
    Wrapper around the hdsobol Sobol pseudo-random generator.
    Values are binarized using a threshold.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values.
    nb: int
        Number of independent generations.
    cutoff: float
        Threshold for binarization.
    Returns
    -------
    res: array
        (nb,dimension) array of random values.
    """
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = np.unique((res > cutoff).astype(int), axis=0)
    return res

def generateSobolConnectionsWithUniformValues(dimension, indBounds, nb, cutoff = 0.50, nbValueSets = 1):
    """
    Wrapper around the hdsobol Sobol pseudo-random generator.
    Values are binarized using a threshold, and used as mask
    for the Numpy random uniform generation. Generation is done
    in batch to avoid issues with the pseudo-random nature of Sobol.

    Parameters
    ----------
    dimension: int
        The dimension of the random array.
    indBounds: pair
        Minimum and maximum values.
    nb: int
        Number of independent generations.
    cutoff: float
        Threshold for binarization.
    nbValueSets: int
        Number of batches for generation.
    Returns
    -------
    res: array
        (nb, dimension) array of random values.
    """
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
    """
    Convenience function to generate a random value on a log 1000 scale.
    Typically used to generate dissociation values.
    """
    while True:
        res = math.exp(0. + random.random() * math.log(1000.)) / 1000.
        if res >= 10. / 1000.:
            return res

def random_log_scale():
    """
    Convenience function to generate a random value on a log 200 scale.
    Typically used to generate concentration values.
    """
    while True:
        res = math.exp(0. + random.random() * math.log(200.)) / 200.
        if res >= 1. / 200.:
            return res
