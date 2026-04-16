:py:mod:`daccadevo.visualization.edges.activation`
==================================================

.. py:module:: daccadevo.visualization.edges.activation

.. autodoc2-docstring:: daccadevo.visualization.edges.activation
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`ActivationEdge <daccadevo.visualization.edges.activation.ActivationEdge>`
     - .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge
          :summary:

API
~~~

.. py:class:: ActivationEdge(source: daccadevo.visualization.node.Node, dest: daccadevo.visualization.node.Node, parent: PySide6.QtWidgets.QGraphicsItem = None)
   :canonical: daccadevo.visualization.edges.activation.ActivationEdge

   Bases: :py:obj:`daccadevo.visualization.edge.Edge`

   .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.__init__

   .. py:property:: s_pos
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.s_pos

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.s_pos

   .. py:property:: e_pos
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.e_pos

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.e_pos

   .. py:property:: control_pos
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.control_pos

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.control_pos

   .. py:method:: _boundingRect_normal() -> PySide6.QtCore.QRectF
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge._boundingRect_normal

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge._boundingRect_normal

   .. py:method:: calculate_bezier(p)
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.calculate_bezier

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.calculate_bezier

   .. py:method:: get_midpoint()
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.get_midpoint

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.get_midpoint

   .. py:method:: draw_edge(painter: PySide6.QtGui.QPainter)
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.draw_edge

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.draw_edge

   .. py:method:: adjust()
      :canonical: daccadevo.visualization.edges.activation.ActivationEdge.adjust

      .. autodoc2-docstring:: daccadevo.visualization.edges.activation.ActivationEdge.adjust
