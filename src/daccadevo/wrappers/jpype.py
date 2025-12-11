import jpype
import jpype.imports
from daccadevo.wrappers.cli import DACCAD_Wrapper, findAllInhibitorsAndConcs

from qdpy.base import registry
import daccadevo.wrappers.daccad as daccad
import numpy as np
from collections.abc import Iterable
	

@registry.register
class Jpype_wrapper(DACCAD_Wrapper):
	"""
	Wrapper relying on writing down the system as a json file and submitting it to the CLI of DACCAD.
	"""

	def __init__(self, config=None):
		super().__init__(config=config)
		self.reset(config)
		daccad.startJVM(rootdir=self.executable_path, 
			debug=config.get("debug",False), jvmpath=config.get("jvmpath"))


	def reset(self, config):
		super().reset(config)
		dconf = self.config['daccad']
		self.script = dconf.get('script', 'cli.sh')
		self.launch_class = dconf.get('launch_class','cli.CLIEvaluator')
		self.executable_path = dconf.get('executable_path','../daccad')
		self.daccad_config_file = dconf.get('config_file', 'daccad_configs/short.conf')

	def generateNode(self, name, stability, activator, graph, species_dict, initConc = 1.0):
		s = graph.getVertexFactory().create()
		if not(activator):
			s.setInhib(True)
		graph.addSpecies(s, stability)
		species_dict[name] = s
		s.setInitialConcentration(initConc)
		return s

	# new
	def generateConnection(self, innov, concentration, fromNode, toNode, graph, species_dict):
		edge = graph.getEdgeFactory().createEdge(species_dict[fromNode], species_dict[toNode])
		graph.addActivation(edge, species_dict[fromNode], species_dict[toNode], concentration)
		return edge

	# TODO interface is not DRY
	def generateAllNodes(self, array, inhibitingSequences, graph, species_dict, initConc = 1.0, nNodes = 5):
		if initConc is None:
			initConc = 1.0
		for i in range(nNodes):
			ic = initConc[i] if isinstance(initConc,Iterable) else initConc
			self.generateNode(i,array[i], True, graph, species_dict, initConc = ic)
		for val in inhibitingSequences:
			_, stab = inhibitingSequences[val]
			self.generateNode(val,stab, False, graph, species_dict, initConc = 0.0)
		return graph

	# new
	def generateAllConnections(self, array,inhibitions,graph, species_dict, nNodes = 5):
		innovation = 0
		offset = nNodes
		for fromNode in range(nNodes):
			for toNode in range(nNodes):
				index = offset + nNodes * fromNode + toNode
				if array[index] > 0.0:
					self.generateConnection(innovation, array[index], fromNode, toNode, graph, species_dict)
					innovation += 1
		for val in inhibitions:
			concs, _ = inhibitions[val]
			for fromNode, concentration in concs:
				edge = self.generateConnection(innovation, concentration, int(fromNode), val, graph, species_dict)
				graph.addInhibition(edge, species_dict[val])
				innovation += 1
		return graph


	def generateEnzymeParameters(self, graph, pol = 1.0, nick = 1.0, exo = 1.0):
		graph.polConc = pol
		graph.nickConc = nick
		graph.exoConc = exo
		return graph


	# new
	def generateFull(self, array, graph, species_dict, nNodes = 5, 
		enzymes = {"pol" : 1.0, "nick" : 1.0, "exo" : 1.0}, initConc = 1.0, **kwargs):
		itc = findAllInhibitorsAndConcs(array,nNodes = nNodes)
		graph = self.generateAllNodes(array, itc, graph, species_dict, nNodes = nNodes, initConc=initConc)
		graph = self.generateAllConnections(array, itc, graph, species_dict, nNodes = nNodes)
		graph = self.generateEnzymeParameters(graph, **enzymes)
		return graph

	# new
	def submitPENSystem(self, array, nNodes = 5, config=None, **kwargs):
		# In case we execute in a different thread without JVM
		daccad.startJVM(rootdir=self.executable_path, 
			debug=config.get("debug",False), jvmpath=config.get("jvmpath",None))
		import model.Constants
		import model.OligoGraph
		import model.OligoSystem
		import model.chemicals.SequenceVertex
		import utils.GraphUtils
		if config is not None:
			self.reset(config)
		if "enzymes" in self.config:
			#just in case
			kwargs["enzymes"] = self.config["enzymes"]
		elif "enzymes" in self.config['daccad']:
			kwargs["enzymes"] = self.config['daccad']["enzymes"]

		g = utils.GraphUtils.initGraph()
		species_dict = {}
		g = self.generateFull(array, g, species_dict, nNodes, **kwargs)
		# TODO: make 
		# os = model.OligoSystem(g, utils.PredatorPreyTemplateFactory(g))
		oligosystem =  model.OligoSystem(g)

		with open(self.daccad_config_file,"r") as f:
			for line in f.readlines():
				if not line.strip().startswith("#"):
					params = line.split("=")
					model.Constants.readConfigFromString(jpype.JClass(model.Constants),params[0].strip(), params[1].strip())
		timeSeries = oligosystem.calculateTimeSeries(None) 
		timeSeries = np.array(timeSeries).T
		return timeSeries


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
