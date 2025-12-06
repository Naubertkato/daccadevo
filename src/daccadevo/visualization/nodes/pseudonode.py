
from __future__ import annotations


from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF
from daccadevo.visualization.node import Node

class PseudoNode(Node):

    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self._radius = 15
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
        self._color = "#EB5E34" # orange

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)