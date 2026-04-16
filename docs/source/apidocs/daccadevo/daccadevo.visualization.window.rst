:py:mod:`daccadevo.visualization.window`
========================================

.. py:module:: daccadevo.visualization.window

.. autodoc2-docstring:: daccadevo.visualization.window
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`MainWindow <daccadevo.visualization.window.MainWindow>`
     - .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow
          :summary:
   * - :py:obj:`timeSeriesWindow <daccadevo.visualization.window.timeSeriesWindow>`
     - .. autodoc2-docstring:: daccadevo.visualization.window.timeSeriesWindow
          :summary:

API
~~~

.. py:class:: MainWindow(parent=None, dict_network=None, figure_path=None, key=None, show_inhibitors=True)
   :canonical: daccadevo.visualization.window.MainWindow

   Bases: :py:obj:`PySide6.QtWidgets.QWidget`

   .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow.__init__

   .. py:method:: quitButton_clicked()
      :canonical: daccadevo.visualization.window.MainWindow.quitButton_clicked

      .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow.quitButton_clicked

   .. py:method:: timeSeriesButton_clicked()
      :canonical: daccadevo.visualization.window.MainWindow.timeSeriesButton_clicked

      .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow.timeSeriesButton_clicked

   .. py:method:: saveButton_clicked()
      :canonical: daccadevo.visualization.window.MainWindow.saveButton_clicked

      .. autodoc2-docstring:: daccadevo.visualization.window.MainWindow.saveButton_clicked

.. py:class:: timeSeriesWindow(parent=None, figure_path=None, key=None)
   :canonical: daccadevo.visualization.window.timeSeriesWindow

   Bases: :py:obj:`PySide6.QtWidgets.QWidget`

   .. autodoc2-docstring:: daccadevo.visualization.window.timeSeriesWindow

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.visualization.window.timeSeriesWindow.__init__

   .. py:method:: saveButton_clicked()
      :canonical: daccadevo.visualization.window.timeSeriesWindow.saveButton_clicked

      .. autodoc2-docstring:: daccadevo.visualization.window.timeSeriesWindow.saveButton_clicked
