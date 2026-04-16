:py:mod:`daccadevo.core.evaluation`
===================================

.. py:module:: daccadevo.core.evaluation

.. autodoc2-docstring:: daccadevo.core.evaluation
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`evaluate_timeseries <daccadevo.core.evaluation.evaluate_timeseries>`
     - .. autodoc2-docstring:: daccadevo.core.evaluation.evaluate_timeseries
          :summary:
   * - :py:obj:`get_standard_metrics <daccadevo.core.evaluation.get_standard_metrics>`
     - .. autodoc2-docstring:: daccadevo.core.evaluation.get_standard_metrics
          :summary:
   * - :py:obj:`oscill_eval_fn <daccadevo.core.evaluation.oscill_eval_fn>`
     - .. autodoc2-docstring:: daccadevo.core.evaluation.oscill_eval_fn
          :summary:

API
~~~

.. py:function:: evaluate_timeseries(daccadIndiv, config=None, scales=[1000.0, 200.0], default_enzymes={'pol': 1.0, 'nick': 1.0, 'exo': 1.0}, wrapper=wr.default_cli_wrapper, **kwargs)
   :canonical: daccadevo.core.evaluation.evaluate_timeseries

   .. autodoc2-docstring:: daccadevo.core.evaluation.evaluate_timeseries

.. py:function:: get_standard_metrics(daccadIndiv)
   :canonical: daccadevo.core.evaluation.get_standard_metrics

   .. autodoc2-docstring:: daccadevo.core.evaluation.get_standard_metrics

.. py:function:: oscill_eval_fn(daccadIndiv, config=None, npeaks=1, **kwargs)
   :canonical: daccadevo.core.evaluation.oscill_eval_fn

   .. autodoc2-docstring:: daccadevo.core.evaluation.oscill_eval_fn
