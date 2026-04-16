:py:mod:`daccadevo.visualization.node`
======================================

.. py:module:: daccadevo.visualization.node

.. autodoc2-docstring:: daccadevo.visualization.node
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Node <daccadevo.visualization.node.Node>`
     - .. autodoc2-docstring:: daccadevo.visualization.node.Node
          :summary:

API
~~~

.. py:class:: Node(name: str, parent=None)
   :canonical: daccadevo.visualization.node.Node

   Bases: :py:obj:`PySide6.QtWidgets.QGraphicsObject`

   .. autodoc2-docstring:: daccadevo.visualization.node.Node

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.node.Node.__init__

   .. py:method:: boundingRect() -> PySide6.QtCore.QRectF
      :canonical: daccadevo.visualization.node.Node.boundingRect

      .. autodoc2-docstring:: daccadevo.visualization.node.Node.boundingRect

   .. py:method:: paint(painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem, widget: PySide6.QtWidgets.QWidget = None)
      :canonical: daccadevo.visualization.node.Node.paint

      .. autodoc2-docstring:: daccadevo.visualization.node.Node.paint

   .. py:method:: add_edge(edge)
      :canonical: daccadevo.visualization.node.Node.add_edge

      .. autodoc2-docstring:: daccadevo.visualization.node.Node.add_edge

   .. py:method:: itemChange(change, value)
      :canonical: daccadevo.visualization.node.Node.itemChange

      .. autodoc2-docstring:: daccadevo.visualization.node.Node.itemChange
