import os
from pathlib import Path
import subprocess
from subprocess import check_output, CalledProcessError
from datetime import datetime
import warnings
import math
import numpy as np

#Default configurations for a CLI run
def get_default_config():
    # dataDir is set automatically by qdpy when running a QDExperiment
    # can be explicitely set in the config file as well
    return {'dataDir': '.', 'daccad': {'config_file':'daccad_configs/short.conf' , 'env_name': 'default', 'executable_path':'../daccad'}}

#Format array: [ all stabilities (nNodes), all activations from i to j (nNodes * nNodes), all inhibitions created by i to the template j to k (nNodes * nNodes * nNodes)]

def findAllInhibitions(array, nNodes = 5):
    beginInhibitionTemplates = nNodes * (nNodes+1)
    inhibitions = {}
    for i in range(nNodes): #For each possible activator
        index = beginInhibitionTemplates + i * nNodes * nNodes
        for fromId in range(nNodes):
            for toId in range(nNodes):
                if array[index + fromId*nNodes + toId] > 0.0:
                    if (fromId,toId) not in inhibitions:
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
                    if name not in inhibitingTemplatesConcs:
                        stability =  1 / 100 * math.exp((math.log(array[fromId]) + math.log(array[toId])) / 2)
                        inhibitingTemplatesConcs[name] = ([],stability)
                    inhibitingTemplatesConcs[name][0].append((str(i),array[index + fromId*nNodes + toId]))
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


def generateNode(name, stability, activator, initConc = '1.0', tab = 1, tabChar = "  "):
    json = (tabChar*tab)+"{\n"
    json += (tabChar*(tab+1))+'"name": "'+str(name)+'",\n'
    json += (tabChar*(tab+1))+'"parameter": '+str(stability)+',\n'
    json += (tabChar*(tab+1))+'"initialConcentration": '+(initConc if activator else '0.0')+',\n'
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

def generateAllNodes(array, inhibitingSequences, nNodes = 5, initConc = '1.0', tab = 1, tabChar = "  "):
    if initConc is None:
        initConc = '1.0'
    json = (tabChar*tab)+'"nodes": [\n'
    for i in range(nNodes):
        ic = initConc if isinstance(initConc, str) else initConc[i]
        json += generateNode(i,array[i], True, initConc = ic, tab = tab + 1, tabChar = tabChar)+',\n'
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

def generateEnzymeParameters(pol = 1.0, nick = 1.0, exo = 1.0, tab = 1, tabChar = "  "):
    json = (tabChar*tab)+'"parameters": {\n'
    json += (tabChar*(tab+1))+'"nick": '+str(nick)+',\n'
    json += (tabChar*(tab+1))+'"pol": '+str(pol)+',\n'
    json += (tabChar*(tab+1))+'"exo": '+str(exo)+'\n'
    json += (tabChar*tab)+"}"
    return json

def generateFullJson(array, enzymes = {"pol" : 1.0, "nick" : 1.0, "exo" : 1.0}, nNodes = 5, initConc = '1.0', tab = 0, tabChar = "  ", **kwargs):
    json = "{\n"
    itc = findAllInhibitorsAndConcs(array,nNodes = nNodes)
    json += generateAllNodes(array, itc, nNodes = nNodes, initConc = initConc, tab = tab + 1, tabChar = tabChar)
    json += ",\n"
    json += generateAllConnections(array,itc,nNodes = nNodes, tab = tab+1, tabChar = tabChar)
    json += ",\n"
    json += generateEnzymeParameters(**enzymes, tab = tab+1, tabChar = tabChar)
    json += "\n}"
    return json

def submitPENSystem(array, nNodes = 5, jsonFileName = None, config = None, **kwargs):
    if config is None:
        config = get_default_config()
    elif "daccad" not in config:
        config["daccad"] = get_default_config()["daccad"]

    if jsonFileName is None:
        jsonFileName = str(datetime.now().isoformat(timespec='microseconds'))+".json"

    jsonFileName = Path(jsonFileName)
    if len(os.path.split(jsonFileName)[0]) == 0:
        folder = Path(config['dataDir'],config['daccad']['env_name']).absolute()
        if not os.path.exists(folder):
            os.makedirs(folder)
        jsonFileName = Path(folder,jsonFileName)

    json = generateFullJson(array, nNodes = nNodes, **kwargs)

    # check if file already exists
    if jsonFileName.exists():
        folder, basename = os.path.split(jsonFileName)
        name, ext = os.path.splitext(basename)
        jsonFileName = jsonFileName.rename(Path(folder, name+"_2"+ext))


    with open(jsonFileName,'w') as f:
        f.write(json)
        f.flush()

    result = submitPENJson(json, jsonFileName = jsonFileName, **config["daccad"], **kwargs)

    if "keepTemporaryFiles" not in config or not config['keepTemporaryFiles']:
        if jsonFileName.exists():
            os.remove(jsonFileName)
        else:
            warnings.warn("ERROR trying to remove file: %s" % str(jsonFileName), RuntimeWarning)

    return result


def submitPENJson(json, executable_path = '../daccad', script = 'cli.sh',
        launch_class = 'cli.CLIEvaluator', config_file = 'daccad_configs/short.conf', jsonFileName = 'generatedGraph0_0_0.json', **kwargs):
    
    exect = os.fspath(Path(executable_path,script).resolve())
    config_file = os.fspath(Path(config_file).resolve())
    jsonFileName = os.fspath(Path(jsonFileName).resolve())
    command = [exect, launch_class, config_file , jsonFileName]
    try:
        raw_result = check_output(command, stderr=subprocess.STDOUT).decode('ascii')
        offset = 1 if raw_result.startswith("profiling") else 0
        # Remove info and the last empty line, parse the rest
        result = np.array([[float(j) for j in i.split(',')[:-1]] for i in raw_result.split('\n')[offset:-1]]) 
    except CalledProcessError:
        warnings.warn("ERROR during DACCAD execution with command: %s" % str(command), RuntimeWarning)
        result = None
    return result


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
