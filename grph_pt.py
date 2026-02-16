import sys
import requests

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("maps.ui", self)
        self.label = self.Map_itself
        self.lineEdit.setText("55.7558")
        self.lineEdit_2.setText("37.6176")
        self.horizontalSlider.setRange(0, 21)  # Допустимые значения z
        self.horizontalSlider.setValue(12)  # Начальный масштаб
        self.horizontalSlider.valueChanged.connect(self.show_map)
        self.pushButton_2.clicked.connect(self.show_map)
        self.show_map()

    def show_map(self):
        coords = f"{self.lineEdit_2.text().strip()},{self.lineEdit.text().strip()}"
        zoom = self.horizontalSlider.value()
        size = "250,250"
        map_type = "map"

        url = f"https://static-maps.yandex.ru/1.x/?ll={coords}&z={zoom}&size={size}&l={map_type}&pt={coords},pm2rdl"
        response = requests.get(url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
