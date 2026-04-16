:py:mod:`daccadevo.wrappers.cli`
================================

.. py:module:: daccadevo.wrappers.cli

.. autodoc2-docstring:: daccadevo.wrappers.cli
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DACCAD_Wrapper <daccadevo.wrappers.cli.DACCAD_Wrapper>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.DACCAD_Wrapper
          :summary:
   * - :py:obj:`CLI_wrapper <daccadevo.wrappers.cli.CLI_wrapper>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_default_config <daccadevo.wrappers.cli.get_default_config>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.get_default_config
          :summary:
   * - :py:obj:`findAllInhibitions <daccadevo.wrappers.cli.findAllInhibitions>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitions
          :summary:
   * - :py:obj:`findAllInhibitorsAndConcsLegacy <daccadevo.wrappers.cli.findAllInhibitorsAndConcsLegacy>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitorsAndConcsLegacy
          :summary:
   * - :py:obj:`findAllInhibitorsAndConcs <daccadevo.wrappers.cli.findAllInhibitorsAndConcs>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitorsAndConcs
          :summary:
   * - :py:obj:`invalidInhibitions <daccadevo.wrappers.cli.invalidInhibitions>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.invalidInhibitions
          :summary:
   * - :py:obj:`isValid <daccadevo.wrappers.cli.isValid>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.isValid
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`default_cli_wrapper <daccadevo.wrappers.cli.default_cli_wrapper>`
     - .. autodoc2-docstring:: daccadevo.wrappers.cli.default_cli_wrapper
          :summary:

API
~~~

.. py:function:: get_default_config()
   :canonical: daccadevo.wrappers.cli.get_default_config

   .. autodoc2-docstring:: daccadevo.wrappers.cli.get_default_config

.. py:function:: findAllInhibitions(array, nNodes=5)
   :canonical: daccadevo.wrappers.cli.findAllInhibitions

   .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitions

.. py:function:: findAllInhibitorsAndConcsLegacy(array, nNodes=5)
   :canonical: daccadevo.wrappers.cli.findAllInhibitorsAndConcsLegacy

   .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitorsAndConcsLegacy

.. py:function:: findAllInhibitorsAndConcs(array, nNodes=5)
   :canonical: daccadevo.wrappers.cli.findAllInhibitorsAndConcs

   .. autodoc2-docstring:: daccadevo.wrappers.cli.findAllInhibitorsAndConcs

.. py:function:: invalidInhibitions(array, nNodes=5)
   :canonical: daccadevo.wrappers.cli.invalidInhibitions

   .. autodoc2-docstring:: daccadevo.wrappers.cli.invalidInhibitions

.. py:function:: isValid(array, nNodes=5)
   :canonical: daccadevo.wrappers.cli.isValid

   .. autodoc2-docstring:: daccadevo.wrappers.cli.isValid

.. py:class:: DACCAD_Wrapper(config=None)
   :canonical: daccadevo.wrappers.cli.DACCAD_Wrapper

   Bases: :py:obj:`abc.ABC`

   .. autodoc2-docstring:: daccadevo.wrappers.cli.DACCAD_Wrapper

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.wrappers.cli.DACCAD_Wrapper.__init__

   .. py:method:: reset(config)
      :canonical: daccadevo.wrappers.cli.DACCAD_Wrapper.reset

      .. autodoc2-docstring:: daccadevo.wrappers.cli.DACCAD_Wrapper.reset

   .. py:method:: submitPENSystem(array, config=None, **kwargs)
      :canonical: daccadevo.wrappers.cli.DACCAD_Wrapper.submitPENSystem
      :abstractmethod:

      .. autodoc2-docstring:: daccadevo.wrappers.cli.DACCAD_Wrapper.submitPENSystem

.. py:class:: CLI_wrapper(config=None)
   :canonical: daccadevo.wrappers.cli.CLI_wrapper

   Bases: :py:obj:`daccadevo.wrappers.cli.DACCAD_Wrapper`

   .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.__init__

   .. py:method:: reset(config)
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.reset

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.reset

   .. py:method:: generateNode(name, stability, activator, initConc='1.0', tab=1, tabChar='  ')
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateNode

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateNode

   .. py:method:: generateConnection(innov, concentration, fromNode, toNode, tab=1, tabChar='  ')
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateConnection

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateConnection

   .. py:method:: generateAllNodes(array, inhibitingSequences, nNodes=5, initConc='1.0', tab=1, tabChar='  ')
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateAllNodes

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateAllNodes

   .. py:method:: generateAllConnections(array, inhibitions, nNodes=5, tab=1, tabChar='  ')
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateAllConnections

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateAllConnections

   .. py:method:: generateEnzymeParameters(pol=1.0, nick=1.0, exo=1.0, tab=1, tabChar='  ')
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateEnzymeParameters

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateEnzymeParameters

   .. py:method:: generateFullJson(array, enzymes={'pol': 1.0, 'nick': 1.0, 'exo': 1.0}, nNodes=5, initConc='1.0', tab=0, tabChar='  ', **kwargs)
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.generateFullJson

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.generateFullJson

   .. py:method:: submitPENJson(jsonFileName='generatedGraph0_0_0.json', daccad_config_file=None, **kwargs)
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.submitPENJson

      .. autodoc2-docstring:: daccadevo.wrappers.cli.CLI_wrapper.submitPENJson

   .. py:method:: submitPENSystem(array, nNodes=5, config=None, **kwargs)
      :canonical: daccadevo.wrappers.cli.CLI_wrapper.submitPENSystem

.. py:data:: default_cli_wrapper
   :canonical: daccadevo.wrappers.cli.default_cli_wrapper
   :value: 'CLI_wrapper(...)'

   .. autodoc2-docstring:: daccadevo.wrappers.cli.default_cli_wrapper
