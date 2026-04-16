:py:mod:`daccadevo.optimization.evolver`
========================================

.. py:module:: daccadevo.optimization.evolver

.. autodoc2-docstring:: daccadevo.optimization.evolver
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DaccadBioneatMut <daccadevo.optimization.evolver.DaccadBioneatMut>`
     - .. autodoc2-docstring:: daccadevo.optimization.evolver.DaccadBioneatMut
          :summary:

API
~~~

.. py:class:: DaccadBioneatMut(container: qdpy.containers.Container, budget: int, ind_domain: qdpy.phenotype.DomainLike, nb_nodes_domain: typing.Sequence[int] = [1, 7], min_init_budget: int = 1, min_ind_found_in_init: int = 1, init_pb: float = 0.0, sel_pb: float = 1.0, init_ind: typing.Union[str, typing.Callable[[qdpy.phenotype.IndividualLike], qdpy.phenotype.IndividualLike]] = standard_init_ind, prob_parameter_mut: float = 0.4, prob_template_add: float = 0.2, prob_template_del: float = 0.2, prob_signal_species_add: float = 0.1, prob_inhibition_species_add: float = 0.1, nbConnActivationsDomain: typing.Sequence[int] = [1, 7], nbConnInhibitionsDomain: typing.Sequence[int] = [0, 6], nbConnDomain: typing.Sequence[int] = [1, 13], f1: float = 0.2, f2: float = 2.0, mut_pb: float = 0.8, init_drift: int = 1, keep_all_ancestry: bool = False, **kwargs)
   :canonical: daccadevo.optimization.evolver.DaccadBioneatMut

   Bases: :py:obj:`qdpy.algorithms.Evolution`

   .. autodoc2-docstring:: daccadevo.optimization.evolver.DaccadBioneatMut

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.optimization.evolver.DaccadBioneatMut.__init__

   .. py:method:: _select_or_initialise(collection: typing.Sequence[typing.Any], base_ind: qdpy.phenotype.IndividualLike) -> typing.Tuple[typing.Any, bool]
      :canonical: daccadevo.optimization.evolver.DaccadBioneatMut._select_or_initialise

      .. autodoc2-docstring:: daccadevo.optimization.evolver.DaccadBioneatMut._select_or_initialise

   .. py:method:: _vary(individual)
      :canonical: daccadevo.optimization.evolver.DaccadBioneatMut._vary

      .. autodoc2-docstring:: daccadevo.optimization.evolver.DaccadBioneatMut._vary
