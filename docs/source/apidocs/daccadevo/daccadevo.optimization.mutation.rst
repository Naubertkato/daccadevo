:py:mod:`daccadevo.optimization.mutation`
=========================================

.. py:module:: daccadevo.optimization.mutation

.. autodoc2-docstring:: daccadevo.optimization.mutation
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`mutation_param_polybounded <daccadevo.optimization.mutation.mutation_param_polybounded>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_polybounded
          :summary:
   * - :py:obj:`mutation_param_reinit <daccadevo.optimization.mutation.mutation_param_reinit>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_reinit
          :summary:
   * - :py:obj:`mutation_add_activation <daccadevo.optimization.mutation.mutation_add_activation>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation
          :summary:
   * - :py:obj:`mutation_add_activation2 <daccadevo.optimization.mutation.mutation_add_activation2>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation2
          :summary:
   * - :py:obj:`mutation_add_activation_with_gradients <daccadevo.optimization.mutation.mutation_add_activation_with_gradients>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation_with_gradients
          :summary:
   * - :py:obj:`mutation_del_activation <daccadevo.optimization.mutation.mutation_del_activation>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_activation
          :summary:
   * - :py:obj:`mutation_add_inhibition <daccadevo.optimization.mutation.mutation_add_inhibition>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_inhibition
          :summary:
   * - :py:obj:`mutation_del_inhibition <daccadevo.optimization.mutation.mutation_del_inhibition>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_inhibition
          :summary:
   * - :py:obj:`mutation_add_node <daccadevo.optimization.mutation.mutation_add_node>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_node
          :summary:
   * - :py:obj:`mutation_add_node_with_gradients <daccadevo.optimization.mutation.mutation_add_node_with_gradients>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_node_with_gradients
          :summary:
   * - :py:obj:`mutation_del_node <daccadevo.optimization.mutation.mutation_del_node>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_node
          :summary:
   * - :py:obj:`mutation_bioneat_signal_species <daccadevo.optimization.mutation.mutation_bioneat_signal_species>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_bioneat_signal_species
          :summary:
   * - :py:obj:`mutation_bioneat_inhibition_species <daccadevo.optimization.mutation.mutation_bioneat_inhibition_species>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_bioneat_inhibition_species
          :summary:
   * - :py:obj:`disable_template <daccadevo.optimization.mutation.disable_template>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.disable_template
          :summary:
   * - :py:obj:`mutate_one_param_bioneat <daccadevo.optimization.mutation.mutate_one_param_bioneat>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutate_one_param_bioneat
          :summary:
   * - :py:obj:`mutation_param_bioneat <daccadevo.optimization.mutation.mutation_param_bioneat>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_bioneat
          :summary:
   * - :py:obj:`add_node_with_gradients <daccadevo.optimization.mutation.add_node_with_gradients>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.add_node_with_gradients
          :summary:
   * - :py:obj:`add_activation_with_gradients <daccadevo.optimization.mutation.add_activation_with_gradients>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.add_activation_with_gradients
          :summary:
   * - :py:obj:`add_inhibition_with_gradients <daccadevo.optimization.mutation.add_inhibition_with_gradients>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.add_inhibition_with_gradients
          :summary:
   * - :py:obj:`clone_activation <daccadevo.optimization.mutation.clone_activation>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.clone_activation
          :summary:
   * - :py:obj:`clone_inhibition <daccadevo.optimization.mutation.clone_inhibition>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.clone_inhibition
          :summary:
   * - :py:obj:`mutation_clone_activation <daccadevo.optimization.mutation.mutation_clone_activation>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_activation
          :summary:
   * - :py:obj:`mutation_clone_inhibition <daccadevo.optimization.mutation.mutation_clone_inhibition>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_inhibition
          :summary:
   * - :py:obj:`mutation_clone_template <daccadevo.optimization.mutation.mutation_clone_template>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_template
          :summary:
   * - :py:obj:`crossover_uniform <daccadevo.optimization.mutation.crossover_uniform>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.crossover_uniform
          :summary:
   * - :py:obj:`crossover_uniform2 <daccadevo.optimization.mutation.crossover_uniform2>`
     - .. autodoc2-docstring:: daccadevo.optimization.mutation.crossover_uniform2
          :summary:

API
~~~

.. py:function:: mutation_param_polybounded(ind, eta, mut_pb)
   :canonical: daccadevo.optimization.mutation.mutation_param_polybounded

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_polybounded

.. py:function:: mutation_param_reinit(ind)
   :canonical: daccadevo.optimization.mutation.mutation_param_reinit

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_reinit

.. py:function:: mutation_add_activation(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_add_activation

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation

.. py:function:: mutation_add_activation2(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_add_activation2

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation2

.. py:function:: mutation_add_activation_with_gradients(ind, trivial=False, gradients=[0, 1])
   :canonical: daccadevo.optimization.mutation.mutation_add_activation_with_gradients

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_activation_with_gradients

.. py:function:: mutation_del_activation(ind)
   :canonical: daccadevo.optimization.mutation.mutation_del_activation

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_activation

.. py:function:: mutation_add_inhibition(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_add_inhibition

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_inhibition

.. py:function:: mutation_del_inhibition(ind)
   :canonical: daccadevo.optimization.mutation.mutation_del_inhibition

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_inhibition

.. py:function:: mutation_add_node(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_add_node

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_node

.. py:function:: mutation_add_node_with_gradients(ind, trivial=False, gradients=[0, 1])
   :canonical: daccadevo.optimization.mutation.mutation_add_node_with_gradients

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_add_node_with_gradients

.. py:function:: mutation_del_node(ind)
   :canonical: daccadevo.optimization.mutation.mutation_del_node

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_del_node

.. py:function:: mutation_bioneat_signal_species(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_bioneat_signal_species

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_bioneat_signal_species

.. py:function:: mutation_bioneat_inhibition_species(ind, trivial=False)
   :canonical: daccadevo.optimization.mutation.mutation_bioneat_inhibition_species

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_bioneat_inhibition_species

.. py:function:: disable_template(ind, mut_pb=0.8, disabling_pb=0.1)
   :canonical: daccadevo.optimization.mutation.disable_template

   .. autodoc2-docstring:: daccadevo.optimization.mutation.disable_template

.. py:function:: mutate_one_param_bioneat(old, ind_domain, f1=0.2, f2=2.0, max_bound=200.0)
   :canonical: daccadevo.optimization.mutation.mutate_one_param_bioneat

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutate_one_param_bioneat

.. py:function:: mutation_param_bioneat(ind, f1=0.2, f2=2.0, mut_pb=0.8)
   :canonical: daccadevo.optimization.mutation.mutation_param_bioneat

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_param_bioneat

.. py:function:: add_node_with_gradients(ind, gradients=[0, 1])
   :canonical: daccadevo.optimization.mutation.add_node_with_gradients

   .. autodoc2-docstring:: daccadevo.optimization.mutation.add_node_with_gradients

.. py:exception:: NotApplicableError()
   :canonical: daccadevo.optimization.mutation.NotApplicableError

   Bases: :py:obj:`Exception`

.. py:function:: add_activation_with_gradients(ind, gradients=[0, 1])
   :canonical: daccadevo.optimization.mutation.add_activation_with_gradients

   .. autodoc2-docstring:: daccadevo.optimization.mutation.add_activation_with_gradients

.. py:function:: add_inhibition_with_gradients(ind, gradients=[0, 1])
   :canonical: daccadevo.optimization.mutation.add_inhibition_with_gradients

   .. autodoc2-docstring:: daccadevo.optimization.mutation.add_inhibition_with_gradients

.. py:function:: clone_activation(ind, base_activation)
   :canonical: daccadevo.optimization.mutation.clone_activation

   .. autodoc2-docstring:: daccadevo.optimization.mutation.clone_activation

.. py:function:: clone_inhibition(ind, base_inhibition)
   :canonical: daccadevo.optimization.mutation.clone_inhibition

   .. autodoc2-docstring:: daccadevo.optimization.mutation.clone_inhibition

.. py:function:: mutation_clone_activation(ind)
   :canonical: daccadevo.optimization.mutation.mutation_clone_activation

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_activation

.. py:function:: mutation_clone_inhibition(ind)
   :canonical: daccadevo.optimization.mutation.mutation_clone_inhibition

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_inhibition

.. py:function:: mutation_clone_template(ind)
   :canonical: daccadevo.optimization.mutation.mutation_clone_template

   .. autodoc2-docstring:: daccadevo.optimization.mutation.mutation_clone_template

.. py:function:: crossover_uniform(ind1, ind2, prob)
   :canonical: daccadevo.optimization.mutation.crossover_uniform

   .. autodoc2-docstring:: daccadevo.optimization.mutation.crossover_uniform

.. py:function:: crossover_uniform2(ind1, ind2, prob)
   :canonical: daccadevo.optimization.mutation.crossover_uniform2

   .. autodoc2-docstring:: daccadevo.optimization.mutation.crossover_uniform2
