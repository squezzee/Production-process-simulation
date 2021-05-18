from PyQt5 import QtCore, QtWidgets
# import psutil
import sys
import time

from login import *


class ControlPanel(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.operator_last_activity = time.time()

        # PROCESS VARIABLES LABELS INITIALIZATION

        self.engine_temp_label = QtWidgets.QLabel(self.centralwidget)
        self.production_line_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.engine_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.fan_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.production_line_load_label = QtWidgets.QLabel(self.centralwidget)
        self.cooling_system_temp_label = QtWidgets.QLabel(self.centralwidget)

        # WARNING PROCESS VARIABLES LABELS INITIALIZATION

        self.warning_engine_temp_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_production_line_load_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_cooling_system_temp_label = QtWidgets.QLabel(self.centralwidget)
        self.operator_presence_check_label = QtWidgets.QLabel(self.centralwidget)
        self.operator_presence_time_label = QtWidgets.QLabel(self.centralwidget)

        # BUTTONS INITIALIZATION

        self.logout_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.instruction_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.start_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stop_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.operator_presence_check_pushButton = QtWidgets.QPushButton(self.centralwidget)

        # PROGRESSBAR INITIALIZATION

        self.engine_speed_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.fan_speed_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.production_line_speed_progressBar = QtWidgets.QProgressBar(self.centralwidget)

        # PROCESS VARIABLES VALUES INITIALIZATION

        self.engine_temp_lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.production_line_load_lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.cooling_system_temp_lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)

        # PROCESS VARIABLES VALUES SLIDERS INITIALIZATION

        self.engine_speed_ScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.production_line_speed_ScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.fan_speed_ScrollBar = QtWidgets.QScrollBar(self.centralwidget)

        # CREATE DICT FOR CONNECTING PROGRESS BARS WITH SCROLL BARS

        self.progressBars_and_scrollBars_dict = {
            self.engine_speed_progressBar: self.engine_speed_ScrollBar,
            self.engine_speed_ScrollBar: self.engine_speed_progressBar,
            self.fan_speed_progressBar: self.fan_speed_ScrollBar,
            self.fan_speed_ScrollBar: self.fan_speed_progressBar,
            self.production_line_speed_progressBar: self.production_line_speed_ScrollBar,
            self.production_line_speed_ScrollBar: self.production_line_speed_progressBar}

        self.setup_ui()

        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_ui(self):

        # PROCESS VARIABLES LABELS INITIALIZATION

        self.engine_temp_label.setGeometry(QtCore.QRect(120, 270, 141, 17))
        self.engine_temp_label.setObjectName("engine_temp_label")
        self.engine_temp_label.setText("Temperatura silnika")

        self.production_line_speed_label.setGeometry(QtCore.QRect(120, 180, 191, 17))
        self.production_line_speed_label.setObjectName("production_line_speed_label")
        self.production_line_speed_label.setText("Prędkość linii produkcyjnej")

        self.engine_speed_label.setGeometry(QtCore.QRect(120, 80, 161, 17))
        self.engine_speed_label.setObjectName("engine_speed_label")
        self.engine_speed_label.setText("Prędkość silnika")

        self.fan_speed_label.setGeometry(QtCore.QRect(120, 130, 171, 17))
        self.fan_speed_label.setObjectName("fan_speed_label")
        self.fan_speed_label.setText("Prędkość wentylatorów")

        self.production_line_load_label.setGeometry(QtCore.QRect(120, 320, 201, 17))
        self.production_line_load_label.setObjectName("production_line_load_label")
        self.production_line_load_label.setText("Obciążenie linii produkcyjnej")

        self.cooling_system_temp_label.setGeometry(QtCore.QRect(120, 370, 291, 17))
        self.cooling_system_temp_label.setObjectName("cooling_system_temp_label")
        self.cooling_system_temp_label.setText("Temperatura układu chłodzenia")

        # WARNING PROCESS VARIABLES LABELS INITIALIZATION

        self.warning_engine_temp_label.setGeometry(QtCore.QRect(510, 270, 281, 21))
        self.warning_engine_temp_label.setObjectName("warning_engine_temp_label")
        self.warning_engine_temp_label.setText("Ostrzeżenie dot. temp. silnika")

        self.warning_production_line_load_label.setGeometry(QtCore.QRect(510, 320, 281, 21))
        self.warning_production_line_load_label.setObjectName("warning_production_line_load_label")
        self.warning_production_line_load_label.setText("Ostrzeżenie dot. obciążenia linii prod.")

        self.warning_cooling_system_temp_label.setGeometry(QtCore.QRect(510, 370, 281, 21))
        self.warning_cooling_system_temp_label.setObjectName("warning_cooling_system_temp_label")
        self.warning_cooling_system_temp_label.setText("Ostrzeżenie dot. temp. układu chłodzenia")

        self.operator_presence_check_label.setGeometry(QtCore.QRect(120, 20, 361, 17))
        self.operator_presence_check_label.setObjectName("operator_presence_check_label")
        self.operator_presence_check_label.setText("Wymagane sprawdzeie obecności operatora!")

        self.operator_presence_time_label.setGeometry(QtCore.QRect(610, 20, 121, 21))
        self.operator_presence_time_label.setObjectName("operator_presence_time_label")
        self.operator_presence_time_label.setText("30:00")

        # BUTTONS INITIALIZATION

        self.logout_pushButton.setGeometry(QtCore.QRect(140, 480, 89, 25))
        self.logout_pushButton.setObjectName("logout_pushButton")
        self.logout_pushButton.setText("Wyloguj")
        self.logout_pushButton.clicked.connect(self.operator_log_out)

        self.instruction_pushButton.setGeometry(QtCore.QRect(280, 480, 89, 25))
        self.instruction_pushButton.setObjectName("instruction_pushButton")
        self.instruction_pushButton.setText("Instrukcja")

        self.start_pushButton.setGeometry(QtCore.QRect(430, 480, 89, 25))
        self.start_pushButton.setObjectName("start_pushButton")
        self.start_pushButton.setText("Start")

        self.stop_pushButton.setGeometry(QtCore.QRect(570, 480, 89, 25))
        self.stop_pushButton.setObjectName("stop_pushButton")
        self.stop_pushButton.setText("Stop")

        self.operator_presence_check_pushButton.setGeometry(QtCore.QRect(500, 20, 89, 25))
        self.operator_presence_check_pushButton.setObjectName("operator_presence_check_pushButton")
        self.operator_presence_check_pushButton.setText("Potwierdź")

        # PROGRESSBAR INITIALIZATION

        self.engine_speed_progressBar.setGeometry(QtCore.QRect(360, 80, 118, 23))
        self.engine_speed_progressBar.setProperty("value", 25)
        self.engine_speed_progressBar.setObjectName("engine_speed_progressBar")

        self.fan_speed_progressBar.setGeometry(QtCore.QRect(360, 130, 118, 23))
        self.fan_speed_progressBar.setProperty("value", 24)
        self.fan_speed_progressBar.setObjectName("fan_speed_progressBar")

        self.production_line_speed_progressBar.setGeometry(QtCore.QRect(360, 180, 118, 23))
        self.production_line_speed_progressBar.setProperty("value", 26)
        self.production_line_speed_progressBar.setObjectName("production_line_speed_progressBar")

        # PROCESS VARIABLES VALUES INITIALIZATION

        self.engine_temp_lcdNumber.setGeometry(QtCore.QRect(420, 270, 64, 23))
        self.engine_temp_lcdNumber.setObjectName("engine_temp_lcdNumber")
        self.engine_temp_lcdNumber.setProperty("value", 24)

        self.production_line_load_lcdNumber.setGeometry(QtCore.QRect(420, 320, 64, 23))
        self.production_line_load_lcdNumber.setObjectName("production_line_load_lcdNumber")

        self.cooling_system_temp_lcdNumber.setGeometry(QtCore.QRect(420, 370, 64, 23))
        self.cooling_system_temp_lcdNumber.setObjectName("lcdNumber_2")
        self.cooling_system_temp_lcdNumber.setProperty("value", 25)

        # PROCESS VARIABLES VALUES SLIDERS INITIALIZATION

        self.engine_speed_ScrollBar.setGeometry(QtCore.QRect(500, 80, 160, 16))
        self.engine_speed_ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.engine_speed_ScrollBar.setObjectName("engine_speed_ScrollBar")
        self.engine_speed_ScrollBar.setMaximum(101)
        self.engine_speed_ScrollBar.setMinimum(-1)
        self.engine_speed_ScrollBar.valueChanged.connect(
            lambda: self.update_slider(self.engine_speed_ScrollBar)
        )

        self.production_line_speed_ScrollBar.setGeometry(QtCore.QRect(500, 180, 160, 16))
        self.production_line_speed_ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.production_line_speed_ScrollBar.setObjectName("production_line_speed_ScrollBar")
        self.production_line_speed_ScrollBar.setMaximum(101)
        self.production_line_speed_ScrollBar.setMinimum(-1)
        self.production_line_speed_ScrollBar.valueChanged.connect(
            lambda: self.update_slider(self.production_line_speed_ScrollBar)
        )

        self.fan_speed_ScrollBar.setGeometry(QtCore.QRect(500, 130, 160, 16))
        self.fan_speed_ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.fan_speed_ScrollBar.setObjectName("fan_speed_ScrollBar")
        self.fan_speed_ScrollBar.setMaximum(101)
        self.fan_speed_ScrollBar.setMinimum(-1)
        self.fan_speed_ScrollBar.valueChanged.connect(
            lambda: self.update_slider(self.fan_speed_ScrollBar)
        )

    def update_slider(self, slider):
        value = slider.value()
        self.progressBars_and_scrollBars_dict[slider].setProperty('value', value)
        self.operator_last_activity = time.time()

    def operator_log_out(self):
        print("Bout to log out")
        self.close()
        log_window.show()




