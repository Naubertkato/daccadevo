import pytest
from daccadevo.individual import *
from daccadevo.mutation_utils import *


@pytest.fixture
def indiv_dom():
	return [0.0,200.0]

@pytest.fixture
def base_indiv(indiv_dom):
    return standard_init_ind(next(gen_daccad_individuals(indiv_dom)))

@pytest.fixture
def base_indiv0(indiv_dom):
    return standard_init_ind0(next(gen_daccad_individuals(indiv_dom)))

@pytest.fixture
def base_indiv_grad4(indiv_dom):
    return standard_init_ind_grad4(next(gen_daccad_individuals(indiv_dom)))

@pytest.fixture
def base_indiv_act(indiv_dom):
    return standard_init_act(next(gen_daccad_individuals(indiv_dom)))

# 29-31

@pytest.mark.parametrize('ind',["base_indiv", "base_indiv0", "base_indiv_grad4", "base_indiv_act"])
def test_update(ind, indiv_dom, request):
	ind = request.getfixturevalue(ind)
	vals = generateUniform(len(ind), indiv_dom, 1)[0]
	ind[:] = vals
	ind.update()
	for i in range(ind.nb_nodes):
		assert ind.stabilities[i] == vals[i]
	for i in range(ind.nb_nodes):
		for j in range(ind.nb_nodes):
			assert ind.activations[i,j] == vals[ind.nb_nodes+i*ind.nb_nodes+j]
	for i in range(ind.nb_nodes):
		for j in range(ind.nb_nodes):
			for k in range(ind.nb_nodes):
				assert ind.inhibitions[i,j,k] == vals[ind.nb_nodes+ind.nb_nodes*ind.nb_nodes+i*ind.nb_nodes*ind.nb_nodes+j*ind.nb_nodes+k]


 #41-43
@pytest.mark.parametrize('size',[1,3,5])
def test_resize(size, base_indiv):
	base_indiv.resize(size)
	assert base_indiv.nb_nodes == size
	assert base_indiv.is_valid()


#  59-66
def test_active_nodes(base_indiv):
	res = base_indiv.active_nodes()
	assert len(res) == 1 and (2 in res)
	base_indiv.activations[0,1] = 1.0
	base_indiv.assemble()
	res = base_indiv.active_nodes()
	assert len(res) == 3 and (0 in res) and (1 in res)

# 69-80, 84, 88-90
# valid indexes + values
