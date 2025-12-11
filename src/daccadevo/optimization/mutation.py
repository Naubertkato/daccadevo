import copy
import math
import random

import numpy as np
from qdpy import tools

from daccadevo.core.mutation_utils import random_log_scale, random_log_scale_1000

#### Functions to perform mutation operations on PEN DNA toolbox systems introduced by Aubert-Kato et al. 2017

def mutation_param_polybounded(ind, eta, mut_pb):
    tools.mut_polynomial_bounded(ind.stabilities, eta=eta, low=ind.ind_domain[0], up=ind.ind_domain[1], mut_pb=mut_pb)
    ind.activations[np.where(ind.activations)] = tools.mut_polynomial_bounded(ind.activations[np.where(ind.activations)], eta=eta, low=ind.ind_domain[0], up=ind.ind_domain[1], mut_pb=mut_pb)
    ind.inhibitions[np.where(ind.inhibitions)] = tools.mut_polynomial_bounded(ind.inhibitions[np.where(ind.inhibitions)], eta=eta, low=ind.ind_domain[0], up=ind.ind_domain[1], mut_pb=mut_pb)

def mutation_param_reinit(ind):
    ind.stabilities = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1], len(ind.stabilities))
    ind.activations[np.where(ind.activations)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1], len(ind.activations[np.where(ind.activations)]))
    ind.inhibitions[np.where(ind.inhibitions)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1], len(ind.inhibitions[np.where(ind.inhibitions)]))


def mutation_add_activation(ind, trivial=False):
    activations_coords_set = {(x, y) for x in range(ind.nb_nodes) for y in range(ind.nb_nodes)}
    active_activations_coords = list(zip(*np.where(ind.activations)))
    inactive_activations_coords = list(activations_coords_set - set(active_activations_coords))
    if len(inactive_activations_coords) == 0:
        return
    if trivial:
        ind.activations[random.choice(inactive_activations_coords)] = 0.0000015
    else:
        ind.activations[random.choice(inactive_activations_coords)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])


# Make sure that the activation is added to a node with already an activation
def mutation_add_activation2(ind, trivial=False):
    activations_coords_set = {(x, y) for x in range(ind.nb_nodes) for y in range(ind.nb_nodes)}
    active_activations_coords = list(zip(*np.where(ind.activations)))
    inactive_activations_coords = list(activations_coords_set - set(active_activations_coords))
    active_nodes = ind.active_nodes()
    candidates_activations = []
    for c in inactive_activations_coords:
        if c[0] in active_nodes or c[1] in active_nodes:
            candidates_activations.append(c)
    if len(candidates_activations) == 0:
        return
    if trivial:
        ind.activations[random.choice(candidates_activations)] = 0.0000015
    else:
        ind.activations[random.choice(candidates_activations)] = random_log_scale()


def mutation_add_activation_with_gradients(ind, trivial=False, gradients=[0,1]):
    activations_coords_set = {(x, y) for x in range(ind.nb_nodes) for y in range(ind.nb_nodes)}
    activations_coords_set -= {(x, y) for x in range(ind.nb_nodes) for y in gradients}
    active_activations_coords = list(zip(*np.where(ind.activations)))
    inactive_activations_coords = list(activations_coords_set - set(active_activations_coords))
    if trivial:
        ind.activations[random.choice(inactive_activations_coords)] = 0.0051
    else:
        ind.activations[random.choice(inactive_activations_coords)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])


def mutation_del_activation(ind):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    coord = random.choice(active_activations_coords)
    ind.activations[coord] = 0.
    # Remove invalid inhibitions
    for i in range(ind.nb_nodes):
        ind.inhibitions[(i,) + coord] = 0.


def mutation_add_inhibition(ind, trivial=False):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
    allowed_inhibitions_coords = []
    for coord in active_activations_coords:
        # Verify if there are not already an inhibition on this template
        already_an_inhibition = np.any(ind.inhibitions[:, coord[0], coord[1]])
        if already_an_inhibition:
            continue
        # Register an inhibition
        target_nodes = list(range(ind.nb_nodes))
        np.random.shuffle(target_nodes)
        for i in target_nodes:
            coord2 = (i,) + coord
            if coord2 not in active_inhibitions_coords:
                allowed_inhibitions_coords.append(coord2)
                break
    if len(allowed_inhibitions_coords):
        if trivial:
            ind.inhibitions[random.choice(allowed_inhibitions_coords)] = 0.0000015
        else:
            ind.inhibitions[random.choice(allowed_inhibitions_coords)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    else:
        # No remaining place to put an inhibition, delete one instead
        ind.inhibitions[random.choice(active_inhibitions_coords)] = 0.

def mutation_del_inhibition(ind):
    active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
    if len(active_inhibitions_coords):
        ind.inhibitions[random.choice(active_inhibitions_coords)] = 0.
    else:
        # No inhibition found, add one instead
        mutation_add_inhibition(ind)

def mutation_add_node(ind, trivial=False):
    ind.resize(ind.nb_nodes+1)

    active_activations_coords = list(zip(*np.where(ind.activations)))
    allowed_inhibitions_coords = []
    for coord in active_activations_coords:
        coord2 = (ind.nb_nodes-1,) + coord
        allowed_inhibitions_coords.append(coord2)

    choice2 = np.random.choice(5) if len(allowed_inhibitions_coords) else np.random.choice(3)
    if trivial:
        if choice2 == 0:
            ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = 0.0000015
        elif choice2 == 1:
            ind.activations[-1, np.random.choice(ind.nb_nodes-1)] = 0.0000015
        elif choice2 == 2:
            ind.activations[np.random.choice(ind.nb_nodes-1), -1] = 0.0000015
        elif choice2 == 3 or choice2 == 4:
            ind.inhibitions[random.choice(allowed_inhibitions_coords)] = 0.0000015
            ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = 0.0000015
    elif choice2 == 0:
        ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 1:
        ind.activations[-1, np.random.choice(ind.nb_nodes-1)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 2:
        ind.activations[np.random.choice(ind.nb_nodes-1), -1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 3 or choice2 == 4:
        ind.inhibitions[random.choice(allowed_inhibitions_coords)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
        ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])

def mutation_add_node_with_gradients(ind, trivial=False, gradients=[0,1]):
    ind.resize(ind.nb_nodes+1)

    active_activations_coords = list(zip(*np.where(ind.activations)))
    allowed_inhibitions_coords = []
    for coord in active_activations_coords:
        coord2 = (ind.nb_nodes-1,) + coord
        allowed_inhibitions_coords.append(coord2)

    choice2 = np.random.choice(5) if len(allowed_inhibitions_coords) else np.random.choice(3)
    if trivial:
        if choice2 == 0:
            ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = 0.0051
        elif choice2 == 1:
            to_node = np.random.choice(list(set(range(ind.nb_nodes-1)) - set(gradients)))
            ind.activations[-1, to_node] = 0.0051
        elif choice2 == 2:
            ind.activations[np.random.choice(ind.nb_nodes-1), -1] = 0.0051
        elif choice2 == 3 or choice2 == 4:
            ind.inhibitions[random.choice(allowed_inhibitions_coords)] = 0.0051
            ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = 0.0051
    elif choice2 == 0:
        ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 1:
        to_node = np.random.choice(list(set(range(ind.nb_nodes-1)) - set(gradients)))
        ind.activations[-1, to_node] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 2:
        ind.activations[np.random.choice(ind.nb_nodes-1), -1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
    elif choice2 == 3 or choice2 == 4:
        ind.inhibitions[random.choice(allowed_inhibitions_coords)] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
        ind.activations[ind.nb_nodes-1, ind.nb_nodes-1] = np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])

def mutation_del_node(ind):
    node_to_del = np.random.choice(ind.nb_nodes)
    ind.nb_nodes -= 1
    mask_activations = np.ones_like(ind.activations, dtype=bool)
    mask_activations[node_to_del, :] = mask_activations[:, node_to_del] = False
    ind.activations = ind.activations[mask_activations].reshape((ind.nb_nodes, ind.nb_nodes))
    mask_inhibitions = np.ones_like(ind.inhibitions, dtype=bool)
    mask_inhibitions[node_to_del, :, :] = mask_inhibitions[:, node_to_del, :] = mask_inhibitions[:, :, node_to_del] = False
    ind.inhibitions = ind.inhibitions[mask_inhibitions].reshape((ind.nb_nodes, ind.nb_nodes, ind.nb_nodes))
    ind.stabilities = np.delete(ind.stabilities, node_to_del)


def mutation_bioneat_signal_species(ind, trivial=False):
    choice = np.random.choice(2)
    if choice == 0: # a->b becomes a->c->b
        ind.resize(ind.nb_nodes+1)
        active_activations_coords = list(zip(*np.where(ind.activations)))
        old_activation_coord = random.choice(active_activations_coords)
        ind.activations[old_activation_coord[0], -1] = ind.activations[old_activation_coord]
        ind.activations[old_activation_coord] = 0.
        ind.activations[-1, old_activation_coord[1]] = ind.activations[old_activation_coord]
        ind.inhibitions[:,old_activation_coord[0], -1] = ind.inhibitions[:,old_activation_coord[0],old_activation_coord[1]]
        ind.inhibitions[:,old_activation_coord[0],old_activation_coord[1]] = 0.
        ind.stabilities[-1] = random_log_scale_1000()

    else: # Add node x->x and x->y with y a random signal
        signal_id = np.random.choice(ind.nb_nodes)
        ind.resize(ind.nb_nodes+1)
        if trivial:
            ind.activations[-1, -1] = 0.0000015
            ind.activations[-1, signal_id] = 0.0000015
            ind.stabilities[-1] = random_log_scale_1000()
        else:
            ind.activations[-1, -1] = random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
            ind.activations[-1, signal_id] = random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])
            ind.stabilities[-1] = random_log_scale_1000()


# Only applicable if not all templates present
def mutation_bioneat_inhibition_species(ind, trivial=False):
    activations_coords_set = {(x, y) for x in range(ind.nb_nodes) for y in range(ind.nb_nodes)}
    active_activations_coords = list(zip(*np.where(ind.activations)))
    inactive_activations_coords = list(activations_coords_set - set(active_activations_coords))

    choice = np.random.choice(2)
    if choice == 0 or len(inactive_activations_coords) == 0:
        # Inhibition add
        mutation_add_inhibition(ind, trivial)
        return

    # Add a template + inhibition of this template
    added_activation_coord = random.choice(inactive_activations_coords)
    if trivial:
        ind.activations[added_activation_coord] = 0.0000015
    else:
        ind.activations[added_activation_coord] = random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])

    # Determine the origin of the inhibition
    list_nodes = list(range(ind.nb_nodes))
    list_nodes.remove(added_activation_coord[0])
    if added_activation_coord[1] in list_nodes:
        list_nodes.remove(added_activation_coord[1])

    if len(list_nodes) == 0: # no room left, just mutate the parameters then
        # Note that most run should limit the maximum number of inhibitions to avoid this,
        # but it can still happen for very small networks
        list_nodes = list(range(ind.nb_nodes))
    chosen_inhibition_coord = (random.choice(list_nodes),) + added_activation_coord

    if trivial:
        ind.inhibitions[chosen_inhibition_coord] = 0.0000015
    else:
        ind.inhibitions[chosen_inhibition_coord] = random_log_scale() #np.random.uniform(ind.ind_domain[0], ind.ind_domain[1])



# Only applicable if there is at least one template
def disable_template(ind, mut_pb=0.8, disabling_pb=0.1):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    for coord in active_activations_coords:
        if random.random() < mut_pb:
            if random.random() < min(1., max(0., disabling_pb - math.log10(ind.activations[coord] / 10.))):
                ind.activations[coord] = 0.
                for i in range(ind.nb_nodes): # Remove invalid inhibitions
                    ind.inhibitions[(i,) + coord] = 0.
    active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
    for coord in active_inhibitions_coords:
        if random.random() < mut_pb:
            if random.random() < min(1., max(0., disabling_pb - math.log10(ind.inhibitions[coord] / 10.))):
                ind.inhibitions[coord] = 0.


#double mutatedParam = Math.exp(Math.log(oldParam) * (1 + randGaussian * 0.2)) + randGaussian * 2;
def mutate_one_param_bioneat(old, ind_domain, f1=0.2, f2=2., max_bound=200.):
    gauss = random.gauss(0., 1.)
    res = (math.exp(math.log(old * max_bound) * (1. + gauss * f1)) + gauss * f2) / max_bound
    if res < ind_domain[0]+0.0051:
        return ind_domain[0]+0.0051
    if res > ind_domain[1]:
        return ind_domain[1]
    return res

def mutation_param_bioneat(ind, f1=0.2, f2=2.0, mut_pb=0.8):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
    for i, old in enumerate(ind.stabilities):
        if random.random() < mut_pb:
            ind.stabilities[i] = mutate_one_param_bioneat(old, ind.ind_domain, f1, f2, 1000.)
    for coord in active_activations_coords:
        if random.random() < mut_pb:
            ind.activations[coord] = mutate_one_param_bioneat(ind.activations[coord], ind.ind_domain, f1, f2, 200.)
    for coord in active_inhibitions_coords:
        if random.random() < mut_pb:
            ind.inhibitions[coord] = mutate_one_param_bioneat(ind.inhibitions[coord], ind.ind_domain, f1, f2, 200.)


# Mutation for Reaction-Diffusion systems where gradients nodes are inputs from the environment (thus cannot be changed)
def add_node_with_gradients(ind, gradients=[0,1]):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    # active_inhibitions_coords = list(zip(*np.where(ind.inhibitions))) # TODO: Handle inhibitions?
    if random.random() < 1. / (len(active_activations_coords) + 1.) or len(active_activations_coords) == 0:
        if np.random.choice(2) or len(active_activations_coords) == 0:
            ind.resize(ind.nb_nodes+1)
            ind.stabilities[-1] = random_log_scale_1000()
            ind.activations[-1, -1] = random_log_scale()
            to_node = np.random.choice(list(set(range(ind.nb_nodes)) - set(gradients)))
            ind.activations[-1, to_node] = random_log_scale()
        else:
            selected_activation = random.choice(active_activations_coords)
            ind.resize(ind.nb_nodes+1)
            ind.stabilities[-1] = random_log_scale_1000()
            ind.activations[-1, -1] = random_log_scale()
            ind.inhibitions[-1, selected_activation[0],selected_activation[1]] = random_log_scale()
    else: # TODO: Handle inhibitions?
        selected_activation = random.choice(active_activations_coords)
        def get_back_template(templace_coord):
            active_out_coords = [(templace_coord[0], x) for x in np.where(ind.activations[templace_coord[0],:])[0]]
            count_out = len(active_out_coords)
            active_in_coords = [(x, templace_coord[0]) for x in np.where(ind.activations[:,templace_coord[0]])[0]]
            if templace_coord in active_in_coords:
                active_in_coords.remove(templace_coord)
            count_in = len(active_in_coords)
            return active_in_coords[0] if count_in == 1 and count_out == 1 else None
        def get_correct_template(templace_coord):
            coord = templace_coord
            while(True):
                next_coord = get_back_template(coord)
                if next_coord is None or next_coord == templace_coord:
                    break
                coord = next_coord
            return coord
        activation = get_correct_template(selected_activation)
        old_activation_val = ind.activations[activation]
        ind.activations[activation] = 0.
        for i in range(ind.nb_nodes): # Remove invalid inhibitions
            ind.inhibitions[(i,) + activation] = 0.
        ind.resize(ind.nb_nodes+1)
        ind.stabilities[-1] = random_log_scale_1000()
        ind.activations[activation[0], -1] = old_activation_val # random_log_scale() # TODO Handle inhibitions
        ind.activations[-1, activation[1]] = old_activation_val


class NotApplicableError(Exception):
    pass


# Only applicable if all activations are not already set
# Add a new connection to a non-input species
def add_activation_with_gradients(ind, gradients=[0,1]):
    activations_coords_set = {(x, y) for x in range(ind.nb_nodes) for y in range(ind.nb_nodes)}
    activations_coords_set -= {(x, y) for x in range(ind.nb_nodes) for y in gradients}
    active_activations_coords = list(zip(*np.where(ind.activations)))
    inactive_activations_coords = list(activations_coords_set - set(active_activations_coords))
    if len(inactive_activations_coords) == 0:
        #return
        raise NotApplicableError("Not applicable")
    ind.activations[random.choice(inactive_activations_coords)] = random_log_scale()


# Only applicable if all inhibitions are not already set
# 50% chance flip
# Add an inhibition, potentially turning an activation into a double inhibition
# Input ("gradient") species cannot be targeted.
def add_inhibition_with_gradients(ind, gradients=[0,1]):
    def add_inhibition(node_from, node_to):
        possibles_templates_from = np.where(ind.activations[:, node_to])[0]
        if len(possibles_templates_from) == 0:
            selected_template = (node_to, node_to)
            ind.activations[selected_template] = random_log_scale()
        else:
            selected_template = (random.choice(possibles_templates_from), node_to)
        ind.inhibitions[node_from, selected_template[0], selected_template[1]] = random_log_scale()

    active_activations_coords = list(zip(*np.where(ind.activations)))
    choice = np.random.choice(2)
    if choice == 0 or len(active_activations_coords) == 0: # Add simple inhibition
        node_from = np.random.choice(ind.nb_nodes)
        node_to = np.random.choice(list(set(range(ind.nb_nodes)) - set(gradients)))
        add_inhibition(node_from, node_to)
    else: # Replace an activation with a double inhibition
        selected_activation = random.choice(active_activations_coords)
        # Remove selected activation
        ind.activations[selected_activation] = 0.
        # Remove invalid inhibitions
        for i in range(ind.nb_nodes):
            ind.inhibitions[(i,) + selected_activation] = 0.
        # Add double inhibition
        ind.resize(ind.nb_nodes+1)
        new_node = ind.nb_nodes-1
        ind.stabilities[new_node] = random_log_scale_1000()
        add_inhibition(selected_activation[0], new_node)
        add_inhibition(new_node, selected_activation[1])


def clone_activation(ind, base_activation):
    base_activation_conc = ind.activations[base_activation]
    ind.resize(ind.nb_nodes+1)
    ind.stabilities[-1] = random_log_scale_1000()
    ind.activations[base_activation[0], -1] = base_activation_conc
    ind.activations[-1, base_activation[1]] = base_activation_conc

def clone_inhibition(ind, base_inhibition):
    base_inhibition_conc = ind.inhibitions[base_inhibition]
    node_from, templ0, templ1 = base_inhibition
    ind.resize(ind.nb_nodes+1)
    ind.stabilities[-1] = random_log_scale_1000()
    ind.activations[node_from, -1] = base_inhibition_conc
    ind.inhibitions[-1, templ0, templ1] = base_inhibition_conc

def mutation_clone_activation(ind):
    active_activations_coords = list(zip(*np.where(ind.activations)))
    if len(active_activations_coords) == 0:
        raise NotApplicableError("Not applicable")
    base_activation = random.choice(active_activations_coords)
    clone_activation(ind, base_activation)

def mutation_clone_inhibition(ind):
    active_inhibitions_coords = list(zip(*np.where(ind.inhibitions)))
    if len(active_inhibitions_coords) == 0:
        raise NotApplicableError("Not applicable")
    base_inhibition = random.choice(active_inhibitions_coords)
    clone_inhibition(ind, base_inhibition)

def mutation_clone_template(ind):
    if np.random.choice(2):
        mutation_clone_activation(ind)
    else:
        mutation_clone_inhibition(ind)


def crossover_uniform(ind1, ind2, prob):
    min_nb_nodes = min(ind1.nb_nodes, ind2.nb_nodes)
    ind1_active_activations_coords = list(zip(*np.where(ind1.activations)))
    ind1_active_inhibitions_coords = list(zip(*np.where(ind1.inhibitions)))
    ind2_active_activations_coords = list(zip(*np.where(ind2.activations)))
    ind2_active_inhibitions_coords = list(zip(*np.where(ind2.inhibitions)))
    new_ind1 = copy.deepcopy(ind1)
    new_ind2 = copy.deepcopy(ind2)

    for x, y in ind1_active_activations_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes:
            new_ind1.activations[x, y], new_ind2.activations[x, y] = ind2.activations[x, y], ind1.activations[x, y]
    for x, y in ind2_active_activations_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes:
            new_ind1.activations[x, y], new_ind2.activations[x, y] = ind2.activations[x, y], ind1.activations[x, y]

    for x, y, z in ind1_active_inhibitions_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes and z < min_nb_nodes:
            new_ind1.inhibitions[x, y, z], new_ind2.inhibitions[x, y, z] = ind2.inhibitions[x, y, z], ind1.inhibitions[x, y, z]
    for x, y, z in ind2_active_inhibitions_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes and z < min_nb_nodes:
            new_ind1.inhibitions[x, y, z], new_ind2.inhibitions[x, y, z] = ind2.inhibitions[x, y, z], ind1.inhibitions[x, y, z]
    return new_ind1, new_ind2



def crossover_uniform2(ind1, ind2, prob):
    min_nb_nodes = min(ind1.nb_nodes, ind2.nb_nodes)
    ind1_active_activations_coords = list(zip(*np.where(ind1.activations)))
    ind2_active_activations_coords = list(zip(*np.where(ind2.activations)))
    new_ind1 = copy.deepcopy(ind1)
    new_ind2 = copy.deepcopy(ind2)

    for x, y in ind1_active_activations_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes:
            new_ind1.activations[x, y], new_ind2.activations[x, y] = ind2.activations[x, y], ind1.activations[x, y]
            for z in range(min_nb_nodes):
                new_ind1.inhibitions[z, x, y], new_ind2.inhibitions[z, x, y] = ind2.inhibitions[z, x, y], ind1.inhibitions[z, x, y]
    for x, y in ind2_active_activations_coords:
        if random.random() < prob and x < min_nb_nodes and y < min_nb_nodes:
            new_ind1.activations[x, y], new_ind2.activations[x, y] = ind2.activations[x, y], ind1.activations[x, y]
            for z in range(min_nb_nodes):
                new_ind1.inhibitions[z, x, y], new_ind2.inhibitions[z, x, y] = ind2.inhibitions[z, x, y], ind1.inhibitions[z, x, y]

    return new_ind1, new_ind2
