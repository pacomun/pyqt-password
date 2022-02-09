"""Implementación de Widgets diálogos personalizados.

"""
import sys
from pathlib import Path
from helpGit import helpgnupg, configuracion
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QPushButton, QLabel,
                             QLineEdit, QComboBox, QGridLayout,
                             QHBoxLayout, QApplication, QMenu,
                             QTextEdit, QVBoxLayout)


class DialogEdit(QDialog):
    """Ventana de diálogo para editar datos de la
    aplicación. Parámetros:
    title: una cadena para el título de la ventana.
    parent: Widget padre.
    values: una lista devuelta por la lectura del
    directorio de trabajo.

    """
    def __init__(self, title, parent=None, values=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        if values is None:
            values = []
        self.values = values
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.addItems(self.get_carpetas())
        self.le_nombre = QLineEdit()
        self.le_password = QLineEdit()
        self.b_generar = QPushButton('Generar')
        self.b_generar.clicked.connect(self.generar)
        self.text_edit = QTextEdit(self)
        self.b_aceptar = QPushButton('Aceptar')
        self.b_aceptar.clicked.connect(self.boton_aceptar)
        self.b_cancelar = QPushButton('Cancelar')
        self.b_cancelar.clicked.connect(self.close)

        grid = QGridLayout(self)
        grid.setSpacing(10)
        hbox = QHBoxLayout()
        grid.addWidget(QLabel('Carpeta: '), 0, 0)
        grid.addWidget(self.combo, 0, 1)
        grid.addWidget(QLabel('Nombre: '), 1, 0)
        grid.addWidget(self.le_nombre, 1, 1)
        grid.addWidget(QLabel("password: "), 2, 0)
        grid.addWidget(self.le_password, 2, 1)
        grid.addWidget(self.b_generar, 2, 2)
        grid.addWidget(self.text_edit, 3, 0, 1, 3)
        hbox.addStretch(1)
        hbox.addWidget(self.b_aceptar)
        hbox.addWidget(self.b_cancelar)
        grid.addLayout(hbox, 4, 1)
        self.setContentsMargins(15, 20, 15, 20)

    def get_carpetas(self):
        """Extrae de values una lista con carpetas."""
        lstcarpetas = ['']
        for value in self.values:
            if isinstance(value, list):
                lstcarpetas.append(value[0].name)
        return lstcarpetas

    def generar(self):
        """Generamos password y cumplimentamos la entrada."""
        password = helpgnupg.generador()
        self.le_password.setText(password)

    def boton_aceptar(self):
        """Recuperar datos cumplimentados. Si todo va bien, se guarda
        el archivo cifrado"""
        if __debug__:
            print('carpeta: ', self.combo.lineEdit().text())
            print('nombre: ', self.le_nombre.text())
            print('password: ', self.le_password.text())
            print('datos extra: ', self.text_edit.toPlainText())
        datos = [self.combo.lineEdit().text(),
                 self.le_nombre.text(),
                 self.le_password.text(),
                 self.text_edit.toPlainText()]
        archivo = helpgnupg.guardar_archivo(datos)
        helpgnupg.cifrar_archivo(archivo)
        self.accept()


class DialogModificar(DialogEdit):
    """Clase derivada de DialogoEdit para modificar una clave."""
    def __init__(self, archivo, title, parent=None, values=None ):
        super().__init__(title=title, parent=parent, values=values)
        self.archivo = Path(archivo)
        self.datos_iniciales = self.get_datos()
        self.combo.lineEdit().setText(self.datos_iniciales[0])
        self.le_nombre.setText(self.datos_iniciales[1])
        self.le_password.setText(self.datos_iniciales[2])
        self.text_edit.setText(self.datos_iniciales[3])

    def get_datos(self) -> list:
        """Devuelve lista con los siguiente valores: carpeta,
        nombre, password, y datos extra.

        """
        carpeta = self.archivo.parents[0].name
        if carpeta == Path.cwd().name:
            carpeta = ''
        nombre = self.archivo.stem
        lst_contenido = helpgnupg.descifrar_archivo(self.archivo)
        if len(lst_contenido) > 1:
            datos_extra = '\n'.join(lst_contenido[1:])
        else:
            datos_extra = ''
        password = lst_contenido[0]

        return [carpeta, nombre, password, datos_extra]

    def boton_aceptar(self):
        """Redefinición del método para poder borrar archivo
        modificado si procede"""
        datos = [self.combo.lineEdit().text(),
                 self.le_nombre.text(),
                 self.le_password.text(),
                 self.text_edit.toPlainText()]
        archivo = helpgnupg.guardar_archivo(datos)
        helpgnupg.cifrar_archivo(archivo)

        # Borrar archivo si se renombra o cambia ubicación
        if datos[:2] != self.datos_iniciales[:2]:
            Path(self.archivo).unlink()
        self.accept()


class DialogoRenombra(QDialog):
    """Ventana de diálogo para renombrar una carpeta. Recibe como argumentos:
    parent: Widget padre.
    title: título de la ventana.
    carpeta: cadena con la ruta de la carpeta a renombrar.
    """
    def __init__(self, title, carpeta, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.carpeta = Path(carpeta)
        label = QLabel('Edita Nombre de la carpeta: ')
        self.qline_edit = QLineEdit()
        self.qline_edit.setText(self.carpeta.name)
        boton_aceptar = QPushButton('Aceptar')
        boton_aceptar.clicked.connect(self.aceptar)
        boton_cancelar = QPushButton('Cancelar')
        boton_cancelar.clicked.connect(self.reject)
        vbox = QVBoxLayout(self)
        hbox_top = QHBoxLayout()
        hbox_bottom = QHBoxLayout()

        hbox_top.addWidget(label)
        hbox_top.addWidget(self.qline_edit)
        vbox.addLayout(hbox_top)
        hbox_bottom.addWidget(boton_aceptar)
        hbox_bottom.addWidget(boton_cancelar)
        vbox.addLayout(hbox_bottom)

    def aceptar(self):
        """Acción para el botón aceptar."""
        nuevo_nombre = self.qline_edit.text()
        nombre = self.carpeta.name
        if nuevo_nombre != nombre:
            nuevo_nombre = self.carpeta.with_name(nuevo_nombre)
            self.carpeta.replace(nuevo_nombre)
        self.accept()


class DialogoConfig(QDialog):
    """Documentar..."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(600, 400, 800, 300)
        self.d_cfg = configuracion.cfg_inicial()
        if Path(self.d_cfg['pypass_cfg']).exists():
            self.d_cfg = configuracion.read_cfg(self.d_cfg['pypass_cfg'])
        self.le_user = QLineEdit()
        self.le_editor = QLineEdit()
        self.le_home = QLineEdit()
        self.le_password_store = QLineEdit()
        self.le_keyid = QLineEdit()
        self.le_os = QLineEdit()
        self.le_pypass_cfg = QLineEdit()
        self.boton_aceptar = QPushButton('Aceptar')
        self.boton_aceptar.clicked.connect(self.aceptar)
        self.empaquetado()

    def empaquetado(self):
        """Empaquetado de etiqueta y Líneas de edición."""
        grid = QGridLayout(self)
        label1 = QLabel('Usuario: ')
        grid.addWidget(label1, 0, 0)
        self.le_user.setText(self.d_cfg['user'])
        self.le_user.setReadOnly(True)
        grid.addWidget(self.le_user, 0, 1)
        label2 = QLabel('Editor: ')
        grid.addWidget(label2, 1, 0)
        self.le_editor.setText(self.d_cfg['editor'])
        grid.addWidget(self.le_editor, 1, 1)
        label3 = QLabel('HOME: ')
        grid.addWidget(label3, 2, 0)
        self.le_home.setText(self.d_cfg['home'])
        self.le_home.setReadOnly(True)
        grid.addWidget(self.le_home, 2, 1)
        label4 = QLabel('Almacén de Claves: ')
        grid.addWidget(label4, 3, 0)
        self.le_password_store.setText(self.d_cfg['password_store'])
        grid.addWidget(self.le_password_store, 3, 1)
        label5 = QLabel('keyid: ')
        grid.addWidget(label5, 4, 0)
        self.le_keyid.setText(self.d_cfg['keyid'])
        grid.addWidget(self.le_keyid, 4, 1)
        label6 = QLabel('Sistema Operativo: ')
        grid.addWidget(label6, 5, 0)
        self.le_os.setText(self.d_cfg['os'])
        self.le_os.setReadOnly(True)
        grid.addWidget(self.le_os, 5, 1)
        label7 = QLabel('Archivo de Configuración: ')
        grid.addWidget(label7, 6, 0)
        self.le_pypass_cfg.setText(self.d_cfg['pypass_cfg'])
        self.le_pypass_cfg.setReadOnly(True)
        grid.addWidget(self.le_pypass_cfg, 6, 1)
        boton_cancelar = QPushButton('Cancelar')
        boton_cancelar.clicked.connect(self.reject)
        hbox = QHBoxLayout()
        hbox.addWidget(self.boton_aceptar)
        hbox.addWidget(boton_cancelar)
        hbox.setContentsMargins(20, 10, 10, 10)
        grid.addLayout(hbox, 7, 1, 2, 1, Qt.AlignVCenter)

    def aceptar(self):
        """Acción para botón Aceptar: recoge los datos en el diccionario y
        guarda la configuración."""
        self.d_cfg['editor'] = self.le_editor.text()
        self.d_cfg['password_store'] = self.le_password_store.text()
        self.d_cfg['keyid'] = self.le_keyid.text()

        print(self.d_cfg)
        configuracion.write_cfg(**self.d_cfg)
        self.accept()
