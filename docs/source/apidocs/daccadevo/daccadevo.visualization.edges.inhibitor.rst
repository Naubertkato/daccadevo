:py:mod:`daccadevo.visualization.edges.inhibitor`
=================================================

.. py:module:: daccadevo.visualization.edges.inhibitor

.. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`InhibitorEdge <daccadevo.visualization.edges.inhibitor.InhibitorEdge>`
     - .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge
          :summary:

API
~~~

.. py:class:: InhibitorEdge(source: daccadevo.visualization.node.Node, dest: daccadevo.visualization.node.Node, parent: PySide6.QtWidgets.QGraphicsItem = None)
   :canonical: daccadevo.visualization.edges.inhibitor.InhibitorEdge

   Bases: :py:obj:`daccadevo.visualization.edge.Edge`

   .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge.__init__

   .. py:method:: adjust()
      :canonical: daccadevo.visualization.edges.inhibitor.InhibitorEdge.adjust

      .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge.adjust

   .. py:method:: draw_edge(painter: PySide6.QtGui.QPainter)
      :canonical: daccadevo.visualization.edges.inhibitor.InhibitorEdge.draw_edge

      .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge.draw_edge

   .. py:method:: _draw_inhibition_head(painter: PySide6.QtGui.QPainter, tip: PySide6.QtCore.QPointF)
      :canonical: daccadevo.visualization.edges.inhibitor.InhibitorEdge._draw_inhibition_head

      .. autodoc2-docstring:: daccadevo.visualization.edges.inhibitor.InhibitorEdge._draw_inhibition_head
