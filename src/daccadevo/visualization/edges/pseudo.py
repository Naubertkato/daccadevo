"""
pseudo.py
"""

from __future__ import annotations

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QLinearGradient, QPainterPath
import math
from edge import Edge


class PseudoEdge(Edge):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        self._source = source
        self._dest = dest
        super().__init__(source, dest, parent)
        self._start = QPointF()
        self._end = QPointF()
        self._c1 = QPointF()
        self._c2 = QPointF()
        self._color = "#EB5E34" # orange
        
    def draw_edge(self, painter: QPainter):
        self._path.moveTo(self._start)
        self._path.lineTo(self._start)
        self._path.cubicTo(self._c1, self._c2, self._end)
        painter.drawPath(self._path)
        
    def adjust(self):
        self._path = QPainterPath()
        self._start = self._source.pos() + self._source.boundingRect().center()
        self._end = self._dest.pos() + self._dest.boundingRect().center()
        self._c1 = self._start + QPointF(50, -30)
        self._c2 = self._end + QPointF(-30, 50)