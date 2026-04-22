from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                                 QComboBox, QLabel, QSlider, QLineEdit, QPushButton)
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from src.engine import ASKModulator, FSKModulator, PSKModulator

plt.style.use('dark_background')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Communication Simulation")
        self.resize(1000, 700)
        self.setStyleSheet("QMainWindow {background-color: #2d2d2d;} QWidget {background-color: #2d2d2d; color: white;}")
        
        main_layout = QHBoxLayout()
        
        # --- Controls Sidebar ---
        control_layout = QVBoxLayout()
        
        self.system_selector = QComboBox()
        self.system_selector.addItems(["ASK", "FSK", "PSK"])
        control_layout.addWidget(QLabel("Modulation System:"))
        control_layout.addWidget(self.system_selector)
        
        self.input_bits = QLineEdit("10110")
        control_layout.addWidget(QLabel("Input Bits (0/1):"))
        control_layout.addWidget(self.input_bits)
        
        self.update_btn = QPushButton("Update Simulation")
        control_layout.addWidget(self.update_btn)
        
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setRange(1, 20)
        self.freq_slider.setValue(5)
        control_layout.addWidget(QLabel("Carrier Frequency:"))
        control_layout.addWidget(self.freq_slider)
        
        self.snr_slider = QSlider(Qt.Horizontal)
        self.snr_slider.setRange(0, 50)
        self.snr_slider.setValue(50)
        control_layout.addWidget(QLabel("SNR (dB):"))
        control_layout.addWidget(self.snr_slider)
        
        control_layout.addStretch()
        
        # --- Plotting Area ---
        plot_layout = QVBoxLayout()
        self.figure, (self.ax_in, self.ax_out) = plt.subplots(2, 1, figsize=(8, 6))
        self.figure.tight_layout(pad=3.0)
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas, stretch=1)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addLayout(control_layout, stretch=1)
        main_layout.addLayout(plot_layout, stretch=3)
        
        container = QWidget()
        container.setLayout(main_layout)
        container.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(container)
        
        self.update_btn.clicked.connect(self.update_plot)
        self.system_selector.currentIndexChanged.connect(self.update_plot)
        self.freq_slider.valueChanged.connect(self.update_plot)
        self.snr_slider.valueChanged.connect(self.update_plot)
        self.update_plot()
        
    def update_plot(self):
        # Validate Input
        bit_str = self.input_bits.text()
        try:
            data = np.array([int(b) for b in bit_str if b in '01'])
            if len(data) == 0: raise ValueError
        except:
            return # Ignore invalid input
            
        system = self.system_selector.currentText()
        freq = self.freq_slider.value()
        snr = self.snr_slider.value()
        
        # Scale time based on input length
        t = np.linspace(0, len(data), len(data) * 2000, endpoint=False)
        
        # Input Plot
        self.ax_in.clear()
        self.ax_in.plot(t, np.repeat(data, 2000), color='white', linewidth=2)
        self.ax_in.set_title("Input Digital Signal")
        self.ax_in.set_xlim(t[0]-0.1, t[-1]+0.1)
        self.ax_in.grid(True, color='#444444', linestyle='--')
        
        # Output Plot
        if system == "ASK":
            mod = ASKModulator()
            _, modulated = mod.modulate(data, carrier_freq=freq, snr=snr)
        elif system == "FSK":
            mod = FSKModulator()
            _, modulated = mod.modulate(data, freq1=freq, freq2=freq*3, snr=snr)
        else: # PSK
            mod = PSKModulator()
            _, modulated = mod.modulate(data, carrier_freq=freq, snr=snr)
            
        self.ax_out.clear()
        self.ax_out.plot(t, modulated, color='#00FF00', linewidth=1.5)
        self.ax_out.set_title("Output Modulated Signal")
        self.ax_out.set_xlim(t[0]-0.1, t[-1]+0.1)
        self.ax_out.set_ylim(-1.5, 1.5) # Fixed y-limits
        self.ax_out.grid(True, color='#444444', linestyle='--')
        
        self.canvas.draw()





