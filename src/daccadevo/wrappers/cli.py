import os
from pathlib import Path
import subprocess
from subprocess import check_output, CalledProcessError
from datetime import datetime
import warnings
import math
import numpy as np
from abc import ABC, abstractmethod
from collections.abc import Iterable
from qdpy.base import registry

#Default configurations for calling DACCAD
def get_default_config():
    # dataDir is set automatically by qdpy when running a QDExperiment
    # can be explicitely set in the config file as well
    return {'dataDir': '.', 'daccad': {'config_file':'daccad_configs/short.conf' , 'env_name': 'default', 'executable_path':'../daccad'}}


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

class DACCAD_Wrapper(ABC):
    """
    Provides the basic methods for interpreting an array into a chemical reaction network.
    Format array: [ all stabilities (nNodes), all activations from i to j (nNodes * nNodes), \
    all inhibitions created by i to the template j to k (nNodes * nNodes * nNodes)]

    Subclasses need to implement the actual call to DACCAD. They may replace or add methods to describe 
    extended versions of the underlying chemistry.
    """

    def __init__(self, config = None):
        self.reset(config)

    def reset(self, config):
        self.config = config if config is not None else get_default_config()
        if "daccad" not in self.config:
            self.config["daccad"] = get_default_config()["daccad"]



    @abstractmethod
    def submitPENSystem(self, array, config=None, **kwargs):
        """
        Actual call to DACCAD
        """
        if config is not None:
            self.reset(config)


@registry.register
class CLI_wrapper(DACCAD_Wrapper):
    """
    Wrapper relying on writing down the system as a json file and submitting it to the CLI of DACCAD.
    """

    def __init__(self, config=None):
        super().__init__(config=config)
        self.reset(config)



    def reset(self, config):
        super().reset(config)
        dconf = self.config['daccad']
        self.script = dconf.get('script', 'cli.sh')
        self.launch_class = dconf.get('launch_class','cli.CLIEvaluator')
        self.executable_path = dconf.get('executable_path','../daccad')
        self.daccad_config_file = dconf.get('config_file', 'daccad_configs/short.conf')


    def generateNode(self, name, stability, activator, initConc = '1.0', tab = 1, tabChar = "  "):
        """
        Nodes are using the BioNEAT format.
        Name is used for display and to identify nodes in connections.
        Parameter is the dissociation constant of the DNA sequence.
        Initial concentration is used to initialize the simulation.
        Type specifies if a molecular species is an activator or an inhibitor.
        ProtectedSequence means that the molecule has been modified to prevent the activity of the
        exonuclease (not supported by the current DACCAD cli).
        DNAString allows BioNEAT to compute directly the dissociation constant of the DNA sequence
        (not supported by the current DACCAD cli).
        Reporter provides additional molecular beacons to follow the concentration of the species
        over time, making the system closer to a wetlab experiment (not supported by the current 
        DACCAD cli).
        hasPseudoTemplate, when true, adds an additional concentration sink to the species (not 
        supported by the current DACCAD cli).
        pseudoTemplateConcentration provides the concentration of the pseudo-template (not supported 
        by the current DACCAD cli).
        """
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

    def generateConnection(self, innov, concentration, fromNode, toNode, tab = 1, tabChar = "  "):
        """
        Connections are using the BioNEAT format. 
        Innovation number is used to match networks against each other. 
        Enabled allows BioNEAT to keep potentially helpful connections around but still remove them
        from evaluation by setting the parameter to false.
        From and To indicates respectively the source and destination of the connection. 
        """
        json = (tabChar*tab)+"{\n"
        json += (tabChar*(tab+1))+'"innovation": '+str(innov)+',\n'
        json += (tabChar*(tab+1))+'"enabled": true,\n'
        json += (tabChar*(tab+1))+'"parameter": '+str(concentration)+',\n'
        json += (tabChar*(tab+1))+'"from": "'+str(fromNode)+'",\n'
        json += (tabChar*(tab+1))+'"to": "'+str(toNode)+'"\n'
        json += (tabChar*tab)+"}"
        return json

    def generateAllNodes(self, array, inhibitingSequences, nNodes = 5, initConc = '1.0', tab = 1, tabChar = "  "):
        if initConc is None:
            initConc = '1.0'
        json = (tabChar*tab)+'"nodes": [\n'
        for i in range(nNodes):
            ic = initConc if isinstance(initConc, str) else initConc[i]
            json += self.generateNode(i,array[i], True, initConc = ic, tab = tab + 1, tabChar = tabChar)+',\n'
        for val in inhibitingSequences:
            _, stab = inhibitingSequences[val]
            json += self.generateNode(val,stab, False, tab = tab + 1, tabChar = tabChar)+',\n'
        json = json[:-2]+"\n"
        json += (tabChar*tab)+']'
        return json

    def generateAllConnections(self, array,inhibitions,nNodes = 5, tab = 1, tabChar = "  "):
        innovation = 0
        offset = nNodes
        json = (tabChar*tab)+'"connections": [\n'
        for fromNode in range(nNodes):
            for toNode in range(nNodes):
                index = offset + nNodes * fromNode + toNode
                if array[index] > 0.0:
                    json += self.generateConnection(innovation, array[index], fromNode, toNode, tab = tab+1, tabChar = tabChar)+',\n'
                    innovation += 1
        for val in inhibitions:
            concs, _ = inhibitions[val]
            for fromNode, concentration in concs:
                json += self.generateConnection(innovation, concentration, fromNode, val, tab = tab+1, tabChar = tabChar)+',\n'
                innovation += 1
        json = json[:-2]+"\n"
        json += (tabChar*tab)+']'
        return json

    def generateEnzymeParameters(self, pol = 1.0, nick = 1.0, exo = 1.0, tab = 1, tabChar = "  "):
        json = (tabChar*tab)+'"parameters": {\n'
        json += (tabChar*(tab+1))+'"nick": '+str(nick)+',\n'
        json += (tabChar*(tab+1))+'"pol": '+str(pol)+',\n'
        json += (tabChar*(tab+1))+'"exo": '+str(exo)+'\n'
        json += (tabChar*tab)+"}"
        return json

    def generateFullJson(self, array, enzymes = {"pol" : 1.0, "nick" : 1.0, "exo" : 1.0}, nNodes = 5, initConc = '1.0', tab = 0, tabChar = "  ", **kwargs):
        # First, check if initConc is a str or not for compatibility reason with other wrappers
        if not isinstance(initConc,str):
            if isinstance(initConc,Iterable):
                initConc = [str(ic) for ic in initConc]
            else: # single value
                initConc = str(initConc)

        json = "{\n"
        itc = findAllInhibitorsAndConcs(array,nNodes = nNodes)
        json += self.generateAllNodes(array, itc, nNodes = nNodes, initConc = initConc, tab = tab + 1, tabChar = tabChar)
        json += ",\n"
        json += self.generateAllConnections(array,itc,nNodes = nNodes, tab = tab+1, tabChar = tabChar)
        json += ",\n"
        json += self.generateEnzymeParameters(**enzymes, tab = tab+1, tabChar = tabChar)
        json += "\n}"
        return json

    def submitPENJson(self, jsonFileName = 'generatedGraph0_0_0.json', daccad_config_file = None, **kwargs):
        """
        Submit a JSON representation of a PEN system to the CLI of DACCAD
        jsonFileName: the json file describing the system
        daccad_config_file: the DACCAD configuration file to use. If None, use the config file of the wrapper.
        """

        if daccad_config_file is None:
            daccad_config_file = self.daccad_config_file
        exect = os.fspath(Path(self.executable_path,self.script).resolve())
        config_file = os.fspath(Path(self.daccad_config_file).resolve())
        jsonFileName = os.fspath(Path(jsonFileName).resolve())
        command = [exect, self.launch_class, config_file , jsonFileName]
        try:
            raw_result = check_output(command, stderr=subprocess.STDOUT).decode('ascii')
            offset = 1 if raw_result.startswith("profiling") else 0
            # Remove info and the last empty line, parse the rest
            result = np.array([[float(j) for j in i.split(',')[:-1]] for i in raw_result.split('\n')[offset:-1]]) 
        except CalledProcessError:
            warnings.warn("ERROR during DACCAD execution with command: %s" % str(command), RuntimeWarning)
            result = None
        return result

    def submitPENSystem(self, array, nNodes = 5, config = None, **kwargs):
        self.reset(config)
        jsonFileName = kwargs.pop("jsonFileName", None)
        if jsonFileName is None:
            jsonFileName = str(datetime.now().isoformat(timespec='microseconds'))+".json"

        jsonFileName = Path(jsonFileName)
        if len(os.path.split(jsonFileName)[0]) == 0:
            dataDir = self.config.get('dataDir', ".")
            env_name = self.config['daccad'].get('env_name','.')
            folder = Path(dataDir,env_name).absolute()
            if not os.path.exists(folder):
                os.makedirs(folder)
            jsonFileName = Path(folder,jsonFileName)

        json = self.generateFullJson(array, nNodes = nNodes, **kwargs)

        # check if file already exists
        if jsonFileName.exists():
            folder, basename = os.path.split(jsonFileName)
            name, ext = os.path.splitext(basename)
            jsonFileName = jsonFileName.rename(Path(folder, name+"_2"+ext))


        with open(jsonFileName,'w') as f:
            f.write(json)
            f.flush()

        result = self.submitPENJson(jsonFileName = jsonFileName, **kwargs)

        if "keepTemporaryFiles" not in self.config or not self.config['keepTemporaryFiles']:
            if jsonFileName.exists():
                os.remove(jsonFileName)
            else:
                warnings.warn("ERROR trying to remove file: %s" % str(jsonFileName), RuntimeWarning)

        return result


"""
Default cli wrapper
"""
default_cli_wrapper = CLI_wrapper()

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
