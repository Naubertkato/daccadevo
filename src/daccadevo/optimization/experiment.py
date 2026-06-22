from functools import partial

from qdpy.base import registry
from qdpy.experiment import QDExperiment

from daccadevo.core.evaluation import oscill_eval_fn
from daccadevo.wrappers import default_cli_wrapper


class DACCADExperiment(QDExperiment):
    """
    Extention of qdpy's Quality Diversity experiment to automatically
    extract the evaluation function from the configuration file.
    Defaults to `oscill_eval_fn` if not provided.

    Parameters
    ----------
    config_filename: path to the configuration file
        follows the qdpy format. Two additional entries are recognized:
        - wrapper: specify which DACCAD wrapper to use (defaults to `cli`)
        - eval_fn: specify which evaluation function to use (defaults to `oscill_eval_fn`)

    kwargs: arguments passed directly to the super constructor
        follows qdpy's QDExperiement format.

    Attributes
    ----------
    _wrapper: DACCAD_Wrapper
        A wrapper used to simulate individuals with DACCAD.
        Can be set by using the "wrapper" keyword in the configuration file
        (pointing to a registered wrapper object). Otherwise, defaults to
        the `default_cli_wrapper`.

    _eval_fn: Callable
        An evaluation function following the qdpy format: takes an `Individual`
        as argument, as well as a configuration dictionary used to pass additional
        arguments. Either returns the same `Individual` with updated fitness
        and features, or two tuples corresponding to the fitness and features.
    """
    def __init__(self, config_filename, **kwargs):
        super().__init__(config_filename, **kwargs)
        if 'wrapper' in self.config:
            self._wrapper = registry[self.config['wrapper']](self.config)
        else:
            self._wrapper = default_cli_wrapper

        if 'eval_fn' in self.config:
            self._eval_fn = registry[self.config['eval_fn']]
        else:
            self._eval_fn = oscill_eval_fn
        self._eval_fn = partial(self._eval_fn, wrapper=self._wrapper)

    def reinit(self):
        """
        Overwrite of the QDExperiment `reinint`, setting up the `env_name` to match
        that of the DACCAD environment.
        """
        super().reinit()
        self.env_name = self.config['daccad']['env_name']

    def eval_fn(self, ind):
        """
        Overwrite of the QDExperiment `eval_fn`, calling automatically the evaluation function
        set during construction, and passing `self.config` as config argument (so that the call
        matches the signature of `eval_fn` in `QDExperiment`).

        Arguments
        ---------
        ind: DaccadIndividual
            The indidivual solution to evaluate.

        """
        return self._eval_fn(ind, config = self.config)
