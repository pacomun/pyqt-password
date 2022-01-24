"""Ejemplo en Qt6 del widget QTableWidget

"""
import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication,
                               QTableWidget,
                               QTableWidgetItem)


colors = [("Rojo", "FF0000"),
          ("Verde", "00FF00"),
          ("Azul", "0000FF"),
          ("Negro", "000000"),
          ("Blanco", "FFFFFF"),
          ("Verde electrico", "#41CD52"),
          ("Azul oscuro", "#222840"),
          ("Amarillo","#F8E56d")
          ]


def get_rgb_from_hex(code):
    """Función que convierte código de color en hexadecimal a
    código RGB"""
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])


app = QApplication(sys.argv)

table = QTableWidget()
table.setRowCount(len(colors))
table.setColumnCount(len(colors[0]) + 1)
table.setHorizontalHeaderLabels(["Nombre", "Code Hex", "Color"])

for i, (name, code) in enumerate(colors):
    item_name = QTableWidgetItem(name)
    item_code = QTableWidgetItem(code)
    item_color = QTableWidgetItem()
    item_color.setBackground(get_rgb_from_hex(code))
    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_code)
    table.setItem(i, 2, item_color)

table.show()
sys.exit(app.exec())
