import argparse
import warnings

from daccadevo.optimization.experiment import DACCADExperiment


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configFilename', type=str, default='configs/test.yaml', help = "Path of configuration file")
    parser.add_argument('-e', '--evaluation', type=str, default=None, help = "Path to the python file providing the implementation of the evaluation function")
    parser.add_argument('-o', '--resultsBaseDir', type=str, default='results/', help = "Path of results files")
    parser.add_argument('-p', '--parallelismType', type=str, default='concurrent', help = "Type of parallelism to use")
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-r','--repeats', type=int, default=1, help="Number of repeats for evaluations")
    return parser.parse_args()

def create_base_config(args):
    base_config = {}
    if len(args.resultsBaseDir) > 0:
        base_config['resultsBaseDir'] = args.resultsBaseDir
    return base_config


def create_experiment(args, base_config):
    exp = DACCADExperiment(args.configFilename, parallelism_type =args.parallelismType, seed=args.seed, base_config=base_config)
    print("INFO: Using configuration file '%s'. Instance name: '%s'" % (args.configFilename, exp.instance_name))
    return exp

def main():
    import traceback
    args = parse_args()
    base_config = create_base_config(args)
    if args.evaluation is not None:
        import importlib.util
        import sys
        from pathlib import Path
        p = Path(args.evaluation)
        name = p.stem
        module_name = ".".join(p.parent.parts)+"."+name
        spec = importlib.util.spec_from_file_location(module_name, p)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    for _ in range(args.repeats):
        try:
            exp = create_experiment(args, base_config)
            exp.run()
        except Exception as e:
            warnings.warn(f"Run failed: {e!s}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
