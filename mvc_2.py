"""Documentación del módulo

"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                             QWidget, QTreeView, QVBoxLayout)
from PyQt5.QtGui import QStandardItemModel, QStandardItem

ALMACEN = '/home/pacomun/tmp/password-store'


def leer_almacen(ruta):
    """Guardamos en una lísta los archivo del almacén."""
    if not os.path.exists(ruta):
        raise ValueError('La ruta no existe', ruta)
    listado = []
    for archivo in os.scandir(ruta):
        if not archivo.name.startswith('.') and not archivo.name.startswith('_'):
            if archivo.is_file():
                listado.append(archivo)
            elif archivo.is_dir():
                carpeta = leer_almacen(archivo.path)
                carpeta.insert(0, archivo)
                listado.append(carpeta)

    return listado


lst_leida = leer_almacen(ALMACEN)


def desplegar_ruta(listado):
    """Imprime la lista en formato adecuado."""
    for elemento in listado:
        if isinstance(elemento, list):
            for sub_elem in elemento[1:]:
                print(elemento[0].name, '->', sub_elem.name.removesuffix('.gpg'))
        else:
            print(elemento.name.removesuffix('.gpg'))


desplegar_ruta(lst_leida)


class View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tree = QTreeView(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        # Aquí creo el modelo para gestionar los datos.
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Passwords', 'Ruta'])
        self.tree.header().setDefaultSectionSize(300)
        self.tree.setModel(self.model)
        self.importar_datos(lst_leida)

    def importar_datos(self, datos, root=None):
        self.model.setRowCount(1)
        if root is None:
            root = self.model.invisibleRootItem()
            root.setSelectable(False)
        for dato in datos:
            if isinstance(dato, list):
                carpeta = QStandardItem(dato[0].name)
                root.appendRow([carpeta,
                                QStandardItem(dato[0].path)])
                for hijo in dato[1:]:
                    carpeta.appendRow([QStandardItem(hijo.name.removesuffix('.gpg')),
                                       QStandardItem(hijo.path)])
            else:
                root.appendRow([QStandardItem(dato.name.removesuffix('.gpg')),
                                QStandardItem(dato.path)])


app = QApplication(sys.argv)
win = View()
win.setGeometry(600, 200, 800, 400)
win.show()

sys.exit(app.exec())
