"""
window.py
"""

# from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QWidget
from PySide6.QtWidgets import QComboBox, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QPointF, QEasingCurve, QSize, Qt
from PySide6.QtGui import QPixmap, QPainter, QImage
import networkx as nx
from node import Node
from nodes import NormalNode, PseudoNode, PredatorNode, ActivationNode
from edges import ActivationEdge, AutoActivationEdge, InhibitorEdge, PredatorPreyEdge, PseudoEdge
from edge import Edge
from view import GraphView
from graph_builder import GraphBuilder
from scene_builder import SceneBuilder
import numpy as np
import sys, os
array = np.array

class MainWindow(QWidget):
    def __init__(self, parent=None, dict_network=None, figure_path=None, key=None):
        super().__init__(parent)
        self.resize(800, 600)
        self.setGeometry(800, 600, 800, 600)
        self.dict_network = dict_network
        self.figure_path = figure_path
        self.key = key
        
        if dict_network is not None:
            self.dict_network = dict_network
        else:
            self.dict_network = {
                    'stabilities': array([0.32414728, 0.55184075, 0.02224416, 0.06769786, 0.04517213, 0.02649793]),
                    'activations': array([[0.        , 0.        , 0.        , 0.        , 0.40467229,
                                                0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        ,
                                                0.        ],
                                            [0.54206948, 0.        , 0.20922323, 0.        , 0.        ,
                                                0.        ],
                                            [0.        , 0.06412739, 0.        , 0.07471709, 0.        ,
                                                0.        ],
                                            [0.        , 0.        , 0.        , 0.00687618, 0.        ,
                                                0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.93153457,
                                                0.        ]]),
                    'inhibitions': array([[[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.0627569 , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]],
                                        [[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [1.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]],
                                        [[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.01898459, 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]],
                                        [[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]],
                                        [[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]],
                                        [[0.        , 0.        , 0.        , 0.        , 0.47786695, 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.81454706, 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                            [0.        , 0.        , 0.        , 0.        , 0.        , 0.        ]]]),
                    'predator_prey_templates': array([0.51, 0., 0., 0., 0., 0.])
         }
        graph_builder = GraphBuilder()
        self.graph = graph_builder.build_graph(self.dict_network)
        
        self.setWindowTitle("Main")
        self.view = GraphView(self.graph)
        b_layout = QHBoxLayout()
        
        self.choice_combo = QComboBox()
        self.choice_combo.addItems(self.view.get_nx_layouts())
        self.choice_combo.currentTextChanged.connect(self.view.set_nx_layout)
        b_layout.addWidget(self.choice_combo)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveButton_clicked)
        b_layout.addWidget(self.saveButton)
        
        if figure_path:
            self.timeSeriesButton = QPushButton("Timeseries", self)
            self.timeSeriesButton.clicked.connect(self.timeSeriesButton_clicked)
            b_layout.addWidget(self.timeSeriesButton)
        
        self.quitButton = QPushButton("Quit", self)
        self.quitButton.clicked.connect(self.quitButton_clicked)
        b_layout.addWidget(self.quitButton)
        
        v_layout = QVBoxLayout(self)
        v_layout.addLayout(b_layout)
        v_layout.addWidget(self.view)    
        
    def quitButton_clicked(self):
        self.close()

    def timeSeriesButton_clicked(self):
        self.w = timeSeriesWindow(figure_path=self.figure_path, key=self.key)
        self.w.show()

    def saveButton_clicked(self):
        if isinstance(self.key, tuple):
            key_str = "_".join(map(str, self.key))
        else:
            key_str = self.key
        pixmap = self.view.grab()
        pixmap.setDevicePixelRatio(2)
        scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled_pixmap.save(f"temp/network_{key_str}.png", "PNG")

class timeSeriesWindow(QWidget):
    def __init__(self, parent=None, figure_path=None, key=None):
        super().__init__(parent)
        self.setWindowTitle('Timeseries')
        self.setFixedSize(800, 600)
        self.setGeometry(200, 300, 800, 600)

        self.figure_path = figure_path
        self.key = key
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveButton_clicked)
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(figure_path)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.image_label)
    
    def saveButton_clicked(self):
        if isinstance(self.key, tuple):
            key_str = "_".join(map(str, self.key))
        else:
            key_str = self.key
        new_path = f"temp/plot_{key_str}.png"
        os.rename(self.figure_path, new_path)


    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    # Create a networkx graph
    widget = MainWindow()
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())