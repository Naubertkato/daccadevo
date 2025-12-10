from qdpy.base import registry
from qdpy.experiment import QDExperiment
from daccadevo.core.evaluation import oscill_eval_fn

class DACCADExperiment(QDExperiment):
    """
    Extention of qdpy's Quality Diversity experiment to automatically
    extract the evaluation function from the configuration file and
    default to `oscill_eval_fn` if not provided.
    """
    def __init__(self, config_filename, **kwargs):
        super().__init__(config_filename, **kwargs)
        if 'eval_fn' in self.config:
            self._eval_fn = registry[self.config['eval_fn']]          
        else:
            self._eval_fn = oscill_eval_fn
        
    def reinit(self):
        super().reinit()
        self.env_name = self.config['daccad']['env_name']
        
    def eval_fn(self, ind):
        return self._eval_fn(ind, config = self.config)