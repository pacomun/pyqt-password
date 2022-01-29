"""Documentación del módulo

"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QWidget)

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


def desplegar_ruta(listado):
    """Imprime la lista en formato adecuado."""
    for elemento in listado:
        if isinstance(elemento, list):
            for sub_elem in elemento[1:]:
                print(elemento[0].name, '->', sub_elem.name.removesuffix('.gpg'))
        else:
            print(elemento.name.removesuffix('.gpg'))


class Visor(QWidget):
    """Clase principal de la aplicación Qt_password"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Contraseñas')
        self.setGeometry(600, 300, 800, 300)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(['Claves', 'ruta'])
        self.tree.header().setDefaultSectionSize(300)
        self.tree.hideColumn(1)
        self.tree.selectionModel().currentChanged.connect(self.seleccion)
        self.importar_datos(lst_leida)
        self.empaquetar_widgets()

    def empaquetar_widgets(self):
        """Empaqueta los widgets en la ventana."""
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)

    def importar_datos(self, datos):
        """Función que carga en el visor los datos de la
        lista pasada como argumento."""
        items = []
        for value in datos:
            if isinstance(value, list):
                item = QTreeWidgetItem([value[0].name,
                                        value[0].path])
                for sub_value in value[1:]:
                    nombre = sub_value.name.removesuffix('.gpg')
                    archivo = sub_value.path
                    child = QTreeWidgetItem([nombre, archivo])
                    item.addChild(child)
                items.append(item)
            else:
                item = QTreeWidgetItem([value.name.removesuffix('.gpg'),
                                        value.path])
                items.append(item)

        self.tree.insertTopLevelItems(0, items)

    def seleccion(self, index):
        print(index.data())
        print(index.sibling(index.row(), 1).data())

if __name__ == '__main__':
    lst_leida = leer_almacen(ALMACEN)
    desplegar_ruta(lst_leida)

    app = QApplication(sys.argv)
    win = Visor()
    win.show()
    sys.exit(app.exec())
