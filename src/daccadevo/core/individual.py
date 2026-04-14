from datetime import datetime

import numpy as np
from qdpy.base import registry
from qdpy.phenotype import Individual

import daccadevo.wrappers as wr

from .mutation_utils import random_log_scale_1000

########## INDIVIDUALS AND FITNESSES ###########

class DaccadIndividual(Individual):
    """An extension of the QDPy Individual class, encoding a molecular network for the DACCAD simulator.

    A DaccadIndividual implements a PEN DNA network while following the QDPy IndividualLike interface.
    A PEN DNA network is comprised of molecular signal species that dynamically produce other signal
    species through enzymatic reactions involving molecular templates. For instance, a molecula A can
    react with the A->B template to produce B over time. A specific type of signal species, called
    inhibitors will attach to its target, preventing further reactions until it is degraded and thus
    disabling the template. All signal species are also degraded over time by the exonuclease enzyme,
    keeping the system dynamic.

    The main informations needed for simulation are: 

    - DNA sequence stabilities: 
        representing how long a signal species will remain duplexed to a target template. Note that, 
        despite the name, this value encodes the *dissociation* rate. Thus, a high value represents 
        an *un* stable species, while a low value represents a stable species. The stability of 
        inhibitor species is calculated by DACCAD.
    - Template concentrations: 
        representing the actual network, as the output of a given template will act as the input of 
        others, potentially forming loops. The DaccadIndividual class provides an interface to access 
        and modify those informations directly as well as a method (``self.assemble``) to turn them 
        into a format usable by QDPy (namely, a 1D NumPy array). That two step approach was favored 
        to deal efficiently with cases were the number of signal species is modified by the algorithm, 
        thus changing the lengths of the various attributes.

    Parameters
    ----------
    ind_domain: list, array, or tuple of length 2
        Domain for the individual, corresponding to the valid concentration range for templates. 
        Typical values are [0, 1] (normalized) or [0, 200] (direct implementation).

    nb_nodes: int, optional
        Number of signal species in the network (ignoring inhibiting species).
        Default value is 0, corresponding to an empty network.

    species: int, optional
        Species identifier, either used to track phylogeny or to allow genetic crossover in the ERNE
        algorithm. Default is 0. 

    name: Any, optional
        A convenience descriptor for the individual. Inherited from QDPy.

    **kwargs: QDPy individual arguments
        See QDPy's documentation for a list of valid arguments. 

    Attributes
    ----------
    stabilities: 1D array
        Array of length ``nb_nodes``. ith value corresponds to the stability (dissociation rate) of 
        the ith signal species.

    activations: 2D array
        Array of shape ``(nb_nodes, nb_nodes)``. ``activations[i,j]`` corresponds to the concentration
        the template producing the jth species from the ith species. A value of 0 means that the
        template is not present in the system.

    inhibitions: 3D array
        Array of shape ``(nb_nodes, nb_nodes, nb_nodes)``. ``inhibitions[i,j,k]`` corresponds to the
        concentration of the template taking the ith species as input and producing the *inhibitor*
        of the j->k template. A non-zero value is not valid if the j->k template is not present in
        the network. If there is no production of the inhibitor of the j->k template 
        (``inhibitions[i,j,k]`` is 0 for all i), then the inhibitor will not be instanciated in the
        simulator.

    Examples
    --------
    Implementation of a simple bistable system: A->A, B->B, A -> Inh(B->B), B -> Inh(A->A)
    
    >>> from daccadevo.core import DaccadIndividual
    >>> indiv = DaccadIndividual([0,1], nb_nodes = 2)
    >>> indiv.activations[0,0] = 10.0
    >>> indiv.activations[1,1] = 10.0
    >>> indiv.inhibitions[0,1,1]=20.0
    >>> indiv.inhibitions[1,0,0]=20.0

    For other examples, see the :ref: `base_examples.ipynb`

    """
    
    def __init__(self, ind_domain, nb_nodes = 0, species=0, **kwargs):
        """Constructor method
        """
        super().__init__(**kwargs)
        self.nb_nodes = nb_nodes
        self.ind_domain = ind_domain
        self.stabilities = np.zeros(self.nb_nodes)
        self.activations = np.zeros((self.nb_nodes, self.nb_nodes))
        self.inhibitions = np.zeros((self.nb_nodes, self.nb_nodes, self.nb_nodes))
        self.name = kwargs.get("name", str(datetime.now()))
        self.species = species

    def is_valid(self):
        """Check the validity of a DaccadIndividual.
        """
        return len(self.stabilities) == self.nb_nodes and self.activations.shape == (self.nb_nodes,self.nb_nodes) \
                and self.inhibitions.shape == (self.nb_nodes,self.nb_nodes,self.nb_nodes) \
                and wr.isValid(self, self.nb_nodes)

    def assemble(self):
        """Transcribe the current information into the underlying ndarray of the QDPy Individual object.
        """
        self[:] = list(self.stabilities) + list(self.activations.flatten()) + list(self.inhibitions.flatten())

    def update(self):
        """Copy the underlying data of the QDPy individual into the DaccadIndividual structure.
        """
        self.stabilities = np.array(self[:self.nb_nodes])
        self.activations = np.array(self[self.nb_nodes: self.nb_nodes + self.nb_nodes*self.nb_nodes]).reshape((self.nb_nodes, self.nb_nodes))
        self.inhibitions = np.array(self[self.nb_nodes + self.nb_nodes*self.nb_nodes:]).reshape((self.nb_nodes, self.nb_nodes, self.nb_nodes))

    def same_species_as(self, other):
        """Check if the species of other is identical to this one.

        Used to keep track of lineage. Can be used to implement BioNEAT/ERNE-like species.
        """
        return self.species == other.species

    def resize(self, nb_nodes):
        """Change the number of signal species, updating all data structures.
        """
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
        """Get a list of all signal species contributing to the dynamics of the system.
        """
        res = []
        for i in range(self.nb_nodes):
            if sum(self.activations[i,:]>0) or sum(self.activations[:,i]>0) \
                    or sum(self.inhibitions[i,:,:].flatten()>0) \
                    or sum(self.inhibitions[:,i,:].flatten()>0) \
                    or sum(self.inhibitions[:,:,i].flatten()>0):
                res.append(i)
        return res

    def valid_indexes(self):
        """Get a list of indexes of active signal species.
        """
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

@registry.register
def gen_daccad_individuals(ind_domain):
    """Yield a new unique individual with an empty network"""
    while(True):
        yield DaccadIndividual(ind_domain)

@registry.register
def standard_init_ind(ind):
    """Create a base individual, with 3 nodes and a "2->2" connection"""
    ind.resize(3)
    ind.stabilities = np.array([random_log_scale_1000() for _ in range(3)])
    #ind.stabilities = [10./1000., 10./1000., 100./1000.]
    ind.activations[2,2] = 0.025 #random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind

@registry.register
def standard_init_ind_grad4(ind):
    """Create a base individual in a setup with 4 gradients, with 5 nodes and a "4->4" connection"""
    ind.resize(5)
    ind.stabilities = np.array([random_log_scale_1000() for _ in range(5)])
    ind.stabilities = [10./1000., 10./1000., 10./1000., 10./1000, 100./1000.,]
    ind.activations[4,4] = 0.025 #random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind

@registry.register
def standard_init_ind0(ind):
    """Create a base individual, with 1 node and a "0->0" connection"""
    ind.resize(1)
    ind.activations[0,0] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind

@registry.register
def standard_init_act(ind):
    """Create a base individual, with 2 nodes and a "0->1" connection"""
    ind.resize(2)
    ind.activations[0,1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    ind.assemble()
    return ind
