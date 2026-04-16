:py:mod:`daccadevo.core.mutation_utils`
=======================================

.. py:module:: daccadevo.core.mutation_utils

.. autodoc2-docstring:: daccadevo.core.mutation_utils
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`generateUniform <daccadevo.core.mutation_utils.generateUniform>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateUniform
          :summary:
   * - :py:obj:`generateSparseUniform <daccadevo.core.mutation_utils.generateSparseUniform>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSparseUniform
          :summary:
   * - :py:obj:`generateSparseUniformDomain <daccadevo.core.mutation_utils.generateSparseUniformDomain>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSparseUniformDomain
          :summary:
   * - :py:obj:`generateSobol <daccadevo.core.mutation_utils.generateSobol>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSobol
          :summary:
   * - :py:obj:`generateBinarySobol <daccadevo.core.mutation_utils.generateBinarySobol>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateBinarySobol
          :summary:
   * - :py:obj:`generateSobolConnectionsWithUniformValues <daccadevo.core.mutation_utils.generateSobolConnectionsWithUniformValues>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSobolConnectionsWithUniformValues
          :summary:
   * - :py:obj:`random_log_scale_1000 <daccadevo.core.mutation_utils.random_log_scale_1000>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.random_log_scale_1000
          :summary:
   * - :py:obj:`random_log_scale <daccadevo.core.mutation_utils.random_log_scale>`
     - .. autodoc2-docstring:: daccadevo.core.mutation_utils.random_log_scale
          :summary:

API
~~~

.. py:function:: generateUniform(dimension, indBounds, nb)
   :canonical: daccadevo.core.mutation_utils.generateUniform

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateUniform

.. py:function:: generateSparseUniform(dimension, indBounds, nb, sparsity)
   :canonical: daccadevo.core.mutation_utils.generateSparseUniform

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSparseUniform

.. py:function:: generateSparseUniformDomain(dimension, indBounds, nb, sparsityDomain)
   :canonical: daccadevo.core.mutation_utils.generateSparseUniformDomain

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSparseUniformDomain

.. py:function:: generateSobol(dimension, indBounds, nb)
   :canonical: daccadevo.core.mutation_utils.generateSobol

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSobol

.. py:function:: generateBinarySobol(dimension, indBounds, nb, cutoff=0.5)
   :canonical: daccadevo.core.mutation_utils.generateBinarySobol

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateBinarySobol

.. py:function:: generateSobolConnectionsWithUniformValues(dimension, indBounds, nb, cutoff=0.5, nbValueSets=1)
   :canonical: daccadevo.core.mutation_utils.generateSobolConnectionsWithUniformValues

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.generateSobolConnectionsWithUniformValues

.. py:function:: random_log_scale_1000()
   :canonical: daccadevo.core.mutation_utils.random_log_scale_1000

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.random_log_scale_1000

.. py:function:: random_log_scale()
   :canonical: daccadevo.core.mutation_utils.random_log_scale

   .. autodoc2-docstring:: daccadevo.core.mutation_utils.random_log_scale
