"""
predatorprey.py
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, QSizeF, QLineF
from PySide6.QtGui import QPainter
import math
from daccadevo.visualization.edge import Edge 
from daccadevo.visualization.node import Node

class PredatorPreyEdge(Edge):
    def __init__(self, predator_node: Node, prey_node: Node, parent=None):
        self.prey_node = prey_node
        self.predator_node = predator_node
        self._loop_radius = self.predator_node._radius
        super().__init__(self.predator_node, self.predator_node, parent)  # PredatorPreyEdgeの本体をloopにする
        self._color = "#F294CE"
        self._arrow_size = 15
        self._line_to_loop = QLineF()
        self._loop_angle = 0
        self._loop_rect = QRectF() 
        
        
    def draw_edge(self, painter: QPainter):
        self.draw_arc(painter, self._loop_rect, self._loop_angle,
                    radius=self.source._radius, arrow_size=self._arrow_size, span_angle=270)
        painter.drawLine(self._line_to_loop)

    def adjust(self):
        self.prepareGeometryChange()
        predator_center = self.source.pos() + self.source.boundingRect().center()
        prey_center = self.prey_node.pos() + self.prey_node.boundingRect().center()
        loop_center = self._loop_rect.center()
        vec = prey_center - predator_center
        angle = math.atan2(vec.y(), vec.x())
        offset_x = math.cos(angle) * self._loop_radius
        offset_y = math.sin(angle) * self._loop_radius

        top_left = QPointF(self.source.x() + offset_x, self.source.y() + offset_y)
        self._loop_rect = QRectF(top_left, QSizeF(self._loop_radius*2, self._loop_radius*2))
        self._loop_angle = (90 - math.degrees(angle)) % 360 + 135

        line_loop_x = loop_center.x()+ self._loop_radius * math.cos(angle)
        line_loop_y = loop_center.y()+ self._loop_radius * math.sin(angle)
        start_point = QPointF(line_loop_x, line_loop_y)
        self._line_to_loop = QLineF(start_point, prey_center)
        return (self.source.pos(), self.dest.pos())