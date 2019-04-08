from mymapapi import *
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
 
W = 400
H = 500
dMenu = 50
m = 10 #отступ
map_w, map_h = W -2 * m, (H - dMenu - 2 * m)-50


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.sz = 8
        self.m_type = 'sat'
        self.s1 = "55.7507"
        self.s2 = "37.6256"
        self.matka = None
        self.initUI()
 
    def initUI(self):
        self.setGeometry(100, 100, W, H)
        self.setWindowTitle('Карта')

        self.maps = "one.png"
        
        self.label = QLabel(self)
        self.label.setText("Измените масштаб:")
        self.label.move(300, 10)
        
        self.btn = QPushButton('+', self)
        self.btn.setFocusPolicy(0)
        self.btn.resize(23, 23)
        self.btn.move(373, 29)
        self.btn.clicked.connect(self.cp)
        
        self.btn = QPushButton('-', self)
        self.btn.setFocusPolicy(0)
        self.btn.resize(23, 23)
        self.btn.move(347, 29) 
        self.btn.clicked.connect(self.cm)
 
        self.label = QLabel(self)
        self.label.setText("Введите координаты центра карты:")
        self.label.move(10, 10)
 
        self.lat_input = QLineEdit(self)
        self.lat_input.setFocusPolicy(2)
        self.lat_input.setText("55.7507")
        self.lat_input.move(10, 30)
        
        self.lon_input = QLineEdit(self)
        self.lon_input.setFocusPolicy(2)
        self.lon_input.setText("37.6256")
        self.lon_input.move(W //3 * 1, 30)
        
        self.btn = QPushButton('Отобразить', self)
        self.btn.setFocusPolicy(0)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(W //3 * 2, 29)
        self.btn.clicked.connect(self.show_map_file)

        self.pixmap = QPixmap(self.maps)
        self.lbl = QLabel(self)
        self.lbl.setFocusPolicy(0)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(m , m + dMenu, map_w, map_h)
        self.lbl.move(10, 60)
        
        self.combo = QComboBox(self)
        self.combo.resize(90, 25)
        self.combo.addItems(["схема", "спутник", 'гибрид'])
        self.combo.move(W // 2, 4)
        self.combo.activated[str].connect(self.onActivated)
        self.combo.setFocusPolicy(0)
        
        self.poisk = QLineEdit(self)
        self.poisk.setFocusPolicy(2)
        self.poisk.move(10, 450)  
        self.poisk.resize(200, 21)
        
        self.btn = QPushButton('Поиск', self)
        self.btn.setFocusPolicy(0)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(W //3 * 1.6, 449)
        self.btn.clicked.connect(self.find)
         
        self.count = 0
        
        self.show_map_file()
        
    def find(self):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(self.poisk.text())
 
        response = None
        response = requests.get(geocoder_request)
        if response:
            
            json_response = response.json()
            
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.s1, self.s2 = toponym_coodrinates.split()
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        self.matka = True
        
        self.show_map_file()
    
    def onActivated(self, text):
        d = {"спутник":"sat", "схема":"map", 'гибрид':'skl'}
        if text in d:
            self.m_type = d[text]
        
    def show_map_file(self):
        if self.sender() and self.sender().text() == 'Отобразить':
            self.s1 = self.lat_input.text()
            self.s2 = self.lon_input.text()
        # Показать карту
        lon = self.s1
        lat = self.s2
            
        map_locations = "ll=" + ",".join([lon,lat])# + "&spn=1.0,1.+-0"
                    
        map_type = self.m_type
        if self.matka:
            map_param = "z={}&size=400,400&pt={},{}".format(self.sz, self.s1, self.s2)
        else:
            map_param = "z={}&size=400,400".format(self.sz)
        f_name = get_file_map(map_locations, map_type,map_param)
        if f_name:
            self.maps = f_name
            
        self.pixmap.load(self.maps)
        self.lbl.setPixmap(self.pixmap)
        self.matka = False
    
    def cm(self): #ужасное решение ну ладно
        if 1 < self.sz:
            self.sz -= 1
            self.show_map_file()
    
    def cp(self):
        if self.sz < 17:
            self.sz += 1
            self.show_map_file()

    def keyPressEvent(self, event):
        if self.lat_input.hasFocus():
            self.lat_input.clearFocus()
        if self.lon_input.hasFocus():
            self.lon_input.clearFocus()
        if self.poisk.hasFocus():
            self.poisk.clearFocus()
        if event.key() == QtCore.Qt.Key_PageDown:
            self.cm()
        if event.key() == QtCore.Qt.Key_PageUp:
            self.cp()
        if event.key() == QtCore.Qt.Key_Up:
            self.s2 = str(float(self.s2) + 8/self.sz)
            self.lon_input.setText(self.s2)
            self.show_map_file()
        if event.key() == QtCore.Qt.Key_Down:
            self.s2 = str(float(self.s2) - 8/self.sz)
            self.lon_input.setText(self.s2)
            self.show_map_file()
        if event.key() == QtCore.Qt.Key_Right:
            self.s1 = str(float(self.s1) + 8/self.sz)
            self.lat_input.setText(self.s1)
            self.show_map_file()
        if event.key() == QtCore.Qt.Key_Left:
            self.s1 = str(float(self.s1) - 8/self.sz)
            self.lat_input.setText(self.s1)
            self.show_map_file()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
