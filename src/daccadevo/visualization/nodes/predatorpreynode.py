
from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsItem

from daccadevo.visualization.node import Node


class PredatorNode(Node):

    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self._radius = 30
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
        self._color = "#F294CE" # pink
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
