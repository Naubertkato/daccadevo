"""
inhibitor.py
"""
from __future__ import annotations

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QPointF, QLineF
from PySide6.QtGui import QPainter, QPen, QColor
import math
from daccadevo.visualization.edge import Edge
from daccadevo.visualization.node import Node

class InhibitorEdge(Edge):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        super().__init__(source, dest, parent)
        self._color = "#4C34EB" # blue
        self._arrow_size = 6 

    def adjust(self):
        super().adjust()
        self._arrow_tip = self.arrow_target()
    
    def draw_edge(self, painter: QPainter):
        start = self._line.p1()
        tip = self._arrow_tip
        self.draw_line(painter, start, tip)
        self._draw_inhibition_head(painter, tip)

    def _draw_inhibition_head(self, painter: QPainter, tip: QPointF):
        size = self._arrow_size
        line = QLineF(self._line.p2(), self._line.p1())
        angle = math.atan2(-line.dy(), line.dx())

        p1 = tip + QPointF(math.sin(angle) * size, math.cos(angle) * size)
        p2 = tip - QPointF(math.sin(angle) * size, math.cos(angle) * size)

        pen = QPen(QColor(self._color))
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawLine(p1, p2)