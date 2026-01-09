import sys
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Notes Editor")
        # self.setFixedSize(QSize(800, 500))
        layout = QGridLayout()

        self.label = QLabel("Text of Notes:")
        self.input = QLineEdit()
        self.btn_image = QPushButton("Import Image")
        self.btn_save = QPushButton("Save Notes")
        self.widget = QLabel("Image")
        self.btn_image.clicked.connect(self.add_image)
        self.btn_save.clicked.connect(self.save_notes)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.input, 0, 1, 1, 2)
        layout.addWidget(self.btn_image, 1, 0)
        layout.addWidget(self.btn_save, 1, 1)
        layout.addWidget(self.widget, 2, 0, 2, 3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_notes(self):
        QMessageBox.information(self, "Information", "Your file has been saved.")

    def add_image(self):
        self.img_path = QFileDialog.getOpenFileName(self, "Select a File",
                                                os.path.expanduser("~"),
                                                "Images (*.png *.jpg)")[0]
        if self.img_path:
            pixmap = QPixmap(self.img_path)
            pixmap = pixmap.scaledToWidth(400)
            self.widget.setPixmap(pixmap)
            QMessageBox.information(self, "Image", "Your image has been loaded.")
        else:
            self.widget.setText("Not Image")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()