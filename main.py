import sys
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QPushButton,
    QLabel, QLineEdit, QGridLayout, QFileDialog, QMessageBox,
    QComboBox, QSpinBox
)
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageOps

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_hight = 300
        self.filters = ['null', 'grayscale', 'cutting']

        self.setWindowTitle("Notes Editor")
        self.setFixedSize(QSize(400, 500))
        self.layout_grid = QGridLayout()

        self.label = QLabel("Text of Notes:")
        self.input = QLineEdit()
        self.btn_image = QPushButton("Import Image")
        self.btn_save = QPushButton("Save Notes")
        self.widget = QLabel("Image")
        self.img_filters = QComboBox()
        self.btn_image.clicked.connect(self.add_image)
        self.btn_save.clicked.connect(self.save_notes)
        self.layout_grid.addWidget(self.label, 0, 0)
        self.layout_grid.addWidget(self.input, 0, 1, 1, 3)
        self.layout_grid.addWidget(self.btn_image, 1, 0)
        self.layout_grid.addWidget(self.btn_save, 1, 1)
        self.layout_grid.addWidget(self.widget, 2, 0, 2, 4)

        container = QWidget()
        container.setLayout(self.layout_grid)
        self.setCentralWidget(container)

    def save_notes(self):
        QMessageBox.information(self, "Information", "Your file has been saved.")

    def add_image(self):
        self.img_path = QFileDialog.getOpenFileName(self, "Select a File",
                                                os.path.expanduser("~"),
                                                "Images (*.png *.jpg)")[0]
        if self.img_path:
            self.reset_image()
            self.layout_grid.addWidget(QLabel("Filter: "), 4, 0)
            self.img_filters.addItems(self.filters)
            self.img_filters.currentTextChanged.connect(self.filter_to_image)
            self.layout_grid.addWidget(self.img_filters, 4, 1, 1, 2)
            self.btn_reset = QPushButton("Reset Image")
            self.btn_reset.clicked.connect(self.reset_image)
            self.layout_grid.addWidget(self.btn_reset, 1, 2)
            # QMessageBox.information(self, "Image", "Your image has been loaded.")
        else:
            self.widget.setText("Not Image")

    def render(self, image_path, filter):
        image = Image.open(image_path)
        image = self.image_filter(image, filter)
        image.save(self.tmp_path)
        self.pixmap(self.tmp_path)
        return image

    def reset_image(self):
        self.tmp_path = 'temp/' + os.path.basename(self.img_path)
        image = self.render(self.img_path, None)
        self.img_filters.setCurrentIndex(0)
        self.construct_cutter(image)

    def filter_to_image(self, filter=None):
        self.render(self.tmp_path, filter)

    def pixmap(self, img_path):
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaledToHeight(self.img_hight)
        self.widget.setPixmap(pixmap)

    def construct_cutter(self, image: Image.Image):
        self.spin = {
                    'Left': QSpinBox(),
                    'Up': QSpinBox(),
                    "Down": QSpinBox(),
                    "Right": QSpinBox()
        }
        for i, spin in enumerate(self.spin.keys()):
            self.spin[spin].setMinimum(0)
            self.spin[spin].setMaximum(10000)
            self.layout_grid.addWidget(self.spin[spin], 5, i)

        self.spin["Right"].setValue(image.size[1])
        self.spin["Down"].setValue(image.size[0])
        self.btn_cutt = QPushButton("Cutting")
        self.layout_grid.addWidget(self.btn_cutt, 4, 3)
        self.btn_cutt.clicked.connect(self.cutter)

    def image_filter(self, image: Image.Image, filter):
        match filter:
            case 'grayscale':
                return ImageOps.grayscale(image)
            case 'cutting':
                self.construct_cutter(image)
                return image

        return image

    def cutter(self):
        img_size = tuple(val.value() for val in self.spin.values())
        img_path = 'temp/' + os.path.basename(self.img_path)
        image = Image.open(img_path)
        image = image.crop(box=img_size)
        image.save(img_path)
        self.pixmap(img_path)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()