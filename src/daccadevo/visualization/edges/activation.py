"""
activation.py
"""

from __future__ import annotations


from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QPointF, QRectF, QLineF
from PySide6.QtGui import QPainter, QPen, QColor
import math
from edge import Edge 

class ActivationEdge(Edge):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        super().__init__(source, dest, parent)
        self._color = "#2EE3F0" #light blue
        

    def draw_edge(self, painter: QPainter):
        start = self._line.p1()
        painter.drawLine(self._line) 
        end = self._arrow_tip 
        self.draw_line(painter, start, end)
        self.draw_arrow_head(painter, start, end)

    def adjust(self):
        super().adjust()
        self._arrow_tip = self.arrow_target()