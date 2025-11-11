"""
mainDACCAD.py
"""

from PySide6.QtCore import (QEasingCurve, QLineF,
                            QParallelAnimationGroup, QPointF, QSizeF,
                            QPropertyAnimation, QRectF, Qt)
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF, QPainterPath
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsItem,
                               QGraphicsObject, QGraphicsScene, QGraphicsView,
                               QStyleOptionGraphicsItem, QVBoxLayout, QWidget)

import networkx as nx

from nodes import NormalNode, ActivationNode, PseudoNode, PredatorNode
from edges import ActivationEdge, AutoActivationEdge, InhibitorEdge, PredatorPreyEdge, PseudoEdge
from window import MainWindow 

import pickle, os, sys

import numpy as np
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..") 
sys.path.append(project_root)
import individual, submitDACCAD


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pickle_file")
    parser.add_argument("--cell", type=int, nargs="*")
    parser.add_argument("--timeseries", type=bool, nargs="?")
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
        dict_network = {}
        dict_network['stabilities'] = getattr(network_sequence, 'stabilities', None)
        dict_network['activations'] = getattr(network_sequence, 'activations', None)
        dict_network['inhibitions'] = getattr(network_sequence, 'inhibitions', None)
        dict_network['pseudo_templates'] = getattr(network_sequence, 'pseudo_templates', None)
        dict_network['predator_prey_templates'] = getattr(network_sequence, 'predator_prey_templates', None)
    else:
        key = "best"
        network_sequence=raw_data["container"].best
        dict_network=network_sequence.__dict__

    print(key)

    
    # if args.timeseries:
    #     figure_path = plot_timeseries(network_sequence)
    # else:
    #     figure_path = None
    figure_path = None

    app = QApplication(sys.argv)
    window = MainWindow(dict_network=dict_network, figure_path=figure_path, key=key)
    window.show()
    sys.exit(app.exec())

def plot_timeseries(network_sequence, scales = [300.0, 200.0, 50.0, 1.6], offset = [10.0, 0.0, 0.0], npeaks = 1):
    daccadIndivarray = np.array(network_sequence)
    config = {
        'daccad': {
            'path':'../../daccad',
            'sim_length': 1500,
            'kmPredator': 1760,
            'exo': daccadIndivarray[-2]*scales[3],
            'pol': daccadIndivarray[-1]*scales[3] + offset[2]
        }
    }

    daccadIndivarray = daccadIndivarray[:-2]
    nNodes = network_sequence.nb_nodes
    scaling = [scales[0]]*nNodes + [scales[1]]* nNodes*nNodes*(nNodes+1) + [scales[2]]*nNodes
    myarray = np.array(scaling)*daccadIndivarray
    scaling2 = [offset[0] if myarray[i] > 0 else 0.0 for i in range(0,nNodes)]
    scaling2.extend([offset[1]] * (nNodes*nNodes*(nNodes+1)+nNodes))
    myarray2 = myarray+ np.array(scaling2)
    jikeiretu = submitDACCAD_pp.submitPENSystem_pp(myarray2, nNodes = nNodes, config = config["daccad"])
    dataResult = [[float(j) for j in i[:-1]] for i in jikeiretu[0:]]

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


