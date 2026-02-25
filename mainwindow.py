import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox

import config
import geocoder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("maps.ui", self)
        self.label = self.Map_itself

        self.marker_coords = (config.DEFAULT_LON, config.DEFAULT_LAT)

        self.lineEdit.setText(str(config.DEFAULT_LAT))
        self.lineEdit_2.setText(str(config.DEFAULT_LON))
        self.horizontalSlider.setRange(0, 21)
        self.horizontalSlider.setValue(config.DEFAULT_ZOOM)

        self.checkBox_2.stateChanged.connect(self.update_map)
        self.horizontalSlider.valueChanged.connect(self.update_map)
        self.pushButton_2.clicked.connect(self.set_marker_and_show)

        self.pushButton.clicked.connect(self.search_object)
        self.lineEdit_3.returnPressed.connect(self.search_object)

        self.lineEdit.textChanged.connect(self.update_map)
        self.lineEdit_2.textChanged.connect(self.update_map)

        self.update_map()

    def show_map(self, center_coords, zoom, theme, marker_coords):
        size = "250,250"
        map_type = "map"
        url = "https://static-maps.yandex.ru/v1"
        params = {
            "ll": center_coords,
            "z": zoom,
            "size": size,
            "l": map_type,
            "pt": f"{marker_coords[0]},{marker_coords[1]},pm2rdl",
            "theme": theme,
            "apikey": config.STATIC_API_KEY
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.label.setPixmap(pixmap)
        except Exception as e:
            print("Ошибка загрузки карты:", e)

    def update_map(self):
        try:
            lon = float(self.lineEdit_2.text().strip())
            lat = float(self.lineEdit.text().strip())
            lon, lat = self.normalize_coords(lon, lat)
            center_coords = f"{lon},{lat}"
            zoom = self.horizontalSlider.value()
            theme = "dark" if self.checkBox_2.isChecked() else "light"
            self.show_map(center_coords, zoom, theme, self.marker_coords)
        except ValueError:
            pass

    def set_marker_and_show(self):
        try:
            lon = float(self.lineEdit_2.text().strip())
            lat = float(self.lineEdit.text().strip())
            lon, lat = self.normalize_coords(lon, lat)
            self.marker_coords = (lon, lat)
            self.update_map()
        except ValueError:
            pass

    def search_object(self):
        query = self.lineEdit_3.text().strip()
        if not query:
            return

        result = geocoder.search_object(query, config.GEOCODER_API_KEY)
        if result is None:
            QMessageBox.information(self, "Результат", "Ничего не найдено или ошибка запроса")
            return

        lon, lat = result
        lon, lat = self.normalize_coords(lon, lat)

        self.lineEdit_2.setText(str(lon))
        self.lineEdit.setText(str(lat))
        self.marker_coords = (lon, lat)
        self.update_map()

    def keyPressEvent(self, event):
        try:
            lon = float(self.lineEdit_2.text().strip())
            lat = float(self.lineEdit.text().strip())

            if event.key() == Qt.Key.Key_6:
                lon += 0.06
            elif event.key() == Qt.Key.Key_4:
                lon -= 0.06
            elif event.key() == Qt.Key.Key_8:
                lat += 0.044
            elif event.key() == Qt.Key.Key_2:
                lat -= 0.044
            else:
                return

            lon, lat = self.normalize_coords(lon, lat)
            self.lineEdit_2.setText(str(lon))
            self.lineEdit.setText(str(lat))
        except ValueError:
            pass

    @staticmethod
    def normalize_coords(lon, lat):
        if lat < -90:
            lat = -90
        elif lat > 90:
            lat = 90
        if lon < -180:
            lon = -180
        elif lon > 180:
            lon = 180
        return lon, lat