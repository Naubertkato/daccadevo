:py:mod:`daccadevo.wrappers.jpype`
==================================

.. py:module:: daccadevo.wrappers.jpype

.. autodoc2-docstring:: daccadevo.wrappers.jpype
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Jpype_wrapper <daccadevo.wrappers.jpype.Jpype_wrapper>`
     - .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper
          :summary:

API
~~~

.. py:class:: Jpype_wrapper(config=None)
   :canonical: daccadevo.wrappers.jpype.Jpype_wrapper

   Bases: :py:obj:`daccadevo.wrappers.cli.DACCAD_Wrapper`

   .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.__init__

   .. py:method:: reset(config)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.reset

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.reset

   .. py:method:: generateNode(name, stability, activator, graph, species_dict, initConc=1.0)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateNode

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateNode

   .. py:method:: generateConnection(innov, concentration, fromNode, toNode, graph, species_dict)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateConnection

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateConnection

   .. py:method:: generateAllNodes(array, inhibitingSequences, graph, species_dict, initConc=1.0, nNodes=5)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateAllNodes

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateAllNodes

   .. py:method:: generateAllConnections(array, inhibitions, graph, species_dict, nNodes=5)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateAllConnections

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateAllConnections

   .. py:method:: generateEnzymeParameters(graph, pol=1.0, nick=1.0, exo=1.0)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateEnzymeParameters

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateEnzymeParameters

   .. py:method:: generateFull(array, graph=None, species_dict={}, nNodes=5, enzymes={'pol': 1.0, 'nick': 1.0, 'exo': 1.0}, initConc=1.0, **kwargs)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.generateFull

      .. autodoc2-docstring:: daccadevo.wrappers.jpype.Jpype_wrapper.generateFull

   .. py:method:: submitPENSystem(array, nNodes=5, config=None, **kwargs)
      :canonical: daccadevo.wrappers.jpype.Jpype_wrapper.submitPENSystem
