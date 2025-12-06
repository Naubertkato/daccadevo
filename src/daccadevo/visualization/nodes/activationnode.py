
from __future__ import annotations

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF
from daccadevo.visualization.node import Node

class ActivationNode(Node):
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.activationedge = None
        self.source = None
        self.dest = None

        self._radius = 30
        self._rect = QRectF(0, 0, self._radius * 1, self._radius * 1)
        self._color = "#2EE3F0" #light blue
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setOpacity(0.0)
        