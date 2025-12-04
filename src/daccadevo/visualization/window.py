"""
window.py
"""

from PySide6.QtWidgets import QComboBox, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from daccadevo.visualization.view import GraphView
from daccadevo.visualization.graph_builder import GraphBuilder
import numpy as np
import os

class MainWindow(QWidget):
    def __init__(self, parent=None, dict_network=None, figure_path=None, key=None, show_inhibitors = True):
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
                    'stabilities': np.array([1.]),
                    'activations': np.array([[1.]]),
                    'inhibitions': np.array([[[0.]]]),
                    'predator_prey_templates': np.array([0.1])
         }
        graph_builder = GraphBuilder()
        self.graph = graph_builder.build_graph(self.dict_network, show_inhibitors = show_inhibitors)
        
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