import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from src.ui import MainWindow

if __name__ == "__main__":
    # Qt6 enables high-DPI scaling automatically by default.
    
    # Ensure system Qt6 plugins are loaded
    QCoreApplication.addLibraryPath('/usr/lib/qt6/plugins')
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

