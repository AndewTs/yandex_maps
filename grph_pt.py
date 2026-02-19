import sys
import requests

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("maps.ui", self)
        self.label = self.Map_itself
        self.lineEdit.setText("55.7558")
        self.lineEdit_2.setText("37.6176")
        self.horizontalSlider.setRange(0, 21)
        self.horizontalSlider.setValue(12)
        self.horizontalSlider.valueChanged.connect(self.update_map)
        self.pushButton_2.clicked.connect(self.update_map)
        self.update_map()

    def show_map(self, coords, zoom):
        size = "250,250"
        map_type = "map"
        url = (
            f"https://static-maps.yandex.ru/1.x/?ll={coords}"
            f"&z={zoom}&size={size}&l={map_type}&pt={coords},pm2rdl"
        )
        response = requests.get(url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.label.setPixmap(pixmap)

    def update_map(self):
        lon = self.lineEdit_2.text().strip()
        lat = self.lineEdit.text().strip()
        coords = f"{lon},{lat}"
        zoom = self.horizontalSlider.value()
        self.show_map(coords, zoom)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_6:
            lon = float(self.lineEdit_2.text().strip()) + 0.06
            lat = float(self.lineEdit.text().strip())

            lon, lat = self.normalize_coords(lon, lat)
            self.lineEdit_2.setText(str(lon))
            self.lineEdit.setText(str(lat))
            self.update_map()

        if event.key() == Qt.Key.Key_4:
            lon = float(self.lineEdit_2.text().strip()) - 0.06
            lat = float(self.lineEdit.text().strip())

            lon, lat = self.normalize_coords(lon, lat)
            self.lineEdit_2.setText(str(lon))
            self.lineEdit.setText(str(lat))
            self.update_map()

        if event.key() == Qt.Key.Key_8:
            lon = float(self.lineEdit_2.text().strip())
            lat = float(self.lineEdit.text().strip()) + 0.044

            lon, lat = self.normalize_coords(lon, lat)
            self.lineEdit_2.setText(str(lon))
            self.lineEdit.setText(str(lat))
            self.update_map()

        if event.key() == Qt.Key.Key_2:
            lon = float(self.lineEdit_2.text().strip())
            lat = float(self.lineEdit.text().strip()) - 0.044

            lon, lat = self.normalize_coords(lon, lat)
            self.lineEdit_2.setText(str(lon))
            self.lineEdit.setText(str(lat))
            self.update_map()

    def normalize_coords(self, lon, lat):
        if lat < -90:
            lat = -90
        elif lat > 90:
            lat = 90
        if lon < -180:
            lon = -180
        elif lon > 180:
            lon = 180
        return lon, lat


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
