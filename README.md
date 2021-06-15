# DACCAD EVO #

Python wrapper to combine DACCAD with QDPY

## Usage

$ python3 scripts/DACCADRun.py -c config_file

The DACCADRun.py script is the main script to start an optimization.
If no fitness function is specified, the system will default to using the oscillator fitness function

## Example

$ python3 scripts/DACCADRun.py -c configs/test.yaml