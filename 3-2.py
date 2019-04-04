from mymapapi import *
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
 
W = 400
H = 450
dMenu = 50
m = 10 #отступ
map_w, map_h = W -2 * m, H - dMenu - 2 * m


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.sz = 8
        self.initUI()
 
    def initUI(self):
        self.setGeometry(100, 100, W, H)
        self.setWindowTitle('Карта')

        self.maps = "one.png"
         
        self.btn = QPushButton('Отобразить', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(W //3 * 2, 29)
        self.btn.clicked.connect(self.show_map_file)
        
        self.label = QLabel(self)
        self.label.setText("Измените масштаб:")
        self.label.move(300, 10)
        
        self.btn = QPushButton('+', self)
        self.btn.resize(20, 20)
        self.btn.move(380, 29)
        self.btn.clicked.connect(self.cp)
        
        self.btn = QPushButton('-', self)
        self.btn.resize(20, 20)
        self.btn.move(350, 29) 
        self.btn.clicked.connect(self.cm)
 
        self.label = QLabel(self)
        self.label.setText("Введите координаты центра карты:")
        self.label.move(10, 10)
 
        self.lat_input = QLineEdit(self)
        self.lat_input.move(10, 30)
        self.lat_input.setText("55.7507")
        self.lon_input = QLineEdit(self)
        self.lon_input.move(W //3 * 1, 30)
        self.lon_input.setText("37.6256")

        self.pixmap = QPixmap(self.maps)
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(m , m + dMenu, map_w, map_h)
        self.lbl.move(10, 60)
         
        self.count = 0
 
    def show_map_file(self):
        # Показать карту
        lon = self.lon_input.text()
        lat = self.lat_input.text()
        
        map_locations = "ll=" + ",".join([lon,lat])# + "&spn=1.0,1.0"
                
        map_type = "sat"
        map_param = "z={}&size=400,400".format(self.sz)
        f_name = get_file_map(map_locations, map_type,map_param)
        if f_name:
            self.maps = f_name
        
        self.pixmap.load(self.maps)
        self.lbl.setPixmap(self.pixmap)
    
    def cm(self):
        self.sz -= 1
        self.show_map_file()
    
    def cp(self):
        self.sz += 1
        self.show_map_file()
        
    def keyPressEvent(self, event):
        
        if 1 < self.sz and event.key() == QtCore.Qt.Key_PageDown:
            self.cm()
        if event.key() == QtCore.Qt.Key_PageUp and self.sz < 18:
            self.cp()  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())