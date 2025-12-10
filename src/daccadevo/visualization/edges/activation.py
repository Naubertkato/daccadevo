"""
activation.py
"""

from __future__ import annotations


from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QPointF, QLineF, QRectF
from PySide6.QtGui import QPainter, QPainterPath
from daccadevo.visualization.edge import Edge 
from daccadevo.visualization.node import Node

class ActivationEdge(Edge):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        super().__init__(source, dest, parent)
        self._color = "#2EE3F0" #light blue

    @property
    def s_pos(self):
        return self.source.pos()+ self.source.boundingRect().center()
    @property
    def e_pos(self):
        return self.dest.pos()+ self.dest.boundingRect().center()

    @property
    def control_pos(self):
        mid = super().get_midpoint()
        e = self.e_pos
        x = mid.x() - (e.y()-mid.y())
        y = mid.y() + (e.x()-mid.x())
        return QPointF(x, y)
    

    def _boundingRect_normal(self) -> QRectF:
        s = self.s_pos
        e = self.e_pos
        c = self.control_pos
        min_x = min(s.x(),e.x(),c.x())
        min_y = min(s.y(),e.y(),c.y())
        max_x = max(s.x(),e.x(),c.x())
        max_y = max(s.y(),e.y(),c.y())

        return (
            QRectF(QPointF(min_x, min_y), QPointF(max_x, max_y))
            .normalized()
            .adjusted(
                -self._tickness - self._arrow_size,
                -self._tickness - self._arrow_size,
                self._tickness + self._arrow_size,
                self._tickness + self._arrow_size,
            )
        )
        

    def calculate_bezier(self, p):
        s = self.s_pos
        e = self.e_pos
        c = self.control_pos
        return c + (1.0 - p)*(1.0 - p)*(s - c) + p*p*(e - c)

    def get_midpoint(self):
        return self.calculate_bezier(0.5)

    def draw_edge(self, painter: QPainter):
        #start = self._line.p1()
        #end = self._arrow_tip
        #self.draw_line(painter, start, end) 
        s = self.s_pos
        e = self.e_pos
        control = self.control_pos
        path = QPainterPath()
        path.moveTo(s)
        path.quadTo(control, e)

        #painter.drawArc(self.boundingRect(), 0, int(180 * 16))
        painter.drawPath(path)

        # solving the intersection between the node and the Bezier curve
        line = QLineF(s, e)
        length = line.length()
        rad = self.dest._radius
        # approximation of the analytical solution, but close enough
        parameter = 1 - 1/(1+length/(0.83*rad))
        parameter_behind = 1 - 1/(1+length/(0.83*(rad+1)))
        pos = self.calculate_bezier(parameter)
        pos_behind = self.calculate_bezier(parameter_behind)

        self.draw_arrow_head(painter, pos_behind, pos)

    def adjust(self):
        super().adjust()
        self._arrow_tip = self.arrow_target()