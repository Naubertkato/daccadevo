
from __future__ import annotations

from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
import math
from node import Node
import networkx as nx

class ActivationNode(Node):
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.activaionedge = None
        self.source = None
        self.dest = None

        self._radius = 1
        self._rect = QRectF(0, 0, self._radius * 1, self._radius * 1)
        self._color = "#2EE3F0" #light blue
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setOpacity(0.0)
        