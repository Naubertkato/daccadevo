"""
view.py
"""
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QPointF, QEasingCurve
import networkx as nx
from daccadevo.visualization.nodes import ActivationNode
from daccadevo.visualization.scene_builder import SceneBuilder

class GraphView(QGraphicsView):
    def __init__(self, graph: nx.DiGraph, parent=None):
        """GraphView constructor

        This widget can display a directed graph

        Args:
            graph (nx.DiGraph): a networkx directed graph
        """
        super().__init__()
        self._graph = graph
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        self._graph_scale = 200

        self.nodes_map = {}

        self._nx_layout = {
            "circular": nx.circular_layout,
            "planar": nx.planar_layout,
            "random": nx.random_layout,
            "shell_layout": nx.shell_layout,
            "kamada_kawai_layout": nx.kamada_kawai_layout,
            "spring_layout": nx.spring_layout,
            "spiral_layout": nx.spiral_layout,
        }

        self._load_graph()
        self.set_nx_layout("circular")

    def get_nx_layouts(self) -> list:
        """Return all layout names

        Returns:
            list: layout name (str)
        """
        return self._nx_layout.keys()

    def set_nx_layout(self, name: str):
        """Set networkx layout and start animation

        Args:
            name (str): Layout name
        """
        if name in self._nx_layout:
            self._nx_layout_function = self._nx_layout[name]

            # Compute node position from layout function
            positions = self._nx_layout_function(self._graph)

            # Change position of all nodes using an animation
            self.animations = QParallelAnimationGroup()

            for node, pos in positions.items():   
                item = self.nodes_map[node]
                if not isinstance(item, ActivationNode):
                    x, y = positions[node]
                    x *= self._graph_scale
                    y *= self._graph_scale 
                else:
                    midpoint = item.activationedge.get_midpoint()
                    x = midpoint.x()
                    y = midpoint.y()

                item.setPos(x, y)   
                if hasattr(item, "_edges"):
                    for edge in item._edges:
                        edge.adjust()     
                
                
                animation = QPropertyAnimation(item, b"pos")
                animation.setDuration(1000)
                animation.setEndValue(QPointF(x, y))
                animation.setEasingCurve(QEasingCurve.Type.OutExpo)
                self.animations.addAnimation(animation)
            self.animations.start()
    
    def _load_graph(self):
        """Load graph into QGraphicsScene using SceneBuilder"""
        self.scene().clear()
        self.nodes_map.clear()

        builder = SceneBuilder(self._graph, self._scene, self.nodes_map)
        builder.build_scene()
