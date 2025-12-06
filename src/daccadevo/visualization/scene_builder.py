"""
scene_builder.py
"""

from daccadevo.visualization.nodes import NormalNode, PseudoNode, PredatorNode, ActivationNode
from daccadevo.visualization.edges import ActivationEdge, AutoActivationEdge, InhibitorEdge, PseudoEdge, PredatorPreyEdge
from daccadevo.visualization.edge import Edge

class SceneBuilder:
    def __init__(self, graph, scene, nodes_map):
        self.graph = graph
        self.scene = scene
        self.nodes_map = nodes_map
        self.activation_nodes = {}  # Represents the target of inhibition species
        self.pseudo_nodes = {}

    def build_scene(self):
        self.scene.clear()
        self.nodes_map.clear()

        # === Add nodes ===
        for node_id, attr in self.graph.nodes(data=True):
            node_type = attr.get("type")
            if node_type == "activation_node":
                item = ActivationNode(node_id)
            elif node_type == "pseudo_node":
                item = PseudoNode(node_id)
            elif node_type == "predator_node":
                item = PredatorNode(node_id)
            else:
                item = NormalNode(node_id)

            self.scene.addItem(item)
            self.nodes_map[node_id] = item

        # === Add edges ===        
        for source_id, dest_id, attr in self.graph.edges(data=True):
            edge_type = attr.get("type")
            source = self.nodes_map[source_id]
            dest = self.nodes_map[dest_id]

            if edge_type == "activation":
                edge = ActivationEdge(source, dest)
                aid = f'a{source_id}_{dest_id}'
                if aid in self.nodes_map:
                    # Template can be inhibited, otherwise not
                    self.nodes_map[aid].activationedge = edge
                    self.nodes_map[aid].source = source
                    self.nodes_map[aid].dest = dest
                    self.activation_nodes[(source_id, dest_id)] = self.nodes_map[aid]
                self.scene.addItem(edge)

            elif edge_type == "autoactivation":
                edge = AutoActivationEdge(source, dest)
                aid = f'a{source_id}_{dest_id}'
                self.nodes_map[aid].activaionedge = edge
                self.nodes_map[aid].source = source
                self.nodes_map[aid].dest = dest
                self.activation_nodes[(source_id, dest_id)] = self.nodes_map[aid]
                self.scene.addItem(edge)


            elif edge_type == "predator_prey_edge":
                edge = PredatorPreyEdge(source, dest)
                self.scene.addItem(edge)

            elif edge_type == "inhibition_edge":
                edge = InhibitorEdge(source, dest)
                self.scene.addItem(edge)

            elif edge_type == "pseudo_edge":
                edge = PseudoEdge(source, dest)
                self.nodes_map[source_id].pseudoedge = edge
                self.pseudo_nodes[(source_id, dest_id)] = self.nodes_map[source_id]
                self.scene.addItem(edge)

            else:
                edge = Edge(source, dest)
                self.scene.addItem(edge)

            source.add_edge(edge)
            dest.add_edge(edge)

        self.scene.activation_nodes = self.activation_nodes
        self.scene.pseudo_nodes = self.pseudo_nodes