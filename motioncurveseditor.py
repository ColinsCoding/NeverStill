from PyQt5 import QtWidgets

import pyqtgraph as pg

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curves Editor")
        
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.position_plot = pg.PlotWidget()
        self.velocity_plot = pg.PlotWidget()
        self.acceleration_plot = pg.PlotWidget()

        layout.addWidget(self.position_plot)
        layout.addWidget(self.velocity_plot)
        layout.addWidget(self.acceleration_plot)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())
