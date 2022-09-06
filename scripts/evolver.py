import submitDACCAD

import numpy as np
import copy
import pickle

from qdpy.base import *
from qdpy.algorithms import *
from qdpy.containers import *
from qdpy import tools

from individual import *
from mutation import *

from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload

@registry.register
class DaccadBioneatMut(Evolution):
    """Basic class for QD implementing BioNEAT mutations"""

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike,
            nb_nodes_domain: Sequence[int] = [1, 7],
            min_init_budget: int = 1,
            min_ind_found_in_init: int = 1,
            init_pb: float = 0.0,
            sel_pb: float = 1.0,
            prob_parameter_mut: float = 0.4,
            prob_template_add: float = 0.2,
            prob_template_del: float = 0.2,
            prob_signal_species_add: float = 0.1,
            prob_inhibition_species_add: float = 0.1,
            nbConnActivationsDomain: Sequence[int] = [1, 7],
            nbConnInhibitionsDomain: Sequence[int] = [0, 6],
            nbConnDomain: Sequence[int] = [1, 13],
            f1: float = 0.2,
            f2: float = 2.0,
            mut_pb: float = 0.8,
            init_drift: int = 1, #number of mutations applied on initial individuals
            **kwargs):
        self.ind_domain = ind_domain
        self.nb_nodes_domain = nb_nodes_domain
        self.min_init_budget = min_init_budget
        self.min_ind_found_in_init = min_ind_found_in_init
        self.init_pb = init_pb
        self.sel_pb = sel_pb
        self.prob_parameter_mut = prob_parameter_mut
        self.prob_template_add = prob_template_add
        self.prob_template_del = prob_template_del
        self.prob_signal_species_add = prob_signal_species_add
        self.prob_inhibition_species_add = prob_inhibition_species_add
        self.nbConnActivationsDomain = nbConnActivationsDomain
        self.nbConnInhibitionsDomain = nbConnInhibitionsDomain
        self.nbConnDomain = nbConnDomain
        self.f1 = f1
        self.f2 = f2
        self.mut_pb = 0.8
        self.init_drift = init_drift
        

        super().__init__(container, budget, select_or_initialise=self._select_or_initialise, vary=self._vary, base_ind_gen=gen_daccad_individuals(self.ind_domain), **kwargs)


    def _select_or_initialise(self, collection: Sequence[Any], base_ind: IndividualLike) -> Tuple[Any, bool]:
        initialise = self._nb_suggestions < self.min_init_budget or len(collection) < self.min_ind_found_in_init
        if not initialise:
            operation = np.random.choice(range(2), p=[self.sel_pb, self.init_pb])
            initialise = operation == 1

        if initialise: # Initialisation
            # Create a base individual
            
            standard_init_ind(base_ind)
            for _ in range(self.init_drift):
                base_ind = self._vary(base_ind)
            return base_ind, False

        else: # Selection
            try:
                choice = np.random.choice(2)
                if choice == 0:
                    res = tools.non_trivial_sel_random(collection), True
                else:
                    res = tools.sel_random(collection), True
            except Exception as e:
                print(f"EXCEPTION ! {e}")
                traceback.print_exc()
            
            return res


    def _vary(self, individual):
        
        for _ in range(500): # Max number of retries to find a valid individual
            ind = copy.deepcopy(individual)
            ind.name = str(id(ind))

            active_activations_coords = list(zip(*np.where(ind.activations)))
            nb_active_activations = len(active_activations_coords)
            active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
            nb_active_inhibitions = len(active_inhibitions_coords)

            # Choose the kind of mutation
            choice = np.random.choice(5, p=(self.prob_parameter_mut,
                self.prob_template_add, self.prob_template_del,
                self.prob_signal_species_add, self.prob_inhibition_species_add))

            # Perform the mutation
            if choice == 0: # Parameters mutation
                #mutation_param_polybounded(ind, self.eta, self.mutationPb)
                #mutation_param_bioneat(ind, self.f1, self.f2, 1)
                mutation_param_bioneat(ind, self.f1, self.f2, self.mut_pb)
            elif choice == 1: # Add Activation
                mutation_add_activation(ind)
            elif choice == 2: # Del Activation
                mutation_del_activation(ind)
            elif choice == 3: # Signal species
                mutation_bioneat_signal_species(ind)
            elif choice == 4: # Inhibition species
                mutation_bioneat_inhibition_species(ind)


            ## Verify if there are no orphaned nodes
            #is_orphaned = (not(any(ind.activations[:,i]) or any(ind.activations[i,:]) or any(ind.inhibitions[i,:,:].flatten())) for i in range(ind.nb_nodes))
            #if any(is_orphaned):
            #    continue

            # Assemble individual
            ind.assemble()
            # Verify if valid
            if ind.is_valid():
                # Verify if within bounds
                active_activations_coords = list(zip(*np.where(ind.activations)))
                nb_active_activations = len(active_activations_coords)
                active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
                nb_active_inhibitions = len(active_inhibitions_coords)
                if nb_active_activations >= self.nbConnActivationsDomain[0] and nb_active_activations <= self.nbConnActivationsDomain[1] and nb_active_inhibitions >= self.nbConnInhibitionsDomain[0] and nb_active_inhibitions <= self.nbConnInhibitionsDomain[1] and nb_active_activations + nb_active_inhibitions >= self.nbConnDomain[0] and nb_active_activations + nb_active_inhibitions <= self.nbConnDomain[1]:
                    break
            else:
                print(f"VARY: NOT VALID ! (choice={choice})")
                #raise RuntimeError(f"VARY: NOT VALID ! (choice={choice})")
        return ind


@registry.register
class DaccadBioneatMut_smaller(Evolution):
    """Basic class for QD implementing BioNEAT mutations"""

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike,
            nb_nodes_domain: Sequence[int] = [1, 7],
            min_init_budget: int = 1,
            min_ind_found_in_init: int = 1,
            init_pb: float = 0.0,
            sel_pb: float = 1.0,
            prob_parameter_mut: float = 0.45,
            prob_template_add: float = 0.,
            prob_template_del: float = 0.25,
            prob_signal_species_add: float = 0.15,
            prob_inhibition_species_add: float = 0.15,
            nbConnActivationsDomain: Sequence[int] = [1, 7],
            nbConnInhibitionsDomain: Sequence[int] = [0, 6],
            nbConnDomain: Sequence[int] = [1, 13],
            f1: float = 0.2,
            f2: float = 2.0,
            mut_pb: float = 0.8,
            init_drift: int = 1, #number of mutations applied on initial individuals
            **kwargs):
        self.ind_domain = ind_domain
        self.nb_nodes_domain = nb_nodes_domain
        self.min_init_budget = min_init_budget
        self.min_ind_found_in_init = min_ind_found_in_init
        self.init_pb = init_pb
        self.sel_pb = sel_pb
        self.prob_parameter_mut = prob_parameter_mut
        self.prob_template_add = prob_template_add
        self.prob_template_del = prob_template_del
        self.prob_signal_species_add = prob_signal_species_add
        self.prob_inhibition_species_add = prob_inhibition_species_add
        self.nbConnActivationsDomain = nbConnActivationsDomain
        self.nbConnInhibitionsDomain = nbConnInhibitionsDomain
        self.nbConnDomain = nbConnDomain
        self.f1 = f1
        self.f2 = f2
        self.mut_pb = 0.8
        self.init_drift = init_drift
        

        super().__init__(container, budget, select_or_initialise=self._select_or_initialise, vary=self._vary, base_ind_gen=gen_daccad_individuals(self.ind_domain), **kwargs)


    def _select_or_initialise(self, collection: Sequence[Any], base_ind: IndividualLike) -> Tuple[Any, bool]:
        initialise = self._nb_suggestions < self.min_init_budget or len(collection) < self.min_ind_found_in_init
        if not initialise:
            operation = np.random.choice(range(2), p=[self.sel_pb, self.init_pb])
            initialise = operation == 1

        if initialise: # Initialisation
            # Create a base individual
            standard_init_ind2(base_ind)
            for _ in range(self.init_drift):
                base_ind = self._vary(base_ind)
            return base_ind, False

        else: # Selection
            try:
                choice = np.random.choice(2)
                if choice == 0:
                    res = tools.non_trivial_sel_random(collection), True
                else:
                    res = tools.sel_random(collection), True
            except Exception as e:
                print(f"EXCEPTION ! {e}")
                traceback.print_exc()
            
            return res


    def _vary(self, individual):
        
        for _ in range(500): # Max number of retries to find a valid individual
            ind = copy.deepcopy(individual)
            ind.name = str(id(ind))

            active_activations_coords = list(zip(*np.where(ind.activations)))
            nb_active_activations = len(active_activations_coords)
            active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
            nb_active_inhibitions = len(active_inhibitions_coords)

            # Choose the kind of mutation
            choice = np.random.choice(5, p=(self.prob_parameter_mut,
                self.prob_template_add, self.prob_template_del,
                self.prob_signal_species_add, self.prob_inhibition_species_add))
                
            # Perform the mutation
            if choice == 0: # Parameters mutation
                #mutation_param_polybounded(ind, self.eta, self.mutationPb)
                #mutation_param_bioneat(ind, self.f1, self.f2, 1)
                mutation_param_bioneat(ind, self.f1, self.f2, self.mut_pb)
            elif choice == 1: # Add Activation
                mutation_add_activation(ind)
            elif choice == 2: # Del Activation
                mutation_del_activation(ind)
            elif choice == 3: # Signal species
                mutation_bioneat_signal_species(ind)
            elif choice == 4: # Inhibition species
                mutation_bioneat_inhibition_species(ind)


            ## Verify if there are no orphaned nodes
            #is_orphaned = (not(any(ind.activations[:,i]) or any(ind.activations[i,:]) or any(ind.inhibitions[i,:,:].flatten())) for i in range(ind.nb_nodes))
            #if any(is_orphaned):
            #    continue

            # Assemble individual
            ind.assemble()
            # Verify if valid
            if ind.is_valid():
                # Verify if within bounds
                active_activations_coords = list(zip(*np.where(ind.activations)))
                nb_active_activations = len(active_activations_coords)
                active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
                nb_active_inhibitions = len(active_inhibitions_coords)
                if nb_active_activations >= self.nbConnActivationsDomain[0] and nb_active_activations <= self.nbConnActivationsDomain[1] and nb_active_inhibitions >= self.nbConnInhibitionsDomain[0] and nb_active_inhibitions <= self.nbConnInhibitionsDomain[1] and nb_active_activations + nb_active_inhibitions >= self.nbConnDomain[0] and nb_active_activations + nb_active_inhibitions <= self.nbConnDomain[1]:
                    break
            else:
                print(f"VARY: NOT VALID ! (choice={choice})")
                #raise RuntimeError(f"VARY: NOT VALID ! (choice={choice})")
        return ind


@registry.register
class DaccadBioneatMut_5(Evolution):
    """Basic class for QD implementing BioNEAT mutations"""

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike,
            nb_nodes_domain: Sequence[int] = [1, 7],
            min_init_budget: int = 1,
            min_ind_found_in_init: int = 1,
            init_pb: float = 0.0,
            sel_pb: float = 1.0,
            prob_parameter_mut: float = 0.5,
            prob_template_add: float = 0.25,
            prob_template_del: float = 0.25,
            prob_signal_species_add: float = 0,
            prob_inhibition_species_add: float = 0,
            nbConnActivationsDomain: Sequence[int] = [1, 7],
            nbConnInhibitionsDomain: Sequence[int] = [0, 6],
            nbConnDomain: Sequence[int] = [1, 13],
            f1: float = 0.2,
            f2: float = 2.0,
            mut_pb: float = 0.8,
            init_drift: int = 1, #number of mutations applied on initial individuals
            **kwargs):
        self.ind_domain = ind_domain
        self.nb_nodes_domain = nb_nodes_domain
        self.min_init_budget = min_init_budget
        self.min_ind_found_in_init = min_ind_found_in_init
        self.init_pb = init_pb
        self.sel_pb = sel_pb
        self.prob_parameter_mut = prob_parameter_mut
        self.prob_template_add = prob_template_add
        self.prob_template_del = prob_template_del
        self.prob_signal_species_add = prob_signal_species_add
        self.prob_inhibition_species_add = prob_inhibition_species_add
        self.nbConnActivationsDomain = nbConnActivationsDomain
        self.nbConnInhibitionsDomain = nbConnInhibitionsDomain
        self.nbConnDomain = nbConnDomain
        self.f1 = f1
        self.f2 = f2
        self.mut_pb = 0.8
        self.init_drift = init_drift
        

        super().__init__(container, budget, select_or_initialise=self._select_or_initialise, vary=self._vary, base_ind_gen=gen_daccad_individuals(self.ind_domain), **kwargs)


    def _select_or_initialise(self, collection: Sequence[Any], base_ind: IndividualLike) -> Tuple[Any, bool]:
        initialise = self._nb_suggestions < self.min_init_budget or len(collection) < self.min_ind_found_in_init
        if not initialise:
            operation = np.random.choice(range(2), p=[self.sel_pb, self.init_pb])
            initialise = operation == 1

        if initialise: # Initialisation
            # Create a base individual
            standard_init_ind_grad4(base_ind)
            for _ in range(self.init_drift):
                base_ind = self._vary(base_ind)
            return base_ind, False

        else: # Selection
            try:
                choice = np.random.choice(2)
                if choice == 0:
                    res = tools.non_trivial_sel_random(collection), True
                else:
                    res = tools.sel_random(collection), True
            except Exception as e:
                print(f"EXCEPTION ! {e}")
                traceback.print_exc()
            
            return res


    def _vary(self, individual):
        
        for _ in range(500): # Max number of retries to find a valid individual
            ind = copy.deepcopy(individual)
            ind.name = str(id(ind))

            active_activations_coords = list(zip(*np.where(ind.activations)))
            nb_active_activations = len(active_activations_coords)
            active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
            nb_active_inhibitions = len(active_inhibitions_coords)

            # Choose the kind of mutation
            choice = np.random.choice(5, p=(self.prob_parameter_mut,
                self.prob_template_add, self.prob_template_del,
                self.prob_signal_species_add, self.prob_inhibition_species_add))
                
            # Perform the mutation
            if choice == 0: # Parameters mutation
                #mutation_param_polybounded(ind, self.eta, self.mutationPb)
                #mutation_param_bioneat(ind, self.f1, self.f2, 1)
                mutation_param_bioneat(ind, self.f1, self.f2, self.mut_pb)
            elif choice == 1: # Add Activation
                mutation_add_activation(ind)
            elif choice == 2: # Del Activation
                mutation_del_activation(ind)
            elif choice == 3: # Signal species
                mutation_bioneat_signal_species(ind)
            elif choice == 4: # Inhibition species
                mutation_bioneat_inhibition_species(ind)


            ## Verify if there are no orphaned nodes
            #is_orphaned = (not(any(ind.activations[:,i]) or any(ind.activations[i,:]) or any(ind.inhibitions[i,:,:].flatten())) for i in range(ind.nb_nodes))
            #if any(is_orphaned):
            #    continue

            # Assemble individual
            ind.assemble()
            # Verify if valid
            if ind.is_valid():
                # Verify if within bounds
                active_activations_coords = list(zip(*np.where(ind.activations)))
                nb_active_activations = len(active_activations_coords)
                active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
                nb_active_inhibitions = len(active_inhibitions_coords)
                if nb_active_activations >= self.nbConnActivationsDomain[0] and nb_active_activations <= self.nbConnActivationsDomain[1] and nb_active_inhibitions >= self.nbConnInhibitionsDomain[0] and nb_active_inhibitions <= self.nbConnInhibitionsDomain[1] and nb_active_activations + nb_active_inhibitions >= self.nbConnDomain[0] and nb_active_activations + nb_active_inhibitions <= self.nbConnDomain[1]:
                    break
            else:
                print(f"VARY: NOT VALID ! (choice={choice})")
                #raise RuntimeError(f"VARY: NOT VALID ! (choice={choice})")
        return ind


@registry.register
class DaccadBioneatMut_2step(Evolution):
    """Basic class for QD implementing BioNEAT mutations"""

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike,
            nb_nodes_domain: Sequence[int] = [1, 7],
            min_init_budget: int = 1,
            min_ind_found_in_init: int = 1,
            init_pb: float = 0.0,
            sel_pb: float = 1.0,
            prob_parameter_mut: float = 0.5,
            prob_template_add: float = 0.25,
            prob_template_del: float = 0.25,
            prob_signal_species_add: float = 0,
            prob_inhibition_species_add: float = 0,
            nbConnActivationsDomain: Sequence[int] = [1, 7],
            nbConnInhibitionsDomain: Sequence[int] = [0, 6],
            nbConnDomain: Sequence[int] = [1, 13],
            f1: float = 0.2,
            f2: float = 2.0,
            mut_pb: float = 0.8,
            init_drift: int = 1, #number of mutations applied on initial individuals
            **kwargs):
        self.ind_domain = ind_domain
        self.nb_nodes_domain = nb_nodes_domain
        self.min_init_budget = min_init_budget
        self.min_ind_found_in_init = min_ind_found_in_init
        self.init_pb = init_pb
        self.sel_pb = sel_pb
        self.prob_parameter_mut = prob_parameter_mut
        self.prob_template_add = prob_template_add
        self.prob_template_del = prob_template_del
        self.prob_signal_species_add = prob_signal_species_add
        self.prob_inhibition_species_add = prob_inhibition_species_add
        self.nbConnActivationsDomain = nbConnActivationsDomain
        self.nbConnInhibitionsDomain = nbConnInhibitionsDomain
        self.nbConnDomain = nbConnDomain
        self.f1 = f1
        self.f2 = f2
        self.mut_pb = 0.8
        self.init_drift = init_drift
        self.count = 0
        with open("./results/reservoir_jacobian_surrogate/final_" + "20220728011411" + ".p", "rb") as f:
            self.data = pickle.load(f)
        

        super().__init__(container, budget, select_or_initialise=self._select_or_initialise, vary=self._vary, base_ind_gen=gen_daccad_individuals(self.ind_domain), **kwargs)


    def _select_or_initialise(self, collection: Sequence[Any], base_ind: IndividualLike) -> Tuple[Any, bool]:
        initialise = self._nb_suggestions < self.min_init_budget or len(collection) < self.min_ind_found_in_init
        if not initialise:
            operation = np.random.choice(range(2), p=[self.sel_pb, self.init_pb])
            initialise = operation == 1

        if initialise: # Initialisation
            # Create a base individual
            
            # standard_init_ind(base_ind)
            if self.count < len(self.data["container"]):
                print("initialize")
                base_ind = self.data["container"][self.count]
            else:
                standard_init_ind(base_ind)
            for _ in range(self.init_drift):
                base_ind = self._vary(base_ind)
            self.count += 1
            return base_ind, False

        else: # Selection
            try:
                choice = np.random.choice(2)
                if choice == 0:
                    res = tools.non_trivial_sel_random(collection), True
                else:
                    res = tools.sel_random(collection), True
            except Exception as e:
                print(f"EXCEPTION ! {e}")
                traceback.print_exc()
            
            return res


    def _vary(self, individual):
        
        for _ in range(500): # Max number of retries to find a valid individual
            ind = copy.deepcopy(individual)
            ind.name = str(id(ind))

            active_activations_coords = list(zip(*np.where(ind.activations)))
            nb_active_activations = len(active_activations_coords)
            active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
            nb_active_inhibitions = len(active_inhibitions_coords)

            # Choose the kind of mutation
            choice = np.random.choice(5, p=(self.prob_parameter_mut,
                self.prob_template_add, self.prob_template_del,
                self.prob_signal_species_add, self.prob_inhibition_species_add))

            # Perform the mutation
            if choice == 0: # Parameters mutation
                #mutation_param_polybounded(ind, self.eta, self.mutationPb)
                #mutation_param_bioneat(ind, self.f1, self.f2, 1)
                mutation_param_bioneat(ind, self.f1, self.f2, self.mut_pb)
            elif choice == 1: # Add Activation
                mutation_add_activation(ind)
            elif choice == 2: # Del Activation
                mutation_del_activation(ind)
            elif choice == 3: # Signal species
                mutation_bioneat_signal_species(ind)
            elif choice == 4: # Inhibition species
                mutation_bioneat_inhibition_species(ind)


            ## Verify if there are no orphaned nodes
            #is_orphaned = (not(any(ind.activations[:,i]) or any(ind.activations[i,:]) or any(ind.inhibitions[i,:,:].flatten())) for i in range(ind.nb_nodes))
            #if any(is_orphaned):
            #    continue

            # Assemble individual
            ind.assemble()
            # Verify if valid
            if ind.is_valid():
                # Verify if within bounds
                active_activations_coords = list(zip(*np.where(ind.activations)))
                nb_active_activations = len(active_activations_coords)
                active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
                nb_active_inhibitions = len(active_inhibitions_coords)
                if nb_active_activations >= self.nbConnActivationsDomain[0] and nb_active_activations <= self.nbConnActivationsDomain[1] and nb_active_inhibitions >= self.nbConnInhibitionsDomain[0] and nb_active_inhibitions <= self.nbConnInhibitionsDomain[1] and nb_active_activations + nb_active_inhibitions >= self.nbConnDomain[0] and nb_active_activations + nb_active_inhibitions <= self.nbConnDomain[1]:
                    break
            else:
                print(f"VARY: NOT VALID ! (choice={choice})")
                #raise RuntimeError(f"VARY: NOT VALID ! (choice={choice})")
        return ind

