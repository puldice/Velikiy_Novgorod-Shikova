import sys, requests

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from io import BytesIO
from PIL import Image


class MapSearcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.searchButton.clicked.connect(self.run)

    def run(self):
        self.getImage()

    def getImage(self):
        api_server = "https://static-maps.yandex.ru/v1"
        lon = self.lon.text()
        lat = self.lat.text()
        delta1 = str(float(self.spn.text()))
        delta2 = str(float(self.spn.text()))
        apikey = "5815d7d2-6bbe-424d-a32d-028b8c596fa2"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta1, delta2]),
            "apikey": apikey,
        }
        response = requests.get(api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapSearcher()
    ex.show()
    sys.exit(app.exec())