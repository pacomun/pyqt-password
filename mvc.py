"""Documentación del módulo

"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QWidget, QPushButton,
                             QHBoxLayout, QMessageBox)
from helpGit.dialogos import DialogEdit, DialogModificar, DialogoRenombra
from helpGit.helpgnupg import (descifrar_archivo, subir_al_servidor,
                               traer_del_servidor, hacer_commit)

ALMACEN = '/home/pacomun/tmp/password-store'


class Visor(QWidget):
    """Clase principal de la aplicación Qt_password"""
    def __init__(self, almacen, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Contraseñas')
        self.setGeometry(600, 300, 800, 300)
        self.almacen = almacen
        os.chdir(self.almacen)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(['Claves', 'ruta'])
        self.tree.header().setDefaultSectionSize(300)
        self.tree.hideColumn(1)
        self.tree.selectionModel().currentChanged.connect(self.seleccion)
        self.tree.itemDoubleClicked.connect(self.doble_clicked)
        self.actualizar_datos()
        self.empaquetar_widgets()

        self.selected = ''

    def botones_git(self):
        """Crear botones."""
        b_subir_al_servidor = QPushButton("Subir al servidor")
        b_subir_al_servidor.clicked.connect(self.boton_subir)
        b_bajar_del_servidor = QPushButton("Bajar del servidor")
        b_bajar_del_servidor.clicked.connect(self.boton_baja)
        layout_git = QHBoxLayout()
        layout_git.addWidget(b_subir_al_servidor)
        layout_git.addWidget(b_bajar_del_servidor)
        layout_git.addStretch(1)
        return layout_git

    def botones_edicion(self):
        "Crea los botones para editar y devueve la capa."
        b_borrar = QPushButton("Borrar")
        b_borrar.clicked.connect(self.boton_borrar)
        b_editar = QPushButton("Editar")
        b_editar.clicked.connect(self.boton_editar)
        b_nuevo = QPushButton("Nuevo")
        b_nuevo.clicked.connect(self.nueva_password)
        layout_edit = QHBoxLayout()
        layout_edit.addStretch(1)
        layout_edit.addWidget(b_borrar)
        layout_edit.addWidget(b_editar)
        layout_edit.addWidget(b_nuevo)
        return layout_edit

    def empaquetar_widgets(self):
        """Empaqueta los widgets en la ventana."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.addLayout(self.botones_git())
        layout.addWidget(self.tree)
        layout.addLayout(self.botones_edicion())

    def actualizar_datos(self):
        """Función que carga en el visor los datos de la
        lista pasada como argumento."""
        datos = self.leer_almacen(self.almacen)
        items = []
        self.tree.clear()
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

    def leer_almacen(self, ruta):
        """Guardamos en una lísta los archivo del almacén."""
        if not os.path.exists(ruta):
            raise ValueError('La ruta no existe', ruta)
        listado = []
        for archivo in os.scandir(ruta):
            if (not archivo.name.startswith('.')
                    and not archivo.name.startswith('_')):
                if archivo.is_file():
                    listado.append(archivo)
                elif archivo.is_dir():
                    carpeta = self.leer_almacen(archivo.path)
                    carpeta.insert(0, archivo)
                    listado.append(carpeta)
        return listado

    def seleccion(self, index):
        """Hace algo al cambiar la selección"""
        if __debug__:
            print(index.data())
            print(index.sibling(index.row(), 1).data())
        self.selected = index.sibling(index.row(), 1).data()

    def doble_clicked(self, item, fila):
        """Hará algo al hacer doble click en la fila."""
        if __debug__:
            print('Padre', item.text(fila))
            print('Texto: ', item.text(1))
        if not Path(item.text(1)).is_dir():
            contenido = descifrar_archivo(item.text(1))
            dialogo = QMessageBox()
            dialogo.setContentsMargins(50, 50, 15, 15)
            dialogo.setIcon(QMessageBox.Information)
            if len(contenido) > 1:
                texto = '\n'.join(contenido[1:])
                dialogo.setInformativeText(texto)
            dialogo.setWindowTitle(item.text(fila))
            dialogo.setText(contenido[0])
            dialogo.exec()

    def nueva_password(self):
        """Abrimos Diálogo para recibir datos del usuario."""
        almacen = self.leer_almacen(self.almacen)
        dialogo = DialogEdit('Nueva Password',
                             parent=self, values=almacen)
        dialogo.exec_()
        self.actualizar_datos()

    def boton_borrar(self):
        """Borra el archivo seleccionado, con confirmación.
        En caso de carpeta la borrará si está vacía."""
        if self.selected is None:
            return
        archivo_a_borrar = Path(self.selected)
        if archivo_a_borrar.is_file():
            msg = f'¿Quieres borrar definitivamente {archivo_a_borrar.name}?'
            msgebox = QMessageBox()
            msgebox.setIcon(QMessageBox.Warning)
            msgebox.setText(msg)
            msgebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgebox.setDefaultButton(QMessageBox.No)
            msgebox.setEscapeButton(QMessageBox.No)
            res = msgebox.exec()
            if res == QMessageBox.Yes:
                archivo_a_borrar.unlink()
        else:
            try:
                archivo_a_borrar.rmdir()
            except OSError:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText('Para borrar la carpeta tiene que estar vacía')
                msgbox.exec()
        self.actualizar_datos()

    def boton_editar(self):
        """Acción para el botón editar."""
        almacen = self.leer_almacen(self.almacen)
        if self.selected is None:
            return
        if Path(self.selected).is_file():
            dialogo_modificar = DialogModificar(self.selected,
                                                "Modificar Ĉlave",
                                                self, almacen)
            dialogo_modificar.exec_()
        elif Path(self.selected):
            dialogo_carpeta = DialogoRenombra(title='Renombrar Carpeta',
                                              carpeta=self.selected,
                                              parent=self)
            dialogo_carpeta.exec_()
        self.actualizar_datos()

    def boton_subir(self):
        """Realiza commit y sube los cambios al servidor Git"""
        hacer_commit()
        subir_al_servidor()

    def boton_baja(self):
        """Realiza 'Push' al servidor y actualiza los datos"""
        traer_del_servidor()
        self.actualizar_datos()


def main():
    """Función principal para desplegar aplicación."""
    app = QApplication(sys.argv)
    win = Visor(ALMACEN)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
