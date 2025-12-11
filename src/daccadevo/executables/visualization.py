"""
visualization.py
"""

import os
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import yaml
from PySide6.QtWidgets import QApplication

import daccadevo.wrappers as wr
from daccadevo.visualization.window import MainWindow


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pickle_file", type=str, help="Result file where individuals are stored")
    parser.add_argument("--cell", type=int, nargs="*")
    parser.add_argument("--timeseries", action='store_true', help="Simulate the system and show its time series.")
    parser.add_argument("--config", type=str, default=None, help="Used to restore the simulation settings. \
        If not provided, defaults to the configuration stored in the pickle file")
    parser.add_argument("--no-inhibitors",action='store_true')
    parser.add_argument("-v", "--verbose",action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.pickle_file):
        raise FileNotFoundError(f"This pickle file does not exist: {args.pickle_file}")
    with open(args.pickle_file, "rb") as f:
        raw_data = pickle.load(f)

    if args.cell is not None:
        key = tuple(args.cell)
        if key not in raw_data["container"].solutions:
            raise KeyError(f"{key} does not exist in container")
        key_cell = raw_data["container"].solutions[key]
        if not key_cell:
            raise ValueError("The specified cell is empty.")
        network_sequence=key_cell[0]
    else:
        key = "best"
        network_sequence=raw_data["container"].best
    dict_network = {}
    dict_network['stabilities'] = getattr(network_sequence, 'stabilities', None)
    dict_network['activations'] = getattr(network_sequence, 'activations', None)
    dict_network['inhibitions'] = getattr(network_sequence, 'inhibitions', None)
    dict_network['pseudo_templates'] = getattr(network_sequence, 'pseudo_templates', None)
    dict_network['predator_prey_templates'] = getattr(network_sequence, 'predator_prey_templates', None)

    if args.verbose:
        print(key, f"{len(dict_network['stabilities'])} nodes", network_sequence)

    config = args.config
    if config is not None:
        config = yaml.safe_load(open(config))
        if args.verbose:
            print("Configuration file:",config)
    else:
        config = raw_data["config"]

    if args.timeseries:
        figure_path = plot_timeseries(network_sequence, config = config)
    else:
        figure_path = None

    app = QApplication(sys.argv)
    window = MainWindow(dict_network=dict_network, figure_path=figure_path, key=key, show_inhibitors = not args.no_inhibitors)
    window.show()
    sys.exit(app.exec())

def plot_timeseries(network_sequence, scales = [300.0, 200.0, 50.0, 1.6], offset = [10.0, 0.0, 0.0], config = None):
    daccadIndivarray = np.array(network_sequence)
    wrapper = wr.CLI_wrapper()

    nNodes = network_sequence.nb_nodes
    basearray = daccadIndivarray[:nNodes+nNodes*nNodes+nNodes*nNodes*nNodes]
    scaling = [scales[0]]*nNodes + [scales[1]]* nNodes*nNodes*(nNodes+1)
    if len(scales) > 1 and len(daccadIndivarray) > len(basearray):
        scaling += [scales[2]]*nNodes
    myarray = np.array(scaling)*daccadIndivarray

    # TODO: explain offset
    #scaling2 = [offset[0] if myarray[i] > 0 else 0.0 for i in range(0,nNodes)]
    #scaling2.extend([offset[1]] * (nNodes*nNodes*(nNodes+1)+nNodes))
    #myarray2 = myarray+ np.array(scaling2)

    jikeiretu = wrapper.submitPENSystem(myarray, nNodes = nNodes, config = config)
    if "profiling" in jikeiretu[0]:
        jikeiretu = jikeiretu[1:]
    dataResult = [[float(j) for j in i[:-1]] for i in jikeiretu]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5))
    ax1.plot(dataResult)
    ax1.set_title("All Columns in dataResult")
    ax1.grid(True)

    y = np.array(dataResult)[:, 0]
    ax2.plot(y, color="orange")
    ax2.set_title("Node 0")
    ax2.grid(True)

    fig.tight_layout()
    folder_path = "temp"
    os.makedirs(folder_path, exist_ok=True)
    tmp_fig_path = os.path.join(folder_path, "temp.png")
    plt.savefig(tmp_fig_path,  dpi=200)

    return tmp_fig_path



if __name__ == "__main__":
    main()


