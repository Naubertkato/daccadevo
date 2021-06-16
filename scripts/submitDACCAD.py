#First we need to turn an array into a JSON

import os
import subprocess
from subprocess import check_output, CalledProcessError
import warnings
import yaml
from timeit import default_timer as timer
import math

#Format array: [ all stabilities (nNodes), all activations from i to j (nNodes * nNodes), all inhibitions created by i to the template j to k (nNodes * nNodes * nNodes)]

def findAllInhibitions(array, nNodes = 5):
    beginInhibitionTemplates = nNodes * (nNodes+1)
    inhibitions = {}
    for i in range(nNodes): #For each possible activator
        index = beginInhibitionTemplates + i * nNodes * nNodes
        for fromId in range(nNodes):
            for toId in range(nNodes):
                if array[index + fromId*nNodes + toId] > 0.0:
                    if not (fromId,toId) in inhibitions:
                        inhibitions[(fromId,toId)] = []
                    inhibitions[(fromId,toId)].append(i)
    return inhibitions

#Kept for testing purpose; correct behavior
def findAllInhibitorsAndConcsLegacy(array,nNodes = 5):
    beginInhibitionTemplates = nNodes * (nNodes+1)
    inhibitingTemplatesConcs = {}
    for i in range(nNodes): #For each possible activator
        index = beginInhibitionTemplates + i * nNodes * nNodes
        for fromId in range(nNodes):
            for toId in range(nNodes):
                if array[index + fromId*nNodes + toId] > 0.0:
                    name = 'I'+str(fromId)+'T'+str(toId)
                    if not name in inhibitingTemplatesConcs:
                        inhibitingTemplatesConcs[name] = []
                    inhibitingTemplatesConcs[name].append((str(i),array[index + fromId*nNodes + toId]))
    return inhibitingTemplatesConcs

#New version, relies on findAllInhibitions (i.e. more modular).
def findAllInhibitorsAndConcs(array,nNodes = 5):
    allInhibitions = findAllInhibitions(array,nNodes = nNodes)
    beginInhibitionTemplates = nNodes * (nNodes+1)
    inhibitingTemplatesConcs = {}
    for fromId,toId in allInhibitions:
        name = 'I'+str(fromId)+'T'+str(toId)
        indexes = allInhibitions[(fromId,toId)]
        base = fromId*nNodes + toId + beginInhibitionTemplates
        stability =  1 / 100 * math.exp((math.log(array[fromId]) + math.log(array[toId])) / 2)
        inhibitingTemplatesConcs[name] = [(str(i), array[base+i*nNodes*nNodes]) for i in indexes],stability
    return inhibitingTemplatesConcs

def invalidInhibitions(array, nNodes = 5):
    inhibTemps = findAllInhibitions(array,nNodes = nNodes)
    beginTemplates = nNodes
    res = []
    for fromId,toId in inhibTemps:
        if array[beginTemplates+fromId*nNodes + toId] <= 0.0:
            res.append(((fromId,toId),inhibTemps[(fromId,toId)]))
    return res

def isValid(array, nNodes = 5):
    return not invalidInhibitions(array, nNodes = nNodes)


def generateNode(name, stability, activator, tab = 1, tabChar = "  "):
    json = (tabChar*tab)+"{\n"
    json += (tabChar*(tab+1))+'"name": "'+str(name)+'",\n'
    json += (tabChar*(tab+1))+'"parameter": '+str(stability)+',\n'
    json += (tabChar*(tab+1))+'"initialConcentration": '+('1.0' if activator else '0.0')+',\n'
    json += (tabChar*(tab+1))+'"type": '+('1' if activator else '2')+',\n'
    json += (tabChar*(tab+1))+'"protectedSequence": false,\n'
    json += (tabChar*(tab+1))+'"DNAString": "",\n'
    json += (tabChar*(tab+1))+'"reporter": false,\n'
    json += (tabChar*(tab+1))+'"hasPseudoTemplate": false,\n'
    json += (tabChar*(tab+1))+'"pseudoTemplateConcentration": 0.0\n'
    json += (tabChar*tab)+"}"
    return json

def generateConnection(innov, concentration, fromNode, toNode, tab = 1, tabChar = "  "):
    json = (tabChar*tab)+"{\n"
    json += (tabChar*(tab+1))+'"innovation": '+str(innov)+',\n'
    json += (tabChar*(tab+1))+'"enabled": true,\n'
    json += (tabChar*(tab+1))+'"parameter": '+str(concentration)+',\n'
    json += (tabChar*(tab+1))+'"from": "'+str(fromNode)+'",\n'
    json += (tabChar*(tab+1))+'"to": "'+str(toNode)+'"\n'
    json += (tabChar*tab)+"}"
    return json

def generateAllNodes(array, inhibitingSequences, nNodes = 5, tab = 1, tabChar = "  "):
    json = (tabChar*tab)+'"nodes": [\n'
    for i in range(nNodes):
        json += generateNode(i,array[i], True, tab = tab + 1, tabChar = tabChar)+',\n'
    for val in inhibitingSequences:
        _, stab = inhibitingSequences[val]
        json += generateNode(val,stab, False, tab = tab + 1, tabChar = tabChar)+',\n'
    json = json[:-2]+"\n"
    json += (tabChar*tab)+']'
    return json

def generateAllConnections(array,inhibitions,nNodes = 5, tab = 1, tabChar = "  "):
    innovation = 0
    offset = nNodes
    json = (tabChar*tab)+'"connections": [\n'
    for fromNode in range(nNodes):
        for toNode in range(nNodes):
            index = offset + nNodes * fromNode + toNode
            if array[index] > 0.0:
                json += generateConnection(innovation, array[index], fromNode, toNode, tab = tab+1, tabChar = tabChar)+',\n'
                innovation += 1
    for val in inhibitions:
        concs, _ = inhibitions[val]
        for fromNode, concentration in concs:
            json += generateConnection(innovation, concentration, fromNode, val, tab = tab+1, tabChar = tabChar)+',\n'
            innovation += 1
    json = json[:-2]+"\n"
    json += (tabChar*tab)+']'
    return json

def generateLegacyParameters(pol = 10.0, nick = 10.0, exo = 10.0, tab = 1, tabChar = "  "):
    json = (tabChar*tab)+'"parameters": {\n'
    json += (tabChar*(tab+1))+'"nick": '+str(nick)+',\n'
    json += (tabChar*(tab+1))+'"pol": '+str(pol)+',\n'
    json += (tabChar*(tab+1))+'"exo": '+str(exo)+'\n'
    json += (tabChar*tab)+"}"
    return json

def generateFullJson(array, nNodes = 5, tab = 0, tabChar = "  "):
    json = "{\n"
    itc = findAllInhibitorsAndConcs(array,nNodes = nNodes)
    json += generateAllNodes(array, itc, nNodes = nNodes, tab = tab + 1, tabChar = tabChar)
    json += ",\n"
    json += generateAllConnections(array,itc,nNodes = nNodes, tab = tab+1, tabChar = tabChar)
    json += ",\n"
    json += generateLegacyParameters(tab = tab+1, tabChar = tabChar)
    json += "\n}"
    return json

def submitPENSystem(array, nNodes = 5, executablePath = '../../daccad', launchScript = 'cli.sh',
        launchClass = 'cli.CLIEvaluator', configFile = 'config/configEvaluation.config', baseDir = ".", jsonFileName = 'generatedGraph0_0_0.json'):

    json = generateFullJson(array, nNodes)
    with open(jsonFileName,'w') as f:
        f.write(json)
        f.flush()
    #in case of the default jsonFileName
    if not os.sep in jsonFileName:
        #we are using the default file name
        jsonFileName = os.path.join(os.getcwd(),jsonFileName)
    exect = os.path.join(executablePath,launchScript)
    #config = os.path.join(executablePath,configFile)
    command = [exect, launchClass, configFile , jsonFileName]
    try:
        result = check_output(command)
    except CalledProcessError as e:
        warnings.warn("ERROR during DACCAD execution with command: %s" % str(command), RuntimeWarning)
        result = None
    return result


def submitPENJson(json, executablePath = '../../daccad', launchScript = 'cli.sh',
        launchClass = 'cli.CLIEvaluator', configFile = 'config/configEvaluation.config', baseDir = "."):
    jsonFileName = 'generatedGraph0_0_0.json'
    exect = os.path.join(executablePath,launchScript)
    #config = os.path.join(executablePath,configFile)
    command = [exect, launchClass, configFile , jsonFileName]
    try:
        result = check_output(command, stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        warnings.warn("ERROR during DACCAD execution with command: %s" % str(command), RuntimeWarning)
        result = None
    return result

def submitPENSystem_input(array, nNodes = 5, executablePath = '../../daccad', launchScript = 'cli.sh',
        launchClass = 'cli.CLIEvaluatorwithInput', configFile = '../daccadConf.conf', baseDir = ".", jsonFileName = 'generatedGraph0_0_0.json',
        configFile_input = '../config.json'):

    json = generateFullJson(array, nNodes)
    with open(jsonFileName,'w') as f:
        f.write(json)
        f.flush()
    #in case of the default jsonFileName
    if not os.sep in jsonFileName:
        #we are using the default file name
        jsonFileName = os.path.join(os.getcwd(),jsonFileName)
    exect = os.path.join(executablePath,launchScript)
    config = os.path.join(executablePath,configFile)
    config_input = os.path.join(executablePath, configFile_input)
    command = [exect, launchClass, config, jsonFileName, config_input]
    try:
        result = check_output(command)
    except CalledProcessError as e:
        warnings.warn("ERROR during DACCAD execution with command: %s" % str(command), RuntimeWarning)
        result = None
    return result
# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
