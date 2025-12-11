"""
graph_builder.py
"""
import networkx as nx


class GraphBuilder:
    """
    Graph implementation of a PEN system using networkx.
    Since PEN systems are not proper graphs (inhibitions are edges targeting other edges; predators use multi-edges), 
    we use hidden nodes (e.g., activation nodes) to represent those behaviors in the final view. 
    """
    def __init__(self):
        pass

    def build_graph(self, data: dict, show_inhibitors = True) -> nx.DiGraph:
        G = nx.DiGraph()

        # === Add nodes ===
        stabilities = data.get('stabilities')
        if stabilities is not None:
            for i, stability in enumerate(stabilities):
                node_id = f'{i}'
                G.add_node(node_id, stability=stability, type='normal')


        # === Add activation edges ===
        activations = data.get('activations')
        if activations is not None:
            for i in range(len(activations)):
                for j in range(len(activations[i])):
                    concentration = activations[i, j]
                    if concentration > 0:
                        # activation edge node id
                        aid = f'a{i}_{j}'
                        G.add_node(aid, type='activation_node', concentration=concentration, source = i, dest = j)
                        if i == j:
                            G.add_edge(f'{i}', f'{i}', type='autoactivation')
                        else:
                            G.add_edge(f'{i}', f'{j}', type='activation')  # from source node to activation node


        # Add inhibition edges
        inhibitions = data.get('inhibitions')
        if inhibitions is not None:
            for i in range(len(inhibitions)):
                for j in range(len(inhibitions[i])):
                    for k in range(len(inhibitions[i][j])):
                        concentration = inhibitions[i][j][k]
                        if concentration > 0:
                            aid = f'a{j}_{k}'
                            inhibid = f'{i}'
                            if show_inhibitors:
                                inhibid = f'I{j}_{k}'
                                G.add_node(inhibid, stability="calculated", type='normal')
                                G.add_edge(f'{i}', inhibid, type='activation')
                            G.add_edge(inhibid, aid, type='inhibition_edge', concentration=concentration)      # from source node to aid node

        # === Add predator-prey templates ===
        predator_templates = data.get('predator_prey_templates')
        if predator_templates is not None:
            for i, concentration in enumerate(predator_templates):
                if concentration > 0:
                    predator_id = f'pr{i}'
                    G.add_node(predator_id, type='predator_node')
                    G.add_edge(predator_id, f'{i}', type='predator_prey_edge', concentration=concentration)

        # === Add pseudo edges ===
        pseudo = data.get('pseudo_templates')
        if pseudo is not None:
            for i, concentration in enumerate(pseudo):
                if concentration > 0:
                    pseudo_id = f'ps{i}'
                    G.add_node(pseudo_id, type='pseudo_node')
                    G.add_edge(pseudo_id, f'{i}', type='pseudo_edge', concentration=concentration)

        return G
