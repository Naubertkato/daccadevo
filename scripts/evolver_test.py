from evolver import DaccadBioneatMut
from qdpy.containers import *
from individual import *

if __name__ == "__main__":
    grid = Grid(shape=(10,10), max_items_per_bin=1, fitness_domain=((0., 1.),), features_domain=((0., 1.), (0., 1.)))
    evo = DaccadBioneatMut(grid, 10, [0.0,200.0])

    indiv = evo.ask()
    print(indiv)

    for _ in range(100):
        indiv = evo._vary(indiv)
    print("="*10,"\n",indiv)
