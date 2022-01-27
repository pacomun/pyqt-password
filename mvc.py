"""Documentación del módulo

"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem


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


app = QApplication(sys.argv)


tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Claves", "ruta"])
tree.header().setDefaultSectionSize(300)

items = []
for value in lst_leida:
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

tree.insertTopLevelItems(0, items)

tree.show()
sys.exit(app.exec())
