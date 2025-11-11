"""
edge.py
Define the base Edge class.
"""
from __future__ import annotations

import networkx as nx
from PySide6.QtWidgets import QGraphicsItem,QGraphicsObject
from PySide6.QtCore import QPointF, QLineF, QRectF, Qt, QSizeF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
import math 
from node import Node
from nodes import NormalNode, PseudoNode, PredatorNode, ActivationNode


class Edge(QGraphicsItem):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        super().__init__(parent)
        self.source = source
        self.dest = dest

        self._tickness = 2
        self._color = "#2BB53C"
        self._arrow_size = 15
        self.source.add_edge(self)
        self.dest.add_edge(self)

        self._line = QLineF()
        self._loop_rect = QRectF()
        self._loop_angle = 0
        self.setZValue(-1)
        self.adjust()

    def boundingRect(self) -> QRectF:
        if self.source == self.dest:
            return self.boundingRect_loop()
        else:
            return self._boundingRect_normal()
    
    def _boundingRect_normal(self) -> QRectF:
        return (
            QRectF(self._line.p1(), self._line.p2())
            .normalized()
            .adjusted(
                -self._tickness - self._arrow_size,
                -self._tickness - self._arrow_size,
                self._tickness + self._arrow_size,
                self._tickness + self._arrow_size,
            )
        )

    def get_midpoint(self) -> QPointF:
        if self.source != self.dest:
            p1 = self._line.p1()
            p2 = self._line.p2()
            x = (p1.x()+p2.x())/2
            y = (p1.y()+p2.y())/2
        else:
            rect = self._loop_rect
            start_angle_deg = self._loop_angle
            span_deg = 45
            mid_angle_deg = (start_angle_deg + span_deg)
            theta = math.radians(mid_angle_deg)
        
            centerX = rect.center().x()
            centerY = rect.center().y()
            radius = self.source._radius

            x = centerX + math.cos(theta) * radius
            y = centerY + math.sin(theta) * radius
        return QPointF(x, y)

    def adjust(self):
        self.prepareGeometryChange()
        if self.source == self.dest:  
            self._adjust_loop()
        else:
            self._adjust_normal()
        return (self.source.pos(), self.dest.pos())

    def _adjust_normal(self):
        self._line = QLineF(
                self.source.pos() + self.source.boundingRect().center(),
                self.dest.pos() + self.dest.boundingRect().center(),
            )

    def draw_line(self, painter: QPainter, start: QPointF, end: QPointF):
        painter.drawLine(QLineF(start, end))

    def draw_arrow_head(self, painter: QPainter, start: QPointF, end: QPointF):
        painter.setBrush(QBrush(self._color))
        line = QLineF(end, start)
        angle = math.atan2(-line.dy(), line.dx())
        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi / 3) * self._arrow_size,
        )
        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
        )
        arrow_head = QPolygonF([line.p1(), arrow_p1, arrow_p2])
        painter.drawPolygon(arrow_head)

    def _adjust_loop(self, radius_offset=30):
        preferred_angles = [45, 135, 225, 315]
        edges = self.dest._edges
        used_angles = []
        for edge in edges:
            if edge.source != edge.dest:
                vec = edge.dest.pos() - edge.source.pos()
                angle = math.atan2(vec.y(), vec.x())
                used_angles.append(math.degrees(angle))
        countAngle = []
        for angle in preferred_angles:
            i = 0
            for a in used_angles:
                diff = abs((angle - a + 180) % 360 - 180)
                if diff > 120:
                    i += 1
            countAngle.append(i)
        self._loop_angle = preferred_angles[countAngle.index(min(countAngle))]

        offset_x = 0
        offset_y = 0
        if self._loop_angle == 45:
            offset_x = -radius_offset
        elif self._loop_angle == 135:
            offset_y = radius_offset
        elif self._loop_angle == 225:
            offset_x = radius_offset
        elif self._loop_angle == 315:
            offset_y = -radius_offset
        base = self.source
        top_left = QPointF(base.x() + offset_x, base.y() + offset_y)
        self._loop_rect = QRectF(top_left, QSizeF(radius_offset*2, radius_offset*2))

    def boundingRect_loop(self, margin=50.0):
        if hasattr(self, "_loop_rect"):
            margin = 50.0
            return self._loop_rect.adjusted(-margin, -margin, margin, margin)
        else:
            rect_size = 60.0
            margin = 120.0
            return QRectF(
                self.source.x() - rect_size / 2 - margin,
                self.source.y() - rect_size / 2 - margin,
                rect_size + margin * 2,
                rect_size + margin * 2
            )

    def draw_arc(self, painter: QPainter, rect: QRectF, start_angle: float, radius: float, arrow_size: float, span_angle: float = 270):
        if not hasattr(self, "_loop_rect") or not hasattr(self, "_loop_angle"):
            return
        start_angle = self._loop_angle
        painter.drawArc(self._loop_rect, int(start_angle * 16), int(span_angle * 16))
        loop_center = self._loop_rect.center()
        loop_radius = self.source._radius
        tip_pos_angle = (90 - start_angle + 257) % 360
        tip_x = loop_center.x() + loop_radius * math.cos(math.radians(tip_pos_angle))
        tip_y = loop_center.y() + loop_radius * math.sin(math.radians(tip_pos_angle))
        tip = QPointF(tip_x, tip_y)
        predator_center = self.source.pos() + self.source.boundingRect().center()
        vec = tip - predator_center
        tangent = QPointF(-vec.y(), vec.x())  
        arrow_angle = math.atan2(tangent.y(), tangent.x()) + math.pi /4
        size = self._arrow_size
        triangle_angle = math.pi / 6
        arrow_p1 = tip - QPointF(math.cos(arrow_angle - triangle_angle) * size,
                                 math.sin(arrow_angle - triangle_angle) * size)
        arrow_p2 = tip - QPointF(math.cos(arrow_angle + triangle_angle) * size,
                                 math.sin(arrow_angle + triangle_angle) * size)
        arrow_head = QPolygonF([tip, arrow_p1, arrow_p2])
        painter.setBrush(QBrush(self._color))
        painter.drawPolygon(arrow_head)
        

    def arrow_target(self) -> QPointF:
        target = self._line.p1()
        center = self._line.p2()
        radius = self.dest._radius
        vector = target - center
        length = math.sqrt(vector.x() ** 2 + vector.y() ** 2)
        if length == 0:
            return target
        normal = vector / length
        target = QPointF(center.x() + (normal.x() * radius), center.y() + (normal.y() * radius))
        return target

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        if self.source and self.dest:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            painter.setPen(
                QPen(
                    QColor(self._color),
                    self._tickness,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            self.draw_edge(painter)

    def draw_edge(self, painter: QPainter):
        pass
