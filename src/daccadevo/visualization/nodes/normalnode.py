
from __future__ import annotations


from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF
from daccadevo.visualization.node import Node

class NormalNode(Node):

    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.setZValue(1)
        self._color = "#5AD469"
        self._radius = 30
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
        # self.affecting_nodes = []
        # self.setOpacity(0.5)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
    