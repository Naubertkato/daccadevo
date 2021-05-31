import numpy as np
from individual import *
from mutation import *



if __name__ == "__main__":
    ind = next(gen_daccad_individuals([0.,200.]))
    standard_init_ind0(ind)
    print("Base:",ind)
    print("Is valid:",ind.is_valid())
    print('='*10)
    for _ in range(2):
        val = np.random.choice(3,p=[0.1,0.5,0.4])
        if val == 0:
            mutation_add_node(ind)
        elif val == 1:
            mutation_add_activation(ind)
        else:
            mutation_add_inhibition(ind)
        ind.assemble()
    print("Mutated:",ind)
    print("Is valid:",ind.is_valid())
