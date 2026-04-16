:py:mod:`daccadevo.core.individual`
===================================

.. py:module:: daccadevo.core.individual

.. autodoc2-docstring:: daccadevo.core.individual
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DaccadIndividual <daccadevo.core.individual.DaccadIndividual>`
     - .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`gen_daccad_individuals <daccadevo.core.individual.gen_daccad_individuals>`
     - .. autodoc2-docstring:: daccadevo.core.individual.gen_daccad_individuals
          :summary:
   * - :py:obj:`standard_init_ind <daccadevo.core.individual.standard_init_ind>`
     - .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind
          :summary:
   * - :py:obj:`standard_init_ind_grad4 <daccadevo.core.individual.standard_init_ind_grad4>`
     - .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind_grad4
          :summary:
   * - :py:obj:`standard_init_ind0 <daccadevo.core.individual.standard_init_ind0>`
     - .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind0
          :summary:
   * - :py:obj:`standard_init_act <daccadevo.core.individual.standard_init_act>`
     - .. autodoc2-docstring:: daccadevo.core.individual.standard_init_act
          :summary:

API
~~~

.. py:class:: DaccadIndividual(ind_domain, nb_nodes=0, species=0, **kwargs)
   :canonical: daccadevo.core.individual.DaccadIndividual

   Bases: :py:obj:`qdpy.phenotype.Individual`

   .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual

   .. rubric:: Initialization

   .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.__init__

   .. py:method:: is_valid()
      :canonical: daccadevo.core.individual.DaccadIndividual.is_valid

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.is_valid

   .. py:method:: assemble()
      :canonical: daccadevo.core.individual.DaccadIndividual.assemble

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.assemble

   .. py:method:: update()
      :canonical: daccadevo.core.individual.DaccadIndividual.update

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.update

   .. py:method:: same_species_as(other)
      :canonical: daccadevo.core.individual.DaccadIndividual.same_species_as

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.same_species_as

   .. py:method:: resize(nb_nodes)
      :canonical: daccadevo.core.individual.DaccadIndividual.resize

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.resize

   .. py:method:: active_nodes()
      :canonical: daccadevo.core.individual.DaccadIndividual.active_nodes

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.active_nodes

   .. py:method:: valid_indexes()
      :canonical: daccadevo.core.individual.DaccadIndividual.valid_indexes

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.valid_indexes

   .. py:property:: values
      :canonical: daccadevo.core.individual.DaccadIndividual.values

      .. autodoc2-docstring:: daccadevo.core.individual.DaccadIndividual.values

.. py:function:: gen_daccad_individuals(ind_domain)
   :canonical: daccadevo.core.individual.gen_daccad_individuals

   .. autodoc2-docstring:: daccadevo.core.individual.gen_daccad_individuals

.. py:function:: standard_init_ind(ind)
   :canonical: daccadevo.core.individual.standard_init_ind

   .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind

.. py:function:: standard_init_ind_grad4(ind)
   :canonical: daccadevo.core.individual.standard_init_ind_grad4

   .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind_grad4

.. py:function:: standard_init_ind0(ind)
   :canonical: daccadevo.core.individual.standard_init_ind0

   .. autodoc2-docstring:: daccadevo.core.individual.standard_init_ind0

.. py:function:: standard_init_act(ind)
   :canonical: daccadevo.core.individual.standard_init_act

   .. autodoc2-docstring:: daccadevo.core.individual.standard_init_act
