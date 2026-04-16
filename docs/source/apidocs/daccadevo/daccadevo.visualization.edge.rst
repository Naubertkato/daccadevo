:py:mod:`daccadevo.visualization.edge`
======================================

.. py:module:: daccadevo.visualization.edge

.. autodoc2-docstring:: daccadevo.visualization.edge
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Edge <daccadevo.visualization.edge.Edge>`
     - .. autodoc2-docstring:: daccadevo.visualization.edge.Edge
          :summary:

API
~~~

.. py:class:: Edge(source: daccadevo.visualization.node.Node, dest: daccadevo.visualization.node.Node, parent: PySide6.QtWidgets.QGraphicsItem = None)
   :canonical: daccadevo.visualization.edge.Edge

   Bases: :py:obj:`PySide6.QtWidgets.QGraphicsItem`

   .. autodoc2-docstring:: daccadevo.visualization.edge.Edge

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.__init__

   .. py:method:: boundingRect() -> PySide6.QtCore.QRectF
      :canonical: daccadevo.visualization.edge.Edge.boundingRect

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.boundingRect

   .. py:method:: _boundingRect_normal() -> PySide6.QtCore.QRectF
      :canonical: daccadevo.visualization.edge.Edge._boundingRect_normal

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge._boundingRect_normal

   .. py:method:: get_midpoint() -> PySide6.QtCore.QPointF
      :canonical: daccadevo.visualization.edge.Edge.get_midpoint

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.get_midpoint

   .. py:method:: adjust()
      :canonical: daccadevo.visualization.edge.Edge.adjust

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.adjust

   .. py:method:: _adjust_normal()
      :canonical: daccadevo.visualization.edge.Edge._adjust_normal

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge._adjust_normal

   .. py:method:: draw_line(painter: PySide6.QtGui.QPainter, start: PySide6.QtCore.QPointF, end: PySide6.QtCore.QPointF)
      :canonical: daccadevo.visualization.edge.Edge.draw_line

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.draw_line

   .. py:method:: draw_arrow_head(painter: PySide6.QtGui.QPainter, start: PySide6.QtCore.QPointF, end: PySide6.QtCore.QPointF)
      :canonical: daccadevo.visualization.edge.Edge.draw_arrow_head

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.draw_arrow_head

   .. py:method:: _adjust_loop(radius_offset=30)
      :canonical: daccadevo.visualization.edge.Edge._adjust_loop

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge._adjust_loop

   .. py:method:: _boundingRect_loop(margin=50.0)
      :canonical: daccadevo.visualization.edge.Edge._boundingRect_loop

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge._boundingRect_loop

   .. py:method:: draw_arc(painter: PySide6.QtGui.QPainter, rect: PySide6.QtCore.QRectF, start_angle: float, radius: float, arrow_size: float, span_angle: float = 270)
      :canonical: daccadevo.visualization.edge.Edge.draw_arc

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.draw_arc

   .. py:method:: arrow_target() -> PySide6.QtCore.QPointF
      :canonical: daccadevo.visualization.edge.Edge.arrow_target

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.arrow_target

   .. py:method:: paint(painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem, widget=None)
      :canonical: daccadevo.visualization.edge.Edge.paint

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.paint

   .. py:method:: draw_edge(painter: PySide6.QtGui.QPainter)
      :canonical: daccadevo.visualization.edge.Edge.draw_edge

      .. autodoc2-docstring:: daccadevo.visualization.edge.Edge.draw_edge
