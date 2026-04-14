# DACCADevo #

Python wrapper for the DACCAD molecular system simulator, combining it with the Quality-Diversity optimization library QDPY.

For the version of DACCADevo used in the paper Aubert-Kato, Nathanael, and Mika Ito. "Exploration of Reservoir Properties in Molecular Computing Systems." 2024 IEEE Congress on Evolutionary Computation (CEC), check the `reservoir` branch.

## Installation

You can install the current version of the code through pip or uv.

### From a local folder

```bash
$ pip install .
```

or

```bash
$ uv pip install .
```

### Directly from repository

```bash
$ pip install git+https://AubertKato@bitbucket.org/AubertKato/daccadevo.git
```

or

```bash
$ uv pip install git+https://AubertKato@bitbucket.org/AubertKato/daccadevo.git
```

## Installing DACCAD

Most features in DACCADEvo rely on DACCAD. The path to your DACCAD installation should be provided in the configuration file when performing a run. If not specified, DACCAD is assumed to be in the parent directory.

### Download the latest version of DACCAD

```bash
$ git clone git@bitbucket.org:AubertKato/daccad.git
```

### Compile the code

```bash
$ cd daccad
$ ./gradlew dist
```

## Using development features

DACCADevo provides settings to run optimizations relying on development features of QDPY. To use those settings, you need to install `PyTorch` as well as the development branch of QDPY. For instance, with pip:

```bash
$ pip install torch git+https://gitlab.com/leo.cazenille/qdpy.git@develop
```

## Usage

DACCADevo provides three CLI interfaces for fast setup: one for optimization, one for the analysis of optimization results, and one for the direct
visualization of molecular systems.

As a library, DACCADEvo provides additional functionalities for interfacing with DACCAD and analyzing molecular systems.
See the examples for more details.

### Optimization

The `optimize` module allows you to start an optimization.
If no fitness function is specified, the system will default to using the oscillator fitness function.

Direct call:

```bash
$ python3 -m daccadevo.executables.optimize[-c config_file] [-e evaluation_file] [-r repeats]
```

Using Docker:

You need to build the image first (only once). Assuming you are at the root of the daccadevo folder:

```bash
$ docker build -t daccadevo .
```

Then, run the following script:

```bash
$ ./runDockerExp.sh config_file repeats_number evaluation_file [image_name]
```

If running the default optimization function, `evaluation_file` can be omitted. 
Note that both `config_file` and `evaluation_file` must be present inside the Docker image.

`image_name` only needs to be specified if it is different from `daccadevo`.

## Examples

### Dummy optimization

To perform 5 independent runs described in the `configs/short_test.yaml` file, with an evaluation 
function defined in `examples/test_eval.py`, run:

```bash
$ python3 -m daccadevo.executables.optimize -c configs/short_test.yaml -r 5 -e examples/test_eval.py
```

Or through docker:

```bash
$ ./runDockerExp.sh configs/short_test.yaml 5 examples/test_eval.py
```

Note that the name of the function in the Python file needs to match the `eval_fn` entry in the configuration file. 

### Results analysis

The `analyze` CLI allows you to see basic statistics about a run or set of runs.

```bash
$ python3 -m daccadevo.executables.analyze results/short_test -c configs/short_test.yaml -n 5 --merge
```

### Visualization

The `visualization` CLI allows you to see the network of a given individual from a saved run (.p files).
You may provide the position of the individual with `--cell` followed by its index (as provided by `analysis`
for instance). If no position is provided, the best individual will be selected by default.

```bash
$ python3 -m daccadevo.executables.visualization results/short_test/final.p 
```

