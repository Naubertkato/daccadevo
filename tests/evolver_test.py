import pytest
from daccadevo.evolver import DaccadBioneatMut
from qdpy.containers import *
from daccadevo.individual import *


@pytest.fixture
def evolver(): 
    grid = Grid(shape=(10,10), max_items_per_bin=1, fitness_domain=((0., 1.),), features_domain=((0., 1.), (0., 1.)))
    return DaccadBioneatMut(grid, 10, [0.0,200.0], optimisation_task="max")

@pytest.fixture
def evolver_full(evolver): 
    for i in range(5):
        a = evolver.ask()
        evolver.tell(a,fitness=[0.1],features=[0.0,float(i)/5.0])
    return evolver

@pytest.fixture
def evolver_custom_gen(): 
    grid = Grid(shape=(10,10), max_items_per_bin=1, fitness_domain=((0., 1.),), features_domain=((0., 1.), (0., 1.)))
    return DaccadBioneatMut(grid, 10, [0.0,200.0],init_ind="standard_init_ind0", optimisation_task="max")

@pytest.fixture
def base_indiv(evolver):
    return standard_init_ind(next(gen_daccad_individuals(evolver.ind_domain)))

@pytest.fixture
def base_indiv0(evolver_custom_gen):
    return standard_init_ind0(next(gen_daccad_individuals(evolver_custom_gen.ind_domain)))

@pytest.mark.parametrize('ind,result',
                             [("base_indiv",3), ("base_indiv0",1)])
def test_base_indiv(ind, result, request):
    ind = request.getfixturevalue(ind)
    assert ind is not None
    assert ind.nb_nodes == result
    print(len(ind.stabilities), len(ind.activations), len(ind))
    assert ind.is_valid()

@pytest.mark.parametrize('evo,ind',
                             [("evolver","base_indiv"), ("evolver_full","base_indiv"), ("evolver_custom_gen","base_indiv0")])
def test_evolver_tell(evo, ind, request):
    evo = request.getfixturevalue(evo)
    ind = request.getfixturevalue(ind)
    size = evo.container.size
    assert evo.budget == 10
    evo.tell(ind,fitness=[1.0],features=[0.5,0.5])
    assert evo.container.size == size + 1
    assert evo.best() == ind

# Check if we are initializing or selecting from collection when asking
@pytest.mark.parametrize('evo,ind,result',
                             [("evolver","base_indiv",False), ("evolver_full","base_indiv",True), ("evolver_custom_gen","base_indiv0",False)])
def test_evolver_ask(evo, ind, result, request):
    evo = request.getfixturevalue(evo)
    ind = request.getfixturevalue(ind)
    _, res = evo._select_or_initialise(evo.container,ind)
    assert res == result

# test exceptions when dealing with an incorrectly parametered evolver
@pytest.mark.parametrize('evo',["evolver","evolver_custom_gen"])
def test_selection_fail(evo, request):
    evo = request.getfixturevalue(evo)
    evo.min_init_budget = 0
    evo.min_ind_found_in_init = 0
    with pytest.raises(Exception) as e_info:
        evo.ask()

@pytest.mark.parametrize('evo,ind',
                             [("evolver","base_indiv"), ("evolver_custom_gen","base_indiv0")])
def test_mutation_rnd(evo, ind, request):
    evo = request.getfixturevalue(evo)
    ind = request.getfixturevalue(ind)

    # check random applications of mutations
    indiv_list = [ind]
    for _ in range(100):
        indiv_list.append(evo._vary(indiv_list[-1]))

    
    assert all(i.nb_nodes > 0 for i in indiv_list)
    assert all(i.is_valid for i in indiv_list)
    def get_vals_helper(ind):
        active_activations_coords = list(zip(*np.where(ind.activations)))
        nb_active_activations = len(active_activations_coords)
        active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
        nb_active_inhibitions = len(active_inhibitions_coords)
        return nb_active_activations, nb_active_inhibitions
    vals = [get_vals_helper(i) for i in indiv_list]  
    assert all(a>= evo.nbConnActivationsDomain[0] and a <= evo.nbConnActivationsDomain[1] and b >= evo.nbConnInhibitionsDomain[0] \
        and b <= evo.nbConnInhibitionsDomain[1] and a + b >= evo.nbConnDomain[0] and a + b <= evo.nbConnDomain[1] for a,b in vals)


@pytest.mark.parametrize('evo,ind',
                             [("evolver","base_indiv"), ("evolver_custom_gen","base_indiv0")])
def test_individual_mutations(evo, ind, request):
    evo = request.getfixturevalue(evo)
    ind = request.getfixturevalue(ind)
    probs = ["prob_parameter_mut","prob_template_add", "prob_template_del", "prob_signal_species_add", "prob_inhibition_species_add"]
    indiv_list = []
    for p in probs:
        for q in probs:
            setattr(evo,q,0.0)
        setattr(evo,p,1.0)
        for _ in range(20):
            indiv_list.append(evo._vary(ind))
    assert all(i.nb_nodes > 0 for i in indiv_list)
    assert all(i.is_valid for i in indiv_list)


def test_invalid_vary(evolver, base_indiv0):
    base_indiv0.activations[0,0] = 0.0
    base_indiv0.inhibitions[0,0,0] = 1.0
    base_indiv0.assemble()
    evolver.prob_parameter_mut = 1.0
    evolver.prob_template_add = 0.0
    evolver.prob_template_del = 0.0
    evolver.prob_signal_species_add = 0.0
    evolver.prob_inhibition_species_add = 0.0
    err = evolver._vary(base_indiv0)
    assert not err.is_valid()

def test_species(evolver_full):
    import time
    evolver_full.min_init_budget = 100
    evolver_full.min_ind_found_in_init = 100
    ind_a = evolver_full.ask() # should be new
    ind_b = evolver_full.ask() # should be new
    evolver_full.min_init_budget = 0
    evolver_full.min_ind_found_in_init = 0
    ind_c = evolver_full.ask() # should come from the collection
    ind_d = evolver_full.ask() # should come from the collection
    for ind in [ind_b, ind_c, ind_d]:
        assert not ind_a.same_species_as(ind)
    assert not ind_b.same_species_as(ind_c)
    assert ind_c.same_species_as(ind_d)


