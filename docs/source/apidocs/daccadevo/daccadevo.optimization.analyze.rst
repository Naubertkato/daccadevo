:py:mod:`daccadevo.optimization.analyze`
========================================

.. py:module:: daccadevo.optimization.analyze

.. autodoc2-docstring:: daccadevo.optimization.analyze
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_data <daccadevo.optimization.analyze.get_data>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.get_data
          :summary:
   * - :py:obj:`extract_from_individuals <daccadevo.optimization.analyze.extract_from_individuals>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.extract_from_individuals
          :summary:
   * - :py:obj:`get_bests <daccadevo.optimization.analyze.get_bests>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.get_bests
          :summary:
   * - :py:obj:`merge_containers <daccadevo.optimization.analyze.merge_containers>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.merge_containers
          :summary:
   * - :py:obj:`get_metric_over_time <daccadevo.optimization.analyze.get_metric_over_time>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.get_metric_over_time
          :summary:
   * - :py:obj:`evaluate_timeseries_on_bests <daccadevo.optimization.analyze.evaluate_timeseries_on_bests>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.evaluate_timeseries_on_bests
          :summary:
   * - :py:obj:`plot_bests <daccadevo.optimization.analyze.plot_bests>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.plot_bests
          :summary:
   * - :py:obj:`default_analysis <daccadevo.optimization.analyze.default_analysis>`
     - .. autodoc2-docstring:: daccadevo.optimization.analyze.default_analysis
          :summary:

API
~~~

.. py:function:: get_data(path)
   :canonical: daccadevo.optimization.analyze.get_data

   .. autodoc2-docstring:: daccadevo.optimization.analyze.get_data

.. py:function:: extract_from_individuals(container, func)
   :canonical: daccadevo.optimization.analyze.extract_from_individuals

   .. autodoc2-docstring:: daccadevo.optimization.analyze.extract_from_individuals

.. py:function:: get_bests(container, n=5, threshold=None, key=lambda indiv: indiv.fitness[0])
   :canonical: daccadevo.optimization.analyze.get_bests

   .. autodoc2-docstring:: daccadevo.optimization.analyze.get_bests

.. py:function:: merge_containers(containers)
   :canonical: daccadevo.optimization.analyze.merge_containers

   .. autodoc2-docstring:: daccadevo.optimization.analyze.merge_containers

.. py:function:: get_metric_over_time(dt, metric='qd_score', batch_size=None)
   :canonical: daccadevo.optimization.analyze.get_metric_over_time

   .. autodoc2-docstring:: daccadevo.optimization.analyze.get_metric_over_time

.. py:function:: evaluate_timeseries_on_bests(container, config, n_best=3, threshold=None, verbose=False, key=lambda indiv: indiv.fitness[0])
   :canonical: daccadevo.optimization.analyze.evaluate_timeseries_on_bests

   .. autodoc2-docstring:: daccadevo.optimization.analyze.evaluate_timeseries_on_bests

.. py:function:: plot_bests(time_series, container, labels=None, configs=None, figname=None)
   :canonical: daccadevo.optimization.analyze.plot_bests

   .. autodoc2-docstring:: daccadevo.optimization.analyze.plot_bests

.. py:function:: default_analysis(evo_data_list, n_best=3, config=None, threshold_best=None, verbose=False, merge_data=True)
   :canonical: daccadevo.optimization.analyze.default_analysis

   .. autodoc2-docstring:: daccadevo.optimization.analyze.default_analysis
