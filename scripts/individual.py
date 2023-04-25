import numpy as np
from qdpy.phenotype import Individual
import submitDACCAD
from mutation_utils import random_log_scale_1000

########## INDIVIDUALS AND FITNESSES ###########

class DaccadIndividual(Individual):
    # ind_domain: valid concentration domain for templates. [0,200] for instance
    def __init__(self, ind_domain, **kwargs):
        super().__init__(**kwargs)
        self.nb_nodes = 0
        self.ind_domain = ind_domain
        self.stabilities = []
        self.activations = np.zeros((self.nb_nodes, self.nb_nodes))
        self.inhibitions = np.zeros((self.nb_nodes, self.nb_nodes, self.nb_nodes))
        self.name = str(id(self))
        self.specie = 0

    def is_valid(self):
        return submitDACCAD.isValid(self, self.nb_nodes)

    def assemble(self):
        self[:] = list(self.stabilities) + list(self.activations.flatten()) + list(self.inhibitions.flatten())

    def update(self):
        self.stabilities = np.array(self[:self.nb_nodes])
        self.activations = np.array(self[self.nb_nodes: self.nb_nodes + self.nb_nodes*self.nb_nodes]).reshape((self.nb_nodes, self.nb_nodes))
        self.inhibitions = np.array(self[self.nb_nodes + self.nb_nodes*self.nb_nodes:]).reshape((self.nb_nodes, self.nb_nodes, self.nb_nodes))

    #Used to implement BioNEAT-like species
    def same_species_as(self, other):
        return self.specie == other.specie

    def resize(self, nb_nodes):
        if nb_nodes == self.nb_nodes:
            return
        elif nb_nodes < self.nb_nodes:
            self.stabilities = self.stabilities[:nb_nodes]
            self.activations = self.activations[:nb_nodes, :nb_nodes]
            self.inhibitions = self.inhibitions[:nb_nodes, :nb_nodes, :nb_nodes]
        else:
            stabilities = np.empty(nb_nodes)
            stabilities[:self.nb_nodes] = self.stabilities
            stabilities[self.nb_nodes:] = np.random.uniform(self.ind_domain[0], self.ind_domain[1], nb_nodes - self.nb_nodes)
            self.stabilities = stabilities
            activations = np.zeros((nb_nodes, nb_nodes))
            activations[:self.nb_nodes, :self.nb_nodes] = self.activations
            self.activations = activations
            inhibitions = np.zeros((nb_nodes, nb_nodes, nb_nodes))
            inhibitions[:self.nb_nodes, :self.nb_nodes, :self.nb_nodes] = self.inhibitions
            self.inhibitions = inhibitions
        self.nb_nodes = nb_nodes
        self.assemble()

    def active_nodes(self):
        res = []
        for i in range(self.nb_nodes):
            if sum(self.activations[i,:]>0) or sum(self.activations[:,i]>0) \
                    or sum(self.inhibitions[i,:,:].flatten()>0) \
                    or sum(self.inhibitions[:,i,:].flatten()>0) \
                    or sum(self.inhibitions[:,:,i].flatten()>0):
                res.append(i)
        return res

    def valid_indexes(self):
        self.assemble()
        res = list(np.where(self)[0])
        # Remove stabilities of unconnected nodes
        for i in range(self.nb_nodes):
            if sum(self.activations[i,:]>0) or sum(self.activations[:,i]>0) \
                    or sum(self.inhibitions[i,:,:].flatten()>0) \
                    or sum(self.inhibitions[:,i,:].flatten()>0) \
                    or sum(self.inhibitions[:,:,i].flatten()>0):
                continue
            else:
                res.remove(i)
        return res

    @property
    def values(self):
        return np.array(self)[self.valid_indexes()]

    @values.setter
    def values(self, vals):
        for ivals, iself in enumerate(self.valid_indexes()):
            self[iself] = vals[ivals]
        self.update()

def gen_daccad_individuals(ind_domain):
    """Yield a new unique individual with an empty network"""
    while(True):
        yield DaccadIndividual(ind_domain)

def standard_init_ind(ind):
    """Create a base individual, with 3 nodes and a "2->2" connection"""
    ind.resize(3)
    ind.stabilities = np.array([random_log_scale_1000() for _ in range(3)])
    ind.stabilities = [10./1000., 10./1000., 100./1000.]
    ind.activations[2,2] = 0.025 #random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind


def standard_init_ind_grad4(ind):
    """Create a base individual in a setup with 4 gradients, with 5 nodes and a "4->4" connection"""
    ind.resize(5)
    ind.stabilities = np.array([random_log_scale_1000() for _ in range(5)])
    ind.stabilities = [10./1000., 10./1000., 10./1000., 10./1000, 100./1000.,]
    ind.activations[4,4] = 0.025 #random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind


def standard_init_ind0(ind):
    """Create a base individual, with 1 node and a "0->0" connection"""
    ind.resize(1)
    ind.activations[0,0] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind
