import random
from PyQt5 import QtCore, QtWidgets
import sys
import time

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox


class Worker(QObject):
    finished = pyqtSignal()
    inactive = pyqtSignal()
    second_passed = pyqtSignal()
    logout = pyqtSignal()

    def __init__(self):
        super(Worker, self).__init__(parent=None)
        self.engine_var = 0
        self.production_var = 0
        self.cooling_system_var = 0
        self.last_activity = time.time()
        self._isRunning = False
        self.is_operator_active = False

    def run(self):
        while True:
            if self._isRunning is True:
                self.engine_var = random.randint(-10, 10)/10.0
                self.production_var = random.randint(-10, 10)/10.0
                self.cooling_system_var = random.randint(-10, 10)/10.0
                time.sleep(1)
                self.finished.emit()

    def get_last_activity(self):
        while True:
            if self._isRunning:
                if time.time() - self.last_activity > 20:
                    self.inactive.emit()
                    self.last_activity = time.time()

    def start_timer(self):
        self.is_operator_active = False
        for i in range(0, 20):
            time.sleep(1)
            if self.is_operator_active:
                break
            self.second_passed.emit()
        if self.is_operator_active:
            self.finished.emit()
        else:
            self.logout.emit()

    def stop(self):
        self._isRunning = False


class Login(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.label = QtWidgets.QLabel(self)
        self.label_2 = QtWidgets.QLabel(self)
        self.pushButton = QtWidgets.QPushButton(self)

        self.setup_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_ui(self):
        self.lineEdit.setGeometry(QtCore.QRect(200, 110, 113, 25))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2.setGeometry(QtCore.QRect(200, 150, 113, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.label.setGeometry(QtCore.QRect(90, 110, 67, 17))
        self.label.setObjectName("label")
        self.label.setText("Login")

        self.label_2.setGeometry(QtCore.QRect(90, 150, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Hasło")

        self.pushButton.setGeometry(QtCore.QRect(160, 220, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.confirm_login)
        self.pushButton.setText("Potwierdź")

    def confirm_login(self):
        if self.lineEdit.text() == 'admin' and self.lineEdit_2.text() == 'admin':
            control_panel.show()
            self.hide()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Nieudane logowanie")
            msg.setText("Niepoprawne dane uwierzytelniające, spróbuj \nlogin: \nadmin \nhasło: \nadmin")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


class ControlPanel(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.operator_last_activity = time.time()
        self.rand_engine_temp_var = 0
        self.rand_cooling_system_var = 0
        self.rand_production_line_load_var = 0

        self.thread_production = QThread(parent=self)
        self.worker_production = Worker()
        self.worker_production.moveToThread(self.thread_production)
        self.thread_production.started.connect(self.worker_production.run)
        self.thread_production.start()
        self.worker_production.finished.connect(
            lambda: self.update_lcd_numbers(
                self.worker_production.engine_var,
                self.worker_production.production_var,
                self.worker_production.cooling_system_var
            )
        )

        self.thread_activity = QThread(parent=self)
        self.worker_activity = Worker()
        self.worker_activity.moveToThread(self.thread_activity)
        self.thread_activity.started.connect(self.worker_activity.get_last_activity)
        self.thread_activity.start()
        self.worker_activity.inactive.connect(
            lambda: self.confirm_operator_presence()
            )

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
        self.operator_presence_time_lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)

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

        # CREATE DICT FOR CONNECTING LCD NUMBERS WITH THEIR LABELS

        self.lcd_numbers_to_labels_dict = {
            self.engine_temp_lcdNumber: self.warning_engine_temp_label,
            self.production_line_load_lcdNumber: self.warning_production_line_load_label,
            self.cooling_system_temp_lcdNumber: self.warning_cooling_system_temp_label
        }

        # CREATE DICT FOR PROCESS VARIABLES WARNING VALUES

        self.warnings_dict = {
            self.engine_temp_lcdNumber: {
                'above normal': 60,
                'high': 80,
                'too high': 100
            },

            self.cooling_system_temp_lcdNumber: {
                'above normal': 70,
                'high': 85,
                'too high': 90
            },

            self.production_line_load_lcdNumber: {
                'above normal': 70,
                'high': 85,
                'too high': 90
            },
        }

        self.setup_ui()

        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_ui(self):

        # PROCESS VARIABLES LABELS INITIALIZATION

        self.engine_temp_label.setGeometry(QtCore.QRect(120, 270, 141, 17))
        self.engine_temp_label.setObjectName("engine_temp_label")
        self.engine_temp_label.setText("Temperatura silnika")

        self.production_line_speed_label.setGeometry(QtCore.QRect(120, 130, 171, 17))
        self.production_line_speed_label.setObjectName("production_line_speed_label")
        self.production_line_speed_label.setText("Prędkość produkcji")

        self.engine_speed_label.setGeometry(QtCore.QRect(120, 80, 161, 17))
        self.engine_speed_label.setObjectName("engine_speed_label")
        self.engine_speed_label.setText("Prędkość silnika")

        self.fan_speed_label.setGeometry(QtCore.QRect(120, 180, 191, 17))
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
        self.operator_presence_check_label.hide()

        # BUTTONS INITIALIZATION

        self.logout_pushButton.setGeometry(QtCore.QRect(140, 480, 89, 25))
        self.logout_pushButton.setObjectName("logout_pushButton")
        self.logout_pushButton.setText("Wyloguj")
        self.logout_pushButton.clicked.connect(self.operator_log_out)

        self.instruction_pushButton.setGeometry(QtCore.QRect(280, 480, 89, 25))
        self.instruction_pushButton.setObjectName("instruction_pushButton")
        self.instruction_pushButton.setText("Instrukcja")
        self.instruction_pushButton.clicked.connect(self.show_instruction)

        self.start_pushButton.setGeometry(QtCore.QRect(430, 480, 89, 25))
        self.start_pushButton.setObjectName("start_pushButton")
        self.start_pushButton.setText("Start")
        self.start_pushButton.clicked.connect(self.start_process_simulation)
        self.start_pushButton.clicked.connect(self.start_measure_activity)

        self.stop_pushButton.setGeometry(QtCore.QRect(570, 480, 89, 25))
        self.stop_pushButton.setObjectName("stop_pushButton")
        self.stop_pushButton.setText("Stop")
        self.stop_pushButton.clicked.connect(self.stop_process_simulation)
        self.stop_pushButton.setEnabled(False)

        self.operator_presence_check_pushButton.setGeometry(QtCore.QRect(500, 20, 89, 25))
        self.operator_presence_check_pushButton.setObjectName("operator_presence_check_pushButton")
        self.operator_presence_check_pushButton.setText("Potwierdź")
        self.operator_presence_check_pushButton.clicked.connect(self.operator_is_present)
        self.operator_presence_check_pushButton.hide()

        # PROGRESSBAR INITIALIZATION

        self.engine_speed_progressBar.setGeometry(QtCore.QRect(360, 80, 118, 23))
        self.engine_speed_progressBar.setProperty("value", 0)
        self.engine_speed_progressBar.setObjectName("engine_speed_progressBar")

        self.fan_speed_progressBar.setGeometry(QtCore.QRect(360, 180, 118, 23))
        self.fan_speed_progressBar.setProperty("value", 0)
        self.fan_speed_progressBar.setObjectName("fan_speed_progressBar")

        self.production_line_speed_progressBar.setGeometry(QtCore.QRect(360, 130, 118, 23))
        self.production_line_speed_progressBar.setProperty("value", 0)
        self.production_line_speed_progressBar.setObjectName("production_line_speed_progressBar")

        # PROCESS VARIABLES VALUES INITIALIZATION

        self.engine_temp_lcdNumber.setGeometry(QtCore.QRect(420, 270, 64, 23))
        self.engine_temp_lcdNumber.setObjectName("engine_temp_lcdNumber")
        self.engine_temp_lcdNumber.setProperty("value", 22)

        self.production_line_load_lcdNumber.setGeometry(QtCore.QRect(420, 320, 64, 23))
        self.production_line_load_lcdNumber.setObjectName("production_line_load_lcdNumber")
        self.production_line_load_lcdNumber.setProperty('value', 0)

        self.cooling_system_temp_lcdNumber.setGeometry(QtCore.QRect(420, 370, 64, 23))
        self.cooling_system_temp_lcdNumber.setObjectName("lcdNumber_2")
        self.cooling_system_temp_lcdNumber.setProperty("value", 22)

        self.operator_presence_time_lcdNumber.setGeometry(QtCore.QRect(610, 20, 121, 21))
        self.operator_presence_time_lcdNumber.setObjectName("operator_presence_time_label")
        self.operator_presence_time_lcdNumber.setProperty("value", 10)
        self.operator_presence_time_lcdNumber.hide()

        # PROCESS VARIABLES VALUES SLIDERS INITIALIZATION

        self.engine_speed_ScrollBar.setGeometry(QtCore.QRect(500, 80, 160, 16))
        self.engine_speed_ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.engine_speed_ScrollBar.setObjectName("engine_speed_ScrollBar")
        self.engine_speed_ScrollBar.setMaximum(101)
        self.engine_speed_ScrollBar.setMinimum(-1)
        self.engine_speed_ScrollBar.valueChanged.connect(
            lambda: self.update_slider(self.engine_speed_ScrollBar)
        )

        self.production_line_speed_ScrollBar.setGeometry(QtCore.QRect(500, 130, 160, 16))
        self.production_line_speed_ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.production_line_speed_ScrollBar.setObjectName("production_line_speed_ScrollBar")
        self.production_line_speed_ScrollBar.setMaximum(101)
        self.production_line_speed_ScrollBar.setMinimum(-1)
        self.production_line_speed_ScrollBar.valueChanged.connect(
            lambda: self.update_slider(self.production_line_speed_ScrollBar)
        )

        self.fan_speed_ScrollBar.setGeometry(QtCore.QRect(500, 180, 160, 16))
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
        self.hide()
        log_window.show()

    def show_instruction(self):
        msg = QMessageBox()
        msg.setWindowTitle("Symulator procesu produkcyjnego")
        msg.setText("Twoim zadaniem jest doglądać proces produkcji. Jego trzy kluczowe elementy, sterowane przez Ciebie to:\n"
                    "Prędkość silnika\n"
                    "Prędkość wentylatorów\n"
                    "Prędkość linii produkcyjnej\n"
                    "Mają one wpływ na:\n"
                    "Temperaturę silnika\n"
                    "Temperaturę ukłądu chłodzenia\n"
                    "Obciążenie linii produkcyjnej\n"
                    "Staraj tak się sterować procesem produkcji, aby nie przekraczać wartości krańcowych zmiennych produkcyjnych.\n"
                    "Pomocne przy tym będą kolory danych wartości:\n"
                    "Biały - wszystko ok\n"
                    "Żółty - zmienna powyżej normy\n"
                    "Pomarańczowy - wysoka wartość zmiennej\n"
                    "Czerwony - za wysoka wartość zmiennej\n"
                    "Po wciśnięciu przycisku start rozpocznie się proces produkcji i będziesz mógł za pomocą suwaków "
                    "ustalać wartości zmiennych występujących w procesie. Gdy coś wymknie się spod kontroli zawsze "
                    "możesz użyć przycisku stop, który automatycznie wszystko wyłączy. Ponadto podczas trwania "
                    "produkcji okresowo pojawiać się będzie komunikat o badaniu przytomności. Będziesz miał 20 sekund "
                    "na wciśnięcie przycisku na górze ekranu (pojawi się wraz z komunikatem). "
                    "Jeśli nie zdążysz go wcisnąć zostaniesz wylogowany.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def update_lcd_numbers(self, val1, val2, val3):
        engine_speed = self.engine_speed_progressBar.value()
        fan_speed = self.fan_speed_progressBar.value()
        production_speed = self.production_line_speed_progressBar.value()

        new_engine_temp = self.engine_temp_lcdNumber.value() + \
            (engine_speed + 22 - self.engine_temp_lcdNumber.value()) * 0.1 - fan_speed * 0.03 \
            + val1
        if new_engine_temp < 18:
            new_engine_temp = 18
        self.engine_temp_lcdNumber.setProperty(
            "value", new_engine_temp
        )

        new_load = self.production_line_load_lcdNumber.value() +\
            (production_speed - self.production_line_load_lcdNumber.value()) * 0.1\
            + val2
        if new_load < 0:
            new_load = 0
        elif new_load > 100:
            new_load = 100
        elif production_speed == 0:
            new_load = 0
        self.production_line_load_lcdNumber.setProperty(
            "value", new_load
        )

        new_cooling_temp = self.cooling_system_temp_lcdNumber.value() + \
            (fan_speed - (self.cooling_system_temp_lcdNumber.value() - 22)) * 0.1 + val3

        if new_cooling_temp < 22:
            new_cooling_temp = 22
        self.cooling_system_temp_lcdNumber.setProperty(
            "value", new_cooling_temp
        )
        self.check_production_state_for_warnings()

    def start_process_simulation(self):
        self.start_pushButton.setEnabled(False)
        self.stop_pushButton.setEnabled(True)
        self.worker_production._isRunning = True

    def start_measure_activity(self):
        self.worker_activity.last_activity = time.time()
        self.worker_activity._isRunning = True

    def stop_process_simulation(self):
        self.start_pushButton.setEnabled(True)
        self.stop_pushButton.setEnabled(False)
        self.fan_speed_ScrollBar.setProperty('value', 0)
        self.engine_speed_ScrollBar.setProperty('value', 0)
        self.production_line_speed_ScrollBar.setProperty('value', 0)

    def check_production_state_for_warnings(self):
        for dict in self.warnings_dict:
            if dict.value() > self.warnings_dict[dict]['too high']:
                dict.setStyleSheet('background-color: red')
                self.lcd_numbers_to_labels_dict[dict].setText('Uwaga! Terperatura za wysoka')

            elif dict.value() > self.warnings_dict[dict]['high']:
                dict.setStyleSheet('background-color: orange')
                self.lcd_numbers_to_labels_dict[dict].setText('Wysoka temperatura')

            elif dict.value() > self.warnings_dict[dict]['above normal']:
                dict.setStyleSheet('background-color: yellow')
                self.lcd_numbers_to_labels_dict[dict].setText('Temperatura powyżej normalnej')

            else:
                dict.setStyleSheet('background-color: white')
                self.lcd_numbers_to_labels_dict[dict].setText('Temperatura w normie')

    def confirm_operator_presence(self):
        self.operator_presence_time_lcdNumber.setProperty("value", 20)
        self.operator_presence_time_lcdNumber.show()
        self.operator_presence_check_label.show()
        self.operator_presence_check_pushButton.show()

        self.thread_timer = QThread(parent=self)
        self.worker_timer = Worker()
        self.worker_timer.moveToThread(self.thread_timer)
        self.thread_timer.started.connect(self.worker_timer.start_timer)
        self.thread_timer.start()
        self.worker_timer.second_passed.connect(
            lambda: self.update_timer()
        )
        self.worker_timer.logout.connect(
            lambda: self.operator_is_present()
        )
        self.worker_timer.logout.connect(
            lambda: self.operator_log_out()
        )
        self.worker_timer.finished.connect(self.thread_timer.quit)
        self.worker_timer.finished.connect(self.worker_timer.deleteLater)
        self.thread_timer.finished.connect(self.thread_timer.deleteLater)
        self.worker_timer.logout.connect(self.thread_timer.quit)
        self.worker_timer.logout.connect(self.worker_timer.deleteLater)

    def operator_is_present(self):
        self.worker_timer.is_operator_active = True
        self.worker_activity.last_activity = time.time()
        self.setStyleSheet('background-color:white')
        self.operator_presence_time_lcdNumber.setProperty("value", 20)
        self.operator_presence_time_lcdNumber.hide()
        self.operator_presence_check_pushButton.hide()
        self.operator_presence_check_label.hide()

    def update_timer(self):
        self.operator_presence_time_lcdNumber.setProperty("value", self.operator_presence_time_lcdNumber.value() - 1)
        if self.operator_presence_time_lcdNumber.value() < 10:
            if 'red' in self.styleSheet():
                self.setStyleSheet('background-color:white')
            else:
                self.setStyleSheet('background-color:red')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    log_window = Login()
    control_panel = ControlPanel()
    log_window.show()
    sys.exit(app.exec_())
