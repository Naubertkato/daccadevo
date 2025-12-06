"""
autoactivation.py
"""
from __future__ import annotations


from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QPainter
from daccadevo.visualization.edge import Edge
from daccadevo.visualization.node import Node

class AutoActivationEdge(Edge):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        super().__init__(source, dest, parent)
        self._color = "#2EE3F0"   #light blue
        

    def draw_edge(self, painter: QPainter):
        self.draw_arc(painter, self._loop_rect, self._loop_angle, radius=self.source._radius, arrow_size=self._arrow_size, span_angle=270)
