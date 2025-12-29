import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("MyApp")
        self.button_is_checked = True

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        # self.button.clicked.connect(self.button_togled)
        self.button.setChecked(self.button_is_checked)
        self.setFixedSize(QSize(400, 300))
        # button.setFixedSize(QSize(100, 50))
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def button_clicked(self):
        self.button.setText("ClickedOfMe")
        self.button.setEnabled(False)

        self.setWindowTitle("My Oneshot App")

    def button_togled(self, checked):
        self.button_is_checked = checked
        print("Checked?", self.button_is_checked)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()