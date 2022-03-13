"""Aplicación que gestiona archivos cifrados de un almacén de claves
compatible con el programa PASS de Unix.


"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QWidget, QPushButton,
                             QHBoxLayout, QMessageBox)
from .helpGit.dialogos import (DialogEdit, DialogModificar, DialogoRenombra,
                              DialogoConfig, DialogoPassword)
from .helpGit.helpgnupg import (descifrar_archivo, subir_al_servidor,
                               traer_del_servidor, hacer_commit)
from .helpGit.configuracion import cfg_inicial, read_cfg


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
        """Guardamos en una lísta los archivo del almacén. Esa función debo rescribirla
        de forma recursiva para que lea cualquier nivel de profundidad. Ahora
        sólo lee un nivel de directorio.

        """
        if not os.path.exists(ruta):
            raise ValueError('La ruta no existe', ruta)
        listado = []
        for archivo in os.scandir(ruta):
            if (not archivo.name.startswith('.')
                    and not archivo.name.startswith('_')):
                if archivo.is_file():
                    listado.append(archivo)
                elif archivo.is_dir():
                    carpeta = []
                    for sub_carpeta in os.scandir(archivo):
                        if (not sub_carpeta.name.startswith('.')
                                and not sub_carpeta.name.startswith('_')):
                            if sub_carpeta.is_file():
                                carpeta.append(sub_carpeta)
                    carpeta.insert(0, archivo)
                    listado.append(carpeta)
        return listado

    def seleccion(self, index):
        """Actualiza self.selected al cambiar la selección"""
        if __debug__:
            print(index.data())
            print(index.sibling(index.row(), 1).data())
        self.selected = index.sibling(index.row(), 1).data()

    def doble_clicked(self, item, fila):
        """Hará algo al hacer doble click en la fila."""
        if not __debug__:
            print('Padre', item.text(fila))
            print('Texto: ', item.text(1))
        if not Path(item.text(1)).is_dir():
            dialogo_pass = DialogoPassword('Password', self)
            if dialogo_pass.exec_() == DialogoPassword.Accepted:
                password = dialogo_pass.get_output()
            else:
                return
            contenido = descifrar_archivo(item.text(1), password=password)
            password = ''  # limpio password
            dialogo = QMessageBox()
            dialogo.setContentsMargins(50, 50, 15, 15)
            dialogo.setIcon(QMessageBox.Information)
            QApplication.clipboard().setText(contenido[0])
            if len(contenido) > 1:
                texto = '\n'.join(contenido[1:])
                dialogo.setInformativeText(texto)
            dialogo.setWindowTitle(item.text(fila))
            dialogo.setText(contenido[0])
            dialogo.exec()
            QApplication.clipboard().setText('')

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
            try:
                dialogo_modificar = DialogModificar(self.selected,
                                                    "Modificar Ĉlave",
                                                    self, almacen)
                dialogo_modificar.exec_()
            except ValueError:
                print("No se ha introducido la clave para descifrar")
        elif Path(self.selected):
            dialogo_carpeta = DialogoRenombra(title='Renombrar Carpeta',
                                              carpeta=self.selected,
                                              parent=self)
            dialogo_carpeta.exec_()
        self.actualizar_datos()

    def boton_subir(self):
        """Realiza commit y sube los cambios al servidor Git"""
        hacer_commit()
        salida_push = subir_al_servidor()
        aviso = QMessageBox()
        if salida_push.returncode == 0:
            aviso.setIcon(QMessageBox.Information)
            aviso.setText('Subida realizada con éxito')
        else:
            aviso.setIcon(QMessageBox.Warning)
            aviso.setText(f'Error: código {salida_push.returncode}')
        aviso.exec()

    def boton_baja(self):
        """Realiza 'Push' al servidor y actualiza los datos"""
        bajada_pull = traer_del_servidor()
        aviso = QMessageBox()
        if bajada_pull.returncode == 0:
            aviso.setIcon(QMessageBox.Information)
            aviso.setText('Bajada realizada con éxito')
        else:
            aviso.setIcon(QMessageBox.Warning)
            aviso.setText(f'Error: códiogo {bajada_pull.returncode}')
        aviso.exec()
        self.actualizar_datos()


def main():
    """Función principal para desplegar aplicación."""
    app = QApplication(sys.argv)
    dic_cfg = cfg_inicial()
    config = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'config':
            config = True
    if not os.path.exists(dic_cfg['pypass_cfg']) or config:
        win_cfg = DialogoConfig('Configuración')
        win_cfg.exec()

    dic_cfg = read_cfg(dic_cfg['pypass_cfg'])
    win = Visor(dic_cfg['password_store'])
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
