:py:mod:`daccadevo.visualization.view`
======================================

.. py:module:: daccadevo.visualization.view

.. autodoc2-docstring:: daccadevo.visualization.view
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`GraphView <daccadevo.visualization.view.GraphView>`
     - .. autodoc2-docstring:: daccadevo.visualization.view.GraphView
          :summary:

API
~~~

.. py:class:: GraphView(graph: networkx.DiGraph, parent=None)
   :canonical: daccadevo.visualization.view.GraphView

   Bases: :py:obj:`PySide6.QtWidgets.QGraphicsView`

   .. autodoc2-docstring:: daccadevo.visualization.view.GraphView

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.view.GraphView.__init__

   .. py:method:: get_nx_layouts() -> list
      :canonical: daccadevo.visualization.view.GraphView.get_nx_layouts

      .. autodoc2-docstring:: daccadevo.visualization.view.GraphView.get_nx_layouts

   .. py:method:: set_nx_layout(name: str)
      :canonical: daccadevo.visualization.view.GraphView.set_nx_layout

      .. autodoc2-docstring:: daccadevo.visualization.view.GraphView.set_nx_layout

   .. py:method:: _load_graph()
      :canonical: daccadevo.visualization.view.GraphView._load_graph

      .. autodoc2-docstring:: daccadevo.visualization.view.GraphView._load_graph
