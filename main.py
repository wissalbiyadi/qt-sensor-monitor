import sys
import random
import csv
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

class SensorMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Sensor Monitor")
        self.setGeometry(100, 100, 900, 600)

        # Central Widget and Layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.plot_widget = pg.PlotWidget(title="Live Sensor Data")
        self.plot_widget.setLabel('left', 'Sensor Value')
        self.plot_widget.setLabel('bottom', 'Time')

        self.x = list(range(100))
        self.temp_data = [0]*100
        self.accel_data = [0]*100

        self.temp_line = self.plot_widget.plot(self.x, self.temp_data, pen='r', name="Temperature")
        self.accel_line = self.plot_widget.plot(self.x, self.accel_data, pen='b', name="Acceleration")

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)

        # Buttons
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.save_button = QtWidgets.QPushButton("Save Data")

        self.start_button.clicked.connect(self.timer.start)
        self.stop_button.clicked.connect(self.timer.stop)
        self.save_button.clicked.connect(self.save_data)

        # Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.plot_widget)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

    def update_plot_data(self):
        new_temp = random.randint(20, 30)
        new_accel = random.randint(0, 100)

        self.temp_data = self.temp_data[1:] + [new_temp]
        self.accel_data = self.accel_data[1:] + [new_accel]

        self.temp_line.setData(self.x, self.temp_data)
        self.accel_line.setData(self.x, self.accel_data)

    def save_data(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sensor_data_{timestamp}.csv"

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Temperature", "Acceleration"])
            for i in range(len(self.temp_data)):
                writer.writerow([i, self.temp_data[i], self.accel_data[i]])

        QtWidgets.QMessageBox.information(self, "Data Saved", f"Data saved to {filename}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = SensorMonitor()
    main_win.show()
    sys.exit(app.exec_())
