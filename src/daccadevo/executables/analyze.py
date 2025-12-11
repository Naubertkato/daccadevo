from pathlib import Path

import yaml

from daccadevo.optimization import default_analysis, get_data


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file_or_directory", nargs='+', help='Files or directories to analyze.')
    parser.add_argument('-c', '--configFilename', type=str, default=None, help = "Path of configuration file (if different from saved results)")
    parser.add_argument('-m', '--merge', action='store_true', help = "Aggregate all results")
    parser.add_argument('-n', '--nbest', type=int, default=3, help = "Number of best individuals to re-evaluate")
    parser.add_argument('-t', '--threshold', type=float, default=None, help = "Number of best individuals to re-evaluate")
    return parser

def setup_config(configFilename, path):
    config = None
    if configFilename is not None:
        with open(configFilename) as f:
            config = yaml.safe_load(f)
        if "dataDir" not in config:
            config["dataDir"] = path if path.is_dir() else path.parent
    return config

def main():
    parser = parse_args()
    args =  parser.parse_args()
    config = None
    for entry in args.file_or_directory:
        p = Path(entry)
        config = setup_config(args.configFilename,p)
        if p.is_dir():
            dt = [get_data(f) for f in p.glob("*.p")]
        else:
            dt = [get_data(p)]
        default_analysis(dt, config= config, merge_data=args.merge, n_best=args.nbest, threshold_best=args.threshold, verbose=True)

if __name__ == "__main__":
    main()
