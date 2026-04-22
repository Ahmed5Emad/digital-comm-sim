# Digital Communication Simulator

A real-time Python-based simulator for fundamental digital communication modulation techniques.

## Features

- **Real-time Modulation:** Simulate ASK, FSK, and PSK systems.
- **Interactive UI:** Control Frequency, Noise (SNR), and input bit sequences.
- **High-Quality Plotting:** Uses `matplotlib` for crisp, publication-quality waveform visualization.
- **Cross-Platform:** Automatic builds for Windows (.exe) and Linux (AppImage).

## Getting Started

### Prerequisites

- Python 3.12+
- `pip`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmed5Emad/digital-comm-sim.git
   cd digital-comm-sim
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Usage

Run the simulator directly:
```bash
python main.py
```

## Built With

- [PySide6](https://doc.qt.io/qtforpython/) - UI framework
- [Matplotlib](https://matplotlib.org/) - Plotting library
- [NumPy/SciPy](https://numpy.org/) - Signal processing math

