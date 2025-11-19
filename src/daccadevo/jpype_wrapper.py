import os
import subprocess
from subprocess import check_output, CalledProcessError
import warnings
import yaml
from timeit import default_timer as timer
import math
from .submitDACCAD import findAllInhibitorsAndConcs

import daccadevo.daccad as daccad
daccad.startJVM()
import model.Constants
import model.OligoGraph
import model.OligoSystem
import model.chemicals.SequenceVertex
import utils.GraphUtils

import numpy as np

# new 
def generateNode(name, stability, activator, graph, species_dict):
    s = graph.getVertexFactory().create()
    if not(activator):
        s.setInhib(True)
    graph.addSpecies(s, stability)
    species_dict[name] = s
    s.setInitialConcentration(0.1)
    return s

# new
def generateConnection(innov, concentration, fromNode, toNode, graph, species_dict):
    edge = graph.getEdgeFactory().createEdge(species_dict[fromNode], species_dict[toNode])
    graph.addActivation(edge, species_dict[fromNode], species_dict[toNode], concentration)
    return edge

# new
def generateAllNodes(array, inhibitingSequences, graph, species_dict, nNodes = 5):
    for i in range(nNodes):
        generateNode(i,array[i], True, graph, species_dict)
    for val in inhibitingSequences:
        _, stab = inhibitingSequences[val]
        generateNode(val,stab, False, graph, species_dict)
    return graph

# new
def generateAllConnections(array,inhibitions,graph, species_dict, nNodes = 5):
    innovation = 0
    offset = nNodes
    for fromNode in range(nNodes):
        for toNode in range(nNodes):
            index = offset + nNodes * fromNode + toNode
            if array[index] > 0.0:
                generateConnection(innovation, array[index], fromNode, toNode, graph, species_dict)
                innovation += 1
    for val in inhibitions:
        concs, _ = inhibitions[val]
        for fromNode, concentration in concs:
            edge = generateConnection(innovation, concentration, int(fromNode), val, graph, species_dict)
            graph.addInhibition(edge, species_dict[val])
            innovation += 1
    return graph


def generateEnzymeParameters(graph, pol = 1.0, nick = 1.0, exo = 1.0):
    graph.polConc = pol
    graph.nickConc = nickConc
    graph.exoConc = exoConc
    return graph


# new
def generateFull(array, graph, species_dict, nNodes = 5):
    itc = findAllInhibitorsAndConcs(array,nNodes = nNodes)
    generateAllNodes(array, itc, graph, species_dict, nNodes = nNodes)
    generateAllConnections(array, itc, graph, species_dict, nNodes = nNodes)
    return graph

# new
def submitPENSystem(array, nNodes = 5, config_file = 'daccad_configs/short.conf'):
    g = utils.GraphUtils.initGraph()
    species_dict = {}
    g = generateFull(array, g, species_dict, nNodes)
    # os = model.OligoSystem(g, utils.PredatorPreyTemplateFactory(g)) OSの違いに注意する
    os =  model.OligoSystem(g)
    # TODO: read config
    with open(config_file,"r") as f:
        for line in f.lines():
            if not line.strip().startswith("#"):
                params = line.split()
                model.Constants.readConfigFromString(jpype.JClass(model.Constants),params[0].strip(), params[1].strip());
    #model.Constants.numberOfPoints = 3000
    timeSeries = os.calculateTimeSeries(None) 
    timeSeries = np.array(timeSeries).T
    return timeSeries


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
